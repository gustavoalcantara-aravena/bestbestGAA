"""
============================================================
Solution Evaluator
VRPTW Solomon
============================================================

Responsabilidades:
- Evaluar soluciones VRPTW (V, D)
- Verificar factibilidad (capacidad y tiempo)
- Calcular penalizaciones suaves (soft constraints)
- Calcular fitness escalar para GAA
- Integración directa con BKS
"""

from typing import Dict, List, Tuple
import math


# ============================================================
# Evaluación de una Ruta
# ============================================================

def evaluate_route(
    route: List[int],
    instance: Dict
) -> Dict:
    """
    Evalúa una ruta individual (incluye depósito 0 al inicio y fin).

    Retorna métricas y violaciones:
    - distance
    - capacity_violation
    - time_violation
    - feasible
    """
    nodes = instance["nodes"]
    dist = instance["distance_matrix"]
    Q = instance["capacity"]

    load = 0
    time = 0.0
    distance = 0.0

    time_violation = 0.0

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]

        distance += dist[u][v]
        time += dist[u][v]

        node_u = nodes[u]
        node_v = nodes[v]

        # Servicio en u (excepto depósito final)
        if u != 0:
            time += node_u["service_time"]

        # Espera si se llega temprano
        if time < node_v["ready_time"]:
            time = node_v["ready_time"]

        # Violación de ventana
        if time > node_v["due_date"]:
            time_violation += time - node_v["due_date"]

        if v != 0:
            load += node_v["demand"]

    capacity_violation = max(0, load - Q)

    feasible = (capacity_violation == 0 and time_violation == 0)

    return {
        "distance": distance,
        "capacity_violation": capacity_violation,
        "time_violation": time_violation,
        "feasible": feasible
    }


# ============================================================
# Evaluación de una Solución Completa
# ============================================================

def evaluate_solution(
    solution: Dict,
    instance: Dict
) -> Dict:
    """
    Evalúa una solución completa (lista de rutas).

    solution:
    {
        "routes": [[0, i, j, 0], ...]
    }
    """
    total_distance = 0.0
    total_capacity_violation = 0.0
    total_time_violation = 0.0
    feasible = True

    for route in solution["routes"]:
        metrics = evaluate_route(route, instance)

        total_distance += metrics["distance"]
        total_capacity_violation += metrics["capacity_violation"]
        total_time_violation += metrics["time_violation"]

        if not metrics["feasible"]:
            feasible = False

    return {
        "num_vehicles": len(solution["routes"]),
        "total_distance": total_distance,
        "capacity_violation": total_capacity_violation,
        "time_violation": total_time_violation,
        "feasible": feasible
    }


# ============================================================
# Penalización Suave (Soft Constraints)
# ============================================================

def compute_penalty(
    eval_metrics: Dict,
    alpha_cap: float,
    alpha_time: float
) -> float:
    """
    Penalización escalar por violaciones.
    """
    return (
        alpha_cap * eval_metrics["capacity_violation"]
        + alpha_time * eval_metrics["time_violation"]
    )


# ============================================================
# Fitness para GAA
# ============================================================

def compute_fitness(
    eval_metrics: Dict,
    penalty: float,
    w_vehicles: float,
    w_distance: float
) -> float:
    """
    Fitness escalar (a maximizar).

    Convención:
    - Menos vehículos → mejor
    - Menor distancia → mejor
    - Penalizaciones → muy malas
    """
    return -(
        w_vehicles * eval_metrics["num_vehicles"]
        + w_distance * eval_metrics["total_distance"]
        + penalty
    )


# ============================================================
# Evaluación Completa (One-shot)
# ============================================================

def evaluate_solution_full(
    solution: Dict,
    instance: Dict,
    penalty_cfg: Dict,
    fitness_cfg: Dict
) -> Dict:
    """
    Pipeline completo de evaluación.

    penalty_cfg:
    {
        "alpha_capacity": float,
        "alpha_time": float
    }

    fitness_cfg:
    {
        "w_vehicles": float,
        "w_distance": float
    }
    """
    metrics = evaluate_solution(solution, instance)

    penalty = compute_penalty(
        metrics,
        penalty_cfg["alpha_capacity"],
        penalty_cfg["alpha_time"]
    )

    fitness = compute_fitness(
        metrics,
        penalty,
        fitness_cfg["w_vehicles"],
        fitness_cfg["w_distance"]
    )

    return {
        "metrics": metrics,
        "penalty": penalty,
        "fitness": fitness
    }
