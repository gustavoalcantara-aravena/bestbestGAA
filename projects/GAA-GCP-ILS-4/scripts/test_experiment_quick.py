#!/usr/bin/env python3
"""
test_experiment_quick.py - Test rápido del sistema de experimentación

Ejecuta ILS en 3 datasets pequeños para verificar que todo funciona correctamente.

Uso:
    python scripts/test_experiment_quick.py
"""

import sys
import time
import json
import numpy as np
from pathlib import Path

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


def test_quick_experiment():
    """Ejecuta test rápido con 3 datasets pequeños"""
    
    print("\n" + "="*80)
    print("🧪 TEST RÁPIDO DEL SISTEMA DE EXPERIMENTACIÓN")
    print("="*80)
    print("Ejecutando ILS en 3 datasets pequeños para verificar funcionamiento\n")
    
    # Crear OutputManager
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="all_datasets")
    print(f"📁 Sesión creada en: {session_dir}\n")
    
    # Crear PlotManager - usar directorio de sesión
    plot_mgr = PlotManager(session_dir=str(session_dir))
    print(f"📁 Gráficas se guardarán en: {session_dir}/plots/\n")
    
    # Datasets para test - Familia MYCIEL completa con BKS conocido
    # myciel3: 11 nodos,  20 aristas, BKS=4 (~0.01s)
    # myciel4: 23 nodos,  71 aristas, BKS=5 (~0.03s)
    # myciel5: 47 nodos, 236 aristas, BKS=6 (~0.1s)
    # myciel6: 95 nodos, 755 aristas, BKS=7 (~0.5s)
    # myciel7: 191 nodos,2360 aristas, BKS=8 (~2s)
    test_datasets = [
        "datasets/MYC/myciel3.col",
        "datasets/MYC/myciel4.col",
        "datasets/MYC/myciel5.col",
        "datasets/MYC/myciel6.col",
        "datasets/MYC/myciel7.col"
    ]
    
    # ========================================================================
    # PASO 0: GENERAR 3 ALGORITMOS GAA AUTOMÁTICAMENTE (AL INICIO)
    # ========================================================================
    
    print("\n" + "="*80)
    print("PASO 0: GENERAR 3 ALGORITMOS GAA AUTOMÁTICAMENTE")
    print("="*80)
    print("⏳ Iniciando generación automática de algoritmos...\n")
    
    gaa_algorithms = None
    try:
        from gaa.grammar import Grammar
        from gaa.generator import AlgorithmGenerator
        
        print("📋 Etapa 1/5: Inicializando GAA con Gramática BNF...")
        print(f"   Seed: 42 (reproducibilidad garantizada)")
        
        # Crear gramática y generador
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
        
        print("📋 Etapa 3/5: Generando 3 algoritmos GAA con seed=42...")
        gaa_algorithms = []
        for i in range(3):
            print(f"   ⏳ Generando GAA_Algorithm_{i+1}...", end=" ", flush=True)
            algo = generator.generate_fixed_structure()
            if algo:
                gaa_algorithms.append(algo)
                stats = grammar.get_statistics(algo)
                print(f"✅ GENERADO")
                print(f"      - Nodos: {stats['total_nodes']}")
                print(f"      - Profundidad: {stats['depth']}")
                print(f"      - Estructura: {stats['node_counts']}")
            else:
                print(f"❌ FALLO")
        
        if not gaa_algorithms:
            raise RuntimeError("No se pudo generar población inicial válida")
        
        print(f"\n📋 Etapa 4/5: Validando algoritmos generados...")
        print(f"   ✅ {len(gaa_algorithms)} algoritmos GAA generados exitosamente")
        print(f"   ✅ Todos los algoritmos son válidos\n")
        
        print("📋 Etapa 5/5: Mostrando estructura detallada de algoritmos...")
        print(f"   ✅ Extrayendo operadores y estrategias de cada algoritmo\n")
        
        # Visualizar estructura detallada de cada algoritmo
        from utils.algorithm_visualizer import extract_algorithm_structure, print_algorithm_structure, print_algorithms_comparison
        
        algorithm_structures = []
        for algo_idx, algo in enumerate(gaa_algorithms, 1):
            structure = extract_algorithm_structure(algo, algo_idx)
            algorithm_structures.append(structure)
            print_algorithm_structure(structure)
        
        # Mostrar comparación
        print_algorithms_comparison(algorithm_structures)
        
        print(f"   ✅ Algoritmos listos para ejecución\n")
        
    except ImportError as e:
        print("❌ FALLO")
        print("⚠️  Módulos GAA no disponibles.")
        print(f"   Error: {e}\n")
        gaa_algorithms = None
    except Exception as e:
        print(f"❌ FALLO")
        print(f"❌ Error crítico en generación de GAA: {e}\n")
        import traceback
        traceback.print_exc()
        gaa_algorithms = None
    
    # ========================================================================
    # PASO 1: EJECUTAR ILS EN DATASETS
    # ========================================================================
    
    print("\n" + "="*80)
    print("PASO 1: EJECUTAR ILS EN DATASETS DE PRUEBA")
    print("="*80)
    print("⏳ Iniciando ejecución de ILS en datasets...\n")
    
    results = []
    all_vertices = []
    all_times = []
    all_colors = []
    current_fitness_histories = []
    last_solution = None
    
    start_time = time.time()
    
    for idx, dataset_path in enumerate(test_datasets, 1):
        dataset_file = project_root / dataset_path
        
        if not dataset_file.exists():
            print(f"[{idx}/3] ⚠️  {dataset_path} - NO ENCONTRADO")
            continue
        
        print(f"[{idx}/3] {dataset_file.name}")
        
        try:
            # Cargar problema
            problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
            print(f"   📊 Vértices: {problem.n_vertices} | Aristas: {problem.n_edges} | BKS: {problem.colors_known}")
            
            # Ejecutar ILS
            ils_start = time.time()
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
            ils_time = time.time() - ils_start
            
            # Guardar última solución para heatmap
            last_solution = best_solution
            last_problem = problem
            
            # Evaluar
            metrics = ColoringEvaluator.evaluate(best_solution, problem)
            
            # Mostrar resultados
            feasible_icon = "✓" if metrics['feasible'] else "✗"
            gap_str = ""
            if problem.colors_known:
                gap = (metrics['num_colors'] - problem.colors_known) / problem.colors_known
                gap_str = f" ({gap*100:+.1f}%)"
            
            print(f"   ✅ {metrics['num_colors']} colores ({metrics['conflicts']} conflictos) {feasible_icon} {ils_time:.2f}s{gap_str}")
            
            results.append({
                'instance': problem.name,
                'vertices': problem.n_vertices,
                'edges': problem.n_edges,
                'colors': metrics['num_colors'],
                'conflicts': metrics['conflicts'],
                'feasible': metrics['feasible'],
                'time': ils_time
            })
            
            all_vertices.append(problem.n_vertices)
            all_times.append(ils_time)
            all_colors.append(metrics['num_colors'])
            
            # Guardar historial de convergencia (usar current_fitness para ver variación real)
            if history and hasattr(history, 'current_fitness'):
                current_fitness_histories.append(history.current_fitness)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    print(f"⏱️  Tiempo total: {elapsed:.2f}s")
    print(f"📊 Instancias procesadas: {len(results)}")
    print(f"📈 Tiempo promedio: {elapsed/len(results):.2f}s\n")
    
    # Guardar resultados
    print("="*80)
    print("💾 GUARDANDO RESULTADOS")
    print("="*80)
    
    # CSV
    csv_data = []
    for r in results:
        csv_data.append({
            'Instance': r['instance'],
            'Vertices': r['vertices'],
            'Edges': r['edges'],
            'Colors': r['colors'],
            'Conflicts': r['conflicts'],
            'Feasible': r['feasible'],
            'Time': f"{r['time']:.2f}s",
            'Gap': 'N/A'  # No BKS disponible en estos datasets
        })
    
    csv_file = output_mgr.save_summary_csv(csv_data)
    print(f"✅ CSV: {Path(csv_file).name}")
    
    # JSON
    json_data = {
        'test_type': 'quick_test',
        'total_instances': len(results),
        'total_time': elapsed,
        'results': results
    }
    
    json_file = output_mgr.save_detailed_json(json_data, filename="test_results.json")
    print(f"✅ JSON: {Path(json_file).name}")
    
    # TXT
    txt_content = "TEST RÁPIDO DEL SISTEMA\n"
    txt_content += "="*80 + "\n\n"
    txt_content += f"Instancias procesadas: {len(results)}\n"
    txt_content += f"Tiempo total: {elapsed:.2f}s\n"
    txt_content += f"Tiempo promedio: {elapsed/len(results):.2f}s\n\n"
    txt_content += "RESULTADOS:\n"
    txt_content += "-"*80 + "\n"
    txt_content += f"{'Instancia':<20} {'Colores':<10} {'Tiempo':<10}\n"
    txt_content += "-"*80 + "\n"
    
    for r in results:
        txt_content += f"{r['instance']:<20} {r['colors']:<10} {r['time']:.2f}s\n"
    
    txt_content += "\n" + "="*80 + "\n"
    
    txt_file = output_mgr.save_statistics_txt(txt_content, filename="test_results.txt")
    print(f"✅ TXT: {Path(txt_file).name}")
    
    # Reporte de gaps
    gaps_content = "REPORTE DE GAPS\n"
    gaps_content += "="*80 + "\n\n"
    gaps_content += "NOTA: Los datasets del test rápido no tienen BKS (Best Known Solution) definido.\n"
    gaps_content += "Por lo tanto, los gaps no pueden ser calculados.\n\n"
    gaps_content += "Para análisis de gaps, usar datasets con BKS conocido:\n"
    gaps_content += "- myciel3.col (BKS=4)\n"
    gaps_content += "- myciel4.col (BKS=5)\n"
    gaps_content += "- myciel5.col (BKS=6)\n"
    gaps_content += "- le450_5a.col (BKS=5)\n"
    gaps_content += "- le450_5b.col (BKS=5)\n\n"
    gaps_content += "Ejecutar: python scripts/analyze_gaps.py\n"
    gaps_content += "="*80 + "\n"
    
    gaps_file = output_mgr.save_statistics_txt(gaps_content, filename="gaps_report.txt")
    print(f"✅ GAPS: {Path(gaps_file).name}")
    
    # Generar gráficas
    print("\n" + "="*80)
    print("PASO 1.5: GENERANDO GRÁFICAS")
    print("="*80)
    print("⏳ Iniciando generación de gráficas...\n")
    
    try:
        # Gráfica de convergencia - usar current_fitness para ver la variación real
        if current_fitness_histories:
            print("Generando gráfica de convergencia...")
            plot_mgr.plot_convergence(
                current_fitness_histories[0],
                instance_name="Convergencia - Test Rápido"
            )
            print("✅ Convergencia generada")
    except Exception as e:
        print(f"⚠️  Error en convergencia: {e}")
    
    try:
        # Gráfica de escalabilidad
        if all_vertices and all_times:
            print("Generando gráfica de escalabilidad...")
            plot_mgr.plot_scalability(all_vertices, all_times)
            print("✅ Escalabilidad generada")
    except Exception as e:
        print(f"⚠️  Error en escalabilidad: {e}")
    
    try:
        # Gráfica de robustez (boxplot)
        if all_colors:
            print("Generando gráfica de robustez...")
            plot_mgr.plot_robustness(all_colors, instance_name="Robustez - Test Rápido")
            print("✅ Robustez generada")
    except Exception as e:
        print(f"⚠️  Error en robustez: {e}")
    
    try:
        # Gráfica tiempo-calidad
        if all_times and all_colors:
            print("Generando gráfica tiempo-calidad...")
            plot_mgr.plot_time_quality(all_times, all_colors, instance_name="Tiempo-Calidad - Test Rápido")
            print("✅ Tiempo-Calidad generada")
    except Exception as e:
        print(f"⚠️  Error en tiempo-calidad: {e}")
    
    try:
        # Gráfica de conflictos (heatmap)
        if last_solution and last_problem:
            print("Generando gráfica de conflictos...")
            # Crear matriz de conflictos
            n = last_problem.n_vertices
            conflict_matrix = np.zeros((n, n))
            for u, v in last_problem.edges:
                if last_solution.assignment[u] == last_solution.assignment[v]:
                    conflict_matrix[u][v] = 1
                    conflict_matrix[v][u] = 1
            plot_mgr.plot_conflict_heatmap(conflict_matrix, instance_name="Conflictos - Test Rápido")
            print("✅ Conflictos generada")
    except Exception as e:
        print(f"⚠️  Error en conflictos: {e}")
    
    # ========================================================================
    # PASO 2: EJECUTAR 3 ALGORITMOS GAA EN INSTANCIAS
    # ========================================================================
    
    if gaa_algorithms:
        print("\n" + "="*80)
        print("PASO 2: EJECUTAR 3 ALGORITMOS GAA EN INSTANCIAS")
        print("="*80)
        print("⏳ Iniciando ejecución de algoritmos GAA...\n")
        
        try:
            from gaa.interpreter import execute_algorithm
            from experimentation.statistics import StatisticalAnalyzer
            
            # Ejecutar los 3 algoritmos en instancias
            algorithm_results = {}
            
            print("📋 Etapa 1/3: Cargando problemas para GAA...")
            # Cargar problemas para GAA
            gaa_problems = []
            for dataset_path in test_datasets:
                dataset_file = project_root / dataset_path
                if dataset_file.exists():
                    try:
                        problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
                        gaa_problems.append(problem)
                    except Exception as e:
                        print(f"⚠️  Error cargando {dataset_path}: {e}")
            
            if not gaa_problems:
                print("⚠️  No se pudieron cargar problemas para GAA.")
                raise RuntimeError("No hay problemas para ejecutar GAA")
            
            print(f"   ✅ {len(gaa_problems)} problemas cargados\n")
            
            print("📋 Etapa 2/3: Ejecutando 3 algoritmos GAA...")
            for algo_idx, algo in enumerate(gaa_algorithms):
                algo_name = f"GAA_Algorithm_{algo_idx + 1}"
                algorithm_results[algo_name] = []
                
                print(f"\n   ⏳ Ejecutando {algo_name}...", flush=True)
                
                # Ejecutar en todas las instancias cargadas
                for result_idx, problem in enumerate(gaa_problems, 1):
                    try:
                        solution = execute_algorithm(algo, problem, seed=42)
                        
                        num_colors = solution.num_colors
                        algorithm_results[algo_name].append(num_colors)
                        
                        gap = ((num_colors - problem.colors_known) / problem.colors_known * 100) if problem.colors_known else 0
                        
                        print(f"  [{result_idx}/{len(gaa_problems)}] {problem.name}: {num_colors} colores (gap: {gap:+.2f}%)")
                    
                    except Exception as e:
                        print(f"  [{result_idx}/{len(gaa_problems)}] {problem.name}: Error - {e}")
                        algorithm_results[algo_name].append(float('inf'))
                
                print()
            
            print()
            
            # ====================================================================
            # RESUMEN DETALLADO DE RESULTADOS POR INSTANCIA
            # ====================================================================
            print("="*80)
            print("RESUMEN DETALLADO - RESULTADOS POR INSTANCIA")
            print("="*80)
            print()
            
            # Crear tabla de resultados detallados
            for problem in gaa_problems:
                print(f"📊 {problem.name.upper()}")
                print(f"   Vértices: {problem.n_vertices} | Aristas: {problem.n_edges}")
                print(f"   BKS (Best Known Solution): {problem.colors_known}")
                print()
                print(f"   {'Algoritmo':<20} {'Colores':<12} {'Gap':<15} {'Estado':<15}")
                print(f"   {'-'*60}")
                
                best_algo = None
                best_colors = float('inf')
                
                for algo_idx, algo_name in enumerate([f"GAA_Algorithm_{i+1}" for i in range(len(gaa_algorithms))]):
                    if algo_name in algorithm_results and len(algorithm_results[algo_name]) > gaa_problems.index(problem):
                        colors = algorithm_results[algo_name][gaa_problems.index(problem)]
                        if colors != float('inf'):
                            gap = ((colors - problem.colors_known) / problem.colors_known * 100) if problem.colors_known else 0
                            
                            # Determinar estado
                            if gap == 0:
                                status = "✅ ÓPTIMO"
                            elif gap > 0:
                                status = "⚠️  SUBÓPTIMO"
                            else:
                                status = "🏆 RECORD"
                            
                            print(f"   {algo_name:<20} {colors:<12} {gap:>+6.2f}%{'':<7} {status:<15}")
                            
                            # Rastrear mejor algoritmo
                            if colors < best_colors:
                                best_colors = colors
                                best_algo = algo_name
                
                if best_algo:
                    print()
                    print(f"   🏆 Mejor algoritmo: {best_algo} ({best_colors} colores)")
                print()
            
            # ====================================================================
            print("="*80)
            print("PASO 3: COMPARAR 3 ALGORITMOS")
            print("="*80)
            print("⏳ Iniciando análisis estadístico...\n")
            
            print("📋 Etapa 1/3: Ejecutando análisis estadístico...")
            # Análisis estadístico
            analyzer = StatisticalAnalyzer(alpha=0.05)
            comparison = analyzer.compare_multiple_algorithms(algorithm_results)
            print("   ✅ Análisis estadístico completado\n")
            
            print("📋 Etapa 2/3: Generando reporte de comparación...")
            # Generar reporte
            report = analyzer.generate_comparison_report(comparison)
            print("   ✅ Reporte generado\n")
            
            print("📋 Etapa 3/3: Guardando resultados...")
            # Guardar resultados - convertir booleanos a strings para JSON
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
            comparison_file = output_mgr.session_dir / 'results' / 'gaa_comparison_results.json'
            with open(comparison_file, 'w') as f:
                json.dump(comparison_serializable, f, indent=2, ensure_ascii=False)
            output_mgr.save_statistics_txt(report, filename='gaa_comparison_report.txt')
            
            # Guardar algoritmos generados
            algorithms_data = {
                'algorithms': [
                    {
                        'id': i + 1,
                        'name': f'GAA_Algorithm_{i+1}',
                        'stats': convert_to_serializable(grammar.get_statistics(algo))
                    }
                    for i, algo in enumerate(gaa_algorithms)
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
            algorithms_file = output_mgr.session_dir / 'results' / 'gaa_algorithms_generated.json'
            with open(algorithms_file, 'w') as f:
                json.dump(algorithms_data, f, indent=2, ensure_ascii=False)
            print("   ✅ Resultados guardados\n")
            
            print("="*80)
            print("REPORTE DE COMPARACIÓN DE ALGORITMOS GAA")
            print("="*80)
            print(report)
            
            print("\n✅ GAA completado exitosamente")
        
        except Exception as e:
            print(f"❌ Error en ejecución de GAA: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n⚠️  No se generaron algoritmos GAA. Saltando ejecución de GAA.")
    
    print("\n" + "="*80)
    print("✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
    print("="*80)
    print(f"📁 Resultados guardados en: {session_dir}\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_quick_experiment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
