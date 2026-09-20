"""Tarjeta que muestra el resultado de la predicción del paciente."""

from __future__ import annotations

import html

import streamlit as st

from config.theme import COLORS


_RIESGO_COLORES = {
    "Alto": (COLORS.risk_high, COLORS.risk_high_bg),
    "Medio": (COLORS.risk_medium, COLORS.risk_medium_bg),
    "Bajo": (COLORS.risk_low, COLORS.risk_low_bg),
}


def _factor(etiqueta: str, porcentaje: int) -> str:
    texto = html.escape(etiqueta)
    ancho = max(0, min(100, porcentaje))
    return (
        '<div class="tarjeta-resultado__factor">'
        f"<span>{texto}</span>"
        f'<div class="tarjeta-resultado__barra"><i style="width:{ancho}%"></i></div>'
        "</div>"
    )


def render_tarjeta_resultado(
    probabilidad: float,
    nivel_riesgo: str,
    cohorte_pct: float,
    factores: list[tuple[str, int]],
    nota: str,
) -> None:
    """Muestra la probabilidad, el nivel de riesgo y la nota del resultado."""
    color, fondo = _RIESGO_COLORES[nivel_riesgo]
    valor = f"{probabilidad:.2f}".replace(".", ",")
    etiqueta_riesgo = html.escape(f"Riesgo {nivel_riesgo.lower()}")

    factores_html = ""
    if factores:
        detalle = "".join(_factor(texto, porcentaje) for texto, porcentaje in factores)
        factores_html = (
            '<p class="tarjeta-resultado__subtitulo">'
            "Qué pesó en esta estimación"
            "</p>"
            f'<div class="tarjeta-resultado__factores">{detalle}</div>'
        )

    contenido = (
        '<div class="tarjeta-resultado">'
        f'<div class="tarjeta-resultado__header" style="background-color:{fondo};">'
        f'<span class="tarjeta-resultado__valor" style="color:{color};">{valor}</span>'
        f'<span class="tarjeta-resultado__etiqueta" style="color:{color};">'
        f"<b>{etiqueta_riesgo}</b>"
        "<span>probabilidad de reingreso &lt; 30 días</span>"
        "</span>"
        "</div>"
        '<div class="tarjeta-resultado__body">'
        f"{factores_html}"
        f'<p class="tarjeta-resultado__nota">{html.escape(nota)}</p>'
        "</div>"
        "</div>"
    )

    st.markdown(contenido, unsafe_allow_html=True)