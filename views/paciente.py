"""Vista: Paciente.

Detalle individual de un paciente: datos del encuentro y prediccion del
modelo obtenida a traves de la API.
"""

import streamlit as st

from components.tarjeta_resultado import render_tarjeta_resultado
from components.topbar import render_page_header
from utils.fecha import formatear_fecha_hora

_RANGOS_EDAD = [
    "[0-10)",
    "[10-20)",
    "[20-30)",
    "[30-40)",
    "[40-50)",
    "[50-60)",
    "[60-70)",
    "[70-80)",
    "[80-90)",
    "[90-100)",
]
_TIPOS_ADMISION = ["Emergency", "Urgent", "Elective", "Newborn", "Not Available"]
_SERVICIOS = ["Nephrology", "InternalMedicine", "Emergency/Trauma", "Family/General", "Surgery-General", "Orthopedics", "Cardiology"]
_RESULTADOS_A1C = ["No medido", "Norm", ">7", ">8"]
_CAMBIO_MEDICACION = ["Sí", "No"]


_FACTORES_EJEMPLO = [
    ("5 ingresos previos en el último año", 100),
    ("Estancia de 9 días", 58),
    ("A1C no medida en el episodio", 41),
    ("9 diagnósticos registrados", 33),
    ("Alta desde nefrología", 26),
]


def render() -> None:
    render_page_header("Evaluar paciente", "POST /predict · 142 ms")

    col_form, col_resultado = st.columns([1.05, 1], gap="large")

    with col_form:
        with st.container(key="paciente-formulario"):
            col_izq, col_der = st.columns(2)
            with col_izq:
                st.selectbox("Rango de edad", options=_RANGOS_EDAD, index=_RANGOS_EDAD.index("[70-80)"), filter_mode=None)
            with col_der:
                st.selectbox("Tipo de admisión", options=_TIPOS_ADMISION, filter_mode=None)

            col_izq, col_der = st.columns(2)
            with col_izq:
                st.selectbox("Servicio que da el alta", options=_SERVICIOS, filter_mode=None)
            with col_der:
                st.number_input("Días de estancia", min_value=1, value=9, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                st.number_input("N.º de diagnósticos", min_value=1, value=9, step=1)
            with col_der:
                st.number_input("N.º de medicamentos", min_value=1, value=21, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                st.number_input("Ingresos previos (1 año)", min_value=0, value=5, step=1)
            with col_der:
                st.number_input("Urgencias previas (1 año)", min_value=0, value=2, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                st.selectbox("Resultado de A1C", options=_RESULTADOS_A1C, filter_mode=None)
            with col_der:
                st.selectbox("Cambio de medicación", options=_CAMBIO_MEDICACION, filter_mode=None)

            st.button("Calcular riesgo", type="primary")

    with col_resultado:
        render_tarjeta_resultado(
            probabilidad=0.52,
            nivel_riesgo="Alto",
            cohorte_pct=11.4,
            factores=_FACTORES_EJEMPLO,
            nota="La probabilidad se muestra calibrada. Un valor sin calibrar induce a error al usuario clínico.",
        )
