"""
Graph Coloring Problem - Definición del Problema

Modelo Matemático:
    Minimizar: k (número de colores utilizados)
    
    Sujeto a:
        c_i ≠ c_j,  ∀(i,j) ∈ E  (vértices adyacentes con colores diferentes)
        c_i ∈ {1, 2, ..., k},  ∀i ∈ V
        
Variables:
    - c_i: color asignado al vértice i
    - V: conjunto de vértices
    - E: conjunto de aristas
    - k: número de colores (a minimizar)
    - n = |V|: número de vértices
    - m = |E|: número de aristas
"""

from typing import List, Set, Dict, Tuple, Optional
from pathlib import Path
import numpy as np


class GraphColoringProblem:
    """
    Instancia del Graph Coloring Problem (0/1 GCP)
    
    Attributes:
        n: Número de vértices
        edges: Lista de aristas (pares de vértices)
        adjacency: Lista de adyacencia para acceso rápido
        name: Nombre de la instancia
        optimal_value: Óptimo conocido (si existe)
        lower_bound: Cota inferior del número cromático
    """
    
    def __init__(self,
                 n: int,
                 edges: List[Tuple[int, int]],
                 name: str = "GCP",
                 optimal_value: Optional[int] = None,
                 lower_bound: Optional[int] = None):
        """
        Inicializa instancia del GCP
        
        Args:
            n: Número de vértices
            edges: Lista de aristas (v1, v2) con v1 < v2
            name: Nombre de la instancia
            optimal_value: Valor óptimo conocido
            lower_bound: Cota inferior
            
        Raises:
            ValueError: Si n <= 0 o si hay errores en aristas
        """
        if n <= 0:
            raise ValueError(f"Número de vértices debe ser positivo, recibido: {n}")
        
        self.n = n
        self.edges = edges
        self.m = len(edges)
        self.name = name
        self.optimal_value = optimal_value
        self.lower_bound = lower_bound
        
        # Construir lista de adyacencia (1-indexed, usando índices 1..n)
        self.adjacency: List[Set[int]] = [set() for _ in range(n + 1)]
        
        for v1, v2 in edges:
            # Validar rango
            if v1 < 1 or v1 > n or v2 < 1 or v2 > n:
                raise ValueError(
                    f"Vértices fuera de rango [1, {n}]: ({v1}, {v2})"
                )
            
            # Validar sin auto-loops
            if v1 == v2:
                raise ValueError(f"Auto-loop detectado: ({v1}, {v2})")
            
            # Agregar a ambos sentidos (grafo no dirigido)
            self.adjacency[v1].add(v2)
            self.adjacency[v2].add(v1)
        
        # Validar sin duplicados
        degrees = [len(adj) for adj in self.adjacency]
        if sum(degrees) != 2 * self.m:
            raise ValueError("Aristas duplicadas detectadas")
        
        # Calcular grado máximo (cota inferior trivial: χ(G) >= Δ(G) + 1 o Δ(G))
        self.max_degree = max(degrees) if degrees else 0
        self.min_degree = min(d for d in degrees[1:] if d > 0) if any(degrees[1:]) else 0
        self.avg_degree = 2 * self.m / n if n > 0 else 0
        
        # Densidad del grafo
        max_possible_edges = n * (n - 1) / 2
        self.density = self.m / max_possible_edges if max_possible_edges > 0 else 0
        
        # Si no hay cota inferior, usar heurística simple
        if self.lower_bound is None:
            # Cota de clique: tamaño de clique máximo >= χ(G)
            # Aquí usamos el grado máximo como aproximación
            self.lower_bound = min(self.max_degree, n)
    
    def get_neighbors(self, v: int) -> Set[int]:
        """
        Retorna los vértices adyacentes a v.
        
        Args:
            v: Vértice (1-indexed)
            
        Returns:
            Conjunto de vértices adyacentes
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice {v} fuera de rango [1, {self.n}]")
        
        return self.adjacency[v].copy()
    
    def is_adjacent(self, u: int, v: int) -> bool:
        """
        Comprueba si dos vértices son adyacentes.
        
        Args:
            u, v: Vértices (1-indexed)
            
        Returns:
            True si (u, v) ∈ E
        """
        if u < 1 or u > self.n or v < 1 or v > self.n:
            return False
        
        return v in self.adjacency[u]
    
    def get_degree(self, v: int) -> int:
        """
        Retorna el grado del vértice v.
        
        Args:
            v: Vértice (1-indexed)
            
        Returns:
            Grado de v
        """
        if v < 1 or v > self.n:
            raise ValueError(f"Vértice {v} fuera de rango [1, {self.n}]")
        
        return len(self.adjacency[v])
    
    def get_saturation_degree(self, coloring: List[int], v: int) -> int:
        """
        Calcula el DSATUR (Degree of Saturation) del vértice v.
        
        DSATUR = número de colores diferentes usados en vecinos de v.
        
        Args:
            coloring: Vector de colores [c_1, c_2, ..., c_n]
            v: Vértice (1-indexed, pero índices en coloring son 0-indexed)
            
        Returns:
            Número de colores saturation
        """
        colors_in_neighbors = set()
        for neighbor in self.adjacency[v]:
            color = coloring[neighbor - 1]  # Convertir a 0-indexed
            if color > 0:  # Color asignado (0 = sin asignar)
                colors_in_neighbors.add(color)
        
        return len(colors_in_neighbors)
    
    @classmethod
    def from_dimacs_file(cls, filepath: str, **kwargs) -> 'GraphColoringProblem':
        """
        Crea instancia desde archivo DIMACS.
        
        Args:
            filepath: Ruta al archivo .col
            **kwargs: Argumentos adicionales (name, optimal_value, lower_bound)
            
        Returns:
            Instancia de GraphColoringProblem
        """
        from .parser import DIMACParser
        
        n, edges = DIMACParser.parse(filepath)
        
        # Usar nombre del archivo si no se proporciona
        if 'name' not in kwargs:
            kwargs['name'] = Path(filepath).stem
        
        return cls(n=n, edges=edges, **kwargs)
    
    def __repr__(self) -> str:
        """Representación string de la instancia"""
        return (
            f"GraphColoringProblem("
            f"n={self.n}, m={self.m}, "
            f"Δ={self.max_degree}, "
            f"density={self.density:.3f}, "
            f"χ≥{self.lower_bound}"
            f")"
        )
    
    def __str__(self) -> str:
        """String informativo"""
        info = f"""
Graph Coloring Problem: {self.name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vértices (n):          {self.n}
Aristas (m):           {self.m}
Grado máximo (Δ):      {self.max_degree}
Grado mínimo (δ):      {self.min_degree}
Grado promedio:        {self.avg_degree:.2f}
Densidad:              {self.density:.4f}
Cota inferior (χ≥):    {self.lower_bound}
Óptimo conocido:       {self.optimal_value if self.optimal_value else 'Desconocido'}
        """
        return info
    
    def summary(self) -> Dict[str, any]:
        """Retorna resumen de la instancia como diccionario"""
        return {
            'name': self.name,
            'n': self.n,
            'm': self.m,
            'max_degree': self.max_degree,
            'min_degree': self.min_degree,
            'avg_degree': self.avg_degree,
            'density': self.density,
            'lower_bound': self.lower_bound,
            'optimal_value': self.optimal_value
        }
