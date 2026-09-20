"""Unico punto de contacto con la API de inferencia.

El tablero no importa el modelo ni carga el artefacto serializado: todo pasa por
HTTP. Concentrar aqui las llamadas mantiene esa frontera visible y facil de
auditar — si aparece un `joblib.load` en este repositorio, la arquitectura se
rompio.
"""

import os
from concurrent.futures import ThreadPoolExecutor

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = 10
# Peticiones simultaneas al predecir un lote de egresos. La API corre en un
# contenedor pequeno: el limite la protege y evita abrir un hilo por fila.
CONCURRENCIA = 8


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


def predecir_lote(encuentros: list[dict]) -> list[dict | ApiError]:
    """Predice una lista de encuentros y conserva el orden de entrada.

    La API expone `/predict` de a un encuentro, asi que el lote son N llamadas
    en paralelo. Un fallo no tumba el lote: la posicion de la fila que fallo
    devuelve su `ApiError` y la vista decide como mostrarla, porque un egreso
    con datos raros no puede dejar sin lista al resto del turno.
    """
    if not encuentros:
        return []

    def _una(encuentro: dict) -> dict | ApiError:
        try:
            return predecir(encuentro)
        except ApiError as exc:
            return exc

    with ThreadPoolExecutor(max_workers=min(CONCURRENCIA, len(encuentros))) as pool:
        return list(pool.map(_una, encuentros))
