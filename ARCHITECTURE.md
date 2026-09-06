# Arquitectura del tablero

Este documento le explica cómo está armado el código de este repositorio y,
sobre todo, cómo debe pensar antes de tocarlo. No es un manual de Streamlit:
es la lógica interna que usted debe respetar para que la siguiente persona
(o usted mismo en dos semanas) entienda una pantalla nueva en cinco minutos,
sin tener que leerse todo el proyecto.

Si el enunciado del curso y este documento discrepan en algo, manda el
enunciado. Esto es solo la forma en que organizamos el código para
cumplirlo.

## La idea de fondo: tres capas que no se mezclan

Cuando usted abra cualquier archivo de `views/`, va a encontrar muy poco
código. Eso es intencional. La lógica está repartida en tres lugares, cada
uno con una sola responsabilidad:

| Capa | Carpeta | Pregunta que responde |
|---|---|---|
| Vista | `views/` | ¿Qué va en esta pantalla y en qué orden? |
| Componente | `components/` | ¿Cómo se pinta ese pedazo de interfaz? |
| Configuración | `config/` | ¿Qué colores, fuentes, menú y textos usa la app? |

Piense en `views/` como el libreto de una obra: dice "aquí entra la tarjeta
de riesgo, luego el formulario, luego el botón", pero no describe de qué
color es cada cosa ni cómo está hecha por dentro. Esa descripción vive en
`components/`. Y los números y nombres que se repiten en varias pantallas
(colores, fuentes, el menú del sidebar) viven en `config/`, para que usted
nunca tenga que buscar un color hexadecimal dentro de un componente.

Hay dos capas más, más chicas pero igual de importantes:

- **`utils/`**: funciones puras sin Streamlit y sin reglas de negocio de una
  pantalla en particular. Ejemplo: `utils/fecha.py` calcula el texto de
  fecha/hora que aparece en la esquina superior derecha; no sabe qué vista
  lo usa ni cómo se ve.
- **`services/`**: la única puerta hacia la API de inferencia
  (`services/api.py`). Ningún otro archivo del repositorio debe hacer una
  llamada HTTP a mano ni cargar un modelo — esa es la regla que no se rompe,
  y está descrita en `CLAUDE.md` y `README.md`.

## Cómo se lee una pantalla real, de punta a punta

Tome `views/priorizacion.py` y sígalo así:

1. **`app.py`** arranca la app, carga el CSS global una sola vez
   (`components.styles.load_css()`) y registra las tres páginas usando
   `config/nav.py` como fuente de verdad del menú.
2. **`views/priorizacion.py`** define `render()`. Esa función no calcula
   nada complicado: en su mayoría son llamadas a componentes, en el orden en
   que deben aparecer en la pantalla.
3. Cada llamada — `render_metric_card(...)`, `render_tabla_priorizacion(...)`
   — vive en `components/` y es la que decide cómo se ve esa pieza.
4. Los colores y fuentes que esos componentes usan no están escritos ahí:
   vienen de `config/theme.py` (`COLORS`, `TYPOGRAPHY`).

Si usted quiere entender **qué** aparece en una pantalla, lea la vista. Si
quiere entender **cómo** se ve una pieza, lea su componente. Si quiere
cambiar **un color en toda la app**, edite `config/theme.py` una sola vez.

## Streamlit nativo primero — HTML propio solo como excepción documentada

Esta es la regla más importante del proyecto y la que más cuesta respetar
bajo presión: **usted debe intentar siempre con los widgets nativos de
Streamlit** (`st.selectbox`, `st.number_input`, `st.metric`, `st.container`,
`st.columns`, etc.) antes de escribir HTML a mano. Los widgets nativos le dan
accesibilidad, comportamiento responsivo y menos código gratis.

Pero hay pantallas de la maqueta (`ux-ui/pantallas.html`) que **ningún**
widget nativo puede reproducir con la fidelidad que exige el diseño. En este
proyecto ya nos topamos con tres casos reales, y aprendimos por qué:

- **`components/topbar.py`** — necesita vivir en la franja del header nativo
  de Streamlit, algo que `st.title`/`st.caption` no permiten posicionar ahí.
- **`components/tabla_priorizacion.py`** — `st.dataframe` se dibuja dentro de
  un `<canvas>` (no se puede tipografiar con CSS) y `st.table` interpreta
  cada celda como Markdown (por eso `>7` se veía como una cita, no como
  texto). Ninguno de los dos deja quitar las líneas verticales ni insertar
  una fila con `colspan`.
- **`components/tarjeta_resultado.py`** y **`components/grafico_barras.py`**
  — necesitan un header con fondo distinto al cuerpo dentro de la misma
  caja, texto con tamaños/pesos/colores mixtos, y barras con posición y
  grosor exactos. `st.metric` y `st.progress` traen su propio "chip" y su
  propio color que no se puede apagar del todo sin artefactos visuales.

Cuando usted se encuentre en una situación parecida, el patrón a seguir es
el mismo en los cuatro archivos de arriba:

1. Construya el HTML en Python, con los valores pasados por `html.escape()`
   (nunca confíe en que un texto no va a tener `<`, `>` o `&`).
2. No le pase estilos por `style=""` sueltos salvo para colores que cambian
   dinámicamente (por ejemplo, el color de un badge de riesgo). Todo lo demás
   — tamaños, espaciados, tipografías — va en `components/styles.py`, bajo
   una clase CSS propia del componente (`.tabla-priorizacion`,
   `.tarjeta-resultado`, `.grafico-card`).
3. Deje un docstring al inicio del archivo explicando **por qué** este
   componente es una excepción. Si alguien lee el archivo sin ese contexto,
   va a pensar que rompimos la regla por pereza.

Si en algún momento un widget nativo nuevo de Streamlit resuelve lo mismo
sin esos problemas, prefiéralo y borre el HTML propio. La excepción es un
último recurso, no un estilo de la casa.

## Los estilos viven en un solo lugar

Todo el CSS de la aplicación se genera en una sola función:
`components/styles.py::_build_css()`, que usa los tokens de
`config/theme.py` y se inyecta una sola vez desde `app.py`. Usted nunca debe
escribir un color o un tamaño de fuente directamente dentro de un
componente — siempre a través de `COLORS`/`TYPOGRAPHY`.

Para escapar el CSS a una sola pantalla o a un solo componente, use la clave
de contenedor de Streamlit: `st.container(key="mi-seccion")` genera
automáticamente la clase `.st-key-mi-seccion`, y usted apunta el CSS a esa
clase. Así lo hacen `.st-key-priorizacion-filtros` y
`.st-key-paciente-formulario` — de hecho comparten una sola regla de CSS
porque tienen el mismo look, en vez de duplicar el bloque.

Una trampa que ya nos mordió y que usted debe recordar: cuando el texto que
quiere estilizar sale de `st.caption()` o `st.markdown()`, Streamlit lo
envuelve en un `<p>` dentro de `[data-testid="stMarkdownContainer"]`, y esa
regla interna de Streamlit tiene **más especificidad CSS** que una sola
clase suya. Si usted cambia un `font-size` o un `margin` y no se nota nada,
casi seguro el elemento es un `<p>` — la solución es agregar `!important` a
esa propiedad, como ya hicimos en `.tarjeta-resultado__nota` y
`.grafico-card__nota`.

## Cómo agregar una pantalla nueva, paso a paso

Cuando el enunciado le pida una pantalla que hoy no existe, siga esta receta
en orden:

1. **Cree el archivo de vista** en `views/`, con una única función pública
   `render() -> None`. No le ponga lógica de negocio pesada: si algo se
   repite en más de una vista, ese es la señal de que debe salir de ahí.
2. **Registre la pantalla** agregando un `NavItem` en `config/nav.py` y una
   entrada en el diccionario `_VIEW_RENDERERS` de `app.py`. No haga esto a
   mano en ningún otro lugar: es la única fuente de verdad del menú.
3. **Levante primero con widgets nativos.** Dibuje la pantalla completa con
   `st.columns`, `st.selectbox`, `st.container`, etc., aunque no se vea
   igual a la maqueta todavía. Es más rápido de escribir y más fácil de
   corregir.
4. **Compare contra la maqueta** (`ux-ui/pantallas.html` y las imágenes de
   `ux-ui/`) pieza por pieza. Si un widget nativo no llega al resultado
   exacto — como nos pasó con las tablas y las tarjetas —, ahí es cuando
   usted decide construir el componente en HTML propio, siguiendo la receta
   de la sección anterior.
5. **Extraiga a `components/`** cualquier pieza visual que se repita dentro
   de la misma vista (como `metric_card.py`, usado cuatro veces en la fila
   de KPIs de Priorización) o que probablemente se repita en otra pantalla
   más adelante.
6. **Lleve los datos fijos** (colores, listas de opciones, textos de la
   maqueta) a constantes al inicio del archivo de vista, no a valores
   sueltos dentro de la función `render()`. Facilita ver de un vistazo qué
   es "dato de ejemplo" y qué es estructura.
7. **No conecte la API todavía si no le corresponde a esta iteración.** Deje
   los datos de ejemplo bien señalados con un comentario (`# Datos de
   ejemplo...`), igual que en `views/priorizacion.py` y `views/paciente.py`,
   para que quede claro qué falta cablear contra `services/api.py`.

## La frontera con la API, otra vez

Este repositorio es la mitad de un proyecto de dos repos. La otra mitad
tiene el modelo. Usted nunca debe importar `joblib`, `scikit-learn`, ni leer
un archivo de datos crudo desde este repositorio — toda predicción pasa por
`services/api.py::predecir()`, que llama a la API por HTTP. Si alguna vez
necesita un dato que hoy no expone la API, la solución es pedir que se
agregue un endpoint allá, nunca calcularlo localmente con el modelo.

## Lecciones que ya pagamos, para que usted no las repita

- `st.metric(delta=...)` trae flecha y "chip" de color por defecto; incluso
  con `delta_color="off"` sigue dibujando la flecha si no le pasa también
  `delta_arrow="off"`. Y aun así, el fondo del chip vive en un `div` interno
  que hay que apagar explícitamente con `background: transparent
  !important` sobre el contenedor y sus descendientes.
- `st.table` interpreta el contenido de cada celda como Markdown. Un valor
  como `>8` se renderiza como una cita, no como texto. Si necesita texto
  literal en una tabla con formato exacto, no use `st.table`.
- `st.dataframe` se pinta en un `<canvas>` (glide-data-grid). El CSS de este
  proyecto no puede tocar su tipografía ni sus colores más allá de lo que
  permite pasar un `pandas.Styler`.
- `st.columns(n, vertical_alignment="bottom")` es la forma nativa de alinear
  un botón sin label contra otros widgets que sí tienen label en la misma
  fila — no intente arreglarlo a mano con márgenes CSS antes de revisar si
  el parámetro nativo ya lo resuelve.
- Los `selectbox` deben llevar `filter_mode=None` cuando quiere que se
  comporten como una lista desplegable pura, sin permitir que el usuario
  escriba texto libre — así están todos los de este proyecto.

Si usted descubre una trampa nueva de este tipo, agréguela a esta lista.
El objetivo de este documento es que la próxima persona la evite en minutos,
no que la vuelva a descubrir a la fuerza.
