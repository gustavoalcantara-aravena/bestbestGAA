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