GRASPSolver (Completo)
Construcción + Búsqueda Local para VRPTW Solomon (GRASP + GAA)
1. Rol del GRASPSolver

El GRASPSolver resuelve una instancia VRPTW mediante GRASP, usando un algoritmo definido por un AST para:

elegir criterios greedy y randomización (fase constructiva)

elegir operadores de búsqueda local y política de aceptación (fase LS)

Entradas:

instance (VRPTWInstance)

algorithm (AST)

config["grasp"] (parámetros GRASP)

Salida:

solution (Solution con rutas + métricas; factible o penalizada)

2. Interfaz del Solver
class GRASPSolver:
    def __init__(self, instance, algorithm, grasp_config, rng):
        ...

    def solve(self) -> Solution:
        ...


Notas:

rng debe ser un generador aleatorio controlado por semilla (no usar random global sin control).

algorithm es inmutable durante la ejecución.

3. Flujo General de solve()

Pseudocódigo:

solve():
    best = None

    for it in 1..max_iterations:
        s = constructive_phase()
        if local_search_enabled:
            s = local_search_phase(s)

        s = finalize_solution(s)  # update metrics, penalty if needed

        if best is None or is_better(s, best):
            best = deep_copy(s)

    return best


El GRASP clásico repite construcción + LS max_iterations veces y retorna la mejor solución.

4. Fase Constructiva (Greedy Randomized)
4.1 Objetivo

Construir una solución inicial (idealmente factible). Para GAA puede permitirse infactible y penalizar.

4.2 Estructuras internas mínimas

unserved: conjunto de clientes no atendidos

solution.routes: lista de rutas

current_route: ruta activa

4.3 Flujo constructivo recomendado (secuencial por rutas)
constructive_phase():
    unserved = all customers
    sol = Solution(instance)

    while unserved not empty:

        route = Route(instance)
        feasible_insertions = compute_all_feasible_insertions(route, unserved)

        if no feasible insertion:
            # cerrar ruta vacía no permitido
            if route has customers:
                sol.add_route(route)
            else:
                # si no puedo insertar ni en ruta nueva, fallback:
                #  - si allow_infeasible: insertar mejor penalizado
                #  - else: break con sol parcial (se penaliza por clientes faltantes)
                handle_no_insertion_case(sol, unserved)
            continue

        # construir una ruta hasta que no se pueda insertar más
        while True:
            candidates = build_candidate_list(route, unserved)
            if candidates empty:
                break

            scores = score_candidates(route, candidates)  # AST aquí
            rcl = build_RCL(candidates, scores, rcl_size or alpha)
            chosen = random_choice(rcl)  # rng controlado

            apply_insertion(route, chosen)
            unserved.remove(chosen.customer)

        sol.add_route(route)

    sol.update()
    return sol

5. Candidate List y RCL
5.1 Candidate (definición)

Un candidato es una inserción potencial:

Candidate:
  customer_id
  position (insert between i and j)
  delta_distance
  delta_time_feasibility_info
  waiting_time
  slack_forward/backward (si existe)
  resulting_load
  resulting_time_violation (si allow_infeasible)

5.2 Construcción de candidatos

Mínimo viable:

Para cada cliente u no servido

Para cada posición posible en la ruta

Chequear factibilidad (tiempo + capacidad)

calcular delta_distance

Para eficiencia:

limitar posiciones (best insertion position)

usar candidate list basada en vecinos cercanos al último nodo

5.3 Scoring (AST)

El AST produce un score para cada candidato basado en terminales.

Ejemplo de interfaz:

score = algorithm.score_insertion(
    instance=instance,
    route=route,
    candidate=candidate,
    state=construction_state
)


Regla:

menor score = mejor (o viceversa), pero definirlo fijo.

5.4 RCL (dos opciones)

Opción A: por tamaño fijo

rcl = best k candidates by score


Opción B: por alpha (clásico GRASP)

threshold = min_score + alpha*(max_score - min_score)
rcl = {c | score(c) <= threshold}

6. Manejo de Infactibilidad (GAA)

Si allow_infeasible = true, se permite:

inserciones con violación temporal/capacidad

se registra magnitud de violación y se penaliza al final

Recomendación mínima:

permitir violación temporal (time windows) con penalización fuerte

evitar violación de “atención única” (nunca duplicar clientes)

si quedan clientes sin servir: penalización por cliente faltante

Penalización sugerida:

penalty += big_M * num_unserved

7. Fase de Búsqueda Local (Local Search)
7.1 Objetivo

Mejorar (V, D) manteniendo factibilidad o reduciendo penalización.

7.2 Operadores mínimos

Relocate (intra + inter)

Swap (inter)

2-opt (intra) o Or-opt (intra)

7.3 Flujo LS recomendado (First Improvement / Best Improvement)
local_search_phase(sol):
    no_improve = 0

    while no_improve < max_no_improve:
        move = select_move(sol)          # AST decide operador y parámetros
        best_neighbor = explore(sol, move.operator)

        if best_neighbor improves sol (lexicographic or penalized objective):
            sol = apply(best_neighbor)
            no_improve = 0
        else:
            no_improve += 1

    return sol

7.4 Selección del operador (AST)

Interfaz sugerida:

op = algorithm.select_operator(state_features)


state_features recomendadas (baratas):

num_vehicles

total_distance

feasible_rate_routes

avg_slack

stagnation_counter

8. Evaluación durante LS
8.1 Comparación canónica (factibles)
better(a, b):
    if a.num_vehicles != b.num_vehicles: return a.num_vehicles < b.num_vehicles
    return a.total_distance < b.total_distance

8.2 Si hay infeasibilidad (penalizada)

Definir una función escalar auxiliar SOLO para guiar LS:

f(sol) = Wv * num_vehicles + Wd * total_distance + Wp * penalty


con:

Wv muy grande para priorizar vehículos

Wp grande para empujar factibilidad

Importante:

La selección final del mejor puede seguir siendo lexicográfica sobre factibles

O penalizada si permites infactibles al final (no recomendado para Solomon)

9. Exploración de vecindario (implementación)
9.1 Relocate inter-route (núcleo para reducir vehículos)

Objetivo:

mover un cliente de una ruta a otra y potencialmente vaciar una ruta.

Pseudocódigo:

for each route_a:
  for each customer u in route_a:
    for each route_b != route_a:
      for each insertion position in route_b:
         if feasible (o allow_infeasible):
            compute delta
            keep best move

9.2 Swap inter-route

Intercambiar u en ruta A por v en ruta B.

9.3 2-opt / Or-opt intra-route

2-opt puede destruir factibilidad temporal

Or-opt (mover cadena corta) suele ser más estable para VRPTW

10. Parada (Stopping Criteria)

Fase GRASP:

max_iterations

Fase LS:

max_no_improve (estancamiento)

opcional: time_limit_seconds global por ejecución

11. Salida del GRASPSolver

Al terminar solve():

retorna la mejor solución encontrada

solución debe tener:

num_vehicles

total_distance

is_feasible

penalty_value

12. Errores típicos a evitar

Usar random global sin semilla controlada

No recalcular tiempos tras movimientos

Aplicar 2-opt sin chequear tiempo

Comparar distancias cuando V difiere

Permitir duplicación de clientes

13. Resumen (lo mínimo que debe existir en código)

constructive_phase() con:

candidate list

scoring AST

RCL + aleatoriedad controlada

local_search_phase() con:

relocate + swap + (or-opt o 2-opt)

selección de operador por AST

criterio de aceptación definido

solve() que repite y retorna el mejor

Si quieres, el siguiente paso lógico es uno de estos:

Especificación exacta del estado (features) que el AST recibe en construcción y LS

Definición del formato JSON del AST + algorithm_id + ast_signature

Diseño de Evaluator (cálculo de V, D, factibilidad, penalización, gap)

Especificación exacta del estado (features) que el AST recibe en construcción y LS

Perfecto. A continuación tienes la especificación exacta, mínima y suficiente del estado (features) que el AST recibe tanto en fase constructiva como en búsqueda local (LS) para VRPTW Solomon + GRASP + GAA.

📌 Objetivo:

Que el AST tenga información rica,

pero barata de computar,

estable entre instancias,

y directamente implementable.

Guárdalo como:

06 Arquitectura de Implementación/03_Estado_AST_Features.md


(en texto plano para notes / markdown)

Estado del AST (Features)
VRPTW – Construcción y Búsqueda Local (GRASP + GAA)
1. Principios de Diseño del Estado

El estado que recibe el AST debe cumplir:

✅ Independiente de la implementación interna del solver

✅ No depender de rutas completas

✅ Computable en O(1) u O(ruta)

✅ Comparable entre instancias Solomon

✅ Suficiente para expresar heurísticas conocidas (Solomon, ALNS, TS)

🚫 No incluir:

listas completas de clientes

matrices de distancias completas

simulaciones profundas dentro del AST

2. Separación por Fase

El AST recibe dos tipos de estado, según la fase:

Estado de Construcción  (Insertion State)
Estado de Búsqueda Local (Local Search State)


Cada uno tiene features específicas, aunque comparten algunas.

3. Estado en Fase Constructiva (Insertion State)

Este estado se pasa al AST cada vez que se evalúa una inserción candidata.

3.1 Identificación básica
phase = "construction"

3.2 Estado Global de la Solución Parcial

Features de la solución parcial actual:

num_routes_current        : int
num_customers_served     : int
num_customers_remaining  : int


Derivables en O(1).

3.3 Estado de la Ruta Activa

Ruta donde se evalúa la inserción:

route_length             : int          # clientes en la ruta
route_load               : float        # demanda acumulada
route_capacity_remaining : float        # Q - route_load

3.4 Estado Temporal de la Ruta

Información temporal resumida (NO cronograma completo):

route_current_time       : float        # tiempo al final de la ruta
route_total_waiting      : float        # espera acumulada
route_slack_forward      : float        # margen máximo de retraso permitido


Si no implementas Savelsbergh aún:

route_slack_forward puede aproximarse como
min(l_i - arrival_i) en la ruta.

3.5 Estado del Cliente Candidato

Cliente u que se intenta insertar:

cust_demand              : float
cust_ready_time          : float        # e_u
cust_due_time            : float        # l_u
cust_service_time        : float

3.6 Estado de la Inserción (Feature CLAVE)

Resultado local de insertar u en una posición específica:

delta_distance           : float
delta_time               : float        # incremento de tiempo
delta_waiting             : float
capacity_violation       : float        # >0 si viola
time_violation            : float        # >0 si viola


Estas features permiten:

Solomon I1

Regret insertion

Penalizaciones suaves

Urgencia temporal

3.7 Features Derivadas (Muy Importantes)

Precomputadas, baratas:

urgency                  = cust_due_time - route_current_time
relative_slack            = route_slack_forward / (cust_due_time - cust_ready_time + ε)
load_ratio                = route_load / Q

3.8 Estado Completo – Construcción (Resumen)
InsertionState = {
  phase,
  num_routes_current,
  num_customers_served,
  num_customers_remaining,

  route_length,
  route_load,
  route_capacity_remaining,

  route_current_time,
  route_total_waiting,
  route_slack_forward,

  cust_demand,
  cust_ready_time,
  cust_due_time,
  cust_service_time,

  delta_distance,
  delta_time,
  delta_waiting,
  capacity_violation,
  time_violation,

  urgency,
  relative_slack,
  load_ratio
}


👉 Este es el estado mínimo recomendado.

4. Estado en Búsqueda Local (Local Search State)

Este estado se pasa al AST cuando decide operador, aceptación o estrategia.

4.1 Identificación básica
phase = "local_search"

4.2 Estado Global de la Solución
num_routes                : int
total_distance            : float
is_feasible               : bool
penalty_value             : float

4.3 Estado de las Rutas (Agregado)

No rutas completas, solo estadísticas:

avg_route_length          : float
min_route_length          : int
max_route_length          : int

avg_route_load_ratio      : float
min_route_slack           : float

4.4 Estado de Factibilidad
num_time_violations       : int
num_capacity_violations   : int

4.5 Estado de Progreso / Estancamiento

Crítico para decisiones adaptativas:

ls_iteration              : int
iterations_no_improve     : int
last_improvement_delta    : float

4.6 Estado del Movimiento Evaluado (si aplica)

Cuando el AST evalúa aceptación de un movimiento:

move_type                 : enum {relocate, swap, or_opt, two_opt}
move_delta_distance       : float
move_delta_vehicles       : int
move_delta_penalty        : float

4.7 Estado Completo – Local Search (Resumen)
LocalSearchState = {
  phase,

  num_routes,
  total_distance,
  is_feasible,
  penalty_value,

  avg_route_length,
  min_route_length,
  max_route_length,

  avg_route_load_ratio,
  min_route_slack,

  num_time_violations,
  num_capacity_violations,

  ls_iteration,
  iterations_no_improve,
  last_improvement_delta,

  move_type,
  move_delta_distance,
  move_delta_vehicles,
  move_delta_penalty
}

5. Interfaz del AST (Contrato)

El AST NO accede al solver, solo recibe estado y devuelve decisiones.

5.1 En Construcción
score = AST.score_insertion(InsertionState)

5.2 En Búsqueda Local
operator = AST.select_operator(LocalSearchState)
accept   = AST.accept_move(LocalSearchState)

6. Qué NO debe hacer el AST

❌ No modificar rutas
❌ No simular inserciones
❌ No acceder a listas de clientes
❌ No recalcular tiempos
❌ No usar random interno sin pasar por solver

7. Correspondencia con la Literatura

Este estado permite expresar:

Solomon I1 / I2 (urgency, delta distance)

Regret insertion

Penalizaciones suaves (Taillard)

ALNS-like decisions (relocate vs swap)

TS / ILS adaptativos (stagnation features)

8. Beneficio para GAA

✔ ASTs compactos
✔ Fácil interpretación
✔ Bloat controlado
✔ Transferible entre familias Solomon
✔ Aprendizaje real de lógica heurística

9. Regla de Oro

Si una feature no cambia la decisión del AST, elimínala.

Este conjunto es suficiente y necesario.