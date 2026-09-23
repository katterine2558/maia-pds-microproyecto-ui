# Manual de usuario

Tablero de apoyo a la priorización del seguimiento tras el alta, para pacientes
diabéticos.

El tablero **estima** qué pacientes tienen mayor probabilidad de reingresar en
los 30 días siguientes al alta, para ayudar a repartir los contactos de
seguimiento cuando hay más egresos que capacidad. **No es un diagnóstico ni una
indicación de tratamiento**: el resultado es orientativo y requiere criterio
clínico.

## Antes de empezar

- El tablero está publicado en
  <https://maia-pds-microproyecto-ui-production.up.railway.app>. Solo necesita
  un navegador; no hay que instalar nada ni iniciar sesión.
- El tablero no guarda nada de lo que usted escribe. Cada consulta se hace en el
  momento y se pierde al recargar la página.
- No cargue datos reales de pacientes en un despliegue de demostración sin la
  autorización de su institución.

## Las tres vistas

El menú de la izquierda tiene tres opciones:

| Vista | Para qué sirve |
|---|---|
| **Paciente** | Estimar el riesgo de **un** encuentro, llenando un formulario |
| **Priorización** | Ordenar **todos** los egresos del turno subiendo un archivo |
| **Contexto** | Ver dónde se concentra el reingreso en la población histórica |

## Paciente: consultar un encuentro

1. Abra **Paciente**.
2. Complete los diez campos del encuentro: rango de edad, tipo de admisión,
   servicio que da el alta, días de estancia, número de diagnósticos, número de
   medicamentos, ingresos previos en el último año, urgencias previas en el
   último año, resultado de A1C y si hubo cambio de medicación.
3. Pulse **Calcular riesgo**.

El resultado aparece a la derecha:

- **La probabilidad**, entre 0 y 1. Un 0,64 significa que el modelo estima un
  64 % de probabilidad de reingreso antes de 30 días.
- **El nivel de riesgo**: Alto, Medio o Bajo (ver más abajo).
- **El umbral de decisión** del modelo y el nombre de la versión que respondió.

Si algo falla, el tablero muestra el mensaje de error y **no deja el resultado
anterior en pantalla**: nunca verá la estimación de otro paciente confundida con
la del que acaba de consultar. Si aparece un error de conexión, anote el mensaje
y avise al equipo técnico.

### Cómo se leen los tres niveles

El modelo tiene un **umbral de decisión** —hoy 0,30— que es el punto a partir
del cual marca a un paciente para seguimiento.

| Nivel | Cuándo aparece | Cómo leerlo |
|---|---|---|
| **Alto** | Probabilidad igual o mayor al umbral | El modelo lo marca para seguimiento |
| **Medio** | Entre 11,4 % y el umbral | Por encima del promedio de la población, sin llegar a la marca |
| **Bajo** | Por debajo de 11,4 % | Por debajo del promedio de la población |

El 11,4 % es la tasa de reingreso de todo el conjunto histórico: de cada 100
egresos, unos 11 volvieron antes de 30 días. Sirve como punto de comparación.

## Priorización: ordenar los egresos del turno

Esta vista recibe la lista de egresos, consulta el modelo para cada uno y los
ordena de mayor a menor riesgo.

### 1. Prepare el archivo

Un archivo **CSV** con una fila por egreso y estas once columnas:

| Columna | Qué lleva |
|---|---|
| `encuentro` | Identificador del egreso. Solo se usa para que usted reconozca al paciente en la lista; no se envía al modelo |
| `rango_edad` | `[0-10)`, `[10-20)`, … `[90-100)` |
| `tipo_admision` | `Emergency`, `Urgent`, `Elective`, `Newborn`, `Not Available` |
| `servicio_alta` | Servicio que da el alta, por ejemplo `Nephrology` |
| `dias_estancia` | Número entero |
| `num_diagnosticos` | Número entero |
| `num_medicamentos` | Número entero |
| `ingresos_previos` | Hospitalizaciones en el último año |
| `urgencias_previas` | Visitas a urgencias en el último año |
| `resultado_a1c` | `No medido`, `Norm`, `>7`, `>8` |
| `cambio_medicacion` | `Sí` o `No` |

Los valores son los mismos que ofrecen las listas desplegables de la vista
Paciente. Si no sabe por dónde empezar, el botón **Descargar plantilla de
ejemplo** le da un archivo con tres filas de muestra que puede abrir en Excel y
reemplazar.

El máximo es **200 egresos por archivo**. Si tiene más, divida la lista por
turno o por servicio.

### 2. Súbalo

Arrastre el archivo al recuadro **Archivo de egresos (CSV)** o pulse para
buscarlo. El tablero valida el archivo antes de consultar el modelo y, si algo
está mal, le dice exactamente qué: una columna que falta, filas con celdas
vacías, o texto donde se esperaba un número.

Si algún egreso no puede evaluarse, el tablero sigue con el resto y le avisa
cuántos quedaron fuera.

### 3. Lea la lista

Arriba aparecen cuatro indicadores:

- **Egresos cargados**: cuántos se evaluaron.
- **Capacidad**: cuántos seguimientos puede hacer hoy. Se elige en el selector.
- **Cubre**: qué porción del riesgo total del turno alcanzan a cubrir los
  pacientes que están dentro de la capacidad.
- **Riesgo alto sin cubrir**: cuántos pacientes marcados como riesgo alto quedan
  por debajo de la línea. Si hay alguno, el indicador se resalta.

La tabla va del más riesgoso al menos riesgoso, con una **línea de capacidad**
que separa a quienes alcanzan los recursos del turno de quienes no.

Puede filtrar por servicio y descargar la lista ordenada con **Descargar
lista**, para repartir los contactos.

### Una advertencia importante

Con el umbral actual, el modelo marca como riesgo alto a una proporción muy
grande de los egresos. Eso es esperable: está ajustado para **no dejar pasar**
reingresos, y el precio es señalar de más. En la práctica, la lista ordenada
importa más que la etiqueta: atienda de arriba hacia abajo hasta donde alcance
la capacidad.

## Contexto: dónde se concentra el riesgo

Tres gráficas descriptivas sobre la población histórica:

- **Por ingresos previos.** El gradiente más fuerte: de 8,6 % sin ingresos
  previos a 37,1 % con cinco o más.
- **Por especialidad que da el alta.** Nefrología (16,1 %) duplica a cardiología
  (8,0 %).
- **Por rango de edad.** Sube de forma sostenida a partir de los 50 años.

Estas cifras describen **la población histórica**, no a un paciente concreto.
Son contexto para interpretar los resultados, no una predicción.

## Preguntas frecuentes

**El botón Calcular riesgo devuelve un error de conexión.**
El tablero no está alcanzando la API. Avise al equipo técnico; no es algo que se
resuelva desde la pantalla.

**Subí el archivo y dice que falta una columna.**
Revise que los nombres de las columnas estén escritos igual que en la tabla de
arriba, en minúsculas y sin tildes. Descargue la plantilla de ejemplo y compare.

**¿Por qué la probabilidad no cambia cuando modifico un campo?**
Hay que pulsar **Calcular riesgo** de nuevo. La tarjeta muestra el resultado de
la última consulta.

**¿El tablero guarda los pacientes que consulto?**
No. Nada se almacena: al recargar la página, la pantalla vuelve a empezar.
