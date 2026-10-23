"""Controladores (la "C" de MVC): blueprints finitos.

Cada handler pide datos a los repositorios/servicios del contenedor, decide qué
vista renderizar y con qué código HTTP. Nada de lógica de negocio ni de acceso
a archivos o base acá.
"""

from flask import Flask


def register_controllers(app: Flask) -> None:
    from .account import bp as account_bp
    from .news import bp as news_bp
    from .pages import bp as pages_bp
    from .system import bp as system_bp

    for bp in (pages_bp, news_bp, account_bp, system_bp):
        app.register_blueprint(bp)
