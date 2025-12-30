"""
Test Script - Validación rápida de módulos VRPTW-GRASP

Prueba carga de datasets, creación de problemas y soluciones.
"""

import sys
from pathlib import Path

# Agregar ruta del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Imports locales
from data.loader import VRPTWDataLoader
from core.problem import VRPTWProblem
from core.solution import VRPTWSolution
from core.evaluation import VRPTWEvaluator


def test_data_loading():
    """Prueba carga de datos"""
    print("="*60)
    print("TEST 1: Data Loading")
    print("="*60)
    
    # Crear loader
    loader = VRPTWDataLoader(str(project_root / 'datasets'))
    
    # Mostrar familias disponibles
    print("\nAvailable Families:")
    print(loader.print_summary())
    
    # Listar instancias de C1
    print("\nInstances in C1:")
    instances = loader.list_instances('C1')
    for inst in instances.get('C1', [])[:3]:
        print(f"  - {inst}")
    
    return loader


def test_problem_loading(loader):
    """Prueba carga de problema"""
    print("\n" + "="*60)
    print("TEST 2: Problem Loading")
    print("="*60)
    
    # Cargar primera instancia de C1
    problem = loader.load_instance('C1', 'C101', vehicle_capacity=200)
    
    if problem is None:
        print("ERROR: Could not load C101")
        return None
    
    print(problem.summary())
    
    return problem


def test_solution_creation(problem):
    """Prueba creación de solución simple"""
    print("\n" + "="*60)
    print("TEST 3: Solution Creation")
    print("="*60)
    
    # Crear solución simple: cada cliente en su propia ruta
    routes = []
    for customer_id in range(1, min(6, problem.n_nodes)):  # Primeros 5 clientes
        route = [0, customer_id, 0]  # Depósito-Cliente-Depósito
        routes.append(route)
    
    solution = VRPTWSolution(routes, problem)
    
    print(solution.info())
    
    return solution


def test_evaluation(problem, solution):
    """Prueba evaluación de solución"""
    print("\n" + "="*60)
    print("TEST 4: Solution Evaluation")
    print("="*60)
    
    evaluator = VRPTWEvaluator(problem)
    
    metrics = evaluator.evaluate(solution)
    
    print("\nMetrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key:20s}: {value:.2f}")
        else:
            print(f"  {key:20s}: {value}")
    
    # Reporte de viabilidad
    feasibility = evaluator.get_feasibility_report(solution)
    
    print("\nFeasibility Report:")
    print(f"  Overall Feasible:    {feasibility['overall_feasible']}")
    print(f"  Capacity Violations: {feasibility['capacity_violations']}")
    print(f"  Time Violations:     {feasibility['time_violations']}")
    print(f"  Coverage Violations: {feasibility['coverage_violations']}")
    
    return evaluator


def test_load_family(loader):
    """Prueba carga de familia completa"""
    print("\n" + "="*60)
    print("TEST 5: Load Complete Family")
    print("="*60)
    
    instances = loader.load_family('C1', vehicle_capacity=200)
    
    print(f"\nLoaded {len(instances)} instances from C1:")
    
    for name, problem in list(instances.items())[:3]:
        print(f"  {name:10s}: {problem.n_customers:3d} customers, "
              f"capacity={problem.vehicle_capacity}, "
              f"demand={problem.total_demand}")
    
    if len(instances) > 3:
        print(f"  ... and {len(instances) - 3} more")
    
    return instances


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("VRPTW-GRASP Component Test Suite")
    print("="*60 + "\n")
    
    try:
        # Test 1: Data Loading
        loader = test_data_loading()
        
        # Test 2: Problem Loading
        problem = test_problem_loading(loader)
        if problem is None:
            print("\nERROR: Problem loading failed")
            return
        
        # Test 3: Solution Creation
        solution = test_solution_creation(problem)
        
        # Test 4: Evaluation
        evaluator = test_evaluation(problem, solution)
        
        # Test 5: Family Loading
        instances = test_load_family(loader)
        
        # Summary
        print("\n" + "="*60)
        print("Summary")
        print("="*60)
        print("✓ Data Loading         PASSED")
        print("✓ Problem Loading      PASSED")
        print("✓ Solution Creation    PASSED")
        print("✓ Solution Evaluation  PASSED")
        print("✓ Family Loading       PASSED")
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
