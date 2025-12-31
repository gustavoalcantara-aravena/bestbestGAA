---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: specification
  last_modified: null
  depends_on:
    - 00-Core/Problem.md
    - 01-System/Grammar.md
    - 02-Components/Search-Operators.md
  triggers_update:
    - 04-Generated/scripts/ils_search.py
    - 04-Generated/scripts/ast_evaluator.py
---

# Función de Fitness Multi-Objetivo para GCP-ILS-GAA

> **Evaluación de configuraciones de algoritmos ILS mediante múltiples criterios de desempeño**

**Proyecto**: GCP-ILS-GAA  
**Basado en**: Problem.md, Grammar.md, Search-Operators.md  
**Versión**: 1.0.0

---

## ⚠️ ACLARACIÓN: Multi-Objetivo es Independiente del Metaheurístico

**"Multi-objetivo" NO implica Algoritmo Genético.**

Multi-objetivo = Optimizar múltiples dimensiones simultáneamente.  
Puede combinarse con CUALQUIER metaheurística:

| Metaheurística | Multi-Objetivo | Ejemplo |
|---|---|---|
| GA | Sí | NSGA-II |
| **ILS** | **Sí** | **← Este Proyecto** |
| PSO | Sí | MOPSO |
| Tabú | Sí | Tabú multi-obj |
| SA | Sí | SA multi-obj |

**Nuestra implementación**: ILS con 4 objetivos agregados mediante pesos.

---

---

## Propósito

La **función de fitness** en GAA-ILS evalúa qué tan buenos son los algoritmos generados.

Cada configuración (AST) que representa un algoritmo ILS se ejecuta en instancias de GCP para obtener:

1. **Fitness scores por instancia**: Número de colores usados
2. **Fitness agregado**: Combinación multi-objetivo de métricas

---

### ¿Por qué Multi-Objetivo?

Una buena configuración debe balancear múltiples criterios:

```
Solo calidad:          Algoritmo rápido pero inconsistente
Solo robustez:         Algoritmo lento pero confiable
Solo eficiencia:       Algoritmo que no garantiza soluciones

Multi-objetivo:        Balance de calidad + robustez + eficiencia
(Lo que implementamos)
```

Esta agregación se hace mediante **pesos** (NO mediante población/generaciones como en GA).

---

## Evaluación Básica

### Ejecución de Configuración

Para cada configuración (algoritmo ILS):

```python
def evaluate_configuration(config: Configuration, 
                         instance: GCPInstance) -> int:
    """
    Ejecutar algoritmo (config.ast) sobre instancia de GCP.
    
    Retorna: número de colores en mejor solución encontrada
    """
    algorithm = config.ast  # AlgorithmNode
    result = algorithm.execute(instance, max_time=60)
    return result['best_colors']
```

**Ejemplo**:
```
Config: [DSATUR, LS(KempeChain), Pert(Random)]
Instance: myciel3 (n=11, m=20)
Result: best_colors = 4
Fitness per instance: 4.0
```

---

## Evaluación Multi-Instancia

### Conjunto de Instancias

Una configuración se evalúa en múltiples instancias para evaluar **robustez**:

```python
def evaluate_configuration_multi_instance(config: Configuration,
                                         instances: List[GCPInstance]) -> Dict[str, float]:
    """
    Ejecutar configuración en todas las instancias.
    
    Retorna:
        {
            'instance1': colors1,
            'instance2': colors2,
            ...
        }
    """
    fitness_scores = {}
    for instance in instances:
        colors = evaluate_configuration(config, instance)
        fitness_scores[instance.name] = colors
    return fitness_scores
```

**Ejemplo con 3 instancias**:
```
myciel3:       4 colors
myciel4:       5 colors
queen5_5:      5 colors

fitness_scores = {
    'myciel3': 4.0,
    'myciel4': 5.0,
    'queen5_5': 5.0
}
```

---

## Fitness Multi-Objetivo

### Componentes de Fitness

Una configuración se evalúa en 4 dimensiones:

#### 1. Calidad (Quality)

**Métrica**: Promedio de colores sobre instancias

$$\text{Quality} = \frac{1}{n} \sum_{i=1}^{n} k_i$$

Donde:
- $k_i$ = número de colores en instancia $i$
- $n$ = número de instancias

**Rango**: [1, ∞) (usualmente 3-100)

**Mejor es**: MENOR

**Ejemplo**:
```
fitness_scores = [4, 5, 5]
quality = (4 + 5 + 5) / 3 = 4.67
```

**Fórmula en código**:
```python
def compute_quality(fitness_scores: Dict[str, float]) -> float:
    scores = list(fitness_scores.values())
    return sum(scores) / len(scores) if scores else float('inf')
```

---

#### 2. Robustez (Robustness)

**Métrica**: Consistencia del desempeño entre instancias

$$\text{Robustness} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (k_i - \bar{k})^2}$$

Donde:
- $\bar{k}$ = promedio de colores
- Desviación estándar de fitness scores

**Rango**: [0, ∞)

**Mejor es**: MENOR (baja varianza = más consistente)

**Ejemplo**:
```
fitness_scores = [4, 5, 5]
mean = 4.67
variance = ((4-4.67)² + (5-4.67)² + (5-4.67)²) / 3
         = (0.449 + 0.108 + 0.108) / 3
         = 0.222
robustness = sqrt(0.222) = 0.471
```

**Interpretación**:
- Robustness ≈ 0.0: Todas las instancias dan mismo resultado (EXCELENTE)
- Robustness ≈ 1.0: Resultados varían significativamente (POBRE)

**Fórmula en código**:
```python
def compute_robustness(fitness_scores: Dict[str, float]) -> float:
    scores = list(fitness_scores.values())
    if len(scores) < 2:
        return 0.0
    mean = sum(scores) / len(scores)
    variance = sum((s - mean)**2 for s in scores) / len(scores)
    return variance ** 0.5
```

---

#### 3. Velocidad (Time Efficiency)

**Métrica**: Penalidad por complejidad de AST

$$\text{Time} = 0.01 \times |AST|$$

Donde:
- $|AST|$ = número de nodos en el árbol

**Rango**: [0.01, 1.0] típicamente

**Mejor es**: MENOR (ASTs más simples)

**Ejemplo**:
```
AST nodes: 15
time_penalty = 0.01 * 15 = 0.15
```

**Justificación**:
- Preferir algoritmos más simples (parsimonia)
- Reducir sobreajuste
- Favorecer interpretabilidad
- Reducir tiempo de ejecución

**Fórmula en código**:
```python
def compute_time_penalty(config: Configuration) -> float:
    stats = ast_statistics(config.ast)
    return stats['num_nodes'] * 0.01
```

---

#### 4. Factibilidad (Feasibility)

**Métrica**: Verificar que siempre encuentra soluciones factibles

$$\text{Feasibility} = \begin{cases}
1.0 & \text{si todos los resultados son factibles} \\
100.0 & \text{si alguno es infactible}
\end{cases}$$

**Rango**: {1.0, 100.0}

**Mejor es**: MENOR (valor 1.0)

**Restricción dura**: Todas las configuraciones deben ser factibles

**Ejemplo**:
```
# Config A: Siempre encuentra soluciones válidas
feasibility = 1.0  ✓

# Config B: A veces genera colorings con conflictos
feasibility = 100.0  ✗ (penalización severa)
```

**Fórmula en código**:
```python
def compute_feasibility(fitness_scores: Dict[str, float]) -> float:
    # Si algún score es inf, hubo infactibilidad
    if any(s == float('inf') for s in fitness_scores.values()):
        return 100.0
    return 1.0
```

---

### Agregación Multi-Objetivo

**Combinación ponderada** de las 4 dimensiones:

$$\text{Fitness} = w_q \cdot \text{Quality} + w_t \cdot \text{Time} + w_r \cdot \text{Robustness} + w_f \cdot \text{Feasibility}$$

Donde:
- $w_q$ = peso de calidad
- $w_t$ = peso de tiempo
- $w_r$ = peso de robustez
- $w_f$ = peso de factibilidad
- $\sum w = 1.0$

**Pesos por defecto** (recomendados):

```yaml
fitness_weights:
  quality: 0.50      # Prioridad: calidad de soluciones
  robustness: 0.20   # Consistencia
  time: 0.20         # Eficiencia
  feasibility: 0.10  # Siempre factible
```

**Justificación**:
- 50% calidad: Objetivo primario de GCP
- 20% robustness: Algoritmo debe ser fiable
- 20% time: ASTs simples son mejores
- 10% feasibility: Restricción de viabilidad

---

#### Ejemplo de Cálculo Completo

**Configuración A**:
```
Quality:      4.67  (promedio de [4, 5, 5])
Robustness:   0.47  (desviación estándar)
Time:         0.15  (15 nodos × 0.01)
Feasibility:  1.0   (todos factibles)

Fitness = 0.50×4.67 + 0.20×0.47 + 0.20×0.15 + 0.10×1.0
        = 2.335 + 0.094 + 0.030 + 0.100
        = 2.559
```

**Configuración B**:
```
Quality:      5.23  (promedio de [5, 5, 6])
Robustness:   0.41  (más consistente)
Time:         0.25  (25 nodos × 0.01)
Feasibility:  1.0   (todos factibles)

Fitness = 0.50×5.23 + 0.20×0.41 + 0.20×0.25 + 0.10×1.0
        = 2.615 + 0.082 + 0.050 + 0.100
        = 2.847
```

**Conclusion**: Config A es mejor (fitness 2.559 < 2.847)
- Mejor calidad de soluciones
- Más simple (menos nodos)

---

## Variantes de Fitness

### Variante 1: Quality-Only (Baseline)

Para comparación, se puede usar fitness basado solo en calidad:

```python
fitness = quality_only(config)  # Solo colores promedio
```

**Ventaja**: Simple de entender y comparar

**Desventaja**: No considera robustez ni eficiencia

---

### Variante 2: Lexicográfica

Ordenar por criterios en cascada:

```python
def lexicographic_fitness(config):
    return (
        compute_feasibility(config),     # Primero: viabilidad
        compute_quality(config),          # Segundo: calidad
        -compute_robustness(config),      # Tercero: robustez
        compute_time_penalty(config)      # Cuarto: eficiencia
    )
```

**Uso**: Comparación de Pareto, exploración multi-objetivo

---

### Variante 3: Normalización por Instancia

Normalizar respecto a mejores/peores conocidos:

$$\text{Quality}_{norm} = \frac{\text{Quality} - \text{Best Known}}{\text{Worst Known} - \text{Best Known}}$$

**Ventaja**: Interpretación más clara (0=óptimo, 1=peor)

**Desventaja**: Requiere benchmarks de referencia

---

## Evaluación Paralela

### Multi-Instancia Paralela

Para aceleración, evaluaciones en múltiples instancias pueden paralelizarse:

```python
def evaluate_parallel(config: Configuration,
                     instances: List[GCPInstance],
                     num_workers: int = 4) -> Dict[str, float]:
    """Evaluar config en instancias con workers paralelos"""
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(evaluate_configuration, config, inst): inst.name
            for inst in instances
        }
        results = {}
        for future in as_completed(futures):
            instance_name = futures[future]
            colors = future.result()
            results[instance_name] = colors
    return results
```

**Speedup esperado**: ~num_workers × (si instancias son grandes)

---

## Benchmarking

### Instancias de Entrenamiento

Conjunto pequeño para evaluación rápida durante ILS:

```
myciel3.col    (n=11,  m=20)      ~ 0.5s
myciel4.col    (n=23,  m=71)      ~ 2s
queen5_5.col   (n=25,  m=160)     ~ 3s
```

**Tiempo total por config**: ~5-10s

---

### Instancias de Validación

Conjunto mediano para validación:

```
anna.col       (n=138, m=493)     ~ 10s
huck.col       (n=74,  m=301)     ~ 5s
jean.col       (n=80,  m=254)     ~ 5s
```

**Tiempo total per config**: ~20-30s

---

### Instancias de Test

Conjunto grande para evaluación final:

```
queen8_8.col   (n=64,  m=728)     ~ 15s
queen9_9.col   (n=81,  m=1152)    ~ 25s
games120.col   (n=120, m=638)     ~ 20s
```

**Tiempo total por config**: ~60-90s

---

## Configuración de Evaluación

```yaml
# Evaluation parameters
max_time_per_instance: 60         # Máximo 60s por instancia
num_workers: 4                    # Evaluación paralela

# Instance selection
training_instances:
  - datasets/training/myciel3.col
  - datasets/training/myciel4.col
  - datasets/training/queen5_5.col

validation_instances:
  - datasets/validation/anna.col
  - datasets/validation/huck.col
  - datasets/validation/jean.col

test_instances:
  - datasets/test/queen8_8.col
  - datasets/test/games120.col
```

---

## Comparación de Algoritmos

### Tabla de Resultados

| Config | Quality | Robust | Time | Feasible | Fitness |
|--------|---------|--------|------|----------|---------|
| Config A | 4.67 | 0.47 | 0.15 | 1.0 | **2.559** |
| Config B | 5.23 | 0.41 | 0.25 | 1.0 | 2.847 |
| Config C | 4.33 | 0.52 | 0.20 | 1.0 | 2.488 |

**Ranking**: C > A > B

---

## Criterios de Parada

### Convergencia Global

El ILS-search se detiene cuando:

```python
if best_fitness <= target_fitness:
    print("Target reached!")
    break

if no_improvement_count >= max_no_improve_iterations:
    print("Stagnation detected!")
    break

if elapsed_time >= max_time_seconds:
    print("Time limit!")
    break
```

**Valores por defecto**:
```yaml
max_iterations: 500
max_no_improve_iterations: 50
max_time_seconds: 3600  # 1 hora
```

---

## Referencias

- Zitzler, E., Laumanns, M., & Thiele, L. (2001). SPEA2: Improving the Strength Pareto Evolutionary Algorithm.
- Hansen, N., & Ostermeier, A. (2001). Completely Derandomized Self-Adaptation in Evolution Strategies.
- Galinier, P., & Hao, J. K. (1999). Hybrid evolutionary algorithms for graph coloring.

---

**Próximo paso**: Implementación en `04-Generated/scripts/ast_evaluator.py`
