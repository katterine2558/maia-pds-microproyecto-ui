# Tablero — Reingreso hospitalario a 30 días

Tablero del micro-proyecto de *Desarrollo de Soluciones*. Consume las predicciones
de la API por HTTP y visualiza los datos descriptivos relevantes para el equipo de
gestión del alta.

Maestría en Inteligencia Artificial (MAIA) — Universidad de los Andes.

## Repositorios

| Repositorio | Contiene |
|---|---|
| [`maia-pds-microproyecto-api`](https://github.com/katterine2558/maia-pds-microproyecto-api) | Datos (DVC), pipelines, experimentos MLflow, modelos empaquetados y la API |
| [`maia-pds-microproyecto-ui`](https://github.com/katterine2558/maia-pds-microproyecto-ui) (este) | Tablero: fuentes y artefactos de despliegue |

## La frontera

```
tablero  →  HTTP  →  API  →  modelo empaquetado
```

**Este repositorio no importa el modelo ni carga el `.pkl`.** Toda comunicación pasa
por `services/api.py`. Es el requisito que evalúa el enunciado, y la separación en
dos repos lo vuelve estructural: aquí no existe el artefacto que se podría cargar
por atajo.

## Las dos funciones del tablero

El enunciado exige ambas; una sola no cumple.

| Sección | Qué hace |
|---|---|
| Predicción | Emplea el modelo **a través de la API**: arma el encuentro y llama `POST /predict` |
| Datos | Visualiza datos descriptivos relevantes para el usuario |

## Levantar el tablero

### Local

```bash
uv sync                          # o: pip install -e .
cp .env.example .env             # ajusta API_URL si hace falta
streamlit run app.py             # http://localhost:8501
```

Necesita la API corriendo. Ver el README del repositorio `-api`.

### Contenedor

```bash
docker build -t reingreso-ui .
docker run -p 8501:8501 -e API_URL=http://host.docker.internal:8000 reingreso-ui
```

`API_URL` es la única configuración: apunta a donde esté la API. Dentro de un
`docker compose` con ambos servicios, va el nombre del servicio (`http://api:8000`).

## Estructura

```
maia-pds-microproyecto-ui/
├── app.py                     # entrada de Streamlit
├── services/
│   └── api.py                 # unico punto de contacto con la API
├── assets/                    # imagenes y estaticos del tablero
├── Dockerfile
├── pyproject.toml
└── .env.example               # API_URL
```

## Flujo de trabajo con Git

Git flow, igual que el repositorio de la API.

| Rama | Rol |
|---|---|
| `main` | Solo estados entregados. Cada entrega queda taggeada aquí. |
| `develop` | Integración. Rama por defecto de trabajo diario. |
| `feature/*` | Una por ítem de trabajo. Sale de `develop` y vuelve a `develop`. |
| `release/*` | Preparación de cada entrega: `develop` → `release/entrega-N` → `main`. |

Tags sin prefijo de versión: `release/entrega-2` produce el tag `entrega-2`.

```bash
git flow feature start formulario-prediccion
git flow feature finish formulario-prediccion

git flow release start entrega-2
git flow release finish entrega-2
```

### Autoría

- Cada integrante commitea **con su propia identidad**. Nadie sube el trabajo de otro.
- **No hacer squash ni rebase que colapse la autoría** al integrar ramas.
- Nombrar las ramas `feature/*` por ítem de trabajo, no por persona.

La nota es individual y se sustenta en los commits. Como el proyecto vive en dos
repositorios, **cada integrante debe tener commits en ambos**.
