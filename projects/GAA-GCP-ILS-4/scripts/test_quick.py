#!/usr/bin/env python3
"""
test_quick.py - Validación rápida (10s)
Verifica que los componentes principales funcionan correctamente

Uso:
    python scripts/test_quick.py

Salida:
    ✓ componente funciona
    ✗ componente falla
    
    RESULTADO: X/5 tests pasados
"""

import sys
import time
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """✓ Validar que todos los imports funcionan correctamente"""
    try:
        from core.problem import GraphColoringProblem
        from core.solution import ColoringSolution
        from core.evaluation import ColoringEvaluator
        print("✓ Imports de core exitosos")
        return True
    except ImportError as e:
        print(f"✗ Error en imports de core: {e}")
        return False


def test_simple_problem():
    """✓ Crear y validar un problema simple (triángulo)"""
    try:
        from core.problem import GraphColoringProblem
        
        # Crear triángulo: 3 vértices, 3 aristas, requiere 3 colores
        edges = [(1, 2), (2, 3), (1, 3)]
        problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
        
        # Validaciones
        assert problem.n_vertices == 3, f"Vértices: esperado 3, obtenido {problem.n_vertices}"
        assert problem.n_edges == 3, f"Aristas: esperado 3, obtenido {problem.n_edges}"
        assert problem.colors_known == 3, f"Colores: esperado 3, obtenido {problem.colors_known}"
        
        print("✓ Problema simple (triángulo) creado correctamente")
        return True
    except Exception as e:
        print(f"✗ Error creando problema simple: {e}")
        return False


def test_solution_creation():
    """✓ Crear solución válida para problema simple"""
    try:
        from core.problem import GraphColoringProblem
        from core.solution import ColoringSolution
        
        edges = [(1, 2), (2, 3), (1, 3)]
        problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
        
        # Crear solución válida: cada vértice color diferente
        assignment = {1: 0, 2: 1, 3: 2}
        solution = ColoringSolution(assignment=assignment)
        
        # Validaciones
        assert solution.num_colors == 3, f"Colores: esperado 3, obtenido {solution.num_colors}"
        assert solution.is_feasible(problem), "Solución debe ser factible"
        
        print("✓ Solución válida creada y validada")
        return True
    except Exception as e:
        print(f"✗ Error creando solución: {e}")
        return False


def test_dimacs_loading():
    """✓ Cargar problema desde archivo DIMACS si existe"""
    try:
        from core.problem import GraphColoringProblem
        from pathlib import Path
        
        # Buscar archivo DIMACS de ejemplo
        dimacs_path = Path("projects/GAA-GCP-ILS-4/datasets/myciel3.col")
        if not dimacs_path.exists():
            print("⊘ Archivo DIMACS no encontrado (opcional)")
            return True
        
        problem = GraphColoringProblem.load_from_dimacs(str(dimacs_path))
        assert problem.n_vertices > 0, "Debe tener vértices"
        assert problem.n_edges > 0, "Debe tener aristas"
        
        print(f"✓ Archivo DIMACS cargado: {problem.n_vertices} vértices, {problem.n_edges} aristas")
        return True
    except FileNotFoundError:
        print("⊘ Archivo DIMACS no encontrado (opcional)")
        return True
    except Exception as e:
        print(f"✗ Error cargando DIMACS: {e}")
        return False


def test_evaluator():
    """✓ Evaluar solución y calcular métricas"""
    try:
        from core.problem import GraphColoringProblem
        from core.solution import ColoringSolution
        from core.evaluation import ColoringEvaluator
        
        # Problema simple
        edges = [(1, 2), (2, 3), (1, 3)]
        problem = GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
        
        # Solución válida
        solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 2})
        
        # Evaluar
        metrics = ColoringEvaluator.evaluate(solution, problem)
        
        # Validaciones
        assert metrics['feasible'] == True, "Debe ser factible"
        assert metrics['num_colors'] == 3, "Debe tener 3 colores"
        assert metrics['conflicts'] == 0, "Debe tener 0 conflictos"
        
        print(f"✓ Evaluador funcionando: {metrics['num_colors']} colores, {metrics['conflicts']} conflictos")
        return True
    except Exception as e:
        print(f"✗ Error en evaluador: {e}")
        return False


def main():
    """Ejecutar validación rápida"""
    print("\n" + "="*60)
    print("  VALIDACIÓN RÁPIDA - GCP con ILS")
    print("  Verifica funcionamiento básico de componentes")
    print("="*60 + "\n")
    
    start = time.time()
    
    # Lista de tests
    tests = [
        ("Imports", test_imports),
        ("Problema simple", test_simple_problem),
        ("Creación de solución", test_solution_creation),
        ("Carga DIMACS", test_dimacs_loading),
        ("Evaluador", test_evaluator),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"[{len(results)+1}/{len(tests)}] {name}...")
        result = test_func()
        results.append(result)
        print()
    
    elapsed = time.time() - start
    
    # Resumen
    print("="*60)
    passed = sum(results)
    total = len(results)
    status = "✓ EXITOSO" if all(results) else "✗ FALLÓ"
    print(f"  RESULTADO: {passed}/{total} tests pasados  {status}")
    print(f"  Tiempo total: {elapsed:.2f}s")
    print("="*60 + "\n")
    
    # Instrucciones siguientes
    if all(results):
        print("✓ Validación rápida completada exitosamente")
        print("\nPróximos pasos:")
        print("  1. Implementar core/problem.py, core/solution.py, core/evaluation.py")
        print("  2. Implementar operators/ (constructive, improvement, perturbation)")
        print("  3. Implementar metaheuristic/ils_core.py")
        print("  4. Ejecutar pytest: pytest tests/ -v")
        print("  5. Ejecutar demo_complete.py para ver resultados\n")
    else:
        print("✗ Algunos tests fallaron. Revisa los errores arriba.\n")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
