"""
Metaheuristic algorithms for VRPTW.

Implements three levels of sophistication:
1. GRASP: Greedy Randomized Adaptive Search (pure constructive + local search)
2. ILS: Iterated Local Search (GRASP + perturbation + acceptance)
3. Hybrid GRASP-ILS: Combines GRASP exploration with ILS refinement
"""

from .grasp import GRASP
from .vnd import VariableNeighborhoodDescent, FirstImprovementVND
from .ils import IteratedLocalSearch, HybridGRASP_ILS

__all__ = [
    'GRASP',
    'VariableNeighborhoodDescent',
    'FirstImprovementVND',
    'IteratedLocalSearch',
    'HybridGRASP_ILS',
]

# Common metaheuristic configurations
METAHEURISTIC_CLASSES = {
    'grasp': GRASP,
    'ils': IteratedLocalSearch,
    'hybrid': HybridGRASP_ILS,
}

METAHEURISTIC_DEFAULT_PARAMS = {
    'grasp': {
        'alpha': 0.15,
        'max_iterations': 100,
        'max_iterations_no_improvement': 20,
        'seed': None,
        'verbose': False,
    },
    'ils': {
        'acceptance_criterion': 'better',
        'perturbation_strength': 5,
        'max_iterations': 100,
        'max_perturbations_no_improvement': 20,
        'seed': None,
        'verbose': False,
    },
    'hybrid': {
        'grasp_iterations': 20,
        'ils_iterations': 50,
        'alpha': 0.15,
        'seed': None,
        'verbose': False,
    },
}
