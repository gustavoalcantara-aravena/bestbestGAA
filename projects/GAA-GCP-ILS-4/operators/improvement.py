"""
Operadores de Mejora para Graph Coloring Problem (GCP)

Este módulo implementa búsqueda local (movimientos) para mejorar soluciones
existentes mediante modificaciones locales:
- KempeChain: Intercambios generalizados usando cadenas de Kempe
- OneVertexMove: Cambio simple de color de un vértice
- TabuCol: Variante con memoria tabú para evitar ciclos

Referencias:
- Kempe, A. B. (1879). On the geographical problem of four colours
- Hertz, A., & de Werra, D. (1987). Using Tabu Search Techniques
- Galinier & Hao (2006). Hybrid evolutionary algorithms for graph coloring
"""

import numpy as np
from typing import Set, Dict, List, Tuple, Optional
from core import GraphColoringProblem, ColoringSolution


class KempeChain:
    """
    Movimiento mediante Cadenas de Kempe
    
    Una cadena de Kempe es un camino alternante máximo entre dos colores.
    Este movimiento intercambia colores a lo largo de la cadena.
    
    Ejemplo:
    - Solución inicial: v1→0, v2→1, v3→0, v4→1 (con conflicto v1-v2)
    - Cadena 0-1 alternante: {v1, v3} ↔ {v2, v4}
    - Intercambio: v1→1, v2→0, v3→1, v4→0
    
    Ventajas:
    - Movimientos más potentes que OneVertexMove
    - Puede resolver conflictos locales
    - Exploración más profunda del espacio
    
    Desventajas:
    - Más computacionalmente costoso: O(n + m) por movimiento
    - No garantiza mejora en cada paso
    """
    
    @staticmethod
    def improve(solution: ColoringSolution, problem: GraphColoringProblem,
                max_iterations: int = 100, seed: int = None) -> ColoringSolution:
        """
        Mejora solución mediante búsqueda local con cadenas de Kempe.
        
        Algoritmo:
        1. Mientras no se cumpla criterio de parada:
           a. Para cada vértice en conflicto (si hay):
              - Enumerar cadenas de Kempe potenciales
              - Evaluar intercambios
              - Aplicar si mejora
           b. Si no hay mejora, parar
        
        Parámetros:
            solution: Solución inicial
            problem: Instancia GCP
            max_iterations: Máximo número de iteraciones
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución mejorada (mejor o igual)
        
        Garantías:
            - Solución retornada es al menos tan buena como entrada
            - Búsqueda local: no hay movimiento mejora desde resultado
        """
        if seed is not None:
            np.random.seed(seed)
        
        current = solution.copy()
        improved = True
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # Obtener vértices en conflicto
            conflict_vertices = current.conflict_vertices(problem)
            
            if not conflict_vertices:
                break  # Solución es factible
            
            # Probar mejoras con cadenas de Kempe
            best_move = None
            best_improvement = 0
            
            for vertex in conflict_vertices:
                current_color = current.get_color(vertex)
                neighbors = problem.neighbors(vertex)
                neighbor_colors = {current.get_color(n) for n in neighbors}
                
                # Enumerar cadenas de Kempe
                for target_color in neighbor_colors:
                    # Encontrar cadena alternante
                    chain = KempeChain._find_chain(
                        current, problem, vertex, current_color, target_color
                    )
                    
                    if chain:
                        # Evaluar movimiento
                        temp_solution = current.copy()
                        KempeChain._swap_chain_colors(
                            temp_solution, chain, current_color, target_color
                        )
                        
                        # Calcular mejora
                        improvement = (current.num_conflicts(problem) - 
                                     temp_solution.num_conflicts(problem))
                        
                        if improvement > best_improvement:
                            best_improvement = improvement
                            best_move = (chain, current_color, target_color)
            
            # Aplicar mejor movimiento si lo hay
            if best_move is not None:
                chain, color_a, color_b = best_move
                KempeChain._swap_chain_colors(current, chain, color_a, color_b)
                improved = True
        
        return current
    
    @staticmethod
    def _find_chain(solution: ColoringSolution, problem: GraphColoringProblem,
                    start_vertex: int, color_a: int, color_b: int) -> Set[int]:
        """
        Encontrar cadena de Kempe máxima alternante entre dos colores.
        
        Una cadena es un conjunto de vértices conectados alternadamente
        entre color_a y color_b.
        
        Parámetros:
            solution: Solución actual
            problem: Instancia GCP
            start_vertex: Vértice inicial (tiene color_a)
            color_a, color_b: Dos colores para alternar
        
        Retorna:
            Set[int]: Vértices que forman la cadena (máxima alcanzable)
        """
        chain = {start_vertex}
        queue = [start_vertex]
        visited = {start_vertex}
        
        while queue:
            v = queue.pop(0)
            current_color = solution.get_color(v)
            next_color = color_b if current_color == color_a else color_a
            
            for neighbor in problem.neighbors(v):
                if neighbor not in visited:
                    if solution.get_color(neighbor) == next_color:
                        visited.add(neighbor)
                        chain.add(neighbor)
                        queue.append(neighbor)
        
        return chain
    
    @staticmethod
    def _swap_chain_colors(solution: ColoringSolution, chain: Set[int],
                          color_a: int, color_b: int) -> None:
        """
        Intercambiar colores en una cadena: color_a ↔ color_b
        
        Modifica la solución in-place.
        """
        for vertex in chain:
            if solution.get_color(vertex) == color_a:
                solution.assignment[vertex] = color_b
            elif solution.get_color(vertex) == color_b:
                solution.assignment[vertex] = color_a


class OneVertexMove:
    """
    Movimiento Simple: Cambiar Color de un Vértice
    
    El movimiento más básico de búsqueda local: cambiar el color de un
    único vértice al menor color disponible.
    
    Complejidad: O(n + m) con evaluación incremental
    
    Ventajas:
    - Simple: fácil de implementar y entender
    - Rápido
    - Movimientos pequeños
    
    Desventajas:
    - Alcanza óptimos locales muy rápidamente
    - Exploración limitada del espacio
    """
    
    @staticmethod
    def improve(solution: ColoringSolution, problem: GraphColoringProblem,
                max_iterations: int = 100, seed: int = None) -> ColoringSolution:
        """
        Mejora solución mediante búsqueda local simple.
        
        Algoritmo:
        1. Mientras no mejore y iteraciones < max:
           a. Para cada vértice:
              - Asignar menor color disponible
              - Si mejora, aplicar y recomenzar
        
        Parámetros:
            solution: Solución inicial
            problem: Instancia GCP
            max_iterations: Máximo de iteraciones
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución mejorada
        """
        if seed is not None:
            np.random.seed(seed)
        
        current = solution.copy()
        improved = True
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # Intentar mejorar cada vértice
            for vertex in range(1, problem.n_vertices + 1):
                # Colores usados por vecinos
                neighbor_colors = {
                    current.get_color(n) 
                    for n in problem.neighbors(vertex)
                }
                
                # Menor color disponible
                best_color = 0
                while best_color in neighbor_colors:
                    best_color += 1
                
                # Aplicar si mejora
                old_color = current.get_color(vertex)
                if best_color < old_color:  # Usa menos colores
                    conflicts_before = current.num_conflicts(problem)
                    current.assignment[vertex] = best_color
                    conflicts_after = current.num_conflicts(problem)
                    
                    if conflicts_after <= conflicts_before:
                        improved = True
                        break
                    else:
                        current.assignment[vertex] = old_color
        
        return current


class TabuCol:
    """
    Búsqueda con Memoria Tabú (Tabu Search)
    
    Extensión de búsqueda local que mantiene una "lista tabú" de
    movimientos recientes para evitar ciclos.
    
    Ventajas:
    - Evita regresar a soluciones recientes
    - Puede escapar de óptimos locales
    - Efectivo para problemas combinatorios duros
    
    Desventajas:
    - Parámetros adicionales (tenure, criterio de aspiración)
    - Más complejo de implementar
    - Overhead computacional
    """
    
    @staticmethod
    def improve(solution: ColoringSolution, problem: GraphColoringProblem,
                max_iterations: int = 100, tenure: int = 10,
                seed: int = None) -> ColoringSolution:
        """
        Mejora solución usando Tabu Search.
        
        Algoritmo:
        1. Inicializar lista tabú vacía
        2. Generar movimientos candidatos
        3. Seleccionar mejor no-tabú (o tabú si cumple aspiración)
        4. Actualizar lista tabú
        5. Repetir hasta criterio de parada
        
        Parámetros:
            solution: Solución inicial
            problem: Instancia GCP
            max_iterations: Máximo iteraciones
            tenure: Tamaño de la lista tabú (en iteraciones)
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Mejor solución encontrada
        """
        if seed is not None:
            np.random.seed(seed)
        
        current = solution.copy()
        best_solution = current.copy()
        best_fitness = current.num_conflicts(problem)
        
        tabu_list: Dict[Tuple[int, int], int] = {}  # (vertex, color) -> iteration
        
        for iteration in range(max_iterations):
            # Generar movimientos candidatos
            candidates = []
            
            for vertex in range(1, problem.n_vertices + 1):
                neighbor_colors = {
                    current.get_color(n) 
                    for n in problem.neighbors(vertex)
                }
                
                for color in range(current.num_colors + 1):
                    if color not in neighbor_colors:
                        old_color = current.get_color(vertex)
                        if color != old_color:
                            candidates.append((vertex, color))
            
            if not candidates:
                break
            
            # Seleccionar mejor candidato no-tabú
            best_candidate = None
            best_candidate_fitness = float('inf')
            
            for vertex, color in candidates:
                move = (vertex, color)
                
                # Verificar si es tabú
                if move in tabu_list and tabu_list[move] > iteration:
                    continue  # Tabú y no cumple aspiración
                
                # Evaluar candidato
                temp = current.copy()
                temp.assignment[vertex] = color
                fitness = temp.num_conflicts(problem)
                
                # Actualizar mejor global
                if fitness < best_fitness:
                    best_solution = temp.copy()
                    best_fitness = fitness
                
                # Actualizar mejor local
                if fitness < best_candidate_fitness:
                    best_candidate = move
                    best_candidate_fitness = fitness
            
            if best_candidate is None:
                break
            
            # Aplicar movimiento y actualizar tabú
            vertex, color = best_candidate
            current.assignment[vertex] = color
            tabu_list[best_candidate] = iteration + tenure
            
            # Limpiar entradas tabú expiradas
            expired = [k for k, v in tabu_list.items() if v <= iteration]
            for k in expired:
                del tabu_list[k]
        
        return best_solution


if __name__ == "__main__":
    from core import GraphColoringProblem, ColoringEvaluator
    from operators.constructive import GreedyDSATUR
    
    # Cargar instancia
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    
    # Solución inicial
    solution = GreedyDSATUR.construct(problem)
    print(f"Solución inicial: {solution.num_colors} colores\n")
    
    # Mejora con KempeChain
    sol_kempe = KempeChain.improve(solution, problem)
    print(f"Después KempeChain: {sol_kempe.num_colors} colores")
    
    # Mejora con OneVertexMove
    sol_ovm = OneVertexMove.improve(solution, problem)
    print(f"Después OneVertexMove: {sol_ovm.num_colors} colores")
    
    # Mejora con Tabu
    sol_tabu = TabuCol.improve(solution, problem, max_iterations=50)
    print(f"Después TabuCol: {sol_tabu.num_colors} colores")
