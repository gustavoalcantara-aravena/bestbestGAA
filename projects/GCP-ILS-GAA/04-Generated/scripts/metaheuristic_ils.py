"""
Auto-generated Metaheuristic Module for GCP-ILS-GAA

Generated from:
  - projects/GCP-ILS-GAA/00-Core/Metaheuristic.md
  - Metaheuristic: Iterated Local Search (ILS)
  - Problem: Graph Coloring Problem (GCP)
  - Version: 1.0.0

This module provides:
  - ILS algorithm implementation
  - Local search strategies
  - Perturbation operators
  - Acceptance criteria
"""

import random
import time
from typing import List, Tuple, Dict, Callable, Optional
import math

from problem_gcp import GCProblem, Graph


class ILSParameters:
    """Configuration parameters for ILS algorithm."""
    
    def __init__(
        self,
        max_iterations: int = 500,
        local_search_iterations: int = 100,
        perturbation_strength: float = 0.2,
        restart_threshold: int = 50,
        restart_intensity: float = 0.5,
        constructive_heuristic: str = "DSATUR",
        acceptance_criterion: str = "better_or_equal",
        temperature: float = 0.1,
        seed: Optional[int] = None,
    ):
        """
        Initialize ILS parameters.
        
        Args:
            max_iterations: Maximum number of main iterations
            local_search_iterations: Max iterations per local search phase
            perturbation_strength: Fraction of vertices to perturb [0, 1]
            restart_threshold: Iterations without improvement before restart
            restart_intensity: Intensity multiplier for restart perturbation
            constructive_heuristic: Initial solution builder (DSATUR, LF, SL, etc.)
            acceptance_criterion: Acceptance strategy (better_or_equal, metropolis)
            temperature: Temperature parameter for Metropolis criterion
            seed: Random seed for reproducibility
        """
        self.max_iterations = max_iterations
        self.local_search_iterations = local_search_iterations
        self.perturbation_strength = perturbation_strength
        self.restart_threshold = restart_threshold
        self.restart_intensity = restart_intensity
        self.constructive_heuristic = constructive_heuristic
        self.acceptance_criterion = acceptance_criterion
        self.temperature = temperature
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
    
    def __repr__(self):
        return (
            f"ILSParameters(max_iter={self.max_iterations}, "
            f"ls_iter={self.local_search_iterations}, "
            f"strength={self.perturbation_strength})"
        )


class ILSExecutionLog:
    """Tracks execution statistics of ILS algorithm."""
    
    def __init__(self):
        self.iterations = []
        self.k_values = []
        self.conflict_values = []
        self.times = []
        self.best_k = float('inf')
        self.best_iteration = 0
        self.start_time = None
        self.end_time = None
    
    def record_iteration(
        self,
        iteration: int,
        k: int,
        conflicts: int,
        elapsed_time: float,
    ):
        """Record metrics for current iteration."""
        self.iterations.append(iteration)
        self.k_values.append(k)
        self.conflict_values.append(conflicts)
        self.times.append(elapsed_time)
        
        if k < self.best_k:
            self.best_k = k
            self.best_iteration = iteration
    
    @property
    def total_time(self) -> float:
        """Total execution time."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def __repr__(self):
        return (
            f"ILSLog(iterations={len(self.iterations)}, "
            f"best_k={self.best_k}, best_at={self.best_iteration}, "
            f"time={self.total_time:.2f}s)"
        )


class ILS:
    """
    Iterated Local Search (ILS) for Graph Coloring Problem.
    
    Algorithm:
    1. Construct initial solution
    2. Apply local search
    3. Repeat:
        a. Perturb current solution
        b. Apply local search
        c. Accept or reject based on criterion
    4. Return best solution found
    """
    
    def __init__(self, problem: GCProblem, params: ILSParameters = None):
        """
        Initialize ILS solver.
        
        Args:
            problem: GCProblem instance
            params: ILSParameters (default values if None)
        """
        self.problem = problem
        self.params = params or ILSParameters()
        self.log = ILSExecutionLog()
    
    def construct_initial_solution(self) -> List[int]:
        """
        Construct initial solution using specified heuristic.
        
        Returns:
            Initial coloring (feasible)
        """
        if self.params.constructive_heuristic == "DSATUR":
            return self._greedy_dsatur()
        elif self.params.constructive_heuristic in ["LF", "LargestFirst"]:
            return self._greedy_largest_first()
        elif self.params.constructive_heuristic in ["SL", "SmallestLast"]:
            return self._greedy_smallest_last()
        else:
            return self._random_sequential_coloring()
    
    def _greedy_dsatur(self) -> List[int]:
        """
        Greedy DSATUR (Degree of Saturation) heuristic.
        
        Selects uncolored vertex with maximum saturation degree
        (most distinct colors in neighbors) and assigns smallest
        available color.
        """
        coloring = [-1] * self.problem.n
        saturation = [set() for _ in range(self.problem.n)]
        
        # Phase 1: Color first vertex (highest degree)
        max_degree_vertex = max(range(self.problem.n), 
                                 key=lambda v: self.problem.graph.get_degree(v))
        coloring[max_degree_vertex] = 1
        
        # Update saturation of neighbors
        for neighbor in self.problem.graph.get_neighbors(max_degree_vertex):
            saturation[neighbor].add(1)
        
        # Phase 2: Color remaining vertices
        for _ in range(self.problem.n - 1):
            # Find uncolored vertex with maximum saturation
            uncolored = [v for v in range(self.problem.n) if coloring[v] == -1]
            if not uncolored:
                break
            
            max_sat_vertex = max(uncolored, 
                                  key=lambda v: (len(saturation[v]), 
                                                  self.problem.graph.get_degree(v)))
            
            # Find smallest available color
            available_colors = set()
            color = 1
            while len(available_colors) == 0:
                if color not in saturation[max_sat_vertex]:
                    coloring[max_sat_vertex] = color
                    available_colors.add(color)
                color += 1
            
            # Update saturation of neighbors
            for neighbor in self.problem.graph.get_neighbors(max_sat_vertex):
                saturation[neighbor].add(coloring[max_sat_vertex])
        
        # Color any uncolored vertices (safety)
        for v in range(self.problem.n):
            if coloring[v] == -1:
                for color in range(1, self.problem.n + 1):
                    if all(coloring[u] != color for u in self.problem.graph.get_neighbors(v)):
                        coloring[v] = color
                        break
                if coloring[v] == -1:
                    coloring[v] = self.problem.n
        
        return coloring
    
    def _greedy_largest_first(self) -> List[int]:
        """
        Greedy Largest First heuristic.
        
        Orders vertices by decreasing degree and colors sequentially
        with smallest available color.
        """
        # Sort vertices by degree (descending)
        sorted_vertices = sorted(range(self.problem.n),
                                  key=lambda v: self.problem.graph.get_degree(v),
                                  reverse=True)
        
        coloring = [0] * self.problem.n
        
        for vertex in sorted_vertices:
            # Find smallest available color
            neighbor_colors = {coloring[u] for u in self.problem.graph.get_neighbors(vertex)
                               if coloring[u] > 0}
            
            color = 1
            while color in neighbor_colors:
                color += 1
            
            coloring[vertex] = color
        
        return coloring
    
    def _greedy_smallest_last(self) -> List[int]:
        """
        Greedy Smallest Last (by Matula & Beck).
        
        Recursively removes minimum degree vertex and colors in reverse order.
        """
        # Compute ordering (not fully recursive for efficiency)
        ordering = []
        remaining = set(range(self.problem.n))
        degrees_copy = self.problem.graph.degrees.copy()
        
        while remaining:
            # Find minimum degree vertex
            min_vertex = min(remaining, key=lambda v: degrees_copy[v])
            ordering.append(min_vertex)
            remaining.remove(min_vertex)
            
            # Update degrees
            for neighbor in self.problem.graph.get_neighbors(min_vertex):
                if neighbor in remaining:
                    degrees_copy[neighbor] -= 1
        
        # Color in reverse order
        coloring = [0] * self.problem.n
        for vertex in reversed(ordering):
            neighbor_colors = {coloring[u] for u in self.problem.graph.get_neighbors(vertex)}
            
            color = 1
            while color in neighbor_colors:
                color += 1
            
            coloring[vertex] = color
        
        return coloring
    
    def _random_sequential_coloring(self) -> List[int]:
        """Random sequential coloring."""
        ordering = list(range(self.problem.n))
        random.shuffle(ordering)
        
        coloring = [0] * self.problem.n
        for vertex in ordering:
            neighbor_colors = {coloring[u] for u in self.problem.graph.get_neighbors(vertex)}
            
            color = 1
            while color in neighbor_colors:
                color += 1
            
            coloring[vertex] = color
        
        return coloring
    
    def local_search(self, coloring: List[int], max_iterations: int = None) -> List[int]:
        """
        Apply local search using Kempe chain moves.
        
        Tries to reduce k by exchanging colors via Kempe chains.
        
        Args:
            coloring: Current coloring
            max_iterations: Maximum iterations (default from params)
        
        Returns:
            Improved coloring
        """
        if max_iterations is None:
            max_iterations = self.params.local_search_iterations
        
        coloring = coloring.copy()
        improved = True
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = False
            k_before = self.problem.num_colors(coloring)
            
            # Try Kempe chain moves to reduce k
            for c1 in range(1, k_before + 1):
                for c2 in range(c1 + 1, k_before + 1):
                    coloring_new = self._kempe_chain_move(coloring, c1, c2)
                    
                    if (self.problem.is_feasible(coloring_new) and
                        self.problem.num_colors(coloring_new) < k_before):
                        coloring = coloring_new
                        improved = True
                        break
                
                if improved:
                    break
            
            iteration += 1
        
        return coloring
    
    def _kempe_chain_move(self, coloring: List[int], c1: int, c2: int) -> List[int]:
        """
        Apply Kempe chain move: swap colors c1 and c2 along alternating path.
        
        Simplified: just swap all instances of c1 with c2.
        """
        coloring_new = coloring.copy()
        for v in range(self.problem.n):
            if coloring_new[v] == c1:
                coloring_new[v] = c2
            elif coloring_new[v] == c2:
                coloring_new[v] = c1
        
        # Normalize colors (remove gaps)
        coloring_new = self._normalize_colors(coloring_new)
        
        return coloring_new
    
    def _normalize_colors(self, coloring: List[int]) -> List[int]:
        """
        Normalize coloring to use colors 1, 2, 3, ... without gaps.
        """
        colors_used = sorted(set(coloring))
        color_map = {old: new for new, old in enumerate(colors_used, 1)}
        
        return [color_map[c] for c in coloring]
    
    def perturbation(self, coloring: List[int], intensity: float = 1.0) -> List[int]:
        """
        Perturb coloring by randomly recoloring vertices.
        
        Args:
            coloring: Current coloring
            intensity: Intensity multiplier for perturbation strength
        
        Returns:
            Perturbed coloring (may be infeasible)
        """
        coloring_pert = coloring.copy()
        k = self.problem.num_colors(coloring)
        
        # Number of vertices to perturb
        n_perturb = max(1, int(self.problem.n * self.params.perturbation_strength * intensity))
        
        # Select random vertices
        vertices_to_perturb = random.sample(range(self.problem.n), n_perturb)
        
        # Recolor randomly
        for v in vertices_to_perturb:
            new_color = random.randint(1, k + 1)
            coloring_pert[v] = new_color
        
        # Repair conflicts
        coloring_pert = self._repair_conflicts(coloring_pert)
        
        return coloring_pert
    
    def _repair_conflicts(self, coloring: List[int]) -> List[int]:
        """
        Repair conflicting edges by recoloring vertices.
        """
        coloring = coloring.copy()
        
        for u, v in self.problem.graph.edges:
            if coloring[u] == coloring[v]:
                # Recolor vertex v to smallest available color
                neighbor_colors = {coloring[w] for w in self.problem.graph.get_neighbors(v)}
                
                color = 1
                while color in neighbor_colors:
                    color += 1
                
                coloring[v] = color
        
        return self._normalize_colors(coloring)
    
    def accept_solution(
        self,
        s_current: List[int],
        s_candidate: List[int],
        s_best: List[int],
    ) -> Tuple[bool, List[int]]:
        """
        Apply acceptance criterion.
        
        Args:
            s_current: Current solution
            s_candidate: Candidate solution (after perturbation + LS)
            s_best: Best solution found so far
        
        Returns:
            (accept: bool, new_current_solution: List[int])
        """
        if self.params.acceptance_criterion == "better_or_equal":
            f_current = self.problem.evaluate(s_current)
            f_candidate = self.problem.evaluate(s_candidate)
            
            if f_candidate <= f_current:
                return True, s_candidate
            else:
                return False, s_current
        
        elif self.params.acceptance_criterion == "metropolis":
            f_current = self.problem.evaluate(s_current)
            f_candidate = self.problem.evaluate(s_candidate)
            
            if f_candidate <= f_current:
                return True, s_candidate
            else:
                delta = f_candidate - f_current
                p_accept = math.exp(-delta / self.params.temperature)
                if random.random() < p_accept:
                    return True, s_candidate
                else:
                    return False, s_current
        
        else:  # Default: better_or_equal
            f_current = self.problem.evaluate(s_current)
            f_candidate = self.problem.evaluate(s_candidate)
            return f_candidate <= f_current, s_candidate
    
    def solve(self, time_limit: Optional[float] = None) -> Tuple[List[int], ILSExecutionLog]:
        """
        Solve GCP using ILS algorithm.
        
        Args:
            time_limit: Maximum execution time in seconds (optional)
        
        Returns:
            (best_coloring, execution_log)
        """
        self.log = ILSExecutionLog()
        self.log.start_time = time.time()
        
        # Step 1: Construct initial solution
        s_best = self.construct_initial_solution()
        s_current = s_best.copy()
        
        iterations_without_improvement = 0
        
        # Step 2: Main loop
        for iteration in range(self.params.max_iterations):
            # Check time limit
            if time_limit and time.time() - self.log.start_time > time_limit:
                break
            
            # Check restart condition
            if iterations_without_improvement >= self.params.restart_threshold:
                # Restart with perturbation
                intensity = self.params.restart_intensity
                s_current = self.perturbation(s_best, intensity=intensity)
                s_current = self.local_search(s_current)
                iterations_without_improvement = 0
            else:
                # Normal ILS step
                s_pert = self.perturbation(s_current)
                s_cand = self.local_search(s_pert)
                
                # Acceptance criterion
                accept, s_current = self.accept_solution(s_current, s_cand, s_best)
                
                # Update best solution
                if self.problem.evaluate(s_current) < self.problem.evaluate(s_best):
                    s_best = s_current.copy()
                    iterations_without_improvement = 0
                else:
                    iterations_without_improvement += 1
            
            # Log iteration
            elapsed = time.time() - self.log.start_time
            k = self.problem.num_colors(s_best)
            conflicts = self.problem.count_conflicts(s_best)
            self.log.record_iteration(iteration, k, conflicts, elapsed)
        
        self.log.end_time = time.time()
        
        return s_best, self.log
    
    def get_summary(self) -> Dict:
        """Get summary of execution."""
        return {
            'best_k': self.log.best_k,
            'best_iteration': self.log.best_iteration,
            'total_iterations': len(self.log.iterations),
            'total_time': self.log.total_time,
            'avg_k': sum(self.log.k_values) / len(self.log.k_values) if self.log.k_values else 0,
        }


# Example usage
if __name__ == "__main__":
    # Create simple problem
    graph = Graph(5, edges=[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
    problem = GCProblem(graph)
    
    # Create solver
    params = ILSParameters(
        max_iterations=100,
        local_search_iterations=50,
        perturbation_strength=0.2,
    )
    
    solver = ILS(problem, params)
    
    # Solve
    coloring, log = solver.solve()
    
    print(f"Best coloring: {coloring}")
    print(f"Number of colors: {problem.num_colors(coloring)}")
    print(f"Feasible: {problem.is_feasible(coloring)}")
    print(f"Execution log: {log}")
    print(f"Summary: {solver.get_summary()}")
