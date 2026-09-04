"""Tablero de reingreso hospitalario a 30 dias.

Esqueleto inicial: verifica la conexion con la API y deja montadas las dos
secciones que exige el enunciado. El contenido de cada una se desarrolla en las
semanas 4 a 6, siguiendo la maqueta.
"""

import streamlit as st

from services import api

st.set_page_config(page_title="Reingreso a 30 dias", layout="wide")

st.title("Reingreso hospitalario a 30 dias")
st.caption("Pacientes diabeticos — apoyo a la decision de a quien agendar seguimiento al alta")

with st.sidebar:
    st.subheader("Conexion")
    st.code(api.API_URL, language=None)
    if st.button("Probar API"):
        try:
            st.success(api.salud())
        except api.ApiError as exc:
            st.error(str(exc))

prediccion, descriptivo = st.tabs(["Prediccion", "Datos"])

with prediccion:
    st.info("Pendiente: formulario de encuentro y llamada a `api.predecir`.")

with descriptivo:
    st.info("Pendiente: visualizaciones descriptivas segun la maqueta.")
