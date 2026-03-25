"""Acceso a la base SQLite estatica.

Este modulo concentra dos ideas importantes:
- la base se abre en modo solo lectura para evitar cambios accidentales;
- si la base versionada va comprimida, se expande automaticamente;
- antes de aceptar peticiones se comprueba que todos los animales tienen
  curiosidades e imagen en base64.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "animales.db"

ANIMAL_PUBLIC_COLUMNS = "id, nombre, url, url_imagen, descripcion, img_b64, curiosidades"


def get_db_path() -> Path:
    """Resuelve la ruta de la base, con soporte para variable de entorno."""

    return Path(os.environ.get("ANIMALES_DB_PATH", str(DEFAULT_DB))).expanduser().resolve()


def _zip_path_for(db_path: Path) -> Path:
    """Devuelve la ruta esperada del archivo zip que contiene la base."""

    return db_path.with_name(f"{db_path.name}.zip")


def ensure_database_file() -> Path:
    """Garantiza que exista la base SQLite lista para abrir.

    Si el repositorio solo contiene `animales.db.zip`, la función lo expande una vez
    a `animales.db` dentro de la misma carpeta.
    """

    db_path = get_db_path()
    if db_path.is_file():
        return db_path

    zip_path = _zip_path_for(db_path)
    if not zip_path.is_file():
        raise FileNotFoundError(
            "No se encuentra la base de datos SQLite ni su copia comprimida en zip: "
            f"{db_path} / {zip_path}"
        )

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as zf:
        members = [name for name in zf.namelist() if name.endswith(db_path.name)]
        if not members:
            raise FileNotFoundError(
                f"El zip no contiene el archivo esperado {db_path.name}: {zip_path}"
            )
        with zf.open(members[0]) as src, db_path.open("wb") as dst:
            dst.write(src.read())

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
        """
        SELECT COUNT(*) FROM animales
        WHERE curiosidades IS NOT NULL
          AND TRIM(curiosidades) != ''
        """
    )
    total_curiosidades = cur.fetchone()[0]
    if total_curiosidades != total:
        conn.close()
        raise ValueError(
            "La base de datos no esta completa: faltan curiosidades en "
            f"{total - total_curiosidades} animales ({db_path})"
        )

    cur = conn.execute(
        """
        SELECT COUNT(*) FROM animales
        WHERE img_b64 IS NOT NULL
          AND TRIM(img_b64) != ''
        """
    )
    total_img_b64 = cur.fetchone()[0]
    if total_img_b64 != total:
        conn.close()
        raise ValueError(
            "La base de datos no esta completa: faltan imagenes b64 en "
            f"{total - total_img_b64} animales ({db_path})"
        )

    return conn
