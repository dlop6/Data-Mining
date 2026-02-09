

import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, List, Optional


def cargar_tipo_normalizado(
    tipo_nombre: str,
    años_rango: Tuple[int, int] = (2009, 2023),
    csv_dir: Optional[Path] = None,
    verbose: bool = True
) -> Tuple[pd.DataFrame, Dict]:
    """
    Carga y normaliza un tipo de dato (defunciones, nacimientos, etc.)
    
    Parametros:
    -----------
    tipo_nombre : str
        Nombre del tipo de dato (ej: 'defunciones', 'nacimientos', 'divorcios')
    años_rango : tuple
        Rango de años a cargar (inicio, fin). Por defecto (2009, 2023)
    csv_dir : Optional[Path]
        Directorio raíz donde están los CSVs
    verbose : bool
        Si True, imprime progreso de carga
    
    Retorna:
    --------
    df_consolidado : pd.DataFrame
        DataFrame con todos los años concatenados (columnas normalizadas a lowercase)
    metadata : dict
        Diccionario con información de carga {año: num_columnas_original}
    """
    if csv_dir is None:
        raise ValueError("csv_dir no puede ser None. Especifica el directorio de los CSVs.")
    
    lista_dfs = []
    metadata = {}
    
    for año in range(*años_rango):
        archivo = csv_dir / f"{año}_{tipo_nombre}.csv"
        
        if not archivo.exists():
            continue
        
        try:
            df = pd.read_csv(archivo, low_memory=False)
            cols_originales = df.columns.tolist()
            
            # Normalizar columnas a lowercase
            df.columns = df.columns.str.lower()
            
            # Agregar año
            df['año'] = año
            
            lista_dfs.append(df)
            metadata[año] = len(cols_originales)
            
            if verbose:
                print(f"✓ {año}: {df.shape[0]:,} filas, {df.shape[1]} columnas")
        
        except Exception as e:
            if verbose:
                print(f"ERROR {año}: {str(e)}")
            continue
    
    if not lista_dfs:
        raise ValueError(f"No se encontraron archivos para {tipo_nombre}")
    
    # Concatenar verticalmente
    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    
    return df_consolidado, metadata


def resumen_carga(
    df: pd.DataFrame,
    tipo_nombre: str,
    metadata: Dict,
    mostrar_columnas: bool = False
) -> None:
    """
    Genera resumen visual de la carga
    
    Parametros:
    -----------
    df : pd.DataFrame
        DataFrame a resumir
    tipo_nombre : str
        Nombre del tipo de dato (para encabezado)
    metadata : dict
        Metadata con información por año
    mostrar_columnas : bool
        Si True, muestra lista de todas las columnas
    """
    print(f"\n{'='*70}")
    print(f"DATASET: {tipo_nombre.upper()}")
    print(f"{'='*70}")
    print(f"Total filas: {df.shape[0]:,}")
    print(f"Total columnas: {df.shape[1]}")
    print(f"Rango años: {df['año'].min()} - {df['año'].max()}")
    print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\nColumnas originales por año:")
    for año in sorted(metadata.keys()):
        print(f"  {año}: {metadata[año]} columnas")
    
    if mostrar_columnas:
        print(f"\nColumnas del dataset consolidado:")
        print(df.columns.tolist())
    
    # Mostrar completitud de datos
    print(f"\nCompletitud de datos (top 5):")
    completitud = df.count().sort_values(ascending=False)
    for col, count in completitud.head(5).items():
        porcentaje = (count / len(df)) * 100
        print(f"  {col:25s}: {count:>10,} ({porcentaje:5.1f}%)")


def consolidar_todos_tipos(
    tipos_lista: List[str],
    años_rango: Tuple[int, int] = (2009, 2023),
    csv_dir: Optional[Path] = None,
    verbose: bool = True
) -> Tuple[Dict, pd.DataFrame]:
    """
    Carga todos los tipos de datos y los consolida en un master dataset
    
    Parametros:
    -----------
    tipos_lista : list
        Lista de tipos a cargar (ej: ['defunciones', 'nacimientos', ...])
    años_rango : tuple
        Rango de años a cargar (inicio, fin)
    csv_dir : Path
        Directorio raíz de los CSVs
    verbose : bool
        Si True, imprime progreso detallado
    
    Retorna:
    --------
    dfs_por_tipo : dict
        Diccionario con estructura:
        {
            'defunciones': {
                'df': DataFrame,
                'metadata': {año: num_cols, ...}
            },
            ...
        }
    master : pd.DataFrame
        Master dataset consolidado con columna 'tipo' identificando la fuente
    """
    if csv_dir is None:
        raise ValueError("csv_dir no puede ser None. Especifica el directorio de los CSVs.")
    
    dfs_por_tipo = {}
    
    print("="*70)
    print("CARGANDO Y NORMALIZANDO TODOS LOS TIPOS")
    print("="*70)
    
    for tipo in tipos_lista:
        try:
            df, metadata = cargar_tipo_normalizado(
                tipo,
                años_rango=años_rango,
                csv_dir=csv_dir,
                verbose=verbose
            )
            
            # Agregar columna identificadora de tipo
            df['tipo'] = tipo
            
            dfs_por_tipo[tipo] = {
                'df': df,
                'metadata': metadata
            }
            
            resumen_carga(df, tipo, metadata, mostrar_columnas=False)
        
        except Exception as e:
            print(f"\nADVERTENCIA: No se pudo cargar {tipo}: {str(e)}\n")
            continue
    
    # Consolidar en master dataset
    print(f"\n{'='*70}")
    print("CONSOLIDANDO MASTER DATASET")
    print(f"{'='*70}")
    
    master = pd.concat(
        [dfs_por_tipo[tipo]['df'] for tipo in dfs_por_tipo.keys()],
        ignore_index=True
    )
    
    print(f"\nMaster dataset:")
    print(f"  Filas totales: {master.shape[0]:,}")
    print(f"  Columnas totales: {master.shape[1]}")
    print(f"  Tipos presentes: {sorted(master['tipo'].unique())}")
    print(f"  Distribución:")
    for tipo in sorted(master['tipo'].unique()):
        count = (master['tipo'] == tipo).sum()
        porcentaje = (count / len(master)) * 100
        print(f"    {tipo:25s}: {count:>10,} ({porcentaje:5.1f}%)")
    
    return dfs_por_tipo, master


def validar_dataset(df: pd.DataFrame, nombre: str = "Dataset") -> Dict:
    """
    Realiza validaciones básicas de calidad de datos
    
    Parametros:
    -----------
    df : pd.DataFrame
        DataFrame a validar
    nombre : str
        Nombre del dataset (para reportes)
    
    Retorna:
    --------
    reporte : dict
        Diccionario con estadísticas de validación
    """
    reporte = {
        'nombre': nombre,
        'filas': len(df),
        'columnas': df.shape[1],
        'columnas_lista': df.columns.tolist(),
        'duplicados_totales': df.duplicated().sum(),
        'nulos_por_columna': df.isnull().sum().to_dict(),
        'tipos_datos': df.dtypes.to_dict(),
    }
    
    print(f"\n{'='*70}")
    print(f"VALIDACIÓN: {nombre}")
    print(f"{'='*70}")
    print(f"Filas: {reporte['filas']:,}")
    print(f"Columnas: {reporte['columnas']}")
    print(f"Filas duplicadas: {reporte['duplicados_totales']:,}")
    print(f"\nColumnas con valores nulos:")
    nulos = {k: v for k, v in reporte['nulos_por_columna'].items() if v > 0}
    if nulos:
        for col, count in sorted(nulos.items(), key=lambda x: x[1], reverse=True)[:5]:
            porcentaje = (count / len(df)) * 100
            print(f"  {col:25s}: {count:>10,} ({porcentaje:5.1f}%)")
    else:
        print("  Ninguna columna con valores nulos")
    
    return reporte


def guardar_dataset(df: pd.DataFrame, ruta_salida: Path, nombre: str = "") -> None:
    """
    Guarda dataset en CSV con confirmación
    
    Parametros:
    -----------
    df : pd.DataFrame
        DataFrame a guardar
    ruta_salida : Path
        Ruta donde guardar el archivo
    nombre : str
        Nombre descriptivo (para mensajes)
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(ruta_salida, index=False)
    tamaño_mb = ruta_salida.stat().st_size / (1024**2)
    
    print(f"\n✓ {nombre} guardado en: {ruta_salida}")
    print(f"  Tamaño: {tamaño_mb:.2f} MB")
