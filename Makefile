# Tareas habituales
.DEFAULT_GOAL := help
SHELL := /bin/bash

PY := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: help
help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Crea el venv e instala las dependencias
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

.PHONY: dev
dev: ## Levanta la app en modo desarrollo (http://127.0.0.1:8000)
	$(PY) -m flask --app app run --debug --port 8000

.PHONY: serve
serve: ## Levanta la app con gunicorn (como en producción)
	.venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 2 'app:create_app()'

.PHONY: css
css: ## Compila el CSS (Tailwind) -> app/static/css/app.css
	./scripts/build-css.sh

.PHONY: css-watch
css-watch: ## Compila el CSS en modo watch
	./scripts/build-css.sh --watch

.PHONY: test
test: ## Corre los tests
	$(PY) -m pytest

.PHONY: check-content
check-content: ## Valida el contenido YAML/Markdown
	$(PY) -m flask --app app check-content

.PHONY: up
up: ## Levanta la app con Docker (web + caddy)
	docker compose up -d --build

.PHONY: down
down: ## Baja los contenedores
	docker compose down

.PHONY: logs
logs: ## Muestra los logs de la app
	docker compose logs -f web
