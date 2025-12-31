---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP con Iterated Local Search"
  problem: "Graph Coloring Problem"
  metaheuristic: "Iterated Local Search"
  status: "active"
  created: "2025-11-17"
---

# Proyecto: Graph Coloring Problem con Iterated Local Search

## ðŸŽ¯ InformaciÃ³n del Proyecto

**Problema**: Graph Coloring Problem (GCP)  
**MetaheurÃ­stica**: Iterated Local Search (ILS)  
**Objetivo**: Generar algoritmos automÃ¡ticamente mediante GAA para resolver instancias de coloraciÃ³n de grafos

---

## ðŸ“‹ Status de ImplementaciÃ³n

**Fase 1: Core (PRIORIDAD 1)** - â³ Pendiente
- [ ] `core/problem.py` - Clase `GraphColoringProblem` con validaciones
- [ ] `core/solution.py` - Clase `ColoringSolution` con propiedades
- [ ] `core/evaluation.py` - Clase `ColoringEvaluator` con mÃ©tricas
- [ ] `core/__init__.py` - Exports

**Fase 2: Operators (PRIORIDAD 2)** - â³ Pendiente
- [ ] `operators/constructive.py` - GreedyDSATUR, GreedyLF, RandomSequential
- [ ] `operators/improvement.py` - KempeChain, OneVertexMove, TabuCol
- [ ] `operators/perturbation.py` - RandomRecolor, PartialDestroy
- [ ] `operators/repair.py` - RepairConflicts
- [ ] `operators/__init__.py` - Exports

**Fase 3: Metaheuristic (PRIORIDAD 3)** - â³ Pendiente
- [ ] `metaheuristic/ils_core.py` - Clase `IteratedLocalSearch`
- [ ] `metaheuristic/perturbation_schedules.py` - Esquemas de perturbaciÃ³n
- [ ] `metaheuristic/__init__.py` - Exports

**Fase 4: Testing (PRIORIDAD 4)** - â³ Pendiente
- [ ] `tests/test_core.py` - 15+ tests para Core
- [ ] `tests/test_operators.py` - Tests para operadores
- [ ] `tests/test_ils.py` - Tests para ILS

**Fase 5: Scripts ejecutables (PRIORIDAD 5)** - â³ Pendiente
- [ ] `scripts/test_quick.py` - ValidaciÃ³n rÃ¡pida (10s)
- [ ] `scripts/demo_complete.py` - Demo funcional (30s)
- [ ] `scripts/demo_experimentation.py` - Experimentos (5 min)
- [ ] `scripts/experiment_large_scale.py` - Benchmarks

**Fase 6: ConfiguraciÃ³n y Docs (PRIORIDAD 6)** - â³ Pendiente
- [ ] `config/config.yaml` - ParÃ¡metros centralizados
- [ ] `docs/QUICKSTART.md` - GuÃ­a de inicio rÃ¡pido
- [ ] `docs/ARCHITECTURE.md` - Diagrama de arquitectura
- [ ] `requirements.txt` - Dependencias Python

---

# PARTE 1: DEFINICIÃ“N DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Graph Coloring Problem (GCP)  
**Tipo**: MinimizaciÃ³n  
**CategorÃ­a**: Combinatorial Optimization - NP-Complete

## DescripciÃ³n Informal

El problema de coloraciÃ³n de grafos consiste en asignar colores a los vÃ©rtices de un grafo de tal manera que ningÃºn par de vÃ©rtices adyacentes (conectados por una arista) tengan el mismo color, utilizando el mÃ­nimo nÃºmero de colores posible.

**Aplicaciones**:
- AsignaciÃ³n de frecuencias en redes de comunicaciÃ³n
- PlanificaciÃ³n de horarios (scheduling)
- AsignaciÃ³n de registros en compiladores
- ResoluciÃ³n de sudokus
- DiseÃ±o de circuitos VLSI

## Mathematical-Model

### FunciÃ³n Objetivo

```math
\text{Minimizar: } k = \text{nÃºmero de colores utilizados}
```

### Restricciones

```math
c_i \neq c_j, \quad \forall (i,j) \in E
```

```math
c_i \in \{1, 2, \ldots, k\}, \quad \forall i \in V
```

### Variables de DecisiÃ³n

- **c_i**: Color asignado al vÃ©rtice i
- **V**: Conjunto de vÃ©rtices del grafo
- **E**: Conjunto de aristas del grafo
- **k**: NÃºmero de colores utilizados (a minimizar)
- **n = |V|**: NÃºmero de vÃ©rtices
- **m = |E|**: NÃºmero de aristas

### ImplementaciÃ³n de Clases (PENDIENTE)

**Archivo**: `core/problem.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np

@dataclass
class GraphColoringProblem:
    """
    DefiniciÃ³n del Graph Coloring Problem (0/1)
    
    Modelo MatemÃ¡tico:
    ------------------
    Minimizar: k = nÃºmero de colores
    
    Sujeto a:
        c_i â‰  c_j, âˆ€(i,j) âˆˆ E  (restricciÃ³n de adyacencia)
        c_i âˆˆ {1,2,...,k}, âˆ€i âˆˆ V  (dominio de colores)
    
    Donde:
        V: conjunto de vÃ©rtices (n = |V|)
        E: conjunto de aristas (m = |E|)
        c_i: color del vÃ©rtice i
        k: nÃºmero de colores (a minimizar)
    
    ParÃ¡metros:
        vertices: int
            NÃºmero de vÃ©rtices (n)
        edges: List[Tuple[int, int]]
            Lista de aristas (u, v) donde u < v
        colors_known: Optional[int]
            NÃºmero cromÃ¡tico conocido (si existe), del archivo BKS.json
        name: str
            Nombre descriptivo de la instancia
    
    Atributos computados:
        adjacency_list: Dict[int, List[int]]
            Lista de adyacencia para acceso rÃ¡pido a vecinos
    
    Ejemplo:
    --------
    >>> problem = GraphColoringProblem(
    ...     vertices=47,
    ...     edges=[(0,1), (0,3), (1,2), ...],
    ...     colors_known=5,
    ...     name="myciel5"
    ... )
    """
    
    vertices: int
    edges: List[Tuple[int, int]]
    colors_known: Optional[int] = None
    name: str = "GCP"
    
    def __post_init__(self):
        """ValidaciÃ³n tras inicializaciÃ³n"""
        
        # Validar vertices
        if self.vertices <= 0:
            raise ValueError(f"NÃºmero de vÃ©rtices debe ser positivo, recibido: {self.vertices}")
        
        # Validar edges
        if not isinstance(self.edges, list):
            self.edges = list(self.edges)
        
        for i, (u, v) in enumerate(self.edges):
            if not (0 <= u < self.vertices and 0 <= v < self.vertices):
                raise ValueError(f"Arista {i}: ({u},{v}) fuera de rango [0,{self.vertices-1}]")
            if u == v:
                raise ValueError(f"Arista {i}: self-loop detectado ({u},{u})")
        
        # Validar colors_known
        if self.colors_known is not None and self.colors_known <= 0:
            raise ValueError(f"colors_known debe ser positivo, recibido: {self.colors_known}")
        
        # Construir lista de adyacencia
        self._build_adjacency_list()
    
    def _build_adjacency_list(self) -> Dict[int, List[int]]:
        """Construir lista de adyacencia para acceso rÃ¡pido"""
        self.adjacency_list = {i: [] for i in range(self.vertices)}
        for u, v in self.edges:
            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)
        return self.adjacency_list
    
    @property
    def num_edges(self) -> int:
        """NÃºmero de aristas"""
        return len(self.edges)
    
    @property
    def density(self) -> float:
        """Densidad del grafo: m / (n*(n-1)/2)"""
        max_edges = self.vertices * (self.vertices - 1) / 2
        return self.num_edges / max_edges if max_edges > 0 else 0
    
    @property
    def max_degree(self) -> int:
        """Grado mÃ¡ximo del grafo"""
        return max((len(neighbors) for neighbors in self.adjacency_list.values()), default=0)
    
    @property
    def min_degree(self) -> int:
        """Grado mÃ­nimo del grafo"""
        return min((len(neighbors) for neighbors in self.adjacency_list.values()), default=0)
    
    @property
    def avg_degree(self) -> float:
        """Grado promedio del grafo"""
        return 2 * self.num_edges / self.vertices if self.vertices > 0 else 0
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GraphColoringProblem':
        """Crear desde diccionario (JSON)"""
        return cls(
            vertices=data['vertices'],
            edges=[tuple(e) for e in data['edges']],
            colors_known=data.get('colors_known'),
            name=data.get('name', 'GCP')
        )
    
    def to_dict(self) -> Dict:
        """Serializar a diccionario"""
        return {
            'vertices': self.vertices,
            'edges': [list(e) for e in self.edges],
            'colors_known': self.colors_known,
            'name': self.name,
            'num_edges': self.num_edges,
            'density': self.density,
            'max_degree': self.max_degree
        }
```

---

### Terminales Identificados

#### Constructivos
- **GreedyDSATUR**: ConstrucciÃ³n voraz por grado de saturaciÃ³n (colores distintos en vecinos) [Brelaz1979]
- **GreedyLF**: Largest First - ordena por grado decreciente y asigna colores [Welsh1967]
- **GreedySL**: Smallest Last - ordena por grado creciente recursivamente [Matula1972]
- **RandomSequential**: AsignaciÃ³n secuencial aleatoria de colores [Johnson1974]
- **RLF**: Recursive Largest First - coloraciÃ³n recursiva por subconjuntos independientes [Leighton1979]

#### Mejora Local
- **KempeChain**: Intercambio de colores mediante cadenas de Kempe [Kempe1879]
- **TabuCol**: BÃºsqueda local con memoria tabÃº [Hertz1987]
- **OneVertexMove**: Cambia color de un vÃ©rtice conflictivo al mejor color disponible [Galinier1999]
- **SwapColors**: Intercambia dos colores en toda la soluciÃ³n [Fleurent1996]

#### PerturbaciÃ³n
- **RandomRecolor**: Recolorea aleatoriamente k vÃ©rtices [Chiarandini2005]
- **PartialDestroy**: Destruye coloraciÃ³n de subgrafo y reconstruye [Malaguti2008]
- **ColorClassMerge**: Fusiona dos clases de color y repara [Avanthay2003]

#### IntensificaciÃ³n
- **Intensify**: Reduce nÃºmero de colores y repara violaciones [Galinier1999]
- **GreedyImprovement**: Mejora local exhaustiva cambiando colores [Hertz1987]

#### ReparaciÃ³n
- **RepairConflicts**: Elimina conflictos cambiando colores de vÃ©rtices conflictivos [Johnson1991]
- **BacktrackRepair**: ReparaciÃ³n con backtracking limitado [Brelaz1979]

## Solution-Representation

### Estructura de Datos

**RepresentaciÃ³n en memoria**:
```python
# Vector de colores de longitud n (nÃºmero de vÃ©rtices)
c = [c_1, c_2, ..., c_n]
# donde c_i âˆˆ {1, 2, ..., k}
# c_i = color asignado al vÃ©rtice i
```

**Ejemplo**:
```
Grafo: n=5 vÃ©rtices, aristas={(0,1), (0,2), (1,2), (2,3), (3,4)}
SoluciÃ³n: c = [1, 2, 3, 1, 2]
InterpretaciÃ³n:
  - VÃ©rtice 0: color 1
  - VÃ©rtice 1: color 2
  - VÃ©rtice 2: color 3
  - VÃ©rtice 3: color 1
  - VÃ©rtice 4: color 2
NÃºmero de colores: k = 3
Conflictos: 0 (soluciÃ³n factible)
```

### ImplementaciÃ³n de Clases (PENDIENTE)

**Archivo**: `core/solution.py`

```python
from dataclasses import dataclass
import numpy as np
from typing import Optional

@dataclass
class ColoringSolution:
    """
    RepresentaciÃ³n de una soluciÃ³n para Graph Coloring Problem
    
    Atributos:
        assignment: np.ndarray
            Vector de asignaciÃ³n de colores [0, 1, 2, 1, ...]
            Ãndice = vÃ©rtice, valor = color asignado (0-indexed)
        problem: GraphColoringProblem
            Referencia al problema
        value: Optional[int]
            Cache del nÃºmero de colores (k)
    """
    
    assignment: np.ndarray
    problem: 'GraphColoringProblem'
    value: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones tras inicializaciÃ³n"""
        # Validar que assignment tiene longitud n
        assert len(self.assignment) == self.problem.vertices
        
        # Validar que todos los colores son vÃ¡lidos (0 <= c < n)
        assert np.all(self.assignment >= 0)
        assert np.all(self.assignment < self.problem.vertices)
    
    @property
    def num_colors(self) -> int:
        """Retorna nÃºmero de colores utilizados"""
        return int(np.max(self.assignment)) + 1
    
    @property
    def num_conflicts(self) -> int:
        """Retorna nÃºmero de conflictos (aristas con vÃ©rtices del mismo color)"""
        conflicts = 0
        for u, v in self.problem.edges:
            if self.assignment[u] == self.assignment[v]:
                conflicts += 1
        return conflicts
    
    def is_feasible(self) -> bool:
        """Â¿La soluciÃ³n es factible? (sin conflictos)"""
        return self.num_conflicts == 0
    
    def copy(self) -> 'ColoringSolution':
        """Crear copia profunda de la soluciÃ³n"""
        return ColoringSolution(
            assignment=self.assignment.copy(),
            problem=self.problem,
            value=self.value
        )
```

---

**Restricciones duras**:
1. **No adyacencia**: VÃ©rtices adyacentes deben tener colores diferentes
2. **Conectividad**: Todos los vÃ©rtices deben estar coloreados

**ParÃ¡metros del problema**:
- **n**: NÃºmero de vÃ©rtices
- **m**: NÃºmero de aristas
- **E**: Conjunto de aristas (pares de vÃ©rtices)
- **Î”**: Grado mÃ¡ximo del grafo
- **Ï‡**: NÃºmero cromÃ¡tico (mÃ­nimo teÃ³rico, usualmente desconocido)

## Evaluation-Criteria

### MÃ©tricas de Calidad

**MÃ©trica principal**: NÃºmero de colores utilizados (k)  
**Criterio de comparaciÃ³n**: Menor es mejor  
**Manejo de infactibilidad**: 
- **PenalizaciÃ³n**: fitness = k + nÃºmero_de_conflictos Ã— 100
- **ReparaciÃ³n**: Aplicar RepairConflicts antes de evaluar
- **Permitir infactibilidad temporal** durante bÃºsqueda (enfoque TabuCol)

### ImplementaciÃ³n de Evaluador (PENDIENTE)

**Archivo**: `core/evaluation.py`

```python
from typing import Dict, Any, Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution

class ColoringEvaluator:
    """
    Evaluador de soluciones para Graph Coloring Problem
    
    Calcula mÃºltiples mÃ©tricas de calidad:
    - fitness: nÃºmero de colores + penalizaciÃ³n por conflictos
    - num_colors: nÃºmero de colores utilizados
    - conflicts: nÃºmero de conflictos (aristas monocromÃ¡ticas)
    - feasible: Â¿es una soluciÃ³n vÃ¡lida?
    - gap: diferencia respecto a mejor conocido
    """
    
    @staticmethod
    def evaluate(solution: ColoringSolution, 
                 problem: GraphColoringProblem) -> Dict[str, Any]:
        """
        Evaluar una soluciÃ³n
        
        ParÃ¡metros:
        -----------
        solution : ColoringSolution
            SoluciÃ³n a evaluar
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        Dict con claves:
            'num_colors' : int
                NÃºmero de colores utilizados (k)
            'conflicts' : int
                NÃºmero de conflictos (aristas monocromÃ¡ticas)
            'feasible' : bool
                Â¿Respeta todas las restricciones?
            'fitness' : float
                Valor de funciÃ³n objetivo con penalizaciÃ³n
            'gap' : Optional[float]
                (optimal - num_colors) / optimal si se conoce Ã³ptimo
        
        Ejemplo:
        --------
        >>> problem = GraphColoringProblem(vertices=47, edges=[...])
        >>> solution = GreedyDSATUR.construct(problem)
        >>> metrics = ColoringEvaluator.evaluate(solution, problem)
        >>> print(f"Colores: {metrics['num_colors']}, Conflictos: {metrics['conflicts']}")
        """
        
        # Calcular nÃºmero de colores
        num_colors = solution.num_colors
        
        # Calcular conflictos
        conflicts = solution.num_conflicts
        
        # Evaluar factibilidad
        feasible = conflicts == 0
        
        # Calcular fitness con penalizaciÃ³n
        CONFLICT_PENALTY = 100
        fitness = num_colors + conflicts * CONFLICT_PENALTY
        
        # Calcular gap respecto a Ã³ptimo
        gap = None
        if problem.colors_known is not None:
            gap = (num_colors - problem.colors_known) / problem.colors_known
        
        return {
            'num_colors': num_colors,
            'conflicts': conflicts,
            'feasible': feasible,
            'fitness': fitness,
            'gap': gap
        }
    
    @staticmethod
    def batch_evaluate(solutions: list[ColoringSolution],
                       problem: GraphColoringProblem) -> list[Dict[str, Any]]:
        """
        Evaluar mÃºltiples soluciones
        
        ParÃ¡metros:
        -----------
        solutions : list[ColoringSolution]
            Lista de soluciones
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        list[Dict[str, Any]]
            Lista de mÃ©tricas (una por soluciÃ³n)
        
        Ejemplo:
        --------
        >>> solutions = [algorithm.run() for _ in range(10)]
        >>> metrics_list = ColoringEvaluator.batch_evaluate(solutions, problem)
        """
        return [ColoringEvaluator.evaluate(sol, problem) for sol in solutions]
```

---

## Domain-Operators---

# PARTE 2: METAHEURÃSTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Iterated Local Search (ILS)  
**Tipo**: MetaheurÃ­stica de trayectoria con perturbaciÃ³n e intensificaciÃ³n  
**Referencia**: [Lourenco2003, StÃ¼tzle2006]

## DescripciÃ³n del MÃ©todo

Iterated Local Search (ILS) es una metaheurÃ­stica que itera entre tres fases principales:
1. **BÃºsqueda local**: IntensificaciÃ³n hasta Ã³ptimo local
2. **PerturbaciÃ³n**: Escape del Ã³ptimo local mediante cambios significativos
3. **Criterio de aceptaciÃ³n**: Decide si acepta la nueva soluciÃ³n

**Ventajas para GAA en GCP**:
- Efectivo para problemas de coloraciÃ³n
- Balance entre intensificaciÃ³n (bÃºsqueda local) y diversificaciÃ³n (perturbaciÃ³n)
- Estructura modular que se adapta bien a AST
- Resultados competitivos en benchmarks de GCP

## Configuration

**ParÃ¡metros principales**:

```yaml
max_iteraciones: 500
intensidad_perturbacion: 0.20  # Porcentaje de vÃ©rtices a recolorear
tipo_busqueda_local: "best_improvement"  # First vs Best
criterio_aceptacion: "better_or_equal"  # Always, Better, Better-or-Equal
max_iteraciones_sin_mejora: 50
```

**JustificaciÃ³n**:
- 500 iteraciones: Balance entre calidad y tiempo
- 20% perturbaciÃ³n: Suficiente para escape, no tan drÃ¡stico
- Best improvement: Mayor calidad de Ã³ptimos locales
- Better-or-equal: Permite diversificaciÃ³n moderada

## Search-Strategy

### Operadores de BÃºsqueda sobre AST

**MutaciÃ³n de Nodo FunciÃ³n**:
- Reemplazar nodo de bÃºsqueda local por otro tipo
- Ejemplo: `LocalSearch(KempeChain)` â†’ `LocalSearch(OneVertexMove)`
- Probabilidad: 0.25

**MutaciÃ³n de Terminal**:
- Cambiar operador de construcciÃ³n o mejora
- Ejemplo: `GreedyDSATUR` â†’ `GreedyLF`
- Probabilidad: 0.50

**MutaciÃ³n de ParÃ¡metro**:
- Modificar intensidad de perturbaciÃ³n
- Ejemplo: perturb_ratio: 0.20 â†’ 0.25
- PerturbaciÃ³n: Â±15%
- Probabilidad: 0.25

### Estructura TÃ­pica de ILS

```python
def ILS():
    s = GenerarSolucionInicial()  # ConstrucciÃ³n
    s = BusquedaLocal(s)           # IntensificaciÃ³n
    s_best = s
    
    for iter in range(max_iterations):
        s_pert = Perturbar(s)      # Escape
        s_new = BusquedaLocal(s_pert)  # IntensificaciÃ³n
        
        if Aceptar(s_new, s):
            s = s_new
        
        if f(s_new) < f(s_best):
            s_best = s_new
    
    return s_best
```

### Acceptance-Criteria

**Estrategias disponibles**:

1. **Always Accept** (Siempre acepta):
```python
def accept(s_new, s_current):
    return True
```

2. **Better Only** (Solo mejoras):
```python
def accept(s_new, s_current):
    return fitness(s_new) < fitness(s_current)
```

3. **Better-or-Equal** (Mejoras o iguales):
```python
def accept(s_new, s_current):
    return fitness(s_new) <= fitness(s_current)
```

**Seleccionado para GCP**: Better-or-Equal (permite moverse por plateaus)

## Presupuesto Computacional

**Criterio de parada**:
- [x] NÃºmero de iteraciones: 500
- [x] Iteraciones sin mejora: 50
- [ ] Tiempo lÃ­mite: N/A
- [ ] Ã“ptimo conocido alcanzado: Opcional

**Presupuesto por evaluaciÃ³n de AST**:
- Iteraciones ILS por instancia: 500
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~45 segundos

## AST-Specific Considerations

**ValidaciÃ³n de AST**:
- Validar gramÃ¡tica despuÃ©s de mutaciÃ³n: SÃ­
- ReparaciÃ³n automÃ¡tica de AST invÃ¡lidos: SÃ­
- Profundidad mÃ¡xima del Ã¡rbol: 10

**InicializaciÃ³n**:
- MÃ©todo: Grow (crecimiento aleatorio con profundidad variable)
- Profundidad inicial: 4-6
- PoblaciÃ³n inicial de AST: 1 (ILS es single-solution)

**Operadores obligatorios en AST**:
- Al menos un constructor (e.g., GreedyDSATUR)
- Al menos una bÃºsqueda local
- Al menos una perturbaciÃ³n

---

# PARTE 3: DATASETS

## UbicaciÃ³n de Datasets

```
projects/GCP-ILS/datasets/
â”œâ”€â”€ training/          # Instancias para optimizar AST
â”‚   â””â”€â”€ [Archivos .col o .txt]
â”œâ”€â”€ validation/        # Instancias para ajustar parÃ¡metros ILS
â”‚   â””â”€â”€ [Archivos .col o .txt]
â””â”€â”€ test/              # Instancias para evaluaciÃ³n final
    â””â”€â”€ [Archivos .col o .txt]
```

## Formato de Archivo de Instancia

**Formato DIMACS** (`.col`):
```
p edge <n> <m>
e <v1> <v2>
e <v1> <v3>
...
```

**Formato Simplificado** (`.txt`):
```
n m
v1 v2
v1 v3
...
```

**Ejemplo** (`myciel3.col`):
```
p edge 11 20
e 1 2
e 1 4
e 1 7
e 1 9
e 2 3
e 2 6
e 2 8
e 3 5
e 3 7
e 3 10
e 4 5
e 4 6
e 4 10
e 5 8
e 6 11
e 7 11
e 8 11
e 9 11
e 10 11
```

## Datasets Disponibles

### ðŸ“Š DescripciÃ³n General

El proyecto incluye **79 instancias DIMACS** organizadas en **8 familias** con caracterÃ­sticas diversas:
- Instancias pequeÃ±as (myciel: 10-23 vÃ©rtices)
- Instancias medianas (LEI, REG, MYC: 100-450 vÃ©rtices)
- Instancias grandes (DSJ, CUL, SGB: 300-1000+ vÃ©rtices)
