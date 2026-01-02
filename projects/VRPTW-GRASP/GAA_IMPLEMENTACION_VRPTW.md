# 🧬 Especificación GAA (Generación Automática de Algoritmos) - VRPTW-GRASP

**Fecha**: 1 de Enero de 2026  
**Proyecto**: VRPTW-GRASP  
**Basado en**: GAA-GCP-ILS-4  
**Status**: Especificación para Implementación

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Componentes de GAA](#componentes-de-gaa)
3. [Estructura de Algoritmos GRASP](#estructura-de-algoritmos-grasp)
4. [Operadores VRPTW-GRASP](#operadores-vrptw-grasp)
5. [Gramática BNF](#gramática-bnf)
6. [Proceso de Generación](#proceso-de-generación)
7. [Ejecución de Algoritmos](#ejecución-de-algoritmos)
8. [Output al Usuario](#output-al-usuario)
9. [Estructura de Directorios](#estructura-de-directorios)

---

## 🎯 Visión General

### ¿Qué es GAA en VRPTW-GRASP?

GAA (Grammar-based Algorithm Algorithm) es un sistema que **genera automáticamente algoritmos GRASP válidos para VRPTW** usando:

1. **Gramática BNF**: Define qué combinaciones de operadores son válidas
2. **Generador**: Crea árboles sintácticos (AST) aleatorios respetando la gramática
3. **Intérprete**: Ejecuta los AST generados en instancias VRPTW
4. **Validador**: Asegura que algoritmos cumplen restricciones (GRASP, operadores, reparación)

### Objetivo

Generar **3 algoritmos GRASP automáticamente**, cada uno con:
- Diferentes **combinaciones de operadores**
- **Misma estructura general** (construcción → búsqueda local)
- Validación de **restricciones VRPTW** (capacidad, ventanas tiempo)
- Ejecución en **56 instancias Solomon**

### Reproducibilidad

- **Seed fijo**: 42 → mismos 3 algoritmos cada vez
- **Determinístico**: Mismo AST, mismo pseudocódigo
- **Reutilizable**: QUICK y FULL usan los 3 mismos algoritmos

---

## 🏗️ Componentes de GAA

### 1. AST Nodes (`gaa/ast_nodes.py`)

Nodos sintácticos que representan operaciones:

```python
# Clase base
class ASTNode:
    def execute(self, problem, seed): pass
    def to_dict(self): pass
    def to_pseudocode(self): pass
    def size(self): pass
    def depth(self): pass

# Nodos de control
class Seq(ASTNode):          # Secuencia de operaciones
    pass

class While(ASTNode):         # Bucle while con condición
    pass

class For(ASTNode):           # Bucle for con iteraciones
    pass

class If(ASTNode):            # Condicional if-then-else
    pass

class Call(ASTNode):          # Llamada a operador (terminal)
    pass

# Nodos especializados VRPTW
class ChooseBestOf(ASTNode):  # GRASP: n iteraciones
    pass

class ApplyUntilNoImprove(ASTNode):  # VND: hasta estancamiento
    pass

class LocalSearch(ASTNode):   # Contenedor de operadores mejora
    pass

class Construction(ASTNode):  # Contenedor de constructores
    pass

class Repair(ASTNode):        # Reparación de restricciones
    pass
```

### 2. Gramática (`gaa/grammar.py`)

Define operadores disponibles y reglas de composición:

```python
class Grammar:
    # Operadores constructivos
    CONSTRUCTIVE_TERMINALS = {
        'RandomizedInsertion': parameters={'alpha': [0.10, 0.15, 0.20]},
        'TimeOrientedNN': parameters={},
        'RegretInsertion': parameters={},
        'NearestNeighbor': parameters={},
    }
    
    # Operadores de mejora local
    IMPROVEMENT_TERMINALS = {
        # Intra-ruta
        'TwoOpt': parameters={'max_iterations': [10, 50, 100]},
        'OrOpt': parameters={'max_iterations': [5, 20, 50]},
        'ThreeOpt': parameters={'max_iterations': [10, 30]},
        'Relocate': parameters={'max_iterations': [10, 50]},
        
        # Inter-ruta
        'CrossExchange': parameters={'max_iterations': [10, 50]},
        'TwoOptStar': parameters={'max_iterations': [10, 30]},
        'SwapCustomers': parameters={'max_iterations': [10, 50]},
        'RelocateInter': parameters={'max_iterations': [10, 50]},
    }
    
    # Operadores de perturbación
    PERTURBATION_TERMINALS = {
        'EjectionChain': parameters={'intensity': [0.1, 0.3, 0.5]},
        'RuinRecreate': parameters={'destroy_rate': [0.2, 0.5, 0.8]},
        'RandomRemoval': parameters={'num_customers': [5, 10, 20]},
        'RouteElimination': parameters={'routes': [1, 2]},
    }
    
    # Operadores de reparación
    REPAIR_TERMINALS = {
        'RepairTimeWindows': parameters={},
        'RepairCapacity': parameters={},
        'GreedyRepair': parameters={},
    }
    
    # Condiciones de control
    CONDITIONS = {
        'Improves': 'nueva_solución es mejor',
        'Feasible': 'solución es factible (sin violaciones)',
        'Stagnation': 'sin mejora en k iteraciones',
        'TimeLimit': 'tiempo < límite',
    }
```

### 3. Generador (`gaa/generator.py`)

Crea árboles sintácticos aleatorios:

```python
class AlgorithmGenerator:
    def __init__(self, grammar: Grammar, seed: int = 42):
        self.grammar = grammar
        self.random = Random(seed)  # Reproducibilidad
    
    def generate_with_validation(self) -> Optional[ASTNode]:
        """Genera un AST válido para VRPTW"""
        # 1. Generar AST aleatorio
        ast = self._generate_grasp_structure()
        
        # 2. Validar según criterios
        if self._validate_vrptw_criteria(ast):
            return ast
        return None
    
    def _generate_grasp_structure(self) -> ASTNode:
        """
        Genera estructura GRASP:
        ChooseBestOf(
            iterations,
            Seq(
                Construction(RandomizedInsertion),
                Seq(
                    ApplyUntilNoImprove(Mejora1),
                    ApplyUntilNoImprove(Mejora2),
                    Repair(...)
                )
            )
        )
        """
        pass
    
    def _validate_vrptw_criteria(self, ast: ASTNode) -> bool:
        """Valida criterios obligatorios de VRPTW"""
        # ✅ Tiene constructor randomizado exactamente 1
        # ✅ Tiene 2+ operadores de mejora
        # ✅ Tiene criterio de iteración
        # ✅ Tiene reparación (recomendado)
        pass
    
    def generate_population(self, size: int) -> List[ASTNode]:
        """Genera población de N algoritmos"""
        return [self.generate_with_validation() for _ in range(size)]
```

### 4. Intérprete (`gaa/interpreter.py`)

Ejecuta AST en instancias VRPTW:

```python
class ExecutionContext:
    """Rastrea estado durante ejecución"""
    def __init__(self):
        self.iterations = 0
        self.evaluations = 0
        self.best_solution = None
        self.best_distance = float('inf')
        self.history = []  # Para gráficas de convergencia

class ASTInterpreter:
    def __init__(self, problem: VRPTWInstance, seed: int = 42):
        self.problem = problem
        self.context = ExecutionContext()
    
    def execute(self, ast: ASTNode) -> Optional[Solution]:
        """Ejecuta un AST en el problema"""
        try:
            solution = self._execute_node(ast)
            return solution
        except TimeoutError:
            return self.context.best_solution
        except Exception as e:
            print(f"❌ Error ejecutando AST: {e}")
            return None
    
    def _execute_node(self, node: ASTNode) -> Solution:
        """Ejecuta recursivamente cada nodo"""
        if isinstance(node, Construction):
            return self._execute_construction(node)
        elif isinstance(node, ChooseBestOf):
            return self._execute_grasp_iterations(node)
        elif isinstance(node, ApplyUntilNoImprove):
            return self._execute_local_search(node)
        elif isinstance(node, Repair):
            return self._execute_repair(node)
        elif isinstance(node, Seq):
            return self._execute_sequence(node)
        # ... más tipos de nodos
    
    def get_execution_report(self) -> Dict:
        """Retorna estadísticas de ejecución"""
        return {
            'iterations': self.context.iterations,
            'evaluations': self.context.evaluations,
            'best_distance': self.context.best_distance,
            'history': self.context.history,
            'time_seconds': ...,
        }
```

---

## 🔄 Estructura de Algoritmos GRASP

### Algoritmo GRASP Típico Generado

```
Algoritmo GRASP Generado (AST):
│
├─ ChooseBestOf(100)                    # 100 iteraciones GRASP
│  │
│  └─ Seq                               # Secuencia de fases
│     │
│     ├─ Construction                   # FASE 1: Construcción
│     │  └─ RandomizedInsertion(α=0.15)
│     │
│     └─ Seq                            # FASE 2: Búsqueda Local (VND)
│        │
│        ├─ ApplyUntilNoImprove         # Vecindario 1
│        │  ├─ Stmt: TwoOpt
│        │  └─ StopCondition: Stagnation(5)
│        │
│        ├─ ApplyUntilNoImprove         # Vecindario 2
│        │  ├─ Stmt: CrossExchange
│        │  └─ StopCondition: Stagnation(3)
│        │
│        └─ Repair                      # REPARACIÓN: Factibilidad
│           ├─ RepairTimeWindows
│           └─ RepairCapacity
```

### Ejemplos de 3 Algoritmos Generados

**Algoritmo 1**:
```
ChooseBestOf(100) [
  RandomizedInsertion(α=0.15)
  VND { TwoOpt, OrOpt, RepairTimeWindows }
]
```

**Algoritmo 2**:
```
ChooseBestOf(100) [
  RegretInsertion()
  VND { CrossExchange, SwapCustomers, RepairCapacity }
]
```

**Algoritmo 3**:
```
ChooseBestOf(100) [
  TimeOrientedNN()
  VND { TwoOpt, TwoOptStar, CrossExchange, RepairTimeWindows }
]
```

---

## 🎯 Operadores VRPTW-GRASP

### Operadores Constructivos

```python
# Constructor GRASP: Inserción Randomizada
class RandomizedInsertion:
    """
    Inserta clientes basándose en:
    1. Calcular costo de inserción en cada posición
    2. Crear RCL (Restricted Candidate List) basada en α
    3. Seleccionar aleatoriamente de RCL
    """
    def __init__(self, alpha: float = 0.15):
        self.alpha = alpha  # 0=greedy, 1=random
    
    def execute(self, problem, seed) -> Solution:
        # Retorna solución inicial con demandas asignadas
        pass

# Otros constructores
class TimeOrientedNN:
    """Vecino más cercano priorizando urgencia temporal"""
    pass

class RegretInsertion:
    """Inserción por arrepentimiento"""
    pass

class NearestNeighbor:
    """Vecino más cercano simple"""
    pass
```

### Operadores de Mejora Local (Intra-ruta)

```python
class TwoOpt:
    """2-opt: elimina 2 aristas y reconecta"""
    def __init__(self, max_iterations: int = 100):
        self.max_iterations = max_iterations
    
    def execute(self, solution, problem, seed) -> Solution:
        # Retorna solución mejorada (o igual si no hay mejora)
        pass

class OrOpt:
    """Reubica secuencias de 1-3 clientes"""
    def __init__(self, max_iterations: int = 50):
        self.max_iterations = max_iterations
    pass

class ThreeOpt:
    """3-opt: más intensivo que 2-opt"""
    pass

class Relocate:
    """Mueve un cliente a otra posición"""
    pass
```

### Operadores de Mejora Local (Inter-ruta)

```python
class CrossExchange:
    """Intercambia segmentos entre rutas"""
    def __init__(self, max_iterations: int = 50):
        self.max_iterations = max_iterations
    pass

class TwoOptStar:
    """2-opt* entre dos rutas diferentes"""
    pass

class SwapCustomers:
    """Intercambia clientes entre rutas"""
    def __init__(self, max_iterations: int = 50):
        self.max_iterations = max_iterations
    pass

class RelocateInter:
    """Mueve cliente de una ruta a otra"""
    pass
```

### Operadores de Reparación

```python
class RepairTimeWindows:
    """Ajusta rutas para cumplir ventanas de tiempo"""
    def execute(self, solution, problem) -> Solution:
        # Asegura que ALL_CLIENTS están visitados en [a_i, b_i]
        # Retorna solución reparada o None si no es posible
        pass

class RepairCapacity:
    """Repara violaciones de capacidad"""
    def execute(self, solution, problem) -> Solution:
        # Asegura que cada ruta ≤ Q
        # Redestribuye clientes si es necesario
        pass

class GreedyRepair:
    """Reparación voraz genérica"""
    def execute(self, solution, problem) -> Solution:
        # Intenta reparar manteniendo estructura
        pass
```

### Operadores de Perturbación

```python
class EjectionChain:
    """Cadenas de eyección de clientes"""
    def __init__(self, intensity: float = 0.3):
        self.intensity = intensity  # Proporción a perturbar
    pass

class RuinRecreate:
    """Destruye parcialmente rutas y reconstruye"""
    def __init__(self, destroy_rate: float = 0.5):
        self.destroy_rate = destroy_rate
    pass

class RandomRemoval:
    """Remueve aleatoriamente k clientes y reinserta"""
    def __init__(self, num_customers: int = 10):
        self.num_customers = num_customers
    pass

class RouteElimination:
    """Elimina una ruta completa y redistribuye"""
    def __init__(self, routes: int = 1):
        self.routes = routes
    pass
```

---

## 📐 Gramática BNF

### Sintaxis Formal

```bnf
<Algorithm> ::= ChooseBestOf(<Iterations>, <RASPBody>)

<RASPBody> ::= Seq(
    <Construction>,
    <LocalSearch>,
    <Repair>
)

<Construction> ::= Call(<ConstructorOperator>)
<ConstructorOperator> ::= RandomizedInsertion | TimeOrientedNN | RegretInsertion | NearestNeighbor

<LocalSearch> ::= ApplyUntilNoImprove(<Operator>, <StopCondition>)
              | Seq(<Operator>, <Operator>, ...) [Multiple VND]

<Operator> ::= TwoOpt | OrOpt | ThreeOpt | Relocate      [Intra-ruta]
           | CrossExchange | TwoOptStar | SwapCustomers   [Inter-ruta]

<Repair> ::= Call(RepairTimeWindows) | Call(RepairCapacity) | Call(GreedyRepair)

<StopCondition> ::= Stagnation(<MaxIter>)
               | TimeLimit(<Seconds>)
               | Improving   # Mientras haya mejora

<Iterations> ::= 50 | 100 | 200  [Configurable]
```

### Restricciones

**OBLIGATORIAS (cada AST generado DEBE cumplir)**:

1. ✅ **Constructor Randomizado**: Exactamente 1
   - Garantiza componente aleatoria (GRASP)
   
2. ✅ **Operadores Mejora Local**: 2 mínimo
   - Recomendado: 1 intra-ruta + 1 inter-ruta
   - Permite VND (Variable Neighborhood Descent)

3. ✅ **Criterio de Iteración**: Exactamente 1
   - ChooseBestOf(n) o ApplyUntilNoImprove con condición

4. ⚠️ **Reparación**: Altamente recomendada
   - VRPTW tiene restricciones duras
   - Sin reparación = soluciones infactibles

---

## 🔧 Proceso de Generación

### Flujo de Generación

```
1. Inicializar Generador(seed=42, grammar)
           ↓
2. Generar AST aleatorio respetando BNF
           ↓
3. Validar restricciones VRPTW
   - ✓ Constructor randomizado?
   - ✓ 2+ operadores mejora?
   - ✓ Criterio iteración?
   - ✓ Reparación?
           ↓
4. Si falla validación → Reintentar (max 5 veces)
           ↓
5. Retornar AST válido
           ↓
6. Repetir 5 veces más → 3 algoritmos finales
```

### Código Pseudocódigo

```python
# En demo_experimentation_quick.py
def generate_algorithms_once():
    """Genera 3 algoritmos VRPTW-GRASP y los guarda"""
    
    # 1. Crear gramática
    grammar = Grammar(
        min_depth=2,
        max_depth=3,
        constructors=['RandomizedInsertion', 'TimeOrientedNN', 'RegretInsertion'],
        improvements=['TwoOpt', 'OrOpt', 'CrossExchange', 'SwapCustomers'],
        repairs=['RepairTimeWindows', 'RepairCapacity']
    )
    
    # 2. Crear generador con seed fijo
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    # 3. Generar 3 algoritmos
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'GAA_Algorithm_{i+1}',
                'ast': ast,
                'pseudocode': ast.to_pseudocode(),
                'properties': grammar.get_statistics(ast)
            })
    
    # 4. Guardar algoritmos
    for algo in algorithms:
        save_algorithm_json(algo['ast'], f"GAA_Algorithm_{algo['name']}.json")
    
    return algorithms
```

---

## ⚡ Ejecución de Algoritmos

### Ejecución Individual

```python
def execute_algorithm_instance(algorithm_ast, problem_instance, seed=42):
    """Ejecuta un AST en una instancia VRPTW"""
    
    # 1. Crear intérprete
    interpreter = ASTInterpreter(problem_instance, seed=seed)
    
    # 2. Ejecutar AST
    solution = interpreter.execute(algorithm_ast)
    
    # 3. Obtener reporte
    report = interpreter.get_execution_report()
    
    return {
        'solution': solution,
        'metrics': {
            'distance': solution.total_distance,
            'vehicles': solution.num_vehicles,
            'violations_capacity': solution.count_capacity_violations(),
            'violations_time_windows': solution.count_time_window_violations(),
            'feasible': solution.is_feasible(),
            'gap_to_bks': (solution.distance - bks_distance) / bks_distance * 100,
        },
        'execution': {
            'iterations': report['iterations'],
            'evaluations': report['evaluations'],
            'time_seconds': report['time_seconds'],
            'convergence_history': report['history'],
        }
    }
```

### Ejecución en Batch (QUICK/FULL)

```python
def run_experiment_mode(mode='quick'):
    """
    Ejecuta experimento completo
    mode = 'quick' → R1 (12 instancias, 36 experimentos)
    mode = 'full' → R1+R2+C1+C2+RC1+RC2 (56 instancias, 168 experimentos)
    """
    
    # 1. Generar 3 algoritmos UNA SOLA VEZ
    algorithms = generate_algorithms_once()  # seed=42
    
    # 2. Cargar instancias según modo
    if mode == 'quick':
        families = ['R1']  # Solo R1
    else:  # full
        families = ['R1', 'R2', 'C1', 'C2', 'RC1', 'RC2']
    
    instances = load_instances(families)
    
    # 3. Matriz de experimentos
    results = []
    total_experiments = len(algorithms) * len(instances) * 1  # 1 repetición
    
    for idx, (algorithm, instance) in enumerate(
        product(algorithms, instances)
    ):
        print(f"[{idx+1}/{total_experiments}] Ejecutando...")
        result = execute_algorithm_instance(
            algorithm['ast'],
            instance,
            seed=42
        )
        results.append({
            'algorithm': algorithm['name'],
            'instance': instance.name,
            'result': result
        })
    
    # 4. Análisis estadístico
    analyze_results(results)
    
    # 5. Generar visualizaciones
    generate_plots(results)
```

---

## 💬 Output al Usuario

### 1. Durante Generación de Algoritmos

```
================================================================================
  GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA) - VRPTW-GRASP
================================================================================

🧬 FASE 1: CREAR GRAMÁTICA
--------------------------------------------------------------------------------
✅ Gramática VRPTW-GRASP creada
   • Operadores constructivos: 4 (RandomizedInsertion, TimeOrientedNN, ...)
   • Operadores de mejora: 8 (TwoOpt, OrOpt, CrossExchange, ...)
   • Operadores de reparación: 3 (RepairTimeWindows, RepairCapacity, ...)
   • Límites: profundidad mín=2, máx=3

🤖 FASE 2: GENERAR 3 ALGORITMOS (seed=42)
--------------------------------------------------------------------------------

✅ Algoritmo 1: GAA_Algorithm_1
   Nodos: 8, Profundidad: 3
   Validación: ✓ Constructor randomizado ✓ 2+ mejora ✓ Reparación
   
   Pseudocódigo:
   ├─ ChooseBestOf(100 iteraciones GRASP)
   │  └─ Seq
   │     ├─ Construction: RandomizedInsertion(α=0.15)
   │     ├─ LocalSearch
   │     │  ├─ ApplyUntilNoImprove: TwoOpt (max_iter=100)
   │     │  └─ ApplyUntilNoImprove: CrossExchange (max_iter=50)
   │     └─ Repair: RepairTimeWindows → RepairCapacity

✅ Algoritmo 2: GAA_Algorithm_2
   Nodos: 7, Profundidad: 3
   Validación: ✓ Constructor randomizado ✓ 2+ mejora ✓ Reparación
   
   Pseudocódigo:
   ├─ ChooseBestOf(100 iteraciones GRASP)
   │  └─ Seq
   │     ├─ Construction: RegretInsertion()
   │     ├─ LocalSearch
   │     │  ├─ ApplyUntilNoImprove: OrOpt (max_iter=50)
   │     │  └─ ApplyUntilNoImprove: SwapCustomers (max_iter=50)
   │     └─ Repair: RepairCapacity → GreedyRepair

✅ Algoritmo 3: GAA_Algorithm_3
   Nodos: 9, Profundidad: 3
   Validación: ✓ Constructor randomizado ✓ 2+ mejora ✓ Reparación
   
   Pseudocódigo:
   ├─ ChooseBestOf(100 iteraciones GRASP)
   │  └─ Seq
   │     ├─ Construction: TimeOrientedNN()
   │     ├─ LocalSearch
   │     │  ├─ ApplyUntilNoImprove: TwoOpt (max_iter=100)
   │     │  ├─ ApplyUntilNoImprove: TwoOptStar (max_iter=50)
   │     │  └─ ApplyUntilNoImprove: CrossExchange (max_iter=50)
   │     └─ Repair: RepairTimeWindows

📁 Algoritmos guardados en: output/algorithms/
   ✓ GAA_Algorithm_1.json
   ✓ GAA_Algorithm_2.json
   ✓ GAA_Algorithm_3.json
   ✓ algorithms_pseudocode.md

================================================================================

```

### 2. Durante Ejecución de Experimentos

```
================================================================================
  TEST QUICK: VALIDACIÓN RÁPIDA (Familia R1 - 12 instancias)
================================================================================

📊 MATRIZ: 12 instancias × 3 algoritmos × 1 rep = 36 experimentos
⏱️  Tiempo estimado: 5-10 minutos

[1/36]  R101 × GAA_Algorithm_1
   ✓ Construcción: 5 vehículos (α=0.15)
   ✓ Mejora 1 (TwoOpt): 5 → 4 vehículos (20 iteraciones)
   ✓ Mejora 2 (CrossExchange): 4 vehículos (sin cambios, 15 iteraciones)
   ✓ Reparación: ✓ Factible (sin violaciones)
   📈 RESULTADO: Distancia=1247.8, Vehículos=4, Gap=2.1%
   ⏱️  Tiempo: 2.3s

[2/36]  R101 × GAA_Algorithm_2
   ✓ Construcción: 5 vehículos
   ✓ Mejora 1 (OrOpt): 5 → 4 vehículos
   ✓ Mejora 2 (SwapCustomers): 4 vehículos (sin cambios)
   ✓ Reparación: ✓ Factible
   📈 RESULTADO: Distancia=1253.4, Vehículos=4, Gap=2.4%
   ⏱️  Tiempo: 2.1s

[3/36]  R101 × GAA_Algorithm_3
   ✓ Construcción: 6 vehículos
   ✓ Mejora 1 (TwoOpt): 6 → 4 vehículos
   ✓ Mejora 2 (TwoOptStar): 4 → 4 vehículos (sin cambios)
   ✓ Mejora 3 (CrossExchange): 4 vehículos
   ✓ Reparación: ✓ Factible
   📈 RESULTADO: Distancia=1241.2, Vehículos=4, Gap=1.8% ⭐
   ⏱️  Tiempo: 2.8s

... (33 experimentos más)

[36/36] RC102 × GAA_Algorithm_2
   ✓ Construcción: 5 vehículos
   ✓ Mejora: Mejoras aplicadas
   ✓ Reparación: ✓ Factible
   📈 RESULTADO: Distancia=1156.7, Vehículos=5, Gap=1.2%
   ⏱️  Tiempo: 2.2s

================================================================================
  ✅ EXPERIMENTOS COMPLETADOS: 36/36
================================================================================

📊 RESUMEN ESTADÍSTICO:
   Experimentos exitosos: 36/36 (100%)
   Soluciones factibles: 36/36 (100%)
   
   • GAA_Algorithm_1: Gap promedio=2.3% (±1.2%)
   • GAA_Algorithm_2: Gap promedio=2.5% (±1.4%)
   • GAA_Algorithm_3: Gap promedio=2.1% (±1.1%) ← MEJOR
   
   Test de Kruskal-Wallis: p-value=0.024 *
   → Diferencias estadísticamente significativas

🏆 MEJOR ALGORITMO (en QUICK test): GAA_Algorithm_3
   (RandomizedInsertion + TwoOpt + TwoOptStar + CrossExchange)

📈 GRÁFICAS GENERADAS: 20 archivos PNG
   • gap_comparison_boxplot.png
   • gap_comparison_bars.png
   • quality_vs_time_scatter.png
   • convergence_curves.png
   • vehicles_used_comparison.png
   • routes_detailed_R101.png ... routes_detailed_RC102.png (12 gráficas)

📁 SALIDA: output/plots_vrptw_QUICK_20260101_120000/

================================================================================
```

### 3. Ejemplo Interactivo Simplificado

```python
# Usuario ejecuta:
python scripts/demo_experimentation_quick.py

# SALIDA:
🧬 Generando 3 algoritmos GRASP automáticamente (seed=42)...
   ✓ GAA_Algorithm_1 generado (8 nodos)
   ✓ GAA_Algorithm_2 generado (7 nodos)
   ✓ GAA_Algorithm_3 generado (9 nodos)

📂 Algoritmos guardados en: output/algorithms/

🚀 Iniciando QUICK test: Familia R1 (12 instancias)

   [████████████████████░░░░░░░░░░░░░░░░░░░░░░] 15% (5/36)
   
   Ejecutando: R102 × GAA_Algorithm_2
   • Construcción: 5 vehículos (2.1s)
   • Mejoras locales: 5 → 4 (1.2s)
   • Reparación: ✓ Factible
   • RESULTADO: Gap=2.4%

   [████████████████████████████████████████░░] 95% (34/36)

✅ COMPLETADO: 36 experimentos en 8 minutos 23 segundos

📊 MEJOR ALGORITMO: GAA_Algorithm_3 (Gap=2.1%)

📁 Salida en: output/plots_vrptw_QUICK_20260101_120000/
```

---

## 📂 Estructura de Directorios

```
VRPTW-GRASP/
├── gaa/                                    # Módulo GAA
│   ├── ast_nodes.py                       # Nodos sintácticos
│   ├── grammar.py                         # Gramática BNF
│   ├── generator.py                       # Generador de AST
│   ├── interpreter.py                     # Intérprete de AST
│   ├── __init__.py                        # Exportación
│   └── README.md                          # Documentación módulo
│
├── scripts/
│   ├── demo_experimentation_quick.py      # Test rápido (1 familia)
│   │   • Genera 3 algoritmos con seed=42
│   │   • Ejecuta en R1 (12 instancias)
│   │   • 36 experimentos
│   │   • Output: 20 archivos
│   │
│   └── demo_experimentation_full.py       # Test completo (6 familias)
│       • Reutiliza 3 algoritmos de quick
│       • Ejecuta en todas familias (56 instancias)
│       • 168 experimentos
│       • Output: 70 archivos
│
├── output/
│   ├── algorithms/                        # Algoritmos generados
│   │   ├── GAA_Algorithm_1.json           # AST serializado
│   │   ├── GAA_Algorithm_2.json
│   │   ├── GAA_Algorithm_3.json
│   │   └── algorithms_pseudocode.md
│   │
│   ├── experiments/
│   │   ├── vrptw_experiments_QUICK_YYYYMMDD_HHMMSS/
│   │   │   └── experiment_quick_*.json    (36 resultados)
│   │   │
│   │   └── vrptw_experiments_FULL_YYYYMMDD_HHMMSS/
│   │       └── experiment_full_*.json     (168 resultados)
│   │
│   └── plots/
│       ├── plots_vrptw_QUICK_YYYYMMDD_HHMMSS/
│       │   ├── gap_comparison_*.png
│       │   ├── routes_detailed_*.png
│       │   ├── README.md
│       │   └── time_tracking.md
│       │
│       └── plots_vrptw_FULL_YYYYMMDD_HHMMSS/
│           ├── gap_comparison_*.png
│           ├── performance_by_family.png
│           ├── family_R_statistics.md
│           ├── family_C_statistics.md
│           ├── family_RC_statistics.md
│           ├── routes_detailed_*.png
│           ├── README.md
│           └── time_tracking.md
│
├── GAA_IMPLEMENTACION_VRPTW.md           # Este documento
└── ...
```

---

## 🔍 Validación de Algoritmos Generados

### Checklist de Validación

Para que un algoritmo generado sea considerado **válido para VRPTW**:

```
✅ Constructor Randomizado:
   □ Exactamente 1 constructor
   □ Es de tipo: RandomizedInsertion | TimeOrientedNN | RegretInsertion | NearestNeighbor
   □ Si RandomizedInsertion: tiene parámetro α definido

✅ Operadores de Mejora Local:
   □ Mínimo 2 operadores
   □ Incluye intra-ruta: TwoOpt OR OrOpt OR ThreeOpt OR Relocate
   □ Incluye inter-ruta: CrossExchange OR TwoOptStar OR SwapCustomers OR RelocateInter
   □ Cada uno tiene max_iterations configurado

✅ Criterio de Iteración:
   □ Exactamente 1 estrategia de control
   □ Es de tipo: ChooseBestOf(n) OR ApplyUntilNoImprove(cond)
   □ Tiene límite de iteraciones o estancamiento

✅ Reparación:
   □ Incluye RepairTimeWindows o RepairCapacity
   □ Se ejecuta DESPUÉS de búsqueda local
   □ Garantiza factibilidad

❌ Rechaza:
   □ Constructores sin aleatoriedad (puro greedy)
   □ Menos de 2 operadores mejora
   □ Sin reparación (advertencia pero no rechazo)
   □ Estructura no es GRASP (sin construcción randomizada)
```

---

## 📝 Ejemplo Completo: Implementación en Script

```python
# scripts/demo_experimentation_quick.py

import sys
from pathlib import Path

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import ASTInterpreter
from data.loader import DatasetLoader
from utils import OutputManager

def main():
    print("\n" + "="*80)
    print("  GAA-QUICK: TEST RÁPIDO VRPTW-GRASP")
    print("="*80 + "\n")
    
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="quick")
    
    # FASE 1: Generar algoritmos
    print("🧬 GENERANDO 3 ALGORITMOS GRASP (seed=42)...")
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar, seed=42)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append(ast)
            print(f"   ✓ GAA_Algorithm_{i+1} ({ast.size()} nodos)")
    
    # FASE 2: Cargar instancias
    print(f"\n📦 Cargando instancias Familia R1...")
    loader = DatasetLoader("datasets")
    instances = loader.load_folder("R1")
    print(f"   ✓ {len(instances)} instancias cargadas")
    
    # FASE 3: Ejecutar experimentos
    print(f"\n🚀 Ejecutando {len(algorithms) * len(instances)} experimentos...")
    
    results = []
    for alg_idx, algorithm in enumerate(algorithms):
        for inst_idx, instance in enumerate(instances):
            total = len(algorithms) * len(instances)
            current = alg_idx * len(instances) + inst_idx + 1
            
            interpreter = ASTInterpreter(instance, seed=42)
            solution = interpreter.execute(algorithm)
            
            results.append({
                'algorithm_id': alg_idx + 1,
                'instance': instance.name,
                'distance': solution.distance,
                'vehicles': solution.num_vehicles,
                'gap': compute_gap(solution, instance.bks),
            })
            
            print(f"   [{current}/{total}] {instance.name} × Alg{alg_idx+1}: "
                  f"Gap={results[-1]['gap']:.1f}%")
    
    # FASE 4: Guardar y analizar
    print(f"\n📊 Analizando resultados...")
    analyze_and_plot(results, session_dir)
    
    print(f"\n✅ Test completado en {session_dir}")

if __name__ == "__main__":
    main()
```

---

## 🎯 Conclusión

**GAA en VRPTW-GRASP** implementa:

1. ✅ **Generación automática** de 3 algoritmos GRASP válidos
2. ✅ **Validación de restricciones** específicas del problema
3. ✅ **Reproducibilidad** con seed=42
4. ✅ **Información clara** al usuario durante ejecución
5. ✅ **Estructura extensible** para futuras mejoras

**Próximos pasos**:
- Implementar módulos AST, Grammar, Generator, Interpreter
- Crear scripts quick.py y full.py
- Agregar visualizaciones de algoritmos generados
- Implementar análisis estadístico comparativo

---

**Documento**: Especificación GAA VRPTW-GRASP  
**Versión**: 1.0  
**Status**: Listo para Implementación  
**Basado en**: GAA-GCP-ILS-4  
**Fecha**: 1 de Enero de 2026
