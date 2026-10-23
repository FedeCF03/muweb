"""Repositorios: cómo se leen y escriben los modelos.

``base`` define los contratos (Protocols). Hay dos implementaciones:

- ``files``: YAML y Markdown en ``content/`` (v0, la que corre hoy).
- ``postgres``: base "muweb" y la base de OpenMU (v1, ver docs/v1-db.md).

El contenedor (``app.container``) elige cuál usar según la configuración. Los
servicios y controladores solo conocen los contratos.
"""
