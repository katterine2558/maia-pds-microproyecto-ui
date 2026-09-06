"""Vista: Priorizacion.

Lista de pacientes ordenados por riesgo de reingreso, para apoyar la
decision de a quien agendar seguimiento al alta.
"""

from datetime import date

import streamlit as st

from components.metric_card import render_metric_card
from components.tabla_priorizacion import render_tabla_priorizacion
from components.topbar import render_page_header
from utils.fecha import formatear_fecha_hora

_TOTAL_EGRESOS = 63

_CARDS = (
    ("egresos", "EGRESOS DEL DÍA", str(_TOTAL_EGRESOS), "pacientes diabéticos", "default"),
    ("capacidad", "CAPACIDAD", "20", "seguimientos agendables", "default"),
    ("cubre", "CUBRE", "78 %", "del riesgo estimado", "default"),
    ("riesgo-alto", "RIESGO ALTO SIN CUBRIR", "4", "quedan bajo la línea", "alert"),
)

_SERVICIOS = ["Todos", "Nephrology", "InternalMedicine", "Emergency/Trauma", "Family/General", "Cardiology"]
_CAPACIDADES = [10, 20, 30, 50]

# Datos de ejemplo (ilustrativos, ver ux-ui/pantallas.html). Se reemplazan por
# datos reales de la API cuando exista un endpoint de listado de pacientes.
_PACIENTES_EJEMPLO = [
    {"#": 1, "Encuentro": "ENC-8271", "Edad": "[70-80)", "Servicio": "Nephrology", "Estancia": "9 d", "Ingresos previos": 5, "A1C": "No medido", "Riesgo": "Alto", "Prob.": 0.52},
    {"#": 2, "Encuentro": "ENC-4410", "Edad": "[80-90)", "Servicio": "InternalMedicine", "Estancia": "12 d", "Ingresos previos": 4, "A1C": ">8", "Riesgo": "Alto", "Prob.": 0.44},
    {"#": 3, "Encuentro": "ENC-1938", "Edad": "[60-70)", "Servicio": "Emergency/Trauma", "Estancia": "6 d", "Ingresos previos": 3, "A1C": "No medido", "Riesgo": "Alto", "Prob.": 0.38},
    {"#": 4, "Encuentro": "ENC-6104", "Edad": "[70-80)", "Servicio": "Nephrology", "Estancia": "7 d", "Ingresos previos": 3, "A1C": "Norm", "Riesgo": "Alto", "Prob.": 0.34},
    {"#": 19, "Encuentro": "ENC-2286", "Edad": "[50-60)", "Servicio": "InternalMedicine", "Estancia": "5 d", "Ingresos previos": 1, "A1C": ">7", "Riesgo": "Medio", "Prob.": 0.21},
    {"#": 20, "Encuentro": "ENC-7702", "Edad": "[60-70)", "Servicio": "Family/General", "Estancia": "4 d", "Ingresos previos": 1, "A1C": "No medido", "Riesgo": "Medio", "Prob.": 0.19},
    {"#": 21, "Encuentro": "ENC-3355", "Edad": "[70-80)", "Servicio": "Nephrology", "Estancia": "6 d", "Ingresos previos": 2, "A1C": "No medido", "Riesgo": "Medio", "Prob.": 0.18},
    {"#": 22, "Encuentro": "ENC-9017", "Edad": "[50-60)", "Servicio": "Cardiology", "Estancia": "3 d", "Ingresos previos": 0, "A1C": "Norm", "Riesgo": "Bajo", "Prob.": 0.07},
]


def render() -> None:
    render_page_header("Egresos programados", formatear_fecha_hora())

    columnas = st.columns(len(_CARDS))
    for columna, (key, label, valor, subtitulo, variante) in zip(columnas, _CARDS):
        with columna:
            render_metric_card(key, label, valor, subtitulo, variante)

    with st.container(key="priorizacion-filtros"):
        col_fecha, col_servicio, col_capacidad, col_boton = st.columns(
            [1, 1, 1, 1], vertical_alignment="bottom"
        )

        with col_fecha:
            st.date_input("Fecha de alta", value=date(2026, 8, 17), format="DD/MM/YYYY")

        with col_servicio:
            st.selectbox("Servicio", options=_SERVICIOS, filter_mode=None)

        with col_capacidad:
            capacidad = st.selectbox(
                "Capacidad de seguimiento",
                options=_CAPACIDADES,
                format_func=lambda n: f"{n} pacientes",
                index=1,
                filter_mode=None,
            )

        with col_boton:
            st.button("Actualizar lista", type="primary", width=200)

    with st.container(key="priorizacion-tabla"):
        sobre_capacidad = [f for f in _PACIENTES_EJEMPLO if f["#"] <= capacidad]
        bajo_capacidad = [f for f in _PACIENTES_EJEMPLO if f["#"] > capacidad]
        texto_linea_capacidad = (
            f"LÍNEA DE CAPACIDAD — {capacidad} de {_TOTAL_EGRESOS} · "
            "debajo no alcanza el recurso de hoy"
        )
        render_tabla_priorizacion(sobre_capacidad, bajo_capacidad, texto_linea_capacidad)
