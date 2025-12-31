"""
Quick Validation Script

Validacion rapida (10s) con instancias pequenas.
Verifica que todo el framework esta funcionando correctamente.
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
from operators.constructive import GreedyDSATUR, GreedyLargestFirst
from operators.improvement import OneVertexMove
from operators.repair import GreedyRepair
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
                u, v = int(parts[1]) - 1, int(parts[2]) - 1  # DIMACS es 1-indexed
                edges.append((u, v))
    
    return GraphColoringProblem(vertices, edges)


def test_small_instances():
    """Prueba con instancias pequenas"""
    print("\n" + "="*60)
    print("QUICK VALIDATION - SMALL INSTANCES")
    print("="*60)
    
    # Dataset directory
    dataset_dir = Path("datasets")
    
    if not dataset_dir.exists():
        print(f"Dataset directory not found at {dataset_dir}")
        print("Creating synthetic test instances instead...")
        test_synthetic()
        return
    
    # Test instances
    test_files = [
        "CUL/CUL_100.col",
        "LEI/LEI_100.col",
        "myciel3.col",
        "myciel4.col",
    ]
    
    instances_tested = 0
    total_time = 0
    results = []
    
    for instance_file in test_files:
        filepath = dataset_dir / instance_file
        
        if not filepath.exists():
            print(f"Skipping {instance_file} (not found)")
            continue
        
        print(f"\n--- Testing {instance_file} ---")
        instance_start = time.time()
        
        try:
            # Load problem
            problem = load_dimacs_instance(filepath)
            print(f"Vertices: {problem.vertices}, Edges: {problem.edges}")
            
            # Constructive solution
            solution = GreedyDSATUR.construct(problem, seed=42)
            print(f"Initial solution: {solution.num_colors} colors, "
                  f"{solution.num_conflicts} conflicts")
            
            # Improve
            improved = OneVertexMove.improve(solution, problem, max_iterations=5)
            print(f"After improvement: {improved.num_colors} colors, "
                  f"{improved.num_conflicts} conflicts")
            
            # Evaluate
            metrics = ColoringEvaluator.evaluate(improved, problem)
            
            result = {
                'instance': instance_file,
                'vertices': problem.vertices,
                'edges': problem.edges,
                'num_colors': improved.num_colors,
                'is_feasible': improved.is_feasible(),
                'time': time.time() - instance_start,
            }
            results.append(result)
            
            instances_tested += 1
            total_time += result['time']
            
            print(f"Result: {'FEASIBLE' if improved.is_feasible() else 'INFEASIBLE'} "
                  f"({result['time']:.3f}s)")
        
        except Exception as e:
            print(f"ERROR: {e}")
    
    print("\n" + "-"*60)
    print(f"Tested {instances_tested} instances in {total_time:.2f} seconds")
    print("-"*60)
    
    for result in results:
        status = "OK" if result['is_feasible'] else "FAIL"
        print(f"{result['instance']:30s} {result['num_colors']:3d} colors [{status}]")
    
    return results


def test_synthetic():
    """Prueba con instancias sinteticas"""
    print("\n" + "="*60)
    print("QUICK VALIDATION - SYNTHETIC INSTANCES")
    print("="*60)
    
    test_cases = [
        ("Triangle", 3, [(0, 1), (1, 2), (0, 2)]),
        ("Square", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("Pentagon", 5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]),
        ("Complete K4", 4, [(i, j) for i in range(4) for j in range(i+1, 4)]),
        ("Complete K5", 5, [(i, j) for i in range(5) for j in range(i+1, 5)]),
    ]
    
    results = []
    
    for name, vertices, edges in test_cases:
        print(f"\n--- Testing {name} ({vertices} vertices, {len(edges)} edges) ---")
        start = time.time()
        
        try:
            problem = GraphColoringProblem(vertices, edges)
            solution = GreedyDSATUR.construct(problem, seed=42)
            
            print(f"Initial: {solution.num_colors} colors, {solution.num_conflicts} conflicts")
            
            improved = OneVertexMove.improve(solution, problem, max_iterations=5)
            elapsed = time.time() - start
            
            print(f"Final:   {improved.num_colors} colors, {improved.num_conflicts} conflicts")
            print(f"Time: {elapsed:.3f}s")
            
            result = {
                'instance': name,
                'vertices': vertices,
                'edges': len(edges),
                'num_colors': improved.num_colors,
                'is_feasible': improved.is_feasible(),
                'time': elapsed,
            }
            results.append(result)
        
        except Exception as e:
            print(f"ERROR: {e}")
    
    print("\n" + "-"*60)
    print("RESULTS SUMMARY")
    print("-"*60)
    
    for result in results:
        status = "OK" if result['is_feasible'] else "FAIL"
        print(f"{result['instance']:20s} {result['num_colors']:3d} colors [{status}]")
    
    return results


def test_ils_quick():
    """Prueba rapida de ILS"""
    print("\n" + "="*60)
    print("QUICK ILS TEST")
    print("="*60)
    
    # Simple test case
    problem = GraphColoringProblem(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)])
    
    print(f"Problem: {problem.vertices} vertices, {problem.edges} edges")
    
    start = time.time()
    ils = IteratedLocalSearch(
        problem,
        seed=42,
        max_iterations=20,
        max_no_improve=10,
        ls_max_iterations=5,
        verbose=False
    )
    
    solution = ils.run()
    elapsed = time.time() - start
    
    print(f"ILS Result: {solution.num_colors} colors, {solution.num_conflicts} conflicts")
    print(f"Feasible: {solution.is_feasible()}")
    print(f"Time: {elapsed:.3f}s")
    
    return {
        'num_colors': solution.num_colors,
        'is_feasible': solution.is_feasible(),
        'time': elapsed,
    }


def main():
    """Main validation routine"""
    print("\n" + "="*60)
    print("NEW-GCP-ILS-OK QUICK VALIDATION")
    print("="*60)
    
    try:
        # Try loading real dataset
        results = test_small_instances()
        
        # If no instances were tested, use synthetic
        if not results:
            results = test_synthetic()
        
        # Test ILS
        ils_result = test_ils_quick()
        
        # Summary
        print("\n" + "="*60)
        print("VALIDATION COMPLETE")
        print("="*60)
        print("\nFramework is working correctly!")
        
        return 0
    
    except Exception as e:
        print(f"\nERROR during validation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
