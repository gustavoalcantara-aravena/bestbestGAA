# Módulo de Visualización - Guía Completa

## 📊 Descripción

El módulo `visualization` proporciona funcionalidades completas para generar visualizaciones de resultados de experimentos con el algoritmo ILS (Iterated Local Search) aplicado al Graph Coloring Problem.

## 📁 Estructura del Módulo

```
visualization/
├── __init__.py                 # Inicialización del módulo
├── convergence.py             # Gráficas de convergencia (fitness vs iteraciones)
├── robustness.py              # Boxplots de robustez (distribución estadística)
├── scalability.py             # Análisis de escalabilidad (|V| vs tiempo/iteraciones)
├── heatmap.py                 # Heatmaps de matriz de conflictos
├── time_quality.py            # Análisis tiempo-calidad (tradeoff)
├── plotter.py                 # Gestor centralizado (PlotManager)
├── example_usage.py           # Ejemplos de uso
└── README.md                  # Esta documentación
```

## 🎯 Tipos de Visualizaciones

### 1. **Convergencia** (`convergence.py`)

Visualiza el comportamiento dinámico del algoritmo durante la búsqueda.

#### Funciones:

- **`plot_convergence_single()`**: Gráfica de una única ejecución
  - Muestra fitness actual vs mejor encontrado
  - Opcional: línea de tiempo en eje secundario
  - Estadísticas incrustadas

- **`plot_convergence_multiple()`**: Promediada de N ejecuciones
  - Líneas individuales con transparencia
  - Banda de desviación estándar
  - Zona IQR (Q1-Q3)

- **`plot_convergence_by_family()`**: Comparación entre familias DIMACS
  - 2x2 subgráficas (hasta 4 familias)
  - Una familia por subgráfica

#### Ejemplo de uso:

```python
from visualization import plot_convergence_single

history = [50, 48, 46, 45, 45, 44]
times = [0.1, 0.2, 0.4, 0.7, 1.0, 1.2]

plot_convergence_single(
    history,
    times=times,
    output_path="convergence.png",
    instance_name="DSJC125.1"
)
```

---

### 2. **Robustez** (`robustness.py`)

Análisis estadístico de múltiples ejecuciones (mínimo 20 ejecuciones).

#### Funciones:

- **`plot_robustness()`**: Boxplot individual
  - Mediana, IQR, outliers
  - Línea BKS de referencia
  - Estadísticas: media, desv. estándar, min/max

- **`plot_multi_robustness()`**: Comparación de instancias
  - Múltiples instancias lado a lado
  - Líneas BKS para cada instancia

#### Ejemplo de uso:

```python
from visualization import plot_robustness

# 30 ejecuciones independientes
results = [45, 45, 46, 45, 46, 45, 47, 46, 45, 45, ...]

plot_robustness(
    results,
    bks=45,
    output_path="robustness.png",
    instance_name="DSJC125.1"
)
```

---

### 3. **Escalabilidad** (`scalability.py`)

Análisis del comportamiento vs tamaño de instancia.

#### Funciones:

- **`plot_scalability_time()`**: Tamaño vs tiempo
  - Dispersión con líneas de tendencia polinomial
  - Agrupación por familia DIMACS
  - Escala logarítmica opcional

- **`plot_scalability_iterations()`**: Tamaño vs iteraciones
  - Similar a tiempo, pero con iteraciones

- **`plot_complexity_analysis()`**: 4 subgráficas
  - Tiempo vs |V|
  - Iteraciones vs |V|
  - Tiempo/Iteración vs |V|
  - Análisis logarítmico (estimación O(|V|^k))

#### Ejemplo de uso:

```python
from visualization import plot_scalability_time

vertices = [50, 100, 150, 200, 250]
times = [0.1, 0.3, 0.8, 1.5, 2.8]
families = ['LEI', 'LEI', 'LEI', 'DSJ', 'DSJ']

plot_scalability_time(
    vertices,
    times,
    family_labels=families,
    output_path="scalability.png"
)
```

---

### 4. **Heatmap de Conflictos** (`heatmap.py`)

Visualización de la matriz de conflictos en la solución final.

#### Funciones:

- **`plot_conflict_heatmap()`**: Matriz n×n
  - Color: verde (sin conflicto) a rojo (conflicto)
  - Automático: colorbar y estadísticas
  - Escalable para matrices pequeñas (n ≤ 20)

- **`plot_conflict_distribution()`**: Distribución por vértice
  - Gráfica de barras + histograma
  - Número de conflictos por vértice

- **`plot_conflict_statistics()`**: Análisis de múltiples soluciones
  - 4 subgráficas: conflictos, distribución, ratios, matriz promediada

#### Ejemplo de uso:

```python
from visualization import plot_conflict_heatmap
import numpy as np

# Matriz 20x20 de conflictos (0 o 1)
conflict_matrix = np.random.choice([0, 1], (20, 20), p=[0.8, 0.2])
conflict_matrix = np.triu(conflict_matrix, 1)
conflict_matrix = conflict_matrix + conflict_matrix.T

plot_conflict_heatmap(
    conflict_matrix,
    instance_name="DSJC125.1",
    output_path="conflicts.png"
)
```

---

### 5. **Análisis Tiempo-Calidad** (`time_quality.py`)

Relación entre tiempo de computación y calidad de solución.

#### Funciones:

- **`plot_time_quality_tradeoff()`**: Curva tiempo-fitness
  - Puntos coloreados por progresión temporal
  - Línea conectora
  - Estadísticas de mejora

- **`plot_multiple_algorithms_tradeoff()`**: Comparación de algoritmos
  - Múltiples curvas en un gráfico
  - Diferentes marcadores por algoritmo

- **`plot_convergence_speed()`**: Velocidad de mejora
  - Curva tiempo-fitness
  - Velocidad instantánea (cambio por segundo)

#### Ejemplo de uso:

```python
from visualization import plot_time_quality_tradeoff

times = [0.1, 0.5, 1.0, 2.0, 3.0]
fitness = [47, 45, 43, 42, 41]

plot_time_quality_tradeoff(
    times,
    fitness,
    instance_name="DSJC125.1",
    output_path="time_quality.png"
)
```

---

## 🎛️ PlotManager - Gestor Centralizado

La clase `PlotManager` orquesta la generación de todas las gráficas.

### Características:

- ✅ Creación automática de directorios con timestamps
- ✅ Manejo centralizado de todas las gráficas
- ✅ Logging integrado
- ✅ Guardado de resumen en JSON
- ✅ Manejo de excepciones robusto

### Ejemplo de uso completo:

```python
from visualization import PlotManager
import numpy as np

# Inicializar gestor
manager = PlotManager(output_dir="output/results")
manager.create_session_dir(mode="all_datasets")

# Preparar datos del experimento
experiment_data = {
    'instance_name': 'DSJC250.1',
    'convergence': [100, 95, 85, 75, 70, 68, 67, 66],
    'convergence_histories': [
        [100, 95, 85, 75, 70, 68, 67, 66],
        [100, 90, 80, 72, 68, 67, 66, 65],
        [100, 92, 82, 74, 69, 67, 66, 65]
    ],
    'robustness': [66, 66, 67, 65, 66, 66, 67, 66],
    'bks': 64,
    'vertices': [50, 100, 150, 200],
    'times': [0.1, 0.3, 0.8, 1.5],
    'conflict_matrix': np.random.randint(0, 2, (50, 50)),
    'time_fitness_pairs': [(0.1, 95), (0.5, 75), (1.0, 70), (2.0, 67)]
}

# Generar todas las gráficas
results = manager.plot_all(experiment_data, mode="all_datasets")

# Guardar resumen
manager.save_summary(experiment_data)

# Acceder a resultados
for plot_type, filepath in results.items():
    print(f"✓ {plot_type}: {filepath}")
```

### Métodos principales:

```python
# Crear directorio de sesión
session_dir = manager.create_session_dir(mode="all_datasets")

# Generar gráficas individuales
manager.plot_convergence(history, instance_name="...")
manager.plot_convergence_ensemble(histories, instance_name="...")
manager.plot_robustness(results, bks=45, instance_name="...")
manager.plot_scalability(vertices, times, family_labels=...)
manager.plot_conflict_heatmap(matrix, instance_name="...")
manager.plot_time_quality(times, fitness, instance_name="...")

# Generar todas las gráficas de una vez
results = manager.plot_all(experiment_data)

# Guardar resumen en JSON
manager.save_summary(data)
```

---

## 📤 Estructura de Salida

Las gráficas se guardan en la siguiente estructura:

```
output/results/
└── all_datasets/
    └── {DD-MM-YY_HH-MM-SS}/
        ├── convergence_plot.png
        ├── convergence_ensemble_plot.png
        ├── boxplot_robustness.png
        ├── scalability_plot.png
        ├── conflict_heatmap.png
        ├── time_quality_tradeoff.png
        ├── summary.json
        └── ...
```

---

## 🔧 Configuración y Personalización

### Parámetros Comunes:

```python
# Tamaño de figura (ancho, alto) en pulgadas
figsize = (12, 7)

# Resolución en dpi
dpi = 300  # Alta calidad

# Título personalizado
title = "Mi Gráfica Personalizada"

# Nombre de instancia
instance_name = "DSJC125.1"

# Ruta de salida
output_path = "output/mi_grafica.png"
```

### Mapas de Color:

```python
# Para heatmaps
cmap = 'RdYlGn_r'  # Rojo-Amarillo-Verde (invertido)
cmap = 'viridis'   # Escala perceptual
cmap = 'coolwarm'  # Azul-Rojo
```

---

## 📦 Dependencias

Las siguientes librerías son requeridas:

```
matplotlib>=3.7.0
seaborn>=0.12.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
```

Todas están incluidas en `requirements.txt`.

---

## 🚀 Inicio Rápido

### 1. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar ejemplos

```bash
python -m visualization.example_usage
```

### 3. Usar en tu código

```python
from visualization import PlotManager

# Crear gestor
manager = PlotManager()

# Generar gráficas
results = manager.plot_all(experiment_data)
```

---

## 💡 Tips y Buenas Prácticas

1. **Normalización de datos**: Asegúrate de que los datos estén normalizados si comparas diferentes instancias
2. **Múltiples ejecuciones**: Para robustez, realiza mínimo 20-50 ejecuciones independientes
3. **Resolución**: Usa `dpi=300` para publicaciones; `dpi=150` para pantalla
4. **Colores**: Los mapas de color están optimizados para daltonismo
5. **Legends**: Las leyendas se generan automáticamente; personaliza con `labels`

---

## 🐛 Troubleshooting

### Error: "No module named 'visualization'"

```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd /path/to/GAA-GCP-ILS-4
python -c "from visualization import PlotManager"
```

### Error: "No data to plot"

```python
# Verifica que los datos no estén vacíos
assert len(fitness_history) > 0, "Historia de fitness vacía"
assert len(results) > 0, "Resultados vacíos"
```

### Gráficas borrosas o de baja calidad

```python
# Aumenta la resolución
plot_convergence_single(history, dpi=300)  # En lugar de 100
```

---

## 📚 Referencias

- **Matplotlib**: https://matplotlib.org/
- **Seaborn**: https://seaborn.pydata.org/
- **NumPy**: https://numpy.org/
- **SciPy**: https://scipy.org/

---

## 📝 Licencia

Parte del proyecto GAA (Generación Automática de Algoritmos).

**Última actualización**: Enero 2025
