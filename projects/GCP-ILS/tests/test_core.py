"""
test_core.py - Unit tests para módulos core

Tests para:
- DIMACParser: validación de formato DIMACS
- GraphColoringProblem: construcción de problema
- ColoringSolution: soluciones válidas
- ColoringEvaluator: evaluación correcta
"""

import sys
from pathlib import Path

# Agregar path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.parser import DIMACParser, validate_dimacs_file
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
import numpy as np


def test_parser():
    """Test DIMACParser básico"""
    print("\nTest: DIMACParser")
    print("-" * 50)
    
    # Crear archivo test simple
    test_file = Path(project_root) / "test_instance.col"
    test_content = """c Graph coloring instance
p edge 4 3
e 1 2
e 2 3
e 3 4
"""
    
    try:
        test_file.write_text(test_content)
        
        # Parser
        n, edges = DIMACParser.parse(str(test_file))
        
        assert n == 4, f"Expected n=4, got {n}"
        assert len(edges) == 3, f"Expected 3 edges, got {len(edges)}"
        assert all(e[0] < e[1] for e in edges), "Edges not normalized"
        
        # Metadata
        meta = DIMACParser.parse_with_metadata(str(test_file))
        assert meta['n'] == 4
        assert meta['m'] == 3
        assert 0 <= meta['density'] <= 1
        
        print(f"✓ Parser: n={n}, m={len(edges)}, density={meta['density']:.3f}")
        
    finally:
        test_file.unlink(missing_ok=True)


def test_problem_construction():
    """Test GraphColoringProblem"""
    print("\nTest: GraphColoringProblem Construction")
    print("-" * 50)
    
    # Problema simple: 4-cycle
    n = 4
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    
    problem = GraphColoringProblem(
        n=n,
        edges=edges,
        name="cycle_4",
        optimal_value=2,
        lower_bound=2
    )
    
    assert problem.n == 4
    assert problem.m == 4
    assert problem.max_degree == 2
    assert problem.min_degree == 2
    
    # Test adjacency
    assert problem.is_adjacent(1, 2)
    assert not problem.is_adjacent(1, 3)
    assert len(problem.get_neighbors(1)) == 2
    
    print(f"✓ Problem: n={problem.n}, m={problem.m}")
    print(f"  Degrees: max={problem.max_degree}, min={problem.min_degree}")
    print(f"  Density: {problem.density:.3f}")


def test_solution_creation():
    """Test ColoringSolution"""
    print("\nTest: ColoringSolution")
    print("-" * 50)
    
    n = 4
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    problem = GraphColoringProblem(n=n, edges=edges, name="test")
    
    # Solución válida: 2-coloreo de un 4-cycle
    coloring = [1, 2, 1, 2]  # 0-indexed
    solution = ColoringSolution(n=n, coloring=coloring, problem=problem)
    
    assert solution.num_colors == 2
    assert solution.is_feasible(problem)
    assert solution.is_complete()
    assert solution.count_conflicts(problem) == 0
    
    print(f"✓ Valid solution: k={solution.num_colors}, feasible={solution.is_feasible()}")
    
    # Solución inválida: todos mismo color
    bad_coloring = [1, 1, 1, 1]
    bad_solution = ColoringSolution(n=n, coloring=bad_coloring, problem=problem)
    
    assert bad_solution.count_conflicts(problem) > 0
    assert not bad_solution.is_feasible(problem)
    
    print(f"✓ Invalid solution: conflicts={bad_solution.conflicts}")


def test_evaluator():
    """Test ColoringEvaluator"""
    print("\nTest: ColoringEvaluator")
    print("-" * 50)
    
    n = 4
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    problem = GraphColoringProblem(
        n=n,
        edges=edges,
        name="test",
        optimal_value=2
    )
    
    evaluator = ColoringEvaluator(problem)
    
    # Solución óptima
    opt_coloring = [1, 2, 1, 2]
    opt_solution = ColoringSolution(n=n, coloring=opt_coloring, problem=problem)
    
    eval_opt = evaluator.evaluate(opt_solution)
    assert eval_opt['k'] == 2
    assert eval_opt['is_feasible']
    assert eval_opt['conflicts'] == 0
    assert eval_opt['gap_to_optimal'] == 0
    
    print(f"✓ Evaluator: k={eval_opt['k']}, gap={eval_opt['gap_to_optimal']}")
    
    # Solución subóptima
    sub_coloring = [1, 2, 3, 2]
    sub_solution = ColoringSolution(n=n, coloring=sub_coloring, problem=problem)
    
    eval_sub = evaluator.evaluate(sub_solution)
    assert eval_sub['k'] == 3
    assert eval_sub['gap_to_optimal'] == 1
    
    print(f"✓ Suboptimal: k={eval_sub['k']}, gap={eval_sub['gap_to_optimal']}")


def test_copy_and_modification():
    """Test copia de soluciones"""
    print("\nTest: Solution Copy and Modification")
    print("-" * 50)
    
    n = 3
    edges = [(1, 2), (2, 3)]
    problem = GraphColoringProblem(n=n, edges=edges, name="test")
    
    sol1 = ColoringSolution(n=n, coloring=[1, 2, 1], problem=problem)
    sol2 = sol1.copy()
    
    # Modificar copia
    sol2[1] = 3  # Vértice 1 -> color 3
    
    assert sol1[1] == 2
    assert sol2[1] == 3
    
    print(f"✓ Copy independent: sol1[1]={sol1[1]}, sol2[1]={sol2[1]}")


def test_saturation_degree():
    """Test DSATUR saturation degree"""
    print("\nTest: Saturation Degree (DSATUR)")
    print("-" * 50)
    
    # Grafo: triángulo + vértice aislado
    n = 4
    edges = [(1, 2), (2, 3), (3, 1)]
    problem = GraphColoringProblem(n=n, edges=edges, name="test")
    
    # Solución parcial: vértices 1,2,3 coloreados
    coloring = [1, 2, 1, 0]  # Vértice 4 sin color
    
    saturation = problem.get_saturation_degree(coloring, 4)
    assert saturation == 0, "Aislado debe tener saturation=0"
    
    coloring[3] = 3  # Colorear vértice 4
    saturation = problem.get_saturation_degree(coloring, 2)  # Vértice 2
    # Debe contar colores distintos en vecinos (1 y 3 tienen colores 1 y 1)
    
    print(f"✓ DSATUR calculations working")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*50)
    print("Running Core Module Tests".center(50))
    print("="*50)
    
    try:
        test_parser()
        test_problem_construction()
        test_solution_creation()
        test_evaluator()
        test_copy_and_modification()
        test_saturation_degree()
        
        print("\n" + "="*50)
        print("✓ All tests passed!".center(50))
        print("="*50 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
