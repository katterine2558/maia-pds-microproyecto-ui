"""Card de metrica: label + valor + subtitulo.

Usa widgets nativos de Streamlit (`st.container` con borde + `st.metric`) en
vez de HTML manual, siguiendo la convencion del resto de `components/`: el
estilo vive en `components/styles.py`, aplicado via la clase `st-key-<key>`
que Streamlit genera para cada contenedor.
"""

from __future__ import annotations

from typing import Literal

import streamlit as st

Variant = Literal["default", "alert"]


def render_metric_card(
    key: str,
    label: str,
    value: str,
    subtitle: str,
    variant: Variant = "default",
) -> None:
    """Pinta una card de metrica: label + valor + subtitulo.

    `key` debe ser unico en la pagina; se usa para el contenedor y, via CSS
    (ver `components/styles.py`), para aplicar el estilo segun `variant`.
    """
    prefix = "metric-card-alert" if variant == "alert" else "metric-card"
    with st.container(border=True, key=f"{prefix}-{key}"):
        st.metric(
            label=label,
            value=value,
            delta=subtitle,
            delta_color="off",
            delta_arrow="off",
        )
