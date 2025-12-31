# Architecture Guide - NEW-GCP-ILS-OK

Documentación detallada de la arquitectura del framework de Graph Coloring con ILS.

## Visión general

El framework NEW-GCP-ILS-OK implementa un solver completo para el Graph Coloring Problem (GCP) usando Iterated Local Search (ILS) como metaheurística principal.

```
┌─────────────────────────────────────────────────────────────┐
│                     APLICACION / USUARIO                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   METAHEURISTIC LAYER                        │
│   ┌────────────────────────────────────────────────────┐    │
│   │  IteratedLocalSearch / HybridILS                   │    │
│   │  - Orquesta el flujo completo                      │    │
│   │  - Gestiona iteraciones y criterio de parada       │    │
│   │  - Registra estadísticas                           │    │
│   └────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐ ┌────────▼────────┐ ┌─────▼──────────┐
│CONSTRUCTIVE  │ │ IMPROVEMENT     │ │ PERTURBATION  │
│OPERATORS     │ │ OPERATORS       │ │ OPERATORS     │
├──────────────┤ ├─────────────────┤ ├────────────────┤
│- DSATUR      │ │- OneVertexMove  │ │- RandomRecolor │
│- LargestFirst│ │- KempeChain     │ │- PartialDestroy│
│- RandomSeq   │ │- TabuColoring   │ │- ColorClassMerge
└──────────────┘ └─────────────────┘ └────────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    SOLUTION LAYER                           │
│   ┌────────────────────────────────────────────────────┐    │
│   │  ColoringSolution                                  │    │
│   │  - Représentation de coloreo                       │    │
│   │  - Cálculo de conflictos                           │    │
│   │  - Validación                                      │    │
│   └────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     PROBLEM LAYER                           │
│   ┌────────────────────────────────────────────────────┐    │
│   │  GraphColoringProblem                              │    │
│   │  - Representación del grafo                        │    │
│   │  - Lista de adyacencia en caché                    │    │
│   │  - Métricas del grafo                             │    │
│   └────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   EVALUATION LAYER                          │
│   ┌────────────────────────────────────────────────────┐    │
│   │  ColoringEvaluator                                 │    │
│   │  - Métricas de calidad                             │    │
│   │  - Comparación de soluciones                       │    │
│   │  - Reportes                                        │    │
│   └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Componentes principales

### 1. FASE 1: CORE

**Ubicación**: `core/`

#### GraphColoringProblem (`core/problem.py`)

Representa una instancia del problema de coloreo de grafos.

```python
class GraphColoringProblem:
    vertices: int              # Número de vértices
    edges: List[Tuple]         # Lista de aristas
    _adjacency_list: Dict      # Caché de lista de adyacencia (O(1) lookup)
    colors_known: Optional[int] # Número cromático conocido (para validación)
```

**Responsabilidades**:
- Validar la instancia del problema
- Proporcionar acceso O(1) a vecinos de un vértice
- Calcular métricas del grafo (densidad, grado, etc.)
- Serialización a/desde JSON

**Métodos clave**:
```python
def get_neighbors(v: int) -> List[int]      # O(1) con caché
def get_degree(v: int) -> int               # Grado del vértice
def is_adjacent(u: int, v: int) -> bool    # ¿Arista existe?

@property
def density() -> float                       # Densidad del grafo
def to_dict() / from_dict()                  # Serialización JSON
```

#### ColoringSolution (`core/solution.py`)

Representa una asignación de colores (solución).

```python
class ColoringSolution:
    assignment: np.ndarray     # Asignación v -> color
    problem: GraphColoringProblem
    _num_conflicts: Optional[int]  # Caché
    _color_classes: Optional[Dict] # Caché
```

**Responsabilidades**:
- Mantener una asignación válida de colores
- Detectar conflictos
- Calcular colores disponibles
- Validar factibilidad

**Métodos clave**:
```python
@property
def num_colors() -> int                     # Colores usados
@property
def num_conflicts() -> int                  # Conflictos detectados
def is_feasible() -> bool                   # ¿Es factible?
def get_available_colors(v: int) -> List   # Colores sin conflicto
def get_conflicting_vertices() -> List[int] # Vértices con conflicto
def fitness(penalty_weight: float) -> float # Función fitness
```

#### ColoringEvaluator (`core/evaluation.py`)

Evalúa soluciones y calcula métricas de calidad.

```python
class ColoringEvaluator:
    CONFLICT_PENALTY = 100  # Penalidad por conflicto
```

**Responsabilidades**:
- Evaluar soluciones individuales
- Comparar pares de soluciones
- Generar reportes

**Métodos clave**:
```python
@staticmethod
def evaluate(solution: ColoringSolution, 
             problem: GraphColoringProblem) -> Dict
    # Retorna: num_colors, num_conflicts, is_feasible, fitness, gap

@staticmethod
def batch_evaluate(solutions: List, problem: GraphColoringProblem) -> List[Dict]

@staticmethod
def compare_solutions(sol1, sol2, problem) -> ColoringSolution
    # Retorna la mejor solución
```

### 2. FASE 2: OPERATORS

**Ubicación**: `operators/`

#### Operadores Constructivos (`operators/constructive.py`)

Generan una solución inicial desde cero.

**GreedyDSATUR**: Algoritmo de Brelaz (1979)
- Ordena vértices por grado de saturación (# colores en vecinos)
- Produce buenas soluciones en O(n²)
- Determinístico

**GreedyLargestFirst**: Ordena por grado decreciente
- Simple y rápido
- O(n²) pero con constante menor que DSATUR

**RandomSequential**: Orden aleatorio
- Genera diversidad con diferentes semillas
- Útil para múltiples arranques

#### Operadores de Mejora (`operators/improvement.py`)

Mejoran una solución mediante búsqueda local.

**OneVertexMove**:
- Intenta mover cada vértice al color que minimiza conflictos
- First-improvement
- O(n·d) por iteración (d = grado máximo)

**KempeChainMove**:
- Intercambia dos colores en componentes conexas
- Puede eliminar conflictos para pasar a factible
- Fundamentado teóricamente

**TabuColMove**:
- Tabu Search con lista tabu
- Permite movimientos que empeoran para escapar óptimos locales
- Parámetro: tabu_tenure

#### Operadores de Perturbación (`operators/perturbation.py`)

Hacen cambios grandes para escapar de óptimos locales.

**RandomRecolor**:
- Reasigna colores aleatorios a k vértices
- Intensidad controlable (k = strength · n)

**PartialDestroy**:
- Destruye parcialmente la solución (remueve colores)
- Repara greedy
- Adapta la solución a nuevas regiones

**ColorClassMerge**:
- Fusiona dos clases de colores
- Intenta reducir número de colores
- Oportunidad de compactación

**AdaptivePerturbation**:
- Adapta intensidad basada en éxito previo
- ↓ intensidad si mejora
- ↑ intensidad si sin mejora

#### Operadores de Reparación (`operators/repair.py`)

Convierten soluciones infactibles a factibles.

**GreedyRepair**:
- Itera sobre vértices con conflictos
- Asigna color mínimo disponible
- O(n·d) iteraciones

**ConflictMinimizingRepair**:
- Minimiza conflictos (no necesariamente factible)
- Para instancias donde factibilidad es difícil

**ConstraintPropagationRepair**:
- Detecta valores forzados rápidamente
- Puede detectar infactibilidad

**BacktrackingRepair**:
- Busca asignación factible con backtracking
- Garantiza factibilidad si existe
- Exponencial pero podable

### 3. FASE 3: METAHEURISTIC

**Ubicación**: `metaheuristic/`

#### IteratedLocalSearch (`metaheuristic/ils_core.py`)

Orquesta el flujo completo de ILS.

```python
class IteratedLocalSearch:
    # Fase 1: Construcción
    # → Generar solución inicial con GreedyDSATUR
    
    # Fase 2: Mejora iterativa
    # → Aplicar OneVertexMove hasta convergencia local
    # → Si mejora respecto a best_solution: aceptar
    # → Sino: aceptar igual (Iterated)
    
    # Fase 3: Perturbación
    # → Perturbar solución actual
    # → Volver a Fase 2
```

**Parámetros**:
- `max_iterations`: Iteraciones totales máximas
- `max_no_improve`: Parada anticipada si no mejora
- `ls_max_iterations`: Iteraciones de búsqueda local
- `perturbation_strength`: Fuerza inicial (0-1)
- `use_adaptive_perturbation`: Adaptación de fuerza

**Historial**:
```python
history = {
    'iteration': [0, 1, 2, ...],
    'best_fitness': [...],
    'current_fitness': [...],
    'num_colors': [...],
    'num_conflicts': [...],
}
```

#### Estrategias de Perturbación (`metaheuristic/schedules.py`)

Controlan cómo varía la intensidad de perturbación.

**ConstantPerturbation**: Fuerza constante
**LinearDecayPerturbation**: Decrece linealmente
**ExponentialDecayPerturbation**: Decrece exponencialmente
**ExplorationExploitationPerturbation**: Transición desde exploración a explotación
**AdaptivePerturbationSchedule**: Se adapta dinámicamente
**CyclicPerturbation**: Oscila entre mín y máx
**DynamicPerturbationSchedule**: Se adapta a velocidad de mejora

### 4. FASE 4: TESTING

**Ubicación**: `tests/`

Tests con pytest:

**test_core.py**: Tests para GraphColoringProblem, ColoringSolution, ColoringEvaluator
**test_operators.py**: Tests para constructivos, mejora, perturbación, reparación
**test_ils.py**: Tests para ILS y casos DIMACS

Ejecutar:
```bash
pytest tests/ -v
pytest tests/test_core.py::TestGraphColoringProblem::test_adjacency_list -v
```

### 5. FASE 5: SCRIPTS

**Ubicación**: `scripts/`

**test_quick.py**: Validación rápida (10s) con instancias pequeñas
**demo_complete.py**: Demo (30s) mostrando capacidades
**experiment.py**: Experimentación extendida (5+ min) con múltiples configuraciones

### 6. FASE 6: CONFIGURATION

**Ubicación**: `config/`

**config.yaml**: Configuración centralizada de:
- Parámetros ILS
- Operadores
- Directorios
- Logging

**requirements.txt**: Dependencias Python

## Flujo de ejecución

### Ejecución simple

```
Usuario llama: ils.run()
    ↓
1. Construcción: GreedyDSATUR.construct()
    ↓
2. LOOP principal (max_iterations):
    a) Mejora: OneVertexMove.improve()
    b) ¿Mejor que best? → Actualizar best
    c) Perturbación: RandomRecolor.perturb()
    d) Registrar en historial
    e) Verificar criterio de parada
    ↓
3. Return best_solution
```

### Integración de componentes

```
GraphColoringProblem (define el grafo)
    ↓
GreedyDSATUR.construct(problem) → ColoringSolution
    ↓
OneVertexMove.improve(solution) → ColoringSolution mejorada
    ↓
ColoringEvaluator.evaluate(solution) → Métricas
    ↓
RandomRecolor.perturb(solution) → Solución perturbada
    ↓
(Repetir hasta convergencia)
```

## Patrones de diseño

### 1. Strategy Pattern

Operadores intercambiables:
```python
# Puede cambiar constructivo
constructor = GreedyDSATUR()  # o GreedyLargestFirst

# Puede cambiar búsqueda local  
local_search = OneVertexMove()  # o KempeChainMove

# Puede cambiar perturbación
perturbator = RandomRecolor()  # o PartialDestroy
```

### 2. Dependency Injection

Cada operador recibe problema y solución como parámetros:
```python
# No hay estado global, todo es funcional
solution = operator.construct(problem, seed=42)
solution = operator.improve(solution, problem)
```

### 3. Composition

ILS compone múltiples operadores:
```python
ils = IteratedLocalSearch(problem)
# Internamente usa:
# - constructor (GreedyDSATUR)
# - local_search (OneVertexMove)
# - perturbator (RandomRecolor)
```

### 4. Data Classes

Uso extensivo de `@dataclass` para objetos limpios:
```python
@dataclass
class GraphColoringProblem:
    vertices: int
    edges: List[Tuple[int, int]]
    ...
```

## Consideraciones de rendimiento

### Cuellos de botella

1. **Cálculo de conflictos**: O(m) por verificación
   - Solución: Mantener en caché, actualizar incrementalmente

2. **Búsqueda de colores disponibles**: O(d) por vértice
   - Solución: Mantener set de colores usados por vecinos

3. **Búsqueda local**: O(n·d·k) donde k = colores
   - Solución: Usar first-improvement, limitar iteraciones

### Optimizaciones aplicadas

1. **Caché de lista de adyacencia**: O(1) lookup en lugar de O(m)
2. **Validación incremental**: No verificar todo el grafo cada vez
3. **Early termination**: Parar búsqueda local si sin mejora
4. **Adaptive perturbation**: Ajustar esfuerzo dinámicamente

## Escalabilidad

El framework está diseñado para:

- **Instancias pequeñas** (n < 50): DSATUR + One Vertex Move
- **Instancias medianas** (50 < n < 500): ILS con perturbación adaptativa  
- **Instancias grandes** (n > 500): Tabu Search + PartialDestroy

Estimaciones de tiempo:
- n=20: < 1 segundo
- n=100: 5-10 segundos
- n=500: 1-5 minutos

## Extensibilidad

Para agregar nuevo operador:

1. Crear clase en `operators/[tipo].py`
2. Implementar método `construct()` o `improve()` o `perturb()`
3. Usar GraphColoringProblem y ColoringSolution
4. Agregar tests en `tests/test_operators.py`
5. Actualizar `operators/__init__.py`

Ejemplo:
```python
class MyNewOperator:
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: Optional[int] = None) 
        → ColoringSolution:
        # Implementación
        return ColoringSolution(assignment, problem)
```

## Limitaciones conocidas

1. **No hay paralelización**: Runs se hacen secuencialmente
2. **Memoria**: Caché de lista de adyacencia puede crecer (O(n+m))
3. **No hay warm start**: Cada ILS comienza desde cero
4. **No hay constraint satisfaction**: Asume 3-coloreabilidad mínima

## Referencias

- **ILS**: Lourenço et al. (2019) "Iterated Local Search"
- **DSATUR**: Brelaz (1979) "New methods to color vertices of a graph"
- **Graph Coloring**: NP-complete problem
- **DIMACS**: Standard benchmark format

## Contacto

Para preguntas sobre arquitectura, revisar `docs/ARCHITECTURE.md` o crear un issue.
