#!/usr/bin/env python
"""
Generate algorithm comparison visualizations from VRPTW results.
"""

import sys
import os
import json
import argparse
from pathlib import Path

os.chdir(Path(__file__).parent)

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
except ImportError:
    print("ERROR: matplotlib and seaborn required")
    sys.exit(1)

sns.set_style("whitegrid")

def load_results(results_file):
    """Load results from JSON"""
    with open(results_file) as f:
        return json.load(f)

def generate_algorithm_performance(results, output_dir):
    """Generate algorithm performance heatmap and ranking"""
    feasible = [r for r in results if r.get("feasible", False)]
    if not feasible:
        print("  No feasible results")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Algorithm Performance Analysis", fontsize=16, fontweight='bold')
    
    # Extract algorithm IDs and vehicles/distances
    algorithms = list(set(r.get("algorithm_id", 0) for r in feasible))
    algorithms.sort()
    
    vehicles_by_alg = {alg: [] for alg in algorithms}
    distances_by_alg = {alg: [] for alg in algorithms}
    
    for r in feasible:
        alg_id = r.get("algorithm_id", 0)
        vehicles_by_alg[alg_id].append(r.get("vehicles", 0))
        distances_by_alg[alg_id].append(r.get("distance", 0))
    
    # Subplot 1: Vehicles by Algorithm (Boxplot)
    veh_data = [vehicles_by_alg[alg] for alg in algorithms]
    axes[0, 0].boxplot(veh_data, labels=[f'Alg{alg}' for alg in algorithms])
    axes[0, 0].set_title('Vehicle Performance by Algorithm')
    axes[0, 0].set_ylabel('Number of Vehicles')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: Distance by Algorithm (Boxplot)
    dist_data = [distances_by_alg[alg] for alg in algorithms]
    axes[0, 1].boxplot(dist_data, labels=[f'Alg{alg}' for alg in algorithms])
    axes[0, 1].set_title('Distance Performance by Algorithm')
    axes[0, 1].set_ylabel('Distance (km)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Subplot 3: Average Vehicles Ranking
    avg_vehicles = [np.mean(vehicles_by_alg[alg]) for alg in algorithms]
    sorted_indices = np.argsort(avg_vehicles)
    axes[1, 0].barh([f'Alg{algorithms[i]}' for i in sorted_indices], 
                     [avg_vehicles[i] for i in sorted_indices], color='steelblue')
    axes[1, 0].set_title('Average Vehicles Ranking (Lower is Better)')
    axes[1, 0].set_xlabel('Average Vehicles')
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # Subplot 4: Average Distance Ranking
    avg_distances = [np.mean(distances_by_alg[alg]) for alg in algorithms]
    sorted_indices = np.argsort(avg_distances)
    axes[1, 1].barh([f'Alg{algorithms[i]}' for i in sorted_indices], 
                     [avg_distances[i] for i in sorted_indices], color='coral')
    axes[1, 1].set_title('Average Distance Ranking (Lower is Better)')
    axes[1, 1].set_xlabel('Average Distance (km)')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_file = output_dir / 'algorithm_performance.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  [OK] Saved: algorithm_performance.png")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    
    print("=" * 80)
    print("GENERATING ALGORITHM COMPARISON VISUALIZATIONS")
    print("=" * 80)
    
    results_file = Path(args.results_file)
    if not results_file.exists():
        print(f"ERROR: {results_file} not found")
        sys.exit(1)
    
    results = load_results(results_file)
    print(f"Processing {len(results)} results...")
    generate_algorithm_performance(results, args.output_dir)
    print("[DONE]\n")
