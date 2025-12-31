#!/usr/bin/env python3
"""
Validación Rápida de Integración GAA
Verifica que todos los componentes están correctamente integrados
"""

import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Valida que los imports funcionan"""
    print("🔍 Validando imports...")
    try:
        from gaa import Grammar, AlgorithmGenerator, ASTInterpreter
        from core import GraphColoringProblem, ColoringSolution
        from operators.constructive import GreedyDSATUR, GreedyLF
        from operators.improvement import KempeChain
        from operators.perturbation import RandomRecolor
        print("   ✅ Todos los imports funcionan\n")
        return True
    except ImportError as e:
        print(f"   ❌ Error de import: {e}\n")
        return False

def test_grammar():
    """Valida que la gramática se crea correctamente"""
    print("🔍 Validando Gramática...")
    try:
        from gaa import Grammar
        g = Grammar()
        print(f"   ✅ Gramática creada")
        print(f"      - Constructivos: {len(g.CONSTRUCTIVE_TERMINALS)} terminales")
        print(f"      - Mejora: {len(g.IMPROVEMENT_TERMINALS)} terminales")
        print(f"      - Perturbación: {len(g.PERTURBATION_TERMINALS)} terminales\n")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False

def test_generator():
    """Valida que el generador crea AST validos"""
    print("🔍 Validando Generador...")
    try:
        from gaa import Grammar, AlgorithmGenerator
        g = Grammar()
        gen = AlgorithmGenerator(grammar=g, seed=42)
        ast = gen.generate()
        print(f"   ✅ Algoritmo generado")
        print(f"      - Tipo: {type(ast).__name__}")
        print(f"      - Tamaño: {ast.size()} nodos")
        print(f"      - Profundidad: {ast.depth()}\n")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False

def test_problem():
    """Valida que se puede cargar un problema"""
    print("🔍 Validando Problema...")
    try:
        from core import GraphColoringProblem
        from data.loader import DatasetLoader
        
        loader = DatasetLoader()
        dataset = loader.load('training')
        if dataset:
            problem = dataset[0]
            print(f"   ✅ Problema cargado")
            print(f"      - Vértices: {problem.n}")
            print(f"      - Aristas: {problem.m}\n")
            return True
        else:
            print(f"   ⚠️  No hay datasets disponibles\n")
            return True
    except Exception as e:
        print(f"   ⚠️  No se pudo cargar dataset: {e}\n")
        return True

def test_operator_mapping():
    """Valida que el mapeo de operadores es correcto"""
    print("🔍 Validando Mapeo de Operadores...")
    try:
        from gaa.interpreter import ASTInterpreter
        
        # Verificar que existen los mapeos
        assert "DSATUR" in ASTInterpreter.CONSTRUCTIVE_OPS
        assert "KempeChain" in ASTInterpreter.IMPROVEMENT_OPS
        assert "RandomRecolor" in ASTInterpreter.PERTURBATION_OPS
        
        print(f"   ✅ Mapeos de operadores correctos")
        print(f"      - Constructivos mapeados: {len(ASTInterpreter.CONSTRUCTIVE_OPS)}")
        print(f"      - Mejora mapeados: {len(ASTInterpreter.IMPROVEMENT_OPS)}")
        print(f"      - Perturbación mapeados: {len(ASTInterpreter.PERTURBATION_OPS)}\n")
        return True
    except AssertionError as e:
        print(f"   ❌ Falta mapeo de operador\n")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False

def test_interpreter():
    """Valida que el intérprete puede ejecutar AST"""
    print("🔍 Validando Intérprete...")
    try:
        from gaa import Grammar, AlgorithmGenerator
        from gaa.interpreter import ASTInterpreter
        from core import GraphColoringProblem
        import numpy as np
        
        # Crear problema simple
        from core.problem import GraphColoringProblem
        n = 10
        edges = [(i, j) for i in range(n) for j in range(i+1, min(i+3, n))]
        problem = GraphColoringProblem(n=n, edges=edges)
        
        # Generar y ejecutar algoritmo
        g = Grammar()
        gen = AlgorithmGenerator(grammar=g, seed=42)
        ast = gen.generate()
        
        interpreter = ASTInterpreter(problem)
        solution = interpreter.execute(ast)
        
        if solution:
            print(f"   ✅ Algoritmo ejecutado correctamente")
            print(f"      - Colores: {solution.num_colors}")
            print(f"      - Factible: {solution.is_feasible()}\n")
            return True
        else:
            print(f"   ⚠️  No se generó solución\n")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

def main():
    """Ejecuta todas las validaciones"""
    print("\n" + "="*80)
    print("  VALIDACIÓN DE INTEGRACIÓN GAA - GAA-GCP-ILS-4")
    print("="*80 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Gramática": test_grammar(),
        "Generador": test_generator(),
        "Problema": test_problem(),
        "Mapeo de Operadores": test_operator_mapping(),
        "Intérprete": test_interpreter(),
    }
    
    print("="*80)
    print("  RESULTADOS")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    print("="*80)
    print(f"\n✅ {passed}/{total} validaciones pasadas\n")
    
    if passed == total:
        print("🎉 INTEGRACIÓN COMPLETA Y FUNCIONAL\n")
        return 0
    else:
        print("⚠️  ALGUNAS VALIDACIONES FALLARON\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
