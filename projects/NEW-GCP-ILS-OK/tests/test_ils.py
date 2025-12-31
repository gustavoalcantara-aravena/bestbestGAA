"""
Tests para metaheuristica ILS

Pruebas del Iterated Local Search
"""

import pytest
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from metaheuristic.ils_core import IteratedLocalSearch, HybridILS


class TestIteratedLocalSearch:
    """Tests para ILS"""
    
    @pytest.fixture
    def simple_problem(self):
        """Problema simple: ciclo de 5 vertices"""
        return GraphColoringProblem(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    
    @pytest.fixture
    def larger_problem(self):
        """Problema mas grande"""
        vertices = 10
        edges = [(i, (i+1) % vertices) for i in range(vertices)]
        return GraphColoringProblem(vertices, edges)
    
    def test_initialization(self, simple_problem):
        """Test inicializacion de ILS"""
        ils = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=10,
            ls_max_iterations=5,
            verbose=False
        )
        
        assert ils.problem == simple_problem
        assert ils.seed == 42
        assert ils.iteration == 0
    
    def test_run_simple(self, simple_problem):
        """Test ejecucion en problema simple"""
        ils = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=20,
            max_no_improve=10,
            ls_max_iterations=5,
            verbose=False
        )
        
        solution = ils.run()
        
        assert isinstance(solution, ColoringSolution)
        assert solution.is_feasible()
        assert solution.num_colors >= 3  # Grafo ciclo impar necesita 3
    
    def test_convergence(self, simple_problem):
        """Test que la busqueda converge"""
        ils = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=50,
            max_no_improve=20,
            ls_max_iterations=10,
            verbose=False
        )
        
        solution = ils.run()
        stats = ils.get_statistics()
        
        # Debe completar sin errores
        assert stats['total_iterations'] > 0
        assert 'best_fitness' in stats
        assert solution.num_colors > 0
    
    def test_reproducibility(self, simple_problem):
        """Test reproducibilidad con seed"""
        ils1 = IteratedLocalSearch(simple_problem, seed=42, max_iterations=10, verbose=False)
        sol1 = ils1.run()
        
        ils2 = IteratedLocalSearch(simple_problem, seed=42, max_iterations=10, verbose=False)
        sol2 = ils2.run()
        
        # Mismo seed debe dar misma solucion
        np.testing.assert_array_equal(sol1.assignment, sol2.assignment)
    
    def test_different_seeds(self, simple_problem):
        """Test que diferentes seeds dan diferentes resultados"""
        ils1 = IteratedLocalSearch(simple_problem, seed=42, max_iterations=20, verbose=False)
        sol1 = ils1.run()
        
        ils2 = IteratedLocalSearch(simple_problem, seed=123, max_iterations=20, verbose=False)
        sol2 = ils2.run()
        
        # Different seeds pueden dar diferentes soluciones (generalmente)
        # No se garantiza pero es probable
        assert isinstance(sol1, ColoringSolution)
        assert isinstance(sol2, ColoringSolution)
    
    def test_get_statistics(self, simple_problem):
        """Test retorno de estadisticas"""
        ils = IteratedLocalSearch(simple_problem, seed=42, max_iterations=10, verbose=False)
        solution = ils.run()
        stats = ils.get_statistics()
        
        assert 'total_iterations' in stats
        assert 'best_fitness' in stats
        assert 'num_colors' in stats
        assert 'is_feasible' in stats
        assert 'history' in stats
        
        history = stats['history']
        assert 'iteration' in history
        assert 'best_fitness' in history
        assert len(history['iteration']) > 0
    
    def test_early_stopping(self, simple_problem):
        """Test parada anticipada por max_no_improve"""
        ils = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=1000,
            max_no_improve=5,
            verbose=False
        )
        
        solution = ils.run()
        stats = ils.get_statistics()
        
        # Debe parar antes de alcanzar max_iterations
        # (si hay convergencia rapida)
        assert stats['total_iterations'] <= 1000
    
    def test_adaptive_perturbation(self, simple_problem):
        """Test perturbacion adaptativa"""
        ils_adaptive = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=20,
            use_adaptive_perturbation=True,
            verbose=False
        )
        
        ils_fixed = IteratedLocalSearch(
            simple_problem,
            seed=42,
            max_iterations=20,
            use_adaptive_perturbation=False,
            verbose=False
        )
        
        sol_adaptive = ils_adaptive.run()
        sol_fixed = ils_fixed.run()
        
        assert isinstance(sol_adaptive, ColoringSolution)
        assert isinstance(sol_fixed, ColoringSolution)
    
    def test_larger_problem(self, larger_problem):
        """Test en problema mas grande"""
        ils = IteratedLocalSearch(
            larger_problem,
            seed=42,
            max_iterations=30,
            max_no_improve=15,
            ls_max_iterations=10,
            verbose=False
        )
        
        solution = ils.run()
        
        assert solution.is_feasible()
        # Ciclo de 10 vertices necesita 2 colores
        assert solution.num_colors >= 2


class TestHybridILS:
    """Tests para Hybrid ILS"""
    
    @pytest.fixture
    def problem(self):
        return GraphColoringProblem(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    
    def test_hybrid_initialization(self, problem):
        """Test inicializacion de Hybrid ILS"""
        hybrid = HybridILS(problem, seed=42, max_iterations=10, verbose=False)
        
        assert hybrid.problem == problem
        assert len(hybrid.ls_strategies) > 0
    
    def test_hybrid_run(self, problem):
        """Test ejecucion de Hybrid ILS"""
        hybrid = HybridILS(
            problem,
            seed=42,
            max_iterations=20,
            max_no_improve=10,
            ls_max_iterations=5,
            verbose=False
        )
        
        solution = hybrid.run()
        
        assert isinstance(solution, ColoringSolution)
        assert solution.is_feasible()


class TestILSWithRealDataset:
    """Tests con instancias reales del dataset DIMACS"""
    
    def test_myciel3(self):
        """Test con myciel3 (pequeno benchmark)"""
        # myciel3: 11 vertices, 20 edges, cromAtico numero 4
        vertices = 11
        edges = [
            (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 2), (1, 5), (1, 6),
            (2, 3), (2, 7), (2, 8),
            (3, 4), (3, 9),
            (4, 10),
            (5, 6), (5, 7), (5, 9),
            (6, 8), (6, 10),
            (7, 8),
            (9, 10)
        ]
        
        problem = GraphColoringProblem(vertices, edges)
        ils = IteratedLocalSearch(
            problem,
            seed=42,
            max_iterations=50,
            max_no_improve=20,
            verbose=False
        )
        
        solution = ils.run()
        
        assert solution.is_feasible()
        # CromAtico numero conocido es 4
        assert solution.num_colors <= 5  # Permitir un color extra
    
    def test_small_instance(self):
        """Test con instancia pequena aleatoria"""
        np.random.seed(42)
        
        # Generar grafo aleatorio
        vertices = 20
        edges = []
        for i in range(vertices):
            for j in range(i+1, vertices):
                if np.random.random() < 0.3:  # 30% densidad
                    edges.append((i, j))
        
        problem = GraphColoringProblem(vertices, edges)
        ils = IteratedLocalSearch(
            problem,
            seed=42,
            max_iterations=100,
            max_no_improve=30,
            ls_max_iterations=20,
            verbose=False
        )
        
        solution = ils.run()
        
        assert solution.is_feasible()
        assert 1 <= solution.num_colors <= vertices


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
