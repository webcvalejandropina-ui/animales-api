FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="Animal Facts API" \
      org.opencontainers.image.description="API gratuita de animales aleatorios con FastAPI, SQLite y base publica incluida" \
      org.opencontainers.image.source="https://github.com/webcvalejandropina-ui/animales-api" \
      org.opencontainers.image.documentation="https://github.com/webcvalejandropina-ui/animales-api#readme"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    ANIMALES_DB_PATH=/app/animales.db

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --shell /usr/sbin/nologin \
        --home-dir /app --no-create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY animales.db.zip ./

RUN python <<'PY'
from pathlib import Path
from shutil import move
from zipfile import ZipFile

zf = ZipFile("animales.db.zip")
try:
    members = [n for n in zf.namelist() if n.endswith("animales.db")]
    if not members:
        raise RuntimeError("animales.db not found in zip")
    zf.extract(members[0], "/tmp")
    move(Path("/tmp") / members[0], Path("/app/animales.db"))
finally:
    zf.close()
Path("animales.db.zip").unlink()
PY

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 13008

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "13008"]
