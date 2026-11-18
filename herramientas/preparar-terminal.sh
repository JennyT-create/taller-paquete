# Prepara la terminal web de Databricks para trabajar con uv, pytest y ruff.
#
# Córrelo una sola vez, desde la raíz del repositorio y con source (no con bash):
#     source herramientas/preparar-terminal.sh
#
# Escribe un bloque en el .bashrc de tu carpeta de usuario del workspace, que Databricks
# lee cada vez que abre una terminal nueva, y lo carga también en la terminal donde
# estás: no hace falta cerrarla ni abrir otra.
#
# Con source, el script corre dentro de tu terminal. Por eso todo va en una función que
# devuelve un error en vez de salir: si algo falla, tu terminal sigue abierta.

if ! (return 0 2>/dev/null); then
    echo "Córrelo con source, no con bash:"
    echo "    source herramientas/preparar-terminal.sh"
    exit 1
fi

_preparar_terminal() {
    local usuario destino bloque
    local inicio="# >>> taller MLOps >>>"
    local fin="# <<< taller MLOps <<<"

    # Tu usuario se lo preguntamos a Databricks: así nadie escribe su correo.
    usuario=$(databricks current-user me --output json 2>/dev/null |
        python3 -c 'import json, sys; print(json.load(sys.stdin)["userName"])' 2>/dev/null)
    if [ -z "$usuario" ]; then
        echo "No pude saber tu usuario de Databricks. ¿Estás en la terminal web de Databricks?"
        return 1
    fi
    destino="/Workspace/Users/${usuario}/.bashrc"

    read -r -d '' bloque <<'BLOQUE'
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

# Dentro de un proyecto, su entorno va en /tmp/entornos, fuera de la carpeta Git.
# Fuera de un proyecto, uv funciona como siempre.
uv() {
    local raiz="$PWD"
    while [ "$raiz" != "/" ] && [ ! -f "$raiz/pyproject.toml" ]; do
        raiz=$(dirname "$raiz")
    done
    if [ -f "$raiz/pyproject.toml" ]; then
        UV_PROJECT_ENVIRONMENT="/tmp/entornos/$(basename "$raiz")" command uv "$@"
    else
        command uv "$@"
    fi
}
BLOQUE

    # Si ya había un bloque del taller, se reemplaza; lo demás del archivo no se toca.
    if [ -f "$destino" ]; then
        python3 - "$destino" "$inicio" "$fin" <<'PY' || return 1
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

    printf '%s\n%s\n%s\n' "$inicio" "$bloque" "$fin" >> "$destino" || return 1

    # Y se carga ya, en esta terminal.
    # shellcheck source=/dev/null
    source "$destino"
    echo "Listo: la terminal está preparada, esta y las que abras desde ahora."
}

_preparar_terminal
unset -f _preparar_terminal
