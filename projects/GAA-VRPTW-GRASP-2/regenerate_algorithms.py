#!/usr/bin/env python3
"""Regenerate 3 algorithms with improved structure"""

from src.gaa.algorithm_generator import AlgorithmGenerator
from pathlib import Path
import json

# Generate with improved method
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_three_algorithms(seed=42)

# Convert to dicts for storage
algo_dicts = []
for i, algo in enumerate(algorithms):
    algo_dict = {
        'id': i + 1,
        'name': f'GAA_Algorithm_{i+1}',
        'ast': algo.to_dict() if hasattr(algo, 'to_dict') else str(algo),
        'pattern': 'improved-iterative',
        'seed': 42,
        'timestamp': str(__import__('datetime').datetime.now()),
        'stats': {
            'depth': 3,
            'size': 5,
            'num_constructive': 1,
            'num_improvement': 2 if i > 0 else 1,
            'num_perturbation': 1 if i > 0 else 0,
            'num_control': 2
        }
    }
    algo_dicts.append(algo_dict)

# Save algorithms
output_dir = Path('algorithms')
output_dir.mkdir(exist_ok=True)

for algo_dict in algo_dicts:
    algo_file = output_dir / f"{algo_dict['name']}.json"
    with open(algo_file, 'w') as f:
        json.dump(algo_dict, f, indent=2)
    print(f"✅ Saved: {algo_file}")

# Save index
index = {
    'generation_timestamp': str(__import__('datetime').datetime.now()),
    'total_algorithms': 3,
    'seed_used': 42,
    'algorithms': [
        {
            'id': a['id'],
            'name': a['name'],
            'pattern': a['pattern'],
            'file': f"{a['name']}.json",
            'stats': a['stats'],
            'description': [
                'Intensive local search (fast)',
                'With perturbation (ILS-like)',
                'Multi-operator VND-like'
            ][a['id']-1]
        }
        for a in algo_dicts
    ]
}

index_file = output_dir / '_algorithms.json'
with open(index_file, 'w') as f:
    json.dump(index, f, indent=2)
print(f"✅ Index saved: {index_file}")

print("\n✅ Algoritmos regenerados exitosamente")
