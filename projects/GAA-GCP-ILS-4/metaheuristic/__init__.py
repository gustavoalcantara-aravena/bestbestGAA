"""
Metaheurística: Iterated Local Search para Graph Coloring Problem

Módulo que implementa el algoritmo ILS y estrategias de perturbación.
"""

from .ils_core import (
    IteratedLocalSearch,
    AdaptiveILS,
    ILSHistory
)

from .perturbation_schedules import (
    PerturbationSchedule,
    ConstantPerturbation,
    LinearPerturbation,
    ExponentialPerturbation,
    DynamicPerturbation,
    CyclicalPerturbation,
    AdaptiveTemperaturePerturbation,
    HybridPerturbation,
    create_schedule
)

__all__ = [
    # ILS
    'IteratedLocalSearch',
    'AdaptiveILS',
    'ILSHistory',
    
    # Perturbation Schedules
    'PerturbationSchedule',
    'ConstantPerturbation',
    'LinearPerturbation',
    'ExponentialPerturbation',
    'DynamicPerturbation',
    'CyclicalPerturbation',
    'AdaptiveTemperaturePerturbation',
    'HybridPerturbation',
    'create_schedule',
]
