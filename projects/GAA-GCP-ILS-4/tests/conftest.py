"""
tests/conftest.py
Configuración y fixtures compartidas para la suite de tests

Fixtures globales:
    - simple_graph: Grafo pequeño para tests rápidos
    - bipartite_graph: Grafo bipartito (2 colores)
    - complete_graph: Grafo completo (n colores)

Configuración:
    - Paths a datasets
    - Parámetros de prueba
"""

import pytest
import numpy as np
from pathlib import Path


# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Directorio de datasets (relativo al proyecto)
DATASETS_DIR = Path(__file__).parent.parent / "datasets"

# Parámetros de prueba
QUICK_TEST_TIMEOUT = 10  # segundos
DEFAULT_SEED = 42


# ============================================================================
# FIXTURES COMPARTIDAS - GRAFOS SIMPLES
# ============================================================================

@pytest.fixture(scope="session")
def simple_triangle():
    """
    Fixture: Triángulo (3 vértices, 3 aristas, requiere 3 colores)
    
    Estructura:
        1 -- 2
        |  /
        | /
        3
    
    Óptimo: 3 colores
    """
    return {
        "vertices": 3,
        "edges": [(1, 2), (2, 3), (1, 3)],
        "colors_known": 3,
        "name": "triangle",
    }


@pytest.fixture(scope="session")
def bipartite_cycle_4():
    """
    Fixture: Ciclo de 4 vértices (bipartito, requiere 2 colores)
    
    Estructura:
        1 -- 2
        |    |
        4 -- 3
    
    Óptimo: 2 colores
    """
    return {
        "vertices": 4,
        "edges": [(1, 2), (2, 3), (3, 4), (4, 1)],
        "colors_known": 2,
        "name": "bipartite_4",
    }


@pytest.fixture(scope="session")
def square_with_diagonal():
    """
    Fixture: Cuadrado con diagonal (requiere 3 colores)
    
    Estructura:
        1 -- 2
        |\   |
        | \ |
        4 --3
    
    Óptimo: 3 colores (arista (1,3) lo hace no bipartito)
    """
    return {
        "vertices": 4,
        "edges": [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)],
        "colors_known": 3,
        "name": "square_diagonal",
    }


@pytest.fixture(scope="session")
def complete_graph_4():
    """
    Fixture: Grafo completo K4 (4 vértices conectados, requiere 4 colores)
    
    Estructura:
        Todos los vértices están conectados entre sí
    
    Óptimo: 4 colores
    """
    return {
        "vertices": 4,
        "edges": [
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)
        ],
        "colors_known": 4,
        "name": "complete_4",
    }


@pytest.fixture(scope="session")
def petersen_graph():
    """
    Fixture: Grafo de Petersen (10 vértices, requiere 3 colores)
    
    Nota: Implementación simplificada
    Óptimo: 3 colores
    """
    return {
        "vertices": 10,
        "edges": [
            # Pentágono exterior
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
            # Pentágono interior
            (6, 7), (7, 8), (8, 9), (9, 10), (10, 6),
            # Conexiones radiales (saltan 2 vértices)
            (1, 7), (2, 8), (3, 9), (4, 10), (5, 6),
        ],
        "colors_known": 3,
        "name": "petersen",
    }


# ============================================================================
# FIXTURES COMPARTIDAS - OBJETOS DEL MODELO
# ============================================================================

@pytest.fixture(scope="function")
def simple_problem(simple_triangle):
    """Fixture: Crear un GraphColoringProblem simple"""
    try:
        from core.problem import GraphColoringProblem
        return GraphColoringProblem(
            vertices=simple_triangle["vertices"],
            edges=simple_triangle["edges"],
            colors_known=simple_triangle["colors_known"]
        )
    except ImportError:
        pytest.skip("core.problem no implementado aún")


@pytest.fixture(scope="function")
def simple_solution(simple_problem):
    """Fixture: Crear una ColoringSolution válida para triángulo"""
    try:
        from core.solution import ColoringSolution
        # Asignar colores diferentes a cada vértice
        assignment = {1: 0, 2: 1, 3: 2}
        return ColoringSolution(assignment=assignment)
    except ImportError:
        pytest.skip("core.solution no implementado aún")


@pytest.fixture(scope="function")
def invalid_solution():
    """Fixture: Crear una ColoringSolution inválida (vértices adyacentes mismo color)"""
    try:
        from core.solution import ColoringSolution
        # Vértices 1 y 2 están adyacentes pero tienen el mismo color
        assignment = {1: 0, 2: 0, 3: 1}
        return ColoringSolution(assignment=assignment)
    except ImportError:
        pytest.skip("core.solution no implementado aún")


# ============================================================================
# FIXTURES COMPARTIDAS - EVALUADOR
# ============================================================================

@pytest.fixture(scope="function")
def evaluator():
    """Fixture: Obtener instancia del evaluador"""
    try:
        from core.evaluation import ColoringEvaluator
        return ColoringEvaluator()
    except ImportError:
        pytest.skip("core.evaluation no implementado aún")


# ============================================================================
# FIXTURES COMPARTIDAS - OPERADORES
# ============================================================================

@pytest.fixture(scope="function")
def constructive_operator():
    """Fixture: Obtener operador constructivo GreedyDSATUR"""
    try:
        from operators.constructive import GreedyDSATUR
        return GreedyDSATUR
    except ImportError:
        pytest.skip("operators.constructive no implementado aún")


@pytest.fixture(scope="function")
def improvement_operator():
    """Fixture: Obtener operador de mejora KempeChain"""
    try:
        from operators.improvement import KempeChain
        return KempeChain
    except ImportError:
        pytest.skip("operators.improvement no implementado aún")


@pytest.fixture(scope="function")
def perturbation_operator():
    """Fixture: Obtener operador de perturbación RandomRecolor"""
    try:
        from operators.perturbation import RandomRecolor
        return RandomRecolor
    except ImportError:
        pytest.skip("operators.perturbation no implementado aún")


# ============================================================================
# FIXTURES COMPARTIDAS - METAHEURÍSTICA
# ============================================================================

@pytest.fixture(scope="function")
def ils_algorithm():
    """Fixture: Obtener instancia de ILS"""
    try:
        from metaheuristic.ils_core import IteratedLocalSearch
        from operators.constructive import GreedyDSATUR
        from operators.improvement import KempeChain
        from operators.perturbation import RandomRecolor
        
        return IteratedLocalSearch(
            constructive=GreedyDSATUR,
            improvement=KempeChain,
            perturbation=RandomRecolor,
            max_iterations=50
        )
    except ImportError:
        pytest.skip("metaheuristic o operators no implementados aún")


# ============================================================================
# HOOKS Y CONFIGURACIÓN
# ============================================================================

def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Agregar markers personalizados
    config.addinivalue_line(
        "markers", "slow: tests que tardan más de 5 segundos"
    )
    config.addinivalue_line(
        "markers", "requires_dimacs: tests que necesitan archivos DIMACS"
    )
    config.addinivalue_line(
        "markers", "parametrize_graphs: tests parametrizados con múltiples grafos"
    )


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Fixture: Resetear seed de NumPy antes de cada test"""
    np.random.seed(DEFAULT_SEED)
    yield
    # Limpiar después del test (opcional)


@pytest.fixture(scope="session")
def setup_test_environment():
    """Fixture: Configurar ambiente de tests al inicio"""
    # Verificar que los directorios existen
    if not DATASETS_DIR.exists():
        print(f"Advertencia: Directorio de datasets no encontrado: {DATASETS_DIR}")
    
    yield
    
    # Cleanup al final de la sesión (si es necesario)


# ============================================================================
# FIXTURES PARAMETRIZADAS
# ============================================================================

@pytest.fixture(
    params=[
        "simple_triangle",
        "bipartite_cycle_4",
        "square_with_diagonal",
    ],
    ids=["3-colors", "2-colors", "3-colors"],
)
def various_graphs(request):
    """Fixture parametrizada: Múltiples grafos para pruebas"""
    graphs = {
        "simple_triangle": {
            "vertices": 3,
            "edges": [(1, 2), (2, 3), (1, 3)],
            "colors_known": 3,
        },
        "bipartite_cycle_4": {
            "vertices": 4,
            "edges": [(1, 2), (2, 3), (3, 4), (4, 1)],
            "colors_known": 2,
        },
        "square_with_diagonal": {
            "vertices": 4,
            "edges": [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)],
            "colors_known": 3,
        },
    }
    return graphs[request.param]


# ============================================================================
# UTILIDADES
# ============================================================================

def get_dimacs_file(filename):
    """Obtener ruta a archivo DIMACS"""
    return DATASETS_DIR / filename


def assert_solution_feasible(solution, problem):
    """Utilidad: Verificar que una solución es factible"""
    assert solution.is_feasible(problem), \
        f"Solución no es factible: {solution.num_conflicts(problem)} conflictos"


def assert_colors_within_bounds(solution, problem):
    """Utilidad: Verificar que número de colores está dentro de cotas"""
    assert solution.num_colors <= problem.upper_bound, \
        f"Número de colores {solution.num_colors} > cota superior {problem.upper_bound}"
    
    assert solution.num_colors >= problem.colors_known if problem.colors_known else True, \
        f"Número de colores {solution.num_colors} < óptimo conocido {problem.colors_known}"


# ============================================================================
# INFORMACIÓN DE DEBUG
# ============================================================================

def pytest_sessionstart(session):
    """Información al iniciar la sesión de tests"""
    print(f"\n{'='*70}")
    print(f"  SUITE DE TESTS - GCP con ILS")
    print(f"{'='*70}")
    print(f"Datasets directory: {DATASETS_DIR}")
    print(f"Random seed: {DEFAULT_SEED}")
    print(f"{'='*70}\n")
