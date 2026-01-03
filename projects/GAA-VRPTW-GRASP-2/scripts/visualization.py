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


    def generate_gap_plots_from_json(self, json_path: str):
        """
        Generate GAP comparison plots from JSON data.
        
        Args:
            json_path: Path to gap_data.json file
        """
        if not Path(json_path).exists():
            print(f"[WARNING] JSON file not found: {json_path}")
            return
        
        try:
            with open(json_path, 'r') as f:
                gap_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load JSON: {e}")
            return
        
        if not MATPLOTLIB_AVAILABLE:
            print("[ERROR] Cannot generate plots without matplotlib")
            return
        
        print(f"[INFO] Generating GAP plots from JSON...")
        
        # GAP COMPARISON PLOTS (5 types)
        self._plot_gap_comparison_bars(gap_data)           # 01_gap_comparison_all_instances
        self._plot_gap_evolution_lines(gap_data)           # 02_gap_evolution_lines
        self._plot_gap_boxplot_by_family(gap_data)         # 03_gap_boxplot_by_family
        self._plot_gap_heatmap(gap_data)                   # 04_gap_heatmap
        self._plot_gap_by_family_grid(gap_data)            # 05_gap_by_family_grid
        
        print(f"[INFO] GAP plots generation complete! (5 comparison plots)")
    
    def _plot_gap_comparison_bars(self, gap_data: Dict):
        """Gráfico 01: Comparación de GAP por instancia (barras)"""
        instances = list(gap_data['instances'].keys())
        instances.sort()
        
        algo1_gaps = []
        algo2_gaps = []
        algo3_gaps = []
        
        for inst in instances:
            inst_data = gap_data['instances'][inst]
            algo1_gaps.append(inst_data['algorithms'].get('algo1', {}).get('gap_percent', 0))
            algo2_gaps.append(inst_data['algorithms'].get('algo2', {}).get('gap_percent', 0))
            algo3_gaps.append(inst_data['algorithms'].get('algo3', {}).get('gap_percent', 0))
        
        fig, ax = plt.subplots(figsize=(24, 8))
        
        x_pos = np.arange(len(instances))
        width = 0.25
        
        ax.bar(x_pos - width, algo1_gaps, width, label='Algoritmo 1', alpha=0.8, color='#FF6B6B')
        ax.bar(x_pos, algo2_gaps, width, label='Algoritmo 2', alpha=0.8, color='#4ECDC4')
        ax.bar(x_pos + width, algo3_gaps, width, label='Algoritmo 3', alpha=0.8, color='#FFE66D')
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
        
        ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Comparación GAP: 3 Algoritmos vs Best Known Solutions\nTodas las Instancias Solomon', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(instances, rotation=45, ha='right')
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        # Colorear fondo por familia
        families = [gap_data['instances'][inst]['family'] for inst in instances]
        unique_families = []
        family_changes = []
        for i, fam in enumerate(families):
            if fam not in unique_families:
                unique_families.append(fam)
                family_changes.append(i)
        
        for i in range(len(family_changes)):
            start = family_changes[i]
            end = family_changes[i + 1] if i + 1 < len(family_changes) else len(instances)
            if i % 2 == 0:
                ax.axvspan(start - 0.5, end - 0.5, alpha=0.1, color='gray', zorder=0)
        
        plt.tight_layout()
        output_path = self.plots_dir / '01_gap_comparison_all_instances.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def _plot_gap_evolution_lines(self, gap_data: Dict):
        """Gráfico 02: Evolución de GAP (líneas)"""
        instances = list(gap_data['instances'].keys())
        instances.sort()
        
        algo1_gaps = []
        algo2_gaps = []
        algo3_gaps = []
        
        for inst in instances:
            inst_data = gap_data['instances'][inst]
            algo1_gaps.append(inst_data['algorithms'].get('algo1', {}).get('gap_percent', 0))
            algo2_gaps.append(inst_data['algorithms'].get('algo2', {}).get('gap_percent', 0))
            algo3_gaps.append(inst_data['algorithms'].get('algo3', {}).get('gap_percent', 0))
        
        fig, ax = plt.subplots(figsize=(24, 8))
        
        x_pos = np.arange(len(instances))
        
        ax.plot(x_pos, algo1_gaps, 'o-', linewidth=2.5, markersize=6, 
                label='Algoritmo 1', color='#FF6B6B', alpha=0.8)
        ax.plot(x_pos, algo2_gaps, 's-', linewidth=2.5, markersize=6, 
                label='Algoritmo 2', color='#4ECDC4', alpha=0.8)
        ax.plot(x_pos, algo3_gaps, '^-', linewidth=2.5, markersize=6, 
                label='Algoritmo 3', color='#FFE66D', alpha=0.8)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2.5, label='BKS (GAP=0)', alpha=0.7)
        
        ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución de GAP por Instancia: Comparación 3 Algoritmos\nTodas las Instancias Solomon', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(instances, rotation=45, ha='right')
        ax.legend(fontsize=11, loc='upper left', framealpha=0.95)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / '02_gap_evolution_lines.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def _plot_gap_boxplot_by_family(self, gap_data: Dict):
        """Gráfico 03: GAP por familia (boxplot)"""
        # Agrupar por familia
        families_dict = {}
        for inst, inst_data in gap_data['instances'].items():
            family = inst_data['family']
            if family not in families_dict:
                families_dict[family] = {'algo1': [], 'algo2': [], 'algo3': []}
            
            for algo_num in [1, 2, 3]:
                gap = inst_data['algorithms'].get(f'algo{algo_num}', {}).get('gap_percent')
                if gap is not None:
                    families_dict[family][f'algo{algo_num}'].append(gap)
        
        families = sorted(families_dict.keys())
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        positions = np.arange(len(families))
        width = 0.25
        
        gap_data_algo1 = [families_dict[fam]['algo1'] for fam in families]
        gap_data_algo2 = [families_dict[fam]['algo2'] for fam in families]
        gap_data_algo3 = [families_dict[fam]['algo3'] for fam in families]
        
        bp1 = ax.boxplot(gap_data_algo1, positions=positions - width, widths=width, 
                          patch_artist=True, label='Algoritmo 1')
        bp2 = ax.boxplot(gap_data_algo2, positions=positions, widths=width, 
                          patch_artist=True, label='Algoritmo 2')
        bp3 = ax.boxplot(gap_data_algo3, positions=positions + width, widths=width, 
                          patch_artist=True, label='Algoritmo 3')
        
        for patch in bp1['boxes']:
            patch.set_facecolor('#FF6B6B')
            patch.set_alpha(0.7)
        for patch in bp2['boxes']:
            patch.set_facecolor('#4ECDC4')
            patch.set_alpha(0.7)
        for patch in bp3['boxes']:
            patch.set_facecolor('#FFE66D')
            patch.set_alpha(0.7)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
        ax.set_xlabel('Familia Solomon', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de GAP por Familia: 3 Algoritmos (Boxplot)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(positions)
        ax.set_xticklabels(families)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / '03_gap_boxplot_by_family.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def _plot_gap_heatmap(self, gap_data: Dict):
        """Gráfico 04: Heatmap de GAP"""
        import pandas as pd
        
        instances = sorted(gap_data['instances'].keys())
        
        gap_matrix_data = {
            'Algo 1': [],
            'Algo 2': [],
            'Algo 3': [],
        }
        
        for inst in instances:
            inst_data = gap_data['instances'][inst]
            gap_matrix_data['Algo 1'].append(inst_data['algorithms'].get('algo1', {}).get('gap_percent', 0))
            gap_matrix_data['Algo 2'].append(inst_data['algorithms'].get('algo2', {}).get('gap_percent', 0))
            gap_matrix_data['Algo 3'].append(inst_data['algorithms'].get('algo3', {}).get('gap_percent', 0))
        
        gap_matrix = pd.DataFrame(gap_matrix_data, index=instances)
        
        fig, ax = plt.subplots(figsize=(12, 16))
        
        sns.heatmap(gap_matrix, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
                    cbar_kws={'label': 'GAP a BKS (%)'}, ax=ax, linewidths=0.5, linecolor='gray')
        
        ax.set_title('Heatmap: GAP de cada Algoritmo vs Instancia\n(Rojo=Peor, Verde=Mejor)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Instancia', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.plots_dir / '04_gap_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def _plot_gap_by_family_grid(self, gap_data: Dict):
        """Gráfico 05: GAP por familia (grid 2x3)"""
        # Agrupar por familia
        families_dict = {}
        for inst, inst_data in gap_data['instances'].items():
            family = inst_data['family']
            if family not in families_dict:
                families_dict[family] = {'instances': [], 'algo1': [], 'algo2': [], 'algo3': []}
            
            families_dict[family]['instances'].append(inst)
            for algo_num in [1, 2, 3]:
                gap = inst_data['algorithms'].get(f'algo{algo_num}', {}).get('gap_percent', 0)
                families_dict[family][f'algo{algo_num}'].append(gap)
        
        families = sorted(families_dict.keys())
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()
        
        for idx, family in enumerate(families):
            family_data = families_dict[family]
            
            x = np.arange(len(family_data['instances']))
            width = 0.25
            
            ax = axes[idx]
            ax.bar(x - width, family_data['algo1'], width, label='Algo 1', color='#FF6B6B', alpha=0.8)
            ax.bar(x, family_data['algo2'], width, label='Algo 2', color='#4ECDC4', alpha=0.8)
            ax.bar(x + width, family_data['algo3'], width, label='Algo 3', color='#FFE66D', alpha=0.8)
            
            ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
            ax.set_title(f'Familia {family} ({len(family_data["instances"])} instancias)', 
                        fontsize=11, fontweight='bold')
            ax.set_xlabel('Instancia', fontsize=10)
            ax.set_ylabel('GAP (%)', fontsize=10)
            ax.set_xticks(x)
            ax.set_xticklabels([inst.replace(family, '') for inst in family_data['instances']], rotation=45)
            ax.grid(axis='y', alpha=0.3)
            ax.legend(fontsize=9)
        
        plt.suptitle('Comparación de GAP por Familia Solomon VRPTW', 
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        output_path = self.plots_dir / '05_gap_by_family_grid.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
    
    def generate_gap_plots_from_json(self, json_path: str):
        """
        Generate all GAP plots from JSON data file
        
        Args:
            json_path: Path to gap_data.json
        """
        json_path = Path(json_path)
        if not json_path.exists():
            print(f"[ERROR] JSON not found: {json_path}")
            return
        
        with open(json_path) as f:
            gap_data = json.load(f)
        
        print(f"\n[GAP PLOTS] Generating from JSON: {json_path.name}")
        
        instances_data = gap_data.get('instances', {})
        if not instances_data:
            print("[WARNING] No instance data in JSON")
            return
        
        # Extract data into sorted lists
        instance_ids = sorted(instances_data.keys())
        families = [instances_data[inst]['family'] for inst in instance_ids]
        
        algo_gaps = {'1': [], '2': [], '3': []}
        algo_distances = {'1': [], '2': [], '3': []}
        
        for instance_id in instance_ids:
            inst_data = instances_data[instance_id]
            for algo_num in ['1', '2', '3']:
                algo_key = f'algo{algo_num}'
                if algo_key in inst_data.get('algorithms', {}):
                    algo_info = inst_data['algorithms'][algo_key]
                    gap = algo_info.get('gap_percent')
                    distance = algo_info.get('distance')
                    if gap is not None:
                        algo_gaps[algo_num].append(gap)
                    if distance is not None:
                        algo_distances[algo_num].append(distance)
        
        # ============================================================
        # GRÁFICO 1: GAP por instancia (todas)
        # ============================================================
        fig, ax = plt.subplots(figsize=(24, 8))
        
        x_pos = np.arange(len(instance_ids))
        width = 0.25
        
        bars1 = ax.bar(x_pos - width, algo_gaps['1'], width, label='Algoritmo 1', alpha=0.8, color='#FF6B6B')
        bars2 = ax.bar(x_pos, algo_gaps['2'], width, label='Algoritmo 2', alpha=0.8, color='#4ECDC4')
        bars3 = ax.bar(x_pos + width, algo_gaps['3'], width, label='Algoritmo 3', alpha=0.8, color='#FFE66D')
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
        ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Comparación GAP: 3 Algoritmos vs Best Known Solutions\n56 Instancias Solomon', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(instance_ids, rotation=45, ha='right')
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / '06_gap_comparison_all_instances.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
        
        # ============================================================
        # GRÁFICO 2: Líneas de GAP
        # ============================================================
        fig, ax = plt.subplots(figsize=(24, 8))
        
        ax.plot(x_pos, algo_gaps['1'], 'o-', linewidth=2.5, markersize=6, 
                label='Algoritmo 1', color='#FF6B6B', alpha=0.8)
        ax.plot(x_pos, algo_gaps['2'], 's-', linewidth=2.5, markersize=6, 
                label='Algoritmo 2', color='#4ECDC4', alpha=0.8)
        ax.plot(x_pos, algo_gaps['3'], '^-', linewidth=2.5, markersize=6, 
                label='Algoritmo 3', color='#FFE66D', alpha=0.8)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2.5, label='BKS (GAP=0)', alpha=0.7)
        ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución de GAP por Instancia: Comparación 3 Algoritmos\n56 Instancias Solomon', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(instance_ids, rotation=45, ha='right')
        ax.legend(fontsize=11, loc='upper left', framealpha=0.95)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / '07_gap_evolution_lines.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
        
        # ============================================================
        # GRÁFICO 3: Boxplot por familia
        # ============================================================
        fig, ax = plt.subplots(figsize=(14, 8))
        
        unique_families = sorted(set(families))
        positions = np.arange(len(unique_families))
        width = 0.25
        
        gap_by_family = {algo: [] for algo in ['1', '2', '3']}
        for family in unique_families:
            for algo in ['1', '2', '3']:
                family_gaps = [algo_gaps[algo][i] for i, f in enumerate(families) if f == family]
                gap_by_family[algo].append(family_gaps)
        
        bp1 = ax.boxplot(gap_by_family['1'], positions=positions - width, widths=width, 
                          patch_artist=True, label='Algoritmo 1')
        bp2 = ax.boxplot(gap_by_family['2'], positions=positions, widths=width, 
                          patch_artist=True, label='Algoritmo 2')
        bp3 = ax.boxplot(gap_by_family['3'], positions=positions + width, widths=width, 
                          patch_artist=True, label='Algoritmo 3')
        
        for patch in bp1['boxes']:
            patch.set_facecolor('#FF6B6B')
            patch.set_alpha(0.7)
        for patch in bp2['boxes']:
            patch.set_facecolor('#4ECDC4')
            patch.set_alpha(0.7)
        for patch in bp3['boxes']:
            patch.set_facecolor('#FFE66D')
            patch.set_alpha(0.7)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
        ax.set_xlabel('Familia Solomon', fontsize=12, fontweight='bold')
        ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de GAP por Familia: 3 Algoritmos\n(Boxplot)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(positions)
        ax.set_xticklabels(unique_families)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.plots_dir / '08_gap_boxplot_by_family.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {output_path.name}")
        
        # ============================================================
        # GRÁFICO 4: Estadísticas resumidas
        # ============================================================
        print(f"\n[GAP STATISTICS]")
        for algo_num in ['1', '2', '3']:
            gaps = algo_gaps[algo_num]
            distances = algo_distances[algo_num]
            if gaps:
                print(f"\nAlgoritmo {algo_num}:")
                print(f"  Promedio GAP: {np.mean(gaps):.2f}%")
                print(f"  Mediana GAP: {np.median(gaps):.2f}%")
                print(f"  Desv. Est.: {np.std(gaps):.2f}%")
                print(f"  Min GAP: {np.min(gaps):.2f}%")
                print(f"  Max GAP: {np.max(gaps):.2f}%")
                print(f"  Promedio Distance: {np.mean(distances):.2f}")
                print(f"  Instancias mejor que BKS: {sum(1 for g in gaps if g < 0)}")





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


def generate_gap_plots(json_path: str, plots_dir: str):
    """
    Generate GAP comparison plots from JSON data.
    
    Args:
        json_path: Path to gap_data.json file
        plots_dir: Directory to save plots
    """
    if not MATPLOTLIB_AVAILABLE:
        print("[WARNING] matplotlib/seaborn required for visualization")
        print("Install with: pip install matplotlib seaborn numpy")
        return
    
    visualizer = ResultVisualizer("", plots_dir)
    visualizer.generate_gap_plots_from_json(json_path)
