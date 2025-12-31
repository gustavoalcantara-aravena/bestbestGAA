# GAA - Generación Automática de Algoritmos
## Guía de Uso del Módulo Implementado

---

## 📚 Introducción

El módulo `gaa/` implementa un sistema completo de **Generación Automática de Algoritmos (GAA)** para Graph Coloring Problem con Iterated Local Search.

**¿Qué hace?**
- Genera algoritmos automáticamente como **Árboles Sintácticos Abstractos (AST)**
- Los algoritmos se representan como combinaciones de operadores (construcción, mejora, perturbación)
- Evoluciona estos algoritmos usando **Simulated Annealing**
- Selecciona el mejor algoritmo después de múltiples generaciones

---

## 🏗️ Estructura del Módulo

```
gaa/
├── __init__.py          # Exportar clases públicas
├── ast_nodes.py         # Definición de nodos AST
├── grammar.py           # Gramática BNF
├── generator.py         # Generador de algoritmos
└── interpreter.py       # Intérprete/ejecutor
```

---

## 🚀 Quickstart

### 1. Demostración Rápida

```bash
python scripts/gaa_quick_demo.py
```

Esto mostrará:
- Cómo se crean algoritmos aleatorios
- Estructura de 3 algoritmos generados
- Ejecución en una pequeña instancia

### 2. Experimento Completo

```bash
python scripts/gaa_experiment.py
```

Esto ejecutará:
- Generación de población inicial de 5 algoritmos
- Evolución durante 20 generaciones
- Guardará resultados en `output/gaa/`

---

## 💻 Uso Programático

### Ejemplo 1: Generar un Algoritmo

```python
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator

# Crear gramática
grammar = Grammar(min_depth=2, max_depth=4)

# Crear generador
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# Generar algoritmo aleatorio válido
algorithm = generator.generate_with_validation()

# Ver pseudocódigo
print(algorithm.to_pseudocode())
```

**Salida esperada:**
```
CONSTRUIR(DSATUR)
MIENTRAS iteraciones < 200:
  SI Improves:
    MEJORA_LOCAL(KempeChain, iter=100)
  SINO:
    PERTURBAR(RandomRecolor, intensidad=0.25)
```

### Ejemplo 2: Ejecutar Algoritmo en Problema

```python
from gaa.interpreter import execute_algorithm
from core.problem import GraphColoringProblem

# Crear problema
problem = GraphColoringProblem(
    vertices=47,
    edges=[(0,1), (0,2), ...],
    colors_known=5,
    name="myciel5"
)

# Ejecutar algoritmo
solution = execute_algorithm(algorithm, problem, seed=42)

# Ver resultados
print(f"Colores: {solution.num_colors}")
print(f"Conflictos: {solution.num_conflicts}")
print(f"Factible: {solution.is_feasible()}")
```

### Ejemplo 3: Evaluar Algoritmo en Múltiples Instancias

```python
from data.loader import DatasetLoader

# Cargar instancias de entrenamiento
loader = DatasetLoader(".")
training = loader.load_folder("training")

# Evaluar algoritmo
fitness_values = []
for instance in training:
    solution = execute_algorithm(algorithm, instance)
    fitness_values.append(solution.num_colors)

# Calcular fitness (promedio)
fitness = sum(fitness_values) / len(fitness_values)
print(f"Fitness promedio: {fitness:.2f}")
```

### Ejemplo 4: Mutar un Algoritmo

```python
from gaa.ast_nodes import mutate_ast

# Mutar algoritmo
mutated = mutate_ast(algorithm, mutation_rate=0.3)

# Ver cambios
print("Original:")
print(algorithm.to_pseudocode())

print("\nMutado:")
print(mutated.to_pseudocode())
```

---

## 🧬 Conceptos Clave

### AST (Árbol Sintáctico Abstracto)

Un algoritmo se representa como un árbol de nodos:

```python
algorithm = Seq([
    GreedyConstruct("DSATUR"),
    While(
        max_iterations=200,
        body=Seq([
            LocalSearch("KempeChain", max_iterations=100),
            If(
                condition="Improves",
                then_branch=Call("KempeChain"),
                else_branch=Perturbation("RandomRecolor", intensity=0.2)
            )
        ])
    )
])
```

**Ventajas:**
- ✅ Representación formal
- ✅ Ejecutable (el intérprete lo ejecuta)
- ✅ Manipulable (mutación, crossover)
- ✅ Serializable (guardar/cargar)

### Nodos Disponibles

| Nodo | Descripción | Ejemplo |
|------|------------|---------|
| `Seq` | Secuencia | `Seq([stmt1, stmt2, ...])` |
| `While` | Bucle | `While(max_iterations=100, body=...)` |
| `For` | Bucle determinista | `For(iterations=5, body=...)` |
| `If` | Condicional | `If(condition="Improves", then=..., else=...)` |
| `Call` | Llamada | `Call(operator="KempeChain")` |
| `GreedyConstruct` | Construcción | `GreedyConstruct("DSATUR")` |
| `LocalSearch` | Mejora | `LocalSearch("KempeChain", max_iter=100)` |
| `Perturbation` | Perturbación | `Perturbation("RandomRecolor", intensity=0.2)` |

### Terminales

**Construcción:**
- `DSATUR` - Grado de saturación
- `LF` - Largest First
- `RandomSequential` - Aleatorio
- `SL` - Smallest Last

**Mejora Local:**
- `KempeChain` - Cadenas de Kempe
- `OneVertexMove` - Cambio de color de un vértice
- `TabuCol` - Búsqueda tabú
- `SwapColors` - Intercambio de colores

**Perturbación:**
- `RandomRecolor` - Recoloración aleatoria
- `PartialDestroy` - Destruir y reconstruir
- `ColorClassMerge` - Fusionar clases de color

### Condiciones

- `Improves` - Si el último movimiento mejoró
- `Feasible` - Si la solución es factible
- `Stagnation` - Si hay estancamiento

---

## 📊 Experimento Completo

El script `gaa_experiment.py` implementa un experimento completo:

```bash
python scripts/gaa_experiment.py
```

**Pasos:**
1. Cargar instancias de entrenamiento
2. Generar población inicial de 10 algoritmos
3. Evolu cionar 50 generaciones con Simulated Annealing
4. Guardar mejor algoritmo encontrado

**Parámetros configurables:**

```python
solver = GAASolver(
    training_dir="datasets/training",
    pop_size=10,
    generations=50,
    seed=42
)
```

**Salida:**
- `output/gaa/best_algorithm_*.json` - Mejor algoritmo (AST)
- `output/gaa/evolution_history_*.json` - Historial de evolución
- `output/gaa/summary_*.txt` - Resumen en texto

---

## 🔧 Validación de Algoritmos

La gramática garantiza que los algoritmos generados sean válidos:

```python
from gaa.grammar import Grammar

grammar = Grammar(min_depth=2, max_depth=5)

# Validar AST
errors = grammar.validate_ast(algorithm)

if errors:
    print("Errores encontrados:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ Algoritmo válido")

# Obtener estadísticas
stats = grammar.get_statistics(algorithm)
print(f"Nodos: {stats['total_nodes']}")
print(f"Profundidad: {stats['depth']}")
print(f"Nodos por tipo: {stats['node_counts']}")
```

---

## 📈 Rendimiento y Límites

### Parámetros

| Parámetro | Default | Rango | Impacto |
|-----------|---------|-------|--------|
| `min_depth` | 2 | 1-10 | Complejidad mínima |
| `max_depth` | 5 | 1-10 | Complejidad máxima |
| `pop_size` | 10 | 1-100 | Diversidad |
| `generations` | 50 | 1-1000 | Tiempo de evolución |
| `mutation_rate` | 0.3 | 0-1 | Cambio por generación |

### Complejidad de Tiempo

- **Generar 1 algoritmo**: ~1 ms
- **Evaluar en 20 instancias**: ~60 segundos (depende de tamaño)
- **Generación SA**: N_gen × (eval_time + overhead)

### Recomendaciones

- Para pruebas rápidas: `pop_size=5, generations=10`
- Para experimento moderado: `pop_size=10, generations=30`
- Para producción: `pop_size=20, generations=50+`

---

## 🧪 Tests

Ejecutar suite completa de tests:

```bash
pytest tests/test_gaa.py -v
```

Tests incluyen:
- ✓ Creación de nodos AST
- ✓ Validación de gramática
- ✓ Generación de algoritmos
- ✓ Reproducibilidad con seed
- ✓ Mutación y crossover
- ✓ Ejecución de intérprete

---

## 🔍 Debugging

### Visualizar AST

```python
# Pseudocódigo
print(algorithm.to_pseudocode(indent=0))

# JSON
import json
print(json.dumps(algorithm.to_dict(), indent=2))

# Estadísticas
stats = grammar.get_statistics(algorithm)
print(f"Tamaño: {stats['total_nodes']} nodos")
print(f"Profundidad: {stats['depth']}")
```

### Rastrear Ejecución

```python
from gaa.interpreter import ASTInterpreter

interpreter = ASTInterpreter(problem)
solution = interpreter.execute(algorithm)

# Acceder a estadísticas
stats = interpreter.context.get_statistics()
print(f"Iteraciones: {stats['iterations']}")
print(f"Evaluaciones: {stats['evaluations']}")
print(f"Mejoras: {stats['improvements']}")
```

---

## 📚 Ejemplos Adicionales

### Crear Algoritmo Manualmente

```python
from gaa.ast_nodes import *

# Algoritmo: DSATUR + Kempe Chains iterativo
algorithm = Seq([
    GreedyConstruct("DSATUR"),
    While(
        max_iterations=500,
        body=LocalSearch("KempeChain", max_iterations=100)
    )
])

print(algorithm.to_pseudocode())
```

### Comparar Dos Algoritmos

```python
gen = AlgorithmGenerator(seed=42)

alg1 = gen.generate()
alg2 = gen.generate()

fitness1 = evaluate_multi_instance(alg1, training)
fitness2 = evaluate_multi_instance(alg2, training)

print(f"Algoritmo 1: {fitness1:.2f}")
print(f"Algoritmo 2: {fitness2:.2f}")

if fitness1 < fitness2:
    print("Ganador: Algoritmo 1")
else:
    print("Ganador: Algoritmo 2")
```

---

## 🐛 Troubleshooting

### "AST excede profundidad máxima"

```python
# Usar generador con validación
generator = AlgorithmGenerator(grammar=Grammar(max_depth=4))
algorithm = generator.generate_with_validation()
```

### "Operador no reconocido"

Verificar que el operador esté en los TERMINALES definidos:

```python
from gaa.grammar import Grammar
grammar = Grammar()
print(grammar.all_terminals)
```

### "No hay instancias de entrenamiento"

Asegurar que las instancias estén en `datasets/training/`:

```python
from data.loader import DatasetLoader
loader = DatasetLoader(".")
instances = loader.load_folder("training")
print(f"Instancias encontradas: {len(instances)}")
```

---

## 🎯 Próximos Pasos

1. **Ejecutar demo rápida**: `python scripts/gaa_quick_demo.py`
2. **Ejecutar experimento**: `python scripts/gaa_experiment.py`
3. **Analizar resultados**: Ver `output/gaa/`
4. **Modificar parámetros**: Ajustar `pop_size`, `generations`, etc.
5. **Extensión**: Agregar nuevos operadores o condiciones

---

## 📖 Referencias

- AST: Abstract Syntax Trees
- SA: Simulated Annealing
- GAA: Generación Automática de Algoritmos
- ILS: Iterated Local Search
- GCP: Graph Coloring Problem

---

**Documentación actualizada**: 31-12-2025
**Módulo GAA completamente implementado y funcional**
