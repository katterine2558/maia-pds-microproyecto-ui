"""Tarjeta de resultado del panel de Paciente: HTML a medida.

Misma excepcion deliberada que `components/tabla_priorizacion.py` (ver su
docstring): la maqueta (`ux-ui/pantallas.html`, bloque `.result`) pide un
header con fondo distinto al body dentro de una sola caja con esquinas
redondeadas y texto con tamanos/pesos/colores mixtos. Ningun widget nativo
(`st.metric`) da ese control sin artefactos — ya lo vivimos con el chip del
delta de `st.metric` en `components/metric_card.py`.

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
    nota: str,
    factores: list[tuple[str, int]] | None = None,
) -> None:
    """Pinta la tarjeta completa (header + body) como una sola pieza.

    `factores` queda opcional: el bloque "Que peso en esta estimacion" solo
    aparece cuando la API devuelve importancias. Hoy `/predict` responde con
    probabilidad, umbral y version del modelo, asi que la tarjeta se pinta sin
    ese bloque en lugar de inventarlo.
    """
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


def render_tarjeta_resultado_skeleton() -> None:
    """Placeholder animado con la misma silueta de la tarjeta, mientras se
    espera la respuesta de `POST /predict`.
    """
    contenido = (
        '<div class="tarjeta-resultado tarjeta-resultado--skeleton">'
        '<div class="tarjeta-resultado__header">'
        '<span class="skeleton-block skeleton-block--valor"></span>'
        '<span class="skeleton-block skeleton-block--etiqueta"></span>'
        "</div>"
        '<div class="tarjeta-resultado__body">'
        '<span class="skeleton-block skeleton-block--linea" style="width:60%"></span>'
        '<span class="skeleton-block skeleton-block--linea" style="width:90%"></span>'
        '<span class="skeleton-block skeleton-block--linea" style="width:75%"></span>'
        "</div>"
        "</div>"
    )
    st.markdown(contenido, unsafe_allow_html=True)
