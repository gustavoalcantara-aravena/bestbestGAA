"""
Improvement operators for Graph Coloring

Operadores que mejoran soluciones existentes mediante busqueda local.
"""

from typing import Optional, Tuple
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class KempeChainMove:
    """
    Kempe Chain interchange move
    
    Un movimiento de Kempe Chain intercambia dos colores en componentes conexas
    del subgrafo inducido por esos dos colores.
    
    Casos:
    1. Si el componente contiene el vertex objetivo, reduce conflictos
    2. Si no, puede buscar oportunidades de compactacion
    
    Ventajas:
    - Fundamentado teoricamente
    - Puede eliminar conflictos para infeasible->feasible
    """
    
    @staticmethod
    def apply(solution: ColoringSolution, problem: GraphColoringProblem,
              vertex: int, new_color: int) -> Optional[ColoringSolution]:
        """
        Aplica movimiento de Kempe Chain
        
        Args:
            solution: Solucion actual
            problem: Instancia del problema
            vertex: Vertice a mover
            new_color: Nuevo color a intentar
        
        Returns:
            Solucion mejorada o None si no es factible
        """
        # Si el vertex ya tiene ese color, no hay cambio
        if solution.assignment[vertex] == new_color:
            return None
        
        old_color = solution.assignment[vertex]
        
        # Crear copia y hacer el intercambio
        new_assignment = solution.assignment.copy()
        new_assignment[vertex] = new_color
        
        # Aplicar Kempe Chain interchange en el subgrafo {old_color, new_color}
        swapped = {vertex}
        stack = list(problem.get_neighbors(vertex))
        
        while stack:
            v = stack.pop()
            if v in swapped:
                continue
            
            # Si v tiene color old_color, intercambiarlo con new_color
            if new_assignment[v] == old_color:
                new_assignment[v] = new_color
                swapped.add(v)
                for neighbor in problem.get_neighbors(v):
                    if neighbor not in swapped and new_assignment[neighbor] in {old_color, new_color}:
                        stack.append(neighbor)
            # Si v tiene color new_color, intercambiarlo con old_color
            elif new_assignment[v] == new_color:
                new_assignment[v] = old_color
                swapped.add(v)
                for neighbor in problem.get_neighbors(v):
                    if neighbor not in swapped and new_assignment[neighbor] in {old_color, new_color}:
                        stack.append(neighbor)
        
        return ColoringSolution(new_assignment, problem)


class OneVertexMove:
    """
    One Vertex Move (OVM)
    
    Intenta asignar a cada vertex el color que minimiza conflictos
    entre sus valores permitidos.
    
    Ventajas:
    - Simple y efectivo
    - Facil de paralelizar
    """
    
    @staticmethod
    def improve(solution: ColoringSolution, problem: GraphColoringProblem,
                max_iterations: int = 100) -> ColoringSolution:
        """
        Mejora solucion usando OVM
        
        Args:
            solution: Solucion inicial
            problem: Instancia del problema
            max_iterations: Iteraciones maximas sin mejora
        
        Returns:
            Solucion mejorada
        """
        best_solution = solution.copy()
        best_fitness = best_solution.fitness()
        
        iterations_without_improvement = 0
        
        while iterations_without_improvement < max_iterations:
            improved = False
            
            # Probar mover cada vertex
            for vertex in range(problem.vertices):
                available_colors = best_solution.get_available_colors(vertex)
                
                # Probar cada color disponible
                for color in available_colors:
                    candidate = OneVertexMove.apply(best_solution, problem, vertex, color)
                    if candidate is not None:
                        candidate_fitness = candidate.fitness()
                        
                        if candidate_fitness < best_fitness:
                            best_solution = candidate
                            best_fitness = candidate_fitness
                            improved = True
                            iterations_without_improvement = 0
            
            if not improved:
                iterations_without_improvement += 1
        
        return best_solution
    
    @staticmethod
    def apply(solution: ColoringSolution, problem: GraphColoringProblem,
              vertex: int, color: int) -> Optional[ColoringSolution]:
        """
        Aplica un movimiento de un vertex
        
        Args:
            solution: Solucion actual
            problem: Instancia del problema
            vertex: Vertice a mover
            color: Nuevo color
        
        Returns:
            Solucion con el cambio aplicado
        """
        new_assignment = solution.assignment.copy()
        old_color = new_assignment[vertex]
        
        if old_color == color:
            return None
        
        new_assignment[vertex] = color
        return ColoringSolution(new_assignment, problem)


class TabuColMove:
    """
    Tabu Coloring Move
    
    Mantiene lista tabu de movimientos recientes para escapar de optimos locales.
    
    Ventajas:
    - Evita ciclos
    - Permite movimientos que empeoran temporalmente la solucion
    """
    
    def __init__(self, tabu_tenure: int = 10):
        """
        Inicializa Tabu Search
        
        Args:
            tabu_tenure: Numero de iteraciones para marcar como tabu
        """
        self.tabu_tenure = tabu_tenure
        self.tabu_list = {}  # (vertex, color) -> iteracion_expiracion
        self.iteration = 0
    
    def improve(self, solution: ColoringSolution, problem: GraphColoringProblem,
                max_iterations: int = 100) -> ColoringSolution:
        """
        Mejora solucion usando Tabu Search
        
        Args:
            solution: Solucion inicial
            problem: Instancia del problema
            max_iterations: Iteraciones maximas
        
        Returns:
            Mejor solucion encontrada
        """
        best_solution = solution.copy()
        best_fitness = best_solution.fitness()
        current_solution = solution.copy()
        current_fitness = current_solution.fitness()
        
        for iteration in range(max_iterations):
            self.iteration = iteration
            
            # Encontrar mejor movimiento no tabu (o tabu si aspira)
            candidates = []
            
            for vertex in range(problem.vertices):
                for color in range(problem.num_colors):
                    # Saltar si el vertex ya tiene ese color
                    if current_solution.assignment[vertex] == color:
                        continue
                    
                    # Verificar si movimiento es tabu
                    move_key = (vertex, color)
                    is_tabu = move_key in self.tabu_list and \
                              self.tabu_list[move_key] > iteration
                    
                    # Aplicar movimiento
                    new_assignment = current_solution.assignment.copy()
                    new_assignment[vertex] = color
                    candidate = ColoringSolution(new_assignment, problem)
                    candidate_fitness = candidate.fitness()
                    
                    # Aspiration criteria: si es mejor que best_solution, ignorar tabu
                    if is_tabu and candidate_fitness >= best_fitness:
                        continue
                    
                    candidates.append((candidate_fitness, candidate, vertex, color))
            
            if not candidates:
                break
            
            # Seleccionar mejor candidato
            candidates.sort()
            _, current_solution, best_vertex, best_color = candidates[0]
            current_fitness = current_solution.fitness()
            
            # Marcar movimiento como tabu
            move_key = (best_vertex, best_color)
            self.tabu_list[move_key] = iteration + self.tabu_tenure
            
            # Actualizar mejor solucion global
            if current_fitness < best_fitness:
                best_solution = current_solution.copy()
                best_fitness = current_fitness
        
        return best_solution
