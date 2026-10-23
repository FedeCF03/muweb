"""Repositorios de contenido sobre la base "muweb" (esquema en db/schema.sql)."""

from __future__ import annotations

from typing import Any

from ...models import Download, DownloadCatalog, NewsItem, Page
from ...models.content import InstallStep
from ...services.markdown import render_markdown
from .connection import Database


def _size_label(size_bytes: int | None) -> str:
    if not size_bytes:
        return ""
    mb = size_bytes / (1024 * 1024)
    return f"≈ {mb:.0f} MB" if mb >= 1 else f"≈ {size_bytes // 1024} KB"


class PgSiteRepository:
    """Ajustes del sitio en ``site_setting`` (key -> value JSON).

    Cada fila es una clave de primer nivel de site.yml ("name", "hero",
    "rates"...). Lo que falte en la base se completa con ``fallback`` (el
    repositorio de archivos), así se puede migrar de a poco.
    """

    def __init__(self, db: Database, fallback: Any | None = None) -> None:
        self.db = db
        self.fallback = fallback

    def get(self) -> dict[str, Any]:
        site: dict[str, Any] = self.fallback.get() if self.fallback else {}
        for row in self.db.fetch_all("SELECT key, value FROM site_setting"):
            site[row["key"]] = row["value"]
        return site


class PgNewsRepository:
    _COLUMNS = "slug, title, excerpt, body_md, tag, published_at"

    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def _to_model(row: dict[str, Any]) -> NewsItem:
        body = row["body_md"] or ""
        return NewsItem(
            slug=row["slug"],
            title=row["title"],
            date=row["published_at"].date(),
            tag=row["tag"] or "",
            excerpt=row["excerpt"] or "",
            body=body,
            html=render_markdown(body),
        )

    def list(self) -> list[NewsItem]:
        rows = self.db.fetch_all(
            f"SELECT {self._COLUMNS} FROM news WHERE published_at <= now() "
            "ORDER BY published_at DESC, slug DESC"
        )
        return [self._to_model(r) for r in rows]

    def get(self, slug: str) -> NewsItem | None:
        row = self.db.fetch_one(
            f"SELECT {self._COLUMNS} FROM news WHERE slug = %s AND published_at <= now()", (slug,)
        )
        return self._to_model(row) if row else None


class PgPageRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def get(self, slug: str) -> Page | None:
        row = self.db.fetch_one("SELECT slug, body_md FROM page WHERE slug = %s AND visible", (slug,))
        if not row:
            return None
        return Page(slug=row["slug"], body=row["body_md"], html=render_markdown(row["body_md"]))

    def slugs(self) -> list[str]:
        return [r["slug"] for r in self.db.fetch_all("SELECT slug FROM page WHERE visible ORDER BY slug")]


class PgDownloadRepository:
    """Descargas en la tabla ``download``. Requisitos e instrucciones siguen
    saliendo de ``fallback`` (downloads.yml) hasta que tengan tabla propia."""

    def __init__(self, db: Database, fallback: Any | None = None) -> None:
        self.db = db
        self.fallback = fallback

    def catalog(self) -> DownloadCatalog:
        rows = self.db.fetch_all(
            "SELECT key, name, kind, version, size_bytes, file, sha256, available, note "
            "FROM download ORDER BY sort_order, id"
        )
        base = self.fallback.catalog() if self.fallback else DownloadCatalog()
        items = [
            Download(
                id=r["key"],
                name=r["name"],
                kind=r["kind"] or "",
                version=r["version"] or "",
                size=_size_label(r["size_bytes"]),
                note=r["note"] or "",
                file=r["file"],
                sha256=r["sha256"],
                available=bool(r["available"]),
            )
            for r in rows
        ]
        return DownloadCatalog(
            items=items,
            requirements=base.requirements,
            instructions=[InstallStep(s.title, s.text) for s in base.instructions],
        )
