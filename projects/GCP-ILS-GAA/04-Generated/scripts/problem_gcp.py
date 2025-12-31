"""
Auto-generated Problem Module for GCP-ILS-GAA

Generated from:
  - projects/GCP-ILS-GAA/00-Core/Problem.md
  - Problem: Graph Coloring Problem (GCP)
  - Version: 1.0.0

This module provides:
  - Graph class for representing problem instances
  - Problem class with evaluation and feasibility checking
  - Helper functions for loading and validation
"""

import os
import sys
from typing import List, Tuple, Set, Dict, Optional
import numpy as np


class Graph:
    """
    Representation of an undirected graph for the Graph Coloring Problem.
    
    Attributes:
        n: Number of vertices
        m: Number of edges
        edges: List of edges as (u, v) tuples
        adjacency: Adjacency list representation
        degrees: Degree of each vertex
    """
    
    def __init__(self, n: int, edges: List[Tuple[int, int]] = None):
        """
        Initialize graph.
        
        Args:
            n: Number of vertices (0-indexed from 0 to n-1)
            edges: List of edges as (u, v) tuples (optional)
        """
        self.n = n
        self.m = 0
        self.edges: List[Tuple[int, int]] = []
        self.adjacency: List[Set[int]] = [set() for _ in range(n)]
        self.degrees = [0] * n
        
        if edges:
            for u, v in edges:
                self.add_edge(u, v)
    
    def add_edge(self, u: int, v: int):
        """Add undirected edge between vertices u and v."""
        if u != v and v not in self.adjacency[u]:
            self.edges.append((u, v))
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)
            self.degrees[u] += 1
            self.degrees[v] += 1
            self.m += 1
    
    def are_adjacent(self, u: int, v: int) -> bool:
        """Check if vertices u and v are adjacent."""
        return v in self.adjacency[u]
    
    def get_neighbors(self, v: int) -> Set[int]:
        """Get all neighbors of vertex v."""
        return self.adjacency[v].copy()
    
    def get_degree(self, v: int) -> int:
        """Get degree of vertex v."""
        return self.degrees[v]
    
    def max_degree(self) -> int:
        """Get maximum degree in graph."""
        return max(self.degrees) if self.degrees else 0
    
    def density(self) -> float:
        """Get edge density: m / (n*(n-1)/2)."""
        if self.n <= 1:
            return 0.0
        max_edges = self.n * (self.n - 1) / 2
        return self.m / max_edges
    
    def __repr__(self):
        return f"Graph(n={self.n}, m={self.m}, density={self.density():.3f})"


class GCProblem:
    """
    Graph Coloring Problem (GCP) - Auto-generated from specification.
    
    Minimizes the number of colors (chromatic number) needed to color
    a graph such that no adjacent vertices have the same color.
    """
    
    def __init__(self, graph: Graph):
        """
        Initialize GCP problem.
        
        Args:
            graph: Graph instance to solve
        """
        self.graph = graph
        self.n = graph.n
        self.m = graph.m
    
    def is_feasible(self, coloring: List[int]) -> bool:
        """
        Check if coloring is feasible (no adjacent vertices with same color).
        
        Args:
            coloring: Vector of colors [c_0, c_1, ..., c_{n-1}]
        
        Returns:
            True if coloring is feasible, False otherwise
        """
        if len(coloring) != self.n:
            return False
        
        for u, v in self.graph.edges:
            if coloring[u] == coloring[v]:
                return False
        
        return True
    
    def count_conflicts(self, coloring: List[int]) -> int:
        """
        Count number of conflicting edges (adjacent vertices with same color).
        
        Args:
            coloring: Vector of colors
        
        Returns:
            Number of conflicts
        """
        conflicts = 0
        for u, v in self.graph.edges:
            if coloring[u] == coloring[v]:
                conflicts += 1
        return conflicts
    
    def num_colors(self, coloring: List[int]) -> int:
        """
        Get number of colors used in coloring.
        
        Args:
            coloring: Vector of colors
        
        Returns:
            Maximum color value (number of colors)
        """
        if not coloring:
            return 0
        return max(coloring) if coloring else 0
    
    def evaluate(self, coloring: List[int], penalty: float = 1000.0) -> float:
        """
        Evaluate fitness of a coloring (Lower is better).
        
        Combines:
        - Primary objective: Number of colors k
        - Secondary penalty: Conflicts with high penalty
        
        Args:
            coloring: Vector of colors
            penalty: Penalty multiplier for conflicts (default 1000)
        
        Returns:
            Fitness value (lower is better)
        """
        k = self.num_colors(coloring)
        conflicts = self.count_conflicts(coloring)
        
        # fitness = k + penalty * conflicts
        return k + penalty * conflicts
    
    def evaluate_detailed(self, coloring: List[int]) -> Dict:
        """
        Detailed evaluation of coloring.
        
        Args:
            coloring: Vector of colors
        
        Returns:
            Dictionary with detailed metrics
        """
        k = self.num_colors(coloring)
        conflicts = self.count_conflicts(coloring)
        feasible = self.is_feasible(coloring)
        
        return {
            'k': k,
            'num_colors': k,
            'conflicts': conflicts,
            'feasible': feasible,
            'fitness': k + 1000 * conflicts,
        }
    
    def get_chromatic_number_lower_bound(self) -> int:
        """
        Get lower bound for chromatic number.
        
        Uses: χ(G) >= Δ + 1 for some graphs, and χ(G) >= n / α(G)
        
        Returns:
            Lower bound estimate
        """
        # Trivial lower bound: max degree + 1 (not always tight)
        delta = self.graph.max_degree()
        return delta + 1
    
    def __repr__(self):
        return f"GCProblem({self.graph})"


# Utility functions for loading instances

def load_instance_dimacs(filepath: str) -> GCProblem:
    """
    Load a GCP instance from DIMACS format file.
    
    DIMACS format:
    ```
    p edge <n> <m>
    e <u> <v>
    e <u> <v>
    ...
    ```
    
    Args:
        filepath: Path to .col file
    
    Returns:
        GCProblem instance
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Instance file not found: {filepath}")
    
    graph = Graph(0)  # Will be reset by parser
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments
            if line.startswith('c'):
                continue
            
            # Parse problem line
            if line.startswith('p'):
                parts = line.split()
                if len(parts) < 4:
                    raise ValueError("Invalid problem line format")
                
                problem_type = parts[1]
                if problem_type != 'edge':
                    raise ValueError(f"Expected 'edge', got '{problem_type}'")
                
                n = int(parts[2])
                m = int(parts[3])
                
                # Reinitialize graph with correct vertex count
                graph = Graph(n)
                continue
            
            # Parse edge line
            if line.startswith('e'):
                parts = line.split()
                if len(parts) < 3:
                    raise ValueError("Invalid edge line format")
                
                u = int(parts[1]) - 1  # Convert to 0-indexed
                v = int(parts[2]) - 1
                
                if 0 <= u < graph.n and 0 <= v < graph.n:
                    graph.add_edge(u, v)
    
    return GCProblem(graph)


def load_instance_simple(filepath: str) -> GCProblem:
    """
    Load a GCP instance from simple format file.
    
    Simple format:
    ```
    n m
    u1 v1
    u2 v2
    ...
    ```
    
    Args:
        filepath: Path to instance file
    
    Returns:
        GCProblem instance
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Instance file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # First line: n m
    n, m = map(int, lines[0].split())
    graph = Graph(n)
    
    # Remaining lines: edges
    for i in range(1, min(len(lines), m + 1)):
        u, v = map(int, lines[i].split())
        graph.add_edge(u, v)
    
    return GCProblem(graph)


def load_instance(filepath: str) -> GCProblem:
    """
    Load a GCP instance (auto-detect format).
    
    Args:
        filepath: Path to instance file (.col or .txt)
    
    Returns:
        GCProblem instance
    """
    if filepath.endswith('.col'):
        return load_instance_dimacs(filepath)
    else:
        return load_instance_simple(filepath)


# Example usage
if __name__ == "__main__":
    # Example: Create simple graph
    graph = Graph(5, edges=[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
    problem = GCProblem(graph)
    
    print(f"Problem: {problem}")
    print(f"Graph: n={problem.n}, m={problem.m}, density={graph.density():.3f}")
    print(f"Chromatic number lower bound: {problem.get_chromatic_number_lower_bound()}")
    
    # Example: Evaluate a coloring
    coloring = [1, 2, 3, 1, 2]
    print(f"\nColoring: {coloring}")
    print(f"Feasible: {problem.is_feasible(coloring)}")
    print(f"Num colors: {problem.num_colors(coloring)}")
    print(f"Conflicts: {problem.count_conflicts(coloring)}")
    print(f"Fitness: {problem.evaluate(coloring)}")
