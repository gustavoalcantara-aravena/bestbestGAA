#!/usr/bin/env python3
"""
Análisis de tiempos por fase para demo_experimentation_both.py
Intercepta y mide cada fase principal
"""

import sys
import os
from pathlib import Path
import time
from datetime import datetime

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Variables para tracking de tiempos
phase_times = {}
current_phase = None
phase_start = None

def start_phase(name):
    """Inicia medición de una fase"""
    global current_phase, phase_start
    if current_phase:
        end_phase()
    current_phase = name
    phase_start = time.time()
    print(f"\n⏱️  [{datetime.now().strftime('%H:%M:%S')}] Iniciando: {name}")

def end_phase():
    """Finaliza medición de una fase"""
    global current_phase, phase_start, phase_times
    if current_phase and phase_start:
        elapsed = time.time() - phase_start
        phase_times[current_phase] = elapsed
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Completado: {current_phase} ({elapsed:.2f}s)")
        current_phase = None
        phase_start = None

def print_summary():
    """Imprime resumen de tiempos"""
    print("\n" + "=" * 80)
    print("  ANÁLISIS DE TIEMPOS POR FASE")
    print("=" * 80)
    print()

    total = sum(phase_times.values())

    # Ordenar por tiempo (mayor a menor)
    sorted_phases = sorted(phase_times.items(), key=lambda x: x[1], reverse=True)

    print(f"{'Fase':<60} {'Tiempo (s)':<10} {'%':<6}")
    print("-" * 80)

    for phase, t in sorted_phases:
        percentage = (t / total * 100) if total > 0 else 0
        print(f"{phase:<60} {t:>8.2f}s {percentage:>6.1f}%")

    print("-" * 80)
    print(f"{'TOTAL':<60} {total:>8.2f}s {'100.0%':>7}")
    print()

    # Identificar cuellos de botella
    print("🔍 ANÁLISIS DE CUELLOS DE BOTELLA:")
    print()

    # Fases que toman más del 20% del tiempo
    bottlenecks = [(p, t, t/total*100) for p, t in sorted_phases if t/total > 0.20]

    if bottlenecks:
        print("⚠️  Fases que consumen más del 20% del tiempo total:")
        for phase, t, pct in bottlenecks:
            print(f"   • {phase}: {t:.2f}s ({pct:.1f}%)")
    else:
        print("✓ No hay fases dominantes individuales (>20%)")

    print()

# Ejecutar análisis
if __name__ == '__main__':
    print("=" * 80)
    print("  ANÁLISIS DE TIEMPOS: demo_experimentation_both.py")
    print("=" * 80)

    total_start = time.time()

    # Imports
    start_phase("Imports y preparación")
    from experimentation.runner import ExperimentRunner, ExperimentConfig
    from experimentation.statistics import StatisticalAnalyzer
    from experimentation.visualization import ResultsVisualizer
    from gaa.generator import AlgorithmGenerator
    from gaa.grammar import Grammar
    from data.loader import DatasetLoader
    end_phase()

    # Generar algoritmos
    start_phase("Generación de 3 algoritmos GAA")
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
    end_phase()

    # Cargar datasets low_dimensional
    start_phase("Carga de datasets low_dimensional (primera vez)")
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    low_dim_instances = loader.load_folder("low_dimensional")
    end_phase()

    print(f"   → Cargadas {len(low_dim_instances)} instancias low_dimensional")

    # Simular carga duplicada
    start_phase("Carga de datasets low_dimensional (segunda vez - DUPLICADA)")
    low_dim_instances_2 = loader.load_folder("low_dimensional")
    end_phase()

    # Cargar datasets large_scale
    start_phase("Carga de datasets large_scale (primera vez)")
    large_scale_instances = loader.load_folder("large_scale")
    end_phase()

    print(f"   → Cargadas {len(large_scale_instances)} instancias large_scale")

    # Simular ejecución SA en una instancia
    start_phase("Ejecución SA en 1 instancia low_dimensional (con tracking)")
    from metaheuristic.sa_core import SimulatedAnnealing
    from core.solution import KnapsackSolution
    import numpy as np

    instance = low_dim_instances[0]
    sa = SimulatedAnnealing(
        problem=instance,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=100,
        T_min=0.01,
        max_evaluations=5000,
        seed=42
    )

    def custom_neighborhood(solution, rng):
        neighbor = solution.copy()
        idx_flip = rng.integers(0, instance.n)
        neighbor.selection[idx_flip] = 1 - neighbor.selection[idx_flip]
        neighbor.evaluate(instance)
        return neighbor

    sa.neighborhood_function = custom_neighborhood
    initial = KnapsackSolution.empty(instance.n, instance)

    # Variables de tracking
    best_values_history = []
    acceptance_history = []
    temperature_history = []
    delta_e_history = []

    current = initial.copy()
    best = current.copy()
    T = sa.T0
    rng = sa.rng
    evaluations = 0

    def get_effective_value(sol):
        if sol.is_feasible:
            return sol.value
        else:
            excess = sol.weight - sol.problem.capacity
            return sol.value - excess * 1000

    while T > sa.T_min and evaluations < sa.max_evaluations:
        for _ in range(sa.iterations_per_temp):
            neighbor = sa.neighborhood_function(current, rng)
            evaluations += 1

            delta = get_effective_value(neighbor) - get_effective_value(current)
            delta_e_history.append(delta)

            accepted = False
            if delta > 0:
                accepted = True
                current = neighbor
            else:
                prob = np.exp(delta / T)
                if rng.random() < prob:
                    accepted = True
                    current = neighbor

            acceptance_history.append(1 if accepted else 0)
            temperature_history.append(T)

            if current.is_feasible and current.value > best.value:
                best = current.copy()

            best_values_history.append(best.value)

            if evaluations >= sa.max_evaluations:
                break

        T *= sa.alpha

    end_phase()

    print(f"   → SA completó {evaluations} evaluaciones")
    print(f"   → Historial: {len(best_values_history)} valores almacenados")

    # Estimar tiempo total
    time_per_low_dim = phase_times.get("Ejecución SA en 1 instancia low_dimensional (con tracking)", 0)
    estimated_low_dim_total = time_per_low_dim * len(low_dim_instances)

    print(f"\n📊 ESTIMACIONES:")
    print(f"   • Tiempo por instancia low_dim: {time_per_low_dim:.2f}s")
    print(f"   • Tiempo estimado para {len(low_dim_instances)} instancias low_dim: {estimated_low_dim_total:.2f}s")
    print(f"   • Tiempo estimado para {len(large_scale_instances)} instancias large_scale: [probablemente mayor]")

    total_elapsed = time.time() - total_start

    # Imprimir resumen
    print_summary()

    print(f"⏱️  Tiempo total del análisis: {total_elapsed:.2f}s")
    print()
