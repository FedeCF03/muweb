"""Aplicación Flask (landing de MU Online).

Uso:

    from app import create_app
    app = create_app()

o, más cómodo, con el CLI de Flask:

    flask --app app run
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_wtf.csrf import CSRFProtect

from .config import BASE_DIR, Config
from .content import content_summary, render_markdown

__all__ = ["create_app", "Config"]

# Navegación principal del header
NAV_ITEMS = [
    ("Inicio", "/"),
    ("Noticias", "/noticias"),
    ("Descargas", "/descargas"),
    ("FAQ", "/faq"),
    ("Reglas", "/reglas"),
]


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Crea y configura la aplicación."""
    load_dotenv(BASE_DIR / ".env")

    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    csrf = CSRFProtect(app)

    # --- Blueprints ---------------------------------------------------------
    from .blueprints.public import bp as public_bp

    app.register_blueprint(public_bp)

    # --- Filtros y helpers de plantilla ------------------------------------
    @app.template_filter("markdown")
    def _markdown(text: str) -> str:
        return render_markdown(text)

    @app.template_filter("date_es")
    def _date_es(value: datetime | None) -> str:
        if value is None:
            return ""
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        return f"{value.day} de {meses[value.month - 1]} de {value.year}"

    # --- Contexto global de las plantillas ----------------------------------
    @app.context_processor
    def _inject_globals():
        from .content import load_site

        site = load_site()
        return {
            "site": site,
            "nav_items": NAV_ITEMS,
            "current_year": datetime.now(timezone.utc).year,
            "feature_registration": app.config.get("FEATURE_REGISTRATION", False),
            "feature_status": app.config.get("FEATURE_STATUS", False),
        }

    # --- Errores ------------------------------------------------------------
    @app.errorhandler(404)
    def _not_found(error):
        return render_template("404.html", title="Página no encontrada"), 404

    @app.errorhandler(500)
    def _server_error(error):
        return render_template("500.html", title="Error del servidor"), 500

    # --- Healthcheck --------------------------------------------------------
    @app.get("/healthz")
    def _healthz():
        return jsonify(
            {
                "status": "ok",
                "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "registration": app.config.get("FEATURE_REGISTRATION", False),
            }
        )

    # --- CLI ----------------------------------------------------------------
    @app.cli.command("check-content")
    def _check_content():
        """Valida que el contenido YAML/Markdown cargue bien."""
        summary = content_summary()
        click_echo = __import__("click").echo
        click_echo("Contenido OK:")
        for key, value in summary.items():
            click_echo(f"  {key}: {value}")

    # Silencia el warning de CSRF en los endpoints que no usan formularios.
    @csrf.exempt
    @app.get("/robots.txt")
    def _robots():
        return (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /registro\n"
            "Sitemap: /sitemap.xml\n",
            200,
            {"Content-Type": "text/plain; charset=utf-8"},
        )

    return app
