
from pathlib import Path
import argparse
import sys
from typing import Dict, List
import pandas as pd
import pyreadstat


# Configuración de rutas relativas al script
SCRIPT_DIR = Path(__file__).parent.parent  # Lab 1/
BASE_DATA_DIR = SCRIPT_DIR / "data"
SAV_SOURCE_DIR = BASE_DATA_DIR / "sav"
CSV_OUTPUT_DIR = BASE_DATA_DIR / "csv"


def convert_sav_to_csv(sav_path: Path, csv_path: Path, verbose: bool = False) -> bool:
    """Convierte un archivo .sav a .csv usando pyreadstat."""
    try:
        df, meta = pyreadstat.read_sav(str(sav_path), apply_value_formats=False)
        assert isinstance(df, pd.DataFrame)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        if verbose:
            print(f"  Convertido: {sav_path.name} → {csv_path.name}")
        return True
    except Exception as e:
        print(f"  Error al convertir {sav_path.name}: {e}")
        return False


def convert_xlsx_to_csv(xlsx_path: Path, csv_path: Path, verbose: bool = False) -> bool:
    """Convierte un archivo .xlsx a .csv usando pandas."""
    try:
        df = pd.read_excel(xlsx_path, engine="openpyxl")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        if verbose:
            print(f"  Convertido: {xlsx_path.name} → {csv_path.name}")
        return True
    except Exception as e:
        print(f"  Error al convertir {xlsx_path.name}: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convertir archivos .sav y .xlsx a .csv de forma recursiva",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo:
    python convertir_sav_xlsx_a_csv.py --verbose
    python convertir_sav_xlsx_a_csv.py --dry-run
        """,
    )
    parser.add_argument("--dry-run", action="store_true", help="Mostrar acciones sin ejecutar")
    parser.add_argument("--verbose", action="store_true", help="Mostrar información detallada")
    args = parser.parse_args()

    # Validar directorios
    if not SAV_SOURCE_DIR.exists():
        print(f"Error: Directorio no encontrado: {SAV_SOURCE_DIR}")
        sys.exit(1)

    # Crear directorio de salida si no existe
    if not args.dry_run:
        CSV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Directorio de salida: {CSV_OUTPUT_DIR}")

    # Buscar todos los archivos .sav y .xlsx
    sav_files = list(SAV_SOURCE_DIR.rglob("*.sav"))
    xlsx_files = list(SAV_SOURCE_DIR.rglob("*.xlsx"))
    
    # Excluir archivos de caché
    sav_files = [f for f in sav_files if "_cache_downloads" not in str(f)]
    xlsx_files = [f for f in xlsx_files if "_cache_downloads" not in str(f)]

    total_files = len(sav_files) + len(xlsx_files)
    if total_files == 0:
        print(f"No se encontraron archivos .sav o .xlsx en {SAV_SOURCE_DIR}")
        return

    print(f"\n{'='*60}")
    print(f"Conversión de archivos a CSV")
    print(f"{'='*60}")
    print(f"Archivos .sav encontrados: {len(sav_files)}")
    print(f"Archivos .xlsx encontrados: {len(xlsx_files)}")
    print(f"Total: {total_files}")

    if args.dry_run:
        print(f"\n[DRY RUN] Se mostrarán las acciones sin ejecutar")

    # Convertir archivos .sav
    if sav_files:
        print(f"\n{'-'*60}")
        print("Procesando archivos .SAV")
        print(f"{'-'*60}")
        success_sav = 0
        for sav_path in sorted(sav_files):
            csv_path = CSV_OUTPUT_DIR / f"{sav_path.stem}.csv"
            
            if args.dry_run:
                print(f"[DRY-RUN] {sav_path.relative_to(SAV_SOURCE_DIR)} → {csv_path.name}")
            else:
                if convert_sav_to_csv(sav_path, csv_path, verbose=args.verbose):
                    success_sav += 1

        if not args.dry_run:
            print(f"\nArchivos .sav convertidos: {success_sav}/{len(sav_files)}")

    # Convertir archivos .xlsx
    if xlsx_files:
        print(f"\n{'-'*60}")
        print("Procesando archivos .XLSX")
        print(f"{'-'*60}")
        success_xlsx = 0
        for xlsx_path in sorted(xlsx_files):
            csv_path = CSV_OUTPUT_DIR / f"{xlsx_path.stem}.csv"
            
            if args.dry_run:
                print(f"[DRY-RUN] {xlsx_path.relative_to(SAV_SOURCE_DIR)} → {csv_path.name}")
            else:
                if convert_xlsx_to_csv(xlsx_path, csv_path, verbose=args.verbose):
                    success_xlsx += 1

        if not args.dry_run:
            print(f"\nArchivos .xlsx convertidos: {success_xlsx}/{len(xlsx_files)}")

    # Resumen
    print(f"\n{'='*60}")
    if not args.dry_run:
        csv_files = list(CSV_OUTPUT_DIR.glob("*.csv"))
        print(f"  PROCESO COMPLETADO")
        print(f"Archivos CSV generados: {len(csv_files)}")
        print(f"Ubicación: {CSV_OUTPUT_DIR}")
    else:
        print(f"[DRY-RUN] Se procesarían {total_files} archivos")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
