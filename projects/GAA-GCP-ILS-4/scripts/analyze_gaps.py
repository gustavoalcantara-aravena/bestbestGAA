#!/usr/bin/env python3
"""
analyze_gaps.py - Analiza los gaps de las soluciones encontradas

Compara las soluciones encontradas con los BKS conocidos.
"""

import sys
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports del proyecto
from core.problem import GraphColoringProblem
from core.evaluation import ColoringEvaluator
from metaheuristic.ils_core import IteratedLocalSearch
from operators.constructive import GreedyDSATUR
from operators.improvement import KempeChain
from operators.perturbation import RandomRecolor


def analyze_gaps():
    """Analiza gaps de las soluciones"""
    
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE GAPS")
    print("="*80 + "\n")
    
    # Datasets con BKS conocido
    test_datasets = [
        ("datasets/MYC/myciel3.col", 4),
        ("datasets/MYC/myciel4.col", 5),
        ("datasets/MYC/myciel5.col", 6),
        ("datasets/LEI/le450_5a.col", 5),
        ("datasets/LEI/le450_5b.col", 5),
    ]
    
    results = []
    
    for dataset_path, bks in test_datasets:
        dataset_file = project_root / dataset_path
        
        if not dataset_file.exists():
            print(f"⚠️  {dataset_path} - NO ENCONTRADO\n")
            continue
        
        problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
        
        # Ejecutar ILS
        ils = IteratedLocalSearch(
            problem=problem,
            constructive=GreedyDSATUR.construct,
            improvement=KempeChain.improve,
            perturbation=RandomRecolor.perturb,
            max_iterations=100,
            time_budget=30.0,
            verbose=False,
            seed=42
        )
        
        best_solution, history = ils.solve()
        metrics = ColoringEvaluator.evaluate(best_solution, problem)
        
        # Calcular gap
        colors_found = metrics['num_colors']
        gap = (colors_found - bks) / bks * 100
        
        feasible_icon = "✓" if metrics['feasible'] else "✗"
        gap_str = f"{gap:+.2f}%" if gap != 0 else "ÓPTIMO"
        
        print(f"{problem.name:<20} BKS: {bks} | Encontrado: {colors_found} | Gap: {gap_str} {feasible_icon}")
        
        results.append({
            'instance': problem.name,
            'bks': bks,
            'found': colors_found,
            'gap': gap,
            'feasible': metrics['feasible']
        })
    
    # Resumen
    print("\n" + "="*80)
    print("📈 RESUMEN DE GAPS")
    print("="*80 + "\n")
    
    gaps = [r['gap'] for r in results]
    feasible_count = sum(1 for r in results if r['feasible'])
    
    print(f"Instancias analizadas: {len(results)}")
    print(f"Instancias factibles: {feasible_count}/{len(results)}")
    print(f"\nGap promedio: {sum(gaps)/len(gaps):+.2f}%")
    print(f"Gap mínimo: {min(gaps):+.2f}%")
    print(f"Gap máximo: {max(gaps):+.2f}%")
    
    # Contar óptimos
    optimal = sum(1 for g in gaps if g == 0)
    print(f"\nSoluciones óptimas (gap=0%): {optimal}/{len(results)}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    analyze_gaps()
