# GCP-ILS Implementation Requirements

**Fecha**: 2025-12-30  
**Estado**: Análisis Completo  
**Proyecto**: Graph Coloring Problem con Iterated Local Search

---

## 📋 CHECKLIST IMPLEMENTACIÓN COMPLETA

### ✅ Ya Disponible
- [x] **79 instancias de benchmark** (DIMACS Challenge suite)
  - CUL (6), DSJ (15), LEI (12), MYC (5), REG (13), SCH (2), SGB (24)
  - Formato: `.col` (DIMACS estándar)
  - Nodos: 11-1000, Aristas: 20-898,898
  - Óptimos conocidos: ~45 instancias, Desconocidos: ~34

- [x] **Especificación del Problema** (`problema_metaheuristica.md`)
  - Modelo matemático completo
  - 15 terminales identificados (constructivos, mejora, perturbación, etc.)
  - Criterios de evaluación

- [x] **Documentación de Dataset**
  - `CONTEXT.md`: Descripción detallada de cada familia
  - `loader.py`: Herramienta Python para acceder instancias
  - `metadata.json`: Información estructurada de 79 grafos
  - Familias documentadas: DSJ, CUL, REG, LEI, SCH, SGB, MYC

- [x] **Configuración Base** (`config.yaml`)
  - Parámetros ILS definidos
  - Operadores especificados
  - Terminales para GAA

---

### ❌ FALTA IMPLEMENTAR (Estructura de Código)

#### 1. **Capa Core - Modelo del Problema**
```
needed_files: core/problem.py
```

**Responsabilidades:**
- Clase `GraphColoringProblem`
  - Constructor que lee formato DIMACS `.col`
  - Atributos: `n` (vértices), `edges` (lista de aristas), `metadata`
  - Métodos: `get_degree(v)`, `get_neighbors(v)`, `is_adjacent(u,v)`
  
- Clase `ColoringSolution`
  - Representación: `coloring = [c_1, c_2, ..., c_n]` donde `c_i ∈ {1..k}`
  - Atributos: `num_colors`, `conflicts` (pares adyacentes con mismo color)
  - Métodos: `is_feasible()`, `count_conflicts()`, `copy()`

**Referencia de diseño**: Ver `KBP-SA/core/problem.py` y `KBP-SA/core/solution.py`

---

#### 2. **Capa Core - Evaluador**
```
needed_files: core/evaluation.py
```

**Responsabilidades:**
- Clase `ColoringEvaluator`
  - `evaluate(solution)` → fitness (minimizar k + penalización por conflictos)
  - `count_conflicts(solution)` → número de aristas monocromáticas
  - `is_feasible(solution)` → boolean
  
**Función de fitness:**
```python
fitness = num_colors + 100 * num_conflicts
```

**Referencia de diseño**: Ver `KBP-SA/core/evaluation.py`

---

#### 3. **Data Layer - Parser DIMACS**
```
needed_files: data/loader.py, data/parser.py
```

**Responsabilidades:**
- `DIMACParser.parse(filepath)` → `(n, edges, metadata)`
  - Lee formato: `p edge n m` + `e v1 v2` lines
  - Valida: numeración desde 1, sin auto-loops, sin duplicados
  - Retorna estructura para `GraphColoringProblem`

- `DataLoader.load_instance(name_or_path)` → `GraphColoringProblem`
  - Integración con `datasets/documentation/loader.py`
  - Busca instancias por nombre en 8 familias
  - Retorna objeto listo para resolver

**Archivos de entrada**: 
- Instancias en: `datasets/CUL/`, `datasets/DSJ/`, ... `datasets/SGB/`
- Metadata en: `datasets/documentation/metadata.json`

**Referencia de diseño**: Ver `KBP-SA/data/loader.py`

---

#### 4. **Operadores - Constructivos**
```
needed_files: operators/constructive.py
```

**Responsabilidades:**
Implementar inicializadores que crean soluciones factibles:

| Operador | Referencia | Complejidad |
|----------|-----------|-------------|
| `GreedyDSATUR` | [Brelaz1979] | O(n²) |
| `GreedyLargestFirst` | [Welsh1967] | O(n²) |
| `GreedySL` | [Matula1972] | O(n log n) |
| `RandomSequential` | [Johnson1974] | O(n·Δ) |
| `RLF` | [Leighton1979] | O(n²) |

**Salida**: Todas retornan `ColoringSolution` factible (sin conflictos)

**Referencia de diseño**: Ver `KBP-SA/operators/constructive.py`

---

#### 5. **Operadores - Mejora Local**
```
needed_files: operators/local_search.py
```

**Responsabilidades:**
Implementar búsqueda local desde solución actual:

| Operador | Técnica | Impacto |
|----------|---------|--------|
| `KempeChain` | Intercambio de colores entre clases | Muy fuerte |
| `TabuCol` | Búsqueda tabú con memoria | Fuerte |
| `OneVertexMove` | Cambia color de 1 vértice conflictivo | Débil |
| `SwapColors` | Intercambia 2 colores en todo grafo | Medio |

**Entrada/Salida**: `ColoringSolution` → `ColoringSolution` (posiblemente infactible temporalmente)

**Referencia de diseño**: Ver `KBP-SA/operators/improvement.py`

---

#### 6. **Operadores - Perturbación/Shake**
```
needed_files: operators/perturbation.py
```

**Responsabilidades:**
Escapar de óptimos locales mediante movimientos grandes:

| Operador | Acción |
|----------|--------|
| `RandomRecolor` | Recolorea k vértices aleatoriamente |
| `PartialDestroy` | Borra coloración de subgrafo, reconstruye |
| `ColorClassMerge` | Fusiona dos clases de color, repara |

**Parámetro clave**: `perturbation_strength` (0.2 = recolorear 20% de nodos)

**Referencia de diseño**: Ver `KBP-SA/operators/perturbation.py`

---

#### 7. **Operadores - Reparación**
```
needed_files: operators/repair.py
```

**Responsabilidades:**
Convertir soluciones infactibles a factibles:

| Operador | Estrategia |
|----------|-----------|
| `RepairConflicts` | Cambia colores de vértices conflictivos |
| `BacktrackRepair` | Reparación con backtracking limitado |
| `GreedyRepair` | Voraz para eliminar conflictos |

**Entrada**: `ColoringSolution` (posiblemente infactible)  
**Salida**: `ColoringSolution` factible

---

#### 8. **Metaheurística - ILS Core**
```
needed_files: metaheuristic/ils_core.py
```

**Responsabilidades:**
Implementar Iterated Local Search:

```python
class IteratedLocalSearch:
    def __init__(self, problem, constructor, local_search, perturb, repair):
        # Inicialización con parámetros del config.yaml
        self.max_iterations = 500
        self.perturbation_strength = 0.2
        self.local_search_iterations = 100
        self.restart_threshold = 50
    
    def run(self) -> ColoringSolution:
        # 1. x_curr = constructor(problem)
        # 2. x_curr = local_search(x_curr)
        # 3. x_best = x_curr
        # 4. iter = 0
        # 5. while iter < max_iterations:
        #    5a. x' = perturb(x_curr)  # Shake
        #    5b. x' = local_search(x')
        #    5c. if evaluate(x') <= evaluate(x_curr):
        #        x_curr = x'
        #        if evaluate(x') < evaluate(x_best):
        #           x_best = x'
        #    5d. else if iter % restart_threshold == 0:
        #        x_curr = new initial solution
        # 6. return x_best
```

**Parámetros**: Ver `config.yaml` metaheuristic section

**Referencia de diseño**: Ver `KBP-SA/metaheuristic/sa_core.py`

---

#### 9. **Sistema GAA - Nodos AST**
```
needed_files: gaa/ast_nodes.py
```

**Responsabilidades:**
Definir nodos abstractos del AST que pueden ser combinados:

- `ConstructorNode` (GreedyDSATUR, RandomSequential, etc.)
- `LocalSearchNode` (KempeChain, TabuCol, etc.)
- `PerturbationNode` (RandomRecolor, PartialDestroy, etc.)
- `SequenceNode` (combina múltiples operadores)
- `ConditionalNode` (ejecuta based on condition)

**Ejemplo de árbol sintáctico para algoritmo generado:**
```
Sequence
  ├─ ConstructorNode(GreedyDSATUR)
  ├─ LocalSearchNode(KempeChain)
  └─ Loop(500 iterations)
      ├─ PerturbationNode(RandomRecolor)
      └─ LocalSearchNode(TabuCol)
```

**Referencia de diseño**: Ver `KBP-SA/gaa/ast_nodes.py`

---

#### 10. **Evaluación Experimental**
```
needed_files: experimentation/runner.py, experimentation/metrics.py
```

**Responsabilidades:**
- `ExperimentRunner`: Ejecuta ILS en múltiples instancias
- `ColoringMetrics`:
  - Evaluación: k (colores), conflictos
  - Gap: gap = (k - optimal) / optimal × 100%
  - Comparación: vs. Best Known Solutions (DIMACS)
  - Agregación: media, desv. estándar, mejora respecto baseline

**Instancias de Prueba Recomendadas:**
- **Training** (5): myciel3, myciel4, queen5_5, anna, david
- **Validation** (3): queen6_6, homer, huck
- **Test** (8): jean, games120, miles250, fpsol2.i.1, zeroin.i.1, le450_5a, DSJC125.1, flat300_20_0

**Referencia de diseño**: Ver `KBP-SA/experimentation/runner.py` y `metrics.py`

---

#### 11. **Scripts Ejecutables**
```
needed_files: 
  scripts/demo_complete.py       # Demo básico (30s)
  scripts/demo_experimentation.py # Experimentos completos (60-90s)
  scripts/run.py                 # Ejecución principal
```

**Responsabilidades:**

**demo_complete.py:**
- Cargar 3-4 instancias pequeñas
- Ejecutar ILS en cada una
- Reportar: k, conflictos, tiempo, gap vs óptimo

**demo_experimentation.py:**
- Cargar todas 79 instancias
- Ejecutar ILS en cada una
- Generar gráficas:
  - Scatter: nodos vs k encontrado
  - Histogram: distribución de gaps
  - Performance profiles: ILS vs baseline greedy
  - Tabla: ranking por familia

**run.py:**
- Interfaz CLI: `python run.py --instance queen12_12 --iterations 500`
- Modes: `train`, `validation`, `test`, `single`

**Referencia de diseño**: Ver `KBP-SA/scripts/demo_complete.py`

---

#### 12. **Tests Unitarios**
```
needed_files: tests/test_core.py
```

**Casos de prueba mínimos:**
- `test_dimacs_parser`: Carga instancia DIMACS válida
- `test_coloring_solution`: Crea/copia soluciones
- `test_is_feasible`: Detecta conflictos correctamente
- `test_constructive`: GreedyDSATUR genera solución factible
- `test_local_search`: KempeChain mejora solución
- `test_evaluate`: Función fitness correcta
- `test_ils_basic`: ILS completa ejecución básica

---

### 📁 ESTRUCTURA FINAL DE DIRECTORIOS

```
GCP-ILS/
├── problema_metaheuristica.md       ✅ (especificación)
├── config.yaml                       ✅ (configuración)
├── README.md                         ✅ (overview)
│
├── datasets/                         ✅ (instancias)
│   ├── CUL/ .... DSJ/ .... SGB/     ✅ (79 .col files)
│   └── documentation/                ✅ (metadata, loader)
│
├── core/                             ❌ (FALTA)
│   ├── __init__.py
│   ├── problem.py                    ❌ GraphColoringProblem
│   ├── solution.py                   ❌ ColoringSolution
│   └── evaluation.py                 ❌ ColoringEvaluator
│
├── data/                             ❌ (FALTA)
│   ├── __init__.py
│   ├── parser.py                     ❌ DIMACParser
│   └── loader.py                     ❌ DataLoader
│
├── operators/                        ❌ (FALTA)
│   ├── __init__.py
│   ├── constructive.py               ❌ Inicializadores
│   ├── local_search.py               ❌ Búsqueda local
│   ├── perturbation.py               ❌ Perturbación
│   └── repair.py                     ❌ Reparación
│
├── metaheuristic/                    ❌ (FALTA)
│   ├── __init__.py
│   └── ils_core.py                   ❌ ILS
│
├── gaa/                              ❌ (FALTA)
│   ├── __init__.py
│   ├── ast_nodes.py                  ❌ Nodos AST
│   └── grammar.py                    ❌ Gramática BNF
│
├── experimentation/                  ❌ (FALTA)
│   ├── __init__.py
│   ├── runner.py                     ❌ ExperimentRunner
│   ├── metrics.py                    ❌ ColoringMetrics
│   └── visualization.py              ❌ Gráficas
│
├── scripts/                          ❌ (FALTA)
│   ├── demo_complete.py              ❌ Demo 30s
│   ├── demo_experimentation.py       ❌ Experimentos 60-90s
│   ├── run.py                        ❌ Main CLI
│   ├── validate_datasets.py          ❌ Validación
│   └── test_quick.py                 ❌ Test rápido
│
├── tests/                            ❌ (FALTA)
│   ├── __init__.py
│   └── test_core.py                  ❌ 18+ tests
│
└── utils/                            ❌ (FALTA)
    ├── __init__.py
    ├── config.py                     ❌ Config loader
    └── logging.py                    ❌ Logging
```

---

## 🎯 PRIORIDAD DE IMPLEMENTACIÓN

### Fase 1: Core Functionality (Día 1-2)
1. ✅ core/problem.py - Parser DIMACS + GraphColoringProblem
2. ✅ core/solution.py - ColoringSolution 
3. ✅ core/evaluation.py - ColoringEvaluator
4. ✅ data/loader.py - Integración con dataset

### Fase 2: Operadores Básicos (Día 2-3)
5. ✅ operators/constructive.py - GreedyDSATUR al menos
6. ✅ operators/local_search.py - KempeChain al menos
7. ✅ operators/perturbation.py - RandomRecolor
8. ✅ operators/repair.py - RepairConflicts

### Fase 3: Metaheurística (Día 3)
9. ✅ metaheuristic/ils_core.py - ILS completo
10. ✅ scripts/run.py - CLI

### Fase 4: Validación & Experimentos (Día 4)
11. ✅ tests/test_core.py - Tests unitarios
12. ✅ experimentation/runner.py - Experimentos
13. ✅ scripts/demo_complete.py - Demo

### Fase 5: GAA Integration (Día 5+)
14. ✅ gaa/ast_nodes.py - Nodos AST
15. ✅ gaa/grammar.py - Gramática BNF

---

## 📊 REFERENCIAS CRUZADAS

### Desde KBP-SA (usar como blueprint)
- **Estructura core**: `projects/KBP-SA/core/` → aplica patrón similar
- **Operadores**: `projects/KBP-SA/operators/` → mismo patrón
- **Metaheurística**: `projects/KBP-SA/metaheuristic/sa_core.py` → adaptar a ILS
- **Experimentation**: `projects/KBP-SA/experimentation/` → usar métodos de metrics
- **Tests**: `projects/KBP-SA/tests/test_core.py` → adaptar casos

### Dataset Tools
- **loader.py**: `projects/GCP-ILS/datasets/documentation/loader.py` (USE THIS!)
- **Metadata**: `projects/GCP-ILS/datasets/documentation/metadata.json`
- **Instancias**: `projects/GCP-ILS/datasets/{CUL,DSJ,...}/`

### Documentación Base
- **Problema**: `projects/GCP-ILS/problema_metaheuristica.md`
- **Config**: `projects/GCP-ILS/config.yaml`

---

## 🚀 PASOS SIGUIENTES

1. **Confirmar scope**: ¿Implementar todos los operadores o subconjunto?
2. **Orden de implementación**: ¿Seguir fases o ajustar?
3. **Baselines**: ¿Comparar contra Greedy pure o BKS DIMACS?
4. **Parámetros ILS**: ¿Ajustar config.yaml según tests iniciales?

---

**Documento creado**: 2025-12-30  
**Próximo paso**: Iniciar Fase 1 (core/problem.py) ✓
