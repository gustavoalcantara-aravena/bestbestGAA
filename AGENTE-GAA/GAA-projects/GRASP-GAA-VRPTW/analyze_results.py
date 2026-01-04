#!/usr/bin/env python
"""
Analyze experiment results and generate statistics
"""

import sys
import os
import json
from pathlib import Path
from statistics import mean, stdev

project_dir = Path(__file__).parent
os.chdir(project_dir)

def analyze_results(results_file):
    """Load and analyze JSON results"""
    
    with open(results_file) as f:
        results = json.load(f)
    
    print("=" * 80)
    print(f"ANALYSIS: {results_file}")
    print("=" * 80)
    print()
    
    # Separate feasible and infeasible
    feasible = [r for r in results if r.get("feasible", False)]
    infeasible = [r for r in results if not r.get("feasible", True)]
    errors = [r for r in results if "error" in r]
    
    print(f"Summary:")
    print(f"  Total runs: {len(results)}")
    print(f"  Feasible: {len(feasible)} ({100*len(feasible)/len(results):.1f}%)")
    print(f"  Infeasible: {len(infeasible)}")
    print(f"  Errors: {len(errors)}")
    print()
    
    if not feasible:
        print("No feasible solutions found!")
        return
    
    # Vehicles statistics
    vehicles = [r.get("vehicles", 0) for r in feasible]
    print(f"Vehicles:")
    print(f"  Mean: {mean(vehicles):.1f}")
    if len(vehicles) > 1:
        print(f"  StDev: {stdev(vehicles):.2f}")
    print(f"  Min: {min(vehicles)}")
    print(f"  Max: {max(vehicles)}")
    print()
    
    # Distance statistics
    distances = [r.get("distance", 0) for r in feasible]
    print(f"Distance (km):")
    print(f"  Mean: {mean(distances):.2f}")
    if len(distances) > 1:
        print(f"  StDev: {stdev(distances):.2f}")
    print(f"  Min: {min(distances):.2f}")
    print(f"  Max: {max(distances):.2f}")
    print()
    
    # Group by instance
    by_instance = {}
    for r in feasible:
        inst = r.get("instance_id")
        if inst not in by_instance:
            by_instance[inst] = []
        by_instance[inst].append(r)
    
    if len(by_instance) > 1:
        print(f"Results by instance:")
        for inst in sorted(by_instance.keys()):
            runs = by_instance[inst]
            avg_vehicles = mean(r.get("vehicles", 0) for r in runs)
            avg_distance = mean(r.get("distance", 0) for r in runs)
            print(f"  {inst:8s}: {len(runs):3d} runs, {avg_vehicles:5.1f} veh, {avg_distance:8.2f} km")
        print()
    
    # Best solution
    best = min(feasible, key=lambda r: (r.get("vehicles", 0), r.get("distance", 0)))
    print(f"Best solution:")
    print(f"  Instance: {best.get('instance_id')}")
    print(f"  Algorithm: {best.get('algorithm_id')}")
    print(f"  Vehicles: {best.get('vehicles')}")
    print(f"  Distance: {best.get('distance'):.2f} km")
    print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze experiment results")
    parser.add_argument("--results-file", type=str, help="Path to results JSON file")
    args = parser.parse_args()
    
    if args.results_file:
        results_file = Path(args.results_file)
        if results_file.exists():
            analyze_results(results_file)
        else:
            print(f"File not found: {results_file}")
    else:
        # Default behavior: analyze canary run
        canary_file = Path("output/canary_run/canary_results.json")
        if canary_file.exists():
            analyze_results(canary_file)
            print()
        
        # Analyze full experiment (if exists)
        full_file = Path("output/full_experiment/experiment_results.json")
        if full_file.exists():
            analyze_results(full_file)
