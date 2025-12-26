# Protocolo Experimental para la Generación Automática de Algoritmos (GAA)

## Contexto

Este protocolo experimental se basa en el script `demo_experimentation_both.py`, en el cual se ha observado que, en múltiples ejecuciones previas, es posible alcanzar tiempos de resolución cercanos a **34 segundos**. Estas observaciones motivan un estudio sistemático y prolongado para comprender las causas subyacentes de dicho desempeño.

## Objetivo General

Identificar, aprender y caracterizar **patrones, estructuras y propiedades** de los algoritmos generados automáticamente que se asocian a menores tiempos de ejecución, manteniendo simultáneamente una calidad de solución aceptable.

Se plantea como **hipótesis inicial** que estas diferencias de tiempo están relacionadas con la forma en que se generan los algoritmos, pero se requiere evidencia empírica que permita descubrir qué características específicas influyen de manera determinante en el rendimiento temporal.

## Diseño Experimental

- Ejecutar pruebas de forma **continua** durante un período total de **3 días**, sin interrupciones.
- Cada corrida corresponde a:
  1. La generación automática de un algoritmo.
  2. Su ejecución y evaluación sobre la instancia del problema.
- Todas las pruebas se ejecutarán en **entorno local**.
- El proceso de registro y documentación debe ser **automático, riguroso y reproducible**.

## Restricciones de Tiempo

- Establecer un límite máximo de ejecución de **60 segundos** por corrida.
- Si una ejecución supera los 60 segundos:
  - Debe ser **detenida automáticamente**.
  - Debe ser **descartada** como solución válida.
  - Debe quedar igualmente **registrada** como corrida fallida por sobretiempo.

## Métricas y Criterios de Evaluación

Para cada algoritmo generado en cada corrida, se debe registrar de manera exhaustiva la siguiente información:

1. **Identificador único** de la corrida.
2. **Representación completa** del algoritmo generado, incluyendo:
   - Estructura del algoritmo.
   - Operadores utilizados.
   - Parámetros internos.
   - Cualquier metadato relevante para su análisis posterior.
3. **Tiempo total de ejecución** (en segundos).
4. **Valor de la función objetivo** obtenido.
5. **Medidas de error**, incluyendo:
   - Error absoluto.
   - Error relativo.
   - %GAP respecto al valor óptimo conocido.
6. **Indicador HIT**, definido como:
   - `HIT = TRUE` si la solución es igual o mejor que un 5% respecto del óptimo.
   - `HIT = FALSE` en caso contrario.
7. **Estado de la ejecución**, clasificado como:
   - Ejecución exitosa.
   - Detenida por sobretiempo (> 60 s).
   - Fallida por error de ejecución (si corresponde).

## Registro y Trazabilidad

Todos los resultados deben almacenarse en un formato estructurado y analizable, como por ejemplo:
- CSV
- JSON
- Base de datos experimental

El registro debe permitir análisis posteriores tales como:
- Correlación entre características del algoritmo y tiempo de ejecución.
- Comparación entre algoritmos HIT y no-HIT.
- Identificación de patrones recurrentes en las corridas de menor tiempo (≈ 34 s).

## Descomposición Temporal de la Experimentación

Para cada corrida experimental se debe medir y registrar explícitamente el tiempo consumido en cada una de las etapas del proceso:

1. **Tiempo de generación del algoritmo**: Tiempo requerido para construir el algoritmo (árbol sintáctico, reglas, operadores y parámetros).
2. **Tiempo de inicialización**: Preparación de estructuras de datos, soluciones iniciales o poblaciones.
3. **Tiempo de búsqueda / optimización**: Tiempo efectivo dedicado al proceso metaheurístico.
4. **Tiempo de evaluación de la función objetivo**: Todas las evaluaciones necesarias durante la búsqueda.
5. **Tiempo de post-procesamiento**: Cálculo de métricas finales, %GAP, HIT y validaciones.
6. **Tiempo total de ejecución**: Suma de todas las etapas anteriores.

Esta descomposición temporal es **obligatoria** para todas las corridas, incluidas aquellas detenidas por sobretiempo.

## Esquema de Logging y Dataset Ideal

Dataset experimental normalizado, donde cada fila corresponda a una corrida:

| Campo | Descripción |
|-------|-------------|
| `run_id` | Identificador único |
| `timestamp` | Fecha y hora de ejecución |
| `algorithm_id` | ID del algoritmo generado |
| `execution_status` | success / timeout / error |
| `time_generation` | Tiempo de generación del algoritmo |
| `time_initialization` | Tiempo de inicialización |
| `time_search` | Tiempo de búsqueda |
| `time_evaluation` | Tiempo de evaluación |
| `time_postprocessing` | Tiempo de post-procesamiento |
| `time_total` | Tiempo total |
| `objective_value` | Valor de función objetivo |
| `optimal_value` | Valor óptimo conocido |
| `absolute_error` | Error absoluto |
| `relative_error` | Error relativo |
| `gap_percent` | %GAP |
| `hit` | Boolean (TRUE si gap ≤ 5%) |

## Features del Algoritmo a Registrar

### 1. Características Estructurales
- Profundidad total del árbol sintáctico
- Número total de nodos
- Número de operadores distintos utilizados
- Tipo de operadores
- Presencia de ciclos, recursión o estructuras iterativas

### 2. Características de la Metaheurística
- Tipo de metaheurística base
- Estrategia de inicialización
- Mecanismo de aceptación (determinista, probabilístico, umbral)

### 3. Parámetros Dinámicos
- Número máximo de iteraciones
- Criterios de parada
- Uso de enfriamiento, reinicios o intensificación/diversificación
- Frecuencia de perturbaciones

### 4. Características de Desempeño Interno
- Número total de evaluaciones de la función objetivo
- Número de mejoras aceptadas
- Ratio mejoras / evaluaciones
- Tiempo promedio por evaluación

Estas features permitirán realizar análisis explicativos avanzados (correlación, clustering, modelos predictivos) para descubrir qué propiedades del algoritmo explican ejecuciones significativamente más rápidas manteniendo calidad de solución.
