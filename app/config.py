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
    CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", DEFAULT_CONTENT_DIR))
    DOWNLOADS_DIR = Path(os.environ.get("DOWNLOADS_DIR", DEFAULT_DOWNLOADS_DIR))

    # --- Flags de funcionalidad ---
    # v0: todo estático. La v1 enciende el registro y el estado real del server.
    FEATURE_REGISTRATION = flag("FEATURE_REGISTRATION", False)
    FEATURE_STATUS = flag("FEATURE_STATUS", False)

    # --- v1: base de datos (ver docs/v1-db.md) ---
    DATABASE_URL = os.environ.get("DATABASE_URL")
    OPENMU_DATABASE_URL = os.environ.get("OPENMU_DATABASE_URL")

    # --- Seguridad del formulario (para la v1) ---
    WTF_CSRF_TIME_LIMIT = 3600
