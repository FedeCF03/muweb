"""Modelos del dominio (la "M" de MVC).

Son dataclasses inmutables, sin dependencias de Flask ni de la fuente de datos:
los repositorios los construyen (desde YAML hoy, desde Postgres en la v1) y los
controladores se los pasan a las vistas.
"""

from .account import AccountRequest, RegistrationError, RegistrationResult, RegistrationUnavailable
from .content import (
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
from .server import ServerStatus

__all__ = [
    "AccountRequest",
    "ClassInfo",
    "Download",
    "DownloadCatalog",
    "EventItem",
    "FaqItem",
    "Gallery",
    "MapEntry",
    "NewsItem",
    "Page",
    "RegistrationError",
    "RegistrationResult",
    "RegistrationUnavailable",
    "ServerStatus",
]
