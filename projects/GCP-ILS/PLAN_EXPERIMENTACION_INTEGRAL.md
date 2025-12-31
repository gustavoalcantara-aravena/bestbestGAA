# Plan de Experimentación Integral - GCP-ILS

**Fecha**: 30 de Diciembre, 2025  
**Proyecto**: GCP-ILS  
**Objetivo**: Análisis exhaustivo del rendimiento del algoritmo ILS

---

## 📋 Plan Ejecutivo

### Fases de Experimentación

```
FASE 1: BENCHMARK BASELINE (15 min)
├─ Ejecutar instancias de referencia con parámetros por defecto
├─ Establecer métricas base (tiempo, calidad, factibilidad)
└─ Generar tabla de resultados

FASE 2: COMPARATIVA DE OPERADORES (30 min)
├─ Variar constructivas (5 alternativas)
├─ Variar local search (4 alternativas)
├─ Medir impacto en calidad y convergencia
└─ Identificar mejores combinaciones

FASE 3: PARAMETER TUNING (25 min)
├─ Variar max_iterations (100, 500, 1000, 2000)
├─ Variar perturbation_strength (0.1, 0.2, 0.3, 0.5)
├─ Variar restart_threshold (10, 30, 50, 100)
└─ Análisis de sensibilidad

FASE 4: INSTANCIA SCALING (20 min)
├─ Pequeñas (n < 50): myciel3-5
├─ Medianas (50 < n < 500): le450_5a-d
├─ Grandes (n > 500): school1, miles*
└─ Analizar escalabilidad

FASE 5: CONVERGENCE ANALYSIS (20 min)
├─ Registrar k en cada iteración
├─ Graficar convergencia
├─ Medir velocidad de convergencia
└─ Análisis de estabilidad

FASE 6: BENCHMARK vs ÓPTIMOS (15 min)
├─ Comparar contra óptimos conocidos (si están disponibles)
├─ Calcular gap para cada instancia
├─ Evaluar calidad de soluciones
└─ Generar reporte final
```

**Tiempo Total Estimado**: ~2 horas

---

## 📊 Estructura de Datos para Resultados

### Tabla Principal de Resultados
```
instance | n | m | constructive | local_search | max_iter | k_found | optimal | gap% | time(s) | feasible | iters_completed
---------|---|---|---|---|---|---|---|---|---|---|---|---
myciel3  | 11| 20| dsatur       | kempe        | 100      | 4       | ?       | ?    | 0.01   | YES      | 100
...
```

### Tabla de Convergencia
```
instance | iteration | k_current | time_at_iter | improvement
---------|-----------|-----------|--------------|-------------
myciel4  | 0         | 5         | 0.0          | initial
myciel4  | 1         | 5         | 0.001        | -
myciel4  | 5         | 5         | 0.005        | -
...
```

### Tabla de Sensibilidad de Parámetros
```
parameter | value | avg_quality | avg_time | std_dev
----------|-------|-------------|----------|--------
max_iter  | 100   | 5.2         | 0.5s     | 0.3
max_iter  | 500   | 4.8         | 1.2s     | 0.2
max_iter  | 1000  | 4.5         | 2.1s     | 0.1
...
```

---

## 🔧 Scripts a Crear

### 1. `experimentation/experiment_benchmark.py`
```python
"""
Fase 1: Benchmark Baseline
- Ejecutar 15 instancias con parámetros por defecto
- Medir tiempo, calidad, factibilidad
- Generar tabla de resultados
"""
```

### 2. `experimentation/experiment_operators.py`
```python
"""
Fase 2: Comparativa de Operadores
- 5 constructivas × 4 local search = 20 combinaciones
- Ejecutar sobre 5 instancias pequeñas
- Medir impacto en k y convergencia
"""
```

### 3. `experimentation/experiment_parameters.py`
```python
"""
Fase 3: Parameter Tuning
- max_iterations: [100, 500, 1000, 2000]
- perturbation_strength: [0.1, 0.2, 0.3, 0.5]
- restart_threshold: [10, 30, 50, 100]
- Análisis de sensibilidad 3D
"""
```

### 4. `experimentation/experiment_scaling.py`
```python
"""
Fase 4: Instancia Scaling
- Instancias pequeñas (n<50)
- Instancias medianas (50<n<500)
- Instancias grandes (n>500)
- Analizar crecimiento de tiempo
"""
```

### 5. `experimentation/experiment_convergence.py`
```python
"""
Fase 5: Convergence Analysis
- Registrar k en cada iteración
- Graficar evolución
- Medir velocidad de convergencia
- Estadísticas de estabilidad
"""
```

### 6. `experimentation/experiment_benchmark_optimal.py`
```python
"""
Fase 6: Benchmark vs Óptimos
- Cargar óptimos conocidos
- Calcular gaps
- Generar reporte final
"""
```

### 7. `experimentation/run_all_experiments.py`
```python
"""
Master script: Ejecuta todas las fases
- Orquesta las 6 fases
- Recolecta resultados
- Genera reportes integrados
"""
```

---

## 📈 Métricas a Recopilar

### Por Ejecución
- **k_found**: Número de colores encontrados
- **time_elapsed**: Tiempo total en segundos
- **iterations_completed**: Iteraciones hasta terminar
- **feasible**: Si la solución es válida
- **conflicts**: Número de conflictos (siempre debe ser 0)
- **improvement_rate**: (k_initial - k_final) / k_initial

### Agregadas
- **avg_quality**: k promedio por instancia
- **std_quality**: Desviación estándar de k
- **avg_time**: Tiempo promedio por instancia
- **convergence_speed**: Iteraciones necesarias para converger
- **robustness**: % de ejecuciones exitosas

### Comparativas
- **gap_to_optimal**: (k_found - optimal) / optimal * 100
- **speedup**: tiempo_baseline / tiempo_variante
- **quality_improvement**: (k_baseline - k_variante) / k_baseline * 100

---

## 🎯 Instancias Seleccionadas

### Benchmark Set (15 instancias variadas)

**Pequeñas (n < 50)**:
- myciel3 (11 vértices)
- myciel4 (23 vértices)
- myciel5 (47 vértices)

**Medianas (50 < n < 500)**:
- le450_5a (450 vértices)
- le450_5b (450 vértices)
- le450_15a (450 vértices)

**Grandes (n > 500)**:
- school1 (385 vértices)
- anna (138 vértices)
- david (87 vértices)
- homer (561 vértices)
- huck (74 vértices)
- jean (80 vértices)
- games120 (120 vértices)
- miles500 (128 vértices)
- queen10_10 (100 vértices)

**Total**: 15 instancias cobriendo todas las familias

---

## 📊 Salidas Esperadas

### Reportes Generados

1. **results/benchmark_baseline.csv**
   - Resultados de fase 1
   - 15 instancias × parámetros por defecto

2. **results/operators_comparison.csv**
   - Resultados de fase 2
   - 20 combinaciones × 5 instancias

3. **results/parameter_tuning.csv**
   - Resultados de fase 3
   - Análisis de sensibilidad

4. **results/scaling_analysis.csv**
   - Resultados de fase 4
   - Relación n vs tiempo

5. **results/convergence_data.csv**
   - Datos de convergencia
   - k vs iteración para gráficos

6. **results/benchmark_optimal.csv**
   - Gaps respecto a óptimos
   - Evaluación de calidad

7. **results/EXPERIMENT_REPORT.md**
   - Resumen ejecutivo
   - Gráficos y análisis
   - Conclusiones

---

## 🎬 Ejecución

### Comando Master
```bash
python experimentation/run_all_experiments.py
```

### O por fases
```bash
python experimentation/experiment_benchmark.py
python experimentation/experiment_operators.py
python experimentation/experiment_parameters.py
python experimentation/experiment_scaling.py
python experimentation/experiment_convergence.py
python experimentation/experiment_benchmark_optimal.py
```

---

## 📈 Gráficos Esperados

### Fase 2: Comparativa de Operadores
```
Gráfico de barras: Promedio k por constructor/local_search
- X: Combinaciones de operadores
- Y: k promedio
```

### Fase 3: Parameter Tuning
```
Heatmap 3D: max_iterations vs perturbation_strength vs restart_threshold
- Color: k promedio
```

### Fase 4: Scaling
```
Línea: Tamaño instancia vs Tiempo
- X: n (vértices)
- Y: Tiempo (segundos)
- Regresión para estimar complejidad
```

### Fase 5: Convergence
```
Línea múltiple: Iteración vs k
- Una línea por instancia
- Mostrar velocidad de convergencia
```

---

## ✅ Checklist de Implementación

- [ ] Crear estructura `/experimentation/` con 7 scripts
- [ ] Crear `/results/` para almacenar CSVs
- [ ] Implementar recolección de datos uniforme
- [ ] Implementar generación de gráficos
- [ ] Implementar reporte final integrado
- [ ] Ejecutar todas las fases
- [ ] Validar resultados
- [ ] Documentar hallazgos

---

## 📝 Salida Final Esperada

```
EXPERIMENT COMPLETE: GCP-ILS Comprehensive Analysis
=====================================================

Phase 1: Benchmark Baseline
  ✓ 15 instances analyzed
  ✓ Average k: 5.8
  ✓ Average time: 1.2s

Phase 2: Operators Comparison
  ✓ 20 combinations tested
  ✓ Best: DSATUR + KempeChain (avg k=5.2)
  ✓ Worst: Random + SwapColors (avg k=6.8)

Phase 3: Parameter Tuning
  ✓ 64 combinations analyzed
  ✓ Optimal: max_iter=1000, perturb=0.2, restart=50
  ✓ Quality improvement: +15%

Phase 4: Scaling Analysis
  ✓ Complexity: ~O(n^1.5)
  ✓ Largest instance: 561 verts in 12.3s

Phase 5: Convergence Analysis
  ✓ Median convergence: 120 iterations
  ✓ Stability: 98% (consistent results)

Phase 6: Benchmark vs Optimal
  ✓ Average gap: 12%
  ✓ Best performance: myciel3 (0% gap)
  ✓ Worst performance: le450_5a (45% gap)

=====================================================
Reports saved to: results/
Graphs saved to: results/graphs/
```

---

## 💡 Decisiones Clave del Plan

1. **Instancias variadas**: Desde muy pequeñas a grandes para ver escalabilidad
2. **Combinaciones completas**: Todos los operadores × instancias para comparativa justa
3. **Parameter tuning sistemático**: Análisis de sensibilidad para encontrar óptimos
4. **Convergence tracking**: Entender cómo se comporta el algoritmo
5. **Benchmark vs óptimos**: Validar que el algoritmo produce buenas soluciones

---

**Próximo paso**: ¿Quieres que implemente todos estos scripts de experimentación?
