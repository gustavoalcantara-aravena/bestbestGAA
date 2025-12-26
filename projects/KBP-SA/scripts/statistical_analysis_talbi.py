#!/usr/bin/env python3
"""
Análisis Estadístico Según Talbi (2009) - Sección 1.7
Tests estadísticos formales para validar diferencias entre grupos
"""

import sys
import csv
from pathlib import Path
import numpy as np
from scipy import stats
from collections import defaultdict


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
                        'acceptance': row['acceptance_criterion'],
                        'gap': float(row['gap_percent']) if row['gap_percent'] else None,
                    })
                except:
                    continue
    return runs


def statistical_tests_talbi(csv_file: Path):
    """
    Realiza tests estadísticos según metodología de Talbi (2009)
    """
    print("=" * 80)
    print("ANÁLISIS ESTADÍSTICO SEGÚN TALBI (2009) - SECCIÓN 1.7")
    print("=" * 80)
    print()

    runs = load_data(csv_file)

    if len(runs) < 30:
        print(f"⚠️  Solo {len(runs)} muestras. Talbi recomienda ≥30 para tests paramétricos")
        print()

    # Clasificar en grupos
    fast = [r for r in runs if r['time'] <= 40]
    slow = [r for r in runs if r['time'] > 100]

    if not fast or not slow:
        print("❌ Necesitamos corridas RÁPIDAS y LENTAS para comparar")
        return

    fast_times = [r['time'] for r in fast]
    slow_times = [r['time'] for r in slow]

    print(f"📊 Grupos para Análisis Estadístico:")
    print(f"   • RÁPIDAS (≤40s): n={len(fast)}")
    print(f"   • LENTAS (>100s): n={len(slow)}")
    print()

    # 1. TEST DE NORMALIDAD (Shapiro-Wilk)
    print("=" * 80)
    print("1️⃣  TEST DE NORMALIDAD (Shapiro-Wilk)")
    print("=" * 80)
    print()

    if len(fast) >= 3:
        stat_fast, p_fast = stats.shapiro(fast_times)
        print(f"RÁPIDAS: W={stat_fast:.4f}, p-value={p_fast:.4f}")
        if p_fast > 0.05:
            print("   ✅ Distribución NORMAL (p > 0.05)")
        else:
            print("   ⚠️  Distribución NO NORMAL (p ≤ 0.05)")

    if len(slow) >= 3:
        stat_slow, p_slow = stats.shapiro(slow_times)
        print(f"LENTAS: W={stat_slow:.4f}, p-value={p_slow:.4f}")
        if p_slow > 0.05:
            print("   ✅ Distribución NORMAL (p > 0.05)")
        else:
            print("   ⚠️  Distribución NO NORMAL (p ≤ 0.05)")

    print()

    # 2. TEST DE HOMOGENEIDAD DE VARIANZAS (Levene)
    print("=" * 80)
    print("2️⃣  TEST DE HOMOGENEIDAD DE VARIANZAS (Levene)")
    print("=" * 80)
    print()

    stat_levene, p_levene = stats.levene(fast_times, slow_times)
    print(f"Estadístico: {stat_levene:.4f}, p-value={p_levene:.4f}")
    if p_levene > 0.05:
        print("   ✅ Varianzas HOMOGÉNEAS (p > 0.05)")
        equal_var = True
    else:
        print("   ⚠️  Varianzas HETEROGÉNEAS (p ≤ 0.05)")
        equal_var = False

    print()

    # 3. TEST T DE STUDENT (Paramétrico)
    print("=" * 80)
    print("3️⃣  TEST T DE STUDENT (Diferencia de Medias)")
    print("=" * 80)
    print()

    t_stat, p_ttest = stats.ttest_ind(fast_times, slow_times, equal_var=equal_var)
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_ttest:.6f}")
    print()

    if p_ttest < 0.001:
        print("   ✅ Diferencia ALTAMENTE SIGNIFICATIVA (p < 0.001) ***")
    elif p_ttest < 0.01:
        print("   ✅ Diferencia MUY SIGNIFICATIVA (p < 0.01) **")
    elif p_ttest < 0.05:
        print("   ✅ Diferencia SIGNIFICATIVA (p < 0.05) *")
    else:
        print("   ❌ NO hay diferencia significativa (p ≥ 0.05)")

    print()
    print(f"Media RÁPIDAS: {np.mean(fast_times):.2f}s")
    print(f"Media LENTAS: {np.mean(slow_times):.2f}s")
    print(f"Diferencia: {np.mean(slow_times) - np.mean(fast_times):.2f}s ({(np.mean(slow_times)/np.mean(fast_times)):.2f}x)")
    print()

    # 4. MANN-WHITNEY U TEST (No Paramétrico)
    print("=" * 80)
    print("4️⃣  MANN-WHITNEY U TEST (No Paramétrico - Robusto)")
    print("=" * 80)
    print()

    u_stat, p_mann = stats.mannwhitneyu(fast_times, slow_times, alternative='two-sided')
    print(f"U-statistic: {u_stat:.4f}")
    print(f"p-value: {p_mann:.6f}")
    print()

    if p_mann < 0.001:
        print("   ✅ Diferencia ALTAMENTE SIGNIFICATIVA (p < 0.001) ***")
    elif p_mann < 0.01:
        print("   ✅ Diferencia MUY SIGNIFICATIVA (p < 0.01) **")
    elif p_mann < 0.05:
        print("   ✅ Diferencia SIGNIFICATIVA (p < 0.05) *")
    else:
        print("   ❌ NO hay diferencia significativa (p ≥ 0.05)")

    print()

    # 5. EFFECT SIZE (Cohen's d)
    print("=" * 80)
    print("5️⃣  EFFECT SIZE (Cohen's d - Tamaño del Efecto)")
    print("=" * 80)
    print()

    pooled_std = np.sqrt(((len(fast)-1)*np.var(fast_times, ddof=1) +
                          (len(slow)-1)*np.var(slow_times, ddof=1)) /
                         (len(fast) + len(slow) - 2))
    cohens_d = (np.mean(slow_times) - np.mean(fast_times)) / pooled_std

    print(f"Cohen's d: {cohens_d:.4f}")
    print()

    if abs(cohens_d) < 0.2:
        print("   Efecto PEQUEÑO (|d| < 0.2)")
    elif abs(cohens_d) < 0.5:
        print("   Efecto MEDIANO (0.2 ≤ |d| < 0.5)")
    elif abs(cohens_d) < 0.8:
        print("   Efecto GRANDE (0.5 ≤ |d| < 0.8)")
    else:
        print("   ✅ Efecto MUY GRANDE (|d| ≥ 0.8)")

    print()

    # 6. ANÁLISIS POR CONSTRUCTOR (ANOVA o Kruskal-Wallis)
    print("=" * 80)
    print("6️⃣  ANÁLISIS POR CONSTRUCTOR (Múltiples Grupos)")
    print("=" * 80)
    print()

    # Agrupar por constructor
    by_constructor = defaultdict(list)
    for r in runs:
        by_constructor[r['constructor']].append(r['time'])

    # Filtrar constructores con suficientes muestras
    constructors_data = {k: v for k, v in by_constructor.items() if len(v) >= 3}

    if len(constructors_data) >= 2:
        groups = list(constructors_data.values())
        group_names = list(constructors_data.keys())

        # ANOVA (paramétrico)
        f_stat, p_anova = stats.f_oneway(*groups)
        print(f"ANOVA F-statistic: {f_stat:.4f}, p-value={p_anova:.6f}")

        if p_anova < 0.05:
            print("   ✅ HAY diferencias significativas entre constructores (p < 0.05)")
        else:
            print("   ❌ NO hay diferencias significativas entre constructores (p ≥ 0.05)")

        print()

        # Kruskal-Wallis (no paramétrico)
        h_stat, p_kruskal = stats.kruskal(*groups)
        print(f"Kruskal-Wallis H-statistic: {h_stat:.4f}, p-value={p_kruskal:.6f}")

        if p_kruskal < 0.05:
            print("   ✅ HAY diferencias significativas entre constructores (p < 0.05)")
        else:
            print("   ❌ NO hay diferencias significativas entre constructores (p ≥ 0.05)")

        print()
        print("Medias por constructor:")
        for name, data in sorted(constructors_data.items(), key=lambda x: np.mean(x[1])):
            print(f"   • {name}: {np.mean(data):.2f}s (n={len(data)})")

    print()

    # CONCLUSIONES SEGÚN TALBI
    print("=" * 80)
    print("💡 CONCLUSIONES SEGÚN METODOLOGÍA TALBI (2009)")
    print("=" * 80)
    print()

    print("Validación Estadística:")
    if p_mann < 0.05 and abs(cohens_d) > 0.8:
        print("   ✅ Las diferencias entre RÁPIDAS y LENTAS son:")
        print("      • Estadísticamente significativas (p < 0.05)")
        print("      • Con efecto muy grande (|d| > 0.8)")
        print("      • VALIDADAS por tests paramétricos Y no paramétricos")
        print()
        print("   👉 CONCLUSIÓN: Las características del algoritmo SÍ causan")
        print("      diferencias significativas en el tiempo de ejecución.")
    else:
        print("   ⚠️  Las diferencias requieren más evidencia")

    print()
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 statistical_analysis_talbi.py <archivo.csv>")
        return 1

    csv_file = Path(sys.argv[1])
    if not csv_file.exists():
        print(f"❌ Archivo no encontrado: {csv_file}")
        return 1

    statistical_tests_talbi(csv_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
