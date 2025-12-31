"""
Tests para modulo CORE

Pruebas unitarias para GraphColoringProblem, ColoringSolution, ColoringEvaluator
"""

import pytest
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator


class TestGraphColoringProblem:
    """Tests para GraphColoringProblem"""
    
    @pytest.fixture
    def simple_problem(self):
        """Problema simple: triangulo (3 vertices)"""
        vertices = 3
        edges = [(0, 1), (1, 2), (0, 2)]
        return GraphColoringProblem(vertices, edges)
    
    @pytest.fixture
    def larger_problem(self):
        """Problema mayor: completo K5 (5 vertices)"""
        vertices = 5
        edges = [(i, j) for i in range(5) for j in range(i+1, 5)]
        return GraphColoringProblem(vertices, edges)
    
    def test_creation(self, simple_problem):
        """Test creacion basica"""
        assert simple_problem.vertices == 3
        assert simple_problem.edges == 3
    
    def test_adjacency_list(self, simple_problem):
        """Test construccion de lista de adyacencia"""
        neighbors_0 = set(simple_problem.get_neighbors(0))
        assert neighbors_0 == {1, 2}
        
        neighbors_1 = set(simple_problem.get_neighbors(1))
        assert neighbors_1 == {0, 2}
    
    def test_degree(self, simple_problem):
        """Test calculo de grados"""
        assert simple_problem.get_degree(0) == 2
        assert simple_problem.get_degree(1) == 2
        assert simple_problem.get_degree(2) == 2
    
    def test_properties(self, simple_problem):
        """Test propiedades del grafo"""
        assert simple_problem.num_edges == 3
        assert simple_problem.max_degree == 2
        assert simple_problem.min_degree == 2
        assert simple_problem.avg_degree == pytest.approx(2.0)
        assert 0 <= simple_problem.density <= 1
    
    def test_is_adjacent(self, simple_problem):
        """Test adyacencia"""
        assert simple_problem.is_adjacent(0, 1)
        assert simple_problem.is_adjacent(1, 0)
        assert not simple_problem.is_adjacent(0, 0)
    
    def test_serialization(self, simple_problem):
        """Test serializacion JSON"""
        data = simple_problem.to_dict()
        assert 'vertices' in data
        assert 'edges' in data
        
        restored = GraphColoringProblem.from_dict(data)
        assert restored.vertices == simple_problem.vertices
        assert restored.edges == simple_problem.edges
    
    def test_invalid_edges(self):
        """Test validacion de aristas invalidas"""
        with pytest.raises(ValueError):
            # Arista a si mismo
            GraphColoringProblem(3, [(0, 0)])
        
        with pytest.raises(ValueError):
            # Vertice fuera de rango
            GraphColoringProblem(3, [(0, 5)])


class TestColoringSolution:
    """Tests para ColoringSolution"""
    
    @pytest.fixture
    def problem(self):
        """Problema triangulo"""
        vertices = 3
        edges = [(0, 1), (1, 2), (0, 2)]
        return GraphColoringProblem(vertices, edges)
    
    @pytest.fixture
    def feasible_solution(self, problem):
        """Solucion factible (3 colores para triangulo)"""
        assignment = np.array([0, 1, 2])
        return ColoringSolution(assignment, problem)
    
    @pytest.fixture
    def infeasible_solution(self, problem):
        """Solucion infactible (conflictos)"""
        assignment = np.array([0, 0, 0])  # Todos el mismo color
        return ColoringSolution(assignment, problem)
    
    def test_creation(self, problem, feasible_solution):
        """Test creacion basica"""
        assert feasible_solution.num_colors == 3
        assert feasible_solution.is_feasible()
    
    def test_num_colors(self, problem):
        """Test conteo de colores"""
        assignment = np.array([0, 1, 0])
        solution = ColoringSolution(assignment, problem)
        assert solution.num_colors == 2
    
    def test_conflicts_detection(self, problem, infeasible_solution):
        """Test deteccion de conflictos"""
        assert infeasible_solution.num_conflicts > 0
        assert not infeasible_solution.is_feasible()
    
    def test_conflicting_vertices(self, problem):
        """Test vertices con conflictos"""
        assignment = np.array([0, 0, 1])
        solution = ColoringSolution(assignment, problem)
        
        conflicting = solution.get_conflicting_vertices()
        assert 0 in conflicting or 1 in conflicting
    
    def test_available_colors(self, problem, feasible_solution):
        """Test colores disponibles"""
        available_0 = feasible_solution.get_available_colors(0)
        assert 0 not in available_0  # Vecinos de 0 tienen colores 1,2
        assert 1 not in available_0
        assert 2 not in available_0
    
    def test_color_classes(self, problem):
        """Test clases de colores"""
        assignment = np.array([0, 0, 1])
        solution = ColoringSolution(assignment, problem)
        
        color_classes = solution.color_classes
        assert 0 in color_classes
        assert 1 in color_classes
        assert set(color_classes[0]) == {0, 1}
        assert set(color_classes[1]) == {2}
    
    def test_copy(self, problem, feasible_solution):
        """Test copia de solucion"""
        copy = feasible_solution.copy()
        
        # Modificar copia
        copy.assignment[0] = 99
        
        # Original no debe cambiar
        assert feasible_solution.assignment[0] != 99
    
    def test_serialization(self, problem, feasible_solution):
        """Test serializacion"""
        data = feasible_solution.to_dict()
        assert 'assignment' in data
        assert 'num_colors' in data
        assert 'num_conflicts' in data
    
    def test_fitness(self, problem, feasible_solution, infeasible_solution):
        """Test calculo de fitness"""
        feasible_fitness = feasible_solution.fitness()
        infeasible_fitness = infeasible_solution.fitness()
        
        assert feasible_fitness < infeasible_fitness
        assert feasible_fitness >= 0


class TestColoringEvaluator:
    """Tests para ColoringEvaluator"""
    
    @pytest.fixture
    def problem(self):
        """Problema triangulo"""
        vertices = 3
        edges = [(0, 1), (1, 2), (0, 2)]
        return GraphColoringProblem(vertices, edges)
    
    def test_evaluate_feasible(self, problem):
        """Test evaluacion de solucion factible"""
        assignment = np.array([0, 1, 2])
        solution = ColoringSolution(assignment, problem)
        
        metrics = ColoringEvaluator.evaluate(solution, problem)
        
        assert metrics['num_colors'] == 3
        assert metrics['num_conflicts'] == 0
        assert metrics['is_feasible']
        assert 'fitness' in metrics
    
    def test_evaluate_infeasible(self, problem):
        """Test evaluacion de solucion infactible"""
        assignment = np.array([0, 0, 0])
        solution = ColoringSolution(assignment, problem)
        
        metrics = ColoringEvaluator.evaluate(solution, problem)
        
        assert metrics['num_colors'] == 1
        assert metrics['num_conflicts'] > 0
        assert not metrics['is_feasible']
    
    def test_batch_evaluate(self, problem):
        """Test evaluacion en lote"""
        solutions = [
            ColoringSolution(np.array([0, 1, 2]), problem),
            ColoringSolution(np.array([0, 1, 0]), problem),
        ]
        
        all_metrics = ColoringEvaluator.batch_evaluate(solutions, problem)
        
        assert len(all_metrics) == 2
        assert all_metrics[0]['num_colors'] == 3
        assert all_metrics[1]['num_colors'] == 2
    
    def test_compare_solutions(self, problem):
        """Test comparacion de soluciones"""
        sol1 = ColoringSolution(np.array([0, 1, 2]), problem)
        sol2 = ColoringSolution(np.array([0, 1, 0]), problem)
        
        better = ColoringEvaluator.compare_solutions(sol1, sol2, problem)
        
        assert better == sol1  # sol1 es factible, sol2 no
    
    def test_print_report(self, problem, capsys):
        """Test reporte formateado"""
        solution = ColoringSolution(np.array([0, 1, 2]), problem)
        
        ColoringEvaluator.print_report(solution, problem)
        
        captured = capsys.readouterr()
        assert 'Colors' in captured.out or 'Colores' in captured.out


class TestIntegration:
    """Tests de integracion entre componentes"""
    
    def test_complete_workflow(self):
        """Test flujo completo: crear problema, solucion, evaluar"""
        # Crear problema
        problem = GraphColoringProblem(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
        
        # Crear solucion
        assignment = np.array([0, 1, 0, 1])
        solution = ColoringSolution(assignment, problem)
        
        # Evaluar
        metrics = ColoringEvaluator.evaluate(solution, problem)
        
        assert metrics['num_colors'] == 2
        assert metrics['is_feasible']
    
    def test_empty_problem(self):
        """Test problema sin aristas"""
        problem = GraphColoringProblem(3, [])
        
        assignment = np.array([0, 0, 0])
        solution = ColoringSolution(assignment, problem)
        
        assert solution.is_feasible()
        assert solution.num_colors == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
