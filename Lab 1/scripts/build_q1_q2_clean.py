"""
Prefase Q1-Q2: limpieza reproducible de nacimientos y defunciones (2009-2022).

Entradas:
    - data/raw/csv/*_nacimientos.csv
    - data/raw/csv/*_defunciones.csv

Salidas:
    - data/processed/nacimientos_clean_2009_2022.csv
    - data/processed/defunciones_clean_2009_2022.csv
    - data/processed/q1q2_control_calidad_2009_2022.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


YEAR_START = 2009
YEAR_END = 2022


@dataclass
class CleanStats:
    tipo: str
    files_considered: int = 0
    rows_input: int = 0
    rows_output: int = 0
    rows_excluded_missing_depreg: int = 0
    nulls: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    parse_errors: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    duplicates_exact: int = 0
    duplicates_operational: int = 0
    year_rows: Dict[int, int] = field(default_factory=lambda: defaultdict(int))


def _iter_files(raw_dir: Path, tipo: str) -> List[Tuple[int, Path]]:
    files: List[Tuple[int, Path]] = []
    for year in range(YEAR_START, YEAR_END + 1):
        path = raw_dir / f"{year}_{tipo}.csv"
        if path.exists():
            files.append((year, path))
    return files


def _read_header(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []
    return [h.strip().lower() for h in header]


def _safe_num(
    raw_value: str | None,
    *,
    integer: bool,
    stats: CleanStats,
    parse_error_key: str,
    null_key: str,
) -> str:
    value = (raw_value or "").strip()
    if value == "":
        stats.nulls[null_key] += 1
        return ""
    try:
        n = float(value)
    except ValueError:
        stats.parse_errors[parse_error_key] += 1
        stats.nulls[null_key] += 1
        return ""
    if integer:
        return str(int(n))
    return str(n)


def _canonical_hash(parts: Sequence[str]) -> str:
    payload = "\x1f".join(parts).encode("utf-8", errors="ignore")
    return hashlib.sha1(payload).hexdigest()


def _clean_tipo(
    *,
    tipo: str,
    raw_dir: Path,
    processed_dir: Path,
    numeric_keys: Sequence[str],
    verbose: bool,
) -> CleanStats:
    files = _iter_files(raw_dir, tipo)
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos para tipo={tipo} en {raw_dir}")

    stats = CleanStats(tipo=tipo, files_considered=len(files))

    # Union de columnas (solo headers) + columna año forzada
    columns_set = {"año"}
    for year, path in files:
        header = _read_header(path)
        if not header:
            if verbose:
                print(f"[WARN] Archivo sin encabezado (saltado): {path.name}")
            continue
        columns_set.update(header)
        if verbose:
            print(f"[HEADER] {path.name}: {len(header)} columnas")

    columns = sorted(columns_set)
    output_path = processed_dir / f"{tipo}_clean_2009_2022.csv"

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE exact_seen (sig TEXT PRIMARY KEY)")
    cur.execute("CREATE TABLE op_seen (sig TEXT PRIMARY KEY)")

    with output_path.open("w", encoding="utf-8", newline="") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=columns)
        writer.writeheader()

        for year, path in files:
            with path.open("r", encoding="utf-8", newline="") as in_f:
                reader = csv.DictReader(in_f)
                if reader.fieldnames is None:
                    if verbose:
                        print(f"[WARN] Sin fieldnames (saltado): {path.name}")
                    continue

                lowered = [h.strip().lower() for h in reader.fieldnames]
                mapping = dict(zip(reader.fieldnames, lowered))

                for row in reader:
                    stats.rows_input += 1

                    normalized: Dict[str, str] = {col: "" for col in columns}
                    for k, v in row.items():
                        lk = mapping.get(k, "").strip().lower()
                        if lk:
                            normalized[lk] = (v or "").strip()

                    # Año forzado desde nombre de archivo
                    normalized["año"] = str(year)

                    # Coercion numerica en claves
                    for key in numeric_keys:
                        if key not in normalized:
                            normalized[key] = ""
                        normalized[key] = _safe_num(
                            normalized[key],
                            integer=True if key in ("año", "depreg") else False,
                            stats=stats,
                            parse_error_key=key,
                            null_key=key,
                        )

                    # Regla de exclusion minima: sin año o sin depreg
                    if normalized.get("año", "") == "" or normalized.get("depreg", "") == "":
                        stats.rows_excluded_missing_depreg += 1
                        continue

                    # Duplicado exacto
                    exact_sig = _canonical_hash([normalized.get(c, "") for c in columns])
                    cur.execute("INSERT OR IGNORE INTO exact_seen(sig) VALUES (?)", (exact_sig,))
                    if cur.rowcount == 0:
                        stats.duplicates_exact += 1

                    # Duplicado operacional (si aplica: año+depreg+mupreg)
                    mupreg = normalized.get("mupreg", "").strip()
                    if mupreg != "":
                        op_sig = _canonical_hash(
                            [normalized.get("año", ""), normalized.get("depreg", ""), mupreg]
                        )
                        cur.execute("INSERT OR IGNORE INTO op_seen(sig) VALUES (?)", (op_sig,))
                        if cur.rowcount == 0:
                            stats.duplicates_operational += 1

                    writer.writerow(normalized)
                    stats.rows_output += 1
                    stats.year_rows[year] += 1

            if verbose:
                print(
                    f"[OK] {path.name}: input acumulado={stats.rows_input:,}, "
                    f"output acumulado={stats.rows_output:,}"
                )

    conn.close()
    return stats


def _write_quality_report(stats_list: Iterable[CleanStats], out_path: Path) -> None:
    fieldnames = ["section", "tipo", "year", "metric", "value"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for st in stats_list:
            summary_rows = [
                ("files_considered", st.files_considered),
                ("rows_input", st.rows_input),
                ("rows_output", st.rows_output),
                ("rows_excluded_missing_depreg", st.rows_excluded_missing_depreg),
                ("duplicates_exact", st.duplicates_exact),
                ("duplicates_operational", st.duplicates_operational),
            ]
            for metric, value in summary_rows:
                writer.writerow(
                    {
                        "section": "summary",
                        "tipo": st.tipo,
                        "year": "",
                        "metric": metric,
                        "value": value,
                    }
                )

            for key in ("año", "depreg", "edadif"):
                writer.writerow(
                    {
                        "section": "nulls",
                        "tipo": st.tipo,
                        "year": "",
                        "metric": f"nulls_{key}",
                        "value": st.nulls.get(key, 0),
                    }
                )
                writer.writerow(
                    {
                        "section": "parse_errors",
                        "tipo": st.tipo,
                        "year": "",
                        "metric": f"parse_errors_{key}",
                        "value": st.parse_errors.get(key, 0),
                    }
                )

            for year in range(YEAR_START, YEAR_END + 1):
                writer.writerow(
                    {
                        "section": "coverage_year",
                        "tipo": st.tipo,
                        "year": year,
                        "metric": "rows_output_year",
                        "value": st.year_rows.get(year, 0),
                    }
                )


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye datasets clean para prefase Q1-Q2.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("Lab 1/data/raw/csv"),
        help="Directorio de CSV crudos",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("Lab 1/data/processed"),
        help="Directorio de salida procesado",
    )
    parser.add_argument("--quiet", action="store_true", help="Silenciar logs de progreso")
    args = parser.parse_args()

    raw_dir = args.raw_dir
    processed_dir = args.processed_dir
    verbose = not args.quiet

    if not raw_dir.exists():
        raise FileNotFoundError(f"No existe raw-dir: {raw_dir}")
    processed_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        print("=== PREFase Q1-Q2: limpieza reproducible ===")
        print(f"raw_dir={raw_dir}")
        print(f"processed_dir={processed_dir}")
        print(f"rango={YEAR_START}-{YEAR_END}")

    nac_stats = _clean_tipo(
        tipo="nacimientos",
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        numeric_keys=("año", "depreg"),
        verbose=verbose,
    )
    def_stats = _clean_tipo(
        tipo="defunciones",
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        numeric_keys=("año", "depreg", "edadif"),
        verbose=verbose,
    )

    quality_path = processed_dir / "q1q2_control_calidad_2009_2022.csv"
    _write_quality_report([nac_stats, def_stats], quality_path)

    if verbose:
        print("=== PREFase completada ===")
        print("[OUT]", processed_dir / "nacimientos_clean_2009_2022.csv")
        print("[OUT]", processed_dir / "defunciones_clean_2009_2022.csv")
        print(f"[OUT] {quality_path}")


if __name__ == "__main__":
    main()
