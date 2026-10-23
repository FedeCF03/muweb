"""Tests de las rutas públicas."""

from __future__ import annotations


def test_home_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"OpenMuArg" in resp.data


def test_server_address_not_in_pages(client, monkeypatch):
    monkeypatch.setenv("CONNECT_HOST", "203.0.113.77")
    for path in ("/", "/descargas", "/faq", "/reglas", "/noticias", "/registro"):
        html = client.get(path).text
        assert "203.0.113.77" not in html, path
        assert "44405" not in html, path


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


def test_gameplay_page(client):
    resp = client.get("/jugabilidad")
    assert resp.status_code == 200
    assert "Sistema de reset" in resp.text
    assert "Happy Hour" in resp.text


def test_download_route_rejects_traversal(client):
    assert client.get("/downloads/../app/config.py").status_code == 404
    assert client.get("/downloads/no-existe.zip").status_code == 404
