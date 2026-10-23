"""Agenda semanal: próximo evento y cuándo empieza."""

from __future__ import annotations

from datetime import datetime, timedelta

from ..models import EventItem


def _aware(now: datetime | None) -> datetime:
    now = now or datetime.now()
    return now if now.tzinfo else now.astimezone()


def event_starts_at(event: EventItem, now: datetime | None = None) -> datetime:
    """Fecha y hora de la próxima edición de un evento (para el countdown)."""
    now = _aware(now)
    candidate = now.replace(hour=event.hour, minute=event.minute, second=0, microsecond=0)
    candidate += timedelta(days=(event.day_index - now.weekday()) % 7)
    if candidate <= now:
        candidate += timedelta(days=7)
    return candidate


def next_event(events: list[EventItem], now: datetime | None = None) -> EventItem | None:
    """El evento más cercano en el tiempo a partir de ``now``."""
    now = _aware(now)
    return min(events, key=lambda ev: event_starts_at(ev, now)) if events else None
