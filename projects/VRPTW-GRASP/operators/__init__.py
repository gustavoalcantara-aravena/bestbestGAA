"""
VRPTW-GRASP Operators Module

Proporciona todos los operadores de construcción, búsqueda local, perturbación y reparación.
"""

from operators.constructive import (
    NearestNeighbor, SavingsHeuristic, NearestInsertion,
    RandomizedInsertion, TimeOrientedNN, RegretInsertion,
    get_constructive_operator
)

from operators.local_search import (
    TwoOpt, OrOpt, ThreeOpt, Relocate,
    CrossExchange, TwoOptStar, RelocateIntRoute, SwapCustomers,
    get_local_search_operator
)

from operators.perturbation import (
    EjectionChain, RuinRecreate, RandomRemoval, RouteElimination,
    get_perturbation_operator
)

from operators.repair import (
    CapacityRepair, TimeWindowRepair, HybridRepair,
    get_repair_operator
)

__all__ = [
    # Constructive
    'NearestNeighbor', 'SavingsHeuristic', 'NearestInsertion',
    'RandomizedInsertion', 'TimeOrientedNN', 'RegretInsertion',
    # Local Search
    'TwoOpt', 'OrOpt', 'ThreeOpt', 'Relocate',
    'CrossExchange', 'TwoOptStar', 'RelocateIntRoute', 'SwapCustomers',
    # Perturbation
    'EjectionChain', 'RuinRecreate', 'RandomRemoval', 'RouteElimination',
    # Repair
    'CapacityRepair', 'TimeWindowRepair', 'HybridRepair',
    # Factories
    'get_constructive_operator', 'get_local_search_operator',
    'get_perturbation_operator', 'get_repair_operator',
]
