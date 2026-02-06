#!/usr/bin/env python3
"""Script temporal: convierte todos los archivos .xlsx en un directorio a .csv.

Uso:
  python convert_xlsx_to_csv_temp.py --dir data

Opciones útiles:
  --recursive    buscar recursivamente
  --dry-run      mostrar lo que se haría sin escribir archivos
  --engine       pasar engine para pandas.read_excel (por ejemplo openpyxl)
"""
from pathlib import Path
import argparse
import sys
from typing import Any

try:
    import pandas as pd
except Exception:
    print("Este script requiere pandas. Instálalo con: pip install pandas openpyxl")
    sys.exit(1)


def convert_xlsx_to_csv(xlsx_path: Path, dry_run: bool = False, engine: Any = None) -> bool:
    out_path = xlsx_path.with_suffix('.csv')
    if dry_run:
        print(f"[DRY-RUN] {xlsx_path} -> {out_path}")
        return True
    try:
        if engine:
            df = pd.read_excel(xlsx_path, engine=engine)
        else:
            df = pd.read_excel(xlsx_path)
        df.to_csv(out_path, index=False)
        print(f"Converted: {xlsx_path} -> {out_path}")
        return True
    except Exception as e:
        print(f"Failed to convert {xlsx_path}: {e}")
        return False


def main() -> None:
    p = argparse.ArgumentParser(description="Convertir .xlsx a .csv (temporal)")
    p.add_argument("--dir", "-d", default="data", help="Directorio donde buscar archivos .xlsx")
    p.add_argument("--recursive", "-r", action="store_true", help="Buscar recursivamente")
    p.add_argument("--dry-run", action="store_true", help="No escribir archivos, solo mostrar acciones")
    p.add_argument("--engine", default=None, help="Engine para pandas.read_excel (p. ej. openpyxl)")
    args = p.parse_args()

    base = Path(args.dir)
    if not base.exists():
        print(f"Directorio no encontrado: {base}")
        sys.exit(1)

    pattern = "**/*.xlsx" if args.recursive else "*.xlsx"
    files = sorted(base.glob(pattern))
    if not files:
        print(f"No se encontraron archivos .xlsx en: {base} (pattern={pattern})")
        return

    success = 0
    for f in files:
        if convert_xlsx_to_csv(f, dry_run=args.dry_run, engine=args.engine):
            success += 1

    print(f"Procesados: {len(files)} archivos. Convertidos correctamente: {success}.")


if __name__ == '__main__':
    main()
