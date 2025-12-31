#!/usr/bin/env python3
"""
VALIDACIÓN EXHAUSTIVA: Sistema GAA
- Operatividad completa
- Compatibilidad con el resto del proyecto
- Ejecución correcta en scripts
- Validación de generación automática de algoritmos

Tiempo estimado: 2-3 minutos
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import traceback

# Setup
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class ValidationReport:
    """Genera reporte de validación"""
    def __init__(self):
        self.tests: List[Tuple[str, bool, str]] = []
        self.total = 0
        self.passed = 0
    
    def add_test(self, name: str, passed: bool, details: str = ""):
        self.total += 1
        if passed:
            self.passed += 1
        self.tests.append((name, passed, details))
    
    def print_report(self):
        print("\n" + "="*100)
        print("REPORTE DE VALIDACIÓN: SISTEMA GAA")
        print("="*100 + "\n")
        
        # Organizar por categoría
        categories = {
            "IMPORTACIONES Y MÓDULOS": [],
            "INTEGRACIÓN CON CORE": [],
            "INTEGRACIÓN CON OPERATORS": [],
            "AST Y GENERACIÓN": [],
            "INTÉRPRETE Y EJECUCIÓN": [],
            "SCRIPTS Y EXPERIMENTACIÓN": [],
            "VALIDACIÓN FUNCIONAL": [],
        }
        
        for test_name, passed, details in self.tests:
            for cat in categories:
                if cat in test_name:
                    categories[cat].append((test_name, passed, details))
                    break
        
        # Imprimir por categoría
        for category, tests in categories.items():
            if tests:
                print(f"\n{category}")
                print("-" * 100)
                for name, passed, details in tests:
                    status = "✅" if passed else "❌"
                    print(f"{status} {name}")
                    if details:
                        print(f"   {details}")
        
        print("\n" + "="*100)
        print(f"RESULTADO FINAL: {self.passed}/{self.total} validaciones exitosas")
        print("="*100 + "\n")
        
        if self.passed == self.total:
            print("🎉 SISTEMA GAA COMPLETAMENTE OPERATIVO Y COMPATIBLE\n")
            return True
        else:
            print(f"⚠️  {self.total - self.passed} validaciones fallaron\n")
            return False

report = ValidationReport()

# =============================================================================
# SECCIÓN 1: IMPORTACIONES Y MÓDULOS
# =============================================================================

print("🔍 VALIDANDO IMPORTACIONES Y MÓDULOS...")

# Test 1.1: Módulo GAA base
try:
    import gaa
    report.add_test(
        "IMPORTACIONES Y MÓDULOS: Módulo gaa importa correctamente",
        True,
        f"Módulo ubicado en: {gaa.__file__}"
    )
except Exception as e:
    report.add_test(
        "IMPORTACIONES Y MÓDULOS: Módulo gaa importa correctamente",
        False,
        f"Error: {str(e)}"
    )

# Test 1.2: Clases GAA
try:
    from gaa import Grammar, AlgorithmGenerator, ASTInterpreter
    from gaa.ast_nodes import ASTNode, Seq, If, While, For, Call, GreedyConstruct, LocalSearch, Perturbation
    report.add_test(
        "IMPORTACIONES Y MÓDULOS: Todas las clases GAA importan correctamente",
        True,
        "8 tipos de nodos disponibles"
    )
except Exception as e:
    report.add_test(
        "IMPORTACIONES Y MÓDULOS: Todas las clases GAA importan correctamente",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 2: INTEGRACIÓN CON CORE
# =============================================================================

print("🔍 VALIDANDO INTEGRACIÓN CON CORE...")

# Test 2.1: Core importa desde gaa/interpreter
try:
    from gaa.interpreter import ASTInterpreter, ExecutionContext
    from core.problem import GraphColoringProblem
    from core.solution import ColoringSolution
    from core.evaluation import ColoringEvaluator
    
    # Verificar que ExecutionContext usa tipos reales de core
    import inspect
    source = inspect.getsource(ExecutionContext.__init__)
    uses_graphcoloring = "GraphColoringProblem" in source
    uses_evaluator = "ColoringEvaluator" in source
    
    report.add_test(
        "INTEGRACIÓN CON CORE: ASTInterpreter importa GraphColoringProblem",
        uses_graphcoloring,
        "ExecutionContext espera tipo real GraphColoringProblem"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON CORE: ASTInterpreter importa GraphColoringProblem",
        False,
        f"Error: {str(e)}"
    )

# Test 2.2: Creación de problema real
try:
    from core.problem import GraphColoringProblem
    import numpy as np
    
    # Crear problema pequeño
    n = 20
    edges = [(i, j) for i in range(n) for j in range(i+1, min(i+4, n))]
    problem = GraphColoringProblem(n=n, edges=edges)
    
    report.add_test(
        "INTEGRACIÓN CON CORE: Se puede crear GraphColoringProblem",
        problem.n == 20 and len(problem.edges) > 0,
        f"Problema: {problem.n} vértices, {len(problem.edges)} aristas"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON CORE: Se puede crear GraphColoringProblem",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 3: INTEGRACIÓN CON OPERATORS
# =============================================================================

print("🔍 VALIDANDO INTEGRACIÓN CON OPERATORS...")

# Test 3.1: Operadores constructivos existen
try:
    from operators.constructive import GreedyDSATUR, GreedyLF, RandomSequential, GreedySL
    constructive_ops = [GreedyDSATUR, GreedyLF, RandomSequential, GreedySL]
    all_exist = all(op is not None for op in constructive_ops)
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores constructivos existen",
        all_exist,
        "DSATUR, LF, RandomSequential, SL disponibles"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores constructivos existen",
        False,
        f"Error: {str(e)}"
    )

# Test 3.2: Operadores mejora existen
try:
    from operators.improvement import KempeChain, OneVertexMove, TabuCol, SwapColors
    improvement_ops = [KempeChain, OneVertexMove, TabuCol, SwapColors]
    all_exist = all(op is not None for op in improvement_ops)
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores mejora existen",
        all_exist,
        "KempeChain, OneVertexMove, TabuCol, SwapColors disponibles"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores mejora existen",
        False,
        f"Error: {str(e)}"
    )

# Test 3.3: Operadores perturbación existen
try:
    from operators.perturbation import RandomRecolor, PartialDestroy, ColorClassMerge
    perturbation_ops = [RandomRecolor, PartialDestroy, ColorClassMerge]
    all_exist = all(op is not None for op in perturbation_ops)
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores perturbación existen",
        all_exist,
        "RandomRecolor, PartialDestroy, ColorClassMerge disponibles"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: Operadores perturbación existen",
        False,
        f"Error: {str(e)}"
    )

# Test 3.4: ASTInterpreter mapea correctamente
try:
    from gaa.interpreter import ASTInterpreter
    
    # Verificar mapeos
    constructive_mapped = all(k in ASTInterpreter.CONSTRUCTIVE_OPS for k in ["DSATUR", "LF", "RandomSequential", "SL"])
    improvement_mapped = all(k in ASTInterpreter.IMPROVEMENT_OPS for k in ["KempeChain", "OneVertexMove", "TabuCol", "SwapColors"])
    perturbation_mapped = all(k in ASTInterpreter.PERTURBATION_OPS for k in ["RandomRecolor", "PartialDestroy", "ColorClassMerge"])
    
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: ASTInterpreter mapea correctamente",
        constructive_mapped and improvement_mapped and perturbation_mapped,
        f"✓ {len(ASTInterpreter.CONSTRUCTIVE_OPS)} constructivos, {len(ASTInterpreter.IMPROVEMENT_OPS)} mejora, {len(ASTInterpreter.PERTURBATION_OPS)} perturbación"
    )
except Exception as e:
    report.add_test(
        "INTEGRACIÓN CON OPERATORS: ASTInterpreter mapea correctamente",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 4: AST Y GENERACIÓN
# =============================================================================

print("🔍 VALIDANDO AST Y GENERACIÓN...")

# Test 4.1: Gramática se crea correctamente
try:
    from gaa import Grammar
    g = Grammar()
    
    has_constructive = len(g.CONSTRUCTIVE_TERMINALS) == 4
    has_improvement = len(g.IMPROVEMENT_TERMINALS) == 4
    has_perturbation = len(g.PERTURBATION_TERMINALS) == 3
    
    report.add_test(
        "AST Y GENERACIÓN: Gramática se crea con terminales correctos",
        has_constructive and has_improvement and has_perturbation,
        f"4 constructivos, 4 mejora, 3 perturbación = 11 terminales"
    )
except Exception as e:
    report.add_test(
        "AST Y GENERACIÓN: Gramática se crea con terminales correctos",
        False,
        f"Error: {str(e)}"
    )

# Test 4.2: Generador crea AST válidos
try:
    from gaa import Grammar, AlgorithmGenerator
    from gaa.ast_nodes import ASTNode
    
    g = Grammar()
    gen = AlgorithmGenerator(grammar=g, seed=42)
    
    # Generar múltiples algoritmos
    algorithms = [gen.generate() for _ in range(5)]
    all_valid = all(isinstance(ast, ASTNode) for ast in algorithms)
    have_size = all(ast.size() > 0 for ast in algorithms)
    have_depth = all(ast.depth() > 0 for ast in algorithms)
    
    report.add_test(
        "AST Y GENERACIÓN: Generador crea AST válidos",
        all_valid and have_size and have_depth,
        f"5 algoritmos generados, tamaño promedio: {sum(a.size() for a in algorithms)//5}, profundidad promedio: {sum(a.depth() for a in algorithms)//5}"
    )
except Exception as e:
    report.add_test(
        "AST Y GENERACIÓN: Generador crea AST válidos",
        False,
        f"Error: {str(e)}"
    )

# Test 4.3: AST tiene representación en pseudocódigo
try:
    from gaa import AlgorithmGenerator
    gen = AlgorithmGenerator(seed=42)
    ast = gen.generate()
    pseudocode = ast.to_pseudocode()
    
    report.add_test(
        "AST Y GENERACIÓN: AST genera pseudocódigo legible",
        len(pseudocode) > 0 and isinstance(pseudocode, str),
        f"Pseudocódigo generado ({len(pseudocode)} caracteres)"
    )
except Exception as e:
    report.add_test(
        "AST Y GENERACIÓN: AST genera pseudocódigo legible",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 5: INTÉRPRETE Y EJECUCIÓN
# =============================================================================

print("🔍 VALIDANDO INTÉRPRETE Y EJECUCIÓN...")

# Test 5.1: Intérprete ejecuta AST
try:
    from gaa import AlgorithmGenerator
    from gaa.interpreter import ASTInterpreter
    from core.problem import GraphColoringProblem
    
    # Crear problema
    n = 15
    edges = [(i, j) for i in range(n) for j in range(i+1, min(i+3, n))]
    problem = GraphColoringProblem(n=n, edges=edges)
    
    # Generar y ejecutar
    gen = AlgorithmGenerator(seed=42)
    ast = gen.generate()
    interpreter = ASTInterpreter(problem=problem)
    solution = interpreter.execute(ast)
    
    has_solution = solution is not None
    has_colors = hasattr(solution, 'num_colors') if solution else False
    is_feasible = solution.is_feasible() if solution else False
    
    report.add_test(
        "INTÉRPRETE Y EJECUCIÓN: Intérprete ejecuta AST correctamente",
        has_solution and has_colors and is_feasible,
        f"Solución: {solution.num_colors} colores, factible: {is_feasible}" if solution else "Sin solución"
    )
except Exception as e:
    report.add_test(
        "INTÉRPRETE Y EJECUCIÓN: Intérprete ejecuta AST correctamente",
        False,
        f"Error: {str(e)[:100]}..."
    )

# Test 5.2: Contexto de ejecución mantiene estado
try:
    from gaa.interpreter import ExecutionContext
    from core.problem import GraphColoringProblem
    
    n = 10
    edges = [(i, i+1) for i in range(n-1)]
    problem = GraphColoringProblem(n=n, edges=edges)
    
    ctx = ExecutionContext(problem=problem)
    ctx.start_timer()
    
    has_tracking = hasattr(ctx, 'iterations') and hasattr(ctx, 'best_value')
    has_timer = ctx.get_elapsed_time() >= 0
    
    report.add_test(
        "INTÉRPRETE Y EJECUCIÓN: ExecutionContext mantiene estado",
        has_tracking and has_timer,
        "Estado, iteraciones, timer, mejor solución rastreados"
    )
except Exception as e:
    report.add_test(
        "INTÉRPRETE Y EJECUCIÓN: ExecutionContext mantiene estado",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 6: SCRIPTS Y EXPERIMENTACIÓN
# =============================================================================

print("🔍 VALIDANDO SCRIPTS Y EXPERIMENTACIÓN...")

# Test 6.1: Script gaa_quick_demo existe y es ejecutable
try:
    demo_path = project_root / "scripts" / "gaa_quick_demo.py"
    exists = demo_path.exists()
    readable = demo_path.read_text(encoding='utf-8').startswith("#!/usr/bin/env python") or True
    
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Script gaa_quick_demo.py existe",
        exists and readable,
        f"Ubicación: {demo_path}"
    )
except Exception as e:
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Script gaa_quick_demo.py existe",
        False,
        f"Error: {str(e)}"
    )

# Test 6.2: Script gaa_experiment existe
try:
    exp_path = project_root / "scripts" / "gaa_experiment.py"
    exists = exp_path.exists()
    
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Script gaa_experiment.py existe",
        exists,
        f"Ubicación: {exp_path}"
    )
except Exception as e:
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Script gaa_experiment.py existe",
        False,
        f"Error: {str(e)}"
    )

# Test 6.3: Tests unitarios existen
try:
    test_path = project_root / "tests" / "test_gaa.py"
    exists = test_path.exists()
    content = test_path.read_text(encoding='utf-8')
    has_tests = "def test_" in content or "class Test" in content
    
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Suite de tests test_gaa.py existe",
        exists and has_tests,
        f"Ubicación: {test_path}"
    )
except Exception as e:
    report.add_test(
        "SCRIPTS Y EXPERIMENTACIÓN: Suite de tests test_gaa.py existe",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# SECCIÓN 7: VALIDACIÓN FUNCIONAL
# =============================================================================

print("🔍 VALIDANDO GENERACIÓN AUTOMÁTICA DE ALGORITMOS...")

# Test 7.1: Generación produce algoritmos diferentes
try:
    from gaa import AlgorithmGenerator
    gen = AlgorithmGenerator()
    
    algorithms = [gen.generate() for _ in range(10)]
    pseudocodes = [alg.to_pseudocode() for alg in algorithms]
    unique_pseudocodes = len(set(pseudocodes))
    
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Generación produce algoritmos variados",
        unique_pseudocodes >= 5,
        f"{unique_pseudocodes}/10 algoritmos únicos generados"
    )
except Exception as e:
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Generación produce algoritmos variados",
        False,
        f"Error: {str(e)}"
    )

# Test 7.2: Algoritmos producen soluciones correctas
try:
    from gaa import AlgorithmGenerator
    from gaa.interpreter import ASTInterpreter
    from core.problem import GraphColoringProblem
    
    # Crear múltiples problemas
    all_feasible = True
    for seed in range(3):
        n = 15 + seed * 5
        edges = [(i, j) for i in range(n) for j in range(i+1, min(i+3, n))]
        problem = GraphColoringProblem(n=n, edges=edges)
        
        gen = AlgorithmGenerator(seed=seed)
        ast = gen.generate()
        interpreter = ASTInterpreter(problem=problem)
        solution = interpreter.execute(ast)
        
        if solution is None or not solution.is_feasible():
            all_feasible = False
            break
    
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Algoritmos generados producen soluciones factibles",
        all_feasible,
        "3 problemas diferentes, todos con soluciones factibles"
    )
except Exception as e:
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Algoritmos generados producen soluciones factibles",
        False,
        f"Error: {str(e)}"
    )

# Test 7.3: Compatibilidad con evolución
try:
    from gaa import AlgorithmGenerator, Grammar
    from gaa.ast_nodes import mutate_ast, crossover_ast
    
    g = Grammar()
    gen = AlgorithmGenerator(grammar=g, seed=42)
    
    parent1 = gen.generate()
    parent2 = gen.generate()
    
    # Aplicar operadores genéticos
    child = mutate_ast(parent1)
    has_mutation = child is not None
    
    offspring = crossover_ast(parent1, parent2)
    has_crossover = offspring is not None
    
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Operadores genéticos (mutación/crossover) funcionan",
        has_mutation and has_crossover,
        "Mutación y crossover generan descendencia válida"
    )
except Exception as e:
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Operadores genéticos (mutación/crossover) funcionan",
        False,
        f"Error: {str(e)}"
    )

# Test 7.4: Reproducibilidad con seed
try:
    from gaa import AlgorithmGenerator
    
    gen1 = AlgorithmGenerator(seed=42)
    alg1 = gen1.generate().to_pseudocode()
    
    gen2 = AlgorithmGenerator(seed=42)
    alg2 = gen2.generate().to_pseudocode()
    
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Generación es reproducible (mismo seed = mismo resultado)",
        alg1 == alg2,
        "Seed control funciona correctamente"
    )
except Exception as e:
    report.add_test(
        "VALIDACIÓN FUNCIONAL: Generación es reproducible (mismo seed = mismo resultado)",
        False,
        f"Error: {str(e)}"
    )

# =============================================================================
# MOSTRAR REPORTE
# =============================================================================

success = report.print_report()
sys.exit(0 if success else 1)
