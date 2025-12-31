"""
tests/__init__.py
Paquete de tests para GCP-ILS

Módulos:
    - test_core: Tests de Core (problema, solución, evaluador)
    - test_operators: Tests de operadores (constructivos, mejora, perturbación)
    - test_ils: Tests de ILS (inicialización, ejecución, convergencia)

Uso:
    pytest tests/ -v                    # Ejecutar todos
    pytest tests/test_core.py -v        # Solo Core
    pytest tests/test_operators.py -v   # Solo Operadores
    pytest tests/test_ils.py -v         # Solo ILS
"""

__version__ = "1.0.0"
__author__ = "GCP-ILS Project"
__all__ = [
    "test_core",
    "test_operators",
    "test_ils",
]
