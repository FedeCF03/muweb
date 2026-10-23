"""Noticias."""

from __future__ import annotations

from flask import Blueprint, render_template

from ..container import services

bp = Blueprint("news", __name__, url_prefix="/noticias")


@bp.get("")
def list():
    return render_template("news_list.html", title="Noticias", news=services().news.list())


@bp.get("/<slug>")
def detail(slug: str):
    item = services().news.get(slug)
    if item is None:
        return render_template("404.html", title="Noticia no encontrada"), 404
    return render_template("news_detail.html", title=item.title, item=item)
