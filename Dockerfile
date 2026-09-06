FROM python:3.12-slim

WORKDIR /app

# Se instala desde uv.lock y no resolviendo pyproject: una reconstruccion
# meses despues trae exactamente las mismas versiones. La Entrega 3 califica
# los artefactos de despliegue, y un contenedor que no reconstruye igual no
# sirve como artefacto.
#
# Van antes de copiar el codigo para que la capa quede cacheada y cada cambio
# del tablero no reinstale todo.
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev --no-install-project \
    && rm -rf /root/.cache

COPY . .

EXPOSE 8501
ENV API_URL=http://api:8000
ENV PORT=8501
# Sin headless, Streamlit pide un correo por consola la primera vez y el
# contenedor se queda esperando una entrada que nunca llega.
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# HEALTHCHECK y CMD usan forma shell (sin corchetes) para poder expandir
# $PORT. Railway inyecta esta variable en runtime; localmente usa el valor
# por defecto (8501) definido arriba.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import os, urllib.request; p = os.environ.get('PORT', '8501'); urllib.request.urlopen('http://localhost:' + p + '/_stcore/health')"

CMD .venv/bin/streamlit run app.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true
