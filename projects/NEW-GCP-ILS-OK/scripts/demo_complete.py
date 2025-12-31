"""
Complete Demo Script

Demo completo (30s) con instancias medianas.
Muestra capacidades del framework ILS con configuracion tunned.
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
from operators.constructive import GreedyDSATUR, GreedyLargestFirst, RandomSequential
from operators.improvement import OneVertexMove, TabuColMove
from metaheuristic.ils_core import IteratedLocalSearch


def load_dimacs_instance(filepath):
    """Carga instancia en formato DIMACS .col"""
    vertices = 0
    edges = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            
            parts = line.split()
            if parts[0] == 'p':
                vertices = int(parts[2])
            elif parts[0] == 'e':
                u, v = int(parts[1]) - 1, int(parts[2]) - 1
                edges.append((u, v))
    
    return GraphColoringProblem(vertices, edges)


def load_bks_data():
    """Carga datos de Best Known Solutions"""
    bks_file = Path("datasets/BKS.json")
    
    if bks_file.exists():
        with open(bks_file, 'r') as f:
            return json.load(f)
    
    return {}


def demo_single_instance(problem, instance_name, bks_value=None, time_limit=10):
    """Demo en una instancia individual"""
    print(f"\n{'='*60}")
    print(f"Instance: {instance_name}")
    print(f"{'='*60}")
    print(f"Problem: {problem.vertices} vertices, {problem.edges} edges")
    print(f"Density: {problem.density:.3f}")
    print(f"Max degree: {problem.max_degree}, Avg degree: {problem.avg_degree:.2f}")
    
    if bks_value:
        print(f"BKS: {bks_value} colors")
    
    # Run ILS with multiple random starts
    print(f"\nRunning ILS (time limit: {time_limit}s)...")
    
    best_solution = None
    best_fitness = float('inf')
    total_time = 0
    run_count = 0
    
    while total_time < time_limit:
        start = time.time()
        
        # Random seed for diversity
        seed = run_count
        
        ils = IteratedLocalSearch(
            problem,
            seed=seed,
            max_iterations=100,
            max_no_improve=30,
            ls_max_iterations=20,
            perturbation_strength=0.15,
            use_adaptive_perturbation=True,
            verbose=False
        )
        
        solution = ils.run()
        elapsed = time.time() - start
        total_time += elapsed
        
        if solution.fitness() < best_fitness:
            best_solution = solution
            best_fitness = solution.fitness()
            
            gap = ""
            if bks_value:
                gap_val = solution.num_colors - bks_value
                gap = f" (gap to BKS: {gap_val:+d})"
            
            print(f"  Run {run_count+1}: {solution.num_colors} colors, "
                  f"{solution.num_conflicts} conflicts [{elapsed:.2f}s]{gap}")
        
        run_count += 1
    
    # Final statistics
    print(f"\n--- RESULTS ---")
    print(f"Best solution: {best_solution.num_colors} colors")
    print(f"Feasible: {best_solution.is_feasible()}")
    print(f"Conflicts: {best_solution.num_conflicts}")
    print(f"Total time: {total_time:.2f}s, Runs: {run_count}")
    
    if bks_value:
        gap = best_solution.num_colors - bks_value
        gap_pct = (gap / bks_value * 100) if bks_value > 0 else 0
        print(f"Gap to BKS: {gap:+d} ({gap_pct:+.1f}%)")
    
    return {
        'instance': instance_name,
        'vertices': problem.vertices,
        'edges': problem.edges,
        'best_num_colors': best_solution.num_colors,
        'best_conflicts': best_solution.num_conflicts,
        'is_feasible': best_solution.is_feasible(),
        'total_time': total_time,
        'runs': run_count,
        'bks': bks_value,
        'gap': (best_solution.num_colors - bks_value) if bks_value else None,
    }


def demo_comparison():
    """Comparacion de diferentes constructivos"""
    print(f"\n{'='*60}")
    print("OPERATOR COMPARISON")
    print(f"{'='*60}")
    
    # Create test problem
    problem = GraphColoringProblem(
        20,
        [(i, (i+np.random.randint(1, 7)) % 20) for i in range(20)]
    )
    
    print(f"Problem: {problem.vertices} vertices, {problem.edges} edges\n")
    
    operators = [
        ("Greedy DSATUR", GreedyDSATUR()),
        ("Greedy Largest First", GreedyLargestFirst()),
        ("Random Sequential", RandomSequential()),
    ]
    
    results = []
    
    for name, operator in operators:
        start = time.time()
        solution = operator.construct(problem, seed=42)
        elapsed = time.time() - start
        
        print(f"{name:25s} -> {solution.num_colors} colors "
              f"({solution.num_conflicts} conflicts) [{elapsed:.3f}s]")
        
        results.append({
            'operator': name,
            'colors': solution.num_colors,
            'conflicts': solution.num_conflicts,
            'time': elapsed,
        })
    
    return results


def demo_improvement_operators():
    """Demostracion de operadores de mejora"""
    print(f"\n{'='*60}")
    print("IMPROVEMENT OPERATORS")
    print(f"{'='*60}")
    
    # Create problem
    problem = GraphColoringProblem(
        15,
        [(i, (i+np.random.randint(1, 6)) % 15) for i in range(15)]
    )
    
    # Initial solution
    initial = GreedyDSATUR.construct(problem, seed=42)
    initial_fitness = initial.fitness()
    
    print(f"Problem: {problem.vertices} vertices, {problem.edges} edges")
    print(f"Initial solution: {initial.num_colors} colors, "
          f"fitness = {initial_fitness:.1f}\n")
    
    operators = [
        ("One Vertex Move", OneVertexMove()),
    ]
    
    results = []
    
    for name, operator in operators:
        start = time.time()
        
        if hasattr(operator, 'improve'):
            improved = operator.improve(initial, problem, max_iterations=50)
        else:
            improved = initial
        
        elapsed = time.time() - start
        improvement = initial_fitness - improved.fitness()
        improvement_pct = (improvement / initial_fitness * 100) if initial_fitness > 0 else 0
        
        print(f"{name:25s} -> {improved.num_colors} colors, "
              f"fitness = {improved.fitness():.1f} "
              f"[improvement: {improvement:+.1f} ({improvement_pct:+.1f}%)]")
        
        results.append({
            'operator': name,
            'colors': improved.num_colors,
            'fitness': improved.fitness(),
            'improvement': improvement,
            'time': elapsed,
        })
    
    return results


def main():
    """Main demo"""
    print("\n" + "="*60)
    print("NEW-GCP-ILS-OK - COMPLETE DEMO")
    print("="*60)
    
    # Load BKS data
    bks_data = load_bks_data()
    
    # Demo on dataset instances
    demo_results = []
    
    dataset_dir = Path("datasets")
    
    if dataset_dir.exists():
        # Test with real dataset instances
        instances = [
            ("CUL/CUL_100.col", 5),
            ("LEI/LEI_100.col", 5),
            ("DSJC125.col", 10),
        ]
        
        for instance_file, time_limit in instances:
            filepath = dataset_dir / instance_file
            
            if filepath.exists():
                try:
                    problem = load_dimacs_instance(filepath)
                    
                    # Get BKS if available
                    instance_key = instance_file.replace(".col", "")
                    bks = bks_data.get(instance_key)
                    
                    result = demo_single_instance(problem, instance_file, bks, time_limit)
                    demo_results.append(result)
                
                except Exception as e:
                    print(f"Error with {instance_file}: {e}")
    
    # If no dataset instances, use synthetic
    if not demo_results:
        print("\nNo dataset instances found, using synthetic instances...")
        
        # Synthetic instances
        instances = [
            ("Random 20", GraphColoringProblem(20, [(i, (i+np.random.randint(1, 7)) % 20) 
                                                     for i in range(20)]), None),
        ]
        
        for name, problem, bks in instances:
            result = demo_single_instance(problem, name, bks, time_limit=5)
            demo_results.append(result)
    
    # Comparison demos
    print("\n" + "="*60)
    comp_results = demo_comparison()
    
    print("\n" + "="*60)
    imp_results = demo_improvement_operators()
    
    # Summary
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nFramework capabilities demonstrated:")
    print("- Multiple constructive operators")
    print("- Local search improvement")
    print("- Iterated Local Search metaheuristic")
    print("- Support for DIMACS benchmark instances")
    
    return 0


if __name__ == '__main__':
    exit(main())
