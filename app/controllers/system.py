"""Endpoints de sistema: healthcheck, robots.txt, sitemap."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request, send_from_directory

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
    pages = [("/", 1.0), ("/noticias", 0.8), ("/descargas", 0.9), ("/jugabilidad", 0.8), ("/faq", 0.6), ("/reglas", 0.6)]
    base = request.url_root.rstrip("/")
    urls = "\n".join(f"  <url><loc>{base}{path}</loc><priority>{p}</priority></url>" for path, p in pages)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )
    return xml, 200, {"Content-Type": "application/xml; charset=utf-8"}


@bp.get("/downloads/<path:filename>")
def download(filename: str):
    """Sirve los archivos de descarga cuando no hay Caddy adelante (desarrollo).

    En producción Caddy atiende /downloads/* antes de llegar a Flask, con
    soporte de rangos para descargas reanudables.
    """
    return send_from_directory(current_app.config["DOWNLOADS_DIR"], filename, as_attachment=True, conditional=True)


# El portfolio que antes vivía en este dominio era una app Blazor con service
# worker: los navegadores que lo visitaron siguen mostrando su copia vieja.
# Este service worker reemplaza al anterior, borra sus cachés, se desinstala
# y recarga la pestaña, así ven la web actual.
_SW_KILL_SWITCH = """
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map((key) => caches.delete(key)));
    await self.registration.unregister();
    const windows = await self.clients.matchAll({ type: 'window' });
    windows.forEach((client) => client.navigate(client.url));
  })());
});
"""


@bp.get("/service-worker.js")
@bp.get("/service-worker.published.js")
def service_worker_kill_switch():
    return (
        _SW_KILL_SWITCH,
        200,
        {
            "Content-Type": "application/javascript; charset=utf-8",
            "Cache-Control": "no-store",
            "Clear-Site-Data": '"cache"',
        },
    )
