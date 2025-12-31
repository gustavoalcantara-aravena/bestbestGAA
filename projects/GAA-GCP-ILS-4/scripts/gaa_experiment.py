#!/usr/bin/env python3
"""
GAA Experiment - GAA-GCP-ILS-4
Script de experimentación para evolucionar algoritmos ILS
mediante Generación Automática de Algoritmos (GAA)

Uso:
    python scripts/gaa_experiment.py [opciones]
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

import numpy as np

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports del proyecto
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import execute_algorithm
from gaa.ast_nodes import mutate_ast
from core.problem import GraphColoringProblem
from data.loader import DatasetLoader


class GAASolver:
    """Solucionador usando Generación Automática de Algoritmos"""
    
    def __init__(self, 
                 training_dir: str = "datasets/training",
                 pop_size: int = 10,
                 generations: int = 50,
                 seed: int = 42):
        """
        Inicializa solucionador GAA
        
        Args:
            training_dir: Directorio de instancias de entrenamiento
            pop_size: Tamaño de población de algoritmos
            generations: Número de generaciones
            seed: Semilla aleatoria
        """
        self.training_dir = Path(training_dir)
        self.pop_size = pop_size
        self.generations = generations
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        # Cargar instancias de entrenamiento
        print(f"📁 Cargando instancias de entrenamiento desde {training_dir}...")
        loader = DatasetLoader(str(project_root))
        self.training_instances = loader.load_folder("training")
        print(f"✅ {len(self.training_instances)} instancias cargadas\n")
        
        # Inicializar generador
        self.grammar = Grammar(min_depth=2, max_depth=5)
        self.generator = AlgorithmGenerator(grammar=self.grammar, seed=seed)
        
        # Historial de evolución
        self.history = []
    
    def evaluate_algorithm(self, algorithm) -> float:
        """
        Evalúa un algoritmo en múltiples instancias
        
        Fitness = promedio de colores en instancias de entrenamiento
        (menor es mejor)
        
        Args:
            algorithm: AST del algoritmo
        
        Returns:
            Fitness (promedio de colores)
        """
        if not self.training_instances:
            return float('inf')
        
        values = []
        
        for instance in self.training_instances:
            try:
                # Ejecutar algoritmo
                solution = execute_algorithm(
                    algorithm,
                    instance,
                    seed=self.rng.integers(0, 2**31)
                )
                
                if solution:
                    values.append(solution.num_colors)
            except Exception as e:
                pass  # Saltar instancias problemáticas
        
        if not values:
            return float('inf')
        
        # Fitness = promedio
        fitness = np.mean(values)
        return fitness
    
    def evolve(self) -> Tuple[Any, float]:
        """
        Evoluciona algoritmos usando Simulated Annealing
        
        Returns:
            (mejor_algoritmo, mejor_fitness)
        """
        print("="*80)
        print("  EVOLUCIÓN DE ALGORITMOS (GAA)")
        print("="*80)
        print()
        
        # Generar población inicial
        print(f"🧬 Generando población inicial ({self.pop_size} algoritmos)...\n")
        
        population = self.generator.generate_population(self.pop_size)
        fitnesses = []
        
        start_time = time.time()
        
        for i, alg in enumerate(population):
            fitness = self.evaluate_algorithm(alg)
            fitnesses.append(fitness)
            print(f"  Algoritmo {i+1:2d}: fitness = {fitness:.2f}")
        
        print()
        
        # Encontrar mejor inicial
        best_idx = np.argmin(fitnesses)
        best_algorithm = population[best_idx]
        best_fitness = fitnesses[best_idx]
        
        print(f"✅ Mejor inicial: fitness = {best_fitness:.2f}\n")
        
        # Parámetros de Simulated Annealing
        T_initial = 100.0
        T_final = 0.1
        cooling_rate = (T_final / T_initial) ** (1 / self.generations)
        T = T_initial
        
        # Evolución
        for gen in range(self.generations):
            print(f"Generación {gen+1:3d}/{self.generations} (T={T:.2f}):")
            
            # Seleccionar algoritmo actual
            current_idx = self.rng.integers(0, len(population))
            current_alg = population[current_idx]
            current_fitness = fitnesses[current_idx]
            
            # Mutar
            try:
                mutated_alg = mutate_ast(current_alg, mutation_rate=0.3)
            except:
                mutated_alg = current_alg
            
            # Evaluar mutante
            mutated_fitness = self.evaluate_algorithm(mutated_alg)
            
            # Criterio de aceptación (SA)
            delta_f = mutated_fitness - current_fitness
            
            if delta_f < 0:  # Mejora
                accept = True
            else:  # Empeora
                if T > 0:
                    prob = np.exp(-delta_f / T)
                    accept = self.rng.random() < prob
                else:
                    accept = False
            
            if accept:
                population[current_idx] = mutated_alg
                fitnesses[current_idx] = mutated_fitness
                
                print(f"  ✓ Aceptado ({'mejora' if delta_f < 0 else 'empeora'})")
                
                # Actualizar mejor global
                if mutated_fitness < best_fitness:
                    best_algorithm = mutated_alg
                    best_fitness = mutated_fitness
                    print(f"  ✨ NUEVO MEJOR: fitness = {best_fitness:.2f}")
            else:
                print(f"  ✗ Rechazado")
            
            # Registrar estadísticas
            self.history.append({
                'generation': gen + 1,
                'temperature': T,
                'best_fitness': best_fitness,
                'current_fitness': current_fitness,
                'mutated_fitness': mutated_fitness,
                'accepted': accept
            })
            
            # Enfriar
            T *= cooling_rate
            print()
        
        elapsed = time.time() - start_time
        
        print("="*80)
        print(f"✅ EVOLUCIÓN COMPLETADA")
        print(f"   Mejor fitness: {best_fitness:.2f}")
        print(f"   Tiempo total: {elapsed:.1f}s")
        print("="*80)
        print()
        
        return best_algorithm, best_fitness
    
    def print_algorithm(self, algorithm, name: str = "Algoritmo"):
        """Imprime estructura del algoritmo"""
        print(f"\n{'='*80}")
        print(f"  {name}")
        print(f"{'='*80}\n")
        
        stats = self.grammar.get_statistics(algorithm)
        
        print("Pseudocódigo:")
        print(algorithm.to_pseudocode(indent=0))
        print()
        
        print("Estadísticas:")
        print(f"  • Total nodos: {stats['total_nodes']}")
        print(f"  • Profundidad: {stats['depth']}")
        print(f"  • Nodos constructivos: {stats['node_counts']['constructive']}")
        print(f"  • Nodos mejora: {stats['node_counts']['improvement']}")
        print(f"  • Nodos perturbación: {stats['node_counts']['perturbation']}")
        print(f"  • Válido: {'✓' if stats['is_valid'] else '✗'}")
        print()
    
    def save_results(self, best_algorithm, best_fitness):
        """Guarda resultados de evolución"""
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        output_dir = project_root / "output" / "gaa"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar mejor algoritmo
        algo_file = output_dir / f"best_algorithm_{timestamp}.json"
        with open(algo_file, 'w') as f:
            json.dump(best_algorithm.to_dict(), f, indent=2)
        
        # Guardar historial
        hist_file = output_dir / f"evolution_history_{timestamp}.json"
        with open(hist_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        
        # Guardar resumen
        summary_file = output_dir / f"summary_{timestamp}.txt"
        with open(summary_file, 'w') as f:
            f.write("RESULTADOS GAA\n")
            f.write("="*80 + "\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Población: {self.pop_size}\n")
            f.write(f"Generaciones: {self.generations}\n")
            f.write(f"Semilla: {self.seed}\n")
            f.write(f"Instancias entrenamiento: {len(self.training_instances)}\n")
            f.write(f"\nMejor fitness encontrado: {best_fitness:.2f}\n")
            f.write(f"\nMejor algoritmo:\n")
            f.write(best_algorithm.to_pseudocode())
        
        print(f"\n📁 Resultados guardados en:")
        print(f"   • {algo_file}")
        print(f"   • {hist_file}")
        print(f"   • {summary_file}")


def main():
    """Función principal"""
    print("\n")
    print("="*80)
    print("  GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA) - GCP-ILS-4")
    print("="*80)
    print("\n")
    
    # Crear solucionador
    solver = GAASolver(
        training_dir="datasets/training",
        pop_size=5,
        generations=20,
        seed=42
    )
    
    # Evol ionar
    best_algorithm, best_fitness = solver.evolve()
    
    # Mostrar mejor algoritmo
    solver.print_algorithm(best_algorithm, "MEJOR ALGORITMO ENCONTRADO")
    
    # Guardar resultados
    solver.save_results(best_algorithm, best_fitness)
    
    print("\n✅ Experimento completado\n")


if __name__ == "__main__":
    main()
