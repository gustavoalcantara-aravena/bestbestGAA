# 📦 Módulos Implementados - Referencia Rápida

## 🎯 Resumen de Módulos

```
GAA-GCP-ILS-4/
├── core/                      [✅ IMPLEMENTADO - 1,300+ líneas]
│   ├── __init__.py
│   ├── problem.py             [GraphColoringProblem - 550+ líneas]
│   ├── solution.py            [ColoringSolution - 450+ líneas]
│   └── evaluation.py          [ColoringEvaluator - 300+ líneas]
├── config/                    [✅ IMPLEMENTADO - 350+ líneas]
│   └── config.yaml            [100+ parámetros]
├── utils/                     [✅ IMPLEMENTADO - 150+ líneas]
│   ├── __init__.py
│   └── config.py              [Config singleton]
├── operators/                 [📋 PENDIENTE - Estructura lista]
│   ├── __init__.py
│   ├── constructive.py        [vacío - para implementar]
│   ├── improvement.py         [vacío - para implementar]
│   ├── perturbation.py        [vacío - para implementar]
│   └── repair.py              [vacío - para implementar]
├── metaheuristic/             [📋 PENDIENTE - Estructura lista]
│   ├── __init__.py
│   ├── ils_core.py            [vacío - para implementar]
│   └── perturbation_schedules.py [vacío - para implementar]
├── tests/                     [✅ INFRAESTRUCTURA LISTA - 42+ tests especificados]
│   ├── __init__.py
│   ├── conftest.py            [300+ líneas de fixtures]
│   ├── test_core.py           [15+ test cases]
│   ├── test_operators.py      [20+ test cases]
│   └── test_ils.py            [10+ test cases]
├── scripts/                   [✅ PARCIAL - Pruebas listas]
│   ├── test_quick.py          [200+ líneas - test rápido]
│   ├── run_tests.py           [120+ líneas - ejecutor]
│   └── [demo_*.py]            [📋 Por implementar]
├── docs/                      [Documentación adicional]
├── datasets/                  [Instancias de prueba DIMACS]
└── [archivos raíz]            [✅ Config del proyecto]
    ├── requirements.txt
    ├── pyproject.toml
    ├── __init__.py
    ├── README.md
    ├── QUICK_START_GUIDE.md
    ├── PROJECT_STRUCTURE.md
    ├── PROJECT_STATUS.md
    ├── STATUS_FINAL.md
    └── problema_metaheuristica.md
```

---

## 📋 Detalle de Archivos Implementados

### core/problem.py (550+ líneas) ✅

**Clase**: `GraphColoringProblem` (dataclass)

**Responsabilidad**: Representar instancias del problema de coloración de grafos

**Campos**:
```python
vertices: int
edges: List[Tuple[int, int]]
colors_known: Optional[int] = None
name: str = "instance"
```

**Métodos públicos** (30+):

| Método | Parámetros | Retorna | Propósito |
|--------|-----------|---------|-----------|
| `load_from_dimacs()` | filepath | GraphColoringProblem | Cargar desde archivo DIMACS |
| `is_edge()` | u, v | bool | ¿Existe arista entre u y v? |
| `neighbors()` | v | List[int] | Vecinos del vértice v |
| `degree()` | v | int | Grado del vértice v |
| `summary()` | - | str | Resumen formateado del problema |
| `@property degree_sequence` | - | np.ndarray | Array de grados |
| `@property n_vertices` | - | int | Número de vértices |
| `@property n_edges` | - | int | Número de aristas |
| `@property max_degree` | - | int | Grado máximo |
| `@property min_degree` | - | int | Grado mínimo |
| `@property average_degree` | - | float | Grado promedio |
| `@property density` | - | float | Densidad del grafo |
| `@property is_bipartite` | - | bool | ¿Es bipartito? |
| `@property upper_bound` | - | int | Cota superior (Δ+1) |
| `@property lower_bound` | - | int | Cota inferior |
| `@property clique_number` | - | int | Número de clique |
| `@property chromatic_number` | - | Optional[int] | Número cromático (si es conocido) |
| `@property adjacency_list` | - | List[List[int]] | Lista de adyacencia |
| `@property adjacency_matrix` | - | np.ndarray | Matriz de adyacencia |
| `@property edge_weight_matrix` | - | np.ndarray | Matriz de pesos |

**Ejemplo de uso**:
```python
from core import GraphColoringProblem

# Cargar desde archivo
problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# Ver información
print(problem.n_vertices)
print(problem.n_edges)
print(problem.degree(5))
print(problem.neighbors(5))
print(problem.is_bipartite)
print(problem.summary())
```

---

### core/solution.py (450+ líneas) ✅

**Clase**: `ColoringSolution` (dataclass)

**Responsabilidad**: Representar una solución (asignación de colores) para una instancia GCP

**Campos**:
```python
assignment: Dict[int, int]  # {vértice: color}
```

**Métodos públicos** (25+):

| Método | Parámetros | Retorna | Propósito |
|--------|-----------|---------|-----------|
| `is_feasible()` | problem | bool | ¿La solución es factible? |
| `num_conflicts()` | problem | int | Número total de conflictos |
| `conflict_vertices()` | problem | Set[int] | Vértices en conflicto |
| `copy()` | - | ColoringSolution | Copia profunda |
| `recolor_vertex()` | vertex, color | ColoringSolution | Recolorear un vértice |
| `recolor_vertices()` | recoloring | ColoringSolution | Recolorear múltiples |
| `get_color()` | vertex | int | Color asignado a un vértice |
| `get_vertices_with_color()` | color | List[int] | Vértices con ese color |
| `is_better_than()` | other, problem | bool | ¿Esta es mejor? |
| `@property num_colors` | - | int | Número de colores utilizados |
| `@property num_vertices` | - | int | Número de vértices |
| `@property color_sets` | - | Dict[int, Set[int]] | {color: {vértices}} |
| `@property color_usage()` | - | Dict[int, int] | {color: cantidad} |
| `@property color_balance()` | - | float | Desviación estándar de uso |
| `__lt__()` | other | bool | Comparación menor que |
| `__eq__()` | other | bool | Comparación igualdad |
| `__le__()` | other | bool | Comparación menor o igual |

**Ejemplo de uso**:
```python
from core import ColoringSolution

# Crear solución
solution = ColoringSolution({1: 0, 2: 1, 3: 0, 4: 2})

# Información
print(solution.num_colors)      # 3
print(solution.color_usage())   # {0: 2, 1: 1, 2: 1}

# Validar
print(solution.is_feasible(problem))
print(solution.num_conflicts(problem))

# Operar
new_sol = solution.recolor_vertex(1, 1)
print(new_sol.is_better_than(solution, problem))
```

---

### core/evaluation.py (300+ líneas) ✅

**Clase**: `ColoringEvaluator` (métodos estáticos)

**Responsabilidad**: Evaluar soluciones y proporcionar métricas

**Métodos públicos** (15+):

| Método | Parámetros | Retorna | Propósito |
|--------|-----------|---------|-----------|
| `evaluate()` | solution, problem | dict | Evaluar solución única |
| `batch_evaluate()` | solutions, problem | List[dict] | Evaluar múltiples |
| `get_best()` | solutions, problem | (solution, dict) | Seleccionar mejor |
| `get_statistics()` | results | dict | Estadísticas de resultados |
| `format_result()` | solution, problem | str | Formatear para salida |
| `compare_solutions()` | solutions, problem | str | Tabla comparativa |

**Métricas devueltas** por `evaluate()`:
```python
{
    'num_colors': int,        # Número de colores utilizados
    'conflicts': int,         # Número de conflictos
    'feasible': bool,         # ¿Es factible?
    'fitness': float,         # Función de fitness
    'gap': float,             # Gap respecto al óptimo
    'gap_percent': float,     # Gap en porcentaje
    'color_balance': float,   # Balanceo de colores
    'timestamp': float        # Timestamp de evaluación
}
```

**Ejemplo de uso**:
```python
from core import ColoringEvaluator

# Evaluar solución
metrics = ColoringEvaluator.evaluate(solution, problem)
print(metrics['num_colors'])
print(metrics['feasible'])

# Evaluar múltiples
solutions = [sol1, sol2, sol3]
results = ColoringEvaluator.batch_evaluate(solutions, problem)

# Encontrar mejor
best_sol, best_metrics = ColoringEvaluator.get_best(solutions, problem)

# Estadísticas
stats = ColoringEvaluator.get_statistics(results)
print(stats['num_colors']['mean'])

# Formatear
output = ColoringEvaluator.format_result(solution, problem, metrics)
print(output)

# Comparar
table = ColoringEvaluator.compare_solutions(solutions, problem)
print(table)
```

---

### config/config.yaml (200+ líneas) ✅

**Responsabilidad**: Centralizar todos los parámetros del proyecto

**Secciones principales**:

#### problem
```yaml
problem:
  datasets_dir: "datasets"
  max_vertices_quick: 100
  validation:
    check_graph: true
    check_solution: true
```

#### ils
```yaml
ils:
  max_iterations: 500
  time_budget: 300  # segundos
  acceptance_strategy: "best"  # best, first, probabilistic
```

#### operators
```yaml
operators:
  constructive:
    method: "greedy_dsatur"
    timeout: 60
  improvement:
    method: "kempe_chain"
    max_iterations: 100
  perturbation:
    method: "random_recolor"
    ratio: 0.2
```

#### tabu_search
```yaml
tabu_search:
  enabled: false
  tenure: 20
  aspiration_criteria: true
```

#### experimentation
```yaml
experimentation:
  num_replicas: 30
  seed_strategy: "random"
  seed_base: 42
```

#### output
```yaml
output:
  results_dir: "results"
  solutions_dir: "results/solutions"
  logs_dir: "results/logs"
  plots_dir: "results/plots"
  generate_plots: true
  csv_format: true
  json_format: true
```

#### execution
```yaml
execution:
  parallelization: true
  num_threads: 4
  verify_results: true
  verbose: true
```

#### logging
```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  console_output: true
  file_output: true
  log_file: "results/logs/execution.log"
```

---

### utils/config.py (150+ líneas) ✅

**Clase**: `Config` (singleton)

**Responsabilidad**: Cargar y gestionar configuración YAML

**Métodos**:

```python
from utils import Config, load_config

# Cargar configuración
config = load_config("config/config.yaml")
# o
Config.load("config/config.yaml")

# Acceder a valores
value = Config.get("section.key", default=None)
value = Config["section.key"]

# Establecer valores
Config.set("section.key", new_value)

# Obtener todo
all_config = Config.get_all()

# Crear directorios
from utils import ensure_directories
ensure_directories()
```

---

### utils/__init__.py (100+ líneas) ✅

**Exportaciones públicas**:
```python
from utils import (
    Config,
    load_config,
    get_config,
    ensure_directories
)
```

---

### core/__init__.py (50+ líneas) ✅

**Exportaciones públicas**:
```python
from core import (
    GraphColoringProblem,
    ColoringSolution,
    ColoringEvaluator
)
```

---

## 🧪 Tests Especificados (42+)

### tests/conftest.py (300+ líneas) ✅
Proporciona fixtures para todos los tests:

**Fixtures disponibles**:
- `myciel3_problem` - Grafo Mycielski 3
- `graph_5_vertices` - Grafo K5 (clique 5)
- `bipartite_graph` - Grafo bipartito
- `random_graph` - Grafo aleatorio
- `single_vertex` - Vértice único
- `random_solution` - Solución aleatoria
- `optimal_solution` - Solución óptima
- `parametrized_graphs` - Múltiples grafos
- `large_graph` - Grafo grande

---

### tests/test_core.py (15+ tests especificados) 📋

```
TestGraphColoringProblem (8 tests)
  ✓ test_load_from_dimacs
  ✓ test_n_vertices_property
  ✓ test_n_edges_property
  ✓ test_is_edge
  ✓ test_neighbors
  ✓ test_degree_sequence
  ✓ test_is_bipartite
  ✓ test_chromatic_number

TestColoringSolution (5 tests)
  ✓ test_create_solution
  ✓ test_is_feasible
  ✓ test_num_conflicts
  ✓ test_recolor_vertex
  ✓ test_comparison

TestColoringEvaluator (4 tests)
  ✓ test_evaluate
  ✓ test_batch_evaluate
  ✓ test_get_best
  ✓ test_compare_solutions
```

---

### tests/test_operators.py (20+ tests especificados) 📋

```
TestConstructiveOperators (8 tests)
TestImprovementOperators (8 tests)
TestPerturbationOperators (4 tests)
```

---

### tests/test_ils.py (10+ tests especificados) 📋

```
TestIteratedLocalSearch (10 tests)
```

---

## 📚 Documentación Integrada

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `QUICK_START_GUIDE.md` | Guía rápida con ejemplos | ✅ Completo |
| `STATUS_FINAL.md` | Estado actual del proyecto | ✅ Completo |
| `PROJECT_STRUCTURE.md` | Estructura de carpetas | ✅ Completo |
| `PROJECT_STATUS.md` | Resumen de implementación | ✅ Completo |
| `problema_metaheuristica.md` | Especificación técnica | ✅ Completo |
| `README.md` | Documentación principal | ✅ Actualizado |
| `requirements.txt` | Dependencias Python | ✅ Completo |
| `pyproject.toml` | Configuración setuptools | ✅ Completo |

---

## 🚀 Cómo Usar Este Documento

**Si necesitas...**
- 📖 Ver clase `GraphColoringProblem` → Ir a **core/problem.py**
- 📖 Ver clase `ColoringSolution` → Ir a **core/solution.py**
- 📖 Ver evaluador → Ir a **core/evaluation.py**
- 🔧 Cambiar parámetros → Editar **config/config.yaml**
- 🧪 Ejecutar tests → Ver **tests/**
- 📚 Ejemplos rápidos → Ver **QUICK_START_GUIDE.md**
- 📊 Estado general → Ver **STATUS_FINAL.md**

---

**Última actualización**: 31 Diciembre 2025
