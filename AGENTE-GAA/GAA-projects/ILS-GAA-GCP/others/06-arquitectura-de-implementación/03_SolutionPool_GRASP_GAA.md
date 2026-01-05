SolutionPool – GRASP + GAA
Diseño del Contenedor de Élite y Evaluación
1. Propósito del SolutionPool

El SolutionPool es el componente responsable de:

almacenar las mejores soluciones encontradas

comparar soluciones según el criterio canónico del VRPTW

mantener la mejor solución global

mantener la mejor solución por algoritmo (AST)

proporcionar ranking de algoritmos en GAA

servir como memoria elitista durante GRASP

El SolutionPool no es una población genética ni mantiene diversidad explícita.

2. Principios de Diseño

Comparación lexicográfica Solomon

Almacenamiento mínimo (sin rutas completas)

Separación entre solución y algoritmo

Independiente de la metaheurística

Compatible con ejecución paralela

Soporte directo a GAA

3. Regla Única de Comparación

Toda comparación de soluciones se basa en el siguiente criterio:

Menor número de vehículos

Menor distancia total

Formalmente:

(V1, D1) ≺ (V2, D2) si:
V1 < V2, o
V1 = V2 y D1 < D2


Esta regla se utiliza en:

actualización del mejor global

actualización del mejor por algoritmo

ranking de algoritmos

4. Estructura del SolutionPool

El SolutionPool mantiene tres componentes:

mejor solución global

mejor solución por algoritmo

registro tabular de resultados

Estructura conceptual:

SolutionPool
│
├── global_best
├── best_by_algorithm {algorithm_id → Solution}
└── logs [log_entry]

5. Responsabilidades del SolutionPool

El SolutionPool debe:

registrar soluciones evaluadas

actualizar el mejor global

actualizar el mejor por algoritmo

almacenar información mínima para logging

permitir ranking de algoritmos

no interferir con la lógica de búsqueda

6. Registro de una Solución

Cada solución generada debe ser registrada mediante una operación atómica que:

evalúa la solución

actualiza mejores soluciones

almacena el log correspondiente

Conceptualmente:

register_solution(solution, log_entry)


Donde:

solution es un objeto Solution evaluado

log_entry es un diccionario con campos tabulares

7. Mejor Solución Global

El SolutionPool mantiene una referencia a la mejor solución global encontrada hasta el momento.

Propiedades:

única

actualizada incrementalmente

basada en criterio lexicográfico

independiente del algoritmo que la generó

8. Mejor Solución por Algoritmo (AST)

Para cada algoritmo (AST) evaluado, el SolutionPool mantiene:

la mejor solución producida por dicho algoritmo

utilizada para ranking GAA

utilizada para selección del ganador

Esto permite comparar algoritmos sin mezclar ejecuciones.

9. Ranking de Algoritmos (GAA)

El ranking de algoritmos se construye a partir de:

la mejor solución obtenida por cada algoritmo

el criterio lexicográfico canónico

Resultado:

lista ordenada de algoritmos

selección directa del mejor algoritmo generado automáticamente

10. Selección del Algoritmo Ganador

El algoritmo ganador es aquel cuya mejor solución:

usa menos vehículos que los demás, o

usa igual número de vehículos y menor distancia

Este algoritmo:

se selecciona para análisis cualitativo

se utiliza en experimentos finales

puede ser comparado contra BKS

11. Qué NO hace el SolutionPool

El SolutionPool NO:

almacena rutas completas

almacena estados intermedios

aplica operadores de búsqueda

evalúa factibilidad

gestiona parámetros

conoce la estructura interna del AST

12. Interacción con Otros Componentes

El SolutionPool interactúa con:

Contenedor de Solución (Solution)

Sistema de Logging

Método Maestro (GRASP)

Evaluación GAA

No interactúa directamente con:

operadores de vecindario

construcción de soluciones

lógica del AST

13. Uso Típico en GRASP + GAA

Flujo conceptual:

generar algoritmo (AST)

ejecutar GRASP con ese algoritmo

obtener solución final

registrar solución en SolutionPool

repetir para otros algoritmos

rankear algoritmos

seleccionar ganador

14. Resumen

El SolutionPool actúa como:

memoria elitista

mecanismo de comparación

puente entre GRASP y GAA

base para ranking y selección de algoritmos

Su diseño es:

minimalista

correcto

reproducible

escalable

alineado con VRPTW Solomon