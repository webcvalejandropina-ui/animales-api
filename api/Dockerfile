FROM python:3.12-slim

WORKDIR /app

LABEL org.opencontainers.image.title="Animal Facts API" \
      org.opencontainers.image.description="API gratuita de animales aleatorios con FastAPI, SQLite y base publica incluida" \
      org.opencontainers.image.source="https://github.com/webcvalejandropina-ui/animales-api" \
      org.opencontainers.image.documentation="https://github.com/webcvalejandropina-ui/animales-api#readme"

ENV PYTHONUNBUFFERED=1 \
    ANIMALES_DB_PATH=/app/animales.db

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY animales.db.zip ./

EXPOSE 13008

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "13008"]
