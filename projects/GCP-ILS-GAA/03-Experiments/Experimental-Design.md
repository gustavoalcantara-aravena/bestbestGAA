---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
    - 00-Core/Metaheuristic.md
  auto_sync: true
---

# Diseño Experimental - GCP-ILS-GAA

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md` y `Metaheuristic.md`.

**Proyecto**: GCP-ILS-GAA  
**Problema**: Graph Coloring Problem (GCP)  
**Metaheurística**: Iterated Local Search (ILS)  
**Fecha**: 30 de Diciembre, 2025  

---

## 📋 Protocolo Experimental Integral

### Configuración Global

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Réplicas por instancia** | 10 | Ejecuciones independientes para estadística |
| **Semilla base** | 42 | Reproducibilidad (seeds: 42, 123, 456, ...) |
| **Presupuesto computacional** | 500 iteraciones | O máximo 300 segundos |
| **Nivel significancia** | α = 0.05 | Para pruebas estadísticas |

---

## 🎯 6 Fases de Experimentación

### FASE 1: BENCHMARK BASELINE

**Objetivo**: Establecer línea base de rendimiento

**Configuración**:
```yaml
Parameters:
  max_iterations: 500
  local_search_iterations: 100
  perturbation_strength: 0.2
  restart_threshold: 50
  constructive_heuristic: "DSATUR"
  acceptance_criterion: "better_or_equal"
```

**Instancias de Prueba**:
```
myciel3:  n=11,  m=20,   χ=4
myciel4:  n=23,  m=71,   χ=5
myciel5:  n=47,  m=236,  χ=6
```

**Métricas a Registrar**:

| Métrica | Fórmula | Interpretación |
|---------|---------|---|
| **k_found** | max(coloring) | Número de colores encontrado |
| **k_optimal** | Dato problema | Óptimo conocido |
| **gap%** | (k_found - k_opt) / k_opt * 100 | % distancia a óptimo |
| **time(s)** | Tiempo de ejecución | Segundos hasta convergencia |
| **conflicts** | # aristas violadas | Cero para solución factible |
| **iterations** | # iteraciones ejecutadas | Convergencia rápida vs lenta |

**Salida Esperada**:

```markdown
| Instancia | n  | m   | k_found | k_opt | gap% | time(s) | conflicts | iters |
|-----------|----|----|---------|-------|------|---------|-----------|-------|
| myciel3   | 11 | 20 | 4       | 4     | 0%   | 0.01    | 0         | 5     |
| myciel4   | 23 | 71 | 5       | 5     | 0%   | 0.05    | 0         | 12    |
| myciel5   | 47 | 236| 6       | 6     | 0%   | 0.2     | 0         | 25    |
```

**Duración Esperada**: 15 minutos

---

### FASE 2: COMPARATIVA DE OPERADORES

**Objetivo**: Identificar mejores combinaciones de operadores

**Dimensiones de Variación**:

**1. Constructivas**:
- DSATUR (voraz por saturación)
- LargestFirst (voraz por grado)
- SmallestLast (orden mínimo grado)
- RandomSequential (aleatorio)

**2. Mejora Local**:
- KempeChain (intercambio de 2 colores)
- SingleVertex (recolorear 1 vértice)
- ColorMerge (fusionar clases de color)

**Diseño Experimental** (Factorial parcial):

```
Constructivas × LocalSearch = 4 × 3 = 12 combinaciones
Por cada combinación: 5 réplicas
Total: 12 × 5 = 60 ejecuciones en Fase 2
```

**Tabla de Resultados**:

```markdown
| Constructiva | LocalSearch | avg_k | std_k | avg_time | best% |
|--------------|-------------|-------|-------|----------|-------|
| DSATUR       | KempeChain  | 4.0   | 0.0   | 0.05     | 100%  |
| DSATUR       | SingleVert  | 4.1   | 0.3   | 0.03     | 80%   |
| LargestFirst | KempeChain  | 4.2   | 0.4   | 0.04     | 60%   |
| ...          | ...         | ...   | ...   | ...      | ...   |
```

**Duración Esperada**: 30 minutos

---

### FASE 3: PARAMETER TUNING (Sensibilidad)

**Objetivo**: Optimizar parámetros del algoritmo

**Parámetros a Variar**:

| Parámetro | Valores a Probar | Rango | Por defecto |
|-----------|------------------|-------|------------|
| **max_iterations** | 100, 500, 1000, 2000 | [100, 5000] | 500 |
| **perturbation_strength** | 0.1, 0.2, 0.3, 0.5 | [0.05, 0.5] | 0.2 |
| **restart_threshold** | 10, 30, 50, 100 | [10, 200] | 50 |

**Diseño**: One-factor-at-a-time (OFAT)

```
3 parámetros × 4 valores cada uno = 12 configuraciones
Por cada config: 10 réplicas × 3 instancias = 30 ejecuciones
Total: 12 × 30 = 360 ejecuciones
```

**Tabla de Sensibilidad**:

```markdown
| Parameter | Value | Avg_k | Avg_Time | Desv.Std | Ranking |
|-----------|-------|-------|----------|----------|---------|
| max_iter  | 100   | 5.1   | 0.5s     | 0.4      | 3/4     |
| max_iter  | 500   | 4.8   | 1.2s     | 0.2      | 1/4     |
| max_iter  | 1000  | 4.7   | 2.1s     | 0.15     | 2/4     |
| max_iter  | 2000  | 4.6   | 4.0s     | 0.1      | 1/4     |
|-----------|-------|-------|----------|----------|---------|
| pert_str  | 0.1   | 5.3   | 1.1s     | 0.5      | 4/4     |
| pert_str  | 0.2   | 4.8   | 1.2s     | 0.2      | 1/4     |
| pert_str  | 0.3   | 4.9   | 1.3s     | 0.25     | 2/4     |
| pert_str  | 0.5   | 5.0   | 1.4s     | 0.3      | 3/4     |
```

**Duración Esperada**: 25 minutos

---

### FASE 4: INSTANCIA SCALING

**Objetivo**: Evaluar escalabilidad con tamaño del problema

**Clasificación por Tamaño**:

| Clase | Rango n | Instancias | # Nodos | Densidad |
|-------|---------|-----------|---------|----------|
| **Pequeña** | 11-50 | myciel3-5, queen8-8 | 5-7 | media |
| **Mediana** | 50-500 | le450_5a-d, queen11-11 | 4 | media |
| **Grande** | 500+ | school1, miles | 2-3 | variable |

**Protocolo**:

```
3 clases × 3-5 instancias = 12 instancias
Por cada instancia: 5 réplicas
Total: 12 × 5 = 60 ejecuciones
```

**Análisis**:

```python
# Gráfico esperado: k vs n (log-log)
# Línea de tendencia: O(n^α)
# Expectativa: α ≈ 0.3-0.5 (logarítmico a lineal)
```

**Tabla de Escalabilidad**:

```markdown
| Clase     | Instancia | n   | m    | χ_opt | χ_found | time(s) | gap% |
|-----------|-----------|-----|------|-------|---------|---------|------|
| Pequeña   | myciel3   | 11  | 20   | 4     | 4       | 0.01    | 0%   |
|           | myciel5   | 47  | 236  | 6     | 6       | 0.2     | 0%   |
| Mediana   | le450_5a  | 450 | 5714 | 5     | 5       | 12      | 0%   |
| Grande    | school1   | 385 | 19095| 14    | 14-15   | 45      | 0-7% |
```

**Duración Esperada**: 20 minutos

---

### FASE 5: CONVERGENCE ANALYSIS

**Objetivo**: Analizar velocidad y patrón de convergencia

**Registro Detallado por Iteración**:

```python
# Por cada iteración i:
log[i] = {
    'iteration': i,
    'k_current': número colores en solución actual,
    'k_best': mejor k encontrado hasta ahora,
    'conflicts': número de violaciones,
    'time_elapsed': tiempo transcurrido,
    'accepted': si la solución fue aceptada
}
```

**Análisis**:

1. **Convergencia General**:
   - Graficar k_best vs iteración
   - Identificar punto de convergencia (sin mejora por X iteraciones)

2. **Velocidad de Convergencia**:
   - Cuántas iteraciones para alcanzar óptimo local
   - Cuántas para alcanzar óptimo global (si existe)

3. **Estabilidad**:
   - Variabilidad entre réplicas
   - Robustez a cambios de semilla

**Gráficos Esperados**:

```
Figura 1: Convergencia típica (pequeña)
k
|     
6 |     *
5 |     * *
4 | * * * * * * * * 
3 |
  +----+----+----+----+----+
    0   50  100  150  200  iteraciones

Figura 2: Convergencia (mediana)
k
|     
8 |       
7 |   *         
6 | * *   *     
5 | * * * * * * * * * *
4 |
  +----+----+----+----+----+
    0  100  200  300  400  iteraciones
```

**Duración Esperada**: 20 minutos

---

### FASE 6: BENCHMARK vs ÓPTIMOS

**Objetivo**: Evaluar calidad de soluciones vs óptimos conocidos

**Comparación**: ILS vs Óptimos/Best-Known

```markdown
| Instancia | n   | χ_known | χ_ils | gap% | tiempo(s) | factible? |
|-----------|-----|---------|-------|------|-----------|-----------|
| myciel3   | 11  | 4       | 4     | 0%   | 0.01      | ✓         |
| myciel4   | 23  | 5       | 5     | 0%   | 0.05      | ✓         |
| myciel5   | 47  | 6       | 6     | 0%   | 0.2       | ✓         |
| le450_5a  | 450 | 5       | 5     | 0%   | 12.5      | ✓         |
| le450_5b  | 450 | 5       | 5     | 0%   | 11.8      | ✓         |
| school1   | 385 | 14      | 14    | 0%   | 38.2      | ✓         |
| miles1000 | 128 | 10      | 10    | 0%   | 2.5       | ✓         |
```

**Estadísticas Resumidas**:

```
Mean gap: 0.5%
Std gap: 1.2%
Min gap: 0%
Max gap: 7%
Instances solved optimally: 15/16
Median time: 1.2s
```

**Duración Esperada**: 15 minutos

---

## 📊 Análisis Estadístico

### Pruebas de Hipótesis

| Pregunta | Prueba | Null Hypothesis |
|----------|--------|-----------------|
| ¿DSATUR mejor que Random? | Wilcoxon | μ(DSATUR) = μ(Random) |
| ¿Máx iter = 500 vs 1000? | t-test | μ(500) = μ(1000) |
| ¿Hay diferencias significativas? | ANOVA | Todos los grupos iguales |

### Nivel de Significancia

- α = 0.05 (5% error Tipo I)
- Método de corrección: Bonferroni (si múltiples comparaciones)

---

## 📈 Formato de Reportes

### Tabla de Resultados Consolidada

```markdown
## FASE 1: BASELINE
| Instancia | k_found | k_opt | gap% | time(s) |
|-----------|---------|-------|------|---------|
| ...       | ...     | ...   | ...  | ...     |
**Promedio**: gap% = 0.0%, time = 0.1s

## FASE 2: OPERADORES
**Mejor combinación**: DSATUR + KempeChain
**Mejora respecto baseline**: -2% gap, -5% tiempo

## FASE 3: TUNING
**Parámetros óptimos encontrados**:
- max_iterations: 1000 (+100% gap mejor)
- perturbation_strength: 0.2 (sin cambio significativo)
- restart_threshold: 50 (recomendado)

## FASE 4: SCALING
**Conclusión**: O(n^0.4) - Escalabilidad logarítmica
**Rango aplicable**: n ≤ 1000

## FASE 5: CONVERGENCIA
**Velocidad típica**: Convergencia en 50-100 iteraciones
**Patrón**: Rápido inicial, luego estabilización

## FASE 6: BENCHMARK
**Calidad**: 0% gap promedio (óptimo)
**Cobertura**: 15/16 instancias en óptimo
```

### Gráficos a Generar

1. **Box plots**: Distribución de k por heurística constructiva
2. **Curvas de convergencia**: k vs iteración para instancias representativas
3. **Scatter plots**: Calidad vs tiempo por instancia
4. **Heatmap**: Matriz de comparación de parámetros
5. **Line plot**: Escalabilidad (n vs tiempo)

---

## 🔄 Reproducibilidad

### Información a Registrar

- Versión del código: GCP-ILS-GAA v1.0.0
- Fecha de ejecución: 30/12/2025
- Sistema operativo: Windows 10
- Python: 3.8+
- Semillas aleatorias: 42, 123, 456, 789, 999, ...
- Parámetros exactos de cada fase
- Versión del framework GAA: v1.0

### Archivos de Salida

```
results/
├── phase1_baseline.csv
├── phase2_operators.csv
├── phase3_tuning.csv
├── phase4_scaling.csv
├── phase5_convergence.csv
├── phase6_benchmark.csv
├── plots/
│   ├── convergence.png
│   ├── scaling.png
│   └── comparison.png
└── report.md
```

---

## ✅ Checklist de Ejecución

```
[ ] FASE 1: Ejecutar benchmark baseline
    [ ] Configurar ILSParameters por defecto
    [ ] Ejecutar 3 instancias × 10 réplicas
    [ ] Registrar resultados en CSV
    [ ] Generar tabla resumen

[ ] FASE 2: Comparativa de operadores
    [ ] Definir matriz de combinaciones
    [ ] Ejecutar 12 × 5 = 60 ejecuciones
    [ ] Análisis de varianza
    [ ] Identificar mejor combinación

[ ] FASE 3: Parameter Tuning
    [ ] Variar max_iterations
    [ ] Variar perturbation_strength
    [ ] Variar restart_threshold
    [ ] Generar gráficos de sensibilidad

[ ] FASE 4: Instancia Scaling
    [ ] Cargar instancias por clase de tamaño
    [ ] Medir tiempo y calidad
    [ ] Graficar escalabilidad
    [ ] Estimar complejidad

[ ] FASE 5: Convergence Analysis
    [ ] Registrar k por iteración
    [ ] Generar curvas de convergencia
    [ ] Medir velocidad
    [ ] Analizar estabilidad

[ ] FASE 6: Benchmark vs Óptimos
    [ ] Compilar óptimos conocidos
    [ ] Calcular gaps
    [ ] Generar reporte final
    [ ] Conclusiones
```

---

## 📝 Notas

- Todas las ejecuciones deben ser **determinísticas** (usar semillas fijas)
- Registrar **todos los parámetros** para reproducibilidad
- Generar **plots automáticamente** con matplotlib/plotly
- Guardar resultados en **CSV** para análisis posterior
- Documentar **desviaciones** del protocolo

---

**Última actualización**: 30 de Diciembre, 2025  
**Responsable**: GAA Framework  
**Status**: 🟢 Listo para ejecutar
