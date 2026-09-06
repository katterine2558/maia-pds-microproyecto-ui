"""Tablero de reingreso hospitalario a 30 dias.

Esqueleto inicial: verifica la conexion con la API y deja montadas las dos
secciones que exige el enunciado. El contenido de cada una se desarrolla en las
semanas 4 a 6, siguiendo la maqueta.
"""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import load_css
from config.nav import NAV_ITEMS
from views import contexto, paciente, priorizacion


st.set_page_config(page_title="Reingreso a 30 dias", layout="wide")
load_css()

_VIEW_RENDERERS = {
    "priorizacion": priorizacion.render,
    "paciente": paciente.render,
    "contexto": contexto.render,
}
UNIDADES_DISPONIBLES = ["Hospital central"]

paginas_por_key = {
    item.key: st.Page(
        _VIEW_RENDERERS[item.key],
        title=item.label,
        url_path=item.key,
        default=(item.key == NAV_ITEMS[0].key),
    )
    for item in NAV_ITEMS
}

pagina_activa = st.navigation(list(paginas_por_key.values()), position="hidden")

unidad_seleccionada = render_sidebar(
    nav_items=NAV_ITEMS,
    pages_by_key=paginas_por_key,
    # La pagina default de st.Page siempre tiene url_path == "" (el parametro
    # url_path se ignora para ella), asi que el "" se traduce de vuelta al key
    # del primer item del nav para que el resaltado de seleccionado funcione.
    active_key=pagina_activa.url_path or NAV_ITEMS[0].key,
    unidades=UNIDADES_DISPONIBLES,
    unidad_actual=UNIDADES_DISPONIBLES[0],
)

pagina_activa.run()

