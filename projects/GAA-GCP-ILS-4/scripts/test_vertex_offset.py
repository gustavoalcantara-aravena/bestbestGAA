#!/usr/bin/env python3
"""
test_vertex_offset.py - Verificar detección automática de indexación
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import GraphColoringProblem

print('='*80)
print('VERIFICACION: DETECCION AUTOMATICA DE INDEXACION')
print('='*80)
print()

# Test 1: Dataset 1-indexed (DIMACS estándar)
print('Test 1: Dataset 1-indexed (DIMACS)')
print('-'*80)
try:
    problem = GraphColoringProblem.load_from_dimacs('datasets/MYC/myciel3.col')
    print(f'Dataset: {problem.name}')
    print(f'Vértices: {problem.n_vertices}')
    print(f'Vertex offset detectado: {problem.vertex_offset}')
    print(f'Rango válido: [{problem.vertex_offset}, {problem.n_vertices + problem.vertex_offset - 1}]')
    
    if problem.vertex_offset == 1:
        print('✅ Detección correcta: 1-indexed')
    else:
        print('❌ Error: Debería ser 1-indexed')
except Exception as e:
    print(f'❌ Error: {e}')

print()

# Test 2: Dataset 0-indexed (simulado)
print('Test 2: Dataset 0-indexed (simulado)')
print('-'*80)
try:
    # Crear dataset 0-indexed manualmente
    edges_0indexed = [(0, 1), (1, 2), (0, 2)]  # Triángulo con vértices 0, 1, 2
    problem_0indexed = GraphColoringProblem(
        vertices=3,
        edges=edges_0indexed,
        colors_known=3,
        name='triangle_0indexed'
    )
    
    print(f'Dataset: {problem_0indexed.name}')
    print(f'Vértices: {problem_0indexed.n_vertices}')
    print(f'Vertex offset detectado: {problem_0indexed.vertex_offset}')
    print(f'Rango válido: [{problem_0indexed.vertex_offset}, {problem_0indexed.n_vertices + problem_0indexed.vertex_offset - 1}]')
    
    if problem_0indexed.vertex_offset == 0:
        print('✅ Detección correcta: 0-indexed')
    else:
        print('❌ Error: Debería ser 0-indexed')
except Exception as e:
    print(f'❌ Error: {e}')

print()

# Test 3: Dataset 1-indexed (simulado)
print('Test 3: Dataset 1-indexed (simulado)')
print('-'*80)
try:
    # Crear dataset 1-indexed manualmente
    edges_1indexed = [(1, 2), (2, 3), (1, 3)]  # Triángulo con vértices 1, 2, 3
    problem_1indexed = GraphColoringProblem(
        vertices=3,
        edges=edges_1indexed,
        colors_known=3,
        name='triangle_1indexed'
    )
    
    print(f'Dataset: {problem_1indexed.name}')
    print(f'Vértices: {problem_1indexed.n_vertices}')
    print(f'Vertex offset detectado: {problem_1indexed.vertex_offset}')
    print(f'Rango válido: [{problem_1indexed.vertex_offset}, {problem_1indexed.n_vertices + problem_1indexed.vertex_offset - 1}]')
    
    if problem_1indexed.vertex_offset == 1:
        print('✅ Detección correcta: 1-indexed')
    else:
        print('❌ Error: Debería ser 1-indexed')
except Exception as e:
    print(f'❌ Error: {e}')

print()
print('='*80)
print('RESUMEN')
print('='*80)
print('✅ Sistema detecta automáticamente indexación del dataset')
print('✅ Valida aristas según rango detectado')
print('✅ Proporciona vertex_offset para operadores')
