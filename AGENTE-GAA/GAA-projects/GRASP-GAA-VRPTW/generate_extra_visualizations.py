"""
Extra Visualizations for VRPTW Experiments
Genera 10 gráficos adicionales para análisis detallado de 5 algoritmos
Adaptados del documento graficos-extra.md
"""

import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict

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

def calculate_gaps(results, bks_data):
    """Calcular gaps por algoritmo e instancia"""
    gaps = defaultdict(lambda: defaultdict(list))
    distances = defaultdict(list)
    vehicles = defaultdict(list)
    
    for r in results:
        algo = r['algorithm_id']
        inst = r['instance_id']
        
        if inst in bks_data:
            bks = bks_data[inst]
            dist = r['distance']
            vehi = r['vehicles']
            
            # GAP de vehículos
            gap_v = ((vehi - bks['vehicles']) / bks['vehicles']) * 100
            gaps['vehicles'][algo].append(gap_v)
            
            # GAP de distancia (solo si V = V*)
            if vehi == bks['vehicles']:
                gap_d = ((dist - bks['distance']) / bks['distance']) * 100
                gaps['distance'][algo].append(gap_d)
            
            distances[algo].append(dist)
            vehicles[algo].append(vehi)
    
    return gaps, distances, vehicles

def setup_style():
    """Configurar estilo visual"""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#1f77b4']
    return colors

# Colores para 5 algoritmos
COLORS_5 = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#1f77b4']
ALGO_NAMES = ['Algoritmo 0', 'Algoritmo 1', 'Algoritmo 2', 'Algoritmo 3', 'Algoritmo 4']

def create_visualizations(results_file, output_dir):
    """Crear todas las visualizaciones"""
    
    # Cargar datos
    results = load_results(results_file)
    bks_data = load_bks()
    gaps, distances, vehicles = calculate_gaps(results, bks_data)
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generando visualizaciones en: {output_path}")
    
    # 01 - Comparación GAP por Instancia (Barras Agrupadas)
    print("01 - Comparación GAP vs BKS...")
    fig, ax = plt.subplots(figsize=(14, 6))
    
    instances = sorted([inst for inst in bks_data.keys() if inst in [r['instance_id'] for r in results]])
    x = np.arange(len(instances))
    width = 0.15
    
    for algo in range(5):
        gap_values = []
        for inst in instances:
            # Encontrar gap para esta instancia y algoritmo
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                r = algo_results[0]
                bks = bks_data[inst]
                gap = ((r['vehicles'] - bks['vehicles']) / bks['vehicles']) * 100
                gap_values.append(gap)
            else:
                gap_values.append(0)
        
        ax.bar(x + algo * width, gap_values, width, label=ALGO_NAMES[algo], color=COLORS_5[algo])
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS')
    ax.set_xlabel('Instancia', fontsize=11, fontweight='bold')
    ax.set_ylabel('GAP (%)', fontsize=11, fontweight='bold')
    ax.set_title('01 - Comparación GAP: 5 Algoritmos vs Best Known Solutions', fontsize=13, fontweight='bold')
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / '01-gap_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 01-gap_comparison.png")
    
    # 02 - Distancia Promedio por Algoritmo
    print("02 - Performance: Distancia Promedio...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    avg_distances = [np.mean(distances[algo]) if algo in distances else 0 for algo in range(5)]
    bars = ax.bar(ALGO_NAMES, avg_distances, color=COLORS_5, width=0.6)
    
    # Valores encima de barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Distancia Promedio', fontsize=11, fontweight='bold')
    ax.set_title('02 - Performance Comparison: Distancia Promedio por Algoritmo', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path / '02-avg_distance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 02-avg_distance.png")
    
    # 03 - Distancia por Instancia (Líneas)
    print("03 - Distancia por Instancia...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    markers = ['o', 's', '^', 'D', 'v']
    for algo in range(5):
        dist_values = []
        for inst in instances:
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                dist_values.append(algo_results[0]['distance'])
            else:
                dist_values.append(np.nan)
        
        ax.plot(range(len(instances)), dist_values, marker=markers[algo], 
                color=COLORS_5[algo], label=ALGO_NAMES[algo], linewidth=2, markersize=8)
    
    ax.set_xlabel('Instancia', fontsize=11, fontweight='bold')
    ax.set_ylabel('Distancia', fontsize=11, fontweight='bold')
    ax.set_title('03 - Distance per Instance by Algorithm', fontsize=13, fontweight='bold')
    ax.set_xticks(range(len(instances)))
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / '03-distance_by_instance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 03-distance_by_instance.png")
    
    # 04 - Evolución de GAP por Instancia
    print("04 - Evolución de GAP...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for algo in range(5):
        gap_values = []
        for inst in instances:
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                r = algo_results[0]
                bks = bks_data[inst]
                gap = ((r['vehicles'] - bks['vehicles']) / bks['vehicles']) * 100
                gap_values.append(gap)
            else:
                gap_values.append(np.nan)
        
        ax.plot(range(len(instances)), gap_values, marker=markers[algo],
                color=COLORS_5[algo], label=ALGO_NAMES[algo], linewidth=2, markersize=8)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS')
    ax.set_xlabel('Instancia', fontsize=11, fontweight='bold')
    ax.set_ylabel('GAP (%)', fontsize=11, fontweight='bold')
    ax.set_title('04 - Evolución de GAP por Instancia', fontsize=13, fontweight='bold')
    ax.set_xticks(range(len(instances)))
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / '04-gap_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 04-gap_evolution.png")
    
    # 05 - Performance por Familia
    print("05 - Performance por Familia...")
    family_distances = defaultdict(list)
    for r in results:
        inst = r['instance_id']
        if inst in bks_data:
            family = bks_data[inst]['family']
            family_distances[family].append(r['distance'])
    
    families = sorted(family_distances.keys())
    avg_fam = [np.mean(family_distances[f]) for f in families]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(families, avg_fam, color='#9467bd', width=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Distancia Promedio', fontsize=11, fontweight='bold')
    ax.set_title('05 - Performance by Instance Family', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '05-performance_by_family.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 05-performance_by_family.png")
    
    # 06 - Distribución de GAP (Boxplot)
    print("06 - Distribución de GAP (Boxplot)...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    gap_data = []
    gap_labels = []
    for algo in range(5):
        algo_gaps = []
        for r in results:
            if r['algorithm_id'] == algo:
                inst = r['instance_id']
                if inst in bks_data:
                    bks = bks_data[inst]
                    gap = ((r['vehicles'] - bks['vehicles']) / bks['vehicles']) * 100
                    algo_gaps.append(gap)
        if algo_gaps:
            gap_data.append(algo_gaps)
            gap_labels.append(ALGO_NAMES[algo])
    
    bp = ax.boxplot(gap_data, labels=gap_labels, patch_artist=True, notch=True)
    for patch, color in zip(bp['boxes'], COLORS_5[:len(gap_data)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS')
    ax.set_ylabel('GAP (%)', fontsize=11, fontweight='bold')
    ax.set_title('06 - Distribución de GAP por Algoritmo', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '06-gap_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 06-gap_distribution.png")
    
    # 07 - Cantidad de Vehículos Promedio
    print("07 - Vehículos Promedio...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    avg_vehicles = [np.mean(vehicles[algo]) if algo in vehicles else 0 for algo in range(5)]
    bars = ax.bar(ALGO_NAMES, avg_vehicles, color=COLORS_5, width=0.6)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Vehículos Promedio', fontsize=11, fontweight='bold')
    ax.set_title('07 - Average Vehicles per Algorithm', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '07-avg_vehicles.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 07-avg_vehicles.png")
    
    # 08 - Heatmap: GAP por Algoritmo vs Instancia
    print("08 - Heatmap de GAP...")
    gap_matrix = []
    for inst in instances:
        row = []
        for algo in range(5):
            algo_results = [r for r in results if r['algorithm_id'] == algo and r['instance_id'] == inst]
            if algo_results:
                r = algo_results[0]
                bks = bks_data[inst]
                gap = ((r['vehicles'] - bks['vehicles']) / bks['vehicles']) * 100
                row.append(gap)
            else:
                row.append(0)
        gap_matrix.append(row)
    
    gap_matrix = np.array(gap_matrix)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(gap_matrix, xticklabels=ALGO_NAMES, yticklabels=instances,
                cmap='RdYlGn_r', annot=True, fmt='.1f', cbar_kws={'label': 'GAP (%)'},
                ax=ax, center=0)
    ax.set_title('08 - Heatmap: GAP de cada Algoritmo vs Instancia', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path / '08-gap_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 08-gap_heatmap.png")
    
    # 09 - Distribución de Distancias (Boxplot)
    print("09 - Distribución de Distancias...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    dist_data = [distances[algo] for algo in range(5) if algo in distances]
    bp = ax.boxplot(dist_data, labels=ALGO_NAMES, patch_artist=True, notch=True)
    for patch, color in zip(bp['boxes'], COLORS_5[:len(dist_data)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Distancia', fontsize=11, fontweight='bold')
    ax.set_title('09 - Distance Distribution by Algorithm', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path / '09-distance_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 09-distance_distribution.png")
    
    # 10 - Calidad Total (Scatter: Vehículos vs Distancia)
    print("10 - Análisis Pareto...")
    fig, ax = plt.subplots(figsize=(11, 7))
    
    for algo in range(5):
        algo_results = [r for r in results if r['algorithm_id'] == algo]
        if algo_results:
            v = [r['vehicles'] for r in algo_results]
            d = [r['distance'] for r in algo_results]
            ax.scatter(v, d, label=ALGO_NAMES[algo], color=COLORS_5[algo], 
                      s=150, alpha=0.7, edgecolors='black', linewidth=1.5)
    
    ax.set_xlabel('Número de Vehículos', fontsize=11, fontweight='bold')
    ax.set_ylabel('Distancia', fontsize=11, fontweight='bold')
    ax.set_title('10 - Análisis Pareto: Vehículos vs Distancia', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path / '10-pareto_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 10-pareto_analysis.png")
    
    print("\n✓ Todas las visualizaciones generadas exitosamente!")
    print(f"Ubicación: {output_path}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python generate_extra_visualizations.py <run_directory>")
        print("Ejemplo: python generate_extra_visualizations.py output/Canary_RUN_2026-01-04_02-21-05")
        sys.exit(1)
    
    run_dir = sys.argv[1]
    results_file = Path(run_dir) / 'canary_results.json'
    
    if not results_file.exists():
        print(f"Error: No se encontró {results_file}")
        sys.exit(1)
    
    output_dir = Path(run_dir) / 'visualizations'
    create_visualizations(str(results_file), str(output_dir))
