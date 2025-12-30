"""
Repair Operators - Reparar soluciones infactibles

Operadores que convierten soluciones infactibles en factibles:
1. RepairConflicts: Reasignar vértices conflictivos
2. BacktrackRepair: Reconstruir desde cero si hay muchos conflictos
"""

import numpy as np
from typing import Set

try:
    from ..core.solution import ColoringSolution
    from ..core.problem import GraphColoringProblem
except ImportError:
    from core.solution import ColoringSolution
    from core.problem import GraphColoringProblem


class RepairConflicts:
    """
    Repair Conflicts - Reparar asignando vértices conflictivos.
    
    Identifica vértices que causan conflictos y los reasigna
    a colores disponibles sin conflictos.
    """
    
    @staticmethod
    def repair(solution: ColoringSolution,
               problem: GraphColoringProblem,
               rng: np.random.Generator = None) -> ColoringSolution:
        """
        Repara solución infactible asignando vértices conflictivos.
        
        Args:
            solution: Solución posiblemente infactible
            problem: Instancia
            rng: Generador aleatorio
            
        Returns:
            Solución factible
        """
        if rng is None:
            rng = np.random.default_rng()
        
        repaired = solution.copy()
        
        # Iterativamente reparar hasta factible o máximo intentos
        max_iterations = problem.n * 2
        iteration = 0
        
        while not repaired.is_feasible(problem) and iteration < max_iterations:
            iteration += 1
            
            # Encontrar vértices conflictivos
            conflicting = repaired.get_conflicting_vertices(problem)
            
            if not conflicting:
                break
            
            # Seleccionar uno aleatorio
            v = conflicting.pop()
            v_idx = v - 1
            
            # Encontrar color sin conflictos
            forbidden = {repaired.coloring[n - 1]
                        for n in problem.get_neighbors(v)
                        if repaired.coloring[n - 1] > 0}
            
            # Probar colores disponibles
            colors_used = set(c for c in repaired.coloring if c > 0)
            colors_available = sorted(colors_used - forbidden)
            
            if colors_available:
                # Usar primer color disponible
                repaired.coloring[v_idx] = colors_available[0]
            else:
                # Si no hay color disponible, usar nuevo
                new_color = max(colors_used) + 1 if colors_used else 1
                repaired.coloring[v_idx] = new_color
            
            repaired.clear_cache()
        
        return repaired


class BacktrackRepair:
    """
    Backtrack Repair - Reconstruir si hay muchos conflictos.
    
    Si la solución tiene demasiados conflictos, es más eficiente
    reconstruirla desde cero con greedy que reparar.
    """
    
    @staticmethod
    def repair(solution: ColoringSolution,
               problem: GraphColoringProblem,
               conflict_threshold: float = 0.05,
               rng: np.random.Generator = None) -> ColoringSolution:
        """
        Repara solución, reconstruyendo si es necesario.
        
        Args:
            solution: Solución posiblemente infactible
            problem: Instancia
            conflict_threshold: Fracción de aristas en conflicto para reconstruir
            rng: Generador aleatorio
            
        Returns:
            Solución factible
        """
        if rng is None:
            rng = np.random.default_rng()
        
        # Contar conflictos
        conflicts = solution.count_conflicts(problem)
        conflict_fraction = conflicts / problem.m if problem.m > 0 else 0
        
        # Si pocos conflictos, reparar incrementalmente
        if conflict_fraction <= conflict_threshold:
            return RepairConflicts.repair(solution, problem, rng)
        
        # Si muchos conflictos, reconstruir con greedy
        repaired = ColoringSolution.empty(problem.n, problem)
        
        # Reconstruir con greedy ordenado por grado
        vertices_by_degree = sorted(
            range(1, problem.n + 1),
            key=lambda v: problem.get_degree(v),
            reverse=True
        )
        
        for v in vertices_by_degree:
            v_idx = v - 1
            
            # Obtener colores forbididos
            forbidden = {repaired.coloring[n - 1]
                        for n in problem.get_neighbors(v)
                        if repaired.coloring[n - 1] > 0}
            
            # Asignar color más pequeño disponible
            color = 1
            while color in forbidden:
                color += 1
            
            repaired.coloring[v_idx] = color
        
        repaired.problem = problem
        repaired.clear_cache()
        
        return repaired


# Factory function
def get_repair(name: str):
    """
    Retorna clase de operador de reparación por nombre.
    
    Args:
        name: Nombre del operador (repair, backtrack)
        
    Returns:
        Clase del operador
    """
    operators = {
        'repair': RepairConflicts,
        'repair_conflicts': RepairConflicts,
        'backtrack': BacktrackRepair,
        'backtrack_repair': BacktrackRepair
    }
    
    name_lower = name.lower().strip()
    if name_lower not in operators:
        raise ValueError(
            f"Operador de reparación desconocido: {name}. "
            f"Opciones: {list(operators.keys())}"
        )
    
    return operators[name_lower]
