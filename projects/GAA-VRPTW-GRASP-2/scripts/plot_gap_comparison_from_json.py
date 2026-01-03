"""
Generador de gráficos GAP basado en JSON
Lee gap_data.json y genera 5 gráficos comparativos de GAP
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

# Colores estándar
COLORS = {
    'algo1': '#FF6B6B',  # Rojo - GRASP Puro
    'algo2': '#4ECDC4',  # Verde/Turquesa - CONTROL
    'algo3': '#FFE66D',  # Amarillo - GRASP Adaptativo
}

LABELS = {
    'algo1': 'Algoritmo 1',
    'algo2': 'Algoritmo 2',
    'algo3': 'Algoritmo 3',
}


def load_gap_data(json_path: str) -> dict:
    """Carga datos de GAP desde JSON"""
    with open(json_path, 'r') as f:
        return json.load(f)


def create_dataframe_from_json(gap_data: dict) -> pd.DataFrame:
    """Convierte JSON de GAP a DataFrame para manipulación fácil"""
    rows = []
    
    for instance_id, instance_data in gap_data['instances'].items():
        for algo_key, algo_data in instance_data['algorithms'].items():
            rows.append({
                'instance': instance_id,
                'family': instance_data['family'],
                'algorithm': algo_key,
                'distance': algo_data['distance'],
                'gap_percent': algo_data['gap_percent'],
                'bks': instance_data['bks'],
            })
    
    return pd.DataFrame(rows)


def generate_gap_charts(json_path: str, output_dir: str):
    """Genera todos los gráficos de GAP"""
    
    json_path = Path(json_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[INFO] Cargando datos de GAP desde: {json_path}")
    gap_data = load_gap_data(str(json_path))
    
    print(f"[INFO] Generando gráficos en: {output_dir}")
    
    # Crear DataFrame
    df = create_dataframe_from_json(gap_data)
    
    # Ordenar instancias
    family_order = {'C1': 0, 'C2': 1, 'R1': 2, 'R2': 3, 'RC1': 4, 'RC2': 5}
    df['family_order'] = df['family'].map(family_order)
    df = df.sort_values(['family_order', 'instance']).reset_index(drop=True)
    
    instances = df['instance'].unique()
    
    # ============================================================
    # GRÁFICO 1: GAP por instancia (todas las 56)
    # ============================================================
    print("[INFO] Generando: 01_gap_comparison_all_instances.png")
    fig, ax = plt.subplots(figsize=(24, 8))
    
    x_pos = np.arange(len(instances))
    width = 0.25
    
    algo1_gaps = [df[(df['instance'] == inst) & (df['algorithm'] == 'algo1')]['gap_percent'].values[0] 
                  if any((df['instance'] == inst) & (df['algorithm'] == 'algo1')) else np.nan 
                  for inst in instances]
    algo2_gaps = [df[(df['instance'] == inst) & (df['algorithm'] == 'algo2')]['gap_percent'].values[0] 
                  if any((df['instance'] == inst) & (df['algorithm'] == 'algo2')) else np.nan 
                  for inst in instances]
    algo3_gaps = [df[(df['instance'] == inst) & (df['algorithm'] == 'algo3')]['gap_percent'].values[0] 
                  if any((df['instance'] == inst) & (df['algorithm'] == 'algo3')) else np.nan 
                  for inst in instances]
    
    ax.bar(x_pos - width, algo1_gaps, width, label='Algoritmo 1', alpha=0.8, color=COLORS['algo1'])
    ax.bar(x_pos, algo2_gaps, width, label='Algoritmo 2', alpha=0.8, color=COLORS['algo2'])
    ax.bar(x_pos + width, algo3_gaps, width, label='Algoritmo 3', alpha=0.8, color=COLORS['algo3'])
    
    # Línea en GAP=0 (BKS)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS (GAP=0)', alpha=0.7)
    
    ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
    ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación GAP: 3 Algoritmos vs Best Known Solutions\n56 Instancias Solomon', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    # Fondo alternado por familia
    unique_families = df.groupby('family_order').first()
    for i, (_, row) in enumerate(unique_families.iterrows()):
        family_instances = df[df['family'] == row['family']]['instance'].unique()
        start_idx = np.where(instances == family_instances[0])[0][0]
        end_idx = np.where(instances == family_instances[-1])[0][0]
        if i % 2 == 0:
            ax.axvspan(start_idx - 0.5, end_idx + 0.5, alpha=0.1, color='gray', zorder=0)
    
    plt.tight_layout()
    plt.savefig(output_dir / '01_gap_comparison_all_instances.png', dpi=300, bbox_inches='tight')
    print("[OK] Guardado: 01_gap_comparison_all_instances.png")
    plt.close()
    
    # ============================================================
    # GRÁFICO 2: Líneas de GAP
    # ============================================================
    print("[INFO] Generando: 02_gap_evolution_lines.png")
    fig, ax = plt.subplots(figsize=(24, 8))
    
    ax.plot(x_pos, algo1_gaps, 'o-', linewidth=2.5, markersize=6, 
            label='Algoritmo 1', color=COLORS['algo1'], alpha=0.8)
    ax.plot(x_pos, algo2_gaps, 's-', linewidth=2.5, markersize=6, 
            label='Algoritmo 2', color=COLORS['algo2'], alpha=0.8)
    ax.plot(x_pos, algo3_gaps, '^-', linewidth=2.5, markersize=6, 
            label='Algoritmo 3', color=COLORS['algo3'], alpha=0.8)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2.5, label='BKS (GAP=0)', alpha=0.7)
    
    ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
    ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
    ax.set_title('Evolución de GAP por Instancia: Comparación 3 Algoritmos\n56 Instancias Solomon', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(instances, rotation=45, ha='right')
    ax.legend(fontsize=11, loc='upper left', framealpha=0.95)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '02_gap_evolution_lines.png', dpi=300, bbox_inches='tight')
    print("[OK] Guardado: 02_gap_evolution_lines.png")
    plt.close()
    
    # ============================================================
    # GRÁFICO 3: Boxplot de GAP por familia
    # ============================================================
    print("[INFO] Generando: 03_gap_boxplot_by_family.png")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    families = sorted(df['family'].unique(), key=lambda x: family_order.get(x, 999))
    positions = np.arange(len(families))
    width = 0.25
    
    gap_data_algo1 = [df[(df['family'] == fam) & (df['algorithm'] == 'algo1')]['gap_percent'].dropna().values 
                      for fam in families]
    gap_data_algo2 = [df[(df['family'] == fam) & (df['algorithm'] == 'algo2')]['gap_percent'].dropna().values 
                      for fam in families]
    gap_data_algo3 = [df[(df['family'] == fam) & (df['algorithm'] == 'algo3')]['gap_percent'].dropna().values 
                      for fam in families]
    
    bp1 = ax.boxplot(gap_data_algo1, positions=positions - width, widths=width, 
                     patch_artist=True, label='Algoritmo 1')
    bp2 = ax.boxplot(gap_data_algo2, positions=positions, widths=width, 
                     patch_artist=True, label='Algoritmo 2')
    bp3 = ax.boxplot(gap_data_algo3, positions=positions + width, widths=width, 
                     patch_artist=True, label='Algoritmo 3')
    
    # Colorear boxplots
    for patch in bp1['boxes']:
        patch.set_facecolor(COLORS['algo1'])
        patch.set_alpha(0.7)
    for patch in bp2['boxes']:
        patch.set_facecolor(COLORS['algo2'])
        patch.set_alpha(0.7)
    for patch in bp3['boxes']:
        patch.set_facecolor(COLORS['algo3'])
        patch.set_alpha(0.7)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
    ax.set_xlabel('Familia Solomon', fontsize=12, fontweight='bold')
    ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
    ax.set_title('Distribución de GAP por Familia: 3 Algoritmos (Boxplot)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(positions)
    ax.set_xticklabels(families)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '03_gap_boxplot_by_family.png', dpi=300, bbox_inches='tight')
    print("[OK] Guardado: 03_gap_boxplot_by_family.png")
    plt.close()
    
    # ============================================================
    # GRÁFICO 4: Heatmap de GAP
    # ============================================================
    print("[INFO] Generando: 04_gap_heatmap.png")
    fig, ax = plt.subplots(figsize=(12, 16))
    
    # Crear matriz
    gap_matrix = pd.DataFrame({
        'Algo 1': [algo1_gaps[i] for i in range(len(instances))],
        'Algo 2': [algo2_gaps[i] for i in range(len(instances))],
        'Algo 3': [algo3_gaps[i] for i in range(len(instances))],
    }, index=instances)
    
    sns.heatmap(gap_matrix, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
                cbar_kws={'label': 'GAP a BKS (%)'}, ax=ax, linewidths=0.5, linecolor='gray')
    
    ax.set_title('Heatmap: GAP de cada Algoritmo vs Instancia\n(Rojo=Peor, Verde=Mejor)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    ax.set_ylabel('Instancia', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / '04_gap_heatmap.png', dpi=300, bbox_inches='tight')
    print("[OK] Guardado: 04_gap_heatmap.png")
    plt.close()
    
    # ============================================================
    # GRÁFICO 5: Grid de GAP por familia
    # ============================================================
    print("[INFO] Generando: 05_gap_by_family_grid.png")
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    for idx, family in enumerate(['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']):
        family_data = df[df['family'] == family]
        family_instances = family_data['instance'].unique()
        
        family_algo1 = [family_data[(family_data['instance'] == inst) & (family_data['algorithm'] == 'algo1')]['gap_percent'].values[0] 
                       if any((family_data['instance'] == inst) & (family_data['algorithm'] == 'algo1')) else np.nan 
                       for inst in family_instances]
        family_algo2 = [family_data[(family_data['instance'] == inst) & (family_data['algorithm'] == 'algo2')]['gap_percent'].values[0] 
                       if any((family_data['instance'] == inst) & (family_data['algorithm'] == 'algo2')) else np.nan 
                       for inst in family_instances]
        family_algo3 = [family_data[(family_data['instance'] == inst) & (family_data['algorithm'] == 'algo3')]['gap_percent'].values[0] 
                       if any((family_data['instance'] == inst) & (family_data['algorithm'] == 'algo3')) else np.nan 
                       for inst in family_instances]
        
        x = np.arange(len(family_instances))
        width = 0.25
        
        ax = axes[idx]
        ax.bar(x - width, family_algo1, width, label='Algo 1', color=COLORS['algo1'], alpha=0.8)
        ax.bar(x, family_algo2, width, label='Algo 2', color=COLORS['algo2'], alpha=0.8)
        ax.bar(x + width, family_algo3, width, label='Algo 3', color=COLORS['algo3'], alpha=0.8)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.set_title(f'Familia {family} ({len(family_instances)} instancias)', fontsize=11, fontweight='bold')
        ax.set_xlabel('Instancia', fontsize=10)
        ax.set_ylabel('GAP (%)', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels([inst.replace(family, '') for inst in family_instances], rotation=45)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=9)
    
    plt.suptitle('Comparación de GAP por Familia Solomon VRPTW', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(output_dir / '05_gap_by_family_grid.png', dpi=300, bbox_inches='tight')
    print("[OK] Guardado: 05_gap_by_family_grid.png")
    plt.close()
    
    # ============================================================
    # Imprimir tabla resumen
    # ============================================================
    print("\n" + "="*80)
    print("RESUMEN ESTADÍSTICO DE GAP POR ALGORITMO")
    print("="*80)
    
    summary_stats = []
    for algo_num in ['1', '2', '3']:
        stats = gap_data['summary_by_algorithm'].get(algo_num, {})
        summary_stats.append({
            f'Algoritmo {algo_num}': [
                f"{stats.get('avg_gap', 'N/A'):.2f}" if isinstance(stats.get('avg_gap'), (int, float)) else 'N/A',
                f"{stats.get('std_gap', 'N/A'):.2f}" if isinstance(stats.get('std_gap'), (int, float)) else 'N/A',
                f"{stats.get('min_gap', 'N/A'):.2f}" if isinstance(stats.get('min_gap'), (int, float)) else 'N/A',
                f"{stats.get('max_gap', 'N/A'):.2f}" if isinstance(stats.get('max_gap'), (int, float)) else 'N/A',
                f"{stats.get('avg_distance', 'N/A'):.2f}" if isinstance(stats.get('avg_distance'), (int, float)) else 'N/A',
            ]
        })
    
    summary_df = pd.DataFrame(
        [[row[f'Algoritmo {i+1}'][j] for i in range(3)] for j in range(5)],
        index=['Promedio GAP (%)', 'Desv. Estándar GAP', 'Min GAP (%)', 'Max GAP (%)', 'Promedio Distancia'],
        columns=[f'Algo{i}' for i in [1, 2, 3]]
    )
    print(summary_df.to_string())
    
    print("\n" + "="*80)
    print(f"[OK] Gráficos generados en: {output_dir}")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python plot_gap_comparison_from_json.py <ruta_json> [ruta_output]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(Path(json_path).parent.parent / 'plots')
    
    generate_gap_charts(json_path, output_path)
