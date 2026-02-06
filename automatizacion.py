from __future__ import annotations

import csv
import hashlib
import os
import shutil
import ssl
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse


# ========= CONFIG =========
CSV_PATH = r"C:\Users\djlop\OneDrive\DIEGO\UVG\2026\primer semestre\Minería de Datos\Laboratorios\ine_vitales_2009_2025.csv"
OUT_DIR = r"C:\Users\djlop\OneDrive\DIEGO\UVG\2026\primer semestre\Minería de Datos\Laboratorios\data\sav"

# Si True: guarda en OUT_DIR\2009\2009_defunciones.sav, etc.
# Si False: guarda todo plano en OUT_DIR\2009_defunciones.sav, etc.
GROUP_BY_YEAR = True

# Si True: si un archivo destino ya existe, no lo toca
SKIP_IF_EXISTS = True

# Descarga una sola vez por URL y luego copia/hardlink para cada año/categoría
DEDUP_BY_URL = True

# Intenta hardlink (rápido y sin duplicar espacio) si mismo disco; si falla, copia normal
TRY_HARDLINK = True

# Reintentos por descarga
RETRIES = 3
RETRY_SLEEP_SECONDS = 1.0

# Timeout de red
TIMEOUT_SECONDS = 60

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonDownloader/1.0"
# =========================


CATEGORIES = [
    "Defunciones",
    "Defunciones fetales",
    "Divorcios",
    "Matrimonios",
    "Nacimientos",
]


def slugify(text: str) -> str:
    # simple slug sin dependencias: lowercase, espacios a _, caracteres raros fuera
    # (suficiente para nombres de archivos)
    import unicodedata
    s = unicodedata.normalize("NFD", text)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")  # quita acentos
    s = s.lower().strip()
    s = s.replace(" ", "_")
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    s = "".join(ch for ch in s if ch in allowed)
    return s or "categoria"


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_url(url: str, dest: Path) -> None:
    # Descarga por streaming a archivo temporal y luego mueve (evita archivos corruptos parciales)
    ensure_dir(dest.parent)
    tmp = dest.with_suffix(dest.suffix + ".part")

    ctx = ssl.create_default_context()
    req = Request(url, headers={"User-Agent": USER_AGENT})

    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            with urlopen(req, timeout=TIMEOUT_SECONDS, context=ctx) as resp:
                # status puede no existir en algunos handlers, pero normalmente sí
                status = getattr(resp, "status", 200)
                if status >= 400:
                    raise HTTPError(url, status, f"HTTP {status}", resp.headers, None)

                with tmp.open("wb") as out:
                    shutil.copyfileobj(resp, out)

            # Si todo bien, renombra atomico
            if dest.exists():
                dest.unlink()
            tmp.replace(dest)
            return

        except (HTTPError, URLError, TimeoutError) as e:
            last_err = e
            if attempt < RETRIES:
                time.sleep(RETRY_SLEEP_SECONDS * attempt)
            else:
                break

        except Exception as e:
            last_err = e
            break

    raise RuntimeError(f"No pude descargar: {url}\nError final: {last_err}")


def try_hardlink_or_copy(src: Path, dest: Path) -> None:
    ensure_dir(dest.parent)

    if SKIP_IF_EXISTS and dest.exists():
        return

    if TRY_HARDLINK:
        try:
            if dest.exists():
                dest.unlink()
            os.link(src, dest)  # hardlink (solo mismo filesystem)
            return
        except OSError:
            # si falla, copiamos
            pass

    shutil.copy2(src, dest)


def parse_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    # utf-8-sig por si Excel mete BOM
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append(row)
        return rows


def get_ext_from_url(url: str, default_ext: str = ".sav") -> str:
    path = urlparse(url).path
    ext = Path(path).suffix
    return ext if ext else default_ext


def main() -> int:
    csv_path = Path(CSV_PATH)
    out_dir = Path(OUT_DIR)

    if not csv_path.exists():
        print(f"❌ No existe el CSV: {csv_path}")
        return 1

    ensure_dir(out_dir)

    rows = parse_csv_rows(csv_path)
    if not rows:
        print("❌ CSV vacío.")
        return 1

    # Validación de columnas
    header_cols = set(rows[0].keys())
    if "Año" not in header_cols:
        print(f"❌ El CSV no tiene columna 'Año'. Columnas: {sorted(header_cols)}")
        return 1

    for c in CATEGORIES:
        if c not in header_cols:
            print(f"❌ El CSV no tiene columna '{c}'. Columnas: {sorted(header_cols)}")
            return 1

    # Recolectar todas las tareas (year, category, url)
    tasks: list[tuple[str, str, str]] = []
    for row in rows:
        year = str(row["Año"]).strip().strip('"')
        for c in CATEGORIES:
            url = (row.get(c) or "").strip().strip('"')
            tasks.append((year, c, url))

    # Resumen de URLs únicas
    all_urls = [u for (_, _, u) in tasks if u]
    unique_urls = sorted(set(all_urls))
    print(f"Total celdas con URL: {len(all_urls)}")
    print(f"URLs únicas: {len(unique_urls)}")
    if len(unique_urls) <= 10:
        for u in unique_urls:
            print(" -", u)

    # Cache de descargas por URL
    cache_dir = out_dir / "_cache_downloads"
    ensure_dir(cache_dir)

    url_to_local: dict[str, Path] = {}

    def local_name_for_url(url: str) -> Path:
        # nombre determinístico por URL (hash) para cache
        ext = get_ext_from_url(url, ".sav")
        h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        return cache_dir / f"file_{h}{ext}"

    # Descargar (o reutilizar) cada URL única
    if DEDUP_BY_URL:
        for i, url in enumerate(unique_urls, 1):
            local_path = local_name_for_url(url)
            url_to_local[url] = local_path

            if local_path.exists():
                # ya está en cache
                continue

            print(f"[{i}/{len(unique_urls)}] ⬇️ Descargando URL única…")
            print("    ", url)
            download_url(url, local_path)
    else:
        # no dedup: se descarga directo a cada destino
        pass

    # Crear archivos finales con nombre por año/categoría
    total_ok = 0
    total_skip = 0
    total_fail = 0

    for (year, cat, url) in tasks:
        if not url:
            total_fail += 1
            continue

        cat_slug = slugify(cat)
        ext = get_ext_from_url(url, ".sav")

        if GROUP_BY_YEAR:
            dest_dir = out_dir / year
        else:
            dest_dir = out_dir

        dest = dest_dir / f"{year}_{cat_slug}{ext}"

        if SKIP_IF_EXISTS and dest.exists():
            total_skip += 1
            continue

        try:
            if DEDUP_BY_URL:
                src = url_to_local[url]
                if not src.exists():
                    raise FileNotFoundError(f"Cache no existe para URL: {url}")
                try_hardlink_or_copy(src, dest)
            else:
                # descarga directa al destino
                download_url(url, dest)

            total_ok += 1

        except Exception as e:
            total_fail += 1
            print(f"❌ Error con {year} / {cat}: {e}")

    print("\n=== RESUMEN ===")
    print("Guardado en:", out_dir)
    print("OK:", total_ok)
    print("Skip:", total_skip)
    print("Fail:", total_fail)
    print("Cache:", cache_dir)

    print("\nNota: si ves que solo hubo 5 URLs únicas, es normal que el cache tenga 5 archivos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
