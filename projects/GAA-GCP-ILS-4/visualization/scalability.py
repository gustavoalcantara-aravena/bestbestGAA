"""
visualization/scalability.py
Análisis de escalabilidad: |V| vs Tiempo/Iteraciones

Visualiza cómo el algoritmo escala con el tamaño de la instancia.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from scipy import stats


def plot_scalability_time(
    vertices: List[int],
    times: List[float],
    family_labels: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    title: str = "Escalabilidad: Tamaño vs Tiempo",
    figsize: tuple = (12, 7),
    dpi: int = 300,
    log_scale: bool = False
) -> Optional[str]:
    """
    Grafica el tiempo de ejecución vs número de vértices.
    
    Parámetros:
        vertices: Lista de tamaños de instancia (|V|)
        times: Lista de tiempos de ejecución
        family_labels: Etiquetas de familias (colores diferentes por familia)
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
        log_scale: Usar escala logarítmica en ambos ejes
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    if family_labels is None:
        family_labels = ['General'] * len(vertices)
    
    # Agrupar por familia
    families = {}
    for v, t, fam in zip(vertices, times, family_labels):
        if fam not in families:
            families[fam] = {'v': [], 't': []}
        families[fam]['v'].append(v)
        families[fam]['t'].append(t)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(families)))
    
    # Graficar por familia
    for (family, data), color in zip(families.items(), colors):
        v_sorted = np.array(sorted(zip(data['v'], data['t'])))
        ax.scatter(v_sorted[:, 0], v_sorted[:, 1], 
                  label=family, s=80, alpha=0.7, color=color)
        
        # Ajustar línea de tendencia
        if len(v_sorted) > 2:
            z = np.polyfit(v_sorted[:, 0], v_sorted[:, 1], 2)
            p = np.poly1d(z)
            v_fit = np.linspace(min(v_sorted[:, 0]), max(v_sorted[:, 0]), 100)
            ax.plot(v_fit, p(v_fit), color=color, linestyle='--', alpha=0.7, linewidth=1.5)
    
    if log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    ax.set_xlabel('Number of Vertices (|V|)', fontsize=12)
    ax.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.legend(loc='best', fontsize=10)
    
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


def plot_scalability_iterations(
    vertices: List[int],
    iterations: List[int],
    family_labels: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    title: str = "Escalabilidad: Tamaño vs Iteraciones",
    figsize: tuple = (12, 7),
    dpi: int = 300,
    log_scale: bool = False
) -> Optional[str]:
    """
    Grafica el número de iteraciones vs tamaño de instancia.
    
    Parámetros:
        vertices: Lista de tamaños de instancia (|V|)
        iterations: Lista de iteraciones requeridas
        family_labels: Etiquetas de familias
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
        log_scale: Usar escala logarítmica
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    if family_labels is None:
        family_labels = ['General'] * len(vertices)
    
    # Agrupar por familia
    families = {}
    for v, it, fam in zip(vertices, iterations, family_labels):
        if fam not in families:
            families[fam] = {'v': [], 'it': []}
        families[fam]['v'].append(v)
        families[fam]['it'].append(it)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(families)))
    
    # Graficar por familia
    for (family, data), color in zip(families.items(), colors):
        v_sorted = np.array(sorted(zip(data['v'], data['it'])))
        ax.scatter(v_sorted[:, 0], v_sorted[:, 1],
                  label=family, s=80, alpha=0.7, color=color)
        
        # Ajustar línea de tendencia
        if len(v_sorted) > 2:
            z = np.polyfit(v_sorted[:, 0], v_sorted[:, 1], 2)
            p = np.poly1d(z)
            v_fit = np.linspace(min(v_sorted[:, 0]), max(v_sorted[:, 0]), 100)
            ax.plot(v_fit, p(v_fit), color=color, linestyle='--', alpha=0.7, linewidth=1.5)
    
    if log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    ax.set_xlabel('Número de vértices (|V|)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Iteraciones requeridas', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.legend(loc='best', fontsize=10)
    
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


def plot_complexity_analysis(
    data: Dict[str, List[float]],
    output_path: Optional[str] = None,
    title: str = "Análisis de Complejidad",
    figsize: tuple = (14, 10),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica múltiples métricas de complejidad: tiempo, iteraciones, memoria.
    
    Parámetros:
        data: Dict con 'vertices', 'times', 'iterations' como listas
        output_path: Ruta para guardar
        title: Título
        figsize: Tamaño de figura
        dpi: Resolución
    
    Retorna:
        str: Ruta del archivo guardado
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize, dpi=dpi)
    
    vertices = np.array(data.get('vertices', []))
    times = np.array(data.get('times', []))
    iterations = np.array(data.get('iterations', []))
    
    # Subgráfica 1: Tiempo vs |V|
    ax = axes[0, 0]
    ax.scatter(vertices, times, alpha=0.6, s=80, color='#1f77b4')
    if len(vertices) > 2:
        z = np.polyfit(vertices, times, 2)
        p = np.poly1d(z)
        v_fit = np.linspace(min(vertices), max(vertices), 100)
        ax.plot(v_fit, p(v_fit), 'r--', alpha=0.7)
    ax.set_xlabel('|V|', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tiempo (s)', fontsize=11, fontweight='bold')
    ax.set_title('Tiempo de Ejecución vs Tamaño', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.2)
    
    # Subgráfica 2: Iteraciones vs |V|
    ax = axes[0, 1]
    ax.scatter(vertices, iterations, alpha=0.6, s=80, color='#ff7f0e')
    if len(vertices) > 2:
        z = np.polyfit(vertices, iterations, 2)
        p = np.poly1d(z)
        v_fit = np.linspace(min(vertices), max(vertices), 100)
        ax.plot(v_fit, p(v_fit), 'r--', alpha=0.7)
    ax.set_xlabel('|V|', fontsize=11, fontweight='bold')
    ax.set_ylabel('Iteraciones', fontsize=11, fontweight='bold')
    ax.set_title('Iteraciones vs Tamaño', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.2)
    
    # Subgráfica 3: Tiempo/Iteración vs |V|
    ax = axes[1, 0]
    time_per_iter = times / iterations
    ax.scatter(vertices, time_per_iter, alpha=0.6, s=80, color='#2ca02c')
    ax.set_xlabel('|V|', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tiempo/Iteración (s)', fontsize=11, fontweight='bold')
    ax.set_title('Eficiencia por Iteración', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.2)
    
    # Subgráfica 4: Escala logarítmica
    ax = axes[1, 1]
    ax.scatter(np.log(vertices), np.log(times), alpha=0.6, s=80, color='#d62728')
    if len(vertices) > 2:
        slope, intercept, r_value, _, _ = stats.linregress(np.log(vertices), np.log(times))
        v_fit = np.linspace(min(np.log(vertices)), max(np.log(vertices)), 100)
        ax.plot(v_fit, slope * v_fit + intercept, 'r--', alpha=0.7,
               label=f'O(|V|^{slope:.2f}), R²={r_value**2:.3f}')
        ax.legend(fontsize=9)
    ax.set_xlabel('log(|V|)', fontsize=11, fontweight='bold')
    ax.set_ylabel('log(Tiempo)', fontsize=11, fontweight='bold')
    ax.set_title('Análisis Logarítmico de Complejidad', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.2)
    
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
