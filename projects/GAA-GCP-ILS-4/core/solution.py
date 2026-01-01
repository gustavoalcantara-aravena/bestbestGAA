"""
core/solution.py
Define la clase ColoringSolution para representar soluciones al problema de coloración de grafos.

Proporciona:
    - Almacenamiento de asignación de colores
    - Validación de factibilidad
    - Cálculo de conflictos
    - Propiedades de calidad
"""

from dataclasses import dataclass, field
from typing import Dict, Set, Optional, List
import numpy as np
from core.problem import GraphColoringProblem


@dataclass
class ColoringSolution:
    """
    Representa una solución al problema de coloración de grafos.
    
    Una solución asigna un color a cada vértice del grafo.
    
    Atributos:
        assignment (Dict[int, int]): Mapeo {vértice: color}
                                     donde colores son 0, 1, 2, ...
    
    Ejemplo:
        >>> assignment = {1: 0, 2: 1, 3: 0}  # Vértices 1 y 3 color 0, vértice 2 color 1
        >>> solution = ColoringSolution(assignment=assignment)
        >>> print(f"Colores utilizados: {solution.num_colors}")
        Colores utilizados: 2
    """
    
    assignment: Dict[int, int]
    
    # Propiedades en caché (calculadas una sola vez)
    _num_colors: Optional[int] = field(default=None, init=False, repr=False)
    _color_sets: Optional[Dict[int, Set[int]]] = field(default=None, init=False, repr=False)
    _conflicts_cache: Optional[int] = field(default=None, init=False, repr=False)
    _last_problem_id: Optional[int] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Validar y procesar la asignación después de la construcción."""
        if not self.assignment:
            raise ValueError("Asignación no puede estar vacía")
        
        # Validar que los colores son no-negativos
        # Nota: Aceptamos vértices >= 0 para soportar tanto 0-indexed como 1-indexed
        for vertex, color in self.assignment.items():
            if not isinstance(vertex, int) or vertex < 0:
                raise ValueError(f"Vértice inválido: {vertex}")
            if not isinstance(color, int) or color < 0:
                raise ValueError(f"Color inválido para vértice {vertex}: {color}")
    
    # ========================================================================
    # PROPIEDADES BÁSICAS
    # ========================================================================
    
    @property
    def num_colors(self) -> int:
        """
        Número de colores utilizados en esta solución.
        
        Retorna:
            int: máximo color + 1 (asume colores 0, 1, 2, ...)
        """
        if self._num_colors is None:
            if not self.assignment:
                self._num_colors = 0
            else:
                self._num_colors = max(self.assignment.values()) + 1
        return self._num_colors
    
    @property
    def color_sets(self) -> Dict[int, Set[int]]:
        """
        Agrupación de vértices por color.
        
        Retorna:
            Dict[int, Set[int]]: {color: {vértices con ese color}}
        
        Ejemplo:
            >>> solution = ColoringSolution({1: 0, 2: 1, 3: 0})
            >>> solution.color_sets
            {0: {1, 3}, 1: {2}}
        """
        if self._color_sets is None:
            self._color_sets = {}
            for vertex, color in self.assignment.items():
                if color not in self._color_sets:
                    self._color_sets[color] = set()
                self._color_sets[color].add(vertex)
        return self._color_sets
    
    @property
    def num_vertices(self) -> int:
        """Número de vértices en la solución."""
        return len(self.assignment)
    
    # ========================================================================
    # MÉTODOS DE VALIDACIÓN
    # ========================================================================
    
    def is_feasible(self, problem: GraphColoringProblem) -> bool:
        """
        Verificar si esta solución es factible (respeta restricciones).
        
        Una solución es factible si no hay dos vértices adyacentes con el mismo color.
        
        Parametros:
            problem (GraphColoringProblem): Instancia del problema
        
        Retorna:
            bool: True si la solución es factible, False en otro caso
        
        Ejemplo:
            >>> problem = GraphColoringProblem(3, [(1, 2), (2, 3), (1, 3)])
            >>> solution = ColoringSolution({1: 0, 2: 1, 3: 2})
            >>> solution.is_feasible(problem)
            True
        """
        return self.num_conflicts(problem) == 0
    
    def num_conflicts(self, problem: GraphColoringProblem) -> int:
        """
        Contar número de conflictos (aristas monocromáticas).
        
        Un conflicto es una arista (u, v) donde u y v tienen el mismo color.
        
        Parametros:
            problem (GraphColoringProblem): Instancia del problema
        
        Retorna:
            int: Número de aristas con colores iguales en sus extremos
        """
        # Verificar si el caché es válido (problema no ha cambiado)
        problem_id = id(problem)
        if self._conflicts_cache is not None and self._last_problem_id == problem_id:
            return self._conflicts_cache
        
        conflicts = 0
        for u, v in problem.edges:
            if self.assignment.get(u, -1) == self.assignment.get(v, -1):
                conflicts += 1
        
        # Guardar en caché
        self._conflicts_cache = conflicts
        self._last_problem_id = problem_id
        
        return conflicts
    
    def conflict_vertices(self, problem: GraphColoringProblem) -> Set[int]:
        """
        Obtener conjunto de vértices que están en conflicto (adyacentes a mismo color).
        
        Parametros:
            problem (GraphColoringProblem): Instancia del problema
        
        Retorna:
            Set[int]: Conjunto de vértices en conflicto
        """
        conflicted = set()
        for u, v in problem.edges:
            if self.assignment.get(u, -1) == self.assignment.get(v, -1):
                conflicted.add(u)
                conflicted.add(v)
        return conflicted
    
    # ========================================================================
    # OPERACIONES EN SOLUCIONES
    # ========================================================================
    
    def copy(self) -> "ColoringSolution":
        """
        Crear una copia independiente de esta solución.
        
        Retorna:
            ColoringSolution: Nueva solución con copia profunda de la asignación
        
        Ejemplo:
            >>> sol1 = ColoringSolution({1: 0, 2: 1})
            >>> sol2 = sol1.copy()
            >>> sol2.assignment[1] = 99
            >>> sol1.assignment[1]
            0
        """
        return ColoringSolution(assignment=self.assignment.copy())
    
    def recolor_vertex(self, vertex: int, new_color: int) -> "ColoringSolution":
        """
        Crear nueva solución con un vértice recoloreado.
        
        Parametros:
            vertex (int): Vértice a recolorear
            new_color (int): Nuevo color
        
        Retorna:
            ColoringSolution: Nueva solución con el cambio
        """
        new_assignment = self.assignment.copy()
        new_assignment[vertex] = new_color
        return ColoringSolution(assignment=new_assignment)
    
    def recolor_vertices(self, recoloring: Dict[int, int]) -> "ColoringSolution":
        """
        Crear nueva solución con múltiples vértices recoloreados.
        
        Parametros:
            recoloring (Dict[int, int]): {vértice: nuevo_color}
        
        Retorna:
            ColoringSolution: Nueva solución con los cambios
        """
        new_assignment = self.assignment.copy()
        new_assignment.update(recoloring)
        return ColoringSolution(assignment=new_assignment)
    
    # ========================================================================
    # ANÁLISIS DE SOLUCIÓN
    # ========================================================================
    
    def color_usage(self) -> Dict[int, int]:
        """
        Calcular número de vértices de cada color.
        
        Retorna:
            Dict[int, int]: {color: cantidad de vértices}
        """
        usage = {}
        for color in range(self.num_colors):
            usage[color] = len(self.color_sets.get(color, set()))
        return usage
    
    def color_balance(self) -> float:
        """
        Medir el balance de colores (desviación estándar de uso).
        
        Valor bajo = colores bien distribuidos
        Valor alto = colores desbalanceados
        
        Retorna:
            float: Desviación estándar del uso de colores
        """
        usage = list(self.color_usage().values())
        if not usage:
            return 0.0
        return float(np.std(usage))
    
    def get_color(self, vertex: int) -> Optional[int]:
        """Obtener color de un vértice."""
        return self.assignment.get(vertex)
    
    def get_vertices_with_color(self, color: int) -> Set[int]:
        """Obtener todos los vértices con un color específico."""
        return self.color_sets.get(color, set()).copy()
    
    # ========================================================================
    # COMPARACIÓN
    # ========================================================================
    
    def is_better_than(self, other: "ColoringSolution", problem: GraphColoringProblem) -> bool:
        """
        Comparar dos soluciones (mejor = menos colores y/o menos conflictos).
        
        Parametros:
            other (ColoringSolution): Otra solución
            problem (GraphColoringProblem): Instancia del problema
        
        Retorna:
            bool: True si esta solución es mejor que other
        """
        # Primero: menos conflictos (factibilidad)
        my_conflicts = self.num_conflicts(problem)
        other_conflicts = other.num_conflicts(problem)
        
        if my_conflicts != other_conflicts:
            return my_conflicts < other_conflicts
        
        # Segundo: menos colores
        return self.num_colors < other.num_colors
    
    def __eq__(self, other: object) -> bool:
        """Dos soluciones son iguales si tienen la misma asignación."""
        if not isinstance(other, ColoringSolution):
            return False
        return self.assignment == other.assignment
    
    def __lt__(self, other: "ColoringSolution") -> bool:
        """Comparación: menos colores = menor."""
        if self.num_colors != other.num_colors:
            return self.num_colors < other.num_colors
        # Si mismo número de colores, por ID de solución
        return id(self) < id(other)
    
    # ========================================================================
    # REPRESENTACIÓN
    # ========================================================================
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"ColoringSolution(colors={self.num_colors}, vertices={self.num_vertices})"
    
    def __repr__(self) -> str:
        """Representación para debug."""
        return f"ColoringSolution(assignment={self.assignment})"
    
    def detailed_summary(self, problem: Optional[GraphColoringProblem] = None) -> str:
        """Resumen detallado de la solución."""
        summary = f"{'='*60}\n"
        summary += f"Solución de Coloración de Grafos\n"
        summary += f"{'='*60}\n"
        summary += f"Colores utilizados:    {self.num_colors}\n"
        summary += f"Vértices coloreados:   {self.num_vertices}\n"
        
        if problem:
            conflicts = self.num_conflicts(problem)
            summary += f"Conflictos:            {conflicts}\n"
            summary += f"Factible:              {'Sí' if conflicts == 0 else 'No'}\n"
            summary += f"Óptimo conocido:       {problem.colors_known if problem.colors_known else 'desconocido'}\n"
            
            if problem.colors_known:
                gap = self.num_colors - problem.colors_known
                gap_percent = 100 * gap / problem.colors_known if problem.colors_known > 0 else 0
                summary += f"Gap a óptimo:          {gap} ({gap_percent:.2f}%)\n"
        
        summary += f"\nDistribución de colores:\n"
        usage = self.color_usage()
        for color in sorted(usage.keys()):
            count = usage[color]
            summary += f"  Color {color}: {count} vértices\n"
        
        summary += f"{'='*60}\n"
        return summary
