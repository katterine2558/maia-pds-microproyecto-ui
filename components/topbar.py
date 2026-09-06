"""Barra de titulo superior, compartida por las vistas.

Reemplaza `st.title` + `st.caption`: en vez de vivir en el flujo normal del
contenido, ocupa (via CSS, ver `components/styles.py`) la franja que deja
`[data-testid="stHeader"]`, con el titulo a la izquierda y un texto libre a
la derecha (tipicamente la fecha/hora, calculada por quien llama).

Este componente NO calcula nada (ni fecha, ni ningun otro dato): solo pinta
lo que la vista le pasa. El calculo de la fecha vive en `utils/fecha.py` y
se invoca desde la capa `views/`.
"""

from __future__ import annotations

import streamlit as st


def render_page_header(title: str, right_text: str | None = None, subtitle: str | None = None) -> None:
    """Pinta el titulo de la vista a la izquierda y `right_text` a la derecha."""
    right_html = f"<time>{right_text}</time>" if right_text else ""
    st.markdown(
        f"""
        <div class="app-topbar">
            <h1>{title}</h1>
            {right_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if subtitle:
        st.caption(subtitle)
