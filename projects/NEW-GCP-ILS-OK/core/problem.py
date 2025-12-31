"""
Core module: Graph Coloring Problem definition

Este modulo define la clase GraphColoringProblem que representa
una instancia del problema de coloracion de grafos en formato DIMACS.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
import numpy as np


@dataclass
class GraphColoringProblem:
    """
    Representacion de una instancia del Graph Coloring Problem (GCP)
    
    El problema consiste en asignar colores a los vertices de un grafo
    tal que ningun par de vertices adyacentes tenga el mismo color,
    minimizando el numero de colores utilizados.
    
    Atributos:
        vertices (int): Numero de vertices (n)
        edges (List[Tuple[int, int]]): Lista de aristas (u, v) donde u < v
        colors_known (Optional[int]): Numero cromatico conocido del BKS.json
        name (str): Nombre descriptivo de la instancia
        source (str): Familia de la instancia (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
        adjacency_list (Dict[int, List[int]]): Lista de adyacencia (computada)
    
    Ejemplo:
        >>> problem = GraphColoringProblem(
        ...     vertices=47,
        ...     edges=[(0,1), (0,3), (1,2), (2,3)],
        ...     colors_known=5,
        ...     name="myciel5",
        ...     source="MYC"
        ... )
        >>> print(problem.num_edges)
        4
        >>> print(problem.density)
        0.11627906976744186
    """
    
    vertices: int
    edges: List[Tuple[int, int]]
    colors_known: Optional[int] = None
    name: str = "GCP"
    source: str = "UNKNOWN"
    adjacency_list: Dict[int, List[int]] = field(default_factory=dict, init=False)
    
    def __post_init__(self):
        """Validaciones tras inicializacion"""
        
        # Validar numero de vertices
        if self.vertices <= 0:
            raise ValueError(
                f"Numero de vertices debe ser positivo, recibido: {self.vertices}"
            )
        
        # Convertir edges a lista si es necesario
        if not isinstance(self.edges, list):
            self.edges = list(self.edges)
        
        # Validar cada arista
        for i, (u, v) in enumerate(self.edges):
            if not isinstance(u, (int, np.integer)) or not isinstance(v, (int, np.integer)):
                raise TypeError(f"Arista {i}: vertices deben ser enteros, recibido ({type(u)}, {type(v)})")
            
            u, v = int(u), int(v)
            if not (0 <= u < self.vertices and 0 <= v < self.vertices):
                raise ValueError(
                    f"Arista {i}: ({u},{v}) fuera de rango [0,{self.vertices-1}]"
                )
            
            if u == v:
                raise ValueError(f"Arista {i}: self-loop detectado ({u},{u})")
            
            # Normalizar arista (u < v)
            if u > v:
                self.edges[i] = (v, u)
        
        # Validar colors_known
        if self.colors_known is not None and self.colors_known <= 0:
            raise ValueError(
                f"colors_known debe ser positivo, recibido: {self.colors_known}"
            )
        
        # Construir lista de adyacencia
        self._build_adjacency_list()
    
    def _build_adjacency_list(self) -> None:
        """Construir lista de adyacencia para acceso rapido"""
        self.adjacency_list = {i: [] for i in range(self.vertices)}
        for u, v in self.edges:
            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)
        
        # Ordenar para consistencia
        for neighbors in self.adjacency_list.values():
            neighbors.sort()
    
    @property
    def num_edges(self) -> int:
        """Retorna el numero de aristas"""
        return len(self.edges)
    
    @property
    def density(self) -> float:
        """
        Densidad del grafo: m / (n*(n-1)/2)
        
        Rango: [0, 1]
        - Cercano a 0: grafo disperso
        - Cercano a 1: grafo denso
        """
        max_edges = self.vertices * (self.vertices - 1) / 2
        return self.num_edges / max_edges if max_edges > 0 else 0
    
    @property
    def max_degree(self) -> int:
        """Retorna el grado maximo del grafo"""
        return max(
            (len(neighbors) for neighbors in self.adjacency_list.values()),
            default=0
        )
    
    @property
    def min_degree(self) -> int:
        """Retorna el grado minimo del grafo"""
        return min(
            (len(neighbors) for neighbors in self.adjacency_list.values()),
            default=0
        )
    
    @property
    def avg_degree(self) -> float:
        """Retorna el grado promedio del grafo"""
        return 2 * self.num_edges / self.vertices if self.vertices > 0 else 0
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Retorna los vecinos de un vertice"""
        if not (0 <= vertex < self.vertices):
            raise ValueError(f"Vertice {vertex} fuera de rango [0,{self.vertices-1}]")
        return self.adjacency_list[vertex]
    
    def is_adjacent(self, u: int, v: int) -> bool:
        """Verifica si dos vertices son adyacentes"""
        if not (0 <= u < self.vertices and 0 <= v < self.vertices):
            raise ValueError(f"Vertices ({u},{v}) fuera de rango [0,{self.vertices-1}]")
        return v in self.adjacency_list[u]
    
    def get_degree(self, vertex: int) -> int:
        """Retorna el grado de un vertice"""
        if not (0 <= vertex < self.vertices):
            raise ValueError(f"Vertice {vertex} fuera de rango [0,{self.vertices-1}]")
        return len(self.adjacency_list[vertex])
    
    @classmethod
    def from_dict(cls, data: Dict) -> "GraphColoringProblem":
        """
        Crea una instancia desde un diccionario (formato JSON)
        
        Args:
            data: Diccionario con claves 'vertices', 'edges', 'colors_known', 'name'
        
        Returns:
            GraphColoringProblem
        """
        return cls(
            vertices=data['vertices'],
            edges=[tuple(e) for e in data['edges']],
            colors_known=data.get('colors_known'),
            name=data.get('name', 'GCP'),
            source=data.get('source', 'UNKNOWN')
        )
    
    def to_dict(self) -> Dict:
        """Serializa la instancia a diccionario"""
        return {
            'vertices': self.vertices,
            'edges': [list(e) for e in self.edges],
            'colors_known': self.colors_known,
            'name': self.name,
            'source': self.source,
            'num_edges': self.num_edges,
            'density': self.density,
            'max_degree': self.max_degree,
            'avg_degree': self.avg_degree
        }
    
    def __str__(self) -> str:
        """Representacion en string"""
        return (
            f"GraphColoringProblem(name='{self.name}', "
            f"vertices={self.vertices}, edges={self.num_edges}, "
            f"density={self.density:.3f}, colors_known={self.colors_known})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
