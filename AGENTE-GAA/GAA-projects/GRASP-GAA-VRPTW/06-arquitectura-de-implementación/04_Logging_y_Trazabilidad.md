Logging y Trazabilidad
VRPTW – GRASP + GAA
1. Propósito del Sistema de Logging

El sistema de logging tiene como objetivo:

garantizar reproducibilidad experimental

permitir análisis estadístico posterior

registrar resultados de forma compacta y estructurada

evitar almacenamiento innecesario de información

servir como base para ranking y comparación de algoritmos

El logging NO es un sistema de depuración.

2. Principios de Diseño

Una fila = una ejecución

Datos no reconstruibles únicamente

Formato tabular (CSV)

Independiente de la metaheurística

Compatible con ejecución masiva

Fácilmente analizable (Python / R / Excel)

3. Unidad de Logging

La unidad básica de logging es una ejecución completa:

Un algoritmo (AST) ejecutado sobre una instancia VRPTW, con una semilla específica, produciendo una solución final.

4. Campos Obligatorios por Ejecución
4.1 Identificación
run_id
instance_id
family
seed
algorithm_id

4.2 Métricas Canónicas (Solomon)
num_vehicles
total_distance

4.3 Relación con BKS
bks_vehicles
bks_distance
gap_distance


Reglas:

gap_distance solo se calcula si num_vehicles == bks_vehicles

si num_vehicles > bks_vehicles, gap_distance = NaN

si num_vehicles < bks_vehicles, se considera mejora del BKS

4.4 Factibilidad y Penalización
is_feasible
penalty_value

4.5 Tiempo Computacional
cpu_time_sec


Tiempo total de ejecución sobre la instancia.

4.6 Identidad del Algoritmo (GAA)
ast_depth
num_function_nodes
ast_signature

5. Campos Prohibidos

NO deben almacenarse:

secuencia de rutas

secuencia de clientes

estados intermedios

movimientos de búsqueda

listas de vecinos

información por iteración

Estos datos:

no se analizan

no se publican

inflan el tamaño de logs

6. Formato del Log
6.1 Formato Recomendado

CSV (una fila por ejecución).

6.2 Orden de Columnas
run_id,
instance_id,
family,
seed,
algorithm_id,
num_vehicles,
total_distance,
bks_vehicles,
bks_distance,
gap_distance,
is_feasible,
penalty_value,
cpu_time_sec,
ast_depth,
num_function_nodes,
ast_signature

7. Archivo de Salida

Un único archivo de log por experimento:

results_log.csv


O, alternativamente:

logs/
 ├── experiment_01.csv
 ├── experiment_02.csv

8. Uso del Log en el Experimento

El log se utiliza para:

cálculo de promedios y desviaciones

ranking de algoritmos

comparación con BKS

detección de soluciones infactibles

análisis de robustez

selección del algoritmo ganador

9. Reproducibilidad

Para cada fila del log, la ejecución es reproducible usando:

instance_id

seed

algorithm_id

versión fija del código

10. Relación con SolutionPool

El SolutionPool:

no guarda soluciones completas

utiliza el log como registro histórico

puede reconstruir rankings a partir del log

mantiene solo referencias a mejores soluciones

11. Resumen

El sistema de logging proporciona:

trazabilidad completa

mínimo almacenamiento

rigor experimental

alineación con literatura VRPTW

soporte directo a GAA

Es un componente esencial, pero no intrusivo, del sistema.