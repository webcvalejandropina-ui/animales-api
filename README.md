# API educativa de animales aleatorios

API mínima, autocontenida y lista para ejecutar en local que devuelve un animal aleatorio desde una base de datos SQLite pública incluida en el propio repositorio.

El objetivo del proyecto es educativo:
- mostrar una API pequeña y fácil de entender;
- enseñar una estructura backend simple con FastAPI;
- trabajar con una base SQLite ya preparada y versionada;
- ofrecer una demo reproducible sin depender de servicios externos.

## Qué resuelve este proyecto

La API expone un único recurso útil:

```text
GET /animal-aleatorio
```

Cada petición devuelve un animal distinto con:
- nombre;
- enlace de referencia;
- descripción;
- curiosidad educativa;
- imagen en base64 lista para incrustar en una web.

También incluye:

```text
GET /health
```

para comprobar que la API y la base están listas.

## Base de datos pública incluida

Este repositorio incluye la base completa en formato comprimido en:

```text
api/animales.db.gz
```

Punto importante:
- la base forma parte del proyecto y debe subirse al repositorio;
- la versión publicada es `gzip` para reducir el peso del fichero;
- la aplicación la descomprime automáticamente al primer arranque;
- no se descarga en tiempo de ejecución;
- no hace falta ninguna API key;
- no hace falta conexión externa para que la app funcione una vez construida;
- cualquiera puede clonar el repositorio y ejecutarlo en local.

La política de versionado está preparada para:
- subir `api/animales.db.gz`;
- ignorar la copia expandida `api/animales.db` que se genera localmente;
- excluir artefactos temporales en `.gitignore`.

### Por qué la base va comprimida

La base original sin comprimir ocupa aproximadamente `107 MB`.

La copia publicada:
- reduce el tamaño del repo;
- facilita la subida a servicios Git con límites de tamaño más estrictos;
- mantiene el proyecto autocontenido;
- sigue dejando la base pública y visible dentro del repositorio.

## Origen de los datos

El conjunto base de datos procede de Wikipedia y Wikimedia Commons:
- `nombre`, `url` y `descripcion` se apoyan en registros de Wikipedia en español;
- `url_imagen` apunta a imágenes alojadas en Wikimedia Commons;
- `img_b64` es una representación embebible derivada de esas imágenes;
- `curiosidades` se presenta como capa educativa asociada al animal dentro de la base final del proyecto.

Si reutilizas el contenido fuera de este proyecto, revisa siempre la atribución y la licencia del recurso original en su página de Wikipedia o Wikimedia Commons.

## Estado actual del dataset

La base incluida contiene:
- 2239 animales;
- 2239 filas con `url`;
- 2239 filas con `descripcion`;
- 2239 filas con `img_b64`;
- 2239 filas con `curiosidades`;
- 2174 filas con `url_imagen`.

Nota importante:
- `url_imagen` debe considerarse opcional;
- la imagen utilizable para cliente es `img_b64`, que sí está completa en toda la base.

## Archivos que sí deben subirse

Para publicar este proyecto de forma mínima y correcta, los archivos necesarios son:

```text
README.md
.gitignore
api/.dockerignore
api/Dockerfile
api/animales.db.gz
api/docker-compose.yml
api/requirements.txt
api/app/__init__.py
api/app/database.py
api/app/main.py
```

No hace falta subir:
- `api/animales.db` expandida localmente;
- entornos virtuales;
- logs;
- zips auxiliares;
- caches o artefactos temporales.

## Estructura del proyecto

```text
.
├── README.md
├── .gitignore
└── api
    ├── .dockerignore
    ├── Dockerfile
    ├── animales.db.gz
    ├── docker-compose.yml
    ├── requirements.txt
    └── app
        ├── __init__.py
        ├── database.py
        └── main.py
```

## Diseño técnico

El proyecto está intencionadamente simplificado:
- una sola API;
- una sola base SQLite;
- un solo endpoint funcional;
- validación fuerte en el arranque;
- superficie pequeña para mantenimiento y aprendizaje.

La aplicación:
- expande automáticamente `api/animales.db.gz` a `api/animales.db` en el primer arranque si hace falta;
- abre la base en modo solo lectura;
- valida que la tabla exista;
- valida que no esté vacía;
- valida que todas las filas tengan `curiosidades`;
- valida que todas las filas tengan `img_b64`.

Si alguna de esas comprobaciones falla, la API no arranca.

## Respuesta de la API

Ejemplo de respuesta:

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

### Significado de cada campo

- `id`: identificador interno en SQLite.
- `nombre`: nombre principal del animal.
- `url`: enlace informativo del registro.
- `url_imagen`: URL original de la imagen cuando está disponible.
- `descripcion`: resumen corto del animal.
- `img_b64`: imagen codificada en base64, lista para mostrar en cliente.
- `curiosidades`: texto corto de orientación educativa.

## Cómo ejecutarlo en local

### Opción 1: Python

Requisitos:
- Python 3.9 o superior

Pasos:

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 13008
```

Accesos:

```text
http://127.0.0.1:13008/health
http://127.0.0.1:13008/animal-aleatorio
http://127.0.0.1:13008/docs
```

### Opción 2: Docker

```bash
cd api
docker compose up --build
```

Nombre unificado en Docker:

```text
Proyecto Compose: alex-alimales-api
Servicio Compose: alex-alimales-api
Imagen: alex-alimales-api
Contenedor: alex-alimales-api
```

## Verificación rápida

Comprobar salud:

```bash
curl http://127.0.0.1:13008/health
```

Pedir un animal aleatorio:

```bash
curl http://127.0.0.1:13008/animal-aleatorio
```

## Uso de `img_b64` en frontend

HTML:

```html
<img src="data:image/jpeg;base64,AQUI_VA_IMG_B64" alt="Animal" />
```

JavaScript:

```js
const imageSrc = `data:image/jpeg;base64,${animal.img_b64}`;
```

## Archivos principales

- `api/app/main.py`: API FastAPI y endpoints públicos.
- `api/app/database.py`: apertura, expansión y validación de la base SQLite.
- `api/animales.db.gz`: base pública incluida en el repositorio.
- `api/docker-compose.yml`: arranque local con nombre final unificado.
- `api/Dockerfile`: imagen lista para construir.

## Recomendación de uso

Este proyecto es especialmente útil para:
- demos;
- pruebas locales;
- ejemplos educativos de FastAPI;
- proyectos frontend que necesiten un endpoint simple y sin dependencias externas.
