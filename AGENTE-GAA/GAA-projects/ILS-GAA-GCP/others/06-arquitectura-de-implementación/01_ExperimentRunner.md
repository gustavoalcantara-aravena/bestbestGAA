ExperimentRunner
Diseño Completo para GRASP + GAA – VRPTW Solomon
1. Rol del ExperimentRunner

El ExperimentRunner es el orquestador del experimento computacional.

Su responsabilidad es:

ejecutar algoritmos (ASTs) sobre instancias VRPTW

controlar repeticiones (runs)

gestionar semillas

evaluar soluciones

registrar resultados

alimentar el SolutionPool

garantizar reproducibilidad

🚫 NO implementa:

GRASP

VRPTW

lógica de fitness

operadores

2. Responsabilidades (Single Responsibility)

El ExperimentRunner debe:

Iterar sobre algoritmos generados (ASTs)

Iterar sobre instancias Solomon

Ejecutar múltiples runs por par (algoritmo, instancia)

Controlar semillas por run

Ejecutar el solver GRASP

Evaluar la solución final

Registrar la solución en:

logs

SolutionPool

Almacenar resultados agregados

Exportar resultados finales

3. Entradas del ExperimentRunner
Parámetros obligatorios
algorithms      : List[AlgorithmAST]
instances       : List[Instance]
bks_data        : Dict[instance_id → (k_bks, d_bks)]
config          : Dict (desde config.yaml)
solution_pool   : SolutionPool
logger          : Logger

4. Salidas del ExperimentRunner

Logs por ejecución

Resultados agregados por:

algoritmo

instancia

Ranking de algoritmos

Mejor algoritmo global

Archivos CSV / JSON de resultados

5. Estructura Interna Recomendada
ExperimentRunner
│
├── run()
│   ├── loop_algorithms()
│   │   ├── loop_instances()
│   │   │   ├── loop_runs()
│   │   │   │   ├── set_seed()
│   │   │   │   ├── run_solver()
│   │   │   │   ├── evaluate()
│   │   │   │   ├── log()
│   │   │   │   └── register_solution()
│
├── aggregate_results()
├── rank_algorithms()
└── save_results()

6. Clase ExperimentRunner (Interfaz)
class ExperimentRunner:

    def __init__(
        self,
        algorithms,
        instances,
        bks_data,
        config,
        solution_pool,
        logger
    )

7. Método run()
Función

Ejecuta el experimento completo.

Pseudocódigo
def run():

    for algorithm in algorithms:
        logger.info("Algorithm start")

        for instance in instances:
            for run_id in range(num_runs):

                seed = base_seed + run_id
                set_seed(seed)

                solution = run_single_execution(
                    algorithm,
                    instance,
                    run_id
                )

                solution_pool.register(solution)
                log_solution(solution)

    aggregate_results()
    rank_algorithms()

8. Ejecución Individual (Core Loop)
Método interno recomendado
_run_single_execution(algorithm, instance, run_id)

Pseudocódigo
start_timer()

solver = GRASPSolver(
    algorithm=algorithm,
    instance=instance,
    config=config["grasp"]
)

solution = solver.solve()

evaluation = Evaluator.evaluate(solution, instance, bks_data)

solution.attach_metrics(evaluation)

stop_timer()

solution.cpu_time = elapsed_time

return solution

9. Control de Semillas (CRÍTICO)

Regla:

Cada run debe ser reproducible e independiente

Recomendación:

global_seed = config["random"]["global_seed"]

seed = global_seed
     + algorithm_index * 1000
     + instance_index * 100
     + run_id


Esto evita correlación entre ejecuciones.

10. Qué Registra el ExperimentRunner

Por cada ejecución:

algorithm_id

instance_id

run_id

seed

num_vehicles

total_distance

feasibility

penalty

gap_vs_bks

cpu_time

11. Manejo de BKS

Durante evaluación:

if solution.num_vehicles > bks.k:
    mark as dominated
    apply strong penalty
elif solution.num_vehicles == bks.k:
    compute gap
else:
    mark as improvement


⚠️ Nunca comparar distancias si V(sol) ≠ V(BKS)

12. Agregación de Resultados

Después de todas las ejecuciones:

Por algoritmo:

promedio V

promedio D

promedio gap

desviación estándar

tasa de factibilidad

tiempo promedio

13. Ranking de Algoritmos

Criterio recomendado (lexicográfico):

Menor promedio de vehículos

Menor gap promedio (cuando V coincide)

Menor desviación estándar

Menor tiempo promedio

14. Guardado de Resultados

Archivos mínimos:

results/
├── runs_log.csv
├── algorithm_summary.csv
├── best_algorithm.json

15. Invariantes del ExperimentRunner

Debe cumplirse siempre:

No modifica algoritmos

No modifica instancias

No almacena rutas completas

No guarda estados intermedios

No decide operadores

16. Errores Comunes a Evitar

❌ Mezclar lógica GRASP aquí
❌ Comparar distancias con diferente número de vehículos
❌ Reutilizar semillas
❌ Guardar rutas completas en logs
❌ Cambiar AST durante ejecución

17. Resultado Esperado

Al finalizar run():

Todos los algoritmos han sido evaluados

SolutionPool contiene los mejores

Logs permiten reproducir cada ejecución

Se puede responder:

¿qué algoritmo es mejor?

¿por qué?

¿en qué tipo de instancia?

18. Este diseño es adecuado porque

✔ Compatible con GAA
✔ Compatible con GRASP
✔ Reproducible
✔ Escalable
✔ Interpretable
✔ Aceptable para revisión académica