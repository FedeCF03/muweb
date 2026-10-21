# ---------------------------------------------------------------------------
# Imagen de la landing. El CSS ya viene compilado en app/static/css/app.css,
# así que la imagen no necesita Node ni el binario de Tailwind.
# ---------------------------------------------------------------------------
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY content ./content
COPY downloads ./downloads

RUN useradd --create-home --uid 10001 muweb \
    && chown -R muweb:muweb /app
USER muweb

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"

# exec para que gunicorn reciba las señales de docker stop
CMD ["sh", "-c", "exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --threads 4 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    'app:create_app()'"]
