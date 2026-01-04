"""
Extra Visualizations Set 2 for VRPTW Experiments
Genera 8 gráficos adicionales (11-18) para análisis detallado de 5 algoritmos
Adaptados del documento grafiicos-extra-extra.md
"""

import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

def load_results(results_file):
    """Cargar resultados de experimento"""
    with open(results_file, 'r') as f:
        return json.load(f)

def load_bks():
    """Cargar Best Known Solutions"""
    bks_data = {}
    with open('03-data/best_known_solutions-Solomon-VRPTW-Dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instance = row['instance_id'].strip()
            bks_data[instance] = {
                'vehicles': int(row['k_bks']),
                'distance': float(row['d_bks']),
                'family': row['family']
            }
    return bks_data

# Colores para 5 algoritmos - Estilo similar a imagen de referencia
# Verde (similar a GAA_Algorithm_1), Rojo, Azul (similar a GAA_Algorithm_3), Turquesa, Naranja
COLORS_5 = ['#2ecc71', '#e74c3c', '#3498db', '#1abc9c', '#f39c12']  # Verde, Rojo, Azul, Turquesa, Naranja
ALGO_NAMES = ['Algoritmo 0', 'Algoritmo 1', 'Algoritmo 2', 'Algoritmo 3', 'Algoritmo 4']

def create_visualizations_set2(results_file, output_dir):
    """Crear visualizaciones set 2 (11-18)"""
    
    # Cargar datos
    results = load_results(results_file)
    bks_data = load_bks()
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generando visualizaciones set 2 en: {output_path}")
    
    # 11 - Comparación: Vehículos Promedio por Algoritmo
    print("11 - Comparación Vehículos Promedio...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calcular promedio de vehículos por algoritmo
    avg_vehicles = []
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            avg_vehicles.append(np.mean([r['vehicles'] for r in algo_results]))
        else:
            avg_vehicles.append(0)
    
    # Gráfico de barras
    bars = ax.bar(ALGO_NAMES, avg_vehicles, color=COLORS_5, width=0.6)
    
    # Valores encima de barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Número Promedio de Vehículos', fontsize=11, fontweight='bold')
    ax.set_title('11 - Performance Comparison: Vehículos Promedio por Algoritmo', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path / '11-vehicles_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 11-vehicles_comparison.png")
    
    # 12 - Comparación: Distancia BKS vs Lograda
    print("12 - Comparación Distancia BKS vs Lograda...")
    # 12 - Comparación: Distancia Promedio por Algoritmo
    print("12 - Comparación Distancia Promedio...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calcular promedio de distancia por algoritmo
    avg_distances = []
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            avg_distances.append(np.mean([r['distance'] for r in algo_results]))
        else:
            avg_distances.append(0)
    
    # Gráfico de barras
    bars = ax.bar(ALGO_NAMES, avg_distances, color=COLORS_5, width=0.6)
    
    # Valores encima de barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Distancia Promedio (km)', fontsize=11, fontweight='bold')
    ax.set_title('12 - Performance Comparison: Distancia Promedio por Algoritmo', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path / '12-distance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 12-distance_comparison.png")
    
    # 13 - Performance Heatmap: Distancia promedio por Familia y Algoritmo
    print("13 - Performance Heatmap...")
    
    family_algo_dist = defaultdict(lambda: defaultdict(list))
    for r in results:
        inst = r['instance_id']
        if inst in bks_data:
            family = bks_data[inst]['family']
            algo = r['algorithm_id']
            family_algo_dist[family][algo].append(r['distance'])
    
    families = sorted(family_algo_dist.keys())
    heatmap_data = []
    for family in families:
        row = []
        for algo in range(5):
            if algo in family_algo_dist[family]:
                avg_dist = np.mean(family_algo_dist[family][algo])
                row.append(avg_dist)
            else:
                row.append(np.nan)
        heatmap_data.append(row)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(np.array(heatmap_data), xticklabels=ALGO_NAMES, yticklabels=families,
                cmap='RdYlGn_r', annot=True, fmt='.1f', cbar_kws={'label': 'Distance (km)'},
                ax=ax)
    ax.set_title('13 - Performance Heatmap: Average Distance by Family and Algorithm', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path / '13-performance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 13-performance_heatmap.png")
    
    # 14 - Multi-Objective Analysis: K vs D
    print("14 - Multi-Objective Analysis (Pareto)...")
    fig, ax = plt.subplots(figsize=(11, 7))
    
    markers = ['o', 's', '^', 'D', 'v']
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            vehicles = [r['vehicles'] for r in algo_results]
            distances = [r['distance'] for r in algo_results]
            ax.scatter(vehicles, distances, label=ALGO_NAMES[algo], color=COLORS_5[algo],
                      marker=markers[algo], s=180, alpha=0.7, edgecolors='black', linewidth=1.5)
    
    ax.set_xlabel('Número de Vehículos (K)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Distancia Total (D)', fontsize=11, fontweight='bold')
    ax.set_title('14 - Multi-Objective Analysis: K vs D (Pareto Front)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / '14-pareto_multiobjective.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 14-pareto_multiobjective.png")
    
    # 15 - Robustness Analysis: Distribución por Instancia
    print("15 - Robustness Analysis...")
    
    # Tomar primeras instancias para visualizar
    instances_to_plot = instances[:min(6, len(instances))]
    n_instances = len(instances_to_plot)
    n_cols = 3
    n_rows = (n_instances + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4*n_rows))
    axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]
    
    for idx, inst in enumerate(instances_to_plot):
        ax = axes[idx]
        dist_data = []
        labels = []
        
        for algo in range(5):
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                dist_data.append([r['distance'] for r in algo_results])
                labels.append(f'A{algo}')
        
        if dist_data:
            bp = ax.boxplot(dist_data, labels=labels, patch_artist=True, notch=True)
            for patch, color in zip(bp['boxes'], COLORS_5[:len(dist_data)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel('Distance', fontsize=9)
            ax.set_title(f'Instance: {inst}', fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
    
    # Ocultar subplots vacíos
    for idx in range(n_instances, len(axes)):
        axes[idx].set_visible(False)
    
    fig.suptitle('15 - Robustness Analysis: Distance Distribution by Instance', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path / '15-robustness_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 15-robustness_analysis.png")
    
    # 16 - K_BKS Feasibility Rate
    print("16 - K_BKS Feasibility Rate...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    feasibility_rates = []
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            feasible_count = sum(1 for r in algo_results 
                               if r['instance_id'] in bks_data and 
                               r['vehicles'] == bks_data[r['instance_id']]['vehicles'])
            rate = (feasible_count / len(algo_results)) * 100
            feasibility_rates.append(rate)
        else:
            feasibility_rates.append(0)
    
    bars = ax.bar(ALGO_NAMES, feasibility_rates, color=COLORS_5, width=0.6)
    ax.axhline(y=100, color='red', linestyle='--', linewidth=2, label='100% Target')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Feasibility Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('16 - K_BKS Feasibility Rate by Algorithm', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 110)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '16-feasibility_rate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 16-feasibility_rate.png")
    
    # 17 - Solved vs Unsolved Instances
    print("17 - Solved vs Unsolved...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    solved = []
    unsolved = []
    
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            s_count = sum(1 for r in algo_results 
                         if r['instance_id'] in bks_data and 
                         r['vehicles'] == bks_data[r['instance_id']]['vehicles'])
            u_count = len(algo_results) - s_count
            solved.append(s_count)
            unsolved.append(u_count)
        else:
            solved.append(0)
            unsolved.append(0)
    
    x_pos = np.arange(len(ALGO_NAMES))
    bars1 = ax.bar(x_pos, solved, label='Solved (K=BKS)', color='#2ecc71', width=0.6)
    bars2 = ax.bar(x_pos, unsolved, bottom=solved, label='Unsolved (K>BKS)', color='#e74c3c', width=0.6)
    
    ax.set_ylabel('Number of Instances', fontsize=11, fontweight='bold')
    ax.set_title('17 - Solved vs Unsolved Instances', fontsize=13, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(ALGO_NAMES)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Valores totales encima
    for i, (s, u) in enumerate(zip(solved, unsolved)):
        ax.text(i, s + u, f'{s+u}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path / '17-solved_unsolved.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 17-solved_unsolved.png")
    
    # 18 - Radar Chart (Multi-Dimensional)
    print("18 - Radar Chart...")
    
    # Normalizar métricas
    all_distances = [r['distance'] for r in results]
    min_dist = min(all_distances) if all_distances else 1
    max_dist = max(all_distances) if all_distances else 1
    
    metrics = []
    algo_labels = []
    
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            # Métrica 1: Eficiencia de tiempo (inverso de distancia normalizada)
            avg_dist = np.mean([r['distance'] for r in algo_results])
            time_efficiency = 1 - ((avg_dist - min_dist) / (max_dist - min_dist + 0.01))
            
            # Métrica 2: Distancia promedio (normalizada invertida)
            avg_vehicles = np.mean([r['vehicles'] for r in algo_results])
            avg_distance_norm = 1 - ((avg_vehicles - 3) / (20 - 3))
            
            # Métrica 3: Consistencia (inverso de desviación estándar normalizada)
            consistency = 1 / (1 + np.std([r['distance'] for r in algo_results]) / (np.mean([r['distance'] for r in algo_results]) + 0.01))
            
            metrics.append([time_efficiency, avg_distance_norm, consistency])
            algo_labels.append(ALGO_NAMES[algo])
    
    if metrics:
        # Dimensiones del radar
        categories = ['Time Efficiency', 'Avg Distance', 'Consistency']
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for idx, (metric, label, color) in enumerate(zip(metrics, algo_labels, COLORS_5[:len(metrics)])):
            values = metric + metric[:1]
            ax.plot(angles, values, 'o-', linewidth=2.5, label=label, color=color, markersize=8)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=11, frameon=True, shadow=True)
        ax.set_title('Algorithm Comparison: Multi-Dimensional Radar', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path / '18-radar_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 18-radar_chart.png")
    
    print("\n✓ Todas las visualizaciones set 2 generadas exitosamente!")
    print(f"Ubicación: {output_path}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python generate_extra_visualizations_set2.py <run_directory>")
        sys.exit(1)
    
    try:
        run_dir = sys.argv[1]
        results_file = Path(run_dir) / 'canary_results.json'
        
        if not results_file.exists():
            print(f"Error: No se encontró {results_file}")
            sys.exit(1)
        
        output_dir = Path(run_dir) / 'visualizations'
        create_visualizations_set2(str(results_file), str(output_dir))
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
