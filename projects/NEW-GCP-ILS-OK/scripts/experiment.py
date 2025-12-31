"""
Experimentation Script

Script extendido (5+ minutos) para experimentacion completa.
Realiza multiples runs con diferentes configuraciones y registra resultados.
"""

import os
import json
import csv
import time
import numpy as np
from pathlib import Path
from datetime import datetime
from core.problem import GraphColoringProblem
from core.evaluation import ColoringEvaluator
from metaheuristic.ils_core import IteratedLocalSearch, HybridILS
from metaheuristic.schedules import (
    ConstantPerturbation,
    LinearDecayPerturbation,
    ExponentialDecayPerturbation,
)


def load_dimacs_instance(filepath):
    """Carga instancia en formato DIMACS"""
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


def run_experiment(problem, instance_name, config, seed, bks=None):
    """
    Ejecuta un experimento individual
    
    Returns:
        Diccionario con resultados
    """
    start = time.time()
    
    try:
        # Create ILS instance with config
        ils = IteratedLocalSearch(
            problem,
            seed=seed,
            max_iterations=config['max_iterations'],
            max_no_improve=config['max_no_improve'],
            ls_max_iterations=config['ls_max_iterations'],
            perturbation_strength=config['perturbation_strength'],
            use_adaptive_perturbation=config['use_adaptive_perturbation'],
            verbose=False
        )
        
        # Run
        solution = ils.run()
        elapsed = time.time() - start
        
        # Calculate metrics
        gap = None
        gap_pct = None
        if bks:
            gap = solution.num_colors - bks
            gap_pct = (gap / bks * 100) if bks > 0 else 0
        
        result = {
            'instance': instance_name,
            'seed': seed,
            'vertices': problem.vertices,
            'edges': problem.edges,
            'density': problem.density,
            'max_iterations': config['max_iterations'],
            'num_colors': solution.num_colors,
            'num_conflicts': solution.num_conflicts,
            'is_feasible': solution.is_feasible(),
            'fitness': solution.fitness(),
            'time': elapsed,
            'bks': bks,
            'gap': gap,
            'gap_pct': gap_pct,
        }
        
        return result
    
    except Exception as e:
        return {
            'instance': instance_name,
            'seed': seed,
            'error': str(e),
        }


def load_bks_data():
    """Carga BKS"""
    bks_file = Path("datasets/BKS.json")
    
    if bks_file.exists():
        with open(bks_file, 'r') as f:
            return json.load(f)
    
    return {}


def main():
    """Experimento principal"""
    print("\n" + "="*70)
    print("NEW-GCP-ILS-OK EXPERIMENTATION")
    print("="*70)
    
    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Load BKS
    bks_data = load_bks_data()
    
    # Configurations to test
    configs = [
        {
            'name': 'Fast',
            'max_iterations': 50,
            'max_no_improve': 20,
            'ls_max_iterations': 10,
            'perturbation_strength': 0.2,
            'use_adaptive_perturbation': False,
        },
        {
            'name': 'Balanced',
            'max_iterations': 100,
            'max_no_improve': 40,
            'ls_max_iterations': 20,
            'perturbation_strength': 0.15,
            'use_adaptive_perturbation': True,
        },
        {
            'name': 'Thorough',
            'max_iterations': 200,
            'max_no_improve': 80,
            'ls_max_iterations': 40,
            'perturbation_strength': 0.1,
            'use_adaptive_perturbation': True,
        },
    ]
    
    # Test instances
    dataset_dir = Path("datasets")
    test_instances = []
    
    if dataset_dir.exists():
        # Real instances
        instance_files = [
            "myciel3.col",
            "myciel4.col",
            "CUL/CUL_100.col",
            "LEI/LEI_100.col",
            "DSJC125.col",
        ]
        
        for instance_file in instance_files:
            filepath = dataset_dir / instance_file
            if filepath.exists():
                problem = load_dimacs_instance(filepath)
                instance_key = instance_file.replace(".col", "").replace("/", "_")
                bks = bks_data.get(instance_key)
                test_instances.append((instance_file, problem, bks))
    
    # Synthetic instances if no dataset
    if not test_instances:
        print("Creating synthetic test instances...")
        
        for size in [10, 15, 20]:
            np.random.seed(42)
            edges = []
            for i in range(size):
                for _ in range(np.random.randint(2, 6)):
                    j = np.random.randint(0, size)
                    if i != j and (i, j) not in edges and (j, i) not in edges:
                        edges.append((i, j))
            
            problem = GraphColoringProblem(size, edges)
            test_instances.append((f"Synthetic_{size}", problem, None))
    
    print(f"\nTest instances: {len(test_instances)}")
    print(f"Configurations: {len(configs)}")
    print(f"Seeds per config: 3")
    print(f"Total experiments: {len(test_instances) * len(configs) * 3}\n")
    
    # Run experiments
    all_results = []
    total_experiments = len(test_instances) * len(configs) * 3
    current_experiment = 0
    
    for instance_name, problem, bks in test_instances:
        print(f"\nInstance: {instance_name} ({problem.vertices}v, {problem.edges}e)")
        
        for config in configs:
            print(f"  Config: {config['name']:10s}", end=' ')
            
            config_results = []
            config_times = []
            
            for seed in [42, 123, 456]:
                current_experiment += 1
                
                result = run_experiment(problem, instance_name, config, seed, bks)
                all_results.append(result)
                config_results.append(result)
                config_times.append(result.get('time', 0))
            
            # Summary for this config
            feasibles = sum(1 for r in config_results if r.get('is_feasible', False))
            avg_colors = np.mean([r['num_colors'] for r in config_results])
            avg_time = np.mean(config_times)
            
            print(f"Colors: {avg_colors:.1f}, Feasible: {feasibles}/3, "
                  f"Time: {avg_time:.2f}s")
    
    # Save results to CSV
    csv_file = results_dir / f"experiment_results_{timestamp}.csv"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
    
    print(f"\nResults saved to {csv_file}")
    
    # Print summary statistics
    print("\n" + "="*70)
    print("EXPERIMENT SUMMARY")
    print("="*70)
    
    # Group by instance
    by_instance = {}
    for result in all_results:
        instance = result.get('instance')
        if instance not in by_instance:
            by_instance[instance] = []
        by_instance[instance].append(result)
    
    print("\nBest results by instance:")
    print(f"{'Instance':30s} {'Colors':>8s} {'Feasible':>10s} {'Gap':>8s}")
    print("-" * 60)
    
    for instance in sorted(by_instance.keys()):
        results_for_instance = by_instance[instance]
        
        # Filter feasible solutions
        feasible = [r for r in results_for_instance if r.get('is_feasible', False)]
        
        if feasible:
            best = min(feasible, key=lambda r: r['num_colors'])
            gap_str = f"{best['gap']:+d}" if best['gap'] is not None else "N/A"
            print(f"{instance:30s} {best['num_colors']:>8d} {'Yes':>10s} {gap_str:>8s}")
        else:
            print(f"{instance:30s} {'N/A':>8s} {'No':>10s} {'N/A':>8s}")
    
    print("\nExperimentation complete!")
    
    return 0


if __name__ == '__main__':
    exit(main())
