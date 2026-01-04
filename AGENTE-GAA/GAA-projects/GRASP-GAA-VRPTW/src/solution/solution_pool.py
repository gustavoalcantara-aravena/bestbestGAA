"""
============================================================
Solution Pool
VRPTW - GRASP + GAA
============================================================

Este módulo define el contenedor global de soluciones.

Responsabilidades:
- Almacenar soluciones generadas
- Mantener el mejor global y por instancia
- Facilitar ranking, filtrado y análisis
- Servir como memoria compartida para GRASP y GAA
"""

from __future__ import annotations

from typing import List, Dict, Optional
from collections import defaultdict
import copy

from solution.solution_container import Solution


# ============================================================
# SolutionPool
# ============================================================

class SolutionPool:
    """
    Pool de soluciones VRPTW con orden canónico Solomon.
    """

    def __init__(self, max_size: Optional[int] = None):
        """
        :param max_size: Máximo de soluciones almacenadas (None = ilimitado)
        """
        self.max_size = max_size

        # Todas las soluciones
        self.solutions: List[Solution] = []

        # Mejores soluciones por instancia
        self.best_by_instance: Dict[str, Solution] = {}

        # Mejores soluciones por algoritmo
        self.best_by_algorithm: Dict[str, Solution] = {}

        # Conteo por familia
        self.count_by_family: Dict[str, int] = defaultdict(int)

    # ========================================================
    # Inserción
    # ========================================================

    def add(self, solution: Solution) -> None:
        """
        Inserta una solución en el pool y actualiza estadísticas.
        """
        self.solutions.append(solution)

        # Limitar tamaño si corresponde
        if self.max_size is not None and len(self.solutions) > self.max_size:
            self._prune()

        # Actualizar mejor por instancia
        self._update_best_by_instance(solution)

        # Actualizar mejor por algoritmo
        self._update_best_by_algorithm(solution)

        # Contabilizar familia
        self.count_by_family[solution.family] += 1

    # ========================================================
    # Actualizaciones internas
    # ========================================================

    def _update_best_by_instance(self, solution: Solution) -> None:
        instance_id = solution.instance_id

        if instance_id not in self.best_by_instance:
            self.best_by_instance[instance_id] = solution
            return

        if solution.better_than(self.best_by_instance[instance_id]):
            self.best_by_instance[instance_id] = solution

    def _update_best_by_algorithm(self, solution: Solution) -> None:
        algorithm_id = solution.algorithm_id

        if algorithm_id not in self.best_by_algorithm:
            self.best_by_algorithm[algorithm_id] = solution
            return

        if solution.better_than(self.best_by_algorithm[algorithm_id]):
            self.best_by_algorithm[algorithm_id] = solution

    # ========================================================
    # Pruning
    # ========================================================

    def _prune(self) -> None:
        """
        Reduce el pool eliminando las peores soluciones.
        """
        # Orden Solomon (mejores primero)
        self.solutions.sort(key=lambda s: (s.num_vehicles, s.total_distance))
        self.solutions = self.solutions[: self.max_size]

    # ========================================================
    # Consultas
    # ========================================================

    def get_best_overall(self) -> Optional[Solution]:
        """
        Devuelve la mejor solución global.
        """
        if not self.solutions:
            return None

        return min(
            self.solutions,
            key=lambda s: (s.num_vehicles, s.total_distance)
        )

    def get_best_for_instance(self, instance_id: str) -> Optional[Solution]:
        """
        Devuelve la mejor solución para una instancia.
        """
        return self.best_by_instance.get(instance_id)

    def get_best_for_algorithm(self, algorithm_id: str) -> Optional[Solution]:
        """
        Devuelve la mejor solución producida por un algoritmo.
        """
        return self.best_by_algorithm.get(algorithm_id)

    def get_all(self) -> List[Solution]:
        """
        Devuelve todas las soluciones (copia).
        """
        return list(self.solutions)

    def get_feasible(self) -> List[Solution]:
        """
        Devuelve solo soluciones factibles.
        """
        return [s for s in self.solutions if s.feasible]

    def get_infeasible(self) -> List[Solution]:
        """
        Devuelve solo soluciones infactibles.
        """
        return [s for s in self.solutions if not s.feasible]

    # ========================================================
    # Ranking y análisis
    # ========================================================

    def rank_by_instance(self, instance_id: str) -> List[Solution]:
        """
        Ranking Solomon para una instancia específica.
        """
        sols = [s for s in self.solutions if s.instance_id == instance_id]
        return sorted(sols, key=lambda s: (s.num_vehicles, s.total_distance))

    def rank_global(self) -> List[Solution]:
        """
        Ranking Solomon global.
        """
        return sorted(self.solutions, key=lambda s: (s.num_vehicles, s.total_distance))

    # ========================================================
    # Estadísticas
    # ========================================================

    def summary(self) -> Dict[str, int]:
        """
        Resumen rápido del pool.
        """
        return {
            "total_solutions": len(self.solutions),
            "feasible": len(self.get_feasible()),
            "infeasible": len(self.get_infeasible()),
            "instances_covered": len(self.best_by_instance),
            "algorithms": len(self.best_by_algorithm),
        }

    # ========================================================
    # Export
    # ========================================================

    def to_dict(self) -> Dict[str, any]:
        """
        Serializa el pool completo (para reportes).
        """
        return {
            "summary": self.summary(),
            "solutions": [s.to_dict() for s in self.solutions],
        }

    # ========================================================
    # Debug
    # ========================================================

    def __len__(self) -> int:
        return len(self.solutions)

    def __repr__(self) -> str:
        return (
            f"SolutionPool("
            f"solutions={len(self.solutions)}, "
            f"instances={len(self.best_by_instance)}, "
            f"algorithms={len(self.best_by_algorithm)})"
        )
