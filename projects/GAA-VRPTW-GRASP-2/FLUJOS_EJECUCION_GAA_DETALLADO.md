# Flujos de Ejecución: GAA, Operadores y AST

**Documentación Técnica Detallada**  
**Fecha:** 2 de Enero, 2026

---

## Índice

1. [Flujo Principal de Ejecución](#flujo-principal)
2. [Generación de Algoritmos GAA](#generación-gaa)
3. [Estructura y Componentes del AST](#estructura-ast)
4. [Operadores: Clasificación y Uso](#operadores)
5. [Integración con Metaheurísticas](#integración)
6. [Detalles Técnicos Profundos](#detalles-técnicos)

---

## Flujo Principal de Ejecución {#flujo-principal}

### Nivel 1: Ejecución de Experimentos

```
INICIO (QUICK o FULL)
    ↓
1. parse_arguments() [scripts/experiments.py:540]
    ├─ mode: 'QUICK' o 'FULL'
    ├─ seed: 42 (default)
    └─ families: ['R1'] o ['C1','C2','R1','R2','RC1','RC2']
    ↓
2. QuickExperiment.run() o FullExperiment.run()
    ├─ ExperimentConfig(mode, families, algorithms, seed=42)
    ├─ GENERAR ALGORITMOS GAA ← ⭐⭐⭐ PUNTO CLAVE 1
    │   ├─ AlgorithmGenerator(seed=42)
    │   ├─ generate_three_algorithms()
    │   └─ Salida: 3 algoritmos con AST
    ├─ ExperimentExecutor(config)
    ├─ get_solomon_instances(families)
    │   └─ Carga datasets: C1/R1/R101.csv, etc.
    └─ EJECUTAR EXPERIMENTOS ← ⭐⭐⭐ PUNTO CLAVE 2
        └─ for family in families:
            └─ for instance_id in instances:
                └─ for algo_name in ['GRASP','VND','ILS']:
                    ├─ GRASP.solve(instance) ← Usa operadores
                    ├─ VND.search(instance) ← Usa operadores
                    └─ ILS.solve(instance) ← Usa operadores
    ↓
3. save_raw_results() → raw_results.csv
4. generate_visualizations()
5. generate_summary_report()
    ↓
FIN
```

### Código de Entry Point

```python
# scripts/experiments.py

def main():
    """Main entry point"""
    args = parse_arguments()
    
    if args.mode == 'QUICK':
        executor = QuickExperiment.run()
    elif args.mode == 'FULL':
        executor = FullExperiment.run()
    
    print(f"[OK] Resultados en: {executor.results_dir}")
    return executor
```

---

## Generación de Algoritmos GAA {#generación-gaa}

### Nivel 2: Generación Detallada

```
AlgorithmGenerator(seed=42)
    ↓
generate_three_algorithms()
    │
    ├─ for i in [1, 2, 3]:
    │   ├─ random.seed(42 + i)  ← Determinismo
    │   ├─ generate_with_validation(max_attempts=20)
    │   │   └─ LOOP:
    │   │       ├─ ast = generate()  ← Patrón aleatorio
    │   │       ├─ errors = grammar.validate_ast(ast)
    │   │       └─ IF errors: continue ELSE: return ast
    │   │
    │   ├─ ast.to_dict() → Serialización
    │   ├─ grammar.get_statistics(ast) → Metadatos
    │   │
    │   └─ RETURN algoritmo_dict:
    │       {
    │           'id': 1,
    │           'name': 'GAA_Algorithm_1',
    │           'ast': {...},          ← AST completo
    │           'pattern': 'simple',   ← Tipo de patrón
    │           'seed': 42,
    │           'timestamp': '2026...',
    │           'stats': {
    │               'depth': 2,
    │               'size': 3,
    │               'num_constructive': 1,
    │               'num_improvement': 1,
    │               'num_perturbation': 0
    │           }
    │       }
    │
    ↓
save_algorithms(algorithms, 'algorithms/')
    ├─ GAA_Algorithm_1.json
    ├─ GAA_Algorithm_2.json
    ├─ GAA_Algorithm_3.json
    └─ _algorithms.json ← Índice con metadata
```

### Generación de Patrones: Detalle Técnico

```python
# gaa/generator.py

def generate():
    """Selecciona patrón aleatorio"""
    pattern = random.choice(['simple', 'iterative', 'multistart', 'complex'])
    
    if pattern == 'simple':
        return _generate_simple()      # 25% probabilidad
    elif pattern == 'iterative':
        return _generate_iterative()   # 25% probabilidad
    elif pattern == 'multistart':
        return _generate_multistart()  # 25% probabilidad
    else:
        return _generate_complex()     # 25% probabilidad
```

#### Patrón 1: SIMPLE (25%)

```
_generate_simple()
    ├─ GreedyConstruct(
    │   heuristic = random.choice([6 operadores]),
    │   alpha = random.uniform(0.1, 0.5)
    │ )
    │
    └─ LocalSearch(
        operator = random.choice([8 operadores]),
        max_iterations = random.choice([50,100,150,200])
    )
    
RETORNA: Seq(body=[GreedyConstruct, LocalSearch])

Estructura AST:
Seq
├── GreedyConstruct(heuristic="Savings", alpha=0.25)
└── LocalSearch(operator="TwoOpt", max_iterations=100)

Profundidad: 2
Tamaño: 3 nodos
Complejidad: ⭐
```

#### Patrón 2: ITERATIVE (25%)

```
_generate_iterative()
    ├─ GreedyConstruct(...)
    │
    └─ While(
        condition = "IterBudget",
        max_iterations = 100,
        body = Seq(
            LocalSearch(...),
            Perturbation(...)
        )
    )
    
RETORNA: Seq(body=[GreedyConstruct, While])

Estructura AST:
Seq
├── GreedyConstruct(heuristic="Sweep")
└── While(max_iterations=100)
    └── Seq
        ├── LocalSearch(operator="OrOpt")
        └── Perturbation(operator="RandomRouteRemoval", strength=2)

Profundidad: 4
Tamaño: 6 nodos
Complejidad: ⭐⭐
```

#### Patrón 3: MULTISTART (25%)

```
_generate_multistart()
    └─ For(
        iterations = random.choice([3,5,10]),
        body = Seq(
            GreedyConstruct(...),
            LocalSearch(...)
        )
    )
    
RETORNA: For(iterations=5, body=...)

Estructura AST:
For(iterations=5)
└── Seq
    ├── GreedyConstruct(heuristic="NearestNeighbor")
    └── LocalSearch(operator="ThreeOpt")

Profundidad: 3
Tamaño: 4 nodos
Complejidad: ⭐⭐
```

#### Patrón 4: COMPLEX (25%)

```
_generate_complex()
    ├─ GreedyConstruct(...)
    │
    └─ While(
        max_iterations = 100,
        body = Seq(
            If(
                condition = "Improves",
                then_branch = LocalSearch(...),
                else_branch = Perturbation(...)
            ),
            ...
        )
    )
    
RETORNA: Seq(body=[GreedyConstruct, While])

Estructura AST:
Seq
├── GreedyConstruct(heuristic="RegretInsertion")
└── While(max_iterations=100)
    └── If(condition="Improves")
        ├── then: LocalSearch(operator="GENI")
        └── else: Perturbation(operator="WorseFeasibleMove")

Profundidad: 4-5
Tamaño: 7-8 nodos
Complejidad: ⭐⭐⭐
```

---

## Estructura y Componentes del AST {#estructura-ast}

### Nivel 3: Arquitectura del AST

```
ASTNode (Base Class)
├── Métodos abstractos:
│   ├── depth() → int
│   ├── size() → int
│   ├── get_all_nodes() → List[ASTNode]
│   ├── to_pseudocode() → str
│   ├── to_dict() → Dict
│   └── validate() → bool
│
├── NODOS DE CONTROL
│   ├── Seq (Secuencia)
│   │   └── body: List[ASTNode]
│   │       Ejemplo: A → B → C
│   │       Profundidad: 1 + max(profundidades hijos)
│   │       Tamaño: 1 + suma de tamaños hijos
│   │
│   ├── If (Condicional)
│   │   ├── condition: str
│   │   ├── then_branch: ASTNode
│   │   └── else_branch: ASTNode
│   │       Profundidad: 1 + max(then, else)
│   │       Tamaño: 1 + then.size + else.size
│   │
│   ├── While (Bucle iterativo)
│   │   ├── condition: str
│   │   ├── max_iterations: int
│   │   └── body: ASTNode
│   │       Profundidad: 1 + body.depth
│   │       Tamaño: 1 + body.size
│   │
│   └── For (Bucle determinista)
│       ├── iterations: int
│       └── body: ASTNode
│           Profundidad: 1 + body.depth
│           Tamaño: 1 + body.size
│
└── NODOS DE OPERADORES
    ├── GreedyConstruct (Construcción)
    │   ├── heuristic: str (uno de 6)
    │   └── alpha: float ∈ [0.1, 0.5]
    │       Profundidad: 1
    │       Tamaño: 1
    │
    ├── LocalSearch (Mejora)
    │   ├── operator: str (uno de 8)
    │   └── max_iterations: int ∈ [1, 500]
    │       Profundidad: 1
    │       Tamaño: 1
    │
    └── Perturbation (Perturbación)
        ├── operator: str (uno de 4)
        └── strength: int ∈ [1, 5]
            Profundidad: 1
            Tamaño: 1
```

### Validación y Estadísticas

```python
# Grammar validation flow

Grammar.validate_ast(ast):
    checks = []
    
    if not isinstance(ast, ASTNode):
        checks.append("AST must be ASTNode instance")
    
    if ast.depth() < self.min_depth:
        checks.append(f"Depth {ast.depth()} < {self.min_depth}")
    
    if ast.depth() > self.max_depth:
        checks.append(f"Depth {ast.depth()} > {self.max_depth}")
    
    if ast.size() < 3:
        checks.append("Size < 3")
    
    if ast.size() > 100:
        checks.append("Size > 100")
    
    # Validar operadores usados
    for node in ast.get_all_nodes():
        if isinstance(node, GreedyConstruct):
            if node.heuristic not in CONSTRUCTIVE_TERMINALS:
                checks.append(f"Invalid heuristic: {node.heuristic}")
        
        if isinstance(node, LocalSearch):
            if node.operator not in IMPROVEMENT_TERMINALS:
                checks.append(f"Invalid operator: {node.operator}")
        
        if isinstance(node, Perturbation):
            if node.operator not in PERTURBATION_TERMINALS:
                checks.append(f"Invalid perturbation: {node.operator}")
    
    return checks  # Empty = válido
```

### Serialización a JSON

```json
{
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
}
```

---

## Operadores: Clasificación y Uso {#operadores}

### Nivel 4: Los 18 Operadores

#### CONSTRUCTIVOS (6): Construcción de solución inicial

```
1. NearestNeighbor
   └─ Comportamiento: Greedy selecciona cliente más cercano
   └─ Parámetro: alpha = probabilidad de NO seleccionar el mejor
   └─ Uso típico: Construcción inicial rápida

2. Savings
   └─ Comportamiento: Merge rutas basado en ahorros (Clarke-Wright)
   └─ Parámetro: alpha = factor de aleatorización
   └─ Uso típico: Buena calidad inicial

3. Sweep
   └─ Comportamiento: Barrido angular desde depósito
   └─ Parámetro: alpha = desviación del ángulo
   └─ Uso típico: Instancias clustered (C1, C2)

4. TimeOrientedNN
   └─ Comportamiento: NN pero considerando ventanas de tiempo
   └─ Parámetro: alpha = factor de ventana
   └─ Uso típico: Instancias VRPTW con restricciones fuertes

5. RegretInsertion
   └─ Comportamiento: Inserta cliente que maximiza costo de no insertar
   └─ Parámetro: alpha = factor de regret
   └─ Uso típico: Buena calidad, más lento

6. RandomizedInsertion
   └─ Comportamiento: Inserción aleatoria con penalizaciones
   └─ Parámetro: alpha = factor de penalización
   └─ Uso típico: Diversidad de soluciones
```

#### MEJORA (8): Búsqueda local

```
1. TwoOpt
   └─ Comportamiento: Invierte arcos (i,i+1) y (j,j+1)
   └─ Complejidad: O(n²)
   └─ Mejora esperada: 5-10% típicamente
   └─ Uso: Estándar, muy efectivo

2. OrOpt
   └─ Comportamiento: Mueve cadena de 1-3 clientes
   └─ Complejidad: O(n²-n³)
   └─ Mejora esperada: 2-5%
   └─ Uso: Complementa TwoOpt

3. ThreeOpt
   └─ Comportamiento: Elimina 3 arcos y reconecta
   └─ Complejidad: O(n³)
   └─ Mejora esperada: 8-15%
   └─ Uso: Más lento pero más potente

4. Relocate
   └─ Comportamiento: Mueve cliente a mejor posición
   └─ Complejidad: O(n²)
   └─ Mejora esperada: 1-3%
   └─ Uso: Rápido, básico

5. Exchange
   └─ Comportamiento: Intercambia dos clientes entre rutas
   └─ Complejidad: O(n²)
   └─ Mejora esperada: 2-4%
   └─ Uso: Especialmente efectivo en VRP

6. GENI
   └─ Comportamiento: Generalización generalized insertion
   └─ Complejidad: O(n²)
   └─ Mejora esperada: 4-8%
   └─ Uso: Especializado, muy efectivo

7. LKH
   └─ Comportamiento: Lin-Kernighan Heuristic adaptado
   └─ Complejidad: O(n²-n³)
   └─ Mejora esperada: 10-20%
   └─ Uso: Muy potente pero complejo

8. VND
   └─ Comportamiento: Variable Neighborhood Descent
   └─ Complejidad: O(n² * k) donde k=vecindarios
   └─ Mejora esperada: 15-25%
   └─ Uso: Meta-búsqueda, ordena operadores
```

#### PERTURBACIÓN (4): Diversificación

```
1. RandomRouteRemoval
   └─ Comportamiento: Elimina ruta aleatoria, reinsertar clientes
   └─ Alcance: Media-alta (destruye ruta completa)
   └─ Uso típico: Para ILS después mejora local

2. WorseFeasibleMove
   └─ Comportamiento: Aplica movimiento que empeora solución
   └─ Alcance: Baja-media (movimiento individual)
   └─ Uso típico: Escapa de mínimos locales suaves

3. RandomRelocate
   └─ Comportamiento: Mueve cliente a posición aleatoria
   └─ Alcance: Media (reposiciona clientes)
   └─ Uso típico: Diversidad controlada

4. SegmentShift
   └─ Comportamiento: Desplaza segmento de ruta
   └─ Alcance: Media (afecta múltiples clientes)
   └─ Uso típico: Cambios estructurales suaves
```

### Matriz de Compatibilidad: Operador × Patrón

```
                 SIMPLE  ITERATIVE  MULTISTART  COMPLEX
NearestNeighbor   ✅       ✅          ✅         ✅
Savings           ✅       ✅          ✅         ✅
Sweep             ✅       ✅          ✅         ✅
TimeOrientedNN    ✅       ✅          ✅         ✅
RegretInsertion   ✅       ✅          ✅         ✅
RandomizedInsertion ✅     ✅          ✅         ✅

TwoOpt            ✅       ✅          ✅         ✅
OrOpt             ✅       ✅          ✅         ✅
ThreeOpt          ✅       ✅          ✅         ✅
Relocate          ✅       ✅          ✅         ✅
Exchange          ✅       ✅          ✅         ✅
GENI              ✅       ✅          ✅         ✅
LKH               ✅       ✅          ✅         ✅
VND               ✅       ✅          ✅         ✅

RandomRouteRemoval ❌      ✅          ❌         ✅
WorseFeasibleMove  ❌      ✅          ❌         ✅
RandomRelocate    ❌      ✅          ❌         ✅
SegmentShift      ❌      ✅          ❌         ✅

Nota: ✅ = Compatible, ❌ = No usado en ese patrón
```

---

## Integración con Metaheurísticas {#integración}

### Nivel 5: Flujo de Ejecución Real

```
INSTANCE DATA
    └─ VRP Instance
        ├─ customers: List[Customer]
        ├─ depot: Depot
        ├─ distance_matrix
        └─ time_matrix
        
        ↓
        
ALGORITMO 1: GRASP
    └─ GRASP(alpha=0.15, max_iterations=100, seed=42)
       ├─ for iter in [1..100]:
       │   ├─ FASE 1: CONSTRUCTION
       │   │   └─ _construct_solution()
       │   │       ├─ Usa operador constructivo (ej: Savings)
       │   │       ├─ alpha controla aleatorización
       │   │       └─ RETORNA: Solution candidata
       │   │
       │   └─ FASE 2: LOCAL SEARCH
       │       └─ _local_search(solution)
       │           ├─ Aplica operador mejora (ej: TwoOpt)
       │           ├─ Mejora iterativa hasta óptimo local
       │           └─ RETORNA: Solution mejorada
       │
       ├─ RETORNA: mejor_solution encontrada
       └─ Output: k (vehículos), d (distancia), fitness

ALGORITMO 2: VND
    └─ VariableNeighborhoodDescent()
       ├─ Requiere: solution inicial (de GRASP)
       ├─ BUCLE VND:
       │   └─ k = 1 (operador TwoOpt)
       │       ├─ Busca mejora local
       │       ├─ Si encuentra mejora: k=1, ir a siguiente solución
       │       ├─ Si NO encuentra: k=2
       │       │
       │   └─ k = 2 (operador OrOpt)
       │       ├─ Busca mejora local
       │       ├─ Si encuentra mejora: k=1
       │       ├─ Si NO encuentra: k=3
       │       │
       │   └─ ... (hasta k=8 o converger)
       │
       ├─ RETORNA: Solución óptimo local (VND)
       └─ Output: k, d, fitness

ALGORITMO 3: ILS (Iterated Local Search)
    └─ IteratedLocalSearch(perturbation_strength=3, max_iterations=100, seed=42)
       ├─ solution_actual = GRASP.solve(instance)
       ├─ for iter in [1..100]:
       │   │
       │   ├─ FASE 1: LOCAL SEARCH
       │   │   └─ solution_mejorada = VND.search(solution_actual)
       │   │
       │   ├─ FASE 2: PERTURBATION
       │   │   └─ if iter % 5 == 0:
       │   │       └─ solution_actual = _perturbation(solution_mejorada)
       │   │           ├─ Usa operador perturbación
       │   │           │  (ej: RandomRouteRemoval, strength=3)
       │   │           ├─ Destruye solution para escape
       │   │           └─ RETORNA: solution diversificada
       │   │
       │   ├─ FASE 3: ACEPTACIÓN
       │   │   └─ if fitness(solution_mejorada) < fitness(better):
       │   │       └─ better = solution_mejorada
       │   │
       │   └─ solution_actual = solution_mejorada
       │
       ├─ RETORNA: mejor_solution encontrada
       └─ Output: k, d, fitness
```

### Flujo Detallado: GRASP en una Instancia

```
GRASP.solve(instance: VRPInstance) → (solution, fitness, stats)
│
├─ for iteration in range(1, max_iterations+1):
│   │
│   ├─ CONSTRUCCIÓN GREEDY ALEATORIA
│   │   └─ routes = []
│   │       ├─ candidates = [clientes no asignados]
│   │       ├─ route_actual = [depot]
│   │       │
│   │       └─ while candidates:
│   │           ├─ RCL = Restricted Candidate List
│   │           │   ├─ calcular costos: c[i] = distancia(actual → i)
│   │           │   ├─ c_min = min(c), c_max = max(c)
│   │           │   ├─ RCL = {i : c[i] <= c_min + alpha*(c_max-c_min)}
│   │           │   └─ Típicamente 10-20% de candidatos
│   │           │
│   │           ├─ cliente = random.choice(RCL)
│   │           │   ├─ Selección aleatoria de RCL
│   │           │   ├─ NO siempre el mejor
│   │           │   └─ Introduce diversidad
│   │           │
│   │           ├─ if ruta_actual puede insertar cliente:
│   │           │   └─ route_actual.append(cliente)
│   │           │       └─ Verifica capacidad, time windows, etc.
│   │           └─ else:
│   │               ├─ Inicia nueva ruta
│   │               └─ route_actual = [depot, cliente]
│   │
│   │   └─ RETORNA: solución inicial (candidata)
│   │
│   ├─ BÚSQUEDA LOCAL
│   │   └─ improved = True
│   │       ├─ while improved:
│   │       │   ├─ improved = False
│   │       │   │
│   │       │   └─ for (i,j) in todos_arcos_pares:
│   │       │       ├─ if aplicar_2opt(i,j) mejora fitness:
│   │       │       │   ├─ routes = _2opt(routes, i, j)
│   │       │       │   ├─ improved = True
│   │       │       │   └─ break (primera mejora)
│   │       │       └─ RETORNA: solución mejorada local
│   │
│   └─ if fitness(candidata) < fitness(mejor):
│       └─ mejor = candidata
│
└─ RETORNA: mejor solución encontrada en 100 iteraciones
```

---

## Detalles Técnicos Profundos {#detalles-técnicos}

### Cálculo de Profundidad en AST

```python
# Definición recursiva

def depth(node: ASTNode) -> int:
    
    if isinstance(node, (GreedyConstruct, LocalSearch, Perturbation)):
        # Nodos hoja (terminales)
        return 1
    
    elif isinstance(node, Seq):
        # Profundidad máxima del body
        if not node.body:
            return 1
        return 1 + max(depth(child) for child in node.body)
    
    elif isinstance(node, If):
        # Máxima de ramas
        then_depth = depth(node.then_branch) if node.then_branch else 1
        else_depth = depth(node.else_branch) if node.else_branch else 1
        return 1 + max(then_depth, else_depth)
    
    elif isinstance(node, While):
        # Body + 1
        return 1 + depth(node.body)
    
    elif isinstance(node, For):
        # Body + 1
        return 1 + depth(node.body)

# Ejemplo de cálculo:

Seq(body=[
    GreedyConstruct(),           # depth=1
    While(body=Seq(body=[         # depth= 1 + depth(Seq)
        LocalSearch(),             # depth=1
        Perturbation()             # depth=1
    ]))                            # depth = 1 + max(1,1) = 2
])                                 # depth = 1 + max(1, 1+2) = 1 + 3 = 4

PROFUNDIDAD FINAL = 4
```

### Cálculo de Tamaño en AST

```python
# Contar todos los nodos

def size(node: ASTNode) -> int:
    
    if isinstance(node, (GreedyConstruct, LocalSearch, Perturbation)):
        # Nodos hoja cuentan como 1
        return 1
    
    elif isinstance(node, Seq):
        # 1 (Seq) + todos los hijos
        return 1 + sum(size(child) for child in node.body)
    
    elif isinstance(node, If):
        # 1 (If) + then + else
        then_size = size(node.then_branch) if node.then_branch else 1
        else_size = size(node.else_branch) if node.else_branch else 1
        return 1 + then_size + else_size
    
    elif isinstance(node, While):
        # 1 (While) + body
        return 1 + size(node.body)
    
    elif isinstance(node, For):
        # 1 (For) + body
        return 1 + size(node.body)

# Ejemplo:

Seq(body=[                      # Seq = 1
    GreedyConstruct(),          # Greedy = 1
    While(body=Seq(body=[       # While = 1, Seq = 1
        LocalSearch(),          # LocalSearch = 1
        Perturbation()          # Perturbation = 1
    ]))
])

TAMAÑO FINAL = 1 + 1 + (1 + (1 + 1 + 1)) = 1 + 1 + 4 = 6
```

### Validación de Gramática: Proceso Completo

```python
# scripts/experiments.py :: QuickExperiment.run()

# PASO 1: Generar 3 algoritmos
gaa_generator = AlgorithmGenerator(seed=42)
gaa_algorithms = gaa_generator.generate_three_algorithms()
# Retorna lista de 3 dicts con AST

# En AlgorithmGenerator.generate_three_algorithms():
for i in range(3):
    random.seed(42 + i)  # 42, 43, 44
    
    ast = self.generate_with_validation(max_attempts=20)
    #  └─ LOOP:
    #      for attempt in range(20):
    #          ast = self.generate()
    #          errors = self.grammar.validate_ast(ast)
    #          if not errors:
    #              return ast
    
    if ast is None:
        print(f"[WARNING] No se pudo generar algoritmo {i+1}")
        continue
    
    # PASO 2: Validar
    stats = self.grammar.get_statistics(ast)
    #  └─ En Grammar.get_statistics():
    #      {
    #          'depth': ast.depth(),              # ∈ [2,5]
    #          'size': ast.size(),                 # ∈ [3,100]
    #          'num_constructive': count(...),     # ≥ 1
    #          'num_improvement': count(...),      # ≥ 1
    #          'num_perturbation': count(...)      # ≥ 0
    #      }
    
    # PASO 3: Serializar
    algo_dict = {
        'id': i + 1,
        'name': f'GAA_Algorithm_{i+1}',
        'ast': ast.to_dict(),        # Serialización JSON
        'pattern': _detect_pattern(ast),
        'seed': 42,
        'timestamp': datetime.now().isoformat(),
        'stats': stats
    }
    
    algorithms.append(algo_dict)

# PASO 4: Guardar
gen.save_algorithms(algorithms, 'algorithms/')
#  └─ Crea:
#      algorithms/GAA_Algorithm_1.json
#      algorithms/GAA_Algorithm_2.json
#      algorithms/GAA_Algorithm_3.json
#      algorithms/_algorithms.json (índice)
```

### Flujo de Datos: Desde generación hasta Ejecución

```
┌──────────────────────────────────────────────────────────┐
│ ARCHIVO: algorithms/_algorithms.json                     │
│ {                                                        │
│   "generation_timestamp": "2026-01-02T...",             │
│   "total_algorithms": 3,                                │
│   "seed_used": 42,                                      │
│   "algorithms": [                                       │
│     {                                                  │
│       "id": 1,                                         │
│       "name": "GAA_Algorithm_1",                      │
│       "pattern": "simple",                            │
│       "stats": {...}                                 │
│     }, ...                                           │
│   ]                                                  │
│ }                                                    │
└──────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────┐
│ ARCHIVO: algorithms/GAA_Algorithm_1.json                │
│ {                                                       │
│   "id": 1,                                            │
│   "name": "GAA_Algorithm_1",                         │
│   "ast": {                                          │
│     "type": "Seq",                                 │
│     "body": [                                      │
│       {                                           │
│         "type": "GreedyConstruct",               │
│         "heuristic": "Savings",                  │
│         "alpha": 0.25                           │
│       },                                         │
│       {                                         │
│         "type": "LocalSearch",                 │
│         "operator": "TwoOpt",                  │
│         "max_iterations": 100                 │
│       }                                        │
│     ]                                         │
│   },                                          │
│   "pattern": "simple",                       │
│   "stats": {                                 │
│     "depth": 2,                             │
│     "size": 3,                              │
│     ...                                     │
│   }                                         │
│ }                                           │
└──────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────┐
│ EJECUCIÓN EN EXPERIMENTO                               │
│                                                        │
│ instance = loader.load_instance('R1/R101.csv')        │
│ algoname = 'GRASP'                                     │
│                                                        │
│ ├─ GRASP(alpha=0.15, max_iterations=100, seed=42)    │
│ │   ├─ Usa operador: Savings (del AST)               │
│ │   ├─ alpha: 0.25 (del AST)                        │
│ │   │                                               │
│ │   └─ for iter in [1..100]:                        │
│ │       ├─ RCL = candidatos dentro alpha            │
│ │       ├─ solución = construcción greedy           │
│ │       ├─ mejorada = busqueda local (TwoOpt)      │
│ │       └─ guarda si mejora                        │
│ │                                                   │
│ └─ RETORNA: (solution, fitness, stats)              │
│                                                    │
│ RESULTADOS:                                        │
│   k_final: 11 (vehículos)                         │
│   d_final: 1234.5 (distancia)                     │
│   time_sec: 2.34 (segundos)                      │
│                                                  │
└──────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────┐
│ ARCHIVO: output/raw_results.csv                        │
│ algorithm,instance_id,family,k_final,d_final,time_sec │
│ GRASP,R101,R1,11,1234.5,2.34                         │
│ VND,R101,R1,10,1210.2,3.21                          │
│ ILS,R101,R1,10,1198.7,5.45                          │
│ ...                                                 │
└──────────────────────────────────────────────────────────┘
```

---

## Resumen de Flujos

### Flujo 1: Generación de Algoritmos
```
AlgorithmGenerator(seed=42)
└─ generate_three_algorithms()
   ├─ generate_with_validation() × 3
   │  └─ generate() → selecciona patrón
   │     └─ _generate_{simple|iterative|multistart|complex}()
   │        └─ combina operadores + nodos control
   ├─ validate_ast() → check gramática
   ├─ to_dict() → serialización
   ├─ get_statistics() → metadatos
   └─ save_algorithms() → JSON files
```

### Flujo 2: Ejecución Experimental
```
ExperimentExecutor(config)
└─ for family in ['R1', ...]:
   └─ for instance_id in instances:
      ├─ instance = load_instance()
      └─ for algo in ['GRASP', 'VND', 'ILS']:
         ├─ GRASP.solve(instance)
         │  ├─ construcción (operador del AST)
         │  └─ mejora local (operador del AST)
         ├─ VND.search(instance)
         │  └─ ordena operadores
         └─ ILS.solve(instance)
            ├─ mejora local
            ├─ perturbación (operador del AST)
            └─ aceptación
```

### Flujo 3: Operadores en Uso Real
```
Construcción (6 opciones)
    ↓ usa alpha del AST
Solución Inicial
    ↓
Mejora Local (8 opciones)
    ↓ usa max_iterations del AST
Óptimo Local
    ↓
[Solo en ITERATIVE/COMPLEX]
Perturbación (4 opciones)
    ↓ usa strength del AST
Solución Diversificada
    ↓
[Vuelve a Mejora Local]
```

---

## Conclusión

El sistema GAA integra **generación automática de algoritmos (AST)** con **ejecución experimental** a través de:

1. **Generación:** AlgorithmGenerator crea AST siguiendo 4 patrones
2. **Validación:** Grammar valida estructura, profundidad, tamaño
3. **Serialización:** AST se convierte a JSON para persistencia
4. **Ejecución:** Algoritmos GRASP/VND/ILS usan operadores del AST
5. **Medición:** Resultados se recopilan en CSV para análisis

Todo es **determinístico con seed=42** para reproducibilidad garantizada.
