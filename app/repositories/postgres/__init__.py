"""Backend Postgres (v1). Ver docs/v1-db.md.

- ``content``: base propia "muweb" (noticias, descargas, páginas, ajustes).
- ``openmu``: base de OpenMU (cuentas). Solo lectura más INSERT en "Account".

psycopg se importa recién al conectar: la app arranca sin él mientras el
backend sea "files". Para usarlo: ``pip install -r requirements-db.txt``.
"""

from .connection import Database
from .content import PgDownloadRepository, PgNewsRepository, PgPageRepository, PgSiteRepository
from .openmu import OpenMuAccountRepository

__all__ = [
    "Database",
    "OpenMuAccountRepository",
    "PgDownloadRepository",
    "PgNewsRepository",
    "PgPageRepository",
    "PgSiteRepository",
]
