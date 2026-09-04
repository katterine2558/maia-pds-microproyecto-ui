"""Unico punto de contacto con la API de inferencia.

El tablero no importa el modelo ni carga el artefacto serializado: todo pasa por
HTTP. Concentrar aqui las llamadas mantiene esa frontera visible y facil de
auditar — si aparece un `joblib.load` en este repositorio, la arquitectura se
rompio.
"""

import os

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = 10


class ApiError(RuntimeError):
    """La API no respondio o respondio con error."""


def _pedir(metodo: str, ruta: str, **kwargs):
    url = f"{API_URL}{ruta}"
    try:
        respuesta = requests.request(metodo, url, timeout=TIMEOUT, **kwargs)
        respuesta.raise_for_status()
    except requests.RequestException as exc:
        raise ApiError(f"{metodo} {url}: {exc}") from exc
    return respuesta.json()


def salud() -> dict:
    """Estado de la API y version del modelo cargado."""
    return _pedir("GET", "/health")


def predecir(encuentro: dict) -> dict:
    """Probabilidad de reingreso a 30 dias para un encuentro hospitalario."""
    return _pedir("POST", "/predict", json=encuentro)
