"""Utilidad de riesgo compartida por las vistas.

Centraliza el mapeo entre un nivel de riesgo (Alto/Medio/Bajo) y el color de
badge nativo de Streamlit (`:color-badge[...]`), para que la tabla de
Priorizacion y, mas adelante, el panel de Paciente, pinten el mismo badge sin
duplicar el mapeo.
"""

from __future__ import annotations

_COLORES_BADGE: dict[str, str] = {
    "Alto": "red",
    "Medio": "orange",
    "Bajo": "green",
}


def badge_riesgo(nivel: str) -> str:
    """Texto Markdown del badge nativo de Streamlit para `nivel` de riesgo."""
    color = _COLORES_BADGE[nivel]
    return f":{color}-badge[{nivel}]"
