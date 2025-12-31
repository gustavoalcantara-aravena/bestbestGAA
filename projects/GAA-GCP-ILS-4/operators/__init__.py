"""
Operadores del Dominio - Graph Coloring Problem

Módulo que agrupa todos los operadores para GCP:
- Constructivos: Generar soluciones iniciales
- Mejora: Búsqueda local (movimientos)
- Perturbación: Escapar de óptimos locales
- Reparación: Convertir infactibles a factibles
"""

from .constructive import (
    GreedyDSATUR,
    GreedyLF,
    RandomSequential,
    compare_constructives
)

from .improvement import (
    KempeChain,
    OneVertexMove,
    TabuCol
)

from .perturbation import (
    RandomRecolor,
    PartialDestroy,
    AdaptivePerturbation
)

from .repair import (
    RepairConflicts,
    IntensifyColor,
    Diversify
)

__all__ = [
    # Constructivos
    'GreedyDSATUR',
    'GreedyLF',
    'RandomSequential',
    'compare_constructives',
    
    # Mejora
    'KempeChain',
    'OneVertexMove',
    'TabuCol',
    
    # Perturbación
    'RandomRecolor',
    'PartialDestroy',
    'AdaptivePerturbation',
    
    # Reparación
    'RepairConflicts',
    'IntensifyColor',
    'Diversify',
]
