"""
Local Search Operators - Mejora de soluciones

Operadores que mejoran soluciones existentes:
1. KempeChain: Intercambiar colores en cadena de Kempe
2. TabuCol: Búsqueda tabu con lista tabu simple
3. OneVertexMove: Reasignar vértice a otro color
4. SwapColors: Intercambiar dos colores globalmente
"""

import numpy as np
from typing import List, Set, Tuple, Optional

try:
    from ..core.solution import ColoringSolution
    from ..core.problem import GraphColoringProblem
except ImportError:
    from core.solution import ColoringSolution
    from core.problem import GraphColoringProblem


class KempeChain:
    """
    Kempe Chain - Operador basado en cadenas de Kempe.
    
    Una cadena de Kempe es una secuencia alternada de aristas
    que conecta dos colores. Intercambiar colores en la cadena
    puede reducir el número de colores.
    """
    
    @staticmethod
    def improve(solution: ColoringSolution,
                problem: GraphColoringProblem,
                max_iterations: int = 100,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Mejora solución usando cadenas de Kempe.
        
        Args:
            solution: Solución inicial
            problem: Instancia del problema
            max_iterations: Número máximo de intentos de mejora
            rng: Generador aleatorio
            
        Returns:
            Solución mejorada
        """
        if rng is None:
            rng = np.random.default_rng()
        
        best_solution = solution.copy()
        best_k = best_solution.num_colors
        
        for iteration in range(max_iterations):
            # Seleccionar dos colores aleatorios
            colors_used = set(c for c in best_solution.coloring if c > 0)
            if len(colors_used) < 2:
                break
            
            colors_list = list(colors_used)
            c1, c2 = rng.choice(colors_list, size=2, replace=False)
            
            # Construir cadena de Kempe
            kempe_chain = KempeChain._build_chain(
                best_solution, problem, c1, c2
            )
            
            # Intercambiar colores en la cadena
            test_solution = best_solution.copy()
            for v in kempe_chain:
                v_idx = v - 1
                if test_solution.coloring[v_idx] == c1:
                    test_solution.coloring[v_idx] = c2
                elif test_solution.coloring[v_idx] == c2:
                    test_solution.coloring[v_idx] = c1
            
            test_solution.clear_cache()
            
            # Aceptar si mejora
            if test_solution.num_colors < best_k:
                best_solution = test_solution
                best_k = best_solution.num_colors
        
        return best_solution
    
    @staticmethod
    def _build_chain(solution: ColoringSolution,
                     problem: GraphColoringProblem,
                     c1: int,
                     c2: int) -> Set[int]:
        """
        Construye cadena de Kempe entre dos colores.
        
        Args:
            solution: Solución actual
            problem: Instancia
            c1, c2: Colores
            
        Returns:
            Conjunto de vértices en la cadena
        """
        chain = set()
        
        # Empezar con un vértice de color c1
        start_vertices = {v + 1 for v, c in enumerate(solution.coloring) 
                         if c == c1}
        
        if not start_vertices:
            return chain
        
        # BFS en el subgrafo de aristas c1-c2
        queue = [next(iter(start_vertices))]
        visited = set(queue)
        
        while queue:
            v = queue.pop(0)
            chain.add(v)
            
            for neighbor in problem.get_neighbors(v):
                if neighbor not in visited:
                    c_neighbor = solution.coloring[neighbor - 1]
                    if c_neighbor in (c1, c2):
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return chain


class TabuCol:
    """
    Tabu Col - Búsqueda tabu para Graph Coloring.
    
    Mantiene lista tabu de movimientos recientes prohibidos.
    Permite movimientos que empeoran la solución si están permitidos
    y no hay mejora disponible.
    """
    
    @staticmethod
    def improve(solution: ColoringSolution,
                problem: GraphColoringProblem,
                max_iterations: int = 1000,
                tabu_tenure: int = 20,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Mejora solución usando búsqueda tabu.
        
        Args:
            solution: Solución inicial
            problem: Instancia
            max_iterations: Máximo de iteraciones
            tabu_tenure: Duración de lista tabu
            rng: Generador aleatorio
            
        Returns:
            Solución mejorada
        """
        if rng is None:
            rng = np.random.default_rng()
        
        current = solution.copy()
        best = current.copy()
        best_k = best.num_colors
        
        tabu_list = {}  # (vertex, color) -> iteration_added
        
        for iteration in range(max_iterations):
            # Generar movimientos vecinos
            neighbors = TabuCol._get_neighbors(current, problem, rng)
            
            if not neighbors:
                break
            
            # Seleccionar mejor movimiento no tabu
            best_neighbor = None
            best_neighbor_k = float('inf')
            
            for neighbor in neighbors:
                k = neighbor.num_colors
                
                # Verificar si está en tabu
                is_tabu = False
                for v_idx, c in enumerate(neighbor.coloring):
                    if c != current.coloring[v_idx]:
                        if (v_idx + 1, c) in tabu_list:
                            if tabu_list[(v_idx + 1, c)] > iteration:
                                is_tabu = True
                                break
                
                # Aceptar si mejora o no está tabu
                if not is_tabu or k < best_k:
                    if k < best_neighbor_k:
                        best_neighbor = neighbor
                        best_neighbor_k = k
            
            if best_neighbor is None:
                break
            
            current = best_neighbor
            
            # Actualizar tabu list
            for v_idx, c in enumerate(current.coloring):
                if c != solution.coloring[v_idx]:
                    tabu_list[(v_idx + 1, c)] = iteration + tabu_tenure
            
            # Actualizar best
            if current.num_colors < best_k:
                best = current.copy()
                best_k = best.num_colors
        
        return best
    
    @staticmethod
    def _get_neighbors(solution: ColoringSolution,
                       problem: GraphColoringProblem,
                       rng: np.random.Generator,
                       sample_size: int = 10) -> List[ColoringSolution]:
        """
        Genera soluciones vecinas (reasignaciones).
        
        Args:
            solution: Solución actual
            problem: Instancia
            rng: Generador aleatorio
            sample_size: Número de vecinos a generar
            
        Returns:
            Lista de soluciones vecinas
        """
        neighbors = []
        
        # Seleccionar vértices aleatorios
        for _ in range(sample_size):
            v = rng.integers(1, problem.n + 1)
            v_idx = v - 1
            
            # Intentar nuevos colores
            forbidden = {solution.coloring[n - 1] for n in problem.get_neighbors(v)
                        if solution.coloring[n - 1] > 0}
            
            # Colores disponibles
            colors_used = set(c for c in solution.coloring if c > 0)
            colors_available = colors_used - forbidden
            
            if not colors_available:
                colors_available.add(max(colors_used) + 1)
            
            for new_color in colors_available:
                neighbor = solution.copy()
                neighbor.coloring[v_idx] = new_color
                neighbor.clear_cache()
                neighbors.append(neighbor)
        
        return neighbors


class OneVertexMove:
    """
    One Vertex Move - Reasignar un vértice a un color diferente.
    
    Operador simple: toma un vértice y lo asigna a otro color
    disponible, priorizando colores que existen vs crear nuevos.
    """
    
    @staticmethod
    def improve(solution: ColoringSolution,
                problem: GraphColoringProblem,
                max_iterations: int = 100,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Mejora solución usando reasignación de vértices.
        
        Args:
            solution: Solución inicial
            problem: Instancia
            max_iterations: Máximo de iteraciones
            rng: Generador aleatorio
            
        Returns:
            Solución mejorada
        """
        if rng is None:
            rng = np.random.default_rng()
        
        best = solution.copy()
        best_k = best.num_colors
        improved = True
        
        iteration = 0
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # Intentar reasignar cada vértice
            for v in range(1, problem.n + 1):
                v_idx = v - 1
                
                # Colores forbididos por vecinos
                forbidden = {best.coloring[n - 1] 
                            for n in problem.get_neighbors(v)
                            if best.coloring[n - 1] > 0}
                
                # Colores disponibles
                colors_used = set(c for c in best.coloring if c > 0)
                colors_available = colors_used - forbidden
                
                # Si hay colores disponibles, intentar reasignar
                if colors_available:
                    for new_color in colors_available:
                        test = best.copy()
                        test.coloring[v_idx] = new_color
                        test.clear_cache()
                        
                        if test.num_colors < best_k:
                            best = test
                            best_k = best.num_colors
                            improved = True
                            break
                
                if improved:
                    break
        
        return best


class SwapColors:
    """
    Swap Colors - Intercambiar dos colores globalmente.
    
    Reemplaza todas las ocurrencias de un color por otro.
    Útil cuando hay colores redundantes.
    """
    
    @staticmethod
    def improve(solution: ColoringSolution,
                problem: GraphColoringProblem,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Intenta eliminar colores inútiles mediante intercambios.
        
        Args:
            solution: Solución inicial
            problem: Instancia
            rng: Generador aleatorio
            
        Returns:
            Solución mejorada
        """
        if rng is None:
            rng = np.random.default_rng()
        
        best = solution.copy()
        best_k = best.num_colors
        
        colors_used = sorted(set(c for c in best.coloring if c > 0))
        
        if len(colors_used) < 2:
            return best
        
        # Intentar intercambiar cada par de colores
        for i, c1 in enumerate(colors_used):
            for c2 in colors_used[i+1:]:
                test = best.copy()
                
                # Intercambiar c1 y c2
                for v_idx in range(len(test.coloring)):
                    if test.coloring[v_idx] == c1:
                        test.coloring[v_idx] = c2
                    elif test.coloring[v_idx] == c2:
                        test.coloring[v_idx] = c1
                
                test.clear_cache()
                
                if test.num_colors < best_k:
                    best = test
                    best_k = best.num_colors
        
        return best


# Factory function
def get_local_search(name: str):
    """
    Retorna clase de operador local search por nombre.
    
    Args:
        name: Nombre del operador (kempe, tabu, ovm, swap)
        
    Returns:
        Clase del operador
    """
    operators = {
        'kempe': KempeChain,
        'kempe_chain': KempeChain,
        'tabu': TabuCol,
        'tabu_col': TabuCol,
        'ovm': OneVertexMove,
        'one_vertex_move': OneVertexMove,
        'swap': SwapColors,
        'swap_colors': SwapColors
    }
    
    name_lower = name.lower().strip()
    if name_lower not in operators:
        raise ValueError(
            f"Operador local search desconocido: {name}. "
            f"Opciones: {list(operators.keys())}"
        )
    
    return operators[name_lower]
