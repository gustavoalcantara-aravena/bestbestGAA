#!/usr/bin/env python
"""
Utility to access latest canary or full experiment results easily.
"""

import json
from pathlib import Path
from typing import Tuple, Dict, List
import sys

def get_latest_run(run_type: str = "canary") -> Path:
    """Get the latest canary or full experiment run directory."""
    output_dir = Path("output")
    
    if run_type.lower() == "canary":
        pattern = "Canary_RUN_*"
    elif run_type.lower() == "full":
        pattern = "FULL_EXPERIMENT_RUN_*"
    else:
        raise ValueError(f"Invalid run_type: {run_type}. Use 'canary' or 'full'")
    
    runs = sorted(output_dir.glob(pattern))
    if not runs:
        raise FileNotFoundError(f"No {run_type} runs found in output/")
    
    return runs[-1]

def get_results(run_dir: Path) -> List[Dict]:
    """Load results JSON from a run directory."""
    if "Canary" in str(run_dir):
        results_file = run_dir / "canary_results.json"
    else:
        results_file = run_dir / "experiment_results.json"
    
    if not results_file.exists():
        raise FileNotFoundError(f"Results file not found: {results_file}")
    
    with open(results_file) as f:
        return json.load(f)

def get_algorithm_logs(run_dir: Path) -> Dict[int, Dict]:
    """Load all algorithm AST logs from a run directory."""
    logs_dir = run_dir / "logs"
    if not logs_dir.exists():
        raise FileNotFoundError(f"Logs directory not found: {logs_dir}")
    
    algorithms = {}
    for alg_file in sorted(logs_dir.glob("algorithm_*.json")):
        with open(alg_file) as f:
            alg_data = json.load(f)
            alg_id = alg_data["algorithm_id"]
            algorithms[alg_id] = alg_data
    
    return algorithms

def summarize_results(results: List[Dict]) -> Dict:
    """Generate summary statistics from results."""
    if not results:
        return {}
    
    vehicles = [r.get("total_vehicles", 0) for r in results]
    distances = [r.get("total_distance", 0) for r in results]
    feasible_count = sum(1 for r in results if r.get("feasible", False))
    
    return {
        "total_runs": len(results),
        "feasible_runs": feasible_count,
        "min_vehicles": min(vehicles) if vehicles else 0,
        "max_vehicles": max(vehicles) if vehicles else 0,
        "avg_vehicles": sum(vehicles) / len(vehicles) if vehicles else 0,
        "min_distance": min(distances) if distances else 0,
        "max_distance": max(distances) if distances else 0,
        "avg_distance": sum(distances) / len(distances) if distances else 0,
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Access latest experiment results")
    parser.add_argument("--type", choices=["canary", "full"], default="canary",
                      help="Run type to retrieve")
    parser.add_argument("--summary", action="store_true",
                      help="Show summary statistics")
    parser.add_argument("--algorithms", action="store_true",
                      help="List algorithm IDs and AST sizes")
    parser.add_argument("--dir", action="store_true",
                      help="Print the run directory path")
    
    args = parser.parse_args()
    
    try:
        run_dir = get_latest_run(args.type)
        print(f"Latest {args.type} run: {run_dir.name}")
        
        if args.dir:
            print(f"Directory: {run_dir}")
        
        if args.summary:
            results = get_results(run_dir)
            summary = summarize_results(results)
            print("\nSummary Statistics:")
            for key, value in summary.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.2f}")
                else:
                    print(f"  {key}: {value}")
        
        if args.algorithms:
            algorithms = get_algorithm_logs(run_dir)
            print(f"\nAlgorithms ({len(algorithms)} total):")
            for alg_id in sorted(algorithms.keys()):
                alg = algorithms[alg_id]
                const_size = len(str(alg.get("construction_ast", {})))
                ls_size = len(str(alg.get("ls_operator_ast", {})))
                print(f"  Algorithm {alg_id}: {const_size} bytes (construction), "
                      f"{ls_size} bytes (LS)")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
