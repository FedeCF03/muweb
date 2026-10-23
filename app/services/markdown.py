"""Markdown -> HTML saneado. Lo usan los repositorios y el filtro de plantilla."""

from __future__ import annotations

import markdown
import nh3

_EXTENSIONS = ["extra", "sane_lists", "nl2br"]

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
    html = markdown.markdown(text, extensions=_EXTENSIONS)
    return nh3.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        url_schemes={"http", "https", "mailto"},
        link_rel=None,
        strip_comments=True,
    )
