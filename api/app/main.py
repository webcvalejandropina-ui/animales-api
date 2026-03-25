"""API minima para fines educativos.

La idea del proyecto es mostrar una API muy pequena, facil de leer y sin
dependencias externas en tiempo de ejecucion:
- abre una base SQLite estatica;
- valida el contenido al arrancar;
- expone un endpoint util y un endpoint de salud.
"""

from __future__ import annotations

import logging
import random
import sqlite3
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.database import ANIMAL_PUBLIC_COLUMNS, load_valid_animal_ids, open_database

logger = logging.getLogger(__name__)


class Animal(BaseModel):
    """Modelo publico que representa la respuesta de la API."""

    id: int
    nombre: str
    url: Optional[str] = None
    url_imagen: Optional[str] = Field(
        None,
        description="Enlace a la imagen en la web.",
    )
    descripcion: Optional[str] = None
    img_b64: Optional[str] = Field(
        None,
        description="Miniatura JPEG codificada en base64, sin prefijo data:.",
    )
    curiosidades: Optional[str] = None

    @field_validator("img_b64", mode="before")
    @classmethod
    def _img_b64_no_urls(cls, value: object) -> object:
        if value is None or not isinstance(value, str):
            return value
        cleaned = value.strip()
        if not cleaned:
            return None
        if cleaned.lower().startswith(("http://", "https://")):
            return None
        return cleaned


_db: Optional[sqlite3.Connection] = None
_valid_animal_ids: Tuple[int, ...] = ()


def require_database() -> sqlite3.Connection:
    """Devuelve la conexion abierta o corta la peticion si la app no arranco bien."""

    if _db is None:
        raise HTTPException(status_code=503, detail="Base de datos no inicializada")
    return _db


def require_valid_animal_ids() -> Tuple[int, ...]:
    """Devuelve los ids publicables y evita responder con filas invalidas."""

    if not _valid_animal_ids:
        raise HTTPException(status_code=503, detail="No hay animales validos disponibles")
    return _valid_animal_ids


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Abre la base una sola vez durante la vida de la aplicacion."""

    del app
    global _db, _valid_animal_ids
    _db = open_database()
    _valid_animal_ids = load_valid_animal_ids(_db)
    if not _valid_animal_ids:
        if _db is not None:
            _db.close()
            _db = None
        raise RuntimeError("La base de datos no contiene animales validos para la API")
    try:
        yield
    finally:
        _valid_animal_ids = ()
        if _db is not None:
            _db.close()
            _db = None


app = FastAPI(
    title="Animales aleatorios",
    description=(
        "API minima con base SQLite estatica. "
        "Devuelve un animal aleatorio con descripcion, curiosidades e imagen en base64."
    ),
    lifespan=lifespan,
)


@app.get("/animal-aleatorio", response_model=Animal)
def animal_aleatorio() -> Dict[str, Any]:
    """Obtiene un unico animal aleatorio desde la base validada."""

    db = require_database()
    valid_animal_ids = require_valid_animal_ids()
    animal_id = random.choice(valid_animal_ids)
    cur = db.execute(
        f"SELECT {ANIMAL_PUBLIC_COLUMNS} FROM animales WHERE id = ?",
        (animal_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise HTTPException(
            status_code=503,
            detail="No se pudo recuperar un animal valido de la base de datos",
        )

    payload = dict(row)
    try:
        return Animal.model_validate(payload).model_dump()
    except ValidationError:
        logger.warning("Fila descartada en /animal-aleatorio: %r", payload)
        raise HTTPException(
            status_code=503,
            detail="No se pudo serializar un animal valido de la base de datos",
        ) from None


@app.get("/health")
def health() -> Dict[str, str]:
    """Confirma que la aplicacion y la base estan listas para responder."""

    require_database()
    require_valid_animal_ids()
    return {"status": "ok"}
