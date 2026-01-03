#!/usr/bin/env python3
"""
ITER-4 Experiment: C2 Family Optimization
Compares ITER-3 (NearestNeighbor) vs ITER-4 (AdaptiveConstructor) on C2 instances

Purpose: 
Test if RandomizedInsertion constructor improves clustered long-horizon instances

Instances: C201, C202, C203, C204, C205, C206, C207, C208 (8 total)
Algorithms: Algo2 ITER-3 vs Algo2 ITER-4
Duration: ~2-3 minutes
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.loader import SolomonLoader
from src.gaa.algorithm_generator import AlgorithmGenerator
from src.gaa.interpreter import ASTInterpreter
from src.gaa.ast_nodes import Seq, GreedyConstruct, While, LocalSearch, Perturbation


def create_algo2_iter3():
    """Create Algoritmo 2 ITER-3 (baseline: NearestNeighbor)"""
    return Seq(body=[
        GreedyConstruct(heuristic='NearestNeighbor'),
        While(
            max_iterations=80,
            body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=50),
                Perturbation(operator='DoubleBridge', strength=3),
                LocalSearch(operator='TwoOpt', max_iterations=35),
                LocalSearch(operator='Relocate', max_iterations=20)
            ])
        )
    ])


def create_algo2_iter4():
    """Create Algoritmo 2 ITER-4 (adaptive: RandomizedInsertion for C2)"""
    return Seq(body=[
        # ITER-4: AdaptiveConstructor que elige según familia
        GreedyConstruct(
            heuristic='AdaptiveConstructor',
            metadata={
                'default': 'NearestNeighbor',
                'clustered': 'RandomizedInsertion',
                'randomness': 0.25
            }
        ),
        While(
            max_iterations=100,  # +20 iteraciones
            body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=60),  # +10
                Perturbation(operator='DoubleBridge', strength=3),
                LocalSearch(operator='TwoOpt', max_iterations=35),
                LocalSearch(operator='Relocate', max_iterations=20)
            ])
        )
    ])


def run_iter4_c2_experiment():
    """
    Run ITER-4 experiment on C2 family only
    """
    
    print("=" * 80)
    print("ITER-4 EXPERIMENT: C2 Family Optimization (Clustered Long-Horizon)")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load instances
    loader = SolomonLoader()
    c2_instances = ['C201', 'C202', 'C203', 'C204', 'C205', 'C206', 'C207', 'C208']
    
    print(f"📊 Loading {len(c2_instances)} C2 instances...")
    instances = {}
    for instance_name in c2_instances:
        try:
            instance = loader.load_instance(f'datasets/C2/{instance_name}.csv')
            instances[instance_name] = instance
            print(f"  ✓ {instance_name}: {len(instance.customers)} customers")
        except Exception as e:
            print(f"  ✗ {instance_name}: ERROR - {e}")
            return False
    
    print(f"\n✅ Loaded {len(instances)}/{len(c2_instances)} instances")
    
    # Create interpreter
    interpreter = ASTInterpreter()
    
    # Create algorithms
    print("\n🔧 Creating algorithms...")
    algo2_iter3 = create_algo2_iter3()
    algo2_iter4 = create_algo2_iter4()
    print("  ✓ Algo2 ITER-3 (baseline: NearestNeighbor)")
    print("  ✓ Algo2 ITER-4 (adaptive: RandomizedInsertion for C)")
    
    # Run experiments
    results = {
        'timestamp': datetime.now().isoformat(),
        'experiment': 'ITER-4 C2 Optimization',
        'instances': c2_instances,
        'results_by_instance': {}
    }
    
    print(f"\n{'='*80}")
    print("RUNNING EXPERIMENTS")
    print(f"{'='*80}\n")
    
    all_results = []
    
    for instance_name in c2_instances:
        instance = instances[instance_name]
        
        print(f"📍 Instance: {instance_name}")
        print(f"   Customers: {len(instance.customers)}")
        
        # Run ITER-3
        print(f"   Running Algo2 ITER-3...", end=' ', flush=True)
        start_time = time.time()
        try:
            solution_iter3 = interpreter.execute(algo2_iter3, instance)
            time_iter3 = time.time() - start_time
            distance_iter3 = solution_iter3.total_distance
            vehicles_iter3 = len(solution_iter3.routes)
            print(f"✓ D={distance_iter3:.2f}, K={vehicles_iter3}, t={time_iter3:.2f}s")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            distance_iter3 = None
            vehicles_iter3 = None
            time_iter3 = None
        
        # Run ITER-4
        print(f"   Running Algo2 ITER-4...", end=' ', flush=True)
        start_time = time.time()
        try:
            solution_iter4 = interpreter.execute(algo2_iter4, instance)
            time_iter4 = time.time() - start_time
            distance_iter4 = solution_iter4.total_distance
            vehicles_iter4 = len(solution_iter4.routes)
            print(f"✓ D={distance_iter4:.2f}, K={vehicles_iter4}, t={time_iter4:.2f}s")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            distance_iter4 = None
            vehicles_iter4 = None
            time_iter4 = None
        
        # Calculate improvement
        if distance_iter3 is not None and distance_iter4 is not None:
            improvement = distance_iter3 - distance_iter4
            improvement_pct = (improvement / distance_iter3) * 100
            status = "✅ MEJOR" if improvement > 0 else "❌ PEOR"
            print(f"   {status}: Mejora = {improvement:.2f} ({improvement_pct:+.2f}%)")
        
        print()
        
        # Store results
        all_results.append({
            'instance': instance_name,
            'distance_iter3': distance_iter3,
            'distance_iter4': distance_iter4,
            'vehicles_iter3': vehicles_iter3,
            'vehicles_iter4': vehicles_iter4,
            'time_iter3': time_iter3,
            'time_iter4': time_iter4,
            'improvement': improvement if distance_iter3 and distance_iter4 else None,
            'improvement_pct': improvement_pct if distance_iter3 and distance_iter4 else None
        })
        
        results['results_by_instance'][instance_name] = all_results[-1]
    
    # Summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()
    
    # Filter valid results
    valid_results = [r for r in all_results if r['distance_iter3'] and r['distance_iter4']]
    
    if valid_results:
        print(f"{'Métrica':<30} {'ITER-3':<15} {'ITER-4':<15} {'Mejora':<15}")
        print("-" * 75)
        
        avg_iter3 = sum(r['distance_iter3'] for r in valid_results) / len(valid_results)
        avg_iter4 = sum(r['distance_iter4'] for r in valid_results) / len(valid_results)
        avg_improvement = avg_iter3 - avg_iter4
        avg_improvement_pct = (avg_improvement / avg_iter3) * 100
        
        print(f"{'Promedio Distancia':<30} {avg_iter3:<15.2f} {avg_iter4:<15.2f} {avg_improvement:+15.2f} ({avg_improvement_pct:+.2f}%)")
        
        min_iter3 = min(r['distance_iter3'] for r in valid_results)
        min_iter4 = min(r['distance_iter4'] for r in valid_results)
        print(f"{'Mínimo Distancia':<30} {min_iter3:<15.2f} {min_iter4:<15.2f}")
        
        max_iter3 = max(r['distance_iter3'] for r in valid_results)
        max_iter4 = max(r['distance_iter4'] for r in valid_results)
        print(f"{'Máximo Distancia':<30} {max_iter3:<15.2f} {max_iter4:<15.2f}")
        
        # Standard deviation
        import statistics
        std_iter3 = statistics.stdev([r['distance_iter3'] for r in valid_results])
        std_iter4 = statistics.stdev([r['distance_iter4'] for r in valid_results])
        print(f"{'Desv. Est. Distancia':<30} {std_iter3:<15.2f} {std_iter4:<15.2f}")
        
        # Count improvements
        improvements_count = sum(1 for r in valid_results if r['improvement'] > 0)
        print(f"{'Instancias Mejoradas':<30} {improvements_count:<15}/{len(valid_results)}")
        
        # Average time
        avg_time_iter3 = sum(r['time_iter3'] for r in valid_results) / len(valid_results)
        avg_time_iter4 = sum(r['time_iter4'] for r in valid_results) / len(valid_results)
        print(f"{'Promedio Tiempo (s)':<30} {avg_time_iter3:<15.2f} {avg_time_iter4:<15.2f}")
    
    # Hypothesis test
    print()
    print("=" * 80)
    print("HYPOTHESIS TEST")
    print("=" * 80)
    print()
    
    improvements = [r['improvement_pct'] for r in valid_results if r['improvement_pct'] is not None]
    avg_improvement_pct = sum(improvements) / len(improvements) if improvements else 0
    
    print(f"H0 (Nula): Constructor RandomizedInsertion NO mejora C2 significativamente")
    print(f"H1 (Alternativa): Constructor RandomizedInsertion MEJORA C2 (> 15% reducción)")
    print()
    print(f"Promedio mejora observado: {avg_improvement_pct:+.2f}%")
    print()
    
    if avg_improvement_pct > 15:
        print("✅ RESULTADO: ÉXITO - Rechazar H0, aceptar H1")
        print("   Constructor adaptativo es EFECTIVO para C2")
        print("   Recomendación: Usar ITER-4 en producción")
    elif avg_improvement_pct > 5:
        print("⚠️ RESULTADO: ÉXITO PARCIAL - Mejora moderada")
        print("   Constructor adaptativo ayuda pero no resuelve completamente")
        print("   Recomendación: Investigación adicional (ITER-5)")
    else:
        print("❌ RESULTADO: FRACASO - No hay mejora significativa")
        print("   Constructor adaptativo no funciona para C2")
        print("   Recomendación: Aceptar limitación, especialidad en R/RC")
    
    print()
    
    # Save results
    output_dir = Path('output') / f'ITER4_C2_{datetime.now().strftime("%d-%m-%y_%H-%M-%S")}'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    results_json = output_dir / 'iter4_results.json'
    with open(results_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved: {results_json}")
    
    # Save CSV
    import csv
    results_csv = output_dir / 'iter4_results.csv'
    with open(results_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Instance', 'Distance_ITER3', 'Distance_ITER4', 'Improvement', 'Improvement_%', 
                        'Vehicles_ITER3', 'Vehicles_ITER4', 'Time_ITER3', 'Time_ITER4'])
        for r in all_results:
            writer.writerow([
                r['instance'],
                f"{r['distance_iter3']:.2f}" if r['distance_iter3'] else '',
                f"{r['distance_iter4']:.2f}" if r['distance_iter4'] else '',
                f"{r['improvement']:.2f}" if r['improvement'] else '',
                f"{r['improvement_pct']:.2f}" if r['improvement_pct'] else '',
                r['vehicles_iter3'],
                r['vehicles_iter4'],
                f"{r['time_iter3']:.2f}" if r['time_iter3'] else '',
                f"{r['time_iter4']:.2f}" if r['time_iter4'] else '',
            ])
    print(f"💾 CSV saved: {results_csv}")
    
    print()
    print("=" * 80)
    print("ITER-4 EXPERIMENT COMPLETE")
    print("=" * 80)
    
    return True


if __name__ == '__main__':
    try:
        run_iter4_c2_experiment()
    except Exception as e:
        print(f"\n❌ EXPERIMENT FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
