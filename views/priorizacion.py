"""Vista: Priorizacion.

Lista de egresos ordenados por riesgo de reingreso, para apoyar la decision de
a quien agendar seguimiento al alta.

El usuario sube el archivo de egresos del turno y el tablero pide una
prediccion por fila a la API. La lista sale del `POST /predict` del modelo
empaquetado, igual que la vista Paciente: aqui tampoco se carga un artefacto ni
se lee `data/`.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components.metric_card import render_metric_card
from components.tabla_priorizacion import render_tabla_priorizacion
from components.topbar import render_page_header
from services import api
from utils import egresos as lector
from utils.fecha import formatear_fecha_hora
from utils.riesgo import nivel_de_riesgo

_CAPACIDADES = [10, 20, 30, 50]
_TODOS = "Todos"

_PLANTILLA = (
    "encuentro,rango_edad,tipo_admision,servicio_alta,dias_estancia,"
    "num_diagnosticos,num_medicamentos,ingresos_previos,urgencias_previas,"
    "resultado_a1c,cambio_medicacion\n"
    "ENC-8271,[70-80),Emergency,Nephrology,9,9,21,5,2,No medido,Sí\n"
    "ENC-4410,[80-90),Urgent,InternalMedicine,12,8,18,4,1,>8,Sí\n"
    "ENC-9017,[50-60),Elective,Cardiology,3,5,7,0,0,Norm,No\n"
)


def _cargar() -> None:
    """Lee el archivo subido, pide las predicciones y guarda el resultado."""
    archivo = st.session_state.get("priorizacion-archivo")
    if archivo is None:
        st.session_state.pop("priorizacion-resultado", None)
        return

    try:
        egresos = lector.leer(archivo)
    except lector.ArchivoInvalido as exc:
        st.session_state["priorizacion-error"] = str(exc)
        st.session_state.pop("priorizacion-resultado", None)
        return

    with st.spinner(f"Consultando la API para {egresos.total} egresos…"):
        respuestas = api.predecir_lote(egresos.encuentros())

    errores = [r for r in respuestas if isinstance(r, api.ApiError)]
    if len(errores) == len(respuestas):
        st.session_state["priorizacion-error"] = (
            f"Ningun egreso pudo evaluarse. {errores[0]}"
        )
        st.session_state.pop("priorizacion-resultado", None)
        return

    filas = []
    for (_, fila), respuesta in zip(egresos.tabla.iterrows(), respuestas):
        if isinstance(respuesta, api.ApiError):
            continue
        probabilidad = float(respuesta["probabilidad"])
        umbral = float(respuesta["umbral"])
        filas.append(
            {
                "Encuentro": fila[lector.COLUMNA_ENCUENTRO],
                "Edad": fila["rango_edad"],
                "Servicio": fila["servicio_alta"],
                "Estancia": f"{fila['dias_estancia']} d",
                "Ingresos previos": int(fila["ingresos_previos"]),
                "A1C": fila["resultado_a1c"],
                "Riesgo": nivel_de_riesgo(probabilidad, umbral),
                "Prob.": probabilidad,
            }
        )

    st.session_state.pop("priorizacion-error", None)
    st.session_state["priorizacion-resultado"] = {
        "tabla": pd.DataFrame(filas).sort_values(
            "Prob.", ascending=False, ignore_index=True
        ),
        "descartados": len(errores),
        "archivo": archivo.name,
    }


def _metricas(tabla: pd.DataFrame, capacidad: int) -> None:
    total = len(tabla)
    atendidos = tabla.head(capacidad)
    riesgo_total = float(tabla["Prob."].sum())
    cubierto = float(atendidos["Prob."].sum()) / riesgo_total if riesgo_total else 0.0
    altos_sin_cubrir = int((tabla.tail(max(total - capacidad, 0))["Riesgo"] == "Alto").sum())

    cards = (
        ("egresos", "EGRESOS CARGADOS", str(total), "encuentros evaluados", "default"),
        ("capacidad", "CAPACIDAD", str(min(capacidad, total)), "seguimientos agendables", "default"),
        ("cubre", "CUBRE", f"{cubierto:.0%}", "del riesgo estimado", "default"),
        (
            "riesgo-alto",
            "RIESGO ALTO SIN CUBRIR",
            str(altos_sin_cubrir),
            "quedan bajo la línea",
            "alert" if altos_sin_cubrir else "default",
        ),
    )
    for columna, (key, label, valor, subtitulo, variante) in zip(st.columns(len(cards)), cards):
        with columna:
            render_metric_card(key, label, valor, subtitulo, variante)


def _sin_lista() -> None:
    """Estado inicial: no hay archivo cargado todavia."""
    st.info(
        "Sube el archivo de egresos del turno para ordenarlos por riesgo. "
        "El tablero pide una predicción por egreso a la API."
    )
    st.download_button(
        "Descargar plantilla de ejemplo",
        data=_PLANTILLA,
        file_name="egresos-ejemplo.csv",
        mime="text/csv",
    )
    with st.expander("Columnas que debe traer el archivo"):
        st.write(", ".join(f"`{c}`" for c in lector.COLUMNAS_REQUERIDAS))
        st.caption(
            "`encuentro` identifica al paciente en la lista y no viaja a la API. "
            "Las demás son las diez variables del modelo, con los mismos valores "
            "que ofrece el formulario de Paciente."
        )


def render() -> None:
    render_page_header("Egresos programados", formatear_fecha_hora())

    with st.container(key="priorizacion-carga"):
        st.file_uploader(
            "Archivo de egresos (CSV)",
            type="csv",
            key="priorizacion-archivo",
            on_change=_cargar,
        )

    error = st.session_state.get("priorizacion-error")
    if error:
        st.error(error)

    resultado = st.session_state.get("priorizacion-resultado")
    if resultado is None:
        _sin_lista()
        return

    tabla: pd.DataFrame = resultado["tabla"]
    if resultado["descartados"]:
        st.warning(
            f"{resultado['descartados']} egreso(s) del archivo no pudieron evaluarse "
            "y quedaron fuera de la lista."
        )

    with st.container(key="priorizacion-filtros"):
        col_servicio, col_capacidad, col_descarga = st.columns([1, 1, 1], vertical_alignment="bottom")

        with col_servicio:
            servicios = [_TODOS, *sorted(tabla["Servicio"].unique())]
            servicio = st.selectbox("Servicio", options=servicios, filter_mode=None)

        with col_capacidad:
            capacidad = st.selectbox(
                "Capacidad de seguimiento",
                options=_CAPACIDADES,
                format_func=lambda n: f"{n} pacientes",
                index=1,
                filter_mode=None,
            )

    if servicio != _TODOS:
        tabla = tabla[tabla["Servicio"] == servicio].reset_index(drop=True)

    if tabla.empty:
        st.info("Ningún egreso del archivo corresponde a ese servicio.")
        return

    _metricas(tabla, capacidad)

    with col_descarga:
        st.download_button(
            "Descargar lista",
            data=tabla.to_csv(index=False).encode("utf-8"),
            file_name=f"priorizacion-{resultado['archivo']}",
            mime="text/csv",
            width=200,
        )

    with st.container(key="priorizacion-tabla"):
        numerada = tabla.assign(**{"#": range(1, len(tabla) + 1)})
        filas = numerada.to_dict(orient="records")
        sobre_capacidad = filas[:capacidad]
        bajo_capacidad = filas[capacidad:]
        texto_linea_capacidad = (
            f"LÍNEA DE CAPACIDAD — {min(capacidad, len(filas))} de {len(filas)} · "
            "debajo no alcanza el recurso de hoy"
        )
        render_tabla_priorizacion(sobre_capacidad, bajo_capacidad, texto_linea_capacidad)
