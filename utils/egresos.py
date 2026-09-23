"""Lectura y validacion del archivo de egresos que sube el usuario.

La vista Priorizacion recibe un CSV con los egresos del turno y los manda a la
API. Este modulo se queda con la parte que no es interfaz: leer el archivo,
comprobar que trae las columnas que `POST /predict` exige y convertir cada fila
al cuerpo JSON de esa peticion.

La validacion vive aqui, antes de la primera llamada, porque un archivo con una
columna mal escrita produciria N respuestas 422 identicas: es mas util un solo
mensaje que diga que falta.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

# Identificador del egreso. No viaja a la API: sirve para que el usuario
# reconozca al paciente en la lista que devuelve el tablero.
COLUMNA_ENCUENTRO = "encuentro"

# Las diez variables del modelo, con el nombre que espera el cuerpo de
# `POST /predict`.
COLUMNAS_MODELO = [
    "rango_edad",
    "tipo_admision",
    "servicio_alta",
    "dias_estancia",
    "num_diagnosticos",
    "num_medicamentos",
    "ingresos_previos",
    "urgencias_previas",
    "resultado_a1c",
    "cambio_medicacion",
]
COLUMNAS_REQUERIDAS = [COLUMNA_ENCUENTRO, *COLUMNAS_MODELO]

_ENTEROS = {
    "dias_estancia",
    "num_diagnosticos",
    "num_medicamentos",
    "ingresos_previos",
    "urgencias_previas",
}

# Tope de filas por archivo. Cada fila es una llamada HTTP a la API; mas alla
# de esto la espera dentro del tablero deja de ser razonable y conviene partir
# el archivo por turno o por servicio.
MAXIMO_FILAS = 200


class ArchivoInvalido(ValueError):
    """El archivo no sirve como lista de egresos."""


@dataclass(frozen=True)
class Egresos:
    """Egresos leidos de un archivo, listos para mandar a la API."""

    tabla: pd.DataFrame

    @property
    def total(self) -> int:
        return len(self.tabla)

    def encuentros(self) -> list[dict]:
        """Cuerpos de `POST /predict`, uno por fila y en el orden del archivo."""
        return self.tabla[COLUMNAS_MODELO].to_dict(orient="records")


def leer(archivo) -> Egresos:
    """Lee el CSV subido y devuelve sus egresos, o explica por que no puede.

    `archivo` es lo que entrega `st.file_uploader`: un objeto con interfaz de
    fichero, no una ruta.
    """
    try:
        tabla = pd.read_csv(archivo)
    except Exception as exc:  # pandas levanta de todo ante un archivo corrupto
        raise ArchivoInvalido(f"No se pudo leer el archivo: {exc}") from exc

    tabla.columns = [str(c).strip() for c in tabla.columns]

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in tabla.columns]
    if faltantes:
        raise ArchivoInvalido(
            "Al archivo le faltan columnas: " + ", ".join(faltantes) + "."
        )

    tabla = tabla[COLUMNAS_REQUERIDAS].copy()

    if tabla.empty:
        raise ArchivoInvalido("El archivo no tiene filas.")
    if len(tabla) > MAXIMO_FILAS:
        raise ArchivoInvalido(
            f"El archivo trae {len(tabla)} filas y el tope es {MAXIMO_FILAS}. "
            "Divide la lista por turno o por servicio."
        )

    vacias = tabla[tabla.isna().any(axis=1)]
    if not vacias.empty:
        filas = ", ".join(str(i + 2) for i in vacias.index[:5])
        raise ArchivoInvalido(
            f"Hay filas con celdas vacias (linea {filas}). Completa o quita esas filas."
        )

    for columna in _ENTEROS:
        numeros = pd.to_numeric(tabla[columna], errors="coerce")
        if numeros.isna().any():
            raise ArchivoInvalido(f"La columna «{columna}» debe traer numeros enteros.")
        tabla[columna] = numeros.astype(int)

    for columna in set(COLUMNAS_REQUERIDAS) - _ENTEROS:
        tabla[columna] = tabla[columna].astype(str).str.strip()

    return Egresos(tabla=tabla)
