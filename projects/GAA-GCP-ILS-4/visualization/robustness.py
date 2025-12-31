"""
visualization/robustness.py
Boxplots de robustez: Distribución estadística de resultados

Genera visualizaciones de la robustez del algoritmo en múltiples ejecuciones.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional


def plot_robustness(
    results: List[float],
    bks: Optional[float] = None,
    output_path: Optional[str] = None,
    instance_name: str = "Instance",
    title: str = "Robustez de ILS (30 ejecuciones)",
    figsize: tuple = (10, 6),
    dpi: int = 300
) -> Optional[str]:
    """
    Genera boxplot de robustez: distribución de resultados en múltiples ejecuciones.
    
    Parámetros:
        results: Lista de valores finales de fitness (30+ ejecuciones)
        bks: Best Known Solution (línea de referencia)
        output_path: Ruta para guardar la imagen
        instance_name: Nombre de la instancia
        title: Título de la gráfica
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    
    Ejemplo:
        >>> results = [45, 45, 46, 45, 46, 45, 47, 46, 45, 45]
        >>> plot_robustness(results, bks=45, output_path="robustness.png")
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Crear boxplot
    bp = ax.boxplot([results], 
                     vert=True, 
                     patch_artist=True,
                     widths=0.5,
                     showmeans=True,
                     meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
    
    # Colorear la caja
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    # Calcular estadísticas
    mean_val = np.mean(results)
    median_val = np.median(results)
    std_val = np.std(results)
    min_val = np.min(results)
    max_val = np.max(results)
    q1 = np.percentile(results, 25)
    q3 = np.percentile(results, 75)
    
    # Línea de BKS si está disponible
    if bks is not None:
        ax.axhline(y=bks, color='green', linestyle='--', linewidth=2, label=f'BKS = {bks}')
    
    ax.set_ylabel('Número de colores', fontsize=12, fontweight='bold')
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    ax.set_xticklabels([instance_name])
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    
    # Agregar estadísticas en texto
    stats_text = (
        f"Media: {mean_val:.2f}\n"
        f"Mediana: {median_val:.2f}\n"
        f"Desv. Est.: {std_val:.2f}\n"
        f"Min: {min_val:.0f}, Max: {max_val:.0f}\n"
        f"IQR: [{q1:.0f}, {q3:.0f}]"
    )
    
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    if bks:
        ax.legend(loc='upper left', fontsize=10)
    
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


def plot_multi_robustness(
    results_dict: Dict[str, List[float]],
    bks_dict: Optional[Dict[str, float]] = None,
    output_path: Optional[str] = None,
    title: str = "Comparación de Robustez",
    figsize: tuple = (14, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Compara robustez de múltiples instancias o algoritmos.
    
    Parámetros:
        results_dict: {nombre_instancia: [lista_de_resultados]}
        bks_dict: {nombre_instancia: valor_bks}
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    instances = list(results_dict.keys())
    data = [results_dict[inst] for inst in instances]
    
    bp = ax.boxplot(data, 
                    labels=instances,
                    patch_artist=True,
                    showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markersize=7))
    
    # Colorear cajas
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    # Líneas de BKS si están disponibles
    if bks_dict:
        for i, (inst, bks) in enumerate(bks_dict.items(), 1):
            ax.hlines(bks, i - 0.4, i + 0.4, colors='green', 
                     linestyle='--', linewidth=2, alpha=0.7)
    
    ax.set_ylabel('Número de colores', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    plt.xticks(rotation=45, ha='right')
    
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
