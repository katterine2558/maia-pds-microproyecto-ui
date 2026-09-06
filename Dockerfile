FROM python:3.12-slim

WORKDIR /app

# Las dependencias se instalan antes de copiar el codigo para que la capa
# quede cacheada y cada cambio del tablero no reinstale todo.
COPY pyproject.toml ./
RUN pip install --no-cache-dir . && rm -rf /root/.cache

COPY . .

EXPOSE 8501
ENV API_URL=http://api:8000
ENV PORT=8501

# HEALTHCHECK y CMD usan forma shell (sin corchetes) para poder expandir
# $PORT. Railway inyecta esta variable en runtime; localmente usa el valor
# por defecto (8501) definido arriba.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import os, urllib.request; p = os.environ.get('PORT', '8501'); urllib.request.urlopen('http://localhost:' + p + '/_stcore/health')"

CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
