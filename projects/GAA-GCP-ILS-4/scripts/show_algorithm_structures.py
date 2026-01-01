#!/usr/bin/env python3
"""
show_algorithm_structures.py - Mostrar estructura detallada de 3 algoritmos GAA generados
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from utils.algorithm_visualizer import extract_algorithm_structure, print_algorithm_structure, print_algorithms_comparison

print("\n" + "="*100)
print("GENERACIÓN Y VISUALIZACIÓN DE 3 ALGORITMOS GAA")
print("="*100)
print()

# Crear gramática y generador
print("📋 Inicializando gramática GAA...")
grammar = Grammar(min_depth=2, max_depth=5)
generator = AlgorithmGenerator(grammar=grammar, seed=42)
print("✅ Gramática inicializada\n")

# Generar 3 algoritmos
print("📋 Generando 3 algoritmos GAA con seed=42...")
gaa_algorithms = []
for i in range(3):
    print(f"   ⏳ Generando GAA_Algorithm_{i+1}...", end=" ", flush=True)
    algo = generator.generate_fixed_structure()
    if algo:
        gaa_algorithms.append(algo)
        stats = grammar.get_statistics(algo)
        print(f"✅ GENERADO (nodos={stats['total_nodes']}, profundidad={stats['depth']})")
    else:
        print(f"❌ FALLO")

print()

if not gaa_algorithms:
    print("❌ Error: No se pudieron generar algoritmos")
    sys.exit(1)

# Extraer y mostrar estructura detallada
print("="*100)
print("ESTRUCTURA DETALLADA DE CADA ALGORITMO")
print("="*100)
print()

algorithm_structures = []
for algo_idx, algo in enumerate(gaa_algorithms, 1):
    structure = extract_algorithm_structure(algo, algo_idx)
    algorithm_structures.append(structure)
    print_algorithm_structure(structure)

# Mostrar comparación
print_algorithms_comparison(algorithm_structures)

print("="*100)
print("✅ VISUALIZACIÓN COMPLETADA")
print("="*100)
