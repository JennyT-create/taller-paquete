# taller-paquete

Material de referencia del taller T03 del programa MLOps: **del notebook al paquete**. Es el proyecto del libro
(*Hotel Booking*) y crece taller a taller. Clónalo en una carpeta Git de Databricks Free Edition para leerlo y
correrlo; con *Pull* recibes las actualizaciones.

> **Regla de oro:** este repositorio es público. Nada del banco: ni datos, ni código, ni nombres de tablas o
> modelos, ni el nombre del banco.

## Qué hay aquí

| Archivo o carpeta | Para qué sirve |
|---|---|
| `notebooks/preprocesamiento.py` | El "antes": todo el preprocesamiento en un notebook |
| `notebooks/revisar.py` | Instala el paquete, corre las pruebas y pasa ruff. Córrelo antes de cada commit |
| `src/hotel_booking/` | El "después": el código como paquete de Python |
| `tests/` | Las pruebas, que se corren con pytest |
| `pyproject.toml` | Nombre del paquete, dependencias y configuración de las herramientas |
| `uv.lock` | Las versiones exactas de todo lo que se instala |
| `project_config.yml` | Lo que esperamos que cambie: catálogos, hiperparámetros, columnas |
| `herramientas/preparar-terminal.sh` | Prepara la terminal web de Databricks para usar uv. Se corre una sola vez |
| `.github/workflows/revision.yml` | La revisión automática: pruebas y ruff en cada pull request |
| `.pre-commit-config.yaml` | Las revisiones antes de cada commit, para quien trabaja en una PC |
| `.devcontainer/` | La receta de un Codespace (Python 3.12 y uv), por si se habilita |

## En Databricks Free Edition: la terminal web

Abre cualquier notebook, conéctalo a *Serverless* y pulsa el ícono de terminal (al pie de la barra derecha).
La primera vez, prepárala:

```bash
cd /Workspace/Users/<tu-correo>/taller-paquete
bash herramientas/preparar-terminal.sh
```

Cierra la terminal y abre una nueva. Desde entonces, en cada sesión:

```bash
cd /Workspace/Users/<tu-correo>/taller-paquete
uv sync --extra dev          # crea el entorno con las versiones de uv.lock
uv run pytest                # corre las pruebas
uv run ruff check .          # el guardia: reglas
uv run ruff format .         # el guardia: formato
```

Sin terminal, `notebooks/revisar` hace lo mismo: córrelo completo (*Run all*).

## En una PC o un Codespace

```bash
uv sync --extra dev          # crea el entorno e instala todo
uv run pre-commit install    # activa las revisiones antes de cada commit
uv run pytest                # corre las pruebas
```

Datos: el dataset público *Hotel Booking* del libro *MLOps with Databricks*. No se guarda en este repositorio.
