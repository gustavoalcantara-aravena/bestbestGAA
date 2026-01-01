#!/usr/bin/env python3
"""
run_full_experiment_with_plotsv2.py

Script mejorado que usa PlotManagerV2 para generar ploteos en estructura multinivel:
- Nivel 1: Ploteos individuales por instancia
- Nivel 2: Ploteos agregados por familia
- Nivel 3: Ploteos comparativos entre familias
- Nivel 4: Resumen y síntesis

Estructura de outputs:
output/{timestamp}/plots/
├── 1_individual/
├── 2_family/
├── 3_comparison/
└── 4_summary/
"""

import sys
from pathlib import Path
import time
import numpy as np
from collections import defaultdict

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import GraphColoringProblem
from metaheuristic.ils_core import IteratedLocalSearch
from utils.output_manager import OutputManager
from visualization.plotter_v2 import PlotManagerV2
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import execute_algorithm


class FullExperimentV2:
    """Experimento completo con PlotManagerV2"""
    
    def __init__(self, num_replicas: int = 1):
        self.num_replicas = num_replicas
        self.output_manager = OutputManager()
        self.session_dir = self.output_manager.create_session_directory()
        self.plot_manager = PlotManagerV2(str(self.session_dir))
        
        # Almacenar datos para ploteos
        self.results = []
        self.convergence_histories = {}
        self.family_data = defaultdict(lambda: {
            'instances': [],
            'vertices': [],
            'times': [],
            'gaps': [],
            'algorithm_results': defaultdict(list)
        })
    
    def load_datasets(self, family: str = "MYC") -> list:
        """Cargar datasets de una familia"""
        dataset_dir = project_root / "datasets" / family
        if not dataset_dir.exists():
            print(f"⚠️  Directorio no encontrado: {dataset_dir}")
            return []
        
        datasets = sorted(dataset_dir.glob("*.col"))
        print(f"✅ Cargados {len(datasets)} datasets de familia {family}")
        return datasets
    
    def run_ils_on_instance(self, problem: GraphColoringProblem) -> tuple:
        """Ejecutar ILS en una instancia"""
        ils = IteratedLocalSearch(
            problem=problem,
            max_iterations=100,
            seed=42
        )
        
        solution, metrics, history = ils.run()
        return solution, metrics, history
    
    def run_experiment(self, families: list = ["MYC"]):
        """Ejecutar experimento completo"""
        print("\n" + "="*80)
        print("🧪 EXPERIMENTO COMPLETO CON PLOTSV2")
        print("="*80 + "\n")
        
        # Cargar datasets por familia
        all_datasets = {}
        for family in families:
            datasets = self.load_datasets(family)
            all_datasets[family] = datasets
        
        # Ejecutar en cada dataset
        for family, datasets in all_datasets.items():
            print(f"\n📊 FAMILIA: {family}")
            print("="*80)
            
            for dataset_file in datasets[:5]:  # Limitar a 5 por familia
                problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
                print(f"\n📈 {problem.name}")
                
                # Ejecutar ILS
                solution, metrics, history = self.run_ils_on_instance(problem)
                
                # Almacenar datos
                self.results.append({
                    'family': family,
                    'instance': problem.name,
                    'vertices': problem.n_vertices,
                    'edges': problem.n_edges,
                    'bks': problem.colors_known,
                    'num_colors': metrics['num_colors'],
                    'gap': (metrics['num_colors'] - problem.colors_known) / problem.colors_known * 100 if problem.colors_known else 0,
                    'time': metrics.get('time', 0),
                    'conflicts': metrics['conflicts']
                })
                
                self.convergence_histories[problem.name] = history
                
                # Almacenar para ploteos de familia
                self.family_data[family]['instances'].append(problem.name)
                self.family_data[family]['vertices'].append(problem.n_vertices)
                self.family_data[family]['times'].append(metrics.get('time', 0))
                self.family_data[family]['gaps'].append(
                    (metrics['num_colors'] - problem.colors_known) / problem.colors_known * 100 
                    if problem.colors_known else 0
                )
                
                print(f"   ✅ {metrics['num_colors']} colores (gap: {self.results[-1]['gap']:+.2f}%)")
        
        # Generar ploteos
        self._generate_plots_v2()
        
        # Generar algoritmos GAA
        self._generate_gaa_algorithms()
    
    def _generate_plots_v2(self):
        """Generar ploteos en estructura multinivel"""
        print("\n" + "="*80)
        print("📊 GENERANDO PLOTEOS (ESTRUCTURA MULTINIVEL)")
        print("="*80 + "\n")
        
        # Nivel 1: Ploteos individuales
        print("📋 Nivel 1: Ploteos individuales por instancia...")
        for result in self.results[:3]:  # Primeras 3 instancias
            instance_name = result['instance']
            
            if instance_name in self.convergence_histories:
                history = self.convergence_histories[instance_name]
                
                # Ploteo 01: Convergencia
                if 'current_fitness' in history:
                    self.plot_manager.plot_instance_convergence(
                        instance_name,
                        history['current_fitness']
                    )
                
                # Ploteo 02: Distribución de fitness
                if 'current_fitness' in history:
                    self.plot_manager.plot_instance_fitness_distribution(
                        instance_name,
                        history['current_fitness']
                    )
        
        print("   ✅ Ploteos individuales generados\n")
        
        # Nivel 2: Ploteos por familia
        print("📋 Nivel 2: Ploteos agregados por familia...")
        for family, data in self.family_data.items():
            if data['instances']:
                # Ploteo 01: Escalabilidad (Tiempo)
                self.plot_manager.plot_family_scalability_time(
                    family,
                    data['instances'],
                    data['vertices'],
                    data['times']
                )
                
                # Ploteo 02: Escalabilidad (Calidad)
                self.plot_manager.plot_family_scalability_quality(
                    family,
                    data['instances'],
                    data['vertices'],
                    data['gaps']
                )
        
        print("   ✅ Ploteos de familia generados\n")
        
        # Nivel 3: Ploteos comparativos
        print("📋 Nivel 3: Ploteos comparativos entre familias...")
        if len(self.family_data) > 1:
            families_comparison_data = {}
            for family, data in self.family_data.items():
                families_comparison_data[family] = {
                    'vertices': data['vertices'],
                    'times': data['times'],
                    'gaps': data['gaps']
                }
            
            self.plot_manager.plot_families_scalability_comparison(families_comparison_data)
        
        print("   ✅ Ploteos comparativos generados\n")
        
        # Nivel 4: Resumen
        print("📋 Nivel 4: Creando resumen...")
        self.plot_manager.create_summary_readme()
        print("   ✅ Resumen creado\n")
    
    def _generate_gaa_algorithms(self):
        """Generar algoritmos GAA"""
        print("\n" + "="*80)
        print("🧬 GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA)")
        print("="*80 + "\n")
        
        try:
            grammar = Grammar(min_depth=2, max_depth=5)
            generator = AlgorithmGenerator(grammar=grammar, seed=42)
            
            print("📋 Generando 3 algoritmos...")
            algorithms = [generator.generate_fixed_structure() for _ in range(3)]
            
            # Usar primer dataset para prueba
            if self.results:
                first_result = self.results[0]
                problem = GraphColoringProblem.load_from_dimacs(
                    str(project_root / "datasets" / first_result['family'] / f"{first_result['instance']}.col")
                )
                
                print(f"\n📊 Ejecutando en {problem.name}...")
                for i, algo in enumerate(algorithms, 1):
                    try:
                        solution = execute_algorithm(algo, problem, seed=42)
                        print(f"   ✅ GAA_Algorithm_{i}: {solution.num_colors} colores")
                    except Exception as e:
                        print(f"   ❌ GAA_Algorithm_{i}: Error - {e}")
        
        except Exception as e:
            print(f"⚠️  Error en GAA: {e}")


def main():
    """Función principal"""
    experiment = FullExperimentV2(num_replicas=1)
    
    # Ejecutar con familia MYCIEL
    experiment.run_experiment(families=["MYC"])
    
    print("\n" + "="*80)
    print("✅ EXPERIMENTO COMPLETADO")
    print("="*80)
    print(f"\n📁 Resultados guardados en: {experiment.session_dir}")
    print(f"📊 Ploteos en: {experiment.session_dir}/plots/")


if __name__ == "__main__":
    main()
