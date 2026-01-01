#!/usr/bin/env python3
"""
debug_convergence.py - Debug de datos de convergencia

Verifica qué datos se están capturando en el historial de convergencia.
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


def debug_convergence():
    """Debug de convergencia"""
    
    print("\n" + "="*80)
    print("🔍 DEBUG DE CONVERGENCIA")
    print("="*80 + "\n")
    
    # Cargar problema pequeño
    dataset_file = project_root / "datasets/MYC/myciel3.col"
    problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
    
    print(f"Problema: {problem.name}")
    print(f"Vértices: {problem.n_vertices}")
    print(f"Aristas: {problem.n_edges}\n")
    
    # Ejecutar ILS con verbose
    print("Ejecutando ILS con verbose=True...\n")
    ils = IteratedLocalSearch(
        problem=problem,
        constructive=GreedyDSATUR.construct,
        improvement=KempeChain.improve,
        perturbation=RandomRecolor.perturb,
        max_iterations=50,
        time_budget=30.0,
        verbose=True,
        seed=42
    )
    
    best_solution, history = ils.solve()
    
    print("\n" + "="*80)
    print("📊 DATOS DE CONVERGENCIA")
    print("="*80 + "\n")
    
    print(f"Tipo de history: {type(history)}")
    print(f"Atributos de history: {dir(history)}\n")
    
    print(f"history.num_colors (primeros 20): {history.num_colors[:20]}")
    print(f"Longitud de history.num_colors: {len(history.num_colors)}\n")
    
    print(f"history.best_fitness (primeros 20): {history.best_fitness[:20]}")
    print(f"Longitud de history.best_fitness: {len(history.best_fitness)}\n")
    
    print(f"history.current_fitness (primeros 20): {history.current_fitness[:20]}")
    print(f"Longitud de history.current_fitness: {len(history.current_fitness)}\n")
    
    print(f"history.iterations (primeros 20): {history.iterations[:20]}")
    print(f"Longitud de history.iterations: {len(history.iterations)}\n")
    
    # Verificar si hay variación
    if len(history.num_colors) > 1:
        min_colors = min(history.num_colors)
        max_colors = max(history.num_colors)
        print(f"Rango de num_colors: {min_colors} - {max_colors}")
        print(f"Variación: {max_colors - min_colors}")
    else:
        print("⚠️  Solo hay 1 o 0 valores en history.num_colors")
    
    # Evaluar solución final
    metrics = ColoringEvaluator.evaluate(best_solution, problem)
    print(f"\nSolución final: {metrics['num_colors']} colores")
    print(f"Conflictos: {metrics['conflicts']}")
    print(f"Factible: {metrics['feasible']}")


if __name__ == "__main__":
    debug_convergence()
