#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAA Executor - Real ILS execution for GCP instances

Executes the actual Iterated Local Search algorithm on GCP instances
using the problem_gcp.py module for evaluation.

THIS EXECUTES REAL ALGORITHM, NOT SIMULATION.
"""

import sys
import time
import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional, Optional

# Add 04-Generated/scripts to path (from project root)
project_root = Path(__file__).parent.parent
gaa_scripts = project_root / "04-Generated" / "scripts"
sys.path.insert(0, str(gaa_scripts))

try:
    from ast_evaluator import InstanceLoader
    from problem_gcp import Graph, GCProblem
except ImportError as e:
    print(f"[ERROR] Could not import GAA modules: {e}")
    print(f"        Expected location: {gaa_scripts}")
    print("        Make sure 04-Generated/scripts/ exists and is accessible")
    sys.exit(1)


class GreedyColorer:
    """Greedy coloring heuristic for initial solution"""
    
    @staticmethod
    def color(graph: Graph) -> List[int]:
        """
        Color graph using greedy largest-first algorithm.
        
        Returns:
            Coloring vector where coloring[v] = color of vertex v
        """
        n = graph.n
        coloring = [-1] * n
        
        # Get vertices sorted by degree (largest first for better results)
        vertices = sorted(range(n), key=lambda v: graph.get_degree(v), reverse=True)
        
        for v in vertices:
            # Find minimum color not used by neighbors
            neighbor_colors = set()
            for u in graph.get_neighbors(v):
                if coloring[u] != -1:
                    neighbor_colors.add(coloring[u])
            
            # Assign smallest available color
            color = 0
            while color in neighbor_colors:
                color += 1
            coloring[v] = color
        
        return coloring


class LocalSearchImprover:
    """Local search to improve existing colorings"""
    
    @staticmethod
    def improve_by_vertex_moves(coloring: List[int], graph: Graph, 
                                problem: GCProblem, max_moves: int = 100) -> List[int]:
        """
        Improve coloring by trying to move vertices to different colors
        """
        best_coloring = coloring.copy()
        best_fitness = problem.evaluate(best_coloring)
        n = len(coloring)
        
        for _ in range(max_moves):
            # Random vertex
            v = random.randint(0, n - 1)
            
            # Try different colors
            neighbor_colors = {best_coloring[u] for u in graph.get_neighbors(v)}
            max_color = max(best_coloring)
            
            # Try unused colors and color+1
            possible_colors = [c for c in range(max_color + 2) 
                              if c not in neighbor_colors]
            
            if possible_colors:
                new_color = random.choice(possible_colors)
                candidate = best_coloring.copy()
                candidate[v] = new_color
                
                candidate_fitness = problem.evaluate(candidate)
                if candidate_fitness < best_fitness:
                    best_coloring = candidate
                    best_fitness = candidate_fitness
        
        return best_coloring


class GAAExecutor:
    """Execute REAL ILS algorithm on GCP instances"""
    
    def __init__(self, dataset_dir: str = "datasets"):
        self.dataset_dir = Path(dataset_dir)
        self.loader = InstanceLoader()
        self.current_instance = None
        self.current_graph = None
        self.current_problem = None
        self.current_result = None
    
    def load_instance(self, family: str, instance_name: str) -> bool:
        """Load a GCP instance from file"""
        instance_path = self.dataset_dir / family / f"{instance_name}.col"
        
        if not instance_path.exists():
            print(f"[ERROR] Instance file not found: {instance_path}")
            return False
        
        try:
            # Load using InstanceLoader (DIMACS format)
            self.current_instance = self.loader.load_instance(str(instance_path))
            
            # Create Graph object from loaded instance
            self.current_graph = Graph(
                self.current_instance.num_vertices,
                self.current_instance.edges
            )
            
            # Create Problem object for evaluation
            self.current_problem = GCProblem(self.current_graph)
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load instance: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def execute_ils(self, max_iterations: int = 100, timeout: float = 60.0) -> Dict[str, Any]:
        """
        Execute REAL Iterated Local Search algorithm on current instance.
        
        This is NOT a simulation - it runs actual algorithm with real graph data.
        
        Returns:
            Dictionary with execution results including chromatic_number from real ILS
        """
        if self.current_instance is None or self.current_problem is None:
            raise RuntimeError("No instance loaded. Call load_instance() first.")
        
        instance_name = self.current_instance.name
        num_vertices = self.current_instance.num_vertices
        num_edges = self.current_instance.num_edges
        
        print(f"[GAA] REAL ILS EXECUTION")
        print(f"[GAA] Instance: {instance_name}")
        print(f"[GAA] Vertices: {num_vertices}")
        print(f"[GAA] Edges: {num_edges}")
        print(f"[GAA] Running algorithm...")
        print()
        
        start_time = time.time()
        
        # PHASE 1: Get initial solution using greedy coloring
        print(f"   [PHASE 1] Greedy initial coloring...")
        try:
            initial_coloring = GreedyColorer.color(self.current_graph)
            initial_fitness = self.current_problem.evaluate(initial_coloring)
            initial_chromatic = self.current_problem.num_colors(initial_coloring)
            
            best_coloring = initial_coloring.copy()
            best_fitness = initial_fitness
            best_chromatic = initial_chromatic
            
            print(f"            Initial chromatic: {best_chromatic}")
            print(f"            Initial fitness: {best_fitness:.1f}")
        except Exception as e:
            print(f"   [ERROR] Initial coloring failed: {e}")
            return {'instance': instance_name, 'status': 'error', 'error': str(e)}
        
        iteration = 0
        improvements = 0
        
        try:
            for iteration in range(1, max_iterations + 1):
                # Check timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    print(f"[GAA] Timeout reached ({timeout}s)")
                    break
                
                # PHASE 2: Local search - improve current solution
                current_coloring = best_coloring.copy()
                current_coloring = LocalSearchImprover.improve_by_vertex_moves(
                    current_coloring, self.current_graph, self.current_problem,
                    max_moves=num_vertices
                )
                
                current_fitness = self.current_problem.evaluate(current_coloring)
                current_chromatic = self.current_problem.num_colors(current_coloring)
                
                # Update best if improved
                if current_fitness < best_fitness:
                    best_coloring = current_coloring.copy()
                    best_fitness = current_fitness
                    best_chromatic = current_chromatic
                    improvements += 1
                    
                    if iteration % 5 == 0:
                        print(f"   [Iter {iteration:3d}] IMPROVEMENT: chromatic={best_chromatic}, "
                              f"fitness={best_fitness:.1f}")
                
                # Progress report every 20 iterations
                if iteration % 20 == 0:
                    elapsed = time.time() - start_time
                    print(f"   [Iter {iteration:3d}] Time: {elapsed:.1f}s, "
                          f"Best chromatic: {best_chromatic}, Fitness: {best_fitness:.1f}")
                
                # PHASE 3: Perturbation to escape local optima
                if iteration % 5 == 0:
                    best_coloring = self._perturb_solution(best_coloring)
        
        except KeyboardInterrupt:
            print("[GAA] Interrupted by user")
        
        elapsed = time.time() - start_time
        
        # Validate final solution
        is_feasible = self.current_problem.is_feasible(best_coloring)
        conflicts = self.current_problem.count_conflicts(best_coloring)
        
        # Build result with REAL chromatic number from ILS execution
        result = {
            'instance': instance_name,
            'vertices': num_vertices,
            'edges': num_edges,
            'iterations': iteration,
            'improvements': improvements,
            'elapsed_time': elapsed,
            'chromatic_number': best_chromatic,  # REAL from ILS algorithm
            'best_fitness': float(best_fitness),  # Actual fitness = k + penalty*conflicts
            'num_colors': best_chromatic,
            'conflicts': conflicts,
            'feasible': is_feasible,
            'status': 'completed' if is_feasible else 'infeasible_warn'
        }
        
        print(f"\n[GAA] REAL ILS COMPLETE")
        print(f"      Iterations: {iteration}")
        print(f"      Improvements: {improvements}")
        print(f"      Time: {elapsed:.2f}s")
        print(f"      *** CHROMATIC NUMBER: {result['chromatic_number']} ***")
        print(f"      Feasible: {is_feasible}")
        print(f"      Conflicts: {conflicts}")
        
        self.current_result = result
        return result
    
    def _perturb_solution(self, coloring: List[int]) -> List[int]:
        """
        Perturbation: randomly reassign colors to escape local optima
        """
        perturbed = coloring.copy()
        n = len(coloring)
        num_to_perturb = max(1, n // 8)  # Perturb ~12.5% of vertices
        
        for _ in range(num_to_perturb):
            v = random.randint(0, n - 1)
            # Assign random color (0 to max+1)
            perturbed[v] = random.randint(0, max(coloring) + 1)
        
        return perturbed
    
    def execute_batch(self, family: str, instances: list, max_iterations: int = 50) -> list:
        """
        Execute REAL ILS on multiple instances
        
        Args:
            family: Dataset family name
            instances: List of instance names
            max_iterations: Max iterations per instance
            
        Returns:
            List of results with REAL chromatic numbers
        """
        results = []
        
        for i, instance_name in enumerate(instances, 1):
            print(f"\n{'='*70}")
            print(f"[BATCH] Instance {i}/{len(instances)}: {instance_name}")
            print(f"{'='*70}\n")
            
            # Load and execute REAL algorithm
            if self.load_instance(family, instance_name):
                try:
                    result = self.execute_ils(max_iterations=max_iterations, timeout=30.0)
                    results.append(result)
                except Exception as e:
                    print(f"[ERROR] Execution failed: {e}")
                    import traceback
                    traceback.print_exc()
                    results.append({
                        'instance': instance_name,
                        'status': 'error',
                        'error': str(e)
                    })
            else:
                results.append({
                    'instance': instance_name,
                    'status': 'load_error'
                })
        
        return results


def main():
    """Example usage"""
    executor = GAAExecutor()
    
    # Example: Run on CUL family, flat300_20_0 instance
    print("[GAA] Executor initialized")
    print()
    
    if executor.load_instance("CUL", "flat300_20_0"):
        result = executor.execute_ils(max_iterations=50, timeout=10.0)
        print(f"\nResult: {json.dumps(result, indent=2)}")
    else:
        print("[ERROR] Could not load instance")


if __name__ == '__main__':
    main()
