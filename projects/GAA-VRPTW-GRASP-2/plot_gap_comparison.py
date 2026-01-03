"""
Gráficos comparativos de GAP entre los 3 algoritmos
Muestra visualmente cómo cada algoritmo se desempeña vs BKS
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns
import glob
from datetime import datetime

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (20, 12)
plt.rcParams['font.size'] = 10

# BKS - Best Known Solutions (Solomon VRPTW)
BKS = {
    'C101': 828.94, 'C102': 828.94, 'C103': 828.94, 'C104': 828.94, 'C105': 828.94,
    'C106': 828.94, 'C107': 828.94, 'C108': 828.94, 'C109': 828.94,
    'C201': 589.86, 'C202': 589.86, 'C203': 589.86, 'C204': 589.86, 'C205': 589.86,
    'C206': 589.86, 'C207': 589.86, 'C208': 589.86,
    'R101': 1650.80, 'R102': 1486.12, 'R103': 1292.65, 'R104': 1109.80, 'R105': 1377.11,
    'R106': 1251.43, 'R107': 1104.28, 'R108': 960.88, 'R109': 1194.73, 'R110': 1118.60,
    'R111': 1096.72, 'R112': 948.14,
    'R201': 1252.37, 'R202': 1191.70, 'R203': 939.54, 'R204': 825.52, 'R205': 994.42,
    'R206': 906.14, 'R207': 890.60, 'R208': 726.82, 'R209': 909.23, 'R210': 939.40,
    'R211': 885.84,
    'RC101': 1696.94, 'RC102': 1554.75, 'RC103': 1460.99, 'RC104': 1357.04, 
    'RC105': 1629.44, 'RC106': 1446.43, 'RC107': 1371.16, 'RC108': 1117.75,
    'RC201': 1406.91, 'RC202': 1365.64, 'RC203': 1057.46, 'RC204': 798.46, 
    'RC205': 1297.65, 'RC206': 1143.32, 'RC207': 1061.14, 'RC208': 880.59,
}

# Buscar el archivo CSV más reciente en output/*/results/raw_results.csv
output_dir = Path('output')
csv_files = sorted(output_dir.glob('*/results/raw_results.csv'), key=lambda x: x.stat().st_mtime, reverse=True)

if not csv_files:
    print(f"Error: No se encontraron archivos raw_results.csv en {output_dir}")
    exit(1)

results_path = csv_files[0]
plots_dir = results_path.parent.parent / 'plots'
plots_dir.mkdir(exist_ok=True, parents=True)

print(f"📊 Cargando CSV más reciente: {results_path}")
print(f"📁 Guardando gráficas en: {plots_dir}\n")

raw_df = pd.read_csv(results_path)
print(f"Datos cargados: {len(raw_df)} filas")

# Calcular gap correctamente para algoritmo 3 (que tiene NaN)
raw_df['gap_calc'] = ((raw_df['d_final'] - raw_df['d_bks']) / raw_df['d_bks'] * 100)

# Pivot: cada instancia es una fila, cada algoritmo es una columna
df = raw_df.pivot_table(
    index='instance_id',
    columns='algorithm',
    values=['d_final', 'gap_calc'],
    aggfunc='first'
).reset_index()

# Aplanar columnas
df.columns = [f'{col[0]}_{col[1].replace("GAA_Algorithm_", "")}' if col[0] != 'instance_id' else col[1]
              for col in df.columns]
df = df.rename(columns={'': 'instance_id'})

# Renombrar columnas de forma clara
df.columns = ['instance' if 'instance_id' in c else c for c in df.columns]

# Extraer nombre de instancia
df = df.rename(columns={c: c.replace('d_final_', 'distance_algo').replace('gap_calc_', 'gap_algo') 
                        for c in df.columns if 'd_final' in c or 'gap_calc' in c})

# Limpiar estructura
df_clean = pd.DataFrame()
df_clean['instance'] = raw_df['instance_id'].unique()

for instance in df_clean['instance']:
    inst_data = raw_df[raw_df['instance_id'] == instance]
    for algo_num in [1, 2, 3]:
        algo_name = f'GAA_Algorithm_{algo_num}'
        algo_row = inst_data[inst_data['algorithm'] == algo_name]
        if not algo_row.empty:
            d_final = algo_row['d_final'].values[0]
            gap = ((d_final - algo_row['d_bks'].values[0]) / algo_row['d_bks'].values[0] * 100)
            
            if f'distance_algo{algo_num}' not in df_clean.columns:
                df_clean[f'distance_algo{algo_num}'] = 0.0
                df_clean[f'gap_algo{algo_num}'] = 0.0
            
            df_clean.loc[df_clean['instance'] == instance, f'distance_algo{algo_num}'] = d_final
            df_clean.loc[df_clean['instance'] == instance, f'gap_algo{algo_num}'] = gap

# Usar df_clean
df = df_clean.copy()

# Extraer familia
df['family'] = df['instance'].str.extract(r'([RC]+\d)')[0]

# Ordenar
family_order = {'C1': 0, 'C2': 1, 'R1': 2, 'R2': 3, 'RC1': 4, 'RC2': 5}
df['family_order'] = df['family'].map(family_order)
df = df.sort_values(['family_order', 'instance']).reset_index(drop=True)

print(f"\nInstancias por familia:")
print(df['family'].value_counts().sort_index())

# ============================================================
# GRÁFICO 1: GAP por instancia (todas las 56)
# ============================================================
fig, ax = plt.subplots(figsize=(24, 8))

x_pos = np.arange(len(df))
width = 0.25

bars1 = ax.bar(x_pos - width, df['gap_algo1'], width, label='Algoritmo 1', alpha=0.8, color='#FF6B6B')
bars2 = ax.bar(x_pos, df['gap_algo2'], width, label='Algoritmo 2', alpha=0.8, color='#4ECDC4')
bars3 = ax.bar(x_pos + width, df['gap_algo3'], width, label='Algoritmo 3', alpha=0.8, color='#FFE66D')

# Línea en GAP=0 (BKS)
ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)

ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparación GAP: 3 Algoritmos vs Best Known Solutions\n56 Instancias Solomon', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(df['instance'], rotation=45, ha='right')
ax.legend(fontsize=11, loc='upper left')
ax.grid(axis='y', alpha=0.3)

# Colorear fondo por familia
family_changes = df['family'].ne(df['family'].shift()).cumsum()
for i, (family, group) in enumerate(df.groupby('family')):
    group_indices = group.index
    if i % 2 == 0:
        ax.axvspan(group_indices[0] - 0.5, group_indices[-1] + 0.5, 
                   alpha=0.1, color='gray', zorder=0)

plt.tight_layout()
plt.savefig(plots_dir / '01_gap_comparison_all_instances.png', dpi=300, bbox_inches='tight')
print("[OK] Guardado: 01_gap_comparison_all_instances.png")
plt.close()

# ============================================================
# GRÁFICO 2: Líneas de GAP (56 instancias)
# ============================================================
fig, ax = plt.subplots(figsize=(24, 8))

ax.plot(x_pos, df['gap_algo1'], 'o-', linewidth=2.5, markersize=6, 
        label='Algoritmo 1', color='#FF6B6B', alpha=0.8)
ax.plot(x_pos, df['gap_algo2'], 's-', linewidth=2.5, markersize=6, 
        label='Algoritmo 2', color='#4ECDC4', alpha=0.8)
ax.plot(x_pos, df['gap_algo3'], '^-', linewidth=2.5, markersize=6, 
        label='Algoritmo 3', color='#FFE66D', alpha=0.8)

# BKS line
ax.axhline(y=0, color='red', linestyle='--', linewidth=2.5, label='BKS (GAP=0)', alpha=0.7)

ax.set_xlabel('Instancia (Solomon VRPTW)', fontsize=12, fontweight='bold')
ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
ax.set_title('Evolución de GAP por Instancia: Comparación 3 Algoritmos\n56 Instancias Solomon', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(df['instance'], rotation=45, ha='right')
ax.legend(fontsize=11, loc='upper left', framealpha=0.95)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(plots_dir / '02_gap_evolution_lines.png', dpi=300, bbox_inches='tight')
print("[OK] Guardado: 02_gap_evolution_lines.png")
plt.close()

# ============================================================
# GRÁFICO 3: GAP por familia (boxplots comparativos)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))

families = df['family'].unique()
positions = np.arange(len(families))
width = 0.25

gap_data_algo1 = [df[df['family'] == fam]['gap_algo1'].values for fam in families]
gap_data_algo2 = [df[df['family'] == fam]['gap_algo2'].values for fam in families]
gap_data_algo3 = [df[df['family'] == fam]['gap_algo3'].values for fam in families]

bp1 = ax.boxplot(gap_data_algo1, positions=positions - width, widths=width, 
                  patch_artist=True, label='Algoritmo 1')
bp2 = ax.boxplot(gap_data_algo2, positions=positions, widths=width, 
                  patch_artist=True, label='Algoritmo 2')
bp3 = ax.boxplot(gap_data_algo3, positions=positions + width, widths=width, 
                  patch_artist=True, label='Algoritmo 3')

# Colorear boxplots
for patch in bp1['boxes']:
    patch.set_facecolor('#FF6B6B')
    patch.set_alpha(0.7)
for patch in bp2['boxes']:
    patch.set_facecolor('#4ECDC4')
    patch.set_alpha(0.7)
for patch in bp3['boxes']:
    patch.set_facecolor('#FFE66D')
    patch.set_alpha(0.7)

ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='BKS', alpha=0.7)
ax.set_xlabel('Familia Solomon', fontsize=12, fontweight='bold')
ax.set_ylabel('GAP a BKS (%)', fontsize=12, fontweight='bold')
ax.set_title('Distribución de GAP por Familia: 3 Algoritmos\n(Boxplot)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(positions)
ax.set_xticklabels(families)
ax.legend(fontsize=11, loc='upper left')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(plots_dir / '03_gap_boxplot_by_family.png', dpi=300, bbox_inches='tight')
print("[OK] Guardado: 03_gap_boxplot_by_family.png")
plt.close()

# ============================================================
# GRÁFICO 4: Heatmap de GAP (instancias vs algoritmos)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 16))

# Crear matriz: instancias x algoritmos
gap_matrix = pd.DataFrame({
    'Algo 1': df['gap_algo1'].values,
    'Algo 2': df['gap_algo2'].values,
    'Algo 3': df['gap_algo3'].values,
}, index=df['instance'].values)

sns.heatmap(gap_matrix, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
            cbar_kws={'label': 'GAP a BKS (%)'}, ax=ax, linewidths=0.5, linecolor='gray')

ax.set_title('Heatmap: GAP de cada Algoritmo vs Instancia\n(Rojo=Peor, Verde=Mejor)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
ax.set_ylabel('Instancia', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(plots_dir / '04_gap_heatmap.png', dpi=300, bbox_inches='tight')
print("[OK] Guardado: 04_gap_heatmap.png")
plt.close()

# ============================================================
# GRÁFICO 5: Resumen estadístico por familia
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, family in enumerate(['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']):
    family_data = df[df['family'] == family]
    
    x = np.arange(len(family_data))
    width = 0.25
    
    ax = axes[idx]
    ax.bar(x - width, family_data['gap_algo1'], width, label='Algo 1', color='#FF6B6B', alpha=0.8)
    ax.bar(x, family_data['gap_algo2'], width, label='Algo 2', color='#4ECDC4', alpha=0.8)
    ax.bar(x + width, family_data['gap_algo3'], width, label='Algo 3', color='#FFE66D', alpha=0.8)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.set_title(f'Familia {family} ({len(family_data)} instancias)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Instancia', fontsize=10)
    ax.set_ylabel('GAP (%)', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(family_data['instance'].str.replace(f'{family}', ''), rotation=45)
    ax.grid(axis='y', alpha=0.3)
    ax.legend(fontsize=9)

plt.suptitle('Comparación de GAP por Familia Solomon VRPTW', 
             fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(plots_dir / '05_gap_by_family_grid.png', dpi=300, bbox_inches='tight')
print("[OK] Guardado: 05_gap_by_family_grid.png")
plt.close()

# ============================================================
# Tabla resumen de estadísticas
# ============================================================
print("\n" + "="*80)
print("RESUMEN ESTADÍSTICO DE GAP POR ALGORITMO")
print("="*80)

summary = pd.DataFrame({
    'Algoritmo 1': [
        df['gap_algo1'].mean(),
        df['gap_algo1'].median(),
        df['gap_algo1'].std(),
        df['gap_algo1'].min(),
        df['gap_algo1'].max(),
        (df['gap_algo1'] < 0).sum(),
        (df['gap_algo1'] < 5).sum(),
    ],
    'Algoritmo 2': [
        df['gap_algo2'].mean(),
        df['gap_algo2'].median(),
        df['gap_algo2'].std(),
        df['gap_algo2'].min(),
        df['gap_algo2'].max(),
        (df['gap_algo2'] < 0).sum(),
        (df['gap_algo2'] < 5).sum(),
    ],
    'Algoritmo 3': [
        df['gap_algo3'].mean(),
        df['gap_algo3'].median(),
        df['gap_algo3'].std(),
        df['gap_algo3'].min(),
        df['gap_algo3'].max(),
        (df['gap_algo3'] < 0).sum(),
        (df['gap_algo3'] < 5).sum(),
    ]
}, index=['Promedio GAP (%)', 'Mediana GAP (%)', 'Desv. Estándar', 
          'Min GAP (%)', 'Max GAP (%)', 'Instancias mejor que BKS', 'Instancias < 5% GAP'])

print(summary.round(2))

# Resumen por familia
print("\n" + "="*80)
print("RESUMEN POR FAMILIA")
print("="*80)

for family in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
    family_data = df[df['family'] == family]
    print(f"\n{family} ({len(family_data)} instancias):")
    print(f"  Algo 1: Promedio={family_data['gap_algo1'].mean():.2f}%, Mediana={family_data['gap_algo1'].median():.2f}%")
    print(f"  Algo 2: Promedio={family_data['gap_algo2'].mean():.2f}%, Mediana={family_data['gap_algo2'].median():.2f}%")
    print(f"  Algo 3: Promedio={family_data['gap_algo3'].mean():.2f}%, Mediana={family_data['gap_algo3'].median():.2f}%")
    
    # Mejor algoritmo
    means = [family_data['gap_algo1'].mean(), family_data['gap_algo2'].mean(), family_data['gap_algo3'].mean()]
    best_algo = np.argmin(means) + 1
    print(f"  ✅ MEJOR: Algoritmo {best_algo}")

print("\n" + "="*80)
print("Gráficos generados en: " + str(plots_dir))
print("="*80)
