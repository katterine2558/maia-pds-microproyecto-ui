"""Utilidad de riesgo compartida por las vistas.

Centraliza dos cosas para que Priorizacion y Paciente hablen el mismo idioma:
el mapeo entre un nivel de riesgo (Alto/Medio/Bajo) y el color de badge nativo
de Streamlit (`:color-badge[...]`), y las bandas que convierten la probabilidad
que devuelve la API en ese nivel.
"""

from __future__ import annotations

# Tasa de reingreso < 30 dias del conjunto completo (99 343 encuentros). Es la
# misma linea base que anota la vista Contexto.
TASA_BASE = 0.114

_COLORES_BADGE: dict[str, str] = {
    "Alto": "red",
    "Medio": "orange",
    "Bajo": "green",
}


def badge_riesgo(nivel: str) -> str:
    """Texto Markdown del badge nativo de Streamlit para `nivel` de riesgo."""
    color = _COLORES_BADGE[nivel]
    return f":{color}-badge[{nivel}]"


def nivel_de_riesgo(probabilidad: float, umbral: float) -> str:
    """Banda de riesgo de una probabilidad, contra el umbral del modelo.

    `Alto` es lo que el modelo marca para seguimiento: probabilidad por encima
    del umbral de decision que la API devuelve junto con la prediccion. Por
    debajo, la referencia deja de ser el umbral y pasa a ser la tasa base del
    conjunto: un encuentro que supera esa tasa es `Medio`, y por debajo `Bajo`.
    """
    if probabilidad >= umbral:
        return "Alto"
    if probabilidad >= TASA_BASE:
        return "Medio"
    return "Bajo"
