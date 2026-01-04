#!/usr/bin/env python
"""
Generate GAP visualizations from VRAPTW experiment results
Requires: matplotlib, seaborn
"""

import sys
import os
import json
from pathlib import Path
import statistics

project_dir = Path(__file__).parent
os.chdir(project_dir)

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print("ERROR: matplotlib and seaborn required")
    print("Install with: pip install matplotlib seaborn")
    sys.exit(1)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

def load_results(results_file):
    """Load JSON results"""
    with open(results_file) as f:
        return json.load(f)

def generate_gap_distribution(results, output_dir):
    """Generate GAP distribution visualization"""
    
    feasible = [r for r in results if r.get("feasible", False)]
    if not feasible:
        print("  No feasible results for GAP analysis")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Calculate baseline (best solution found)
    best_vehicles = min(r["vehicles"] for r in feasible)
    best_distance = min(r["distance"] for r in feasible)
    
    # Calculate GAP percentages
    gap_vehicles = [((r["vehicles"] - best_vehicles) / best_vehicles) * 100 for r in feasible]
    gap_distance = [((r["distance"] - best_distance) / best_distance) * 100 for r in feasible]
    
    # Subplot 1: Histograma GAP Vehículos
    axes[0, 0].hist(gap_vehicles, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0, 0].axvline(statistics.mean(gap_vehicles), color='red', linestyle='--', linewidth=2, label=f'Mean: {statistics.mean(gap_vehicles):.2f}%')
    axes[0, 0].set_title('GAP Distribution - Vehicles (%)')
    axes[0, 0].set_xlabel('GAP %')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: Histograma GAP Distancia
    axes[0, 1].hist(gap_distance, bins=20, edgecolor='black', alpha=0.7, color='coral')
    axes[0, 1].axvline(statistics.mean(gap_distance), color='red', linestyle='--', linewidth=2, label=f'Mean: {statistics.mean(gap_distance):.2f}%')
    axes[0, 1].set_title('GAP Distribution - Distance (%)')
    axes[0, 1].set_xlabel('GAP %')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Subplot 3: Boxplot GAP Vehículos
    axes[1, 0].boxplot(gap_vehicles, vert=False)
    axes[1, 0].set_title('GAP Box Plot - Vehicles')
    axes[1, 0].set_xlabel('GAP %')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Subplot 4: Boxplot GAP Distancia
    axes[1, 1].boxplot(gap_distance, vert=False)
    axes[1, 1].set_title('GAP Box Plot - Distance')
    axes[1, 1].set_xlabel('GAP %')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = output_dir / 'gap_distribution.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  [OK] Saved: {output_file}")
    plt.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate gap visualizations")
    parser.add_argument("--results-file", type=str, help="Path to results JSON file")
    parser.add_argument("--output-dir", type=str, help="Path to output directory")
    args = parser.parse_args()
    
    print("=" * 80)
    print("GENERATING GAP VISUALIZATIONS")
    print("=" * 80)
    print()
    
    if args.results_file and args.output_dir:
        results_file = Path(args.results_file)
        if results_file.exists():
            results = load_results(results_file)
            print(f"[*] Processing {len(results)} results...")
            generate_gap_distribution(results, args.output_dir)
            print("  [OK] Gap visualizations complete")
        else:
            print(f"ERROR: Results file not found: {results_file}")
    else:
        print("Usage: python generate_gap_visualizations_clean.py --results-file <path> --output-dir <path>")
    
    print()
