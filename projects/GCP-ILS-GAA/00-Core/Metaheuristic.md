---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: trigger
  last_modified: null
  triggers_update:
    - 02-Components/Search-Operators.md
    - 02-Components/Fitness-Function.md
    - 03-Experiments/Experimental-Design.md
    - 04-Generated/scripts/metaheuristic_ils.py
  extraction_rules:
    algorithm_type: "section:Selected-Metaheuristic"
    parameters: "section:Configuration"
    operators: "section:Search-Strategy"
---

# Metaheurística: Iterated Local Search (ILS) para GCP

> **🎯 ARCHIVO EDITABLE**: Este archivo es un trigger principal para GCP-ILS-GAA. Al editarlo, se actualizarán automáticamente todos los archivos dependientes.

**Proyecto**: GCP-ILS-GAA  
**Metaheurística**: Iterated Local Search (ILS)  
**Versión**: 1.0.0

---

## Selected-Metaheuristic

**Algoritmo**: Iterated Local Search (ILS)  
**Tipo**: Local Search + Perturbation (Hybrid)  
**Categoría**: Trajectory-based Metaheuristic  
**Referencias**: [Lourenço2003, Stützle2010]

### Descripción del Método

**Iterated Local Search (ILS)** es un algoritmo de búsqueda que combina:

1. **Búsqueda Local (LS)**: Mejora iterativa desde solución actual
2. **Perturbación**: Modifica solución actual para escapar óptimos locales
3. **Criterio de Aceptación**: Decide si aceptar nueva solución

**Pseudocódigo**:
```
s := ConstructureInitialSolution()
s* := LocalSearch(s)
repeat
    s' := Perturbation(s*, intensidad)
    s' := LocalSearch(s')
    s* := AcceptanceCriterion(s*, s')
until TerminationCondition()
return s*
```

### Ventajas para GCP

- ✅ **Simple y efectivo**: Fácil de implementar y entender
- ✅ **Flexible**: Combina múltiples constructivas y mejoras locales
- ✅ **Adaptable**: Parámetros sintonizables según instancia
- ✅ **Robusto**: Escala bien con tamaño del problema

---

## Configuration

### Parámetros Principales

#### Parámetros de Búsqueda

| Parámetro | Valor por Defecto | Rango | Descripción |
|-----------|-------------------|-------|-------------|
| `max_iterations` | 500 | [100, 5000] | Máximo de iteraciones del algoritmo principal |
| `local_search_iterations` | 100 | [10, 1000] | Iteraciones de búsqueda local por perturbación |
| `perturbation_strength` | 0.2 | [0.05, 0.5] | Porcentaje de vértices a perturbar (rango 0-1) |
| `restart_threshold` | 50 | [10, 200] | Reiniciar si no hay mejora en N iteraciones |
| `restart_intensity` | 0.5 | [0.1, 1.0] | Intensidad de perturbación en reinicio |

#### Parámetros de Construcción Inicial

| Parámetro | Valor por Defecto | Descripción |
|-----------|-------------------|-------------|
| `constructive_heuristic` | "DSATUR" | Método para solución inicial (DSATUR, LF, SL, RLC, RLF) |
| `initial_k_estimate` | "greedy" | Estimación inicial de $k$ (greedy, heurístico, fijo) |

#### Parámetros de Aceptación

| Parámetro | Valor por Defecto | Descripción |
|-----------|-------------------|-------------|
| `acceptance_criterion` | "better_or_equal" | Criterio de aceptación (better, better_or_equal, metropolis) |
| `temperature` | 0.1 | Temperatura para criterio Metropolis (si aplica) |

### Configuración Recomendada por Instancia

#### Instancias Pequeñas (n < 100)
```yaml
max_iterations: 1000
local_search_iterations: 200
perturbation_strength: 0.15
restart_threshold: 100
acceptance_criterion: "better_or_equal"
```

#### Instancias Medianas (100 ≤ n < 500)
```yaml
max_iterations: 500
local_search_iterations: 100
perturbation_strength: 0.2
restart_threshold: 50
acceptance_criterion: "better_or_equal"
```

#### Instancias Grandes (n ≥ 500)
```yaml
max_iterations: 200
local_search_iterations: 50
perturbation_strength: 0.25
restart_threshold: 30
acceptance_criterion: "better_or_equal"
```

---

## Search-Strategy

### Operadores de Búsqueda sobre Coloraciones

#### 1. Construcción Inicial

**Operador Seleccionable**:
- `GreedyDSATUR(graph)` → Solución inicial
- `GreedyLargestFirst(graph)` → Alternativa
- `RLF(graph)` → Alternativa más lenta

**Implementación Conceptual**:
```python
def construct_initial_solution(graph, heuristic="DSATUR"):
    if heuristic == "DSATUR":
        return greedy_dsatur(graph)
    elif heuristic == "LargestFirst":
        return greedy_largest_first(graph)
    else:
        return random_coloring(graph)
```

**Salida**: Coloring inicial factible (usualmente con $k$ > óptimo)

#### 2. Búsqueda Local (Local Search Phase)

**Objetivo**: Mejorar solución actual mediante movimientos locales

**Movimientos disponibles**:
1. **Kempe Chain Exchange**: Intercambiar dos colores mediante cadena
2. **Single Vertex Recolor**: Recolorear un vértice conflictivo
3. **Color Class Merge**: Fusionar dos clases de color y reparar

**Pseudocódigo**:
```python
def local_search(coloring, graph, max_iterations=100):
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        
        for move in generate_moves(coloring, graph):
            coloring_new = apply_move(coloring, move)
            
            if is_feasible(coloring_new) and k_new < k_current:
                coloring = coloring_new
                improved = True
                break  # First improvement
        
        iteration += 1
    
    return coloring, iteration
```

**Estrategia**: First Improvement (aceptar primer movimiento que mejore)

#### 3. Perturbación (Shake Phase)

**Objetivo**: Escapar del óptimo local actual

**Método**: Recolorear aleatoriamente $\lfloor n \times \text{strength} \rfloor$ vértices

**Pseudocódigo**:
```python
def perturbation(coloring, graph, strength=0.2, intensity=1.0):
    """
    strength: Fracción de vértices a perturbar [0, 1]
    intensity: Factor multiplicador de cambios
    """
    coloring_pert = coloring.copy()
    n_verts = len(coloring)
    
    # Número de vértices a perturbar
    n_perturb = int(n_verts * strength * intensity)
    n_perturb = max(1, n_perturb)
    
    # Seleccionar vértices aleatorios
    vertices_to_perturb = random.sample(range(n_verts), n_perturb)
    
    # Recolorear aleatoriamente
    for v in vertices_to_perturb:
        # Asignar color aleatorio (posiblemente inviable)
        new_color = random.randint(1, max(coloring) + 1)
        coloring_pert[v] = new_color
    
    # Reparar conflictos resultantes
    coloring_pert = repair_conflicts(coloring_pert, graph)
    
    return coloring_pert
```

**Intensidad escalable**: En reinicio, usar `intensity > 1.0` para perturbaciones más fuertes

#### 4. Criterio de Aceptación

**Opción 1: Better-or-Equal** (Recomendado para GCP)
```python
def accept_better_or_equal(s_current, s_candidate, best):
    if evaluate(s_candidate) <= evaluate(s_current):
        return True, s_candidate
    else:
        return False, s_current
```
Siempre acepta movimientos que mejoren o igualen la calidad actual.

**Opción 2: Metropolis** (Probabilístico)
```python
def accept_metropolis(s_current, s_candidate, temperature):
    delta = evaluate(s_candidate) - evaluate(s_current)
    
    if delta <= 0:
        return True, s_candidate
    else:
        p_accept = exp(-delta / temperature)
        return random.random() < p_accept, s_candidate if random.random() < p_accept else s_current
```

**Opción 3: Aceptación con Reinicio**
```python
def accept_with_restart(s_current, s_best, iterations_without_improvement):
    if iterations_without_improvement > restart_threshold:
        # Reiniciar desde mejor solución encontrada
        return True, construct_initial_solution()
    else:
        return False, s_current
```

### Estrategia de Terminación

**Criterio de Parada** (Cualquiera que se cumpla primero):

1. **Por iteraciones**: `iterations >= max_iterations`
2. **Por tiempo**: `time_elapsed >= time_limit`
3. **Por convergencia**: `iterations_without_improvement >= restart_threshold * 10`
4. **Por optimalidad**: `k_current == known_optimum` (si disponible)

---

## Performance-Expectations

### Desempeño Esperado por Instancia

#### Pequeñas (n < 100)
```
myciel3:  k_found = 4,  k_opt = 4    gap = 0%
myciel4:  k_found = 5,  k_opt = 5    gap = 0%
myciel5:  k_found = 6,  k_opt = 6    gap = 0%
```
Típicamente encuentra óptimo en < 1 segundo

#### Medianas (100 ≤ n < 500)
```
le450_5a: k_found ~ 5,  k_opt = 5    gap ~ 0-2%
le450_5b: k_found ~ 5,  k_opt = 5    gap ~ 0-2%
```
Típicamente en 5-30 segundos

#### Grandes (n ≥ 500)
```
school1:  k_found ~ 14, k_opt ~ 14   gap ~ 0-5%
miles1000: k_found ~ 10, k_opt ~ 10   gap ~ 0-5%
```
Típicamente en 30-120 segundos con parámetros ajustados

---

## Notas de Implementación

### Operadores Recomendados en Orden de Prioridad

1. **Construcción**: DSATUR (balance entre calidad y velocidad)
2. **Mejora Local**: KempeChain (más efectivo) + OneVertexMove (más rápido)
3. **Perturbación**: RandomRecolor (simple, robusto)
4. **Reparación**: RepairConflicts iterativo

### Sintonización Típica

Para competencia / experimentación:
```yaml
max_iterations: 500
local_search_iterations: 100
perturbation_strength: 0.2
restart_threshold: 50
```

Para validación rápida:
```yaml
max_iterations: 100
local_search_iterations: 30
perturbation_strength: 0.3
restart_threshold: 20
```

### Referencias Implementación

- Lourenço et al. (2003): ILS survey
- Stützle (2010): ILS handbook chapter
- Hertz & de Werra (1987): Tabu search for GCP
- Chiarandini et al. (2005): Metaheuristics benchmarking for GCP
