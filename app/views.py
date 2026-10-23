"""Capa de vista (la "V" de MVC): las plantillas viven en app/templates;
acá están los filtros, el contexto común y las páginas de error."""

from __future__ import annotations

from datetime import date, datetime, timezone

from flask import Flask, render_template

from .container import services
from .services.markdown import render_markdown

# Navegación principal del header
NAV_ITEMS = [
    ("Inicio", "/"),
    ("Noticias", "/noticias"),
    ("Jugabilidad", "/jugabilidad"),
    ("Descargas", "/descargas"),
    ("FAQ", "/faq"),
    ("Reglas", "/reglas"),
]

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def date_es(value: date | datetime | None) -> str:
    if value is None:
        return ""
    return f"{value.day} de {MESES[value.month - 1]} de {value.year}"


def register_views(app: Flask) -> None:
    app.add_template_filter(render_markdown, "markdown")
    app.add_template_filter(date_es, "date_es")

    @app.context_processor
    def _globals():
        svc = services()
        site = svc.site.get()
        server = site.get("server", {})
        return {
            "site": site,
            "server_status": svc.status.current(site),
            "server_info": server,
            "discord_url": server.get("discord_url", "#"),
            "nav_items": NAV_ITEMS,
            "current_year": datetime.now(timezone.utc).year,
            "feature_registration": app.config.get("FEATURE_REGISTRATION", False),
            "feature_status": app.config.get("FEATURE_STATUS", False),
        }

    @app.errorhandler(404)
    def _not_found(error):
        return render_template("404.html", title="Página no encontrada"), 404

    @app.errorhandler(500)
    def _server_error(error):
        return render_template("500.html", title="Error del servidor"), 500
