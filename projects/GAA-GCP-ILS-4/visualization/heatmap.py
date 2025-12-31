"""
visualization/heatmap.py
Heatmaps de conflictos: Visualización de matriz de conflictos

Muestra la matriz n×n de conflictos en la solución final.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple


def plot_conflict_heatmap(
    conflict_matrix: np.ndarray,
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Matriz de Conflictos",
    figsize: Optional[Tuple[int, int]] = None,
    dpi: int = 300,
    cmap: str = 'RdYlGn_r'
) -> Optional[str]:
    """
    Genera heatmap de la matriz de conflictos.
    
    Parámetros:
        conflict_matrix: Matriz n×n de conflictos (0 sin conflicto, 1 con conflicto)
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título del heatmap
        figsize: Tamaño de figura (si None, se calcula automáticamente)
        dpi: Resolución
        cmap: Mapa de colores
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> matrix = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        >>> plot_conflict_heatmap(matrix, output_path="conflicts.png")
    """
    n = conflict_matrix.shape[0]
    
    # Calcular tamaño automático si no se proporciona
    if figsize is None:
        size = max(6, min(14, n / 10))
        figsize = (size, size)
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Crear heatmap
    im = ax.imshow(conflict_matrix, cmap=cmap, aspect='auto', interpolation='nearest')
    
    # Etiquetas de ejes
    ax.set_xlabel('Vértice (j)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Vértice (i)', fontsize=11, fontweight='bold')
    ax.set_title(f"{title}\n{instance_name} (n={n})", fontsize=12, fontweight='bold', pad=15)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Conflicto', fontsize=10, fontweight='bold')
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Sin conflicto', 'Con conflicto'])
    
    # Configurar tics si es matriz pequeña
    if n <= 20:
        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.set_xticklabels(np.arange(n), fontsize=8)
        ax.set_yticklabels(np.arange(n), fontsize=8)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    else:
        # Para matrices grandes, mostrar menos tics
        step = max(1, n // 10)
        ax.set_xticks(np.arange(0, n, step))
        ax.set_yticks(np.arange(0, n, step))
        ax.set_xticklabels(np.arange(0, n, step), fontsize=8)
        ax.set_yticklabels(np.arange(0, n, step), fontsize=8)
    
    # Estadísticas
    num_conflicts = np.sum(conflict_matrix)
    total_edges = n * (n - 1) // 2
    conflict_ratio = num_conflicts / total_edges if total_edges > 0 else 0
    
    stats_text = (
        f"Conflictos: {int(num_conflicts)}\n"
        f"Total aristas: {total_edges}\n"
        f"Ratio: {conflict_ratio:.2%}"
    )
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
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


def plot_conflict_distribution(
    conflict_degree: List[int],
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Distribución de Conflictos por Vértice",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica la distribución del número de conflictos por vértice.
    
    Parámetros:
        conflict_degree: Lista con número de conflictos por vértice
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> degrees = [5, 3, 7, 2, 4, 6]
        >>> plot_conflict_distribution(degrees, output_path="conflict_dist.png")
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi)
    
    vertices = np.arange(len(conflict_degree))
    
    # Subgráfica 1: Gráfica de barras
    colors = plt.cm.RdYlGn_r(np.linspace(0, 1, len(conflict_degree)))
    bars = ax1.bar(vertices, conflict_degree, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('Vértice', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Número de conflictos', fontsize=11, fontweight='bold')
    ax1.set_title(f"Conflictos por Vértice\n{instance_name}", fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_axisbelow(True)
    
    # Subgráfica 2: Histograma de distribución
    ax2.hist(conflict_degree, bins=min(20, max(conflict_degree) - min(conflict_degree) + 1),
            color='#1f77b4', alpha=0.7, edgecolor='black')
    
    ax2.set_xlabel('Número de conflictos', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frecuencia (vértices)', fontsize=11, fontweight='bold')
    ax2.set_title('Distribución de Frecuencias', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_axisbelow(True)
    
    # Estadísticas
    mean_conflicts = np.mean(conflict_degree)
    std_conflicts = np.std(conflict_degree)
    max_conflicts = np.max(conflict_degree)
    min_conflicts = np.min(conflict_degree)
    
    stats_text = (
        f"Media: {mean_conflicts:.2f}\n"
        f"Desv. Est.: {std_conflicts:.2f}\n"
        f"Min: {min_conflicts}, Max: {max_conflicts}\n"
        f"Total: {sum(conflict_degree)}"
    )
    
    ax1.text(0.98, 0.97, stats_text, transform=ax1.transAxes,
            fontsize=9, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
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


def plot_conflict_statistics(
    conflict_matrices: List[np.ndarray],
    instance_name: str = "Instance",
    output_path: Optional[str] = None,
    title: str = "Análisis Estadístico de Conflictos",
    figsize: tuple = (14, 8),
    dpi: int = 300
) -> Optional[str]:
    """
    Analiza estadísticas de conflictos en múltiples soluciones.
    
    Parámetros:
        conflict_matrices: Lista de matrices de conflictos (múltiples ejecuciones)
        instance_name: Nombre de la instancia
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize, dpi=dpi)
    
    # Calcular métricas para cada matriz
    num_conflicts = [np.sum(m) for m in conflict_matrices]
    conflict_ratios = [np.sum(m) / (m.shape[0] * (m.shape[0] - 1) // 2) 
                       for m in conflict_matrices]
    
    # Subgráfica 1: Número de conflictos por ejecución
    ax = axes[0, 0]
    ax.bar(range(len(num_conflicts)), num_conflicts, color='#ff7f0e', alpha=0.7)
    ax.set_xlabel('Ejecución', fontsize=10, fontweight='bold')
    ax.set_ylabel('Número de conflictos', fontsize=10, fontweight='bold')
    ax.set_title('Conflictos por Ejecución', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Subgráfica 2: Distribución de conflictos
    ax = axes[0, 1]
    ax.boxplot([np.sum(m, axis=1) for m in conflict_matrices],
              labels=[f'Ej. {i}' for i in range(len(conflict_matrices))])
    ax.set_ylabel('Conflictos por vértice', fontsize=10, fontweight='bold')
    ax.set_title('Distribución de Conflictos', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Subgráfica 3: Ratios de conflicto
    ax = axes[1, 0]
    ax.bar(range(len(conflict_ratios)), conflict_ratios, color='#2ca02c', alpha=0.7)
    ax.set_xlabel('Ejecución', fontsize=10, fontweight='bold')
    ax.set_ylabel('Ratio de conflicto', fontsize=10, fontweight='bold')
    ax.set_title('Ratio de Conflicto (Conflictos/Total)', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Subgráfica 4: Heatmap promediado
    ax = axes[1, 1]
    avg_matrix = np.mean(conflict_matrices, axis=0)
    im = ax.imshow(avg_matrix, cmap='RdYlGn_r', aspect='auto', interpolation='nearest')
    ax.set_title('Matriz Promediada', fontsize=10, fontweight='bold')
    ax.set_xlabel('Vértice (j)', fontsize=9, fontweight='bold')
    ax.set_ylabel('Vértice (i)', fontsize=9, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Probabilidad de conflicto')
    
    fig.suptitle(f"{title}\n{instance_name}", fontsize=12, fontweight='bold')
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
