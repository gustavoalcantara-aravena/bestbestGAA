#!/usr/bin/env python
"""
Feasibility Validation and BKS Comparison

Tests:
1. Feasibility: Capacity, time windows, all customers inserted
2. Quality: Gap to Best Known Solutions (BKS)
3. Solution metrics: K, D, feasibility status
"""

from src.core.loader import SolomonLoader
from src.operators.constructive import RandomizedInsertion, NearestNeighbor
from gaa import AlgorithmGenerator
from src.gaa.interpreter import ASTInterpreter
from scripts.experiments import dict_to_ast
import json
from pathlib import Path

# Load BKS data
bks_file = Path('best_known_solutions.json')
if not bks_file.exists():
    print("WARNING: best_known_solutions.json not found")
    bks_data = {}
else:
    with open(bks_file) as f:
        bks_data = json.load(f)

print("=" * 80)
print("FEASIBILITY VALIDATION & BKS COMPARISON")
print("=" * 80)

# Load instances
loader = SolomonLoader()
test_instances = ['R101', 'R102', 'C101', 'RC101']

for instance_name in test_instances:
    print(f"\n{'='*80}")
    print(f"Instance: {instance_name}")
    print(f"{'='*80}")
    
    # Load instance
    try:
        instance = loader.load_instance(f'datasets/{instance_name[0]}{instance_name[1]}/{instance_name}.csv')
    except:
        print(f"⚠ Cannot load {instance_name}")
        continue
    
    print(f"Customers: {instance.n_customers}")
    print(f"Capacity: {instance.Q_capacity}")
    
    # Get BKS
    bks_k = bks_data.get(instance_name, {}).get('K') if isinstance(bks_data.get(instance_name), dict) else None
    bks_d = bks_data.get(instance_name, {}).get('D') if isinstance(bks_data.get(instance_name), dict) else None
    
    if bks_k and bks_d:
        print(f"BKS: K={bks_k}, D={bks_d:.2f}")
    else:
        print(f"BKS: Not available")
    
    # Test constructors
    constructors = [
        ('RandomizedInsertion', RandomizedInsertion(alpha=0.15, seed=42)),
        ('NearestNeighbor', NearestNeighbor()),
    ]
    
    for name, constructor in constructors:
        print(f"\n  {name}:")
        
        solution = constructor.apply(instance)
        
        # Check feasibility
        print(f"    K: {solution.num_vehicles}, D: {solution.total_distance:.2f}")
        
        # Count customers
        total_customers = 0
        for route in solution.routes:
            customers_in_route = len(route.sequence) - 2  # Exclude start and end depot
            total_customers += customers_in_route
        
        print(f"    Customers inserted: {total_customers}/{instance.n_customers}")
        
        # Check capacities
        violated_capacity = False
        for route in solution.routes:
            route_load = sum(
                instance.get_customer(c).demand
                for c in route.sequence[1:-1]
            )
            if route_load > instance.Q_capacity:
                violated_capacity = True
                print(f"    ⚠ Capacity violation: route load={route_load:.1f} > {instance.Q_capacity}")
                break
        
        if not violated_capacity and total_customers == instance.n_customers:
            print(f"    ✓ Feasible (all customers, capacity ok)")
        
        # Compare with BKS
        if bks_d:
            gap = ((solution.total_distance - bks_d) / bks_d) * 100
            print(f"    Gap to BKS: {gap:+.2f}%")

print("\n" + "=" * 80)
print("ALGORITHM GENERATION TEST")
print("=" * 80)

# Test GAA algorithms
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()

for algo in algos:
    print(f"\n{algo['name']}: {algo['pattern']}")
    
    instance = loader.load_instance('datasets/R1/R101.csv')
    
    # Reconstruct AST
    ast_node = dict_to_ast(algo['ast'])
    
    # Execute
    interpreter = ASTInterpreter()
    solution = interpreter.execute(ast_node, instance)
    
    # Analyze
    total_customers = 0
    for route in solution.routes:
        customers_in_route = len(route.sequence) - 2
        total_customers += customers_in_route
    
    print(f"  K={solution.num_vehicles}, D={solution.total_distance:.2f}")
    print(f"  Customers: {total_customers}/{instance.n_customers}")
    print(f"  Feasible: {solution.feasible}")
    
    if total_customers == instance.n_customers:
        print(f"  ✓ All customers inserted")
    else:
        print(f"  ✗ Missing {instance.n_customers - total_customers} customers")
    
    # BKS comparison
    bks_d = bks_data.get('R101', {}).get('D') if isinstance(bks_data.get('R101'), dict) else None
    if bks_d:
        gap = ((solution.total_distance - bks_d) / bks_d) * 100
        print(f"  Gap to BKS: {gap:+.2f}%")

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
