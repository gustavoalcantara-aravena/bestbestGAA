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

# Colores para 5 algoritmos
COLORS_5 = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#1f77b4']
ALGO_NAMES = ['Algoritmo 0', 'Algoritmo 1', 'Algoritmo 2', 'Algoritmo 3', 'Algoritmo 4']

def create_visualizations_set2(results_file, output_dir):
    """Crear visualizaciones set 2 (11-18)"""
    
    # Cargar datos
    results = load_results(results_file)
    bks_data = load_bks()
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generando visualizaciones set 2 en: {output_path}")
    
    # 11 - Comparación: Vehículos BKS vs Utilizados
    print("11 - Comparación Vehículos BKS vs Utilizados...")
    fig, ax = plt.subplots(figsize=(14, 6))
    
    instances = sorted([inst for inst in bks_data.keys() if inst in [r['instance_id'] for r in results]])
    x = np.arange(len(instances))
    width = 0.12
    
    # BKS
    bks_vehicles = [bks_data[inst]['vehicles'] for inst in instances]
    ax.bar(x - 2.4*width, bks_vehicles, width, label='BKS', color='#2ecc71')
    
    # Algoritmos
    for algo in range(5):
        algo_vehicles = []
        for inst in instances:
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                algo_vehicles.append(algo_results[0]['vehicles'])
            else:
                algo_vehicles.append(0)
        
        ax.bar(x + (algo - 2)*width, algo_vehicles, width, label=ALGO_NAMES[algo], color=COLORS_5[algo])
    
    ax.set_xlabel('Instancia', fontsize=11, fontweight='bold')
    ax.set_ylabel('Número de Vehículos', fontsize=11, fontweight='bold')
    ax.set_title('11 - Comparación: Vehículos BKS vs Utilizados por cada Algoritmo', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '11-vehicles_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] 11-vehicles_comparison.png")
    
    # 12 - Comparación: Distancia BKS vs Lograda
    print("12 - Comparación Distancia BKS vs Lograda...")
    fig, ax = plt.subplots(figsize=(14, 6))
    
    bks_distances = [bks_data[inst]['distance'] for inst in instances]
    ax.bar(x - 2.4*width, bks_distances, width, label='BKS', color='#2ecc71')
    
    for algo in range(5):
        algo_distances = []
        for inst in instances:
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                algo_distances.append(algo_results[0]['distance'])
            else:
                algo_distances.append(0)
        
        ax.bar(x + (algo - 2)*width, algo_distances, width, label=ALGO_NAMES[algo], color=COLORS_5[algo])
    
    ax.set_xlabel('Instancia', fontsize=11, fontweight='bold')
    ax.set_ylabel('Distancia (km)', fontsize=11, fontweight='bold')
    ax.set_title('12 - Comparación: Distancia BKS vs Distancia Total Lograda por cada Algoritmo', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '12-distance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] 12-distance_comparison.png")
    
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
    print("[OK] 13-performance_heatmap.png")
    
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
    print("[OK] 14-pareto_multiobjective.png")
    
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
    print("[OK] 15-robustness_analysis.png")
    
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
    print("[OK] 16-feasibility_rate.png")
    
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
    print("[OK] 17-solved_unsolved.png")
    
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
            # Métrica 1: Distancia promedio (normalizada invertida: mejor = cercano a 1)
            avg_dist = np.mean([r['distance'] for r in algo_results])
            norm_dist = 1 - ((avg_dist - min_dist) / (max_dist - min_dist + 0.01))
            
            # Métrica 2: Eficiencia (tasa de instancias con pocos vehículos)
            avg_vehicles = np.mean([r['vehicles'] for r in algo_results])
            # Asumir K mínimo = 3, máximo = 20
            efficiency = 1 - ((avg_vehicles - 3) / (20 - 3))
            
            # Métrica 3: Consistencia (inverso de desviación estándar normalizada)
            consistency = 1 / (1 + np.std([r['distance'] for r in algo_results]) / (np.mean([r['distance'] for r in algo_results]) + 0.01))
            
            metrics.append([norm_dist, efficiency, consistency])
            algo_labels.append(ALGO_NAMES[algo])
    
    if metrics:
        angles = np.linspace(0, 2 * np.pi, 3, endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for idx, (metric, label, color) in enumerate(zip(metrics, algo_labels, COLORS_5[:len(metrics)])):
            values = metric + metric[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=label, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(['Distance', 'Efficiency', 'Consistency'], fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.grid(True)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
        ax.set_title('18 - Algorithm Comparison: Multi-Dimensional Radar', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path / '18-radar_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] 18-radar_chart.png")
    
    print("\n[OK] Todas las visualizaciones set 2 generadas exitosamente!")
    print(f"Ubicación: {output_path}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python generate_extra_visualizations_set2.py <run_directory>")
        sys.exit(1)
    
    run_dir = sys.argv[1]
    results_file = Path(run_dir) / 'canary_results.json'
    
    if not results_file.exists():
        print(f"Error: No se encontró {results_file}")
        sys.exit(1)
    
    output_dir = Path(run_dir) / 'visualizations'
    create_visualizations_set2(str(results_file), str(output_dir))
