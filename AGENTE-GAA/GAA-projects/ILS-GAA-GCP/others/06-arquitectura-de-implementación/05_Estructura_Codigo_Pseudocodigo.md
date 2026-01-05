Estructura de Código y Pseudocódigo
VRPTW – GRASP + GAA
1. Arquitectura General del Sistema

El sistema se organiza en capas bien definidas, con dependencias unidireccionales.

┌───────────────────────────────┐
│        Experiment Runner       │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│       Master Problem (GAA)     │
│          (GRASP)               │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│        Algorithm (AST)         │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│      VRPTW Solver Engine       │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│      Solution / Evaluator      │
└───────────────────────────────┘

2. Estructura de Carpetas de Código

Estructura mínima recomendada:

src/
│
├── data/
│   └── solomon_loader.py
│
├── model/
│   ├── instance.py
│   ├── solution.py
│   └── evaluator.py
│
├── ast/
│   ├── nodes.py
│   ├── grammar.py
│   └── generator.py
│
├── grasp/
│   ├── grasp_runner.py
│   └── local_search.py
│
├── gaa/
│   ├── master_problem.py
│   └── fitness.py
│
├── pool/
│   └── solution_pool.py
│
├── logging/
│   └── experiment_logger.py
│
└── main.py

3. Flujo General de Ejecución

Pseudocódigo de alto nivel:

load_instances()

initialize_solution_pool()
initialize_logger()

for each algorithm_id in generated_ASTs:
    for each run in runs:
        set_seed(seed)
        solution = run_GRASP_with_AST(algorithm_id)
        evaluate_solution(solution)
        solution_pool.register(solution)
        logger.log(solution)

rank_algorithms()
select_best_algorithm()

4. Clase Instance

Responsabilidad: representar una instancia VRPTW.

class Instance:
    id
    family
    nodes
    demands
    time_windows
    service_times
    distance_matrix

5. Clase Solution

Responsabilidad: representar el resultado final de una ejecución.

class Solution:
    instance_id
    algorithm_id
    num_vehicles
    total_distance
    is_feasible
    penalty_value
    cpu_time


NO contiene rutas completas.

6. Evaluador de Soluciones

Responsabilidad: calcular métricas finales.

class Evaluator:
    evaluate(solution, instance):
        compute_num_vehicles()
        compute_total_distance()
        check_feasibility()
        compute_penalty()

7. AST – Representación del Algoritmo
Nodo Base
class ASTNode:
    children
    execute(state)

Ejemplo de Nodo Funcional
class IfNode(ASTNode):
    condition
    then_branch
    else_branch

Terminal
class Terminal(ASTNode):
    heuristic_name

8. Generador de AST

Responsabilidad: generar algoritmos automáticamente.

generate_random_AST(max_depth, max_nodes)

9. GRASP Runner

Responsabilidad: ejecutar GRASP usando un AST.

run_GRASP(instance, AST):
    solution = greedy_construction(AST)
    solution = local_search(AST, solution)
    return solution

10. Master Problem (GAA)

Responsabilidad: explorar espacio de algoritmos.

class GAAMaster:
    generate_ASTs()
    evaluate_algorithms()
    select_best()

11. SolutionPool

Responsabilidad: mantener mejores soluciones.

class SolutionPool:
    global_best
    best_by_algorithm

    register(solution):
        update_global_best()
        update_best_by_algorithm()

12. Logger

Responsabilidad: registrar ejecuciones.

class ExperimentLogger:
    log(solution, metadata)

13. main.py

Punto de entrada del sistema.

def main():
    load_data()
    generate_algorithms()
    run_experiments()
    summarize_results()

14. Principios Clave de Implementación

sin estado global oculto

control explícito de semillas

separación estricta de responsabilidades

logging solo al final de cada ejecución

sin efectos colaterales entre runs

15. Resumen

Esta estructura:

es minimalista

es escalable

es reproducible

es alineada con GAA

es interpretable

es compatible con Solomon VRPTW