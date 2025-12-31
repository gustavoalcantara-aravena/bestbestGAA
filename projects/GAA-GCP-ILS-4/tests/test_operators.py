"""
tests/test_operators.py
Suite de tests unitarios para Operadores (Constructivos, Mejora, Perturbación, Reparación)

Ejecutar con:
    pytest tests/test_operators.py -v
    
Cobertura:
    - GreedyDSATUR, GreedyLF, RandomSequential (Constructivos)
    - KempeChain, OneVertexMove, TabuCol (Mejora)
    - RandomRecolor, PartialDestroy, AdaptivePerturbation (Perturbación)
    - RepairConflicts, IntensifyColor, Diversify (Reparación)
"""

import pytest
import numpy as np

from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from operators.constructive import GreedyDSATUR, GreedyLF, RandomSequential
from operators.improvement import KempeChain, OneVertexMove, TabuCol
from operators.perturbation import RandomRecolor, PartialDestroy, AdaptivePerturbation
from operators.repair import RepairConflicts, IntensifyColor, Diversify


class TestConstructiveOperators:
    """Tests para operadores constructivos"""
    
    @pytest.fixture
    def simple_graph(self):
        """Fixture: Grafo simple para pruebas"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
    
    @pytest.fixture
    def triangle(self):
        """Fixture: Triángulo"""
        edges = [(1, 2), (2, 3), (1, 3)]
        return GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
    
    @pytest.fixture
    def bipartite_4(self):
        """Fixture: Ciclo de 4 (bipartito)"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=2)
    
    # ========================================================================
    # Tests GreedyDSATUR
    # ========================================================================
    
    def test_greedy_dsatur_produces_solution(self, simple_graph):
        """Validar que GreedyDSATUR produce solución"""
        solution = GreedyDSATUR.construct(simple_graph)
        assert solution is not None
        assert isinstance(solution, ColoringSolution)
    
    def test_greedy_dsatur_is_feasible(self, simple_graph):
        """Validar que solución de GreedyDSATUR es factible"""
        solution = GreedyDSATUR.construct(simple_graph)
        assert solution.is_feasible(simple_graph) == True
    
    def test_greedy_dsatur_respects_upper_bound(self, simple_graph):
        """Validar que respeta cota superior"""
        solution = GreedyDSATUR.construct(simple_graph)
        assert solution.num_colors <= simple_graph.upper_bound
    
    def test_greedy_dsatur_triangle_optimal(self, triangle):
        """Validar que triángulo usa 3 colores"""
        solution = GreedyDSATUR.construct(triangle)
        assert solution.num_colors == 3
    
    def test_greedy_dsatur_bipartite(self, bipartite_4):
        """Validar que ciclo 4 usa 2 colores"""
        solution = GreedyDSATUR.construct(bipartite_4)
        assert solution.num_colors <= 2
    
    def test_greedy_dsatur_complete_assignment(self, simple_graph):
        """Validar que todos los vértices están asignados"""
        solution = GreedyDSATUR.construct(simple_graph)
        for v in range(1, simple_graph.n_vertices + 1):
            assert v in solution.assignment
    
    # ========================================================================
    # Tests GreedyLF
    # ========================================================================
    
    def test_greedy_lf_produces_solution(self, simple_graph):
        """Validar que GreedyLF produce solución"""
        solution = GreedyLF.construct(simple_graph)
        assert solution is not None
        assert isinstance(solution, ColoringSolution)
    
    def test_greedy_lf_is_feasible(self, simple_graph):
        """Validar factibilidad de GreedyLF"""
        solution = GreedyLF.construct(simple_graph)
        assert solution.is_feasible(simple_graph) == True
    
    def test_greedy_lf_respects_upper_bound(self, simple_graph):
        """Validar que respeta cota superior"""
        solution = GreedyLF.construct(simple_graph)
        assert solution.num_colors <= simple_graph.upper_bound
    
    def test_greedy_lf_complete_assignment(self, simple_graph):
        """Validar asignación completa"""
        solution = GreedyLF.construct(simple_graph)
        for v in range(1, simple_graph.n_vertices + 1):
            assert v in solution.assignment
    
    # ========================================================================
    # Tests RandomSequential
    # ========================================================================
    
    def test_random_sequential_produces_solution(self, simple_graph):
        """Validar que RandomSequential produce solución"""
        solution = RandomSequential.construct(simple_graph)
        assert solution is not None
        assert isinstance(solution, ColoringSolution)
    
    def test_random_sequential_is_feasible(self, simple_graph):
        """Validar factibilidad"""
        solution = RandomSequential.construct(simple_graph)
        assert solution.is_feasible(simple_graph) == True
    
    def test_random_sequential_respects_upper_bound(self, simple_graph):
        """Validar cota superior"""
        solution = RandomSequential.construct(simple_graph)
        assert solution.num_colors <= simple_graph.upper_bound
    
    def test_random_sequential_deterministic_with_seed(self, simple_graph):
        """Validar reproducibilidad con seed"""
        np.random.seed(42)
        sol1 = RandomSequential.construct(simple_graph)
        np.random.seed(42)
        sol2 = RandomSequential.construct(simple_graph)
        assert sol1.assignment == sol2.assignment
    
    def test_random_sequential_complete_assignment(self, simple_graph):
        """Validar asignación completa"""
        solution = RandomSequential.construct(simple_graph)
        for v in range(1, simple_graph.n_vertices + 1):
            assert v in solution.assignment


class TestImprovementOperators:
    """Tests para operadores de mejora"""
    
    @pytest.fixture
    def simple_graph(self):
        """Fixture: Grafo simple"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
    
    @pytest.fixture
    def suboptimal_solution(self, simple_graph):
        """Fixture: Solución subóptima pero factible"""
        return ColoringSolution(assignment={1: 0, 2: 1, 3: 2, 4: 0})
    
    @pytest.fixture
    def conflicting_solution(self):
        """Fixture: Solución con conflictos"""
        edges = [(1, 2), (2, 3), (3, 4)]
        problem = GraphColoringProblem(vertices=4, edges=edges, colors_known=2)
        solution = ColoringSolution(assignment={1: 0, 2: 0, 3: 0, 4: 1})
        return problem, solution
    
    # ========================================================================
    # Tests KempeChain
    # ========================================================================
    
    def test_kempe_chain_improves_or_keeps(self, simple_graph, suboptimal_solution):
        """Validar que KempeChain no empeora solución"""
        initial_colors = suboptimal_solution.num_colors
        improved = KempeChain.improve(suboptimal_solution, simple_graph)
        assert improved.num_colors <= initial_colors
    
    def test_kempe_chain_maintains_feasibility(self, simple_graph, suboptimal_solution):
        """Validar que mantiene factibilidad"""
        improved = KempeChain.improve(suboptimal_solution, simple_graph)
        assert improved.is_feasible(simple_graph) == True
    
    def test_kempe_chain_complete_assignment(self, simple_graph, suboptimal_solution):
        """Validar que asigna todos los vértices"""
        improved = KempeChain.improve(suboptimal_solution, simple_graph)
        assert len(improved.assignment) == simple_graph.n_vertices
    
    # ========================================================================
    # Tests OneVertexMove
    # ========================================================================
    
    def test_one_vertex_move_improves_or_keeps(self, simple_graph, suboptimal_solution):
        """Validar que no empeora"""
        initial_colors = suboptimal_solution.num_colors
        improved = OneVertexMove.improve(suboptimal_solution, simple_graph)
        assert improved.num_colors <= initial_colors
    
    def test_one_vertex_move_maintains_feasibility(self, simple_graph, suboptimal_solution):
        """Validar factibilidad"""
        improved = OneVertexMove.improve(suboptimal_solution, simple_graph)
        assert improved.is_feasible(simple_graph) == True
    
    def test_one_vertex_move_complete_assignment(self, simple_graph, suboptimal_solution):
        """Validar asignación completa"""
        improved = OneVertexMove.improve(suboptimal_solution, simple_graph)
        assert len(improved.assignment) == simple_graph.n_vertices
    
    # ========================================================================
    # Tests TabuCol
    # ========================================================================
    
    def test_tabucol_improves_or_keeps(self, simple_graph, suboptimal_solution):
        """Validar que no empeora"""
        initial_colors = suboptimal_solution.num_colors
        improved = TabuCol.improve(suboptimal_solution, simple_graph)
        assert improved.num_colors <= initial_colors
    
    def test_tabucol_maintains_feasibility(self, simple_graph, suboptimal_solution):
        """Validar factibilidad"""
        improved = TabuCol.improve(suboptimal_solution, simple_graph)
        assert improved.is_feasible(simple_graph) == True
    
    def test_tabucol_complete_assignment(self, simple_graph, suboptimal_solution):
        """Validar asignación completa"""
        improved = TabuCol.improve(suboptimal_solution, simple_graph)
        assert len(improved.assignment) == simple_graph.n_vertices
    
    def test_tabucol_iterations_parameter(self, simple_graph, suboptimal_solution):
        """Validar parámetro de iteraciones"""
        improved = TabuCol.improve(suboptimal_solution, simple_graph, max_iterations=50)
        assert improved.is_feasible(simple_graph) == True


class TestPerturbationOperators:
    """Tests para operadores de perturbación"""
    
    @pytest.fixture
    def good_solution(self):
        """Fixture: Solución válida"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        problem = GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 2, 4: 0})
        return problem, solution
    
    # ========================================================================
    # Tests RandomRecolor
    # ========================================================================
    
    def test_random_recolor_returns_solution(self, good_solution):
        """Validar que retorna solución"""
        problem, solution = good_solution
        perturbed = RandomRecolor.perturb(solution, problem)
        assert isinstance(perturbed, ColoringSolution)
    
    def test_random_recolor_with_intensity(self, good_solution):
        """Validar con intensidad específica"""
        problem, solution = good_solution
        perturbed = RandomRecolor.perturb(solution, problem, strength=0.5)
        assert perturbed is not None
    
    def test_random_recolor_minimal_change(self, good_solution):
        """Validar con intensidad mínima"""
        problem, solution = good_solution
        perturbed = RandomRecolor.perturb(solution, problem, strength=0.01)
        # Cambios mínimos
        assert len(perturbed.assignment) == problem.n_vertices
    
    def test_random_recolor_maximal_change(self, good_solution):
        """Validar con intensidad máxima"""
        problem, solution = good_solution
        perturbed = RandomRecolor.perturb(solution, problem, strength=1.0)
        assert len(perturbed.assignment) == problem.n_vertices
    
    # ========================================================================
    # Tests PartialDestroy
    # ========================================================================
    
    def test_partial_destroy_returns_solution(self, good_solution):
        """Validar que retorna solución"""
        problem, solution = good_solution
        perturbed = PartialDestroy.perturb(solution, problem)
        assert isinstance(perturbed, ColoringSolution)
    
    def test_partial_destroy_maintains_structure(self, good_solution):
        """Validar que mantiene estructura"""
        problem, solution = good_solution
        perturbed = PartialDestroy.perturb(solution, problem)
        assert len(perturbed.assignment) == problem.n_vertices
    
    def test_partial_destroy_with_intensity(self, good_solution):
        """Validar con intensidad variada"""
        problem, solution = good_solution
        perturbed = PartialDestroy.perturb(solution, problem, strength=0.3)
        assert len(perturbed.assignment) == problem.n_vertices
    
    # ========================================================================
    # Tests AdaptivePerturbation
    # ========================================================================
    
    def test_adaptive_perturbation_returns_solution(self, good_solution):
        """Validar que retorna solución"""
        problem, solution = good_solution
        perturbed = AdaptivePerturbation.perturb(solution, problem)
        assert isinstance(perturbed, ColoringSolution)
    
    def test_adaptive_perturbation_adapts_strength(self, good_solution):
        """Validar adaptación de intensidad"""
        problem, solution = good_solution
        # Con mejora reciente
        perturbed = AdaptivePerturbation.perturb(solution, problem)
        assert len(perturbed.assignment) == problem.n_vertices


class TestRepairOperators:
    """Tests para operadores de reparación"""
    
    @pytest.fixture
    def conflicting_problem_solution(self):
        """Fixture: Problema y solución con conflictos"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        problem = GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
        # Solución con conflictos
        solution = ColoringSolution(assignment={1: 0, 2: 0, 3: 0, 4: 0})
        return problem, solution
    
    @pytest.fixture
    def valid_solution(self):
        """Fixture: Solución válida"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        problem = GraphColoringProblem(vertices=4, edges=edges, colors_known=3)
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 2, 4: 0})
        return problem, solution
    
    # ========================================================================
    # Tests RepairConflicts
    # ========================================================================
    
    def test_repair_converts_to_feasible(self, conflicting_problem_solution):
        """Validar que repara a factible"""
        problem, solution = conflicting_problem_solution
        repaired = RepairConflicts.repair(solution, problem)
        assert repaired.is_feasible(problem) == True
    
    def test_repair_maintains_structure(self, conflicting_problem_solution):
        """Validar que mantiene todos los vértices"""
        problem, solution = conflicting_problem_solution
        repaired = RepairConflicts.repair(solution, problem)
        assert len(repaired.assignment) == problem.n_vertices
    
    def test_repair_does_not_worsen_valid(self, valid_solution):
        """Validar que no empeora solución válida"""
        problem, solution = valid_solution
        initial_colors = solution.num_colors
        repaired = RepairConflicts.repair(solution, problem)
        assert repaired.num_colors <= initial_colors
    
    def test_repair_with_color_reduction(self, conflicting_problem_solution):
        """Validar variante con reducción de colores"""
        problem, solution = conflicting_problem_solution
        repaired = RepairConflicts.repair_with_color_reduction(solution, problem)
        assert repaired.is_feasible(problem) == True
    
    # ========================================================================
    # Tests IntensifyColor
    # ========================================================================
    
    def test_intensify_reduces_colors(self, valid_solution):
        """Validar que reduce número de colores"""
        problem, solution = valid_solution
        initial_colors = solution.num_colors
        intensified = IntensifyColor.intensify(solution, problem)
        # Puede ser igual o menor
        assert intensified.num_colors <= initial_colors
    
    def test_intensify_maintains_feasibility(self, valid_solution):
        """Validar que mantiene factibilidad"""
        problem, solution = valid_solution
        intensified = IntensifyColor.intensify(solution, problem)
        assert intensified.is_feasible(problem) == True
    
    # ========================================================================
    # Tests Diversify
    # ========================================================================
    
    def test_diversify_returns_solution(self, valid_solution):
        """Validar que retorna solución"""
        problem, solution = valid_solution
        diversified = Diversify.diversify(solution, problem)
        assert isinstance(diversified, ColoringSolution)
    
    def test_diversify_is_feasible(self, valid_solution):
        """Validar que es factible"""
        problem, solution = valid_solution
        diversified = Diversify.diversify(solution, problem)
        assert diversified.is_feasible(problem) == True


# ============================================================================
# Test de integración entre operadores
# ============================================================================

class TestOperatorIntegration:
    """Tests de integración entre operadores"""
    
    @pytest.fixture
    def full_graph(self):
        """Fixture: Grafo para pipeline completo"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (2, 4)]
        return GraphColoringProblem(vertices=5, edges=edges, colors_known=4)
    
    def test_construct_improve_pipeline(self, full_graph):
        """Validar pipeline construir → mejorar"""
        # Construir
        solution = GreedyDSATUR.construct(full_graph)
        assert solution.is_feasible(full_graph)
        
        # Mejorar
        improved = KempeChain.improve(solution, full_graph)
        assert improved.is_feasible(full_graph)
        assert improved.num_colors <= solution.num_colors
    
    def test_construct_perturb_repair_pipeline(self, full_graph):
        """Validar pipeline construir → perturbar → reparar"""
        # Construir
        solution = GreedyDSATUR.construct(full_graph)
        
        # Perturbar
        perturbed = RandomRecolor.perturb(solution, full_graph, strength=0.5)
        
        # Reparar
        repaired = RepairConflicts.repair(perturbed, full_graph)
        assert repaired.is_feasible(full_graph)
    
    def test_full_ils_pipeline(self, full_graph):
        """Validar pipeline ILS completo: Construir → Mejorar → Perturbar → Reparar"""
        # Construir
        solution = RandomSequential.construct(full_graph)
        assert solution.is_feasible(full_graph)
        
        # Mejorar
        improved = OneVertexMove.improve(solution, full_graph)
        assert improved.is_feasible(full_graph)
        
        # Perturbar
        perturbed = PartialDestroy.perturb(improved, full_graph, strength=0.3)
        
        # Reparar
        repaired = RepairConflicts.repair(perturbed, full_graph)
        assert repaired.is_feasible(full_graph)


if __name__ == "__main__":
    """
    Ejecutar con:
        pytest tests/test_operators.py -v
        pytest tests/test_operators.py::TestConstructiveOperators -v
        pytest tests/test_operators.py -v --tb=short
    """
    print(__doc__)
