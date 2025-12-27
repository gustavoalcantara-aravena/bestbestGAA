#!/usr/bin/env python3
"""
Experimentación Científica Rigurosa - KBP-SA
Ejecuta múltiples corridas del experimento REAL y aprende de los resultados
"""

import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


def parse_execution_output(output: str) -> dict:
    """
    Parsea la salida de una ejecución para extraer información relevante

    Returns:
        Dict con algoritmos generados y tiempos
    """
    # Extraer algoritmos
    algorithms = {}
    pattern = r'✅ Algoritmo (\d+) generado\s+Pseudocódigo:\s+((?:.*\n?)+?)(?=✅|\n\n|  ✅)'
    matches = re.finditer(pattern, output, re.MULTILINE)

    for match in matches:
        algo_num = match.group(1)
        pseudocode = match.group(2).strip()
        algorithms[f'Algorithm_{algo_num}'] = pseudocode

    # Extraer tiempos
    time_pattern = r'× GAA_Algorithm_(\d+) \(rep \d+\).*?tiempo=([\d.]+)s'
    time_matches = re.findall(time_pattern, output)

    times_by_algorithm = {f'Algorithm_{i}': [] for i in range(1, 10)}
    for algo_num, time_str in time_matches:
        times_by_algorithm[f'Algorithm_{algo_num}'].append(float(time_str))

    # Extraer tiempo total
    total_time = None
    total_match = re.search(r'⏱️ \s+Tiempo total:\s+([\d.]+)s', output)
    if total_match:
        total_time = float(total_match.group(1))
    else:
        # Buscar el último timestamp
        time_matches = re.findall(r'⏱️ \s+Duración:\s+([\d.]+)s', output)
        if time_matches:
            total_time = sum(float(t) for t in time_matches)

    return {
        'algorithms': algorithms,
        'times': times_by_algorithm,
        'total_time': total_time
    }


def run_single_experiment(
    iteration: int,
    output_dir: Path,
    timeout: int = 600
) -> dict:
    """
    Ejecuta un experimento completo

    Args:
        iteration: Número de iteración
        output_dir: Directorio para guardar outputs
        timeout: Timeout en segundos

    Returns:
        Dict con resultados
    """
    print(f"\n{'=' * 80}")
    print(f"EJECUCIÓN {iteration}")
    print(f"{'=' * 80}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = output_dir / f"execution_{iteration}_{timestamp}.log"

    print(f"⏱️  Iniciando ejecución {iteration} - {datetime.now().strftime('%H:%M:%S')}")
    print(f"📄 Log: {log_file.name}")
    print()

    start_time = time.time()

    try:
        # Ejecutar el script original
        result = subprocess.run(
            ['python3', str(project_root / 'scripts' / 'demo_experimentation_both.py')],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        execution_time = time.time() - start_time

        # Guardar output completo
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\n=== STDERR ===\n")
                f.write(result.stderr)

        # Parsear resultados
        parsed = parse_execution_output(result.stdout)

        print(f"✅ Ejecución {iteration} completada en {execution_time:.1f}s")
        print(f"   • Tiempo reportado: {parsed['total_time']:.1f}s" if parsed['total_time'] else "")
        print(f"   • Algoritmos generados: {len(parsed['algorithms'])}")
        print()

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'reported_time': parsed['total_time'],
            'log_file': str(log_file),
            'algorithms': parsed['algorithms'],
            'times': parsed['times'],
            'success': True,
            'error': None
        }

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"⚠️  TIMEOUT en ejecución {iteration} después de {execution_time:.1f}s")

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'success': False,
            'error': 'TIMEOUT',
            'log_file': str(log_file) if log_file.exists() else None
        }

    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ ERROR en ejecución {iteration}: {e}")

        return {
            'iteration': iteration,
            'timestamp': timestamp,
            'execution_time': execution_time,
            'success': False,
            'error': str(e)
        }


def analyze_results(results: list, analyzer: AlgorithmPatternAnalyzer, output_dir: Path):
    """
    Analiza todos los resultados y genera reportes científicos

    Args:
        results: Lista de resultados de ejecuciones
        analyzer: Analizador de patrones
        output_dir: Directorio de salida
    """
    print(f"\n{'=' * 80}")
    print("ANÁLISIS DE RESULTADOS")
    print(f"{'=' * 80}\n")

    # Filtrar ejecuciones exitosas
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"📊 Ejecuciones exitosas: {len(successful)}/{len(results)}")
    if failed:
        print(f"⚠️  Ejecuciones fallidas: {len(failed)}")
        for r in failed:
            print(f"   • Iteración {r['iteration']}: {r['error']}")
    print()

    # Analizar tiempos de ejecución
    if successful:
        times = [r['execution_time'] for r in successful]
        print(f"⏱️  Tiempos de ejecución:")
        print(f"   • Promedio: {sum(times)/len(times):.1f}s")
        print(f"   • Mínimo: {min(times):.1f}s")
        print(f"   • Máximo: {max(times):.1f}s")
        print(f"   • Variabilidad: {(max(times)/min(times) - 1)*100:.1f}%")
        print()

    # Agregar datos al analizador
    print("📚 Aprendiendo de los resultados...")
    print()

    for result in successful:
        for algo_name, pseudocode in result['algorithms'].items():
            times_list = result['times'].get(algo_name, [])
            if times_list:
                analyzer.add_observed_performance(
                    algorithm_name=f"exec{result['iteration']}_{algo_name}",
                    pseudocode=pseudocode,
                    experiment_times=times_list,
                    timeout_count=0
                )

                print(f"   ✅ Aprendido: Ejecución {result['iteration']} - {algo_name}")

    print()

    # Generar reporte de patrones
    pattern_report = output_dir / "learned_patterns_report.md"
    analyzer.generate_report(str(pattern_report))

    print(f"✅ Reporte de patrones: {pattern_report}")
    print()

    # Mostrar correlaciones aprendidas
    correlations = analyzer.analyze_pattern_correlations()

    print("📊 PATRONES APRENDIDOS:\n")

    print("Constructores (de más rápido a más lento):")
    for constructor, stats in sorted(correlations['constructors'].items(), key=lambda x: x[1]['avg']):
        print(f"   • {constructor:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")
    print()

    print("Operadores (de más rápido a más lento):")
    for operator, stats in sorted(correlations['operators'].items(), key=lambda x: x[1]['avg']):
        print(f"   • {operator:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")
    print()

    if 'acceptance' in correlations and correlations['acceptance']:
        print("Criterios de Aceptación (de más rápido a más lento):")
        for acceptance, stats in sorted(correlations['acceptance'].items(), key=lambda x: x[1]['avg']):
            print(f"   • {acceptance:20s}: {stats['avg']:6.3f}s ± {stats['std']:.3f}s (n={stats['count']})")
        print()

    # Generar reporte científico completo
    scientific_report = output_dir / "scientific_analysis.md"
    generate_scientific_report(results, correlations, scientific_report)

    print(f"✅ Reporte científico: {scientific_report}")


def generate_scientific_report(results: list, correlations: dict, output_file: Path):
    """Genera un reporte científico completo"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Análisis Científico: Patrones de Rendimiento en Algoritmos GAA\n\n")
        f.write(f"**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Metodología\n\n")
        f.write("Este estudio ejecutó múltiples iteraciones del framework GAA (Grammar-based Algorithm Algorithm) ")
        f.write("para identificar patrones en las características de algoritmos que correlacionan con ")
        f.write("tiempos de ejecución más rápidos o más lentos.\n\n")

        f.write("### Diseño Experimental\n\n")
        f.write(f"- **Número de ejecuciones**: {len(results)}\n")
        successful = [r for r in results if r['success']]
        f.write(f"- **Ejecuciones exitosas**: {len(successful)}\n")
        f.write("- **Script ejecutado**: `demo_experimentation_both.py` (original, sin modificaciones)\n")
        f.write("- **Seed**: 42 (configuración original)\n")
        f.write("- **Instancias evaluadas**: 10 low-dimensional + 21 large-scale = 31 total\n")
        f.write("- **Algoritmos por ejecución**: 3\n")
        f.write("- **Repeticiones por instancia**: 1\n\n")

        f.write("---\n\n")

        f.write("## Resultados\n\n")

        f.write("### Tiempos de Ejecución\n\n")
        if successful:
            times = [r['execution_time'] for r in successful]
            import numpy as np
            f.write(f"| Métrica | Valor |\n")
            f.write(f"|---------|-------|\n")
            f.write(f"| Promedio | {np.mean(times):.1f}s |\n")
            f.write(f"| Desviación Estándar | {np.std(times):.1f}s |\n")
            f.write(f"| Mínimo | {min(times):.1f}s |\n")
            f.write(f"| Máximo | {max(times):.1f}s |\n")
            f.write(f"| Mediana | {np.median(times):.1f}s |\n")
            f.write(f"| Variabilidad (max/min) | {max(times)/min(times):.2f}x |\n\n")

            f.write("### Distribución de Tiempos por Ejecución\n\n")
            f.write("| Ejecución | Tiempo (s) | Relativo al Promedio |\n")
            f.write("|-----------|------------|----------------------|\n")
            avg_time = np.mean(times)
            for r in successful:
                rel = r['execution_time'] / avg_time
                f.write(f"| {r['iteration']} | {r['execution_time']:.1f} | {rel:.2f}x |\n")
            f.write("\n")

        f.write("---\n\n")

        f.write("## Análisis de Patrones\n\n")

        f.write("### Constructores\n\n")
        f.write("| Constructor | Tiempo Promedio | Desv. Estándar | Muestras |\n")
        f.write("|-------------|-----------------|----------------|----------|\n")
        for constructor, stats in sorted(correlations['constructors'].items(), key=lambda x: x[1]['avg']):
            f.write(f"| {constructor} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
        f.write("\n")

        f.write("### Operadores\n\n")
        f.write("| Operador | Tiempo Promedio | Desv. Estándar | Muestras |\n")
        f.write("|----------|-----------------|----------------|----------|\n")
        for operator, stats in sorted(correlations['operators'].items(), key=lambda x: x[1]['avg']):
            f.write(f"| {operator} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
        f.write("\n")

        if 'acceptance' in correlations and correlations['acceptance']:
            f.write("### Criterios de Aceptación\n\n")
            f.write("| Criterio | Tiempo Promedio | Desv. Estándar | Muestras |\n")
            f.write("|----------|-----------------|----------------|----------|\n")
            for acceptance, stats in sorted(correlations['acceptance'].items(), key=lambda x: x[1]['avg']):
                f.write(f"| {acceptance} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
            f.write("\n")

        f.write("---\n\n")

        f.write("## Conclusiones\n\n")

        best_constructor = min(correlations['constructors'].items(), key=lambda x: x[1]['avg'])
        worst_constructor = max(correlations['constructors'].items(), key=lambda x: x[1]['avg'])

        f.write(f"### Hallazgos Clave\n\n")
        f.write(f"1. **Mejor Constructor**: {best_constructor[0]} ({best_constructor[1]['avg']:.3f}s promedio)\n")
        f.write(f"2. **Peor Constructor**: {worst_constructor[0]} ({worst_constructor[1]['avg']:.3f}s promedio)\n")
        f.write(f"3. **Diferencia**: {worst_constructor[1]['avg']/best_constructor[1]['avg']:.2f}x más lento\n\n")

        best_operator = min(correlations['operators'].items(), key=lambda x: x[1]['avg'])
        worst_operator = max(correlations['operators'].items(), key=lambda x: x[1]['avg'])

        f.write(f"4. **Mejor Operador**: {best_operator[0]} ({best_operator[1]['avg']:.3f}s promedio)\n")
        f.write(f"5. **Peor Operador**: {worst_operator[0]} ({worst_operator[1]['avg']:.3f}s promedio)\n")
        f.write(f"6. **Diferencia**: {worst_operator[1]['avg']/best_operator[1]['avg']:.2f}x más lento\n\n")

        f.write("### Recomendaciones\n\n")
        f.write("Para minimizar el tiempo de ejecución, se recomienda:\n\n")
        f.write(f"- ✅ Usar constructor **{best_constructor[0]}**\n")
        f.write(f"- ✅ Usar operador **{best_operator[0]}**\n")
        f.write(f"- ❌ Evitar constructor **{worst_constructor[0]}**\n")
        f.write(f"- ❌ Evitar operador **{worst_operator[0]}**\n\n")

        f.write("---\n\n")
        f.write(f"**Análisis completado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    """Función principal"""
    print("=" * 80)
    print("EXPERIMENTACIÓN CIENTÍFICA RIGUROSA")
    print("Ejecución múltiple de demo_experimentation_both.py")
    print("=" * 80)
    print()

    # Configuración
    num_experiments = int(input("¿Cuántas ejecuciones deseas realizar? [5]: ") or "5")
    timeout = int(input("Timeout por ejecución (segundos) [600]: ") or "600")

    output_dir = project_root / 'output' / 'scientific_experiments_real'
    output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print(f"📊 Configuración:")
    print(f"   • Número de ejecuciones: {num_experiments}")
    print(f"   • Timeout: {timeout}s")
    print(f"   • Output: {output_dir}")
    print()
    print("Iniciando experimentación...")
    print()

    # Crear analizador
    analyzer = AlgorithmPatternAnalyzer()

    # Ejecutar experimentos
    results = []
    for i in range(1, num_experiments + 1):
        result = run_single_experiment(i, output_dir, timeout)
        results.append(result)

        # Guardar resultados parciales
        partial_results_file = output_dir / f"results_partial.json"
        with open(partial_results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        time.sleep(2)  # Pausa entre ejecuciones

    # Guardar resultados completos
    results_file = output_dir / "results_complete.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Resultados guardados: {results_file}")
    print()

    # Analizar resultados
    analyze_results(results, analyzer, output_dir)

    print()
    print("=" * 80)
    print("EXPERIMENTACIÓN COMPLETADA")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
