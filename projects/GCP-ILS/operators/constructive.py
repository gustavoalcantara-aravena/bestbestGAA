"""
Constructive Operators - Heurísticas constructivas para Graph Coloring

Operadores que crean soluciones iniciales:
1. GreedyDSATUR: Ordenar por saturation degree (más restringidos primero)
2. GreedyLargestFirst (LF): Ordenar por grado (vértices con más vecinos primero)
3. RandomSequential: Orden aleatorio
4. GreedySmallestLast (SL): Ordenar por grado (vértices con menos vecinos último)
5. RLF (Recursive Large First): Variante de LF con selección aleatoria
"""

import numpy as np
from typing import List, Tuple
from ..core.solution import ColoringSolution
from ..core.problem import GraphColoringProblem


class GreedyDSATUR:
    """
    DSATUR (Degree of Saturation) - Heurística de Brooks.
    
    Ordena vértices por:
    1. Saturation Degree (número de colores vecinos distintos) - DESC
    2. Grado (número de vecinos) - DESC como desempate
    
    Asigna el color más pequeño disponible a cada vértice.
    """
    
    @staticmethod
    def build(problem: GraphColoringProblem, 
              rng: np.random.Generator = None) -> ColoringSolution:
        """
        Construye solución usando DSATUR.
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio (no usado en DSATUR puro)
            
        Returns:
            ColoringSolution factible
        """
        n = problem.n
        coloring = [0] * n  # 0-indexed
        
        # Asignar color 1 al primer vértice
        coloring[0] = 1
        
        # Procesar vértices restantes
        for _ in range(n - 1):
            # Encontrar vértice sin color con máximo saturation degree
            best_vertex = -1
            max_saturation = -1
            max_degree = -1
            
            for v in range(n):
                if coloring[v] == 0:  # Sin color
                    saturation = problem.get_saturation_degree(coloring, v + 1)
                    degree = problem.get_degree(v + 1)
                    
                    # Máximo saturation, con desempate por grado
                    if (saturation > max_saturation or 
                        (saturation == max_saturation and degree > max_degree)):
                        best_vertex = v
                        max_saturation = saturation
                        max_degree = degree
            
            # Asignar color más pequeño disponible
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(best_vertex + 1):
                if coloring[neighbor - 1] > 0:
                    forbidden_colors.add(coloring[neighbor - 1])
            
            # Encontrar primer color disponible
            color = 1
            while color in forbidden_colors:
                color += 1
            
            coloring[best_vertex] = color
        
        return ColoringSolution(n=n, coloring=coloring, problem=problem)


class GreedyLargestFirst:
    """
    Largest First (LF) - Greedy por grado decreciente.
    
    Ordena vértices por grado (mayor primero).
    Asigna color disponible más pequeño a cada vértice.
    """
    
    @staticmethod
    def build(problem: GraphColoringProblem,
              rng: np.random.Generator = None) -> ColoringSolution:
        """
        Construye solución usando Largest First.
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio (no usado en LF puro)
            
        Returns:
            ColoringSolution factible
        """
        n = problem.n
        coloring = [0] * n
        
        # Ordenar vértices por grado decreciente
        vertices_sorted = sorted(
            range(1, n + 1),
            key=lambda v: problem.get_degree(v),
            reverse=True
        )
        
        # Colorear en orden
        for v in vertices_sorted:
            v_idx = v - 1
            
            # Encontrar colores forbididos por vecinos
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(v):
                if coloring[neighbor - 1] > 0:
                    forbidden_colors.add(coloring[neighbor - 1])
            
            # Asignar primer color disponible
            color = 1
            while color in forbidden_colors:
                color += 1
            
            coloring[v_idx] = color
        
        return ColoringSolution(n=n, coloring=coloring, problem=problem)


class GreedySmallestLast:
    """
    Smallest Last (SL) - Greedy por grado creciente.
    
    Ordena vértices al revés (los de menor grado al final).
    Asigna colores de menor a mayor.
    """
    
    @staticmethod
    def build(problem: GraphColoringProblem,
              rng: np.random.Generator = None) -> ColoringSolution:
        """
        Construye solución usando Smallest Last.
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio (no usado en SL puro)
            
        Returns:
            ColoringSolution factible
        """
        n = problem.n
        coloring = [0] * n
        
        # Ordenar vértices por grado creciente (smallest last)
        vertices_sorted = sorted(
            range(1, n + 1),
            key=lambda v: problem.get_degree(v),
            reverse=False  # Creciente = smallest last
        )
        
        # Colorear en orden inverso (los de mayor grado primero)
        for v in reversed(vertices_sorted):
            v_idx = v - 1
            
            # Encontrar colores forbididos
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(v):
                if coloring[neighbor - 1] > 0:
                    forbidden_colors.add(coloring[neighbor - 1])
            
            # Asignar primer color disponible
            color = 1
            while color in forbidden_colors:
                color += 1
            
            coloring[v_idx] = color
        
        return ColoringSolution(n=n, coloring=coloring, problem=problem)


class RandomSequential:
    """
    Random Sequential (RS) - Greedy con orden aleatorio.
    
    Ordena vértices aleatoriamente.
    Asigna color disponible más pequeño a cada vértice.
    """
    
    @staticmethod
    def build(problem: GraphColoringProblem,
              rng: np.random.Generator = None) -> ColoringSolution:
        """
        Construye solución usando orden aleatorio.
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio
            
        Returns:
            ColoringSolution factible
        """
        if rng is None:
            rng = np.random.default_rng()
        
        n = problem.n
        coloring = [0] * n
        
        # Orden aleatorio
        vertices_order = list(range(1, n + 1))
        rng.shuffle(vertices_order)
        
        # Colorear en orden
        for v in vertices_order:
            v_idx = v - 1
            
            # Encontrar colores forbididos
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(v):
                if coloring[neighbor - 1] > 0:
                    forbidden_colors.add(coloring[neighbor - 1])
            
            # Asignar primer color disponible
            color = 1
            while color in forbidden_colors:
                color += 1
            
            coloring[v_idx] = color
        
        return ColoringSolution(n=n, coloring=coloring, problem=problem)


class RLF:
    """
    Recursive Large First (RLF) - Variante de LF con selección aleatoria.
    
    Similar a LF pero con elemento de aleatoriedad en la selección.
    Útil para generar diversidad en múltiples ejecuciones.
    """
    
    @staticmethod
    def build(problem: GraphColoringProblem,
              rng: np.random.Generator = None,
              alpha: float = 0.2) -> ColoringSolution:
        """
        Construye solución usando RLF.
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio
            alpha: Parámetro de aleatoriedad (0=determinístico, 1=aleatorio)
                  Selecciona del top-alpha% de vértices por grado
            
        Returns:
            ColoringSolution factible
        """
        if rng is None:
            rng = np.random.default_rng()
        
        n = problem.n
        coloring = [0] * n
        uncolored = set(range(1, n + 1))
        
        while uncolored:
            # Ordenar uncolored por grado (en el subgrafo inducido)
            degrees_in_subgraph = []
            for v in uncolored:
                # Contar vecinos aún sin color
                neighbors_uncolored = len(
                    problem.get_neighbors(v) & uncolored
                )
                degrees_in_subgraph.append((v, neighbors_uncolored))
            
            degrees_in_subgraph.sort(key=lambda x: x[1], reverse=True)
            
            # Seleccionar vértices candidatos (top-alpha%)
            k = max(1, int(len(degrees_in_subgraph) * alpha))
            candidates = [v for v, _ in degrees_in_subgraph[:k]]
            
            # Seleccionar aleatoriamente del top
            v = candidates[rng.integers(0, len(candidates))]
            v_idx = v - 1
            
            # Asignar color
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(v):
                if coloring[neighbor - 1] > 0:
                    forbidden_colors.add(coloring[neighbor - 1])
            
            color = 1
            while color in forbidden_colors:
                color += 1
            
            coloring[v_idx] = color
            uncolored.remove(v)
        
        return ColoringSolution(n=n, coloring=coloring, problem=problem)


# Factory function
def get_constructive(name: str):
    """
    Retorna clase de operador constructivo por nombre.
    
    Args:
        name: Nombre del operador (dsatur, lf, sl, rs, rlf)
        
    Returns:
        Clase del operador
    """
    constructives = {
        'dsatur': GreedyDSATUR,
        'lf': GreedyLargestFirst,
        'largest_first': GreedyLargestFirst,
        'sl': GreedySmallestLast,
        'smallest_last': GreedySmallestLast,
        'rs': RandomSequential,
        'random_sequential': RandomSequential,
        'rlf': RLF,
        'recursive_large_first': RLF
    }
    
    name_lower = name.lower().strip()
    if name_lower not in constructives:
        raise ValueError(
            f"Operador constructivo desconocido: {name}. "
            f"Opciones: {list(constructives.keys())}"
        )
    
    return constructives[name_lower]
