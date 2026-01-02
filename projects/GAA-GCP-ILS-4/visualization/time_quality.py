"""
visualization/time_quality.py
Análisis de tiempo-calidad: Frontera de Pareto

Visualiza la relación entre tiempo de computación y calidad de la solución.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def plot_time_quality_tradeoff(
    times: List[float],
    fitness_values: List[float],
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Tiempo-Calidad Tradeoff",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica la relación entre tiempo de computación y calidad de solución.
    
    Parámetros:
        times: Lista de tiempos de computación
        fitness_values: Lista de valores de fitness correspondientes
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> times = [0.1, 0.5, 1.0, 2.0]
        >>> fitness = [45, 43, 42, 41]
        >>> plot_time_quality_tradeoff(times, fitness, output_path="tradeoff.png")
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Graficar puntos
    scatter = ax.scatter(times, fitness_values, 
                        c=np.arange(len(times)), cmap='viridis',
                        s=100, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Conectar puntos con línea
    sorted_idx = np.argsort(times)
    ax.plot(np.array(times)[sorted_idx], np.array(fitness_values)[sorted_idx],
           color='gray', alpha=0.5, linestyle='--', linewidth=1.5)
    
    # Colorbar mostrando progresión temporal
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Execution Time', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Computation Time (seconds)', fontsize=12)
    ax.set_ylabel('Number of Colors (Fitness)', fontsize=12)
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Estadísticas
    improvement = fitness_values[0] - fitness_values[-1]
    improvement_ratio = (improvement / fitness_values[0] * 100) if fitness_values[0] > 0 else 0
    time_ratio = times[-1] / times[0] if times[0] > 0 else 0
    
    stats_text = (
        f"Improvement: {improvement:.0f} ({improvement_ratio:.1f}%)\n"
        f"Total Time: {times[-1]:.2f}s\n"
        f"Initial Fitness: {fitness_values[0]:.0f}\n"
        f"Final Fitness: {fitness_values[-1]:.0f}"
    )
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Decoración
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return str(output_path)
    else:
        plt.show()
        plt.close()
        return None


def plot_multiple_algorithms_tradeoff(
    algorithms: Dict[str, Dict[str, List[float]]],
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Comparación Tiempo-Calidad",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Compara múltiples algoritmos en el plano tiempo-calidad.
    
    Parámetros:
        algorithms: {nombre_algoritmo: {'times': [...], 'fitness': [...]}}
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> algs = {
        ...     'ILS': {'times': [0.1, 0.5, 1.0], 'fitness': [45, 42, 41]},
        ...     'GRASP': {'times': [0.2, 0.8, 1.5], 'fitness': [44, 40, 39]}
        ... }
        >>> plot_multiple_algorithms_tradeoff(algs)
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(algorithms)))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
    
    for (alg_name, data), color, marker in zip(algorithms.items(), colors, markers):
        times = data['times']
        fitness = data['fitness']
        
        ax.plot(times, fitness, marker=marker, markersize=8, linewidth=2.5,
               label=alg_name, color=color, alpha=0.7)
    
    ax.set_xlabel('Tiempo de computación (segundos)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de colores (Fitness)', fontsize=12, fontweight='bold')
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.legend(loc='best', fontsize=10, framealpha=0.95)
    
    # Decoración
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return str(output_path)
    else:
        plt.show()
        plt.close()
        return None


def plot_convergence_speed(
    time_fitness_pairs: List[Tuple[float, float]],
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Velocidad de Convergencia",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica la velocidad de convergencia: mejora por unidad de tiempo.
    
    Parámetros:
        time_fitness_pairs: Lista de tuplas (tiempo, fitness)
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    """
    times = np.array([t for t, _ in time_fitness_pairs])
    fitness = np.array([f for _, f in time_fitness_pairs])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi)
    
    # Subgráfica 1: Curva tiempo-fitness
    ax1.plot(times, fitness, marker='o', markersize=6, linewidth=2.5, color='#1f77b4')
    ax1.fill_between(times, fitness, alpha=0.2, color='#1f77b4')
    
    ax1.set_xlabel('Tiempo (segundos)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Fitness', fontsize=11, fontweight='bold')
    ax1.set_title('Curva Tiempo-Fitness', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Subgráfica 2: Velocidad de mejora
    velocity = np.diff(fitness) / np.diff(times)
    velocity = np.abs(velocity)  # Valor absoluto porque fitness decrece
    mid_times = times[:-1] + np.diff(times) / 2
    
    colors = plt.cm.RdYlGn(velocity / velocity.max())
    ax2.scatter(mid_times, velocity, c=velocity, cmap='RdYlGn', s=100, alpha=0.7)
    ax2.bar(mid_times, velocity, width=np.diff(times), color=colors, alpha=0.6, edgecolor='black')
    
    ax2.set_xlabel('Tiempo (segundos)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Velocidad de mejora (colores/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Velocidad de Convergencia', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    fig.suptitle(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return str(output_path)
    else:
        plt.show()
        plt.close()
        return None
