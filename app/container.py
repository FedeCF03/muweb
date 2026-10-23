"""Contenedor de dependencias: arma repositorios y servicios según la config.

Es el único lugar que sabe qué backend se usa. Los controladores piden lo que
necesitan con ``services()`` y no importan ningún repositorio concreto.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from flask import Flask, current_app

from .repositories.base import (
    AccountRepository,
    ClassRepository,
    DownloadRepository,
    EventRepository,
    FaqRepository,
    GalleryRepository,
    GameplayRepository,
    NewsRepository,
    PageRepository,
    SiteRepository,
)
from .repositories.disabled import DisabledAccountRepository
from .repositories.files import (
    FileClassRepository,
    FileDownloadRepository,
    FileEventRepository,
    FileFaqRepository,
    FileGalleryRepository,
    FileGameplayRepository,
    FileNewsRepository,
    FilePageRepository,
    FileSiteRepository,
)
from .repositories.files.storage import FileStore
from .services.accounts import AccountService
from .services.status import LiveStatusService, StaticStatusService, StatusService

EXTENSION_KEY = "muweb"


@dataclass
class Services:
    site: SiteRepository
    news: NewsRepository
    pages: PageRepository
    downloads: DownloadRepository
    faq: FaqRepository
    classes: ClassRepository
    gallery: GalleryRepository
    events: EventRepository
    gameplay: GameplayRepository
    accounts: AccountService
    status: StatusService
    backend: str


def build(config: dict[str, Any]) -> Services:
    """Construye todo a partir de la configuración de Flask."""
    store = FileStore(Path(config["CONTENT_DIR"]))
    site: SiteRepository = FileSiteRepository(store)
    news: NewsRepository = FileNewsRepository(store)
    pages: PageRepository = FilePageRepository(store)
    downloads: DownloadRepository = FileDownloadRepository(store)
    account_repo: AccountRepository = DisabledAccountRepository()

    backend = config.get("CONTENT_BACKEND", "files")
    if backend == "db":
        from .repositories.postgres import (
            Database,
            PgDownloadRepository,
            PgNewsRepository,
            PgPageRepository,
            PgSiteRepository,
        )

        db = Database(config.get("DATABASE_URL") or "")
        site = PgSiteRepository(db, fallback=site)
        news = PgNewsRepository(db)
        pages = PgPageRepository(db)
        downloads = PgDownloadRepository(db, fallback=downloads)
    elif backend != "files":
        raise ValueError(f"CONTENT_BACKEND desconocido: {backend!r} (usá 'files' o 'db')")

    if config.get("FEATURE_REGISTRATION") and config.get("OPENMU_DATABASE_URL"):
        from .repositories.postgres import Database, OpenMuAccountRepository

        account_repo = OpenMuAccountRepository(
            Database(config["OPENMU_DATABASE_URL"]),
            writes_verified=bool(config.get("OPENMU_WRITES_VERIFIED")),
        )

    status: StatusService = StaticStatusService()
    if config.get("FEATURE_STATUS"):
        import os

        status = LiveStatusService(os.environ.get("CONNECT_HOST", "127.0.0.1"), int(config.get("CONNECT_PORT", 44405)))

    return Services(
        site=site,
        news=news,
        pages=pages,
        downloads=downloads,
        faq=FileFaqRepository(store),
        classes=FileClassRepository(store),
        gallery=FileGalleryRepository(store),
        events=FileEventRepository(store),
        gameplay=FileGameplayRepository(store),
        accounts=AccountService(account_repo, enabled=bool(config.get("FEATURE_REGISTRATION"))),
        status=status,
        backend=backend,
    )


def init_app(app: Flask) -> Services:
    services_ = build(app.config)
    app.extensions[EXTENSION_KEY] = services_
    return services_


def services() -> Services:
    """Servicios de la app actual (para usar dentro de una request o app context)."""
    return current_app.extensions[EXTENSION_KEY]
