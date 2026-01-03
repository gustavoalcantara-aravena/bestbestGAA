"""
Visualization module for VRPTW experiment results.

Generates comprehensive plots and charts to analyze algorithm performance:
- Performance comparison by algorithm
- Distance distribution by family
- Time analysis
- Gap analysis (vs BKS)
- Heatmaps of results
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[WARNING] matplotlib/seaborn not available. Install with: pip install matplotlib seaborn")


class ResultVisualizer:
    """Generate visualizations from experiment results"""
    
    def __init__(self, results_csv_path: str, plots_output_dir: str):
        """
        Initialize visualizer.
        
        Args:
            results_csv_path: Path to raw_results.csv
            plots_output_dir: Directory to save plots
        """
        self.results_path = Path(results_csv_path)
        self.plots_dir = Path(plots_output_dir)
        self.plots_dir.mkdir(exist_ok=True, parents=True)
        
        self.data = self._load_results()
        
        if MATPLOTLIB_AVAILABLE:
            sns.set_style("whitegrid")
            plt.rcParams['figure.figsize'] = (12, 6)
            plt.rcParams['font.size'] = 10
    
    def _load_results(self) -> List[Dict]:
        """Load results from CSV"""
        results = []
        
        if not self.results_path.exists():
            print(f"[WARNING] Results file not found: {self.results_path}")
            return results
        
        with open(self.results_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key in ['k_final', 'd_final', 'k_bks', 'd_bks', 'time_sec']:
                    if key in row and row[key]:
                        try:
                            row[key] = float(row[key])
                        except (ValueError, TypeError):
                            pass
                
                results.append(row)
        
        print(f"[INFO] Loaded {len(results)} results from CSV")
        return results
    
    def generate_all(self):
        """Generate all visualizations (11 canonical types)"""
        if not MATPLOTLIB_AVAILABLE:
            print("[ERROR] Cannot generate plots without matplotlib/seaborn")
            return
        
        if not self.data:
            print("[WARNING] No data to visualize")
            return
        
        print(f"[INFO] Generating visualizations in {self.plots_dir}...")
        
        # CANONICAL PLOTS (11 types as per specification)
        self.plot_performance_comparison()              # 1
        self.plot_distance_by_algorithm()               # 2
        self.plot_distance_by_family()                  # 3
        self.plot_execution_time()                      # 4
        self.plot_gap_analysis()                        # 5
        self.plot_algorithms_boxplot()                  # 6
        self.plot_family_performance_heatmap()          # 7
        self.plot_k_vs_d_pareto()                       # 8
        self.plot_robustness_by_instance()              # 9
        self.plot_k_feasibility_analysis()              # 10
        self.plot_algorithm_comparison_radar()          # 11
        
        print(f"[INFO] Visualization complete! (11 canonical plots generated)")
    
    def plot_performance_comparison(self):
        """Bar chart: Average distance by algorithm"""
        if not self.data:
            return
        
        algo_distances = {}
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                if algo not in algo_distances:
                    algo_distances[algo] = []
                algo_distances[algo].append(distance)
            except (ValueError, TypeError):
                continue
        
        if not algo_distances:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(algo_distances.keys())
        avg_distances = [np.mean(algo_distances[a]) for a in algorithms]
        colors = ['#2ecc71', '#e74c3c', '#3498db'][:len(algorithms)]
        
        bars = ax.bar(algorithms, avg_distances, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Distance', fontsize=12, fontweight='bold')
        ax.set_title('Performance Comparison: Average Distance by Algorithm', 
                     fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "01_performance_comparison.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_distance_by_algorithm(self):
        """Line plot: Distance per instance by algorithm"""
        if not self.data:
            return
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Group by algorithm
        algo_data = {}
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            instance = row.get('instance_id', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                if algo not in algo_data:
                    algo_data[algo] = {'instances': [], 'distances': []}
                algo_data[algo]['instances'].append(instance)
                algo_data[algo]['distances'].append(distance)
            except (ValueError, TypeError):
                continue
        
        # Sort by instance ID
        colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
        markers = ['o', 's', '^', 'D', 'v', '<']
        
        for (algo, data), color, marker in zip(algo_data.items(), colors, markers):
            # Sort indices by instance
            indices = range(len(data['instances']))
            ax.plot(indices, data['distances'], marker=marker, label=algo, 
                   linewidth=2, markersize=6, color=color, alpha=0.8)
        
        ax.set_xlabel('Instance Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Distance', fontsize=12, fontweight='bold')
        ax.set_title('Distance per Instance by Algorithm', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "02_distance_by_instance.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_distance_by_family(self):
        """Bar chart: Average distance by family"""
        if not self.data:
            return
        
        family_distances = {}
        for row in self.data:
            family = row.get('family', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                if family not in family_distances:
                    family_distances[family] = []
                family_distances[family].append(distance)
            except (ValueError, TypeError):
                continue
        
        if not family_distances:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        families = sorted(family_distances.keys())
        avg_distances = [np.mean(family_distances[f]) for f in families]
        colors = plt.cm.viridis(np.linspace(0, 1, len(families)))
        
        bars = ax.bar(families, avg_distances, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Instance Family', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Distance', fontsize=12, fontweight='bold')
        ax.set_title('Performance by Instance Family', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "03_distance_by_family.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_execution_time(self):
        """Bar chart: Average execution time by algorithm"""
        if not self.data:
            return
        
        algo_times = {}
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                time_sec = float(row.get('time_sec', 0))
                if algo not in algo_times:
                    algo_times[algo] = []
                algo_times[algo].append(time_sec)
            except (ValueError, TypeError):
                continue
        
        if not algo_times:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(algo_times.keys())
        avg_times = [np.mean(algo_times[a]) for a in algorithms]
        colors = ['#2ecc71', '#e74c3c', '#3498db'][:len(algorithms)]
        
        bars = ax.bar(algorithms, avg_times, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}s',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "04_execution_time.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_gap_analysis(self):
        """Bar chart: Gap vs BKS by algorithm (only where K matches BKS)"""
        algo_gaps = {}
        count = {}
        
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                k_final = float(row.get('k_final', 0))
                k_bks = float(row.get('k_bks', 0))
                d_final = float(row.get('d_final', 0))
                d_bks = float(row.get('d_bks', 0))
                
                # Only count where K matches BKS
                if k_final == k_bks and d_bks > 0:
                    gap_percent = ((d_final - d_bks) / d_bks) * 100
                    if algo not in algo_gaps:
                        algo_gaps[algo] = []
                        count[algo] = 0
                    algo_gaps[algo].append(gap_percent)
                    count[algo] += 1
            except (ValueError, TypeError):
                continue
        
        if not algo_gaps:
            print("  [SKIP] Gap analysis: No instances with matching K and BKS")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(algo_gaps.keys())
        avg_gaps = [np.mean(algo_gaps[a]) for a in algorithms]
        colors = ['#2ecc71', '#e74c3c', '#3498db'][:len(algorithms)]
        
        bars = ax.bar(algorithms, avg_gaps, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels and counts
        for bar, algo in zip(bars, algorithms):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}%\n(n={count[algo]})',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='BKS')
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Gap vs BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Gap Analysis: Distance Gap vs Best Known Solution (When K=BKS)', 
                     fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "05_gap_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_algorithms_boxplot(self):
        """Boxplot: Distance distribution by algorithm"""
        if not self.data:
            return
        
        algo_distances = {}
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                if algo not in algo_distances:
                    algo_distances[algo] = []
                algo_distances[algo].append(distance)
            except (ValueError, TypeError):
                continue
        
        if not algo_distances:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = sorted(algo_distances.keys())
        data_to_plot = [algo_distances[a] for a in algorithms]
        
        bp = ax.boxplot(data_to_plot, labels=algorithms, patch_artist=True)
        
        colors = ['#2ecc71', '#e74c3c', '#3498db'][:len(algorithms)]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Distance', fontsize=12, fontweight='bold')
        ax.set_title('Distance Distribution by Algorithm (Boxplot)', 
                     fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "06_algorithms_boxplot.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_family_performance_heatmap(self):
        """Heatmap: Average distance by family and algorithm"""
        if not self.data:
            return
        
        # Build matrix: rows=families, cols=algorithms
        families = sorted(set(row.get('family', 'Unknown') for row in self.data))
        algorithms = sorted(set(row.get('algorithm', 'Unknown') for row in self.data))
        
        matrix = np.zeros((len(families), len(algorithms)))
        counts = np.zeros((len(families), len(algorithms)))
        
        for row in self.data:
            family = row.get('family', 'Unknown')
            algo = row.get('algorithm', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                f_idx = families.index(family)
                a_idx = algorithms.index(algo)
                matrix[f_idx, a_idx] += distance
                counts[f_idx, a_idx] += 1
            except (ValueError, TypeError, IndexError):
                continue
        
        # Compute averages
        with np.errstate(divide='ignore', invalid='ignore'):
            matrix = np.where(counts > 0, matrix / counts, 0)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto')
        
        ax.set_xticks(range(len(algorithms)))
        ax.set_yticks(range(len(families)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.set_yticklabels(families)
        
        # Add text annotations
        for i in range(len(families)):
            for j in range(len(algorithms)):
                if counts[i, j] > 0:
                    text = ax.text(j, i, f'{matrix[i, j]:.1f}',
                                 ha="center", va="center", color="black", fontsize=9)
        
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Instance Family', fontsize=12, fontweight='bold')
        ax.set_title('Performance Heatmap: Average Distance by Family and Algorithm', 
                     fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Average Distance', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.plots_dir / "07_family_algorithm_heatmap.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_k_vs_d_pareto(self):
        """Scatter plot: K vs D (multi-objective Pareto analysis)"""
        if not self.data:
            return
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        algorithms = sorted(set(row.get('algorithm', 'Unknown') for row in self.data))
        colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12'][:len(algorithms)]
        markers = ['o', 's', '^', 'D'][:len(algorithms)]
        
        for algo, color, marker in zip(algorithms, colors, markers):
            algo_data = [row for row in self.data if row.get('algorithm') == algo]
            
            k_values = []
            d_values = []
            for row in algo_data:
                try:
                    k = float(row.get('k_final', 0))
                    d = float(row.get('d_final', 0))
                    k_values.append(k)
                    d_values.append(d)
                except (ValueError, TypeError):
                    continue
            
            if k_values:
                ax.scatter(k_values, d_values, label=algo, color=color, marker=marker,
                          s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Number of Vehicles (K)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Distance (D)', fontsize=12, fontweight='bold')
        ax.set_title('Multi-Objective Analysis: K vs D (Pareto Front)', 
                     fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "08_k_vs_d_pareto.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_robustness_by_instance(self):
        """Boxplot: Distance distribution by instance and algorithm"""
        if not self.data:
            return
        
        # Get all instances
        instances = sorted(set(row.get('instance_id', 'Unknown') for row in self.data))
        
        # Only plot first 6 instances to avoid overcrowding
        instances_to_plot = instances[:min(6, len(instances))]
        
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        axes = axes.flatten()
        
        algorithms = sorted(set(row.get('algorithm', 'Unknown') for row in self.data))
        colors = ['#2ecc71', '#e74c3c', '#3498db'][:len(algorithms)]
        
        for idx, instance in enumerate(instances_to_plot):
            ax = axes[idx]
            instance_data = [row for row in self.data if row.get('instance_id') == instance]
            
            algo_distances = {}
            for row in instance_data:
                algo = row.get('algorithm', 'Unknown')
                try:
                    distance = float(row.get('d_final', 0))
                    if algo not in algo_distances:
                        algo_distances[algo] = []
                    algo_distances[algo].append(distance)
                except (ValueError, TypeError):
                    continue
            
            if algo_distances:
                algorithms_in_instance = sorted(algo_distances.keys())
                data_to_plot = [algo_distances[a] for a in algorithms_in_instance]
                
                bp = ax.boxplot(data_to_plot, labels=algorithms_in_instance, patch_artist=True)
                
                for patch, color in zip(bp['boxes'], colors[:len(algorithms_in_instance)]):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                ax.set_title(f'Instance: {instance}', fontweight='bold', fontsize=11)
                ax.set_ylabel('Distance', fontsize=10, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
        
        # Hide unused subplots
        for idx in range(len(instances_to_plot), len(axes)):
            axes[idx].axis('off')
        
        fig.suptitle('Robustness Analysis: Distance Distribution by Instance', 
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        output_path = self.plots_dir / "09_robustness_by_instance.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_k_feasibility_analysis(self):
        """Analysis: Feasibility rate (achieving K_BKS) by algorithm"""
        if not self.data:
            return
        
        algo_feasible = {}
        algo_total = {}
        
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                k_final = float(row.get('k_final', 0))
                k_bks = float(row.get('k_bks', 0))
                
                if algo not in algo_total:
                    algo_feasible[algo] = 0
                    algo_total[algo] = 0
                
                algo_total[algo] += 1
                if k_final == k_bks:
                    algo_feasible[algo] += 1
            except (ValueError, TypeError):
                continue
        
        if not algo_total:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        algorithms = sorted(algo_total.keys())
        feasibility_rates = [100 * algo_feasible[a] / algo_total[a] for a in algorithms]
        
        colors = ['#2ecc71' if rate == 100 else '#f39c12' if rate >= 50 else '#e74c3c' 
                 for rate in feasibility_rates]
        
        # Bar chart
        bars = ax1.bar(algorithms, feasibility_rates, color=colors, alpha=0.8, edgecolor='black')
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax1.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Feasibility Rate (%)', fontsize=12, fontweight='bold')
        ax1.set_title('K_BKS Feasibility Rate by Algorithm', fontsize=13, fontweight='bold')
        ax1.set_ylim(0, 105)
        ax1.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5)
        ax1.grid(axis='y', alpha=0.3)
        
        # Count comparison
        instances_solved = [algo_feasible[a] for a in algorithms]
        instances_unsolved = [algo_total[a] - algo_feasible[a] for a in algorithms]
        
        x_pos = np.arange(len(algorithms))
        width = 0.6
        
        ax2.bar(x_pos, instances_solved, width, label='Solved (K=BKS)', color='#2ecc71', alpha=0.8)
        ax2.bar(x_pos, instances_unsolved, width, bottom=instances_solved, 
               label='Unsolved (K>BKS)', color='#e74c3c', alpha=0.8)
        
        ax2.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Instance Count', fontsize=12, fontweight='bold')
        ax2.set_title('Solved vs Unsolved Instances', fontsize=13, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(algorithms)
        ax2.legend(loc='upper left', fontsize=10)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / "10_k_feasibility_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def plot_algorithm_comparison_radar(self):
        """Radar chart: Multi-dimensional algorithm comparison (CANONICAL #11)"""
        if not self.data:
            return
        
        try:
            from math import pi
        except ImportError:
            return
        
        # Collect metrics per algorithm
        algo_metrics = {}
        for row in self.data:
            algo = row.get('algorithm', 'Unknown')
            try:
                distance = float(row.get('d_final', 0))
                time_sec = float(row.get('time_sec', 0))
                
                if algo not in algo_metrics:
                    algo_metrics[algo] = {'distances': [], 'times': []}
                algo_metrics[algo]['distances'].append(distance)
                algo_metrics[algo]['times'].append(time_sec)
            except (ValueError, TypeError):
                continue
        
        if not algo_metrics:
            return
        
        # Compute normalized metrics (0-1 scale)
        algorithms = sorted(algo_metrics.keys())
        
        # Normalize metrics
        all_distances = []
        all_times = []
        for algo_data in algo_metrics.values():
            all_distances.extend(algo_data['distances'])
            all_times.extend(algo_data['times'])
        
        min_dist = min(all_distances) if all_distances else 1
        max_dist = max(all_distances) if all_distances else 1
        min_time = min(all_times) if all_times else 1
        max_time = max(all_times) if all_times else 1
        
        # Prepare data for radar
        categories = ['Avg Distance', 'Time Efficiency', 'Consistency']
        N = len(categories)
        
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6']
        
        for algo, color in zip(algorithms, colors):
            try:
                avg_dist = np.mean(algo_metrics[algo]['distances'])
                avg_time = np.mean(algo_metrics[algo]['times'])
                
                # Normalize to 0-1 scale
                norm_dist = 1.0 - (avg_dist - min_dist) / (max_dist - min_dist) if max_dist > min_dist else 0.5
                norm_time = 1.0 - (avg_time - min_time) / (max_time - min_time) if max_time > min_time else 0.5
                norm_consistency = 1.0 - (np.std(algo_metrics[algo]['distances']) / avg_dist) if avg_dist > 0 else 0.5
                
                values = [norm_dist, norm_time, norm_consistency]
                values += values[:1]
                
                ax.plot(angles, values, 'o-', linewidth=2, label=algo, color=color)
                ax.fill(angles, values, alpha=0.15, color=color)
            except (ValueError, ZeroDivisionError):
                continue
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=9)
        ax.grid(True, alpha=0.3)
        
        ax.set_title('Algorithm Comparison: Multi-Dimensional Radar', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
        
        plt.tight_layout()
        output_path = self.plots_dir / "11_algorithm_radar_comparison.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")


def generate_visualizations(results_csv_path: str, plots_dir: str):
    """
    Generate all visualizations from experiment results.
    
    Args:
        results_csv_path: Path to raw_results.csv file
        plots_dir: Directory to save plots
    """
    if not MATPLOTLIB_AVAILABLE:
        print("[WARNING] matplotlib/seaborn required for visualization")
        print("Install with: pip install matplotlib seaborn numpy")
        return
    
    visualizer = ResultVisualizer(results_csv_path, plots_dir)
    visualizer.generate_all()
