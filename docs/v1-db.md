# Plan de integración con base de datos (v1)
#
# Estado actual: la v0 es 100% estática. El contenido vive en YAML/Markdown
# dentro de content/ y la capa app/content.py es la única que lee esos
# archivos. Esta nota deja diagramado el camino a la v1 sin tocar plantillas.
#
# ---------------------------------------------------------------------------
# 1. Dónde vive la base
# ---------------------------------------------------------------------------
#
# El server corre OpenMU sobre PostgreSQL (contenedor openmu_postgres) en la
# red docker "openmu_openmu". La base "openmu" NO está publicada al exterior.
#
# La landing se une a esa red y usa una base propia llamada "muweb" dentro del
# mismo motor. Un solo Postgres, un solo backup.
#
#   web (esta app)  --red openmu_openmu-->  database:5432
#                       base "muweb"   (noticias, descargas, admin)
#                       base "openmu"  (solo lectura + INSERT en Account)
#
# ---------------------------------------------------------------------------
# 2. Roles de Postgres
# ---------------------------------------------------------------------------
#
# Desde un cliente psql como el admin del contenedor:
#
#   CREATE DATABASE muweb;
#   CREATE ROLE muweb_app LOGIN PASSWORD 'CLAVE_FUERTE';
#   GRANT ALL PRIVILEGES ON DATABASE muweb TO muweb_app;
#
#   \c openmu
#   CREATE ROLE muweb_ro LOGIN PASSWORD 'CLAVE_FUERTE';
#   GRANT CONNECT ON DATABASE openmu TO muweb_ro;
#   GRANT USAGE ON SCHEMA public TO muweb_ro;
#   GRANT SELECT ON ALL TABLES IN SCHEMA public TO muweb_ro;
#   GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO muweb_ro;
#   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO muweb_ro;
#
#   -- solo lo necesario para crear cuentas desde la web:
#   GRANT INSERT ON TABLE "Account" TO muweb_ro;
#
# Nunca uses el usuario postgres desde la app.
#
# ---------------------------------------------------------------------------
# 3. Esquema de la base "muweb"
# ---------------------------------------------------------------------------
#
#   admin_user       id, username, password_hash, created_at, last_login
#   news             id, slug, title, excerpt, body_md, tag, published_at,
#                    created_at, updated_at
#   download         id, key, name, kind, version, size_bytes, file, url,
#                    sha256, available, sort_order
#   page             id, slug, title, body_md, visible
#   site_setting     key, value (json)
#   web_registration id, login_name, email, ip, created_at, status
#
# Migraciones con Alembic (o Flask-Migrate si se usa SQLAlchemy en la app).
#
# ---------------------------------------------------------------------------
# 4. Cambios en el código
# ---------------------------------------------------------------------------
#
# 1) Dependencias: SQLAlchemy 2, psycopg[binary], Flask-Migrate, Flask-Login.
# 2) app/content.py: las funciones load_site/load_news/load_downloads/load_faq/
#    load_page pasan a leer de la base. Se mantienen los mismos nombres y los
#    mismos tipos de retorno (dataclasses) para no tocar ni una plantilla.
# 3) Se agrega el repositorio de OpenMU (app/services/openmu.py) con las
#    consultas de lectura: top de personajes, guilds, etc.
# 4) El registro web (app/blueprints/public.py::register_post) deja de
#    devolver 503 y llama a OpenMU. Ver la seccion 5.
#
# ---------------------------------------------------------------------------
# 5. Crear cuentas en OpenMU (lo más delicado)
# ---------------------------------------------------------------------------
#
# Antes de escribir código, verificar contra la base real:
#
#   a) Reglas del login: longitud mínima/máxima y caracteres permitidos.
#   b) Límite de longitud de la contraseña (el cliente clásico acepta 10).
#   c) Cómo hashea OpenMU la contraseña: si es BCrypt, hay que usar el mismo
#      algoritmo y el mismo costo (work factor) que usa el server.
#   d) Qué columnas tiene la tabla "Account" y cuáles son obligatorias.
#
# Procedimiento recomendado:
#   1. Crear una cuenta de prueba desde el panel de OpenMU (puerto 8080).
#   2. Leer su fila de "Account" y comparar el hash con lo que genera la web.
#   3. Insertar de prueba y entrar al juego con el cliente para confirmar.
#   4. Recién ahí, exponer el formulario (FEATURE_REGISTRATION=1).
#
# Extra: OpenMU no persiste "el jugador está online", así que el contador real
# de conectados no sale de la base. Opciones: consultar al Connect Server o
# dejar un badge estático como en la v0.
#
# ---------------------------------------------------------------------------
# 6. Seguridad
# ---------------------------------------------------------------------------
#
# - CSRF ya está activo (Flask-WTF) en todos los formularios.
# - Rate limit en /registro: se puede sumar Flask-Limiter (5/min y 20/h por IP).
# - Captcha: Turnstile necesita dominio público; en LAN usar honeypot.
# - Cookie "secure" activa cuando haya HTTPS (COOKIE_SECURE=1).
# - El registro nunca loguea contraseñas.
