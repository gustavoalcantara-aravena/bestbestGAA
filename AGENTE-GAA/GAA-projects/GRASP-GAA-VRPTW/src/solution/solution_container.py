"""
============================================================
Solution Container
VRPTW - Solomon
============================================================

Este módulo define el contenedor canónico de una solución VRPTW.

Objetivos:
- Representar una solución de forma clara y consistente
- Almacenar métricas, fitness y trazabilidad
- Facilitar comparación, logging y ranking
- Ser inmutable conceptualmente (copias controladas)

Una Solution NO es el algoritmo, es el RESULTADO de ejecutarlo.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import copy
import time


# ============================================================
# Solution Container
# ============================================================

@dataclass
class Solution:
    """
    Contenedor canónico de solución VRPTW.
    """

    # --------------------------------------------------------
    # Identidad
    # --------------------------------------------------------
    solution_id: str
    algorithm_id: str
    instance_id: str
    family: str
    seed: int

    # --------------------------------------------------------
    # Solución estructural
    # --------------------------------------------------------
    routes: List[List[int]]  # cada ruta empieza y termina en 0

    # --------------------------------------------------------
    # Métricas canónicas (Solomon)
    # --------------------------------------------------------
    num_vehicles: int
    total_distance: float

    # --------------------------------------------------------
    # Factibilidad
    # --------------------------------------------------------
    feasible: bool
    capacity_violation: float
    time_violation: float

    # --------------------------------------------------------
    # Fitness (para GAA)
    # --------------------------------------------------------
    fitness: float
    penalty: float

    # --------------------------------------------------------
    # Referencia BKS
    # --------------------------------------------------------
    bks_vehicles: int
    bks_distance: float
    gap_bks: Optional[float]  # None si V != V_BKS

    # --------------------------------------------------------
    # Metadata experimental
    # --------------------------------------------------------
    iteration: int
    phase: str               # "construction", "ls", "final"
    timestamp: float = field(default_factory=time.time)

    # --------------------------------------------------------
    # Diagnóstico opcional
    # --------------------------------------------------------
    notes: Dict[str, Any] = field(default_factory=dict)

    # ========================================================
    # Factory method
    # ========================================================

    @staticmethod
    def from_evaluation(
        *,
        solution_id: str,
        algorithm_id: str,
        instance_id: str,
        family: str,
        seed: int,
        routes: List[List[int]],
        evaluation: Dict[str, Any],
        bks: Dict[str, Any],
        iteration: int,
        phase: str,
        notes: Optional[Dict[str, Any]] = None
    ) -> "Solution":
        """
        Construye una Solution a partir del output del evaluator.
        """

        metrics = evaluation["metrics"]

        # Gap solo es válido si iguala número de vehículos BKS
        gap = None
        if metrics["num_vehicles"] == bks["k_bks"]:
            gap = (metrics["total_distance"] - bks["d_bks"]) / bks["d_bks"]

        return Solution(
            solution_id=solution_id,
            algorithm_id=algorithm_id,
            instance_id=instance_id,
            family=family,
            seed=seed,

            routes=copy.deepcopy(routes),

            num_vehicles=metrics["num_vehicles"],
            total_distance=metrics["total_distance"],

            feasible=metrics["feasible"],
            capacity_violation=metrics["capacity_violation"],
            time_violation=metrics["time_violation"],

            fitness=evaluation["fitness"],
            penalty=evaluation["penalty"],

            bks_vehicles=bks["k_bks"],
            bks_distance=bks["d_bks"],
            gap_bks=gap,

            iteration=iteration,
            phase=phase,
            notes=notes or {}
        )

    # ========================================================
    # Comparadores (orden canónico Solomon)
    # ========================================================

    def dominates(self, other: "Solution") -> bool:
        """
        Dominancia lexicográfica Solomon:
        - Menos vehículos domina siempre
        - Igual vehículos, menor distancia domina
        """
        if self.num_vehicles < other.num_vehicles:
            return True
        if self.num_vehicles == other.num_vehicles:
            return self.total_distance < other.total_distance
        return False

    def better_than(self, other: "Solution") -> bool:
        """
        Alias semántico de dominates.
        """
        return self.dominates(other)

    # ========================================================
    # Utilidades
    # ========================================================

    def copy(self) -> "Solution":
        """
        Copia profunda de la solución.
        """
        return copy.deepcopy(self)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialización simple (logging / JSON).
        """
        return {
            "solution_id": self.solution_id,
            "algorithm_id": self.algorithm_id,
            "instance_id": self.instance_id,
            "family": self.family,
            "seed": self.seed,

            "num_vehicles": self.num_vehicles,
            "total_distance": self.total_distance,
            "feasible": self.feasible,
            "capacity_violation": self.capacity_violation,
            "time_violation": self.time_violation,

            "fitness": self.fitness,
            "penalty": self.penalty,

            "bks_vehicles": self.bks_vehicles,
            "bks_distance": self.bks_distance,
            "gap_bks": self.gap_bks,

            "iteration": self.iteration,
            "phase": self.phase,
            "timestamp": self.timestamp,
            "notes": self.notes,
        }

    # ========================================================
    # Pretty printing
    # ========================================================

    def summary(self) -> str:
        """
        Resumen compacto para consola/logs.
        """
        gap_str = "N/A" if self.gap_bks is None else f"{100*self.gap_bks:.2f}%"
        return (
            f"[{self.instance_id}] "
            f"Alg={self.algorithm_id} | "
            f"V={self.num_vehicles} | "
            f"D={self.total_distance:.2f} | "
            f"Gap={gap_str} | "
            f"Feasible={self.feasible}"
        )
