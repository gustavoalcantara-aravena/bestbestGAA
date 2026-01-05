Flujo de Experimento Completo
GRASP + GAA para VRPTW (Solomon)
1. Objetivo del Flujo Experimental

Definir paso a paso cómo se ejecuta un experimento completo de Generación Automática de Algoritmos (GAA) usando GRASP como metaheurística de exploración, garantizando:

Reproducibilidad

Comparabilidad entre algoritmos generados

Separación clara entre:

generación de algoritmos

ejecución

evaluación

análisis

El flujo optimiza algoritmos, no soluciones individuales.

2. Unidades Fundamentales del Experimento
2.1 Algoritmo (Unidad de Diseño)

Representado por un AST

Fijo durante una ejecución

Identificado por algorithm_id

2.2 Run (Unidad Estocástica)

Ejecución independiente de un algoritmo

Usa una semilla controlada

Produce una solución

2.3 Instancia (Unidad del Problema)

Una instancia Solomon VRPTW

Identificada por instance_id

3. Jerarquía Experimental
Experimento
└── Algoritmos (AST)
    └── Runs
        └── Instancias
            └── Solución


Formalmente:

FOR each algorithm a:
    FOR each run r:
        FOR each instance i:
            execute(a, r, i)

4. Fase 0 — Inicialización Global
Pasos

Definir parámetros experimentales:

número de algoritmos

número de runs

semillas

límites de AST

Inicializar:

Logger

SolutionPool

Random Generator

Cargar:

instancias Solomon

BKS por instancia

5. Fase 1 — Generación de Algoritmos (GAA)
Objetivo

Crear un conjunto inicial de algoritmos candidatos.

Procedimiento
algorithms = []

FOR k in range(num_algorithms):
    AST = generate_random_AST()
    algorithms.append(AST)

Resultado

Conjunto fijo de ASTs

Cada AST define un algoritmo completo

NO se modifican durante la evaluación

6. Fase 2 — Ejecución Experimental
Objetivo

Evaluar cada algoritmo de forma justa y comparable.

6.1 Loop Principal
FOR each algorithm in algorithms:
    FOR run_id in runs:
        set_random_seed(seed_base + run_id)
        FOR instance in instances:
            solution = run_GRASP(instance, algorithm)
            evaluate(solution)
            log(solution)
            solution_pool.register(solution)

6.2 Ejecución de GRASP (por instancia)
run_GRASP(instance, algorithm):
    s0 = greedy_construction(instance, algorithm)
    s1 = local_search(instance, algorithm, s0)
    return s1


Características clave:

GRASP opera a nivel solución

El AST controla:

criterios greedy

selección aleatoria

operadores locales

El algoritmo no aprende online

7. Fase 3 — Evaluación de Soluciones
Métrica Canónica (Solomon)

Orden lexicográfico:

Número de vehículos

Distancia total

Evaluación por solución
evaluate(solution):
    compute_vehicles()
    compute_distance()
    check_feasibility()
    compute_penalty_if_needed()

Gap respecto a BKS
IF vehicles == BKS_vehicles:
    gap = (distance - BKS_distance) / BKS_distance
ELSE:
    gap = +∞

8. Fase 4 — Registro y Trazabilidad

Cada solución genera una entrada de log.

Campos mínimos:

algorithm_id

run_id

instance_id

vehicles

distance

gap

feasibility

cpu_time

seed

NO se loguean movimientos internos.

9. Fase 5 — Agregación de Resultados
Por algoritmo

Para cada algorithm_id:

mean_gap
std_gap
mean_vehicles
feasible_rate
mean_time

10. Fase 6 — Ranking de Algoritmos
Criterio principal
rank by:
1) mean number of vehicles
2) mean gap to BKS
3) standard deviation

Selección final
best_algorithm = argmin(rank_score)

11. Fase 7 — Análisis Cualitativo del Algoritmo Ganador

Solo para el algoritmo ganador:

estructura del AST

nodos dominantes

profundidad real

lógica inducida

Objetivo: interpretabilidad, no optimización adicional.

12. Control de Reproducibilidad

Semilla fija por run

Orden fijo de instancias

ASTs inmutables durante evaluación

Sin estado global compartido

13. Qué NO hace este Flujo (Importante)

❌ No entrena modelos

❌ No hace aprendizaje online

❌ No ajusta parámetros durante runs

❌ No usa train/test ML clásico

Esto NO es machine learning, es Algorithm Design.

14. Resumen Ejecutivo

Este flujo:

evalúa algoritmos, no soluciones

separa claramente diseño y ejecución

es compatible con Solomon VRPTW

es reproducible

es defendible académicamente

es implementable directamente en código