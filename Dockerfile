FROM python:3.12-slim

WORKDIR /app

# Las dependencias se instalan antes de copiar el codigo para que la capa
# quede cacheada y cada cambio del tablero no reinstale todo.
COPY pyproject.toml ./
RUN pip install --no-cache-dir . && rm -rf /root/.cache

COPY . .

EXPOSE 8501
ENV API_URL=http://api:8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
