"""Estado del servidor de juego."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ServerStatus:
    """Estado que muestra la web.

    ``source`` dice de dónde sale: "static" (texto de site.yml, v0) o "live"
    (consulta al Connect Server, v1). La vista nunca debe presentar un estado
    estático como si fuera medido.
    """

    label: str
    online: bool
    source: str = "static"
