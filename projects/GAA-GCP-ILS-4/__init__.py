"""
GCP-ILS: Graph Coloring Problem con Iterated Local Search

Un proyecto de investigación en optimización combinatoria usando Generación
Automática de Algoritmos (GAA).

Estructura:
    - core/: Componentes fundamentales (problema, solución, evaluador)
    - operators/: Operadores de búsqueda
    - metaheuristic/: Algoritmos (ILS)
    - config/: Configuración centralizada
    - tests/: Suite de tests
    - scripts/: Scripts ejecutables
    - utils/: Utilidades

Uso:
    >>> from core import GraphColoringProblem, ColoringSolution
    >>> problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    >>> print(problem.summary())

Documentación:
    Ver problema_metaheuristica.md para especificación técnica completa.
"""

__version__ = "1.0.0"
__author__ = "GCP-ILS Project Team"
__license__ = "MIT"

from core import (
    GraphColoringProblem,
    ColoringSolution,
    ColoringEvaluator,
)

__all__ = [
    "GraphColoringProblem",
    "ColoringSolution",
    "ColoringEvaluator",
]
