"""
Tests para modulo OPERATORS

Pruebas de constructivos, mejora, perturbacion y reparacion
"""

import pytest
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from operators.constructive import GreedyDSATUR, GreedyLargestFirst, RandomSequential
from operators.improvement import OneVertexMove, KempeChainMove, TabuColMove
from operators.perturbation import RandomRecolor, PartialDestroy, ColorClassMerge
from operators.repair import GreedyRepair, ConflictMinimizingRepair


class TestConstructive:
    """Tests para operadores constructivos"""
    
    @pytest.fixture
    def problem(self):
        """Problema triangulo"""
        vertices = 3
        edges = [(0, 1), (1, 2), (0, 2)]
        return GraphColoringProblem(vertices, edges)
    
    def test_greedy_dsatur(self, problem):
        """Test DSATUR"""
        solution = GreedyDSATUR.construct(problem)
        
        assert solution.num_colors >= 1
        assert solution.is_feasible()
        assert len(solution.assignment) == problem.vertices
    
    def test_greedy_largest_first(self, problem):
        """Test Largest First"""
        solution = GreedyLargestFirst.construct(problem)
        
        assert solution.num_colors >= 1
        assert solution.is_feasible()
    
    def test_random_sequential(self, problem):
        """Test Random Sequential"""
        solution = RandomSequential.construct(problem, seed=42)
        
        assert solution.num_colors >= 1
        assert solution.is_feasible()
    
    def test_reproducibility(self, problem):
        """Test reproducibilidad con seed"""
        sol1 = RandomSequential.construct(problem, seed=42)
        sol2 = RandomSequential.construct(problem, seed=42)
        
        np.testing.assert_array_equal(sol1.assignment, sol2.assignment)


class TestImprovement:
    """Tests para operadores de mejora"""
    
    @pytest.fixture
    def problem(self):
        """Problema ciclo de 4 vertices"""
        return GraphColoringProblem(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    
    @pytest.fixture
    def initial_solution(self, problem):
        """Solucion inicial (no optimal)"""
        return ColoringSolution(np.array([0, 1, 0, 1]), problem)
    
    def test_one_vertex_move(self, problem, initial_solution):
        """Test One Vertex Move"""
        improved = OneVertexMove.improve(initial_solution, problem, max_iterations=10)
        
        # Debe ser al menos tan buena como la inicial
        assert improved.fitness() <= initial_solution.fitness()
    
    def test_kempe_chain(self, problem, initial_solution):
        """Test Kempe Chain"""
        result = KempeChainMove.apply(initial_solution, problem, vertex=0, new_color=2)
        
        if result is not None:
            assert isinstance(result, ColoringSolution)
    
    def test_tabu_col(self, problem, initial_solution):
        """Test Tabu Coloring"""
        tabu = TabuColMove(tabu_tenure=5)
        improved = tabu.improve(initial_solution, problem, max_iterations=20)
        
        assert isinstance(improved, ColoringSolution)
        # Debe ser al menos tan buena como la inicial
        assert improved.fitness() <= initial_solution.fitness()


class TestPerturbation:
    """Tests para operadores de perturbacion"""
    
    @pytest.fixture
    def problem(self):
        """Problema simple"""
        return GraphColoringProblem(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    
    @pytest.fixture
    def solution(self, problem):
        """Solucion factible"""
        return GreedyDSATUR.construct(problem, seed=42)
    
    def test_random_recolor(self, problem, solution):
        """Test Random Recolor"""
        perturbed = RandomRecolor.perturb(solution, problem, num_vertices=2, seed=42)
        
        assert isinstance(perturbed, ColoringSolution)
        # Puede ser peor, igual o mejor
        assert perturbed.assignment.shape == solution.assignment.shape
    
    def test_partial_destroy(self, problem, solution):
        """Test Partial Destroy"""
        perturbed = PartialDestroy.perturb(solution, problem, destruction_rate=0.2, seed=42)
        
        assert isinstance(perturbed, ColoringSolution)
        assert perturbed.is_feasible()
    
    def test_color_class_merge(self, problem, solution):
        """Test Color Class Merge"""
        # Solo si hay multiples clases de color
        if solution.num_colors > 1:
            perturbed = ColorClassMerge.perturb(solution, problem, seed=42)
            
            if perturbed is not None:
                assert isinstance(perturbed, ColoringSolution)


class TestRepair:
    """Tests para operadores de reparacion"""
    
    @pytest.fixture
    def problem(self):
        """Problema triangulo"""
        return GraphColoringProblem(3, [(0, 1), (1, 2), (0, 2)])
    
    @pytest.fixture
    def broken_solution(self, problem):
        """Solucion con conflictos"""
        return ColoringSolution(np.array([0, 0, 0]), problem)
    
    def test_greedy_repair(self, problem, broken_solution):
        """Test Greedy Repair"""
        repaired = GreedyRepair.repair(broken_solution, problem)
        
        assert repaired.is_feasible()
        assert repaired.num_conflicts == 0
    
    def test_conflict_minimizing_repair(self, problem, broken_solution):
        """Test Conflict Minimizing Repair"""
        repaired = ConflictMinimizingRepair.repair(broken_solution, problem)
        
        # Debe tener igual o menos conflictos
        assert repaired.num_conflicts <= broken_solution.num_conflicts
    
    def test_repair_already_feasible(self, problem):
        """Test reparacion de solucion ya factible"""
        feasible = ColoringSolution(np.array([0, 1, 2]), problem)
        
        repaired = GreedyRepair.repair(feasible, problem)
        
        assert repaired.is_feasible()
        assert repaired.num_conflicts == 0


class TestOperatorChaining:
    """Tests de encadenamiento de operadores"""
    
    @pytest.fixture
    def problem(self):
        return GraphColoringProblem(6, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5)])
    
    def test_construct_improve_perturb(self, problem):
        """Test flujo: construir -> mejorar -> perturbar"""
        # Construir
        solution = GreedyDSATUR.construct(problem, seed=42)
        initial_fitness = solution.fitness()
        
        # Mejorar
        improved = OneVertexMove.improve(solution, problem, max_iterations=5)
        improved_fitness = improved.fitness()
        
        # Mejorado debe ser igual o mejor
        assert improved_fitness <= initial_fitness
        
        # Perturbar
        perturbed = RandomRecolor.perturb(improved, problem, num_vertices=2, seed=42)
        
        # Perturbado puede ser peor, pero debe ser valido
        assert isinstance(perturbed, ColoringSolution)
    
    def test_construct_repair(self, problem):
        """Test flujo: construir -> puede ser reparado si infactible"""
        solution = RandomSequential.construct(problem, seed=42)
        
        # Si no es factible, puede ser reparado
        if not solution.is_feasible():
            repaired = GreedyRepair.repair(solution, problem)
            assert repaired.is_feasible()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
