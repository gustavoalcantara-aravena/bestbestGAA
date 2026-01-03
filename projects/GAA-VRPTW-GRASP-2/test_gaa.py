#!/usr/bin/env python
"""Test GAA Algorithm Generation"""

from gaa import AlgorithmGenerator

# Test generation
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()

print('[TEST] Generación de 3 algoritmos GAA exitosa')
for algo in algos:
    print(f"  - {algo['name']}: patrón={algo['pattern']}, profundidad={algo['stats']['depth']}, tamaño={algo['stats']['size']}")

print()
print('[TEST] Pseudocódigo del primer algoritmo:')
print(algos[0]['name'])
print("-" * 70)

# Recreate AST from dict to show pseudocode
# For now just show the pattern
print(f"Patrón: {algos[0]['pattern']}")
print(f"Estructura AST (JSON): {algos[0]['ast']}")
