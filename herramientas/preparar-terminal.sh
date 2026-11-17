#!/usr/bin/env bash
# Prepara la terminal web de Databricks para trabajar con uv, pytest y ruff.
#
# Córrelo una sola vez, desde la carpeta del repositorio:
#     bash herramientas/preparar-terminal.sh
#
# Escribe un bloque en el .bashrc de tu carpeta de usuario del workspace.
# Databricks lee ese archivo cada vez que abres una terminal, así que después
# solo tienes que escribir: uv sync --extra dev, uv run pytest, uv run ruff check .
set -euo pipefail

usuario=$(databricks current-user me --output json |
    python3 -c 'import json, sys; print(json.load(sys.stdin)["userName"])')
destino="/Workspace/Users/${usuario}/.bashrc"
inicio="# >>> taller MLOps >>>"
fin="# <<< taller MLOps <<<"

read -r -d '' bloque <<'BLOQUE' || true
# Lo escribió herramientas/preparar-terminal.sh. Para actualizarlo, vuelve a correrlo.

# Las carpetas Git no permiten crear __pycache__ ni cachés: que nadie lo intente.
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_ADDOPTS="-p no:cacheprovider"
export RUFF_CACHE_DIR=/tmp/ruff-cache

# uv usa PyPI, igual que la revisión automática de GitHub, e ignora la
# configuración que Databricks deja en /etc/uv (apunta a otro servidor de paquetes).
export UV_NO_CONFIG=1
export UV_LINK_MODE=copy
unset VIRTUAL_ENV

# El cómputo serverless empieza limpio en cada sesión: si falta uv, se instala.
if ! command -v uv >/dev/null 2>&1; then
    echo "Instalando uv (solo al empezar la sesión)..."
    (cd /tmp && pip install --quiet uv)
fi

# Cada proyecto tiene su entorno en /tmp/entornos, fuera de la carpeta Git.
uv() {
    local raiz="$PWD"
    while [ "$raiz" != "/" ] && [ ! -f "$raiz/pyproject.toml" ]; do
        raiz=$(dirname "$raiz")
    done
    UV_PROJECT_ENVIRONMENT="/tmp/entornos/$(basename "$raiz")" command uv "$@"
}
BLOQUE

# Si ya había un bloque del taller, se reemplaza; lo demás del archivo no se toca.
if [ -f "$destino" ]; then
    python3 - "$destino" "$inicio" "$fin" <<'PY'
import sys

ruta, inicio, fin = sys.argv[1:]
lineas = open(ruta).read().splitlines()
fuera, dentro = [], False
for linea in lineas:
    if linea == inicio:
        dentro = True
    elif linea == fin:
        dentro = False
    elif not dentro:
        fuera.append(linea)
with open(ruta, "w") as archivo:
    archivo.write("\n".join(fuera) + ("\n" if fuera else ""))
PY
fi

printf '%s\n%s\n%s\n' "$inicio" "$bloque" "$fin" >> "$destino"
echo "Listo: $destino"
echo "Cierra esta terminal (la X del panel) y abre una nueva para que tome los cambios."
