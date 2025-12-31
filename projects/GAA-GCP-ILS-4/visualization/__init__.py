"""
visualization/
Módulo de visualización de resultados

Genera gráficas de convergencia, robustez, escalabilidad y análisis.
"""

# Convergence plots
from .convergence import (
    plot_convergence_single,
    plot_convergence_multiple,
    plot_convergence_by_family
)

# Robustness analysis
from .robustness import (
    plot_robustness,
    plot_multi_robustness
)

# Scalability analysis
from .scalability import (
    plot_scalability_time,
    plot_scalability_iterations,
    plot_complexity_analysis
)

# Conflict visualization
from .heatmap import (
    plot_conflict_heatmap,
    plot_conflict_distribution,
    plot_conflict_statistics
)

# Time-quality analysis
from .time_quality import (
    plot_time_quality_tradeoff,
    plot_multiple_algorithms_tradeoff,
    plot_convergence_speed
)

# Main plotter manager
from .plotter import PlotManager

__all__ = [
    # Convergence
    'plot_convergence_single',
    'plot_convergence_multiple',
    'plot_convergence_by_family',
    # Robustness
    'plot_robustness',
    'plot_multi_robustness',
    # Scalability
    'plot_scalability_time',
    'plot_scalability_iterations',
    'plot_complexity_analysis',
    # Heatmap
    'plot_conflict_heatmap',
    'plot_conflict_distribution',
    'plot_conflict_statistics',
    # Time-Quality
    'plot_time_quality_tradeoff',
    'plot_multiple_algorithms_tradeoff',
    'plot_convergence_speed',
    # Manager
    'PlotManager'
]
