"""
Core module: Graph Coloring Solution representation

Este modulo define la clase ColoringSolution que representa
una solucion (asignacion de colores) a una instancia GCP.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np
from core.problem import GraphColoringProblem


@dataclass
class ColoringSolution:
    """
    Representacion de una solucion para el Graph Coloring Problem
    
    Una solucion es una asignacion de colores a todos los vertices
    del grafo. Los colores se representan con enteros de 0 a k-1,
    donde k es el numero de colores utilizado.
    
    Atributos:
        assignment (np.ndarray): Vector de asignacion [c_0, c_1, ..., c_{n-1}]
                                donde c_i es el color del vertice i
        problem (GraphColoringProblem): Referencia a la instancia del problema
        value (Optional[int]): Cache del numero de colores (k)
    
    Ejemplo:
        >>> problem = GraphColoringProblem(vertices=5, edges=[(0,1), (1,2)])
        >>> assignment = np.array([0, 1, 0, 1, 0])
        >>> solution = ColoringSolution(assignment, problem)
        >>> print(solution.num_colors)
        2
        >>> print(solution.num_conflicts)
        0
        >>> print(solution.is_feasible())
        True
    """
    
    assignment: np.ndarray
    problem: GraphColoringProblem
    value: Optional[int] = field(default=None, init=False)
    
    def __post_init__(self):
        """Validaciones tras inicializacion"""
        # Validar que assignment es numpy array
        if not isinstance(self.assignment, np.ndarray):
            self.assignment = np.array(self.assignment, dtype=int)
        else:
            self.assignment = self.assignment.astype(int)
        
        # Validar longitud
        if len(self.assignment) != self.problem.vertices:
            raise ValueError(
                f"Assignment tiene {len(self.assignment)} elementos, "
                f"pero problema tiene {self.problem.vertices} vertices"
            )
        
        # Validar que todos los colores son no-negativos
        if np.any(self.assignment < 0):
            raise ValueError("Los colores deben ser no-negativos")
        
        # Validar que los colores son consecutivos desde 0
        # Esto es una restriccion razonable para soluciones validas
        max_color = np.max(self.assignment)
        used_colors = set(self.assignment)
        if len(used_colors) != max_color + 1:
            # Renormalizar colores para que sean consecutivos
            color_mapping = {old: new for new, old in enumerate(sorted(used_colors))}
            self.assignment = np.array([color_mapping[c] for c in self.assignment], dtype=int)
    
    @property
    def num_colors(self) -> int:
        """Retorna el numero de colores utilizados en la solucion"""
        return int(np.max(self.assignment)) + 1 if len(self.assignment) > 0 else 0
    
    @property
    def num_conflicts(self) -> int:
        """
        Retorna el numero de conflictos (aristas monocromaticas)
        
        Una arista (u,v) es conflictiva si assignment[u] == assignment[v]
        """
        conflicts = 0
        for u, v in self.problem.edges:
            if self.assignment[u] == self.assignment[v]:
                conflicts += 1
        return conflicts
    
    @property
    def color_classes(self) -> dict:
        """
        Retorna un diccionario con los vertices agrupados por color
        
        Returns:
            dict: {color: [vertices con ese color]}
        """
        classes = {}
        for vertex, color in enumerate(self.assignment):
            color = int(color)
            if color not in classes:
                classes[color] = []
            classes[color].append(vertex)
        return classes
    
    def is_feasible(self) -> bool:
        """
        Verifica si la solucion es factible (sin conflictos)
        
        Una solucion es factible si no hay dos vertices adyacentes
        con el mismo color.
        """
        return self.num_conflicts == 0
    
    def get_conflicting_vertices(self) -> set:
        """
        Retorna el conjunto de vertices que participan en conflictos
        
        Returns:
            set: Vertices involucrados en aristas monocromaticas
        """
        conflicting = set()
        for u, v in self.problem.edges:
            if self.assignment[u] == self.assignment[v]:
                conflicting.add(u)
                conflicting.add(v)
        return conflicting
    
    def get_conflicting_neighbors(self, vertex: int) -> set:
        """
        Retorna los vecinos del vertice que tienen el mismo color
        
        Args:
            vertex: Indice del vertice
        
        Returns:
            set: Vecinos con el mismo color que el vertice
        """
        if not (0 <= vertex < self.problem.vertices):
            raise ValueError(f"Vertice {vertex} fuera de rango")
        
        color = self.assignment[vertex]
        conflicting_neighbors = set()
        for neighbor in self.problem.get_neighbors(vertex):
            if self.assignment[neighbor] == color:
                conflicting_neighbors.add(neighbor)
        return conflicting_neighbors
    
    def get_available_colors(self, vertex: int) -> set:
        """
        Retorna los colores disponibles para un vertice
        (colores no utilizados por sus vecinos)
        
        Args:
            vertex: Indice del vertice
        
        Returns:
            set: Colores que pueden asignarse al vertice sin crear conflictos
        """
        if not (0 <= vertex < self.problem.vertices):
            raise ValueError(f"Vertice {vertex} fuera de rango")
        
        # Colores prohibidos (utilizados por vecinos)
        prohibited = set()
        for neighbor in self.problem.get_neighbors(vertex):
            prohibited.add(int(self.assignment[neighbor]))
        
        # Colores disponibles son todos excepto los prohibidos
        all_colors = set(range(self.num_colors))
        available = all_colors - prohibited
        
        # Siempre es posible usar un color nuevo
        available.add(self.num_colors)
        
        return available
    
    def copy(self) -> "ColoringSolution":
        """
        Crea una copia profunda de la solucion
        
        Returns:
            ColoringSolution: Nueva instancia con asignacion copiada
        """
        return ColoringSolution(
            assignment=self.assignment.copy(),
            problem=self.problem
        )
    
    def fitness(self, penalty_weight: int = 100) -> float:
        """
        Calcula el fitness de la solucion
        
        fitness = num_colors + penalty_weight * num_conflicts
        
        Args:
            penalty_weight: Peso de penalizacion por conflictos
        
        Returns:
            float: Valor de fitness
        """
        return self.num_colors + penalty_weight * self.num_conflicts
    
    def to_dict(self) -> dict:
        """Serializa la solucion a diccionario"""
        return {
            'assignment': self.assignment.tolist(),
            'num_colors': self.num_colors,
            'num_conflicts': self.num_conflicts,
            'is_feasible': self.is_feasible(),
            'fitness': self.fitness(),
            'color_classes': self.color_classes
        }
    
    def __str__(self) -> str:
        """Representacion en string"""
        status = "FACTIBLE" if self.is_feasible() else "INFACTIBLE"
        return (
            f"ColoringSolution("
            f"colors={self.num_colors}, "
            f"conflicts={self.num_conflicts}, "
            f"status={status})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
