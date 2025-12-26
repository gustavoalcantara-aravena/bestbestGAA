#!/usr/bin/env python3
"""
Análisis de Causas de Variabilidad
Objetivo: Descubrir por qué a veces se logran ~34 segundos y otras veces >100s
"""

import sys
import json
import csv
from pathlib import Path
from collections import defaultdict
import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


def analyze_csv_results(csv_file: Path):
    """Analiza resultados del CSV y encuentra causas de variabilidad"""

    print("=" * 80)
    print("ANÁLISIS DE CAUSAS DE VARIABILIDAD")
    print("=" * 80)
    print(f"\n📂 Archivo: {csv_file.name}\n")

    # Leer CSV
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
                        'acceptance': row['acceptance_criterion'],
                        'has_loop': row['has_loop'] == 'True',
                        'loop_budget': int(row['loop_budget']) if row['loop_budget'] else None,
                        'complexity': float(row['complexity_score']) if row['complexity_score'] else None,
                    })
                except:
                    continue

    if not runs:
        print("❌ No hay corridas exitosas para analizar")
        return

    # Estadísticas generales
    times = [r['time'] for r in runs]
    print(f"📊 Estadísticas Generales ({len(runs)} corridas exitosas)")
    print(f"   • Promedio: {np.mean(times):.1f}s")
    print(f"   • Mínimo: {np.min(times):.1f}s ⚡")
    print(f"   • Máximo: {np.max(times):.1f}s")
    print(f"   • Mediana: {np.median(times):.1f}s")
    print(f"   • Desv. Estándar: {np.std(times):.1f}s")
    print(f"   • Variabilidad: {(np.max(times)/np.min(times)):.1f}x")
    print()

    # Clasificar por velocidad
    # RÁPIDAS: ≤40s (cercanas al objetivo de 34s)
    # MEDIAS: 40-100s
    # LENTAS: >100s
    fast_runs = [r for r in runs if r['time'] <= 40]
    medium_runs = [r for r in runs if 40 < r['time'] <= 100]
    slow_runs = [r for r in runs if r['time'] > 100]

    print("📈 Distribución de Tiempos:")
    print(f"   • RÁPIDAS (≤40s): {len(fast_runs)} ({len(fast_runs)/len(runs)*100:.1f}%)")
    if fast_runs:
        fast_times = [r['time'] for r in fast_runs]
        print(f"     - Promedio: {np.mean(fast_times):.1f}s")
        print(f"     - Rango: {np.min(fast_times):.1f}s - {np.max(fast_times):.1f}s")

    print(f"   • MEDIAS (40-100s): {len(medium_runs)} ({len(medium_runs)/len(runs)*100:.1f}%)")
    if medium_runs:
        medium_times = [r['time'] for r in medium_runs]
        print(f"     - Promedio: {np.mean(medium_times):.1f}s")
        print(f"     - Rango: {np.min(medium_times):.1f}s - {np.max(medium_times):.1f}s")

    print(f"   • LENTAS (>100s): {len(slow_runs)} ({len(slow_runs)/len(runs)*100:.1f}%)")
    if slow_runs:
        slow_times = [r['time'] for r in slow_runs]
        print(f"     - Promedio: {np.mean(slow_times):.1f}s")
        print(f"     - Rango: {np.min(slow_times):.1f}s - {np.max(slow_times):.1f}s")
    print()

    # ANÁLISIS COMPARATIVO: RÁPIDAS vs LENTAS
    print("=" * 80)
    print("🔍 ANÁLISIS COMPARATIVO: RÁPIDAS vs LENTAS")
    print("=" * 80)
    print()

    if not fast_runs or not slow_runs:
        print("⚠️  Necesitamos tanto corridas RÁPIDAS como LENTAS para comparar")
        return

    # Comparar constructores
    print("1️⃣  CONSTRUCTORES")
    print("-" * 80)

    fast_constructors = defaultdict(int)
    for r in fast_runs:
        fast_constructors[r['constructor']] += 1

    slow_constructors = defaultdict(int)
    for r in slow_runs:
        slow_constructors[r['constructor']] += 1

    print("\nCorridas RÁPIDAS (≤40s):")
    for constructor, count in sorted(fast_constructors.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(fast_runs) * 100
        print(f"   • {constructor}: {count} veces ({pct:.1f}%)")

    print("\nCorridas LENTAS (>100s):")
    for constructor, count in sorted(slow_constructors.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(slow_runs) * 100
        print(f"   • {constructor}: {count} veces ({pct:.1f}%)")

    # Identificar constructor "ganador"
    if fast_constructors:
        best_fast = max(fast_constructors.items(), key=lambda x: x[1])
        print(f"\n✅ Constructor predominante en RÁPIDAS: {best_fast[0]} ({best_fast[1]}/{len(fast_runs)})")

    if slow_constructors:
        worst_slow = max(slow_constructors.items(), key=lambda x: x[1])
        print(f"❌ Constructor predominante en LENTAS: {worst_slow[0]} ({worst_slow[1]}/{len(slow_runs)})")

    print()

    # Comparar operadores
    print("2️⃣  OPERADORES")
    print("-" * 80)

    fast_operators = defaultdict(int)
    for r in fast_runs:
        for op in r['operators']:
            if op:
                fast_operators[op] += 1

    slow_operators = defaultdict(int)
    for r in slow_runs:
        for op in r['operators']:
            if op:
                slow_operators[op] += 1

    print("\nCorridas RÁPIDAS (≤40s):")
    for operator, count in sorted(fast_operators.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(fast_runs) * 100
        print(f"   • {operator}: {count} veces ({pct:.1f}%)")

    print("\nCorridas LENTAS (>100s):")
    for operator, count in sorted(slow_operators.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(slow_runs) * 100
        print(f"   • {operator}: {count} veces ({pct:.1f}%)")

    if fast_operators:
        best_fast_op = max(fast_operators.items(), key=lambda x: x[1])
        print(f"\n✅ Operador predominante en RÁPIDAS: {best_fast_op[0]} ({best_fast_op[1]}/{len(fast_runs)})")

    if slow_operators:
        worst_slow_op = max(slow_operators.items(), key=lambda x: x[1])
        print(f"❌ Operador predominante en LENTAS: {worst_slow_op[0]} ({worst_slow_op[1]}/{len(slow_runs)})")

    print()

    # Comparar criterios de aceptación
    print("3️⃣  CRITERIOS DE ACEPTACIÓN")
    print("-" * 80)

    fast_acceptance = defaultdict(int)
    for r in fast_runs:
        acc = r['acceptance'] or 'None'
        fast_acceptance[acc] += 1

    slow_acceptance = defaultdict(int)
    for r in slow_runs:
        acc = r['acceptance'] or 'None'
        slow_acceptance[acc] += 1

    print("\nCorridas RÁPIDAS (≤40s):")
    for acceptance, count in sorted(fast_acceptance.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(fast_runs) * 100
        print(f"   • {acceptance}: {count} veces ({pct:.1f}%)")

    print("\nCorridas LENTAS (>100s):")
    for acceptance, count in sorted(slow_acceptance.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(slow_runs) * 100
        print(f"   • {acceptance}: {count} veces ({pct:.1f}%)")

    print()

    # Comparar complejidad
    print("4️⃣  COMPLEJIDAD DE ALGORITMOS")
    print("-" * 80)

    fast_complexities = [r['complexity'] for r in fast_runs if r['complexity'] is not None]
    slow_complexities = [r['complexity'] for r in slow_runs if r['complexity'] is not None]

    if fast_complexities and slow_complexities:
        print(f"\nCorridas RÁPIDAS (≤40s):")
        print(f"   • Complejidad promedio: {np.mean(fast_complexities):.2f}")
        print(f"   • Rango: {np.min(fast_complexities):.2f} - {np.max(fast_complexities):.2f}")

        print(f"\nCorridas LENTAS (>100s):")
        print(f"   • Complejidad promedio: {np.mean(slow_complexities):.2f}")
        print(f"   • Rango: {np.min(slow_complexities):.2f} - {np.max(slow_complexities):.2f}")

        diff = np.mean(slow_complexities) / np.mean(fast_complexities)
        print(f"\n📊 Las corridas LENTAS tienen {diff:.1f}x más complejidad que las RÁPIDAS")

    print()

    # CONCLUSIONES
    print("=" * 80)
    print("💡 CONCLUSIONES Y CAUSAS DE VARIABILIDAD")
    print("=" * 80)
    print()

    print("Para lograr tiempos ≤40s (objetivo ~34s), preferir:")
    print()

    if fast_constructors:
        best = max(fast_constructors.items(), key=lambda x: x[1])
        print(f"   ✅ Constructor: {best[0]}")

    if fast_operators:
        best = max(fast_operators.items(), key=lambda x: x[1])
        print(f"   ✅ Operador: {best[0]}")

    if fast_acceptance:
        best = max(fast_acceptance.items(), key=lambda x: x[1])
        print(f"   ✅ Aceptación: {best[0]}")

    print()
    print("Para EVITAR tiempos >100s, NO usar:")
    print()

    if slow_constructors:
        worst = max(slow_constructors.items(), key=lambda x: x[1])
        print(f"   ❌ Constructor: {worst[0]}")

    if slow_operators:
        worst = max(slow_operators.items(), key=lambda x: x[1])
        print(f"   ❌ Operador: {worst[0]}")

    if slow_acceptance:
        worst = max(slow_acceptance.items(), key=lambda x: x[1])
        print(f"   ❌ Aceptación: {worst[0]}")

    print()
    print("=" * 80)


def main():
    """Función principal"""

    if len(sys.argv) < 2:
        print("Uso: python3 analyze_variability_causes.py <archivo.csv>")
        print()
        print("Ejemplo:")
        print("  python3 analyze_variability_causes.py output/3day_protocol/3day_protocol_*.csv")
        return 1

    csv_file = Path(sys.argv[1])

    if not csv_file.exists():
        print(f"❌ Archivo no encontrado: {csv_file}")
        return 1

    analyze_csv_results(csv_file)

    return 0


if __name__ == '__main__':
    sys.exit(main())
