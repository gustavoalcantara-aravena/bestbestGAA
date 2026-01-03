# 🧬 GAA: Generación Automática de Algoritmos para VRPTW-GRASP

## Descripción

El módulo **GAA (Automatic Algorithm Generation)** genera automáticamente algoritmos válidos para VRPTW-GRASP representados como **Árboles de Sintaxis Abstracta (AST)**.

## Componentes

### 1. `grammar.py` - Gramática BNF
Define los operadores y restricciones válidas:
- **6 operadores constructivos**: NearestNeighbor, Savings, Sweep, TimeOrientedNN, RegretInsertion, RandomizedInsertion
- **8 operadores de mejora**: TwoOpt, OrOpt, ThreeOpt, Relocate, Exchange, GENI, LKH, VND
- **4 operadores de perturbación**: RandomRouteRemoval, WorseFeasibleMove, RandomRelocate, SegmentShift

### 2. `ast_nodes.py` - Nodos del AST
Implementa todos los nodos del árbol:

**Nodos de control de flujo:**
- `Seq` - Secuencia (ejecuta operaciones en orden)
- `If` - Condicional (if-then-else)
- `While` - Bucle while
- `For` - Bucle for

**Nodos de operadores:**
- `GreedyConstruct` - Construcción greedy
- `LocalSearch` - Búsqueda local
- `Perturbation` - Perturbación

Cada nodo implementa:
- `depth()` - Profundidad del subárbol
- `size()` - Número total de nodos
- `get_all_nodes()` - Lista de todos los nodos
- `to_pseudocode()` - Pseudocódigo del algoritmo
- `to_dict()` - Serialización a diccionario

### 3. `generator.py` - Generador
Genera algoritmos válidos automáticamente con 4 patrones:

| Patrón | Estructura | Complejidad | Uso |
|--------|-----------|-------------|-----|
| **Simple** | Construcción + Mejora | ⭐ Baja | Instancias pequeñas |
| **Iterativo** | Construcción + While(Mejora + Perturbación) | ⭐⭐ Media | Instancias medianas |
| **Multi-start** | For(Construcción + Mejora) | ⭐⭐ Media | Exploración |
| **Complejo** | Construcción + While(If(Mejora, Perturbación)) | ⭐⭐⭐ Alta | Instancias grandes |

### 4. `__init__.py` - Modulo
Exporta públicamente los componentes principales.

## Uso

### Generar 3 Algoritmos

```python
from gaa import AlgorithmGenerator

# Crear generador con seed (reproducibilidad)
generator = AlgorithmGenerator(seed=42)

# Generar 3 algoritmos diversos
algorithms = generator.generate_three_algorithms()

# Guardar a archivos JSON
generator.save_algorithms(algorithms)

# Output:
# [
#   {
#     'name': 'GAA_Algorithm_1',
#     'ast': {'type': 'Seq', 'body': [...]},
#     'pattern': 'simple',
#     'stats': {'depth': 2, 'size': 3, ...}
#   },
#   ...
# ]
```

### Generar un Algoritmo Individual

```python
from gaa import AlgorithmGenerator

generator = AlgorithmGenerator(seed=42)

# Generar con validación
ast = generator.generate_with_validation(max_attempts=100)

if ast:
    print(ast.to_pseudocode())
    # Output:
    # SECUENCIA:
    #   1. Construcción: Savings(alpha=0.25)
    #   2. MIENTRAS IterBudget < 200:
    #        1. Mejora Local: TwoOpt(max_iter=100)
    #        2. Perturbación: RandomRouteRemoval(strength=2)
```

## Estructura de Archivos

```
gaa/
├── __init__.py                  # Módulo (exporta componentes)
├── grammar.py                   # Gramática BNF (6+8+4 operadores)
├── ast_nodes.py                # Nodos del AST (Seq, If, While, For, Greedy, LS, Pert)
├── generator.py                 # Generador (4 patrones)
├── interpreter.py (futuro)     # Intérprete (ejecuta AST)
└── README.md                     # Este archivo
```

## Especificación Técnica

### Parámetros de la Gramática
- **min_depth**: 2 (profundidad mínima)
- **max_depth**: 5 (profundidad máxima)
- **Tamaño máximo AST**: 100 nodos

### Parámetros de Generación
- **alpha (GRASP)**: Uniforme en [0.1, 0.5]
- **max_iterations**: Elegido de [50, 100, 150, 200, 300, 500]
- **strength (Perturbación)**: Elegido de [1, 2, 3]

### Validación
Cada AST se valida según:
1. ✓ Tipo correcto (ASTNode)
2. ✓ Profundidad en rango [min_depth, max_depth]
3. ✓ Tamaño en rango [3, 100]

## Salida

### Estructura de Algoritmo Generado

```json
{
  "id": 1,
  "name": "GAA_Algorithm_1",
  "ast": {
    "type": "Seq",
    "body": [
      {
        "type": "GreedyConstruct",
        "heuristic": "Savings",
        "alpha": 0.25
      },
      {
        "type": "LocalSearch",
        "operator": "TwoOpt",
        "max_iterations": 100
      }
    ]
  },
  "pattern": "simple",
  "seed": 42,
  "timestamp": "2026-01-02T14:30:45.123456",
  "stats": {
    "depth": 2,
    "size": 3,
    "num_constructive": 1,
    "num_improvement": 1,
    "num_perturbation": 0,
    "num_control": 1
  }
}
```

### Archivos Generados
- `algorithms/GAA_Algorithm_1.json` - Algoritmo 1
- `algorithms/GAA_Algorithm_2.json` - Algoritmo 2
- `algorithms/GAA_Algorithm_3.json` - Algoritmo 3
- `algorithms/_algorithms.json` - Índice con metadata global

## Integración

El módulo GAA se integra en `scripts/experiments.py`:

```python
from gaa import AlgorithmGenerator

# Durante la ejecución de experimentos
gaa_gen = AlgorithmGenerator(seed=42)
gaa_algos = gaa_gen.generate_three_algorithms()
gaa_gen.save_algorithms(gaa_algos)

# Cada algoritmo generado tiene:
# - Estructura AST validada
# - Pseudocódigo interpretable
# - Estadísticas de complejidad
# - Metadata de generación
```

## Próximas Fases

1. **Intérprete (interpreter.py)**: Ejecutar AST generado en instancias reales
2. **Operadores Genéticos**: Mutación y crossover de AST
3. **Evaluador**: Evaluar fitness de algoritmos generados
4. **Selector**: Seleccionar mejores algoritmos por torneo

## Referencias

- Documento: `10-gaa-ast-implementation.md`
- Documento: `11-buenas-practicas-gaa.md`
- Proyecto similar: `GAA-GCP-ILS-4` (coloring problems)
