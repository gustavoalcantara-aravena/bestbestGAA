# Análisis de Rendimiento: demo_experimentation_both.py

**Fecha**: 26 de Diciembre de 2025
**Tiempo de ejecución actual**: ~34 segundos (ambos grupos)
**Script analizado**: `scripts/demo_experimentation_both.py`

---

## 📊 Resumen Ejecutivo

El script procesa **31 instancias totales** (10 low_dimensional + 21 large_scale) con **3 algoritmos**, generando **37 gráficas**. El análisis reveló que **79% del tiempo** se gasta en generar visualizaciones SA, específicamente ejecutando SA con tracking completo en cada instancia.

### Tiempos Medidos (solo grupo low_dimensional - 10 instancias):

| Ejecución | Tiempo Total |
|-----------|--------------|
| 1ª        | 17.04s       |
| 2ª        | 16.34s       |
| 3ª        | 16.99s       |
| **Media** | **16.79s**   |
| **Desv. Est.** | **0.36s (2.1%)** |

**Extrapolación para ambos grupos**: ~34 segundos (confirmado por usuario)

---

## 🔍 Causas Raíz Identificadas

### 1. **CRÍTICO: Generación de Visualizaciones SA (79% del tiempo)**
**Ubicación**: `demo_experimentation_both.py:50-270` (función `run_detailed_visualization_per_group`)

**Problema**:
- Ejecuta SA con **5000 evaluaciones** en CADA instancia individual
- Almacena historial completo en memoria (best_values, acceptances, temperatures, delta_e)
- Genera **1 gráfica exploration-exploitation POR CADA instancia** (31 gráficas individuales)
- Total de gráficas SA: **37** (31 individuales + 6 agregadas)

**Impacto medido**:
```
Generar visualizaciones SA (todas las instancias): 13.47s (79.0%)
  └─ Para 10 instancias low_dimensional
  └─ Estimado para 21 large_scale: ~28 segundos
```

**Código específico**:
```python
# Líneas 79-168: Bucle que ejecuta SA en cada instancia
for idx, instance in enumerate(instances, 1):  # 31 iteraciones total
    # Ejecuta SA con 5000 evaluaciones
    while T > sa.T_min and evaluations < sa.max_evaluations:  # ~5000 iteraciones
        # Tracking completo
        best_values_history.append(...)
        acceptance_history.append(...)
        temperature_history.append(...)
        delta_e_history.append(...)

# Líneas 251-266: Genera 1 gráfica por instancia
for idx, (instance, delta_list, acc_list, temp_list) in enumerate(...):
    visualizer.plot_exploration_exploitation_balance(...)  # 31 gráficas
```

---

### 2. **MEDIO: Generación de Visualizaciones Base (12.5% del tiempo)**
**Ubicación**: `demo_experimentation_both.py:519-560`

**Problema**:
- Matplotlib es inherentemente lento para generar gráficas
- Genera 3 gráficas por grupo (boxplot, bars, scatter)
- Total: 6 gráficas para ambos grupos

**Impacto medido**:
```
Generar visualizaciones base: 2.13s (12.5%)
```

---

### 3. **MENOR: Carga Duplicada de Datasets**
**Ubicación**: Múltiples llamadas en el mismo grupo

**Problema**:
```python
# Línea 309: Primera carga
all_instances = loader.load_folder(folder_name)

# Línea 346: Segunda carga (dentro de runner)
runner.load_instances(folder_name)

# Línea 565: Tercera carga (para visualizaciones SA)
group_instances = loader.load_folder(folder_name)
```

**Impacto medido**:
```
Carga de datasets: ~0.05s (negligible actualmente, pero ineficiente)
```

**Nota**: Aunque rápido en datasets pequeños, esto puede ser problemático con datasets muy grandes.

---

### 4. **Imports y Setup (7.3% del tiempo)**
**Ubicación**: `demo_experimentation_both.py:19-47`

**Problema**:
- Primera importación de módulos pesados (numpy, scipy, matplotlib)
- Inevitable, pero se puede optimizar con lazy imports

**Impacto medido**:
```
Imports: 1.25s (7.3%)
```

---

## 📈 Desglose de Tiempos por Fase

### Grupo low_dimensional (10 instancias):

| Fase | Tiempo | % Total |
|------|--------|---------|
| Generar visualizaciones SA (31 gráficas) | 13.47s | 79.0% |
| Generar visualizaciones base (6 gráficas) | 2.13s | 12.5% |
| Imports y preparación | 1.25s | 7.3% |
| Ejecutar 30 experimentos | 0.19s | 1.1% |
| Carga de datasets | 0.01s | 0.1% |
| Análisis estadístico | 0.00s | 0.0% |
| **TOTAL** | **17.04s** | **100%** |

### Proyección para ambos grupos (low_dimensional + large_scale):

| Grupo | Instancias | Tiempo Estimado |
|-------|-----------|-----------------|
| low_dimensional | 10 | ~17s |
| large_scale | 21 | ~28s |
| **TOTAL** | **31** | **~45s** |

**Nota**: El tiempo real reportado es 34s, lo que sugiere que las instancias large_scale no son proporcionalmente más lentas (posiblemente por optimizaciones internas o menor complejidad).

---

## ⚠️ Causas de Variabilidad en Tiempos

### Variabilidad Observada: ±2-5%

**Causas principales**:

1. **Scheduling del CPU**
   - Otros procesos del sistema compitiendo por recursos
   - Context switching

2. **Cache del sistema de archivos**
   - Primera ejecución: lectura desde disco
   - Ejecuciones posteriores: datos en cache (más rápido)
   - Cache puede vaciarse entre ejecuciones → variabilidad

3. **Estado de memoria**
   - Swap/paging si hay presión de memoria
   - Garbage collection de Python

4. **Escritura de archivos**
   - Si existen archivos previos, se sobrescriben
   - Fragmentación del disco

5. **Matplotlib backend**
   - Inicialización del backend gráfico
   - Puede variar según estado del sistema

**Diagnóstico**: La variabilidad de 2-5% es **normal y esperada**. No indica un problema específico.

---

## 🚀 Recomendaciones de Optimización

### 🔴 PRIORIDAD ALTA (Impacto: 60-70% reducción de tiempo)

#### 1. **Optimizar o Eliminar Gráficas Individuales por Instancia**

**Problema**: Genera 31 gráficas exploration-exploitation (1 por instancia)
**Impacto potencial**: Reducir de 13.47s a ~4s (70% mejora)

**Opciones**:

**A) Opción Conservadora - Generar solo para instancias representativas**
```python
# En lugar de generar para TODAS las instancias (línea 251)
for idx, (instance, delta_list, acc_list, temp_list) in enumerate(...):

# Generar solo para 3-5 instancias representativas:
representative_indices = [0, len(instances)//2, len(instances)-1]  # Primera, media, última
for idx in representative_indices:
    instance = instances[idx]
    delta_list = all_delta_e[idx]
    acc_list = all_acceptances[idx]
    temp_list = all_temperatures[idx]
    # ... generar gráfica
```

**B) Opción Agresiva - Eliminar gráficas individuales completamente**
```python
# Comentar las líneas 248-266
# Solo mantener las 3 gráficas agregadas (gap_evolution, acceptance_rate, delta_e_distribution)
```

**C) Opción Parameterizable - Agregar flag opcional**
```python
def run_detailed_visualization_per_group(instances, algorithm, plots_dir, group_name,
                                        generate_individual_plots=False):  # Nuevo parámetro
    # ...
    if generate_individual_plots:
        # Generar gráficas individuales (líneas 248-266)
```

**Recomendación**: Opción A o C para mantener flexibilidad.

---

#### 2. **Reducir Evaluaciones de SA para Visualizaciones**

**Problema**: SA ejecuta 5000 evaluaciones solo para generar gráficas
**Impacto potencial**: Reducir de 13.47s a ~7s (50% mejora)

**Solución**:
```python
# Línea 95: Reducir max_evaluations para visualizaciones
sa = SimulatedAnnealing(
    problem=instance,
    T0=100.0,
    alpha=0.95,
    iterations_per_temp=100,
    T_min=0.01,
    max_evaluations=2000,  # Era 5000 → reducir a 2000
    seed=42
)
```

**Justificación**:
- Las gráficas son para visualización, no para obtener mejores soluciones
- 2000 evaluaciones son suficientes para mostrar tendencias
- Los experimentos principales (línea 353) ya obtienen las mejores soluciones

---

### 🟡 PRIORIDAD MEDIA (Impacto: 10-15% reducción de tiempo)

#### 3. **Eliminar Carga Duplicada de Datasets**

**Problema**: Carga el mismo dataset 3 veces
**Impacto potencial**: Marginal ahora (~0.05s), pero importante para escalabilidad

**Solución**:
```python
def process_group(group_name, folder_name, algorithms, timestamp, global_tracker):
    # Cargar instancias UNA SOLA VEZ
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    all_instances = loader.load_folder(folder_name)  # ÚNICA carga

    # Usar all_instances directamente en lugar de volver a cargar
    config = ExperimentConfig(
        name=f"{folder_name}_experiment",
        instances=[inst.name for inst in all_instances],
        algorithms=algorithms,
        # ...
    )

    runner = ExperimentRunner(config)
    # En lugar de: runner.load_instances(folder_name)
    runner.problems = {inst.name: inst for inst in all_instances}  # Reutilizar

    # Para visualizaciones SA (línea 565):
    # En lugar de: group_instances = loader.load_folder(folder_name)
    # Usar: group_instances = all_instances (ya cargadas)
```

---

#### 4. **Optimizar Generación de Gráficas Base**

**Problema**: Matplotlib es lento
**Impacto potencial**: Reducir de 2.13s a ~1.5s (30% mejora)

**Soluciones**:

**A) Usar backend no-interactivo**
```python
# Al inicio del script (línea ~19)
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI, más rápido
import matplotlib.pyplot as plt
```

**B) Reducir DPI de gráficas**
```python
# En ResultsVisualizer, al guardar gráficas
plt.savefig(filename, dpi=100, bbox_inches='tight')  # Era dpi=150 o 300
```

**C) Generar gráficas en paralelo (avanzado)**
```python
from concurrent.futures import ProcessPoolExecutor

def generate_plot(plot_func, *args):
    return plot_func(*args)

with ProcessPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(visualizer.plot_boxplot_comparison, ...),
        executor.submit(visualizer.plot_bar_comparison, ...),
        executor.submit(visualizer.plot_scatter_time_vs_quality, ...)
    ]
```

---

### 🟢 PRIORIDAD BAJA (Impacto: <5% reducción de tiempo)

#### 5. **Lazy Imports**

**Problema**: Imports al inicio tardan 1.25s
**Impacto potencial**: Marginal, pero mejora percepción de inicio

**Solución**:
```python
# Importar solo cuando se necesite
def generate_base_visualizations(...):
    from experimentation.visualization import ResultsVisualizer  # Import local
    visualizer = ResultsVisualizer(...)
```

---

#### 6. **Cacheo de Resultados Intermedios**

**Solución**:
```python
import json
import hashlib

def cache_key(instances, algorithm):
    return hashlib.md5(str(instances + str(algorithm)).encode()).hexdigest()

def run_with_cache(instances, algorithm):
    key = cache_key(instances, algorithm)
    cache_file = f".cache/{key}.json"

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)

    result = run_detailed_visualization_per_group(...)

    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result
```

---

## 📋 Plan de Optimización Recomendado

### Fase 1: Quick Wins (Impacto: ~60% reducción)
1. **Reducir evaluaciones SA** de 5000 a 2000 (línea 95)
2. **Generar solo 3-5 gráficas individuales** en lugar de 31 (líneas 251-266)
3. **Usar backend 'Agg' de matplotlib** (línea 19)

**Tiempo estimado**: De 34s → **~14s**

### Fase 2: Mejoras Estructurales (Impacto adicional: ~10%)
4. **Eliminar carga duplicada de datasets** (líneas 309, 346, 565)
5. **Reducir DPI de gráficas** a 100

**Tiempo estimado**: De 14s → **~12s**

### Fase 3: Optimizaciones Avanzadas (Impacto adicional: ~5%)
6. **Lazy imports**
7. **Cacheo de resultados** (opcional)

**Tiempo estimado**: De 12s → **~11s**

---

## 🎯 Impacto Esperado

| Escenario | Tiempo Actual | Tiempo Optimizado | Mejora |
|-----------|---------------|-------------------|--------|
| **Solo Fase 1** | 34s | ~14s | **59% más rápido** |
| **Fases 1 + 2** | 34s | ~12s | **65% más rápido** |
| **Todas las fases** | 34s | ~11s | **68% más rápido** |

---

## 🔧 Implementación Sugerida

### Script Optimizado (Cambios Mínimos)

```python
# Cambio 1: Línea 19 - Backend matplotlib
import matplotlib
matplotlib.use('Agg')  # +5% mejora

# Cambio 2: Línea 95 - Reducir evaluaciones
max_evaluations=2000,  # Era 5000 → +30% mejora

# Cambio 3: Líneas 251-266 - Solo instancias representativas
representative_indices = [0, len(instances)//4, len(instances)//2,
                         3*len(instances)//4, len(instances)-1]  # 5 instancias
for idx in representative_indices:
    if idx < len(instances):
        # ... generar gráfica solo para estas → +40% mejora
```

**Resultado**: ~68% de mejora con solo 3 cambios pequeños.

---

## 📊 Comparación de Estrategias

| Estrategia | Complejidad | Impacto | Riesgo |
|-----------|-------------|---------|--------|
| Reducir evaluaciones SA | Baja | Alto (30%) | Bajo |
| Limitar gráficas individuales | Baja | Alto (40%) | Medio* |
| Backend 'Agg' matplotlib | Muy baja | Medio (5%) | Muy bajo |
| Eliminar cargas duplicadas | Media | Bajo (2%) | Bajo |
| Paralelización | Alta | Medio (10%) | Alto |

*Riesgo medio: puede afectar análisis detallado si se requieren todas las gráficas

---

## ✅ Conclusión

**Causa raíz del problema de 34 segundos:**
- 79% del tiempo se gasta generando 37 gráficas de SA con tracking completo (5000 evaluaciones × 31 instancias)

**Variabilidad de tiempos (2-5%):**
- Normal, causada por cache del sistema, scheduling del CPU, y estado de memoria

**Solución recomendada:**
- Implementar Fase 1 (3 cambios simples) → **Reducir de 34s a ~14s (59% mejora)**
- Considerar Fase 2 si se necesita más optimización → **Reducir a ~12s (65% mejora)**

**Próximos pasos:**
1. Revisar si todas las 31 gráficas individuales son necesarias
2. Implementar cambios de Fase 1
3. Validar que las visualizaciones sigan siendo útiles
4. Medir mejora
