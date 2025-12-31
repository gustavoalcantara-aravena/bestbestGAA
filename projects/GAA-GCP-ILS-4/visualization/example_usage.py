"""
visualization/example_usage.py
Ejemplos de uso del módulo de visualización

Demuestra cómo utilizar las funciones de visualización con datos sintéticos.
"""

import numpy as np
from pathlib import Path
from .plotter import PlotManager
from .convergence import plot_convergence_single, plot_convergence_multiple
from .robustness import plot_robustness
from .scalability import plot_scalability_time
from .heatmap import plot_conflict_heatmap
from .time_quality import plot_time_quality_tradeoff


def example_convergence():
    """Ejemplo: Gráfica de convergencia simple."""
    print("📊 Generando ejemplo de convergencia...")
    
    # Datos sintéticos
    fitness_history = [50, 48, 46, 45, 45, 44, 44, 43, 43, 43]
    times = [0.1 * i for i in range(len(fitness_history))]
    
    output_path = Path("output/examples/convergence_example.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plot_convergence_single(
        fitness_history,
        times=times,
        output_path=str(output_path),
        instance_name="myciel3",
        title="Convergencia de ILS"
    )
    
    print(f"✓ Guardado: {output_path}")


def example_robustness():
    """Ejemplo: Boxplot de robustez."""
    print("📊 Generando ejemplo de robustez...")
    
    # Datos sintéticos (30 ejecuciones)
    results = [45, 45, 46, 45, 46, 45, 47, 46, 45, 45,
               45, 46, 45, 44, 45, 46, 45, 45, 46, 45,
               46, 45, 47, 46, 45, 45, 45, 46, 45, 44]
    
    output_path = Path("output/examples/robustness_example.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plot_robustness(
        results,
        bks=45,
        output_path=str(output_path),
        instance_name="DSJC125.1",
        title="Robustez de ILS (30 ejecuciones)"
    )
    
    print(f"✓ Guardado: {output_path}")


def example_scalability():
    """Ejemplo: Gráfica de escalabilidad."""
    print("📊 Generando ejemplo de escalabilidad...")
    
    # Datos sintéticos
    vertices = [50, 100, 150, 200, 250, 300, 350, 400]
    times = [0.1, 0.3, 0.8, 1.5, 2.8, 4.5, 6.5, 9.0]
    families = ['LEI' if v < 200 else 'DSJ' for v in vertices]
    
    output_path = Path("output/examples/scalability_example.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plot_scalability_time(
        vertices,
        times,
        family_labels=families,
        output_path=str(output_path),
        title="Escalabilidad de ILS"
    )
    
    print(f"✓ Guardado: {output_path}")


def example_heatmap():
    """Ejemplo: Heatmap de conflictos."""
    print("📊 Generando ejemplo de heatmap...")
    
    # Matriz de conflictos sintética
    n = 20
    conflict_matrix = np.random.choice([0, 1], size=(n, n), p=[0.8, 0.2])
    conflict_matrix = np.triu(conflict_matrix, 1)  # Triangular superior
    conflict_matrix = conflict_matrix + conflict_matrix.T  # Simétrica
    
    output_path = Path("output/examples/heatmap_example.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plot_conflict_heatmap(
        conflict_matrix,
        instance_name="DSJC125.1",
        output_path=str(output_path)
    )
    
    print(f"✓ Guardado: {output_path}")


def example_time_quality():
    """Ejemplo: Gráfica tiempo-calidad."""
    print("📊 Generando ejemplo de tiempo-calidad...")
    
    # Datos sintéticos
    times = [0.1, 0.5, 1.0, 2.0, 3.0, 5.0]
    fitness = [47, 45, 43, 42, 41, 41]
    
    output_path = Path("output/examples/time_quality_example.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plot_time_quality_tradeoff(
        times,
        fitness,
        instance_name="DSJC125.1",
        output_path=str(output_path)
    )
    
    print(f"✓ Guardado: {output_path}")


def example_all_plots():
    """Ejemplo: Generar todas las gráficas con PlotManager."""
    print("📊 Generando todas las gráficas...")
    
    manager = PlotManager(output_dir="output/examples")
    manager.create_session_dir(mode="test")
    
    # Preparar datos
    experiment_data = {
        'instance_name': 'DSJC250.1',
        'convergence': [100, 95, 85, 75, 70, 68, 67, 67, 66, 66],
        'convergence_histories': [
            [100, 95, 85, 75, 70, 68, 67, 67, 66, 66],
            [100, 90, 80, 72, 68, 67, 66, 66, 65, 65],
            [100, 92, 82, 74, 69, 67, 66, 65, 65, 65]
        ],
        'robustness': [66, 66, 67, 65, 66, 66, 67, 66, 65, 66],
        'bks': 64,
        'vertices': [50, 100, 150, 200, 250],
        'times': [0.1, 0.3, 0.8, 1.5, 2.8],
        'time_fitness_pairs': [(0.1, 95), (0.5, 75), (1.0, 70), (2.0, 67), (3.0, 66)]
    }
    
    # Generar todas las gráficas
    results = manager.plot_all(experiment_data, mode="test")
    
    print("\n✓ Gráficas generadas:")
    for plot_type, path in results.items():
        print(f"  - {plot_type}: {path}")
    
    # Guardar resumen
    manager.save_summary(experiment_data)


def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("EJEMPLOS DE USO - MÓDULO DE VISUALIZACIÓN")
    print("=" * 70)
    print()
    
    try:
        example_convergence()
        example_robustness()
        example_scalability()
        example_heatmap()
        example_time_quality()
        example_all_plots()
        
        print("\n" + "=" * 70)
        print("✓ Todos los ejemplos completados exitosamente")
        print("=" * 70)
    
    except Exception as e:
        print(f"\n✗ Error durante la generación de ejemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
