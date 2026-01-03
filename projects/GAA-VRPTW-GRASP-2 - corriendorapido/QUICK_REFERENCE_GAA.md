# Quick Reference: GAA, Operadores y AST

**Guía de Consulta Rápida para Desarrolladores**

---

## 1. Componentes Principales

| Componente | Ubicación | Líneas | Función |
|-----------|-----------|--------|----------|
| Grammar | `gaa/grammar.py` | 116 | Define 18 operadores, valida AST |
| AST Nodes | `gaa/ast_nodes.py` | 335 | 7 tipos de nodos (Seq, If, While, For, etc) |
| Generator | `gaa/generator.py` | 410 | Genera 4 patrones, reproducible con seed |
| Integration | `scripts/experiments.py` | 583 | Ejecuta GRASP/VND/ILS con algoritmos GAA |

---

## 2. Los 18 Operadores

### Constructivos (6)
| # | Nombre | Alpha | Complejidad | Nota |
|---|--------|-------|-------------|------|
| 1 | NearestNeighbor | [0.1-0.5] | O(n²) | Rápido, calidad media |
| 2 | Savings | [0.1-0.5] | O(n²) | Clarke-Wright |
| 3 | Sweep | [0.1-0.5] | O(n·log n) | Para C1, C2 |
| 4 | TimeOrientedNN | [0.1-0.5] | O(n²) | VRPTW específico |
| 5 | RegretInsertion | [0.1-0.5] | O(n²) | Buena calidad |
| 6 | RandomizedInsertion | [0.1-0.5] | O(n²) | Diversidad |

### Mejora (8)
| # | Nombre | Max Iterations | Complejidad | Mejora Típica |
|---|--------|---|-------------|--------------|
| 1 | TwoOpt | [1-500] | O(n²) | 5-10% |
| 2 | OrOpt | [1-500] | O(n²) | 2-5% |
| 3 | ThreeOpt | [1-500] | O(n³) | 8-15% |
| 4 | Relocate | [1-500] | O(n²) | 1-3% |
| 5 | Exchange | [1-500] | O(n²) | 2-4% |
| 6 | GENI | [1-500] | O(n²) | 4-8% |
| 7 | LKH | [1-500] | O(n²-n³) | 10-20% |
| 8 | VND | [1-500] | O(n²·k) | 15-25% |

### Perturbación (4)
| # | Nombre | Strength | Alcance | Uso |
|---|--------|----------|--------|-----|
| 1 | RandomRouteRemoval | [1-5] | Alta | ILS, COMPLEX |
| 2 | WorseFeasibleMove | [1-5] | Baja | ILS iterativo |
| 3 | RandomRelocate | [1-5] | Media | ILS diverso |
| 4 | SegmentShift | [1-5] | Media | ILS gradual |

---

## 3. Los 4 Patrones de Generación

| Patrón | Profundidad | Tamaño | Estructura | Frecuencia |
|--------|-----------|--------|-----------|-----------|
| **Simple** | 2 | 3 | Seq(Greedy, LocalS) | 25% |
| **Iterativo** | 4 | 6 | Seq(Greedy, While(Seq(LocalS, Perturb))) | 25% |
| **Multistart** | 3-4 | 4 | For(Seq(Greedy, LocalS)) | 25% |
| **Complejo** | 4-5 | 7-8 | Seq(Greedy, While(If(LocalS, Perturb))) | 25% |

---

## 4. Nodos AST: Propiedades

### Nodos de Control
```
Seq:     body: List[ASTNode]
If:      condition: str, then_branch, else_branch
While:   condition: str, max_iterations: int, body
For:     iterations: int, body

Métodos:
  depth() → int
  size() → int
  get_all_nodes() → List[ASTNode]
  to_pseudocode() → str
  to_dict() → Dict
```

### Nodos de Operadores
```
GreedyConstruct:
  heuristic: str (uno de 6)
  alpha: float ∈ [0.1, 0.5]

LocalSearch:
  operator: str (uno de 8)
  max_iterations: int ∈ [1, 500]

Perturbation:
  operator: str (uno de 4)
  strength: int ∈ [1, 5]
```

---

## 5. Validación de AST

```python
grammar = Grammar()
errors = grammar.validate_ast(ast)

Checks automáticos:
  ✓ Profundidad ∈ [2, 5]
  ✓ Tamaño ∈ [3, 100]
  ✓ Operadores válidos
  ✓ Estructura correcta
```

---

## 6. Estadísticas de Algoritmo

Obtenidas automáticamente con `grammar.get_statistics(ast)`:

```python
{
  'depth': int,                 # ∈ [2, 5]
  'size': int,                  # ∈ [3, 100]
  'num_constructive': int,      # ≥ 1
  'num_improvement': int,       # ≥ 1
  'num_perturbation': int       # ≥ 0
}
```

---

## 7. Reproducibilidad

### Con Seed=42
```
Gen1(seed=42) → [simple, simple, iterative]
Gen2(seed=42) → [simple, simple, iterative]
Gen3(seed=42) → [simple, simple, iterative]
```

### Mecanismo
```python
for i in range(3):
    random.seed(42 + i)  # Seeds: 42, 43, 44
    ast = generate()     # Determinístico
```

---

## 8. Flujo de Ejecución

### Paso 1: Generación
```python
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()
# Retorna: [algo1, algo2, algo3] con AST completo
```

### Paso 2: Ejecución
```python
for algo in algos:
    for instance in instances:
        grasp = GRASP(...)
        result = grasp.solve(instance)
        # Usa operadores del AST
```

### Paso 3: Resultados
```python
raw_results.csv:
  algorithm | instance | k | d | time
  GRASP     | R101     | 11| 1234.5 | 2.34
  VND       | R101     | 10| 1210.2 | 3.21
  ILS       | R101     | 10| 1198.7 | 5.45
```

---

## 9. Comandos Típicos

### Generar Algoritmos
```python
from gaa import AlgorithmGenerator

gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()
gen.save_algorithms(algos, 'algorithms/')
```

### Validar AST
```python
from gaa import Grammar

grammar = Grammar()
errors = grammar.validate_ast(ast)
if not errors:
    print("AST válido")
```

### Generar Estadísticas
```python
stats = grammar.get_statistics(ast)
print(f"Depth: {stats['depth']}, Size: {stats['size']}")
```

### Ejecutar Experimento
```bash
cd scripts/
python experiments.py --mode QUICK   # ~10 min, 12 instancias
python experiments.py --mode FULL    # ~45 min, 56 instancias
```

---

## 10. Archivos Generados

### Algoritmos
```
algorithms/
├── GAA_Algorithm_1.json    (AST + metadatos)
├── GAA_Algorithm_2.json
├── GAA_Algorithm_3.json
└── _algorithms.json        (índice)
```

### Resultados Experimento
```
output/
├── raw_results.csv         (36 o 168 filas)
├── experiment_metadata.json
├── plots/
│   ├── k_distribution.png
│   ├── distance_distribution.png
│   ├── time_comparison.png
│   └── ...
└── summary_report.txt
```

---

## 11. Parámetros Clave

| Parámetro | Valor | Rango | Nota |
|-----------|-------|-------|------|
| Seed | 42 | int | Reproducibilidad |
| Min Depth | 2 | [1,∞] | Mínimo complejidad |
| Max Depth | 5 | [2,∞] | Máxima complejidad |
| Min Size | 3 | [1,∞] | Mínimo nodos |
| Max Size | 100 | [3,∞] | Máximo nodos |
| Alpha (Greedy) | [0.1, 0.5] | float | Aleatorización |
| Max Iter (LocalS) | [1, 500] | int | Iteraciones búsqueda |
| Strength (Perturb) | [1, 5] | int | Intensidad perturbación |

---

## 12. Matriz de Compatibilidad

```
PATRÓN vs OPERADOR

                     SIMPLE  ITER  MULTI  COMPLEX
Constructivos         ✅     ✅    ✅     ✅
Mejora                ✅     ✅    ✅     ✅
Perturbación          ❌     ✅    ❌     ✅

Nota: Solo en ITERATIVO y COMPLEX se usan perturbaciones
```

---

## 13. Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| AST inválido | Profundidad > 5 | Reducir complejidad |
| Generación lenta | Max attempts bajo | Aumentar a 50 |
| No reproducible | Seed no consistente | Usar seed=42 |
| Operador no existe | Nombre inválido | Ver lista de 18 |

---

## 14. Tests Disponibles

```bash
# Unitarios (39 tests)
python test_gaa_comprehensive.py

# Integración (14 tests)
python test_gaa_integration.py

# Validación rápida
python -c "from gaa import AlgorithmGenerator; \
           gen = AlgorithmGenerator(seed=42); \
           algos = gen.generate_three_algorithms(); \
           print(f'OK: {len(algos)} algoritmos generados')"
```

---

## 15. Documentación Completa

| Documento | Contenido |
|-----------|----------|
| `FLUJOS_EJECUCION_GAA_DETALLADO.md` | Flujos técnicos profundos |
| `DIAGRAMAS_FLUJOS_ASCII.md` | Visualizaciones ASCII |
| `gaa/README.md` | Overview módulo GAA |
| `STATUS_REPORT_GAA.md` | Estado producción |
| `CHECKLIST_GAA_CUMPLIMIENTO.md` | Validación especificación |

---

## 16. Estructura de Directorios

```
GAA-VRPTW-GRASP-2/
├── gaa/
│   ├── __init__.py           (exports)
│   ├── grammar.py            (18 operadores, validación)
│   ├── ast_nodes.py          (7 tipos nodos)
│   └── generator.py          (4 patrones)
│
├── scripts/
│   └── experiments.py        (QUICK/FULL + GAA integration)
│
├── algorithms/               (algoritmos generados)
│   ├── GAA_Algorithm_1.json
│   ├── GAA_Algorithm_2.json
│   ├── GAA_Algorithm_3.json
│   └── _algorithms.json
│
├── test_gaa_comprehensive.py (39 tests)
├── test_gaa_integration.py   (14 tests)
│
└── output/                   (resultados experimentales)
    ├── raw_results.csv
    └── plots/
```

---

**Esta guía permite navegar rápidamente todos los componentes del sistema GAA integrado.**

