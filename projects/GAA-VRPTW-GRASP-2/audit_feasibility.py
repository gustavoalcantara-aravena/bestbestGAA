#!/usr/bin/env python
"""
Detailed Feasibility Audit - Inspect what's happening in solution construction

Analyzes:
1. How many customers are being inserted
2. Where time window violations occur
3. Capacity violations
4. Route quality metrics
"""

from src.core.loader import SolomonLoader
from src.operators.constructive import RandomizedInsertion, NearestNeighbor
from src.core.models import Solution, Route
import random

# Load instance
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')
print("=" * 80)
print("FEASIBILITY AUDIT - RandomizedInsertion Constructor")
print("=" * 80)
print(f"\nInstance: R101")
print(f"  - Total customers: {instance.n_customers}")
print(f"  - K (vehicles available): {instance.K_vehicles}")
print(f"  - Q (capacity per vehicle): {instance.Q_capacity}")

# Test 1: RandomizedInsertion
print("\n" + "=" * 80)
print("TEST 1: RandomizedInsertion with alpha=0.15")
print("=" * 80)
constructor = RandomizedInsertion(alpha=0.15, seed=42)
solution = constructor.apply(instance)

print(f"\nSolution generated:")
print(f"  - K (routes created): {len(solution.routes)}")
print(f"  - Num vehicles: {solution.num_vehicles}")
print(f"  - Total distance: {solution.total_distance:.2f}")
print(f"  - Feasible: {solution.feasible}")

# Analyze routes
total_customers_inserted = 0
for i, route in enumerate(solution.routes):
    print(f"\n  Route {i}:")
    print(f"    - Sequence length: {len(route.sequence)}")
    print(f"    - Sequence: {route.sequence}")
    print(f"    - Load: {route.load if hasattr(route, 'load') else 'N/A'}")
    print(f"    - Duration: {route.duration if hasattr(route, 'duration') else 'N/A'}")
    print(f"    - Feasible: {route.feasible if hasattr(route, 'feasible') else 'N/A'}")
    
    # Count actual customers (exclude depot 0 at start and end)
    actual_customers = len(route.sequence) - 2
    total_customers_inserted += actual_customers
    print(f"    - Customers in route: {actual_customers}")

print(f"\nTotal customers inserted: {total_customers_inserted} / {instance.n_customers}")
print(f"Insertion rate: {100 * total_customers_inserted / instance.n_customers:.1f}%")

# Test 2: NearestNeighbor (simpler, usually better)
print("\n" + "=" * 80)
print("TEST 2: NearestNeighbor (baseline)")
print("=" * 80)
constructor_nn = NearestNeighbor()
solution_nn = constructor_nn.apply(instance)

print(f"\nSolution generated:")
print(f"  - K (routes created): {len(solution_nn.routes)}")
print(f"  - Num vehicles: {solution_nn.num_vehicles}")
print(f"  - Total distance: {solution_nn.total_distance:.2f}")
print(f"  - Feasible: {solution_nn.feasible}")

total_customers_nn = 0
for i, route in enumerate(solution_nn.routes):
    actual_customers = len(route.sequence) - 2
    total_customers_nn += actual_customers
    
print(f"Total customers inserted: {total_customers_nn} / {instance.n_customers}")
print(f"Insertion rate: {100 * total_customers_nn / instance.n_customers:.1f}%")

# Test 3: Check what happened to missing customers
print("\n" + "=" * 80)
print("TEST 3: Identify missing customers (not inserted)")
print("=" * 80)

inserted_customers = set()
for route in solution.routes:
    # route.sequence is [0, c1, c2, ..., cn, 0]
    for customer_id in route.sequence[1:-1]:  # Skip depot at start and end
        inserted_customers.add(customer_id)

missing_customers = set(range(1, instance.n_customers + 1)) - inserted_customers
print(f"\nMissing customers from RandomizedInsertion: {len(missing_customers)}")
if len(missing_customers) <= 20:
    print(f"Missing IDs: {sorted(missing_customers)}")
else:
    print(f"First 20 missing: {sorted(list(missing_customers))[:20]}")

# Check for duplicates
print("\n" + "=" * 80)
print("TEST 4: Check for duplicate customer insertions")
print("=" * 80)
all_insertions = []
for route in solution.routes:
    for customer_id in route.sequence[1:-1]:
        all_insertions.append(customer_id)

duplicates = [c for c in all_insertions if all_insertions.count(c) > 1]
if duplicates:
    unique_duplicates = set(duplicates)
    print(f"Found {len(unique_duplicates)} customers inserted multiple times!")
    print(f"Duplicates: {sorted(unique_duplicates)}")
else:
    print("No duplicates found - good!")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"RandomizedInsertion: K={solution.num_vehicles}, D={solution.total_distance:.2f}, Feasible={solution.feasible}")
print(f"  - Customers inserted: {total_customers_inserted}/{instance.n_customers}")
print(f"  - Missing: {len(missing_customers)}")
print(f"\nNearestNeighbor: K={solution_nn.num_vehicles}, D={solution_nn.total_distance:.2f}, Feasible={solution_nn.feasible}")
print(f"  - Customers inserted: {total_customers_nn}/{instance.n_customers}")
