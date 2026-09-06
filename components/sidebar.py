from __future__ import annotations

import streamlit as st

from config.nav import NavItem

APP_TITLE = "Reingreso 30d"
APP_SUBTITLE = "GESTIÓN HOSPITALARIA"
APP_VERSION_LABEL = "v0.1 · maqueta"


def render_sidebar(
    nav_items: tuple[NavItem, ...],
    pages_by_key: dict[str, "st.Page"],
    active_key: str,
    unidades: list[str],
    unidad_actual: str,
) -> str:
    """Pinta el sidebar completo, de arriba a abajo.

    Devuelve la unidad seleccionada para que `app.py` la pueda propagar a
    las pantallas cuando empiecen a filtrar por unidad.
    """
    with st.sidebar:
        _render_header()
        _render_nav(nav_items, pages_by_key, active_key)
        unidad = _render_unidad(unidades, unidad_actual)
        _render_footer()
    return unidad


def _render_header() -> None:
    with st.container(key="reingreso-30d", gap="xxsmall"):
        st.subheader("Regingreso 30d")
        st.caption("GESTION HOSPITALARIA")


def _render_nav(
    nav_items: tuple[NavItem, ...],
    pages_by_key: dict[str, "st.Page"],
    active_key: str,
) -> None:
    for item in nav_items:
        is_active = item.key == active_key
        nav_slot = st.container(key="nav-item-active") if is_active else st.container()
        with nav_slot:
            st.page_link(
                pages_by_key[item.key],
                label=item.label,
                icon=item.icon,
                disabled=is_active,
            )

def _render_unidad(unidades: list[str], unidad_actual: str) -> str:
    with st.container(key="sidebar-section-label"):
        st.caption('UNIDAD')
    return st.selectbox(
        "Unidad",
        options=unidades,
        index=unidades.index(unidad_actual) if unidad_actual in unidades else 0,
        label_visibility="collapsed",
        filter_mode=None,
    )

def _render_footer() -> None:
    with st.container(key="sidebar-footer"):
        st.caption(APP_VERSION_LABEL)