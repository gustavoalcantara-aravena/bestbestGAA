# Guía Rápida de Uso - GCP-ILS

**Para**: Desarrolladores que necesitan usar el módulo Core implementado

---

## 🚀 Instalación

```bash
cd GAA-GCP-ILS-4
pip install -r requirements.txt
```

---

## 📖 Ejemplos de Uso

### 1. Cargar una Instancia de Problema

```python
from core import GraphColoringProblem

# Opción A: Desde archivo DIMACS
problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# Opción B: Crear manualmente
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
problem = GraphColoringProblem(
    vertices=4,
    edges=edges,
    colors_known=3,
    name="test_instance"
)

# Ver información de la instancia
print(problem.summary())
```

**Salida**:
```
============================================================
Instancia: myciel3
============================================================
Vértices:              11
Aristas:               20
Densidad:              0.3636
Grado máximo (Δ):      4
Grado mínimo:          2
Grado promedio:        3.64
Bipartito:             False
Cota superior (Δ+1):   5
Cota inferior:         4
Óptimo conocido (χ):   4
============================================================
```

### 2. Crear una Solución

```python
from core import ColoringSolution

# Crear solución manualmente
assignment = {1: 0, 2: 1, 3: 0, 4: 2}
solution = ColoringSolution(assignment=assignment)

print(f"Colores utilizados: {solution.num_colors}")
print(f"Vértices: {solution.num_vertices}")
print(f"Distribución: {solution.color_usage()}")
```

**Salida**:
```
Colores utilizados: 3
Vértices: 4
Distribución: {0: 2, 1: 1, 2: 1}
```

### 3. Validar Factibilidad

```python
from core import ColoringSolution, GraphColoringProblem

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
solution = ColoringSolution({i: i % 3 for i in range(1, 12)})

# Verificar si es factible
is_feasible = solution.is_feasible(problem)
print(f"¿Solución factible? {is_feasible}")

# Contar conflictos
conflicts = solution.num_conflicts(problem)
print(f"Número de conflictos: {conflicts}")

# Obtener vértices en conflicto
conflicted = solution.conflict_vertices(problem)
print(f"Vértices en conflicto: {conflicted}")
```

### 4. Evaluar una Solución

```python
from core import ColoringEvaluator

metrics = ColoringEvaluator.evaluate(solution, problem)

print(f"Colores: {metrics['num_colors']}")
print(f"Conflictos: {metrics['conflicts']}")
print(f"Factible: {metrics['feasible']}")
print(f"Fitness: {metrics['fitness']}")
print(f"Gap: {metrics['gap_percent']:.2f}%")
```

**Salida**:
```
Colores: 3
Conflictos: 0
Factible: True
Fitness: 3.0
Gap: 0.00%
```

### 5. Evaluar Múltiples Soluciones

```python
from core import ColoringEvaluator

# Crear múltiples soluciones
solutions = [
    ColoringSolution({i: 0 for i in range(1, 12)}),  # Todos mismo color (mala)
    ColoringSolution({i: i % 3 for i in range(1, 12)}),  # Random
    ColoringSolution({i: i % 4 for i in range(1, 12)}),  # 4 colores
]

# Evaluar todas
results = ColoringEvaluator.batch_evaluate(solutions, problem)

for i, result in enumerate(results):
    print(f"Solución {i+1}: {result['num_colors']} colores, "
          f"Factible: {result['feasible']}")

# Obtener la mejor
best_solution, best_metrics = ColoringEvaluator.get_best(solutions, problem)
print(f"\nMejor: {best_metrics['num_colors']} colores")
```

### 6. Comparar Soluciones

```python
from core import compare_solutions

# Comparar visualmente
table = compare_solutions(solutions, problem)
print(table)
```

**Salida**:
```
====================================================================================================
Comparación de Soluciones - myciel3
====================================================================================================
Sol    Colores    Conflictos   Factible   Gap        Fitness        
----------------------------------------------------------------------------------------------------
1      11         50           ✗           175.00%    51000.00       
2      4          0            ✓          0.00%      4.00           
3      4          0            ✓          0.00%      4.00           
====================================================================================================
```

### 7. Operar en Soluciones

```python
# Copiar solución
solution_copy = solution.copy()

# Recolorear un vértice
new_solution = solution.recolor_vertex(1, 2)

# Recolorear múltiples vértices
recoloring = {1: 0, 2: 1, 3: 0}
new_solution = solution.recolor_vertices(recoloring)

# Comparar soluciones
is_better = new_solution.is_better_than(solution, problem)
print(f"¿Nueva es mejor? {is_better}")
```

### 8. Usar Configuración

```python
from utils import Config, load_config

# Cargar configuración
config = load_config("config/config.yaml")

# Acceder a parámetros
max_iters = config.get("ils.max_iterations")
ratio = config.get("operators.perturbation.ratio")

print(f"Max iteraciones: {max_iters}")
print(f"Ratio perturbación: {ratio}")

# Crear directorios
from utils import ensure_directories
ensure_directories()  # Crea todos los directorios necesarios
```

---

## 🧪 Testing

### Ejecutar Tests Rápidos

```bash
python scripts/test_quick.py
```

### Ejecutar Suite Completa

```bash
pytest tests/ -v
```

### Ejecutar Tests Específicos

```bash
# Solo tests de Core
pytest tests/test_core.py -v

# Solo una clase de tests
pytest tests/test_core.py::TestGraphColoringProblem -v

# Con cobertura
pytest tests/ --cov=core --cov-report=html
```

---

## 📚 Clases Principales

### GraphColoringProblem

```python
# Crear
problem = GraphColoringProblem(
    vertices=10,
    edges=[(1,2), (2,3), ...],
    colors_known=5,
    name="myinstance"
)

# Propiedades
problem.n_vertices       # Número de vértices
problem.n_edges          # Número de aristas
problem.max_degree       # Grado máximo
problem.degree_sequence  # Array de grados
problem.is_bipartite     # ¿Es bipartito?
problem.upper_bound      # Cota superior trivial

# Métodos
problem.is_edge(u, v)                    # ¿Existe arista?
problem.neighbors(v)                     # Vecinos de v
problem.degree(v)                        # Grado de v
problem.load_from_dimacs("file.col")     # Cargar DIMACS
problem.summary()                         # Resumen detallado
```

### ColoringSolution

```python
# Crear
solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 0})

# Propiedades
solution.num_colors          # Número de colores
solution.num_vertices        # Número de vértices
solution.color_sets          # {color: {vértices}}
solution.color_usage()       # {color: cantidad}
solution.color_balance()     # Desviación estándar

# Validación
solution.is_feasible(problem)           # ¿Es factible?
solution.num_conflicts(problem)         # Cantidad de conflictos
solution.conflict_vertices(problem)     # Vértices en conflicto

# Operaciones
solution.copy()                         # Copiar
solution.recolor_vertex(v, color)       # Recolorear un vértice
solution.recolor_vertices({...})        # Recolorear múltiples
solution.is_better_than(other, problem) # Comparar
```

### ColoringEvaluator

```python
# Métodos estáticos
metrics = ColoringEvaluator.evaluate(solution, problem)
results = ColoringEvaluator.batch_evaluate(solutions, problem)
best, metrics = ColoringEvaluator.get_best(solutions, problem)
stats = ColoringEvaluator.get_statistics(results)
string = ColoringEvaluator.format_result(solution, problem)
```

---

## 🔧 API Completa de Configuración

```python
from utils import Config

# Cargar
config = Config.load("config/config.yaml")

# Leer parámetros
value = Config.get("section.subsection.key", default=None)

# Estableces valores
Config.set("section.key", new_value)

# Obtener todo
all_config = Config.get_all()

# Acceso directo
value = Config["section.key"]
```

**Parámetros disponibles**:
```
problem.datasets_dir
problem.max_vertices_quick
ils.max_iterations
ils.time_budget
ils.acceptance_strategy
operators.constructive.method
operators.improvement.method
operators.perturbation.method
operators.perturbation.ratio
output.results_dir
output.generate_plots
logging.level
```

---

## 📝 Patrón Típico de Uso

```python
from core import GraphColoringProblem, ColoringSolution, ColoringEvaluator
from utils import Config, load_config

# 1. Cargar configuración
config = load_config()

# 2. Cargar instancia
problem = GraphColoringProblem.load_from_dimacs(
    f"{config.get('problem.datasets_dir')}/myciel3.col"
)
print(problem.summary())

# 3. Crear solución (placeholder - será implementado por operadores)
solution = ColoringSolution({i: (i-1) % problem.colors_known 
                             for i in range(1, problem.n_vertices + 1)})

# 4. Validar
print(f"Factible: {solution.is_feasible(problem)}")

# 5. Evaluar
metrics = ColoringEvaluator.evaluate(solution, problem)
print(ColoringEvaluator.format_result(solution, problem, metrics))

# 6. Mejorar (will be done by improvement operators)
# improved = KempeChain.improve(solution, problem)
```

---

## 🎯 Próximos Pasos

Una vez implementados los operadores, se usarán así:

```python
# Importar operadores (cuando estén implementados)
from operators.constructive import GreedyDSATUR
from operators.improvement import KempeChain
from operators.perturbation import RandomRecolor
from metaheuristic.ils_core import IteratedLocalSearch

# Crear algoritmo
ils = IteratedLocalSearch(
    constructive=GreedyDSATUR,
    improvement=KempeChain,
    perturbation=RandomRecolor,
    max_iterations=500
)

# Ejecutar
best_solution, history = ils.solve(problem)

# Analizar resultados
metrics = ColoringEvaluator.evaluate(best_solution, problem)
print(f"Solución final: {best_solution.num_colors} colores")
```

---

## 💡 Tips y Trucos

### Debugging

```python
# Ver detalles de una solución
print(solution.detailed_summary(problem))

# Ver detalles del problema
print(problem.summary())

# Ver si es bipartito
print(f"Bipartito: {problem.is_bipartite}")
```

### Performance

```python
import time

start = time.time()
metrics = ColoringEvaluator.evaluate(solution, problem)
elapsed = time.time() - start
print(f"Evaluación: {elapsed:.4f}s")
```

### Reproducibilidad

```python
import numpy as np

# Fijar seed
np.random.seed(42)

# Ahora generaciones aleatorias serán reproducibles
```

---

**Versión**: 1.0.0  
**Última actualización**: 31 Diciembre 2025
