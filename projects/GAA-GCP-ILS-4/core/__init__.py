"""
core/__init__.py
Módulo Core: Componentes fundamentales del GCP-ILS

Contiene:
    - GraphColoringProblem: Representación de instancias
    - ColoringSolution: Representación de soluciones
    - ColoringEvaluator: Evaluación de soluciones
"""

from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator, compare_solutions

__version__ = "1.0.0"
__author__ = "GCP-ILS Project"

__all__ = [
    "GraphColoringProblem",
    "ColoringSolution",
    "ColoringEvaluator",
    "compare_solutions",
]
