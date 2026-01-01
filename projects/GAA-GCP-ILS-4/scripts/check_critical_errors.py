#!/usr/bin/env python3
"""
check_critical_errors.py - Revisar errores críticos en el sistema
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print('='*80)
print('REVISION DE ERRORES CRITICOS EN EL SISTEMA')
print('='*80)
print()

# 1. Verificar sintaxis de módulos principales
print('1. Verificando sintaxis de modulos principales...')
modules_to_check = [
    'core/problem.py',
    'core/solution.py',
    'gaa/grammar.py',
    'gaa/generator.py',
    'gaa/interpreter.py',
    'scripts/test_experiment_quick.py',
    'scripts/run_full_experiment.py',
    'utils/algorithm_visualizer.py'
]

import py_compile
syntax_errors = []
for module in modules_to_check:
    try:
        py_compile.compile(module, doraise=True)
        print(f'   OK {module}')
    except py_compile.PyCompileError as e:
        print(f'   ERROR {module}: {e}')
        syntax_errors.append(module)

print()

# 2. Verificar imports críticos
print('2. Verificando imports criticos...')
import_errors = []

try:
    from core.problem import GraphColoringProblem
    print('   OK GraphColoringProblem')
except Exception as e:
    print(f'   ERROR GraphColoringProblem: {e}')
    import_errors.append('GraphColoringProblem')

try:
    from gaa.grammar import Grammar
    print('   OK Grammar')
except Exception as e:
    print(f'   ERROR Grammar: {e}')
    import_errors.append('Grammar')

try:
    from gaa.generator import AlgorithmGenerator
    print('   OK AlgorithmGenerator')
except Exception as e:
    print(f'   ERROR AlgorithmGenerator: {e}')
    import_errors.append('AlgorithmGenerator')

try:
    from utils.algorithm_visualizer import extract_algorithm_structure
    print('   OK algorithm_visualizer')
except Exception as e:
    print(f'   ERROR algorithm_visualizer: {e}')
    import_errors.append('algorithm_visualizer')

print()

# 3. Verificar BKS loading
print('3. Verificando carga de BKS...')
bks_errors = []
try:
    problem = GraphColoringProblem.load_from_dimacs('datasets/MYC/myciel3.col')
    if problem.colors_known == 4:
        print(f'   OK BKS cargado correctamente (myciel3: {problem.colors_known})')
    else:
        print(f'   ERROR BKS incorrecto (myciel3: {problem.colors_known}, esperado 4)')
        bks_errors.append('myciel3')
except Exception as e:
    print(f'   ERROR cargando BKS: {e}')
    bks_errors.append('load_bks')

print()

# 4. Verificar generación de algoritmos
print('4. Verificando generacion de algoritmos...')
gen_errors = []
try:
    grammar = Grammar(min_depth=2, max_depth=5)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    algo = generator.generate_fixed_structure()
    
    if algo:
        stats = grammar.get_statistics(algo)
        if stats['total_nodes'] == 5 and stats['depth'] == 3:
            print(f'   OK Algoritmo generado (nodos={stats["total_nodes"]}, profundidad={stats["depth"]})')
        else:
            print(f'   ERROR Estructura incorrecta (nodos={stats["total_nodes"]}, profundidad={stats["depth"]})')
            gen_errors.append('structure')
    else:
        print(f'   ERROR No se pudo generar algoritmo')
        gen_errors.append('generate')
except Exception as e:
    print(f'   ERROR generando algoritmo: {e}')
    gen_errors.append('generate')
    import traceback
    traceback.print_exc()

print()

# 5. Verificar extracción de estructura
print('5. Verificando extraccion de estructura...')
extract_errors = []
try:
    from utils.algorithm_visualizer import extract_algorithm_structure
    grammar = Grammar(min_depth=2, max_depth=5)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    algo = generator.generate_fixed_structure()
    
    structure = extract_algorithm_structure(algo, 1)
    
    if structure['constructive'] and structure['improvement'] and structure['perturbation']:
        print(f'   OK Estructura extraida correctamente')
        print(f'      - Constructivo: {structure["constructive"]}')
        print(f'      - Mejora: {structure["improvement"]}')
        print(f'      - Perturbacion: {structure["perturbation"]}')
    else:
        print(f'   ERROR Estructura incompleta: {structure}')
        extract_errors.append('incomplete')
except Exception as e:
    print(f'   ERROR extrayendo estructura: {e}')
    extract_errors.append('extract')
    import traceback
    traceback.print_exc()

print()

# 6. Resumen
print('='*80)
total_errors = len(syntax_errors) + len(import_errors) + len(bks_errors) + len(gen_errors) + len(extract_errors)

if total_errors == 0:
    print('OK NO HAY ERRORES CRITICOS EN EL SISTEMA')
else:
    print(f'ERROR ERRORES ENCONTRADOS: {total_errors}')
    if syntax_errors:
        print(f'  - Sintaxis: {syntax_errors}')
    if import_errors:
        print(f'  - Imports: {import_errors}')
    if bks_errors:
        print(f'  - BKS: {bks_errors}')
    if gen_errors:
        print(f'  - Generacion: {gen_errors}')
    if extract_errors:
        print(f'  - Extraccion: {extract_errors}')

print('='*80)
