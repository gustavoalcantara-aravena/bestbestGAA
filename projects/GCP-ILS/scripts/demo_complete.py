"""
demo_complete.py - Demostración completa de ILS con múltiples instancias

Ejecuta ILS sobre un conjunto de instancias pequeñas y muestra resultados
"""

import sys
from pathlib import Path

# Agregar path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.loader import DataLoader
from core.evaluation import ColoringEvaluator
from metaheuristic.ils_core import IteratedLocalSearch
import numpy as np


def run_demo():
    """Ejecuta demostración completa"""
    
    print("="*70)
    print("Graph Coloring ILS - Complete Demo".center(70))
    print("="*70)
    print()
    
    # Cargar dataset
    loader = DataLoader()
    
    print("Available instances:")
    families = loader.get_available_families()
    for family in families:
        instances = loader.list_by_family(family)
        print(f"  {family}: {len(instances)} instances")
    
    print()
    print("="*70)
    print("Executing ILS on sample instances...".center(70))
    print("="*70)
    print()
    
    # Seleccionar instancias pequeñas para demo
    sample_instances = [
        'myciel3',
        'myciel4', 
        'myciel5',
        'le450_5a'
    ]
    
    results = []
    
    for instance_name in sample_instances:
        try:
            print(f"\n>>> Instance: {instance_name}")
            print("-" * 70)
            
            # Cargar instancia
            problem = loader.load(instance_name)
            print(f"  Graph: n={problem.n}, m={problem.m}, "
                  f"density={problem.density:.3f}")
            
            if problem.optimal_value:
                print(f"  Known optimal: k={problem.optimal_value}")
            
            # Ejecutar ILS
            ils = IteratedLocalSearch(
                problem=problem,
                constructive='dsatur',
                local_search='kempe',
                perturbation='random_recolor',
                max_iterations=200,
                perturbation_strength=0.2,
                restart_threshold=30,
                seed=42,
                verbose=False
            )
            
            best_solution, stats = ils.run()
            
            # Mostrar resultados
            print(f"  Result: k={stats['best_k']}")
            print(f"  Time: {stats['total_time']:.2f}s")
            print(f"  Iterations: {stats['iterations_completed']}")
            
            if problem.optimal_value:
                gap = best_solution.num_colors - problem.optimal_value
                gap_pct = gap / problem.optimal_value * 100
                print(f"  Gap: {gap} ({gap_pct:.1f}%)")
            
            # Validar factibilidad
            conflicts = best_solution.count_conflicts(problem)
            status = "✓ FEASIBLE" if conflicts == 0 else f"✗ {conflicts} conflicts"
            print(f"  Status: {status}")
            
            results.append({
                'instance': instance_name,
                'n': problem.n,
                'm': problem.m,
                'k_found': stats['best_k'],
                'k_optimal': problem.optimal_value,
                'time': stats['total_time'],
                'feasible': conflicts == 0
            })
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Resumen
    print()
    print("="*70)
    print("Summary".center(70))
    print("="*70)
    print()
    print(f"{'Instance':<12} {'n':>5} {'m':>6} {'k':>4} {'Opt':>4} {'Gap':>6} {'Time':>7}")
    print("-" * 70)
    
    for r in results:
        gap = "-"
        if r['k_optimal']:
            gap = f"{r['k_found']-r['k_optimal']:>5}"
        
        print(f"{r['instance']:<12} {r['n']:>5} {r['m']:>6} {r['k_found']:>4} "
              f"{str(r['k_optimal']):>4} {gap:>6} {r['time']:>6.2f}s")
    
    print()
    print("="*70)
    print()


def run_detailed_single():
    """Demostración detallada en una única instancia"""
    
    print("="*70)
    print("Detailed Analysis - Single Instance".center(70))
    print("="*70)
    print()
    
    loader = DataLoader()
    
    # Cargar instancia pequeña
    instance_name = 'CUL10'
    print(f"Loading {instance_name}...")
    problem = loader.load(instance_name)
    
    print(f"\nProblem Information:")
    print(f"  Vertices: {problem.n}")
    print(f"  Edges: {problem.m}")
    print(f"  Density: {problem.density:.4f}")
    print(f"  Max degree: {problem.max_degree}")
    print(f"  Min degree: {problem.min_degree}")
    print(f"  Avg degree: {problem.avg_degree:.2f}")
    
    if problem.optimal_value:
        print(f"  Optimal chromatic number: {problem.optimal_value}")
    
    print(f"  Lower bound: {problem.lower_bound}")
    print(f"  Upper bound (Δ+1): {problem.max_degree + 1}")
    
    # Ejecutar ILS con diferentes constructivos
    print()
    print("="*70)
    print(f"Testing different Constructive Operators on {instance_name}".center(70))
    print("="*70)
    print()
    
    constructives = ['dsatur', 'lf', 'sl', 'rlf']
    
    for const_name in constructives:
        print(f"\nConstructive: {const_name.upper()}")
        print("-" * 70)
        
        ils = IteratedLocalSearch(
            problem=problem,
            constructive=const_name,
            local_search='kempe',
            max_iterations=300,
            perturbation_strength=0.2,
            restart_threshold=40,
            seed=42,
            verbose=False
        )
        
        best_solution, stats = ils.run()
        
        print(f"  Final k: {stats['best_k']}")
        print(f"  Time: {stats['total_time']:.2f}s")
        print(f"  Iterations: {stats['iterations_completed']}")
        
        conflicts = best_solution.count_conflicts(problem)
        if conflicts == 0:
            print(f"  Status: ✓ FEASIBLE")
        else:
            print(f"  Status: ✗ {conflicts} CONFLICTS")
    
    print()
    print("="*70)
    print()


if __name__ == '__main__':
    # Ejecutar demo completa
    run_demo()
    
    # Ejecutar análisis detallado
    # Descomenta la siguiente línea para análisis detallado:
    # run_detailed_single()
