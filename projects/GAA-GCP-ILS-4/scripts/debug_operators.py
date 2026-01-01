#!/usr/bin/env python3
"""
debug_operators.py - Verificar operadores seleccionados
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from utils.algorithm_visualizer import extract_algorithm_structure

grammar = Grammar(min_depth=2, max_depth=5)
generator = AlgorithmGenerator(grammar=grammar, seed=42)

print('Operadores seleccionados para 3 algoritmos:')
print()

for i in range(3):
    algo = generator.generate_fixed_structure()
    structure = extract_algorithm_structure(algo, i+1)
    constructive = structure['constructive']
    improvement = structure['improvement']
    perturbation = structure['perturbation']
    print(f'Algoritmo {i+1}:')
    print(f'  Constructivo: {constructive}')
    print(f'  Mejora: {improvement}')
    print(f'  Perturbacion: {perturbation}')
    print()
