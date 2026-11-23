# taller-paquete

Material de referencia del taller T03 del programa MLOps: **del notebook al paquete**. Es el proyecto del libro
(*Hotel Booking*) y crece taller a taller. Clónalo en una carpeta Git de Databricks Free Edition para leerlo y
correrlo; con *Pull* recibes las actualizaciones.

> **Regla de oro:** este repositorio es público. Nada del banco: ni datos, ni código, ni nombres de tablas o
> modelos, ni el nombre del banco.

## Qué hay aquí

| Archivo o carpeta | Para qué sirve |
|---|---|
| `notebooks/cargar-datos.py` | Baja los datos al catálogo de Databricks y muestra cómo son. Se corre una vez |
| `notebooks/preprocesamiento.py` | El "antes": todo el preprocesamiento en un notebook |
| `src/hotel_booking/` | El "después": el código como paquete de Python |
| `tests/` | Las pruebas, que se corren con pytest |
| `pyproject.toml` | Nombre del paquete, dependencias y configuración de las herramientas |
| `uv.lock` | Las versiones exactas de todo lo que se instala |
| `project_config.yml` | Lo que esperamos que cambie: catálogos, hiperparámetros, columnas |
| `.github/workflows/revision.yml` | La revisión automática: pruebas y ruff en cada pull request |
| `.github/CODEOWNERS` | Quién debe aprobar un pull request para que entre a `main` |
| `.pre-commit-config.yaml` | Las revisiones antes de cada commit, para quien trabaja en una PC |

## En Databricks Free Edition: la terminal web

**La primera vez, prepara la terminal** con el repositorio
[`chapter-aa/herramientas`](https://github.com/chapter-aa/herramientas): clónalo en tu carpeta de usuario, junto a
este, y sigue su README. Se hace una sola vez y sirve para todos los proyectos.

Después, abre un notebook de este repositorio (por ejemplo, `notebooks/preprocesamiento`), conéctalo a *Serverless*
y pulsa el ícono de terminal (al pie de la barra derecha). La terminal se abre en la carpeta de ese notebook. En cada
sesión:

```bash
cd ..                        # de notebooks/ a la raíz del repositorio
uv sync --extra dev          # crea el entorno con las versiones de uv.lock
uv run pytest                # corre las pruebas
uv run ruff check .          # el guardia: reglas
uv run ruff format .         # el guardia: formato
```

## En una PC

```bash
uv sync --extra dev          # crea el entorno e instala todo
uv run pre-commit install    # activa las revisiones antes de cada commit
uv run pytest                # corre las pruebas
```

## Los datos

El dataset público *Hotel Booking* del libro *MLOps with Databricks*. No se guarda en este repositorio: los datos
no van a Git. En Databricks, corre una vez el notebook `notebooks/cargar-datos` (en *Serverless*, *Run all*): lo
baja del repositorio del libro a `/Volumes/mlops_dev/hotel_booking/datos/booking.csv`.
