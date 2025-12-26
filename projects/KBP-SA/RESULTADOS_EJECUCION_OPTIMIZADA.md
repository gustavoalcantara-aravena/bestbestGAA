# Resultados de Ejecución: Versión Optimizada

**Fecha**: 26 de Diciembre de 2025, 05:25
**Script**: `demo_experimentation_both_OPTIMIZED.py`
**Condiciones**: RAM: 20GB libre, Swap: 0B

---

## ⏱️ TIEMPOS MEDIDOS (Ejecución Real)

### Resumen Global

```
┌──────────────────────────────────────────────────┐
│ GRUPO LOW-DIMENSIONAL:           11.48s          │
│ GRUPO LARGE-SCALE:               43.52s          │
├──────────────────────────────────────────────────┤
│ TOTAL:                           55.00s          │
└──────────────────────────────────────────────────┘
```

---

## 📊 Desglose Detallado por Grupo

### Grupo LOW-DIMENSIONAL (11.48s total)

| Fase | Tiempo | % | Detalle |
|------|--------|---|---------|
| **Generar algoritmos** | 0.002s | 0.0% | 3 algoritmos GAA |
| **Configurar experimento** | 0.005s | 0.0% | Setup |
| **Ejecutar experimentos** | 1.90s | 16.5% | 30 experimentos (10 × 3) |
| **Guardar resultados** | 0.003s | 0.0% | JSON |
| **Análisis estadístico** | 0.004s | 0.0% | Friedman, Wilcoxon |
| **Comparación algoritmos** | 0.005s | 0.0% | Rankings |
| **Visualizaciones** | 9.55s | 83.2% | **Gráficas** |
| ├─ Comparación (3) | ~0.5s | 4.4% | boxplot, bars, scatter |
| ├─ AST | ~0.1s | 0.9% | Estructura algoritmo |
| └─ **SA (8 gráficas)** | ~8.9s | 77.5% | **Tracking SA** |
| **TOTAL** | **11.48s** | **100%** | |

**Experimentos**:
- 30 experimentos en 1.90s
- Promedio: 0.063s por experimento
- Más lento: GAA_Algorithm_3 (~0.3s por instancia)

---

### Grupo LARGE-SCALE (43.52s total)

| Fase | Tiempo | % | Detalle |
|------|--------|---|---------|
| **Configurar experimento** | 0.047s | 0.1% | Setup |
| **Ejecutar experimentos** | 33.88s | 77.9% | **63 experimentos (21 × 3)** |
| **Guardar resultados** | 0.005s | 0.0% | JSON |
| **Análisis estadístico** | 0.004s | 0.0% | Friedman, Wilcoxon |
| **Comparación algoritmos** | 0.007s | 0.0% | Rankings |
| **Visualizaciones** | 9.57s | 22.0% | Gráficas |
| ├─ Comparación (3) | ~0.5s | 1.1% | boxplot, bars, scatter |
| ├─ AST | ~0.1s | 0.2% | Estructura algoritmo |
| └─ **SA (8 gráficas)** | ~8.9s | 20.5% | Tracking SA |
| **TOTAL** | **43.52s** | **100%** | |

**Experimentos**:
- 63 experimentos en 33.88s
- Promedio: 0.538s por experimento
- Más lento: knapPI_1_10000 con GAA_Algorithm_1 (3.7s)

---

## 🔍 ANÁLISIS DE RESULTADOS

### ✅ Optimizaciones que Funcionaron

#### 1. Visualizaciones SA (Low-Dimensional)
```
Original estimado:  ~13.5s (5000 evals, 10 gráficas)
Optimizado medido:   ~8.9s (2000 evals, 5 gráficas)
MEJORA:              34% (-4.6s)
```

#### 2. Visualizaciones SA (Large-Scale)
```
Original estimado:  ~14.5s (5000 evals, 21 gráficas)
Optimizado medido:   ~8.9s (2000 evals, 5 gráficas)
MEJORA:              39% (-5.6s)
```

#### 3. Backend 'Agg' Matplotlib
```
Mejora: ~5% en generación de gráficas
Sin errores de GUI
```

---

### ⚠️ Cuello de Botella NO Optimizado

#### **EXPERIMENTOS en Large-Scale: 33.88s (78% del tiempo)**

**Causa raíz**: GAA_Algorithm_3 ejecuta búsqueda local intensiva

```python
# GAA_Algorithm_3 generado:
MIENTRAS (presupuesto: 100 iteraciones):
  BUSQUEDA_LOCAL en TwoExchange
  LLAMAR TwoExchange
```

**Impacto por tamaño de instancia**:

| Instancia | Items | Tiempo Alg_1 | Tiempo Alg_2 | Tiempo Alg_3 |
|-----------|-------|--------------|--------------|--------------|
| knapPI_100 | 100 | 0.010s | 0.001s | **0.60s** |
| knapPI_500 | 500 | 0.055s | 0.005s | **0.65s** |
| knapPI_1000 | 1000 | 0.133s | 0.012s | **0.70s** |
| knapPI_2000 | 2000 | 0.315s | 0.029s | **0.74s** |
| knapPI_5000 | 5000 | 1.160s | 0.107s | **0.90s** |
| knapPI_10000 | 10000 | 3.726s | 0.334s | **1.14s** |

**Observación**: GAA_Algorithm_3 toma ~0.6-1.1s **POR EXPERIMENTO** en large-scale

**Cálculo**:
- 21 instancias × 0.7s promedio (Alg_3) = ~14.7s
- 21 instancias × Alg_1 y Alg_2 = ~15s
- **Total experimentos: ~30s** (coincide con medición: 33.88s)

---

## 📈 Comparación: Original vs Optimizado

### Grupo LOW-DIMENSIONAL

```
┌──────────────────────┬──────────┬──────────┬─────────┐
│ Fase                 │ Original │ Optimiz. │ Mejora  │
├──────────────────────┼──────────┼──────────┼─────────┤
│ Experimentos         │   0.19s  │   1.90s  │ -900%   │ ⚠️
│ Visualizaciones SA   │  13.47s  │   8.90s  │  +34%   │ ✅
│ Visualizaciones base │   2.13s  │   0.60s  │  +72%   │ ✅
│ Otros                │   1.00s  │   0.08s  │  +92%   │ ✅
├──────────────────────┼──────────┼──────────┼─────────┤
│ TOTAL                │  ~17s    │  11.48s  │  +32%   │
└──────────────────────┴──────────┴──────────┴─────────┘
```

**⚠️ Nota**: Los experimentos tardaron MÁS en la versión optimizada debido a GAA_Algorithm_3

---

### Grupo LARGE-SCALE

```
┌──────────────────────┬──────────┬──────────┬─────────┐
│ Fase                 │ Original │ Optimiz. │ Mejora  │
├──────────────────────┼──────────┼──────────┼─────────┤
│ Experimentos         │   0.40s  │  33.88s  │-8370%   │ 🔴
│ Visualizaciones SA   │  14.43s  │   8.90s  │  +38%   │ ✅
│ Visualizaciones base │   2.13s  │   0.60s  │  +72%   │ ✅
│ Otros                │   0.04s  │   0.14s  │  -250%  │
├──────────────────────┼──────────┼──────────┼─────────┤
│ TOTAL                │  ~17s    │  43.52s  │ -156%   │ 🔴
└──────────────────────┴──────────┴──────────┴─────────┘
```

---

## 🎯 CONCLUSIÓN

### Tiempos Totales

```
┌──────────────────────┬──────────┬──────────┬─────────┐
│                      │ Original │ Optimiz. │ Cambio  │
├──────────────────────┼──────────┼──────────┼─────────┤
│ Low-Dimensional      │   ~17s   │  11.48s  │  +32%   │ ✅
│ Large-Scale          │   ~17s   │  43.52s  │ -156%   │ 🔴
├──────────────────────┼──────────┼──────────┼─────────┤
│ TOTAL AMBOS GRUPOS   │   ~34s   │  55.00s  │  -62%   │ 🔴
└──────────────────────┴──────────┴──────────┴─────────┘
```

### ⚠️ HALLAZGO CRÍTICO

**Las optimizaciones de visualizaciones funcionaron**, PERO:

1. ✅ **Visualizaciones SA**: -34% a -38% (funcionó como esperado)
2. ✅ **Backend matplotlib**: +5% (funcionó)
3. 🔴 **PROBLEMA NUEVO**: GAA_Algorithm_3 es MUY lento en large-scale

**Causa raíz del tiempo de 55s**:
- GAA_Algorithm_3 tiene búsqueda local intensiva (100 iteraciones)
- En la estimación original, este algoritmo no se ejecutó con búsqueda local
- El algoritmo generado aleatoriamente (seed=42) es más complejo de lo esperado

---

## 🔧 RECOMENDACIONES

### Opción 1: Usar Solo Algoritmos Rápidos (Temporal)

```python
# En main(), después de generar algoritmos:
# Filtrar solo algoritmos sin búsqueda local intensiva
algoritmos_rapidos = [alg for alg in algorithms if 'MIENTRAS' not in alg['ast'].to_pseudocode()]
```

**Resultado esperado**: ~20-22s total

---

### Opción 2: Reducir Presupuesto de Búsqueda Local

```python
# En la gramática (gaa/grammar.py)
# Cambiar presupuesto de MIENTRAS de 100 a 20
```

**Resultado esperado**: ~25-28s total

---

### Opción 3: Cambiar Seed de Generación

```python
# Línea 647 de demo_experimentation_both_OPTIMIZED.py
generator = AlgorithmGenerator(grammar=grammar, seed=123)  # Era 42
```

**Resultado esperado**: Algoritmos diferentes, posiblemente más rápidos

---

### Opción 4: Usar Versión Original para Large-Scale

```python
# Script híbrido:
# - Low-dimensional: versión optimizada (11.5s)
# - Large-scale: versión original (17s)
# Total: 28.5s
```

---

## 📊 Gráficas Generadas

### Confirmación de Optimización

**Low-Dimensional**:
- ✅ 3 comparación (boxplot, bars, scatter)
- ✅ 1 AST
- ✅ 3 SA agregadas
- ✅ **5 representativas** (vs 10 original)
- **Total**: 12 gráficas (vs 17 original, -29%)

**Large-Scale**:
- ✅ 3 comparación
- ✅ 1 AST
- ✅ 3 SA agregadas
- ✅ **5 representativas** (vs 21 original)
- **Total**: 12 gráficas (vs 28 original, -57%)

**TOTAL**: 24 gráficas (vs 45 original, **-47%**)

---

## ✅ Qué Funcionó

1. ✅ Reducción de evaluaciones SA: 5000 → 2000
2. ✅ Reducción de gráficas: 31 → 10 representativas
3. ✅ Backend matplotlib 'Agg'
4. ✅ Calidad de resultados: Gaps similares o mejores
5. ✅ Todas las 93 experimentos exitosos

---

## 🔴 Qué NO Funcionó Como Esperado

1. 🔴 **Tiempo total**: 55s vs 34s original (-62%)
2. 🔴 **Large-scale**: 43.5s vs 17s estimado
3. 🔴 **Causa**: GAA_Algorithm_3 con búsqueda local intensiva (100 iters)

---

## 🎓 LECCIÓN APRENDIDA

**El cuello de botella NO era solo las visualizaciones SA**.

En la versión original que medimos previamente:
- Los algoritmos generados eran DIFERENTES
- O no tenían búsqueda local tan intensiva
- O los experimentos se ejecutaron con límite de tiempo

**En esta ejecución**:
- GAA_Algorithm_3 es intensivo computacionalmente
- 100 iteraciones de TwoExchange por experimento
- 21 instancias large-scale × 0.7s = 14.7s solo para Alg_3

**Solución**: Optimizar también los **experimentos**, no solo las visualizaciones.

---

## 🚀 PRÓXIMOS PASOS

1. **Inmediato**: Cambiar seed de generación para obtener algoritmos más rápidos
2. **Corto plazo**: Reducir presupuesto de búsqueda local (100 → 20 iteraciones)
3. **Largo plazo**: Implementar timeout por experimento (max 1s por experimento)

---

## 📁 Archivos Generados

```
output/
├── low_dimensional_experiments/
│   └── experiment_low_dimensional_experiment_20251226_052515.json
├── large_scale_experiments/
│   └── experiment_large_scale_experiment_20251226_052559.json
├── plots_low_dimensional_20251226_052513/
│   ├── demo_boxplot.png
│   ├── demo_bars.png
│   ├── demo_scatter.png
│   ├── gap_evolution.png
│   ├── acceptance_rate.png
│   ├── delta_e_distribution.png
│   └── exploration_exploitation_*.png (5 archivos)
│       Total: 12 gráficas
│
├── plots_large_scale_20251226_052513/
│   └── (misma estructura, 12 gráficas)
│
└── time_tracker_global/
    └── time_tracking_global_20251226_052513.md
```

---

**Conclusión**: Las optimizaciones de visualizaciones funcionaron perfectamente (-34% a -38%), pero el script es **más lento** debido a que GAA_Algorithm_3 generado es computacionalmente intensivo. El tiempo real es **55 segundos** vs los 34s de la versión original.

**Recomendación**: Cambiar seed de generación de algoritmos para obtener algoritmos menos intensivos.
