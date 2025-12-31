"""
core/problem.py
Define la clase GraphColoringProblem para representar instancias del problema de coloración de grafos.

Proporciona:
    - Carga desde formato DIMACS
    - Validación de grafo
    - Propiedades y métodos helper
    - Información de la instancia (vértices, aristas, grados, etc.)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Set, Optional, Dict
import numpy as np
from pathlib import Path


@dataclass
class GraphColoringProblem:
    """
    Representa una instancia del problema de coloración de grafos (Graph Coloring Problem - GCP).
    
    Problema:
        Asignar colores a vértices de un grafo de modo que no haya dos vértices adyacentes
        con el mismo color, minimizando el número de colores utilizados (número cromático χ).
    
    Atributos:
        vertices (int): Número de vértices (V)
        edges (List[Tuple[int, int]]): Lista de aristas (E) como tuplas (u, v)
        colors_known (Optional[int]): Número cromático óptimo conocido (si está disponible)
        guaranteed_upper_bound (Optional[int]): Cota superior garantizada
        name (str): Nombre de la instancia (para referencia)
    
    Ejemplo:
        >>> edges = [(1, 2), (2, 3), (1, 3)]  # Triángulo
        >>> problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
        >>> print(f"Vértices: {problem.n_vertices}, Aristas: {problem.n_edges}")
        Vértices: 3, Aristas: 3
    """
    
    vertices: int
    edges: List[Tuple[int, int]]
    colors_known: Optional[int] = None
    guaranteed_upper_bound: Optional[int] = None
    name: str = "unnamed"
    
    # Propiedades calculadas (se computan una sola vez)
    _adjacency_list: Dict[int, Set[int]] = field(default_factory=dict, init=False, repr=False)
    _edge_weight_matrix: Optional[np.ndarray] = field(default=None, init=False, repr=False)
    _degree_sequence: Optional[np.ndarray] = field(default=None, init=False, repr=False)
    _max_degree: Optional[int] = field(default=None, init=False, repr=False)
    _is_bipartite: Optional[bool] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Validar e inicializar la instancia después de la construcción."""
        # Validaciones básicas
        if self.vertices <= 0:
            raise ValueError(f"Número de vértices debe ser positivo, obtenido: {self.vertices}")
        
        if not self.edges:
            # Grafo sin aristas
            self._validate_edges()
            self._build_adjacency_list()
        else:
            # Validar aristas
            self._validate_edges()
            self._build_adjacency_list()
        
        # Si no se proporciona óptimo, computar cota superior
        if self.colors_known is None and self.guaranteed_upper_bound is None:
            self.guaranteed_upper_bound = self.upper_bound
    
    def _validate_edges(self):
        """Validar que las aristas son correctas."""
        for u, v in self.edges:
            if u < 1 or u > self.vertices:
                raise ValueError(f"Vértice {u} fuera de rango [1, {self.vertices}]")
            if v < 1 or v > self.vertices:
                raise ValueError(f"Vértice {v} fuera de rango [1, {self.vertices}]")
            if u == v:
                raise ValueError(f"Arista de auto-loop no permitida: ({u}, {v})")
    
    def _build_adjacency_list(self):
        """Construir lista de adyacencia a partir de las aristas."""
        self._adjacency_list = {i: set() for i in range(1, self.vertices + 1)}
        for u, v in self.edges:
            self._adjacency_list[u].add(v)
            self._adjacency_list[v].add(u)
    
    # ========================================================================
    # PROPIEDADES BÁSICAS
    # ========================================================================
    
    @property
    def n_vertices(self) -> int:
        """Número de vértices del grafo."""
        return self.vertices
    
    @property
    def n_edges(self) -> int:
        """Número de aristas del grafo."""
        return len(self.edges)
    
    @property
    def adjacency_list(self) -> Dict[int, Set[int]]:
        """Lista de adyacencia: {vértice: {vértices adyacentes}}."""
        return self._adjacency_list
    
    # ========================================================================
    # PROPIEDADES DE GRADOS
    # ========================================================================
    
    @property
    def degree_sequence(self) -> np.ndarray:
        """Secuencia de grados: array de grados de cada vértice."""
        if self._degree_sequence is None:
            self._degree_sequence = np.array(
                [len(self._adjacency_list[i]) for i in range(1, self.vertices + 1)]
            )
        return self._degree_sequence
    
    @property
    def max_degree(self) -> int:
        """Grado máximo del grafo (Δ)."""
        if self._max_degree is None:
            self._max_degree = int(np.max(self.degree_sequence)) if self.n_vertices > 0 else 0
        return self._max_degree
    
    @property
    def min_degree(self) -> int:
        """Grado mínimo del grafo."""
        return int(np.min(self.degree_sequence)) if self.n_vertices > 0 else 0
    
    @property
    def average_degree(self) -> float:
        """Grado promedio del grafo."""
        return float(np.mean(self.degree_sequence)) if self.n_vertices > 0 else 0.0
    
    # ========================================================================
    # PROPIEDADES DE COTAS
    # ========================================================================
    
    @property
    def upper_bound(self) -> int:
        """Cota superior trivial: Δ(G) + 1 (Teorema de Brooks)."""
        return self.max_degree + 1
    
    @property
    def lower_bound(self) -> int:
        """Cota inferior: ω(G) o clique number (aquí: tamaño máx. clique)."""
        # Aproximación simple: máximo grado + 1
        # Para mejor estimación se requeriría detectar cliques
        return max(2, int(np.sqrt(2 * self.n_edges)))
    
    # ========================================================================
    # PROPIEDADES DE MATRIZ
    # ========================================================================
    
    @property
    def edge_weight_matrix(self) -> np.ndarray:
        """
        Matriz de adyacencia (peso de aristas).
        W[i-1, j-1] = 1 si existe arista (i, j), 0 en otro caso.
        """
        if self._edge_weight_matrix is None:
            W = np.zeros((self.vertices, self.vertices), dtype=np.int32)
            for u, v in self.edges:
                W[u-1, v-1] = 1
                W[v-1, u-1] = 1
            self._edge_weight_matrix = W
        return self._edge_weight_matrix
    
    # ========================================================================
    # MÉTODOS DE CONSULTA
    # ========================================================================
    
    def is_edge(self, u: int, v: int) -> bool:
        """
        Verificar si existe una arista entre u y v.
        
        Parametros:
            u, v (int): Vértices
        
        Retorna:
            bool: True si existe arista (u, v), False en otro caso
        """
        if u < 1 or u > self.vertices or v < 1 or v > self.vertices:
            return False
        return v in self._adjacency_list[u]
    
    def neighbors(self, v: int) -> Set[int]:
        """
        Obtener vecinos de un vértice.
        
        Parametros:
            v (int): Vértice
        
        Retorna:
            Set[int]: Conjunto de vértices adyacentes a v
        """
        if v < 1 or v > self.vertices:
            raise ValueError(f"Vértice {v} fuera de rango [1, {self.vertices}]")
        return self._adjacency_list[v].copy()
    
    def degree(self, v: int) -> int:
        """Grado de un vértice."""
        if v < 1 or v > self.vertices:
            raise ValueError(f"Vértice {v} fuera de rango [1, {self.vertices}]")
        return len(self._adjacency_list[v])
    
    # ========================================================================
    # DETECCIÓN DE PROPIEDADES
    # ========================================================================
    
    @property
    def is_bipartite(self) -> bool:
        """Detectar si el grafo es bipartito (2-coloreable)."""
        if self._is_bipartite is None:
            self._is_bipartite = self._check_bipartite()
        return self._is_bipartite
    
    def _check_bipartite(self) -> bool:
        """Verificar si el grafo es bipartito usando BFS."""
        if self.n_edges == 0:
            return True
        
        color = [-1] * (self.vertices + 1)
        
        for start in range(1, self.vertices + 1):
            if color[start] != -1:
                continue
            
            # BFS
            queue = [start]
            color[start] = 0
            
            while queue:
                u = queue.pop(0)
                for v in self._adjacency_list[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
        
        return True
    
    @property
    def clique_number(self) -> int:
        """Estimación del número de clique (≤ tamaño máximo clique)."""
        # Aproximación simple basada en grado máximo
        # Un clique es un conjunto de vértices totalmente conectados
        return min(self.vertices, self.max_degree + 1)
    
    # ========================================================================
    # CARGA DESDE ARCHIVOS
    # ========================================================================
    
    @classmethod
    def load_from_dimacs(cls, filepath: str) -> "GraphColoringProblem":
        """
        Cargar instancia desde archivo DIMACS (.col).
        
        Formato DIMACS:
            c Comments
            p edge <nodes> <edges>
            e <v1> <v2>
            ...
        
        Parametros:
            filepath (str): Ruta al archivo DIMACS
        
        Retorna:
            GraphColoringProblem: Instancia cargada
        
        Ejemplo:
            >>> problem = GraphColoringProblem.load_from_dimacs("myciel3.col")
            >>> print(f"Vértices: {problem.n_vertices}")
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        n_vertices = None
        n_edges_declared = None
        edges = []
        colors_known = None
        
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Comentarios
                if line.startswith('c'):
                    # Buscar "optimal" en comentarios
                    if "optimal" in line.lower():
                        try:
                            tokens = line.split()
                            for i, token in enumerate(tokens):
                                if token.isdigit() and int(token) > 0:
                                    colors_known = int(token)
                                    break
                        except:
                            pass
                    continue
                
                # Header
                if line.startswith('p'):
                    tokens = line.split()
                    if len(tokens) >= 4 and tokens[1] == 'edge':
                        n_vertices = int(tokens[2])
                        n_edges_declared = int(tokens[3])
                    continue
                
                # Aristas
                if line.startswith('e'):
                    tokens = line.split()
                    if len(tokens) >= 3:
                        u = int(tokens[1])
                        v = int(tokens[2])
                        edges.append((u, v))
        
        if n_vertices is None:
            raise ValueError("Archivo DIMACS inválido: falta header 'p edge'")
        
        name = path.stem  # Nombre sin extensión
        
        return cls(
            vertices=n_vertices,
            edges=edges,
            colors_known=colors_known,
            name=name
        )
    
    # ========================================================================
    # REPRESENTACIÓN
    # ========================================================================
    
    def __str__(self) -> str:
        """Representación en string."""
        return (
            f"GraphColoringProblem({self.name}): "
            f"{self.n_vertices} vértices, {self.n_edges} aristas, "
            f"χ={self.colors_known if self.colors_known else '?'}"
        )
    
    def __repr__(self) -> str:
        """Representación para debug."""
        return (
            f"GraphColoringProblem(vertices={self.vertices}, edges={len(self.edges)}, "
            f"colors_known={self.colors_known}, name='{self.name}')"
        )
    
    def summary(self) -> str:
        """Resumen detallado de la instancia."""
        return (
            f"{'='*60}\n"
            f"Instancia: {self.name}\n"
            f"{'='*60}\n"
            f"Vértices:              {self.n_vertices}\n"
            f"Aristas:               {self.n_edges}\n"
            f"Densidad:              {2*self.n_edges / (self.n_vertices*(self.n_vertices-1)):.4f}\n"
            f"Grado máximo (Δ):      {self.max_degree}\n"
            f"Grado mínimo:          {self.min_degree}\n"
            f"Grado promedio:        {self.average_degree:.2f}\n"
            f"Bipartito:             {self.is_bipartite}\n"
            f"Cota superior (Δ+1):   {self.upper_bound}\n"
            f"Cota inferior:         {self.lower_bound}\n"
            f"Óptimo conocido (χ):   {self.colors_known if self.colors_known else 'desconocido'}\n"
            f"{'='*60}\n"
        )
