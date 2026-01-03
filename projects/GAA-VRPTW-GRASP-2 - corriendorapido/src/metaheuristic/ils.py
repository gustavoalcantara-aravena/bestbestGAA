"""
Iterated Local Search (ILS) for VRPTW

Combines GRASP with perturbations and acceptance criteria to escape local optima.
More sophisticated than pure GRASP, maintains search diversity over multiple restarts.

Standard ILS structure:
1. Generate initial solution (or GRASP)
2. Apply local search
3. Perturb solution
4. Apply local search to perturbed solution
5. Accept or reject based on criterion
6. Repeat from step 3
"""

import random
import time
from typing import Optional, Type, List, Tuple, Callable
from copy import deepcopy

from src.core import Instance, Solution
from src.operators.base import PerturbationOperator
from src.operators import (
    RuinRecreate,
    RandomRemoval,
    RouteElimination,
)
from src.metaheuristic.grasp import GRASP
from src.metaheuristic.vnd import VariableNeighborhoodDescent


class IteratedLocalSearch:
    """
    Iterated Local Search (ILS) metaheuristic for VRPTW.
    
    Combines local search with perturbation to escape local optima.
    More sophisticated search than GRASP alone, maintains diversity.
    """
    
    def __init__(
        self,
        grasp: Optional[GRASP] = None,
        perturbation_operator: Optional[PerturbationOperator] = None,
        vnd: Optional[VariableNeighborhoodDescent] = None,
        acceptance_criterion: str = "better",  # "better" or "accept_probability"
        perturbation_strength: int = 5,  # For RandomRemoval: k customers
        max_iterations: int = 100,
        max_perturbations_no_improvement: int = 20,
        seed: Optional[int] = None,
        verbose: bool = False,
    ):
        """
        Initialize ILS.
        
        Args:
            grasp: GRASP instance for initial solution (default: create one)
            perturbation_operator: Perturbation operator class (default RuinRecreate)
            vnd: VND instance for local search (default: create one)
            acceptance_criterion: "better" (deterministic) or "probability" (stochastic)
            perturbation_strength: Strength of perturbation (depends on operator)
            max_iterations: Maximum ILS iterations
            max_perturbations_no_improvement: Stop if no improvement for this many perturbations
            seed: Random seed
            verbose: Print progress
        """
        self.verbose = verbose
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        # Initialize GRASP if not provided
        self.grasp = grasp or GRASP(
            alpha=0.15,
            max_iterations=10,  # Fewer GRASP iterations in ILS context
            seed=seed,
            verbose=False,
        )
        
        # Initialize perturbation operator
        self.perturbation_operator = perturbation_operator or RuinRecreate(destroy_ratio=0.2)
        self.perturbation_strength = perturbation_strength
        
        # Initialize VND
        self.vnd = vnd or VariableNeighborhoodDescent(verbose=False)
        
        # Acceptance criterion
        self.acceptance_criterion = acceptance_criterion
        self.max_iterations = max_iterations
        self.max_perturbations_no_improvement = max_perturbations_no_improvement
        
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
        Run ILS algorithm.
        
        Args:
            instance: VRPTW problem instance
            time_limit: Maximum execution time in seconds
            
        Returns:
            Tuple of (best_solution, fitness, stats)
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  Iterated Local Search for {instance.name}")
            print(f"  Perturbation: {self.perturbation_operator.name}")
            print(f"{'='*60}")
        
        start_time = time.time()
        
        # Phase 1: Get initial solution using GRASP
        if self.verbose:
            print(f"  Generating initial solution with GRASP...")
        
        self.best_solution, self.best_fitness, _ = self.grasp.solve(
            instance,
            time_limit=time_limit * 0.1 if time_limit else None,
        )
        
        self.iteration_log = []
        perturbations_no_improvement = 0
        
        # Phase 2: Iterated perturbation + local search
        for iteration in range(self.max_iterations):
            elapsed_time = time.time() - start_time
            
            # Check time limit
            if time_limit is not None and elapsed_time > time_limit:
                if self.verbose:
                    print(f"⏱️  Time limit reached ({elapsed_time:.2f}s)")
                break
            
            # Perturb current best solution
            perturbed = self.perturbation_operator.apply(deepcopy(self.best_solution))
            
            # Apply local search to perturbed solution
            improved = self.vnd.search(perturbed)
            
            # Acceptance criterion
            accept = self._accept_solution(improved)
            
            # Update best if improvement
            improved_best = False
            if improved.fitness < self.best_fitness:
                self.best_solution = deepcopy(improved)
                self.best_fitness = improved.fitness
                perturbations_no_improvement = 0
                improved_best = True
            elif accept:
                # Accept non-improving solution (diversification)
                self.best_solution = deepcopy(improved)
                perturbations_no_improvement += 1
            else:
                perturbations_no_improvement += 1
            
            # Log iteration
            self.iteration_log.append({
                'iteration': iteration,
                'solution_fitness': improved.fitness,
                'best_fitness': self.best_fitness,
                'accepted': accept,
                'improved': improved_best,
                'time': elapsed_time,
            })
            
            if self.verbose:
                status = "[OK]" if improved_best else ("[OK]" if accept else "[NO]")
                print(f"  [{iteration+1:3d}] K={improved.num_vehicles}, D={improved.total_distance:.2f}  " +
                      f"Best: K={self.best_fitness[0]}, D={self.best_fitness[1]:.2f}  " +
                      f"[{status}]  ({elapsed_time:.2f}s)")
            
            # Early stopping
            if perturbations_no_improvement >= self.max_perturbations_no_improvement:
                if self.verbose:
                    print(f"[STOP] No improvement for {self.max_perturbations_no_improvement} perturbations")
                break
        
        elapsed_time = time.time() - start_time
        
        stats = {
            'total_iterations': len(self.iteration_log),
            'total_time': elapsed_time,
            'best_fitness': self.best_fitness,
            'num_vehicles': self.best_fitness[0],
            'total_distance': self.best_fitness[1],
        }
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  ILS Completed")
            print(f"  Best Solution: K={self.best_fitness[0]}, D={self.best_fitness[1]:.2f}")
            print(f"  Time: {elapsed_time:.2f}s, Iterations: {stats['total_iterations']}")
            print(f"{'='*60}\n")
        
        return self.best_solution, self.best_fitness, stats
    
    def _accept_solution(self, solution: Solution) -> bool:
        """
        Acceptance criterion for non-improving solutions.
        
        Args:
            solution: New solution
            
        Returns:
            True if solution should be accepted, False otherwise
        """
        if self.acceptance_criterion == "better":
            # Only accept improving solutions (deterministic)
            return solution.fitness < self.best_fitness
        
        elif self.acceptance_criterion == "probability":
            # Accept with probability (Metropolis-like)
            if solution.fitness < self.best_fitness:
                return True  # Always accept improving
            
            # Calculate acceptance probability based on fitness degradation
            k_worse = solution.num_vehicles - self.best_fitness[0]
            d_worse = solution.total_distance - self.best_fitness[1]
            
            # Normalize degradation to probability
            penalty = k_worse * 1000 + d_worse  # K is primary objective
            temperature = 100.0  # Acceptance temperature
            probability = min(1.0, 1.0 / (1.0 + penalty / temperature))
            
            return random.random() < probability
        
        else:
            raise ValueError(f"Unknown acceptance criterion: {self.acceptance_criterion}")


class HybridGRASP_ILS:
    """
    Hybrid approach: GRASP for initial solution + ILS for refinement.
    
    Combines fast GRASP iterations with deeper ILS exploration.
    """
    
    def __init__(
        self,
        grasp_iterations: int = 20,
        ils_iterations: int = 50,
        alpha: float = 0.15,
        seed: Optional[int] = None,
        verbose: bool = False,
    ):
        """
        Initialize hybrid GRASP-ILS.
        
        Args:
            grasp_iterations: GRASP iterations in first phase
            ils_iterations: ILS iterations in second phase
            alpha: GRASP alpha parameter
            seed: Random seed
            verbose: Print progress
        """
        self.grasp_iterations = grasp_iterations
        self.ils_iterations = ils_iterations
        self.alpha = alpha
        self.seed = seed
        self.verbose = verbose
    
    def solve(
        self,
        instance: Instance,
        time_limit: Optional[float] = None,
    ) -> Tuple[Solution, Tuple[int, float], dict]:
        """
        Run hybrid GRASP-ILS.
        
        Args:
            instance: VRPTW problem instance
            time_limit: Maximum execution time
            
        Returns:
            Tuple of (best_solution, fitness, stats)
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  Hybrid GRASP-ILS for {instance.name}")
            print(f"  GRASP: {self.grasp_iterations} iter, ILS: {self.ils_iterations} iter")
            print(f"{'='*60}")
        
        start_time = time.time()
        
        # Phase 1: GRASP
        if self.verbose:
            print(f"\n  Phase 1: GRASP ({self.grasp_iterations} iterations)")
        
        grasp = GRASP(
            alpha=self.alpha,
            max_iterations=self.grasp_iterations,
            seed=self.seed,
            verbose=self.verbose,
        )
        
        time_remaining = time_limit - (time.time() - start_time) if time_limit else None
        best_solution, best_fitness, grasp_stats = grasp.solve(instance, time_limit=time_remaining)
        
        # Phase 2: ILS for refinement
        if self.verbose:
            print(f"\n  Phase 2: ILS ({self.ils_iterations} iterations)")
        
        ils = IteratedLocalSearch(
            grasp=GRASP(
                alpha=self.alpha,
                max_iterations=1,  # Minimal GRASP in ILS
                seed=self.seed,
            ),
            max_iterations=self.ils_iterations,
            verbose=self.verbose,
        )
        
        time_remaining = time_limit - (time.time() - start_time) if time_limit else None
        final_solution, final_fitness, ils_stats = ils.solve(instance, time_limit=time_remaining)
        
        elapsed_time = time.time() - start_time
        
        stats = {
            'total_time': elapsed_time,
            'grasp_stats': grasp_stats,
            'ils_stats': ils_stats,
            'best_fitness': final_fitness,
            'num_vehicles': final_fitness[0],
            'total_distance': final_fitness[1],
        }
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  Hybrid GRASP-ILS Completed")
            print(f"  Best Solution: K={final_fitness[0]}, D={final_fitness[1]:.2f}")
            print(f"  Time: {elapsed_time:.2f}s")
            print(f"{'='*60}\n")
        
        return final_solution, final_fitness, stats
