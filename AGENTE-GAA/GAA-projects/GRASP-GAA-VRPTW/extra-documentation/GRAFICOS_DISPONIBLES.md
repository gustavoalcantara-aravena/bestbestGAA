# GRÁFICOS Y REPORTES - PIPELINE DE VISUALIZACIONES

**Fecha**: 4 Enero 2026  
**Status**: Sistema completo de visualizaciones listo

---

## Resumen General

Se generarán **3 tipos de reportes** con un total de **12+ gráficos** por cada ejecución:

1. **Visualizaciones estándar** (generate_visualizations.py)
2. **Análisis de GAP** (generate_gap_visualizations.py)  
3. **Reportes HTML** (generate_reports.py)

---

## 1. VISUALIZACIONES ESTÁNDAR (generate_visualizations.py)

### Para Canary Run
**Ubicación**: `output/canary_run/visualizations/canary_visualizations.png`

Contiene 4 subgráficas:
- ✓ **Boxplot Vehículos por Algoritmo** - Distribución y outliers
- ✓ **Boxplot Distancia por Algoritmo** - Variabilidad por algoritmo
- ✓ **Histograma Vehículos** - Distribución de frecuencias (media marcada)
- ✓ **Histograma Distancia** - Distribución de frecuencias (media marcada)

### Para Full Experiment - Por Familia Solomon
**Ubicación**: `output/full_experiment/visualizations/by_family.png`

Contiene 4 subgráficas:
- ✓ **Boxplot Vehículos por Familia** - C1, C2, R1, R2, RC1, RC2
- ✓ **Boxplot Distancia por Familia** - Variabilidad entre familias
- ✓ **Barras Vehículos Promedio** - Comparación de promedios
- ✓ **Barras Distancia Promedio** - Comparación de promedios

### Para Full Experiment - Por Instancia
**Ubicación**: `output/full_experiment/visualizations/by_instance.png`

Contiene 2 subgráficas (primeras 20 instancias):
- ✓ **Barras Vehículos Promedio** - Por instancia individual
- ✓ **Barras Distancia Promedio** - Por instancia individual

### Para Full Experiment - Por Algoritmo
**Ubicación**: `output/full_experiment/visualizations/by_algorithm.png`

Contiene 4 subgráficas:
- ✓ **Boxplot Vehículos por Algoritmo** - 10 algoritmos generados
- ✓ **Boxplot Distancia por Algoritmo** - Variabilidad del rendimiento
- ✓ **Barras Vehículos Promedio** - Ranking de algoritmos
- ✓ **Barras Distancia Promedio** - Cuál algoritmo mejor?

### Resumen Estadístico
**Ubicación**: `output/full_experiment/visualizations/summary_statistics.png`

- Tabla con estadísticas globales (Min, Mean, Max, StDev)
- Desglose por familia Solomon
- Totales por familia

---

## 2. ANÁLISIS DE GAP (generate_gap_visualizations.py)

**Definición GAP**: 
```
%GAP = ((valor_obtenido - valor_baseline) / valor_baseline) * 100
```

Baseline = mejor solución encontrada

### Gap Distribution
**Ubicación**: `output/canary_run/visualizations/gap_distribution.png`

Contiene 3 elementos:
- ✓ **Histograma %GAP Vehículos** - vs baseline
- ✓ **Histograma %GAP Distancia** - vs baseline
- ✓ **Tabla de Estadísticas** - Mean, StDev, Min, Max, Median para ambos

### Gap por Algoritmo
**Ubicación**: `output/*/visualizations/gap_by_algorithm.png`

Contiene 2 subgráficas:
- ✓ **Boxplot %GAP Vehículos** - Por cada uno de 10 algoritmos
- ✓ **Boxplot %GAP Distancia** - Cuál algoritmo más cercano a baseline?

### Gap por Instancia
**Ubicación**: `output/full_experiment/visualizations/gap_by_instance.png`

Contiene 2 subgráficas:
- ✓ **Barras %GAP Vehículos Promedio** - Por instancia
- ✓ **Barras %GAP Distancia Promedio** - Instancias más difíciles?

### Gap Scatter Plot
**Ubicación**: `output/*/visualizations/gap_scatter.png`

- ✓ **2D Scatter: %GAP Vehículos vs %GAP Distancia**
  - Coloreado por algoritmo
  - Baseline marcado con estrella roja
  - Muestra trade-off entre vehículos y distancia

### Gap Cumulative Distribution
**Ubicación**: `output/*/visualizations/gap_cumulative.png`

Contiene 2 subgráficas:
- ✓ **CDF %GAP Vehículos** - Percentil de soluciones
- ✓ **CDF %GAP Distancia** - Cuántas soluciones mejoran baseline?

---

## 3. COMPARACIÓN DE ALGORITMOS (generate_algorithm_comparison.py)

**Ubicación**: `output/*/visualizations/algorithm_*.png`

### Rendimiento Relativo
**Archivo**: `algorithm_performance.png`

Contiene 4 subgráficas:
- ✓ **Heatmap: Algoritmo vs Instancia (Vehículos)**
  - Filas = algoritmos, Columnas = instancias
  - Color indica calidad (verde bueno, rojo malo)
- ✓ **Heatmap: Algoritmo vs Instancia (Distancia)**
- ✓ **Ranking Vehículos** - Top 5 algoritmos
- ✓ **Ranking Distancia** - Cuál es mejor en promedio?

### Convergencia de Algoritmos
**Archivo**: `algorithm_convergence.png`

Contiene 2 subgráficas:
- ✓ **Líneas de convergencia** - Cómo mejora cada algoritmo en promedio?
- ✓ **Tasa de éxito (Feasibility)** - % de soluciones factibles

### Variabilidad de Algoritmos
**Archivo**: `algorithm_variability.png`

- ✓ **Violín plot: Vehículos** - Distribución completa por algoritmo
- ✓ **Violín plot: Distancia** - Variabilidad y asimetría

### Trade-off Vehículos vs Distancia
**Archivo**: `algorithm_tradeoff.png`

- ✓ **Scatter: Vehículos (eje X) vs Distancia (eje Y)**
  - Cada punto = un algoritmo en una instancia
  - Coloreado por algoritmo
  - Muestra frontera de Pareto

---

## 4. REPORTES HTML (generate_reports.py)

### Reporte Canary Run
**Ubicación**: `output/canary_run/report.html`

Contiene:
- ✓ Resumen ejecutivo (totales, tasas de éxito)
- ✓ Estadísticas de vehículos (Min, Max, Mean, StDev)
- ✓ Estadísticas de distancia (Min, Max, Mean, StDev)
- ✓ Mejor solución encontrada
- ✓ Top 10 soluciones
- ✓ Estilo profesional con CSS gradientes

### Reporte Full Experiment
**Ubicación**: `output/full_experiment/report.html`

Contiene:
- ✓ Detalles de todas las instancias
- ✓ Tasas de factibilidad
- ✓ Estadísticas completas
- ✓ Mejor solución global
- ✓ Top 10 soluciones de 560 ejecuciones

---

## RESUMEN VISUAL

```
CANARY RUN (5 algoritmos, 1 instancia C101)
├── visualizations/
│   ├── canary_visualizations.png (4 gráficas)
│   ├── gap_distribution.png
│   ├── gap_by_algorithm.png
│   ├── gap_scatter.png
│   ├── gap_cumulative.png
│   └── algorithm_*.png (5 gráficas adicionales)
└── report.html

FULL EXPERIMENT (10 algoritmos, 56 instancias)
├── visualizations/
│   ├── by_family.png
│   ├── by_instance.png
│   ├── by_algorithm.png
│   ├── summary_statistics.png
│   ├── gap_distribution.png
│   ├── gap_by_algorithm.png
│   ├── gap_by_instance.png
│   ├── gap_scatter.png
│   ├── gap_cumulative.png
│   └── algorithm_*.png (5 gráficas)
└── report.html
```

---

## CÓMO EJECUTAR

### Paso 1: Canary Run
```bash
python canary_run.py
# Output: 5 soluciones en output/canary_run/canary_results.json
```

### Paso 2: Generar Gráficas Canary
```bash
python generate_visualizations.py
python generate_gap_visualizations.py
python generate_algorithm_comparison.py
python generate_reports.py
# Output: 12+ gráficas PNG + 1 HTML
```

### Paso 3: Full Experiment
```bash
python full_experiment.py
# Output: 560 soluciones en output/full_experiment/experiment_results.json
# Tiempo: 1.5-2.5 horas
```

### Paso 4: Generar Gráficas Full
```bash
python generate_visualizations.py
python generate_gap_visualizations.py
python generate_algorithm_comparison.py
python generate_reports.py
# Output: 20+ gráficas PNG + 1 HTML
```

### Todo en uno
```bash
python run_all_visualizations.py
# Ejecuta todos los generadores secuencialmente
```

---

## MÉTRICAS CANÓNICAS

Cada gráfica utiliza métricas estándar para VRPTW:

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| **Vehículos** | Número total de rutas/vehículos | Count(routes) |
| **Distancia** | Distancia total recorrida (km) | Sum(arc distances) |
| **%GAP** | Diferencia % respecto a baseline | ((valor - baseline) / baseline) * 100 |
| **Factibilidad** | Solución cumple restricciones | capacity + time windows |
| **Feasible %** | Porcentaje de soluciones válidas | 100 * (factibles / total) |

---

## CARACTERÍSTICAS ESPECIALES

✓ **Colorimetría consistente** - Mismo algoritmo = mismo color en todas las gráficas  
✓ **Grid y leyendas** - Información clara y legible  
✓ **Escalas automáticas** - Se adaptan al rango de datos  
✓ **Estadísticas embebidas** - Valores mean/stdev directamente en gráficas  
✓ **Reportes HTML profesionales** - CSS con gradientes y tablas interactivas  
✓ **Alta resolución** - 150 DPI para impresión y presentaciones  

---

## PRÓXIMO PASO

Ejecutar: `python full_experiment.py` para generar datos de 560 ejecuciones, luego los 4 generadores de gráficas.

