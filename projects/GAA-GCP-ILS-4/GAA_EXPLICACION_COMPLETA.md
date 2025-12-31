# Generación Automática de Algoritmos (GAA): Guía de Funcionamiento
## Con ejemplos de ejecución tipo

---

## ⚠️ Aclaración Importante

**En GAA-GCP-ILS-4**: NO hay generación automática de algoritmos.  
**En KBP-SA**: SÍ hay generación automática completa y funcional.

Este documento describe **cómo funciona en KBP-SA** como referencia para entender el concepto.

---

## 📐 Arquitectura General del Sistema GAA

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA GAA                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. GRAMMAR (Gramática BNF)                                  │
│     └─ Define terminales y no-terminales válidos             │
│     └─ Especifica reglas de combinación                      │
│                                                               │
│  2. GENERATOR (Generador Aleatorio)                          │
│     └─ Crea AST aleatorios respetando gramática             │
│     └─ Control de profundidad y diversidad                  │
│                                                               │
│  3. AST NODES (Nodos del Árbol Sintáctico)                   │
│     └─ Seq, If, While, For, Call                            │
│     └─ GreedyConstruct, LocalSearch, Perturbation          │
│                                                               │
│  4. INTERPRETER (Intérprete/Ejecutor)                        │
│     └─ Ejecuta algoritmo representado como AST              │
│     └─ Mantiene estado (solución, mejor, estadísticas)     │
│                                                               │
│  5. METAHEURISTIC (SA, GP, ILS)                              │
│     └─ Busca mejor algoritmo (AST) entre población          │
│     └─ Operadores genéticos sobre AST                       │
│                                                               │
│  6. EVALUATOR (Evaluador Multi-Instancia)                    │
│     └─ Ejecuta algoritmo en N instancias                    │
│     └─ Calcula fitness como promedio de rendimiento        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Ejecución Tipo

### Fase 1: Inicialización

```
┌─────────────────────────────────────────┐
│ 1. Cargar Gramática                     │
│    • Terminales constructivos            │
│    • Terminales de mejora                │
│    • Terminales de perturbación          │
│    • Límites de profundidad              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 2. Cargar Problemas de Entrenamiento    │
│    • Instancias pequeñas (training/)    │
│    • Instancias medias (validation/)    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 3. Inicializar Generador y Metaheurística│
│    • Seed aleatorio o fijo              │
│    • Población de algoritmos (AST)      │
│    • Parámetros de evolución            │
└─────────────────────────────────────────┘
```

### Fase 2: Generación de Algoritmos (Primera Población)

```
GENERADOR CREA 5 ALGORITMOS ALEATORIOS:

Algoritmo 1: 
  ┌─ Seq
  │  ├─ GreedyConstruct("GreedyByRatio")
  │  └─ While(IterBudget=100)
  │     └─ LocalSearch("FlipBestItem", "Improving")

Algoritmo 2:
  ┌─ Seq
  │  ├─ GreedyConstruct("GreedyByWeight")
  │  ├─ For(n=10)
  │  │  └─ If(Prob=0.3)
  │  │     ├─ Call("FlipBestItem")
  │  │     └─ Call("RandomFlip", args={k: 2})

Algoritmo 3:
  ┌─ ChooseBestOf(n_tries=5)
  │  └─ Seq
  │     ├─ GreedyConstruct("GreedyByValue")
  │     └─ LocalSearch("TwoExchange", "BestImprovement")

... (Algoritmos 4 y 5)
```

### Fase 3: Evaluación de Algoritmos (Multi-Instancia)

```
PARA CADA ALGORITMO (j=1 a 5):
  fitness[j] = 0
  
  PARA CADA INSTANCIA DE ENTRENAMIENTO (i=1 a 20):
    • Crear intérprete nuevo
    • Ejecutar AST_j sobre instancia_i
    • Registrar valor de solución final
    
  fitness[j] = mean(valores de todas instancias)

RESULTADO:
  Algoritmo 1: fitness = 850.5 (promedio en 20 instancias)
  Algoritmo 2: fitness = 923.1 ← MEJOR
  Algoritmo 3: fitness = 785.2
  Algoritmo 4: fitness = 901.3
  Algoritmo 5: fitness = 812.7
```

### Fase 4: Evolución mediante Metaheurística (Simulated Annealing)

```
TEMPERATURA INICIAL: T = 1000

GENERACIÓN 1:
  Estado actual: Algoritmo 2 (fitness=923.1)
  
  • Mutar: Cambiar un nodo del AST
    - Reemplazar GreedyByRatio con GreedyByWeight
    
  AST mutado:
    ┌─ Seq
    │  ├─ GreedyConstruct("GreedyByWeight")  ← MUTADO
    │  └─ While(IterBudget=100)
    │     └─ LocalSearch("FlipBestItem", "Improving")
  
  • Evaluar: fitness_mutado = 931.2 (mejora ✓)
  
  • Aceptar: SIEMPRE (mejora)
  
  Mejor hasta ahora: Algoritmo Mutado (931.2)

GENERACIÓN 2:
  Estado actual: Algoritmo Mutado
  
  • Mutar: Cambiar profundidad del bucle While
    - Cambiar IterBudget=100 a IterBudget=200
  
  • Evaluar: fitness_mutado2 = 928.5 (empeora ✗)
  
  • Aceptar: CON PROBABILIDAD e^(Δf/T)
    - Δf = 928.5 - 931.2 = -2.7
    - P = e^(-2.7/1000) ≈ 0.997 ← ACEPTA igual (casi)
  
GENERACIÓN 3:
  Estado actual: Algoritmo Mutado2
  
  • Mutar: Cambiar condicional
  
  • Evaluar: fitness_mutado3 = 920.1 (peor)
  
  • Aceptar: P = e^(-11.1/1000) ≈ 0.989 ← RECHAZA
  
  Volver a estado anterior

... (generaciones 4 a N)

TEMPERATURA FINAL: T = 0.1

RESULTADO FINAL:
  Mejor algoritmo encontrado: Algoritmo Evolucionado
  Fitness final: 945.7 (mejora respecto al inicial 923.1)
```

---

## 💻 Ejemplo Detallado de Código

### 1. Crear Generador

```python
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator

# Crear gramática (carga terminales del problema)
grammar = Grammar(min_depth=2, max_depth=4)

# Crear generador
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# Generar algoritmo aleatorio
algorithm_ast = generator.generate()

print("Algoritmo generado:")
print(algorithm_ast.to_pseudocode())

# Salida:
# SECUENCIA:
#   1. Construcción: GreedyByRatio
#   2. MIENTRAS IterBudget < 100:
#        Mejora Local: FlipBestItem
#   3. SI Estancamiento > 10:
#        Perturbación: RandomFlip(k=2)
```

### 2. Ejecutar Algoritmo en Instancia

```python
from gaa.interpreter import ASTInterpreter
from core.problem import KnapsackProblem
from core.evaluation import KnapsackEvaluator

# Cargar problema
problem = KnapsackProblem.load_from_file("datasets/training/kbp_100_1.txt")

# Crear intérprete
interpreter = ASTInterpreter(problem=problem, seed=42)

# Ejecutar algoritmo (AST) sobre problema
best_solution = interpreter.execute(algorithm_ast)

print(f"Solución encontrada:")
print(f"  • Valor: {best_solution.value}")
print(f"  • Items: {best_solution.items_count}")
print(f"  • Peso total: {best_solution.total_weight}")
print(f"  • Estadísticas:")
print(f"    - Iteraciones: {interpreter.context.iterations}")
print(f"    - Evaluaciones: {interpreter.context.evaluations}")
print(f"    - Tiempo (s): {interpreter.context.get_elapsed_time():.2f}")
```

### 3. Evaluar en Múltiples Instancias

```python
from data.loader import DatasetLoader

# Cargar múltiples instancias
loader = DatasetLoader("datasets/")
training_instances = loader.load_folder("training")  # 20 instancias

# Función de evaluación
def evaluate_algorithm(algorithm_ast, instances):
    """Calcula fitness como promedio de desempeño en instancias"""
    
    values = []
    
    for instance in instances:
        # Crear intérprete para cada instancia
        interpreter = ASTInterpreter(problem=instance)
        
        # Ejecutar algoritmo
        solution = interpreter.execute(algorithm_ast)
        
        # Registrar valor
        values.append(solution.value)
    
    # Fitness = promedio
    fitness = sum(values) / len(values)
    
    return fitness

# Evaluar nuestro algoritmo
fitness = evaluate_algorithm(algorithm_ast, training_instances)

print(f"Fitness del algoritmo: {fitness:.2f}")
print(f"  (promedio de {len(training_instances)} instancias)")
```

### 4. Evolucionar Algoritmo con Simulated Annealing

```python
from metaheuristic.sa_core import SimulatedAnnealing

# Crear metaheurística
sa = SimulatedAnnealing(
    initial_temperature=1000,
    cooling_rate=0.95,
    max_iterations=100
)

# Función objetiva: evaluar algoritmo en instancias
def objective(algorithm_ast):
    return evaluate_algorithm(algorithm_ast, training_instances)

# Optimizar (buscar mejor algoritmo)
best_algorithm, best_fitness = sa.optimize(
    initial_solution=algorithm_ast,
    objective_function=objective,
    move_operator=lambda ast: mutate_ast(ast, grammar)
)

print(f"Mejor algoritmo encontrado:")
print(f"  • Fitness: {best_fitness:.2f}")
print(f"  Pseudocódigo:")
print(best_algorithm.to_pseudocode())
```

---

## 📊 Ejecución Completa: Script `demo_complete.py`

```bash
$ python scripts/demo_complete.py
```

**Salida esperada:**

```
================================================================================
  DEMO 1: Carga de Instancias
================================================================================

✅ Instancia cargada: kbp_100_1
   • n = 100 ítems
   • capacity = 500
   • optimal = 1050

✅ 20 instancias cargadas de training/

================================================================================
  DEMO 2: Generación Automática de Algoritmos (GAA)
================================================================================

🌳 Gramática GAA cargada:
   • Terminales constructivos: 4
   • Terminales de mejora: 5
   • Terminales de perturbación: 3
   • Total de terminales: 12

🎲 Generando 3 algoritmos aleatorios...

✅ Algoritmo 1 generado
   Pseudocódigo:
   SECUENCIA:
     1. Construcción: GreedyByRatio
     2. MIENTRAS IterBudget < 100:
          Mejora Local: FlipBestItem

✅ Algoritmo 2 generado
   Pseudocódigo:
   SECUENCIA:
     1. Construcción: GreedyByValue
     2. PARA i = 0 a 20:
          SI Prob(0.3):
            Llamada: TwoExchange
          SINO:
            Llamada: RandomFlip(k=2)

✅ Algoritmo 3 generado
   Pseudocódigo:
   ChooseBestOf(n=5):
     1. Construcción: GreedyByWeight
     2. MIENTRAS IterBudget < 500:
          Mejora Local: BestImproveAll

================================================================================
  DEMO 3: Evaluación de Algoritmos (Multi-Instancia)
================================================================================

🔬 Evaluando 3 algoritmos en 20 instancias...

Algoritmo 1:
  Instancia 1 (kbp_100_1): 1025.0
  Instancia 2 (kbp_100_2): 1012.5
  Instancia 3 (kbp_100_3): 1018.2
  ...
  Instancia 20 (kbp_100_20): 1020.1
  
  ✅ Fitness: 1018.5 (promedio)
  ✅ Tiempo total: 45.3 segundos

Algoritmo 2:
  ...
  ✅ Fitness: 1035.2 (promedio) ← MEJOR
  ✅ Tiempo total: 52.1 segundos

Algoritmo 3:
  ...
  ✅ Fitness: 995.7 (promedio)
  ✅ Tiempo total: 38.9 segundos

================================================================================
  DEMO 4: Evolución con Simulated Annealing
================================================================================

🧬 Ejecutando Simulated Annealing para optimizar algoritmos...

  Generación 1 (T=1000.00):
    Mejor actual: Alg_2 (fitness=1035.2)
    Mutación: Cambiar mejora a "BestImproveOne"
    Evaluado: fitness=1038.1 (mejora ✓)
    Aceptado: SIEMPRE
    
    Mejor global: 1038.1

  Generación 2 (T=950.00):
    Mejor actual: Alg_2_mut (fitness=1038.1)
    Mutación: Cambiar IterBudget a 200
    Evaluado: fitness=1036.5 (empeora ✗)
    Aceptado: P(0.991) ✓
    
    Mejor global: 1038.1 (sin cambio)

  Generación 3 (T=902.50):
    Mejor actual: Alg_2_mut2 (fitness=1036.5)
    Mutación: Cambiar construcción a "GreedyByWeight"
    Evaluado: fitness=1041.3 (mejora ✓)
    Aceptado: SIEMPRE
    
    Mejor global: 1041.3 ✨

  ...

  Generación 100 (T=0.10):
    Mejor actual: Alg_FINAL (fitness=1045.7)
    Mutación: Cambiar parámetro
    Evaluado: fitness=1045.5 (empeora)
    Aceptado: P(0.001) ✗
    
    Mejor global: 1045.7

🏁 Simulated Annealing finalizado

  ✅ Mejor algoritmo encontrado: Alg_FINAL
  ✅ Fitness final: 1045.7
  ✅ Mejora respecto al inicial: 10.5 (1.0%)
  ✅ Tiempo total: 432.1 segundos

================================================================================
  DEMO 5: Análisis de Resultados
================================================================================

📊 Algoritmo Evolucionado - Análisis Detallado

Estructura AST:
  Profundidad máxima: 4
  Total nodos: 12
  Operadores: 5
  Válido: ✓

Desempeño en training:
  Promedio: 1045.7
  Mínimo: 1041.2
  Máximo: 1049.3
  Desviación estándar: 2.1

Información detallada:
  Instancia 1: 1047.0
  Instancia 2: 1045.3
  Instancia 3: 1043.1
  ...
  Instancia 20: 1046.2

Configuración del algoritmo:
  Construcción: GreedyByWeight
  Mejora 1: BestImproveAll (IterBudget=200)
  Mejora 2: TwoExchange (IterBudget=100)
  Condicional: SI Mejora ENTONCES Aceptar

Pseudocódigo legible:
  1. Construcción inicial con GreedyByWeight
  2. MIENTRAS evaluaciones < 200:
       Aplicar BestImproveAll
       SI mejora: aceptar
       SINO: con prob 0.3 aceptar igual
  3. PARA i = 1 a 100:
       SI no hay mejora hace 10 iteraciones:
         Perturbación: RandomFlip(k=3)
       Mejora local: TwoExchange
```

---

## 🔑 Conceptos Clave

### Árbol Sintáctico Abstracto (AST)

Un algoritmo se representa como un árbol de nodos:

```
Algorithm = Seq([
    GreedyConstruct("GreedyByRatio"),
    While(
        budget=IterBudget(100),
        body=Seq([
            LocalSearch("FlipBestItem"),
            If(
                condition="Improves",
                then_branch=Call("TwoExchange"),
                else_branch=Call("RandomFlip", k=2)
            )
        ])
    )
])
```

**Ventajas:**
- ✅ Representación formal y estructurada
- ✅ Fácil de manipular genéticamente (mutar/cruzar subárboles)
- ✅ Ejecutable (intérprete convierte AST en acciones)
- ✅ Serializable (guardar/cargar algoritmos)

### Gramática BNF

Define qué AST son válidos:

```bnf
<Algorithm> ::= <Stmt>
<Stmt> ::= Seq(<Stmt>*)
          | While(<Budget>, <Stmt>)
          | For(n, <Stmt>)
          | If(<Cond>, <Stmt>, <Stmt>)
          | Call(<Op>, <Args>)

<Op> ::= GreedyByRatio | GreedyByValue | ... (13 terminales)
<Cond> ::= Improves | Feasible | Prob(p)
```

**Beneficio:** El generador respeta estas reglas, evitando AST inválidos.

### Fitness Multi-Instancia

Un algoritmo se evalúa en VARIAS instancias de entrenamiento:

```
fitness = mean([ejecutar(algoritmo, instancia_i).valor 
               for instancia_i in training_set])
```

**Por qué:** Mide generalización del algoritmo, no solo desempeño en caso particular.

---

## ⚙️ Cómo Implementarlo en GAA-GCP-ILS-4

Si quisieras agregar GAA a GAA-GCP-ILS-4, estos serían los pasos:

### Paso 1: Crear módulo `gaa/`

```
gaa/
├── __init__.py          # Exportar clases
├── ast_nodes.py         # Nodos: Seq, If, While, Call, GreedyConstruct, etc.
├── grammar.py           # Reglas BNF de ILS para GCP
├── generator.py         # AlgorithmGenerator
└── interpreter.py       # ASTInterpreter (ejecutor)
```

### Paso 2: Definir Terminales para GCP

```python
# Terminales constructivos
CONSTRUCTIVE_TERMINALS = [
    "GreedyDSATUR",
    "GreedyLF",
    "RandomSequential",
    "GreedySL"
]

# Terminales de mejora
IMPROVEMENT_TERMINALS = [
    "KempeChain",
    "OneVertexMove",
    "TabuCol",
    "SwapColors"
]

# Terminales de perturbación
PERTURBATION_TERMINALS = [
    "RandomRecolor",
    "PartialDestroy",
    "ColorClassMerge"
]
```

### Paso 3: Gramática BNF para ILS-GCP

```bnf
<ILSAlgorithm> ::= <Construction> <LoopPhase>

<Construction> ::= Call(GreedyDSATUR | GreedyLF | RandomSequential)

<LoopPhase> ::= While(<IterBudget>, <IterationBody>)

<IterationBody> ::= Seq([<Improvement>, <Perturbation>])
                   | Seq([<Improvement>, If(Improves, <Perturbation>)])

<Improvement> ::= Call(KempeChain | OneVertexMove | TabuCol)

<Perturbation> ::= Call(RandomRecolor | PartialDestroy)
                   with args {intensity: 0.1-0.5}
```

### Paso 4: Script de Experimentación

```python
# scripts/gaa_experiment.py

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import ASTInterpreter
from data.loader import DatasetLoader
from metaheuristic.sa_core import SimulatedAnnealing

# Cargar problemas de entrenamiento
loader = DatasetLoader("datasets/")
training = loader.load_folder("training")  # Pequeños para entrenar

# Crear generador
grammar = Grammar(min_depth=2, max_depth=4)
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# Generar población inicial
population = [generator.generate() for _ in range(10)]

# Definir fitness
def evaluate(algorithm):
    fitness = 0
    for instance in training:
        interpreter = ASTInterpreter(instance)
        solution = interpreter.execute(algorithm)
        fitness += (instance.colors_known - solution.num_colors)  # gap
    return fitness / len(training)

# Evolucionar con SA
sa = SimulatedAnnealing(max_iterations=50)
best_algorithm, best_fitness = sa.optimize(
    population[0], 
    evaluate,
    mutation_operator=lambda x: mutate_ast(x)
)

# Testear en validación
validation = loader.load_folder("validation")
test_fitness = evaluate_on_set(best_algorithm, validation)

print(f"Mejor algoritmo encontrado: {best_fitness}")
print(f"Desempeño en validación: {test_fitness}")
```

---

## 📈 Ventajas de GAA

| Aspecto | Ventaja |
|--------|---------|
| **Automatización** | No necesitas diseñar manualmente cada algoritmo |
| **Optimización** | Los algoritmos se adaptan al problema específico |
| **Generalización** | Multi-instancia asegura desempeño en casos nuevos |
| **Reproducibilidad** | Algoritmos son código (AST) ejecutable |
| **Escalabilidad** | Puedes evolucionar gran población de algoritmos |
| **Análisis** | Entiendes qué funciona mejor (estructura AST) |

---

## 🎯 Conclusión

**GAA es un metamodelo**: en lugar de evolucionar soluciones de un problema,
evolucionas **algoritmos completos** representados como árboles sintácticos.

La ejecución tipo:
1. Generar AST aleatorios
2. Evaluar cada uno en múltiples instancias
3. Evolucionar usando metaheurística (SA, GP, ILS)
4. Seleccionar mejor algoritmo después de N generaciones

**Resultado**: Un algoritmo automáticamente optimizado y generalizable.

---

**Referencia**: Implementación completa en `projects/KBP-SA/gaa/`
