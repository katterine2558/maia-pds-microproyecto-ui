"""Vista: Paciente.

Detalle individual de un paciente: datos del encuentro y prediccion del
modelo obtenida a traves de la API.
"""

import streamlit as st

from components.tarjeta_resultado import render_tarjeta_resultado
from components.topbar import render_page_header
from services import api

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


def render() -> None:
    render_page_header("Evaluar paciente", "Predicción mediante la API")

    col_form, col_resultado = st.columns([1.05, 1], gap="large")

    with col_form:
        with st.container(key="paciente-formulario"):
            col_izq, col_der = st.columns(2)
            with col_izq:
                rango_edad = st.selectbox(
                    "Rango de edad", options=_RANGOS_EDAD, index=_RANGOS_EDAD.index("[70-80)"), filter_mode=None
                )
            with col_der:
                tipo_admision = st.selectbox("Tipo de admisión", options=_TIPOS_ADMISION, filter_mode=None)

            col_izq, col_der = st.columns(2)
            with col_izq:
                servicio_alta = st.selectbox("Servicio que da el alta", options=_SERVICIOS, filter_mode=None)
            with col_der:
                dias_estancia = st.number_input("Días de estancia", min_value=1, value=9, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                num_diagnosticos = st.number_input("N.º de diagnósticos", min_value=1, value=9, step=1)
            with col_der:
                num_medicamentos = st.number_input("N.º de medicamentos", min_value=1, value=21, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                ingresos_previos = st.number_input("Ingresos previos (1 año)", min_value=0, value=5, step=1)
            with col_der:
                urgencias_previas = st.number_input("Urgencias previas (1 año)", min_value=0, value=2, step=1)

            col_izq, col_der = st.columns(2)
            with col_izq:
                resultado_a1c = st.selectbox("Resultado de A1C", options=_RESULTADOS_A1C, filter_mode=None)
            with col_der:
                cambio_medicacion = st.selectbox("Cambio de medicación", options=_CAMBIO_MEDICACION, filter_mode=None)

            if st.button("Calcular riesgo", type="primary"):
                encuentro = {
                    "rango_edad": rango_edad,
                    "tipo_admision": tipo_admision,
                    "servicio_alta": servicio_alta,
                    "dias_estancia": dias_estancia,
                    "num_diagnosticos": num_diagnosticos,
                    "num_medicamentos": num_medicamentos,
                    "ingresos_previos": ingresos_previos,
                    "urgencias_previas": urgencias_previas,
                    "resultado_a1c": resultado_a1c,
                    "cambio_medicacion": cambio_medicacion,
                }
                try:
                    response = api.predecir(encuentro)
                    probabilidad = response.get("probabilidad")
                    if isinstance(probabilidad, bool) or not isinstance(probabilidad, (int, float)) or not 0 <= probabilidad <= 1:
                        raise api.ApiError("La API no devolvió una probabilidad válida entre 0 y 1.")
                    umbral = response.get("umbral")
                    if isinstance(umbral, bool) or not isinstance(umbral, (int, float)) or not 0 <= umbral <= 1:
                        raise api.ApiError("La API no devolvió el umbral de decisión del modelo.")
                    st.session_state["resultado_paciente"] = response
                except api.ApiError as exc:
                    st.session_state.pop("resultado_paciente", None)
                    st.error(str(exc))

    with col_resultado:
        resultado = st.session_state.get("resultado_paciente")
        if resultado is None:
            st.info("Ingresa los datos del encuentro y pulsa Calcular riesgo para consultar la API.")
        else:
            probabilidad = float(resultado["probabilidad"])
            umbral = resultado.get("umbral")
            nivel = "Alto" if probabilidad >= umbral else "Bajo"
            nota = f"Umbral de decisión: {umbral:.2f}. Resultado orientativo; requiere criterio clínico."
            render_tarjeta_resultado(
                probabilidad=probabilidad,
                nivel_riesgo=nivel,
                cohorte_pct=11.4,
                factores=[],
                nota=nota,
            )
            if resultado.get("modelo"):
                st.caption(f"Modelo: {resultado['modelo']}")
