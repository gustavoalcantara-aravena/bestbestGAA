---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP-ILS-GAA"
  type: trigger
  last_modified: null
  depends_on:
    - 01-System/Grammar.md
  triggers_update:
    - 02-Components/ast_nodes.py
    - 04-Generated/scripts/ast_nodes.py
    - 04-Generated/scripts/ast_evaluator.py
  extraction_rules:
    node_types: "section:Node-Classes"
    operations: "section:Node-Operations"
---

# Nodos AST para GCP-ILS-GAA

> **🎯 ARCHIVO EDITABLE**: Define la estructura de AST (Abstract Syntax Tree) para representar algoritmos.

**Proyecto**: GCP-ILS-GAA  
**Basado en**: 01-System/Grammar.md  
**Versión**: 1.0.0

---

## Propósito

Un **AST (Abstract Syntax Tree)** es una representación en árbol de un algoritmo que:

1. **Estructura jerárquica**: Refleja la composición del algoritmo
2. **Ejecutable**: Puede ser interpretado para resolver problemas
3. **Evolvable**: Puede ser mutado y recombinado por Genetic Programming
4. **Evaluable**: Se puede medir su fitness en problemas

---

## Jerarquía-de-Nodos

```
ASTNode (clase base abstracta)
├── AlgorithmNode
│   ├── InitPhaseNode
│   ├── SearchPhaseNode
│   ├── TerminationNode
│   └── AcceptanceNode
├── OperatorNode (clase base para operadores)
│   ├── ConstructiveNode
│   │   ├── DSATURNode
│   │   ├── LargestFirstNode
│   │   ├── SmallestLastNode
│   │   ├── RandomSequentialNode
│   │   └── RLFNode
│   ├── LocalSearchNode
│   │   ├── KempeChainNode
│   │   ├── SingleVertexMoveNode
│   │   ├── ColorClassMergeNode
│   │   ├── TabuSearchNode
│   │   └── SwapColorsNode
│   ├── PerturbationNode
│   │   ├── RandomRecolorNode
│   │   ├── PartialDestroyNode
│   │   ├── ColorClassMergeNode (puede ser perturbación)
│   │   └── ShakeColorsNode
│   └── TerminationNode
│       ├── MaxIterNode
│       ├── TimeLimitNode
│       ├── NoImprovementNode
│       └── OptimalReachedNode
└── CompositeNode (composición de operadores)
    ├── LocalSearchPhaseNode
    ├── PerturbationPhaseNode
    └── AlgorithmLoopNode
```

---

## Node-Classes

### Clase Base: ASTNode

```python
class ASTNode(ABC):
    """
    Clase base para todos los nodos del AST.
    
    Atributos:
        node_id: Identificador único del nodo
        node_type: Tipo de nodo (ej: CONSTRUCTIVE, LOCAL_SEARCH)
        parameters: Parámetros del nodo
        parent: Nodo padre (None para raíz)
        children: Lista de nodos hijo
    """
    
    @abstractmethod
    def __repr__(self) -> str:
        """Representación en string del nodo"""
        pass
    
    @abstractmethod
    def to_pseudocode(self) -> str:
        """Convertir a pseudocódigo legible"""
        pass
    
    @abstractmethod
    def to_json(self) -> dict:
        """Serializar a JSON"""
        pass
    
    def copy(self) -> 'ASTNode':
        """Crear copia profunda del nodo"""
        pass
    
    def depth(self) -> int:
        """Profundidad del subárbol"""
        pass
    
    def size(self) -> int:
        """Número de nodos en subárbol"""
        pass
```

### AlgorithmNode (Raíz)

```python
class AlgorithmNode(ASTNode):
    """
    Nodo raíz que representa un algoritmo completo.
    
    Estructura:
        - init_phase: Fase de inicialización
        - search_phases: Lista de fases de búsqueda
        - termination: Condición de terminación
        - acceptance: Criterio de aceptación
    
    Ejemplo:
        Algorithm:
          InitPhase: DSATUR
          SearchPhases: [
            LocalSearchPhase: [KempeChain],
            PerturbationPhase: RandomRecolor,
            LocalSearchPhase: [KempeChain]
          ]
          Termination: MaxIterations(500)
          Acceptance: BetterOrEqual
    """
    
    def __init__(self, init_phase, search_phases, termination, acceptance):
        self.init_phase: InitPhaseNode = init_phase
        self.search_phases: List[SearchPhaseNode] = search_phases
        self.termination: TerminationNode = termination
        self.acceptance: AcceptanceNode = acceptance
    
    def execute(self, problem, coloring=None, context=None):
        """Ejecutar algoritmo completo"""
        pass
    
    def is_valid(self) -> bool:
        """Verificar que cumple gramática"""
        pass
```

### InitPhaseNode

```python
class InitPhaseNode(ASTNode):
    """Fase de inicialización con heurística constructiva"""
    
    def __init__(self, constructive: ConstructiveNode):
        self.constructive = constructive
    
    def execute(self, problem):
        """Ejecutar constructiva y retornar solución inicial"""
        pass
```

### SearchPhaseNode (Base)

```python
class SearchPhaseNode(ASTNode):
    """Clase base para fases de búsqueda"""
    
    @abstractmethod
    def execute(self, problem, coloring, context):
        """Ejecutar fase y retornar coloring mejorado"""
        pass
```

#### LocalSearchPhaseNode

```python
class LocalSearchPhaseNode(SearchPhaseNode):
    """
    Fase de búsqueda local con 1+ operadores.
    
    Los operadores se aplican secuencialmente:
    coloring = op1(op2(op3(coloring)))
    
    Parámetros:
        operators: Lista de operadores a aplicar [op1, op2, ...]
        max_iterations: Máximo de iteraciones
        first_improvement: Aceptar primer movimiento mejorante
    """
    
    def __init__(self, operators: List[LocalSearchNode], 
                 max_iterations: int = 100,
                 first_improvement: bool = True):
        self.operators = operators
        self.max_iterations = max_iterations
        self.first_improvement = first_improvement
    
    def execute(self, problem, coloring, context):
        """Aplicar todos los operadores secuencialmente"""
        pass
```

#### PerturbationPhaseNode

```python
class PerturbationPhaseNode(SearchPhaseNode):
    """
    Fase de perturbación con 1 operador.
    
    Parámetros:
        operator: Operador de perturbación
        strength: Intensidad (0.1 a 0.9)
    """
    
    def __init__(self, operator: PerturbationNode, 
                 strength: float = 0.2):
        self.operator = operator
        self.strength = strength
    
    def execute(self, problem, coloring, context):
        """Aplicar perturbación"""
        pass
```

### OperatorNode (Base)

```python
class OperatorNode(ASTNode):
    """Clase base para operadores"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Nombre del operador"""
        pass
    
    @abstractmethod
    def execute(self, problem, coloring, **params):
        """Ejecutar operador sobre coloring"""
        pass
```

### ConstructiveNodes

```python
class DSATURNode(OperatorNode):
    """Construcción por grado de saturación"""
    def execute(self, problem, coloring=None):
        # Retorna coloring inicial factible
        pass

class LargestFirstNode(OperatorNode):
    """Construcción por orden de grado decreciente"""
    pass

class SmallestLastNode(OperatorNode):
    """Construcción por orden de grado creciente"""
    pass

class RandomSequentialNode(OperatorNode):
    """Construcción aleatoria secuencial"""
    pass

class RLFNode(OperatorNode):
    """Recursive Largest First"""
    pass
```

### LocalSearchNodes

```python
class KempeChainNode(OperatorNode):
    """Intercambio de colores via Kempe chains"""
    def __init__(self, max_iterations: int = 100):
        self.max_iterations = max_iterations
    
    def execute(self, problem, coloring):
        # Retorna coloring mejorado
        pass

class SingleVertexMoveNode(OperatorNode):
    """Recolorear un vértice a la vez"""
    pass

class ColorClassMergeNode(OperatorNode):
    """Fusionar dos clases de color"""
    pass

class TabuSearchNode(OperatorNode):
    """Búsqueda local con memoria tabú"""
    pass

class SwapColorsNode(OperatorNode):
    """Intercambiar dos colores directamente"""
    pass
```

### PerturbationNodes

```python
class RandomRecolorNode(PerturbationNode):
    """Recolorear p% de vértices aleatoriamente"""
    def __init__(self, strength: float = 0.2):
        self.strength = strength
    
    def execute(self, problem, coloring):
        # Retorna coloring perturbado (posiblemente infactible)
        pass

class PartialDestroyNode(PerturbationNode):
    """Destruir y reconstruir subgrafo"""
    pass

class ShakeColorsNode(PerturbationNode):
    """Permutación aleatoria de colores"""
    pass
```

### TerminationNodes

```python
class MaxIterNode(TerminationNode):
    """Parar después de N iteraciones"""
    def __init__(self, max_iterations: int = 500):
        self.max_iterations = max_iterations

class TimeLimitNode(TerminationNode):
    """Parar después de T segundos"""
    def __init__(self, time_limit_seconds: float = 60):
        self.time_limit = time_limit_seconds

class NoImprovementNode(TerminationNode):
    """Parar si no hay mejora en N iteraciones"""
    def __init__(self, patience: int = 50):
        self.patience = patience

class OptimalReachedNode(TerminationNode):
    """Parar si se alcanza óptimo conocido"""
    def __init__(self, known_optimal: int):
        self.optimal = known_optimal
```

### AcceptanceNodes

```python
class BetterOrEqualNode(ASTNode):
    """Aceptar si mejora o iguala"""
    def should_accept(self, f_current, f_candidate):
        return f_candidate <= f_current

class MetropolisNode(ASTNode):
    """Aceptación probabilística"""
    def __init__(self, temperature: float = 0.1):
        self.temperature = temperature
    
    def should_accept(self, f_current, f_candidate):
        # Metropolis criterion
        pass

class FirstImprovementNode(ASTNode):
    """Aceptar primer movimiento mejorante"""
    pass
```

---

## Node-Operations

### Operaciones Estructurales

**Mutación**: Cambiar un nodo por otro compatible

```python
def mutate(ast: AlgorithmNode, mutation_rate: float = 0.1) -> AlgorithmNode:
    """
    Mutar AST aleatoriamente.
    
    Operaciones:
    1. Cambiar constructiva (DSATUR → LargestFirst)
    2. Cambiar operador LS (KempeChain → SingleVertex)
    3. Cambiar operador perturbación
    4. Cambiar parámetro (max_iterations, strength)
    """
    pass
```

**Crossover**: Intercambiar partes entre 2 ASTs

```python
def crossover(parent1: AlgorithmNode, parent2: AlgorithmNode) -> Tuple[AlgorithmNode, AlgorithmNode]:
    """
    Cruzamiento de 2 algoritmos.
    
    Estrategias:
    1. Single-point: Cortar en una fase, intercambiar
    2. Multi-point: Intercambiar múltiples subfases
    3. Subtree: Intercambiar subárboles
    """
    pass
```

**Inserción**: Agregar nueva fase

```python
def insert_phase(ast: AlgorithmNode, phase: SearchPhaseNode, 
                position: int) -> AlgorithmNode:
    """Insertar nueva fase de búsqueda en posición"""
    pass
```

**Eliminación**: Eliminar fase redundante

```python
def remove_phase(ast: AlgorithmNode, position: int) -> AlgorithmNode:
    """Eliminar fase de búsqueda"""
    pass
```

### Operaciones de Análisis

**Validación**

```python
def is_valid(ast: AlgorithmNode) -> bool:
    """Verificar que respeta gramática"""
    # R1: Estructura mínima
    # R2-R5: Restricciones
    pass
```

**Serialización**

```python
def to_pseudocode(ast: AlgorithmNode) -> str:
    """Convertir a pseudocódigo legible"""
    # Formato similar a Grammar.md
    pass

def to_json(ast: AlgorithmNode) -> str:
    """Serializar a JSON"""
    pass

def to_python(ast: AlgorithmNode) -> str:
    """Generar código Python ejecutable"""
    pass
```

**Estadísticas**

```python
def ast_statistics(ast: AlgorithmNode) -> dict:
    """Calcular estadísticas del AST"""
    return {
        'num_nodes': ast.size(),
        'depth': ast.depth(),
        'num_constructives': count_of_type(ast, ConstructiveNode),
        'num_local_search': count_of_type(ast, LocalSearchNode),
        'num_perturbations': count_of_type(ast, PerturbationNode),
        'num_phases': len(ast.search_phases),
    }
```

---

## Ejemplo-Completo

### AST para ILS Clásico

```
AlgorithmNode
├── InitPhase
│   └── DSATURNode
├── SearchPhases
│   ├── LocalSearchPhaseNode
│   │   └── KempeChainNode(max_iterations=100)
│   ├── PerturbationPhaseNode
│   │   └── RandomRecolorNode(strength=0.2)
│   └── LocalSearchPhaseNode
│       └── KempeChainNode(max_iterations=100)
├── Termination
│   └── MaxIterNode(500)
└── Acceptance
    └── BetterOrEqualNode
```

### Pseudocódigo

```
INIT: DSATUR
SEARCH:
  LS[KempeChain(100)]
  PERT[RandomRecolor(0.2)]
  LS[KempeChain(100)]
TERM: MAX_ITER(500)
ACCEPT: BETTER_OR_EQUAL
```

### JSON

```json
{
  "type": "Algorithm",
  "init_phase": {
    "type": "InitPhase",
    "constructive": {"type": "DSATUR"}
  },
  "search_phases": [
    {
      "type": "LocalSearchPhase",
      "operators": [{"type": "KempeChain", "max_iterations": 100}]
    },
    {
      "type": "PerturbationPhase",
      "operator": {"type": "RandomRecolor", "strength": 0.2}
    },
    {
      "type": "LocalSearchPhase",
      "operators": [{"type": "KempeChain", "max_iterations": 100}]
    }
  ],
  "termination": {"type": "MaxIter", "value": 500},
  "acceptance": {"type": "BetterOrEqual"}
}
```

---

## Validación-de-Gramática

Antes de ejecutar un AST, debe validar:

```python
def validate_ast(ast: AlgorithmNode) -> Tuple[bool, List[str]]:
    """
    Validar que AST respeta gramática.
    
    Retorna:
        (is_valid, error_list)
    """
    errors = []
    
    # R1: Estructura mínima
    if not ast.init_phase:
        errors.append("R1: Falta InitPhase")
    if not ast.search_phases:
        errors.append("R1: Falta SearchPhase")
    if not ast.termination:
        errors.append("R1: Falta Termination")
    
    # R2: LocalSearch válido
    for phase in ast.search_phases:
        if isinstance(phase, LocalSearchPhaseNode):
            if len(phase.operators) > 3:
                errors.append(f"R2: Fase LS tiene {len(phase.operators)} > 3")
    
    # R3: Perturbación válida
    # ... (similar)
    
    return len(errors) == 0, errors
```

---

**Próximo paso**: Implementar clases Python en `04-Generated/scripts/ast_nodes.py`
