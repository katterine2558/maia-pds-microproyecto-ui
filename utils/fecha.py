"""Utilidad de fecha/hora para las vistas.

El calculo y formato del momento actual vive aqui, no en
`components/topbar.py`: ese componente solo pinta el texto que la vista
(capa `views/`) le pasa, no calcula nada por su cuenta.
"""

from __future__ import annotations

from datetime import datetime

_DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
_MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def formatear_fecha_hora(momento: datetime | None = None) -> str:
    """Fecha y hora en espanol, ej: 'lunes 5 sep 2026 · 15:13'.

    Si no se pasa `momento`, usa la hora actual del servidor.
    """
    momento = momento or datetime.now()
    dia = _DIAS[momento.weekday()]
    mes = _MESES[momento.month - 1]
    return f"{dia} {momento.day} {mes} {momento.year} · {momento.strftime('%H:%M')}"
