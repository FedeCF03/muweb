"""Resumen del contenido, para el comando ``flask check-content``."""

from __future__ import annotations

from typing import Any


def summary(s: Any) -> dict[str, Any]:
    """Carga todo lo publicable: si algo está mal escrito, falla acá."""
    return {
        "backend": s.backend,
        "site": s.site.get().get("name", "?"),
        "noticias": len(s.news.list()),
        "descargas": len(s.downloads.catalog().items),
        "clases": len(s.classes.list()),
        "galeria": len(s.gallery.get().items),
        "eventos": len(s.events.list()),
        "faq": len(s.faq.list()),
        "paginas": s.pages.slugs(),
    }
