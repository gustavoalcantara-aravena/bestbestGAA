"""
tests/test_core.py
Suite de tests unitarios para los componentes Core del proyecto GCP-ILS

Ejecutar con:
    pytest tests/test_core.py -v
    
Cobertura:
    - GraphColoringProblem: Carga, validación, propiedades
    - ColoringSolution: Asignación, factibilidad, conflictos
    - ColoringEvaluator: Métricas, evaluación
"""

import pytest
import numpy as np
from pathlib import Path

from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator


class TestGraphColoringProblem:
    """Tests para GraphColoringProblem"""
    
    @pytest.fixture
    def triangle_problem(self):
        """Fixture: Problema simple (triángulo)"""
        edges = [(1, 2), (2, 3), (1, 3)]
        return GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
    
    @pytest.fixture
    def bipartite_problem(self):
        """Fixture: Grafo bipartito (ciclo de 4)"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=2)
    
    @pytest.fixture
    def complete_graph_5(self):
        """Fixture: Grafo completo K5"""
        edges = [(i, j) for i in range(1, 6) for j in range(i+1, 6)]
        return GraphColoringProblem(vertices=5, edges=edges, colors_known=5)
    
    @pytest.fixture
    def empty_problem(self):
        """Fixture: Grafo sin aristas"""
        return GraphColoringProblem(vertices=3, edges=[], colors_known=1)
    
    # ========================================================================
    # Tests básicos de propiedades
    # ========================================================================
    
    def test_vertices_count(self, triangle_problem):
        """Validar conteo de vértices"""
        assert triangle_problem.n_vertices == 3
    
    def test_edges_count(self, triangle_problem):
        """Validar conteo de aristas"""
        assert triangle_problem.n_edges == 3
    
    def test_empty_graph(self, empty_problem):
        """Validar grafo sin aristas"""
        assert empty_problem.n_vertices == 3
        assert empty_problem.n_edges == 0
    
    def test_colors_known_property(self, triangle_problem):
        """Validar propiedad colors_known"""
        assert triangle_problem.colors_known == 3
    
    # ========================================================================
    # Tests de adyacencia
    # ========================================================================
    
    def test_adjacency_list_exists(self, triangle_problem):
        """Validar que existe lista de adyacencia"""
        adj = triangle_problem.adjacency_list
        assert adj is not None
        assert 1 in adj
        assert 2 in adj
        assert 3 in adj
    
    def test_adjacency_list_connectivity(self, triangle_problem):
        """Validar conectividad en lista de adyacencia"""
        adj = triangle_problem.adjacency_list
        assert 2 in adj[1]  # 1 conectado con 2
        assert 3 in adj[1]  # 1 conectado con 3
        assert 1 in adj[2]  # 2 conectado con 1
        assert 3 in adj[2]  # 2 conectado con 3
    
    def test_is_edge_true(self, triangle_problem):
        """Validar detección de arista existente"""
        assert triangle_problem.is_edge(1, 2) == True
        assert triangle_problem.is_edge(2, 3) == True
        assert triangle_problem.is_edge(1, 3) == True
    
    def test_is_edge_false(self, triangle_problem):
        """Validar detección de arista inexistente"""
        assert triangle_problem.is_edge(1, 4) == False
        assert triangle_problem.is_edge(2, 4) == False
    
    def test_is_edge_symmetric(self, triangle_problem):
        """Validar simetría de aristas"""
        assert triangle_problem.is_edge(1, 2) == triangle_problem.is_edge(2, 1)
        assert triangle_problem.is_edge(2, 3) == triangle_problem.is_edge(3, 2)
    
    # ========================================================================
    # Tests de grados
    # ========================================================================
    
    def test_degree_of_vertex(self, triangle_problem):
        """Validar grado de vértice individual"""
        assert triangle_problem.degree(1) == 2
        assert triangle_problem.degree(2) == 2
        assert triangle_problem.degree(3) == 2
    
    def test_degree_sequence(self, triangle_problem):
        """Validar secuencia de grados"""
        degrees = triangle_problem.degree_sequence
        assert np.allclose(degrees, [2, 2, 2])
    
    def test_max_degree_triangle(self, triangle_problem):
        """Validar grado máximo en triángulo"""
        assert triangle_problem.max_degree == 2
    
    def test_max_degree_complete(self, complete_graph_5):
        """Validar grado máximo en grafo completo"""
        assert complete_graph_5.max_degree == 4  # K5: cada vértice conectado con 4
    
    def test_max_degree_bipartite(self, bipartite_problem):
        """Validar grado máximo en grafo bipartito"""
        assert bipartite_problem.max_degree == 2
    
    # ========================================================================
    # Tests de propiedades especiales
    # ========================================================================
    
    def test_is_bipartite_true(self, bipartite_problem):
        """Validar detección de grafo bipartito"""
        assert bipartite_problem.is_bipartite == True
    
    def test_is_bipartite_false(self, triangle_problem):
        """Validar que triángulo no es bipartito"""
        assert triangle_problem.is_bipartite == False
    
    def test_upper_bound_property(self, triangle_problem):
        """Validar cota superior calculada"""
        assert triangle_problem.upper_bound >= triangle_problem.colors_known
    
    # ========================================================================
    # Tests de validación
    # ========================================================================
    
    def test_invalid_vertex_count(self):
        """Validar rechazo de conteo de vértices negativo"""
        with pytest.raises(ValueError):
            GraphColoringProblem(vertices=0, edges=[])
    
    def test_invalid_edge_vertex_out_of_range(self):
        """Validar rechazo de vértices fuera de rango"""
        with pytest.raises(ValueError):
            GraphColoringProblem(vertices=3, edges=[(1, 5)])
    
    def test_invalid_self_loop(self):
        """Validar rechazo de autolazos"""
        with pytest.raises(ValueError):
            GraphColoringProblem(vertices=3, edges=[(1, 1)])


class TestColoringSolution:
    """Tests para ColoringSolution"""
    
    @pytest.fixture
    def valid_solution(self):
        """Fixture: Solución válida para triángulo"""
        assignment = {1: 0, 2: 1, 3: 2}
        return ColoringSolution(assignment=assignment)
    
    @pytest.fixture
    def suboptimal_solution(self):
        """Fixture: Solución subóptima pero válida"""
        assignment = {1: 0, 2: 1, 3: 1}  # Mismo color para 2 y 3 (no adyacentes en algunos)
        return ColoringSolution(assignment=assignment)
    
    @pytest.fixture
    def conflicting_solution(self):
        """Fixture: Solución con conflictos"""
        assignment = {1: 0, 2: 0, 3: 0}
        return ColoringSolution(assignment=assignment)
    
    @pytest.fixture
    def triangle_problem(self):
        """Fixture: Problema triángulo"""
        edges = [(1, 2), (2, 3), (1, 3)]
        return GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
    
    @pytest.fixture
    def cycle4_problem(self):
        """Fixture: Ciclo de 4 vértices"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        return GraphColoringProblem(vertices=4, edges=edges, colors_known=2)
    
    # ========================================================================
    # Tests básicos
    # ========================================================================
    
    def test_assignment_storage(self, valid_solution):
        """Validar almacenamiento de asignación"""
        assert valid_solution.assignment[1] == 0
        assert valid_solution.assignment[2] == 1
        assert valid_solution.assignment[3] == 2
    
    def test_num_colors_calculation(self, valid_solution):
        """Validar cálculo del número de colores"""
        assert valid_solution.num_colors == 3
    
    def test_num_colors_suboptimal(self, suboptimal_solution):
        """Validar cálculo de colores en solución subóptima"""
        assert suboptimal_solution.num_colors == 2
    
    def test_empty_assignment_invalid(self):
        """Validar rechazo de asignación vacía"""
        with pytest.raises(ValueError):
            ColoringSolution(assignment={})
    
    def test_invalid_color_negative(self):
        """Validar rechazo de colores negativos"""
        with pytest.raises(ValueError):
            ColoringSolution(assignment={1: -1})
    
    # ========================================================================
    # Tests de factibilidad
    # ========================================================================
    
    def test_is_feasible_valid_triangle(self, valid_solution, triangle_problem):
        """Validar que solución válida se reconoce como factible"""
        assert valid_solution.is_feasible(triangle_problem) == True
    
    def test_is_feasible_valid_cycle4(self, suboptimal_solution, cycle4_problem):
        """Validar factibilidad en ciclo de 4 con 2 colores"""
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 0, 4: 1})
        assert solution.is_feasible(cycle4_problem) == True
    
    def test_is_feasible_invalid(self, conflicting_solution, triangle_problem):
        """Validar que solución inválida se reconoce como no factible"""
        assert conflicting_solution.is_feasible(triangle_problem) == False
    
    # ========================================================================
    # Tests de conflictos
    # ========================================================================
    
    def test_num_conflicts_valid(self, valid_solution, triangle_problem):
        """Validar cero conflictos en solución válida"""
        assert valid_solution.num_conflicts(triangle_problem) == 0
    
    def test_num_conflicts_invalid(self, conflicting_solution, triangle_problem):
        """Validar conteo de conflictos en solución inválida"""
        # Triángulo: todas las aristas (1,2), (2,3), (1,3) tienen conflicto
        conflicts = conflicting_solution.num_conflicts(triangle_problem)
        assert conflicts == 3
    
    def test_conflicting_edges_detection(self, conflicting_solution, triangle_problem):
        """Validar detección de vértices en conflicto"""
        vertices = conflicting_solution.conflict_vertices(triangle_problem)
        # Triángulo: todas las aristas tienen conflicto cuando todos mismo color
        assert len(vertices) >= 1  # Al menos hay conflictos
    
    # ========================================================================
    # Tests de copias
    # ========================================================================
    
    def test_copy_independence(self, valid_solution):
        """Validar que copiar crea objeto independiente"""
        sol_copy = valid_solution.copy()
        sol_copy.assignment[1] = 99
        assert valid_solution.assignment[1] == 0
    
    def test_copy_content(self, valid_solution):
        """Validar que copia tiene contenido correcto"""
        sol_copy = valid_solution.copy()
        assert sol_copy.assignment == valid_solution.assignment


class TestColoringEvaluator:
    """Tests para ColoringEvaluator"""
    
    @pytest.fixture
    def triangle_setup(self):
        """Fixture: Problema y solución para triángulo"""
        edges = [(1, 2), (2, 3), (1, 3)]
        problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 2})
        return problem, solution
    
    @pytest.fixture
    def cycle4_valid(self):
        """Fixture: Ciclo de 4 con solución óptima"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        problem = GraphColoringProblem(vertices=4, edges=edges, colors_known=2)
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 0, 4: 1})
        return problem, solution
    
    @pytest.fixture
    def conflict_setup(self):
        """Fixture: Solución con conflictos"""
        edges = [(1, 2), (2, 3)]
        problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=2)
        solution = ColoringSolution(assignment={1: 0, 2: 0, 3: 1})
        return problem, solution
    
    # ========================================================================
    # Tests básicos de evaluación
    # ========================================================================
    
    def test_evaluate_returns_dict(self, triangle_setup):
        """Validar que evaluate retorna diccionario"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert isinstance(metrics, dict)
    
    def test_evaluate_contains_required_keys(self, triangle_setup):
        """Validar claves requeridas en resultado"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        required_keys = ['num_colors', 'conflicts', 'feasible', 'fitness']
        assert all(key in metrics for key in required_keys)
    
    # ========================================================================
    # Tests de métricas básicas
    # ========================================================================
    
    def test_evaluate_num_colors(self, triangle_setup):
        """Validar cálculo de colores"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert metrics['num_colors'] == 3
    
    def test_evaluate_conflicts_valid(self, triangle_setup):
        """Validar conflictos en solución válida"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert metrics['conflicts'] == 0
    
    def test_evaluate_conflicts_invalid(self, conflict_setup):
        """Validar conflictos en solución inválida"""
        problem, solution = conflict_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert metrics['conflicts'] >= 1
    
    def test_evaluate_feasible_valid(self, triangle_setup):
        """Validar factibilidad en solución válida"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert metrics['feasible'] == True
    
    def test_evaluate_feasible_invalid(self, conflict_setup):
        """Validar factibilidad en solución inválida"""
        problem, solution = conflict_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        assert metrics['feasible'] == False
    
    # ========================================================================
    # Tests de fitness
    # ========================================================================
    
    def test_fitness_valid_solution(self, triangle_setup):
        """Validar fitness para solución válida"""
        problem, solution = triangle_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        # Fitness debe ser al menos el número de colores
        assert metrics['fitness'] >= metrics['num_colors']
    
    def test_fitness_penalizes_conflicts(self, conflict_setup):
        """Validar que fitness penaliza conflictos"""
        problem, solution = conflict_setup
        metrics = ColoringEvaluator.evaluate(solution, problem)
        # Fitness con conflictos > num_colors
        assert metrics['fitness'] > metrics['num_colors']
    
    # ========================================================================
    # Tests de evaluación en lote
    # ========================================================================
    
    def test_batch_evaluate_returns_list(self, triangle_setup):
        """Validar que batch_evaluate retorna lista"""
        problem, solution = triangle_setup
        solutions = [solution, solution.copy()]
        results = ColoringEvaluator.batch_evaluate(solutions, problem)
        assert isinstance(results, list)
        assert len(results) == 2
    
    def test_batch_evaluate_all_dicts(self, triangle_setup):
        """Validar que batch retorna diccionarios"""
        problem, solution = triangle_setup
        solutions = [solution, solution.copy(), solution.copy()]
        results = ColoringEvaluator.batch_evaluate(solutions, problem)
        assert all(isinstance(r, dict) for r in results)
    
    def test_batch_evaluate_consistency(self, triangle_setup):
        """Validar consistencia entre batch y individual"""
        problem, solution = triangle_setup
        individual = ColoringEvaluator.evaluate(solution, problem)
        batch = ColoringEvaluator.batch_evaluate([solution], problem)[0]
        assert individual == batch
    
    # ========================================================================
    # Tests de comparación
    # ========================================================================
    
    def test_evaluate_better_than_comparison(self, triangle_setup):
        """Validar método is_better_than de soluciones"""
        problem, solution = triangle_setup
        solution2 = solution.copy()
        # Misma solución, no es mejor
        assert not solution.is_better_than(solution2, problem)


# ============================================================================
# Test de integración
# ============================================================================

class TestIntegration:
    """Tests de integración entre componentes"""
    
    def test_problem_solution_integration(self):
        """Validar integración problema-solución"""
        # Crear problema
        problem = GraphColoringProblem(
            vertices=5,
            edges=[(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)],
            colors_known=3
        )
        
        # Crear solución válida
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 0, 4: 1, 5: 2})
        
        # Validar
        assert solution.is_feasible(problem)
        assert solution.num_conflicts(problem) == 0
    
    def test_evaluation_pipeline(self):
        """Validar pipeline completo de evaluación"""
        # Crear instancia
        problem = GraphColoringProblem(
            vertices=4,
            edges=[(1, 2), (2, 3), (3, 4), (4, 1)],
            colors_known=2
        )
        
        # Crear solución
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 0, 4: 1})
        
        # Evaluar
        metrics = ColoringEvaluator.evaluate(solution, problem)
        
        # Validaciones
        assert metrics['feasible'] == True
        assert metrics['conflicts'] == 0
        assert metrics['num_colors'] == 2
        assert metrics['fitness'] >= 2


if __name__ == "__main__":
    """
    Ejecutar con:
        pytest tests/test_core.py -v                    # Todos
        pytest tests/test_core.py::TestGraphColoringProblem -v  # Específica
        pytest tests/test_core.py -v --tb=short         # Con traceback corto
    """
    print(__doc__)
