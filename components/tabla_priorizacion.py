"""Tabla de priorizacion: HTML a medida.

Excepcion deliberada al patron "solo widgets nativos" del resto de la app,
igual que `components/topbar.py` (ver su docstring): la maqueta
(`ux-ui/pantallas.html`) pide una sola tabla continua, sin lineas
verticales, con badges de riesgo (punto + texto en negrita) y una fila
divisoria de capacidad que no la corte en pedazos.

Ningun widget nativo de Streamlit llega a eso:
- `st.dataframe` se pinta en un `<canvas>` (glide-data-grid): el CSS de
  `components/styles.py` no puede tocar su tipografia ni sus colores mas
  alla de fondo/texto plano via `pandas.Styler`.
- `st.table` genera una tabla HTML real, pero sin control de bordes por eje,
  sin `colspan` para una fila divisoria, e interpreta cada celda como
  Markdown (por eso `>7` se veia como una cita, no como texto literal).

Por eso este componente construye el HTML el mismo, con los valores
escapados (`html.escape`), y todo su estilo vive en `components/styles.py`
bajo el selector `.tabla-priorizacion`, igual que el resto del CSS del
proyecto.
"""

from __future__ import annotations

import html
from typing import Optional

import streamlit as st

from config.theme import COLORS

_COLUMNAS = [
    "#",
    "Encuentro",
    "Edad",
    "Servicio",
    "Estancia",
    "Ingresos previos",
    "A1C",
    "Riesgo",
    "Prob.",
]
# Columnas con fuente mono/tabular, igual que ".n" en ux-ui/pantallas.html.
_COLUMNAS_MONO = {"#", "Encuentro", "Estancia", "Ingresos previos", "Prob."}

_RIESGO_COLORES = {
    "Alto": (COLORS.risk_high, COLORS.risk_high_bg),
    "Medio": (COLORS.risk_medium, COLORS.risk_medium_bg),
    "Bajo": (COLORS.risk_low, COLORS.risk_low_bg),
}


def _celda(columna: str, valor: object) -> str:
    clase = ' class="n"' if columna in _COLUMNAS_MONO else ""

    if columna == "Riesgo":
        color, fondo = _RIESGO_COLORES[str(valor)]
        texto = html.escape(str(valor))
        return (
            f'<td{clase}><span class="pill" '
            f'style="color:{color};background-color:{fondo};">'
            f'<i style="background-color:{color};"></i>{texto}</span></td>'
        )

    if columna == "Prob.":
        valor = f"{float(valor):.2f}".replace(".", ",")

    return f"<td{clase}>{html.escape(str(valor))}</td>"


def _fila(fila: dict) -> str:
    celdas = "".join(_celda(columna, fila[columna]) for columna in _COLUMNAS)
    return f"<tr>{celdas}</tr>"


def _fila_divisoria(texto: str) -> str:
    columnas = len(_COLUMNAS)
    return (
        f'<tr class="cutrow"><td colspan="{columnas}">'
        f'<div class="cutline">{html.escape(texto)}</div></td></tr>'
    )


def render_tabla_priorizacion(
    filas_sobre_capacidad: list[dict],
    filas_bajo_capacidad: list[dict],
    texto_linea_capacidad: Optional[str],
) -> None:
    """Pinta la tabla completa como una sola pieza (thead + tbody).

    Si `filas_bajo_capacidad` no esta vacia, inserta la fila divisoria de
    capacidad (`texto_linea_capacidad`) entre ambos grupos, dentro del mismo
    `<table>`, para que se vea como una tabla continua y no como piezas
    separadas.
    """
    encabezado = "".join(f"<th>{html.escape(c)}</th>" for c in _COLUMNAS)

    cuerpo = "".join(_fila(fila) for fila in filas_sobre_capacidad)
    if texto_linea_capacidad and filas_bajo_capacidad:
        cuerpo += _fila_divisoria(texto_linea_capacidad)
        cuerpo += "".join(_fila(fila) for fila in filas_bajo_capacidad)

    st.markdown(
        f"""
        <div class="tabla-priorizacion">
            <table>
                <thead><tr>{encabezado}</tr></thead>
                <tbody>{cuerpo}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
