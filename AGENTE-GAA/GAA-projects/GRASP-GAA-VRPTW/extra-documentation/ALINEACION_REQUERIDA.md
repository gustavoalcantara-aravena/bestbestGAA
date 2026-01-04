# 🔍 ALINEACIÓN REQUERIDA: Generator ↔ Validator ↔ Parser

## 1️⃣ NODE TYPES: QUÉ DEBE EXISTIR EN CADA MÓDULO

### ✅ EN VALIDATOR (DEFINIDO)
```python
DEFAULT_ALLOWED_NODE_TYPES = {
    "Const", "Feature",
    "Add", "Sub", "Mul", "Div",
    "Less", "Greater", "And", "Or",
    "If", "Normalize", "Clip", "Choose",
    "WeightedSum"
}
```

### ✅ EN GENERATOR (DEBE GENERAR SOLO ESTOS TIPOS)
Verificar que `_gen_numeric_expr()` y `_gen_bool_expr()` generan SOLO tipos en DEFAULT_ALLOWED_NODE_TYPES.

**Tipos esperados por fase:**

**Construction phase** (retorna `float`):
- Const, Feature
- Add, Sub, Mul, Div
- If
- Normalize, Clip
- WeightedSum

**Local Search phase** (retorna `str`):
- Choose (selector de operador)
- If (selector condicional)
- Las comparaciones booleanas (Less, Greater, And, Or) deben estar en ramas booleanas

### ✅ EN PARSER (DEBE IMPLEMENTAR EVALUATE() PARA TODOS)

```python
class ASTParser:
    def parse(self, ast: Dict) -> Node:
        """Retorna objeto Node con evaluate(state) -> float|str"""
        
    # Internamente debe tener:
    def _parse_const(self, node) -> ConstNode
    def _parse_feature(self, node) -> FeatureNode
    def _parse_add(self, node) -> AddNode
    def _parse_sub(self, node) -> SubNode
    # ... etc para todos los tipos
```

---

## 2️⃣ CAMPOS DE NODOS: QUÉ ESTRUCTURA ESPERA CADA UNO

### ✅ NUMERIC OPERATORS (retornan float)

**Add, Sub, Mul, Div:**
```json
{
  "type": "Add",
  "left": { "type": "Feature", "name": "route_load" },
  "right": { "type": "Const", "value": 10 }
}
```

**Campos obligatorios:** `left`, `right`
**Validador verifica:** ambos existen y son tipo numérico
**Parser hace:** `left_val + right_val`

---

### ✅ BOOLEAN OPERATORS (retornan bool, para If y Choose)

**Less, Greater, And, Or:**
```json
{
  "type": "Less",
  "left": { "type": "Feature", "name": "route_load" },
  "right": { "type": "Const", "value": 100 }
}
```

**Campos obligatorios:** `left`, `right`
**Validador verifica:** comparaciones válidas
**Parser hace:** `left_val < right_val`

---

### ✅ CONTROL FLOW (If, Choose)

**If (retorna float o str según rama):**
```json
{
  "type": "If",
  "condition": { "type": "Less", "left": {...}, "right": {...} },
  "then": { "type": "Add", ... },
  "else": { "type": "Const", "value": 0 }
}
```

**Campos obligatorios:** `condition`, `then`, `else`
**Validador verifica:** condition es booleano, then/else mismo tipo
**Parser hace:** evaluar condition, retornar then o else

---

**Choose (selector de operador para Local Search):**
```json
{
  "type": "Choose",
  "options": [
    {"weight": 0.3, "value": "TwoOpt"},
    {"weight": 0.5, "value": "Relocate"},
    {"weight": 0.2, "value": "OrOpt"}
  ]
}
```

**Campos obligatorios:** `options` (array de objects con `weight` y `value`)
**Validador verifica:** suma de weights ≈ 1, todos valores son operadores válidos
**Parser hace:** seleccionar según pesos aleatorios (con RNG)

---

### ✅ AGREGACIÓN (Normalize, Clip, WeightedSum)

**Normalize (escala a [0,1]):**
```json
{
  "type": "Normalize",
  "expr": { "type": "Feature", "name": "utilization" },
  "min": 0.0,
  "max": 1.0
}
```

**Clip (limita a rango):**
```json
{
  "type": "Clip",
  "expr": { "type": "Add", ... },
  "min": 0,
  "max": 100
}
```

**WeightedSum (suma ponderada):**
```json
{
  "type": "WeightedSum",
  "terms": [
    {"weight": 0.5, "expr": { "type": "Feature", "name": "urgency" }},
    {"weight": 0.3, "expr": { "type": "Feature", "name": "utilization" }},
    {"weight": 0.2, "expr": { "type": "Const", "value": 1.0 }}
  ]
}
```

---

## 3️⃣ FEATURES DISPONIBLES: ESTADO CONGELADO

### Construction Phase State
```python
CONSTRUCTION_STATE_KEYS = {
    "route_length",           # int: número de clientes en ruta
    "route_load",             # float: carga actual de ruta
    "route_capacity_remaining",  # float: capacidad disponible
    "route_current_time",     # float: tiempo actual en ruta
    "cust_demand",            # float: demanda del cliente a insertar
    "cust_ready_time",        # float: earliest time window del cliente
    "cust_due_time",          # float: latest time window del cliente
    "delta_distance",         # float: distancia al insertar
    "urgency",                # float: [0,1] qué tan urgente es el cliente
    "utilization",            # float: [0,1] qué tan cargada está la ruta
}
```

**El generator SOLO puede usar features que existan en este diccionario.**

### Local Search Phase State
```python
LOCAL_SEARCH_STATE_KEYS = {
    "num_routes",            # int: número de rutas
    "total_distance",        # float: distancia total actual
    "penalty_value",         # float: penalización por infeasibility
    "iterations_no_improve", # int: iteraciones sin mejora
    "temperature",           # float: [0,1] temperatura para aceptación
    "acceptance_threshold",  # float: threshold para aceptar worse moves
    "feasibility_score",     # float: [0,1] qué tan factible es
}
```

---

## 4️⃣ VALIDACIÓN: QUÉ CHECA EL VALIDATOR

Para cada AST generado, el validator debe verificar:

### Type Safety
- ✅ Cada nodo tiene field "type"
- ✅ Type está en DEFAULT_ALLOWED_NODE_TYPES
- ✅ Todos los campos obligatorios existen

### Return Type Consistency
- ✅ Construction AST retorna float
- ✅ Local Search AST retorna str (nombre de operador)
- ✅ If nodes: then/else tienen mismo tipo retorno

### Structure Validity
- ✅ Profundidad ≤ max_depth (default 10)
- ✅ Número de nodos funcionales ≤ max_functional_nodes (default 50)
- ✅ Número total de nodos ≤ max_total_nodes (default 500)

### Feature Validity
- ✅ Feature names existen en estado correspondiente (construction vs local_search)
- ✅ No hay features undefined

---

## 5️⃣ PARSER: QUÉ DEBE IMPLEMENTAR

```python
class Node:
    """Interfaz base para todos los nodos AST."""
    def evaluate(self, state: Dict[str, Any]) -> Union[float, str]:
        """Retorna float (para numeric) o str (para operador selector)."""
        raise NotImplementedError

class ConstNode(Node):
    def __init__(self, value: float):
        self.value = value
    
    def evaluate(self, state):
        return self.value

class FeatureNode(Node):
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, state):
        if self.name not in state:
            raise ValueError(f"Feature '{self.name}' not found in state")
        return state[self.name]

class AddNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state):
        return self.left.evaluate(state) + self.right.evaluate(state)

# ... etc para todos los tipos
```

---

## 6️⃣ CHECKLIST ANTES DE EJECUTAR TESTS

- [ ] Generator produce SOLO tipos en DEFAULT_ALLOWED_NODE_TYPES
- [ ] Generator usa SOLO features en CONSTRUCTION_STATE_KEYS (construction) o LOCAL_SEARCH_STATE_KEYS (local_search)
- [ ] Validator tiene reglas para TODOS los tipos permitidos
- [ ] Validator checa que features existen en state correspondiente
- [ ] Parser implementa Node.evaluate() para TODOS los tipos
- [ ] Parser NO usa RNG (es determinista)
- [ ] Parser retorna float para construction, str para local_search

---

## 7️⃣ TESTING ITERATIVO

**Orden recomendado:**

1. **TestASTLanguageAlignment** ← Primero este (identifica qué falta)
2. **TestStateContracts** ← Validar que states están correctos
3. **TestASTRoundTrip** ← El test más importante (generation → validation → parsing)
4. **TestDeterminism** ← Verificar reproducibilidad
5. **TestSolomonAndBKS** ← Verificar data loading
6. **TestSolutionPool** ← Verificar almacenamiento
7. **TestLogging** ← Verificar auditoría
8. **TestCanaryRun** ← End-to-end

**Si falla TestASTLanguageAlignment:**
→ Hay mismatch entre Generator, Validator, Parser. Arreglar antes de continuar.

**Si falla TestASTRoundTrip:**
→ Hay bug en generation, validation, o parsing. Debuguear exactamente dónde con test.

**Si falla TestDeterminism:**
→ Hay RNG donde no debería haber (ej: en Parser o Validator). Removr.

---

## 8️⃣ INTEGRACIÓN CON GRASP

Solo después de pasar TODOS los tests del checklist:

```python
from grasp.grasp_solver import GRASPSolver

# 1. Cargar instancia Solomon (requiere SolomonLoader)
instance = load_solomon("C101.txt")

# 2. Generar 1 algoritmo
gen = RandomASTGenerator(seed=42)
ast_const = gen.generate(phase="construction", seed=42)
ast_ls = gen.generate(phase="local_search", seed=42)

# 3. Validar (debe pasar)
validator = ASTValidator()
assert validator.validate_construction_ast(ast_const).ok
assert validator.validate_local_search_ast(ast_ls).ok

# 4. Parsear (debe dar Node con evaluate())
parser = ASTParser()
const_scorer = parser.parse(ast_const)
ls_selector = parser.parse(ast_ls)

# 5. Ejecutar GRASP
solver = GRASPSolver(instance, const_scorer, ls_selector)
best_solution = solver.solve(max_iterations=100)

# 6. Evaluar contra BKS
bks = load_bks_file("best_known_solutions.json")
gap = compute_gap(best_solution, bks["C101"])

# 7. Loguear
log_entry({
    "algorithm_id": "algo_1",
    "seed": 42,
    "instance_id": "C101",
    "vehicles": best_solution["vehicles"],
    "distance": best_solution["distance"],
    "gap_percent": gap,
    "feasible": best_solution["feasible"],
})
```

---

**Estado Actual:**
- ✅ Tests creados (test_checklist_alignment.py)
- ✅ Alineación especificada
- ❌ Generator/Validator/Parser aún no fully wired
- ⏳ Siguientes pasos: verificar alineación real en código
