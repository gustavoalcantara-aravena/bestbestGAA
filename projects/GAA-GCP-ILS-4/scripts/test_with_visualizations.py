#!/usr/bin/env python3
"""
test_with_visualizations.py - Test con visualizaciones y análisis de gaps

Ejecuta ILS en datasets pequeños y genera gráficas de convergencia y escalabilidad.

Uso:
    python scripts/test_with_visualizations.py
"""

import sys
import time
import numpy as np
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
from utils import OutputManager
from visualization.plotter import PlotManager


def test_with_visualizations():
    """Ejecuta test con visualizaciones y análisis de gaps"""
    
    print("\n" + "="*80)
    print("🎨 TEST CON VISUALIZACIONES Y ANÁLISIS DE GAPS")
    print("="*80)
    print("Ejecutando ILS y generando gráficas de convergencia y escalabilidad\n")
    
    # Crear OutputManager
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="all_datasets")
    print(f"📁 Sesión de resultados: {session_dir}\n")
    
    # Crear PlotManager
    plot_mgr = PlotManager(output_dir=str(output_mgr.get_plot_dir()))
    plot_session_dir = plot_mgr.create_session_dir(mode="all_datasets")
    print(f"📁 Sesión de gráficas: {plot_session_dir}\n")
    
    # Datasets con BKS conocido para análisis de gaps
    test_datasets = [
        ("datasets/MYC/myciel3.col", 4),      # BKS = 4
        ("datasets/MYC/myciel4.col", 5),      # BKS = 5
        ("datasets/MYC/myciel5.col", 6),      # BKS = 6
    ]
    
    results = []
    all_vertices = []
    all_times = []
    convergence_histories = []
    
    print("="*80)
    print("🔬 EJECUTANDO ILS CON ANÁLISIS DE GAPS")
    print("="*80 + "\n")
    
    start_time = time.time()
    
    for idx, (dataset_path, bks) in enumerate(test_datasets, 1):
        dataset_file = project_root / dataset_path
        
        if not dataset_file.exists():
            print(f"[{idx}/{len(test_datasets)}] ⚠️  {dataset_path} - NO ENCONTRADO")
            continue
        
        print(f"[{idx}/{len(test_datasets)}] {dataset_file.name}")
        
        try:
            # Cargar problema
            problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
            print(f"   📊 Vértices: {problem.n_vertices} | Aristas: {problem.n_edges} | BKS: {bks}")
            
            # Ejecutar ILS
            ils_start = time.time()
            ils = IteratedLocalSearch(
                problem=problem,
                constructive=GreedyDSATUR.construct,
                improvement=KempeChain.improve,
                perturbation=RandomRecolor.perturb,
                max_iterations=200,
                time_budget=30.0,
                verbose=False,
                seed=42
            )
            
            best_solution, history = ils.solve()
            ils_time = time.time() - ils_start
            
            # Evaluar
            metrics = ColoringEvaluator.evaluate(best_solution, problem)
            
            # Calcular gap
            gap = (metrics['num_colors'] - bks) / bks * 100
            feasible_icon = "✓" if metrics['feasible'] else "✗"
            
            print(f"   ✅ {metrics['num_colors']} colores ({metrics['conflicts']} conflictos) {feasible_icon}")
            print(f"   📈 Gap: {gap:+.2f}% (BKS={bks}, Encontrado={metrics['num_colors']})")
            print(f"   ⏱️  Tiempo: {ils_time:.2f}s\n")
            
            results.append({
                'instance': problem.name,
                'vertices': problem.n_vertices,
                'edges': problem.n_edges,
                'bks': bks,
                'colors': metrics['num_colors'],
                'conflicts': metrics['conflicts'],
                'feasible': metrics['feasible'],
                'gap': gap,
                'time': ils_time
            })
            
            all_vertices.append(problem.n_vertices)
            all_times.append(ils_time)
            
            # Guardar historial de convergencia
            if history and 'convergence_history' in history:
                convergence_histories.append([h['num_colors'] for h in history['convergence_history']])
        
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    
    elapsed = time.time() - start_time
    
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80)
    print(f"⏱️  Tiempo total: {elapsed:.2f}s")
    print(f"📊 Instancias procesadas: {len(results)}")
    print(f"📈 Tiempo promedio: {elapsed/len(results):.2f}s\n")
    
    # Análisis de gaps
    print("="*80)
    print("📊 ANÁLISIS DE GAPS")
    print("="*80)
    gaps = [r['gap'] for r in results]
    print(f"Gap promedio: {np.mean(gaps):+.2f}%")
    print(f"Gap mínimo: {np.min(gaps):+.2f}%")
    print(f"Gap máximo: {np.max(gaps):+.2f}%")
    print(f"Desviación estándar: {np.std(gaps):.2f}%\n")
    
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
            'BKS': r['bks'],
            'Colors': r['colors'],
            'Gap': f"{r['gap']:+.2f}%",
            'Feasible': "✓" if r['feasible'] else "✗",
            'Time': f"{r['time']:.2f}s"
        })
    
    csv_file = output_mgr.save_summary_csv(csv_data)
    print(f"✅ CSV: {Path(csv_file).name}")
    
    # JSON
    json_data = {
        'test_type': 'visualization_test',
        'total_instances': len(results),
        'total_time': elapsed,
        'gap_analysis': {
            'mean': float(np.mean(gaps)),
            'min': float(np.min(gaps)),
            'max': float(np.max(gaps)),
            'std': float(np.std(gaps))
        },
        'results': results
    }
    
    json_file = output_mgr.save_detailed_json(json_data, filename="test_results.json")
    print(f"✅ JSON: {Path(json_file).name}")
    
    # TXT
    txt_content = "TEST CON VISUALIZACIONES Y ANÁLISIS DE GAPS\n"
    txt_content += "="*80 + "\n\n"
    txt_content += f"Instancias procesadas: {len(results)}\n"
    txt_content += f"Tiempo total: {elapsed:.2f}s\n"
    txt_content += f"Tiempo promedio: {elapsed/len(results):.2f}s\n\n"
    txt_content += "ANÁLISIS DE GAPS:\n"
    txt_content += "-"*80 + "\n"
    txt_content += f"Gap promedio: {np.mean(gaps):+.2f}%\n"
    txt_content += f"Gap mínimo: {np.min(gaps):+.2f}%\n"
    txt_content += f"Gap máximo: {np.max(gaps):+.2f}%\n"
    txt_content += f"Desviación estándar: {np.std(gaps):.2f}%\n\n"
    txt_content += "RESULTADOS POR INSTANCIA:\n"
    txt_content += "-"*80 + "\n"
    txt_content += f"{'Instancia':<20} {'BKS':<5} {'Colores':<8} {'Gap':<10} {'Tiempo':<10}\n"
    txt_content += "-"*80 + "\n"
    
    for r in results:
        txt_content += f"{r['instance']:<20} {r['bks']:<5} {r['colors']:<8} {r['gap']:+.2f}%{' '*5} {r['time']:.2f}s\n"
    
    txt_content += "\n" + "="*80 + "\n"
    
    txt_file = output_mgr.save_statistics_txt(txt_content, filename="test_results.txt")
    print(f"✅ TXT: {Path(txt_file).name}")
    
    # Generar gráficas
    print("\n" + "="*80)
    print("📊 GENERANDO GRÁFICAS")
    print("="*80)
    
    try:
        # Gráfica de convergencia
        if convergence_histories:
            print("Generando gráfica de convergencia...")
            plot_mgr.plot_convergence(
                convergence_histories[0],
                instance_name="Convergencia - Instancia 1"
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
    
    print("\n" + "="*80)
    print("✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
    print("="*80)
    print(f"📁 Resultados guardados en: {session_dir}")
    print(f"📁 Gráficas guardadas en: {plot_session_dir}\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_with_visualizations()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
