#!/usr/bin/env python
"""Test RandomizedInsertion directly"""

from src.core.loader import SolomonLoader
from src.operators.constructive import RandomizedInsertion

# Load instance
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')
print(f"Instance R101 loaded: {len(instance.customers)} customers")
print(f"Instance attributes: {dir(instance)}")

# Try constructor
print("\n" + "=" * 80)
print("Testing RandomizedInsertion constructor")
print("=" * 80)
constructor = RandomizedInsertion(alpha=0.15, seed=42)
print(f"Constructor created: {constructor}")

try:
    solution = constructor.apply(instance)
    print(f"Solution generated successfully")
    print(f"  - Routes: {len(solution.routes)}")
    print(f"  - Vehicles: {solution.num_vehicles}")
    print(f"  - Distance: {solution.total_distance}")
    print(f"  - Feasible: {solution.feasible}")
    
    if len(solution.routes) > 0:
        for i, route in enumerate(solution.routes):
            print(f"  Route {i}: sequence={route.sequence}, distance={route.distance}")
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
