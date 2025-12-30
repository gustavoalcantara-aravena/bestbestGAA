"""
ILS Core - Iterated Local Search para Graph Coloring Problem

Metaheurística ILS con estructura:
1. Initial Solution: Generar solución inicial con constructiva
2. Local Search: Mejorar con local search
3. Perturbation: Perturbar para escapar óptimos locales
4. Termination: Reiniciar o terminar
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from time import time

try:
    from ..core.problem import GraphColoringProblem
    from ..core.solution import ColoringSolution
    from ..core.evaluation import ColoringEvaluator
    from ..operators.constructive import get_constructive
    from ..operators.local_search import get_local_search
    from ..operators.perturbation import get_perturbation
    from ..operators.repair import get_repair
except ImportError:
    from core.problem import GraphColoringProblem
    from core.solution import ColoringSolution
    from core.evaluation import ColoringEvaluator
    from operators.constructive import get_constructive
    from operators.local_search import get_local_search
    from operators.perturbation import get_perturbation
    from operators.repair import get_repair


class IteratedLocalSearch:
    """
    Algoritmo Iterated Local Search para Graph Coloring.
    
    Parámetros principales:
    - constructive: Operador constructivo ('dsatur', 'lf', 'sl', 'rs', 'rlf')
    - local_search: Operador local search ('kempe', 'tabu', 'ovm', 'swap')
    - perturbation: Operador de perturbación ('random_recolor', 'partial_destroy')
    - max_iterations: Máximo de iteraciones principales
    - perturbation_strength: Fracción de vértices a perturbar (0.0-1.0)
    - restart_threshold: Iteraciones sin mejora antes de reiniciar
    """
    
    def __init__(self,
                 problem: GraphColoringProblem,
                 constructive: str = 'dsatur',
                 local_search: str = 'kempe',
                 perturbation: str = 'random_recolor',
                 max_iterations: int = 500,
                 perturbation_strength: float = 0.2,
                 restart_threshold: int = 50,
                 seed: int = None,
                 verbose: bool = False):
        """
        Inicializa ILS.
        
        Args:
            problem: Instancia del problema
            constructive: Nombre del operador constructivo
            local_search: Nombre del operador local search
            perturbation: Nombre del operador de perturbación
            max_iterations: Máximo de iteraciones
            perturbation_strength: Intensidad de perturbación
            restart_threshold: Iteraciones sin mejora para reiniciar
            seed: Semilla aleatoria
            verbose: Modo verboso
        """
        self.problem = problem
        self.evaluator = ColoringEvaluator(problem)
        
        # Operadores
        self.constructive_class = get_constructive(constructive)
        self.local_search_class = get_local_search(local_search)
        self.perturbation_class = get_perturbation(perturbation)
        self.repair_class = get_repair('backtrack')  # Usar backtrack por defecto
        
        # Parámetros
        self.max_iterations = max_iterations
        self.perturbation_strength = perturbation_strength
        self.restart_threshold = restart_threshold
        self.verbose = verbose
        
        # RNG
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        # Estadísticas
        self.best_solution = None
        self.best_k = float('inf')
        self.iteration_history = []
        self.start_time = None
        self.end_time = None
    
    def run(self) -> Tuple[ColoringSolution, Dict]:
        """
        Ejecuta el algoritmo ILS.
        
        Returns:
            (best_solution, statistics)
        """
        self.start_time = time()
        
        if self.verbose:
            print(f"ILS para Graph Coloring (n={self.problem.n}, m={self.problem.m})")
            print(f"Constructive: {self.constructive_class.__name__}")
            print(f"Local Search: {self.local_search_class.__name__}")
            print(f"Perturbation: {self.perturbation_class.__name__}")
            print("=" * 60)
        
        # Generar solución inicial
        current = self._construct_initial_solution()
        current = self.repair_class.repair(current, self.problem, rng=self.rng)
        
        # Mejorar solución inicial
        current = self._local_search(current)
        
        # Actualizar mejor
        if current.num_colors < self.best_k:
            self.best_solution = current.copy()
            self.best_k = self.best_solution.num_colors
            if self.verbose:
                print(f"Iter 0: Initial k={self.best_k}")
        
        # Loop principal ILS
        iterations_without_improvement = 0
        
        for iteration in range(1, self.max_iterations + 1):
            # Perturbar solución actual
            perturbed = self._perturb(current)
            
            # Mejorar solución perturbada
            candidate = self._local_search(perturbed)
            
            # Aceptar? (criterio: mejor o igual que actual)
            if self.evaluator.is_better(candidate, current):
                current = candidate
            
            # Actualizar mejor solución global
            if candidate.num_colors < self.best_k:
                self.best_solution = candidate.copy()
                self.best_k = self.best_solution.num_colors
                iterations_without_improvement = 0
                
                if self.verbose:
                    elapsed = time() - self.start_time
                    print(f"Iter {iteration}: k={self.best_k} (t={elapsed:.2f}s)")
            else:
                iterations_without_improvement += 1
            
            # Guardar en historial
            self.iteration_history.append({
                'iteration': iteration,
                'best_k': self.best_k,
                'current_k': current.num_colors,
                'time': time() - self.start_time
            })
            
            # Reiniciar si sin mejora
            if iterations_without_improvement >= self.restart_threshold:
                if self.verbose:
                    print(f"Iter {iteration}: Restart (no improvement for {self.restart_threshold} iters)")
                
                current = self._construct_initial_solution()
                current = self.repair_class.repair(current, self.problem, rng=self.rng)
                current = self._local_search(current)
                iterations_without_improvement = 0
        
        self.end_time = time()
        
        stats = self._get_statistics()
        
        if self.verbose:
            print("=" * 60)
            print(f"Final: k={self.best_k}")
            print(f"Total time: {stats['total_time']:.2f}s")
            print(f"Iterations: {stats['iterations_completed']}")
        
        return self.best_solution, stats
    
    def _construct_initial_solution(self) -> ColoringSolution:
        """Genera solución inicial"""
        return self.constructive_class.build(
            self.problem,
            rng=self.rng
        )
    
    def _local_search(self, solution: ColoringSolution) -> ColoringSolution:
        """Aplica local search a una solución"""
        return self.local_search_class.improve(
            solution,
            self.problem,
            max_iterations=100,
            rng=self.rng
        )
    
    def _perturb(self, solution: ColoringSolution) -> ColoringSolution:
        """Perturba una solución"""
        perturbed = self.perturbation_class.perturb(
            solution,
            self.problem,
            perturbation_rate=self.perturbation_strength,
            rng=self.rng
        )
        
        # Reparar si es necesario
        perturbed = self.repair_class.repair(
            perturbed,
            self.problem,
            rng=self.rng
        )
        
        return perturbed
    
    def _get_statistics(self) -> Dict:
        """Compila estadísticas de la ejecución"""
        return {
            'best_k': self.best_k,
            'total_time': self.end_time - self.start_time,
            'iterations_completed': len(self.iteration_history),
            'lower_bound': self.problem.lower_bound,
            'upper_bound': self.evaluator.get_upper_bound(),
            'gap_to_lower': self.best_k - self.problem.lower_bound if self.problem.lower_bound else None,
            'optimality_gap': self.evaluator.optimality_gap(self.best_k),
            'history': self.iteration_history
        }
    
    def summary(self) -> str:
        """Retorna resumen de ejecución"""
        stats = self._get_statistics()
        
        summary = f"""
ILS Execution Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Problem:              {self.problem.name} (n={self.problem.n}, m={self.problem.m})
Best k found:         {stats['best_k']}
Total time:           {stats['total_time']:.2f}s
Iterations:           {stats['iterations_completed']}
        """
        
        if self.problem.optimal_value:
            gap_pct = ((self.best_k - self.problem.optimal_value) / 
                       self.problem.optimal_value * 100)
            summary += f"""Optimal k:            {self.problem.optimal_value}
Gap %:                {gap_pct:.2f}%
        """
        
        summary += f"""Lower bound:          {stats['lower_bound']}
Upper bound:          {stats['upper_bound']}
Gap to lower:         {stats['gap_to_lower']}
        """
        
        return summary
