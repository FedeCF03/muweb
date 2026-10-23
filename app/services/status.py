"""Estado del servidor de juego.

v0: el texto lo escribe el operador en site.yml (``server.status_label``).
v1: ``LiveStatusService`` consulta el Connect Server (OpenMU no guarda en la
base quién está conectado, ver docs/v1-db.md sección 5).
"""

from __future__ import annotations

import socket
from typing import Any, Protocol

from ..models import ServerStatus

ONLINE_LABELS = {"online", "en línea", "en linea", "abierto"}


class StatusService(Protocol):
    def current(self, site: dict[str, Any]) -> ServerStatus: ...


class StaticStatusService:
    """Muestra el texto de site.yml tal cual (sin sondear nada)."""

    def current(self, site: dict[str, Any]) -> ServerStatus:
        label = str(site.get("server", {}).get("status_label", "Offline"))
        return ServerStatus(label=label, online=label.strip().lower() in ONLINE_LABELS, source="static")


class LiveStatusService:
    """Abre una conexión TCP al Connect Server: si responde, está online.

    Se activa con FEATURE_STATUS=1. El timeout es corto para no frenar la página.
    """

    def __init__(self, host: str, port: int, timeout: float = 0.6) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

    def current(self, site: dict[str, Any]) -> ServerStatus:
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout):
                return ServerStatus(label="Online", online=True, source="live")
        except OSError:
            return ServerStatus(label="Offline", online=False, source="live")
