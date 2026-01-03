#!/usr/bin/env python
"""Convert best_known_solutions.json to datasets/bks.json format"""

import json
from pathlib import Path

# Load best_known_solutions.json
input_file = Path('best_known_solutions.json')
output_file = Path('datasets') / 'bks.json'

with open(input_file, 'r') as f:
    data = json.load(f)

# Convert to bks.json format
bks_dict = {}
for family_key, family_data in data['families'].items():
    for instance in family_data['instances']:
        # Key format: 'family/instance_id' (e.g., 'C1/C101', 'R1/R101')
        key = f'{family_key}/{instance["id"]}'
        bks_dict[key] = {
            'K': instance['k_bks'],
            'D': instance['d_bks']
        }

print(f'✓ Converted {len(bks_dict)} instances')
print(f'Sample keys: {list(bks_dict.keys())[:5]}')

# Verify some keys
for test_key in ['C1/C101', 'R1/R101', 'RC1/RC101']:
    if test_key in bks_dict:
        print(f'✓ {test_key}: {bks_dict[test_key]}')

# Save bks.json
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(bks_dict, f, indent=2)

print(f'\n✓ Created {output_file}')
