"""Grafico de barras horizontales del panel de Contexto: HTML a medida.

Misma excepcion deliberada que `components/tabla_priorizacion.py` y
`components/tarjeta_resultado.py` (ver sus docstrings): la maqueta
(`ux-ui/pantallas.html`, bloque `.card`/`.chart`/`.bar-row`) pide una columna
de categoria de ancho fijo alineada a la derecha, una barra con radios de
esquina asimetricos, y un tooltip por fila que aparece al pasar el cursor o
al enfocar con teclado (`:hover`/`:focus-within`, sin JavaScript). Ningun
grafico nativo de Streamlit (`st.bar_chart`) da ese control pixel a pixel.

El HTML vive aqui, escapado con `html.escape`; el estilo vive en
`components/styles.py` bajo el selector `.grafico-card`.
"""

from __future__ import annotations

import html

import streamlit as st

# Fila: (categoria, ancho_pct de la barra, valor mostrado, texto del tooltip)
Fila = tuple[str, float, str, str]


def _fila(fila: Fila) -> str:
    categoria, ancho_pct, valor, tooltip = fila
    ancho = max(0.0, min(100.0, ancho_pct))
    return (
        '<div class="grafico-card__fila" tabindex="0">'
        f'<span class="grafico-card__categoria">{html.escape(categoria)}</span>'
        f'<div class="grafico-card__barra"><i style="width:{ancho}%"></i></div>'
        f'<span class="grafico-card__valor">{html.escape(valor)}</span>'
        f'<span class="grafico-card__tooltip">{html.escape(tooltip)}</span>'
        "</div>"
    )


def render_grafico_barras(
    titulo: str,
    descripcion: str,
    filas: list[Fila],
    nota: str,
) -> None:
    """Pinta una tarjeta completa: titulo + descripcion + filas + nota."""
    filas_html = "".join(_fila(fila) for fila in filas)

    st.markdown(
        f"""
        <div class="grafico-card">
            <h4>{html.escape(titulo)}</h4>
            <p class="grafico-card__descripcion">{html.escape(descripcion)}</p>
            <div class="grafico-card__filas">{filas_html}</div>
            <p class="grafico-card__nota">{html.escape(nota)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
