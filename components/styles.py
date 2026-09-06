import streamlit as st

from config.theme import COLORS, TYPOGRAPHY

def load_css() -> None:
    """Inyecta el CSS global. Llamar una sola vez, al inicio de `app.py`."""
    st.markdown(f"<style>{_build_css()}</style>", unsafe_allow_html=True)

def _build_css() -> str:
    c = COLORS
    t = TYPOGRAPHY
    return f"""
    .stApp {{
        background-color: {c.app_bg};
    }}

    h1, h2, h3 {{
        font-family: {t.heading_font} !important;
        color: {c.text_primary};
    }}

    /* ---- Barra superior de Streamlit: sin "Deploy" ni menu, no son parte
    de la maqueta.

    Se ocultan las piezas una por una y NO la barra completa. Streamlit
    renderiza dentro de `stToolbar` el boton que vuelve a abrir el sidebar
    cuando esta colapsado; al ocultar `stToolbar` entero ese boton queda con
    caja de 0px y colapsar el sidebar se vuelve un camino sin retorno.

    El header se deja sin fondo y sin capturar clics: cuando Streamlit detecta
    el indicador de "running" le pone un fondo blanco opaco que, al estar por
    encima en z-index, tapa nuestro topbar aunque sus botones ya esten
    ocultos. El boton de reabrir el sidebar recupera los clics por su cuenta,
    mas abajo. ---- */

    [data-testid="stToolbarActions"] {{
        display: none !important;
    }}

    [data-testid="stAppDeployButton"] {{
        display: none !important;
    }}

    [data-testid="stStatusWidget"] {{
        display: none !important;
    }}

    [data-testid="stDecoration"] {{
        display: none !important;
    }}

    #MainMenu {{
        display: none !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
        pointer-events: none !important;
    }}

    /* Unico control del header que si debe recibir clics. */
    [data-testid="stExpandSidebarButton"] {{
        pointer-events: auto !important;
        color: {c.text_primary} !important;
    }}

    /* ---- Streamlit reserva 6rem de padding-top en el contenedor principal
    para dejar sitio al header por defecto (deploy/menu). Como aqui el
    header queda transparente y sin controles (el sidebar esta siempre
    visible), lo reducimos a un espacio minimo. ---- */

    [data-testid="stMainBlockContainer"] {{
        padding-top: 0.8rem !important;
    }}

    /* ---- Topbar por vista: reemplaza st.title/st.caption. ---- */

    .app-topbar {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 1rem;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid {c.card_border};
        margin-bottom: 1rem;
    }}

    .app-topbar h1 {{
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        /* Con !important porque la regla `h1, h2, h3` de mas arriba pierde
        por especificidad contra la propia hoja de Streamlit. */
        color: {c.text_primary} !important;
    }}

    .app-topbar time {{
        font-family: {t.mono_font};
        font-size: 0.85rem;
        color: {c.text_muted};
        white-space: nowrap;
    }}

    /* ---- Sidebar: contenedor y tipografia base ---- */

    [data-testid="stSidebar"] {{
        background-color: {c.sidebar_bg};
    }}

    [data-testid="stSidebar"] * {{
        color: {c.sidebar_text};
    }}

    [data-testid="stSidebarUserContent"] {{
        padding-top: 1.5rem !important;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }}

    /* ---- Titulo del sidebnar ---- */

    .st-key-reingreso-30d {{
        margin-top: -4rem;
        margin-bottom: 2rem;
    }}

    .st-key-reingreso-30d .stHeading h3 {{
        font-family: {t.heading_font};
        font-weight: 200;
        font-size: 1.35rem;
        line-height: 1.2;
    }}

    .st-key-reingreso-30d [data-testid="stCaptionContainer"] {{
        font-family: {t.mono_font};
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        color: {c.sidebar_text_muted} !important;
    }}

    /* ---- Menu page links ---- */

    [data-testid="stSidebar"] [data-testid="stPageLink"] a {{
        padding: 0.5rem 0.75rem;
    }}

    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {{
        background-color: rgba(255, 255, 255, 0.08);
    }}

    .st-key-nav-item-active a {{
        width: 100%;
        justify-content: flex-start;
        text-align: left;
        border: none;
        border-radius: 6px;
        background-color: {c.sidebar_bg_active};
        font-family: {t.body_font};
        font-weight: 400;
    }}

    /* ---- Selección de unidad ---- */

    .st-key-sidebar-section-label {{
        font-family: {t.mono_font};
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        color: {c.sidebar_text_muted} !important;
        margin-top: 2rem;
    }}

    /* Streamlit 1.63 cambio el selectbox de BaseWeb a react-aria: se cubren
    las dos marcas para no depender de la version. El sidebar es la unica
    superficie oscura del tablero, asi que su selector necesita fondo propio;
    los del area principal los resuelve el tema claro. ---- */

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .react-aria-ComboBox > div,
    [data-testid="stSidebar"] .react-aria-ComboBox input {{
        background-color: {c.sidebar_bg_active} !important;
        border-color: {c.sidebar_text_muted} !important;
        color: {c.sidebar_text} !important;
    }}

    [data-testid="stSidebar"] .react-aria-ComboBox input::placeholder {{
        color: {c.sidebar_text_muted} !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] svg,
    [data-testid="stSidebar"] .react-aria-ComboBox svg {{
        fill: {c.sidebar_text} !important;
        color: {c.sidebar_text} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSelectbox"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] * {{
        cursor: pointer !important;
    }}

    /* ---- Footer del sidebar ---- */

    .st-key-sidebar-footer {{
        position: absolute;
        bottom: 1rem;
    }}

    .st-key-sidebar-footer,
    .st-key-sidebar-footer * {{
        font-family: {t.mono_font};
        font-size: 0.7rem;
        color: {c.sidebar_text_muted} !important;
    }}

    /* ---- Cards de metricas (fila superior de Priorizacion) ---- */

    [class*="st-key-metric-card-"] {{
        background-color: {c.card_bg} !important;
        border-color: {c.card_border} !important;
    }}

    [class*="st-key-metric-card-"] [data-testid="stMetricLabel"] {{
        font-family: {t.mono_font};
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {c.text_muted};
    }}

    [class*="st-key-metric-card-"] [data-testid="stMetricValue"] {{
        font-family: {t.heading_font};
    }}

    [class*="st-key-metric-card-"] [data-testid="stMetricDelta"],
    [class*="st-key-metric-card-"] [data-testid="stMetricDelta"] * {{
        font-family: {t.body_font};
        color: {c.text_muted} !important;
        background: transparent !important;
        background-color: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
    }}

    [class*="st-key-metric-card-alert-"] {{
        background-color: {c.risk_high_bg} !important;
        border-color: {c.risk_high_bg} !important;
    }}

    [class*="st-key-metric-card-alert-"] [data-testid="stMetricLabel"],
    [class*="st-key-metric-card-alert-"] [data-testid="stMetricValue"],
    [class*="st-key-metric-card-alert-"] [data-testid="stMetricDelta"],
    [class*="st-key-metric-card-alert-"] [data-testid="stMetricDelta"] * {{
        color: {c.risk_high} !important;
    }}

    /* ---- Campos de formulario: fila de filtros de Priorizacion y
    formulario de Paciente comparten el mismo estilo de labels, selects y
    boton primario. ---- */

    .st-key-priorizacion-filtros [data-testid="stWidgetLabel"],
    .st-key-paciente-formulario [data-testid="stWidgetLabel"] {{
        font-family: {t.mono_font};
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {c.text_muted};
    }}

    .st-key-priorizacion-filtros [data-testid="stButton"] button[kind="primary"],
    .st-key-paciente-formulario [data-testid="stButton"] button[kind="primary"] {{
        background-color: {c.accent};
        border-color: {c.accent};
        padding-top: 0.35rem;
        padding-bottom: 0.35rem;
    }}

    .st-key-priorizacion-filtros [data-testid="stButton"] button[kind="primary"]:hover,
    .st-key-paciente-formulario [data-testid="stButton"] button[kind="primary"]:hover {{
        background-color: {c.accent};
        opacity: 0.9;
    }}

    .st-key-priorizacion-filtros [data-testid="stSelectbox"],
    .st-key-priorizacion-filtros [data-testid="stSelectbox"] *,
    .st-key-paciente-formulario [data-testid="stSelectbox"],
    .st-key-paciente-formulario [data-testid="stSelectbox"] * {{
        cursor: pointer !important;
    }}

    /* ---- Cajas de texto del formulario de Paciente: fondo transparente,
    tanto en los selects como en los number_input. ---- */

    .st-key-paciente-formulario [data-baseweb="select"] > div,
    .st-key-paciente-formulario [data-testid="stNumberInputContainer"],
    .st-key-paciente-formulario [data-testid="stNumberInputContainer"] * {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* ---- Tabla de Priorizacion (HTML propio, ver components/tabla_priorizacion.py) ---- */

    .tabla-priorizacion {{
        border: 1px solid {c.card_border};
        border-radius: 6px;
        overflow: hidden;
    }}

    .tabla-priorizacion table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}

    .tabla-priorizacion th,
    .tabla-priorizacion td {{
        text-align: left;
        padding: 0.5rem 0.85rem;
        white-space: nowrap;
    }}

    .tabla-priorizacion thead th {{
        background-color: {c.card_bg};
        font-family: {t.mono_font};
        font-size: 0.65rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {c.text_muted};
        font-weight: 600;
        border-bottom: 1px solid {c.card_border};
    }}

    .tabla-priorizacion tbody td {{
        font-family: {t.body_font};
        color: {c.text_primary};
        border-bottom: 1px solid {c.card_border};
    }}

    .tabla-priorizacion tbody td.n {{
        font-family: {t.mono_font};
        font-variant-numeric: tabular-nums;
    }}

    .tabla-priorizacion tbody tr:last-child td {{
        border-bottom: none;
    }}

    .tabla-priorizacion tbody tr:hover td {{
        background-color: {c.app_bg};
    }}

    .tabla-priorizacion .pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.1rem 0.6rem 0.1rem 0.45rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
    }}

    .tabla-priorizacion .pill i {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: block;
    }}

    .tabla-priorizacion .cutrow td {{
        padding: 0;
        border-bottom: none;
    }}

    .tabla-priorizacion .cutline {{
        padding: 0.45rem 0.85rem;
        background-color: {c.accent}12;
        border-top: 1px dashed {c.accent};
        border-bottom: 1px dashed {c.accent};
        font-family: {t.mono_font};
        font-size: 0.68rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: {c.accent};
        font-weight: 600;
    }}

    /* ---- Tarjeta de resultado del panel de Paciente (HTML propio, ver
    components/tarjeta_resultado.py) ---- */

    .tarjeta-resultado {{
        border: 1px solid {c.card_border};
        border-radius: 6px;
        overflow: hidden;
    }}

    .tarjeta-resultado__header {{
        display: flex;
        align-items: center;
        gap: 1.1rem;
        padding: 1.1rem 1.25rem;
    }}

    .tarjeta-resultado__valor {{
        font-family: {t.heading_font};
        font-size: 2.7rem;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }}

    .tarjeta-resultado__etiqueta {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }}

    .tarjeta-resultado__etiqueta b {{
        font-size: 0.85rem;
        font-weight: 700;
    }}

    .tarjeta-resultado__etiqueta span {{
        font-size: 0.75rem;
        opacity: 0.82;
    }}

    .tarjeta-resultado__body {{
        padding: 1rem 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }}

    .tarjeta-resultado__subtitulo {{
        font-family: {t.mono_font};
        font-size: 0.72rem !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: {c.text_muted};
        margin: 0;
    }}

    .tarjeta-resultado__factores {{
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }}

    .tarjeta-resultado__factor {{
        display: grid;
        grid-template-columns: 1fr 84px;
        gap: 0.75rem;
        align-items: center;
        font-size: 0.9rem;
        color: {c.text_primary};
    }}

    .tarjeta-resultado__barra {{
        height: 6px;
        background-color: {c.track_bg};
        border-radius: 3px;
        overflow: hidden;
    }}

    .tarjeta-resultado__barra i {{
        display: block;
        height: 100%;
        background-color: {c.accent};
        border-radius: 0 3px 3px 0;
    }}

    .tarjeta-resultado__nota {{
        font-family: {t.mono_font};
        font-size: 0.72rem !important;
        letter-spacing: 0.01em;
        color: {c.text_muted};
        margin: 0;
    }}

    /* ---- Graficos de barras del panel de Contexto (HTML propio, ver
    components/grafico_barras.py) ---- */

    .grafico-card {{
        border: 1px solid {c.card_border};
        border-radius: 6px;
        padding: 17px 19px 4px;
        display: flex;
        flex-direction: column;
        gap: 3px;
        margin-bottom: 1.1rem;
    }}

    .grafico-card h4 {{
        font-family: {t.heading_font};
        font-size: 15.5px;
        margin: 0;
    }}

    .grafico-card__descripcion {{
        font-size: 12.5px !important;
        color: {c.text_muted_strong};
        margin: 0 0 13px 0;
    }}

    .grafico-card__filas {{
        display: flex;
        flex-direction: column;
        gap: 2px;
    }}

    .grafico-card__fila {{
        display: grid;
        grid-template-columns: 116px 1fr 50px;
        gap: 12px;
        align-items: center;
        padding: 3px 0;
        position: relative;
    }}

    .grafico-card__categoria {{
        font-size: 12.5px;
        color: {c.text_muted_strong};
        text-align: right;
    }}

    .grafico-card__barra {{
        height: 17px;
        background-color: {c.track_bg};
        border-radius: 2px;
        position: relative;
    }}

    .grafico-card__barra i {{
        position: absolute;
        inset: 0 auto 0 0;
        display: block;
        background-color: {c.accent};
        border-radius: 2px 4px 4px 2px;
    }}

    .grafico-card__valor {{
        font-family: {t.mono_font};
        font-size: 12px;
        font-variant-numeric: tabular-nums;
        color: {c.text_primary};
    }}

    .grafico-card__fila:hover .grafico-card__barra i {{
        filter: brightness(1.12);
    }}

    .grafico-card__tooltip {{
        position: absolute;
        left: 128px;
        bottom: calc(100% - 2px);
        z-index: 5;
        background-color: {c.text_primary};
        color: {c.card_bg};
        border-radius: 4px;
        padding: 5px 9px;
        font-family: {t.mono_font};
        font-size: 11px;
        white-space: nowrap;
        opacity: 0;
        transform: translateY(3px);
        transition: opacity .12s ease, transform .12s ease;
        pointer-events: none;
    }}

    .grafico-card__fila:hover .grafico-card__tooltip,
    .grafico-card__fila:focus-within .grafico-card__tooltip {{
        opacity: 1;
        transform: translateY(0);
    }}

    .grafico-card__nota {{
        font-family: {t.mono_font};
        font-size: 10.5px !important;
        color: {c.text_muted};
        margin-top: 18px !important;
    }}

    """