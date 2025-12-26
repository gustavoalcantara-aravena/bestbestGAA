#!/usr/bin/env python3
"""
Script para analizar patrones de algoritmos y correlacionarlos con tiempos de ejecución
"""

import sys
import json
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


def parse_log_file(log_file: Path) -> dict:
    """
    Parsea un archivo de log para extraer algoritmos y tiempos

    Returns:
        Dict con información de algoritmos y tiempos
    """
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer algoritmos y pseudocódigo
    algorithms = {}

    # Buscar bloques de algoritmos
    # Formato: "✅ Algoritmo X generado\n   Pseudocódigo:\n       ..."
    pattern = r'✅ Algoritmo (\d+) generado\s+Pseudocódigo:\s+((?:.*\n?)+?)(?=✅|\n\n|  ✅)'
    matches = re.finditer(pattern, content, re.MULTILINE)

    for match in matches:
        algo_num = match.group(1)
        pseudocode = match.group(2).strip()
        algorithms[f'Algorithm_{algo_num}'] = pseudocode

    # Extraer tiempos por algoritmo
    # Formato: "× GAA_Algorithm_X (rep 1) ... ✅ valor=XXX, gap=X.XX%, tiempo=X.XXXs"
    time_pattern = r'× GAA_Algorithm_(\d+) \(rep \d+\).*?tiempo=([\d.]+)s'
    time_matches = re.findall(time_pattern, content)

    times_by_algorithm = {f'Algorithm_{i}': [] for i in range(1, 10)}
    for algo_num, time_str in time_matches:
        times_by_algorithm[f'Algorithm_{algo_num}'].append(float(time_str))

    # Contar timeouts
    timeout_pattern = r'× GAA_Algorithm_(\d+) \(rep \d+\).*?TIMEOUT'
    timeout_matches = re.findall(timeout_pattern, content)
    timeouts_by_algorithm = {f'Algorithm_{i}': 0 for i in range(1, 10)}
    for algo_num in timeout_matches:
        timeouts_by_algorithm[f'Algorithm_{algo_num}'] += 1

    return {
        'algorithms': algorithms,
        'times': times_by_algorithm,
        'timeouts': timeouts_by_algorithm
    }


def main():
    """Main analysis function"""

    print("=" * 80)
    print("ANÁLISIS DE PATRONES DE ALGORITMOS")
    print("=" * 80)
    print()

    analyzer = AlgorithmPatternAnalyzer()

    # Buscar archivos de log
    log_files = [
        project_root / 'output' / 'corrida_original_1.log',
        project_root / 'output' / 'corrida_original_2.log',
    ]

    execution_count = 0

    for log_file in log_files:
        if not log_file.exists():
            print(f"⚠️  Log file not found: {log_file}")
            continue

        execution_count += 1
        print(f"📄 Procesando: {log_file.name}")

        data = parse_log_file(log_file)

        # Agregar datos al analizador
        for algo_name, pseudocode in data['algorithms'].items():
            times = data['times'].get(algo_name, [])
            timeouts = data['timeouts'].get(algo_name, 0)

            if times or timeouts > 0:
                analyzer.add_observed_performance(
                    algorithm_name=f"{log_file.stem}_{algo_name}",
                    pseudocode=pseudocode,
                    experiment_times=times,
                    timeout_count=timeouts
                )

                # Mostrar análisis individual
                category, score, details = analyzer.predict_speed_category(pseudocode)

                print(f"\n  🔍 {algo_name}:")
                print(f"     Categoría: {category}")
                print(f"     Score de complejidad: {score:.2f}")
                print(f"     Tiempo estimado: {details['estimated_time_per_experiment']}")
                if times:
                    import numpy as np
                    print(f"     Tiempo real promedio: {np.mean(times):.3f}s")
                    print(f"     Tiempo real máximo: {np.max(times):.3f}s")
                if timeouts > 0:
                    print(f"     ⚠️  Timeouts: {timeouts}")
                print(f"     Constructor: {details['constructor']}")
                print(f"     Operadores: {', '.join(details['operators'])}")
                print(f"     Aceptación: {details['acceptance']}")

        print()

    if execution_count == 0:
        print("❌ No se encontraron archivos de log para analizar")
        return 1

    print("=" * 80)
    print("ANÁLISIS DE CORRELACIONES")
    print("=" * 80)
    print()

    # Generar reporte
    output_file = project_root / 'output' / 'pattern_analysis_report.md'
    analyzer.generate_report(str(output_file))

    print(f"✅ Reporte generado: {output_file}")
    print()

    # Mostrar correlaciones en consola
    correlations = analyzer.analyze_pattern_correlations()

    print("📊 CONSTRUCTORES (ordenados por velocidad):")
    for constructor, stats in sorted(correlations['constructors'].items(),
                                     key=lambda x: x[1]['avg']):
        print(f"   • {constructor:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")

    print()
    print("🔧 OPERADORES (ordenados por velocidad):")
    for operator, stats in sorted(correlations['operators'].items(),
                                  key=lambda x: x[1]['avg']):
        print(f"   • {operator:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")

    print()
    print("✅ CRITERIOS DE ACEPTACIÓN (ordenados por velocidad):")
    for acceptance, stats in sorted(correlations['acceptance'].items(),
                                    key=lambda x: x[1]['avg']):
        print(f"   • {acceptance:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")

    print()
    print("=" * 80)
    print("RECOMENDACIONES")
    print("=" * 80)
    print()

    # Identificar mejores combinaciones
    best_constructor = min(correlations['constructors'].items(), key=lambda x: x[1]['avg'])
    best_operator = min(correlations['operators'].items(), key=lambda x: x[1]['avg'])
    best_acceptance = min(correlations['acceptance'].items(), key=lambda x: x[1]['avg'])

    print("Para algoritmos RÁPIDOS, preferir:")
    print(f"   ✅ Constructor: {best_constructor[0]} ({best_constructor[1]['avg']:.3f}s)")
    print(f"   ✅ Operador: {best_operator[0]} ({best_operator[1]['avg']:.3f}s)")
    print(f"   ✅ Aceptación: {best_acceptance[0]} ({best_acceptance[1]['avg']:.3f}s)")
    print()

    # Identificar peores combinaciones
    worst_constructor = max(correlations['constructors'].items(), key=lambda x: x[1]['avg'])
    worst_operator = max(correlations['operators'].items(), key=lambda x: x[1]['avg'])
    worst_acceptance = max(correlations['acceptance'].items(), key=lambda x: x[1]['avg'])

    print("Para EVITAR algoritmos lentos, NO usar:")
    print(f"   ❌ Constructor: {worst_constructor[0]} ({worst_constructor[1]['avg']:.3f}s)")
    print(f"   ❌ Operador: {worst_operator[0]} ({worst_operator[1]['avg']:.3f}s)")
    print(f"   ❌ Aceptación: {worst_acceptance[0]} ({worst_acceptance[1]['avg']:.3f}s)")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
