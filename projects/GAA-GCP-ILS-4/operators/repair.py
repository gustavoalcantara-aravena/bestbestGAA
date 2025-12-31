"""
Operadores de Reparación para Graph Coloring Problem (GCP)

Estos operadores reparan soluciones infactibles (con conflictos) usando
estrategias heurísticas eficientes.

- RepairConflicts: Resolución secuencial de conflictos
- IntensifyColor: Intensificación de un color específico
- Diversify: Diversificación mediante reasignación global
"""

import numpy as np
from typing import Set, Dict
from core import GraphColoringProblem, ColoringSolution


class RepairConflicts:
    """
    Reparación: Resolver Conflictos Secuencialmente
    
    Identifica vértices en conflicto y recolorea usando el menor color
    disponible que no cause conflictos adicionales.
    
    Algoritmo greedy que es muy efectivo cuando hay pocos conflictos.
    
    Ventajas:
    - Muy rápido: O(m) por iteración
    - Efectivo cuando num_conflicts es bajo
    - Mantiene estructura general de solución
    
    Desventajas:
    - Puede converger a óptimos locales
    - Orden de reparación afecta resultado
    """
    
    @staticmethod
    def repair(solution: ColoringSolution, problem: GraphColoringProblem,
               max_iterations: int = 100, seed: int = None) -> ColoringSolution:
        """
        Reparar solución eliminando conflictos.
        
        Algoritmo:
        1. Mientras haya conflictos y iteraciones < max:
           a. Obtener vértices en conflicto
           b. Para cada vértice en conflicto:
              - Asignar menor color que resuelve sus conflictos
              - Si no existe, usar nuevo color
        
        Parámetros:
            solution: Solución potencialmente infactible
            problem: Instancia GCP
            max_iterations: Máximo de reparaciones
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución factible (sin conflictos)
        
        Garantías:
            - Retorna siempre factible (num_conflicts = 0)
            - O(n * m) en peor caso
            - Frecuentemente mucho más rápido
        """
        if seed is not None:
            np.random.seed(seed)
        
        repaired = solution.copy()
        
        for iteration in range(max_iterations):
            conflict_vertices = repaired.conflict_vertices(problem)
            
            if not conflict_vertices:
                break  # Solución es factible
            
            # Ordenar conflictivos por número de conflictos (más conflictivos primero)
            conflicted_with_count = {}
            for vertex in conflict_vertices:
                count = sum(
                    1 for neighbor in problem.neighbors(vertex)
                    if repaired.get_color(vertex) == repaired.get_color(neighbor)
                )
                conflicted_with_count[vertex] = count
            
            vertices_to_repair = sorted(
                conflict_vertices,
                key=lambda v: conflicted_with_count[v],
                reverse=True
            )
            
            # Reparar cada vértice
            for vertex in vertices_to_repair:
                # Colores de vecinos
                neighbor_colors = {
                    repaired.get_color(n) for n in problem.neighbors(vertex)
                }
                
                # Mejor color: que resuelve más conflictos
                best_color = None
                best_conflicts = float('inf')
                
                for color in range(repaired.num_colors + 2):
                    if color not in neighbor_colors:
                        # Evaluar este color
                        old_color = repaired.get_color(vertex)
                        repaired.assignment[vertex] = color
                        
                        # Contar conflictos de este vértice
                        num_conflicts = sum(
                            1 for neighbor in problem.neighbors(vertex)
                            if repaired.get_color(neighbor) == color
                        )
                        
                        if num_conflicts < best_conflicts:
                            best_conflicts = num_conflicts
                            best_color = color
                        
                        repaired.assignment[vertex] = old_color
                
                # Aplicar mejor color
                if best_color is not None:
                    repaired.assignment[vertex] = best_color
        
        return repaired
    
    @staticmethod
    def repair_with_color_reduction(solution: ColoringSolution,
                                   problem: GraphColoringProblem,
                                   max_iterations: int = 100,
                                   seed: int = None) -> ColoringSolution:
        """
        Reparar y simultáneamente reducir número de colores.
        
        Después de reparar conflictos, intenta fusionar colores.
        
        Parámetros:
            solution: Solución potencialmente infactible
            problem: Instancia GCP
            max_iterations: Máximo de reparaciones
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución factible con menos colores
        """
        repaired = RepairConflicts.repair(solution, problem, max_iterations, seed)
        
        # Intentar fusionar colores
        improved = True
        while improved:
            improved = False
            
            for color1 in range(repaired.num_colors):
                for color2 in range(color1 + 1, repaired.num_colors):
                    # Intentar fusionar color2 en color1
                    temp = repaired.copy()
                    
                    for vertex in range(1, problem.n_vertices + 1):
                        if temp.get_color(vertex) == color2:
                            temp.assignment[vertex] = color1
                    
                    if temp.is_feasible(problem):
                        repaired = temp
                        improved = True
                        break
                
                if improved:
                    break
        
        return repaired


class IntensifyColor:
    """
    Intensificación: Concentrar Colores Específicos
    
    Intenta maximizar el uso de ciertos colores reduciendo otros.
    Útil después de reparación para optimización final.
    """
    
    @staticmethod
    def intensify(solution: ColoringSolution, problem: GraphColoringProblem,
                  target_colors: int = None, max_iterations: int = 50,
                  seed: int = None) -> ColoringSolution:
        """
        Intensificar uso de target_colors.
        
        Parámetros:
            solution: Solución factible
            problem: Instancia GCP
            target_colors: Número objetivo de colores (default: num_colors - 1)
            max_iterations: Máximo de intentos
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución mejorada con ≤ target_colors
        """
        if seed is not None:
            np.random.seed(seed)
        
        if target_colors is None:
            target_colors = max(1, solution.num_colors - 1)
        
        current = solution.copy()
        
        for iteration in range(max_iterations):
            if current.num_colors <= target_colors:
                break
            
            # Intentar eliminar un color
            colors_used = set()
            for v in range(1, problem.n_vertices + 1):
                colors_used.add(current.get_color(v))
            
            max_color = max(colors_used)
            
            # Intentar reasignar vértices de max_color a otros
            vertices_with_max = [
                v for v in range(1, problem.n_vertices + 1)
                if current.get_color(v) == max_color
            ]
            
            for vertex in vertices_with_max:
                neighbor_colors = {
                    current.get_color(n) for n in problem.neighbors(vertex)
                }
                
                for color in range(max_color):
                    if color not in neighbor_colors:
                        current.assignment[vertex] = color
                        break
        
        return current


class Diversify:
    """
    Diversificación: Explorar Nuevas Regiones del Espacio
    
    Realiza cambios más drásticos que reparación para alcanzar
    diferentes partes del espacio de búsqueda.
    """
    
    @staticmethod
    def diversify(solution: ColoringSolution, problem: GraphColoringProblem,
                  perturbation_strength: float = 0.5,
                  seed: int = None) -> ColoringSolution:
        """
        Diversificar mediante reasignación aleatoria y reparación.
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            perturbation_strength: Intensidad de cambios (0.0 a 1.0)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución factible pero diferente
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Perturbar aleatoriamente
        perturbed = solution.copy()
        n = problem.n_vertices
        num_to_change = max(1, int(perturbation_strength * n))
        
        vertices_to_change = np.random.choice(
            list(range(1, n + 1)),
            size=num_to_change,
            replace=False
        )
        
        for vertex in vertices_to_change:
            # Asignar color aleatorio
            new_color = np.random.randint(0, solution.num_colors + 1)
            perturbed.assignment[vertex] = new_color
        
        # Reparar conflictos
        return RepairConflicts.repair(perturbed, problem)


if __name__ == "__main__":
    from core import GraphColoringProblem, ColoringEvaluator
    from operators.constructive import GreedyDSATUR, RandomSequential
    
    # Cargar instancia
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    
    # Crear solución infactible
    print("=== Operadores de Reparación ===\n")
    
    infeasible = RandomSequential.construct(problem, seed=42)
    print(f"Solución inicial (posiblemente infactible):")
    print(f"  Colores: {infeasible.num_colors}")
    print(f"  Conflictos: {infeasible.num_conflicts(problem)}")
    print(f"  Factible: {infeasible.is_feasible(problem)}\n")
    
    # Reparar
    repaired = RepairConflicts.repair(infeasible, problem)
    print(f"Después de RepairConflicts:")
    print(f"  Colores: {repaired.num_colors}")
    print(f"  Conflictos: {repaired.num_conflicts(problem)}")
    print(f"  Factible: {repaired.is_feasible(problem)}\n")
    
    # Intensificar
    intensified = IntensifyColor.intensify(repaired, problem, target_colors=4)
    print(f"Después de IntensifyColor (target=4):")
    print(f"  Colores: {intensified.num_colors}")
    print(f"  Conflictos: {intensified.num_conflicts(problem)}")
    print(f"  Factible: {intensified.is_feasible(problem)}")
