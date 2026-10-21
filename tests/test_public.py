"""Tests de las rutas públicas."""

from __future__ import annotations

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test"})
    with app.test_client() as test_client:
        yield test_client


def test_home_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"MU Argentum" in resp.data


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_news_list(client):
    resp = client.get("/noticias")
    assert resp.status_code == 200
    assert b"Noticias" in resp.data


def test_news_detail(client):
    resp = client.get("/noticias/2026-10-18-apertura")
    assert resp.status_code == 200
    assert "Abierto el server" in resp.text


def test_unknown_news_is_404(client):
    resp = client.get("/noticias/no-existe")
    assert resp.status_code == 404


def test_downloads_page(client):
    resp = client.get("/descargas")
    assert resp.status_code == 200
    assert b"Cliente" in resp.data


def test_faq_page(client):
    resp = client.get("/faq")
    assert resp.status_code == 200


def test_rules_page(client):
    resp = client.get("/reglas")
    assert resp.status_code == 200
    assert b"Reglas" in resp.data


def test_register_page_is_disabled(client):
    resp = client.get("/registro")
    assert resp.status_code == 200
    assert b"disabled" in resp.data


def test_register_post_returns_503(client):
    # El endpoint es un stub: todavía no hay base de datos para crear cuentas.
    page = client.get("/registro")
    token = page.data.decode().split('name="csrf_token" value="')[1].split('"')[0]
    resp = client.post("/registro", data={"csrf_token": token})
    assert resp.status_code == 503


def test_404_page(client):
    resp = client.get("/no-existe")
    assert resp.status_code == 404
    assert b"404" in resp.data


def test_robots_and_sitemap(client):
    assert client.get("/robots.txt").status_code == 200
    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    assert b"<urlset" in sitemap.data
