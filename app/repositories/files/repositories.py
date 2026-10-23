"""Implementación de los repositorios sobre archivos de ``content/``."""

from __future__ import annotations

import copy
from datetime import date
from typing import Any

from ...models import (
    ClassInfo,
    Download,
    DownloadCatalog,
    EventItem,
    FaqItem,
    Gallery,
    MapEntry,
    NewsItem,
    Page,
)
from ...models.content import InstallStep
from ...services.markdown import render_markdown
from .storage import FileStore, split_front_matter

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


DAILY = {"todos los días", "todos los dias", "diario", "todos"}
DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def _parse_time(value: Any) -> tuple[int, int]:
    """"21:30" -> (21, 30). Tolerante a formatos raros."""
    hours, _, minutes = str(value or "0:0").partition(":")
    try:
        return int(hours), int(minutes or 0)
    except ValueError:
        return 0, 0


def _optional(value: Any) -> str | None:
    return str(value) if value not in (None, "") else None


class FileSiteRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def get(self) -> dict[str, Any]:
        # Copia para que nadie modifique el dict cacheado. La dirección del
        # Connect Server no se agrega nunca: la web no expone la red del server.
        site = copy.deepcopy(self.store.yaml("site.yml"))
        server = site.setdefault("server", {})
        for key in ("connect_host", "connect_port", "host", "ip", "port"):
            server.pop(key, None)
        return site


class FileNewsRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def list(self) -> list[NewsItem]:
        directory = self.store.path("news")

        def load() -> list[NewsItem]:
            items: list[NewsItem] = []
            for path in sorted(directory.glob("*.md")):
                meta, body = split_front_matter(path.read_text(encoding="utf-8"))
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

        return self.store.cached(directory, load, stamp=self.store.dir_stamp(directory, "*.md"))

    def get(self, slug: str) -> NewsItem | None:
        return next((item for item in self.list() if item.slug == slug), None)


class FilePageRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def get(self, slug: str) -> Page | None:
        if not self.store.path(f"{slug}.md").exists():
            return None
        raw = self.store.text(f"{slug}.md")
        return Page(slug=slug, body=raw, html=render_markdown(raw))

    def slugs(self) -> list[str]:
        return [p.stem for p in sorted(self.store.root.glob("*.md"))]


class FileDownloadRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def catalog(self) -> DownloadCatalog:
        data = self.store.yaml("downloads.yml")
        items = [
            Download(
                id=str(raw.get("id", "")),
                name=str(raw.get("name", "")),
                kind=str(raw.get("kind") or ""),
                version=str(raw.get("version") or ""),
                size=str(raw.get("size") or ""),
                note=str(raw.get("note", "") or ""),
                file=_optional(raw.get("file")),
                sha256=_optional(raw.get("sha256")),
                available=bool(raw.get("available", False)),
            )
            for raw in data.get("items", [])
        ]
        return DownloadCatalog(
            items=items,
            requirements=[str(r) for r in data.get("requirements", [])],
            instructions=[
                InstallStep(title=str(s.get("title", "")), text=str(s.get("text", "")))
                for s in data.get("instructions", [])
            ],
        )


class FileFaqRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def list(self) -> list[FaqItem]:
        return [
            FaqItem(question=str(raw.get("question", "")), answer=str(raw.get("answer", "")))
            for raw in self.store.yaml("faq.yml").get("items", [])
        ]


class FileClassRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def list(self) -> list[ClassInfo]:
        items: list[ClassInfo] = []
        for raw in self.store.yaml("classes.yml").get("classes", []):
            stats = {str(k): int(v) for k, v in (raw.get("stats") or {}).items()}
            items.append(
                ClassInfo(
                    key=str(raw.get("key", "")),
                    name=str(raw.get("name", "")),
                    role=str(raw.get("role", "")),
                    icon=str(raw.get("icon", "spark")),
                    accent=str(raw.get("accent", "#7cff9e")),
                    description=str(raw.get("description", "")),
                    stats=stats,
                    requirement=_optional(raw.get("requirement")),
                )
            )
        return items


class FileGalleryRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def get(self) -> Gallery:
        data = self.store.yaml("gallery.yml")
        return Gallery(
            note=str(data.get("note", "")),
            items=[
                MapEntry(
                    map=str(raw.get("map", "")),
                    level=str(raw.get("level", "")),
                    tag=str(raw.get("tag", "")),
                    palette=str(raw.get("palette", "plains")),
                    image=_optional(raw.get("image")),
                )
                for raw in data.get("items", [])
            ],
        )


class FileGameplayRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def get(self) -> dict[str, Any]:
        return copy.deepcopy(self.store.yaml("gameplay.yml"))


class FileEventRepository:
    def __init__(self, store: FileStore) -> None:
        self.store = store

    def list(self) -> list[EventItem]:
        items: list[EventItem] = []
        for raw in self.store.yaml("events.yml").get("events", []):
            day = str(raw.get("day", ""))
            key = day.strip().lower()
            daily = key in DAILY
            indexes = list(range(7)) if daily else [WEEKDAYS_ES.get(key)]
            if indexes == [None]:
                continue
            hour, minute = _parse_time(raw.get("time"))
            for day_index in indexes:
                items.append(
                    EventItem(
                        name=str(raw.get("name", "")),
                        day=DAY_NAMES[day_index] if daily else day,
                        day_index=day_index,
                        time=str(raw.get("time", "")),
                        hour=hour,
                        minute=minute,
                        duration=str(raw.get("duration", "")),
                        daily=daily,
                    )
                )
        items.sort(key=lambda ev: (ev.day_index, ev.hour, ev.minute))
        return items

    def timezone_note(self) -> str:
        return str(self.store.yaml("events.yml").get("timezone_note", ""))
