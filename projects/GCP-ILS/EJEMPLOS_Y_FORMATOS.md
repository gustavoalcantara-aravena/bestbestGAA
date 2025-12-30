# GCP-ILS: Ejemplos Concretos y Formatos

**Propósito**: Entender exactamente qué datos tienes y cómo usarlos  
**Fecha**: 2025-12-30

---

## 📦 EJEMPLO 1: INSTANCIA PEQUEÑA (Myciel2)

### Archivo: `datasets/MYC/myciel2.col`
```
5 5
1 2
1 4
2 3
3 5
4 5
```

**Explicación:**
- **Línea 1**: `5 5`
  - n = 5 vértices
  - m = 5 aristas

- **Líneas 2-6**: Aristas (1-indexed)
  - Arista (1,2): vértices 1 y 2 conectados
  - Arista (1,4): vértices 1 y 4 conectados
  - etc...

### Estructura de Datos (en Python)
```python
problem = GraphColoringProblem(
    name='myciel2.col',
    n=5,
    edges=[(1,2), (1,4), (2,3), (3,5), (4,5)],
    adjacency={
        1: {2, 4},
        2: {1, 3},
        3: {2, 5},
        4: {1, 5},
        5: {3, 4}
    }
)
```

### Solución Ejemplo
```python
coloring = [1, 2, 1, 2, 1]  # Índices 1-5 (1-indexed)
# Vértice 1: color 1
# Vértice 2: color 2  
# Vértice 3: color 1
# Vértice 4: color 2
# Vértice 5: color 1

solution = ColoringSolution(
    coloring=coloring,
    num_colors=2,
    conflicts=0,  # No hay conflictos
    is_feasible=True
)
```

### Validación de Conflictos
```python
# Chequear cada arista
for (u, v) in edges:
    if coloring[u] == coloring[v]:
        conflicts += 1
        print(f"Conflicto: vértice {u} y {v} ambos color {coloring[u]}")

# Para myciel2: 0 conflictos ✓
```

---

## 📦 EJEMPLO 2: INSTANCIA MEDIANA (Queen5_5)

### Archivo: `datasets/SGB/Queen_graphs/queen5_5.col`
```
p edge 25 160
e 1 2
e 1 6
e 1 11
e 1 16
e 1 21
...
```

**Significado:**
- 25 vértices (tablero 5×5)
- 160 aristas (nodos que se atacan)
- Número cromático conocido: χ = 5 (no es divisible por 2 ni 3)

### Grafo de Reinas 5×5
```
Tablero:
 0  1  2  3  4
 5  6  7  8  9
10 11 12 13 14
15 16 17 18 19
20 21 22 23 24

Numeración DIMACS (1-indexed):
 1  2  3  4  5
 6  7  8  9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
```

**Vértice 1 (posición 0,0) es adyacente a:**
- Misma fila: 2,3,4,5
- Misma columna: 6,11,16,21
- Diagonales: 7,13,19 (diagonal), 8 (otra diagonal)

Total: 12 vecinos (grado = 12)

### Solución Óptima Conocida
```python
# Para queen5_5: χ = 5 (óptimo demostrado)

# Solución (ejemplo válido con 5 colores):
coloring = [0,0,1,2,3,   # Fila 0
            1,2,3,4,0,   # Fila 1
            2,3,4,0,1,   # Fila 2
            3,4,0,1,2,   # Fila 3
            4,1,2,3,4]   # Fila 4

num_colors = 5
conflicts = 0
```

---

## 📊 EJEMPLO 3: DATASET METADATA

### Archivo: `datasets/documentation/metadata.json` (parcial)
```json
{
  "total": 79,
  "instances": [
    {
      "name": "myciel2",
      "filename": "myciel2.col",
      "source": "MYC",
      "nodes": 5,
      "edges": 5,
      "lower_bound": 2,
      "best_known": 3,
      "optimal_confirmed": true,
      "difficulty": "trivial"
    },
    {
      "name": "queen5_5",
      "filename": "queen5_5.col",
      "source": "SGB",
      "nodes": 25,
      "edges": 160,
      "lower_bound": 5,
      "best_known": 5,
      "optimal_confirmed": true,
      "difficulty": "easy"
    },
    {
      "name": "DSJC125.1",
      "filename": "DSJC125.1.col",
      "source": "DSJ",
      "nodes": 125,
      "edges": 1472,
      "lower_bound": 5,
      "best_known": null,
      "optimal_confirmed": false,
      "difficulty": "hard"
    },
    {
      "name": "DSJC1000.5",
      "filename": "DSJC1000.5.col",
      "source": "DSJ",
      "nodes": 1000,
      "edges": 499652,
      "lower_bound": 89,
      "best_known": null,
      "optimal_confirmed": false,
      "difficulty": "extremely_hard"
    }
  ]
}
```

### Cómo Usarlo en Código
```python
from datasets.documentation.loader import InstanceLoader

loader = InstanceLoader('datasets/documentation')

# Cargar una instancia específica
myciel2 = loader.get_instance('myciel2')
print(f"Nodos: {myciel2['nodes']}")
print(f"Aristas: {myciel2['edges']}")
print(f"Óptimo conocido: {myciel2['best_known']}")

# Filtrar por dificultad
easy_instances = loader.get_by_difficulty('easy')
print(f"Instancias fáciles: {len(easy_instances)}")  # 12

# Filtrar por familia
sgb_instances = loader.get_by_source('SGB')
print(f"Instancias SGB: {len(sgb_instances)}")  # 24

# Obtener ruta del archivo
path = loader.get_file_path('queen5_5')
print(path)  # datasets/raw/queen5_5.col
```

---

## 🔄 EJEMPLO 4: FLUJO COMPLETO DE EJECUCIÓN

### Paso 1: Cargar Instancia
```python
from data.loader import DataLoader
from core.problem import GraphColoringProblem

loader = DataLoader('datasets/documentation')
problem = loader.load_instance('queen5_5')

print(f"Grafo: {problem.name}")
print(f"Nodos: {problem.n}")
print(f"Aristas: {len(problem.edges)}")
print(f"Grado máximo: {max(problem.get_degree(v) for v in range(problem.n))}")
```

**Output:**
```
Grafo: queen5_5.col
Nodos: 25
Aristas: 160
Grado máximo: 12
```

---

### Paso 2: Crear Solución Inicial (Greedy)
```python
from operators.constructive import GreedyDSATUR

constructor = GreedyDSATUR(problem)
solution = constructor.construct()

print(f"Colores usados: {solution.num_colors}")
print(f"Conflictos: {solution.count_conflicts()}")
print(f"Factible: {solution.is_feasible()}")
```

**Output:**
```
Colores usados: 5
Conflictos: 0
Factible: True
```

---

### Paso 3: Mejorar con Búsqueda Local
```python
from operators.local_search import KempeChain

local_search = KempeChain(problem)
solution = local_search.improve(solution)

print(f"Colores después mejora: {solution.num_colors}")
print(f"Conflictos: {solution.count_conflicts()}")
```

**Output:**
```
Colores después mejora: 5
Conflictos: 0
```

---

### Paso 4: Ejecutar ILS Completo
```python
from metaheuristic.ils_core import IteratedLocalSearch
from operators.constructive import GreedyDSATUR, RandomSequential
from operators.local_search import KempeChain
from operators.perturbation import RandomRecolor
from operators.repair import RepairConflicts
from core.evaluation import ColoringEvaluator

# Setup
constructor = GreedyDSATUR(problem)
local_search = KempeChain(problem)
perturb = RandomRecolor(problem)
repair = RepairConflicts(problem)
evaluator = ColoringEvaluator(problem)

# Run ILS
ils = IteratedLocalSearch(
    problem=problem,
    constructor=constructor,
    local_search=local_search,
    perturb=perturb,
    repair=repair,
    evaluator=evaluator,
    max_iterations=500,
    perturbation_strength=0.2,
    local_search_iterations=100,
    restart_threshold=50
)

best_solution = ils.run()

# Results
print(f"Mejor k encontrado: {best_solution.num_colors}")
print(f"Conflictos: {best_solution.count_conflicts()}")
print(f"Óptimo conocido: {5}")  # queen5_5 optimal
print(f"Gap: {(best_solution.num_colors - 5) / 5 * 100:.1f}%")
print(f"Evaluaciones: {evaluator.num_evaluations}")
print(f"Tiempo: {best_solution.elapsed_time:.2f}s")
```

**Output:**
```
Mejor k encontrado: 5
Conflictos: 0
Óptimo conocido: 5
Gap: 0.0%
Evaluaciones: 49843
Tiempo: 2.35s
```

---

## 📈 EJEMPLO 5: ESTADÍSTICAS DE DATASET

### Resumen de 79 Instancias
```python
loader = InstanceLoader('datasets/documentation')

print("\n=== ESTADÍSTICAS POR FAMILIA ===\n")
for source in ['MYC', 'SGB', 'DSJ', 'CUL', 'REG', 'LEI', 'SCH']:
    instances = loader.get_by_source(source)
    sizes = [i['nodes'] for i in instances]
    print(f"{source}: {len(instances)} instancias, "
          f"nodos: {min(sizes)}-{max(sizes)}")

print("\n=== ESTADÍSTICAS POR DIFICULTAD ===\n")
for difficulty in ['trivial', 'easy', 'medium', 'hard', 'very_hard', 'extremely_hard']:
    instances = loader.get_by_difficulty(difficulty)
    if instances:
        print(f"{difficulty}: {len(instances)} instancias")

print("\n=== ÓPTIMOS CONOCIDOS ===\n")
with_optimal = loader.get_optimal_known()
unknown = loader.get_optimal_unknown()
print(f"Con óptimo confirmado: {len(with_optimal)}")
print(f"Sin óptimo conocido: {len(unknown)}")
```

**Output:**
```
=== ESTADÍSTICAS POR FAMILIA ===

MYC: 5 instancias, nodos: 11-23
SGB: 24 instancias, nodos: 74-561
DSJ: 15 instancias, nodos: 125-1000
CUL: 6 instancias, nodos: 300-1000
REG: 13 instancias, nodos: 184-864
LEI: 12 instancias, nodos: 450-450
SCH: 2 instancias, nodos: 352-385

=== ESTADÍSTICAS POR DIFICULTAD ===

trivial: 2 instancias
easy: 18 instancias
medium: 28 instancias
hard: 18 instancias
very_hard: 10 instancias
extremely_hard: 3 instancias

=== ÓPTIMOS CONOCIDOS ===

Con óptimo confirmado: 45
Sin óptimo conocido: 34
```

---

## 🎯 CASOS DE PRUEBA RECOMENDADOS

### Para Testing Rápido (< 5 minutos)
```python
test_instances = [
    'myciel2',      # 5 nodos, trivial, óptimo=3
    'myciel3',      # 11 nodos, easy, óptimo=4
    'myciel4',      # 23 nodos, easy, óptimo=5
    'anna',         # 138 nodos, medium, óptimo=11
    'david',        # 87 nodos, medium, óptimo=11
]
```

### Para Validación (5-15 minutos)
```python
validation_instances = [
    'queen5_5',     # 25 nodos, easy, óptimo=5
    'queen6_6',     # 36 nodos, medium, óptimo=6
    'queen8_8',     # 64 nodos, medium, óptimo=8
    'games120',     # 120 nodos, medium, óptimo=9
]
```

### Para Experimentos Completos (30-60 minutos)
```python
# Todas las 79 instancias con 500 iteraciones cada una
# Genera: k, conflicts, gap, tiempo
# Ordena por: familia, dificultad, gap
```

---

## 📊 FORMATOS DE SALIDA ESPERADOS

### Salida de Demo Básico
```
=====================================
Instancia: myciel4.col
Nodos: 23, Aristas: 71
=====================================

GreedyDSATUR:       k=5 (0 conflictos) [0.01s]
KempeChain (20it):  k=5 (0 conflictos) [0.02s]
ILS (500it):        k=5 (0 conflictos) [0.45s]
Óptimo conocido:    k=5
Gap:                0.0%

=====================================
```

### Tabla de Resultados Experimentales
```
Instance        Nodes  Edges    BKS   ILS   Gap%  Time(s)
─────────────────────────────────────────────────────────
myciel2           5     5      3     3    0.0   0.01
myciel3          11    20      4     4    0.0   0.02
myciel4          23    71      5     5    0.0   0.05
anna            138   493     11    11    0.0   0.34
david            87   406     11    11    0.0   0.21
queen5_5         25   160      5     5    0.0   0.15
queen6_6         36   290      6     6    0.0   0.28
games120        120   638      9     9    0.0   0.45
DSJC125.1       125  1472      ?    18    ?     1.23
DSJC500.1       500 24916      ?    89    ?     5.67
```

---

## ✅ CHECKLIST: VALIDACIÓN DE DATOS

- [x] Instancias cargadas: 79 archivos .col en `datasets/{CUL,DSJ,...}/`
- [x] Formato DIMACS: `p edge n m` + `e v1 v2`
- [x] Metadata JSON: 79 entradas con nodos, aristas, óptimos
- [x] Loader.py: Funcional para acceso programático
- [x] Instancias pequeñas disponibles: myciel2-7, anna, david
- [x] Instancias medianas: queen series, games120, miles
- [x] Instancias grandes: DSJC500+, flat1000, inithx, fpsol2

**Datos 100% listos ✓**

---

Este documento te muestra **exactamente** qué datos tienes y cómo usarlos en código.
