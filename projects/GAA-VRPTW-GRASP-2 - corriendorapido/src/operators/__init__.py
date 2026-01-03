"""
Operators Module for VRPTW

Comprehensive collection of 22 domain operators:
- 6 Constructive operators
- 4 Intra-route local search
- 4 Inter-route local search
- 4 Perturbation operators
- 3 Repair operators

All operators follow the BaseOperator interface and can be combined
in variable neighborhood search, GRASP, iterated local search, etc.
"""

# Base classes
from src.operators.base import (
    BaseOperator,
    ConstructiveOperator,
    LocalSearchIntraOperator,
    LocalSearchInterOperator,
    PerturbationOperator,
    RepairOperator,
)

# Constructive operators
from src.operators.constructive import (
    SavingsHeuristic,
    NearestNeighbor,
    TimeOrientedNN,
    InsertionI1,
    RegretInsertion,
    RandomizedInsertion,
)

# Intra-route local search
from src.operators.local_search_intra import (
    TwoOpt,
    OrOpt,
    Relocate,
    ThreeOpt,
)

# Inter-route local search
from src.operators.local_search_inter import (
    CrossExchange,
    TwoOptStar,
    SwapCustomers,
    RelocateInter,
)

# Perturbation
from src.operators.perturbation import (
    EjectionChain,
    RuinRecreate,
    RandomRemoval,
    RouteElimination,
)

# Repair
from src.operators.perturbation import (
    RepairCapacity,
    RepairTimeWindows,
    GreedyRepair,
)

__all__ = [
    # Base classes
    'BaseOperator',
    'ConstructiveOperator',
    'LocalSearchIntraOperator',
    'LocalSearchInterOperator',
    'PerturbationOperator',
    'RepairOperator',
    
    # Constructive (6)
    'SavingsHeuristic',
    'NearestNeighbor',
    'TimeOrientedNN',
    'InsertionI1',
    'RegretInsertion',
    'RandomizedInsertion',
    
    # Intra-route (4)
    'TwoOpt',
    'OrOpt',
    'Relocate',
    'ThreeOpt',
    
    # Inter-route (4)
    'CrossExchange',
    'TwoOptStar',
    'SwapCustomers',
    'RelocateInter',
    
    # Perturbation (4)
    'EjectionChain',
    'RuinRecreate',
    'RandomRemoval',
    'RouteElimination',
    
    # Repair (3)
    'RepairCapacity',
    'RepairTimeWindows',
    'GreedyRepair',
]

# Convenient groupings for VND and algorithm design
CONSTRUCTIVE_OPERATORS = [
    SavingsHeuristic,
    NearestNeighbor,
    TimeOrientedNN,
    InsertionI1,
    RegretInsertion,
    RandomizedInsertion,
]

LOCAL_SEARCH_INTRA = [
    TwoOpt,
    OrOpt,
    Relocate,
    ThreeOpt,
]

LOCAL_SEARCH_INTER = [
    CrossExchange,
    TwoOptStar,
    SwapCustomers,
    RelocateInter,
]

PERTURBATION_OPERATORS = [
    EjectionChain,
    RuinRecreate,
    RandomRemoval,
    RouteElimination,
]

REPAIR_OPERATORS = [
    RepairCapacity,
    RepairTimeWindows,
    GreedyRepair,
]

# All operators
ALL_OPERATORS = (
    CONSTRUCTIVE_OPERATORS +
    LOCAL_SEARCH_INTRA +
    LOCAL_SEARCH_INTER +
    PERTURBATION_OPERATORS +
    REPAIR_OPERATORS
)

OPERATOR_COUNTS = {
    'constructive': len(CONSTRUCTIVE_OPERATORS),
    'local_search_intra': len(LOCAL_SEARCH_INTRA),
    'local_search_inter': len(LOCAL_SEARCH_INTER),
    'perturbation': len(PERTURBATION_OPERATORS),
    'repair': len(REPAIR_OPERATORS),
    'total': len(ALL_OPERATORS),
}
