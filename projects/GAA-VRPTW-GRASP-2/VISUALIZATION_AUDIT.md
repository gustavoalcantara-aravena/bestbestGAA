"""
ANÁLISIS: Gráficos Generados vs Gráficos Requeridos
====================================================

DOCUMENTACIÓN ENCONTRADA:
- Archivo: 09-outputs-estructura.md
- Dice: "Gráficos canónicos: 11 tipos"
- Menciona en la estructura: "plots/ ├─ convergence_K.png, convergence_D.png, gap_analysis.png, [8-10 gráficos más], route_visualization_*.png"

GRÁFICOS ACTUALMENTE GENERADOS (6 tipos):
✓ 01_performance_comparison.png       - Comparación promedio de distancia por algoritmo
✓ 02_distance_by_instance.png         - Línea: Distancia por instancia
✓ 03_distance_by_family.png           - Barras: Distancia promedio por familia
✓ 04_execution_time.png               - Barras: Tiempo ejecución por algoritmo
✓ 06_algorithms_boxplot.png           - Boxplot: Distribución distancia por algoritmo
✓ 07_family_algorithm_heatmap.png     - Heatmap: Distancia por familia x algoritmo

GRÁFICOS FALTANTES (5-6 tipos):
✗ convergence_K.png                   - Convergencia del número de vehículos (K)
✗ convergence_D.png                   - Convergencia de distancia (D)
✗ gap_analysis.png                    - Análisis de gap vs BKS (mejorado)
✗ route_visualization_*.png            - Visualización de rutas de soluciones
✗ Algorithm Comparison (multi-objetivo) - Comparación K vs D (scatter/pareto)
✗ Robustness Boxplot                  - Distribución por instancia

TOTAL ACTUAL: 6 gráficos
TOTAL REQUERIDO: 11-12 gráficos
DIFERENCIA: Faltan 5-6 gráficos
"""

print(__doc__)
