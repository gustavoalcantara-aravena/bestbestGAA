---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: specification
  last_modified: null
  depends_on:
    - 01-System/Grammar.md
    - 01-System/AST-Nodes.md
  triggers_update:
    - 04-Generated/scripts/ils_search.py
  extraction_rules:
    mutation_types: "section:Mutation-Operators"
    local_search: "section:Local-Search-Phase"
    perturbation: "section:Perturbation-Phase"
---

# Operadores de Búsqueda para Configuraciones ILS

> **Especificación de operadores de variación que modifican configuraciones de algoritmos**

**Proyecto**: GCP-ILS-GAA  
**Basado en**: Grammar.md, AST-Nodes.md  
**Versión**: 1.0.0

---

## ⚠️ ACLARACIÓN IMPORTANTE: Esto NO es Algoritmo Genético

**Este documento especifica operadores de PERTURBACIÓN en ILS, NO reproducción genética.**

| Concepto | En GA | En ILS (Este Proyecto) |
|----------|-------|--------------------------|
| **"Mutación"** | Cambio en cromosoma de población | Perturbación de UNA solución (escape) |
| **Propósito** | Mantener diversidad genética | Escapar óptimo local |
| **Contexto** | Múltiples soluciones evolucionan | Una solución se refina iterativamente |
| **Recombinación** | Sí (crossover) | NO |
| **Generaciones** | Sí | NO (iteraciones) |

**Nota**: En ILS, "mutación" = "perturbación" = "cambio aleatorio para escape"  
**No hay**: Población, crossover, selección natural ni genes.

---

---

## Propósito

Este documento especifica los operadores de búsqueda en el **ciclo ILS**:

```
ILS Loop:
├─ Búsqueda Local: Mejora parámetros actuales
├─ Mutación/Perturbación: Escapa óptimo local ← ESTE DOCUMENTO
├─ Aceptación: Decide si mantener cambio
└─ Iteración: Repite 500 veces
```

Estos operadores actúan sobre **una única solución** (AST configuración):

1. **Mutación Constructiva**: Cambia operador inicial
2. **Mutación de LS Operator**: Cambia operador de búsqueda local
3. **Mutación de Perturbación**: Cambia operador de perturbación
4. **Mutación de Parámetros**: Ajusta valores numéricos
5. **Mutación de Estructura**: Agrega/elimina fases

**Nota**: Estas mutaciones NO son reproducción genética. Son perturbaciones simples para escapar óptimos locales en una solución única que evoluciona iterativamente.

---

## Mutation-Operators (Perturbación en ILS)

### Tipos de Mutación / Perturbación

⚠️ **En contexto ILS**: "Mutación" = "Perturbación" = "Cambio aleatorio en la solución actual para escape".

**NO es** reproducción genética como en GA.  
**ES** un operador de escape para la búsqueda local.

Las mutaciones cambian aspectos específicos de una configuración con probabilidades controladas:

#### 1. Mutación de Constructiva

**Qué cambia**: El operador de construcción inicial

**Cómo funciona**:
```
ANTES: InitPhase: DSATUR
DESPUÉS: InitPhase: LargestFirst
```

**Terminales disponibles**:
- DSATUR (grado de saturación)
- LargestFirst (grado decreciente)
- SmallestLast (grado creciente)
- RandomSequential (orden aleatorio)
- RLF (Recursive Largest First)

**Probabilidad**: 0.20

**Código**:
```python
def mutate_constructive(config: Configuration) -> Configuration:
    mutated = config.copy()
    new_constructive = random.choice([
        DSATURNode(), LargestFirstNode(), SmallestLastNode(),
        RandomSequentialNode(), RLFNode()
    ])
    mutated.ast.init_phase.constructive = new_constructive
    return mutated
```

**Impacto en fitness**: ALTO
- Diferentes constructivas tienen diferentes propiedades
- DSATUR tiende a ser mejor pero más lento
- RandomSequential es rápido pero de baja calidad

---

#### 2. Mutación de Operador de Búsqueda Local

**Qué cambia**: Los operadores aplicados en fases de búsqueda local

**Cómo funciona**:
```
ANTES: LocalSearchPhase: [KempeChain(100)]
DESPUÉS: LocalSearchPhase: [TabuSearch(100)]
```

**Terminales disponibles**:
- KempeChain: Intercambio de colores via cadenas
- TabuSearch: Búsqueda tabú
- SingleVertexMove: Recolor de un vértice
- ColorClassMerge: Fusión de clases de color
- SwapColors: Intercambio de dos colores

**Probabilidad**: 0.20

**Código**:
```python
def mutate_ls_operator(config: Configuration) -> Configuration:
    mutated = config.copy()
    new_ls = random.choice([
        KempeChainNode(), TabuSearchNode(),
        SingleVertexMoveNode(), ColorClassMergeNode(),
        SwapColorsNode()
    ])
    for phase in mutated.ast.search_phases:
        if isinstance(phase, LocalSearchPhaseNode) and phase.operators:
            idx = random.randint(0, len(phase.operators) - 1)
            phase.operators[idx] = new_ls.copy()
    return mutated
```

**Impacto en fitness**: ALTO
- KempeChain: Excelente calidad, moderada velocidad
- TabuSearch: Muy buena calidad, más lento
- SingleVertexMove: Rápido, calidad moderada

---

#### 3. Mutación de Operador de Perturbación

**Qué cambia**: El operador usado para perturbar la solución

**Cómo funciona**:
```
ANTES: Perturbation: RandomRecolor(0.20)
DESPUÉS: Perturbation: PartialDestroy(0.25)
```

**Terminales disponibles**:
- RandomRecolor: Recoloración aleatoria
- PartialDestroy: Destrucción y reconstrucción
- ShakeColors: Permutación de colores

**Probabilidad**: 0.20

**Código**:
```python
def mutate_perturbation(config: Configuration) -> Configuration:
    mutated = config.copy()
    new_pert = random.choice([
        RandomRecolorNode(), PartialDestroyNode(),
        ShakeColorsNode()
    ])
    for phase in mutated.ast.search_phases:
        if isinstance(phase, PerturbationPhaseNode):
            phase.operator = new_pert.copy()
    return mutated
```

**Impacto en fitness**: MEDIO
- RandomRecolor: Perturbación controlada
- PartialDestroy: Fuerte, requiere búsqueda local posterior
- ShakeColors: Muy fuerte, puede romper buenos óptimos

---

#### 4. Mutación de Parámetros

**Qué cambia**: Valores numéricos de parámetros

**Parámetros mutables**:

##### max_iterations (para operadores LS)

**Rango**: [50, 100, 200, 500]

**Cambio**: Seleccionar nuevo valor aleatorio

```python
# ANTES: KempeChain(max_iterations=100)
# DESPUÉS: KempeChain(max_iterations=200)
```

**Impacto**: 
- Aumentar: Mejor calidad, más lento
- Disminuir: Más rápido, calidad inferior

##### strength (para operadores de perturbación)

**Rango**: [0.1, 0.5] continuo

**Cambio**: Perturbación ±5% sobre valor actual

```python
# ANTES: RandomRecolor(strength=0.20)
# DESPUÉS: RandomRecolor(strength=0.23)
```

**Impacto**:
- Aumentar: Mayor escape de óptimos locales
- Disminuir: Menos destructivo, mejor preservación

##### tabu_tenure (para TabuSearch)

**Rango**: [5, 10, 20]

**Cambio**: Seleccionar nuevo valor

**Impacto**:
- Aumentar: Más diversificación
- Disminuir: Más intensificación

**Probabilidad global de mutación de parámetro**: 0.20

---

#### 5. Mutación de Estructura

**Qué cambia**: Número y orden de fases de búsqueda

**Operaciones**:

##### Inserción de Fase

```
ANTES: [LS(KempeChain), Pert(RandomRecolor), LS(KempeChain)]
DESPUÉS: [LS(KempeChain), Pert(RandomRecolor), LS(TabuSearch), LS(KempeChain)]
```

**Restricción**: Máximo 5 fases (por complejidad)

**Probabilidad**: 0.10

##### Eliminación de Fase

```
ANTES: [LS(KempeChain), Pert(RandomRecolor), LS(KempeChain)]
DESPUÉS: [LS(KempeChain), LS(KempeChain)]
```

**Restricción**: Mínimo 1 fase (ya hay inicialización)

**Probabilidad**: 0.10

**Código**:
```python
def mutate_structure(config: Configuration) -> Configuration:
    mutated = config.copy()
    
    if random.random() < 0.5 and len(mutated.ast.search_phases) < 5:
        # Insert phase
        new_phase = random.choice([
            LocalSearchPhaseNode([random.choice(LS_OPERATORS)]),
            PerturbationPhaseNode(random.choice(PERT_OPERATORS))
        ])
        position = random.randint(0, len(mutated.ast.search_phases))
        mutated.ast.search_phases.insert(position, new_phase)
    
    elif random.random() < 0.5 and len(mutated.ast.search_phases) > 1:
        # Remove phase
        position = random.randint(0, len(mutated.ast.search_phases) - 1)
        mutated.ast.search_phases.pop(position)
    
    return mutated
```

**Impacto en fitness**: MEDIO
- Insertar LS: Usualmente mejora calidad
- Insertar Pert: Aumenta diversificación
- Eliminar: Reduce complejidad, puede perjudicar

---

### Mutación Combinada (Perturbación)

En ILS, la **perturbación** aplica múltiples mutaciones simultáneamente para escape:

**Fuerza de perturbación** (strength ∈ [0.1, 0.5]):

```python
def apply_random_mutation(config, strength=0.20):
    """
    Aplicar mutaciones aleatorias con intensidad dada.
    
    strength: fracción de tipos de mutación a aplicar
    """
    mutations = [
        mutate_constructive,
        mutate_ls_operator,
        mutate_perturbation,
        mutate_parameter,
        mutate_structure
    ]
    
    num_mutations = max(1, int(len(mutations) * strength))
    selected = random.sample(mutations, num_mutations)
    
    for mutation in selected:
        config = mutation(config)
    
    return config
```

**Ejemplos**:

| strength | Mutaciones | Escape | Efectividad |
|----------|-----------|--------|-------------|
| 0.10 | 0-1 mutaciones | Débil | Conservador |
| 0.20 | 1 mutación | Moderado | Balanceado (recomendado) |
| 0.40 | 2 mutaciones | Fuerte | Exploratorio |
| 0.60 | 3 mutaciones | Muy fuerte | Radical |

---

## Local-Search-Phase

### Búsqueda Local sobre Configuraciones

La **búsqueda local** en el espacio de configuraciones es **parameter tuning**: pequeñas mejoras a parámetros.

### Estrategia: Variable Neighborhood Descent (VND)

```python
def parameter_tuning(config, max_moves=10, max_no_improve=3):
    """
    Búsqueda local: ajustar parámetros de configuración.
    
    Itera intentando mejorar mediante cambios pequeños.
    """
    current = config.copy()
    improvements = 0
    no_improve = 0
    
    for move in range(max_moves):
        if no_improve >= max_no_improve:
            break
        
        # Generar vecino por cambio pequeño de parámetro
        neighbor = generate_neighbor(current)
        neighbor_fitness = evaluate(neighbor)
        
        if neighbor_fitness < current_fitness:
            current = neighbor
            improvements += 1
            no_improve = 0
        else:
            no_improve += 1
    
    return current, improvements
```

### Movimientos de Búsqueda Local

#### Movimiento 1: Ajuste Fine de max_iterations

**Rango de cambio**: ±10% del valor actual

```
ANTES: KempeChain(max_iterations=100)
DESPUÉS: KempeChain(max_iterations=110)
         (100 * 1.10 = 110)
```

**Criterio de aceptación**: First improvement

**Impacto**: Pequeña ganancia de calidad vs tiempo

---

#### Movimiento 2: Ajuste Fine de strength

**Rango de cambio**: ±0.05

```
ANTES: RandomRecolor(strength=0.20)
DESPUÉS: RandomRecolor(strength=0.23)
         (0.20 + 0.03 aleatorio)
```

**Criterio de aceptación**: First improvement

---

#### Movimiento 3: Ajuste de tabu_tenure

**Rango de cambio**: ±3

```
ANTES: TabuSearch(tabu_tenure=10)
DESPUÉS: TabuSearch(tabu_tenure=13)
```

**Impacto**: Balance exploración-explotación

---

### Configuración de Búsqueda Local

```yaml
# ILS local search phase
enable_local_search: true
ls_max_moves: 10           # Máximo de intentos de mejora
ls_max_no_improve: 3       # Parar si 3 intentos sin mejora
```

**Complejidad**: O(10 × evaluaciones_por_configuración)

---

## Perturbation-Phase

### Perturbación en ILS para Configuraciones

Mientras que **mutación es aleatoria uniforme**, la **perturbación** es sistemática y fuerte:

### Estrategia: Perturbación Múltiple

```python
def perturb(config, strength=0.20):
    """
    Perturbar para escape de óptimos locales.
    """
    return apply_random_mutation(config, strength=strength)
```

### Fases de ILS

**ILS tiene estructura clara**:

```
1. s = InitConfiguration()        # Crear aleatoria o referencia
2. s = LocalSearch(s)             # Mejorar (parameter tuning)
3. s_best = s
4. while not terminated:
     4.1. s_pert = Perturb(s)     # Escape
     4.2. s_new = LocalSearch(s_pert)  # Mejorar
     4.3. if Accept(s_new, s):
            s = s_new
     4.4. if f(s_new) < f(s_best):
            s_best = s_new
5. return s_best
```

### Parámetros de Perturbación

**Fuerza (strength)**: 0.20 (recomendado)
- Cambia ~1 tipo de operador
- Balance entre exploración y explotación
- Empirically tuned para GCP-ILS

**Criterio de aceptación**: "better_or_equal"
- Acepta mejoras
- Acepta soluciones iguales (permite plateaus)
- Rechaza empeoramientos

---

## Comparación de Operadores

### Impacto en Búsqueda

| Operador | Tipo | Exploración | Explotación | Eficacia |
|----------|------|------------|-------------|----------|
| mutate_constructive | Exploración | MUY ALTA | Baja | MEDIA |
| mutate_ls_operator | Exploración | ALTA | Baja | ALTA |
| mutate_perturbation | Exploración | ALTA | Baja | MEDIA |
| mutate_parameter | Explotación | Baja | ALTA | MEDIA |
| mutate_structure | Exploración | MEDIA | MEDIA | BAJA |

### Costo Computacional

| Operador | Evaluaciones requeridas | Tiempo estimado |
|----------|----------------------|-----------------|
| mutate_constructive | 1 | ~45s |
| mutate_ls_operator | 1 | ~45s |
| mutate_parameter | 1-2 | ~45-90s |
| Local search (5 movimientos) | 5 | ~225s |
| Perturbación | 1 | ~45s |

---

## Configuración Recomendada

```yaml
# Operators configuration
mutation_rate: 0.40                # Aplicar mutación con probabilidad 0.4

perturbation_strength: 0.20        # Fuerza de perturbación
perturbation_type: "mutation"      # Usar mutación para perturbar

# Local search settings
enable_local_search: true
ls_max_moves: 10                   # Intentos de mejora por configuración
ls_max_no_improve: 3               # Parar si 3 sin mejora

# ILS acceptance criterion
acceptance_criterion: "better_or_equal"  # Permite plateaus

# Termination
max_iterations: 500                # Iteraciones principales de ILS
max_no_improve_iterations: 50      # Parar si 50 sin mejora global
```

---

## Ejemplos de Evolución

### Ejemplo 1: Búsqueda Exitosa

```
Iter 0: config=[DSATUR, LS(Kempe), Pert(Random)]
        fitness=4.50
        
Iter 1: MUTATE_LS_OPERATOR
        config=[DSATUR, LS(Tabu), Pert(Random)]
        fitness=4.25  ✓ MEJORÓ
        
Iter 2: LOCAL_SEARCH (parameter tuning)
        config=[DSATUR, LS(Tabu,iter=110), Pert(Random)]
        fitness=4.20  ✓ MEJORÓ
        
Iter 3: PERTURB
        config=[LargestFirst, LS(Tabu), Pert(Destroy)]
        fitness=4.80  ✗ EMPEORÓ (aceptado para escape)
        
Iter 4: LOCAL_SEARCH (parameter tuning)
        config=[LargestFirst, LS(Tabu,iter=120), Pert(Destroy)]
        fitness=4.15  ✓✓ NUEVA MEJOR
```

### Ejemplo 2: Escape de Óptimo Local

```
Iter 10: local optimum
         config=[DSATUR, LS(Kempe), Pert(Random)]
         fitness=4.10 (no mejora en últimas 10 iteraciones)
         
Iter 11: PERTURB (strength=0.40, 2 mutaciones)
         MUTATE_CONSTRUCTIVE: DSATUR → SmallestLast
         MUTATE_PERTURBATION: Random → PartialDestroy
         
         config=[SmallestLast, LS(Kempe), Pert(Destroy)]
         fitness=4.50  ✗ EMPEORADO
         Pero ACEPTADO por escape
         
Iter 12: LOCAL_SEARCH
         config=[SmallestLast, LS(Tabu,iter=150), Pert(Destroy)]
         fitness=3.95  ✓✓✓ NUEVO MEJOR
```

---

## Referencias

- Lourenço, H., Martin, O., & Stützle, T. (2003). Iterated Local Search. Handbook of Metaheuristics.
- Hertz, A., & de Werra, D. (1987). Using tabu search techniques for graph coloring.
- Galinier, P., & Hao, J. K. (1999). Hybrid evolutionary algorithms for graph coloring.

---

**Próximo paso**: Implementación en `04-Generated/scripts/ils_search.py`
