"""
INTEGRATION GUIDE - Módulo de Visualización

Cómo integrar el módulo visualization en tus scripts de experimento.
"""

# ============================================================================
# OPCIÓN 1: Uso Simple (Funciones Individuales)
# ============================================================================

def example_simple_usage():
    """Usar funciones individuales de visualización."""
    from visualization import (
        plot_convergence_single,
        plot_robustness,
        plot_conflict_heatmap
    )
    import numpy as np
    
    # Después de ejecutar ILS
    history = [50, 48, 46, 45, 45, 44]  # Historial de fitness
    times = [0.1, 0.2, 0.4, 0.7, 1.0, 1.2]  # Tiempos
    
    # Generar gráfica de convergencia
    plot_convergence_single(
        history,
        times=times,
        output_path="output/convergence.png",
        instance_name="DSJC125.1"
    )
    
    # Generar boxplot de robustez (múltiples ejecuciones)
    results = [45, 45, 46, 45, 46, 45, 47, 46, 45, 45]
    plot_robustness(
        results,
        bks=45,
        output_path="output/robustness.png",
        instance_name="DSJC125.1"
    )
    
    # Generar heatmap de conflictos
    conflict_matrix = np.random.randint(0, 2, (50, 50))
    plot_conflict_heatmap(
        conflict_matrix,
        instance_name="DSJC125.1",
        output_path="output/conflicts.png"
    )


# ============================================================================
# OPCIÓN 2: Uso Avanzado (PlotManager - RECOMENDADO)
# ============================================================================

def example_plot_manager_usage():
    """Usar PlotManager para generar todas las gráficas."""
    from visualization import PlotManager
    import numpy as np
    from datetime import datetime
    
    # Crear gestor
    manager = PlotManager(output_dir="output/results")
    
    # Crear directorio de sesión con timestamp
    session_dir = manager.create_session_dir(mode="all_datasets")
    print(f"📁 Sesión creada en: {session_dir}")
    
    # Recopilar datos del experimento
    experiment_data = {
        'instance_name': 'DSJC250.1',
        'convergence': [100, 95, 85, 75, 70, 68, 67, 66, 66, 66],
        'times': [0.1, 0.2, 0.4, 0.7, 1.0, 1.2, 1.5, 1.8, 2.0, 2.1],
        'convergence_histories': [
            [100, 95, 85, 75, 70, 68, 67, 66, 66, 66],
            [100, 90, 80, 72, 68, 67, 66, 65, 65, 65],
            [100, 92, 82, 74, 69, 67, 66, 65, 65, 65],
        ],
        'robustness': [66, 66, 67, 65, 66, 66, 67, 66, 65, 66] * 3,  # 30 ejecuciones
        'bks': 64,
        'vertices': [50, 100, 150, 200, 250],
        'times_scalability': [0.1, 0.3, 0.8, 1.5, 2.8],
        'family_labels': ['LEI', 'LEI', 'LEI', 'DSJ', 'DSJ'],
        'conflict_matrix': np.random.choice([0, 1], (50, 50), p=[0.8, 0.2]),
        'time_fitness_pairs': [(0.1, 95), (0.5, 75), (1.0, 70), (2.0, 67), (3.0, 66)],
    }
    
    # Generar TODAS las gráficas
    results = manager.plot_all(experiment_data, mode="all_datasets")
    
    # Ver resultados
    print("\n✓ Gráficas generadas:")
    for plot_type, filepath in results.items():
        print(f"  - {plot_type}: {filepath}")
    
    # Guardar resumen en JSON
    summary_file = manager.save_summary(experiment_data)
    print(f"\n✓ Resumen guardado: {summary_file}")
    
    return results, summary_file


# ============================================================================
# OPCIÓN 3: Integración en Script de Experimentación
# ============================================================================

def run_experiment_with_visualization():
    """Ejemplo completo de experimento con visualizaciones."""
    from visualization import PlotManager
    from metaheuristic.ils_core import ILS  # Tu implementación de ILS
    import numpy as np
    
    # ==== FASE 1: Ejecutar experimento ====
    ils = ILS(num_iterations=1000)
    instance = "datasets/DSJC250.1.col"
    
    # Ejecución simple
    solution, history = ils.solve(instance)
    
    # Ejecuciones múltiples para estadísticas
    results = []
    histories = []
    for run in range(30):
        sol, hist = ils.solve(instance)
        results.append(sol.num_colors)
        histories.append(hist.best_fitness)
    
    # ==== FASE 2: Generar visualizaciones ====
    manager = PlotManager()
    manager.create_session_dir(mode="single_instance")
    
    experiment_data = {
        'instance_name': 'DSJC250.1',
        'convergence': history.best_fitness,  # Última ejecución
        'times': history.times,
        'convergence_histories': histories,  # Las 30 ejecuciones
        'robustness': results,  # 30 resultados finales
        'bks': 28,  # Best Known Solution (si lo conoces)
        'conflict_matrix': solution.conflict_matrix,
        'time_fitness_pairs': list(zip(history.times, history.best_fitness)),
    }
    
    # Generar gráficas
    viz_results = manager.plot_all(experiment_data)
    
    # Guardar resumen
    manager.save_summary(experiment_data)
    
    # ==== FASE 3: Reportar resultados ====
    print("\n" + "="*70)
    print("RESULTADOS DEL EXPERIMENTO")
    print("="*70)
    print(f"Instancia: DSJC250.1")
    print(f"Media de ejecuciones: {np.mean(results):.2f}")
    print(f"Desv. Est.: {np.std(results):.2f}")
    print(f"Mejor encontrado: {min(results)}")
    print(f"Peor encontrado: {max(results)}")
    print(f"\nGráficas guardadas en: {manager.session_dir}")
    print("="*70)
    
    return viz_results


# ============================================================================
# OPCIÓN 4: Análisis Post-Experimento
# ============================================================================

def analyze_existing_results(results_dir):
    """Analizar resultados ya guardados."""
    from visualization import PlotManager
    import json
    from pathlib import Path
    
    # Cargar datos del resumen
    summary_file = Path(results_dir) / "summary.json"
    with open(summary_file, 'r') as f:
        data = json.load(f)
    
    # Regenerar con diferentes parámetros
    manager = PlotManager()
    manager.session_dir = Path(results_dir)
    
    # Puedes modificar parámetros y regenerar
    # por ejemplo, cambiar escala a logarítmica, etc.


# ============================================================================
# PLANTILLA PARA TUS EXPERIMENTOS
# ============================================================================

"""
# Estructura recomendada en tu script de experimento:

from visualization import PlotManager

def main():
    # Configuración
    instances = ['DSJC125.1', 'DSJC250.1', 'DSJC500.1']
    num_runs = 30
    
    # Crear gestor de visualización
    manager = PlotManager(output_dir="output/results")
    manager.create_session_dir(mode="batch_experiment")
    
    # Loop de experimentos
    for instance_name in instances:
        print(f"\\nProcesando {instance_name}...")
        
        # Tu código de ejecución de ILS
        # ...
        
        # Recopilar datos
        experiment_data = {
            'instance_name': instance_name,
            'convergence': history.best_fitness,
            'convergence_histories': all_histories,
            'robustness': final_results,
            'conflict_matrix': solution.conflict_matrix,
            # ... más datos
        }
        
        # Generar visualizaciones
        results = manager.plot_all(experiment_data)
        
        # Guardar resumen
        manager.save_summary(experiment_data)
    
    print(f"\\n✓ Experimento completado. Resultados en: {manager.session_dir}")

if __name__ == "__main__":
    main()
"""


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def collect_experiment_data(ils_history, solutions_list, instance_info):
    """
    Recopilar datos de experimento en formato compatible con visualization.
    
    Parámetros:
        ils_history: Objeto ILSHistory de una ejecución
        solutions_list: Lista de soluciones (múltiples ejecuciones)
        instance_info: Información de la instancia
    
    Retorna:
        dict: Datos listos para PlotManager.plot_all()
    """
    import numpy as np
    
    data = {
        'instance_name': instance_info.get('name', 'Unknown'),
        'convergence': ils_history.best_fitness,
        'times': ils_history.times,
        'conflict_matrix': solutions_list[0].conflict_matrix if solutions_list else None,
        'time_fitness_pairs': list(zip(ils_history.times, ils_history.best_fitness)),
    }
    
    # Si hay múltiples ejecuciones
    if len(solutions_list) > 1:
        final_colors = [sol.num_colors for sol in solutions_list]
        data['robustness'] = final_colors
        data['bks'] = instance_info.get('bks', min(final_colors))
    
    return data


def load_experiment_summary(summary_json_path):
    """Cargar resumen de experimento desde JSON."""
    import json
    from pathlib import Path
    
    with open(summary_json_path, 'r') as f:
        return json.load(f)


# ============================================================================
# EJECUCIÓN DE EJEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("Ejemplos de integración del módulo visualization\n")
    
    # Ejemplo 1: Uso simple
    print("1️⃣  Ejecutando ejemplo simple...")
    # example_simple_usage()
    
    # Ejemplo 2: PlotManager
    print("\n2️⃣  Ejecutando ejemplo con PlotManager...")
    results, summary = example_plot_manager_usage()
    
    # Ejemplo 3: Script completo
    print("\n3️⃣  Ejemplo de script completo (comentado)")
    print("""
    Ver run_experiment_with_visualization() para ejemplo completo
    """)
