"""
Constructive operators for Graph Coloring

Operadores que generan soluciones iniciales a partir de cero.
"""

from typing import Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class GreedyDSATUR:
    """
    Greedy Degree of Saturation (DSATUR) coloring
    
    Algoritmo de Brelaz (1979) que ordena vertices por grado de saturacion
    (numero de colores distintos en sus vecinos).
    
    Ventajas:
    - Produce soluciones de buena calidad
    - Rapido O(n^2)
    - Deterministico
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: Optional[int] = None) -> ColoringSolution:
        """
        Construye una solucion usando DSATUR
        
        Args:
            problem: Instancia del problema
            seed: Semilla para reproducibilidad
        
        Returns:
            ColoringSolution: Solucion construida
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.vertices
        assignment = np.full(n, -1, dtype=int)
        
        # Calcular grado de saturacion inicial (0 para todos)
        saturation_degree = np.zeros(n, dtype=int)
        colors_used = set()
        next_color = 0
        
        # Seleccionar vertex con mayor grado para empezar
        vertex = np.argmax([problem.get_degree(v) for v in range(n)])
        
        # Asignar primer color al vertex seleccionado
        assignment[vertex] = 0
        colors_used.add(0)
        next_color = 1
        
        # Actualizar grado de saturacion de vecinos
        for neighbor in problem.get_neighbors(vertex):
            saturation_degree[neighbor] += 1
        
        # Colorear resto de vertices
        colored = 1
        while colored < n:
            # Seleccionar vertex no coloreado con mayor grado de saturacion
            # (desempate por grado del grafo)
            candidates = [(saturation_degree[v], problem.get_degree(v), v) 
                         for v in range(n) if assignment[v] == -1]
            candidates.sort(reverse=True)
            vertex = candidates[0][2]
            
            # Encontrar color minimo disponible
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(vertex):
                if assignment[neighbor] != -1:
                    forbidden_colors.add(assignment[neighbor])
            
            # Asignar color minimo disponible
            color = 0
            while color in forbidden_colors:
                color += 1
            
            assignment[vertex] = color
            colors_used.add(color)
            next_color = max(next_color, color + 1)
            colored += 1
            
            # Actualizar grado de saturacion de vecinos no coloreados
            for neighbor in problem.get_neighbors(vertex):
                if assignment[neighbor] == -1:
                    saturation_degree[neighbor] += 1
        
        return ColoringSolution(assignment, problem)


class GreedyLargestFirst:
    """
    Greedy Largest First (LF) coloring
    
    Ordena vertices por grado decreciente y asigna colores greedy.
    
    Ventajas:
    - Simple y rapido
    - Funciona bien para muchos casos
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: Optional[int] = None) -> ColoringSolution:
        """
        Construye una solucion usando Largest First
        
        Args:
            problem: Instancia del problema
            seed: Semilla para reproducibilidad
        
        Returns:
            ColoringSolution: Solucion construida
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.vertices
        assignment = np.full(n, -1, dtype=int)
        
        # Ordenar vertices por grado decreciente
        vertices_by_degree = sorted(
            range(n),
            key=lambda v: problem.get_degree(v),
            reverse=True
        )
        
        # Colorear vertices en orden
        for vertex in vertices_by_degree:
            # Encontrar color minimo disponible
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(vertex):
                if assignment[neighbor] != -1:
                    forbidden_colors.add(assignment[neighbor])
            
            # Asignar color minimo disponible
            color = 0
            while color in forbidden_colors:
                color += 1
            
            assignment[vertex] = color
        
        return ColoringSolution(assignment, problem)


class RandomSequential:
    """
    Random Sequential coloring
    
    Asigna colores a vertices en orden aleatorio.
    
    Ventajas:
    - Diversidad: diferentes semillas dan diferentes soluciones
    - Rapido
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: Optional[int] = None) -> ColoringSolution:
        """
        Construye una solucion usando Random Sequential
        
        Args:
            problem: Instancia del problema
            seed: Semilla para reproducibilidad
        
        Returns:
            ColoringSolution: Solucion construida
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.vertices
        assignment = np.full(n, -1, dtype=int)
        
        # Orden aleatorio de vertices
        vertices_order = np.random.permutation(n)
        
        # Colorear vertices en orden aleatorio
        for vertex in vertices_order:
            # Encontrar color minimo disponible
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(vertex):
                if assignment[neighbor] != -1:
                    forbidden_colors.add(assignment[neighbor])
            
            # Asignar color minimo disponible
            color = 0
            while color in forbidden_colors:
                color += 1
            
            assignment[vertex] = color
        
        return ColoringSolution(assignment, problem)
