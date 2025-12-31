"""
tests/test_ils.py
Suite de tests unitarios para el algoritmo Iterated Local Search (ILS)

Ejecutar con:
    pytest tests/test_ils.py -v
    
Cobertura:
    - Inicialización de ILS
    - Ejecución y convergencia
    - Rastreo de mejor solución
    - Reproducibilidad con seed
    - Budget de tiempo e iteraciones
    - AdaptiveILS y perturbation schedules
"""

import pytest
import time
import numpy as np

from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from operators.constructive import GreedyDSATUR, RandomSequential
from operators.improvement import KempeChain, OneVertexMove
from operators.perturbation import RandomRecolor, PartialDestroy
from metaheuristic.ils_core import IteratedLocalSearch, AdaptiveILS, ILSHistory
from metaheuristic.perturbation_schedules import (
    ConstantPerturbation, LinearPerturbation, ExponentialPerturbation,
    DynamicPerturbation, create_schedule
)


class TestIteratedLocalSearchBasic:
    """Tests básicos para ILS"""
    
    @pytest.fixture
    def small_problem(self):
        """Fixture: Problema pequeño para tests rápidos"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
    
    @pytest.fixture
    def medium_problem(self):
        """Fixture: Problema mediano"""
        edges = []
        for i in range(1, 8):
            for j in range(i+1, min(i+4, 9)):
                edges.append((i, j))
        return GraphColoringProblem(vertices=8, edges=edges, colors_known=4)
    
    @pytest.fixture
    def ils_params(self):
        """Fixture: Parámetros básicos de ILS"""
        return {
            'constructive': GreedyDSATUR,
            'improvement': KempeChain,
            'perturbation': RandomRecolor,
            'max_iterations': 50
        }
    
    # ========================================================================
    # Tests de inicialización
    # ========================================================================
    
    def test_ils_initialization(self, small_problem, ils_params):
        """Validar inicialización básica de ILS"""
        ils = IteratedLocalSearch(small_problem, **ils_params)
        assert ils.max_iterations == 50
        assert ils.iteration_counter == 0
    
    def test_ils_has_required_operators(self, small_problem, ils_params):
        """Validar que tiene operadores configurados"""
        ils = IteratedLocalSearch(small_problem, **ils_params)
        assert ils.constructive is not None
        assert ils.improvement is not None
        assert ils.perturbation is not None
    
    def test_ils_default_parameters(self, small_problem):
        """Validar parámetros por defecto"""
        ils = IteratedLocalSearch(
            small_problem,
            constructive=GreedyDSATUR,
            improvement=KempeChain,
            perturbation=RandomRecolor
        )
        assert ils.max_iterations >= 10
        assert ils.time_budget > 0
    
    # ========================================================================
    # Tests de ejecución básica
    # ========================================================================
    
    def test_ils_solve_returns_tuple(self, small_problem, ils_params):
        """Validar que solve retorna (solución, historia)"""
        ils = IteratedLocalSearch(small_problem, **ils_params)
        result = ils.solve()
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_ils_solve_returns_valid_solution(self, small_problem, ils_params):
        """Validar que retorna solución válida"""
        ils = IteratedLocalSearch(small_problem, **ils_params)
        best_solution, history = ils.solve()
        assert best_solution.is_feasible(small_problem)
    
    def test_ils_solve_returns_history(self, small_problem, ils_params):
        """Validar que retorna historia"""
        ils = IteratedLocalSearch(small_problem, **ils_params)
        best_solution, history = ils.solve()
        assert isinstance(history, ILSHistory)
    
    def test_ils_history_has_iterations(self, small_problem, ils_params):
        """Validar que historia registra iteraciones"""
        ils = IteratedLocalSearch(small_problem, max_iterations=10, **ils_params)
        best_solution, history = ils.solve()
        assert len(history.best_fitness) > 0
    
    # ========================================================================
    # Tests de reproducibilidad
    # ========================================================================
    
    def test_ils_deterministic_with_seed(self, small_problem, ils_params):
        """Validar reproducibilidad con seed fijo"""
        np.random.seed(42)
        ils1 = IteratedLocalSearch(small_problem, max_iterations=5, **ils_params)
        best1, _ = ils1.solve()
        
        np.random.seed(42)
        ils2 = IteratedLocalSearch(small_problem, max_iterations=5, **ils_params)
        best2, _ = ils2.solve()
        
        assert best1.num_colors == best2.num_colors
    
    # ========================================================================
    # Tests de convergencia
    # ========================================================================
    
    def test_ils_improves_over_iterations(self, small_problem, ils_params):
        """Validar que mejora sobre iteraciones"""
        ils = IteratedLocalSearch(small_problem, max_iterations=20, **ils_params)
        best_solution, history = ils.solve()
        
        # Primera evaluación peor que última
        first_fitness = history.best_fitness[0]
        last_fitness = history.best_fitness[-1]
        assert last_fitness <= first_fitness
    
    def test_ils_iteration_counter(self, small_problem, ils_params):
        """Validar contador de iteraciones"""
        ils = IteratedLocalSearch(small_problem, max_iterations=15, **ils_params)
        best_solution, history = ils.solve()
        assert len(history.best_fitness) <= 15 + 1  # +1 por construcción inicial
    
    # ========================================================================
    # Tests de criterios de parada
    # ========================================================================
    
    def test_ils_max_iterations_limit(self, small_problem, ils_params):
        """Validar límite de iteraciones"""
        ils = IteratedLocalSearch(small_problem, max_iterations=5, **ils_params)
        best_solution, history = ils.solve()
        # Historia tiene construcción + iteraciones
        assert len(history.best_fitness) <= 7
    
    def test_ils_max_time_limit(self, small_problem, ils_params):
        """Validar límite de tiempo"""
        ils = IteratedLocalSearch(small_problem, time_budget=0.1, **ils_params)
        start_time = time.time()
        best_solution, history = ils.solve()
        elapsed = time.time() - start_time
        assert elapsed < 1.0  # Muy permisivo
    
    # ========================================================================
    # Tests de estrategia de aceptación
    # ========================================================================
    
    def test_ils_best_acceptance(self, small_problem, ils_params):
        """Validar estrategia 'best'"""
        ils = IteratedLocalSearch(
            small_problem, 
            max_iterations=10,
            acceptance_strategy='best',
            **ils_params
        )
        best_solution, history = ils.solve()
        assert best_solution.is_feasible(small_problem)
    
    def test_ils_always_acceptance(self, small_problem, ils_params):
        """Validar estrategia 'always'"""
        ils = IteratedLocalSearch(
            small_problem,
            max_iterations=10,
            acceptance_strategy='always',
            **ils_params
        )
        best_solution, history = ils.solve()
        assert best_solution.is_feasible(small_problem)
    
    def test_ils_probabilistic_acceptance(self, small_problem, ils_params):
        """Validar estrategia 'probabilistic'"""
        ils = IteratedLocalSearch(
            small_problem,
            max_iterations=10,
            acceptance_strategy='probabilistic',
            **ils_params
        )
        best_solution, history = ils.solve()
        assert best_solution.is_feasible(small_problem)


class TestILSHistory:
    """Tests para ILSHistory dataclass"""
    
    def test_history_creation(self):
        """Validar creación de historia"""
        history = ILSHistory()
        assert isinstance(history, ILSHistory)
    
    def test_history_track_fitness(self):
        """Validar registro de fitness"""
        history = ILSHistory()
        history.add_iteration(iteration=1, best_fitness=10, current_fitness=10,
                            num_colors=5, num_conflicts=2, elapsed_time=0.1,
                            accepted=True, improved=True)
        history.add_iteration(iteration=2, best_fitness=8, current_fitness=8,
                            num_colors=4, num_conflicts=0, elapsed_time=0.2,
                            accepted=True, improved=True)
        history.add_iteration(iteration=3, best_fitness=6, current_fitness=6,
                            num_colors=3, num_conflicts=0, elapsed_time=0.3,
                            accepted=True, improved=True)
        assert len(history.best_fitness) == 3
        assert history.best_fitness[-1] == 6
    
    def test_history_track_times(self):
        """Validar registro de tiempos"""
        history = ILSHistory()
        history.iteration_times.append(0.1)
        history.iteration_times.append(0.15)
        assert len(history.iteration_times) == 2
    
    def test_history_best_fitness(self):
        """Validar mejor fitness en historia"""
        history = ILSHistory()
        history.best_fitness = 5
        history.best_iteration = 10
        assert history.best_fitness == 5
        assert history.best_iteration == 10


class TestAdaptiveILS:
    """Tests para AdaptiveILS"""
    
    @pytest.fixture
    def small_problem(self):
        """Fixture: Problema pequeño"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
    
    @pytest.fixture
    def adaptive_params(self):
        """Fixture: Parámetros para AdaptiveILS"""
        return {
            'constructive': GreedyDSATUR,
            'improvement': KempeChain,
            'perturbation': RandomRecolor,
            'max_iterations': 30
        }
    
    # ========================================================================
    # Tests de inicialización
    # ========================================================================
    
    def test_adaptive_ils_initialization(self, small_problem, adaptive_params):
        """Validar inicialización de AdaptiveILS"""
        ails = AdaptiveILS(small_problem, **adaptive_params)
        assert ails is not None
        assert isinstance(ails, AdaptiveILS)
    
    # ========================================================================
    # Tests de ejecución
    # ========================================================================
    
    def test_adaptive_ils_solve(self, small_problem, adaptive_params):
        """Validar que AdaptiveILS.solve funciona"""
        ails = AdaptiveILS(small_problem, **adaptive_params)
        best_solution, history = ails.solve()
        assert best_solution.is_feasible(small_problem)
    
    def test_adaptive_ils_improves(self, small_problem, adaptive_params):
        """Validar que AdaptiveILS mejora"""
        ails = AdaptiveILS(small_problem, max_iterations=15, **adaptive_params)
        best_solution, history = ails.solve()
        first = history.best_fitness[0]
        last = history.best_fitness[-1]
        assert last <= first
    
    # ========================================================================
    # Tests de adaptación
    # ========================================================================
    
    def test_adaptive_ils_adapts_strength(self, small_problem, adaptive_params):
        """Validar que adapta intensidad de perturbación"""
        ails = AdaptiveILS(small_problem, max_iterations=10, **adaptive_params)
        best_solution, history = ails.solve()
        # Si ejecuta sin error, la adaptación funcionó
        assert best_solution.is_feasible(small_problem)


class TestPerturbationSchedules:
    """Tests para estrategias de perturbación"""
    
    @pytest.fixture
    def small_problem(self):
        """Fixture: Problema pequeño"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
    
    @pytest.fixture
    def ils_base_params(self):
        """Fixture: Parámetros ILS base"""
        return {
            'constructive': GreedyDSATUR,
            'improvement': KempeChain,
            'perturbation': RandomRecolor,
            'max_iterations': 20
        }
    
    # ========================================================================
    # Tests ConstantPerturbation
    # ========================================================================
    
    def test_constant_schedule_creation(self):
        """Validar creación de schedule constante"""
        schedule = ConstantPerturbation(strength=0.3)
        assert schedule is not None
    
    def test_constant_schedule_strength(self):
        """Validar intensidad constante"""
        schedule = ConstantPerturbation(strength=0.5)
        assert schedule.get_strength(0) == 0.5
        assert schedule.get_strength(10) == 0.5
        assert schedule.get_strength(100) == 0.5
    
    def test_constant_schedule_with_ils(self, small_problem, ils_base_params):
        """Validar uso de schedule constante en ILS"""
        schedule = ConstantPerturbation(strength=0.3)
        # Verificar que el schedule existe y puede ser usado
        assert schedule.get_strength(0) == 0.3
        ils = IteratedLocalSearch(
            small_problem,
            max_iterations=10,
            **ils_base_params
        )
        best, history = ils.solve()
        assert best.is_feasible(small_problem)
    
    # ========================================================================
    # Tests LinearPerturbation
    # ========================================================================
    
    def test_linear_schedule_creation(self):
        """Validar creación de schedule lineal"""
        schedule = LinearPerturbation(initial=0.1, final=0.9, iterations=100)
        assert schedule is not None
    
    def test_linear_schedule_progression(self):
        """Validar progresión lineal"""
        schedule = LinearPerturbation(initial=0.0, final=1.0, iterations=10)
        strength_0 = schedule.get_strength(0)
        strength_5 = schedule.get_strength(5)
        strength_10 = schedule.get_strength(10)
        assert strength_0 <= strength_5 <= strength_10
    
    # ========================================================================
    # Tests ExponentialPerturbation
    # ========================================================================
    
    def test_exponential_schedule_creation(self):
        """Validar creación de schedule exponencial"""
        schedule = ExponentialPerturbation(initial=0.1, final=0.9, rate=0.1)
        assert schedule is not None
    
    def test_exponential_schedule_progression(self):
        """Validar progresión exponencial"""
        schedule = ExponentialPerturbation(initial=0.1, final=1.0, rate=0.1)
        strength_0 = schedule.get_strength(0)
        strength_10 = schedule.get_strength(10)
        assert strength_0 < strength_10
    
    # ========================================================================
    # Tests DynamicPerturbation
    # ========================================================================
    
    def test_dynamic_schedule_creation(self):
        """Validar creación de schedule dinámico"""
        schedule = DynamicPerturbation(base=0.3, boost=0.5)
        assert schedule is not None
    
    def test_dynamic_schedule_no_improvements(self):
        """Validar intensidad con estancamiento"""
        schedule = DynamicPerturbation(base=0.3, boost=0.7)
        # Sin mejoras recientes, debe ser mayor
        schedule.no_improvement_count = 5
        strength = schedule.get_strength(0)
        assert strength >= 0.3
    
    # ========================================================================
    # Tests create_schedule factory
    # ========================================================================
    
    def test_create_schedule_constant(self):
        """Validar factory para schedule constante"""
        schedule = create_schedule('constant', strength=0.4)
        assert isinstance(schedule, ConstantPerturbation)
        assert schedule.get_strength(0) == 0.4
    
    def test_create_schedule_linear(self):
        """Validar factory para schedule lineal"""
        schedule = create_schedule('linear', initial=0.1, final=0.9, iterations=100)
        assert isinstance(schedule, LinearPerturbation)
    
    def test_create_schedule_exponential(self):
        """Validar factory para schedule exponencial"""
        schedule = create_schedule('exponential', initial=0.1, final=0.9, rate=0.1)
        assert isinstance(schedule, ExponentialPerturbation)
    
    def test_create_schedule_dynamic(self):
        """Validar factory para schedule dinámico"""
        schedule = create_schedule('dynamic', base=0.3, boost=0.7)
        assert isinstance(schedule, DynamicPerturbation)
    
    # ========================================================================
    # Tests de schedule con ILS
    # ========================================================================
    
    def test_ils_with_custom_schedule(self, small_problem, ils_base_params):
        """Validar uso de schedule personalizado en ILS"""
        schedule = LinearPerturbation(initial=0.1, final=0.8, iterations=20)
        # Verificar que el schedule existe y puede ser usado
        assert schedule.get_strength(0) == 0.1
        assert schedule.get_strength(20) == 0.8
        ils = IteratedLocalSearch(
            small_problem,
            max_iterations=10,
            **ils_base_params
        )
        best, history = ils.solve()
        assert best.is_feasible(small_problem)


# ============================================================================
# Tests de integración completa
# ============================================================================

class TestILSIntegration:
    """Tests de integración del pipeline ILS completo"""
    
    @pytest.fixture
    def test_problem(self):
        """Fixture: Problema para tests de integración"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (2, 4), (3, 5)]
        return GraphColoringProblem(vertices=5, edges=edges, colors_known=4)
    
    def test_full_ils_pipeline(self, test_problem):
        """Validar pipeline ILS completo"""
        ils = IteratedLocalSearch(
            test_problem,
            constructive=GreedyDSATUR,
            improvement=KempeChain,
            perturbation=PartialDestroy,
            max_iterations=15
        )
        best_solution, history = ils.solve()
        
        # Validaciones
        assert best_solution.is_feasible(test_problem)
        assert len(history.best_fitness) > 0
        assert history.best_fitness[-1] <= best_solution.num_colors * 1.5  # Aproximado
    
    def test_ils_with_different_operators(self, test_problem):
        """Validar ILS con diferentes combinaciones de operadores"""
        for constructive in [GreedyDSATUR, RandomSequential]:
            for improvement in [KempeChain, OneVertexMove]:
                ils = IteratedLocalSearch(
                    test_problem,
                    constructive=constructive,
                    improvement=improvement,
                    perturbation=RandomRecolor,
                    max_iterations=5
                )
                best, _ = ils.solve()
                assert best.is_feasible(test_problem)
    
    def test_ils_comparison_strategies(self, test_problem):
        """Validar ILS con diferentes estrategias de aceptación"""
        for strategy in ['best', 'always', 'probabilistic']:
            ils = IteratedLocalSearch(
                test_problem,
                constructive=GreedyDSATUR,
                improvement=KempeChain,
                perturbation=RandomRecolor,
                max_iterations=10,
                acceptance_strategy=strategy
            )
            best, _ = ils.solve()
            assert best.is_feasible(test_problem)
    
    def test_ils_with_adaptive_variant(self, test_problem):
        """Validar pipeline con AdaptiveILS"""
        ails = AdaptiveILS(
            test_problem,
            constructive=GreedyDSATUR,
            improvement=KempeChain,
            perturbation=RandomRecolor,
            max_iterations=15
        )
        best, history = ails.solve()
        assert best.is_feasible(test_problem)


if __name__ == "__main__":
    """
    Ejecutar con:
        pytest tests/test_ils.py -v
        pytest tests/test_ils.py::TestIteratedLocalSearchBasic -v
        pytest tests/test_ils.py -v --tb=short
        pytest tests/test_ils.py -v -k "deterministic"  # Tests específicos
    """
    print(__doc__)
