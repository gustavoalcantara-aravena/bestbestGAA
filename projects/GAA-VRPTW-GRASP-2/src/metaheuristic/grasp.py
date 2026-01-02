"""
GRASP (Greedy Randomized Adaptive Search Procedure) for VRPTW

Two-phase metaheuristic:
1. Greedy Randomized Construction: Build solution using RCL (Restricted Candidate List)
2. Local Search: Improve via variable neighborhood descent

Parameters:
- alpha: RCL threshold (0.15 recommended for VRPTW)
- max_iterations: Number of GRASP iterations (default 100)
- constructor: Constructive operator (default RandomizedInsertion)
"""

import random
import time
from typing import Optional, Tuple, Type, List
from copy import deepcopy

from src.core import Instance, Solution
from src.operators.base import ConstructiveOperator, LocalSearchIntraOperator
from src.operators import RandomizedInsertion, TwoOpt, OrOpt, Relocate, SwapCustomers
from src.operators.perturbation import RepairTimeWindows, RepairCapacity


class GRASP:
    """
    GRASP metaheuristic for VRPTW.
    
    Balances greediness and randomness through RCL (Restricted Candidate List)
    parameter alpha and iterates between construction and local search.
    """
    
    def __init__(
        self,
        alpha: float = 0.15,
        max_iterations: int = 100,
        max_iterations_no_improvement: int = 20,
        constructor: Optional[ConstructiveOperator] = None,
        local_search_ops: Optional[List[Type[LocalSearchIntraOperator]]] = None,
        seed: Optional[int] = None,
        verbose: bool = False,
    ):
        """
        Initialize GRASP.
        
        Args:
            alpha: RCL parameter (0-1). Controls randomness in construction.
                   0=greedy pure, 1=random pure, 0.15=recommended
            max_iterations: Maximum GRASP iterations
            max_iterations_no_improvement: Stop if no improvement for this many iterations
            constructor: Constructive operator (default RandomizedInsertion with alpha)
            local_search_ops: List of local search operator classes for VND
            seed: Random seed for reproducibility
            verbose: Print progress information
        """
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.max_iterations_no_improvement = max_iterations_no_improvement
        self.verbose = verbose
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        # Default constructor: RandomizedInsertion with alpha parameter
        self.constructor = constructor or RandomizedInsertion(alpha=alpha, seed=seed)
        
        # Default local search operators (in VND order)
        self.local_search_ops = local_search_ops or [
            TwoOpt,
            OrOpt,
            Relocate,
            SwapCustomers,
        ]
        
        # Statistics
        self.best_solution = None
        self.best_fitness = None
        self.iteration_log = []
    
    def solve(
        self,
        instance: Instance,
        time_limit: Optional[float] = None,
    ) -> Tuple[Solution, Tuple[int, float], dict]:
        """
        Run GRASP algorithm.
        
        Args:
            instance: VRPTW problem instance
            time_limit: Maximum execution time in seconds (optional)
            
        Returns:
            Tuple of:
            - best_solution: Best solution found
            - fitness: (K, D) tuple
            - stats: Statistics dictionary
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  GRASP for {instance.name}")
            print(f"  α={self.alpha}, max_iter={self.max_iterations}")
            print(f"{'='*60}")
        
        start_time = time.time()
        self.best_solution = None
        self.best_fitness = (float('inf'), float('inf'))
        self.iteration_log = []
        
        iterations_no_improvement = 0
        
        for iteration in range(self.max_iterations):
            elapsed_time = time.time() - start_time
            
            # Check time limit
            if time_limit is not None and elapsed_time > time_limit:
                if self.verbose:
                    print(f"⏱️  Time limit reached ({elapsed_time:.2f}s)")
                break
            
            # Phase 1: Greedy Randomized Construction
            solution = self._construct_solution(instance)
            
            # Ensure feasibility
            if not solution.feasible:
                solution = self._repair_solution(solution)
            
            # Phase 2: Local Search (VND)
            solution = self._local_search(solution)
            
            # Update best solution
            current_fitness = solution.fitness
            improved = False
            
            if current_fitness[0] < self.best_fitness[0]:
                # Improvement in K (primary objective)
                self.best_solution = deepcopy(solution)
                self.best_fitness = current_fitness
                iterations_no_improvement = 0
                improved = True
            elif (current_fitness[0] == self.best_fitness[0] and 
                  current_fitness[1] < self.best_fitness[1]):
                # Improvement in D (secondary objective)
                self.best_solution = deepcopy(solution)
                self.best_fitness = current_fitness
                iterations_no_improvement = 0
                improved = True
            else:
                iterations_no_improvement += 1
            
            # Log iteration
            self.iteration_log.append({
                'iteration': iteration,
                'solution_fitness': current_fitness,
                'best_fitness': self.best_fitness,
                'time': elapsed_time,
                'improved': improved,
            })
            
            if self.verbose:
                status = "✓" if improved else " "
                print(f"  [{iteration+1:3d}] K={current_fitness[0]}, D={current_fitness[1]:.2f}  " +
                      f"Best: K={self.best_fitness[0]}, D={self.best_fitness[1]:.2f}  [{status}]  " +
                      f"({elapsed_time:.2f}s)")
            
            # Check early stopping
            if iterations_no_improvement >= self.max_iterations_no_improvement:
                if self.verbose:
                    print(f"⏸️  No improvement for {self.max_iterations_no_improvement} iterations")
                break
        
        elapsed_time = time.time() - start_time
        
        # Statistics
        stats = {
            'total_iterations': len(self.iteration_log),
            'total_time': elapsed_time,
            'best_iteration': self._get_best_iteration(),
            'best_fitness': self.best_fitness,
            'num_vehicles': self.best_fitness[0],
            'total_distance': self.best_fitness[1],
        }
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  GRASP Completed")
            print(f"  Best Solution: K={self.best_fitness[0]}, D={self.best_fitness[1]:.2f}")
            print(f"  Time: {elapsed_time:.2f}s, Iterations: {stats['total_iterations']}")
            print(f"{'='*60}\n")
        
        return self.best_solution, self.best_fitness, stats
    
    def _construct_solution(self, instance: Instance) -> Solution:
        """
        Phase 1: Greedy randomized construction.
        
        Args:
            instance: Problem instance
            
        Returns:
            Constructed solution (may be infeasible)
        """
        return self.constructor.apply(instance)
    
    def _repair_solution(self, solution: Solution) -> Solution:
        """
        Repair infeasible solution.
        
        Args:
            solution: Potentially infeasible solution
            
        Returns:
            Feasible solution
        """
        # Repair in order of criticality
        repaired = deepcopy(solution)
        
        # First repair time windows (more critical)
        if not all(route.is_feasible for route in repaired.routes):
            repair_tw = RepairTimeWindows()
            repaired = repair_tw.apply(repaired)
        
        # Then repair capacity if needed
        if not repaired.feasible:
            repair_cap = RepairCapacity()
            repaired = repair_cap.apply(repaired)
        
        return repaired
    
    def _local_search(self, solution: Solution) -> Solution:
        """
        Phase 2: Variable Neighborhood Descent (VND).
        
        Args:
            solution: Initial solution
            
        Returns:
            Improved solution (local optimum)
        """
        current = deepcopy(solution)
        k = 0  # Neighborhood index
        
        while k < len(self.local_search_ops):
            # Instantiate operator
            operator = self.local_search_ops[k]()
            
            # Try to improve
            improved = operator.apply(current)
            
            # Check if improvement
            if improved.fitness < current.fitness:
                current = improved
                k = 0  # Restart from first neighborhood
            else:
                k += 1  # Move to next neighborhood
        
        return current
    
    def _get_best_iteration(self) -> int:
        """Get iteration number where best solution was found."""
        if not self.iteration_log:
            return 0
        
        best_fitness = self.best_fitness
        for log_entry in self.iteration_log:
            if log_entry['best_fitness'] == best_fitness:
                return log_entry['iteration'] + 1
        
        return 0
