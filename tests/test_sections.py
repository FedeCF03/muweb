"""Tests de las secciones nuevas: clases, galería y agenda de eventos."""

from __future__ import annotations

from datetime import datetime

import pytest

from app import create_app
from app.content import (
    event_starts_at,
    load_classes,
    load_events,
    load_events_note,
    load_gallery,
    next_event,
)


@pytest.fixture()
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test"})


def test_classes_structure(app):
    classes = load_classes()
    assert len(classes) == 5
    for item in classes:
        assert item.name
        assert item.icon
        assert 0 <= len(item.stats) <= 3
        for label, value in item.stats.items():
            assert 0 <= value <= 100, f"{item.name}: stat fuera de rango"
        assert item.accent.startswith("#")


def test_locked_classes_have_requirement(app):
    by_key = {item.key: item for item in load_classes()}
    assert by_key["mg"].requirement
    assert by_key["dl"].requirement
    assert by_key["dk"].requirement is None


def test_gallery_items(app):
    gallery = load_gallery()
    assert gallery["note"]
    items = gallery["items"]
    assert len(items) >= 6
    for item in items:
        assert item["map"]
        assert item["palette"]
        # image: null o una ruta de static
        assert item["image"] is None or "/" not in str(item["image"])


def test_events_sorted_by_day_and_time(app):
    events = load_events()
    assert events, "la agenda no puede estar vacía"
    order = [(ev.day_index, ev.hour, ev.minute) for ev in events]
    assert order == sorted(order)


def test_next_event_is_in_the_future(app):
    now = datetime.now().astimezone()
    upcoming = next_event(now)
    assert upcoming is not None
    starts = event_starts_at(upcoming, now)
    assert starts > now
    # no más de 7 días de acá
    assert (starts - now).days <= 7


def test_next_event_wraps_around_week(app):
    # lunes 22:10 => el próximo evento no puede ser el lunes que ya pasó
    monday_evening = datetime(2026, 10, 19, 22, 10).astimezone()
    upcoming = next_event(monday_evening)
    assert upcoming is not None
    starts = event_starts_at(upcoming, monday_evening)
    assert starts > monday_evening


def test_events_note(app):
    assert "UTC" in load_events_note() or "horario" in load_events_note().lower()
