"""Configuración de la aplicación, leída del entorno (archivo .env)."""

from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONTENT_DIR = BASE_DIR / "content"
DEFAULT_DOWNLOADS_DIR = BASE_DIR / "downloads"


def flag(name: str, default: bool = False) -> bool:
    """Lee un booleano del entorno: 1/true/yes/on activan el flag."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Valores por defecto. Se pueden pisar pasando un dict a create_app()."""

    # --- Flask ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-cambiar-esta-clave")
    SESSION_COOKIE_SECURE = flag("COOKIE_SECURE", False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 64 * 1024  # 64 KB alcanza para un formulario

    # --- Rutas ---
    # Las rutas relativas del .env se resuelven desde la raíz del proyecto
    CONTENT_DIR = BASE_DIR / os.environ.get("CONTENT_DIR", str(DEFAULT_CONTENT_DIR))
    DOWNLOADS_DIR = BASE_DIR / os.environ.get("DOWNLOADS_DIR", str(DEFAULT_DOWNLOADS_DIR))

    # --- Flags de funcionalidad ---
    # v0: todo estático. La v1 enciende el registro y el estado real del server.
    FEATURE_REGISTRATION = flag("FEATURE_REGISTRATION", False)
    FEATURE_STATUS = flag("FEATURE_STATUS", False)

    # --- Backend de datos ---
    # "files": YAML/Markdown en content/ (v0).
    # "db": noticias, descargas, páginas y ajustes desde Postgres (v1); lo que
    #       todavía no tiene tabla (clases, agenda, galería, FAQ) sigue en archivos.
    CONTENT_BACKEND = os.environ.get("CONTENT_BACKEND", "files").strip().lower()

    # --- v1: base de datos (ver docs/v1-db.md) ---
    DATABASE_URL = os.environ.get("DATABASE_URL")
    OPENMU_DATABASE_URL = os.environ.get("OPENMU_DATABASE_URL")
    # Solo después de verificar el INSERT en "Account" contra OpenMU (docs/v1-db.md §5)
    OPENMU_WRITES_VERIFIED = flag("OPENMU_WRITES_VERIFIED", False)

    # --- Estado en vivo del server (FEATURE_STATUS=1) ---
    CONNECT_PORT = int(os.environ.get("CONNECT_PORT", "44405"))

    # --- Seguridad del formulario (para la v1) ---
    WTF_CSRF_TIME_LIMIT = 3600
