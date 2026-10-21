#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Compila el CSS (Tailwind v4) sin necesidad de Node.
#
#   ./scripts/build-css.sh            compila una vez
#   ./scripts/build-css.sh --watch    recompila al guardar
#
# El binario de Tailwind se descarga en tools/ (no se versiona).
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")/.."

TOOLS_DIR="tools"
BIN="${TOOLS_DIR}/tailwindcss"
VERSION="${TAILWIND_VERSION:-v4.3.3}"
INPUT="src/app.css"
OUTPUT="app/static/css/app.css"

if [ ! -x "${BIN}" ]; then
  echo "==> Descargando Tailwind CLI ${VERSION}"
  mkdir -p "${TOOLS_DIR}"
  curl -sSL -o "${BIN}" \
    "https://github.com/tailwindlabs/tailwindcss/releases/download/${VERSION}/tailwindcss-linux-x64"
  chmod +x "${BIN}"
fi

if [ "${1:-}" = "--watch" ]; then
  echo "==> Compilando en modo watch (Ctrl+C para salir)"
  exec "${BIN}" -i "${INPUT}" -o "${OUTPUT}" --watch
fi

echo "==> Compilando ${INPUT} -> ${OUTPUT}"
"${BIN}" -i "${INPUT}" -o "${OUTPUT}" --minify
echo "==> Listo: $(du -h "${OUTPUT}" | cut -f1)"
