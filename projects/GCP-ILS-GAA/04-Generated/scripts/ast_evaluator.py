"""
AST Evaluator for GCP-ILS-GAA

Evaluates algorithm configurations (AST nodes) on GCP problem instances.

Main responsibilities:
1. Load GCP instances (DIMACS format)
2. Execute each configuration on instances
3. Aggregate fitness across instances
4. Handle multi-instance evaluation
5. Parallel evaluation support

Author: GAA Framework
Version: 1.0.0
"""

import os
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from ast_nodes import AlgorithmNode, ast_statistics, validate_ast
from ils_search import Configuration


# ============================================================================
# GCP PROBLEM AND SOLVER
# ============================================================================

@dataclass
class GCPInstance:
    """Graph Coloring Problem instance"""
    
    name: str
    num_vertices: int
    num_edges: int
    edges: List[Tuple[int, int]]
    
    def __repr__(self):
        return f"GCP({self.name}, n={self.num_vertices}, m={self.num_edges})"
    
    def get_adjacency_list(self) -> Dict[int, set]:
        """Build adjacency list from edges"""
        adj = {i: set() for i in range(self.num_vertices)}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)
        return adj


class GCPSolver:
    """
    Executes a coloring algorithm (AST) on a GCP instance.
    
    This is the evaluation engine that interprets and runs AST-encoded algorithms.
    """
    
    def __init__(self, instance: GCPInstance, seed: Optional[int] = None):
        self.instance = instance
        self.adjacency = instance.get_adjacency_list()
        self.seed = seed
        
        if seed is not None:
            import random
            random.seed(seed)
    
    def execute_ast(self, algorithm: AlgorithmNode, max_time: float = 60) -> Dict[str, Any]:
        """
        Execute algorithm AST on the GCP instance.
        
        Returns:
            {
                'best_colors': int,
                'best_coloring': list,
                'iterations': int,
                'elapsed_time': float,
                'feasible': bool,
                'conflicts': int,
                'log': [...]
            }
        """
        
        start_time = time.time()
        
        # Validate AST
        is_valid, errors = validate_ast(algorithm)
        if not is_valid:
            return {
                'best_colors': float('inf'),
                'best_coloring': None,
                'iterations': 0,
                'elapsed_time': 0,
                'feasible': False,
                'conflicts': float('inf'),
                'log': [],
                'errors': errors
            }
        
        # Execute algorithm (would call algorithm.execute() in real implementation)
        # For now, return a placeholder with basic evaluation
        
        # Initialize with random coloring
        coloring = self._random_coloring()
        
        # Apply initialization phase
        coloring = self._execute_init_phase(algorithm.init_phase, coloring)
        
        best_coloring = coloring.copy()
        best_colors = self._count_colors(coloring)
        
        # Main search loop
        iteration = 0
        no_improve_count = 0
        max_iterations = 500  # Default
        
        while iteration < max_iterations and no_improve_count < 50:
            if time.time() - start_time > max_time:
                break
            
            # Apply search phases
            for phase in algorithm.search_phases:
                coloring = self._execute_phase(phase, coloring)
            
            # Evaluate
            colors = self._count_colors(coloring)
            conflicts = self._count_conflicts(coloring)
            
            # Update best
            if colors < best_colors:
                best_coloring = coloring.copy()
                best_colors = colors
                no_improve_count = 0
            else:
                no_improve_count += 1
            
            iteration += 1
        
        elapsed = time.time() - start_time
        conflicts = self._count_conflicts(best_coloring)
        
        return {
            'best_colors': best_colors,
            'best_coloring': best_coloring,
            'iterations': iteration,
            'elapsed_time': elapsed,
            'feasible': conflicts == 0,
            'conflicts': conflicts,
            'log': []
        }
    
    def _random_coloring(self) -> Dict[int, int]:
        """Create random initial coloring"""
        import random
        max_colors = min(self.instance.num_vertices, 10)
        return {v: random.randint(1, max_colors) for v in range(self.instance.num_vertices)}
    
    def _execute_init_phase(self, init_phase, coloring: Dict) -> Dict:
        """Execute initialization phase"""
        # Placeholder: return DSATUR-like coloring
        return self._greedy_dsatur()
    
    def _execute_phase(self, phase, coloring: Dict) -> Dict:
        """Execute a search phase (simplified)"""
        # Placeholder: apply basic local search moves
        return self._apply_local_search_moves(coloring)
    
    def _greedy_dsatur(self) -> Dict[int, int]:
        """DSATUR heuristic"""
        coloring = {}
        vertices_order = sorted(range(self.instance.num_vertices),
                              key=lambda v: len(self.adjacency[v]), reverse=True)
        
        for v in vertices_order:
            colors_used = set(coloring.get(u, 0) for u in self.adjacency[v] if u in coloring)
            color = 1
            while color in colors_used:
                color += 1
            coloring[v] = color
        
        return coloring
    
    def _apply_local_search_moves(self, coloring: Dict) -> Dict:
        """Apply local search moves (Kempe chain like)"""
        import random
        
        # Try to improve via color exchanges
        for _ in range(min(10, self.instance.num_vertices)):
            u = random.randint(0, self.instance.num_vertices - 1)
            v = random.randint(0, self.instance.num_vertices - 1)
            
            if u != v and coloring.get(u, 0) != coloring.get(v, 0):
                # Try swapping colors
                c1, c2 = coloring[u], coloring[v]
                coloring[u], coloring[v] = c2, c1
        
        return coloring
    
    def _count_colors(self, coloring: Dict) -> int:
        """Count colors used"""
        return len(set(coloring.values()))
    
    def _count_conflicts(self, coloring: Dict) -> int:
        """Count edges with same color on both endpoints"""
        conflicts = 0
        for u, v in self.instance.edges:
            if coloring.get(u) == coloring.get(v):
                conflicts += 1
        return conflicts


# ============================================================================
# INSTANCE LOADER
# ============================================================================

class InstanceLoader:
    """Load GCP instances from files"""
    
    @staticmethod
    def load_dimacs(filepath: str) -> GCPInstance:
        """
        Load GCP instance from DIMACS format (.col file).
        
        Format:
            p edge <n> <m>
            e <u> <v>
            ...
        """
        edges = []
        num_vertices = 0
        num_edges = 0
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c'):
                    continue
                
                parts = line.split()
                if parts[0] == 'p':
                    num_vertices = int(parts[2])
                    num_edges = int(parts[3])
                
                elif parts[0] == 'e':
                    u = int(parts[1]) - 1  # 0-indexed
                    v = int(parts[2]) - 1
                    edges.append((u, v))
        
        name = Path(filepath).stem
        return GCPInstance(name, num_vertices, num_edges, edges)
    
    @staticmethod
    def load_simple(filepath: str) -> GCPInstance:
        """Load GCP instance from simple format"""
        edges = []
        
        with open(filepath, 'r') as f:
            first_line = f.readline().strip().split()
            num_vertices = int(first_line[0])
            num_edges = int(first_line[1]) if len(first_line) > 1 else None
            
            for line in f:
                line = line.strip()
                if line:
                    u, v = map(int, line.split())
                    edges.append((u, v))
        
        if num_edges is None:
            num_edges = len(edges)
        
        name = Path(filepath).stem
        return GCPInstance(name, num_vertices, num_edges, edges)
    
    @staticmethod
    def load_instance(filepath: str) -> GCPInstance:
        """Auto-detect format and load"""
        if filepath.endswith('.col'):
            return InstanceLoader.load_dimacs(filepath)
        else:
            return InstanceLoader.load_simple(filepath)


# ============================================================================
# CONFIGURATION EVALUATOR
# ============================================================================

@dataclass
class EvaluationResult:
    """Result of evaluating one configuration on one instance"""
    
    configuration_id: str
    instance_name: str
    best_colors: int
    elapsed_time: float
    feasible: bool
    conflicts: int
    iterations: int


class ConfigurationEvaluator:
    """Evaluates a configuration on a set of instances"""
    
    def __init__(self, instances: List[GCPInstance], 
                 num_workers: int = 1,
                 seed: Optional[int] = None):
        self.instances = instances
        self.num_workers = num_workers
        self.seed = seed
    
    def evaluate(self, config: Configuration, max_time_per_instance: float = 60) -> Dict[str, float]:
        """
        Evaluate configuration on all instances.
        
        Returns:
            {
                'instance_name': num_colors,
                ...
            }
        """
        
        results = {}
        
        for instance in self.instances:
            solver = GCPSolver(instance, seed=self.seed)
            result = solver.execute_ast(config.ast, max_time=max_time_per_instance)
            
            # Store fitness (number of colors, or inf if infeasible)
            if result['feasible']:
                results[instance.name] = float(result['best_colors'])
            else:
                # Penalize infeasible solutions
                results[instance.name] = float(result['best_colors']) + 100 * result['conflicts']
        
        return results
    
    def evaluate_parallel(self, config: Configuration, 
                         max_time_per_instance: float = 60) -> Dict[str, float]:
        """Parallel evaluation across instances"""
        
        if self.num_workers == 1:
            return self.evaluate(config, max_time_per_instance)
        
        results = {}
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {}
            
            for instance in self.instances:
                future = executor.submit(
                    self._evaluate_single,
                    config,
                    instance,
                    max_time_per_instance
                )
                futures[future] = instance.name
            
            for future in as_completed(futures):
                instance_name = futures[future]
                fitness = future.result()
                results[instance_name] = fitness
        
        return results
    
    @staticmethod
    def _evaluate_single(config: Configuration, instance: GCPInstance, 
                        max_time: float) -> float:
        """Helper for parallel evaluation"""
        solver = GCPSolver(instance)
        result = solver.execute_ast(config.ast, max_time=max_time)
        
        if result['feasible']:
            return float(result['best_colors'])
        else:
            return float(result['best_colors']) + 100 * result['conflicts']


# ============================================================================
# BATCH EVALUATION
# ============================================================================

class BatchEvaluator:
    """Evaluate multiple configurations on multiple instances"""
    
    def __init__(self, instances: List[GCPInstance]):
        self.instances = instances
    
    def evaluate_population(self, configurations: List[Configuration],
                          max_time_per_instance: float = 60,
                          num_workers: int = 1) -> List[Configuration]:
        """
        Evaluate all configurations.
        
        Returns:
            Configurations with fitness_scores set
        """
        
        evaluator = ConfigurationEvaluator(self.instances, num_workers=num_workers)
        
        for i, config in enumerate(configurations):
            if config.aggregated_fitness == float('inf'):
                # Need to evaluate
                config.fitness_scores = evaluator.evaluate(config, max_time_per_instance)
        
        return configurations


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Create a small test instance
    instance = GCPInstance(
        name="test",
        num_vertices=5,
        num_edges=4,
        edges=[(0, 1), (1, 2), (2, 3), (3, 4)]
    )
    
    # Create a simple AST algorithm
    from ast_nodes import AlgorithmNode, InitPhaseNode, DSATURNode, MaxIterNode, BetterOrEqualNode
    
    ast = AlgorithmNode(
        init_phase=InitPhaseNode(DSATURNode()),
        search_phases=[],
        termination=MaxIterNode(10),
        acceptance=BetterOrEqualNode()
    )
    
    config = Configuration(ast=ast)
    
    # Evaluate
    evaluator = ConfigurationEvaluator([instance])
    fitness_scores = evaluator.evaluate(config)
    
    print(f"Fitness scores: {fitness_scores}")
    print(f"Average: {sum(fitness_scores.values()) / len(fitness_scores):.2f}")
