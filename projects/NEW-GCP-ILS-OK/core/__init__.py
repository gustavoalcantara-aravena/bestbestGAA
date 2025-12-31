"""
Core module exports

Exporta las clases principales del modulo core
"""

from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator

__all__ = [
    'GraphColoringProblem',
    'ColoringSolution',
    'ColoringEvaluator'
]
