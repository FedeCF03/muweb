#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Levanta la landing en esta máquina SIN Docker: Gunicorn + Caddy.
# (Equivalente local del compose.yml)
#
#   ./scripts/serve-local.sh start     levanta gunicorn + caddy
#   ./scripts/serve-local.sh stop      los para
#   ./scripts/serve-local.sh restart
#   ./scripts/serve-local.sh status
#   ./scripts/serve-local.sh logs      sigue los logs
#
# La web queda en http://<IP-LAN>:80
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")/.."

ROOT="$(pwd)"
RUN_DIR="${ROOT}/.run"
VENV="${ROOT}/.venv"
HTTP_PORT="${HTTP_PORT:-80}"
WEB_PORT="${WEB_PORT:-8000}"
CADDY_BIN="${ROOT}/tools/caddy"

mkdir -p "${RUN_DIR}"

pid_of() { # pid_of <archivo de pid>
  [ -f "$1" ] && cat "$1" || true
}

is_running() {
  local pid
  pid="$(pid_of "$1")"
  [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null
}

start() {
  # --- Requisitos -------------------------------------------------------
  if [ ! -x "${VENV}/bin/gunicorn" ]; then
    echo "Falta el venv. Ejecutá: make setup" >&2
    exit 1
  fi
  if [ ! -x "${CADDY_BIN}" ]; then
    echo "==> Descargando Caddy"
    mkdir -p "${ROOT}/tools"
    local tag
    tag="$(curl -s https://api.github.com/repos/caddyserver/caddy/releases/latest \
      | grep -oP '"tag_name":\s*"\K[^"]+')"
    curl -sSL "https://github.com/caddyserver/caddy/releases/download/${tag}/caddy_${tag#v}_linux_amd64.tar.gz" \
      -o /tmp/caddy.tgz
    tar xzf /tmp/caddy.tgz -C "${ROOT}/tools" caddy
    chmod +x "${CADDY_BIN}"
    rm -f /tmp/caddy.tgz
  fi

  # --- Gunicorn ---------------------------------------------------------
  if is_running "${RUN_DIR}/web.pid"; then
    echo "La app ya está corriendo (pid $(pid_of "${RUN_DIR}/web.pid"))"
  else
    echo "==> Levantando Gunicorn en 127.0.0.1:${WEB_PORT}"
    (
      cd "${ROOT}"
      nohup "${VENV}/bin/gunicorn" \
        --bind "127.0.0.1:${WEB_PORT}" \
        --workers "${GUNICORN_WORKERS:-3}" \
        --threads 4 \
        --timeout 60 \
        --access-logfile "${RUN_DIR}/access.log" \
        --error-logfile "${RUN_DIR}/web.log" \
        "app:create_app()" > /dev/null 2>&1 &
      echo $! > "${RUN_DIR}/web.pid"
    )
    sleep 2
  fi

  # --- Caddy ------------------------------------------------------------
  # Para escuchar en puertos menores a 1024 hace falta el permiso
  # cap_net_bind_service (los puertos altos, tipo 8080, no lo necesitan).
  if [ "${HTTP_PORT}" -lt 1024 ]; then
    if ! sudo -n setcap cap_net_bind_service=+ep "${CADDY_BIN}" 2>/dev/null; then
      echo "    No se pudo dar permiso a caddy para el puerto ${HTTP_PORT}." >&2
      echo "    Usá un puerto alto:  HTTP_PORT=8080 $0 start" >&2
      exit 1
    fi
  fi

  if is_running "${RUN_DIR}/caddy.pid"; then
    echo "Caddy ya está corriendo (pid $(pid_of "${RUN_DIR}/caddy.pid"))"
  else
    echo "==> Levantando Caddy en el puerto ${HTTP_PORT}"
    (
      cd "${ROOT}"
      HTTP_PORT="${HTTP_PORT}" \
      WEB_UPSTREAM="127.0.0.1:${WEB_PORT}" \
      DOWNLOADS_DIR="${ROOT}/downloads" \
      nohup "${CADDY_BIN}" run --config "${ROOT}/docker/Caddyfile" --adapter caddyfile \
        > "${RUN_DIR}/caddy.log" 2>&1 &
      echo $! > "${RUN_DIR}/caddy.pid"
    )
    sleep 2
  fi

  local ip
  ip="$(ip -4 addr show scope global 2>/dev/null | grep -oP 'inet \K[\d.]+' | head -1)"
  echo
  echo "Listo:"
  echo "  http://localhost:${HTTP_PORT}/"
  [ -n "${ip}" ] && echo "  http://${ip}:${HTTP_PORT}/   (desde la LAN)"
}

stop() {
  for name in caddy web; do
    local pid
    pid="$(pid_of "${RUN_DIR}/${name}.pid")"
    if [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null; then
      kill "${pid}" 2>/dev/null || true
      echo "==> Parado ${name} (pid ${pid})"
    fi
    rm -f "${RUN_DIR}/${name}.pid"
  done
}

status() {
  echo "== Puertos =="
  ss -ltn 2>/dev/null | grep -E ":(${HTTP_PORT}|${WEB_PORT})\b" || echo "(nada escuchando)"
  echo
  echo "== Healthcheck =="
  curl -s "http://127.0.0.1:${HTTP_PORT}/healthz" || echo "sin respuesta"
  echo
}

case "${1:-start}" in
  start) start ;;
  stop) stop ;;
  restart) stop; sleep 1; start ;;
  status) status ;;
  logs) tail -f "${RUN_DIR}"/*.log ;;
  *) echo "Uso: $0 {start|stop|restart|status|logs}" >&2; exit 1 ;;
esac
