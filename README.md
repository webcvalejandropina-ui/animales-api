# API de animales aleatorios gratis con FastAPI, SQLite y base de datos pública.

Si buscas una API de animales aleatorios que sea rápida, gratis, fácil de ejecutar y lista para integrarse en una web, este proyecto es una muy buena base.

Está pensada para demos, proyectos educativos, portfolios, experimentos de frontend, widgets, juegos, pruebas de producto y cualquier caso en el que quieras obtener un animal aleatorio con descripción, curiosidad e imagen en base64 sin depender de servicios de pago.

## Por qué esta API mola tanto.

- Es gratis de ejecutar en local.
- No necesita API keys.
- No depende de terceros en tiempo de ejecución.
- Incluye la base de datos pública dentro del propio proyecto.
- Devuelve imágenes en base64 listas para usar en cliente.
- Está montada con FastAPI y SQLite, así que es fácil de entender y mantener.
- Se levanta en pocos minutos con Python o Docker.

## Qué devuelve.

Endpoint principal:

```text
GET /animal-aleatorio
```

Respuesta pública:

```json
{
  "id": 1633,
  "nombre": "Picamaderos",
  "url": "https://es.wikipedia.org/wiki/...",
  "url_imagen": "https://upload.wikimedia.org/...",
  "descripcion": "Descripción breve del animal.",
  "img_b64": "/9j/4AAQSkZJRgABAQ...",
  "curiosidades": "Texto breve con enfoque divulgativo."
}
```

Además incluye:

```text
GET /health
```

para comprobar que la API y la base están listas.

## Para quién encaja especialmente bien.

Esta API de animales aleatorios es ideal para:
- portfolios.
- landing pages interactivas.
- mini apps educativas.
- juegos y trivias.
- proyectos de aula.
- pruebas de producto.
- demos de FastAPI.
- integraciones frontend que quieran contenido visual sin coste.

## Base de datos pública incluida en el repo.

La base principal se publica en este archivo:

```text
api/animales.db.zip
```

Eso significa que:
- la base forma parte real del producto.
- no hace falta descargar nada desde fuera al montar el proyecto.
- cualquier persona puede clonar el repo y ejecutarlo.
- la app expande el archivo `zip` automáticamente cuando necesita la SQLite local.

### Qué contiene la base.

La base actual incluye:
- 2239 animales.
- 2239 filas con `url`.
- 2239 filas con `descripcion`.
- 2239 filas con `img_b64`.
- 2239 filas con `curiosidades`.
- 2174 filas con `url_imagen`.

Nota importante:
- `url_imagen` debe tratarse como campo opcional.
- `img_b64` sí está completa en toda la base y es la mejor opción para frontend.

## Origen de los datos.

El dataset base procede de Wikipedia y Wikimedia Commons.

En concreto:
- `nombre`, `url` y `descripcion` se apoyan en registros de Wikipedia en español.
- `url_imagen` apunta a recursos alojados en Wikimedia Commons.
- `img_b64` se obtiene a partir de esas imágenes.
- `curiosidades` se presenta como capa divulgativa asociada a cada animal dentro de la base final del proyecto.

## Licencia y reutilización del contenido.

Este repositorio deja claro lo siguiente:
- el código de la app se comparte con finalidad educativa y práctica.
- la base de datos incluida es pública dentro del proyecto.
- los datos de referencia proceden de Wikipedia y Wikimedia Commons.
- este proyecto no sustituye la licencia original de cada página, texto o imagen.
- la reutilización correcta siempre pasa por revisar la licencia y la atribución del recurso original en su fuente.

En resumen:
- no se publican datos privados.
- no se afirma una licencia única nueva sobre todo el contenido de terceros.
- el uso responsable exige respetar la atribución del recurso original.

## Stack técnico.

- FastAPI.
- SQLite.
- Docker.
- Docker Compose.
- Python 3.9 o superior.

## Cómo ejecutarlo en local.

### Opción 1. Python.

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 13008
```

### Opción 2. Docker.

```bash
cd api
docker compose up --build
```

Puerto por defecto:

```text
13008
```

URLs locales:

```text
http://127.0.0.1:13008/health
http://127.0.0.1:13008/animal-aleatorio
http://127.0.0.1:13008/docs
```

## Archivos importantes del proyecto.

```text
README.md
api/Dockerfile
api/animales.db.zip
api/docker-compose.yml
api/requirements.txt
api/app/__init__.py
api/app/database.py
api/app/main.py
```

## Cómo se comporta la app al arrancar.

La aplicación:
- expande `api/animales.db.zip` a `api/animales.db` si hace falta.
- abre la SQLite en modo solo lectura.
- valida que la tabla exista.
- valida que la base no esté vacía.
- valida que todas las filas tengan `curiosidades`.
- valida que todas las filas tengan `img_b64`.

Si alguna de esas comprobaciones falla, la API no arranca.

## Por qué es una base brutal para construir producto.

Porque combina varias cosas que normalmente cuestan tiempo:
- contenido listo para enseñar.
- imágenes listas para renderizar.
- estructura backend simple.
- coste cero en local.
- integración rápida con cualquier frontend.
- dataset ya empaquetado dentro del repo.

## Uso de `img_b64` en frontend.

HTML:

```html
<img src="AQUI_VA_LA_DATA_URL_GENERADA" alt="Animal" />
```

JavaScript:

```js
const imageSrc = buildImageSrc(animal.img_b64)
```

## Resumen.

Esta API de animales aleatorios es una solución pequeña, potente, gratis y muy fácil de reutilizar.

Si quieres una base pública con animales, FastAPI, SQLite, Docker y una integración sencilla para frontend, aquí tienes un producto realmente bueno para arrancar rápido.
