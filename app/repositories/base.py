"""Contratos de los repositorios.

Cualquier backend (archivos, Postgres, una API) implementa estos métodos y
devuelve los modelos de ``app.models``. Agregar un backend nuevo no toca
servicios, controladores ni plantillas.
"""

from __future__ import annotations

from typing import Any, Protocol

from ..models import (
    AccountRequest,
    ClassInfo,
    DownloadCatalog,
    EventItem,
    FaqItem,
    Gallery,
    NewsItem,
    Page,
    RegistrationResult,
)


class SiteRepository(Protocol):
    def get(self) -> dict[str, Any]:
        """Ajustes generales (nombre, rates, hero, features...). v1: tabla site_setting."""


class NewsRepository(Protocol):
    def list(self) -> list[NewsItem]:
        """Todas las noticias publicadas, de la más nueva a la más vieja."""

    def get(self, slug: str) -> NewsItem | None: ...


class PageRepository(Protocol):
    def get(self, slug: str) -> Page | None: ...

    def slugs(self) -> list[str]: ...


class DownloadRepository(Protocol):
    def catalog(self) -> DownloadCatalog: ...


class FaqRepository(Protocol):
    def list(self) -> list[FaqItem]: ...


class ClassRepository(Protocol):
    def list(self) -> list[ClassInfo]: ...


class GalleryRepository(Protocol):
    def get(self) -> Gallery: ...


class GameplayRepository(Protocol):
    def get(self) -> dict[str, Any]:
        """Configuración de juego: EXP, resets, clases, PvP, mapas, Chaos Mix."""


class EventRepository(Protocol):
    def list(self) -> list[EventItem]:
        """Agenda ordenada por día y hora."""

    def timezone_note(self) -> str: ...


class AccountRepository(Protocol):
    def exists(self, username: str) -> bool: ...

    def create(self, request: AccountRequest) -> RegistrationResult:
        """Crea la cuenta. Lanza RegistrationUnavailable si el backend no puede."""
