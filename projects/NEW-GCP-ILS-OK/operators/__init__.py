"""
Operators for Graph Coloring Problem

Modulo que contiene todos los operadores para el problema GCP:
- Constructivos: Generan soluciones iniciales
- Mejora: Busqueda local
- Perturbacion: Escapar de optimos locales
- Reparacion: Arreglar soluciones infeasibles
"""

from operators.constructive import (
    GreedyDSATUR,
    GreedyLargestFirst,
    RandomSequential,
)

from operators.improvement import (
    KempeChainMove,
    OneVertexMove,
    TabuColMove,
)

from operators.perturbation import (
    RandomRecolor,
    PartialDestroy,
    ColorClassMerge,
    AdaptivePerturbation,
)

from operators.repair import (
    GreedyRepair,
    ConflictMinimizingRepair,
    ConstraintPropagationRepair,
    BacktrackingRepair,
)

__all__ = [
    # Constructive
    "GreedyDSATUR",
    "GreedyLargestFirst",
    "RandomSequential",
    # Improvement
    "KempeChainMove",
    "OneVertexMove",
    "TabuColMove",
    # Perturbation
    "RandomRecolor",
    "PartialDestroy",
    "ColorClassMerge",
    "AdaptivePerturbation",
    # Repair
    "GreedyRepair",
    "ConflictMinimizingRepair",
    "ConstraintPropagationRepair",
    "BacktrackingRepair",
]
