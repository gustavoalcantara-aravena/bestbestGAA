#!/usr/bin/env python3
"""
Experimentación Masiva - KBP-SA
Objetivo: Ejecutar múltiples corridas de demo_experimentation_both.py
          para aprender qué patrones de algoritmos generan tiempos < 120s

Configuración:
- Timeout: 120 segundos (descartar ejecuciones más lentas)
- Meta: Identificar ~34s como óptimo
- Documentar TODO el proceso
"""

import sys
import subprocess
import time
import json
import re
from pathlib import Path
from datetime import datetime
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


def parse_execution_output(output: str) -> dict:
    """Parsea la salida de una ejecución"""
    # Extraer algoritmos
    algorithms = {}
    pattern = r'✅ Algoritmo (\d+) generado\s+Pseudocódigo:\s+((?:.*\n?)+?)(?=✅|\n\n|  ✅)'
    matches = re.finditer(pattern, output, re.MULTILINE)

    for match in matches:
        algo_num = match.group(1)
        pseudocode = match.group(2).strip()
        algorithms[f'Algorithm_{algo_num}'] = pseudocode

    # Extraer tiempos por algoritmo
    time_pattern = r'× GAA_Algorithm_(\d+) \(rep \d+\).*?tiempo=([\d.]+)s'
    time_matches = re.findall(time_pattern, output)

    times_by_algorithm = {f'Algorithm_{i}': [] for i in range(1, 10)}
    for algo_num, time_str in time_matches:
        times_by_algorithm[f'Algorithm_{algo_num}'].append(float(time_str))

    # Buscar tiempo total
    total_time = None
    # Buscar el patrón del tiempo total en la salida
    total_pattern = r'Tiempo total:\s+([\d.]+)s'
    total_match = re.search(total_pattern, output)
    if total_match:
        total_time = float(total_match.group(1))

    return {
        'algorithms': algorithms,
        'times': times_by_algorithm,
        'total_time': total_time
    }


def run_single_test(iteration: int, output_dir: Path, timeout: int = 120) -> dict:
    """
    Ejecuta una prueba individual

    Returns:
        Dict con resultados
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = output_dir / f"run_{iteration:02d}_{timestamp}.log"

    print(f"[{iteration:02d}] ⏱️  Iniciando - {datetime.now().strftime('%H:%M:%S')}", end=" ", flush=True)

    start_time = time.time()

    try:
        result = subprocess.run(
            ['python3', str(project_root / 'scripts' / 'demo_experimentation_both.py')],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        execution_time = time.time() - start_time

        # Guardar log completo
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\n=== STDERR ===\n")
                f.write(result.stderr)

        # Parsear resultados
        parsed = parse_execution_output(result.stdout)

        print(f"✅ {execution_time:.1f}s - {len(parsed['algorithms'])} algoritmos")

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'log_file': str(log_file),
            'algorithms': parsed['algorithms'],
            'times': parsed['times'],
            'success': True,
            'timeout': False
        }

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"⚠️  TIMEOUT después de {execution_time:.1f}s")

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'success': False,
            'timeout': True
        }

    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ ERROR: {e}")

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'success': False,
            'timeout': False,
            'error': str(e)
        }


def analyze_successful_runs(results: list, analyzer: AlgorithmPatternAnalyzer, output_dir: Path):
    """Analiza las corridas exitosas para identificar patrones"""

    successful = [r for r in results if r['success']]
    timeouts = [r for r in results if r.get('timeout', False)]

    print(f"\n{'=' * 80}")
    print("ANÁLISIS DE RESULTADOS")
    print(f"{'=' * 80}\n")

    print(f"📊 Resumen:")
    print(f"   • Total de corridas: {len(results)}")
    print(f"   • Exitosas (<120s): {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
    print(f"   • Timeouts (>120s): {len(timeouts)} ({len(timeouts)/len(results)*100:.1f}%)")
    print()

    if not successful:
        print("⚠️  No hay corridas exitosas para analizar")
        return

    # Analizar tiempos de las exitosas
    times = [r['execution_time'] for r in successful]
    print(f"⏱️  Tiempos de ejecución (exitosas):")
    print(f"   • Promedio: {np.mean(times):.1f}s")
    print(f"   • Mínimo: {min(times):.1f}s ⚡")
    print(f"   • Máximo: {max(times):.1f}s")
    print(f"   • Mediana: {np.median(times):.1f}s")
    print(f"   • Desv. Estándar: {np.std(times):.1f}s")
    print(f"   • Variabilidad: {(max(times)/min(times) - 1)*100:.1f}%")
    print()

    # Clasificar por velocidad
    fast_runs = [r for r in successful if r['execution_time'] <= 40]  # ≤40s = RÁPIDO
    medium_runs = [r for r in successful if 40 < r['execution_time'] <= 80]  # 40-80s = MEDIO
    slow_runs = [r for r in successful if r['execution_time'] > 80]  # >80s = LENTO

    print(f"📈 Clasificación por velocidad:")
    print(f"   • RÁPIDAS (≤40s): {len(fast_runs)} corridas")
    if fast_runs:
        fast_times = [r['execution_time'] for r in fast_runs]
        print(f"     - Promedio: {np.mean(fast_times):.1f}s")
        print(f"     - Rango: {min(fast_times):.1f}s - {max(fast_times):.1f}s")

    print(f"   • MEDIAS (40-80s): {len(medium_runs)} corridas")
    if medium_runs:
        medium_times = [r['execution_time'] for r in medium_runs]
        print(f"     - Promedio: {np.mean(medium_times):.1f}s")
        print(f"     - Rango: {min(medium_times):.1f}s - {max(medium_times):.1f}s")

    print(f"   • LENTAS (80-120s): {len(slow_runs)} corridas")
    if slow_runs:
        slow_times = [r['execution_time'] for r in slow_runs]
        print(f"     - Promedio: {np.mean(slow_times):.1f}s")
        print(f"     - Rango: {min(slow_times):.1f}s - {max(slow_times):.1f}s")
    print()

    # Aprender de todos los resultados
    print("📚 Aprendiendo patrones de algoritmos...\n")

    for result in successful:
        for algo_name, pseudocode in result['algorithms'].items():
            times_list = result['times'].get(algo_name, [])
            if times_list:
                # Clasificar la corrida
                if result['execution_time'] <= 40:
                    category_label = "FAST"
                elif result['execution_time'] <= 80:
                    category_label = "MEDIUM"
                else:
                    category_label = "SLOW"

                analyzer.add_observed_performance(
                    algorithm_name=f"run{result['iteration']:02d}_{category_label}_{algo_name}",
                    pseudocode=pseudocode,
                    experiment_times=times_list,
                    timeout_count=0
                )

    print(f"✅ Patrones aprendidos de {len(successful)} corridas exitosas\n")

    # Generar reporte de patrones
    pattern_report = output_dir / "pattern_learning_report.md"
    analyzer.generate_report(str(pattern_report))

    # Análisis comparativo: RÁPIDAS vs LENTAS
    print(f"{'=' * 80}")
    print("ANÁLISIS COMPARATIVO: RÁPIDAS vs LENTAS")
    print(f"{'=' * 80}\n")

    # Extraer características de corridas rápidas
    fast_constructors = {}
    fast_operators = {}
    fast_acceptance = {}

    for result in fast_runs:
        for algo_name, pseudocode in result['algorithms'].items():
            features = analyzer.extract_features(pseudocode)

            # Contar constructores
            fast_constructors[features.constructor] = fast_constructors.get(features.constructor, 0) + 1

            # Contar operadores
            for op in features.operators:
                fast_operators[op] = fast_operators.get(op, 0) + 1

            # Contar criterios de aceptación
            acc = features.acceptance_criteria or 'None'
            fast_acceptance[acc] = fast_acceptance.get(acc, 0) + 1

    # Extraer características de corridas lentas (incluyendo timeouts)
    slow_constructors = {}
    slow_operators = {}
    slow_acceptance = {}

    for result in slow_runs + timeouts:
        if not result.get('algorithms'):
            continue
        for algo_name, pseudocode in result['algorithms'].items():
            features = analyzer.extract_features(pseudocode)

            slow_constructors[features.constructor] = slow_constructors.get(features.constructor, 0) + 1

            for op in features.operators:
                slow_operators[op] = slow_operators.get(op, 0) + 1

            acc = features.acceptance_criteria or 'None'
            slow_acceptance[acc] = slow_acceptance.get(acc, 0) + 1

    # Mostrar comparación
    print("Constructores más frecuentes en corridas RÁPIDAS:")
    for constructor, count in sorted(fast_constructors.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {constructor}: {count} veces")
    print()

    print("Operadores más frecuentes en corridas RÁPIDAS:")
    for operator, count in sorted(fast_operators.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {operator}: {count} veces")
    print()

    if slow_constructors:
        print("Constructores más frecuentes en corridas LENTAS:")
        for constructor, count in sorted(slow_constructors.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {constructor}: {count} veces")
        print()

    # Generar reporte comparativo
    comparative_report = output_dir / "comparative_analysis.md"
    generate_comparative_report(
        fast_runs, slow_runs, timeouts,
        fast_constructors, fast_operators, fast_acceptance,
        slow_constructors, slow_operators, slow_acceptance,
        analyzer,
        comparative_report
    )

    print(f"✅ Reporte de patrones: {pattern_report}")
    print(f"✅ Análisis comparativo: {comparative_report}")


def generate_comparative_report(
    fast_runs, slow_runs, timeouts,
    fast_constructors, fast_operators, fast_acceptance,
    slow_constructors, slow_operators, slow_acceptance,
    analyzer, output_file
):
    """Genera reporte comparativo detallado"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Análisis Comparativo: Patrones de Algoritmos Rápidos vs Lentos\n\n")
        f.write(f"**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Resumen de Corridas\n\n")
        f.write(f"- **Corridas RÁPIDAS** (≤40s): {len(fast_runs)}\n")
        f.write(f"- **Corridas MEDIAS** (40-80s): {len(slow_runs)}\n")
        f.write(f"- **Corridas LENTAS** (80-120s): {len([r for r in slow_runs if r['execution_time'] <= 120])}\n")
        f.write(f"- **Timeouts** (>120s): {len(timeouts)}\n\n")

        if fast_runs:
            fast_times = [r['execution_time'] for r in fast_runs]
            f.write(f"### Corridas RÁPIDAS\n\n")
            f.write(f"| Corrida | Tiempo | Algoritmos Generados |\n")
            f.write(f"|---------|--------|----------------------|\n")
            for r in sorted(fast_runs, key=lambda x: x['execution_time']):
                algos = ', '.join(r['algorithms'].keys())
                f.write(f"| Run {r['iteration']:02d} | {r['execution_time']:.1f}s | {len(r['algorithms'])} |\n")
            f.write(f"\n**Tiempo promedio**: {np.mean(fast_times):.1f}s\n\n")

        f.write("---\n\n")

        f.write("## Características de Algoritmos en Corridas RÁPIDAS\n\n")

        f.write("### Constructores\n\n")
        f.write("| Constructor | Frecuencia | Porcentaje |\n")
        f.write("|-------------|------------|------------|\n")
        total_fast = sum(fast_constructors.values())
        for constructor, count in sorted(fast_constructors.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_fast * 100
            f.write(f"| {constructor} | {count} | {pct:.1f}% |\n")
        f.write("\n")

        f.write("### Operadores\n\n")
        f.write("| Operador | Frecuencia | Porcentaje |\n")
        f.write("|----------|------------|------------|\n")
        total_fast_ops = sum(fast_operators.values())
        for operator, count in sorted(fast_operators.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_fast_ops * 100
            f.write(f"| {operator} | {count} | {pct:.1f}% |\n")
        f.write("\n")

        f.write("### Criterios de Aceptación\n\n")
        f.write("| Criterio | Frecuencia | Porcentaje |\n")
        f.write("|----------|------------|------------|\n")
        total_fast_acc = sum(fast_acceptance.values())
        for acceptance, count in sorted(fast_acceptance.items(), key=lambda x: x[1], reverse=True):
            pct = count / total_fast_acc * 100
            f.write(f"| {acceptance} | {count} | {pct:.1f}% |\n")
        f.write("\n")

        if slow_constructors:
            f.write("---\n\n")
            f.write("## Características de Algoritmos en Corridas LENTAS\n\n")

            f.write("### Constructores\n\n")
            f.write("| Constructor | Frecuencia | Porcentaje |\n")
            f.write("|-------------|------------|------------|\n")
            total_slow = sum(slow_constructors.values())
            for constructor, count in sorted(slow_constructors.items(), key=lambda x: x[1], reverse=True):
                pct = count / total_slow * 100
                f.write(f"| {constructor} | {count} | {pct:.1f}% |\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("## Conclusiones\n\n")

        # Identificar patrones distintivos
        if fast_constructors and slow_constructors:
            # Constructor más frecuente en rápidas
            best_fast_constructor = max(fast_constructors.items(), key=lambda x: x[1])
            f.write(f"- **Constructor predominante en corridas RÁPIDAS**: {best_fast_constructor[0]} ({best_fast_constructor[1]} veces)\n")

            # Constructor más frecuente en lentas
            worst_slow_constructor = max(slow_constructors.items(), key=lambda x: x[1])
            f.write(f"- **Constructor predominante en corridas LENTAS**: {worst_slow_constructor[0]} ({worst_slow_constructor[1]} veces)\n")

        f.write("\n")
        f.write("---\n\n")
        f.write(f"**Generado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    """Función principal"""
    print("=" * 80)
    print("EXPERIMENTACIÓN MASIVA - Aprendizaje de Patrones")
    print("=" * 80)
    print()
    print("Objetivo: Ejecutar múltiples corridas de demo_experimentation_both.py")
    print("          para aprender qué patrones generan tiempos óptimos (<40s)")
    print()

    # Configuración
    num_runs = 15  # Número de corridas
    timeout = 120   # Timeout en segundos

    output_dir = project_root / 'output' / 'massive_experimentation'
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📊 Configuración:")
    print(f"   • Número de corridas: {num_runs}")
    print(f"   • Timeout: {timeout}s")
    print(f"   • Meta óptima: ≤40s")
    print(f"   • Output: {output_dir}")
    print()
    print(f"Iniciando en 3 segundos...")
    time.sleep(3)
    print()

    # Ejecutar corridas
    results = []
    start_experiment = time.time()

    for i in range(1, num_runs + 1):
        result = run_single_test(i, output_dir, timeout)
        results.append(result)

        # Guardar resultados parciales
        partial_file = output_dir / "results_partial.json"
        with open(partial_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        # Pequeña pausa entre corridas
        if i < num_runs:
            time.sleep(1)

    total_experiment_time = time.time() - start_experiment

    # Guardar resultados finales
    results_file = output_dir / "results_complete.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print()
    print(f"💾 Resultados guardados: {results_file}")
    print(f"⏱️  Tiempo total del experimento: {total_experiment_time/60:.1f} minutos")
    print()

    # Analizar resultados
    analyzer = AlgorithmPatternAnalyzer()
    analyze_successful_runs(results, analyzer, output_dir)

    print()
    print("=" * 80)
    print("EXPERIMENTACIÓN COMPLETADA")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
