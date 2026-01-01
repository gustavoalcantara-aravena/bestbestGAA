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

from utils import OutputManager


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
    
    # Crear gestor de outputs
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="gaa_experiment")
    print(f"📁 Sesión creada en: {session_dir}\n")
    
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
    test_details = []
    
    for name, test_func in tests:
        print(f"[{len(results)+1}/{len(tests)}] {name}...")
        result = test_func()
        results.append(result)
        test_details.append({
            'test_name': name,
            'passed': result,
            'status': '✓ PASÓ' if result else '✗ FALLÓ'
        })
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
    
    # Guardar resultados de tests
    summary_text = _generate_test_summary(test_details, passed, total, elapsed)
    output_mgr.save_statistics_txt(summary_text, filename="test_results.txt")
    
    output_mgr.save_detailed_json({
        'test_results': test_details,
        'summary': {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'elapsed_time': elapsed,
            'status': status
        }
    }, filename="test_results.json")
    
    print(f"✅ Resultados guardados en: {session_dir}\n")
    
    # Instrucciones siguientes
    if all(results):
        print("✓ Validación rápida completada exitosamente")
        print("\nPróximos pasos:")
        print("  1. Ejecutar pytest: pytest tests/ -v")
        print("  2. Ejecutar scripts/gaa_quick_demo.py para ver demo GAA")
        print("  3. Ejecutar scripts/gaa_experiment.py para evolucionar algoritmos\n")
    else:
        print("✗ Algunos tests fallaron. Revisa los errores arriba.\n")
    
    return 0 if all(results) else 1


def _generate_test_summary(test_details, passed, total, elapsed) -> str:
    """Genera resumen de tests en texto"""
    text = "RESULTADOS DE VALIDACIÓN RÁPIDA\n"
    text += "="*60 + "\n\n"
    text += f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    text += f"Total de tests: {total}\n"
    text += f"Tests pasados: {passed}\n"
    text += f"Tests fallidos: {total - passed}\n"
    text += f"Tiempo total: {elapsed:.2f}s\n\n"
    text += "DETALLE DE TESTS:\n"
    text += "-"*60 + "\n"
    
    for test in test_details:
        text += f"{test['status']:12} {test['test_name']}\n"
    
    text += "\n" + "="*60 + "\n"
    
    return text


if __name__ == "__main__":
    sys.exit(main())
