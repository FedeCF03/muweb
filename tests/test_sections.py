"""Tests de clases, galería, agenda y del tablero de la home."""

from __future__ import annotations

from datetime import datetime

from app.services import schedule


def test_classes_structure(svc):
    classes = svc.classes.list()
    assert len(classes) == 7
    for item in classes:
        assert item.name
        assert item.icon
        assert 0 <= len(item.stats) <= 3
        for value in item.stats.values():
            assert 0 <= value <= 100, f"{item.name}: stat fuera de rango"
        assert item.accent.startswith("#")


def test_locked_classes_have_requirement(svc):
    by_key = {item.key: item for item in svc.classes.list()}
    assert by_key["mg"].requirement
    assert by_key["dl"].requirement
    assert by_key["dk"].requirement is None


def test_gallery_items(svc):
    gallery = svc.gallery.get()
    assert gallery.note
    assert len(gallery.items) >= 6
    for item in gallery.items:
        assert item.map
        assert item.palette
        # image: None o un nombre de archivo dentro de static/img/gallery
        assert item.image is None or "/" not in item.image


def test_events_sorted_by_day_and_time(svc):
    events = svc.events.list()
    assert events, "la agenda no puede estar vacía"
    order = [(ev.day_index, ev.hour, ev.minute) for ev in events]
    assert order == sorted(order)


def test_next_event_is_in_the_future(svc):
    now = datetime.now().astimezone()
    upcoming = schedule.next_event(svc.events.list(), now)
    assert upcoming is not None
    starts = schedule.event_starts_at(upcoming, now)
    assert starts > now
    assert (starts - now).days <= 7


def test_next_event_wraps_around_week(svc):
    # lunes 22:10 => el próximo evento no puede ser el lunes que ya pasó
    monday_evening = datetime(2026, 10, 19, 22, 10).astimezone()
    upcoming = schedule.next_event(svc.events.list(), monday_evening)
    assert upcoming is not None
    assert schedule.event_starts_at(upcoming, monday_evening) > monday_evening


def test_next_event_empty_agenda():
    assert schedule.next_event([]) is None


def test_events_note(svc):
    note = svc.events.timezone_note()
    assert "UTC" in note or "horario" in note.lower()


def test_gameplay_config(svc):
    gameplay = svc.gameplay.get()
    labels = {row["label"]: row["value"] for row in gameplay["config"]}
    assert labels["Nivel máximo"] == "400"
    reset = {row["label"]: row["value"] for row in gameplay["reset"]["points"]}
    assert reset["Puntos por reset"] == "500"
    # cada clase de classes.yml tiene sus puntos por nivel
    keys = {item.key for item in svc.classes.list()}
    assert keys <= set(gameplay["class_points"])


def test_daily_events_expand_to_every_day(svc):
    daily = [ev for ev in svc.events.list() if ev.daily]
    assert daily
    assert {ev.day_index for ev in daily} == set(range(7))
