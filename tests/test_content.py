"""Tests de la capa de contenido."""

from __future__ import annotations

from datetime import date

import pytest

from app import create_app
from app.content import (
    get_news,
    load_downloads,
    load_faq,
    load_news,
    load_page,
    load_site,
    render_markdown,
)


@pytest.fixture()
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test"})


def test_site_has_required_keys(app):
    site = load_site()
    for key in ("name", "tagline", "seo", "server", "hero", "rates", "features", "steps"):
        assert key in site, f"falta {key} en site.yml"


def test_server_info(app):
    server = load_site()["server"]
    assert server["connect_host"]
    assert server["connect_port"]


def test_news_are_sorted_by_date(app):
    news = load_news()
    assert news, "debería haber noticias"
    fechas = [item.date for item in news]
    assert fechas == sorted(fechas, reverse=True)
    assert all(isinstance(f, date) for f in fechas)


def test_news_lookup(app):
    item = get_news("2026-10-18-apertura")
    assert item is not None
    assert item.title
    assert "<h2>" in item.html


def test_downloads_structure(app):
    data = load_downloads()
    assert data["items"]
    for item in data["items"]:
        assert item["name"]
        assert "available" in item


def test_faq_items(app):
    items = load_faq()
    assert items
    assert all(item.get("question") and item.get("answer") for item in items)


def test_markdown_page(app):
    raw, html = load_page("rules")
    assert raw
    assert "<li>" in html


def test_markdown_is_sanitized():
    html = render_markdown("<script>alert(1)</script>\n\nTexto")
    assert "<script>" not in html
    assert "Texto" in html


def test_html_attributes_are_filtered():
    html = render_markdown('<a href="javascript:alert(1)">x</a>')
    assert "javascript:" not in html
