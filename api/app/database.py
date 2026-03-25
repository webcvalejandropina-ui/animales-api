"""Acceso a la base SQLite estatica.

Este modulo concentra dos ideas importantes:
- la base se abre en modo solo lectura para evitar cambios accidentales;
- si la base versionada va comprimida, se expande automaticamente;
- antes de aceptar peticiones se comprueba que todos los animales tienen
  los campos publicos necesarios para la API.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "animales.db"

ANIMAL_PUBLIC_COLUMNS = "id, nombre, url, url_imagen, descripcion, img_b64, curiosidades"
REQUIRED_ANIMAL_WHERE = """
id IS NOT NULL
AND
nombre IS NOT NULL AND TRIM(nombre) != ''
AND url IS NOT NULL AND TRIM(url) != ''
AND descripcion IS NOT NULL AND TRIM(descripcion) != ''
AND img_b64 IS NOT NULL AND TRIM(img_b64) != ''
AND curiosidades IS NOT NULL AND TRIM(curiosidades) != ''
"""


def get_db_path() -> Path:
    """Resuelve la ruta de la base, con soporte para variable de entorno."""

    return Path(os.environ.get("ANIMALES_DB_PATH", str(DEFAULT_DB))).expanduser().resolve()


def _zip_path_for(db_path: Path) -> Path:
    """Devuelve la ruta esperada del archivo zip que contiene la base."""

    return db_path.with_name(f"{db_path.name}.zip")


def _looks_like_sqlite_file(db_path: Path) -> bool:
    """Comprueba si el archivo existe y tiene cabecera valida de SQLite."""

    if not db_path.is_file():
        return False
    if db_path.stat().st_size < 100:
        return False
    with db_path.open("rb") as fh:
        return fh.read(16) == b"SQLite format 3\x00"


def _extract_database_from_zip(zip_path: Path, db_path: Path) -> None:
    """Extrae la base de datos de forma atomica para evitar archivos truncados."""

    db_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = db_path.with_name(f"{db_path.name}.tmp")

    with ZipFile(zip_path) as zf:
        members = [name for name in zf.namelist() if name.endswith(db_path.name)]
        if not members:
            raise FileNotFoundError(
                f"El zip no contiene el archivo esperado {db_path.name}: {zip_path}"
            )
        with zf.open(members[0]) as src, tmp_path.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    tmp_path.replace(db_path)


def ensure_database_file() -> Path:
    """Garantiza que exista la base SQLite lista para abrir.

    Si el repositorio solo contiene `animales.db.zip`, la función lo expande una vez
    a `animales.db` dentro de la misma carpeta.
    """

    db_path = get_db_path()
    if _looks_like_sqlite_file(db_path):
        return db_path

    zip_path = _zip_path_for(db_path)
    if not zip_path.is_file():
        raise FileNotFoundError(
            "No se encuentra la base de datos SQLite ni su copia comprimida en zip: "
            f"{db_path} / {zip_path}"
        )

    _extract_database_from_zip(zip_path, db_path)

    if not _looks_like_sqlite_file(db_path):
        raise ValueError(
            "La base de datos extraida no tiene un formato SQLite valido: "
            f"{db_path}"
        )

    return db_path


def open_database() -> sqlite3.Connection:
    """Abre y valida una base SQLite completamente preparada para produccion local."""

    db_path = ensure_database_file()

    conn = sqlite3.connect(
        f"{db_path.as_uri()}?mode=ro",
        uri=True,
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row

    cur = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'animales'"
    )
    if cur.fetchone()[0] == 0:
        conn.close()
        raise ValueError(f"La base de datos no contiene la tabla 'animales': {db_path}")

    cur = conn.execute("SELECT COUNT(*) FROM animales")
    total = cur.fetchone()[0]
    if total == 0:
        conn.close()
        raise ValueError(f"La tabla 'animales' esta vacia: {db_path}")

    cur = conn.execute(
        f"SELECT COUNT(*) FROM animales WHERE {REQUIRED_ANIMAL_WHERE}"
    )
    total_validos = cur.fetchone()[0]
    if total_validos != total:
        conn.close()
        raise ValueError(
            "La base de datos no esta completa: faltan campos publicos obligatorios en "
            f"{total - total_validos} animales ({db_path})"
        )

    return conn
