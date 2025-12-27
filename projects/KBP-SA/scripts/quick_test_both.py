#!/usr/bin/env python3
"""
Test rápido del script both para identificar cuellos de botella
Solo procesa grupo low_dimensional
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import time

# Configurar encoding UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Tracker de tiempos
times = {}

def track_time(phase_name):
    """Decorator para trackear tiempos"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"\n⏱️  Iniciando: {phase_name}...")
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            times[phase_name] = elapsed
            print(f"✅ Completado: {phase_name} ({elapsed:.2f}s)")
            return result
        return wrapper
    return decorator

@track_time("Imports")
def do_imports():
    global ExperimentRunner, ExperimentConfig, StatisticalAnalyzer
    global ResultsVisualizer, ASTVisualizer, TimeTracker
    global AlgorithmGenerator, Grammar, DatasetLoader, SimulatedAnnealing
    global KnapsackSolution, np

    from experimentation.runner import ExperimentRunner, ExperimentConfig
    from experimentation.statistics import StatisticalAnalyzer
    from experimentation.visualization import ResultsVisualizer
    from experimentation.ast_visualization import ASTVisualizer
    from experimentation.time_tracker import TimeTracker
    from gaa.generator import AlgorithmGenerator
    from gaa.grammar import Grammar
    from data.loader import DatasetLoader
    from metaheuristic.sa_core import SimulatedAnnealing
    from core.solution import KnapsackSolution
    import numpy as np

@track_time("Generar 3 algoritmos")
def generate_algorithms():
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'GAA_Algorithm_{i+1}',
                'ast': ast
            })
    return algorithms

@track_time("Cargar instancias low_dimensional")
def load_instances():
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    return loader.load_folder("low_dimensional"), loader

@track_time("Configurar experimento")
def configure_experiment(instances, algorithms):
    instance_names = [inst.name for inst in instances]
    config = ExperimentConfig(
        name="low_dimensional_experiment",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=60.0,
        output_dir="output/low_dimensional_experiments"
    )
    return config

@track_time("Ejecutar experimentos (ExperimentRunner.run_all)")
def run_experiments(config):
    runner = ExperimentRunner(config)
    runner.load_instances("low_dimensional")
    results = runner.run_all(verbose=True)
    return runner, results

@track_time("Análisis estadístico")
def run_statistics(results, algorithms):
    analyzer = StatisticalAnalyzer(alpha=0.05)
    algorithm_results = {}

    for alg in algorithms:
        alg_name = alg['name']
        alg_data = [r for r in results if r.algorithm_name == alg_name and r.success]
        if alg_data:
            gaps = [r.gap_to_optimal for r in alg_data if r.gap_to_optimal is not None]
            algorithm_results[alg_name] = gaps

    return analyzer, algorithm_results

@track_time("Comparación estadística")
def run_comparison(analyzer, algorithm_results):
    if len(algorithm_results) >= 2:
        comparison = analyzer.compare_multiple_algorithms(
            algorithm_results,
            test_type="friedman"
        )
        return comparison
    return None

@track_time("Generar visualizaciones base (boxplot, bars, scatter)")
def generate_base_visualizations(algorithm_results, results, analyzer):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plots_dir = f"output/plots_low_dimensional_{timestamp}"

    visualizer = ResultsVisualizer(output_dir=plots_dir)

    if visualizer.has_matplotlib and len(algorithm_results) >= 2:
        # Boxplot
        visualizer.plot_boxplot_comparison(
            algorithm_results,
            title="Comparación de Algoritmos - Low-Dimensional",
            ylabel="Gap (%)",
            filename="demo_boxplot.png"
        )

        # Barras
        alg_metrics = {}
        for alg_name, gaps in algorithm_results.items():
            stats = analyzer.descriptive_statistics(gaps)
            alg_metrics[alg_name] = {
                'mean_value': stats['mean'],
                'std_value': stats['std']
            }

        visualizer.plot_bar_comparison(
            alg_metrics,
            metric_name='mean_value',
            title="Gap Promedio por Algoritmo - Low-Dimensional",
            ylabel="Gap Promedio (%)",
            filename="demo_bars.png",
            show_error_bars=True
        )

        # Scatter
        result_dicts = [
            {
                'algorithm_name': r.algorithm_name,
                'total_time': r.total_time,
                'gap_to_optimal': r.gap_to_optimal
            }
            for r in results if r.success and r.gap_to_optimal is not None
        ]

        visualizer.plot_scatter_time_vs_quality(
            result_dicts,
            title="Trade-off Tiempo vs Calidad - Low-Dimensional",
            filename="demo_scatter.png"
        )

    return plots_dir

@track_time("Generar visualizaciones SA (todas las instancias)")
def generate_sa_visualizations(instances, algorithm, plots_dir):
    # Esta es la función costosa que ejecuta SA en TODAS las instancias
    from demo_experimentation_both import run_detailed_visualization_per_group

    run_detailed_visualization_per_group(
        instances=instances,
        algorithm=algorithm,
        plots_dir=Path(plots_dir),
        group_name="Low-Dimensional"
    )

# Ejecutar análisis
if __name__ == '__main__':
    print("=" * 80)
    print("  TEST RÁPIDO: demo_experimentation_both.py (solo low_dimensional)")
    print("=" * 80)

    total_start = time.time()

    do_imports()
    algorithms = generate_algorithms()
    instances, loader = load_instances()

    print(f"\n📊 Procesando {len(instances)} instancias con {len(algorithms)} algoritmos")
    print(f"   Total de experimentos: {len(instances) * len(algorithms)}")

    config = configure_experiment(instances, algorithms)
    runner, results = run_experiments(config)
    analyzer, algorithm_results = run_statistics(results, algorithms)
    comparison = run_comparison(analyzer, algorithm_results)

    if comparison:
        best_alg = next(alg for alg in algorithms if alg['name'] == comparison['best_algorithm'])
        plots_dir = generate_base_visualizations(algorithm_results, results, analyzer)

        # Esta es la parte más costosa
        print(f"\n⚠️  ATENCIÓN: La siguiente fase ejecuta SA en {len(instances)} instancias")
        print(f"   con tracking completo y genera {len(instances) + 3} gráficas")
        generate_sa_visualizations(instances, best_alg, plots_dir)

    total_elapsed = time.time() - total_start

    # Resumen
    print("\n" + "=" * 80)
    print("  RESUMEN DE TIEMPOS")
    print("=" * 80)
    print()

    # Ordenar por tiempo
    sorted_times = sorted(times.items(), key=lambda x: x[1], reverse=True)

    print(f"{'Fase':<60} {'Tiempo (s)':<10} {'%':<6}")
    print("-" * 80)

    for phase, t in sorted_times:
        percentage = (t / total_elapsed * 100) if total_elapsed > 0 else 0
        print(f"{phase:<60} {t:>8.2f}s {percentage:>6.1f}%")

    print("-" * 80)
    print(f"{'TOTAL':<60} {total_elapsed:>8.2f}s {'100.0%':>7}")
    print()

    # Análisis
    print("🔍 ANÁLISIS:")
    print()

    bottlenecks = [(p, t, t/total_elapsed*100) for p, t in sorted_times if t/total_elapsed > 0.15]

    if bottlenecks:
        print("⚠️  Cuellos de botella (>15% del tiempo):")
        for phase, t, pct in bottlenecks:
            print(f"   • {phase}: {t:.2f}s ({pct:.1f}%)")

    print()
    print(f"⏱️  Tiempo total: {total_elapsed:.2f} segundos")
    print()
