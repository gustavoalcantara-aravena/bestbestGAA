# 🔧 ESPECIFICACIÓN TÉCNICA PARA IMPLEMENTACIÓN EXPERTA

## COMPONENTE 1: EVALUADOR DE FITNESS (20% → NECESITA 80%)

**Archivo:** `src/evaluation/solution_evaluator.py` (211 líneas)

### ✅ YA IMPLEMENTADO (20%)

```python
✓ evaluate_route()           → Calcula distancia, violaciones por ruta
✓ evaluate_solution()        → Itera rutas, suma métricas
✓ compute_penalty()          → Penalización escalar (alpha_cap, alpha_time)
✓ compute_fitness()          → Métrica de dos objetivos (vehículos + distancia)
✓ evaluate_solution_full()   → Pipeline one-shot
```

### ❌ FALTA IMPLEMENTAR (80%)

#### 1. **Integración con BKS** (CRÍTICO - TEST-4.3)

```python
FALTA:
  • load_bks_file(path: str) → Dict[str, Tuple[int, float]]
    - Lee CSV/JSON con (instance_id, k_bks, d_bks)
    - Retorna dict: {"C101": (10, 828.94), ...}
    
  • compute_gap(solution_metrics, bks) → float
    - gap_percent = (k_sol - k_bks) / k_bks * 100
    - Si k_sol == k_bks: gap = (d_sol - d_bks) / d_bks * 100
    - Retorna gap_percent normalizado
    
  • validate_vs_bks(solution, instance, bks_dict) → Dict
    - Verifica si solución es mejor que BKS
    - Retorna: {"is_feasible", "gap_percent", "dominates_bks"}
```

#### 2. **Métrica Lexicográfica Correcta** (CRÍTICO - TEST-4.2)

```python
PROBLEMA ACTUAL:
  compute_fitness() usa negación simple: -(w_vehicles * V + w_distance * D)
  
FALTA:
  • lexicographic_compare(sol1, sol2) → int {-1, 0, 1}
    - Compara PRIMERO por vehículos (V1 vs V2)
    - Si empate, LUEGO por distancia (D1 vs D2)
    - Esto es la métrica real de Solomon
    
  • compute_lexicographic_fitness(metrics) → Tuple[int, float]
    - Retorna (num_vehicles, total_distance) como tupla
    - Permite comparación lexicográfica directa
    - NO debe ser escalar
```

#### 3. **Validación Exhaustiva de 7 Restricciones** (TEST-4.1)

```python
FALTA (actualmente solo verifica capacidad y tiempo):
  • validate_all_constraints(solution, instance) → Dict[str, bool]
    
    Restricción 1: Cada cliente visitado exactamente 1 vez
    Restricción 2: Cada ruta sale y llega al depósito
    Restricción 3: Capacidad no excedida por ruta
    Restricción 4: Ventanas de tiempo respetadas
    Restricción 5: Continuidad de rutas (sin nodos huérfanos)
    Restricción 6: Todos los clientes incluidos en alguna ruta
    Restricción 7: No hay rutas vacías (excepto si n_vehículos obligatorio)
    
    Retorna: {
      "constraint_1_coverage": bool,
      "constraint_2_depot": bool,
      "constraint_3_capacity": bool,
      "constraint_4_time_window": bool,
      "constraint_5_continuity": bool,
      "constraint_6_completeness": bool,
      "constraint_7_no_empty_routes": bool,
      "all_satisfied": bool
    }
```

#### 4. **Parsing de Instancia Solomon** (TEST-4 pre-req)

```python
FALTA:
  • parse_solomon_instance(file_path: str) → Dict
    - Lee formato Solomon (.txt)
    - Extrae: nodes, distance_matrix, capacity, time_limit
    - Calcula matriz de distancias (Euclideana o leída)
    - Valida coherencia (n_nodes, depot=0, etc)
    
    Retorna: {
      "instance_id": "C101",
      "n_customers": 100,
      "capacity": 200,
      "nodes": [
        {"id": 0, "x": 40, "y": 50, "demand": 0, 
         "ready_time": 0, "due_date": 1000, "service_time": 0},
        {"id": 1, "x": 45.56, "y": 48.3, "demand": 10,
         "ready_time": 100, "due_date": 200, "service_time": 30},
        ...
      ],
      "distance_matrix": [[0, 8.2, ...], ...],
      "time_matrix": [[0, 24.6, ...], ...]
    }
```

#### 5. **Estadísticas Agregadas** (Para logging)

```python
FALTA:
  • solution_statistics(solution, instance, bks_dict) → Dict
    
    Retorna:
    {
      "n_vehicles": 10,
      "total_distance": 1250.3,
      "n_infeasible": 0,
      "capacity_violation": 0.0,
      "time_violation": 0.0,
      "gap_percent": 5.2,
      "feasible": True,
      "routes_utilized": 10,
      "avg_customers_per_route": 10.0,
      "avg_route_distance": 125.03,
      "max_route_distance": 189.2,
      "min_route_distance": 78.9
    }
```

### RESUMEN PARA EXPERTO

| Función | Líneas | Prioridad | Complejidad |
|---------|--------|-----------|-------------|
| `load_bks_file()` | 15 | 🔴 CRÍTICA | 🟢 Baja |
| `compute_gap()` | 10 | 🔴 CRÍTICA | 🟢 Baja |
| `lexicographic_compare()` | 8 | 🔴 CRÍTICA | 🟢 Baja |
| `validate_all_constraints()` | 60 | 🔴 CRÍTICA | 🟡 Media |
| `parse_solomon_instance()` | 40 | 🔴 CRÍTICA | 🟡 Media |
| `solution_statistics()` | 25 | 🟡 ALTA | 🟢 Baja |

**Total estimado:** 160 líneas nuevas  
**Tiempo estimado:** 6-8 horas

---

## COMPONENTE 2: GENERADOR DE AST (10% → NECESITA 90%)

**Archivo:** `src/ast/generator.py` (407 líneas)

### ✅ YA IMPLEMENTADO (10%)

```python
✓ RandomASTGenerator.__init__()     → Inicialización básica
✓ _gen_numeric_expr()               → Generación parcial de expresiones numéricas
✓ _gen_numeric_leaf()               → Hojas numéricas (Feature, Const)
✓ _gen_weighted_sum()               → SUM ponderado de términos
✓ _gen_bool_expr()                  → Expresiones booleanas parciales
✓ _gen_operator_selector()          → Selector de operadores
✓ _weighted_choice()                → Utilidad de selección
```

### ❌ FALTA IMPLEMENTAR CRÍTICAMENTE (90%)

#### 1. **Ejecutabilidad (NON-NEGOTIABLE)** - TEST-5.2

```python
CRÍTICA: Las expresiones generadas deben ser EVALUABLES

FALTA:
  • Toda la clase ASTParser (importada pero NO existe)
  • Métodos de evaluación runtime: 
  
    class ASTNode:
        def evaluate(self, state: Dict[str, float]) → float/str/bool:
            """Ejecuta el AST contra InsertionState actual"""
            pass
    
  • Para Construction scoring:
    state = {
      "route_length": 15,
      "route_load": 150,
      "route_capacity_remaining": 50,
      "cust_demand": 10,
      "cust_urgency": 0.8,
      "delta_distance": 25.3,
      ...
    }
    
    score = ast_root.evaluate(state)  # ← Debe retornar float
    
  • Para Local Search operator selection:
    operator = ast_root.evaluate(state)  # ← Debe retornar string (operator name)
```

#### 2. **Determinismo Garantizado** - TEST-5.2

```python
FALTA:
  • Seed reproduction exacto
  • Verificar que generate_algorithm_json(seed=42) 
    genera SIEMPRE el mismo JSON
  • Implementar test:
    
    gen = RandomASTGenerator(...)
    algo1 = gen.generate_algorithm_json("algo1", seed=42)
    algo2 = gen.generate_algorithm_json("algo2", seed=42)
    
    assert algo1["construction_ast"] == algo2["construction_ast"]
    assert json.dumps(algo1, sort_keys=True) == json.dumps(algo2, sort_keys=True)
```

#### 3. **Validación de Restricciones** - TEST-5.3

```python
FALTA COMPLETAMENTE:
  • ast_validator.py (importado en línea 22 pero NO existe)
  
  class ASTValidator:
      def validate_construction_ast(self, ast_json) → ValidationResult:
          """Valida Construction AST"""
          errors = []
          
          # Verificar profundidad máxima
          if self._max_depth(ast_json) > self.config.max_depth:
              errors.append("Depth exceeded")
          
          # Verificar número máximo de nodos función
          if self._count_function_nodes(ast_json) > self.config.max_function_nodes:
              errors.append("Too many function nodes")
          
          # Verificar type correctness (numeric)
          if not self._is_type_correct(ast_json, expected_type="numeric"):
              errors.append("Type mismatch")
          
          return ValidationResult(
              ok=len(errors) == 0,
              errors=errors,
              stats={...}
          )
      
      def validate_ls_operator_ast(self, ast_json) → ValidationResult:
          """Valida Local Search Operator AST"""
          # Similares checks pero esperando tipo "categorical" (string)
          pass
      
      def _max_depth(self, node) → int:
          """Calcula profundidad máxima recursivamente"""
          pass
      
      def _count_function_nodes(self, node) → int:
          """Cuenta nodos internos (no hojas)"""
          pass
      
      def _is_type_correct(self, node, expected_type) → bool:
          """Verifica type correctness recursivamente"""
          pass
```

#### 4. **Feature Sets y Operator Pool** - TEST-5.1 pre-req

```python
FALTA DOCUMENTACIÓN Y VALIDACIÓN:
  
  CONSTRUCTION_FEATURES (para expresiones de scoring):
    • route_length
    • route_load
    • route_capacity_remaining
    • route_current_time
    • route_total_waiting
    • cust_demand
    • cust_ready_time
    • cust_due_time
    • cust_service_time
    • delta_distance
    • delta_time
    • urgency
    • load_ratio
    • num_customers_remaining
    
  LS_FEATURES (para decisiones de operadores):
    • num_routes
    • total_distance
    • penalty_value
    • avg_route_length
    • iterations_no_improve
    • num_time_violations
    • num_capacity_violations
    
  LS_OPERATORS (válidos para elegir):
    • "relocate"
    • "swap"
    • "two_opt"
    • "or_opt"
    • "cross_exchange"

FALTA:
  • Validar que features requeridas existan en state
  • Validar que operadores estén en lista permitida
  • Validar que features en AST son subset de feature_pool
```

#### 5. **Type System Completo** - Crítico para validación

```python
FALTA:
  class TypeSystem:
      """Type checking para AST"""
      
      TERMINAL_TYPES = {
          "Feature": "numeric" o "bool" (según nombre),
          "Const": "numeric" si float, "categorical" si str
      }
      
      OPERATOR_TYPES = {
          "Add": numeric → numeric,
          "Sub": numeric → numeric,
          "Mul": numeric → numeric,
          "Div": numeric → numeric,
          "And": bool → bool,
          "Or": bool → bool,
          "Less": numeric → bool,
          "Greater": numeric → bool,
          "WeightedSum": [numeric] → numeric,
          "If": (bool, T, T) → T,
          "Choose": [categorical] → categorical,
      }
      
      def infer_type(node) → str:
          """Infiere tipo recursivamente"""
          if node["type"] == "Feature":
              return self._feature_type(node["name"])
          elif node["type"] == "Const":
              return "float" if isinstance(node["value"], float) else "categorical"
          elif node["type"] in OPERATOR_TYPES:
              # Verificar tipos de hijos
              return OPERATOR_TYPES[node["type"]]["return"]
          else:
              raise TypeError(f"Unknown type {node['type']}")
```

#### 6. **Generación No-Sesgada** - Evitar bloat

```python
FALTA:
  • Estrategia de crecimiento controlado:
    - Profundidad no debe ser siempre máxima
    - Funciones no deben aglomerar al inicio
    - Distribución de tipos debe ser balanceada
  
  • Implementar:
    def _should_expand(self, depth, function_nodes_used, max_depth, max_functions) → bool:
        """Decide si seguir expandiendo nodo actual"""
        
        # Expandir menos conforme profundidad aumenta
        expand_prob = 1.0 - (depth / max_depth) * 0.7
        
        # No expandir si sin presupuesto de funciones
        if function_nodes_used >= max_functions:
            expand_prob = 0
        
        return random.random() < expand_prob
```

#### 7. **Integración con AlgorithmGenerator** - TEST-5.1

```python
FALTA VALIDAR:
  • AlgorithmGenerator._generate_single() llama:
    - self.ast_generator.generate(phase=phase)  ← ¿Qué retorna?
    - self.ast_validator.validate_*()  ← ¿Qué estructura espera?
    
  PROBLEMA: RandomASTGenerator.generate() NO EXISTE
           Se importa ASTGenerator pero no es RandomASTGenerator
  
  NECESARIO:
    • Renombar RandomASTGenerator → ASTGenerator (O)
    • Implementar método generate(phase) que:
      
      def generate(self, phase: str) → Dict[str, Any]:
          if phase == "construction":
              ctx = GenContext(...)
              return self._gen_numeric_expr(ctx, depth=0, feature_pool=...)
          else:  # local_search
              ctx = GenContext(...)
              return self._gen_operator_selector(ctx, depth=0)
```

### RESUMEN PARA EXPERTO

| Componente | Líneas | Prioridad | Complejidad | Blocker |
|------------|--------|-----------|-------------|---------|
| **ASTParser** | 120 | 🔴 CRÍTICA | 🔴 ALTA | ✅ SÍ |
| **ASTValidator** | 150 | 🔴 CRÍTICA | 🔴 ALTA | ✅ SÍ |
| **TypeSystem** | 80 | 🔴 CRÍTICA | 🔴 ALTA | ✅ SÍ |
| `generate()` method | 20 | 🔴 CRÍTICA | 🟢 Baja | ✅ SÍ |
| Determinismo tests | 30 | 🟡 ALTA | 🟡 Media | ❌ NO |
| Crecimiento balanced | 25 | 🟡 ALTA | 🟡 Media | ❌ NO |
| Feature validation | 40 | 🟡 ALTA | 🟢 Baja | ✅ SÍ |

**Total estimado:** 460 líneas nuevas  
**Tiempo estimado:** 16-20 horas  
**Blocker crítico:** ASTParser + ASTValidator (sin estos, NO puede ejecutar)

---

## 📋 ORDEN DE IMPLEMENTACIÓN RECOMENDADO

### FASE 1: EVALUADOR (Est. 6-8h)

```
1. parse_solomon_instance()      [40 líneas, 2h]
   └─ Prerequisito para TEST-1.1
   
2. load_bks_file()               [15 líneas, 0.5h]
   └─ Prerequisito para TEST-4.3
   
3. validate_all_constraints()    [60 líneas, 3h]
   └─ Prerequisito para TEST-4.1
   
4. compute_gap()                 [10 líneas, 0.5h]
   └─ Prerequisito para TEST-4.3
   
5. lexicographic_compare()       [8 líneas, 0.5h]
   └─ Prerequisito para TEST-4.2
   
6. solution_statistics()         [25 líneas, 1.5h]
   └─ Para logging reproducible
```

### FASE 2: CORE AST (Est. 16-20h)

```
1. TypeSystem class              [80 líneas, 4h]
   └─ Foundation para validación
   
2. ASTValidator class            [150 líneas, 6h]
   └─ Validación exhaustiva
   
3. ASTParser + Evaluation        [120 líneas, 7h]
   └─ Ejecución en runtime
   
4. Fix RandomASTGenerator.generate() [20 líneas, 1h]
   └─ Integración con AlgorithmGenerator
   
5. Feature validation            [40 líneas, 2h]
   └─ Verificar features existen en state
```

---

## 🎯 INSTRUCCIÓN PARA EXPERTO

**Dale exactamente esto:**

```
Necesito implementar 2 componentes críticos para GAA-GRASP-VRPTW:

1. **EVALUADOR DE FITNESS** (160 líneas nuevo código)
   - load_bks_file(): Carga best-known-solutions Solomon
   - compute_gap(): Calcula brecha (vehículos primero, distancia segundo)
   - validate_all_constraints(): Verifica 7 restricciones VRPTW
   - parse_solomon_instance(): Parser .txt Solomon 56-instancias
   - lexicographic_compare(): Métrica lexicográfica (V, D)
   - solution_statistics(): Stats agregadas para logging JSONL

2. **GENERADOR Y VALIDADOR DE AST** (460 líneas nuevo código)
   - TypeSystem: Type checking recursivo (numeric/bool/categorical)
   - ASTValidator: Validación de restricciones (profundidad, funciones, type-correctness)
   - ASTParser: Ejecución runtime de ASTs contra estado (InsertionState, LSState)
   - Fix generate() method en RandomASTGenerator
   - Feature validation: Verificar features existen

Archivos actuales:
- src/evaluation/solution_evaluator.py (211 líneas, 20% completo)
- src/ast/generator.py (407 líneas, 10% completo)

Sin estos 620 líneas, NO PUEDO:
  ✗ Evaluar soluciones vs BKS (TEST-4.1-4.3)
  ✗ Ejecutar ASTs generados (TEST-5.2)
  ✗ Validar ASTs (TEST-5.3)
  ✗ Correr experimentos (TEST-12)

¿Cuánto tiempo necesitas?
```

---

**Versión:** Análisis Técnico Detallado  
**Fecha:** 4 de Enero, 2026  
**Status:** Listo para entregar a experto
