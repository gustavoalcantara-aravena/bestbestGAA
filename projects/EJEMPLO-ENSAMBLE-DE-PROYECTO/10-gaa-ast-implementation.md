# 🤖 GAA: Generación Automática de Algoritmos VRPTW-GRASP

## Tabla de Contenidos

1. [Introducción a GAA](#introducción-a-gaa)
2. [Representación AST](#representación-ast)
3. [Nodos del AST](#nodos-del-ast)
4. [Generación de Algoritmos](#generación-de-algoritmos)
5. [Operadores Genéticos](#operadores-genéticos)
6. [Interpretación y Ejecución](#interpretación-y-ejecución)
7. [Integración con VRPTW-GRASP](#integración-con-vrptw-grasp)
8. [Ejemplo Completo](#ejemplo-completo)

---

## Introducción a GAA

### ¿Qué es GAA?

**GAA (Genetic Algorithm Approach)** es un sistema que:

- **Genera automáticamente** algoritmos válidos para VRPTW-GRASP
- **Representa** cada algoritmo como un **Árbol de Sintaxis Abstracta (AST)**
- **Evoluciona** estos algoritmos mediante **Algoritmos Genéticos (GA)**
- **Selecciona** automáticamente los mejores operadores y configuraciones

### Motivación

Lugar de implementar manualmente cada combinación de operadores VRPTW, GAA:

```
Operadores Constructivos (6)
    × Operadores de Mejora (8)
    × Operadores de Perturbación (4)
    = 192 combinaciones posibles

GAA busca automáticamente la mejor combinación
```

### Flujo General

```
┌─────────────────┐
│  Gramática BNF  │
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ Generador de AST │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌─────────────────┐
│  Población AST   │────▶│  Algoritmo Gen. │
└────────┬─────────┘     └────────┬────────┘
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌─────────────────┐
│ Interpretador    │     │ Mutación/Crossover
│ (ejecuta AST)    │     └────────┬────────┘
└────────┬─────────┘              │
         │                        ▼
         ▼                  ┌─────────────┐
┌──────────────────┐       │ Nueva Gen.  │
│ VRPTW Instancia  │       └─────────────┘
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Fitness Score   │
└──────────────────┘
```

---

## Representación AST

### Concepto

Un **AST (Abstract Syntax Tree)** es una estructura jerárquica que representa un algoritmo:

```
Algoritmo GRASP Típico:

            ┌─────────┐
            │   Seq   │ (Secuencia)
            └────┬────┘
         ┌──────┴──────┐
         ▼             ▼
   ┌──────────┐   ┌─────────┐
   │Construct │   │ While   │ (bucle de iteraciones)
   │ (NNSE)   │   │(100 iter)
   └──────────┘   └────┬────┘
                       │
                   ┌───┴───┐
                   ▼       ▼
              ┌─────┐  ┌──────────┐
              │Local│  │Perturbat.│
              │Search  │(Eject.)  │
              │(2-opt)  └──────────┘
              └─────┘
```

### Propiedades

| Propiedad | Valor | Descripción |
|-----------|-------|-------------|
| **Profundidad máxima** | 4 | Anidamiento máximo de nodos |
| **Nodos totales** | 5-20 | Típicamente 8-12 nodos |
| **Determinismo** | Fijo | Genera una solución única |
| **Validez** | Garantizada | Siempre ejecutable |

### Ventajas del AST

✅ **Composicional**: Combina operadores de manera válida  
✅ **Ejecutable**: Puede interpretarse directamente  
✅ **Evolvable**: Fácil de mutar y recombinar  
✅ **Análisis**: Permite inspeccionar la estructura del algoritmo  

---

## Nodos del AST

### Nodos de Control

#### 1. **Seq** (Secuencia)

Ejecuta operaciones en orden secuencial.

```python
@dataclass
class Seq(ASTNode):
    """Secuencia de operaciones"""
    body: List[ASTNode]
    
    def execute(self, problem, solution):
        """Ejecuta cada operación en orden"""
        for operation in self.body:
            solution = operation.execute(problem, solution)
        return solution
```

**Ejemplo:**
```
Seq(body=[
    GreedyConstruct(heuristic="NearestNeighbor"),
    LocalSearch(operator="TwoOpt")
])
```

#### 2. **While** (Bucle Iterativo)

Itera mientras se cumple condición o no se alcanza límite.

```python
@dataclass
class While(ASTNode):
    """Bucle con límite de iteraciones"""
    max_iterations: int
    body: ASTNode
    
    def execute(self, problem, solution):
        """Ejecuta cuerpo hasta MAX_ITERATIONS"""
        for _ in range(self.max_iterations):
            solution = self.body.execute(problem, solution)
        return solution
```

**Ejemplo:**
```
While(max_iterations=100, body=
    LocalSearch(operator="OrOpt")
)
```

#### 3. **If** (Condicional)

Ejecuta rama según condición evaluada.

```python
@dataclass
class If(ASTNode):
    """Condicional: Si mejora, hacer A; sino, hacer B"""
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None
    
    def execute(self, problem, solution):
        """Ejecuta rama según mejora"""
        improved = self.then_branch.execute(problem, solution)
        if is_better(improved, solution):
            return improved
        elif self.else_branch:
            return self.else_branch.execute(problem, solution)
        return solution
```

**Ejemplo:**
```
If(
    then_branch=LocalSearch(operator="ThreeOpt"),
    else_branch=Perturbation(operator="EjectionChain")
)
```

#### 4. **For** (Bucle de Iteraciones Fijas)

Itera N veces con propósito de multi-start.

```python
@dataclass
class For(ASTNode):
    """Bucle multi-start: repite N veces"""
    iterations: int
    body: ASTNode
    
    def execute(self, problem, solution):
        """Ejecuta N veces, mantiene mejor"""
        best = solution
        for _ in range(self.iterations):
            current = self.body.execute(problem, solution.copy())
            if is_better(current, best):
                best = current
        return best
```

**Ejemplo:**
```
For(iterations=5, body=
    Seq(body=[
        GreedyConstruct(heuristic="Savings"),
        LocalSearch(operator="TwoOpt")
    ])
)
```

### Nodos de Operadores VRPTW

#### 5. **GreedyConstruct** (Construcción)

Heurística constructiva inicial.

```python
@dataclass
class GreedyConstruct(ASTNode):
    """Heurística constructiva greedy"""
    heuristic: str  # Una de: NNSE, Savings, Sweep, etc.
    
    def execute(self, problem, solution):
        """Ejecuta heurística constructiva"""
        from operators import CONSTRUCTIVE_OPS
        constructor = CONSTRUCTIVE_OPS[self.heuristic]()
        return constructor.construct(problem)
```

**Valores válidos:**
- `"NearestNeighbor"` → GreedyNN
- `"SavingsHeuristic"` → Savings
- `"SweepAlgorithm"` → Sweep
- `"TimeOrientedNN"` → TNN
- `"RegretInsertion"` → Regret
- `"RandomizedInsertion"` → Random

#### 6. **LocalSearch** (Búsqueda Local)

Operador de mejora intra o inter-ruta.

```python
@dataclass
class LocalSearch(ASTNode):
    """Búsqueda local iterativa"""
    operator: str         # Operador: TwoOpt, OrOpt, etc.
    max_iterations: int   # Máximo de iteraciones
    
    def execute(self, problem, solution):
        """Ejecuta búsqueda local"""
        from operators import LOCAL_SEARCH_OPS
        searcher = LOCAL_SEARCH_OPS[self.operator]()
        return searcher.improve(solution, max_iterations=self.max_iterations)
```

**Valores válidos:**
- Intra-ruta: `"TwoOpt"`, `"OrOpt"`, `"ThreeOpt"`, `"Relocate"`
- Inter-ruta: `"CrossExchange"`, `"TwoOptStar"`, `"SwapCustomers"`, `"RelocateInter"`

#### 7. **Perturbation** (Perturbación)

Operador de diversificación.

```python
@dataclass
class Perturbation(ASTNode):
    """Perturbación de solución para escapar óptimos locales"""
    operator: str  # EjectionChain, RuinRecreate, etc.
    strength: int = 2  # Intensidad: 1-5
    
    def execute(self, problem, solution):
        """Ejecuta perturbación"""
        from operators import PERTURBATION_OPS
        perturber = PERTURBATION_OPS[self.operator]()
        return perturber.perturb(solution, strength=self.strength)
```

**Valores válidos:**
- `"EjectionChain"` → Ejecución encadenada
- `"RuinRecreate"` → Destrucción y reconstrucción
- `"RandomRemoval"` → Remoción aleatoria
- `"RouteElimination"` → Eliminación de ruta

---

## Generación de Algoritmos

### Gramática BNF

La gramática define qué estructuras AST son válidas:

```bnf
<Algorithm> ::= <Construction> <Improvement> |
                <IterativeAlg> |
                <MultiStartAlg> |
                <ComplexAlg>

<Construction> ::= GreedyConstruct(<heuristic>)
<heuristic> ::= "NearestNeighbor" | "Savings" | "Sweep" | ...

<Improvement> ::= LocalSearch(<operator>, <iterations>)
<operator> ::= "TwoOpt" | "OrOpt" | "ThreeOpt" | ...
<iterations> ::= 50 | 100 | 200

<IterativeAlg> ::= Seq(body=[
                     <Construction>,
                     While(max_iterations=<iterations>, body=<Improvement>)
                   ])

<MultiStartAlg> ::= For(iterations=<count>, body=
                     Seq(body=[<Construction>, <Improvement>])
                   )

<ComplexAlg> ::= Seq(body=[
                   <Construction>,
                   If(then_branch=<Improvement>,
                      else_branch=<Perturbation>)
                 ])

<Perturbation> ::= Perturbation(<operator>, strength=<strength>)
```

### Generador Aleatorio

```python
class AlgorithmGenerator:
    """Genera AST válido según gramática"""
    
    def __init__(self, seed=None):
        self.rng = np.random.Generator(np.random.PCG64(seed))
    
    def generate(self, max_depth=3):
        """Genera algoritmo aleatorio válido"""
        return self._generate_at_depth(0, max_depth)
    
    def _generate_simple(self):
        """Patrón simple: Construcción + Mejora"""
        construction = GreedyConstruct(
            heuristic=self.rng.choice([
                "NearestNeighbor", "Savings", "Sweep", 
                "TimeOrientedNN", "RegretInsertion"
            ])
        )
        improvement = LocalSearch(
            operator=self.rng.choice([
                "TwoOpt", "OrOpt", "ThreeOpt", "Relocate"
            ]),
            max_iterations=self.rng.choice([50, 100, 200])
        )
        return Seq(body=[construction, improvement])
    
    def _generate_iterative(self):
        """Patrón iterativo: Construcción + Bucle"""
        construction = GreedyConstruct(heuristic=...)
        improvement = LocalSearch(operator=...)
        loop = While(
            max_iterations=self.rng.choice([100, 200, 500]),
            body=improvement
        )
        return Seq(body=[construction, loop])
    
    def _generate_multistart(self):
        """Patrón multi-start: For + Seq"""
        construction = GreedyConstruct(heuristic=...)
        improvement = LocalSearch(operator=...)
        body = Seq(body=[construction, improvement])
        return For(
            iterations=self.rng.choice([3, 5, 10]),
            body=body
        )
    
    def _generate_complex(self):
        """Patrón complejo: Construcción + If + Perturbación"""
        construction = GreedyConstruct(heuristic=...)
        improvement = LocalSearch(operator=...)
        perturbation = Perturbation(operator=...)
        conditional = If(
            then_branch=improvement,
            else_branch=perturbation
        )
        return Seq(body=[construction, conditional])
```

### Patrones Generados

El generador produce 4 patrones principales:

| Patrón | Estructura | Complejidad | Uso |
|--------|-----------|-------------|-----|
| **Simple** | Construcción + Mejora | ⭐ Baja | Instancias pequeñas |
| **Iterativo** | Construcción + While(Mejora) | ⭐⭐ Media | Instancias medianas |
| **Multi-start** | For(Construcción + Mejora) | ⭐⭐ Media | Exploración |
| **Complejo** | Construcción + If(Mejora, Perturbación) | ⭐⭐⭐ Alta | Instancias grandes |

---

## Operadores Genéticos

### 1. Mutación de AST

Cambia aleatoriamente un nodo del árbol.

```python
def mutate_ast(ast: ASTNode, mutation_rate: float = 0.3) -> ASTNode:
    """Muta AST reemplazando un nodo aleatorio"""
    
    # Copiar árbol
    mutated = deepcopy(ast)
    
    # Obtener todos los nodos
    all_nodes = mutated.get_all_nodes()
    
    if not all_nodes or random.random() > mutation_rate:
        return mutated
    
    # Seleccionar nodo aleatorio para mutar
    node_to_mutate = random.choice(all_nodes)
    
    # Mutar según tipo
    if isinstance(node_to_mutate, GreedyConstruct):
        node_to_mutate.heuristic = random.choice([
            "NearestNeighbor", "Savings", "Sweep", ...
        ])
    
    elif isinstance(node_to_mutate, LocalSearch):
        node_to_mutate.operator = random.choice([
            "TwoOpt", "OrOpt", "ThreeOpt", ...
        ])
        node_to_mutate.max_iterations = random.choice([50, 100, 200])
    
    elif isinstance(node_to_mutate, While):
        node_to_mutate.max_iterations = random.choice([100, 200, 500])
    
    elif isinstance(node_to_mutate, Perturbation):
        node_to_mutate.operator = random.choice([
            "EjectionChain", "RuinRecreate", ...
        ])
        node_to_mutate.strength = random.randint(1, 5)
    
    return mutated
```

**Ejemplo:**

```
Antes:
Seq(body=[
    GreedyConstruct("NearestNeighbor"),  ◄─ MUTA
    LocalSearch("TwoOpt", 100)
])

Después:
Seq(body=[
    GreedyConstruct("Savings"),          ◄─ CAMBIÓ
    LocalSearch("TwoOpt", 100)
])
```

### 2. Crossover de AST

Intercambia subtrees entre dos árboles.

```python
def crossover_ast(parent1: ASTNode, parent2: ASTNode) -> Tuple[ASTNode, ASTNode]:
    """Crossover entre dos AST"""
    
    # Copiar padres
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    
    # Obtener todos los nodos
    nodes1 = child1.get_all_nodes()
    nodes2 = child2.get_all_nodes()
    
    if not nodes1 or not nodes2:
        return child1, child2
    
    # Seleccionar puntos de corte
    idx1 = random.randint(0, len(nodes1) - 1)
    idx2 = random.randint(0, len(nodes2) - 1)
    
    # Intercambiar subtrees
    # (implementación simplificada)
    nodes1[idx1], nodes2[idx2] = nodes2[idx2], nodes1[idx1]
    
    return child1, child2
```

**Ejemplo:**

```
Padre 1:                    Padre 2:
  Seq                         Seq
  ├─ Const(NN)               ├─ Const(Savings)
  └─ Local(2-opt)            └─ Local(Or-opt)

Crossover en 2º nodo:

Hijo 1:                     Hijo 2:
  Seq                         Seq
  ├─ Const(NN)               ├─ Const(Savings)
  └─ Local(Or-opt)  ◄────    └─ Local(2-opt)  ◄────
```

### 3. Selección

Selecciona mejores individuos para reproducción.

```python
def tournament_selection(population: List[Individual], 
                        tournament_size: int = 3) -> Individual:
    """Selecciona mejor de N individuos aleatorios"""
    
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda x: x.fitness)
```

---

## Interpretación y Ejecución

### Intérprete de AST

```python
class ASTInterpreter:
    """Ejecuta un AST en una instancia VRPTW"""
    
    def __init__(self, problem: VRPTWInstance):
        self.problem = problem
        self.execution_log = []
    
    def execute(self, ast: ASTNode, seed=None) -> Solution:
        """Ejecuta AST y retorna solución"""
        
        # Inicializar contexto
        self.rng = np.random.Generator(np.random.PCG64(seed))
        
        # Ejecutar AST
        solution = self._execute_node(ast)
        
        return solution
    
    def _execute_node(self, node: ASTNode) -> Solution:
        """Ejecuta nodo según tipo"""
        
        if isinstance(node, Seq):
            solution = None
            for child in node.body:
                solution = self._execute_node(child)
            return solution
        
        elif isinstance(node, While):
            solution = None
            for _ in range(node.max_iterations):
                solution = self._execute_node(node.body)
            return solution
        
        elif isinstance(node, For):
            best = None
            for _ in range(node.iterations):
                current = self._execute_node(node.body)
                if best is None or current.fitness < best.fitness:
                    best = current
            return best
        
        elif isinstance(node, If):
            then_result = self._execute_node(node.then_branch)
            if then_result.fitness < self.current_solution.fitness:
                return then_result
            elif node.else_branch:
                return self._execute_node(node.else_branch)
            return self.current_solution
        
        elif isinstance(node, GreedyConstruct):
            operator = CONSTRUCTIVE_OPS[node.heuristic]()
            return operator.construct(self.problem)
        
        elif isinstance(node, LocalSearch):
            operator = LOCAL_SEARCH_OPS[node.operator]()
            return operator.improve(self.current_solution, 
                                  max_iterations=node.max_iterations)
        
        elif isinstance(node, Perturbation):
            operator = PERTURBATION_OPS[node.operator]()
            return operator.perturb(self.current_solution, 
                                  strength=node.strength)
        
        else:
            raise ValueError(f"Nodo desconocido: {type(node)}")
```

---

## Integración con VRPTW-GRASP

### Flujo de Evaluación

```python
class GAEvaluator:
    """Evalúa fitness de algoritmos generados"""
    
    def __init__(self, instances: List[VRPTWInstance]):
        self.instances = instances
    
    def evaluate_algorithm(self, ast: ASTNode, 
                          seed: Optional[int] = None) -> float:
        """
        Evalúa un algoritmo en múltiples instancias
        
        Returns:
            Fitness agregado (promedio)
        """
        fitness_scores = []
        
        for instance in self.instances:
            # Crear intérprete
            interpreter = ASTInterpreter(instance)
            
            # Ejecutar algoritmo
            solution = interpreter.execute(ast, seed=seed)
            
            # Registrar fitness (canónico: primero K, luego D)
            fitness = (solution.num_vehicles, solution.total_distance)
            fitness_scores.append(fitness)
        
        # Agregar fitness: promedio ponderado
        avg_k = np.mean([f[0] for f in fitness_scores])
        avg_d = np.mean([f[1] for f in fitness_scores])
        
        return avg_k * 1000 + avg_d  # Lexicográfico
    
    def evaluate_population(self, 
                           population: List[ASTNode],
                           seeds: Optional[List[int]] = None) -> Dict[int, float]:
        """Evalúa población completa"""
        
        fitness_map = {}
        
        for i, ast in enumerate(population):
            seed = seeds[i] if seeds else None
            fitness = self.evaluate_algorithm(ast, seed)
            fitness_map[i] = fitness
        
        return fitness_map
```

### Algoritmo Genético Completo

```python
class VRPTWGeneticAlgorithm:
    """GA para evolucionar algoritmos VRPTW"""
    
    def __init__(self, config: Dict):
        self.population_size = config.get("population_size", 20)
        self.generations = config.get("generations", 50)
        self.mutation_rate = config.get("mutation_rate", 0.3)
        self.crossover_rate = config.get("crossover_rate", 0.7)
    
    def run(self, instances: List[VRPTWInstance]) -> ASTNode:
        """Ejecuta GA y retorna mejor algoritmo"""
        
        # Inicializar población
        generator = AlgorithmGenerator()
        population = [generator.generate() for _ in range(self.population_size)]
        
        evaluator = GAEvaluator(instances)
        best_ever = None
        best_fitness = float('inf')
        
        # Evolución
        for gen in range(self.generations):
            
            # Evaluar población actual
            fitness_scores = evaluator.evaluate_population(population)
            
            # Registrar mejor
            for ast, fitness in zip(population, fitness_scores.values()):
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_ever = deepcopy(ast)
            
            # Seleccionar y reproducir
            new_population = []
            
            # Elitismo: mantener mejor
            new_population.append(best_ever)
            
            # Generar nuevos
            while len(new_population) < self.population_size:
                
                # Seleccionar padres
                parent1 = tournament_selection(population, fitness_scores, tournament_size=3)
                parent2 = tournament_selection(population, fitness_scores, tournament_size=3)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = crossover_ast(parent1, parent2)
                else:
                    child1, child2 = deepcopy(parent1), deepcopy(parent2)
                
                # Mutación
                if random.random() < self.mutation_rate:
                    child1 = mutate_ast(child1)
                if random.random() < self.mutation_rate:
                    child2 = mutate_ast(child2)
                
                new_population.extend([child1, child2])
            
            # Truncar a tamaño de población
            new_population = new_population[:self.population_size]
            population = new_population
            
            # Log
            print(f"Gen {gen:3d}: Best={best_fitness:.2f}")
        
        return best_ever
```

---

## Ejemplo Completo

### Paso 1: Generar Algoritmo

```python
from gaa import AlgorithmGenerator

# Generar AST aleatorio
generator = AlgorithmGenerator(seed=42)
algorithm = generator.generate()

print(algorithm)
# Output:
# Seq(body=[
#     GreedyConstruct(heuristic="Savings"),
#     While(max_iterations=200, body=
#         LocalSearch(operator="TwoOpt", max_iterations=100)
#     )
# ])
```

### Paso 2: Visualizar Árbol

```python
def print_ast(node, indent=0):
    """Imprime AST de forma legible"""
    
    prefix = "  " * indent + "├─ "
    
    if isinstance(node, Seq):
        print(f"{prefix}Seq")
        for child in node.body:
            print_ast(child, indent + 1)
    
    elif isinstance(node, While):
        print(f"{prefix}While(max_iterations={node.max_iterations})")
        print_ast(node.body, indent + 1)
    
    elif isinstance(node, GreedyConstruct):
        print(f"{prefix}GreedyConstruct({node.heuristic})")
    
    elif isinstance(node, LocalSearch):
        print(f"{prefix}LocalSearch({node.operator}, {node.max_iterations} iters)")
    
    elif isinstance(node, Perturbation):
        print(f"{prefix}Perturbation({node.operator}, strength={node.strength})")

print_ast(algorithm)
# Output:
# Seq
# ├─ GreedyConstruct(Savings)
# └─ While(max_iterations=200)
#    └─ LocalSearch(TwoOpt, 100 iters)
```

### Paso 3: Ejecutar Algoritmo

```python
from gaa import ASTInterpreter
from datasets import load_solomon_instance

# Cargar instancia
instance = load_solomon_instance("C101", directory="data/Solomon")

# Crear intérprete
interpreter = ASTInterpreter(instance)

# Ejecutar algoritmo
solution = interpreter.execute(algorithm, seed=123)

print(f"Vehículos: {solution.num_vehicles}")
print(f"Distancia: {solution.total_distance:.2f}")
print(f"Fitness (K, D): {(solution.num_vehicles, solution.total_distance)}")
```

### Paso 4: Evaluar Población

```python
from gaa import VRPTWGeneticAlgorithm

# Cargar instancias para evaluación
instances = [
    load_solomon_instance("R101"),
    load_solomon_instance("C101"),
    load_solomon_instance("RC101")
]

# Ejecutar GA
config = {
    "population_size": 15,
    "generations": 20,
    "mutation_rate": 0.3,
    "crossover_rate": 0.7
}

ga = VRPTWGeneticAlgorithm(config)
best_algorithm = ga.run(instances)

print("\n=== MEJOR ALGORITMO ENCONTRADO ===")
print_ast(best_algorithm)
```

### Paso 5: Exportar Algoritmo

```python
import json

def ast_to_json(node):
    """Convierte AST a JSON para persistencia"""
    
    if isinstance(node, Seq):
        return {
            "type": "Seq",
            "body": [ast_to_json(child) for child in node.body]
        }
    
    elif isinstance(node, While):
        return {
            "type": "While",
            "max_iterations": node.max_iterations,
            "body": ast_to_json(node.body)
        }
    
    elif isinstance(node, GreedyConstruct):
        return {
            "type": "GreedyConstruct",
            "heuristic": node.heuristic
        }
    
    elif isinstance(node, LocalSearch):
        return {
            "type": "LocalSearch",
            "operator": node.operator,
            "max_iterations": node.max_iterations
        }
    
    elif isinstance(node, Perturbation):
        return {
            "type": "Perturbation",
            "operator": node.operator,
            "strength": node.strength
        }

# Guardar
best_json = ast_to_json(best_algorithm)
with open("best_algorithm.json", "w") as f:
    json.dump(best_json, f, indent=2)

# Cargar
with open("best_algorithm.json", "r") as f:
    loaded_json = json.load(f)
```

---

## Resumen de Integración

### Módulos Necesarios

```
gaa/
├── __init__.py              # Exporta todas las clases
├── ast_nodes.py             # Definición de nodos (8 tipos)
├── grammar.py               # Gramática BNF para VRPTW
├── generator.py             # AlgorithmGenerator
├── interpreter.py           # ASTInterpreter
└── operators.py             # Mapa de operadores a clases

operators/
├── constructive.py          # 6 operadores constructivos
├── local_search.py          # 8 operadores de mejora
└── perturbation.py          # 4 operadores de perturbación

evaluation/
├── evaluator.py             # GAEvaluator
└── genetic_algorithm.py     # VRPTWGeneticAlgorithm
```

### Flujo de Ejecución

1. **Generación**: `AlgorithmGenerator.generate()` → AST
2. **Mutación/Crossover**: `mutate_ast()`, `crossover_ast()` → AST modificado
3. **Interpretación**: `ASTInterpreter.execute()` → Solution
4. **Evaluación**: `GAEvaluator.evaluate()` → Fitness score
5. **Selección**: `tournament_selection()` → Mejor individuo
6. **Iteración**: Repetir pasos 2-5 por N generaciones

### Ventajas de GAA para VRPTW

✅ **Automático**: No necesita tuning manual de parámetros  
✅ **Adaptativo**: Evoluciona según instancias específicas  
✅ **Exploratorio**: Busca combinaciones no intuitivas  
✅ **Reproducible**: Cada algoritmo es determinista (seeded)  
✅ **Transferible**: Los AST pueden ejecutarse en nuevas instancias  

---

## Referencias

- [INDEX.md](INDEX.md) — Navegación general
- [03-operadores-dominio.md](03-operadores-dominio.md) — 22 operadores disponibles
- [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) — GRASP base
- [07-fitness-canonico.md](07-fitness-canonico.md) — Función fitness
- [09-outputs-estructura.md](09-outputs-estructura.md) — Estructura de outputs
