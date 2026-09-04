# CLAUDE.md

Guía para Claude Code en el repositorio del tablero.

Este repositorio es **una de dos partes** del micro-proyecto. El enunciado
(`maia_pds_proy.pdf`) y el contexto completo del curso viven en
[`maia-pds-microproyecto-api`](https://github.com/katterine2558/maia-pds-microproyecto-api);
cuando este archivo y el enunciado discrepen, manda el enunciado.

## Qué es este repo

El tablero. Dos funciones, ambas exigidas: emplear el modelo **a través de la API**
y visualizar otros datos relevantes para el usuario. Un tablero que solo grafica no
cumple; uno que solo predice, tampoco.

## La regla que no se rompe

```
tablero  →  HTTP  →  API  →  modelo empaquetado
```

Nada en este repositorio importa el modelo, carga un `.pkl` ni lee `data/`. Toda
llamada pasa por `services/api.py`. Si aparece `joblib`, `scikit-learn` o una ruta a
un artefacto de modelo en este repo, la arquitectura entregada no es la pedida.

## Git

Git flow: `main` (entregas, taggeadas) · `develop` (integración) · `feature/*`.
Tags sin prefijo: `entrega-2`, `entrega-3`.

**Los commits, merges y PRs no llevan trailers ni menciones de Claude** — nada de
`Co-Authored-By: Claude`, `Claude-Session:` ni `🤖 Generated with Claude Code`. La
contribución individual se califica a través de los commits, así que la autoría del
historial es evidencia evaluada y debe ser 100% del integrante. Antes de cerrar
cualquier commit o PR, revisar el mensaje contra `Claude|Co-Authored-By|Generated with|claude.ai`.

Cada integrante commitea con su propia identidad. Nada de squash o rebase que
colapse autoría.

## Comandos

```bash
uv sync                  # dependencias
streamlit run app.py     # tablero en http://localhost:8501
docker build -t reingreso-ui .
```

`API_URL` es la única configuración (ver `.env.example`).
