"""Páginas públicas: home, descargas, FAQ, reglas."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, abort, render_template

from ..container import services
from ..services import schedule

bp = Blueprint("pages", __name__)


@bp.get("/")
def index():
    """Inicio del portal: bienvenida, novedades, clases, agenda y mapas."""
    s = services()
    now = datetime.now().astimezone()
    events = s.events.list()
    upcoming = schedule.next_event(events, now)
    return render_template(
        "index.html",
        title=None,
        news=s.news.list()[:3],
        downloads=s.downloads.catalog(),
        faq_preview=s.faq.list()[:4],
        classes=s.classes.list(),
        class_points=s.gameplay.get().get("class_points", {}),
        gallery=s.gallery.get(),
        events=events,
        events_note=s.events.timezone_note(),
        next_event=upcoming,
        next_event_at=schedule.event_starts_at(upcoming, now) if upcoming else None,
        today_index=now.weekday(),
    )


@bp.get("/descargas")
def downloads():
    return render_template("downloads.html", title="Descargas", downloads=services().downloads.catalog())


@bp.get("/jugabilidad")
def gameplay():
    s = services()
    return render_template(
        "gameplay.html",
        title="Jugabilidad",
        gameplay=s.gameplay.get(),
        classes=s.classes.list(),
    )


@bp.get("/faq")
def faq():
    return render_template("faq.html", title="Preguntas frecuentes", faq=services().faq.list())


@bp.get("/reglas")
def rules():
    page = services().pages.get("rules")
    if page is None:
        abort(404)
    return render_template("rules.html", title="Reglas", body=page.html, raw=page.body)
