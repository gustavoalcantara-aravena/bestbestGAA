"""
Operadores de Perturbación para Graph Coloring Problem (GCP)

Estos operadores aplican cambios significativos a la solución para escapar
de óptimos locales en Iterated Local Search:

- RandomRecolor: Cambiar colores de un porcentaje aleatorio de vértices
- PartialDestroy: Destruir una región del grafo y reconstruir

Referencias:
- Lourenço, Martin & Stützle (2003). Iterated Local Search
- Glover & Laguna (1997). Tabu Search
"""

import numpy as np
from typing import Set, List
from core import GraphColoringProblem, ColoringSolution


class RandomRecolor:
    """
    Perturbación: Recolorear Aleatoriamente
    
    Cambia los colores de un porcentaje aleatorio de vértices,
    permitiendo soluciones infactibles (con conflictos).
    
    Ventajas:
    - Simple y rápido
    - Fácil de controlar (parámetro: ratio)
    - Explora el espacio efectivamente
    
    Desventajas:
    - Cambios pueden ser muy grandes
    - Poca correlación con estructura del grafo
    
    Parámetro típico:
    - ratio=0.1-0.2 para perturbaciones suaves
    - ratio=0.3-0.5 para perturbaciones agresivas
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                ratio: float = 0.2, seed: int = None) -> ColoringSolution:
        """
        Perturbar solución recoloreando vértices aleatoriamente.
        
        Algoritmo:
        1. Seleccionar ~ratio * n vértices aleatoriamente
        2. Para cada vértice seleccionado:
           a. Elegir color aleatorio (0 a num_colors)
           b. Asignar a la solución (permitiendo conflictos)
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            ratio: Fracción de vértices a perturbar (0.0 a 1.0)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución perturbada (puede tener conflictos)
        
        Garantías:
            - Solución retornada es válida en estructura (asignación correcta)
            - Puede violar restricciones de no-adyacencia (búsqueda infactible)
        """
        if seed is not None:
            np.random.seed(seed)
        
        perturbed = solution.copy()
        n = problem.n_vertices
        num_to_perturb = max(1, int(ratio * n))
        
        # Seleccionar vértices aleatorios
        vertices_to_perturb = np.random.choice(
            list(range(1, n + 1)),
            size=num_to_perturb,
            replace=False
        )
        
        # Recolorear aleatoriamente
        for vertex in vertices_to_perturb:
            # Nuevo color aleatorio entre 0 y num_colors
            new_color = np.random.randint(0, max(perturbed.num_colors, 1) + 1)
            perturbed.assignment[vertex] = new_color
        
        return perturbed
    
    @staticmethod
    def perturb_proportional(solution: ColoringSolution, 
                            problem: GraphColoringProblem,
                            strength: float = 0.5,
                            seed: int = None) -> ColoringSolution:
        """
        Perturbación proporcional al número de colores.
        
        Usa ratio = strength * num_colors / n para escalar la perturbación.
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            strength: Factor de proporcionalidad (0.0 a 1.0)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución perturbada
        
        Interpretación:
            - strength=0: sin perturbación
            - strength=0.5: perturbar ~50% de los conflictos
            - strength=1.0: perturbar ~100% de los conflictos
        """
        # Calcular ratio basado en número de conflictos
        num_conflicts = solution.num_conflicts(problem)
        ratio = min(strength * (num_conflicts + 1) / max(problem.n_vertices, 1), 1.0)
        
        return RandomRecolor.perturb(solution, problem, ratio=ratio, seed=seed)


class PartialDestroy:
    """
    Perturbación: Destrucción Parcial y Reconstrucción
    
    Selecciona una región del grafo, elimina la coloración en esa región,
    y reconstruye los colores de forma aleatoria.
    
    Ventajas:
    - Respeta la estructura del grafo
    - Cambios más "inteligentes" que random
    - Mantiene coherencia local
    
    Desventajas:
    - Más complejo de implementar
    - Requiere identificar regiones (clustering)
    - Lentitud comparada con RandomRecolor
    
    Usos:
    - Cuando la estructura del grafo es importante
    - Para grafos con estructura clara (clustering)
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                region_size: float = 0.2, seed: int = None) -> ColoringSolution:
        """
        Perturbar solución destruyendo y reconstruyendo una región.
        
        Algoritmo:
        1. Seleccionar región (neighborhood BFS desde vértice aleatorio)
        2. Desasignar colores en la región
        3. Reconstruir colores en la región (greedy o aleatorio)
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            region_size: Tamaño relativo de región a destruir (0.0 a 1.0)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución perturbada con región reconstruida
        """
        if seed is not None:
            np.random.seed(seed)
        
        perturbed = solution.copy()
        n = problem.n_vertices
        
        # Seleccionar vértice inicial aleatorio
        start_vertex = np.random.randint(1, n + 1)
        
        # Encontrar región por BFS
        region = PartialDestroy._find_region_bfs(
            problem, start_vertex, size_ratio=region_size
        )
        
        # Desasignar colores en la región
        for vertex in region:
            del perturbed.assignment[vertex]
        
        # Reconstruir región (greedy: menor color disponible)
        for vertex in sorted(region):
            neighbor_colors = {
                perturbed.assignment[n]
                for n in problem.neighbors(vertex)
                if n in perturbed.assignment
            }
            
            color = 0
            while color in neighbor_colors:
                color += 1
            
            perturbed.assignment[vertex] = color
        
        return perturbed
    
    @staticmethod
    def perturb_random_reconstruction(solution: ColoringSolution,
                                     problem: GraphColoringProblem,
                                     region_size: float = 0.2,
                                     seed: int = None) -> ColoringSolution:
        """
        Destruir región y reconstruir con asignación aleatoria.
        
        Más exploratorio que reconstrucción greedy.
        """
        if seed is not None:
            np.random.seed(seed)
        
        perturbed = solution.copy()
        n = problem.n_vertices
        
        # Seleccionar región
        start_vertex = np.random.randint(1, n + 1)
        region = PartialDestroy._find_region_bfs(problem, start_vertex, region_size)
        
        # Desasignar
        for vertex in region:
            del perturbed.assignment[vertex]
        
        # Reconstruir aleatoriamente
        for vertex in sorted(region):
            num_colors = perturbed.num_colors
            # Preferencia por colores existentes
            if np.random.random() < 0.7 and num_colors > 0:
                color = np.random.randint(0, num_colors)
            else:
                color = num_colors  # Nuevo color
            perturbed.assignment[vertex] = color
        
        return perturbed
    
    @staticmethod
    def _find_region_bfs(problem: GraphColoringProblem, start_vertex: int,
                        size_ratio: float = 0.2) -> Set[int]:
        """
        Encontrar región del grafo usando BFS desde un vértice.
        
        Parámetros:
            problem: Instancia GCP
            start_vertex: Vértice inicial
            size_ratio: Tamaño objetivo de la región como fracción de n
        
        Retorna:
            Set[int]: Vértices en la región
        """
        target_size = max(1, int(size_ratio * problem.n_vertices))
        region = {start_vertex}
        queue = [start_vertex]
        
        while queue and len(region) < target_size:
            v = queue.pop(0)
            
            for neighbor in problem.neighbors(v):
                if neighbor not in region:
                    region.add(neighbor)
                    queue.append(neighbor)
                    
                    if len(region) >= target_size:
                        break
        
        return region


class AdaptivePerturbation:
    """
    Perturbación Adaptativa: Ajusta la intensidad según el estado de búsqueda.
    
    Idea: Perturbar menos cuando se mejora rápidamente, perturbar más
    cuando se estanca.
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                improvement_history: List[float], seed: int = None) -> ColoringSolution:
        """
        Perturbar con intensidad adaptativa.
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            improvement_history: Últimas mejoras (últimos 10-20 pasos)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución perturbada con intensidad adaptativa
        """
        # Calcular estancamiento
        if len(improvement_history) < 5:
            stagnation = 0.0
        else:
            recent_improvements = improvement_history[-5:]
            stagnation = 1.0 - (sum(recent_improvements) / max(len(recent_improvements), 1))
        
        # Escalar ratio según estancamiento
        ratio = 0.1 + stagnation * 0.3  # Entre 0.1 y 0.4
        
        return RandomRecolor.perturb(solution, problem, ratio=ratio, seed=seed)


if __name__ == "__main__":
    from core import GraphColoringProblem, ColoringEvaluator
    from operators.constructive import GreedyDSATUR
    
    # Cargar instancia
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    
    # Solución base
    solution = GreedyDSATUR.construct(problem)
    print(f"Solución original: {solution.num_colors} colores, "
          f"{solution.num_conflicts(problem)} conflictos\n")
    
    # Perturbación 1: Random Recolor
    perturbed1 = RandomRecolor.perturb(solution, problem, ratio=0.3)
    print(f"RandomRecolor (30%): {perturbed1.num_colors} colores, "
          f"{perturbed1.num_conflicts(problem)} conflictos")
    
    # Perturbación 2: Partial Destroy
    perturbed2 = PartialDestroy.perturb(solution, problem, region_size=0.3)
    print(f"PartialDestroy (30%): {perturbed2.num_colors} colores, "
          f"{perturbed2.num_conflicts(problem)} conflictos")
    
    # Perturbación 3: Adaptive
    history = [0, 0.5, 0.3, 0.1, 0, 0, 0]
    perturbed3 = AdaptivePerturbation.perturb(solution, problem, history)
    print(f"AdaptivePerturbation: {perturbed3.num_colors} colores, "
          f"{perturbed3.num_conflicts(problem)} conflictos")
