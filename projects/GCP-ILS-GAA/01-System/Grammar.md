---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: trigger
  last_modified: null
  triggers_update:
    - 01-System/AST-Nodes.md
    - 02-Components/Search-Operators.md
    - 04-Generated/scripts/ast_nodes.py
    - 04-Generated/scripts/genetic_algorithm.py
  extraction_rules:
    terminals: "section:Terminal-Definitions"
    rules: "section:Syntax-Rules"
---

# Gramática de AST para GCP-ILS-GAA

> **🎯 ARCHIVO EDITABLE**: Define la sintaxis y semántica de algoritmos válidos para GCP.

**Proyecto**: GCP-ILS-GAA  
**Versión**: 1.0.0  

---

## Propósito

Esta gramática define:
- **Qué algoritmos son válidos** (sintaxis)
- **Cómo combinar operadores** (composición)
- **Restricciones y dependencias** entre operadores
- **Espacio de búsqueda** para Genetic Programming

El objetivo es que Genetic Programming **genere automáticamente** diferentes algoritmos y encuentre el **óptimo** para GCP.

---

## Sintaxis-Reglas (BNF)

### Regla Principal

```ebnf
<Algorithm> ::= <InitPhase> <SearchPhase> <TerminationCondition>

<InitPhase> ::= "INIT:" <ConstructiveHeuristic>

<SearchPhase> ::= "SEARCH:" (<LocalSearchPhase>)+ (<PerturbationPhase> <LocalSearchPhase>)*

<LocalSearchPhase> ::= "LS[" <LocalSearchOperator> ("|" <LocalSearchOperator>)* "]"

<PerturbationPhase> ::= "PERT[" <PerturbationOperator> ("|" <PerturbationOperator>)* "]"

<TerminationCondition> ::= "TERM:" ("MAX_ITER" | "TIME_LIMIT" | "NO_IMPROVEMENT" | "OPTIMAL")

<AcceptanceCriterion> ::= "ACCEPT:" ("BETTER_OR_EQUAL" | "METROPOLIS" | "FIRST_IMPROVEMENT")
```

---

## Terminal-Definitions

### Constructivas (Solución Inicial)

**Categoría**: Heurísticas de construcción  
**Rol**: Generar solución inicial factible  
**Cardinality**: Exactamente 1 en `InitPhase`

```
Constructives = {
  DSATUR              # Grado de saturación voraz
  LargestFirst        # Ordenar por grado decreciente
  SmallestLast        # Ordenar por grado creciente (recursivo)
  RandomSequential    # Orden aleatorio
  RLF                 # Recursive Largest First
}
```

### Mejora Local (Local Search)

**Categoría**: Operadores de intensificación  
**Rol**: Mejorar solución actual sin cambiar significativamente  
**Cardinality**: Al menos 1 en `LocalSearchPhase`

```
LocalSearchOperators = {
  KempeChain          # Intercambio de 2 colores via cadenas
  SingleVertexMove    # Recolorear 1 vértice conflictivo
  ColorClassMerge     # Fusionar dos clases de color
  TabuSearch          # Búsqueda local con memoria tabú
  SwapColors          # Intercambiar 2 colores directamente
}
```

### Perturbación (Diversificación)

**Categoría**: Operadores de diversificación  
**Rol**: Escapar de óptimos locales modificando solución  
**Cardinality**: 0 o más en `PerturbationPhase`

```
PerturbationOperators = {
  RandomRecolor       # Recolorear p% de vértices aleatoriamente
  PartialDestroy      # Destruir y reconstruir subgrafo
  ColorClassMerge     # Fusionar clases y reparar
  ShakeColors         # Permutación de colores
}
```

### Reparación (Mantenimiento de Factibilidad)

**Categoría**: Operadores de reparación implícita  
**Rol**: Convertir solución infactible en factible  
**Cardinality**: Automática después de perturbación

```
RepairOperators = {
  RepairConflicts     # Iterar hasta eliminar conflictos
  BacktrackRepair     # Reparación con backtracking limitado
  IterativeRepair     # Reparación iterativa
}
```

---

## Restricted-Grammar

### Reglas de Validez

**R1: Estructura Mínima**
```
Toda Algorithm válida DEBE tener:
- InitPhase con exactamente 1 Constructive
- SearchPhase con al menos 1 LocalSearchOperator
- TerminationCondition especificada
```

**R2: Composición de LocalSearch**
```
LocalSearchPhase puede contener:
- 1 operador: LS[KempeChain]
- Múltiples: LS[KempeChain | SingleVertexMove] (se aplican secuencialmente)
- Máximo 3 operadores por fase para eficiencia
```

**R3: Composición de Perturbación**
```
PerturbationPhase es OPCIONAL pero si existe:
- Máximo 1 operador de perturbación por fase
- Debe haber al menos 1 LocalSearchPhase después
- Patrón típico: PERT -> LS -> PERT -> LS
```

**R4: Aceptación**
```
Criterion de aceptación se aplica después de cada búsqueda local
- BETTER_OR_EQUAL: aceptar si mejora o iguala
- METROPOLIS: probabilístico con temperatura
- FIRST_IMPROVEMENT: aceptar primer movimiento que mejore
```

**R5: Restricciones de Compatibilidad**
```
NO permitido:
- 2 operadores de la misma categoría en una fase (ej: LS[KempeChain | KempeChain])
- Perturbación sin LocalSearch posterior
- Más de 5 fases de búsqueda (complejidad)
```

---

## Ejemplos-Válidos

### Ejemplo 1: ILS Clásico
```
INIT: DSATUR
SEARCH:
  LS[KempeChain]
  PERT[RandomRecolor]
  LS[KempeChain]
TERM: MAX_ITER=500
ACCEPT: BETTER_OR_EQUAL
```

**Interpretación**:
1. Construir solución inicial con DSATUR
2. Mejorar con Kempe chains
3. Perturbar aleatoriamente
4. Mejorar de nuevo con Kempe
5. Aceptar si mejora o iguala
6. Repetir hasta 500 iteraciones

### Ejemplo 2: Búsqueda Local Intensiva
```
INIT: LargestFirst
SEARCH:
  LS[KempeChain | SingleVertexMove]
  LS[KempeChain | SingleVertexMove]
TERM: NO_IMPROVEMENT=100
ACCEPT: BETTER_OR_EQUAL
```

**Interpretación**:
1. Construir con LargestFirst
2. Aplicar Kempe AND SingleVertex secuencialmente
3. Repetir intensivamente
4. Parar si no hay mejora en 100 iteraciones

### Ejemplo 3: Perturbación Variable
```
INIT: DSATUR
SEARCH:
  LS[KempeChain]
  PERT[RandomRecolor]
  LS[SingleVertexMove]
  PERT[PartialDestroy]
  LS[KempeChain | SingleVertexMove]
TERM: MAX_ITER=1000
ACCEPT: METROPOLIS
```

**Interpretación**:
1. Construcción DSATUR
2. Mejora → Perturbación ligera → Mejora simple
3. Perturbación fuerte → Mejora combinada
4. Aceptación probabilística

### Ejemplo 4: Random Restart
```
INIT: RandomSequential
SEARCH:
  LS[KempeChain]
  PERT[RandomRecolor]
  LS[KempeChain]
TERM: NO_IMPROVEMENT=50
ACCEPT: BETTER_OR_EQUAL
```

**Interpretación**:
1. Construcción aleatoria (para diversidad)
2. Ciclo: Mejora → Perturbación → Mejora
3. Reinicio cuando no hay mejora

---

## Type-System

### Operador Genérico

```
class OperatorSignature:
  Input: [Coloring, Graph]
  Output: Coloring
  Parameters: Dict[str, float]
  Deterministic: bool
  TimeComplexity: str
```

### Constructive

```
Input: Graph
Output: Coloring (factible)
Parameters: {}
Deterministic: bool (DSATUR sí, Random no)
TimeComplexity: O(n²) a O(n³)
```

### LocalSearchOperator

```
Input: [Coloring, Graph]
Output: Coloring (igual o mejor)
Parameters: {max_iterations: int}
Deterministic: bool (Kempe sí, pero orden no)
TimeComplexity: O(k² * iterations)
```

### PerturbationOperator

```
Input: [Coloring, Graph, strength: float]
Output: Coloring (puede ser infactible)
Parameters: {strength: float ∈ [0.1, 0.9]}
Deterministic: false
TimeComplexity: O(n)
```

---

## Espacio-de-Búsqueda

### Dimensionalidad

```
Constructivas:        5 opciones
LocalSearch combos:   C(5,1) + C(5,2) + C(5,3) = 25 combinaciones
Perturbación:         4 + 1 (ninguna) = 5 opciones
Estructura:           2^3 = 8 patrones (1-3 ciclos LS-PERT)
Aceptación:           3 opciones
Terminación:          4 opciones

Total aproximado: 5 × 25 × 5 × 8 × 3 × 4 ≈ 120,000 algoritmos posibles
```

### Distribución

- **Algoritmos simples** (5-10 operadores): ~10%
- **Algoritmos medianos** (11-20 operadores): ~70%
- **Algoritmos complejos** (21+ operadores): ~20%

---

## Restricted-Search-Space

Para **Genetic Programming**, limitar búsqueda a:

```yaml
constraints:
  max_operations_per_algorithm: 10
  max_local_search_operators: 2
  max_perturbation_phases: 3
  required_components:
    - exactly_one_constructive
    - at_least_one_local_search
    - termination_condition
    - acceptance_criterion
  
  forbidden_patterns:
    - two_identical_operators_in_phase
    - perturbation_without_following_ls
    - termination_without_max_iter_or_time
```

---

## Evolución-de-ASTs

### Operadores Genéticos

**Mutación**: Cambiar un operador por otro
```
Antes: INIT: DSATUR / LS[KempeChain] / PERT[Random] / ...
Mutación: Cambiar DSATUR → LargestFirst
Después: INIT: LargestFirst / LS[KempeChain] / PERT[Random] / ...
```

**Crossover**: Intercambiar subfases entre 2 algoritmos
```
Parent1: INIT: DSATUR / LS[Kempe] / PERT[Random] / LS[Kempe]
Parent2: INIT: LF / LS[SingleVertex] / PERT[Partial] / LS[SingleVertex]
Child1: INIT: DSATUR / LS[SingleVertex] / PERT[Partial] / LS[SingleVertex]
Child2: INIT: LF / LS[Kempe] / PERT[Random] / LS[Kempe]
```

**Inserción**: Agregar nueva fase
```
Antes: INIT / LS / PERT / LS
Después: INIT / LS / PERT / LS / PERT / LS
```

**Eliminación**: Eliminar fase redundante
```
Antes: INIT / LS / LS / PERT / LS
Después: INIT / LS / PERT / LS
```

---

## Fitness-Function-para-ASTs

Un AST se evalúa ejecutándolo en **múltiples instancias** de GCP:

```python
fitness(ast) = (
    avg_solution_quality,      # Menor k es mejor
    -avg_execution_time,       # Menor tiempo es mejor
    feasibility_rate,          # Más soluciones factibles
    convergence_speed,         # Converger rápido
    robustness                 # Consistencia entre réplicas
)
```

**Evaluación Multi-Criterio**: Pareto frontera

```
Objetivo 1: Minimizar k (calidad)
Objetivo 2: Minimizar tiempo (velocidad)
Objetivo 3: Maximizar factibilidad
```

---

## Referencias-Teoría-GAA

Esta gramática implementa los conceptos de:
- **Genetic Programming** (Koza 1992)
- **Hyperheuristics** (Burke & Bykov 2017)
- **Algorithm Schema** (Pisinger & Toth 2005)
- **MetaAlgorithms** (Wolpert & Macready 1997)

El objetivo final es **encontrar automáticamente** el **mejor algoritmo** para GCP dentro del espacio definido por esta gramática.
