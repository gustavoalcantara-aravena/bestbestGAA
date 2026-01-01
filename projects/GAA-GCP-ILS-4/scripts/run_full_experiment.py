#!/usr/bin/env python3
"""
run_full_experiment.py - Experimento Completo GAA-GCP-ILS-4

Ejecuta ILS en todos los 79 datasets DIMACS y genera:
- Resultados tabulares (CSV, JSON)
- Reportes estadísticos (TXT)
- Gráficas de análisis (PNG)
- Archivos de solución (.sol)

Uso:
    python scripts/run_full_experiment.py [opciones]

Opciones:
    --mode all              Ejecutar en todos los 79 datasets (default)
    --mode family DSJ       Ejecutar en familia específica (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
    --max-time 300          Tiempo máximo por instancia en segundos
    --num-replicas 1        Número de ejecuciones independientes por instancia
    --seed 42               Semilla aleatoria
    --verbose               Mostrar progreso detallado

Ejemplos:
    python scripts/run_full_experiment.py --mode all
    python scripts/run_full_experiment.py --mode family DSJ --num-replicas 3
    python scripts/run_full_experiment.py --mode all --max-time 60 --verbose
"""

import sys
import time
import json
import csv
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import numpy as np


class TimingTracker:
    """Registra y documenta tiempos de ejecución de cada etapa"""
    
    def __init__(self):
        self.timings = {}
        self.current_stage = None
        self.stage_start = None
    
    def start_stage(self, stage_name: str):
        """Inicia cronómetro de una etapa"""
        self.current_stage = stage_name
        self.stage_start = time.time()
    
    def end_stage(self) -> float:
        """Termina cronómetro y retorna tiempo transcurrido"""
        if self.current_stage is None:
            return 0
        
        elapsed = time.time() - self.stage_start
        self.timings[self.current_stage] = elapsed
        self.current_stage = None
        self.stage_start = None
        return elapsed
    
    def get_timing(self, stage_name: str) -> float:
        """Obtiene tiempo de una etapa específica"""
        return self.timings.get(stage_name, 0)
    
    def get_all_timings(self) -> Dict[str, float]:
        """Obtiene todos los tiempos registrados"""
        return self.timings.copy()
    
    def format_time(self, seconds: float) -> str:
        """Formatea tiempo en formato legible"""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f}m ({seconds:.0f}s)"
        else:
            hours = seconds / 3600
            return f"{hours:.2f}h ({seconds:.0f}s)"
    
    def generate_report(self) -> str:
        """Genera reporte de tiempos"""
        report = "REPORTE DE TIEMPOS DE EJECUCIÓN\n"
        report += "="*80 + "\n\n"
        
        total_time = sum(self.timings.values())
        
        report += "RESUMEN GENERAL:\n"
        report += "-"*80 + "\n"
        report += f"Tiempo total: {self.format_time(total_time)}\n\n"
        
        report += "DESGLOSE POR ETAPA:\n"
        report += "-"*80 + "\n"
        report += f"{'Etapa':<30} {'Tiempo':<20} {'% Total':<10}\n"
        report += "-"*80 + "\n"
        
        # Ordenar por tiempo descendente
        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)
        
        for stage, elapsed in sorted_timings:
            percentage = (elapsed / total_time * 100) if total_time > 0 else 0
            report += f"{stage:<30} {self.format_time(elapsed):<20} {percentage:>6.1f}%\n"
        
        report += "\n" + "="*80 + "\n"
        
        return report
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte tiempos a diccionario para JSON"""
        total_time = sum(self.timings.values())
        
        return {
            'total_time_seconds': total_time,
            'total_time_formatted': self.format_time(total_time),
            'stages': {
                stage: {
                    'seconds': elapsed,
                    'formatted': self.format_time(elapsed),
                    'percentage': (elapsed / total_time * 100) if total_time > 0 else 0
                }
                for stage, elapsed in self.timings.items()
            }
        }

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports del proyecto
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
from metaheuristic.ils_core import IteratedLocalSearch
from operators.constructive import GreedyDSATUR
from operators.improvement import KempeChain
from operators.perturbation import RandomRecolor
from utils import OutputManager
from visualization.plotter import PlotManager


class FullExperiment:
    """Experimento completo en todos los datasets DIMACS"""
    
    def __init__(self,
                 mode: str = "all",
                 family: Optional[str] = None,
                 max_time: float = 300.0,
                 num_replicas: int = 1,
                 seed: int = 42,
                 verbose: bool = False):
        """
        Inicializa experimento
        
        Args:
            mode: "all" o "family"
            family: Familia específica (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
            max_time: Tiempo máximo por instancia (segundos)
            num_replicas: Número de ejecuciones independientes
            seed: Semilla aleatoria
            verbose: Mostrar progreso detallado
        """
        self.mode = mode
        self.family = family
        self.max_time = max_time
        self.num_replicas = num_replicas
        self.seed = seed
        self.verbose = verbose
        self.rng = np.random.default_rng(seed)
        
        # Gestor de outputs
        self.output_manager = OutputManager()
        if mode == "all":
            self.session_dir = self.output_manager.create_session(mode="all_datasets")
        else:
            self.session_dir = self.output_manager.create_session(
                mode="specific_dataset",
                family=family
            )
        
        # Gestor de gráficas - usar directorio de sesión
        self.plot_manager = PlotManager(session_dir=str(self.session_dir))
        
        # Configurar logging
        self.output_manager.setup_logging(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Sistema de timing
        self.timing = TimingTracker()
        
        # Resultados
        self.results = []
        self.all_solutions = {}
        self.convergence_histories = {}
        
        print(f"\n{'='*80}")
        print(f"  EXPERIMENTO COMPLETO: Graph Coloring Problem con ILS")
        print(f"{'='*80}\n")
        print(f"📁 Sesión: {self.session_dir}")
        print(f"🎯 Modo: {mode}" + (f" ({family})" if family else ""))
        print(f"⏱️  Tiempo máximo por instancia: {max_time}s")
        print(f"🔄 Réplicas por instancia: {num_replicas}")
        print(f"🌱 Semilla: {seed}\n")
    
    def load_datasets(self) -> List[GraphColoringProblem]:
        """Carga datasets DIMACS"""
        print("📂 CARGANDO DATASETS")
        print("-" * 80)
        
        datasets_dir = project_root / "datasets"
        problems = []
        
        if self.mode == "all":
            # Cargar todas las familias
            families = ["CUL", "DSJ", "LEI", "MYC", "REG", "SCH", "SGB"]
        else:
            families = [self.family]
        
        for family in families:
            family_dir = datasets_dir / family
            if not family_dir.exists():
                self.logger.warning(f"Familia {family} no encontrada")
                continue
            
            # Cargar archivos .col de la familia
            col_files = sorted(family_dir.glob("*.col"))
            for col_file in col_files:
                try:
                    problem = GraphColoringProblem.load_from_dimacs(str(col_file))
                    problems.append(problem)
                except Exception as e:
                    self.logger.error(f"Error cargando {col_file}: {e}")
        
        print(f"✅ {len(problems)} datasets cargados\n")
        return problems
    
    def run_ils(self, problem: GraphColoringProblem) -> Tuple[ColoringSolution, Dict, Any]:
        """Ejecuta ILS en una instancia"""
        ils = IteratedLocalSearch(
            problem=problem,
            constructive=GreedyDSATUR.construct,
            improvement=KempeChain.improve,
            perturbation=RandomRecolor.perturb,
            max_iterations=100,
            time_budget=self.max_time,
            verbose=False,
            seed=self.seed
        )
        
        best_solution, history = ils.solve()
        
        # Evaluar solución
        metrics = ColoringEvaluator.evaluate(best_solution, problem)
        
        return best_solution, metrics, history
    
    def run_experiment(self):
        """Ejecuta experimento completo"""
        # Cargar datasets
        self.timing.start_stage("Carga de datasets")
        problems = self.load_datasets()
        load_time = self.timing.end_stage()
        print(f"⏱️  Tiempo de carga: {self.timing.format_time(load_time)}\n")
        
        if not problems:
            print("❌ No hay datasets para ejecutar")
            return
        
        print(f"\n{'='*80}")
        print(f"🔬 EXPERIMENTO COMPLETO: ILS EN {len(problems)} INSTANCIAS")
        print(f"{'='*80}")
        print(f"⏱️  Tiempo máximo por instancia: {self.max_time}s")
        print(f"🔄 Réplicas por instancia: {self.num_replicas}")
        print(f"🌱 Semilla: {self.seed}")
        print(f"{'='*80}\n")
        
        self.timing.start_stage("Ejecución de ILS")
        start_time = time.time()
        
        for idx, problem in enumerate(problems, 1):
            # Barra de progreso
            progress = (idx - 1) / len(problems) * 100
            print(f"\n[{idx:3d}/{len(problems)}] ({progress:5.1f}%) {problem.name}")
            print(f"   📊 Vértices: {problem.n_vertices:4d} | Aristas: {problem.n_edges:6d}", end="")
            if problem.colors_known:
                print(f" | BKS: {problem.colors_known}")
            else:
                print(" | BKS: Desconocido")
            
            instance_results = {
                'instance': problem.name,
                'family': problem.name.split('_')[0] if '_' in problem.name else 'UNKNOWN',
                'vertices': problem.n_vertices,
                'edges': problem.n_edges,
                'bks': problem.colors_known,
                'colors': [],
                'conflicts': [],
                'times': [],
                'gaps': [],
                'feasible': []
            }
            
            # Ejecutar réplicas
            for replica in range(self.num_replicas):
                try:
                    replica_start = time.time()
                    solution, metrics, history = self.run_ils(problem)
                    replica_time = time.time() - replica_start
                    
                    instance_results['colors'].append(metrics['num_colors'])
                    instance_results['conflicts'].append(metrics['conflicts'])
                    instance_results['times'].append(replica_time)
                    instance_results['feasible'].append(metrics['feasible'])
                    
                    if problem.colors_known:
                        gap = (metrics['num_colors'] - problem.colors_known) / problem.colors_known
                        instance_results['gaps'].append(gap)
                        gap_str = f"({gap*100:+.1f}%)"
                    else:
                        gap_str = ""
                    
                    feasible_icon = "✓" if metrics['feasible'] else "✗"
                    print(f"   Réplica {replica+1}/{self.num_replicas}: {metrics['num_colors']} colores "
                          f"({metrics['conflicts']} conflictos) {feasible_icon} {replica_time:.2f}s {gap_str}")
                    
                    # Guardar solución e historial de la primera réplica
                    if replica == 0:
                        self.all_solutions[problem.name] = solution
                        # Guardar el historial de current_fitness para la gráfica de convergencia (muestra variación real)
                        self.convergence_histories[problem.name] = {
                            'current_fitness': history.current_fitness if hasattr(history, 'current_fitness') else [],
                            'best_fitness': history.best_fitness if hasattr(history, 'best_fitness') else [],
                            'metrics': metrics
                        }
                
                except Exception as e:
                    self.logger.error(f"Error en réplica {replica+1}: {e}")
                    print(f"   ❌ Error en réplica {replica+1}: {e}")
            
            # Calcular estadísticas
            if instance_results['colors']:
                instance_results['avg_colors'] = np.mean(instance_results['colors'])
                instance_results['std_colors'] = np.std(instance_results['colors'])
                instance_results['avg_time'] = np.mean(instance_results['times'])
                instance_results['best_colors'] = min(instance_results['colors'])
                instance_results['worst_colors'] = max(instance_results['colors'])
                
                # Resumen de la instancia
                feasible_count = sum(instance_results['feasible'])
                print(f"   📈 Resumen: {instance_results['best_colors']} colores (mejor), "
                      f"{instance_results['avg_colors']:.1f}±{instance_results['std_colors']:.1f} (promedio), "
                      f"{feasible_count}/{self.num_replicas} factibles")
            
            self.results.append(instance_results)
        
        elapsed = time.time() - start_time
        ils_time = self.timing.end_stage()
        
        print(f"\n{'='*80}")
        print(f"✅ EJECUCIÓN DE ILS COMPLETADA")
        print(f"{'='*80}")
        print(f"⏱️  Tiempo total: {self.timing.format_time(ils_time)}")
        print(f"📊 Instancias procesadas: {len(problems)}")
        print(f"🔄 Réplicas por instancia: {self.num_replicas}")
        print(f"📈 Tiempo promedio por instancia: {self.timing.format_time(ils_time/len(problems))}")
        print(f"{'='*80}\n")
        
        # Guardar resultados
        self._save_results(elapsed)
        
        # Generar gráficas
        self._generate_plots()
    
    def _save_results(self, elapsed_time: float):
        """Guarda resultados en archivos"""
        self.timing.start_stage("Guardado de resultados")
        
        print("\n" + "="*80)
        print("💾 GUARDANDO RESULTADOS")
        print("="*80)
        
        # Preparar datos para CSV
        csv_data = []
        for result in self.results:
            csv_data.append({
                'Instance': result['instance'],
                'Family': result['family'],
                'Vertices': result['vertices'],
                'Edges': result['edges'],
                'BKS': result['bks'],
                'Best_Colors': result.get('best_colors', 'N/A'),
                'Avg_Colors': f"{result.get('avg_colors', 0):.2f}",
                'Worst_Colors': result.get('worst_colors', 'N/A'),
                'Feasible': all(result['feasible']),
                'Avg_Time': f"{result.get('avg_time', 0):.2f}",
                'Gap': f"{np.mean(result.get('gaps', [0])):.4f}" if result.get('gaps') else 'N/A'
            })
        
        # Guardar CSV
        csv_file = self.output_manager.save_summary_csv(csv_data)
        print(f"✅ CSV: {Path(csv_file).name}")
        
        # Guardar JSON detallado
        json_data = {
            'metadata': {
                'timestamp': self.output_manager.get_timestamp(),
                'mode': self.mode,
                'family': self.family,
                'total_instances': len(self.results),
                'total_time': elapsed_time,
                'num_replicas': self.num_replicas
            },
            'results': self.results,
            'statistics': self._calculate_statistics()
        }
        
        json_file = self.output_manager.save_detailed_json(json_data)
        print(f"✅ JSON: {Path(json_file).name}")
        
        # Guardar TXT
        txt_content = self._generate_report(elapsed_time)
        txt_file = self.output_manager.save_statistics_txt(txt_content)
        print(f"✅ TXT: {Path(txt_file).name}")
        
        # Guardar soluciones
        for instance_name, solution in self.all_solutions.items():
            try:
                problem = next(p for p in self.results if p['instance'] == instance_name)
                sol_file = self.output_manager.save_solution(instance_name, solution)
                print(f"✅ SOL: {Path(sol_file).name}")
            except Exception as e:
                self.logger.error(f"Error guardando solución {instance_name}: {e}")
        
        # Guardar reporte de timing
        timing_report = self.timing.generate_report()
        timing_file = self.output_manager.save_statistics_txt(timing_report, filename="timing_report.txt")
        print(f"✅ TIMING: {Path(timing_file).name}")
        
        # Guardar timing en JSON
        timing_json = self.timing.to_dict()
        timing_json_file = self.output_manager.save_detailed_json(timing_json, filename="timing_report.json")
        print(f"✅ TIMING JSON: {Path(timing_json_file).name}")
        
        # Guardar reporte de gaps
        gaps_report = self._generate_gaps_report()
        gaps_file = self.output_manager.save_statistics_txt(gaps_report, filename="gaps_report.txt")
        print(f"✅ GAPS: {Path(gaps_file).name}")
        
        save_time = self.timing.end_stage()
        print(f"\n⏱️  Tiempo de guardado: {self.timing.format_time(save_time)}\n")
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calcula estadísticas generales"""
        all_colors = []
        all_times = []
        all_gaps = []
        
        for result in self.results:
            all_colors.extend(result['colors'])
            all_times.extend(result['times'])
            if result.get('gaps'):
                all_gaps.extend(result['gaps'])
        
        return {
            'total_instances': len(self.results),
            'total_feasible': sum(1 for r in self.results if all(r['feasible'])),
            'avg_colors': float(np.mean(all_colors)) if all_colors else 0,
            'std_colors': float(np.std(all_colors)) if all_colors else 0,
            'avg_time': float(np.mean(all_times)) if all_times else 0,
            'avg_gap': float(np.mean(all_gaps)) if all_gaps else 0
        }
    
    def _generate_report(self, elapsed_time: float) -> str:
        """Genera reporte en texto"""
        stats = self._calculate_statistics()
        
        report = "EXPERIMENTO COMPLETO: GRAPH COLORING PROBLEM CON ILS\n"
        report += "="*80 + "\n\n"
        report += f"Timestamp: {self.output_manager.get_timestamp()}\n"
        report += f"Modo: {self.mode}" + (f" ({self.family})" if self.family else "") + "\n"
        report += f"Tiempo total: {elapsed_time:.1f}s\n"
        report += f"Réplicas por instancia: {self.num_replicas}\n\n"
        
        report += "RESUMEN GENERAL:\n"
        report += "-"*80 + "\n"
        report += f"Total instancias: {stats['total_instances']}\n"
        report += f"Instancias factibles: {stats['total_feasible']}/{stats['total_instances']}\n"
        report += f"Colores promedio: {stats['avg_colors']:.2f} ± {stats['std_colors']:.2f}\n"
        report += f"Tiempo promedio: {stats['avg_time']:.2f}s\n"
        report += f"Gap promedio: {stats['avg_gap']:.4f}\n\n"
        
        report += "RESULTADOS POR INSTANCIA:\n"
        report += "-"*80 + "\n"
        report += f"{'Instancia':<20} {'Colores':<10} {'Tiempo':<10} {'Gap':<10}\n"
        report += "-"*80 + "\n"
        
        for result in self.results:
            colors = f"{result.get('best_colors', 'N/A')}"
            time_val = f"{result.get('avg_time', 0):.2f}s"
            gap = f"{np.mean(result.get('gaps', [0])):.4f}" if result.get('gaps') else 'N/A'
            report += f"{result['instance']:<20} {colors:<10} {time_val:<10} {gap:<10}\n"
        
        report += "\n" + "="*80 + "\n"
        
        return report
    
    def _generate_gaps_report(self) -> str:
        """Genera reporte de gaps"""
        report = "REPORTE DE GAPS\n"
        report += "="*80 + "\n\n"
        
        # Contar instancias con BKS
        instances_with_bks = [r for r in self.results if r.get('bks')]
        
        if not instances_with_bks:
            report += "⚠️  No hay instancias con BKS (Best Known Solution) definido.\n"
            report += "Los gaps no pueden ser calculados.\n"
            report += "="*80 + "\n"
            return report
        
        report += f"Instancias con BKS: {len(instances_with_bks)}/{len(self.results)}\n\n"
        
        # Tabla de gaps
        report += f"{'Instancia':<20} {'BKS':<6} {'Encontrado':<12} {'Gap':<10} {'Factible':<10}\n"
        report += "-"*80 + "\n"
        
        all_gaps = []
        for result in instances_with_bks:
            if result.get('gaps'):
                avg_gap = np.mean(result['gaps'])
                all_gaps.append(avg_gap)
                gap_str = f"{avg_gap:+.2f}%"
            else:
                gap_str = "N/A"
            
            feasible = "✓" if all(result['feasible']) else "✗"
            report += f"{result['instance']:<20} {result['bks']:<6} {result.get('best_colors', 'N/A'):<12} {gap_str:<10} {feasible:<10}\n"
        
        # Estadísticas de gaps
        report += "\n" + "="*80 + "\n"
        report += "ESTADÍSTICAS DE GAPS\n"
        report += "-"*80 + "\n"
        
        if all_gaps:
            report += f"Gap promedio: {np.mean(all_gaps):+.2f}%\n"
            report += f"Gap mínimo: {np.min(all_gaps):+.2f}%\n"
            report += f"Gap máximo: {np.max(all_gaps):+.2f}%\n"
            report += f"Desviación estándar: {np.std(all_gaps):.2f}%\n"
            
            # Contar óptimos
            optimal = sum(1 for g in all_gaps if g == 0)
            report += f"\nSoluciones óptimas (gap=0%): {optimal}/{len(all_gaps)}\n"
        
        report += "\n" + "="*80 + "\n"
        
        return report
    
    def _generate_plots(self):
        """Genera gráficas de análisis"""
        self.timing.start_stage("Generación de gráficas")
        
        print("\n" + "="*80)
        print("📊 GENERANDO GRÁFICAS")
        print("="*80)
        
        try:
            # Convergencia - usar current_fitness para ver la variación real
            if self.convergence_histories:
                first_history = list(self.convergence_histories.values())[0]
                if 'current_fitness' in first_history and first_history['current_fitness']:
                    self.plot_manager.plot_convergence(
                        first_history['current_fitness'],
                        instance_name="Convergencia Promedio"
                    )
                    print("✅ Gráfica de convergencia generada")
                else:
                    print("⚠️  No hay datos de current_fitness disponibles")
            else:
                print("⚠️  No hay historiales de convergencia disponibles")
        except Exception as e:
            self.logger.warning(f"Error generando convergencia: {e}")
            print(f"⚠️  Error en gráfica de convergencia: {e}")
        
        try:
            # Escalabilidad
            vertices = [r['vertices'] for r in self.results]
            times = [r.get('avg_time', 0) for r in self.results]
            
            if vertices and times:
                self.plot_manager.plot_scalability(vertices, times)
                print("✅ Gráfica de escalabilidad generada")
            else:
                print("⚠️  No hay datos suficientes para gráfica de escalabilidad")
        except Exception as e:
            self.logger.warning(f"Error generando escalabilidad: {e}")
            print(f"⚠️  Error en gráfica de escalabilidad: {e}")
        
        plots_time = self.timing.end_stage()
        
        # ====================================================================
        # GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA)
        # ====================================================================
        
        self.timing.start_stage("Generación automática de algoritmos")
        
        print("\n" + "="*80)
        print("🧬 GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA)")
        print("="*80 + "\n")
        
        try:
            from gaa.grammar import Grammar
            from gaa.generator import AlgorithmGenerator
            from gaa.interpreter import execute_algorithm
            from gaa.ast_nodes import mutate_ast
            
            print("📋 Etapa 1/5: Inicializando GAA con Gramática BNF...")
            print(f"   Seed: 42 (reproducibilidad garantizada)")
            
            # Crear gramática y generador
            # Usar mismos parámetros que KBP-SA para consistencia
            grammar = Grammar(min_depth=2, max_depth=5)
            generator = AlgorithmGenerator(grammar=grammar, seed=42)
            print("   ✅ Gramática BNF inicializada\n")
            
            print("📋 Etapa 2/5: Mostrando operadores disponibles...")
            print(f"   📊 Gramática BNF:")
            print(f"      - Constructivos: {', '.join(grammar.CONSTRUCTIVE_TERMINALS)}")
            print(f"      - Mejora Local: {', '.join(grammar.IMPROVEMENT_TERMINALS)}")
            print(f"      - Perturbación: {', '.join(grammar.PERTURBATION_TERMINALS)}")
            print(f"      - Profundidad: {grammar.min_depth}-{grammar.max_depth}")
            print("   ✅ Operadores listados\n")
            
            # Cargar instancia de entrenamiento (primera del conjunto)
            if not self.results or 'problem' not in self.results[0]:
                print("⚠️  No hay instancias de entrenamiento disponibles. Saltando GAA.")
                raise RuntimeError("No training instances")
            
            training_problem = self.results[0]['problem']
            
            # ====================================================================
            # PASO 1: GENERAR 3 ALGORITMOS AUTOMÁTICAMENTE
            # ====================================================================
            print("📋 Etapa 3/5: Generando 3 algoritmos GAA con seed=42...")
            population = []
            for i in range(3):
                print(f"   ⏳ Generando GAA_Algorithm_{i+1}...", end=" ", flush=True)
                algo = generator.generate_fixed_structure()
                if algo:
                    population.append(algo)
                    stats = grammar.get_statistics(algo)
                    print(f"✅ GENERADO")
                    print(f"      - Nodos: {stats['total_nodes']}")
                    print(f"      - Profundidad: {stats['depth']}")
                    print(f"      - Estructura: {stats['node_counts']}")
                else:
                    print(f"❌ FALLO")
            
            if not population:
                raise RuntimeError("No se pudo generar población inicial válida")
            
            print(f"\n📋 Etapa 4/5: Validando algoritmos generados...")
            print(f"   ✅ {len(population)} algoritmos GAA generados exitosamente")
            print(f"   ✅ Todos los algoritmos son válidos\n")
            
            print("📋 Etapa 5/5: Guardando información de algoritmos generados...")
            print(f"   ✅ Algoritmos listos para ejecución\n")
            
            # Validar que hay resultados de ILS para ejecutar GAA
            if not self.results:
                print("⚠️  No hay resultados de ILS. Saltando ejecución de GAA.")
                raise RuntimeError("No hay instancias para ejecutar GAA")
            
            print("\n" + "="*80)
            print("PASO 2: EJECUTAR 3 ALGORITMOS EN INSTANCIAS")
            print("="*80 + "\n")
            
            # Ejecutar los 3 algoritmos en instancias
            algorithm_results = {}
            
            # Extraer problemas de self.results (que contiene 'problem' en cada resultado)
            gaa_problems = []
            for result in self.results:
                if 'problem' in result:
                    gaa_problems.append(result['problem'])
            
            if not gaa_problems:
                print("⚠️  No se pudieron extraer problemas de los resultados de ILS.")
                raise RuntimeError("No hay problemas para ejecutar GAA")
            
            for algo_idx, algo in enumerate(population):
                algo_name = f"GAA_Algorithm_{algo_idx + 1}"
                algorithm_results[algo_name] = []
                
                print(f"Ejecutando {algo_name} en instancias...\n")
                
                # Ejecutar en todas las instancias cargadas
                for result_idx, problem in enumerate(gaa_problems, 1):
                    try:
                        solution = execute_algorithm(algo, problem, seed=42)
                        
                        num_colors = solution.num_colors
                        algorithm_results[algo_name].append(num_colors)
                        
                        gap = ((problem.colors_known - num_colors) / problem.colors_known * 100) if problem.colors_known else 0
                        
                        print(f"  [{result_idx}/{len(gaa_problems)}] {problem.name}: {num_colors} colores (gap: {gap:.2f}%)")
                    
                    except Exception as e:
                        print(f"  [{result_idx}/{len(gaa_problems)}] {problem.name}: Error - {e}")
                        algorithm_results[algo_name].append(float('inf'))
                
                print()
            
            # ====================================================================
            print("="*80)
            print("PASO 3: COMPARAR 3 ALGORITMOS")
            print("="*80 + "\n")
            
            # Análisis estadístico
            from experimentation.statistics import StatisticalAnalyzer
            
            analyzer = StatisticalAnalyzer(alpha=0.05)
            comparison = analyzer.compare_multiple_algorithms(algorithm_results)
            
            # Generar reporte
            report = analyzer.generate_comparison_report(comparison)
            print(report)
            
            # Guardar resultados - convertir booleanos a strings para JSON
            import json
            from pathlib import Path
            
            def convert_to_serializable(obj):
                """Convierte objetos no serializables a strings"""
                if isinstance(obj, dict):
                    return {k: convert_to_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [convert_to_serializable(item) for item in obj]
                elif isinstance(obj, bool):
                    return str(obj)
                elif isinstance(obj, (np.bool_, np.integer, np.floating)):
                    return float(obj) if isinstance(obj, (np.floating, float)) else int(obj)
                else:
                    return obj
            
            comparison_serializable = convert_to_serializable(comparison)
            comparison_file = self.output_manager.session_dir / 'results' / 'gaa_comparison_results.json'
            with open(comparison_file, 'w') as f:
                json.dump(comparison_serializable, f, indent=2, ensure_ascii=False)
            self.output_manager.save_statistics_txt(report, filename='gaa_comparison_report.txt')
            
            # Guardar algoritmos generados
            algorithms_data = {
                'algorithms': [
                    {
                        'id': i + 1,
                        'name': f'GAA_Algorithm_{i+1}',
                        'stats': convert_to_serializable(grammar.get_statistics(algo))
                    }
                    for i, algo in enumerate(population)
                ],
                'seed': 42,
                'grammar': {
                    'min_depth': grammar.min_depth,
                    'max_depth': grammar.max_depth,
                    'terminals': {
                        'constructive': grammar.CONSTRUCTIVE_TERMINALS,
                        'improvement': grammar.IMPROVEMENT_TERMINALS,
                        'perturbation': grammar.PERTURBATION_TERMINALS
                    }
                }
            }
            algorithms_file = self.output_manager.session_dir / 'results' / 'gaa_algorithms_generated.json'
            with open(algorithms_file, 'w') as f:
                json.dump(algorithms_data, f, indent=2, ensure_ascii=False)
            
            print("\n✅ GAA completado exitosamente")
            
        except ImportError:
            print("⚠️  Módulos GAA no disponibles. Saltando evolución de algoritmos.")
        except Exception as e:
            self.logger.warning(f"Error en GAA: {e}")
            print(f"⚠️  Error en GAA: {e}")
        
        gaa_time = self.timing.end_stage()
        
        print("\n" + "="*80)
        print("✅ PROCESO COMPLETADO")
        print("="*80)
        print(f"⏱️  Tiempo de generación de gráficas: {self.timing.format_time(plots_time)}")
        print(f"⏱️  Tiempo de GAA: {self.timing.format_time(gaa_time)}")
        print(f"📁 Resultados guardados en: {self.session_dir}")
        print("="*80)
        
        # Mostrar resumen de tiempos
        self._print_timing_summary()
        print("="*80 + "\n")
    
    def _print_timing_summary(self):
        """Imprime resumen de tiempos en pantalla"""
        print("\n⏱️  RESUMEN DE TIEMPOS POR ETAPA")
        print("-"*80)
        
        timings = self.timing.get_all_timings()
        total_time = sum(timings.values())
        
        for stage, elapsed in sorted(timings.items(), key=lambda x: x[1], reverse=True):
            percentage = (elapsed / total_time * 100) if total_time > 0 else 0
            bar_length = int(percentage / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{stage:<30} {self.timing.format_time(elapsed):<20} {bar} {percentage:>6.1f}%")
        
        print("-"*80)
        print(f"{'TIEMPO TOTAL':<30} {self.timing.format_time(total_time):<20}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['all', 'family'], default='all',
                       help='Modo de ejecución')
    parser.add_argument('--family', choices=['CUL', 'DSJ', 'LEI', 'MYC', 'REG', 'SCH', 'SGB'],
                       help='Familia específica (si mode=family)')
    parser.add_argument('--max-time', type=float, default=300.0,
                       help='Tiempo máximo por instancia (segundos)')
    parser.add_argument('--num-replicas', type=int, default=1,
                       help='Número de réplicas por instancia')
    parser.add_argument('--seed', type=int, default=42,
                       help='Semilla aleatoria')
    parser.add_argument('--verbose', action='store_true',
                       help='Mostrar progreso detallado')
    
    args = parser.parse_args()
    
    # Validar argumentos
    if args.mode == 'family' and not args.family:
        parser.error("--family es requerido cuando --mode=family")
    
    # Crear y ejecutar experimento
    experiment = FullExperiment(
        mode=args.mode,
        family=args.family,
        max_time=args.max_time,
        num_replicas=args.num_replicas,
        seed=args.seed,
        verbose=args.verbose
    )
    
    experiment.run_experiment()


if __name__ == "__main__":
    main()
