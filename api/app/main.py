"""API minima para fines educativos.

La idea del proyecto es mostrar una API muy pequena, facil de leer y sin
dependencias externas en tiempo de ejecucion:
- abre una base SQLite estatica;
- valida el contenido al arrancar;
- expone un endpoint util y un endpoint de salud.
"""

from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.database import ANIMAL_PUBLIC_COLUMNS, open_database


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


def require_database() -> sqlite3.Connection:
    """Devuelve la conexion abierta o corta la peticion si la app no arranco bien."""

    if _db is None:
        raise HTTPException(status_code=503, detail="Base de datos no inicializada")
    return _db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Abre la base una sola vez durante la vida de la aplicacion."""

    del app
    global _db
    _db = open_database()
    try:
        yield
    finally:
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
    cur = db.execute(
        f"SELECT {ANIMAL_PUBLIC_COLUMNS} FROM animales ORDER BY RANDOM() LIMIT 1"
    )
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No hay animales en la base de datos")
    return dict(row)


@app.get("/health")
def health() -> Dict[str, str]:
    """Confirma que la aplicacion y la base estan listas para responder."""

    require_database()
    return {"status": "ok"}
