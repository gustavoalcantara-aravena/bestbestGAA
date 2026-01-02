"""
visualization/convergence.py
Gráficas de convergencia: Fitness vs Iteraciones

Visualiza el comportamiento dinámico del algoritmo ILS durante la ejecución.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Tuple


def plot_convergence_single(
    fitness_history: List[float],
    times: Optional[List[float]] = None,
    output_path: Optional[str] = None,
    instance_name: str = "Instance",
    title: str = "Convergencia de ILS",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica la convergencia de una única ejecución.
    
    Parámetros:
        fitness_history: Lista de valores de fitness a lo largo de las iteraciones
        times: Lista de tiempos (opcional, para usar en eje X secundario)
        output_path: Ruta para guardar la imagen
        instance_name: Nombre de la instancia
        title: Título de la gráfica
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> history = [50, 48, 46, 45, 45, 45]
        >>> plot_convergence_single(history, output_path="convergence.png")
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    iterations = np.arange(len(fitness_history))
    
    # Graficar fitness
    ax.plot(iterations, fitness_history, 
           color='#1f77b4', linewidth=2, marker='o', markersize=4, 
           label='Current Fitness', alpha=0.8)
    
    # Graficar mejor valor encontrado (monotónico decreciente)
    best_fitness = np.minimum.accumulate(fitness_history)
    ax.plot(iterations, best_fitness,
           color='#ff7f0e', linewidth=2.5, linestyle='--',
           label='Best Found', alpha=0.8)
    
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Number of Colors (Fitness)', fontsize=12)
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=11)
    
    # Si hay tiempos, agregar eje X secundario
    if times is not None and len(times) == len(fitness_history):
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xlabel('Time (seconds)', fontsize=11, fontweight='bold', color='gray')
        ax2.tick_params(axis='x', labelcolor='gray')
    
    # Estadísticas
    final_fitness = fitness_history[-1]
    best_found = best_fitness[-1]
    improvement = fitness_history[0] - best_found
    
    stats_text = (
        f"Initial: {fitness_history[0]:.0f}\n"
        f"Best: {best_found:.0f}\n"
        f"Final: {final_fitness:.0f}\n"
        f"Improvement: {improvement:.0f} ({improvement/fitness_history[0]*100:.1f}%)"
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


def plot_convergence_multiple(
    fitness_histories: List[List[float]],
    instance_name: str = "Instance",
    title: str = "Convergencia Promediada (N ejecuciones)",
    figsize: tuple = (12, 7),
    dpi: int = 300,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Grafica la convergencia promediada de múltiples ejecuciones.
    
    Parámetros:
        fitness_histories: Lista de historiales de fitness (cada uno de una ejecución)
        instance_name: Nombre de la instancia
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
        output_path: Ruta para guardar
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> runs = [[50, 48, 46], [51, 49, 47], [50, 47, 46]]
        >>> plot_convergence_multiple(runs, output_path="convergence_avg.png")
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Encontrar longitud mínima
    min_length = min(len(h) for h in fitness_histories)
    histories_aligned = [h[:min_length] for h in fitness_histories]
    
    # Calcular estadísticas por iteración
    histories_array = np.array(histories_aligned)
    mean_fitness = np.mean(histories_array, axis=0)
    std_fitness = np.std(histories_array, axis=0)
    q25 = np.percentile(histories_array, 25, axis=0)
    q75 = np.percentile(histories_array, 75, axis=0)
    
    iterations = np.arange(len(mean_fitness))
    
    # Graficar todas las ejecuciones con transparencia
    for hist in histories_aligned:
        ax.plot(iterations, hist, color='gray', alpha=0.15, linewidth=1)
    
    # Graficar promedio
    ax.plot(iterations, mean_fitness, 
           color='#1f77b4', linewidth=2.5, marker='o', markersize=5,
           label=f'Average ({len(histories_aligned)} runs)', zorder=10)
    
    # Zona de confianza (std)
    ax.fill_between(iterations, 
                    mean_fitness - std_fitness,
                    mean_fitness + std_fitness,
                    color='#1f77b4', alpha=0.2, label='Standard Deviation')
    
    # Zona IQR
    ax.fill_between(iterations,
                    q25, q75,
                    color='#ff7f0e', alpha=0.1, label='IQR (Q1-Q3)')
    
    # Mejor encontrado
    best_history = np.minimum.accumulate(mean_fitness)
    ax.plot(iterations, best_history,
           color='#ff7f0e', linewidth=2.5, linestyle='--',
           label='Best Found (average)', zorder=9)
    
    ax.set_xlabel('Iteración', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de colores (Fitness)', fontsize=12, fontweight='bold')
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=11)
    
    # Estadísticas globales
    stats_text = (
        f"Average Best Final: {best_history[-1]:.0f}\n"
        f"Std Dev: ±{std_fitness[-1]:.2f}\n"
        f"Min Observed: {np.min(histories_array):.0f}\n"
        f"Max Observed: {np.max(histories_array):.0f}"
    )
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
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


def plot_convergence_by_family(
    results_dict: Dict[str, List[List[float]]],
    family_names: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    title: str = "Convergencia por Familia DIMACS",
    figsize: tuple = (14, 8),
    dpi: int = 300
) -> Optional[str]:
    """
    Compara convergencia entre diferentes familias de instancias.
    
    Parámetros:
        results_dict: {familia: [lista_de_historiales]}
        family_names: Nombres de las familias para la leyenda
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize, dpi=dpi)
    axes = axes.flatten()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for idx, (family, histories) in enumerate(results_dict.items()):
        if idx >= 4:
            break
        
        ax = axes[idx]
        
        min_length = min(len(h) for h in histories)
        histories_aligned = [h[:min_length] for h in histories]
        histories_array = np.array(histories_aligned)
        
        mean_fitness = np.mean(histories_array, axis=0)
        std_fitness = np.std(histories_array, axis=0)
        iterations = np.arange(len(mean_fitness))
        
        # Todas las ejecuciones
        for hist in histories_aligned:
            ax.plot(iterations, hist, color='gray', alpha=0.1, linewidth=0.8)
        
        # Promedio
        ax.plot(iterations, mean_fitness,
               color=colors[idx], linewidth=2.5, marker='o', markersize=4)
        
        # Banda de desviación
        ax.fill_between(iterations,
                        mean_fitness - std_fitness,
                        mean_fitness + std_fitness,
                        color=colors[idx], alpha=0.2)
        
        ax.set_title(f"Familia: {family}", fontsize=11, fontweight='bold')
        ax.set_xlabel('Iteración', fontsize=10)
        ax.set_ylabel('Fitness', fontsize=10)
        ax.grid(True, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    # Ocultar subplots no utilizados
    for idx in range(len(results_dict), 4):
        axes[idx].set_visible(False)
    
    fig.suptitle(title, fontsize=14, fontweight='bold', y=0.995)
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
