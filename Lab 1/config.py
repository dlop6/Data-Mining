"""
Configuración centralizada del proyecto
Contiene constantes, rutas y parámetros configurables
"""

from pathlib import Path

# Directorio raíz del proyecto (Lab 1)
PROJECT_ROOT = Path(__file__).parent

# Rutas de datos
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_RAW_CSV_DIR = DATA_RAW_DIR / "csv"
DATA_RAW_EXCEL_DIR = DATA_RAW_DIR / "excel"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_INTERIM_DIR = DATA_DIR / "interim"

# Rutas de notebooks
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Rutas de scripts
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Rutas de output
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_FIGURES_DIR = OUTPUT_DIR / "figures"
OUTPUT_TABLES_DIR = OUTPUT_DIR / "tables"
OUTPUT_REPORTS_DIR = OUTPUT_DIR / "reports"

# Constantes del proyecto
AÑOS_INICIO = 2009
AÑOS_FIN = 2023  # Exclusivo (2009-2022 inclusive)
AÑOS_RANGO = (AÑOS_INICIO, AÑOS_FIN)

# Tipos de datos disponibles
TIPOS_DATOS = [
    'defunciones',
    'defunciones_fetales',
    'divorcios',
    'matrimonios',
    'nacimientos'
]

# Parámetros de procesamiento
VERBOSE = True  # Imprimir progreso detallado
RANDOM_STATE = 42  # Seed para reproducibilidad

# Configuración de visualización
FIGURE_DPI = 300  # DPI para exportar figuras
FIGURE_FORMAT = 'png'  # Formato por defecto
SEABORN_STYLE = 'whitegrid'  # Estilo de seaborn
FIGURE_SIZE = (12, 6)  # Tamaño por defecto (ancho, alto)

# Nombres de archivos de salida
MASTER_DATASET_FILENAME = "master_dataset.csv"
DEFUNCIONES_CLEAN_FILENAME = "defunciones_clean.csv"
NACIMIENTOS_CLEAN_FILENAME = "nacimientos_clean.csv"
DIVORCIOS_CLEAN_FILENAME = "divorcios_clean.csv"
MATRIMONIOS_CLEAN_FILENAME = "matrimonios_clean.csv"
DEFUNCIONES_FETALES_CLEAN_FILENAME = "defunciones_fetales_clean.csv"
