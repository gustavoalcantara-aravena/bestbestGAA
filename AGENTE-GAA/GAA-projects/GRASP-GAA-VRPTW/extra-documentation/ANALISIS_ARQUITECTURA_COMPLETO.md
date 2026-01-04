# 🏗️ ANÁLISIS ARQUITECTÓNICO - PROYECTO GRASP-GAA-VRPTW

**Fecha:** 4 de Enero, 2026  
**Objetivo:** Comprender el flujo completo y cómo se conectan todos los componentes

---

## 📚 ÍNDICE

1. [Visión General](#visión-general)
2. [Flujo de Ejecución](#flujo-de-ejecución)
3. [Módulos Principales](#módulos-principales)
4. [Flujo de Datos](#flujo-de-datos)
5. [Estado Actual de Implementación](#estado-actual-de-implementación)
6. [Dependencias entre Módulos](#dependencias-entre-módulos)
7. [Ciclo de Vida del Experimento](#ciclo-de-vida-del-experimento)

---

## 🎯 Visión General

### ¿QUÉ ES ESTE PROYECTO?

**GRASP-GAA-VRPTW** es un sistema de **Generación Automática de Algoritmos** (GAA) que:

1. **Genera algoritmos** (ASTs - Abstract Syntax Trees) automáticamente
2. **Los usa** para resolver VRPTW (Vehicle Routing Problem with Time Windows)
3. **Los evalúa** contra benchmark Solomon con 56 instancias
4. **Los mejora** iterativamente usando GP (Genetic Programming)

### ESTRUCTURA A ALTO NIVEL

```
┌─────────────────────────────────────────────────────────┐
│                   ENTRADA: CONFIG                       │
│  (config.yaml: seed, instancias, parámetros)           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             CARGADOR DE DATOS                          │
│  • SolomonLoader: lee 56 instancias .txt               │
│  • BKSLoader: carga best-known-solutions               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          GENERADOR DE ALGORITMOS (GAA)                 │
│  • RandomASTGenerator: crea ASTs aleatorios            │
│  • ASTValidator: valida restricciones                  │
│  • AlgorithmGenerator: orquesta generación + retries   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            SOLVER GRASP + AST EVALUACIÓN              │
│  • GRASPSolver: metaheurística base                    │
│  • ASTParser: convierte JSON → ejecutable              │
│  • InsertionState: contexto para evaluación            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              EVALUACIÓN Y VALIDACIÓN                   │
│  • SolutionEvaluator: calcula fitness                  │
│  • BKSValidation: compara vs BKS                       │
│  • SolutionPool: ranking de mejores soluciones         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           LOGGING Y RESULTADOS (JSONL)                 │
│  • ExperimentRunner: orquestador final                 │
│  • Logger: escribe métricas por solución               │
│  • Reportes: estadísticas agregadas                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Ejecución

### PASO 1: INICIALIZACIÓN

```python
# 1. Cargar configuración
config = load_config("config/config.yaml")

# 2. Set reproducibilidad
random.seed(config["random"]["global_seed"])  # 42

# 3. Cargar datos
data_loader = SolomonLoader(config["dataset"]["root_dir"])
bks_loader = BKSLoader(config["bks"]["file"])
```

**Entrada:** `config/config.yaml`  
**Salida:** Estructuras de datos en memoria

---

### PASO 2: GENERACIÓN DE ALGORITMOS

```python
# 1. Crear generador de AST
ast_gen = RandomASTGenerator(
    rng=random.Random(seed=42),
    construction_features=[...],
    ls_features=[...],
    ls_operators=["relocate", "swap", "two_opt", ...]
)

# 2. Crear validador
validator = ASTValidator(
    config=ASTValidationConfig(max_depth=3, max_function_nodes=2),
    construction_features=set([...]),
    ls_features=set([...]),
    allowed_operators=set([...])
)

# 3. Generar N algoritmos (con reintentos)
alg_gen = AlgorithmGenerator(
    rng_seed=42,
    ast_generator=ast_gen,
    ast_validator=validator,
    max_attempts_per_algorithm=50
)

# Si validación falla → reintentar hasta max_attempts
algorithms = alg_gen.generate_algorithms(
    n_algorithms=10,
    phase="construction",
    export_path="output/algorithms_construction.json"
)
```

**Entrada:** Límites de AST (profundidad, funciones)  
**Salida:** JSON con ASTs validos + metadatos  
**Manejo de errores:** Si JSON inválido → reintentar (FIX B aplicado)

---

### PASO 3: EJECUCIÓN DEL SOLVER

Para cada algoritmo generado:

```python
# 1. Parse AST JSON → ejecutable
parser = ASTParser(rng=random.Random(seed))
algo_exec = {
    "construction_ast": parser.parse(algo_json["construction_ast"]),
    "ls_operator_ast": parser.parse(algo_json["ls_operator_ast"])
}

# 2. Inicializar GRASP solver
solver = GRASPSolver(
    config=grasp_config,
    construction_ast=algo_exec["construction_ast"],
    ls_operator_ast=algo_exec["ls_operator_ast"]
)

# 3. Para cada instancia Solomon (ej. C101):
for instance in instances:
    
    # 3a. Leer instancia
    inst_data = data_loader.load(instance.id)
    
    # 3b. Ejecutar GRASP
    solution = solver.solve(inst_data, max_iterations=100)
    
    # 3c. Evaluar solución
    metrics = evaluate_solution(solution, inst_data)
    
    # 3d. Comparar vs BKS
    bks = bks_loader.get(instance.id)
    comparison = validate_solution_vs_bks(metrics, bks)
    
    # 3e. Log resultado
    logger.log_jsonl({
        "timestamp": now(),
        "algorithm_id": algo_json["algorithm_id"],
        "instance_id": instance.id,
        "n_vehicles": metrics["n_vehicles"],
        "total_distance": metrics["total_distance"],
        "gap_percent": comparison.distance_gap_percent,
        "feasible": comparison.feasible,
        "dominates_bks": comparison.dominates_bks,
        ...
    })
```

**Entrada:** AST ejecutable + Instancia Solomon  
**Proceso:** 100 iteraciones de GRASP, evaluación por iteración  
**Salida:** Mejor solución encontrada + métricas

---

### PASO 4: AGREGACIÓN DE RESULTADOS

```python
# 1. Leer logs JSONL
results = read_jsonl("logs/experiment_20260104_143000.jsonl")

# 2. Calcular estadísticas
stats = compute_aggregate_statistics(results)
# {
#   "total_runs": 560,  (10 algos × 56 instancias)
#   "feasible_count": 555,
#   "feasible_percent": 99.1%,
#   "avg_gap_percent": 2.34%,
#   "dominates_count": 8
# }

# 3. Generar reportes
print_summary(stats)
save_json("output/summary.json", stats)
```

---

## 🔧 Módulos Principales

### 1. **DATA LOADERS** (`src/data/`)

#### `loader_solomon.py`
- **Función:** Lee archivos Solomon .txt
- **Entrada:** Ruta a archivo (ej. "C101.txt")
- **Salida:** Dict con nodos, matriz de distancias, capacity, time windows

```python
loader = SolomonLoader("data/Solomon-VRPTW-Dataset/")
instance = loader.load("C101")
# {
#   "instance_id": "C101",
#   "n_customers": 100,
#   "capacity": 200,
#   "nodes": [{...}, ...],
#   "distance_matrix": [[...], ...],
#   "time_matrix": [[...], ...]
# }
```

#### `bks_loader.py`
- **Función:** Carga best-known-solutions
- **Entrada:** JSON o CSV con mejores soluciones conocidas
- **Salida:** Dict indexado por instance_id

```python
bks_loader = BKSLoader("data/bks_solomon.json")
bks = bks_loader.get("C101")
# BKSEntry(instance_id="C101", n_vehicles=10, total_distance=828.94)
```

---

### 2. **AST GENERATION** (`src/ast/`)

#### `generator.py` - `RandomASTGenerator`
- **Responsabilidad:** Generar ASTs válidos aleatoriamente
- **Método principal:** `generate_algorithm_json(algorithm_id, seed)`
- **Salida:** JSON con dos ASTs (construction + local_search)

```python
gen = RandomASTGenerator(
    rng=rng,
    construction_features=["urgency", "distance", "load_ratio", ...],
    ls_features=["num_routes", "total_distance", "iterations_no_improve", ...],
    ls_operators=["relocate", "swap", "two_opt", ...],
    limits=GenLimits(max_depth=3, max_function_nodes=2)
)

algo_json = gen.generate_algorithm_json("algo1", seed=42)
# {
#   "algorithm_id": "algo1",
#   "construction_ast": {...},  # Expresión numérica para scoring
#   "ls_operator_ast": {...}     # Decisión de operador (string)
# }
```

#### `validator.py` - `ASTValidator`
- **Responsabilidad:** Validar restricciones de AST
- **Validaciones:**
  - ✓ Profundidad ≤ max_depth
  - ✓ Funciones ≤ max_function_nodes
  - ✓ Type correctness (numeric vs boolean vs categorical)
  - ✓ Features existen en fase correspondiente
  - ✓ Operadores válidos (si AST de LS)

```python
validator = ASTValidator(
    config=ASTValidationConfig(max_depth=3, max_function_nodes=2),
    construction_features=set([...]),
    ls_features=set([...]),
    allowed_operators=set(["relocate", "swap", ...])
)

result = validator.validate_construction_ast(ast_json)
# ValidationResult(
#   ok=True,
#   errors=[],
#   stats={"total_nodes": 12, "max_depth_real": 3, ...}
# )
```

#### `parser.py` - `ASTParser`
- **Responsabilidad:** Convertir JSON → código ejecutable
- **Entrada:** JSON del AST
- **Salida:** Objeto con método `evaluate(state)`

```python
parser = ASTParser(rng=rng)
ast_root = parser.parse(ast_json)

# Durante ejecución GRASP:
insertion_state = {
    "route_length": 5,
    "urgency": 0.8,
    "distance": 15.3,
    ...
}
score = ast_root.evaluate(insertion_state)  # ← Retorna float
```

---

### 3. **ALGORITHM GENERATOR** (`src/gaa/`)

#### `algorithm_generator.py` - `AlgorithmGenerator`
- **Responsabilidad:** Orquestar generación + validación + retries
- **Lógica:**
  1. Generar AST con RandomASTGenerator
  2. Validar con ASTValidator
  3. Si inválido → reintentar (hasta max_attempts=50)
  4. Si válido → exportar JSON

```python
alg_gen = AlgorithmGenerator(
    rng_seed=42,
    ast_generator=ast_gen,
    ast_validator=validator,
    max_attempts_per_algorithm=50
)

algorithms = alg_gen.generate_algorithms(
    n_algorithms=10,
    phase="construction",
    export_path="output/algorithms.json"
)
```

---

### 4. **GRASP SOLVER** (`src/grasp/`)

#### `grasp_solver.py` - `GRASPSolver`
- **Responsabilidad:** Metaheurística GRASP con AST
- **Lógica:**
  1. **Construcción:** Insertar clientes uno a uno usando AST construction
  2. **Local Search:** Aplicar operadores seleccionados por AST LS
  3. **Actualización:** Mantener mejor solución encontrada

```python
solver = GRASPSolver(
    config=grasp_config,
    construction_ast=algo_exec["construction_ast"],
    ls_operator_ast=algo_exec["ls_operator_ast"]
)

solution = solver.solve(
    instance=inst_data,
    max_iterations=100,
    alpha=0.25  # RCL parameter
)

# Retorna Solution con:
# - routes: [[0, i, j, 0], ...]
# - n_vehicles, total_distance
# - metrics: {...}
```

---

### 5. **EVALUATION** (`src/evaluation/`)

#### `solution_evaluator.py`
- **Responsabilidad:** Evaluar solución VRPTW
- **Funciones:**
  - `evaluate_route()`: Calcula distancia, violaciones por ruta
  - `evaluate_solution()`: Suma todas las rutas
  - `validate_all_constraints()`: Verifica 7 restricciones VRPTW
  - `compute_gap()`: Calcula brecha vs BKS

```python
metrics = evaluate_solution(solution, instance)
# {
#   "n_vehicles": 10,
#   "total_distance": 850.5,
#   "capacity_violation": 0,
#   "time_violation": 0,
#   "feasible": True
# }
```

#### `bks_validation.py` - `BKSComparison`
- **Responsabilidad:** Comparar solución vs BKS
- **Campos:**
  - `gap_percent`: (sol - bks) / bks × 100
  - `dominates_bks`: ¿Mejor que BKS?
  - `lexicographic_comparison`: -1/0/+1

```python
comparison = validate_solution_vs_bks(metrics, bks)

if comparison.dominates_bks:
    print(f"✓ {instance_id}: Gap {comparison.distance_gap_percent:.2f}%")
else:
    print(f"✗ {instance_id}: Gap {comparison.distance_gap_percent:.2f}%")
```

---

### 6. **EXPERIMENT RUNNER** (`src/experiment_runner.py`)

- **Responsabilidad:** Orquestar experimento completo
- **Lógica:**
  1. Cargar configuración
  2. Cargar datos + BKS
  3. Para cada instancia + algoritmo:
     - Ejecutar GRASP
     - Evaluar solución
     - Validar vs BKS
     - Loguear resultado (JSONL)
  4. Calcular estadísticas agregadas
  5. Generar reportes

```python
runner = ExperimentRunner(config_path="config/config.yaml")
results = runner.run_experiment()
# {
#   "experiment_id": "abc123",
#   "total_runs": 560,
#   "successful_runs": 555,
#   "aggregate_stats": {...},
#   "duration_seconds": 3245.6
# }
```

---

## 📊 Flujo de Datos

```
CONFIG.yaml
    ↓
[Reproducibilidad: seed=42]
    ↓
┌─────────────────────────────────┐
│   Solomon Instances (56)        │
│   "C101.txt" → inst_data        │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   BKS (best-known-solutions)    │
│   "C101" → (k=10, d=828.94)     │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   AST Generation (retries si inválido)          │
│   RandomASTGenerator → JSON AST                 │
│   ↓ Validador (profundidad, funciones, type)   │
│   ↓ OK → Parser → Ejecutable                   │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   GRASP Solver Loop                            │
│   ┌──────────────────────────────────────────┐ │
│   │ iter=1..100:                             │ │
│   │  • Construction: InsertionState (AST)    │ │
│   │  • Local Search: Operadores (AST)        │ │
│   │  • Evalúa: SolutionEvaluator             │ │
│   │  • Track mejor: SolutionPool             │ │
│   └──────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   Mejor Solución                               │
│   {n_vehicles, total_distance, feasible}       │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   Evaluación Final                             │
│   • validate_solution_vs_bks()                 │
│   • Calcula gap, dominates, lexicographic     │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   Log JSONL                                    │
│   {"timestamp", "algorithm_id", "instance_id", │
│    "gap_percent", "feasible", "dominates", ...}│
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│   Estadísticas Agregadas                       │
│   {avg_gap, dominates_count, feasible_percent} │
└──────────────────────────────────────────────────┘
```

---

## 🔴 Estado Actual de Implementación

### ✅ COMPLETO (100%)

| Componente | Líneas | Status |
|-----------|--------|--------|
| config.yaml | 177 | ✅ Completo |
| BKSLoader | 150 | ✅ Completo |
| BKSValidation | 260 | ✅ Completo |
| RandomASTGenerator | 407 | ✅ Completo |
| ASTValidator | 420 | ✅ Completo (FIX B aplicado) |
| ExperimentRunner | 200 | ✅ Completo |
| SolutionEvaluator | 211 | ✅ Basico (80% pendiente) |

### 🟡 PARCIAL (20-50%)

| Componente | Líneas | Status |
|-----------|--------|--------|
| ASTParser | - | 🟡 Importado pero NO existe |
| GRASPSolver | - | 🟡 Muy basico |
| SolomonLoader | - | 🟡 Esqueleto |
| AlgorithmGenerator | 202 | 🟡 Estructura OK |

### ⚠️ BLOQUEADOR

**ASTParser NO EXISTE.** Sin él:
- ❌ No puedes ejecutar ASTs
- ❌ No puedes correr GRASP
- ❌ No puedes evaluar algoritmos

---

## 🔗 Dependencias entre Módulos

```
main.py
  ├─→ config.yaml [config]
  │
  ├─→ data/loader_solomon.py [instancias]
  ├─→ data/bks_loader.py [BKS]
  │
  ├─→ ast/generator.py [RandomASTGenerator]
  │   └─→ ast/validator.py [ASTValidator]
  │       └─→ ast/typesystem.py [type inference]
  │
  ├─→ ast/parser.py [ASTParser] ⚠️ FALTA
  │   └─→ Convierte JSON → ejecutable
  │
  ├─→ grasp/grasp_solver.py [GRASPSolver]
  │   ├─→ ast/parser.py (para evaluar AST)
  │   └─→ evaluation/solution_evaluator.py
  │
  ├─→ evaluation/bks_validation.py [BKSComparison]
  │   └─→ evaluation/solution_evaluator.py
  │
  └─→ experiment_runner.py [ExperimentRunner]
      └─→ Orquesta todo
```

---

## ⏳ Ciclo de Vida del Experimento

### SEMANA 1: SETUP + VALIDACIÓN BÁSICA

```
DÍA 1-2: Parser de Solomon
  ├─ Leer 56 archivos .txt
  ├─ Validar n_customers=100, depot=0
  ├─ TEST-1.1 PASS
  └─ ⏱️ 2 horas

DÍA 3-5: Evaluador + BKS
  ├─ Evalúar rutas (distancia, ventanas)
  ├─ Comparar vs BKS
  ├─ TEST-4.1, 4.2, 4.3 PASS
  └─ ⏱️ 6 horas

SUBTOTAL SEMANA 1: 8 horas ✓
```

### SEMANA 2: GENERACIÓN DE AST

```
DÍA 6-10: ASTParser + Validador reforzado
  ├─ Convertir JSON → ejecutable
  ├─ Manejo seguro de KeyError (FIX B)
  ├─ TEST-5.1, 5.2, 5.3 PASS
  ├─ TEST-0.1 (Infraestructura) PASS
  └─ ⏱️ 10 horas

SUBTOTAL SEMANA 2: 10 horas ✓
```

### SEMANA 3: GRASP + LOCAL SEARCH

```
DÍA 11-15: GRASPSolver
  ├─ Construcción: 100 iteraciones
  ├─ Local search: Operadores
  ├─ TEST-6 (Construcción) PASS
  ├─ TEST-7 (Local search) PASS
  └─ ⏱️ 12 horas

SUBTOTAL SEMANA 3: 12 horas ✓
```

### SEMANA 4: INTEGRACIÓN + EJECUCIÓN

```
DÍA 16-20: End-to-end
  ├─ ExperimentRunner completo
  ├─ Logging JSONL
  ├─ TEST-10, 11, 12 PASS
  ├─ Prueba piloto (C101 × 3 algos)
  └─ ⏱️ 10 horas

SUBTOTAL SEMANA 4: 10 horas ✓

TOTAL 4 SEMANAS: 40 horas de coding
```

---

## 📋 CHECKLIST DE COMPRENSIÓN

- [x] ¿Cómo se cargan las instancias Solomon?
- [x] ¿Cómo se generan ASTs aleatorios?
- [x] ¿Cómo se validan antes de usar?
- [x] ¿Cómo se ejecutan en GRASP?
- [x] ¿Cómo se evalúan las soluciones?
- [x] ¿Cómo se comparan con BKS?
- [x] ¿Cómo se loguean resultados?
- [x] ¿Dónde están los "blockers"?
- [ ] TODO: Implementar ASTParser (BLOCKER #1)
- [ ] TODO: Completar GRASPSolver
- [ ] TODO: Completar SolomonLoader

---

**Status:** 🟡 ARQUITECTURA CLARA, IMPLEMENTATION 30% COMPLETADA

**Blocker crítico:** ASTParser (sin él no se puede ejecutar nada)  
**Próximo paso:** Implementar ASTParser + arreglar GRASPSolver basico
