"""Modelos de contenido: noticias, descargas, clases, agenda, mapas, FAQ."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


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
class Page:
    """Página de texto en Markdown (reglas, etc.)."""

    slug: str
    body: str
    html: str


@dataclass(frozen=True)
class Download:
    """Un archivo descargable (cliente, parche, launcher)."""

    id: str
    name: str
    kind: str
    version: str
    size: str
    note: str
    file: str | None = None
    sha256: str | None = None
    available: bool = False

    @property
    def ready(self) -> bool:
        """Se puede descargar: está habilitado y tiene archivo."""
        return self.available and bool(self.file)


@dataclass(frozen=True)
class InstallStep:
    title: str
    text: str


@dataclass(frozen=True)
class DownloadCatalog:
    """Descargas más los requisitos y pasos de instalación."""

    items: list[Download] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    instructions: list[InstallStep] = field(default_factory=list)


@dataclass(frozen=True)
class FaqItem:
    question: str
    answer: str


@dataclass(frozen=True)
class ClassInfo:
    """Una clase del juego."""

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


@dataclass(frozen=True)
class MapEntry:
    """Un mapa de la galería. ``image`` es una ruta dentro de static/img."""

    map: str
    level: str
    tag: str
    palette: str
    image: str | None = None


@dataclass(frozen=True)
class Gallery:
    note: str
    items: list[MapEntry] = field(default_factory=list)
