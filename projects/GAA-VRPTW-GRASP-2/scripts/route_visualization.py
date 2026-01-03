"""
Route Visualization Module for VRPTW

Generates 2D visualizations of VRPTW solutions showing:
- Customer nodes (circles)
- Depot node (special marker)
- Directed arcs with arrows showing visit sequence
- Different colors for each vehicle/route
- Route statistics (distance, customers, load)
"""

from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyArrowPatch
    import matplotlib.lines as mlines
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class RouteVisualizer:
    """Visualize VRPTW solutions with routes and directed arcs"""
    
    def __init__(self, instance, solution, output_dir: str = "plots"):
        """
        Initialize route visualizer.
        
        Args:
            instance: VRPTW Instance object with coordinates and customers
            solution: Solution object with routes
            output_dir: Directory to save visualizations
        """
        self.instance = instance
        self.solution = solution
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Prepare coordinates
        self.depot_coord = (instance.get_customer(0).x, instance.get_customer(0).y)
        self.customer_coords = {
            i: (instance.get_customer(i).x, instance.get_customer(i).y)
            for i in range(1, instance.n_customers + 1)
        }
        
        # Color palette for vehicles
        self.colors = self._get_color_palette()
    
    def _get_color_palette(self) -> List[str]:
        """Get distinct colors for routes"""
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
            '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#AED6F1',
            '#F1948A', '#82E0AA', '#F5B7B1', '#A9CCE3', '#F9E79F'
        ]
        return colors
    
    def visualize(self, instance_name: str = None, show_stats: bool = True) -> str:
        """
        Generate route visualization.
        
        Args:
            instance_name: Name for the output file (default: instance ID)
            show_stats: Whether to show route statistics
            
        Returns:
            Path to saved figure
        """
        if not MATPLOTLIB_AVAILABLE:
            print("[WARNING] matplotlib not available for route visualization")
            return None
        
        if instance_name is None:
            instance_name = self.instance.name if hasattr(self.instance, 'name') else 'solution'
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plot depot
        depot_x, depot_y = self.depot_coord
        ax.plot(depot_x, depot_y, marker='s', markersize=20, color='#2C3E50', 
               label='Depot', zorder=5, markeredgecolor='black', markeredgewidth=2)
        ax.text(depot_x, depot_y-2, 'Depot (0)', ha='center', fontsize=9, fontweight='bold')
        
        # Plot routes
        route_stats = []
        for route_idx, route in enumerate(self.solution.routes):
            color = self.colors[route_idx % len(self.colors)]
            customers = route.sequence[1:-1]  # Remove depot from start and end
            
            # Calculate route statistics
            route_distance = route.total_distance
            route_load = sum(self.instance.get_customer(c).demand for c in customers)
            
            route_stats.append({
                'vehicle': route_idx + 1,
                'customers': len(customers),
                'distance': route_distance,
                'load': route_load,
                'capacity': self.instance.Q_capacity
            })
            
            # Plot customers and arcs for this route
            current_x, current_y = depot_x, depot_y
            
            for cust_idx, customer_id in enumerate(route.sequence):
                if customer_id == 0:  # Skip depot markers in sequence
                    continue
                
                next_x, next_y = self.customer_coords[customer_id]
                
                # Plot customer node
                ax.plot(next_x, next_y, marker='o', markersize=12, color=color, 
                       zorder=4, markeredgecolor='black', markeredgewidth=1.5, alpha=0.9)
                
                # Add customer label
                ax.text(next_x + 0.5, next_y + 0.5, str(customer_id), 
                       fontsize=8, fontweight='bold', color=color)
                
                # Draw directed arc from current to next
                if cust_idx > 0 or customer_id != route.sequence[1]:
                    # Calculate arc properties
                    dx = next_x - current_x
                    dy = next_y - current_y
                    
                    # Draw arrow
                    arrow = FancyArrowPatch(
                        (current_x, current_y), (next_x, next_y),
                        arrowstyle='->', mutation_scale=20, linewidth=2.0,
                        color=color, alpha=0.7, zorder=3
                    )
                    ax.add_patch(arrow)
                
                current_x, current_y = next_x, next_y
            
            # Draw return arc to depot
            arrow = FancyArrowPatch(
                (current_x, current_y), (depot_x, depot_y),
                arrowstyle='->', mutation_scale=20, linewidth=2.0,
                color=color, alpha=0.7, linestyle='--', zorder=3
            )
            ax.add_patch(arrow)
        
        # Add legend for routes
        legend_handles = []
        for route_idx, stats in enumerate(route_stats):
            color = self.colors[route_idx % len(self.colors)]
            label = f"Vehicle {stats['vehicle']}: {len(stats['customers'])} cust, D={stats['distance']:.1f}"
            handle = mlines.Line2D([], [], color=color, marker='o', linestyle='-',
                                  markersize=8, linewidth=2, label=label)
            legend_handles.append(handle)
        
        ax.legend(handles=legend_handles, loc='upper left', fontsize=9, framealpha=0.95)
        
        # Set axis properties
        all_x = [depot_x] + [c[0] for c in self.customer_coords.values()]
        all_y = [depot_y] + [c[1] for c in self.customer_coords.values()]
        
        margin_x = (max(all_x) - min(all_x)) * 0.1
        margin_y = (max(all_y) - min(all_y)) * 0.1
        
        ax.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
        ax.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('X Coordinate', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y Coordinate', fontsize=12, fontweight='bold')
        
        title = f"VRPTW Solution: {instance_name}"
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add solution summary
        total_distance = sum(stats['distance'] for stats in route_stats)
        total_customers = sum(stats['customers'] for stats in route_stats)
        summary_text = f"Vehicles: {len(route_stats)} | Customers: {total_customers} | Total Distance: {total_distance:.1f}"
        ax.text(0.5, -0.08, summary_text, transform=ax.transAxes,
               ha='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save figure
        output_file = self.output_dir / f"route_visualization_{instance_name}.png"
        plt.savefig(output_file, dpi=200, bbox_inches='tight')
        plt.close()
        
        print(f"  [OK] Route visualization saved: {output_file.name}")
        
        return str(output_file)
    
    def visualize_multiple_solutions(self, solutions_dict: Dict[str, object], 
                                     output_prefix: str = "comparison"):
        """
        Generate comparison visualization of multiple solutions.
        
        Args:
            solutions_dict: Dict of {algorithm_name: solution}
            output_prefix: Prefix for output file
        """
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        num_solutions = len(solutions_dict)
        cols = min(3, num_solutions)
        rows = (num_solutions + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        if num_solutions == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        depot_x, depot_y = self.depot_coord
        
        for idx, (algo_name, solution) in enumerate(solutions_dict.items()):
            ax = axes[idx]
            
            # Plot depot
            ax.plot(depot_x, depot_y, marker='s', markersize=15, color='#2C3E50',
                   zorder=5, markeredgecolor='black', markeredgewidth=2)
            
            # Plot routes
            for route_idx, route in enumerate(solution.routes):
                color = self.colors[route_idx % len(self.colors)]
                
                # Plot path
                prev_x, prev_y = depot_x, depot_y
                for customer_id in route.sequence[1:-1]:
                    next_x, next_y = self.customer_coords[customer_id]
                    
                    ax.plot(next_x, next_y, marker='o', markersize=8, color=color,
                           zorder=4, markeredgecolor='black', markeredgewidth=1)
                    
                    arrow = FancyArrowPatch(
                        (prev_x, prev_y), (next_x, next_y),
                        arrowstyle='->', mutation_scale=15, linewidth=1.5,
                        color=color, alpha=0.7, zorder=3
                    )
                    ax.add_patch(arrow)
                    
                    prev_x, prev_y = next_x, next_y
                
                # Return to depot
                arrow = FancyArrowPatch(
                    (prev_x, prev_y), (depot_x, depot_y),
                    arrowstyle='->', mutation_scale=15, linewidth=1.5,
                    color=color, alpha=0.7, linestyle='--', zorder=3
                )
                ax.add_patch(arrow)
            
            # Axis settings
            all_x = [depot_x] + [c[0] for c in self.customer_coords.values()]
            all_y = [depot_y] + [c[1] for c in self.customer_coords.values()]
            
            margin_x = (max(all_x) - min(all_x)) * 0.1
            margin_y = (max(all_y) - min(all_y)) * 0.1
            
            ax.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
            ax.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_title(f"{algo_name}\nK={len(solution.routes)}, D={solution.total_distance:.1f}",
                        fontsize=11, fontweight='bold')
        
        # Hide unused subplots
        for idx in range(len(solutions_dict), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        output_file = self.output_dir / f"{output_prefix}_comparison.png"
        plt.savefig(output_file, dpi=200, bbox_inches='tight')
        plt.close()
        
        print(f"  [OK] Comparison visualization saved: {output_file.name}")
        
        return str(output_file)


def generate_route_visualizations(instance, solutions_dict: Dict[str, object], 
                                  output_dir: str = "plots", instance_name: str = None):
    """
    Generate route visualizations for one or more solutions.
    
    Args:
        instance: VRPTW Instance object
        solutions_dict: Dict of {algorithm_name: solution} or single solution
        output_dir: Directory to save plots
        instance_name: Name for files (default: instance.name)
        
    Returns:
        List of saved file paths
    """
    if not MATPLOTLIB_AVAILABLE:
        print("[WARNING] matplotlib not available for route visualization")
        return []
    
    if instance_name is None:
        instance_name = instance.name if hasattr(instance, 'name') else 'solution'
    
    output_files = []
    
    # Handle single solution or dict of solutions
    if not isinstance(solutions_dict, dict):
        # Single solution - create dict
        solutions_dict = {'solution': solutions_dict}
    
    # Generate individual visualizations
    for algo_name, solution in solutions_dict.items():
        visualizer = RouteVisualizer(instance, solution, output_dir)
        output_file = visualizer.visualize(f"{instance_name}_{algo_name}")
        if output_file:
            output_files.append(output_file)
    
    return output_files
