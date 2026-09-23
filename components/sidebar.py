from __future__ import annotations

import streamlit as st

from config.nav import NavItem

APP_TITLE = "Reingreso 30d"
APP_SUBTITLE = "GESTIÓN HOSPITALARIA"
APP_VERSION_LABEL = "v1.0 · Entrega 3"


def render_sidebar(
    nav_items: tuple[NavItem, ...],
    pages_by_key: dict[str, "st.Page"],
    active_key: str,
) -> None:
    """Pinta el sidebar completo, de arriba a abajo."""
    with st.sidebar:
        _render_header()
        _render_nav(nav_items, pages_by_key, active_key)
        _render_footer()


def _render_header() -> None:
    with st.container(key="reingreso-30d", gap="xxsmall"):
        st.subheader("Reingreso 30d")
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

def _render_footer() -> None:
    with st.container(key="sidebar-footer"):
        st.caption(APP_VERSION_LABEL)