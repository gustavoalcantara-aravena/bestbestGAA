# src/evaluation/solution_evaluator.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class RouteMetrics:
    distance: float
    load: float
    time_window_violation: float
    capacity_violation: float
    feasible_time: bool
    feasible_capacity: bool


@dataclass
class SolutionMetrics:
    n_vehicles: int
    total_distance: float
    time_window_violation: float
    capacity_violation: float
    feasible: bool
    lex_key: Tuple[int, float]  # (vehicles, distance)
    gap_k: Optional[int] = None
    gap_d_percent: Optional[float] = None
    dominates_bks: Optional[bool] = None


class SolutionEvaluator:
    """
    Evaluador canónico VRPTW Solomon:
      - evalúa rutas y solución
      - valida restricciones
      - calcula gap vs BKS
      - comparación lexicográfica

    Requiere una Instance con:
      instance.nodes[id], instance.capacity, instance.distance_matrix, instance.time_matrix
    """

    def __init__(self, alpha_cap: float = 1000.0, alpha_time: float = 1000.0):
        self.alpha_cap = float(alpha_cap)
        self.alpha_time = float(alpha_time)

    # ---------- Métricas por ruta ----------

    def evaluate_route(self, route_nodes: List[int], instance) -> RouteMetrics:
        """
        route_nodes: lista de ids, se espera [0, ..., 0]
        """
        if len(route_nodes) < 2:
            return RouteMetrics(0.0, 0.0, 0.0, 0.0, True, True)

        Q = instance.capacity
        nodes = instance.nodes
        dist = instance.distance_matrix
        tmat = instance.time_matrix

        load = 0.0
        time = 0.0  # tiempo actual al salir del depot (0)
        tw_violation = 0.0

        # asumimos empieza en depot
        for idx in range(1, len(route_nodes)):
            i = route_nodes[idx - 1]
            j = route_nodes[idx]

            time += tmat[i][j]      # viaje i->j
            # llegada a j
            ready = nodes[j].ready_time
            due = nodes[j].due_date
            service = nodes[j].service_time

            # esperar si llega antes
            if time < ready:
                time = ready

            # violación si llega después del due (hard TW en Solomon)
            if time > due:
                tw_violation += (time - due)

            # servicio
            time += service

            # carga (no sumar depot)
            if j != 0:
                load += nodes[j].demand

        cap_violation = max(0.0, load - Q)
        route_dist = 0.0
        for idx in range(1, len(route_nodes)):
            i = route_nodes[idx - 1]
            j = route_nodes[idx]
            route_dist += dist[i][j]

        return RouteMetrics(
            distance=route_dist,
            load=load,
            time_window_violation=tw_violation,
            capacity_violation=cap_violation,
            feasible_time=(tw_violation <= 1e-9),
            feasible_capacity=(cap_violation <= 1e-9),
        )

    # ---------- Validación restricciones ----------

    def validate_all_constraints(self, solution, instance) -> Dict[str, Any]:
        """
        Verifica 7 checks prácticos/canónicos.
        Retorna dict con flags + detalles mínimos.
        """
        n_customers = instance.n_customers
        customers_expected = set(range(1, n_customers + 1))

        visited: List[int] = []
        depot_ok = True
        no_empty_routes = True
        continuity_ok = True

        for r in solution.routes:
            rn = getattr(r, "nodes", None)
            if rn is None:
                raise ValueError("Route sin atributo .nodes (lista de ids)")

            # ruta vacía o trivial
            if len(rn) == 0:
                no_empty_routes = False
                continue

            # depot al inicio y fin
            if rn[0] != 0 or rn[-1] != 0:
                depot_ok = False

            # continuidad: ids válidos
            for nid in rn:
                if not (0 <= nid < instance.n_nodes):
                    continuity_ok = False

            # recolectar clientes
            for nid in rn:
                if nid != 0:
                    visited.append(nid)

        # cobertura / unicidad
        visited_set = set(visited)
        coverage_ok = (visited_set == customers_expected)
        duplicates_ok = (len(visited) == len(visited_set))
        completeness_ok = coverage_ok  # redundante pero útil para logging

        # capacidad y TW a nivel solución (desde evaluate_solution)
        solm = self.evaluate_solution(solution, instance)
        capacity_ok = (solm.capacity_violation <= 1e-9)
        time_ok = (solm.time_window_violation <= 1e-9)

        out = {
            "constraint_1_unique_visit": bool(coverage_ok and duplicates_ok),
            "constraint_2_depot": bool(depot_ok),
            "constraint_3_capacity": bool(capacity_ok),
            "constraint_4_time_window": bool(time_ok),
            "constraint_5_continuity": bool(continuity_ok),
            "constraint_6_completeness": bool(completeness_ok),
            "constraint_7_no_empty_routes": bool(no_empty_routes),
        }
        out["all_satisfied"] = all(out.values())
        out["visited_count"] = len(visited)
        out["missing_customers"] = sorted(list(customers_expected - visited_set))
        out["duplicate_customers"] = _find_duplicates(visited)
        return out

    # ---------- Métricas por solución ----------

    def evaluate_solution(self, solution, instance) -> SolutionMetrics:
        total_dist = 0.0
        twv = 0.0
        capv = 0.0

        # contar rutas reales: ruta con al menos un cliente
        n_vehicles = 0
        for r in solution.routes:
            rn = r.nodes
            if any(nid != 0 for nid in rn):
                n_vehicles += 1

            rm = self.evaluate_route(rn, instance)
            total_dist += rm.distance
            twv += rm.time_window_violation
            capv += rm.capacity_violation

        feasible = (twv <= 1e-9) and (capv <= 1e-9)
        lex_key = (n_vehicles, total_dist)

        return SolutionMetrics(
            n_vehicles=n_vehicles,
            total_distance=total_dist,
            time_window_violation=twv,
            capacity_violation=capv,
            feasible=feasible,
            lex_key=lex_key,
        )

    # ---------- Penalización y fitness ----------

    def compute_penalty(self, metrics: SolutionMetrics) -> float:
        return (self.alpha_cap * metrics.capacity_violation) + (self.alpha_time * metrics.time_window_violation)

    def compute_scalar_fitness(self, metrics: SolutionMetrics, w_vehicles: float = 1e6, w_distance: float = 1.0) -> float:
        """
        Fitness escalar para búsquedas internas (si lo necesitas).
        OJO: ranking final debe ser lexicográfico (Solomon).
        """
        penalty = self.compute_penalty(metrics)
        return - (w_vehicles * metrics.n_vehicles + w_distance * metrics.total_distance + penalty)

    # ---------- Lexicográfico ----------

    @staticmethod
    def compute_lexicographic_fitness(metrics: SolutionMetrics) -> Tuple[int, float]:
        return metrics.lex_key

    @staticmethod
    def lexicographic_compare(a: Tuple[int, float], b: Tuple[int, float]) -> int:
        """
        Retorna:
          -1 si a es mejor (menor)
           0 si iguales
           1 si a es peor (mayor)
        """
        if a[0] < b[0]:
            return -1
        if a[0] > b[0]:
            return 1
        # empate en vehículos -> distancia
        if a[1] < b[1]:
            return -1
        if a[1] > b[1]:
            return 1
        return 0

    # ---------- BKS / Gap ----------

    @staticmethod
    def compute_gap(metrics: SolutionMetrics, bks_entry: Tuple[int, float]) -> Tuple[int, Optional[float]]:
        """
        Gap recomendado:
          gap_k = k_sol - k_bks
          gap_d% solo si gap_k == 0
        """
        k_bks, d_bks = bks_entry
        gap_k = metrics.n_vehicles - k_bks
        if gap_k == 0:
            gap_d = ((metrics.total_distance - d_bks) / d_bks) * 100.0
            return gap_k, gap_d
        return gap_k, None

    def validate_vs_bks(self, metrics: SolutionMetrics, bks_entry: Tuple[int, float]) -> Dict[str, Any]:
        """
        dominates_bks: True si (V,D) mejor lexicográficamente que BKS.
        """
        k_bks, d_bks = bks_entry
        cmp_ = self.lexicographic_compare(metrics.lex_key, (k_bks, d_bks))
        gap_k, gap_d = self.compute_gap(metrics, bks_entry)
        return {
            "gap_k": gap_k,
            "gap_d_percent": gap_d,
            "dominates_bks": (cmp_ == -1),
        }

    # ---------- Stats para logging ----------

    def solution_statistics(self, solution, instance, bks_dict: Optional[Dict[str, Tuple[int, float]]] = None) -> Dict[str, Any]:
        metrics = self.evaluate_solution(solution, instance)
        cons = self.validate_all_constraints(solution, instance)

        out: Dict[str, Any] = {
            "n_vehicles": metrics.n_vehicles,
            "total_distance": metrics.total_distance,
            "feasible": bool(metrics.feasible and cons["all_satisfied"]),
            "capacity_violation": metrics.capacity_violation,
            "time_window_violation": metrics.time_window_violation,
            "routes_utilized": metrics.n_vehicles,
            "avg_customers_per_route": (instance.n_customers / metrics.n_vehicles) if metrics.n_vehicles > 0 else 0.0,
        }

        # route stats
        route_dists = []
        for r in solution.routes:
            if any(nid != 0 for nid in r.nodes):
                rm = self.evaluate_route(r.nodes, instance)
                route_dists.append(rm.distance)
        if route_dists:
            out["avg_route_distance"] = sum(route_dists) / len(route_dists)
            out["max_route_distance"] = max(route_dists)
            out["min_route_distance"] = min(route_dists)
        else:
            out["avg_route_distance"] = 0.0
            out["max_route_distance"] = 0.0
            out["min_route_distance"] = 0.0

        # BKS stats
        if bks_dict is not None:
            entry = bks_dict.get(instance.instance_id)
            if entry is not None:
                b = self.validate_vs_bks(metrics, entry)
                out.update(b)
                out["k_bks"], out["d_bks"] = entry
            else:
                out["gap_k"] = None
                out["gap_d_percent"] = None
                out["dominates_bks"] = None

        # constraints snapshot
        out.update({k: v for k, v in cons.items() if k.startswith("constraint_") or k == "all_satisfied"})
        return out


def _find_duplicates(items: List[int]) -> List[int]:
    seen = set()
    dups = set()
    for x in items:
        if x in seen:
            dups.add(x)
        else:
            seen.add(x)
    return sorted(list(dups))
