# taller-paquete

Repositorio plantilla del taller T03 del programa MLOps: **del notebook al paquete**.
Cada persona crea su propia copia con *Use this template*, la clona en una carpeta Git de Databricks Free Edition y
trabaja ahí.

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
| `.github/workflows/revision.yml` | La revisión automática: pruebas y ruff en cada pull request |
| `.pre-commit-config.yaml` | Las revisiones antes de cada commit, para quien trabaja en una PC |
| `.devcontainer/` | La receta de un Codespace (Python 3.12 y uv), por si se habilita |

## En Databricks Free Edition

Abre `notebooks/revisar`, comprueba que el entorno serverless sea la versión 4 o superior y córrelo completo.

## En una PC o un Codespace

```bash
uv sync --extra dev          # crea el entorno e instala todo
uv run pre-commit install    # activa las revisiones antes de cada commit
uv run pytest                # corre las pruebas
```

Datos: el dataset público *Hotel Booking* del libro *MLOps with Databricks*. No se guarda en este repositorio.
