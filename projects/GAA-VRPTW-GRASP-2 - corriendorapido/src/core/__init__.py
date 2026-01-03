"""
Core VRPTW Components

Exports:
- Models: Customer, Route, Instance, Solution
- Loader: SolomonLoader for benchmark instances
- Evaluation: Route/solution evaluation functions
- BKS: Best Known Solutions manager
"""

from .models import Customer, Route, Instance, Solution
from .loader import SolomonLoader
from .evaluation import (
    calculate_route_distance,
    calculate_route_time,
    check_capacity_constraint,
    check_time_window_constraint,
    evaluate_route,
    evaluate_solution,
    fitness_function,
    compare_solutions,
    validate_solution_against_bks,
)
from .bks import BKSManager

__all__ = [
    # Models
    'Customer',
    'Route',
    'Instance',
    'Solution',
    
    # Loader
    'SolomonLoader',
    
    # Evaluation functions
    'calculate_route_distance',
    'calculate_route_time',
    'check_capacity_constraint',
    'check_time_window_constraint',
    'evaluate_route',
    'evaluate_solution',
    'fitness_function',
    'compare_solutions',
    'validate_solution_against_bks',
    
    # BKS
    'BKSManager',
]
