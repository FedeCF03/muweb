"""Blueprint público: la landing y las páginas de contenido."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, current_app, render_template, request

from ..content import (
    event_starts_at,
    get_news,
    load_classes,
    load_downloads,
    load_events,
    load_events_note,
    load_faq,
    load_gallery,
    load_news,
    load_page,
    load_site,
    next_event,
)

bp = Blueprint("public", __name__)


@bp.get("/")
def index():
    """Landing principal."""
    upcoming = next_event()
    return render_template(
        "index.html",
        title=None,
        news=load_news()[:3],
        downloads=load_downloads(),
        faq_preview=load_faq()[:4],
        classes=load_classes(),
        gallery=load_gallery(),
        events=load_events(),
        events_note=load_events_note(),
        next_event=upcoming,
        next_event_at=event_starts_at(upcoming) if upcoming else None,
        today_index=datetime.now().astimezone().weekday(),
    )


@bp.get("/noticias")
def news_list():
    """Listado de noticias."""
    return render_template("news_list.html", title="Noticias", news=load_news())


@bp.get("/noticias/<slug>")
def news_detail(slug: str):
    """Detalle de una noticia."""
    item = get_news(slug)
    if item is None:
        return render_template("404.html", title="Noticia no encontrada"), 404
    return render_template("news_detail.html", title=item.title, item=item)


@bp.get("/descargas")
def downloads():
    """Descargas del cliente."""
    return render_template("downloads.html", title="Descargas", downloads=load_downloads())


@bp.get("/faq")
def faq():
    """Preguntas frecuentes."""
    return render_template("faq.html", title="Preguntas frecuentes", faq=load_faq())


@bp.get("/reglas")
def rules():
    """Reglas del server."""
    raw, html = load_page("rules")
    return render_template("rules.html", title="Reglas", body=html, raw=raw)


@bp.get("/registro")
def register():
    """Formulario de registro.

    En la v0 no hay base de datos: el formulario se muestra deshabilitado y
    queda listo para conectarse en la v1 (ver docs/v1-db.md).
    """
    return render_template("register.html", title="Crear cuenta")


@bp.post("/registro")
def register_post():
    """Recepción del formulario. En la v0 responde 503 (aún no hay cuentas)."""
    return (
        render_template(
            "register.html",
            title="Crear cuenta",
            error="El registro por web todavía no está disponible.",
        ),
        503,
    )


@bp.get("/sitemap.xml")
def sitemap():
    """Sitemap para buscadores."""
    pages = [
        ("/", 1.0),
        ("/noticias", 0.8),
        ("/descargas", 0.9),
        ("/faq", 0.6),
        ("/reglas", 0.6),
    ]
    base = request.url_root.rstrip("/")
    urls = "\n".join(
        f"  <url><loc>{base}{path}</loc><priority>{priority}</priority></url>"
        for path, priority in pages
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    return xml, 200, {"Content-Type": "application/xml; charset=utf-8"}


@bp.app_context_processor
def _template_globals():
    """Datos que usan varias plantillas (footer, header)."""
    site = load_site()
    server = site.get("server", {})
    return {
        "server_info": server,
        "discord_url": server.get("discord_url", "#"),
        "downloads_dir": current_app.config.get("DOWNLOADS_DIR"),
    }
