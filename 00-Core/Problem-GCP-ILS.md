---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: trigger
  last_modified: null
  triggers_update:
    - 01-System/Grammar.md
    - 02-Components/Fitness-Function.md
    - 02-Components/Search-Operators.md
    - 03-Experiments/Experimental-Design.md
    - 04-Generated/scripts/problem.py
    - 04-Generated/scripts/fitness.py
  extraction_rules:
    terminals: "section:Domain-Operators"
    objective: "section:Mathematical-Model"
    constraints: "section:Constraints"
    representation: "section:Solution-Representation"
---

# Problema: Graph Coloring Problem (GCP)

> **🎯 ARCHIVO EDITABLE**: Este archivo es un trigger principal para GCP-ILS-GAA. Al editarlo, se actualizarán automáticamente todos los archivos dependientes.

**Proyecto**: GCP-ILS-GAA  
**Problema**: Graph Coloring Problem (GCP)  
**Versión**: 1.0.0

---

## Problema Seleccionado

**Nombre**: Graph Coloring Problem (GCP)  
**Tipo**: Minimización  
**Categoría**: Combinatorial Optimization - NP-Complete  
**Complejidad**: NP-Hard  
**Referencia**: [Appel1976, Chiarandini2008]

---

## Descripción Informal

El problema de coloración de grafos consiste en asignar colores a los vértices de un grafo de tal manera que ningún par de vértices adyacentes (conectados por una arista) tengan el mismo color, utilizando el **mínimo número de colores posible**.

### Aplicaciones

- **Asignación de frecuencias**: Redes de comunicación inalámbrica
- **Planificación de horarios** (Scheduling): Cursos, exámenes, transportes
- **Asignación de registros**: Compiladores, optimización de código
- **Resolución de Sudokus**: Instancias específicas de coloración
- **Diseño de circuitos VLSI**: Minimización de capas
- **Descomposición de matrices**: Computación científica

---

## Mathematical-Model

### Función Objetivo

```math
\text{Minimizar: } k = \text{número de colores utilizados}
```

donde $k = \max_{i \in V} c_i$ es el número cromático de la solución (máximo color asignado).

### Restricciones

**Restricción de no adyacencia** (Hard Constraint):
```math
c_i \neq c_j, \quad \forall (i,j) \in E
```

donde $(i,j) \in E$ indica que existe arista entre vértices $i$ y $j$.

**Restricción de cobertura**:
```math
c_i \in \{1, 2, \ldots, k\}, \quad \forall i \in V
```

todos los vértices deben estar coloreados con colores válidos.

### Variables de Decisión

- **$c_i$**: Color asignado al vértice $i$ (entero positivo)
- **$k$**: Número cromático de la solución (variable a minimizar)

### Parámetros del Problema

- **$V$**: Conjunto de vértices, $|V| = n$
- **$E$**: Conjunto de aristas, $|E| = m$
- **$n$**: Número de vértices (tamaño del problema)
- **$m$**: Número de aristas (densidad del grafo)
- **$\Delta$**: Grado máximo del grafo
- **$\chi(G)$**: Número cromático óptimo (desconocido en general)

---

## Domain-Operators

### Terminales Constructivos

Operadores que construyen una solución inicial factible (o casi factible):

- **GreedyDSATUR**: Construcción voraz por grado de saturación. Selecciona el vértice con más colores distintos entre sus vecinos y le asigna el menor color disponible. [Brelaz1979]

- **GreedyLargestFirst**: Ordena vértices por grado decreciente y los colorea secuencialmente con el menor color disponible. [Welsh1967]

- **GreedySmallestLast**: Ordena vértices por grado creciente (recursivamente) y los colorea en orden inverso. [Matula1972]

- **RandomSequentialColoring**: Ordena vértices aleatoriamente y asigna el menor color disponible a cada uno. [Johnson1974]

- **RLF** (Recursive Largest First): Coloración recursiva mediante selección de subconjuntos independientes máximos. [Leighton1979]

### Terminales de Mejora Local

Operadores que mejoran una solución existente mediante búsqueda local:

- **KempeChain**: Intercambio de dos colores mediante cadenas de Kempe. Busca un camino alternado de colores A-B en la solución y lo invierte para reducir $k$. [Kempe1879]

- **TabuSearch**: Búsqueda local con memoria tabú. Acepta movimientos que empeoran la solución con penalización decreciente. [Hertz1987]

- **OneVertexMove**: Selecciona un vértice conflictivo (con vecinos del mismo color) y lo recolorea al mejor color disponible. [Galinier1999]

- **SwapColors**: Intercambia dos colores en toda la solución. Útil para reducir $k$ sin crear conflictos. [Fleurent1996]

- **GreedyImprovement**: Itera sobre todos los vértices intentando reducir su color manteniendo factibilidad. [Hertz1987]

### Terminales de Perturbación

Operadores que modifican la solución para escapar de óptimos locales:

- **RandomRecolor**: Recolorea aleatoriamente $p\%$ de los vértices de manera aleatoria. [Chiarandini2005]

- **PartialDestroy**: Destruye la coloración de un subgrafo aleatorio y la reconstruye con constructiva voraz. [Malaguti2008]

- **ColorClassMerge**: Fusiona dos clases de color (todos los vértices de color A toman color B) y repara conflictos. [Avanthay2003]

- **ShakeColors**: Permutación aleatoria de las etiquetas de color en la solución (preserva la estructura, cambia nomenclatura). [Chiarandini2005]

### Terminales de Reparación

Operadores que convierten soluciones infactibles en factibles:

- **RepairConflicts**: Para cada vértice con conflicto (mismo color que vecino), asigna el menor color disponible. [Johnson1991]

- **BacktrackRepair**: Reparación con backtracking limitado. Si un vértice no puede repararse localmente, revierte cambios. [Brelaz1979]

- **IterativeRepair**: Itera hasta eliminar todos los conflictos. Puede aumentar $k$ temporalmente. [Galinier1999]

### Terminales de Intensificación

Operadores que intensifican búsqueda local:

- **ReduceColors**: Intenta reducir $k$ recoloreando vértices de mayor color. Aplica reparación si falla. [Galinier1999]

- **LocalSearchIntensify**: Ejecuta mejora local exhaustiva sobre todos los vértices. [Hertz1987]

---

## Solution-Representation

### Estructura de Datos

**Vector de colores de longitud $n$**:
```python
coloring = [c_0, c_1, c_2, ..., c_{n-1}]
```

donde:
- $c_i \in \{1, 2, ..., k\}$ es el color asignado al vértice $i$
- $k = \max(coloring)$ es el número de colores utilizados
- Índices corresponden a identificadores de vértices (0-indexado)

### Ejemplo Concreto

**Instancia**:
```
Grafo: n=5 vértices
Aristas: {(0,1), (0,2), (1,2), (2,3), (3,4)}
Topología: Camino: 0-1-2-3-4 con triángulo {0,1,2}
```

**Solución**:
```
coloring = [1, 2, 3, 1, 2]

Interpretación:
  Vértice 0 → Color 1
  Vértice 1 → Color 2
  Vértice 2 → Color 3
  Vértice 3 → Color 1
  Vértice 4 → Color 2

Número de colores: k = 3
Conflictos: 0 (FACTIBLE)
```

**Verificación**:
```
Arista (0,1): c_0=1, c_1=2 ✓ (distintos)
Arista (0,2): c_0=1, c_2=3 ✓ (distintos)
Arista (1,2): c_1=2, c_2=3 ✓ (distintos)
Arista (2,3): c_2=3, c_3=1 ✓ (distintos)
Arista (3,4): c_3=1, c_4=2 ✓ (distintos)
```

---

## Constraints

### Restricciones Duras

1. **No adyacencia**: Vértices conectados por arista **deben** tener colores distintos
   - Violación = Conflicto
   - Impacto en factibilidad: Solución infactible

2. **Conectividad**: Todos los vértices **deben** estar coloreados
   - Verificación trivial en representación vectorial

### Restricciones Blandas / Preferencias

- **Minimizar $k$**: Objetivo primario
- **Minimizar conflictos**: Para soluciones parcialmente válidas

### Parámetros del Problema

- **$n$ (Número de vértices)**: Rango 11-1000+ dependiendo instancia
- **$m$ (Número de aristas)**: Densidad varía
- **$\Delta$ (Grado máximo)**: Cota inferior trivial: $\chi(G) \geq \Delta + 1$ para algunos grafos
- **$\chi(G)$ (Número cromático óptimo)**: Desconocido en general, disponible para benchmark

---

## Evaluation-Criteria

### Métrica Primaria

**Función de Aptitud Principal**:
```python
def fitness(coloring, graph):
    """
    Retorna: (calidad, factibilidad)
    """
    k = max(coloring)  # Número de colores utilizados
    conflicts = count_conflicts(coloring, graph.edges)
    
    # Métrica multi-objetivo
    return k, conflicts
```

Interpretación:
- **Menor $k$ es mejor** (objetivo principal)
- **Menor conflictos es mejor** (objetivo secundario)

### Función Objetivo Integrada (Penalización)

Para evaluación única en metaheurística:
```python
def evaluate(coloring, graph, penalty=1000):
    """
    Retorna escalar para optimización
    """
    k = max(coloring)
    conflicts = count_conflicts(coloring, graph.edges)
    
    # Penalización alta a conflictos
    return k + penalty * conflicts
```

**Interpretación**:
- Solución **factible**: $f = k$ (solo número de colores)
- Solución **infactible**: $f = k + 1000 \times \text{conflictos}$ (penalizada)

### Criterio de Comparación

**Menor es mejor**: Se minimiza ambos $k$ y conflictos

### Métricas Adicionales

| Métrica | Descripción | Cálculo |
|---------|-------------|---------|
| **Número cromático** | Número de colores utilizados | $k = \max(\text{coloring})$ |
| **Conflictos** | Pares adyacentes con mismo color | $\text{count_edges}(c_i = c_j)$ |
| **Tasa factibilidad** | % soluciones sin conflictos | $\text{count}(\text{conflictos} = 0) / n$ |
| **Gap a óptimo** | Diferencia a óptimo conocido | $(k_{\text{found}} - k_{\text{opt}}) / k_{\text{opt}}$ |
| **Tiempo de convergencia** | Iteraciones hasta óptima local | $t$ en iteraciones |

---

## Instance-Classes

### Clasificación por Tamaño

| Clase | Rango $n$ | Ejemplos | Características |
|-------|-----------|----------|-----------------|
| **Pequeña** | 11-50 | myciel3-5, queen8-8 | Solubles por optimización exacta |
| **Mediana** | 50-500 | le450_5a-d, queen11-11 | Desafío local search |
| **Grande** | 500+ | school1, miles | Requieren heurísticas eficientes |

### Conjuntos de Datos Disponibles

**Benchmark Standards**:
- **DIMACS**: Formato estándar `.col`
- **Ubicación**: `projects/GCP-ILS/datasets/`
- **Subdirectorios**: MYC, LEI, DSJ, REG, SCH, CUL, SGB

**Formato DIMACS**:
```
p edge <n> <m>
e <v1> <v2>
e <v1> <v3>
...
```

---

## Datos de Instancias Representativas

### Instancias de Prueba

Para experimentación rápida (< 5 minutos):
```
myciel3:  n=11, m=20,  χ=4
myciel4:  n=23, m=71,  χ=5
myciel5:  n=47, m=236, χ=6
```

Para validación (5-30 minutos):
```
le450_5a: n=450, m=5714, χ=5
le450_5b: n=450, m=5734, χ=5
```

Para stress test (> 30 minutos):
```
school1:  n=385, m=19095
miles1000: n=128, m=3040
```

---

## Notas Adicionales

### Propiedades Teóricas

- **Número cromático**: $\chi(G) \leq \Delta(G) + 1$ (Teorema de Brooks)
- **Cota inferior**: $\chi(G) \geq |V| / \alpha(G)$ donde $\alpha(G)$ es independencia máxima
- **Heurística greedy**: Proporciona cota $\chi \leq \Delta + 1$

### Desafíos Computacionales

1. **Espacio de búsqueda exponencial**: $O(k^n)$ coloraciones posibles
2. **No existe estructura gradiente**: Pequeños cambios pueden crear cascadas de conflictos
3. **Falta de optimalidad local**: Muchas soluciones con $k = \chi + 1$ (una encima del óptimo)

### Referencias Clave

- Appel & Haken (1976): Teorema de los 4 colores
- Brelaz (1979): DSATUR algorithm
- Chiarandini et al. (2005): Metaheurísticas para GCP
- Hertz & de Werra (1987): Tabu search para GCP
- Malaguti et al. (2008): Survey sobre métodos de resolución
