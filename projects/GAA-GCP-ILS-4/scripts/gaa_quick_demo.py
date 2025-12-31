#!/usr/bin/env python3
"""
Quick GAA Demo - GAA-GCP-ILS-4
Demostración rápida del sistema GAA funcionando
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import execute_algorithm
from core.problem import GraphColoringProblem
from data.loader import DatasetLoader


def main():
    print("\n" + "="*80)
    print("  DEMO RÁPIDA: GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA)")
    print("="*80 + "\n")
    
    # 1. Crear gramática
    print("1️⃣  CREAR GRAMÁTICA")
    print("-" * 80)
    grammar = Grammar(min_depth=2, max_depth=4)
    print(f"✅ Gramática creada")
    print(f"   • Terminales constructivos: {len(grammar.CONSTRUCTIVE_TERMINALS)}")
    print(f"   • Terminales mejora: {len(grammar.IMPROVEMENT_TERMINALS)}")
    print(f"   • Terminales perturbación: {len(grammar.PERTURBATION_TERMINALS)}")
    print()
    
    # 2. Crear generador
    print("2️⃣  CREAR GENERADOR")
    print("-" * 80)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    print(f"✅ Generador creado con seed=42\n")
    
    # 3. Generar 3 algoritmos aleatorios
    print("3️⃣  GENERAR 3 ALGORITMOS ALEATORIOS")
    print("-" * 80)
    
    algorithms = []
    for i in range(3):
        alg = generator.generate_with_validation()
        if alg:
            algorithms.append(alg)
            stats = grammar.get_statistics(alg)
            print(f"\n✅ Algoritmo {i+1}:")
            print(f"   Nodos: {stats['total_nodes']}, Profundidad: {stats['depth']}")
            print(f"   Pseudocódigo:")
            for line in alg.to_pseudocode(indent=0).split('\n'):
                print(f"     {line}")
    print()
    
    # 4. Cargar problema
    print("4️⃣  CARGAR INSTANCIA")
    print("-" * 80)
    loader = DatasetLoader(str(project_root))
    instances = loader.load_folder("training")
    
    if instances:
        problem = instances[0]
        print(f"✅ Instancia cargada: {problem.name}")
        print(f"   • Vértices: {problem.vertices}")
        print(f"   • Aristas: {problem.num_edges}")
        print(f"   • BKS: {problem.colors_known}\n")
    else:
        print("⚠️  No hay instancias de entrenamiento. Creando pequeño problema...")
        problem = GraphColoringProblem(
            vertices=10,
            edges=[(0,1), (0,2), (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5)],
            colors_known=3,
            name="test_small"
        )
        print(f"✅ Problema creado: {problem.name}\n")
    
    # 5. Ejecutar algoritmos
    print("5️⃣  EJECUTAR ALGORITMOS")
    print("-" * 80)
    
    for i, alg in enumerate(algorithms[:2]):  # Ejecutar primeros 2
        print(f"\nEjecutando Algoritmo {i+1}...")
        solution = execute_algorithm(alg, problem, seed=42)
        
        if solution:
            print(f"   • Colores: {solution.num_colors}")
            print(f"   • Conflictos: {solution.num_conflicts}")
            print(f"   • Factible: {'✓' if solution.is_feasible() else '✗'}")
            if problem.colors_known:
                gap = solution.num_colors - problem.colors_known
                gap_pct = 100 * gap / problem.colors_known if problem.colors_known > 0 else 0
                print(f"   • Gap respecto a BKS: +{gap} ({gap_pct:.1f}%)")
        else:
            print(f"   ✗ Error ejecutando algoritmo")
    
    print("\n" + "="*80)
    print("  ✅ DEMO COMPLETADA")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
