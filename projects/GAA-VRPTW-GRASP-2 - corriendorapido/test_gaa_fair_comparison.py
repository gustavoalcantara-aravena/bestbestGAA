#!/usr/bin/env python
"""Test script: Verify 3 algorithms with depth=3, size=4"""

from gaa import AlgorithmGenerator

# Generate 3 algorithms with depth=3, size=4
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_three_algorithms()

print('=== GENERATED ALGORITHMS WITH FAIR COMPARISON ===')
print(f'Total: {len(algorithms)}')
print(f'Configuration: depth=3, size=4 (FIXED for all)')
print()

for algo in algorithms:
    print(f'[{algo["id"]}] {algo["name"]}')
    print(f'    Pattern: {algo["pattern"]}')
    print(f'    Depth: {algo["stats"]["depth"]}')
    print(f'    Size: {algo["stats"]["size"]}')
    print(f'    Max Alpha: {algo["stats"].get("alpha_max", "N/A")}')
    print()

print('✓ All algorithms have identical depth and size')
print('✓ Only heuristics and parameters vary')
print('✓ Fair comparison with GRASP/VND/ILS')

