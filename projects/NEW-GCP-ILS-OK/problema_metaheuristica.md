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

##  Informacion del Proyecto

**Problema**: Graph Coloring Problem (GCP)  
**METAHEURISTICA**: Iterated Local Search (ILS)  
**Objetivo**: Generar algoritmos automoticamente mediante GAA para resolver instancias de coloracion de grafos

---

##  Status de Implementacion

**Fase 1: Core (PRIORIDAD 1)** -   Pendiente
- [ ] `core/problem.py` - Clase `GraphColoringProblem` con validaciones
- [ ] `core/solution.py` - Clase `ColoringSolution` con propiedades
- [ ] `core/evaluation.py` - Clase `ColoringEvaluator` con metricas
- [ ] `core/__init__.py` - Exports

**Fase 2: Operators (PRIORIDAD 2)** -   Pendiente
- [ ] `operators/constructive.py` - GreedyDSATUR, GreedyLF, RandomSequential
- [ ] `operators/improvement.py` - KempeChain, OneVertexMove, TabuCol
- [ ] `operators/perturbation.py` - RandomRecolor, PartialDestroy
- [ ] `operators/repair.py` - RepairConflicts
- [ ] `operators/__init__.py` - Exports

**Fase 3: Metaheuristic (PRIORIDAD 3)** -   Pendiente
- [ ] `metaheuristic/ils_core.py` - Clase `IteratedLocalSearch`
- [ ] `metaheuristic/perturbation_schedules.py` - Esquemas de perturbacion
- [ ] `metaheuristic/__init__.py` - Exports

**Fase 4: Testing (PRIORIDAD 4)** -   Pendiente
- [ ] `tests/test_core.py` - 15+ tests para Core
- [ ] `tests/test_operators.py` - Tests para operadores
- [ ] `tests/test_ils.py` - Tests para ILS

**Fase 5: Scripts ejecutables (PRIORIDAD 5)** -   Pendiente
- [ ] `scripts/test_quick.py` - Validacion Rapida (10s)
- [ ] `scripts/demo_complete.py` - Demo funcional (30s)
- [ ] `scripts/demo_experimentation.py` - Experimentos (5 min)
- [ ] `scripts/experiment_large_scale.py` - Benchmarks

**Fase 6: CONFIGURACION y Docs (PRIORIDAD 6)** -   Pendiente
- [ ] `config/config.yaml` - Parametros centralizados
- [ ] `docs/QUICKSTART.md` - Guia de inicio rapido
- [ ] `docs/ARCHITECTURE.md` - Diagrama de arquitectura
- [ ] `requirements.txt` - Dependencias Python

---

# PARTE 1: DEFINICION DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Graph Coloring Problem (GCP)  
**Tipo**: Minimizacion  
**Categoria**: Combinatorial Optimization - NP-Complete

## Descripcion Informal

El problema de coloracion de grafos consiste en asignar colores a los vertices de un grafo de tal manera que ningun par de vertices adyacentes (conectados por una arista) tengan el mismo color, utilizando el minimo numero de colores posible.

**Aplicaciones**:
- Asignacion de frecuencias en redes de comunicacion
- Planificacion de horarios (scheduling)
- Asignacion de registros en compiladores
- Resolucion de sudokus
- Diseño de circuitos VLSI

## Mathematical-Model

### Funcion Objetivo

```math
\text{Minimizar: } k = \text{numero de colores utilizados}
```

### Restricciones

```math
c_i \neq c_j, \quad \forall (i,j) \in E
```

```math
c_i \in \{1, 2, \ldots, k\}, \quad \forall i \in V
```

### Variables de Decision

- **c_i**: Color asignado al vertice i
- **V**: Conjunto de vertices del grafo
- **E**: Conjunto de aristas del grafo
- **k**: numero de colores utilizados (a minimizar)
- **n = |V|**: numero de vertices
- **m = |E|**: numero de aristas

### Implementacion de Clases (PENDIENTE)

**Archivo**: `core/problem.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np

@dataclass
class GraphColoringProblem:
    """
    Definicion del Graph Coloring Problem (0/1)
    
    Modelo Matematico:
    ------------------
    Minimizar: k = numero de colores
    
    Sujeto a:
        c_i   c_j,  (i,j)   E  (restriccion de adyacencia)
        c_i   {1,2,...,k},  i   V  (dominio de colores)
    
    Donde:
        V: conjunto de vertices (n = |V|)
        E: conjunto de aristas (m = |E|)
        c_i: color del vertice i
        k: numero de colores (a minimizar)
    
    Parametros:
        vertices: int
            numero de vertices (n)
        edges: List[Tuple[int, int]]
            Lista de aristas (u, v) donde u < v
        colors_known: Optional[int]
            numero cromatico conocido (si existe), del archivo BKS.json
        name: str
            Nombre descriptivo de la instancia
    
    Atributos computados:
        adjacency_list: Dict[int, List[int]]
            Lista de adyacencia para acceso rapido a vecinos
    
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
        """Validacion tras inicializacion"""
        
        # Validar vertices
        if self.vertices <= 0:
            raise ValueError(f"numero de vertices debe ser positivo, recibido: {self.vertices}")
        
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
        """Construir lista de adyacencia para acceso rapido"""
        self.adjacency_list = {i: [] for i in range(self.vertices)}
        for u, v in self.edges:
            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)
        return self.adjacency_list
    
    @property
    def num_edges(self) -> int:
        """numero de aristas"""
        return len(self.edges)
    
    @property
    def density(self) -> float:
        """Densidad del grafo: m / (n*(n-1)/2)"""
        max_edges = self.vertices * (self.vertices - 1) / 2
        return self.num_edges / max_edges if max_edges > 0 else 0
    
    @property
    def max_degree(self) -> int:
        """Grado moximo del grafo"""
        return max((len(neighbors) for neighbors in self.adjacency_list.values()), default=0)
    
    @property
    def min_degree(self) -> int:
        """Grado monimo del grafo"""
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
- **GreedyDSATUR**: Construccion voraz por grado de saturacion (colores distintos en vecinos) [Brelaz1979]
- **GreedyLF**: Largest First - ordena por grado decreciente y asigna colores [Welsh1967]
- **GreedySL**: Smallest Last - ordena por grado creciente recursivamente [Matula1972]
- **RandomSequential**: Asignacion secuencial aleatoria de colores [Johnson1974]
- **RLF**: Recursive Largest First - coloracion recursiva por subconjuntos independientes [Leighton1979]

#### Mejora Local
- **KempeChain**: Intercambio de colores mediante cadenas de Kempe [Kempe1879]
- **TabuCol**: Bosqueda local con memoria tabo [Hertz1987]
- **OneVertexMove**: Cambia color de un vertice conflictivo al mejor color disponible [Galinier1999]
- **SwapColors**: Intercambia dos colores en toda la solucion [Fleurent1996]

#### Perturbacion
- **RandomRecolor**: Recolorea aleatoriamente k vertices [Chiarandini2005]
- **PartialDestroy**: Destruye coloracion de subgrafo y reconstruye [Malaguti2008]
- **ColorClassMerge**: Fusiona dos clases de color y repara [Avanthay2003]

#### Intensificacion
- **Intensify**: Reduce numero de colores y repara violaciones [Galinier1999]
- **GreedyImprovement**: Mejora local exhaustiva cambiando colores [Hertz1987]

#### Reparacion
- **RepairConflicts**: Elimina conflictos cambiando colores de vertices conflictivos [Johnson1991]
- **BacktrackRepair**: Reparacion con backtracking limitado [Brelaz1979]

## Solution-Representation

### Estructura de Datos

**Representacion en memoria**:
```python
# Vector de colores de longitud n (numero de vertices)
c = [c_1, c_2, ..., c_n]
# donde c_i   {1, 2, ..., k}
# c_i = color asignado al vertice i
```

**Ejemplo**:
```
Grafo: n=5 vertices, aristas={(0,1), (0,2), (1,2), (2,3), (3,4)}
Solucion: c = [1, 2, 3, 1, 2]
Interpretacion:
  - vertice 0: color 1
  - vertice 1: color 2
  - vertice 2: color 3
  - vertice 3: color 1
  - vertice 4: color 2
numero de colores: k = 3
Conflictos: 0 (solucion factible)
```

### Implementacion de Clases (PENDIENTE)

**Archivo**: `core/solution.py`

```python
from dataclasses import dataclass
import numpy as np
from typing import Optional

@dataclass
class ColoringSolution:
    """
    Representacion de una solucion para Graph Coloring Problem
    
    Atributos:
        assignment: np.ndarray
            Vector de asignacion de colores [0, 1, 2, 1, ...]
            ondice = vertice, valor = color asignado (0-indexed)
        problem: GraphColoringProblem
            Referencia al problema
        value: Optional[int]
            Cache del numero de colores (k)
    """
    
    assignment: np.ndarray
    problem: 'GraphColoringProblem'
    value: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones tras inicializacion"""
        # Validar que assignment tiene longitud n
        assert len(self.assignment) == self.problem.vertices
        
        # Validar que todos los colores son volidos (0 <= c < n)
        assert np.all(self.assignment >= 0)
        assert np.all(self.assignment < self.problem.vertices)
    
    @property
    def num_colors(self) -> int:
        """Retorna numero de colores utilizados"""
        return int(np.max(self.assignment)) + 1
    
    @property
    def num_conflicts(self) -> int:
        """Retorna numero de conflictos (aristas con vertices del mismo color)"""
        conflicts = 0
        for u, v in self.problem.edges:
            if self.assignment[u] == self.assignment[v]:
                conflicts += 1
        return conflicts
    
    def is_feasible(self) -> bool:
        """ La solucion es factible? (sin conflictos)"""
        return self.num_conflicts == 0
    
    def copy(self) -> 'ColoringSolution':
        """Crear copia profunda de la solucion"""
        return ColoringSolution(
            assignment=self.assignment.copy(),
            problem=self.problem,
            value=self.value
        )
```

---

**Restricciones duras**:
1. **No adyacencia**: vertices adyacentes deben tener colores diferentes
2. **Conectividad**: Todos los vertices deben estar coloreados

**Parametros del problema**:
- **n**: numero de vertices
- **m**: numero de aristas
- **E**: Conjunto de aristas (pares de vertices)
- ****: Grado moximo del grafo
- ****: numero cromatico (monimo teorico, usualmente desconocido)

## Evaluation-Criteria

### 3.1 Representación Estándar del Problema

Sea:
- $G = (V, E)$ un grafo no dirigido
- $|V| = n$ número de vértices
- $|E| = m$ número de aristas
- $k$ número máximo de colores permitidos
- $c(v) \in \{1, \ldots, k\}$ función de asignación de color a cada vértice

---

### 3.2 Función Fitness Clásica Basada en Conflictos

**Definición canónica** (aceptada por la comunidad GCP-ILS):

$$f(S) = \sum_{(u,v) \in E} I[c(u) = c(v)]$$

Donde:
- $I[\cdot]$ es la función indicadora definida como:
  - $I[\text{condición}] = 1$ si la condición es verdadera
  - $I[\text{condición}] = 0$ en caso contrario

**Interpretación**:
- $f(S)$ contabiliza el **número total de conflictos** en la coloración
- Un conflicto es una arista cuyos vértices extremos tienen el mismo color
- Una solución $S$ es una **coloración válida** si y solo si: $f(S) = 0$

✅ **Esta es la formulación correcta para ILS en GCP** según la literatura canónica (Galinier & Hao, 2006; Porumbel et al., 2010)

---

### 3.3 Fitness Penalizada (Minimización de k)

Cuando se reduce dinámicamente el número de colores $k$:

$$f(S) = \alpha \cdot \text{conflictos}(S) + \beta \cdot k$$

Con:
- $\alpha \gg \beta$ (típicamente $\alpha = 1000, \beta = 1$)
- Penaliza fuertemente soluciones inválidas
- Permite búsqueda en espacio infactible temporal

**Ventajas de este enfoque**:
- ✔️ Búsqueda en espacio inviable permite transiciones suaves entre valores de $k$
- ✔️ Si $\alpha$ es suficientemente grande, $f(S) = 0$ se alcanza antes que $k$ sea minimizado
- ✔️ Proporciona trayectoria de búsqueda más flexible

---

### 3.4 Cálculo Correcto en Iterated Local Search

**Pipeline estándar de ILS para GCP**:

1. **Solución inicial** → Usar operador constructivo (DSATUR, LargestFirst)

2. **Búsqueda local** → Aplicar movimientos:
   - Move: Recolorear un vértice (OneVertexMove, KempeChain)
   - Evaluación incremental de conflictos

3. **Perturbación** → Cambiar colores de subconjunto de vértices:
   - Escala de perturbación controla intensidad
   - Perturbar tanto soluciones mejores como peores

4. **Aceptación** → Criterio de aceptación:
   - Mejor fitness global
   - O criterio probabilístico (simulated annealing, umbrales)

5. **Iterar** → Repetir hasta criterio de parada

**Observación crítica**: 
> ✔️ El fitness $f(S)$ **no cambia** durante ILS, lo que cambia es la **trayectoria** de búsqueda explorada.

---

### Metricas de Calidad

**Métrica principal**: número de colores utilizados ($k$)  
**Criterio de comparación**: Menor es mejor  
**Manejo de infactibilidad**: 
- **Opción 1** (Canónica): Garantizar $f(S) = 0$ siempre → Evaluar solo $k$
- **Opción 2** (Flexible): Usar fitness penalizada $f(S) = \alpha \cdot \text{conflictos} + \beta \cdot k$
- **Opción 3** (Estricta): Penalizar con $\infty$ si $f(S) > 0$

---

### 3.5 Compatibilidad con Datasets DIMACS

**Requisito crítico**: Todo el framework debe ser compatible con los 79 datasets DIMACS del proyecto.

**Conjuntos de datos del proyecto**:

| Familia | Cantidad | Rango de instancias | Tipo |
|---------|----------|-------------------|------|
| **CUL** | 6 | $n \in [5-100]$ | Color University of Leeds |
| **DSJ** | 15 | $n \in [125-500]$ | David S. Johnson |
| **LEI** | 12 | $n \in [11-70]$ | Leighton |
| **MYC** | 6 | $n \in [11-22]$ | Mycielski |
| **REG** | 14 | $n \in [20-430]$ | Regular graphs |
| **SCH** | 2 | $n \in [166-686]$ | School scheduling |
| **SGB** | 24 | $n \in [14-512]$ | Stanford GraphBase |
| **TOTAL** | **79** | $n \in [5-686]$ | Diversos |

**Especificaciones técnicas por familia**:
- **CUL**: Instancias pequeñas, útiles para validación rápida
- **DSJ**: Instancias medianas-grandes, referencia de dificultad
- **LEI**: Instancias pequeñas, casos especiales de coloración
- **MYC**: Instancias muy pequeñas, grafos especiales (Mycielski)
- **REG**: Grafos regulares, estructura simétrica
- **SCH**: Grafos densos, problemas reales de horarios
- **SGB**: Variedad de tamaños y densidades

**Requerimientos de evaluación para estos datasets**:

1. **Formato DIMACS**
   - Entrada: Archivos `.col` en formato DIMACS
   - Salida: Debe generar coloraciones válidas para todos los tamaños
   - Verificación: $f(S) = 0$ para todas las soluciones reportadas

2. **Escalabilidad**
   - Algoritmo debe ser eficiente en $n \in [5, 686]$
   - Búsqueda local incremental (no re-evaluar todo el grafo)
   - Manejo eficiente de memoria para grafos densos

3. **Consistencia de evaluación**
   - Misma función fitness para todas las instancias
   - Misma penalización de conflictos ($\alpha, \beta$) en todos los casos
   - Registrar BKS (Best Known Solution) por familia

4. **Reporting estándar**
   - Reportar: $k$, $f(S)$, gap respecto a BKS
   - Salidas en formato CSV/JSON con timestamp DD-MM-YY_HH-MM-SS
   - Incluir logs de conflictos durante búsqueda

✅ **Validación**: Antes de reportar resultados, verificar que:
- Todos los 79 datasets se resuelven con $f(S) = 0$ (o reportan como infactibles)
- No hay inconsistencias en evaluación entre familias
- BKS conocidos se alcanzan o superan en instancias probadas

---

### 3.6 Gráficas de Output Esperadas en Experimentación GCP-DIMACS

En trabajos de nivel experto, no basta con una tabla de colores. Se espera **evidencia empírica multivista** que capture calidad, estabilidad, convergencia y costo computacional.

#### 1.1 Gráfica Principal: Convergencia de la Función Fitness

**Qué muestra**:
- **Eje X**: Iteraciones / Evaluaciones de fitness
- **Eje Y**: Valor de fitness ($f(S)$ conflictos, penalización, o número de colores $k$)
- **Líneas**: Una curva por corrida o promedio de $N$ corridas ($N \geq 20$)

**Por qué es clave** (Talbi-friendly):
- ✔️ Evidencia comportamiento dinámico de ILS
- ✔️ Permite evaluar velocidad de convergencia
- ✔️ Distingue exploración vs explotación
- ✔️ Esperado por revisores de conferencias Q1

**Pregunta que responde**: ¿La metaheurística mejora rápido? ¿Se estanca? ¿Es robusta?

**Ejemplo esperado**:
```
Fitness vs Iteraciones (DSJC250.5)
f(S) |     ___
     |    /   \___
     |   /       \___
     |  /           \____
     | /                \________
     |/___________________
     +---------+----------+--- iteraciones
     0        500       1000
```

---

#### 1.2 Boxplots de Calidad Final (Robustez Estadística)

**Qué muestra**:
- Distribución del fitness final en $N \in [20, 50]$ corridas independientes
- Mediana, rango intercuartil (IQR), outliers
- Permite análisis estadístico (media, desv. estándar, CV)

**Buenas prácticas**:
- Un boxplot por instancia DIMACS (ej. DSJC250.5, myciel5, LEI500)
- Comparación entre algoritmos (ILS vs GRASP vs SA)
- Normalizar por BKS: gap% = $(k - \text{BKS}) / \text{BKS} \times 100$

**Por qué es obligatorio** (Talbi 1.7):
- ✔️ Análisis estadístico obligatorio en journals
- ✔️ Demuestra reproducibilidad y robustez
- ✔️ Permite comparación justa entre métodos

**Ejemplo esperado**:
```
Calidad Final en 30 corridas (DSJC500.5)
gap (%) |  ○
        |  │
        | ╔╩╗
        | ║ ║
        | ╚═╝
        |  ║
        |  ○
        +-------- DSJC500.5
```

---

#### 1.3 Curvas Tiempo–Calidad (Trade-off Computacional)

**Qué muestra**:
- **Eje X**: Tiempo (segundos)
- **Eje Y**: Mejor fitness alcanzado hasta ese tiempo $t$
- Múltiples curvas para diferentes instancias o algoritmos

**Muy valorado cuando**:
- ✔️ Comparas ILS vs GRASP vs SA en igual tiempo
- ✔️ Analizas escalabilidad en grafos grandes
- ✔️ Muestras si hay "punto óptimo" de parada

**Pregunta que responde**: ¿Vale la pena correr 10s vs 60s?

**Ejemplo esperado**:
```
Fitness vs Tiempo (DSJ instances)
fitness |  DSJC125 ___
        |  DSJC250 _____
        |  DSJC500 ________
        |         /
        |        /
        +--------+-----+----- tiempo(s)
        0        10    60
```

---

#### 1.4 Heatmap / Matriz de Conflictos (Análisis Cualitativo)

**Qué muestra**:
- Matriz $n \times n$ donde elemento $(i,j)$ indica:
  - Coloración final del vértice $i$ y $j$
  - Presencia de conflicto si $(i,j) \in E$ y $c(i) = c(j)$
- Colores: Verde (sin conflicto) → Rojo (conflicto)

**Uso**:
- ✔️ Visualizar estructura residual de conflictos
- ✔️ Mostrar dónde falla el algoritmo
- ✔️ Identificar subgrafos problemáticos

**Util para**:
- Discusión cualitativa en papers
- Diagnosticar patrones de fallo
- No reemplaza métricas cuantitativas

---

#### 1.5 Gráfico de Escalabilidad (Clave para Q1)

**Qué muestra**:
- **Eje X**: Tamaño del problema ($|V|$ o $|E|$ o densidad)
- **Eje Y**: Métrica de costo:
  - Tiempo medio hasta solución válida
  - Iteraciones promedio
  - Gap promedio respecto a BKS

**Esperado para todas las familias DIMACS**:
- CUL (5–100 vértices)
- DSJ (125–500 vértices)
- LEI (11–70 vértices)
- MYC (11–22 vértices)
- REG (20–430 vértices)
- SCH (166–686 vértices)
- SGB (14–512 vértices)

**Clave si apuntas a revistas Q1**:
- ✔️ Demuestra eficiencia computacional
- ✔️ Valida complejidad teórica vs práctica
- ✔️ Permite extrapolación a instancias mayores

**Ejemplo esperado**:
```
Tiempo de Convergencia vs |V|
tiempo(s)|              ╱╱╱ ILS
         |            ╱╱
         |          ╱╱ GRASP
         |        ╱╱ SA
         |      ╱╱
         |    ╱╱
         +---+---+----+---- |V|
         0  100 250  500
```

---

### 3.7 Tabla de Reportes Obligatorios

Para cada experimento se debe generar:

| Reporte | Formato | Contenido |
|---------|---------|----------|
| **Summary** | CSV | Instancia, $k$, Gap%, Tiempo, Factible |
| **Detailed Results** | JSON | Config, mejoras por iteración, timestamps |
| **Statistics** | TXT | Media, mediana, std, min, max de 30 corridas |
| **Convergence Plots** | PNG/PDF | 1.1, 1.2, 1.3, 1.5 |
| **Conflict Heatmap** | PNG | Matriz de conflictos final |
| **Reproducibility** | TXT | Seed, params, hardware specs |

✅ **Integración con workflow**:
- Scripts generan automáticamente en `output/results/`
- Plots se producen al terminar cada experimento
- Logs incluyen datos brutos para análisis posterior

---

## 4. Output y Almacenamiento de Resultados

### 4.1 Estructura de Carpetas

Después de **cada ejecución**, todos los resultados se guardan automáticamente en la carpeta `output/` con **timestamp único** (DD-MM-YY_HH-MM-SS) para evitar sobrescrituras.

```
output/
├── results/
│   ├── all_datasets/              ← Ejecución COMPLETA (todos 79 datasets)
│   │   └── 31-12-25_14-35-42/     ← Timestamp: DD-MM-YY_HH-MM-SS
│   │       ├── summary.csv
│   │       ├── detailed_results.json
│   │       ├── statistics.txt
│   │       ├── convergence_plot.png
│   │       ├── boxplot_robustness.png
│   │       ├── time_quality_tradeoff.png
│   │       ├── scalability_plot.png
│   │       └── conflict_heatmap.png
│   │
│   └── specific_datasets/         ← Ejecución ESPECÍFICA (una familia)
│       ├── CUL/
│       │   └── 31-12-25_14-35-42/
│       ├── DSJ/
│       │   └── 31-12-25_14-35-42/
│       ├── LEI/
│       │   └── 31-12-25_14-35-42/
│       ├── MYC/
│       │   └── 31-12-25_14-35-42/
│       ├── REG/
│       │   └── 31-12-25_14-35-42/
│       ├── SCH/
│       │   └── 31-12-25_14-35-42/
│       └── SGB/
│           └── 31-12-25_14-35-42/
│
├── solutions/                      ← Archivos de solución (.sol)
│   ├── DSJC125_31-12-25_14-35-42.sol
│   ├── myciel3_31-12-25_14-35-42.sol
│   └── ... (una por instancia resuelta)
│
└── logs/                          ← Logs de ejecución detallados
    └── execution_31-12-25_14-35-42.log
```

---

### 4.2 Formato del Timestamp: DD-MM-YY_HH-MM-SS

```
31-12-25_14-35-42
DD MM YY HH MM SS
│  │  │  │  │  └─ SS: Segundo (00-59)
│  │  │  │  └───── MM: Minuto (00-59)
│  │  │  └────── HH: Hora (00-23)
│  │  └──────── YY: Año (25 = 2025)
│  └──────────── MM: Mes (01-12)
└───────────────── DD: Día (01-31)
```

**Ejemplo**: `31-12-25_14-35-42` = 31 diciembre 2025 a las 14:35:42 horas

---

### 4.3 Dos Modos de Ejecución

#### Modo 1: ALL (Todos los 79 datasets)

Ejecuta el framework sobre **todas las instancias DIMACS**.

```bash
python scripts/experiment.py --mode all
```

**Resultado en**: `output/results/all_datasets/31-12-25_14-35-42/`

**Contenido**:
- Tabla con 79 instancias (CUL:6 + DSJ:15 + LEI:12 + MYC:6 + REG:14 + SCH:2 + SGB:24)
- Resultados detallados en JSON
- Reporte formateado en TXT
- Gráficas de convergencia, robustez, escalabilidad
- 79 soluciones individuales en `solutions/`

---

#### Modo 2: SPECIFIC (Una familia específica)

Ejecuta sobre **una familia particular** de datasets.

```bash
python scripts/experiment.py --mode specific --dataset DSJ
```

**Familias disponibles**:
- `CUL` → 6 instancias (Color University of Leeds)
- `DSJ` → 15 instancias (David S. Johnson)
- `LEI` → 12 instancias (Leighton)
- `MYC` → 6 instancias (Mycielski)
- `REG` → 14 instancias (Regular)
- `SCH` → 2 instancias (School)
- `SGB` → 24 instancias (Stanford GraphBase)

**Resultado en**: `output/results/specific_datasets/DSJ/31-12-25_14-35-42/`

**Contenido**: Ídem Modo 1 pero solo para la familia seleccionada.

---

### 4.4 Contenido de Archivos de Salida

#### 📄 summary.csv
Tabla rápida e importable para análisis.

```csv
Instance,Dataset,Vertices,Edges,BKS,Colors,Feasible,Gap,Gap(%),Time(s),Conflicts
DSJC125.col,DSJ,125,736,45,48,True,+3,6.67,12.5,0
myciel3.col,MYC,11,20,4,4,True,0,0.00,0.5,0
CUL_100.col,CUL,100,850,5,7,True,+2,40.00,8.3,0
```

#### 📊 detailed_results.json
Información completa máquina-legible con estructura jerárquica.

```json
{
  "metadata": {
    "execution_id": "31-12-25_14-35-42",
    "mode": "all_datasets",
    "total_instances": 79,
    "total_time": 945.3
  },
  "algorithm_config": {
    "name": "IteratedLocalSearch",
    "max_iterations": 1000,
    "perturbation_strength": 0.15,
    "construction": "DSATUR"
  },
  "results": [
    {
      "instance": "DSJC125.col",
      "family": "DSJ",
      "num_colors": 48,
      "num_conflicts": 0,
      "is_feasible": true,
      "fitness": 48,
      "bks": 45,
      "gap": 3,
      "gap_percent": 6.67,
      "time_seconds": 12.5,
      "convergence_history": [
        {"iteration": 0, "fitness": 52, "num_colors": 52},
        {"iteration": 10, "fitness": 50, "num_colors": 50},
        ...
      ]
    }
  ],
  "statistics": {
    "total_feasible": 79,
    "average_time": 11.96,
    "average_colors": 22.4,
    "average_gap_percent": 1.8
  }
}
```

#### 📋 statistics.txt
Reporte legible para humanos.

```
═══════════════════════════════════════════════════════════════
                   NEW-GCP-ILS-OK - REPORT
═══════════════════════════════════════════════════════════════
Execution ID:       31-12-25_14-35-42
Mode:               all_datasets (79 instances)
Algorithm:          Iterated Local Search
Total Execution:    945.3 seconds

RESUMEN GENERAL:
├─ Total instancias:     79
├─ Factibles (f(S)=0):   79/79 (100.0%)
├─ Tiempo promedio:      11.96 segundos
├─ Colores promedio:     22.4
├─ Gap promedio:         +1.8 colors (+1.35%)

MEJOR INSTANCIA:
├─ Instance:     myciel3.col
├─ Colores:      4 (óptimo)
├─ Gap:          0 colors
├─ Tiempo:       0.5 segundos

PEOR INSTANCIA:
├─ Instance:     DSJC500.5
├─ Colores:      185
├─ Gap:          +5 colors
├─ Tiempo:       145.2 segundos

POR FAMILIA:
├─ CUL:  avg_colors=6.2, avg_time=2.3s, feasible=6/6
├─ DSJ:  avg_colors=45.3, avg_time=18.7s, feasible=15/15
├─ LEI:  avg_colors=8.1, avg_time=1.5s, feasible=12/12
├─ MYC:  avg_colors=4.0, avg_time=0.3s, feasible=6/6
├─ REG:  avg_colors=15.7, avg_time=5.2s, feasible=14/14
├─ SCH:  avg_colors=34.5, avg_time=89.1s, feasible=2/2
├─ SGB:  avg_colors=28.3, avg_time=12.8s, feasible=24/24

═══════════════════════════════════════════════════════════════
```

#### 🔍 Gráficas Generadas Automáticamente

1. **convergence_plot.png** → Fitness vs iteraciones (Sección 3.6.1)
2. **boxplot_robustness.png** → Distribución estadística de 30 corridas (Sección 3.6.2)
3. **time_quality_tradeoff.png** → Tiempo vs calidad (Sección 3.6.3)
4. **conflict_heatmap.png** → Matriz de conflictos residuales (Sección 3.6.4)
5. **scalability_plot.png** → $|V|$ vs tiempo/iteraciones (Sección 3.6.5)

---

### 4.5 Archivos Adicionales

#### 💾 Soluciones (.sol)
```
output/solutions/DSJC125_31-12-25_14-35-42.sol
output/solutions/myciel3_31-12-25_14-35-42.sol
```

**Formato**: Línea por vértice con su color asignado:
```
c 1 0
c 2 1
c 3 0
c 4 2
...
```

**Verificación**: $f(S) = 0$ para todas las soluciones reportadas.

#### 📝 Logs (.log)
```
output/logs/execution_31-12-25_14-35-42.log
```

**Contenido**:
- Timestamp de inicio/fin
- Parámetros de ejecución
- Progreso por instancia
- Mensajes de error o warnings
- Estadísticas de hardware (CPU, memoria)

---

### 4.6 Ciclo Completo: Ejecución → Almacenamiento → Análisis

**Paso 1**: Ejecutar experimentación
```bash
python scripts/experiment.py --mode all
```

**Paso 2**: Se generan automáticamente
```
output/results/all_datasets/31-12-25_14-35-42/
├── summary.csv                    # ← Usar para análisis rápido
├── detailed_results.json          # ← Datos completos
├── statistics.txt                 # ← Leer para reporte
├── convergence_plot.png           # ← Incluir en paper
├── boxplot_robustness.png         # ← Estadística Q1
├── time_quality_tradeoff.png      # ← Comparación algoritmos
├── scalability_plot.png           # ← Complejidad
└── conflict_heatmap.png           # ← Análisis cualitativo
```

**Paso 3**: Análisis y reporte
```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar resultados
df = pd.read_csv("output/results/all_datasets/31-12-25_14-35-42/summary.csv")

# Análisis por familia
by_family = df.groupby('Dataset')[['Colors', 'Gap(%)', 'Time(s)']].mean()
print(by_family)

# Visualizar
df.plot(x='Vertices', y='Gap(%)', kind='scatter')
plt.savefig('custom_analysis.png')
```

---

### 4.7 Checklist de Validación Post-Ejecución

Después de cada experimentación confirma que:

- ✅ Carpeta `output/results/` existe
- ✅ Subcarpeta con timestamp correcto (DD-MM-YY_HH-MM-SS)
- ✅ 3 archivos (CSV, JSON, TXT) presentes
- ✅ 5 gráficas PNG generadas (convergencia, boxplot, time-quality, heatmap, scalability)
- ✅ Archivos .sol en `solutions/` (uno por instancia resuelta)
- ✅ Log en `logs/` con información completa
- ✅ **Sin sobrescritura**: cada ejecución = carpeta nueva
- ✅ Todas las instancias reportan $f(S) = 0$ (factibles)
- ✅ BKS conocidos se alcanzan o se superan en instancias validadas
- ✅ Estadísticas coherentes (media, mediana, desv. estándar)

---

### 4.8 Integración con Publicación Académica

Los archivos generados están diseñados para:

| Archivo | Uso en Paper |
|---------|-----------|
| **summary.csv** | Tabla de resultados principal |
| **statistics.txt** | Sección "Results" (valores numéricos) |
| **convergence_plot.png** | Figura 1 (comportamiento dinámico) |
| **boxplot_robustness.png** | Figura 2 (análisis estadístico) |
| **time_quality_tradeoff.png** | Figura 3 (comparación con otros métodos) |
| **scalability_plot.png** | Figura 4 (complejidad computacional) |
| **conflict_heatmap.png** | Figura 5 (análisis cualitativo, opcional) |
| **detailed_results.json** | Datos suplementarios (appendix) |

✅ **Reproducibilidad**: Todos los datos están versionados con timestamp y seed registrado en logs.

### Implementacion de Evaluador (PENDIENTE)

**Archivo**: `core/evaluation.py`

```python
from typing import Dict, Any, Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution

class ColoringEvaluator:
    """
    Evaluador de soluciones para Graph Coloring Problem
    
    Calcula multiples Metricas de calidad:
    - fitness: numero de colores + penalizacion por conflictos
    - num_colors: numero de colores utilizados
    - conflicts: numero de conflictos (aristas monocromoticas)
    - feasible:  es una solucion volida?
    - gap: diferencia respecto a mejor conocido
    """
    
    @staticmethod
    def evaluate(solution: ColoringSolution, 
                 problem: GraphColoringProblem) -> Dict[str, Any]:
        """
        Evaluar una solucion
        
        Parametros:
        -----------
        solution : ColoringSolution
            Solucion a evaluar
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        Dict con claves:
            'num_colors' : int
                numero de colores utilizados (k)
            'conflicts' : int
                numero de conflictos (aristas monocromoticas)
            'feasible' : bool
                 Respeta todas las restricciones?
            'fitness' : float
                Valor de funcion objetivo con penalizacion
            'gap' : Optional[float]
                (optimal - num_colors) / optimal si se conoce optimo
        
        Ejemplo:
        --------
        >>> problem = GraphColoringProblem(vertices=47, edges=[...])
        >>> solution = GreedyDSATUR.construct(problem)
        >>> metrics = ColoringEvaluator.evaluate(solution, problem)
        >>> print(f"Colores: {metrics['num_colors']}, Conflictos: {metrics['conflicts']}")
        """
        
        # Calcular numero de colores
        num_colors = solution.num_colors
        
        # Calcular conflictos
        conflicts = solution.num_conflicts
        
        # Evaluar factibilidad
        feasible = conflicts == 0
        
        # Calcular fitness con penalizacion
        CONFLICT_PENALTY = 100
        fitness = num_colors + conflicts * CONFLICT_PENALTY
        
        # Calcular gap respecto a optimo
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
        Evaluar multiples soluciones
        
        Parametros:
        -----------
        solutions : list[ColoringSolution]
            Lista de soluciones
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        list[Dict[str, Any]]
            Lista de Metricas (una por solucion)
        
        Ejemplo:
        --------
        >>> solutions = [algorithm.run() for _ in range(10)]
        >>> metrics_list = ColoringEvaluator.batch_evaluate(solutions, problem)
        """
        return [ColoringEvaluator.evaluate(sol, problem) for sol in solutions]
```

---

## Domain-Operators---

# PARTE 2: METAHEURISTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Iterated Local Search (ILS)  
**Tipo**: METAHEURISTICA de trayectoria con perturbacion e intensificacion  
**Referencia**: [Lourenco2003, Stützle2006]

## Descripcion del Motodo

Iterated Local Search (ILS) es una METAHEURISTICA que itera entre tres fases principales:
1. **Bosqueda local**: Intensificacion hasta optimo local
2. **Perturbacion**: Escape del optimo local mediante cambios significativos
3. **Criterio de aceptacion**: Decide si acepta la nueva solucion

**Ventajas para GAA en GCP**:
- Efectivo para problemas de coloracion
- Balance entre intensificacion (bosqueda local) y diversificacion (perturbacion)
- Estructura modular que se adapta bien a AST
- Resultados competitivos en benchmarks de GCP

## Configuration

**Parametros principales**:

```yaml
max_iteraciones: 500
intensidad_perturbacion: 0.20  # Porcentaje de vertices a recolorear
tipo_busqueda_local: "best_improvement"  # First vs Best
criterio_aceptacion: "better_or_equal"  # Always, Better, Better-or-Equal
max_iteraciones_sin_mejora: 50
```

**Justificacion**:
- 500 iteraciones: Balance entre calidad y tiempo
- 20% perturbacion: Suficiente para escape, no tan drostico
- Best improvement: Mayor calidad de optimos locales
- Better-or-equal: Permite diversificacion moderada

## Search-Strategy

### Operadores de Bosqueda sobre AST

**Mutacion de Nodo Funcion**:
- Reemplazar nodo de bosqueda local por otro tipo
- Ejemplo: `LocalSearch(KempeChain)`   `LocalSearch(OneVertexMove)`
- Probabilidad: 0.25

**Mutacion de Terminal**:
- Cambiar operador de construccion o mejora
- Ejemplo: `GreedyDSATUR`   `GreedyLF`
- Probabilidad: 0.50

**Mutacion de Parometro**:
- Modificar intensidad de perturbacion
- Ejemplo: perturb_ratio: 0.20   0.25
- Perturbacion:  15%
- Probabilidad: 0.25

### Estructura Topica de ILS

```python
def ILS():
    s = GenerarSolucionInicial()  # Construccion
    s = BusquedaLocal(s)           # Intensificacion
    s_best = s
    
    for iter in range(max_iterations):
        s_pert = Perturbar(s)      # Escape
        s_new = BusquedaLocal(s_pert)  # Intensificacion
        
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
- [x] numero de iteraciones: 500
- [x] Iteraciones sin mejora: 50
- [ ] Tiempo lomite: N/A
- [ ] optimo conocido alcanzado: Opcional

**Presupuesto por evaluacion de AST**:
- Iteraciones ILS por instancia: 500
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~45 segundos

## AST-Specific Considerations

**Validacion de AST**:
- Validar gramotica despuos de mutacion: So
- Reparacion automotica de AST involidos: So
- Profundidad moxima del orbol: 10

**Inicializacion**:
- Motodo: Grow (crecimiento aleatorio con profundidad variable)
- Profundidad inicial: 4-6
- Poblacion inicial de AST: 1 (ILS es single-solution)

**Operadores obligatorios en AST**:
- Al menos un constructor (e.g., GreedyDSATUR)
- Al menos una bosqueda local
- Al menos una perturbacion

---

# PARTE 3: DATASETS

## Ubicacion de Datasets

```
projects/NEW-GCP-ILS-OK/datasets/
    training/          # Instancias para optimizar AST
        [Archivos .col o .txt]
    validation/        # Instancias para ajustar Parametros ILS
        [Archivos .col o .txt]
    test/              # Instancias para evaluacion final
        [Archivos .col o .txt]
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

###  Descripcion General

El proyecto incluye **79 instancias DIMACS** organizadas en **8 familias** con caracterosticas diversas:
- Instancias pequeoas (myciel: 10-23 vertices)
- Instancias medianas (LEI, REG, MYC: 100-450 vertices)
- Instancias grandes (DSJ, CUL, SGB: 300-1000+ vertices)
- Mejores soluciones conocidas documentadas en `BKS.json`

**Estructura de datos**:
```
datasets/
    BKS.json                    # Best Known Solutions para todas las instancias
    CUL/                        # Culberson - Quasi-random coloring
        flat300_20_0.col        # 300 vertices, 21375 aristas, BKS=20
        flat300_26_0.col        # 300 vertices, 21633 aristas, BKS=26
        flat300_28_0.col        # 300 vertices, 21695 aristas, BKS=28
        flat1000_50_0.col       # 1000 vertices, 245000 aristas, BKS=50
        flat1000_60_0.col       # 1000 vertices, 249500 aristas, BKS=60
        flat1000_76_0.col       # 1000 vertices, 249500 aristas, BKS=76
    DSJ/                        # Descartes-Stein-Johnson random graphs
        DSJC125.1.col           # 125 vertices, densidad 0.1
        DSJC125.5.col           # 125 vertices, densidad 0.5
        DSJC125.9.col           # 125 vertices, densidad 0.9
        DSJC250.1.col           # 250 vertices, densidad 0.1
        DSJC250.5.col           # 250 vertices, densidad 0.5
        DSJC250.9.col           # 250 vertices, densidad 0.9
        DSJC500.1.col           # 500 vertices, densidad 0.1
        DSJC500.5.col           # 500 vertices, densidad 0.5
        DSJC500.9.col           # 500 vertices, densidad 0.9
        DSJC1000.1.col          # 1000 vertices, densidad 0.1
        DSJC1000.5.col          # 1000 vertices, densidad 0.5
        DSJC1000.9.col          # 1000 vertices, densidad 0.9
        DSJR500.1.col           # 500 vertices (variante)
        DSJR500.1c.col          # 500 vertices (variante)
        DSJR500.5.col           # 500 vertices, densidad 0.5
    LEI/                        # Lewis - Exam timetabling graphs
        le450_5a.col            # 450 vertices, 5714 aristas
        le450_5b.col            # 450 vertices, 5734 aristas
        le450_5c.col            # 450 vertices, 5786 aristas
        le450_5d.col            # 450 vertices, 5822 aristas
        le450_15a.col           # 450 vertices, 16680 aristas
        le450_15b.col           # 450 vertices, 16872 aristas
        le450_15c.col           # 450 vertices, 16962 aristas
        le450_15d.col           # 450 vertices, 16968 aristas
        le450_25a.col           # 450 vertices, 25119 aristas
        le450_25b.col           # 450 vertices, 25185 aristas
        le450_25c.col           # 450 vertices, 25282 aristas
        le450_25d.col           # 450 vertices, 25363 aristas
    MYC/                        # Mycielski construction - Planar graphs
        myciel2.col             # 5 vertices, 5 aristas (trivial)
        myciel3.col             # 11 vertices, 20 aristas
        myciel4.col             # 23 vertices, 71 aristas
        myciel5.col             # 47 vertices, 236 aristas
        myciel6.col             # 95 vertices, 755 aristas
        myciel7.col             # 191 vertices, 2360 aristas
    REG/                        # Regular graphs & Certification instances
        fpsol2.i.1.col          # 496 vertices (scheduling)
        fpsol2.i.2.col          # 451 vertices (scheduling)
        fpsol2.i.3.col          # 429 vertices (scheduling)
        inithx.i.1.col          # 864 vertices (inithx)
        inithx.i.2.col          # 645 vertices (inithx)
        inithx.i.3.col          # 621 vertices (inithx)
        mulsol.i.1.col          # 197 vertices (mulsol)
        mulsol.i.2.col          # 188 vertices (mulsol)
        mulsol.i.3.col          # 188 vertices (mulsol)
        mulsol.i.4.col          # 185 vertices (mulsol)
        mulsol.i.5.col          # 186 vertices (mulsol)
        zeroin.i.1.col          # 126 vertices (zeroin)
        zeroin.i.2.col          # 157 vertices (zeroin)
        zeroin.i.3.col          # 157 vertices (zeroin)
    SCH/                        # School timetabling
        school1.col             # 385 vertices, 19095 aristas
        school1_nsh.col         # 352 vertices, 14612 aristas
    SGB/                        # Stanford GraphBase - Structured graphs (24 instancias, en subcarpetas)
        Book_graphs/            # Grafos de libros (5 archivos .col)
            book104.col, book105.col, book106.col, book107.col, book108.col
        Game_graph/             # Grafo de juegos (1 archivo .col)
            games120.col
        Miles_graphs/           # Grafos de distancias (5 archivos .col)
            miles1000.col, miles1500.col, miles250.col, miles500.col, miles750.col
        Queen_graphs/           # Grafos de movimientos de reina (13 archivos .col)
            queen10_10.col, queen11_11.col, queen12_12.col, queen13_13.col, queen14_14.col,
            queen15_15.col, queen16_16.col, queen5_5.col, queen6_6.col, queen7_7.col,
            queen8_12.col, queen8_8.col, queen9_9.col
    documentation/
        loader.py               # Utilidad para cargar instancias
        metadata.json           # Informacion de todas las instancias
```

###  Estadosticas de Instancias

| Familia | Cantidad | Rango de vertices | Rango de Aristas | Dificultad | Aplicacion |
|---------|----------|-------------------|------------------|-----------|-----------|
| **MYC** | 6 | 5-191 | 5-2360 |   Trivial-Focil | Matemotica pura (construccion de Mycielski) |
| **DSJ** | 15 | 125-1000 | 2500-450000 |     Media-Difocil | Grafos aleatorios G(n,p) con densidades variables |
| **CUL** | 6 | 300-1000 | 21375-249500 |      Muy Difocil | Grafos cuasi-aleatorios |
| **LEI** | 12 | 450 | 5714-25363 |     Difocil | Programacion de exomenes (timetabling) |
| **REG** | 14 | 126-864 | 4344-32340 |     Difocil | Instancias de certificacion y scheduling |
| **SCH** | 2 | 352-385 | 14612-19095 |     Difocil | Programacion de horarios escolares |
| **SGB** | 24 | Varoan | Varoan |    Media | Grafos estructurados (Book, Game, Miles, Queen) |
| **TOTAL** | **79** | **5-1000** | **5-450000** | **Diversa** | **Benchmark DIMACS completo** |

###  Recomendaciones por Fase

**Training (Desarrollo)**:
-   Usar: MYC (trivial para validacion)
-   Usar: DSJC125.* (pequeoas, Rapidas)
-   Usar: myciel3-5 (10-47 vertices)
-   Tiempo esperado por instancia: < 1 segundo

**Validation (Ajuste de Parametros)**:
-   Usar: DSJC250.*, le450_5*, zeroin.*
-   Usar: myciel6-7 (95-191 vertices)
-   Tiempo esperado por instancia: 1-5 segundos

**Test (Evaluacion final)**:
-   Usar: DSJC500.*, DSJC1000.*, CUL, LEI, REG
-   Usar: fpsol2.i.*, inithx.i.*
-   Usar: Todas las familias (100% coverage)
-   Tiempo esperado por instancia: 5-60 segundos (segon tamaoo)

###  Detalle de Estructura de Carpetas

**  IMPORTANTE: SGB tiene subcarpetas**

```
datasets/
 
    BKS.json                             Archivo de mejores soluciones conocidas
 
    CUL/                                 6 archivos .col directamente
        flat300_20_0.col
        flat300_26_0.col
        flat300_28_0.col
        flat1000_50_0.col
        flat1000_60_0.col
        flat1000_76_0.col
 
    DSJ/                                 15 archivos .col directamente
        DSJC125.1.col
        DSJC125.5.col
        DSJC125.9.col
        ... (12 mos)
        DSJR500.5.col
 
    LEI/                                 12 archivos .col directamente
        le450_5a.col
        le450_5b.col
        ... (10 mos)
        le450_25d.col
 
    MYC/                                 6 archivos .col directamente
        myciel2.col
        myciel3.col
        myciel4.col
        myciel5.col
        myciel6.col
        myciel7.col
 
    REG/                                 14 archivos .col directamente
        fpsol2.i.1.col
        fpsol2.i.2.col
        fpsol2.i.3.col
        inithx.i.1.col
        ... (10 mos)
        zeroin.i.3.col
 
    SCH/                                 2 archivos .col directamente
        school1.col
        school1_nsh.col
 
    SGB/                                   TIENE 4 SUBCARPETAS (24 total)
     
        Book_graphs/                     5 archivos .col en esta subcarpeta
            book104.col
            book105.col
            book106.col
            book107.col
            book108.col
     
        Game_graph/                      1 archivo .col en esta subcarpeta
            games120.col
     
        Miles_graphs/                    5 archivos .col en esta subcarpeta
            miles250.col
            miles500.col
            miles750.col
            miles1000.col
            miles1500.col
     
        Queen_graphs/                    13 archivos .col en esta subcarpeta
            queen5_5.col
            queen6_6.col
            queen7_7.col
            queen8_8.col
            queen8_12.col
            queen9_9.col
            queen10_10.col
            queen11_11.col
            queen12_12.col
            queen13_13.col
            queen14_14.col
            queen15_15.col
            queen16_16.col
 
    documentation/
        loader.py                        Clase InstanceLoader
        metadata.json                    Metadatos de instancias
```

###   Notas Importantes sobre la Estructura

**1. Acceso a archivos SGB**:
   - Los 24 archivos de SGB eston **distribuidos en 4 subcarpetas**
   - El `InstanceLoader` debe buscar recursivamente en subcarpetas
   - Rutas: `datasets/SGB/Book_graphs/`, `datasets/SGB/Queen_graphs/`, etc.

**2. Todas las otras familias (CUL, DSJ, LEI, MYC, REG, SCH)**:
   - Tienen sus archivos `.col` **directamente en la carpeta principal**
   - No tienen subcarpetas
   - Acceso directo: `datasets/CUL/`, `datasets/MYC/`, etc.

**3. BKS.json**:
   - Archivo onico con mejores soluciones conocidas
   - Incluye referencias para **todos los 79 archivos**
   - Ubicado en la raoz: `datasets/BKS.json`


###  Como Cargar Instancias

```python
from datasets.documentation.loader import InstanceLoader

# Inicializar loader
loader = InstanceLoader('datasets/')

# Cargar todas las instancias
all_instances = loader.get_all()

# Filtrar por familia
dsjc_instances = loader.get_by_source('DSJ')
myciel_instances = loader.get_by_source('MYC')

# Filtrar por dificultad
easy_instances = loader.get_by_difficulty('easy')

# Filtrar por tamaoo
small_instances = loader.get_by_size(min_nodes=0, max_nodes=100)
large_instances = loader.get_by_size(min_nodes=500)

# Obtener instancia especofica
myciel5 = loader.get_instance('myciel5')

# Obtener ruta del archivo .col
file_path = loader.get_file_path('DSJC500.5')
```

###  Formato de Instancia

**Archivo `.col` (formato DIMACS)**:
```
c Este es un comentario
p edge 5 7
e 1 2
e 1 3
e 2 4
e 3 4
e 3 5
e 4 5
e 5 1
```

**Estructura en memoria**:
```python
@dataclass
class GraphColoringProblem:
    vertices: int                  # n = 5
    edges: List[Tuple[int, int]]  # [(1,2), (1,3), (2,4), ...]
    adjacency_list: Dict[int, List[int]]  # {1: [2,3,5], 2: [1,4], ...}
    colors_known: Optional[int]    # (G) si se conoce (del BKS.json)
```

###  Informacion Adicional

**BKS.json** contiene para cada instancia:
- `nodes`: numero de vertices
- `edges`: numero de aristas
- `bks`: mejor solucion conocida (colores usados)
- `optimal`:  es optima certificada?
- `guaranteed`:  garantizado que es optimo?
- `open`:  es un problema abierto?

Ejemplo:
```json
"myciel5": {
  "nodes": 47,
  "edges": 236,
  "bks": 5,
  "optimal": true,
  "guaranteed": true,
  "open": false
}
```

---

# PARTE 4: GENERACIoN Y EXPERIMENTACIoN

## Algoritmo Generado

El sistema GAA generaro algoritmos ILS representados como AST combinando:
- **Funciones**: `Seq`, `If`, `While`, `ApplyUntilNoImprove`, `LocalSearch`
- **Terminales**: Los 15 operadores identificados en Domain-Operators

**Ejemplo de AST para ILS**:
```json
{
  "type": "Seq",
  "body": [
    {"type": "Call", "name": "GreedyDSATUR"},
    {"type": "ApplyUntilNoImprove", 
     "stmt": {"type": "Call", "name": "KempeChain"},
     "stop": {"type": "Stagnation", "iters": 10}
    },
    {"type": "While", "budget": {"kind": "IterBudget", "value": 500},
     "body": {
       "type": "Seq",
       "body": [
         {"type": "Call", "name": "RandomRecolor", "args": {"ratio": 0.2}},
         {"type": "ApplyUntilNoImprove",
          "stmt": {"type": "Call", "name": "OneVertexMove"},
          "stop": {"type": "Stagnation", "iters": 5}
         },
         {"type": "If", "cond": {"type": "Improves"},
          "then": {"type": "Call", "name": "Intensify"},
          "else": {"type": "Call", "name": "PartialDestroy"}
         }
       ]
     }
    }
  ]
}
```

## Plan Experimental

**Variables independientes**:
- Algoritmos ILS generados por GAA (variaciones de AST)
- CONFIGURACIONes de perturbacion (ratio)

**Variables dependientes**:
- numero de colores obtenido (k)
- Tiempo de ejecucion
- Gap respecto a mejor conocido (best known)

**Instancias**:
- Diversas estructuras de grafos (aleatorios, bipartitos, planares, etc.)

**Replicas**: 30 ejecuciones por CONFIGURACION (ILS es estocastico)

**Analisis estadistico**:
- Test de Friedman para comparacion multiple
- Post-hoc: Nemenyi test
- Nivel de significancia:  = 0.05

---

##  Referencias Bibliograficas

- [Brelaz1979] Brelaz, D. (1979). New methods to color the vertices of a graph. Communications of the ACM, 22(4), 251-256.
- [Welsh1967] Welsh, D. J., & Powell, M. B. (1967). An upper bound for the chromatic number of a graph. Computer Journal, 10(1), 85-86.
- [Hertz1987] Hertz, A., & de Werra, D. (1987). Using tabu search techniques for graph coloring. Computing, 39(4), 345-351.
- [Lourenco2003] Lourenço, H. R., Martin, O. C., & Stützle, T. (2003). Iterated local search. Handbook of metaheuristics, 320-353.
- [Galinier1999] Galinier, P., & Hao, J. K. (1999). Hybrid evolutionary algorithms for graph coloring. Journal of Combinatorial Optimization, 3(4), 379-397.

---

##   Estado del Proyecto

### Documentacion
- [x] Problema definido (GCP)
- [x] Modelo Matematico formalizado
- [x] Operadores del dominio identificados (15 terminales)
- [x] METAHEURISTICA seleccionada (ILS)
- [x] Parametros de ILS configurados
- [x] Datasets agregados (79 instancias DIMACS clasificadas)
- [x] Datasets descriptos por familia y dificultad

### Implementacion (Pendiente - Fases 1-6)

**  FASE 1: CORE** (Critico - Requiere 2-3 horas)
- [ ] `core/problem.py` - GraphColoringProblem con @dataclass
  - Estructura especificada en este documento
  - Validaciones, propiedades, Metodos helper
- [ ] `core/solution.py` - ColoringSolution con @dataclass
  - Vector de asignacion, propiedades de colores/conflictos
  - Metodos is_feasible(), copy()
- [ ] `core/evaluation.py` - ColoringEvaluator
  - Metricas: num_colors, conflicts, feasible, fitness, gap
  - Batch evaluation para multiples soluciones
- [ ] `core/__init__.py` - Exports

**  FASE 2: OPERADORES** (Importante - Requiere 3-4 horas)
- [ ] `operators/constructive.py` - GreedyDSATUR, GreedyLF, RandomSequential
- [ ] `operators/improvement.py` - KempeChain, OneVertexMove, TabuCol
- [ ] `operators/perturbation.py` - RandomRecolor, PartialDestroy
- [ ] `operators/repair.py` - RepairConflicts
- [ ] `operators/__init__.py` - Exports

**  FASE 3: METAHEURISTICA** (Importante - Requiere 2-3 horas)
- [ ] `metaheuristic/ils_core.py` - IteratedLocalSearch con inyeccion
- [ ] `metaheuristic/perturbation_schedules.py` - Esquemas
- [ ] `metaheuristic/__init__.py` - Exports

**  FASE 4: TESTING** (Importante - Requiere 2 horas)
- [ ] `tests/test_core.py` - 15+ tests para Core
- [ ] `tests/test_operators.py` - Tests para operadores
- [ ] `tests/test_ils.py` - Tests para ILS

**  FASE 5: SCRIPTS** (Importante - Requiere 2 horas)
- [ ] `scripts/test_quick.py` - Validacion Rapida (10s)
- [ ] `scripts/demo_complete.py` - Demo funcional (30s)
- [ ] `scripts/demo_experimentation.py` - Experimentos (5 min)

**  FASE 6: CONFIGURACION** (Importante - Requiere 1 hora)
- [ ] `config/config.yaml` - Parametros centralizados
- [ ] `docs/QUICKSTART.md` - Guia de inicio
- [ ] `requirements.txt` - Dependencias

### Recursos de Referencia
-  Ver `RECOMENDACIONES_PROYECTOS/` en KBP-SA para:
  - `PATRONES_DE_CODIGO.md` - Como implementar @dataclass, Strategy, inyeccion
  - `CHECKLIST_PRACTICO.md` - Guia paso a paso
  - `ARQUITECTURA_VISUAL_Y_REPLICACION.md` - Como replicar estructura




