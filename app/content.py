"""Capa de contenido.

En la v0 no hay base de datos: el contenido vive en archivos YAML y Markdown
dentro de ``content/``. Las funciones públicas de este módulo (load_site,
load_news, load_downloads, load_faq, load_page) son el contrato que en la v1 va
a implementar un repositorio de base de datos, sin tocar las plantillas.

El cache se invalida solo: si cambia el mtime de un archivo, se vuelve a leer.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import markdown
import nh3
import yaml

from .config import DEFAULT_CONTENT_DIR

# --- Markdown -----------------------------------------------------------------

_MARKDOWN = markdown.Markdown(
    extensions=["extra", "sane_lists", "nl2br"],
    output_format="html",
)

_ALLOWED_TAGS = {
    "p", "br", "hr", "strong", "em", "b", "i", "u", "s", "code", "pre", "blockquote",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "a", "img", "table", "thead", "tbody", "tr", "th", "td",
    "span", "div", "figure", "figcaption",
}

_ALLOWED_ATTRS = {
    "a": {"href", "title", "rel", "target"},
    "img": {"src", "alt", "title", "width", "height"},
    "code": {"class"},
    "span": {"class"},
    "div": {"class"},
}

def render_markdown(text: str) -> str:
    """Convierte Markdown a HTML y lo sanea (nada de HTML arbitrario)."""
    if not text:
        return ""
    html = markdown.markdown(text, extensions=["extra", "sane_lists", "nl2br"])
    return nh3.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        url_schemes={"http", "https", "mailto"},
        link_rel=None,
        strip_comments=True,
    )

# --- Lectura de archivos ------------------------------------------------------

def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} debería contener un diccionario YAML")
    return data

_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)

def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Separa el front matter (YAML entre --- ---) del cuerpo en Markdown."""
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    return (meta if isinstance(meta, dict) else {}), text[match.end() :]

# --- Cache por mtime ----------------------------------------------------------

_cache: dict[str, tuple[float, Any]] = {}

def _cached(path: Path, loader, *, stamp: float | None = None):
    """Cachea el resultado de ``loader`` invalidándolo cuando cambia el mtime."""
    key = str(path)
    current = stamp if stamp is not None else (path.stat().st_mtime if path.exists() else 0.0)
    hit = _cache.get(key)
    if hit is not None and hit[0] == current:
        return hit[1]
    value = loader()
    _cache[key] = (current, value)
    return value

def _dir_stamp(directory: Path, pattern: str = "*") -> float:
    """Sello temporal de un directorio: el mtime más reciente de sus archivos."""
    if not directory.exists():
        return 0.0
    stamps = [p.stat().st_mtime for p in directory.glob(pattern) if p.is_file()]
    return max(stamps) if stamps else 0.0

# --- Modelos ------------------------------------------------------------------

@dataclass(frozen=True)
class NewsItem:
    """Una noticia publicada."""

    slug: str
    title: str
    date: date
    tag: str
    excerpt: str
    body: str
    html: str

    @property
    def iso_date(self) -> str:
        return self.date.isoformat()


@dataclass(frozen=True)
class ClassInfo:
    """Una clase del juego, para las tarjetas de la sección de clases."""

    key: str
    name: str
    role: str
    icon: str
    accent: str
    description: str
    stats: dict[str, int]
    requirement: str | None


@dataclass(frozen=True)
class EventItem:
    """Un evento recurrente de la agenda semanal."""

    name: str
    day: str
    day_index: int
    time: str
    hour: int
    minute: int
    duration: str

# --- Contenido ----------------------------------------------------------------

def content_dir() -> Path:
    """Directorio de contenido configurado en la app (o el de por defecto)."""
    from flask import current_app, has_app_context

    if has_app_context():
        return Path(current_app.config.get("CONTENT_DIR", DEFAULT_CONTENT_DIR))
    return DEFAULT_CONTENT_DIR

def load_site() -> dict[str, Any]:
    """Datos generales del sitio (nombre, rates, hero, features, etc.)."""
    path = content_dir() / "site.yml"
    site = _cached(path, lambda: _read_yaml(path))
    # El host del Connect Server no se versiona: viene del entorno (.env)
    server = site.setdefault("server", {})
    server["connect_host"] = os.environ.get("CONNECT_HOST", "127.0.0.1")
    return site

def load_downloads() -> dict[str, Any]:
    """Descargas, requisitos e instrucciones de instalación."""
    path = content_dir() / "downloads.yml"
    return _cached(path, lambda: _read_yaml(path))

def load_faq() -> list[dict[str, str]]:
    """Preguntas frecuentes."""
    path = content_dir() / "faq.yml"
    data = _cached(path, lambda: _read_yaml(path))
    return list(data.get("items", []))


def load_classes() -> list[ClassInfo]:
    """Clases del juego, para las tarjetas de la sección de clases."""
    path = content_dir() / "classes.yml"
    data = _cached(path, lambda: _read_yaml(path))
    items: list[ClassInfo] = []
    for raw in data.get("classes", []):
        stats = {str(k): int(v) for k, v in (raw.get("stats") or {}).items()}
        items.append(
            ClassInfo(
                key=str(raw.get("key", "")),
                name=str(raw.get("name", "")),
                role=str(raw.get("role", "")),
                icon=str(raw.get("icon", "spark")),
                accent=str(raw.get("accent", "#d6b25e")),
                description=str(raw.get("description", "")),
                stats=stats,
                requirement=str(raw["requirement"]) if raw.get("requirement") else None,
            )
        )
    return items


def load_gallery() -> dict[str, Any]:
    """Galería de mapas (nota + tarjetas)."""
    path = content_dir() / "gallery.yml"
    return _cached(path, lambda: _read_yaml(path))


WEEKDAYS_ES = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "miércoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "sábado": 5,
    "domingo": 6,
}


def _parse_time(value: Any) -> tuple[int, int]:
    """"21:30" -> (21, 30). Tolerante a formatos raros."""
    text = str(value or "0:0")
    hours, _, minutes = text.partition(":")
    try:
        return int(hours), int(minutes or 0)
    except ValueError:
        return 0, 0


def _events_raw() -> dict[str, Any]:
    """Archivo completo de la agenda (nota de zona horaria + eventos)."""
    path = content_dir() / "events.yml"
    return _cached(path, lambda: _read_yaml(path))


def load_events_note() -> str:
    """Nota sobre la zona horaria de la agenda."""
    return str(_events_raw().get("timezone_note", ""))


def load_events() -> list[EventItem]:
    """Agenda de eventos recurrentes, ordenada por día y hora."""
    data = _events_raw()
    items: list[EventItem] = []
    for raw in data.get("events", []):
        day = str(raw.get("day", ""))
        day_index = WEEKDAYS_ES.get(day.strip().lower())
        if day_index is None:
            continue
        hour, minute = _parse_time(raw.get("time"))
        items.append(
            EventItem(
                name=str(raw.get("name", "")),
                day=day,
                day_index=day_index,
                time=str(raw.get("time", "")),
                hour=hour,
                minute=minute,
                duration=str(raw.get("duration", "")),
            )
        )
    items.sort(key=lambda ev: (ev.day_index, ev.hour, ev.minute))
    return items


def next_event(now: datetime | None = None) -> EventItem | None:
    """El evento más cercano en el tiempo a partir de ``now``."""
    now = now or datetime.now()
    if not now.tzinfo:
        now = now.astimezone()

    def starts_at(event: EventItem) -> datetime:
        candidate = now.replace(hour=event.hour, minute=event.minute, second=0, microsecond=0)
        days_ahead = (event.day_index - now.weekday()) % 7
        candidate += timedelta(days=days_ahead)
        if candidate <= now:
            candidate += timedelta(days=7)
        return candidate

    events = load_events()
    return min(events, key=starts_at) if events else None


def event_starts_at(event: EventItem, now: datetime | None = None) -> datetime:
    """Fecha y hora de la próxima edición de un evento (para el countdown)."""
    now = now or datetime.now()
    if not now.tzinfo:
        now = now.astimezone()
    candidate = now.replace(hour=event.hour, minute=event.minute, second=0, microsecond=0)
    days_ahead = (event.day_index - now.weekday()) % 7
    candidate += timedelta(days=days_ahead)
    if candidate <= now:
        candidate += timedelta(days=7)
    return candidate

def load_page(name: str) -> tuple[str, str]:
    """Página en Markdown. Devuelve (markdown crudo, html)."""
    path = content_dir() / f"{name}.md"
    raw = _cached(path, lambda: path.read_text(encoding="utf-8") if path.exists() else "")
    return raw, render_markdown(raw)

def load_news() -> list[NewsItem]:
    """Todas las noticias, de la más reciente a la más antigua."""
    directory = content_dir() / "news"
    stamp = _dir_stamp(directory, "*.md")

    def loader() -> list[NewsItem]:
        items: list[NewsItem] = []
        for path in sorted(directory.glob("*.md")):
            meta, body = _split_front_matter(path.read_text(encoding="utf-8"))
            raw_date = meta.get("date")
            if isinstance(raw_date, date):
                published = raw_date
            else:
                try:
                    published = date.fromisoformat(str(raw_date))
                except (TypeError, ValueError):
                    published = date.fromtimestamp(path.stat().st_mtime)
            items.append(
                NewsItem(
                    slug=path.stem,
                    title=str(meta.get("title", path.stem)),
                    date=published,
                    tag=str(meta.get("tag", "")),
                    excerpt=str(meta.get("excerpt", "")),
                    body=body.strip(),
                    html=render_markdown(body),
                )
            )
        items.sort(key=lambda item: (item.date, item.slug), reverse=True)
        return items

    return _cached(directory, loader, stamp=stamp)

def get_news(slug: str) -> NewsItem | None:
    """Busca una noticia por su slug."""
    return next((item for item in load_news() if item.slug == slug), None)

def content_summary() -> dict[str, Any]:
    """Resumen del contenido, para el comando ``flask check-content``."""
    site = load_site()
    return {
        "site": site.get("name", "?"),
        "noticias": len(load_news()),
        "descargas": len(load_downloads().get("items", [])),
        "clases": len(load_classes()),
        "galeria": len(load_gallery().get("items", [])),
        "eventos": len(load_events()),
        "faq": len(load_faq()),
        "paginas": [p.stem for p in sorted(content_dir().glob("*.md"))],
    }
