"""
QUICK REFERENCE - Módulo de Visualización

Referencia rápida de funciones y uso
"""

# ============================================================================
# IMPORTS RÁPIDOS
# ============================================================================

from visualization import PlotManager
from visualization import (
    plot_convergence_single,
    plot_convergence_multiple,
    plot_robustness,
    plot_scalability_time,
    plot_conflict_heatmap,
    plot_time_quality_tradeoff
)


# ============================================================================
# CONVERGENCIA
# ============================================================================

# Una ejecución
plot_convergence_single(
    fitness_history=[50, 48, 46, 45],
    times=[0.1, 0.2, 0.4, 0.7],          # Opcional
    output_path="conv.png",
    instance_name="Instance"
)

# Múltiples ejecuciones promediadas
plot_convergence_multiple(
    fitness_histories=[[50, 48, 46], [51, 49, 47]],
    output_path="conv_avg.png"
)


# ============================================================================
# ROBUSTEZ (30+ ejecuciones)
# ============================================================================

plot_robustness(
    results=[45, 45, 46, 45, 46, 45, 47],  # 30+ valores
    bks=45,                                 # Best Known Solution
    output_path="robust.png",
    instance_name="Instance"
)


# ============================================================================
# ESCALABILIDAD
# ============================================================================

plot_scalability_time(
    vertices=[50, 100, 150, 200],
    times=[0.1, 0.3, 0.8, 1.5],
    family_labels=['LEI', 'LEI', 'DSJ', 'DSJ'],  # Opcional
    output_path="scalability.png"
)


# ============================================================================
# CONFLICTOS (Heatmap)
# ============================================================================

import numpy as np

conflict_matrix = np.random.randint(0, 2, (50, 50))
plot_conflict_heatmap(
    conflict_matrix,
    instance_name="Instance",
    output_path="conflicts.png"
)


# ============================================================================
# TIEMPO-CALIDAD
# ============================================================================

plot_time_quality_tradeoff(
    times=[0.1, 0.5, 1.0, 2.0],
    fitness_values=[47, 45, 43, 42],
    instance_name="Instance",
    output_path="tradeoff.png"
)


# ============================================================================
# PLOTMANAGER - RECOMENDADO ⭐
# ============================================================================

# Crear gestor
manager = PlotManager(output_dir="output/results")

# Crear directorio con timestamp
manager.create_session_dir(mode="all_datasets")

# Preparar datos
data = {
    'instance_name': 'DSJC250.1',
    'convergence': [100, 95, 85, 75, 70],
    'convergence_histories': [[100, 95, 85], [100, 90, 80]],
    'robustness': [65, 66, 67, 65, 66],
    'bks': 64,
    'vertices': [50, 100, 150],
    'times': [0.1, 0.3, 0.8],
    'conflict_matrix': np.random.randint(0, 2, (50, 50)),
    'time_fitness_pairs': [(0.1, 95), (0.5, 75), (1.0, 70)]
}

# GENERAR TODAS LAS GRÁFICAS
results = manager.plot_all(data)

# Guardar resumen
manager.save_summary(data)

# Ver resultados
for plot_type, path in results.items():
    print(f"✓ {plot_type}: {path}")


# ============================================================================
# PARÁMETROS COMUNES
# ============================================================================

"""
Parámetros que funcionan en TODAS las funciones:

output_path : str
    Ruta donde guardar la imagen (ej: "output/grafica.png")

instance_name : str
    Nombre de la instancia (ej: "DSJC125.1")

title : str
    Título personalizado (por defecto según tipo)

figsize : tuple
    Tamaño de figura (ancho, alto) en pulgadas
    Default: (12, 7)

dpi : int
    Resolución en puntos por pulgada
    Default: 300 (publicaciones)
    Use 150 para pantalla
"""


# ============================================================================
# EJEMPLO COMPLETO EN EXPERIMENTO
# ============================================================================

def run_experiment():
    """Plantilla de experimento con visualizaciones."""
    from visualization import PlotManager
    
    manager = PlotManager()
    manager.create_session_dir()
    
    # Tu código ILS aquí
    # ...
    history = [100, 95, 85, 75, 70]  # Ejemplo
    
    # Generar visualización
    manager.plot_convergence(
        history,
        instance_name="DSJC250.1"
    )
    
    # Guardar
    manager.save_summary({'instance': 'DSJC250.1', 'history': history})


# ============================================================================
# TIPS ÚTILES
# ============================================================================

"""
1. Múltiples ejecuciones:
   - Para boxplot: mínimo 20-50 ejecuciones
   - Guarda todos los historiales para promediado

2. Escalabilidad:
   - Agrupa instancias por familia DIMACS
   - Usa family_labels para colorear

3. Conflictos:
   - Matriz debe ser simétrica (n×n)
   - Valores 0 (sin conflicto) o 1 (conflicto)

4. Salida:
   - Default: output/results/{modo}/{timestamp}/
   - Personalizar con output_dir en PlotManager

5. Logging:
   - PlotManager loguea automáticamente
   - Ver console para mensajes de progreso

6. Resolución:
   - dpi=300 para PDFs/publicaciones
   - dpi=150 para web/pantalla
   - dpi=100 para draft rápido
"""


# ============================================================================
# ESTRUCTURA DE DATOS ESPERADA
# ============================================================================

"""
experiment_data = {
    # Básico
    'instance_name': str,              # Requerido para títulos
    
    # Convergencia
    'convergence': List[float],        # Fitness final de una ejecución
    'times': List[float],              # Tiempos correspondientes
    'convergence_histories': List[List[float]],  # Múltiples ejecuciones
    
    # Robustez
    'robustness': List[float],         # Resultados finales (30+ valores)
    'bks': float,                      # Best Known Solution (opcional)
    
    # Escalabilidad
    'vertices': List[int],             # Tamaños de instancia |V|
    'times': List[float],              # Tiempos (puede sobrescribir)
    'family_labels': List[str],        # Familias DIMACS (opcional)
    
    # Conflictos
    'conflict_matrix': np.ndarray,     # Matriz n×n booleana
    
    # Tiempo-Calidad
    'time_fitness_pairs': List[Tuple[float, float]]  # (tiempo, fitness)
}
"""


# ============================================================================
# ATAJOS ÚTILES
# ============================================================================

# Crear gestor y generar TODO en 3 líneas
from visualization import PlotManager
manager = PlotManager()
manager.plot_all({'instance_name': 'X', 'convergence': [...]})

# Función auxiliar: convertir datos ILSHistory
def get_experiment_data(ils_history, instance_name):
    return {
        'instance_name': instance_name,
        'convergence': ils_history.best_fitness,
        'times': ils_history.times,
        'time_fitness_pairs': list(zip(
            ils_history.times,
            ils_history.best_fitness
        ))
    }


# ============================================================================
# TROUBLESHOOTING RÁPIDO
# ============================================================================

"""
❌ Error: "No module named 'visualization'"
✅ Solución: Asegúrate de estar en el directorio raíz del proyecto

❌ Error: "Output directory not created"
✅ Solución: PlotManager crea automáticamente directorios

❌ Gráfica sale borrosa
✅ Solución: Aumenta dpi (dpi=300)

❌ Gráfica se ve rara
✅ Solución: Verifica que los datos sean correctos (len > 0)

❌ ImportError con scipy/numpy
✅ Solución: pip install -r requirements.txt
"""


# ============================================================================
# DOCUMENTACIÓN
# ============================================================================

"""
📖 Documentación completa en:
   - visualization/README.md (420 líneas)
   
🎓 Ejemplos en:
   - visualization/example_usage.py
   - visualization/INTEGRATION_GUIDE.py
   
📋 Detalles técnicos en:
   - visualization/IMPLEMENTACION.md
   
⚡ Código fuente:
   - visualization/*.py (cada función tiene docstring)
"""


# ============================================================================
if __name__ == "__main__":
    print("📊 Referencia rápida de visualization")
    print("Ver docstrings en visualization/*.py para detalles")
