# muweb — landing de un server privado de MU Online (Season 6)

Landing page estática para el server de MU Online. Hecha con **Flask + Jinja +
Tailwind CSS v4**, servida con **Gunicorn** detrás de **Caddy** en Docker.

En esta versión (v0) el sitio **no usa base de datos**: el contenido vive en
archivos YAML y Markdown dentro de `content/` y se edita sin tocar código. La
integración con la base de OpenMU (registro de cuentas, rankings, estado del
server) está planificada en [`docs/v1-db.md`](docs/v1-db.md).

---

## Estructura

```
muweb/
├── app/
│   ├── __init__.py            # app factory (create_app)
│   ├── config.py              # configuración desde el entorno
│   ├── content.py             # carga YAML/Markdown (el punto de reemplazo por la DB)
│   ├── blueprints/public.py   # rutas públicas
│   ├── templates/             # Jinja (base + páginas + partials)
│   └── static/                # css compilado, js, imágenes, fuentes
├── content/                   # <<< TODO EL CONTENIDO EDITABLE
│   ├── site.yml               # nombre, rates, hero, features, footer
│   ├── downloads.yml          # descargas, requisitos, instrucciones
│   ├── faq.yml                # preguntas frecuentes
│   ├── rules.md               # reglas del server
│   └── news/*.md              # noticias (front matter YAML + Markdown)
├── docs/v1-db.md              # plan de integración con la base de datos
├── docker/Caddyfile           # proxy inverso + descargas
├── src/app.css                # fuente de Tailwind (sistema de diseño)
├── scripts/build-css.sh       # compila el CSS
├── tests/                     # tests de rutas y de contenido
├── compose.yml                # web + caddy
└── Dockerfile
```

## Arranque rápido (con Docker)

```bash
cp .env.example .env
# editá .env: poné un SECRET_KEY nuevo
docker compose up -d --build
```

Queda en `http://<IP-DE-LA-PC>/` (puerto 80, solo LAN).

```bash
docker compose logs -f web   # logs
docker compose down          # parar
```

## Arranque sin Docker (Gunicorn + Caddy en la máquina)

Docker no hace falta: hay un script que levanta lo mismo en local.

```bash
./scripts/serve-local.sh start     # levanta gunicorn + caddy
./scripts/serve-local.sh status    # puertos + healthcheck
./scripts/serve-local.sh logs      # logs en vivo
./scripts/serve-local.sh stop      # para todo
```

Queda en `http://<IP-DE-LA-PC>/` (puerto 80). Para escuchar en un puerto alto
sin permisos, usar `HTTP_PORT=8080 ./scripts/serve-local.sh start`.

El script aplica `cap_net_bind_service` al binario de Caddy (con sudo) para
poder usar el puerto 80 sin ser root.

## Arranque sin Docker (desarrollo)

```bash
make setup     # crea .venv e instala dependencias
make css       # compila el CSS (descarga el binario de Tailwind solo la primera vez)
make dev       # http://127.0.0.1:8000 con recarga automática
make test      # tests
```

## Producción sin Docker (systemd)

Si en la máquina no hay Docker, la landing se puede servir con Gunicorn +
Caddy instalados en el host. Hay una unidad lista en `deploy/muweb.service`:

```bash
sudo mkdir -p /opt/muweb && sudo cp -r . /opt/muweb
sudo chown -R muweb:muweb /opt/muweb
sudo cp deploy/muweb.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now muweb
```

Caddy (en el host) se configura con `docker/Caddyfile`, adaptando las rutas de
`/srv/downloads` a `/opt/muweb/downloads`.

## Editar el contenido

Todo el texto de la web sale de `content/`. No hace falta tocar plantillas
ni reiniciar nada: el cache se invalida solo cuando cambia el archivo.

| Quiero cambiar... | Archivo |
|---|---|
| Nombre, rates, textos del hero, features, pasos, footer | `content/site.yml` |
| Descargas, requisitos, instrucciones de instalación | `content/downloads.yml` |
| Preguntas frecuentes | `content/faq.yml` |
| Reglas del server | `content/rules.md` |
| Noticias | `content/news/AAAA-MM-DD-slug.md` |

Una noticia es un `.md` con front matter:

```markdown
---
title: "Título de la noticia"
date: "2026-10-18"
tag: "Eventos"
excerpt: "Resumen corto que sale en la tarjeta."
---

Cuerpo en **Markdown**. Se sanitiza antes de renderizar.
```

Para validar que todo el contenido esté bien:

```bash
make check-content
```

## Publicar el cliente (descargas)

1. Copiá el `.zip` a `downloads/` (por ejemplo `downloads/cliente-s6.zip`).
2. En `content/downloads.yml` poné `file: "cliente-s6.zip"` y `available: true`.
3. Copiá el `sha256sum` al mismo archivo.
4. Recargá la página.

Caddy sirve esa carpeta con soporte de rangos (descarga reanudable) y Flask no
se entera. Ojo: el zip que tenés en `~/MuOnline/Files S6.zip` contiene el
cliente **y** el server: subí solo la carpeta `Cliente S6 Eng`.

## Ponerlo en internet (cuando haya dominio)

1. Apuntar el DNS a la IP de la máquina.
2. En `compose.yml`, cambiar los puertos de caddy a `443:443` y sacar el `80`.
3. En `docker/Caddyfile`, usar el bloque del dominio (está comentado al final)
   y sacar `auto_https off` de la sección global.
4. `COOKIE_SECURE=1` en el `.env`.

El panel de OpenMU (8080) y Postgres (5432) **no** se exponen nunca.

## Variables de entorno

| Variable | Default | Para qué |
|---|---|---|
| `SECRET_KEY` | (inseguro) | Clave de Flask para CSRF y sesiones. **Cambiala.** |
| `PORT` | `8000` | Puerto interno de Gunicorn |
| `GUNICORN_WORKERS` | `2` | Workers de Gunicorn |
| `FEATURE_REGISTRATION` | `0` | Enciende el registro real (v1) |
| `FEATURE_STATUS` | `0` | Enciende el estado real del server (v1) |
| `COOKIE_SECURE` | `0` | Cookies solo por HTTPS (activar con dominio) |
| `CONTENT_DIR` | `./content` | Carpeta de contenido |
| `DOWNLOADS_DIR` | `./downloads` | Carpeta de descargas |
| `DATABASE_URL` | — | v1: base del CMS |
| `OPENMU_DATABASE_URL` | — | v1: base de OpenMU (lectura + Account) |

## Detalles técnicos

- **Tailwind v4** compilado con el binario standalone (sin Node). El CSS
  compilado está commiteado, así que la imagen de Docker no necesita Node.
- **Fuentes self-hosted** (Inter + Cinzel, licencia OFL) en
  `app/static/fonts/`: la web no depende de Google Fonts ni de internet.
- **Sin JavaScript obligatorio**: si el JS no carga, el contenido se ve igual
  (el revelado al scrollear solo se activa con JS).
- **Markdown saneado** con `nh3`: no se puede inyectar HTML.
- **SEO**: metadatos, Open Graph, `robots.txt` y `sitemap.xml` generados.
- **Accesibilidad**: skip link, foco visible, `prefers-reduced-motion`.

## Tests

```bash
make test
```

Cubren las rutas públicas, la carga del contenido y el saneado del Markdown.

## Próximos pasos (v1)

- Registro de cuentas contra la base de OpenMU.
- Panel de administración para noticias y descargas.
- Rankings y estado real del server.
- Shop de la tienda y sistema de tickets.

Ver [`docs/v1-db.md`](docs/v1-db.md) para el detalle técnico.

---

*Proyecto fan no afiliado a Webzen.*
