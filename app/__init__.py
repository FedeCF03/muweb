"""Aplicación Flask (landing de MU Online), organizada en MVC.

    app/models/        modelos del dominio (dataclasses)
    app/repositories/  acceso a datos: files (v0) y postgres (v1)
    app/services/      reglas de negocio (agenda, tablero, cuentas, estado)
    app/controllers/   blueprints: reciben la request y eligen la vista
    app/views.py       filtros, contexto común y errores de las plantillas
    app/templates/     vistas Jinja
    app/container.py   arma repositorios y servicios según la config

Uso:

    from app import create_app
    app = create_app()

o con el CLI de Flask:

    flask --app app run
"""

from __future__ import annotations

from typing import Any

import click
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from . import container
from .config import BASE_DIR, Config
from .controllers import register_controllers
from .services import content_check
from .views import register_views

__all__ = ["create_app", "Config"]


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Crea y configura la aplicación."""
    load_dotenv(BASE_DIR / ".env")

    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    csrf = CSRFProtect(app)
    container.init_app(app)
    register_controllers(app)
    register_views(app)

    # Endpoints sin formularios: no necesitan token CSRF
    for endpoint in ("system.healthz", "system.robots", "system.sitemap"):
        csrf.exempt(app.view_functions[endpoint])

    @app.cli.command("check-content")
    def _check_content():
        """Valida que el contenido cargue bien desde el backend configurado."""
        click.echo("Contenido OK:")
        for key, value in content_check.summary(container.services()).items():
            click.echo(f"  {key}: {value}")

    return app
