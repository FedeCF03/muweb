"""Endpoints de sistema: healthcheck, robots.txt, sitemap."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request

from ..container import services

bp = Blueprint("system", __name__)


@bp.get("/healthz")
def healthz():
    return jsonify(
        {
            "status": "ok",
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "backend": services().backend,
            "registration": current_app.config.get("FEATURE_REGISTRATION", False),
        }
    )


@bp.get("/robots.txt")
def robots():
    return (
        "User-agent: *\nAllow: /\nDisallow: /registro\nSitemap: /sitemap.xml\n",
        200,
        {"Content-Type": "text/plain; charset=utf-8"},
    )


@bp.get("/sitemap.xml")
def sitemap():
    pages = [("/", 1.0), ("/noticias", 0.8), ("/descargas", 0.9), ("/faq", 0.6), ("/reglas", 0.6)]
    base = request.url_root.rstrip("/")
    urls = "\n".join(f"  <url><loc>{base}{path}</loc><priority>{p}</priority></url>" for path, p in pages)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )
    return xml, 200, {"Content-Type": "application/xml; charset=utf-8"}
