"""Tarjeta de resultado del panel de Paciente: HTML a medida.

Misma excepcion deliberada que `components/tabla_priorizacion.py` (ver su
docstring): la maqueta (`ux-ui/pantallas.html`, bloque `.result`) pide un
header con fondo distinto al body dentro de una sola caja con esquinas
redondeadas, texto con tamanos/pesos/colores mixtos, y barras de "que peso
en la estimacion" con posicion y grosor exactos. Ningun widget nativo
(`st.metric`, `st.progress`) da ese control sin artefactos — ya lo vivimos
con el chip del delta de `st.metric` en `components/metric_card.py`.

El HTML vive aqui, escapado con `html.escape`; el estilo vive en
`components/styles.py` bajo el selector `.tarjeta-resultado`.
"""

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
    """Pinta la tarjeta completa (header + body) como una sola pieza."""
    color, fondo = _RIESGO_COLORES[nivel_riesgo]

    valor = f"{probabilidad:.2f}".replace(".", ",")
    cohorte = f"{cohorte_pct:.1f}".replace(".", ",")
    etiqueta_riesgo = html.escape(f"Riesgo {nivel_riesgo.lower()}")
    factores_html = "".join(_factor(texto, porcentaje) for texto, porcentaje in factores)

    st.markdown(
        f"""
        <div class="tarjeta-resultado">
            <div class="tarjeta-resultado__header" style="background-color:{fondo};">
                <span class="tarjeta-resultado__valor" style="color:{color};">{valor}</span>
                <span class="tarjeta-resultado__etiqueta" style="color:{color};">
                    <b>{etiqueta_riesgo}</b>
                    <span>probabilidad de reingreso &lt; 30 días</span>
                    <span>cohorte comparable: {cohorte} %</span>
                </span>
            </div>
            <div class="tarjeta-resultado__body">
                <p class="tarjeta-resultado__subtitulo">Qué pesó en esta estimación</p>
                <div class="tarjeta-resultado__factores">{factores_html}</div>
                <p class="tarjeta-resultado__nota">{html.escape(nota)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
