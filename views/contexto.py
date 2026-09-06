"""Vista: Contexto.

Datos descriptivos generales sobre la poblacion de pacientes diabeticos y
el fenomeno de reingreso hospitalario a 30 dias.
"""

from components.grafico_barras import render_grafico_barras
from components.topbar import render_page_header

_INGRESOS_PREVIOS = (
    "Tasa de reingreso < 30 días según ingresos previos",
    "El gradiente más fuerte del dataset: 4,3× entre los extremos. Es el predictor que más manda.",
    [
        ("Ninguno", 23.2, "8,6 %", "66 245 encuentros · 8,59 %"),
        ("1 ingreso", 35.7, "13,3 %", "18 984 encuentros · 13,25 %"),
        ("2 ingresos", 48.3, "17,9 %", "7 300 encuentros · 17,93 %"),
        ("3 ingresos", 56.6, "21,0 %", "3 271 encuentros · 21,03 %"),
        ("4 ingresos", 65.0, "24,1 %", "1 574 encuentros · 24,14 %"),
        ("5 o más", 100.0, "37,1 %", "1 969 encuentros · 37,13 %"),
    ],
    "Eje: 0 – 37,1 %. Línea base del conjunto: 11,4 %.",
)

_ESPECIALIDAD = (
    "Tasa por especialidad que da el alta",
    "Nefrología duplica a cardiología. Señala en qué servicio reforzar la continuidad del cuidado.",
    [
        ("Nephrology", 100.0, "16,1 %", "1 539 encuentros · 16,11 %"),
        ("Family/General", 75.2, "12,1 %", "7 252 encuentros · 12,12 %"),
        ("InternalMedicine", 71.6, "11,5 %", "14 237 encuentros · 11,53 %"),
        ("Emergency/Trauma", 70.7, "11,4 %", "7 419 encuentros · 11,39 %"),
        ("Surgery-General", 69.4, "11,2 %", "3 059 encuentros · 11,18 %"),
        ("Orthopedics", 67.3, "10,9 %", "1 392 encuentros · 10,85 %"),
        ("Cardiology", 49.8, "8,0 %", "5 279 encuentros · 8,03 %"),
    ],
    "Eje: 0 – 16,1 %. Siete especialidades de mayor volumen.",
)

_RANGO_EDAD = (
    "Tasa por rango de edad",
    "Sube de forma sostenida a partir de los 50. El pico de [20-30) descansa sobre pocos casos.",
    [
        ("[20-30)", 100.0, "14,3 %", "1 649 encuentros · 14,31 %"),
        ("[40-50)", 74.5, "10,7 %", "9 607 encuentros · 10,66 %"),
        ("[50-60)", 68.3, "9,8 %", "17 060 encuentros · 9,77 %"),
        ("[60-70)", 79.0, "11,3 %", "22 059 encuentros · 11,30 %"),
        ("[70-80)", 84.3, "12,1 %", "25 331 encuentros · 12,06 %"),
        ("[80-90)", 87.8, "12,6 %", "16 434 encuentros · 12,57 %"),
    ],
    "Eje: 0 – 14,3 %. Pase el cursor sobre una barra para ver el volumen.",
)

_GRAFICOS = (_INGRESOS_PREVIOS, _ESPECIALIDAD, _RANGO_EDAD)


def render() -> None:
    render_page_header("Dónde se concentra el riesgo", "99 343 encuentros · tasa base 11,4%")

    for titulo, descripcion, filas, nota in _GRAFICOS:
        render_grafico_barras(titulo, descripcion, filas, nota)
