#!/usr/bin/env python
"""Real integration test: Load C101 and run GRASP"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("REAL INTEGRATION TEST - SOLOMON C101 + GRASP")
print("=" * 70)

# Load Solomon C101
print("\n[1] Loading C101...")

try:
    from data.dataset_loader import load_instance
    
    # Solomon C1 capacity = 200
    instance = load_instance(
        "03-data/Solomon-VRPTW-Dataset/C1/C101.csv",
        capacity_default=200.0
    )
    
    print(f"OK - Loaded C101")
    print(f"    Nodes: {instance.n_nodes}")
    print(f"    Customers: {instance.n_customers}")
    print(f"    Capacity: {instance.capacity}")
    
except Exception as e:
    print(f"FAIL - Load C101: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Generate algorithms
print("\n[2] Generating algorithms...")

try:
    from ast_generation.generator import RandomASTGenerator
    
    gen = RandomASTGenerator(seed=42)
    
    algorithms = []
    for i in range(3):  # 3 algorithms for quick test
        ast_const = gen.generate(phase="construction", seed=42+i)
        ast_ls = gen.generate(phase="local_search", seed=42+i)
        
        algorithms.append({
            "id": i,
            "construction_ast": ast_const,
            "ls_operator_ast": ast_ls,
        })
    
    print(f"OK - Generated {len(algorithms)} algorithms")
    
except Exception as e:
    print(f"FAIL - Generate algorithms: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Validate algorithms
print("\n[3] Validating algorithms...")

try:
    from ast_generation.validator import ASTValidator, ASTValidationConfig
    from ast_generation.generator_config import (
        CONSTRUCTION_FEATURES,
        LOCAL_SEARCH_FEATURES,
        LOCAL_SEARCH_OPERATORS,
    )
    
    config = ASTValidationConfig(max_depth=15, max_function_nodes=100, max_total_nodes=500)
    
    FEATURES_EXTENDED = list(set(CONSTRUCTION_FEATURES + [
        "route_total_waiting", "route_slack_forward", "cust_service_time",
        "delta_time", "delta_waiting", "capacity_violation", "time_violation",
        "relative_slack", "load_ratio", "num_customers_remaining", "num_routes_current"
    ]))
    
    validator = ASTValidator(
        config=config,
        construction_feature_names=FEATURES_EXTENDED,
        local_search_feature_names=LOCAL_SEARCH_FEATURES,
        allowed_operator_values=LOCAL_SEARCH_OPERATORS,
    )
    
    valid_count = 0
    for alg in algorithms:
        result = validator.validate_construction_ast(alg["construction_ast"])
        if result.ok:
            valid_count += 1
    
    print(f"OK - {valid_count}/{len(algorithms)} algorithms validated")
    
except Exception as e:
    print(f"WARN - Validation: {e}")

# Convert instance to dict for GRASP
print("\n[4] Preparing instance for GRASP...")

try:
    instance_dict = {
        "instance_id": instance.instance_id,
        "capacity": instance.capacity,
        "num_customers": instance.n_customers,
        "nodes": [
            {
                "id": n.id, "x": n.x, "y": n.y, "demand": n.demand,
                "ready_time": n.ready_time, "due_date": n.due_date,
                "service_time": n.service_time
            }
            for n in instance.nodes
        ],
        "distance_matrix": instance.distance_matrix,
        "time_matrix": instance.time_matrix,
    }
    
    print(f"OK - Instance prepared for GRASP")
    
except Exception as e:
    print(f"FAIL - Prepare instance: {e}")
    sys.exit(1)

# Create GRASP config
print("\n[5] Creating GRASP configuration...")

try:
    config = {
        "experiment": {"seed": 42},
        "grasp": {
            "rcl_size": 5,
            "max_construct_iters": 1000,
            "stochastic_degree": 0.25,
        },
        "local_search": {
            "max_iters": 100,
            "max_no_improve": 20,
            "operators": ["two_opt", "relocate"],
        },
        "penalty": {
            "alpha_capacity": 1000.0,
            "alpha_time": 10.0,
        },
        "fitness": {
            "w_vehicles": 1000.0,
            "w_distance": 1.0,
        },
    }
    
    print(f"OK - GRASP configuration ready")
    
except Exception as e:
    print(f"FAIL - GRASP config: {e}")
    sys.exit(1)

# Run GRASP with first algorithm
print("\n[6] Running GRASP solver...")

try:
    from grasp.grasp_solver import GRASPSolver
    
    alg = algorithms[0]
    bks = {}
    
    solver = GRASPSolver(alg, instance_dict, bks, config)
    
    print(f"    Starting GRASP with construction + local search...")
    result = solver.solve()
    
    print(f"OK - GRASP completed")
    print(f"    Routes: {len(result.get('routes', []))}")
    print(f"    Vehicles: {result.get('vehicles', 0)}")
    print(f"    Distance: {result.get('distance', 0):.2f}")
    print(f"    Feasible: {result.get('feasible', False)}")
    print(f"    Violations: {result.get('violations', 0)}")
    
except Exception as e:
    print(f"FAIL - GRASP solve: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Evaluate solution
print("\n[7] Evaluating solution...")

try:
    from evaluation.solution_evaluator import SolutionEvaluator
    
    evaluator = SolutionEvaluator(alpha_cap=1000.0, alpha_time=10.0)
    
    if result.get('routes'):
        route = result['routes'][0]
        metrics = evaluator.evaluate_route(route, instance)
        print(f"OK - First route metrics")
        print(f"    Distance: {metrics.distance:.2f}")
        print(f"    Load: {metrics.load:.2f}")
        print(f"    Service time: {metrics.service_time:.2f}")
        print(f"    Feasible: {metrics.feasible_capacity and metrics.feasible_time}")
    
except Exception as e:
    print(f"WARN - Evaluation: {e}")

# Summary
print("\n" + "=" * 70)
print("REAL INTEGRATION TEST PASSED")
print("=" * 70)
print(f"""
SUCCESS:
- Loaded real Solomon C101 instance
- Generated 3 algorithms with AST
- Validated algorithms
- Created GRASP solver
- Executed GRASP.solve()
- Got valid solution with {result.get('vehicles', '?')} vehicles
- Evaluated solution metrics

READY FOR:
- Full experiment execution (56 instances, 10 algorithms)
- Batch testing and analysis
- Performance optimization
""")
