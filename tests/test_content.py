"""Tests de los repositorios de archivos (backend v0)."""

from __future__ import annotations

from datetime import date

from app.models import Download, NewsItem
from app.services.markdown import render_markdown


def test_site_has_required_keys(svc):
    site = svc.site.get()
    for key in ("name", "tagline", "seo", "server", "hero", "rates", "features", "steps"):
        assert key in site, f"falta {key} en site.yml"


def test_server_info(svc):
    server = svc.site.get()["server"]
    assert server["client_version"]
    assert server["season"]


def test_server_address_is_never_exposed(svc):
    server = svc.site.get()["server"]
    for key in ("connect_host", "connect_port", "host", "ip", "port"):
        assert key not in server


def test_news_are_sorted_by_date(svc):
    news = svc.news.list()
    assert news, "debería haber noticias"
    assert all(isinstance(item, NewsItem) for item in news)
    fechas = [item.date for item in news]
    assert fechas == sorted(fechas, reverse=True)
    assert all(isinstance(f, date) for f in fechas)


def test_news_lookup(svc):
    item = svc.news.get("2026-10-18-apertura")
    assert item is not None
    assert item.title
    assert "<h2>" in item.html
    assert svc.news.get("no-existe") is None


def test_downloads_structure(svc):
    catalog = svc.downloads.catalog()
    assert catalog.items
    assert all(isinstance(item, Download) and item.name for item in catalog.items)
    assert catalog.requirements
    assert catalog.instructions


def test_download_ready_needs_file():
    assert not Download("a", "A", "", "", "", "", file=None, available=True).ready
    assert Download("a", "A", "", "", "", "", file="a.zip", available=True).ready


def test_faq_items(svc):
    items = svc.faq.list()
    assert items
    assert all(item.question and item.answer for item in items)


def test_markdown_page(svc):
    page = svc.pages.get("rules")
    assert page is not None and page.body
    assert "<li>" in page.html
    assert svc.pages.get("no-existe") is None


def test_markdown_is_sanitized():
    html = render_markdown("<script>alert(1)</script>\n\nTexto")
    assert "<script>" not in html
    assert "Texto" in html


def test_html_attributes_are_filtered():
    html = render_markdown('<a href="javascript:alert(1)">x</a>')
    assert "javascript:" not in html
