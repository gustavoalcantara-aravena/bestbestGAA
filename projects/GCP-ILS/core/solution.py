"""
Coloring Solution - Representación de Soluciones

Una solución es un vector de colores: [c_1, c_2, ..., c_n]
donde c_i ∈ {0, 1, 2, ..., k}
- 0 = vértice sin color asignado (temporal)
- 1..k = colores asignados

Una solución es FACTIBLE si no hay conflictos (aristas monocromáticas).
"""

from typing import List, Optional, Set, Tuple
import numpy as np
from copy import deepcopy


class ColoringSolution:
    """
    Representación de una solución del Graph Coloring Problem.
    
    Attributes:
        coloring: Vector de colores [c_1, c_2, ..., c_n] (1-indexed lógicamente)
        n: Número de vértices
        problem: Referencia al problema (para evaluación)
    """
    
    def __init__(self,
                 n: int,
                 coloring: Optional[List[int]] = None,
                 problem: Optional['GraphColoringProblem'] = None):
        """
        Inicializa una solución.
        
        Args:
            n: Número de vértices
            coloring: Vector de colores (0-indexed en array, pero valores 1..k)
                     Si None, se crea solución vacía (todos 0)
            problem: Referencia al problema
        """
        self.n = n
        self.problem = problem
        
        if coloring is None:
            self.coloring = [0] * n  # Solución vacía
        else:
            self.coloring = list(coloring)
            if len(self.coloring) != n:
                raise ValueError(
                    f"Longitud de coloring debe ser {n}, "
                    f"recibido: {len(self.coloring)}"
                )
        
        # Atributos cached (lazy evaluation)
        self._num_colors = None
        self._conflicts = None
        self._is_feasible = None
        self._conflict_set = None
    
    @classmethod
    def empty(cls, n: int, problem=None) -> 'ColoringSolution':
        """Crea solución vacía (sin colores asignados)"""
        return cls(n=n, coloring=[0] * n, problem=problem)
    
    @classmethod
    def from_sequence(cls, colors: List[int], problem=None) -> 'ColoringSolution':
        """Crea solución desde secuencia de colores"""
        return cls(n=len(colors), coloring=colors, problem=problem)
    
    @classmethod
    def random(cls, n: int, max_color: int, problem=None, 
               rng: np.random.Generator = None) -> 'ColoringSolution':
        """
        Crea solución aleatoria.
        
        Args:
            n: Número de vértices
            max_color: Número máximo de colores a usar
            problem: Problema asociado
            rng: Generador aleatorio
        """
        if rng is None:
            rng = np.random.default_rng()
        
        # Asignar colores aleatorios de 1 a max_color
        coloring = rng.integers(1, max_color + 1, size=n).tolist()
        return cls(n=n, coloring=coloring, problem=problem)
    
    def count_colors(self) -> int:
        """
        Cuenta el número de colores utilizados.
        
        Returns:
            Número de colores diferentes > 0 en la solución
        """
        return len(set(c for c in self.coloring if c > 0))
    
    @property
    def num_colors(self) -> int:
        """Número de colores utilizados (con caching)"""
        if self._num_colors is None:
            self._num_colors = self.count_colors()
        return self._num_colors
    
    def count_conflicts(self, problem=None) -> int:
        """
        Cuenta el número de aristas monocromáticas (conflictos).
        
        Args:
            problem: Problema (usa self.problem si None)
            
        Returns:
            Número de conflictos
        """
        if problem is None:
            problem = self.problem
        
        if problem is None:
            raise ValueError(
                "Se requiere problema para contar conflictos"
            )
        
        conflicts = 0
        for v1, v2 in problem.edges:
            # Convertir de 1-indexed a 0-indexed para el array
            c1 = self.coloring[v1 - 1]
            c2 = self.coloring[v2 - 1]
            
            # Conflicto si ambos tienen el mismo color > 0
            if c1 > 0 and c1 == c2:
                conflicts += 1
        
        return conflicts
    
    @property
    def conflicts(self) -> int:
        """Número de conflictos (con caching)"""
        if self._conflicts is None:
            self._conflicts = self.count_conflicts()
        return self._conflicts
    
    def get_conflicting_vertices(self, problem=None) -> Set[int]:
        """
        Retorna el conjunto de vértices que tienen conflictos.
        
        Args:
            problem: Problema (usa self.problem si None)
            
        Returns:
            Conjunto de vértices conflictivos (1-indexed)
        """
        if problem is None:
            problem = self.problem
        
        if problem is None:
            return set()
        
        conflicting = set()
        for v1, v2 in problem.edges:
            c1 = self.coloring[v1 - 1]
            c2 = self.coloring[v2 - 1]
            
            if c1 > 0 and c1 == c2:
                conflicting.add(v1)
                conflicting.add(v2)
        
        return conflicting
    
    def is_feasible(self, problem=None) -> bool:
        """
        Comprueba si la solución es factible (sin conflictos).
        
        Args:
            problem: Problema (usa self.problem si None)
            
        Returns:
            True si no hay conflictos
        """
        if problem is None:
            problem = self.problem
        
        if problem is None:
            # Sin problema, asumir factible si no hay conflictos evidentes
            return self.count_conflicts() == 0
        
        if self._is_feasible is None:
            self._is_feasible = self.count_conflicts(problem) == 0
        
        return self._is_feasible
    
    def is_complete(self) -> bool:
        """Comprueba si todos los vértices tienen color asignado"""
        return all(c > 0 for c in self.coloring)
    
    def get_uncolored_vertices(self) -> List[int]:
        """Retorna vértices sin color asignado (1-indexed)"""
        return [i + 1 for i, c in enumerate(self.coloring) if c == 0]
    
    def copy(self) -> 'ColoringSolution':
        """Crea copia profunda de la solución"""
        return ColoringSolution(
            n=self.n,
            coloring=self.coloring.copy(),
            problem=self.problem
        )
    
    def clear_cache(self):
        """Limpia el caché de atributos calculados"""
        self._num_colors = None
        self._conflicts = None
        self._is_feasible = None
        self._conflict_set = None
    
    def __setitem__(self, vertex: int, color: int):
        """
        Asigna un color a un vértice.
        
        Args:
            vertex: Vértice (1-indexed)
            color: Color a asignar
        """
        if vertex < 1 or vertex > self.n:
            raise IndexError(f"Vértice {vertex} fuera de rango [1, {self.n}]")
        
        self.coloring[vertex - 1] = color
        self.clear_cache()
    
    def __getitem__(self, vertex: int) -> int:
        """
        Obtiene el color asignado a un vértice.
        
        Args:
            vertex: Vértice (1-indexed)
            
        Returns:
            Color asignado (0 si no está coloreado)
        """
        if vertex < 1 or vertex > self.n:
            raise IndexError(f"Vértice {vertex} fuera de rango [1, {self.n}]")
        
        return self.coloring[vertex - 1]
    
    def __repr__(self) -> str:
        """Representación string"""
        return (
            f"ColoringSolution("
            f"n={self.n}, "
            f"k={self.num_colors}, "
            f"conflicts={self.conflicts}"
            f")"
        )
    
    def __str__(self) -> str:
        """String informativo"""
        info = f"""
Coloring Solution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vértices:        {self.n}
Colores usados:  {self.num_colors}
Conflictos:      {self.conflicts}
Factible:        {'✓' if self.is_feasible() else '✗'}
Completa:        {'✓' if self.is_complete() else '✗'}
Coloring:        {self.coloring[:min(20, len(self.coloring))]}{'...' if self.n > 20 else ''}
        """
        return info
    
    def summary(self) -> dict:
        """Retorna resumen de la solución"""
        return {
            'n': self.n,
            'k': self.num_colors,
            'conflicts': self.conflicts,
            'is_feasible': self.is_feasible(),
            'is_complete': self.is_complete(),
            'uncolored_count': len(self.get_uncolored_vertices())
        }
