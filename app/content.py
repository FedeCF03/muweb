"""Capa de contenido.

En la v0 no hay base de datos: el contenido vive en archivos YAML y Markdown
dentro de ``content/``. Las funciones públicas de este módulo (load_site,
load_news, load_downloads, load_faq, load_page) son el contrato que en la v1 va
a implementar un repositorio de base de datos, sin tocar las plantillas.

El cache se invalida solo: si cambia el mtime de un archivo, se vuelve a leer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

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
    return _cached(path, lambda: _read_yaml(path))

def load_downloads() -> dict[str, Any]:
    """Descargas, requisitos e instrucciones de instalación."""
    path = content_dir() / "downloads.yml"
    return _cached(path, lambda: _read_yaml(path))

def load_faq() -> list[dict[str, str]]:
    """Preguntas frecuentes."""
    path = content_dir() / "faq.yml"
    data = _cached(path, lambda: _read_yaml(path))
    return list(data.get("items", []))

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
        "faq": len(load_faq()),
        "paginas": [p.stem for p in sorted(content_dir().glob("*.md"))],
    }
