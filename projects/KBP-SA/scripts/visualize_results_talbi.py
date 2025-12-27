#!/usr/bin/env python3
"""
Visualizaciones Según Talbi (2009)
Genera boxplots, histogramas y gráficos de distribución
"""

import sys
import csv
from pathlib import Path
import numpy as np
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')  # Sin display
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib no disponible. Instalar con: pip3 install matplotlib")


def load_data(csv_file: Path):
    """Carga datos del CSV"""
    runs = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['execution_status'] == 'success':
                try:
                    runs.append({
                        'time': float(row['time_total']),
                        'constructor': row['constructor_type'],
                        'operators': row['operator_types'].split(',') if row['operator_types'] else [],
                        'acceptance': row['acceptance_criterion'] or 'None',
                        'complexity': float(row['complexity_score']) if row['complexity_score'] else None,
                    })
                except:
                    continue
    return runs


def generate_visualizations(csv_file: Path, output_dir: Path):
    """Genera todas las visualizaciones según Talbi (2009)"""

    if not HAS_MATPLOTLIB:
        print("❌ No se puede generar visualizaciones sin matplotlib")
        return

    print("=" * 80)
    print("GENERANDO VISUALIZACIONES SEGÚN TALBI (2009)")
    print("=" * 80)
    print()

    runs = load_data(csv_file)
    if not runs:
        print("❌ No hay datos para visualizar")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    times = [r['time'] for r in runs]

    # 1. HISTOGRAMA DE DISTRIBUCIÓN DE TIEMPOS
    print("📊 Generando histograma de distribución...")
    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(np.mean(times), color='red', linestyle='--', linewidth=2, label=f'Media: {np.mean(times):.1f}s')
    plt.axvline(np.median(times), color='green', linestyle='--', linewidth=2, label=f'Mediana: {np.median(times):.1f}s')
    plt.xlabel('Tiempo de Ejecución (s)', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.title('Distribución de Tiempos de Ejecución', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'distribution_times.png', dpi=300)
    plt.close()
    print(f"   ✅ {output_dir / 'distribution_times.png'}")

    # 2. BOXPLOT POR CATEGORÍA DE VELOCIDAD
    print("📊 Generando boxplot por categoría...")
    fast = [r['time'] for r in runs if r['time'] <= 40]
    medium = [r['time'] for r in runs if 40 < r['time'] <= 100]
    slow = [r['time'] for r in runs if r['time'] > 100]

    plt.figure(figsize=(10, 6))
    data_to_plot = []
    labels = []
    if fast:
        data_to_plot.append(fast)
        labels.append(f'RÁPIDAS\n(≤40s)\nn={len(fast)}')
    if medium:
        data_to_plot.append(medium)
        labels.append(f'MEDIAS\n(40-100s)\nn={len(medium)}')
    if slow:
        data_to_plot.append(slow)
        labels.append(f'LENTAS\n(>100s)\nn={len(slow)}')

    bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
    colors = ['lightgreen', 'yellow', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors[:len(data_to_plot)]):
        patch.set_facecolor(color)

    plt.ylabel('Tiempo de Ejecución (s)', fontsize=12)
    plt.title('Distribución de Tiempos por Categoría', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / 'boxplot_categories.png', dpi=300)
    plt.close()
    print(f"   ✅ {output_dir / 'boxplot_categories.png'}")

    # 3. BOXPLOT POR CONSTRUCTOR
    print("📊 Generando boxplot por constructor...")
    by_constructor = defaultdict(list)
    for r in runs:
        by_constructor[r['constructor']].append(r['time'])

    # Filtrar constructores con suficientes muestras
    constructors_data = {k: v for k, v in by_constructor.items() if len(v) >= 5}

    if len(constructors_data) >= 2:
        plt.figure(figsize=(12, 6))
        sorted_constructors = sorted(constructors_data.items(), key=lambda x: np.median(x[1]))
        data_to_plot = [data for _, data in sorted_constructors]
        labels = [f'{name}\n(n={len(data)})' for name, data in sorted_constructors]

        bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')

        plt.ylabel('Tiempo de Ejecución (s)', fontsize=12)
        plt.title('Distribución de Tiempos por Constructor', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_dir / 'boxplot_constructors.png', dpi=300)
        plt.close()
        print(f"   ✅ {output_dir / 'boxplot_constructors.png'}")

    # 4. BOXPLOT POR OPERADOR
    print("📊 Generando boxplot por operador...")
    by_operator = defaultdict(list)
    for r in runs:
        for op in r['operators']:
            if op:
                by_operator[op].append(r['time'])

    operators_data = {k: v for k, v in by_operator.items() if len(v) >= 5}

    if len(operators_data) >= 2:
        plt.figure(figsize=(12, 6))
        sorted_operators = sorted(operators_data.items(), key=lambda x: np.median(x[1]))
        data_to_plot = [data for _, data in sorted_operators]
        labels = [f'{name}\n(n={len(data)})' for name, data in sorted_operators]

        bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightyellow')

        plt.ylabel('Tiempo de Ejecución (s)', fontsize=12)
        plt.title('Distribución de Tiempos por Operador', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_dir / 'boxplot_operators.png', dpi=300)
        plt.close()
        print(f"   ✅ {output_dir / 'boxplot_operators.png'}")

    # 5. SCATTER PLOT: COMPLEJIDAD vs TIEMPO
    print("📊 Generando scatter plot complejidad vs tiempo...")
    complexities = [r['complexity'] for r in runs if r['complexity'] is not None]
    times_with_complexity = [r['time'] for r in runs if r['complexity'] is not None]

    if len(complexities) >= 10:
        plt.figure(figsize=(10, 6))
        plt.scatter(complexities, times_with_complexity, alpha=0.5)

        # Línea de tendencia
        z = np.polyfit(complexities, times_with_complexity, 1)
        p = np.poly1d(z)
        plt.plot(complexities, p(complexities), "r--", alpha=0.8, label=f'Tendencia: y={z[0]:.2f}x+{z[1]:.2f}')

        plt.xlabel('Score de Complejidad', fontsize=12)
        plt.ylabel('Tiempo de Ejecución (s)', fontsize=12)
        plt.title('Relación entre Complejidad y Tiempo de Ejecución', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / 'scatter_complexity_time.png', dpi=300)
        plt.close()
        print(f"   ✅ {output_dir / 'scatter_complexity_time.png'}")

    # 6. GRÁFICO DE BARRAS: FRECUENCIA POR CATEGORÍA
    print("📊 Generando gráfico de frecuencias...")
    plt.figure(figsize=(10, 6))
    categories = ['RÁPIDAS\n(≤40s)', 'MEDIAS\n(40-100s)', 'LENTAS\n(>100s)']
    counts = [len(fast), len(medium), len(slow)]
    colors_bar = ['green', 'orange', 'red']

    bars = plt.bar(categories, counts, color=colors_bar, alpha=0.7, edgecolor='black')

    # Agregar porcentajes
    total = sum(counts)
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({count/total*100:.1f}%)',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.ylabel('Número de Corridas', fontsize=12)
    plt.title('Distribución de Corridas por Categoría de Velocidad', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / 'frequency_categories.png', dpi=300)
    plt.close()
    print(f"   ✅ {output_dir / 'frequency_categories.png'}")

    print()
    print("=" * 80)
    print(f"✅ Visualizaciones generadas en: {output_dir}")
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 visualize_results_talbi.py <archivo.csv>")
        return 1

    csv_file = Path(sys.argv[1])
    if not csv_file.exists():
        print(f"❌ Archivo no encontrado: {csv_file}")
        return 1

    output_dir = csv_file.parent / 'visualizations'
    generate_visualizations(csv_file, output_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
