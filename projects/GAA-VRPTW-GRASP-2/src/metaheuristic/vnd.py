"""
Variable Neighborhood Descent (VND) for VRPTW

Advanced local search strategy that switches between different neighborhoods.
When a neighborhood reaches local optimum, VND tries the next neighborhood.
More effective than single-neighborhood local search.
"""

from typing import List, Type, Optional
from copy import deepcopy

from src.core import Solution
from src.operators.base import (
    LocalSearchIntraOperator,
    LocalSearchInterOperator,
)


class VariableNeighborhoodDescent:
    """
    Variable Neighborhood Descent (VND) for local search.
    
    Strategy:
    1. Try neighborhood k
    2. If improvement found: restart from neighborhood 1
    3. If no improvement: move to neighborhood k+1
    4. Stop when all neighborhoods exhausted
    
    This explores different neighborhood structures, more robust than single operator.
    """
    
    def __init__(
        self,
        neighborhoods: Optional[List[Type]] = None,
        verbose: bool = False,
    ):
        """
        Initialize VND.
        
        Args:
            neighborhoods: List of neighborhood/operator classes to use
                          (default: TwoOpt, OrOpt, Relocate, SwapCustomers)
            verbose: Print search progress
        """
        self.verbose = verbose
        
        if neighborhoods is None:
            # Import here to avoid circular imports
            from src.operators import TwoOpt, OrOpt, Relocate, SwapCustomers
            neighborhoods = [TwoOpt, OrOpt, Relocate, SwapCustomers]
        
        self.neighborhoods = neighborhoods
        self.search_log = []
    
    def search(self, solution: Solution) -> Solution:
        """
        Run VND on solution.
        
        Args:
            solution: Initial solution
            
        Returns:
            Improved solution (local optimum w.r.t. VND neighborhoods)
        """
        current = deepcopy(solution)
        self.search_log = []
        
        if self.verbose:
            print(f"    VND starting from K={current.num_vehicles}, D={current.total_distance:.2f}")
        
        k = 0  # Neighborhood index
        iteration = 0
        
        while k < len(self.neighborhoods):
            iteration += 1
            
            # Get operator class and instantiate
            operator_class = self.neighborhoods[k]
            operator = operator_class()
            
            if self.verbose:
                print(f"      [{iteration}] Trying {operator.name}...", end=" ")
            
            # Try to improve using this neighborhood
            improved = operator.apply(current)
            
            # Check if improvement
            if improved.fitness < current.fitness:
                old_fitness = current.fitness
                current = improved
                
                if self.verbose:
                    print(f"[OK] Improved: {old_fitness} -> {current.fitness}")
                
                # Log improvement
                self.search_log.append({
                    'iteration': iteration,
                    'operator': operator.name,
                    'old_fitness': old_fitness,
                    'new_fitness': current.fitness,
                    'improved': True,
                })
                
                # Restart from first neighborhood
                k = 0
            else:
                if self.verbose:
                    print(f"[NO] No improvement")
                
                # Log no improvement
                self.search_log.append({
                    'iteration': iteration,
                    'operator': operator.name,
                    'fitness': current.fitness,
                    'improved': False,
                })
                
                # Move to next neighborhood
                k += 1
        
        if self.verbose:
            print(f"    VND complete: K={current.num_vehicles}, D={current.total_distance:.2f}")
        
        return current
    
    def search_with_shaking(
        self,
        solution: Solution,
        perturbation_operator,
        max_iterations: int = 10,
    ) -> Solution:
        """
        VND with periodic shaking (for Iterated Local Search).
        
        Occasionally apply perturbation to escape local optima.
        
        Args:
            solution: Initial solution
            perturbation_operator: Operator to apply for shaking
            max_iterations: Maximum shaking iterations
            
        Returns:
            Improved solution
        """
        best = deepcopy(solution)
        
        for shake_iter in range(max_iterations):
            # Shake current solution
            shaken = perturbation_operator.apply(deepcopy(best))
            
            # Apply VND to shaken solution
            improved = self.search(shaken)
            
            # Accept if better than best (simple accept)
            if improved.fitness < best.fitness:
                best = improved
                if self.verbose:
                    print(f"  Shake {shake_iter}: Accepted improvement")
        
        return best


class FirstImprovementVND(VariableNeighborhoodDescent):
    """
    VND with first-improvement strategy (vs best-improvement).
    
    Faster variant that accepts first improving move,
    rather than searching for best move in each neighborhood.
    """
    
    def search(self, solution: Solution) -> Solution:
        """
        Run first-improvement VND.
        
        Args:
            solution: Initial solution
            
        Returns:
            Improved solution
        """
        # Same as standard VND since operators already implement
        # first/best improvement internally
        return super().search(solution)
