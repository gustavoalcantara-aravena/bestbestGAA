#!/usr/bin/env python
"""
Generate GAP visualizations from VRPTW results.
GAP = ((obtained_value - baseline) / baseline) * 100
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

# Standard color palette - Verde, Rojo, Azul, Turquesa, Naranja
COLORS_5 = ['#2ecc71', '#e74c3c', '#3498db', '#1abc9c', '#f39c12']

def load_results(results_file):
    """Load results from JSON"""
    with open(results_file) as f:
        return json.load(f)

def generate_gap_distribution(results, output_dir):
    """Generate GAP distribution histogram and stats"""
    feasible = [r for r in results if r.get("feasible", False)]
    if not feasible:
        print("  No feasible results")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find baseline (best solution)
    best_veh = min(r["vehicles"] for r in feasible)
    best_dist = min(r["distance"] for r in feasible)
    
    # Calculate GAP percentages
    gap_veh = [((r["vehicles"] - best_veh) / best_veh) * 100 for r in feasible]
    gap_dist = [((r["distance"] - best_dist) / best_dist) * 100 for r in feasible]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("GAP Distribution Analysis", fontsize=16, fontweight='bold')
    
    # Vehicles GAP histogram
    axes[0, 0].hist(gap_veh, bins=15, edgecolor='black', alpha=0.7, color=COLORS_5[0])
    axes[0, 0].axvline(np.mean(gap_veh), color=COLORS_5[1], linestyle='--', linewidth=2, label=f'Mean: {np.mean(gap_veh):.2f}%')
    axes[0, 0].set_title('GAP Distribution - Vehicles')
    axes[0, 0].set_xlabel('GAP %')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Distance GAP histogram
    axes[0, 1].hist(gap_dist, bins=15, edgecolor='black', alpha=0.7, color=COLORS_5[2])
    axes[0, 1].axvline(np.mean(gap_dist), color=COLORS_5[1], linestyle='--', linewidth=2, label=f'Mean: {np.mean(gap_dist):.2f}%')
    axes[0, 1].set_title('GAP Distribution - Distance')
    axes[0, 1].set_xlabel('GAP %')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Vehicles GAP boxplot
    axes[1, 0].boxplot(gap_veh, vert=False, widths=0.5)
    axes[1, 0].set_title('GAP Boxplot - Vehicles')
    axes[1, 0].set_xlabel('GAP %')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Distance GAP boxplot
    axes[1, 1].boxplot(gap_dist, vert=False, widths=0.5)
    axes[1, 1].set_title('GAP Boxplot - Distance')
    axes[1, 1].set_xlabel('GAP %')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = output_dir / '21-gap_distribution.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  [OK] Saved: gap_distribution.png")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    
    print("=" * 80)
    print("GENERATING GAP VISUALIZATIONS")
    print("=" * 80)
    
    results_file = Path(args.results_file)
    if not results_file.exists():
        print(f"ERROR: {results_file} not found")
        sys.exit(1)
    
    results = load_results(results_file)
    print(f"Processing {len(results)} results...")
    generate_gap_distribution(results, args.output_dir)
    print("[DONE]\n")
