"""Tokens de diseno del tablero: colores y tipografia.

Centralizar estos valores aqui evita que un color o una fuente queden
hardcodeados dentro de un componente. Los valores de color son una
aproximacion visual a la maqueta (`uxui/`) y se ajustan en una iteracion
posterior una vez el equipo confirme la paleta definitiva; el objetivo de
esta capa es que ese ajuste se haga en un solo lugar.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    # Sidebar
    sidebar_bg: str = "#12302A"
    sidebar_bg_active: str = "#1D4B41"
    sidebar_text: str = "#F4F6F5"
    sidebar_text_muted: str = "#8FA39C"

    # Superficie general
    app_bg: str = "#FBFDFC"
    card_bg: str = "#F6F8F7"
    card_border: str = "#E3E6E4"
    text_primary: str = "#1B1F1E"
    text_muted: str = "#6B7570"
    # Gris intermedio, mas oscuro que text_muted (categorias/descripciones
    # de los graficos de barras del panel de Contexto).
    text_muted_strong: str = "#4C625E"

    # Track de barras de progreso (panel de paciente)
    track_bg: str = "#E6ECEA"

    # Acento (botones primarios, indicador de pagina activa)
    accent: str = "#1E5F52"

    # Riesgo (badges de la tabla de priorizacion y del panel de paciente)
    risk_high: str = "#B3261E"
    risk_high_bg: str = "#FBE0DE"
    risk_medium: str = "#B8860B"
    risk_medium_bg: str = "#FBF0DC"
    risk_low: str = "#2E7D32"
    risk_low_bg: str = "#E3F2E4"


@dataclass(frozen=True)
class Typography:
    # Titulos de pantalla ("Egresos programados", "Evaluar paciente"...)
    heading_font: str = "Georgia, 'Times New Roman', serif"
    # Labels, encabezados de tabla y cifras (uppercase, letter-spacing)
    mono_font: str = (
        "ui-monospace, 'SFMono-Regular', 'JetBrains Mono', Menlo, Consolas, monospace"
    )
    # Texto de cuerpo (parrafos, widgets)
    body_font: str = (
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    )


COLORS = Colors()
TYPOGRAPHY = Typography()