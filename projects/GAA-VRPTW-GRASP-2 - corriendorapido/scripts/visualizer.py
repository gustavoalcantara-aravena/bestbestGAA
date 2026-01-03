"""
Phase 8: Visualizations and Graphics - Canonical graphs for VRPTW analysis

Responsabilidades:
1. MatplotlibVisualizer: Generate convergence plots, boxplots, heatmaps
2. Graph methods: convergence_K, convergence_D, K_boxplot, D_boxplot, gap_heatmap
3. File output: Save PNG files to plots/ directory with proper naming
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environments
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class PlotConfig:
    """Configuration for plot styling"""
    dpi: int = 150
    figsize: Tuple[int, int] = (12, 6)
    style: str = 'seaborn-v0_8-darkgrid'
    colors: Dict[str, str] = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                'C': '#1f77b4',   # blue
                'R': '#ff7f0e',   # orange
                'RC': '#2ca02c',  # green
                'convergence': '#d62728',  # red
                'bks': '#9467bd'  # purple
            }


class MatplotlibVisualizer:
    """Generates canonical VRPTW visualization plots"""
    
    def __init__(self, output_dir: str = "output/plots", config: Optional[PlotConfig] = None):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save plots
            config: PlotConfig for styling
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.config = config or PlotConfig()
        
        # Set style
        try:
            plt.style.use(self.config.style)
        except:
            pass  # Fallback to default if style not available
    
    def convergence_K(self, convergence_df: pd.DataFrame, algorithm_id: str, 
                     save_path: Optional[str] = None) -> str:
        """
        Plot convergence of K (number of vehicles) - step-wise decreasing
        
        Args:
            convergence_df: DataFrame with columns: iteration, K_best_so_far, algorithm_id
            algorithm_id: Algorithm identifier
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        algo_data = convergence_df[convergence_df['algorithm_id'] == algorithm_id]
        
        if algo_data.empty:
            raise ValueError(f"No data for algorithm {algorithm_id}")
        
        fig, ax = plt.subplots(figsize=self.config.figsize, dpi=self.config.dpi)
        
        # Group by instance and plot each separately (with transparency)
        for instance_id in algo_data['instance_id'].unique():
            instance_data = algo_data[algo_data['instance_id'] == instance_id].sort_values('iteration')
            ax.step(instance_data['iteration'], instance_data['K_best_so_far'], 
                   where='post', alpha=0.5, linewidth=1.5, label=instance_id)
        
        # Plot mean convergence
        mean_k = algo_data.groupby('iteration')['K_best_so_far'].mean()
        ax.plot(mean_k.index, mean_k.values, color=self.config.colors['convergence'],
               linewidth=3, label='Mean K', linestyle='--')
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('K (Number of Vehicles)', fontsize=12, fontweight='bold')
        ax.set_title(f'Convergence K - {algorithm_id}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8, ncol=2)
        
        if save_path is None:
            save_path = self.output_dir / f"convergence_K_{algorithm_id}.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def convergence_D(self, convergence_df: pd.DataFrame, algorithm_id: str,
                     save_path: Optional[str] = None) -> str:
        """
        Plot convergence of D (distance) - only for iterations where K == K_BKS
        
        Args:
            convergence_df: DataFrame with columns: iteration, D_best_so_far, is_K_BKS, algorithm_id
            algorithm_id: Algorithm identifier
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        algo_data = convergence_df[convergence_df['algorithm_id'] == algorithm_id]
        
        if algo_data.empty:
            raise ValueError(f"No data for algorithm {algorithm_id}")
        
        # Only plot data where K == K_BKS
        valid_data = algo_data[algo_data['is_K_BKS'] == True]
        
        if valid_data.empty:
            # Return empty plot with note
            fig, ax = plt.subplots(figsize=self.config.figsize, dpi=self.config.dpi)
            ax.text(0.5, 0.5, 'No data where K == K_BKS', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(f'Convergence D - {algorithm_id} (No valid K)', fontsize=14, fontweight='bold')
            
            if save_path is None:
                save_path = self.output_dir / f"convergence_D_{algorithm_id}.png"
            else:
                save_path = Path(save_path)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            plt.close()
            return str(save_path)
        
        fig, ax = plt.subplots(figsize=self.config.figsize, dpi=self.config.dpi)
        
        # Plot convergence for each instance (only valid parts)
        for instance_id in valid_data['instance_id'].unique():
            instance_data = valid_data[valid_data['instance_id'] == instance_id].sort_values('iteration')
            ax.plot(instance_data['iteration'], instance_data['D_best_so_far'],
                   alpha=0.5, linewidth=1.5, marker='o', markersize=3, label=instance_id)
        
        # Plot mean convergence
        mean_d = valid_data.groupby('iteration')['D_best_so_far'].mean()
        ax.plot(mean_d.index, mean_d.values, color=self.config.colors['convergence'],
               linewidth=3, label='Mean D (K=BKS)', linestyle='--', marker='s', markersize=5)
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('D (Distance)', fontsize=12, fontweight='bold')
        ax.set_title(f'Convergence D (K=BKS only) - {algorithm_id}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8, ncol=2)
        
        if save_path is None:
            save_path = self.output_dir / f"convergence_D_{algorithm_id}.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def K_boxplot(self, raw_results_df: pd.DataFrame, save_path: Optional[str] = None) -> str:
        """
        Boxplot of K by algorithm and family
        
        Args:
            raw_results_df: DataFrame with columns: algorithm_id, family, K_final
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        fig, ax = plt.subplots(figsize=(14, 6), dpi=self.config.dpi)
        
        # Prepare data: group by algorithm and family
        families = sorted(raw_results_df['family'].unique())
        algorithms = sorted(raw_results_df['algorithm_id'].unique())
        
        positions = []
        labels = []
        data_to_plot = []
        colors_list = []
        
        for i, algo in enumerate(algorithms):
            for j, family in enumerate(families):
                subset = raw_results_df[(raw_results_df['algorithm_id'] == algo) & 
                                       (raw_results_df['family'] == family)]
                if not subset.empty:
                    positions.append(i * (len(families) + 1) + j)
                    labels.append(f"{algo}\n{family}")
                    data_to_plot.append(subset['K_final'].values)
                    colors_list.append(self.config.colors.get(family, '#cccccc'))
        
        bp = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True,
                       showmeans=True, meanline=False)
        
        # Color boxes by family
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('K (Number of Vehicles)', fontsize=12, fontweight='bold')
        ax.set_title('K Distribution by Algorithm and Family (Boxplot)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Legend for families
        legend_elements = [mpatches.Patch(facecolor=self.config.colors.get(fam, '#cccccc'), alpha=0.7, label=fam)
                          for fam in families]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        if save_path is None:
            save_path = self.output_dir / "K_boxplot_by_algorithm_family.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def D_boxplot(self, raw_results_df: pd.DataFrame, save_path: Optional[str] = None) -> str:
        """
        Boxplot of D by algorithm (only for cases where K == K_BKS)
        
        Args:
            raw_results_df: DataFrame with columns: algorithm_id, family, D_final, reached_K_BKS
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        # Filter: only keep rows where reached_K_BKS == True
        valid_data = raw_results_df[raw_results_df['reached_K_BKS'] == True]
        
        if valid_data.empty:
            fig, ax = plt.subplots(figsize=(12, 6), dpi=self.config.dpi)
            ax.text(0.5, 0.5, 'No data where K == K_BKS', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title('D Boxplot (No valid K == K_BKS data)', fontsize=14, fontweight='bold')
            
            if save_path is None:
                save_path = self.output_dir / "D_boxplot_by_algorithm_family.png"
            else:
                save_path = Path(save_path)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            plt.close()
            return str(save_path)
        
        fig, ax = plt.subplots(figsize=(14, 6), dpi=self.config.dpi)
        
        families = sorted(valid_data['family'].unique())
        algorithms = sorted(valid_data['algorithm_id'].unique())
        
        positions = []
        labels = []
        data_to_plot = []
        colors_list = []
        
        for i, algo in enumerate(algorithms):
            for j, family in enumerate(families):
                subset = valid_data[(valid_data['algorithm_id'] == algo) & 
                                   (valid_data['family'] == family)]
                if not subset.empty:
                    positions.append(i * (len(families) + 1) + j)
                    labels.append(f"{algo}\n{family}")
                    data_to_plot.append(subset['D_final'].values)
                    colors_list.append(self.config.colors.get(family, '#cccccc'))
        
        bp = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True,
                       showmeans=True, meanline=False)
        
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('D (Distance)', fontsize=12, fontweight='bold')
        ax.set_title('D Distribution by Algorithm and Family (K=BKS only)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        legend_elements = [mpatches.Patch(facecolor=self.config.colors.get(fam, '#cccccc'), alpha=0.7, label=fam)
                          for fam in families]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        if save_path is None:
            save_path = self.output_dir / "D_boxplot_by_algorithm_family.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def gap_heatmap(self, gap_data_by_family: Dict[str, List[float]], 
                   save_path: Optional[str] = None) -> str:
        """
        Heatmap of %GAP values by family
        
        Args:
            gap_data_by_family: Dict mapping family -> list of gap percentages
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.config.dpi)
        
        families = sorted(gap_data_by_family.keys())
        
        # Create matrix: rows = statistics, cols = families
        stats_data = []
        stats_names = []
        
        for family in families:
            gap_values = gap_data_by_family[family]
            stats_data.append([
                np.mean(gap_values) if gap_values else 0,
                np.std(gap_values) if len(gap_values) > 1 else 0,
                np.min(gap_values) if gap_values else 0,
                np.max(gap_values) if gap_values else 0
            ])
        
        stats_names = ['Mean', 'Std Dev', 'Min', 'Max']
        
        data_matrix = np.array(stats_data).T  # Transpose: stats x families
        
        im = ax.imshow(data_matrix, cmap='RdYlGn_r', aspect='auto')
        
        ax.set_xticks(np.arange(len(families)))
        ax.set_yticks(np.arange(len(stats_names)))
        ax.set_xticklabels(families, fontsize=11)
        ax.set_yticklabels(stats_names, fontsize=11)
        
        # Add text annotations
        for i in range(len(stats_names)):
            for j in range(len(families)):
                text = ax.text(j, i, f'{data_matrix[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=10)
        
        ax.set_title('%GAP Statistics by Family (Heatmap)', fontsize=14, fontweight='bold')
        fig.colorbar(im, ax=ax, label='%GAP Value')
        
        if save_path is None:
            save_path = self.output_dir / "gap_heatmap_by_family.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
    def time_comparison(self, raw_results_df: pd.DataFrame, save_path: Optional[str] = None) -> str:
        """
        Bar chart comparing execution time by algorithm and family
        
        Args:
            raw_results_df: DataFrame with columns: algorithm_id, family, total_time_sec
            save_path: Optional custom save path
            
        Returns:
            Path to saved image
        """
        fig, ax = plt.subplots(figsize=(12, 6), dpi=self.config.dpi)
        
        # Group by algorithm and family, calculate mean time
        grouped = raw_results_df.groupby(['algorithm_id', 'family'])['total_time_sec'].mean().unstack(fill_value=0)
        
        grouped.plot(kind='bar', ax=ax, color=[self.config.colors.get(fam, '#cccccc') 
                                               for fam in grouped.columns], alpha=0.7)
        
        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Average Execution Time by Algorithm and Family', fontsize=14, fontweight='bold')
        ax.legend(title='Family', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        if save_path is None:
            save_path = self.output_dir / "time_comparison.png"
        else:
            save_path = Path(save_path)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        plt.close()
        
        return str(save_path)


if __name__ == "__main__":
    # Example usage
    viz = MatplotlibVisualizer()
    print(f"Visualizer initialized. Output directory: {viz.output_dir}")
