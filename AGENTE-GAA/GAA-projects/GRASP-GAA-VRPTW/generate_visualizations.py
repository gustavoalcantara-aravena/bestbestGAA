#!/usr/bin/env python
"""
Generate visualizations from GRASP-GAA-VRPTW experiment results
Requires: matplotlib, seaborn
"""

import sys
import os
import json
from pathlib import Path
from collections import defaultdict
import statistics

project_dir = Path(__file__).parent
os.chdir(project_dir)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    import seaborn as sns
except ImportError:
    print("ERROR: matplotlib and seaborn required")
    print("Install with: pip install matplotlib seaborn")
    sys.exit(1)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

# Standard color palette - Verde, Rojo, Azul, Turquesa, Naranja
COLORS_5 = ['#2ecc71', '#e74c3c', '#3498db', '#1abc9c', '#f39c12']

def load_results(results_file):
    """Load JSON results"""
    with open(results_file) as f:
        return json.load(f)

def extract_family(instance_id):
    """Extract family from instance ID (C101 -> C)"""
    import re
    match = re.match(r'([A-Z]+)', instance_id)
    return match.group(1) if match else instance_id

def generate_canary_visualizations(results_file, output_dir):
    """Generate visualizations for canary run results"""
    
    results = load_results(results_file)
    feasible = [r for r in results if r.get("feasible", False)]
    
    if not feasible:
        print("No feasible results to visualize")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    vehicles = [r["vehicles"] for r in feasible]
    distances = [r["distance"] for r in feasible]
    algorithms = [r["algorithm_id"] for r in feasible]
    
    # Create figure with subplots
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # 1. Vehicles by Algorithm
    ax1 = fig.add_subplot(gs[0, 0])
    unique_algs = sorted(set(algorithms))
    colors = [COLORS_5[i % len(COLORS_5)] for i in range(len(unique_algs))]
    alg_vehicles = defaultdict(list)
    for alg, veh in zip(algorithms, vehicles):
        alg_vehicles[alg].append(veh)
    
    algs = sorted(alg_vehicles.keys())
    alg_labels = [f"Alg{a}" for a in algs]
    alg_data = [alg_vehicles[a] for a in algs]
    
    bp1 = ax1.boxplot(alg_data, tick_labels=alg_labels, patch_artist=True)
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
    ax1.set_ylabel('Number of Vehicles')
    ax1.set_title('Vehicle Distribution by Algorithm')
    ax1.grid(True, alpha=0.3)
    
    # 2. Distance by Algorithm
    ax2 = fig.add_subplot(gs[0, 1])
    alg_distances = defaultdict(list)
    for alg, dist in zip(algorithms, distances):
        alg_distances[alg].append(dist)
    
    alg_data_dist = [alg_distances[a] for a in algs]
    bp2 = ax2.boxplot(alg_data_dist, tick_labels=alg_labels, patch_artist=True)
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
    ax2.set_ylabel('Distance (km)')
    ax2.set_title('Distance Distribution by Algorithm')
    ax2.grid(True, alpha=0.3)
    
    # 3. Vehicles histogram
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(vehicles, bins=5, color=COLORS_5[0], alpha=0.7, edgecolor='black')
    ax3.axvline(statistics.mean(vehicles), color=COLORS_5[1], linestyle='--', linewidth=2, label=f'Mean: {statistics.mean(vehicles):.1f}')
    ax3.set_xlabel('Number of Vehicles')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Vehicles Distribution')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Distance histogram
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(distances, bins=5, color=COLORS_5[2], alpha=0.7, edgecolor='black')
    ax4.axvline(statistics.mean(distances), color=COLORS_5[1], linestyle='--', linewidth=2, label=f'Mean: {statistics.mean(distances):.1f} km')
    ax4.set_xlabel('Distance (km)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Distance Distribution')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Canary Run Results - C101 Instance', fontsize=16, fontweight='bold')
    
    output_file = output_dir / '20-canary_visualizations.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()

def generate_full_experiment_visualizations(results_file, output_dir):
    """Generate comprehensive visualizations for full experiment"""
    
    results = load_results(results_file)
    feasible = [r for r in results if r.get("feasible", False)]
    
    if not feasible:
        print("No feasible results to visualize")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract and organize data
    by_family = defaultdict(list)
    by_instance = defaultdict(list)
    by_algorithm = defaultdict(list)
    
    for r in feasible:
        inst_id = r["instance_id"]
        family = extract_family(inst_id)
        
        by_family[family].append(r)
        by_instance[inst_id].append(r)
        by_algorithm[r["algorithm_id"]].append(r)
    
    # ========================================================================
    # Figure 1: By Family
    # ========================================================================
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    families = sorted(by_family.keys())
    family_colors = plt.cm.Set2(range(len(families)))
    
    # 1.1 Vehicles by family
    ax1 = fig.add_subplot(gs[0, 0])
    family_vehicles = {f: [r["vehicles"] for r in by_family[f]] for f in families}
    family_labels = families
    family_data = [family_vehicles[f] for f in families]
    
    bp1 = ax1.boxplot(family_data, tick_labels=family_labels, patch_artist=True)
    for patch, color in zip(bp1['boxes'], family_colors):
        patch.set_facecolor(color)
    ax1.set_ylabel('Number of Vehicles')
    ax1.set_title('Vehicle Distribution by Solomon Family')
    ax1.grid(True, alpha=0.3)
    
    # 1.2 Distance by family
    ax2 = fig.add_subplot(gs[0, 1])
    family_distances = {f: [r["distance"] for r in by_family[f]] for f in families}
    family_data_dist = [family_distances[f] for f in families]
    
    bp2 = ax2.boxplot(family_data_dist, tick_labels=family_labels, patch_artist=True)
    for patch, color in zip(bp2['boxes'], family_colors):
        patch.set_facecolor(color)
    ax2.set_ylabel('Distance (km)')
    ax2.set_title('Distance Distribution by Solomon Family')
    ax2.grid(True, alpha=0.3)
    
    # 1.3 Average vehicles per family
    ax3 = fig.add_subplot(gs[1, 0])
    family_avg_veh = {f: statistics.mean([r["vehicles"] for r in by_family[f]]) for f in families}
    ax3.bar(families, [family_avg_veh[f] for f in families], color=family_colors)
    ax3.set_ylabel('Average Vehicles')
    ax3.set_title('Average Vehicles per Family')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 1.4 Average distance per family
    ax4 = fig.add_subplot(gs[1, 1])
    family_avg_dist = {f: statistics.mean([r["distance"] for r in by_family[f]]) for f in families}
    ax4.bar(families, [family_avg_dist[f] for f in families], color=family_colors)
    ax4.set_ylabel('Average Distance (km)')
    ax4.set_title('Average Distance per Family')
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Full Experiment Results - By Solomon Family', fontsize=16, fontweight='bold')
    
    output_file = output_dir / 'by_family.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()
    
    # ========================================================================
    # Figure 2: By Instance (sample)
    # ========================================================================
    fig = plt.figure(figsize=(16, 10))
    
    instances = sorted(by_instance.keys())[:20]  # First 20 instances
    
    ax1 = fig.add_subplot(2, 1, 1)
    instance_avg_veh = {i: statistics.mean([r["vehicles"] for r in by_instance[i]]) for i in instances}
    colors_inst = plt.cm.tab20(range(len(instances)))
    ax1.bar(instances, [instance_avg_veh[i] for i in instances], color=colors_inst)
    ax1.set_ylabel('Average Vehicles')
    ax1.set_title('Average Vehicles per Instance (First 20)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2 = fig.add_subplot(2, 1, 2)
    instance_avg_dist = {i: statistics.mean([r["distance"] for r in by_instance[i]]) for i in instances}
    ax2.bar(instances, [instance_avg_dist[i] for i in instances], color=colors_inst)
    ax2.set_ylabel('Average Distance (km)')
    ax2.set_title('Average Distance per Instance (First 20)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.suptitle('Full Experiment Results - By Instance (Sample)', fontsize=16, fontweight='bold', y=1.00)
    
    output_file = output_dir / 'by_instance.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()
    
    # ========================================================================
    # Figure 3: Algorithm Comparison
    # ========================================================================
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    algorithms = sorted(by_algorithm.keys())
    algo_colors = plt.cm.tab10(range(len(algorithms)))
    
    # 3.1 Vehicles by algorithm
    ax1 = fig.add_subplot(gs[0, 0])
    algo_vehicles = {a: [r["vehicles"] for r in by_algorithm[a]] for a in algorithms}
    algo_labels = [f"Alg{a}" for a in algorithms]
    algo_data = [algo_vehicles[a] for a in algorithms]
    
    bp1 = ax1.boxplot(algo_data, tick_labels=algo_labels, patch_artist=True)
    for patch, color in zip(bp1['boxes'], algo_colors):
        patch.set_facecolor(color)
    ax1.set_ylabel('Number of Vehicles')
    ax1.set_title('Vehicle Distribution by Algorithm')
    ax1.grid(True, alpha=0.3)
    
    # 3.2 Distance by algorithm
    ax2 = fig.add_subplot(gs[0, 1])
    algo_distances = {a: [r["distance"] for r in by_algorithm[a]] for a in algorithms}
    algo_data_dist = [algo_distances[a] for a in algorithms]
    
    bp2 = ax2.boxplot(algo_data_dist, tick_labels=algo_labels, patch_artist=True)
    for patch, color in zip(bp2['boxes'], algo_colors):
        patch.set_facecolor(color)
    ax2.set_ylabel('Distance (km)')
    ax2.set_title('Distance Distribution by Algorithm')
    ax2.grid(True, alpha=0.3)
    
    # 3.3 Average vehicles per algorithm
    ax3 = fig.add_subplot(gs[1, 0])
    algo_avg_veh = {a: statistics.mean([r["vehicles"] for r in by_algorithm[a]]) for a in algorithms}
    ax3.bar(algo_labels, [algo_avg_veh[a] for a in algorithms], color=algo_colors)
    ax3.set_ylabel('Average Vehicles')
    ax3.set_title('Average Vehicles by Algorithm')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 3.4 Average distance per algorithm
    ax4 = fig.add_subplot(gs[1, 1])
    algo_avg_dist = {a: statistics.mean([r["distance"] for r in by_algorithm[a]]) for a in algorithms}
    ax4.bar(algo_labels, [algo_avg_dist[a] for a in algorithms], color=algo_colors)
    ax4.set_ylabel('Average Distance (km)')
    ax4.set_title('Average Distance by Algorithm')
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Full Experiment Results - By Algorithm', fontsize=16, fontweight='bold')
    
    output_file = output_dir / 'by_algorithm.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()
    
    # ========================================================================
    # Figure 4: Summary Statistics
    # ========================================================================
    fig = plt.figure(figsize=(14, 8))
    
    all_vehicles = [r["vehicles"] for r in feasible]
    all_distances = [r["distance"] for r in feasible]
    
    # Create summary table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    summary_data = [
        ['Metric', 'Min', 'Mean', 'Max', 'StDev'],
        ['Vehicles', f"{min(all_vehicles)}", f"{statistics.mean(all_vehicles):.1f}", f"{max(all_vehicles)}", f"{statistics.stdev(all_vehicles):.2f}"],
        ['Distance (km)', f"{min(all_distances):.2f}", f"{statistics.mean(all_distances):.2f}", f"{max(all_distances):.2f}", f"{statistics.stdev(all_distances):.2f}"],
        ['', '', '', '', ''],
        ['Family', 'Instances', 'Avg Vehicles', 'Avg Distance', 'Total Runs'],
    ]
    
    for family in families:
        family_results = by_family[family]
        summary_data.append([
            family,
            f"{len(set(r['instance_id'] for r in family_results))}",
            f"{statistics.mean(r['vehicles'] for r in family_results):.1f}",
            f"{statistics.mean(r['distance'] for r in family_results):.2f}",
            f"{len(family_results)}"
        ])
    
    table = ax.table(cellText=summary_data, cellLoc='center', loc='center',
                     colWidths=[0.2, 0.15, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Color header rows
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(5):
        table[(4, i)].set_facecolor('#2196F3')
        table[(4, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Summary Statistics', fontsize=16, fontweight='bold', pad=20)
    
    output_file = output_dir / 'summary_statistics.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")
    plt.close()

if __name__ == "__main__":
    print("=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    print()
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate visualizations from results")
    parser.add_argument("--results-file", type=str, help="Path to results JSON file")
    parser.add_argument("--output-dir", type=str, help="Path to output visualizations directory")
    parser.add_argument("--type", type=str, choices=["canary", "full"], help="Type of results (canary or full)")
    args = parser.parse_args()
    
    try:
        if args.results_file and args.output_dir and args.type:
            # Generate based on provided paths
            results_file = Path(args.results_file)
            output_dir = args.output_dir
            
            if not results_file.exists():
                print(f"Results file not found: {results_file}")
            elif args.type == "canary":
                generate_canary_visualizations(results_file, output_dir)
            elif args.type == "full":
                generate_full_experiment_visualizations(results_file, output_dir)
    except Exception as e:
        import traceback
        traceback.print_exc()
    else:
        # Default behavior: analyze canary run
        # Canary run
        canary_file = Path("output/canary_run/canary_results.json")
        if canary_file.exists():
            print("[1] Generating canary run visualizations...")
            try:
                generate_canary_visualizations(canary_file, "output/canary_run/visualizations")
            except Exception as e:
                print(f"  Error: {e}")
            print()
        else:
            print("[1] Canary run results not found")
            print()
        
        # Full experiment
        full_file = Path("output/full_experiment/experiment_results.json")
        if full_file.exists():
            print("[2] Generating full experiment visualizations...")
            try:
                generate_full_experiment_visualizations(full_file, "output/full_experiment/visualizations")
            except Exception as e:
                print(f"  Error: {e}")
            print()
        else:
            print("[2] Full experiment results not found (run full_experiment.py first)")
            print()
    
    print("=" * 80)
    print("VISUALIZATIONS COMPLETE")
    print("=" * 80)
