"""
Repair operators for Graph Coloring

Operadores que reparan soluciones infeasibles (con conflictos).
"""

from typing import Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class GreedyRepair:
    """
    Greedy Repair
    
    Itera sobre vertices con conflictos y reasigna greedy el color minimo.
    
    Ventajas:
    - Efectivo para soluciones casi factibles
    - Rapido O(n*d) donde d es grado maximo
    """
    
    @staticmethod
    def repair(solution: ColoringSolution, problem: GraphColoringProblem,
               max_iterations: int = 100) -> ColoringSolution:
        """
        Repara solucion infeasible
        
        Args:
            solution: Solucion a reparar (puede tener conflictos)
            problem: Instancia del problema
            max_iterations: Iteraciones maximas
        
        Returns:
            Solucion factible (si es posible)
        """
        current_solution = solution.copy()
        
        for _ in range(max_iterations):
            # Obtener vertices con conflictos
            conflicting = current_solution.get_conflicting_vertices()
            
            if len(conflicting) == 0:
                # Solucion ya es factible
                return current_solution
            
            # Reasignar cada vertex con conflicto
            for vertex in conflicting:
                # Encontrar colores prohibidos (vecinos)
                forbidden_colors = set()
                for neighbor in problem.get_neighbors(vertex):
                    if current_solution.assignment[neighbor] != -1:
                        forbidden_colors.add(current_solution.assignment[neighbor])
                
                # Asignar minimo color disponible
                color = 0
                while color in forbidden_colors:
                    color += 1
                
                current_solution.assignment[vertex] = color
        
        return current_solution


class ConflictMinimizingRepair:
    """
    Conflict Minimizing Repair
    
    En lugar de garantizar factibilidad, intenta minimizar conflictos
    permitiendo soluciones parcialmente factibles.
    
    Util cuando factibilidad es dificil de alcanzar.
    """
    
    @staticmethod
    def repair(solution: ColoringSolution, problem: GraphColoringProblem,
               max_iterations: int = 50) -> ColoringSolution:
        """
        Repara minimizando conflictos
        
        Args:
            solution: Solucion a reparar
            problem: Instancia del problema
            max_iterations: Iteraciones maximas
        
        Returns:
            Solucion con conflictos minimizados
        """
        best_solution = solution.copy()
        best_conflicts = best_solution.num_conflicts
        
        for iteration in range(max_iterations):
            improved = False
            
            # Para cada vertex, intentar colores que minimizen conflictos
            for vertex in range(problem.vertices):
                # Obtener colores candidatos (algunos que usan vecinos + nuevos)
                used_colors = set()
                for neighbor in problem.get_neighbors(vertex):
                    used_colors.add(best_solution.assignment[neighbor])
                
                # Intentar colores: vecinos + numero de colores actual
                candidate_colors = list(used_colors) + [best_solution.num_colors]
                
                for color in candidate_colors:
                    test_assignment = best_solution.assignment.copy()
                    test_assignment[vertex] = color
                    test_solution = ColoringSolution(test_assignment, problem)
                    
                    if test_solution.num_conflicts < best_conflicts:
                        best_solution = test_solution
                        best_conflicts = test_solution.num_conflicts
                        improved = True
            
            if not improved:
                break
        
        return best_solution


class ConstraintPropagationRepair:
    """
    Constraint Propagation Repair
    
    Usa constraint propagation para detectar valores forzados.
    Si un vertex solo tiene un color disponible, asignarlo.
    
    Ventajas:
    - Puede detectar soluciones infactibles rapido
    - Efectivo cuando hay restricciones fuertes
    """
    
    @staticmethod
    def repair(solution: ColoringSolution, problem: GraphColoringProblem) -> Optional[ColoringSolution]:
        """
        Repara usando constraint propagation
        
        Args:
            solution: Solucion a reparar
            problem: Instancia del problema
        
        Returns:
            Solucion factible o None si infactible
        """
        assignment = solution.assignment.copy()
        changed = True
        
        while changed:
            changed = False
            
            for vertex in range(problem.vertices):
                available_colors = ColoringSolution(assignment, problem).get_available_colors(vertex)
                
                if len(available_colors) == 0:
                    # Vertex sin colores disponibles: infactible
                    return None
                
                if len(available_colors) == 1:
                    # Solo un color disponible: asignarlo
                    color = available_colors[0]
                    if assignment[vertex] != color:
                        assignment[vertex] = color
                        changed = True
        
        return ColoringSolution(assignment, problem)


class BacktrackingRepair:
    """
    Backtracking Repair
    
    Usa busqueda de backtracking para encontrar una asignacion factible.
    
    Ventajas:
    - Garantiza factibilidad si existe
    - Exponencial pero puede podarse efectivamente
    
    Desventajas:
    - Lento para instancias grandes
    """
    
    @staticmethod
    def repair(solution: ColoringSolution, problem: GraphColoringProblem,
               max_attempts: int = 1000) -> Optional[ColoringSolution]:
        """
        Repara usando backtracking
        
        Args:
            solution: Solucion a reparar
            problem: Instancia del problema
            max_attempts: Limites de intentos
        
        Returns:
            Solucion factible o None
        """
        assignment = solution.assignment.copy()
        
        def backtrack(vertex, attempts):
            if attempts[0] > max_attempts:
                return False
            attempts[0] += 1
            
            if vertex == problem.vertices:
                return True
            
            # Obtener colores disponibles en este estado
            available_colors = set(range(solution.num_colors + 1))
            for neighbor in problem.get_neighbors(vertex):
                if assignment[neighbor] != -1:
                    available_colors.discard(assignment[neighbor])
            
            # Intentar cada color disponible
            for color in sorted(available_colors):
                assignment[vertex] = color
                if backtrack(vertex + 1, attempts):
                    return True
                assignment[vertex] = -1
            
            return False
        
        attempts = [0]
        if backtrack(0, attempts):
            return ColoringSolution(assignment, problem)
        else:
            return None
