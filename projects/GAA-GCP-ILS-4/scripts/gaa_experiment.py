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
from utils import OutputManager


class GAASolver:
    """Solucionador usando Generación Automática de Algoritmos"""
    
    def __init__(self, 
                 training_dir: str = "datasets/training",
                 pop_size: int = 10,
                 generations: int = 50,
                 seed: int = 42,
                 output_manager: OutputManager = None):
        """
        Inicializa solucionador GAA
        
        Args:
            training_dir: Directorio de instancias de entrenamiento
            pop_size: Tamaño de población de algoritmos
            generations: Número de generaciones
            seed: Semilla aleatoria
            output_manager: Gestor de outputs (si None, se crea uno)
        """
        self.training_dir = Path(training_dir)
        self.pop_size = pop_size
        self.generations = generations
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
        # Gestor de outputs
        self.output_manager = output_manager or OutputManager()
        
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
        """Guarda resultados de evolución usando OutputManager"""
        session_dir = self.output_manager.get_session_dir()
        
        # Guardar mejor algoritmo (JSON)
        algo_file = self.output_manager.save_algorithm_json(best_algorithm)
        
        # Guardar pseudocódigo
        pseudo_file = self.output_manager.save_algorithm_pseudocode(best_algorithm)
        
        # Guardar historial de evolución (JSON)
        hist_file = self.output_manager.save_detailed_json({
            'best_fitness': float(best_fitness),
            'evolution_history': self.history,
            'algorithm_stats': self.grammar.get_statistics(best_algorithm)
        }, filename="evolution_history.json")
        
        # Generar resumen en texto
        summary_text = self._generate_summary_text(best_algorithm, best_fitness)
        summary_file = self.output_manager.save_statistics_txt(summary_text)
        
        print(f"\n📁 Resultados guardados en: {session_dir}")
        print(f"   • {Path(algo_file).name}")
        print(f"   • {Path(pseudo_file).name}")
        print(f"   • {Path(hist_file).name}")
        print(f"   • {Path(summary_file).name}")
    
    def _generate_summary_text(self, best_algorithm, best_fitness) -> str:
        """Genera resumen en texto"""
        stats = self.grammar.get_statistics(best_algorithm)
        
        text = "RESULTADOS GAA - GENERACIÓN AUTOMÁTICA DE ALGORITMOS\n"
        text += "="*80 + "\n\n"
        text += f"Timestamp: {self.output_manager.get_timestamp()}\n"
        text += f"Población: {self.pop_size}\n"
        text += f"Generaciones: {self.generations}\n"
        text += f"Semilla: {self.seed}\n"
        text += f"Instancias entrenamiento: {len(self.training_instances)}\n"
        text += f"\nMejor fitness encontrado: {best_fitness:.2f}\n"
        text += f"\nESTADÍSTICAS DEL MEJOR ALGORITMO:\n"
        text += f"  • Total nodos: {stats['total_nodes']}\n"
        text += f"  • Profundidad: {stats['depth']}\n"
        text += f"  • Nodos constructivos: {stats['node_counts']['constructive']}\n"
        text += f"  • Nodos mejora: {stats['node_counts']['improvement']}\n"
        text += f"  • Nodos perturbación: {stats['node_counts']['perturbation']}\n"
        text += f"  • Válido: {'✓' if stats['is_valid'] else '✗'}\n"
        text += f"\nPSEUDOCÓDIGO:\n"
        text += best_algorithm.to_pseudocode()
        text += "\n\n" + "="*80 + "\n"
        
        return text


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
