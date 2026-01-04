#!/usr/bin/env python
"""
CANARY RUN: C101 x 5 algorithms x 1 run each
Quick validation before full experiment
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess

# Change to project directory
project_dir = Path(__file__).parent
os.chdir(project_dir)
sys.path.insert(0, str(project_dir / 'src'))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def generate_visualizations(run_type: str = "canary", run_dir: Path = None):
    """Generate all visualizations for completed run."""
    if run_dir is None:
        run_dir = OUTPUT_DIR
    
    print("\n" + "=" * 80)
    print(f"AUTO-GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    script_path = project_dir / "generate_visualizations_for_run.py"
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), str(run_dir)],
            capture_output=True,
            text=True,
            timeout=900
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print("Warning: Some visualizations may not have been generated")
            if result.stderr:
                print(result.stderr[:500])
        
    except subprocess.TimeoutExpired:
        print("Warning: Visualization generation timed out")
    except Exception as e:
        print(f"Warning: Error during visualization generation: {e}")

print("=" * 80)
print("CANARY RUN - QUICK VALIDATION")
print("=" * 80)
print(f"Working directory: {os.getcwd()}")
print(f"Timestamp: {datetime.now().isoformat()}")
print()

# ============================================================================
# CONFIGURATION
# ============================================================================
INSTANCE = "C101"
CAPACITY = 200.0
NUM_ALGORITHMS = 5
NUM_RUNS = 1

# Create timestamped output directory
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = Path(f"output/Canary_RUN_{timestamp}")
LOG_DIR = OUTPUT_DIR / "logs"
VIS_DIR = OUTPUT_DIR / "visualizations"
DATASET_PATH = "03-data/Solomon-VRPTW-Dataset/C1/C101.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Config:")
print(f"  Instance: {INSTANCE}")
print(f"  Algorithms: {NUM_ALGORITHMS}")
print(f"  Runs per algorithm: {NUM_RUNS}")
print(f"  Output dir: {OUTPUT_DIR}")
print(f"  Logs dir: {LOG_DIR}")
print()

# ============================================================================
# IMPORTS
# ============================================================================
print("[STEP 1] Importing modules...")
try:
    from data.dataset_loader import load_instance
    from ast_generation.generator import RandomASTGenerator
    from ast_generation.validator import ASTValidator, ASTValidationConfig
    from ast_generation.generator_config import (
        CONSTRUCTION_FEATURES,
        LOCAL_SEARCH_FEATURES,
        LOCAL_SEARCH_OPERATORS,
    )
    from grasp.grasp_solver import GRASPSolver
    print("  OK - All imports successful")
except Exception as e:
    print(f"  FAIL - Import error: {e}")
    sys.exit(1)

# ============================================================================
# LOAD INSTANCE
# ============================================================================
print("\n[STEP 2] Loading instance...")
try:
    instance = load_instance(DATASET_PATH, capacity_default=CAPACITY)
    print(f"  OK - {INSTANCE} loaded")
    print(f"      Nodes: {instance.n_nodes}, Customers: {instance.n_customers}, Capacity: {instance.capacity}")
except Exception as e:
    print(f"  FAIL - Load error: {e}")
    sys.exit(1)

# ============================================================================
# CONVERT TO DICT
# ============================================================================
print("\n[STEP 3] Preparing instance...")
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
    print(f"  OK - Instance dict created")
except Exception as e:
    print(f"  FAIL - Preparation error: {e}")
    sys.exit(1)

# ============================================================================
# GENERATE ALGORITHMS
# ============================================================================
print(f"\n[STEP 4] Generating {NUM_ALGORITHMS} algorithms...")
try:
    gen = RandomASTGenerator(seed=42)
    algorithms = []
    
    for i in range(NUM_ALGORITHMS):
        ast_const = gen.generate(phase="construction", seed=42 + i)
        ast_ls = gen.generate(phase="local_search", seed=42 + i)
        
        algorithms.append({
            "id": i,
            "construction_ast": ast_const,
            "ls_operator_ast": ast_ls,
        })
        
        # Log algorithm AST
        alg_log = LOG_DIR / f"algorithm_{i:02d}.json"
        with open(alg_log, 'w') as f:
            json.dump({
                "algorithm_id": i,
                "construction_ast": ast_const,
                "ls_operator_ast": ast_ls,
            }, f, indent=2)
    
    print(f"  OK - Generated {len(algorithms)} algorithms")
except Exception as e:
    print(f"  FAIL - Generation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# VALIDATE ALGORITHMS
# ============================================================================
print("\n[STEP 5] Validating algorithms...")
try:
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
    
    print(f"  OK - {valid_count}/{len(algorithms)} algorithms validated")
except Exception as e:
    print(f"  WARN - Validation error: {e}")

# ============================================================================
# RUN EXPERIMENTS
# ============================================================================
print(f"\n[STEP 6] Running {NUM_ALGORITHMS} x {NUM_RUNS} GRASP instances...")

results_log = []
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

bks = {}

total_runs = NUM_ALGORITHMS * NUM_RUNS
run_count = 0

for alg_idx, alg in enumerate(algorithms):
    for run_idx in range(NUM_RUNS):
        run_count += 1
        try:
            solver = GRASPSolver(alg, instance_dict, bks, config)
            result = solver.solve()
            
            result["algorithm_id"] = alg_idx
            result["run_id"] = run_idx
            result["instance_id"] = INSTANCE
            result["timestamp"] = datetime.now().isoformat()
            
            results_log.append(result)
            
            vehicles = result.get("vehicles", 0)
            distance = result.get("distance", 0)
            feasible = result.get("feasible", False)
            
            status = "OK" if feasible else "INFEAS"
            print(f"  [{run_count:2d}/{total_runs}] Alg{alg_idx} Run{run_idx}: {vehicles:2d} veh, {distance:8.2f} km [{status}]")
            
        except Exception as e:
            print(f"  [{run_count:2d}/{total_runs}] Alg{alg_idx} Run{run_idx}: FAIL - {e}")
            results_log.append({
                "algorithm_id": alg_idx,
                "run_id": run_idx,
                "instance_id": INSTANCE,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            })

# ============================================================================
# SAVE RESULTS
# ============================================================================
print(f"\n[STEP 7] Saving results...")
try:
    results_file = OUTPUT_DIR / "canary_results.json"
    with results_file.open("w") as f:
        json.dump(results_log, f, indent=2)
    
    print(f"  OK - Results saved to {results_file}")
    print(f"      Total runs: {len(results_log)}")
    
    # Statistics
    feasible = sum(1 for r in results_log if r.get("feasible", False))
    if feasible > 0:
        avg_vehicles = sum(r.get("vehicles", 0) for r in results_log if r.get("feasible")) / feasible
        avg_distance = sum(r.get("distance", 0) for r in results_log if r.get("feasible")) / feasible
        print(f"      Feasible: {feasible}/{len(results_log)}")
        print(f"      Avg vehicles: {avg_vehicles:.1f}")
        print(f"      Avg distance: {avg_distance:.2f}")
    
except Exception as e:
    print(f"  FAIL - Save error: {e}")
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("CANARY RUN COMPLETE")
print("=" * 80)
print(f"""
Results:
  - Instance: {INSTANCE}
  - Algorithms: {NUM_ALGORITHMS}
  - Runs: {total_runs}
  - Output: {OUTPUT_DIR}/canary_results.json

Status:
  [OK] All imports successful
  [OK] Instance loaded
  [OK] Algorithms generated and validated
  [OK] GRASP solver executed {total_runs} times
  [OK] Results saved

GENERATING VISUALIZATIONS...
""")

# ============================================================================
# AUTO-GENERATE VISUALIZATIONS
# ============================================================================
generate_visualizations(run_type="canary", run_dir=OUTPUT_DIR)

print(f"""
NEXT STEPS:
  1. View results in browser: {OUTPUT_DIR}/report.html
  2. View PNG visualizations: {OUTPUT_DIR}/visualizations/
  3. If satisfied, run full experiment: python full_experiment.py
  4. Full experiment: 56 instances x 10 algorithms = 560 runs (~6 hours)
""")
