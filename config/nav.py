"""Definicion del menu de navegacion del sidebar.

Un solo lugar para agregar, quitar o reordenar pantallas. `app.py` recorre
`NAV_ITEMS` para registrar las paginas en `st.navigation`; este modulo no
conoce Streamlit ni las funciones de render de `views/`, solo describe el
menu (orden, etiqueta, icono).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NavItem:
    key: str
    label: str
    icon: str  # caracter Unicode simple; sin dependencia de fuentes externas


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem(key="priorizacion", label="Priorización", icon=":material/priority_high:"),
    NavItem(key="paciente", label="Paciente", icon=":material/person:"),
    NavItem(key="contexto", label="Contexto", icon=":material/dashboard:"),
)