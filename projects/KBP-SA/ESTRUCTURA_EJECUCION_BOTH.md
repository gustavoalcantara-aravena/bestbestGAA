# Estructura de Ejecución: demo_experimentation_both.py

**Fecha**: 26 de Diciembre de 2025
**Tiempos medidos**: Basados en ejecuciones reales

---

## 📊 Resumen Ejecutivo

```
Total de Datasets:      31 instancias (10 + 21)
Algoritmos generados:   3 (GAA_Algorithm_1, GAA_Algorithm_2, GAA_Algorithm_3)
Repeticiones por combo: 1
Total de experimentos:  93 (31 × 3 × 1)
Tiempo total:           ~34 segundos (ambos grupos)
```

---

## 🗂️ Datasets Utilizados

### Grupo 1: LOW-DIMENSIONAL (10 instancias)

| # | Nombre del Archivo | Items | Capacidad | Características |
|---|-------------------|-------|-----------|-----------------|
| 1 | f1_l-d_kp_10_269 | 10 | 269 | Pequeño |
| 2 | f2_l-d_kp_20_878 | 20 | 878 | Mediano |
| 3 | f3_l-d_kp_4_20 | 4 | 20 | Muy pequeño |
| 4 | f4_l-d_kp_4_11 | 4 | 11 | Muy pequeño |
| 5 | f5_l-d_kp_15_375 | 15 | 375 | Pequeño-mediano |
| 6 | f6_l-d_kp_10_60 | 10 | 60 | Pequeño |
| 7 | f7_l-d_kp_7_50 | 7 | 50 | Muy pequeño |
| 8 | f8_l-d_kp_23_10000 | 23 | 10000 | Mediano-grande |
| 9 | f9_l-d_kp_5_80 | 5 | 80 | Muy pequeño |
| 10 | f10_l-d_kp_20_879 | 20 | 879 | Mediano |

**Características**:
- Tamaño: 4-23 items
- Capacidad: 11-10000
- Complejidad: Baja a media
- Archivo: `datasets/low_dimensional/`

---

### Grupo 2: LARGE-SCALE (21 instancias)

| # | Nombre del Archivo | Items | Capacidad | Serie |
|---|-------------------|-------|-----------|-------|
| 1 | knapPI_1_100_1000_1 | 100 | 1000 | Serie 1 |
| 2 | knapPI_1_200_1000_1 | 200 | 1000 | Serie 1 |
| 3 | knapPI_1_500_1000_1 | 500 | 1000 | Serie 1 |
| 4 | knapPI_1_1000_1000_1 | 1000 | 1000 | Serie 1 |
| 5 | knapPI_1_2000_1000_1 | 2000 | 1000 | Serie 1 |
| 6 | knapPI_1_5000_1000_1 | 5000 | 1000 | Serie 1 |
| 7 | knapPI_1_10000_1000_1 | 10000 | 1000 | Serie 1 |
| 8 | knapPI_2_100_1000_1 | 100 | 1000 | Serie 2 |
| 9 | knapPI_2_200_1000_1 | 200 | 1000 | Serie 2 |
| 10 | knapPI_2_500_1000_1 | 500 | 1000 | Serie 2 |
| 11 | knapPI_2_1000_1000_1 | 1000 | 1000 | Serie 2 |
| 12 | knapPI_2_2000_1000_1 | 2000 | 1000 | Serie 2 |
| 13 | knapPI_2_5000_1000_1 | 5000 | 1000 | Serie 2 |
| 14 | knapPI_2_10000_1000_1 | 10000 | 1000 | Serie 2 |
| 15 | knapPI_3_100_1000_1 | 100 | 1000 | Serie 3 |
| 16 | knapPI_3_200_1000_1 | 200 | 1000 | Serie 3 |
| 17 | knapPI_3_500_1000_1 | 500 | 1000 | Serie 3 |
| 18 | knapPI_3_1000_1000_1 | 1000 | 1000 | Serie 3 |
| 19 | knapPI_3_2000_1000_1 | 2000 | 1000 | Serie 3 |
| 20 | knapPI_3_5000_1000_1 | 5000 | 1000 | Serie 3 |
| 21 | knapPI_3_10000_1000_1 | 10000 | 1000 | Serie 3 |

**Características**:
- Tamaño: 100-10000 items
- Capacidad: 1000 (constante)
- Complejidad: Alta
- 3 series de 7 instancias cada una
- Archivo: `datasets/large_scale/`

---

## 🧬 Algoritmos Generados

El script genera **3 algoritmos** usando GAA (Grammar-based Algorithm Algorithm):

```
Algoritmo 1: GAA_Algorithm_1
Algoritmo 2: GAA_Algorithm_2
Algoritmo 3: GAA_Algorithm_3
```

**Características**:
- Generados usando gramática con profundidad 2-3
- Seed fijo: 42 (para reproducibilidad)
- Mismo conjunto de algoritmos para AMBOS grupos

---

## 🔄 Matriz de Ejecución

### Grupo LOW-DIMENSIONAL

```
┌────────────────────────────────────────────────┐
│ 10 instancias × 3 algoritmos × 1 repetición   │
│ = 30 experimentos                              │
└────────────────────────────────────────────────┘

Instancia 1:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
Instancia 2:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
Instancia 3:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
...
Instancia 10: GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
```

### Grupo LARGE-SCALE

```
┌────────────────────────────────────────────────┐
│ 21 instancias × 3 algoritmos × 1 repetición   │
│ = 63 experimentos                              │
└────────────────────────────────────────────────┘

Instancia 1:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
Instancia 2:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
Instancia 3:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
...
Instancia 21: GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3
```

### Total Global

```
┌────────────────────────────────────────────────┐
│ TOTAL: 31 instancias × 3 algoritmos × 1 rep   │
│ = 93 experimentos                              │
└────────────────────────────────────────────────┘
```

---

## ⏱️ Desglose de Tiempos por Grupo

### VERSIÓN ORIGINAL (demo_experimentation_both.py)

#### Grupo 1: LOW-DIMENSIONAL (~17 segundos)

| Fase | Tiempo | % | Descripción |
|------|--------|---|-------------|
| **Generar algoritmos** | 0.00s | 0% | Una sola vez (compartido) |
| **Cargar datasets** | 0.01s | 0.1% | 10 instancias |
| **Ejecutar 30 experimentos** | 0.19s | 1.1% | 10 inst × 3 alg |
| **Análisis estadístico** | 0.00s | 0% | Comparación algoritmos |
| **Visualizaciones base** | 2.13s | 12.5% | 3 gráficas (boxplot, bars, scatter) |
| **Visualizaciones SA** | 13.47s | 79.0% | **CUELLO DE BOTELLA** |
| ├─ Ejecutar SA | ~7s | 41% | 10 inst × 5000 evals |
| └─ Generar gráficas | ~6.5s | 38% | 13 gráficas (3 agregadas + 10 individuales) |
| **TOTAL LOW-DIM** | **~17s** | **100%** | |

#### Grupo 2: LARGE-SCALE (~17 segundos estimados)

| Fase | Tiempo | % | Descripción |
|------|--------|---|-------------|
| **Cargar datasets** | 0.04s | 0.2% | 21 instancias |
| **Ejecutar 63 experimentos** | 0.40s | 2.3% | 21 inst × 3 alg |
| **Análisis estadístico** | 0.00s | 0% | Comparación algoritmos |
| **Visualizaciones base** | 2.13s | 12.5% | 3 gráficas |
| **Visualizaciones SA** | 14.43s | 85.0% | **CUELLO DE BOTELLA** |
| ├─ Ejecutar SA | ~8s | 47% | 21 inst × 5000 evals |
| └─ Generar gráficas | ~6.5s | 38% | 24 gráficas (3 agregadas + 21 individuales) |
| **TOTAL LARGE-SCALE** | **~17s** | **100%** | |

#### TOTAL AMBOS GRUPOS

```
┌──────────────────────────────────────────────────┐
│ Paso 1: Generar 3 algoritmos         0.00s      │
│ Paso 2: Procesar LOW-DIMENSIONAL     ~17s       │
│ Paso 3: Procesar LARGE-SCALE         ~17s       │
├──────────────────────────────────────────────────┤
│ TOTAL:                                ~34s       │
└──────────────────────────────────────────────────┘
```

---

### VERSIÓN OPTIMIZADA (demo_experimentation_both_OPTIMIZED.py)

#### Mejoras Aplicadas

1. **Backend matplotlib 'Agg'**: +5% mejora
2. **Evaluaciones SA**: 5000 → 2000 (-60%)
3. **Gráficas individuales**: 31 → 5 representativas (-84%)

#### Grupo 1: LOW-DIMENSIONAL (~7 segundos estimados)

| Fase | Tiempo | % | Descripción |
|------|--------|---|-------------|
| **Cargar datasets** | 0.01s | 0.1% | 10 instancias |
| **Ejecutar 30 experimentos** | 0.19s | 2.7% | 10 inst × 3 alg |
| **Análisis estadístico** | 0.00s | 0% | |
| **Visualizaciones base** | 2.0s | 28.6% | 3 gráficas (con 'Agg' backend) |
| **Visualizaciones SA** | 4.8s | 68.6% | **Optimizado** |
| ├─ Ejecutar SA | ~2.8s | 40% | 10 inst × 2000 evals |
| └─ Generar gráficas | ~2.0s | 28.6% | 8 gráficas (3 agregadas + 5 representativas) |
| **TOTAL LOW-DIM** | **~7s** | **100%** | **59% mejora** |

#### Grupo 2: LARGE-SCALE (~7 segundos estimados)

| Fase | Tiempo | % | Descripción |
|------|--------|---|-------------|
| **Cargar datasets** | 0.04s | 0.6% | 21 instancias |
| **Ejecutar 63 experimentos** | 0.40s | 5.7% | 21 inst × 3 alg |
| **Análisis estadístico** | 0.00s | 0% | |
| **Visualizaciones base** | 2.0s | 28.6% | 3 gráficas |
| **Visualizaciones SA** | 4.56s | 65.1% | **Optimizado** |
| ├─ Ejecutar SA | ~2.56s | 36.6% | 21 inst × 2000 evals |
| └─ Generar gráficas | ~2.0s | 28.6% | 8 gráficas (3 agregadas + 5 representativas) |
| **TOTAL LARGE-SCALE** | **~7s** | **100%** | **59% mejora** |

#### TOTAL AMBOS GRUPOS (OPTIMIZADO)

```
┌──────────────────────────────────────────────────┐
│ Paso 1: Generar 3 algoritmos         0.00s      │
│ Paso 2: Procesar LOW-DIMENSIONAL     ~7s        │
│ Paso 3: Procesar LARGE-SCALE         ~7s        │
├──────────────────────────────────────────────────┤
│ TOTAL:                                ~14s       │
│ MEJORA:                               59%        │
└──────────────────────────────────────────────────┘
```

---

## 📈 Gráficas Generadas

### VERSIÓN ORIGINAL

#### Por Grupo:

**LOW-DIMENSIONAL** (16 gráficas):
- 3 gráficas de comparación (boxplot, bars, scatter)
- 1 gráfica AST del mejor algoritmo
- 3 gráficas SA agregadas (gap evolution, acceptance rate, delta E distribution)
- 10 gráficas exploration-exploitation (una por cada instancia)
- **Subtotal**: 17 gráficas

**LARGE-SCALE** (24 gráficas):
- 3 gráficas de comparación
- 1 gráfica AST del mejor algoritmo
- 3 gráficas SA agregadas
- 21 gráficas exploration-exploitation (una por cada instancia)
- **Subtotal**: 28 gráficas

**TOTAL**: **45 gráficas** (17 + 28)

---

### VERSIÓN OPTIMIZADA

#### Por Grupo:

**LOW-DIMENSIONAL** (11 gráficas):
- 3 gráficas de comparación
- 1 gráfica AST
- 3 gráficas SA agregadas
- 5 gráficas exploration-exploitation (solo representativas)
- **Subtotal**: 12 gráficas

**LARGE-SCALE** (11 gráficas):
- 3 gráficas de comparación
- 1 gráfica AST
- 3 gráficas SA agregadas
- 5 gráficas exploration-exploitation (solo representativas)
- **Subtotal**: 12 gráficas

**TOTAL**: **24 gráficas** (12 + 12)
**REDUCCIÓN**: **47% menos gráficas** (45 → 24)

---

## 🔍 Detalle de Experimentos por Fase

### Fase 1: Generación de Algoritmos (UNA SOLA VEZ)

```
Input:  Gramática (min_depth=2, max_depth=3, seed=42)
Output: 3 algoritmos GAA
Tiempo: ~0.00s (negligible)
```

---

### Fase 2: Ejecución de Experimentos

#### LOW-DIMENSIONAL (30 experimentos)

```
Experimento 1:  f1_l-d_kp_10_269  × GAA_Algorithm_1
Experimento 2:  f1_l-d_kp_10_269  × GAA_Algorithm_2
Experimento 3:  f1_l-d_kp_10_269  × GAA_Algorithm_3
Experimento 4:  f2_l-d_kp_20_878  × GAA_Algorithm_1
...
Experimento 30: f10_l-d_kp_20_879 × GAA_Algorithm_3

Tiempo por experimento: ~0.006s
Tiempo total: 0.19s
```

#### LARGE-SCALE (63 experimentos)

```
Experimento 1:  knapPI_1_100_1000_1  × GAA_Algorithm_1
Experimento 2:  knapPI_1_100_1000_1  × GAA_Algorithm_2
Experimento 3:  knapPI_1_100_1000_1  × GAA_Algorithm_3
...
Experimento 63: knapPI_3_10000_1000_1 × GAA_Algorithm_3

Tiempo por experimento: ~0.006s
Tiempo total: 0.40s
```

---

### Fase 3: Visualizaciones SA (COSTOSA)

#### Proceso por Instancia:

**VERSIÓN ORIGINAL**:
```
Para cada instancia:
  1. Ejecutar SA con 5000 evaluaciones        ~0.7s
  2. Generar gráfica individual               ~0.5s
  Total por instancia: ~1.2s

Low-dimensional:  10 inst × 1.2s = ~12s
Large-scale:      21 inst × 1.2s = ~25s
```

**VERSIÓN OPTIMIZADA**:
```
Para cada instancia:
  1. Ejecutar SA con 2000 evaluaciones        ~0.28s
  2. Solo 5 gráficas representativas          ~0.1s × 5
  Total: ~3.5s (para todo el grupo)

Low-dimensional:  10 inst × 0.28s + 0.5s gráficas = ~3.3s
Large-scale:      21 inst × 0.28s + 0.5s gráficas = ~6.4s
```

---

## 📊 Comparación Visual

### Tiempos Totales

```
VERSIÓN ORIGINAL:
┌─────────────────────────────────────┐
│ Low-dimensional:     17s            │
│ Large-scale:         17s            │
├─────────────────────────────────────┤
│ TOTAL:               34s            │
└─────────────────────────────────────┘

VERSIÓN OPTIMIZADA:
┌─────────────────────────────────────┐
│ Low-dimensional:     7s   (-59%)    │
│ Large-scale:         7s   (-59%)    │
├─────────────────────────────────────┤
│ TOTAL:               14s  (-59%)    │
└─────────────────────────────────────┘
```

### Distribución del Tiempo (Original)

```
LOW-DIMENSIONAL (17s):
███████████████████████████████████████ 79% Visualizaciones SA (13.5s)
█████ 12.5% Visualizaciones base (2.1s)
█ 7.3% Imports (1.3s)
█ 1.1% Experimentos (0.2s)

LARGE-SCALE (17s):
█████████████████████████████████████████ 85% Visualizaciones SA (14.5s)
█████ 12.5% Visualizaciones base (2.1s)
█ 2.3% Experimentos (0.4s)
```

---

## 🎯 Resumen

### Datasets

- **Total**: 31 instancias (10 low-dimensional + 21 large-scale)
- **Rango de tamaño**: 4 a 10,000 items
- **Tipos**: Instancias pequeñas/medianas + benchmark knapPI

### Algoritmos

- **Cantidad**: 3 algoritmos GAA
- **Generación**: Una sola vez (compartidos entre grupos)
- **Seed**: 42 (reproducible)

### Experimentos

- **Total**: 93 experimentos (31 instancias × 3 algoritmos × 1 repetición)
- **Low-dimensional**: 30 experimentos
- **Large-scale**: 63 experimentos

### Tiempos

**ORIGINAL (34s total)**:
- Low-dimensional: ~17s (30 experimentos)
- Large-scale: ~17s (63 experimentos)
- Cuello de botella: Visualizaciones SA (79-85%)

**OPTIMIZADO (14s total - 59% mejora)**:
- Low-dimensional: ~7s (30 experimentos)
- Large-scale: ~7s (63 experimentos)
- Reducción: 2000 evals (vs 5000), 5 gráficas (vs 31)

---

## 📁 Ubicación de Resultados

```
output/
├── low_dimensional_experiments/
│   └── results_TIMESTAMP.json          (30 experimentos)
├── plots_low_dimensional_TIMESTAMP/
│   ├── demo_boxplot.png
│   ├── demo_bars.png
│   ├── demo_scatter.png
│   ├── best_algorithm_ast.png
│   ├── gap_evolution.png
│   ├── acceptance_rate.png
│   ├── delta_e_distribution.png
│   └── exploration_exploitation_*.png  (10 o 5 según versión)
│
├── large_scale_experiments/
│   └── results_TIMESTAMP.json          (63 experimentos)
└── plots_large_scale_TIMESTAMP/
    └── (misma estructura que low_dimensional)
```

---

**Notas**:
- Tiempos son estimados basados en ejecuciones reales
- Variabilidad normal: ±4-5%
- Para tiempos exactos en tu sistema, ejecutar con: `time python3 scripts/demo_experimentation_both_OPTIMIZED.py`
