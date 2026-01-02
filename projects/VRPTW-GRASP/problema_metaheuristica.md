---
gaa_metadata:
  version: 1.0.0
  project_name: "VRPTW con GRASP"
  problem: "Vehicle Routing Problem with Time Windows"
  metaheuristic: "GRASP"
  status: "active"
  created: "2025-11-17"
---

# Proyecto: VRPTW con GRASP

## 🎯 Información del Proyecto

**Problema**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Metaheurística**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Objetivo**: Generar algoritmos automáticamente mediante GAA para resolver instancias de ruteo de vehículos con ventanas de tiempo

---

# PARTE 1: DEFINICIó“N DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Tipo**: Minimización  
**Categoría**: Combinatorial Optimization - NP-Hard

## Descripción Informal

El problema de ruteo de vehículos con ventanas de tiempo (VRPTW) consiste en diseñar rutas óptimas para una flota de vehículos que deben atender un conjunto de clientes desde un depósito central. Cada cliente tiene:
- Una demanda de producto
- Una ventana de tiempo [a_i, b_i] durante la cual debe ser visitado
- Un tiempo de servicio s_i

Los vehículos tienen capacidad limitada y deben respetar las ventanas de tiempo de los clientes.

**Aplicaciones**:
- Logística de distribución urbana
- Ruteo de vehículos de transporte escolar
- Servicios de mensajería y paquetería
- Distribución de alimentos y bebidas
- Servicios de mantenimiento programado

## Mathematical-Model

### Función Objetivo

```math
\text{Minimizar: } Z = \sum_{k=1}^{K} \sum_{i=0}^{n} \sum_{j=0}^{n} c_{ij} x_{ijk}
```

Donde:
- c_{ij} = costo (distancia o tiempo) de viajar del nodo i al nodo j
- x_{ijk} = 1 si el vehículo k viaja directamente de i a j, 0 en otro caso

### Restricciones

**1. Asignación de clientes**:
```math
\sum_{k=1}^{K} \sum_{j=1}^{n} x_{ijk} = 1, \quad \forall i \in \{1, \ldots, n\}
```

**2. Conservación de flujo**:
```math
\sum_{i=0}^{n} x_{ijk} - \sum_{j=0}^{n} x_{jik} = 0, \quad \forall k, \forall i
```

**3. Capacidad del vehículo**:
```math
\sum_{i=1}^{n} q_i \sum_{j=0}^{n} x_{ijk} \leq Q, \quad \forall k
```

**4. Ventanas de tiempo**:
```math
a_i \leq w_{ik} \leq b_i, \quad \forall i, k
```

```math
w_{ik} + s_i + t_{ij} \leq w_{jk} + M(1 - x_{ijk}), \quad \forall i,j,k
```

### Variables de Decisión

- **x_{ijk}**: Variable binaria (ruta del vehículo k entre i y j)
- **w_{ik}**: Tiempo de inicio de servicio del vehículo k en el cliente i
- **n**: Número de clientes
- **K**: Número de vehículos disponibles
- **Q**: Capacidad de cada vehículo
- **q_i**: Demanda del cliente i
- **[a_i, b_i]**: Ventana de tiempo del cliente i
- **s_i**: Tiempo de servicio del cliente i
- **t_{ij}**: Tiempo de viaje entre i y j

## Domain-Operators

### Terminales Identificados

#### Constructivos
- **SavingsHeuristic**: Heurística de ahorros de Clarke-Wright [Clarke1964]
- **NearestNeighbor**: Vecino más cercano con consideración de tiempo [Solomon1987]
- **InsertionI1**: Inserción secuencial minimizando costo adicional [Solomon1987]
- **TimeOrientedNN**: Vecino más cercano priorizando urgencia temporal [Potvin1996]
- **RegretInsertion**: Inserción por arrepentimiento (diferencia entre mejor y segunda mejor posición) [Ropke2006]
- **RandomizedInsertion**: Inserción con componente aleatoria (GRASP-style) [Kontoravdis1995]

#### Mejora Local - Intra-ruta
- **TwoOpt**: Mejora 2-opt dentro de una ruta [Lin1965]
- **OrOpt**: Reubicación de secuencias de 1, 2 o 3 clientes [Or1976]
- **ThreeOpt**: Mejora 3-opt (más intensiva) [Lin1965]
- **Relocate**: Mover un cliente a otra posición en la misma ruta [Savelsbergh1992]

#### Mejora Local - Inter-ruta
- **CrossExchange**: Intercambio de segmentos entre rutas [Taillard1997]
- **TwoOptStar**: 2-opt* entre dos rutas diferentes [Potvin1996]
- **SwapCustomers**: Intercambio de clientes entre rutas [Brøysy2005]
- **Relocate Inter**: Mover cliente de una ruta a otra [Pisinger2007]

#### Perturbación
- **EjectionChain**: Cadenas de eyección de clientes [Glover1996]
- **RuinRecreate**: Destruye parcialmente rutas y reconstruye [Schrimpf2000]
- **RandomRemoval**: Remoción aleatoria de k clientes y reinserción [Shaw1998]
- **RouteElimination**: Elimina una ruta completa y redistribuye clientes [Nagata2010]

#### Reparación
- **RepairCapacity**: Repara violaciones de capacidad removiendo clientes [Brøysy2005]
- **RepairTimeWindows**: Ajusta rutas para cumplir ventanas de tiempo [Potvin1996]
- **GreedyRepair**: Reconstrucción voraz tras destrucción [Pisinger2007]

## Solution-Representation

**Estructura de datos**:
```python
# Lista de rutas, cada ruta es una secuencia de clientes
routes = [
    [0, c1, c3, c5, 0],  # Ruta 1: depó³sito â†’ c1 â†’ c3 â†’ c5 â†’ depó³sito
    [0, c2, c4, 0],       # Ruta 2: depó³sito â†’ c2 â†’ c4 â†’ depó³sito
    [0, c6, c7, c8, 0]    # Ruta 3: depó³sito â†’ c6 â†’ c7 â†’ c8 â†’ depó³sito
]
```

**Ejemplo**:
```
Instancia: 8 clientes, 3 vehó­culos, Q=100

Solució³n:
Route 1: 0 â†’ 1(q=30) â†’ 3(q=25) â†’ 5(q=20) â†’ 0  [Carga total: 75]
Route 2: 0 â†’ 2(q=40) â†’ 4(q=35) â†’ 0             [Carga total: 75]
Route 3: 0 â†’ 6(q=15) â†’ 7(q=20) â†’ 8(q=10) â†’ 0  [Carga total: 45]

Costo total: 245.6 unidades
Violaciones: 0 (factible)
```

## Constraints

**Restricciones duras**:
1. **Capacidad**: La demanda acumulada en cada ruta no debe exceder Q
2. **Ventanas de tiempo**: Cada cliente debe ser visitado dentro de su ventana [a_i, b_i]
3. **Cobertura**: Todos los clientes deben ser visitados exactamente una vez
4. **Depó³sito**: Todas las rutas inician y terminan en el depó³sito (nodo 0)

**Restricciones blandas** (pueden penalizarse):
- Minimizar nóºmero de vehó­culos utilizados
- Balancear carga entre vehó­culos

**Paró¡metros del problema**:
- **n**: Nóºmero de clientes
- **K**: Nóºmero de vehó­culos disponibles
- **Q**: Capacidad de vehó­culos
- **q_i**: Demanda del cliente i
- **[a_i, b_i]**: Ventana de tiempo del cliente i
- **s_i**: Tiempo de servicio del cliente i
- **c_{ij}**: Matriz de distancias/tiempos
- **(x_i, y_i)**: Coordenadas geogró¡ficas del cliente i

## Evaluation-Criteria

**Mó©trica principal**: Distancia total recorrida (o costo total)  
**Mó©tricas secundarias**:
- Nóºmero de vehó­culos utilizados
- Violaciones de ventanas de tiempo
- Violaciones de capacidad

**Criterio de comparació³n**: Menor es mejor  

**Manejo de infactibilidad**:
```python
def evaluate(solution):
    total_distance = sum_route_distances(solution)
    capacity_violations = sum_capacity_excess(solution)
    time_violations = sum_time_window_violations(solution)
    
    # Penalizaciones
    penalty = 1000 * capacity_violations + 1000 * time_violations
    
    return total_distance + penalty
```

**Mó©trica jeró¡rquica** (lexicogró¡fica):
1. Minimizar violaciones (factibilidad)
2. Minimizar nóºmero de vehó­culos
3. Minimizar distancia total

---

# PARTE 2: METAHEURóSTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Tipo**: Metaheuró­stica constructiva con bóºsqueda local  
**Referencia**: [Feo1995, Resende2009]

## Descripció³n del Mó©todo

GRASP es una metaheuró­stica iterativa de dos fases:
1. **Fase Constructiva**: Construcció³n voraz aleatoria (greedy randomized)
   - En cada paso, selecciona aleatoriamente de entre las mejores opciones (RCL - Restricted Candidate List)
   - Balancea voracidad y aleatoriedad

2. **Fase de Bóºsqueda Local**: Mejora la solució³n construida
   - Aplica operadores de mejora hasta alcanzar ó³ptimo local

**Ventajas para GAA en VRPTW**:
- Combina construcció³n y mejora (dos pilares del diseó±o de heuró­sticas)
- Paró¡metro Î± controla balance entre voracidad y aleatoriedad
- Efectivo para problemas de ruteo
- Genera soluciones diversas en cada iteració³n

## Configuration

**Paró¡metros principales**:

```yaml
max_iteraciones: 100
alpha: 0.15                    # Paró¡metro RCL: 0=voraz, 1=aleatorio
tamaó±o_rcl: null               # Alternativa: usar tamaó±o fijo de RCL
tipo_mejora: "VND"             # Variable Neighborhood Descent
max_sin_mejora: 20             # Criterio de parada adicional
```

**Paró¡metros del RCL (Restricted Candidate List)**:
```python
# Opció³n 1: Por valor (alpha-based)
threshold = c_min + alpha * (c_max - c_min)
RCL = {i : c_i <= threshold}

# Opció³n 2: Por tamaó±o (size-based)
RCL = {top k candidatos segóºn costo}
```

**Justificació³n**:
- 100 iteraciones: Diversidad suficiente
- Î±=0.15: Balance entre voracidad (0) y aleatoriedad (1)
- VND: Variable Neighborhood Descent para bóºsqueda local exhaustiva

## Search-Strategy

### Operadores de Bóºsqueda sobre AST

**Mutació³n de Nodo Funció³n**:
- Cambiar tipo de bucle o estructura de control
- Ejemplo: `ChooseBestOf(5, Construct)` â†’ `For(10, Construct)`
- Probabilidad: 0.20

**Mutació³n de Terminal**:
- Cambiar heuró­stica constructiva
- Ejemplo: `SavingsHeuristic` â†’ `RegretInsertion`
- Cambiar operador de mejora local
- Ejemplo: `TwoOpt` â†’ `OrOpt`
- Probabilidad: 0.60

**Mutació³n de Paró¡metro**:
- Modificar Î± (paró¡metro RCL)
- Modificar k en operadores paramó©tricos
- Perturbació³n: Â±10%
- Probabilidad: 0.20

### Estructura Tó­pica de GRASP

```python
def GRASP():
    s_best = None
    f_best = infinity
    
    for iter in range(max_iterations):
        # Fase Constructiva (Greedy Randomized)
        s = GreedyRandomizedConstruction(alpha)
        
        # Fase de Bóºsqueda Local
        s = LocalSearch(s)
        
        # Actualizar mejor solució³n
        if f(s) < f_best:
            s_best = s
            f_best = f(s)
    
    return s_best
```

### Construcció³n Voraz Aleatoria

```python
def GreedyRandomizedConstruction(alpha):
    solution = initialize_empty_routes()
    unrouted = all_customers.copy()
    
    while unrouted:
        # Evaluar costos de inserció³n
        costs = evaluate_insertion_costs(unrouted, solution)
        c_min, c_max = min(costs), max(costs)
        
        # Construir RCL
        threshold = c_min + alpha * (c_max - c_min)
        RCL = [i for i in unrouted if costs[i] <= threshold]
        
        # Seleccionar aleatoriamente de RCL
        selected = random.choice(RCL)
        
        # Insertar en mejor posició³n
        insert_customer(selected, solution)
        unrouted.remove(selected)
    
    return solution
```

### Bóºsqueda Local (VND)

```python
def VariableNeighborhoodDescent(solution):
    neighborhoods = [TwoOpt, OrOpt, Relocate, SwapCustomers]
    k = 0
    
    while k < len(neighborhoods):
        s_new = neighborhoods[k](solution)
        
        if f(s_new) < f(solution):
            solution = s_new
            k = 0  # Reiniciar desde primer vecindario
        else:
            k += 1  # Pasar al siguiente vecindario
    
    return solution
```

## Presupuesto Computacional

**Criterio de parada**:
- [x] Nóºmero de iteraciones GRASP: 100
- [x] Iteraciones sin mejora: 20
- [ ] Tiempo ló­mite: N/A
- [ ] ó“ptimo conocido alcanzado: Opcional

**Presupuesto por evaluació³n de AST**:
- Iteraciones GRASP por instancia: 100
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~60 segundos (VRPTW es mó¡s costoso)

## AST-Specific Considerations

**Validació³n de AST**:
- Validar gramó¡tica despuó©s de mutació³n: Só­
- Reparació³n automó¡tica de AST invó¡lidos: Só­
- Profundidad mó¡xima del ó¡rbol: 10

**Inicializació³n**:
- Mó©todo: Ramped Half-and-Half (combinació³n de Full y Grow)
- Profundidad inicial: 4-7
- Població³n inicial de AST: 1 (GRASP es single-solution por iteració³n)

**Operadores obligatorios en AST para GRASP**:
- Al menos un constructor randomizado
- Al menos dos operadores de mejora local (para VND)
- Reparació³n de restricciones

---

# PARTE 3: DATASETS

## Ubicació³n de Datasets

```
projects/VRPTW-GRASP/datasets/
â”œâ”€â”€ training/          # Instancias para optimizar AST
â”‚   â””â”€â”€ [Archivos .txt]
â”œâ”€â”€ validation/        # Instancias para ajustar paró¡metros
â”‚   â””â”€â”€ [Archivos .txt]
â””â”€â”€ test/              # Instancias para evaluació³n final
    â””â”€â”€ [Archivos .txt]
```

## Formato de Archivo de Instancia

**Formato Solomon** (estó¡ndar VRPTW):
```
VEHICLE
NUMBER     CAPACITY
  K          Q

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
    0       x0        y0          0         0          T            0
    1       x1        y1         q1        a1         b1           s1
    2       x2        y2         q2        a2         b2           s2
    ...
```

**Ejemplo** (Solomon R101 - extracto):
```
VEHICLE
NUMBER     CAPACITY
  25         200

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME

    0      35       35          0          0       230           0   
    1      41       49         10        161       171          10   
    2      35       17          7         50        60          10   
    3      55       45         13        116       126          10   
```

## Datasets Recomendados

**Benchmarks cló¡sicos de VRPTW**:

1. **Solomon Instances** (1987):
   - Tipo R: Clientes distribuidos aleatoriamente
   - Tipo C: Clientes en clusters
   - Tipo RC: Mezcla de aleatorio y clusters
   - Tamaó±os: R101, R102, ..., RC108 (25-100 clientes)

2. **Gehring & Homberger** (1999):
   - Extensió³n de Solomon para instancias grandes
   - Tamaó±os: 200, 400, 600, 800, 1000 clientes

3. **Homberger & Gehring** (2005):
   - Instancias con diferentes horizontes temporales

**Fuentes**:
- Solomon: http://web.cba.neu.edu/~msolomon/problems.htm
- Gehring & Homberger: http://www.sintef.no/projectweb/top/vrptw/

**Sugerencias para el proyecto**:
- **Training**: 5 instancias Solomon pequeó±as (R101, C101, RC101, R201, C201)
- **Validation**: 3 instancias medianas
- **Test**: 5-8 instancias variadas

---

# PARTE 4: GENERACIó“N Y EXPERIMENTACIó“N

## Algoritmo Generado

El sistema GAA generaró¡ algoritmos GRASP representados como AST combinando:
- **Funciones**: `Seq`, `For`, `ChooseBestOf`, `ApplyUntilNoImprove`, `LocalSearch`
- **Terminales**: Los 22 operadores identificados en Domain-Operators

**Ejemplo de AST para GRASP**:
```json
{
  "type": "ChooseBestOf",
  "n": 100,
  "stmt": {
    "type": "Seq",
    "body": [
      {
        "type": "Call",
        "name": "RandomizedInsertion",
        "args": {"alpha": 0.15}
      },
      {
        "type": "Seq",
        "body": [
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "TwoOpt"},
            "stop": {"type": "Stagnation", "iters": 5}
          },
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "OrOpt"},
            "stop": {"type": "Stagnation", "iters": 5}
          },
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "SwapCustomers"},
            "stop": {"type": "Stagnation", "iters": 3}
          }
        ]
      }
    ]
  }
}
```

## Plan Experimental

### Visió³n General

El plan experimental sigue el enfoque probado en KBP-SA con **DOS scripts de experimentació³n independientes**:

1. **`demo_experimentation_quick.py`**: Validació³n ró¡pida (1 familia Solomon)
2. **`demo_experimentation_full.py`**: Anó¡lisis exhaustivo (todas las familias Solomon)

**Diferencia con KBP-SA**:
- KBP-SA usaba "both" (2 grupos: low-dimensional + large-scale en 1 script)
- VRPTW-GRASP usa "quick" vs "full" (1 familia vs 3 familias) en 2 scripts separados
- Razó³n: 3 familias Solomon requieren decisió³n expló­cita de quó© ejecutar

**Generació³n de Algoritmos**: 3 algoritmos GRASP automó¡ticos **UNA SOLA VEZ** (seed=42), reutilizados en ambos modos

---

### Dimensiones del Experimento

#### Datasets Disponibles en Carpeta

Estructura actual de `datasets/`:
```
datasets/
â”œâ”€â”€ R1/          â† Familia Random 1 (R101-R112: 12 instancias)
â”œâ”€â”€ R2/          â† Familia Random 2 (R201-R211: 11 instancias)
â”œâ”€â”€ C1/          â† Familia Clusters 1 (C101-C109: 9 instancias)
â”œâ”€â”€ C2/          â† Familia Clusters 2 (C201-C208: 8 instancias)
â”œâ”€â”€ RC1/         â† Familia Mixed 1 (RC101-RC108: 8 instancias)
â”œâ”€â”€ RC2/         â† Familia Mixed 2 (RC201-RC208: 8 instancias)
â””â”€â”€ documentation/
```

**Caracteró­sticas de familias Solomon**:

| Familia | Tipo | Caracteró­stica | Tamaó±o | Aplicació³n |
|---------|------|---|--------|-----------|
| **R (Random)** | Aleatorio | Clientes distribuidos al azar | 25-100 clientes | Casos sin estructura |
| **C (Clusters)** | Agrupados | Clientes en clusters espaciales | 25-100 clientes | Distribució³n urbana |
| **RC (Mixed)** | Mixto | Mezcla de aleatorio + clusters | 25-100 clientes | Casos realistas |

**Total disponible**: 56 instancias Solomon (12+11 R, 9+8 C, 8+8 RC)

#### Modo QUICK (Test Ró¡pido)

**Propó³sito**: Validació³n ró¡pida del sistema GAA  
**Ubicació³n**: `scripts/demo_experimentation_quick.py`

```
Instancias: 1 familia Solomon (ejemplo: R1)
Algoritmos: 3 (GAA_Algorithm_1, GAA_Algorithm_2, GAA_Algorithm_3)
Repeticiones: 1 por combinació³n
Total experimentos: 12 ó— 3 ó— 1 = 36 (si usa R1 completa)
                   o 10 ó— 3 ó— 1 = 30 (si usa subset de 10)

Tiempo estimado: ~5-10 minutos
Validació³n: Funcionalidad de sistema, estructura de datos
```

**Familia recomendada para QUICK**: R1 (representativa, 12 instancias)

#### Modo FULL (Evaluació³n Completa)

**Propó³sito**: Anó¡lisis exhaustivo de desempeó±o en diferentes caracteró­sticas  
**Ubicació³n**: `scripts/demo_experimentation_full.py`

```
Instancias: TODAS las familias disponibles (56 instancias)
Algoritmos: 3 (mismos que en test quick, seed=42 reutilizado)
Repeticiones: 1 por combinació³n
Total experimentos: 56 ó— 3 ó— 1 = 168

Desglose por familia:
  - R1: 12 instancias ó— 3 = 36 experimentos
  - R2: 11 instancias ó— 3 = 33 experimentos
  - C1:  9 instancias ó— 3 = 27 experimentos
  - C2:  8 instancias ó— 3 = 24 experimentos
  - RC1: 8 instancias ó— 3 = 24 experimentos
  - RC2: 8 instancias ó— 3 = 24 experimentos
  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  TOTAL: 56 ó— 3 = 168 experimentos

Tiempo estimado: ~40-60 minutos
Validació³n: Robustez, especializació³n por familia, escalabilidad
```

#### Matriz de Ejecució³n Comparativa

```
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘                    QUICK vs FULL                           â•‘
â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£
â•‘ QUICK (1 script):                                          â•‘
â•‘  Familia R1 (12) ó— 3 algoritmos ó— 1 rep = 36 experimentosâ•‘
â•‘  Tiempo: ~5-10 minutos                                     â•‘
â•‘  Propó³sito: Validació³n ró¡pida                              â•‘
â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£
â•‘ FULL (1 script):                                           â•‘
â•‘  R1 (12) + R2 (11) + C1 (9) + C2 (8) + RC1 (8) + RC2 (8) â•‘
â•‘  = 56 instancias ó— 3 algoritmos ó— 1 rep = 168 experimentos
â•‘  Tiempo: ~40-60 minutos                                    â•‘
â•‘  Propó³sito: Anó¡lisis exhaustivo                            â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

#### Uso de Scripts

```bash
# Test ró¡pido (validació³n): 36 experimentos, ~5-10 min
python scripts/demo_experimentation_quick.py

# Test full (anó¡lisis completo): 168 experimentos, ~40-60 min
python scripts/demo_experimentation_full.py

# Custom (especificar familias)
python scripts/demo_experimentation_quick.py --families R1
python scripts/demo_experimentation_full.py --families R1 C1 RC1
```

**Diferencia clave con KBP-SA**:
- KBP-SA: 1 script `demo_experimentation_both.py` ejecutaba 2 grupos secuencialmente (30+63=93 experimentos)
- VRPTW-GRASP: 2 scripts independientes (`quick.py` vs `full.py`) ejecutan 1 o 3 familias segóºn necesidad

---

### Generació³n de Algoritmos (UNA SOLA VEZ)

**Fase 0**: Antes de cualquier experimento, generar 3 algoritmos GRASP automó¡ticamente

```python
# Pseudocó³digo
algorithms = []
for i in range(3):
    ast = AlgorithmGenerator.generate_with_validation(
        grammar=vrptw_grasp_grammar,
        min_depth=2,
        max_depth=3,
        seed=42
    )
    algorithms.append({
        'name': f'GAA_Algorithm_{i+1}',
        'ast': ast,
        'pseudocode': ast.to_pseudocode()
    })

# Resultado: 3 algoritmos reutilizados en TODOS los experimentos
```

**Duració³n**: ~0.00s (negligible)

---

### Criterio de Uso de Operadores

Los 3 algoritmos generados DEBEN cumplir con restricciones de composició³n de operadores:

#### Restricciones Obligatorias

**1. Constructor Randomizado (Obligatorio)**:
Cada algoritmo DEBE incluir exactamente 1 constructor de entre:
- `RandomizedInsertion(alpha)` âœ… Preferido (probabiló­stico, controla balance)
- `TimeOrientedNN`
- `RegretInsertion`
- `NearestNeighbor` (alternativa bó¡sica)

**Justificació³n**: GRASP requiere componente aleatoria en construcció³n

**2. Operadores de Mejora Local (Mó­nimo 2)**:
Cada algoritmo DEBE incluir al menos 2 operadores de los siguientes:

**Intra-ruta** (mejora dentro de una ruta):
- `TwoOpt` âœ… Muy efectivo para VRPTW
- `OrOpt` âœ… Ró¡pido, óºtil como complemento
- `ThreeOpt` (intensivo, usar con cuidado)
- `Relocate`

**Inter-ruta** (mejora entre rutas):
- `CrossExchange` âœ… Transferencias entre rutas
- `TwoOptStar`
- `SwapCustomers`
- `RelocateInter`

**Recomendado**: Combinar 1 intra-ruta + 1 inter-ruta para balance exploració³n/explotació³n

**Justificació³n**: VND (Variable Neighborhood Descent) efectivo en VRPTW requiere móºltiples vecindarios

**3. Criterio de Iteració³n (Obligatorio)**:
Cada algoritmo DEBE usar exactamente 1 estrategia de control:
- `ApplyUntilNoImprove(max_stagnation=k)` âœ… Estó¡ndar
- `ChooseBestOf(n_iterations)` âœ… Alternativa: n iteraciones GRASP
- `For(fixed_iterations)`

**Justificació³n**: Control expló­cito de presupuesto computacional

**4. Reparació³n (Opcional pero Recomendada)**:
Si se detectan restricciones violadas, incluir:
- `RepairTimeWindows` âœ… Cró­tica para VRPTW
- `RepairCapacity` âœ… Cró­tica para VRPTW
- `GreedyRepair`

**Justificació³n**: VRPTW tiene restricciones duras; necesaria factibilidad

#### Restricciones Prohibidas

**NO permitidos** (pueden romper el modelo VRPTW):
- âŒ Perturbaciones como `RuinRecreate` en bucle principal (solo si se implementa correctamente)
- âŒ `RouteElimination` sin reparació³n posterior
- âŒ Constructores sin aleatoriedad (GreedyByRatio puro sin GRASP)

#### Ejemplos de Algoritmos Vó¡lidos

**Algoritmo 1 (VóLIDO)**:
```
â”œâ”€ ChooseBestOf(100)    # 100 iteraciones GRASP
â”‚  â”œâ”€ RandomizedInsertion(alpha=0.15)  # Construcció³n
â”‚  â””â”€ Seq
â”‚     â”œâ”€ ApplyUntilNoImprove(TwoOpt, max_stagnation=5)
â”‚     â”œâ”€ ApplyUntilNoImprove(CrossExchange, max_stagnation=3)
â”‚     â””â”€ RepairTimeWindows
```
âœ… Cumple: constructor randomizado + 2 operadores + reparació³n

**Algoritmo 2 (INVóLIDO)**:
```
â”œâ”€ For(50)
â”‚  â”œâ”€ GreedyByValue    # âŒ SIN aleatoriedad (no GRASP)
â”‚  â””â”€ TwoOpt           # âŒ Solo 1 operador (necesita 2+)
```
âŒ Falla: no tiene constructor randomizado ni tiene suficientes operadores

**Algoritmo 3 (VóLIDO)**:
```
â”œâ”€ ChooseBestOf(100)
â”‚  â”œâ”€ RegretInsertion(random_seed)  # Construcció³n randomizada
â”‚  â””â”€ ApplyUntilNoImprove(
â”‚     stmt: Seq
â”‚       â”œâ”€ OrOpt      # Intra-ruta
â”‚       â”œâ”€ SwapCustomers  # Inter-ruta
â”‚       â””â”€ RepairCapacity
â”‚     max_stagnation: 4)
```
âœ… Cumple: constructor randomizado + 2 operadores (intra+inter) + reparació³n

---

### Variables Independientes

- **Algoritmo GRASP** (3 variantes generadas automó¡ticamente)
- **Familia de instancias** (R, C, RC) - Modo Full
- **Paró¡metro Î±** (controlado por el AST generado, tó­picamente 0.10-0.20)
- **Operadores de mejora** (combinaciones variables segóºn AST)

### Variables Dependientes

**Mó©tricas de Calidad**:
- **Distancia total recorrida** (objetivo principal)
- **Nóºmero de vehó­culos utilizados** (objetivo secundario)
- **Gap al BKS** (Best Known Solution): `(solució³n - BKS) / BKS ó— 100%`

**Mó©tricas de Rendimiento**:
- **Tiempo de ejecució³n** (segundos)
- **Iteraciones GRASP completadas**
- **Evaluaciones de soluciones**

**Mó©tricas de Validez**:
- **Violaciones de capacidad** (debe ser 0)
- **Violaciones de ventanas de tiempo** (debe ser 0)
- **Factibilidad** (100% de soluciones deben ser factibles)

---

### Comparació³n y Anó¡lisis

**Comparativas realizadas**:

1. **Entre algoritmos GAA**: Cuó¡l de los 3 generados es mejor
   - Mó©trica principal: Gap promedio al BKS
   - Mó©trica secundaria: Tiempo promedio

2. **Por familia de instancias** (Modo Full):
   - Â¿Quó© algoritmo es mejor para instancias aleatorias (R)?
   - Â¿Quó© algoritmo es mejor para instancias agrupadas (C)?
   - Â¿Quó© algoritmo es mejor para instancias mixtas (RC)?

3. **Por tamaó±o de instancia**:
   - Pequeó±as (25-50 clientes)
   - Medianas (50-75 clientes)
   - Grandes (75-100 clientes)

---

### Anó¡lisis Estadó­stico

**Tests realizados**:

1. **Descriptivas por algoritmo**:
   - Media de gap al BKS
   - Desviació³n estó¡ndar
   - Mó­nimo, mó¡ximo
   - Mediana

2. **Comparació³n móºltiple** (Kruskal-Wallis):
   - Compara los 3 algoritmos simultó¡neamente
   - No paramó©trico (no asume distribució³n normal)
   - Resultado: p-value < 0.05 indica diferencias significativas

3. **Comparació³n pareada** (Test de Wilcoxon):
   - Entre los dos mejores algoritmos
   - Determina si la diferencia es estadó­sticamente significativa

4. **Tamaó±o del efecto** (Cohen's d):
   - Magnitud de la diferencia entre algoritmos
   - d < 0.2: efecto pequeó±o
   - 0.2 â‰¤ d < 0.5: efecto mediano
   - d â‰¥ 0.5: efecto grande

5. **Trade-off calidad-tiempo**:
   - Correlació³n entre gap promedio y tiempo promedio
   - Identificar algoritmos Pareto-ó³ptimos

**Nivel de significancia**: Î± = 0.05

---

### Presupuesto Computacional

**Por ejecució³n GRASP**:
- Max iteraciones: 100 (configurable vó­a AST)
- Max sin mejora: 20 iteraciones
- Timeout: 60 segundos por instancia
- Evaluaciones mó¡ximas: ~5000-10000 (depende de operadores usados)

**Presupuesto total**:
- **Test Ró¡pido** (R family, 1 rep): ~5-10 minutos
- **Full** (todas familias, 1 rep): ~20-30 minutos

---

### Generació³n de Reportes y Visualizaciones

**Para CADA modo de ejecució³n se crean directorios separados**:

#### Salida QUICK Mode

```
output/
â”œâ”€â”€ vrptw_experiments_QUICK_YYYYMMDD_HHMMSS/
â”‚   â””â”€â”€ experiment_quick_YYYYMMDD_HHMMSS.json        (36 resultados: 12 instancias ó— 3 alg)
â”‚
â””â”€â”€ plots_vrptw_QUICK_YYYYMMDD_HHMMSS/
    â”œâ”€â”€ README.md                                    (Resumen Quick test)
    â”œâ”€â”€ time_tracking.md                             (Tiempos: 5-10 min)
    â”œâ”€â”€ best_algorithm_ast.png                       (Mejor algoritmo de los 3)
    â”œâ”€â”€ gap_comparison_boxplot.png                   (Comparació³n gap entre 3 algoritmos)
    â”œâ”€â”€ gap_comparison_bars.png                      (Gap promedio Â± desv est)
    â”œâ”€â”€ quality_vs_time_scatter.png                  (Trade-off calidad-tiempo)
    â”œâ”€â”€ convergence_curves.png                       (Evolució³n convergencia)
    â”œâ”€â”€ vehicles_used_comparison.png                 (Nóºmero vehó­culos por algoritmo)
    â”œâ”€â”€ routes_detailed_R101.png                     (Visualizació³n de rutas)
    â”œâ”€â”€ routes_detailed_R102.png
    â””â”€â”€ ... (12 gró¡ficas, 1 por cada instancia R1)
```

**Total archivos QUICK**: ~20 archivos (8 gró¡ficas estadó­sticas + 12 gró¡ficas rutas)

---

#### Salida FULL Mode

```
output/
â”œâ”€â”€ vrptw_experiments_FULL_YYYYMMDD_HHMMSS/
â”‚   â””â”€â”€ experiment_full_YYYYMMDD_HHMMSS.json         (168 resultados: 56 instancias ó— 3 alg)
â”‚
â””â”€â”€ plots_vrptw_FULL_YYYYMMDD_HHMMSS/
    â”œâ”€â”€ README.md                                    (Resumen completo Full test)
    â”œâ”€â”€ time_tracking.md                             (Tiempos: 40-60 min)
    â”œâ”€â”€ best_algorithm_ast.png                       (Mejor algoritmo global)
    â”‚
    â”œâ”€â”€ â”€â”€â”€ GRóFICAS ESTADóSTICAS AGREGADAS â”€â”€â”€
    â”œâ”€â”€ gap_comparison_boxplot.png                   (Gap: 3 algoritmos)
    â”œâ”€â”€ gap_comparison_bars.png                      (Gap promedio)
    â”œâ”€â”€ quality_vs_time_scatter.png                  (Trade-off global)
    â”œâ”€â”€ convergence_curves.png                       (Convergencia agregada)
    â”œâ”€â”€ vehicles_used_comparison.png                 (Vehó­culos)
    â”‚
    â”œâ”€â”€ â”€â”€â”€ ANóLISIS POR FAMILIA (SOLO FULL) â”€â”€â”€
    â”œâ”€â”€ performance_by_family.png                    (R vs C vs RC: comparació³n)
    â”œâ”€â”€ performance_by_size.png                      (Pequeó±o/Mediano/Grande)
    â”œâ”€â”€ best_algorithm_per_family.png                (Â¿Quó© algoritmo domina en cada familia?)
    â”‚
    â”œâ”€â”€ â”€â”€â”€ DETALLE POR SUBFAMILIA â”€â”€â”€
    â”œâ”€â”€ family_R_statistics.md                       (Stats de R1 + R2)
    â”œâ”€â”€ family_C_statistics.md                       (Stats de C1 + C2)
    â”œâ”€â”€ family_RC_statistics.md                      (Stats de RC1 + RC2)
    â”‚
    â”œâ”€â”€ â”€â”€â”€ GRóFICAS DE RUTAS POR INSTANCIA â”€â”€â”€
    â”œâ”€â”€ routes_detailed_R101.png
    â”œâ”€â”€ routes_detailed_R102.png
    â”œâ”€â”€ ... (12 para R1)
    â”œâ”€â”€ routes_detailed_R201.png
    â”œâ”€â”€ ... (11 para R2)
    â”œâ”€â”€ routes_detailed_C101.png
    â”œâ”€â”€ ... (9 para C1)
    â”œâ”€â”€ routes_detailed_C201.png
    â”œâ”€â”€ ... (8 para C2)
    â”œâ”€â”€ routes_detailed_RC101.png
    â”œâ”€â”€ ... (8 para RC1)
    â”œâ”€â”€ routes_detailed_RC201.png
    â”œâ”€â”€ ... (8 para RC2)
    â”‚
    â””â”€â”€ statistics_summary.md                        (Tabla resumen todas instancias)
```

**Total archivos FULL**: ~70 archivos (11 gró¡ficas + 3 estadó­sticas + 56 gró¡ficas rutas)

---

#### Comparació³n: QUICK vs FULL Outputs

| Aspecto | QUICK | FULL |
|--------|-------|------|
| **JSON resultados** | 1 archivo | 1 archivo |
| **Gró¡ficas estadó­sticas** | 8 | 11 |
| **Gró¡ficas rutas** | 12 (R1) | 56 (R1+R2+C1+C2+RC1+RC2) |
| **Anó¡lisis por familia** | NO | Só (3 archivos .md) |
| **Archivos totales** | ~20 | ~70 |
| **Tamaó±o carpeta** | ~5-10 MB | ~20-30 MB |

---

### Algoritmos Generados (Compartidos)

Independientemente de mode (quick/full), se generan **3 algoritmos UNA SOLA VEZ**:

```
algorithms/
â”œâ”€â”€ GAA_Algorithm_1.json                (AST)
â”œâ”€â”€ GAA_Algorithm_2.json                (AST)
â”œâ”€â”€ GAA_Algorithm_3.json                (AST)
â””â”€â”€ algorithms_pseudocode.md            (Pseudocó³digo de los 3)
```

**Seed fijo**: 42  
**Generació³n**: Ocurre al inicio de QUICK (si es primera ejecució³n)  
**Reutilizació³n**: FULL usa los mismos 3 algoritmos

---

### Script Principal de Experimentació³n

**IMPORTANTE**: Existen DOS scripts independientes segóºn modo de ejecució³n:

#### Script 1: QUICK Test (Validació³n Ró¡pida)

**Archivo**: `scripts/demo_experimentation_quick.py`  
**Scope**: Una familia Solomon (tó­picamente R1)  
**Experimentos**: 36 (si usa R1 con 12 instancias)  
**Tiempo**: ~5-10 minutos

**Uso**:
```bash
# Ejecució³n por defecto (usa R1)
python scripts/demo_experimentation_quick.py

# Con especificació³n expló­cita de familia
python scripts/demo_experimentation_quick.py --family R1

# Con subset de instancias
python scripts/demo_experimentation_quick.py --family R1 --limit 10
```

**Salida**:
```
output/vrptw_experiments_QUICK_YYYYMMDD_HHMMSS/
â”œâ”€â”€ experiment_quick_*.json
â””â”€â”€ plots_vrptw_QUICK_YYYYMMDD_HHMMSS/
    â”œâ”€â”€ gap_comparison_*.png
    â”œâ”€â”€ routes_detailed_*.png (solo instancias de R1)
    â””â”€â”€ README.md
```

**Propó³sito**: 
- Validació³n ró¡pida del sistema GAA
- Verificació³n de estructura de datos
- Debugging antes de experimento full
- Estimació³n de tiempos

---

#### Script 2: FULL Test (Evaluació³n Exhaustiva)

**Archivo**: `scripts/demo_experimentation_full.py`  
**Scope**: TODAS las familias Solomon disponibles (R1, R2, C1, C2, RC1, RC2)  
**Experimentos**: 168 (56 instancias ó— 3 algoritmos)  
**Tiempo**: ~40-60 minutos

**Uso**:
```bash
# Ejecució³n completa (todas las familias)
python scripts/demo_experimentation_full.py

# Con especificació³n de familias (subset)
python scripts/demo_experimentation_full.py --families R1 C1 RC1

# Con control de verbosidad
python scripts/demo_experimentation_full.py --verbose --save-solutions
```

**Salida**:
```
output/vrptw_experiments_FULL_YYYYMMDD_HHMMSS/
â”œâ”€â”€ experiment_full_*.json
â””â”€â”€ plots_vrptw_FULL_YYYYMMDD_HHMMSS/
    â”œâ”€â”€ gap_comparison_*.png
    â”œâ”€â”€ performance_by_family.png
    â”œâ”€â”€ performance_by_size.png
    â”œâ”€â”€ convergence_curves.png
    â”œâ”€â”€ routes_detailed_*.png (1 por cada instancia)
    â”œâ”€â”€ statistics_summary.md
    â””â”€â”€ README.md
```

**Propó³sito**:
- Anó¡lisis exhaustivo de robustez
- Identificar especializació³n por familia
- Evaluació³n de escalabilidad
- Comparació³n inter-familias
- Paper-ready results

---

#### Paró¡metros Configurables (Ambos Scripts)

```python
CONFIG_QUICK = {
    'mode': 'quick',
    'families': ['R1'],              # Familia a usar
    'num_algorithms': 3,              # Algoritmos a generar
    'max_iterations_grasp': 100,     # Iteraciones GRASP por algoritmo
    'timeout_per_instance': 60.0,    # Timeout en segundos
    'random_seed': 42,                # Reproducibilidad
    'save_solutions': False,          # Guardar soluciones encontradas
    'generate_visualizations': True,  # Generar gró¡ficas
}

CONFIG_FULL = {
    'mode': 'full',
    'families': ['R1', 'R2', 'C1', 'C2', 'RC1', 'RC2'],  # TODAS
    'num_algorithms': 3,
    'max_iterations_grasp': 100,
    'timeout_per_instance': 60.0,
    'random_seed': 42,
    'save_solutions': False,
    'generate_visualizations': True,
    'aggregate_by_family': True,      # Anó¡lisis por familia
    'compare_families': True,         # Comparació³n familias
}
```

---

#### Flujo de Ejecució³n Recomendado

```
PRIMERA VEZ (Setup):
1. python scripts/demo_experimentation_quick.py
   â†’ Validació³n (5-10 min)
   â†’ Si OK: continuar con Full
   â†’ Si ERROR: debuggear

ANóLISIS COMPLETO:
2. python scripts/demo_experimentation_full.py
   â†’ Experimentació³n exhaustiva (40-60 min)
   â†’ Genera reportes estadó­sticos
   â†’ Crea gró¡ficas comparativas por familia
```

---

### Diferencia Conceptual: KBP-SA vs VRPTW-GRASP

| Aspecto | KBP-SA | VRPTW-GRASP |
|---------|--------|------------|
| **Arquitectura** | 1 script "both" | 2 scripts "quick" + "full" |
| **Grupos/Familias** | 2 (low-dim, large-scale) | 3 (R, C, RC) |
| **Instancias grupo 1** | 10 | 12 (R1) |
| **Instancias grupo 2** | 21 | 11 (R2) + 9 (C1) + 8 (C2) + 8 (RC1) + 8 (RC2) = 44 |
| **Total instancias QUICK** | N/A (siempre "both") | 12 (1 familia) |
| **Total instancias FULL** | 31 | 56 (6 subfamilias) |
| **Experimentos QUICK** | N/A | 36 |
| **Experimentos FULL** | 93 | 168 |
| **Algoritmos** | 3 (generados 1 vez) | 3 (generados 1 vez, seed=42) |
| **Ejecució³n** | Secuencial fijo (ambos grupos) | Flexible (elegir quick o full) |

---

### Validació³n de Datasets

Antes de ejecutar cualquier experimento, verificar disponibilidad:

```bash
# Contar instancias por familia
Get-ChildItem datasets/R1 -Filter *.csv | Measure-Object
Get-ChildItem datasets/R2 -Filter *.csv | Measure-Object
Get-ChildItem datasets/C1 -Filter *.csv | Measure-Object
Get-ChildItem datasets/C2 -Filter *.csv | Measure-Object
Get-ChildItem datasets/RC1 -Filter *.csv | Measure-Object
Get-ChildItem datasets/RC2 -Filter *.csv | Measure-Object
```

**Expected output:**
```
R1:  12 instancias (R101-R112)
R2:  11 instancias (R201-R211)
C1:   9 instancias (C101-C109)
C2:   8 instancias (C201-C208)
RC1:  8 instancias (RC101-RC108)
RC2:  8 instancias (RC201-RC208)
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Total: 56 instancias
```

---

### Criterios de Validació³n

**Antes de aceptar resultados**:

1. âœ… **Factibilidad**: 100% de soluciones factibles
   - Sin violaciones de capacidad
   - Sin violaciones de ventanas de tiempo

2. âœ… **Completitud**: Todos los experimentos completados
   - Test Ró¡pido: 30/30
   - Full: 90/90

3. âœ… **Reproducibilidad**: Usando seed=42
   - Mismos algoritmos generados
   - Diferentes resultados en ejecuciones (GRASP es estocó¡stico)

4. âœ… **Estadó­stica**: Tests reportados con p-values
   - Kruskal-Wallis para comparació³n móºltiple
   - Interpretació³n clara de resultados

5. âœ… **Documentació³n**: Todos los archivos de salida presentes
   - JSONs con resultados crudos
   - Gró¡ficas PNG claras
   - Reportes en markdown

---

### Interpretació³n de Resultados

**Escenario 1: Un algoritmo domina**
```
Ejemplo: GAA_Algorithm_2 con gap promedio 5.2% en todas las familias
â†’ Conclusió³n: Algoritmo robusto para VRPTW
```

**Escenario 2: Especializació³n por familia**
```
Ejemplo:
  - Familia R: GAA_Algorithm_1 mejor
  - Familia C: GAA_Algorithm_3 mejor
  - Familia RC: GAA_Algorithm_2 mejor
â†’ Conclusió³n: Algoritmos especializados, combinar en enfoque mixto
```

**Escenario 3: Trade-off calidad-tiempo**
```
Ejemplo:
  - GAA_Algorithm_1: gap 4.8% (tiempo 25s)
  - GAA_Algorithm_2: gap 5.5% (tiempo 8s)
â†’ Conclusió³n: Seleccionar segóºn restricció³n de tiempo
```

---

### Pró³ximos Pasos Post-Experimentació³n

1. **Anó¡lisis detallado**: Interpretar patrones en resultados
2. **Refinamiento**: Ajustar paró¡metros GRASP segóºn hallazgos
3. **Escalabilidad**: Probar con instancias grandes (Gehring-Homberger)
4. **Comparació³n**: Contra heuró­sticas VRPTW de referencia
5. **Publicació³n**: Documentar metodologó­a y resultados en paper

---

## ðŸ“š Referencias Bibliogró¡ficas

- [Solomon1987] Solomon, M. M. (1987). Algorithms for the vehicle routing and scheduling problems with time window constraints. Operations Research, 35(2), 254-265.
- [Clarke1964] Clarke, G., & Wright, J. W. (1964). Scheduling of vehicles from a central depot to a number of delivery points. Operations Research, 12(4), 568-581.
- [Feo1995] Feo, T. A., & Resende, M. G. (1995). Greedy randomized adaptive search procedures. Journal of Global Optimization, 6(2), 109-133.
- [Resende2009] Resende, M. G., & Ribeiro, C. C. (2009). Greedy randomized adaptive search procedures. Handbook of Metaheuristics, 219-249.
- [Ropke2006] Ropke, S., & Pisinger, D. (2006). An adaptive large neighborhood search heuristic for the pickup and delivery problem with time windows. Transportation Science, 40(4), 455-472.
- [Bró¤ysy2005] Bró¤ysy, O., & Gendreau, M. (2005). Vehicle routing problem with time windows, Part I & II. Transportation Science, 39(1-2).

---

## âœ… Estado del Proyecto

- [x] Problema definido (VRPTW)
- [x] Modelo matemó¡tico formalizado
- [x] Operadores del dominio identificados (22 terminales)
- [x] Metaheuró­stica seleccionada (GRASP)
- [x] Paró¡metros configurados
- [x] Plan experimental completo (Test Ró¡pido + Full)
- [x] Criterios de validació³n de operadores especificados
- [ ] Datasets agregados (Solomon instances recomendados)
- [ ] Gramó¡tica VRPTW-GRASP implementada
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados

---

## ðŸ’¡ Notas Adicionales

**Consideraciones de implementació³n**:
- El có¡lculo de distancias puede ser Euclidiano o basado en matriz
- Las ventanas de tiempo pueden requerir espera (arrival antes de a_i)
- La evaluació³n de inserció³n debe considerar impacto en tiempo de rutas completas
- Reparació³n de restricciones es cró­tica para mantener factibilidad

**Extensiones posibles**:
- VRPTW con flota heterogó©nea
- Móºltiples depó³sitos
- Backhauls (recogidas y entregas)
- Demandas estocó¡sticas

---

# PARTE 8: FUNCIó“N FITNESS 100% CANó“NICA PARA VRPTW (SOLOMON) CON METAHEURóSTICAS TIPO GRASP

## Definició³n canó³nica del objetivo en el VRPTW de Solomon

En la literatura cló¡sica del VRPTW introducida por Solomon (1987) y adoptada posteriormente por pró¡cticamente todos los trabajos de referencia, el problema se formula como un problema de optimizació³n jeró¡rquica con dos objetivos claramente definidos y ordenados.

**Objetivo primario**: Minimizar el nóºmero de vehó­culos utilizados.

**Objetivo secundario**: Minimizar la distancia total recorrida por todos los vehó­culos.

Este orden de prioridad es intró­nseco al benchmark Solomon y no es una decisió³n del investigador. Las mejores soluciones conocidas (BKS) estó¡n definidas bajo este criterio jeró¡rquico.

## Funció³n fitness canó³nica (forma matemó¡tica exacta)

La funció³n fitness canó³nica se define como una funció³n vectorial lexicogró¡fica:

```math
\text{Fitness}(S) = (K(S), D(S))
```

donde:
- $K(S)$ = nóºmero total de vehó­culos (rutas) utilizados en la solució³n $S$
- $D(S)$ = distancia total recorrida por la solució³n $S$

La comparació³n entre dos soluciones $S_1$ y $S_2$ se define estrictamente como:

**$S_1$ es mejor que $S_2$ si y solo si**:
- $K(S_1) < K(S_2)$, o bien
- $K(S_1) = K(S_2)$ y $D(S_1) < D(S_2)$

No existe ningóºn otro criterio de comparació³n vó¡lido dentro del benchmark Solomon.

## Propiedades clave de la funció³n fitness canó³nica

- **Jeró¡rquica** (no ponderada)
- **No es multiobjetivo** en el sentido de Pareto
- **No utiliza pesos, penalizaciones ni combinaciones lineales**
- **Refleja exactamente el criterio de evaluació³n de los benchmarks**

Cualquier desviació³n de esta forma debe ser expló­citamente justificada; de lo contrario, se considera no canó³nica.

## Dominio de definició³n: SOLO soluciones factibles

En la formulació³n canó³nica del VRPTW de Solomon, la funció³n fitness se define exclusivamente sobre soluciones factibles.

Esto implica:
- Todas las ventanas de tiempo son respetadas
- Todas las restricciones de capacidad son respetadas
- Todas las rutas comienzan y terminan en el depó³sito

Las soluciones infeasibles no tienen fitness definido en el modelo canó³nico original.

## Relació³n con GRASP (canó³nica)

GRASP, en su formulació³n original, es totalmente compatible con esta funció³n fitness porque:
- La fase constructiva genera soluciones factibles
- La bóºsqueda local opera exclusivamente dentro del espacio factible
- La aceptació³n de movimientos se rige por la comparació³n lexicogró¡fica del fitness

Por tanto, no es necesario modificar la funció³n fitness para usar GRASP de manera canó³nica en VRPTW Solomon.

## Uso canó³nico del fitness en resultados experimentales

En la presentació³n de resultados:
- El nóºmero de vehó­culos $K$ se reporta siempre primero
- La distancia $D$ se reporta solo para soluciones con el mismo $K$
- El GAP y el %GAP se calculan óºnicamente sobre la distancia $D$, bajo la condició³n de que $K$ coincide con el de la BKS

**Si una solució³n utiliza mó¡s vehó­culos que la BKS, se considera inferior, independientemente de su distancia.**

## Aplicació³n uniforme a las familias C, R y RC

La funció³n fitness canó³nica es idó©ntica para todas las familias Solomon: C (clustered), R (random), RC (mixed).

No existe ninguna modificació³n de la funció³n fitness por familia. Las diferencias de comportamiento emergen de la estructura espacial y temporal de las instancias, no del fitness.

## Forma canó³nica de describir la funció³n fitness en un artó­culo

Texto aceptado y estó¡ndar en la literatura:

> "The VRPTW is addressed as a hierarchical optimization problem. The primary objective is the minimization of the number of vehicles, while the secondary objective is the minimization of the total traveled distance. Solutions are compared lexicographically according to these criteria."

Este texto es pró¡cticamente imposible de objetar por un revisor.

## Quó© NO es canó³nico (importante)

No son canó³nicas, en el contexto Solomon:
- Funciones ponderadas del tipo $w_1 K + w_2 D$
- Funciones con penalizaciones integradas en el fitness final
- Optimizació³n Pareto multiobjetivo
- Minimizar solo distancia ignorando vehó­culos
- Ajustar pesos segóºn la familia de instancias

Estas aproximaciones pueden ser vó¡lidas en otros contextos, pero no son canó³nicas para Solomon + GRASP.

## Resumen final

La funció³n fitness 100% canó³nica para VRPTW con datasets Solomon y metaheuró­sticas como GRASP es una funció³n lexicogró¡fica definida sobre soluciones factibles, que prioriza estrictamente la minimizació³n del nóºmero de vehó­culos y, en segundo lugar, la minimizació³n de la distancia total recorrida.

---

# PARTE 9: GRóFICOS CANó“NICOS PARA GRASP APLICADO AL VRPTW

## Gró¡fico de convergencia del valor objetivo (best-so-far)

**Tipo**: Gró¡fico de ló­neas

**Quó© se grafica**: 
- **Eje horizontal**: Iteraciones de GRASP
- **Eje vertical izquierdo**: Nóºmero de vehó­culos K(t) de la mejor solució³n hasta iteració³n t
- **Eje vertical derecho** (opcional): Distancia D(t) de la mejor solució³n hasta iteració³n t, **SOLO para iteraciones donde K(t) = K_final**

**Nota cró­tica**: La convergencia debe ser representada respetando la jerarquó­a. No se comparan directamente K y D. El gró¡fico tó­picamente mostraró¡ K bajando de forma escalonada, y D disminuyendo en fases donde K es constante.

**Demuestra**: Convergencia jeró¡rquica, primero en reducció³n de vehó­culos y luego en optimizació³n de distancia. Evidencia del comportamiento canó³nico del algoritmo.

---

## Evolució³n del nóºmero de vehó­culos

**Tipo**: Gró¡fico de ló­neas escalonadas (step plot)

**Quó© se grafica**: Eje horizontal = iteraciones; eje vertical = nóºmero de vehó­culos K en la mejor solució³n hasta cada iteració³n.

**Nota cró­tica**: Este gró¡fico es FUNDAMENTAL para demostrar que el algoritmo respeta la jerarquó­a de objetivos. Debe mostrar descensos escalonados en K.

**Demuestra**: Capacidad para mejorar el objetivo primario (minimizació³n de vehó­culos). Si K no cambia, entonces la optimizació³n secundaria (distancia) es irrelevante para la comparació³n con BKS.

---

## Evolució³n de la distancia (SOLO A K constante)

**Tipo**: Gró¡fico de ló­neas

**Quó© se grafica**: Eje horizontal = iteraciones; eje vertical = distancia D en la mejor solució³n, **PERO SOLO MOSTRANDO LA CURVA DESDE EL MOMENTO EN QUE K ALCANZA SU VALOR FINAL (igual al de BKS u ó³ptimo encontrado)**.

**Nota cró­tica**: No incluir iteraciones donde K es diferente. La distancia solo es comparable cuando K es igual. Gró¡ficamente, comenzaró¡ a graficar despuó©s de que K se estabilice.

**Demuestra**: Optimizació³n secundaria dentro del espacio de soluciones con K fijo. Coherente con la funció³n fitness jeró¡rquica.

---

## Distribució³n estadó­stica de la calidad de soluciones

**Tipo**: Boxplot jeró¡rquico (dos paneles claramente diferenciados) o tabla estadó­stica estructurada.

**Quó© se grafica / reporta**:

**Panel 1 (objetivo primario)**:
- Nóºmero de vehó­culos K obtenido por cada algoritmo en móºltiples ejecuciones independientes (â‰¥30)
- Cada boxplot representa la distribució³n de K para un algoritmo

**Panel 2 (objetivo secundario, condicionado)**:
- Distancia total D **óºnicamente para aquellas ejecuciones en las que el algoritmo alcanza el mejor valor de K observado (K_min, idealmente igual a K_BKS)**
- Las ejecuciones que no alcanzan K_min **no se incluyen en este panel** y se reportan expló­citamente como fallidas respecto al objetivo primario

**Reportes opcionales complementarios**:
- Porcentaje de ejecuciones que alcanzan K_min por algoritmo (en tabla o etiquetas en el gró¡fico)

**Nota cró­tica**:
La comparació³n estadó­stica debe respetar estrictamente la jerarquó­a del problema. No es metodoló³gicamente correcto construir un óºnico boxplot del valor objetivo combinado ni comparar distancias entre soluciones con distinto nóºmero de vehó­culos. El anó¡lisis estadó­stico de la distancia solo es vó¡lido dentro del subconjunto de soluciones que alcanzan el mismo valor ó³ptimo del objetivo primario.

**Demuestra**:
- Robustez estadó­stica en la minimizació³n del nóºmero de vehó­culos
- Estabilidad del algoritmo una vez alcanzado el objetivo primario
- Capacidad consistente de optimizació³n secundaria (distancia) en el espacio de soluciones jeró¡rquicamente vó¡lidas

---

## Gró¡fico de tiempo de có³mputo versus calidad de solució³n

**Tipo**: Gró¡fico de dispersió³n o ló­neas (dos ejes)

**Quó© se grafica**: 
- **Eje horizontal**: Tiempo de có³mputo
- **Eje vertical izquierdo**: Nóºmero de vehó­culos K en funció³n del tiempo
- **Eje vertical derecho** (opcional): Distancia D, solo para puntos donde K es ó³ptimo

**Nota cró­tica**: Debe quedar clara la dinó¡mica jeró¡rquica: primero desciende K ró¡pidamente, luego se optimiza D mientras K se mantiene constante.

**Demuestra**: Comportamiento anytime respetando la jerarquó­a: mejoras ró¡pidas en vehó­culos, seguidas de optimizació³n de distancia.

---

## Comparació³n con soluciones de referencia (gap relativo)

**Tipo**: Gró¡fico de barras (dos paneles)

**Quó© se grafica**: 
- **Panel superior**: Diferencia en nóºmero de vehó­culos (K_solució³n - K_BKS) para cada instancia
- **Panel inferior**: Gap porcentual en distancia = ((D_solució³n - D_BKS) / D_BKS) ó— 100, **PERO SOLO PARA INSTANCIAS DONDE K_solució³n = K_BKS**

**Nota cró­tica**: 
- Si K_solució³n > K_BKS, la solució³n es inferior independientemente de D. No se reporta gap de distancia.
- El gap de distancia solo es significativo cuando K coincide.
- Las instancias deben estar claramente etiquetadas indicando si K fue alcanzado.

**Demuestra**: Calidad absoluta respetando la funció³n fitness canó³nica. Esencial para publicació³n cientó­fica.

---

## Anó¡lisis por familias de instancias

**Tipo**: Gró¡fico de barras agrupadas (tres grupos: C, R, RC)

**Quó© se grafica**: 
- **Primer conjunto de barras**: Nóºmero promedio de vehó­culos por familia
- **Segundo conjunto de barras**: Gap promedio de distancia por familia, **SOLO CALCULADO PARA INSTANCIAS DONDE K = K_BKS**

**Nota cró­tica**: Reportar expló­citamente el porcentaje de instancias donde K = K_BKS por familia.

**Demuestra**: Desempeó±o jeró¡rquico por estructura de instancias.

---

## Visualizació³n espacial de las rutas

**Tipo**: Gró¡fico bidimensional

**Quó© se grafica**: Clientes como nodos, depó³sito marcado, rutas de vehó­culos en ló­neas de colores distintos, **con el nóºmero de vehó­culos claramente indicado en el tó­tulo**.

**Nota cró­tica**: Mostrar tanto (K, D) en el tó­tulo. Ejemplo: "Solució³n instancia R101: 4 vehó­culos, 1247.8 km, gap=2.1%"

**Demuestra**: Factibilidad visual y validació³n de que K es mó­nimo (coherencia espacial).

---

## Uso de las ventanas de tiempo

**Tipo**: Histograma o gró¡fico de dispersió³n

**Quó© se grafica**: Tiempo real de llegada versus ventana permitida [a_i, b_i] para cada cliente en una solució³n con K = K_BKS.

**Nota cró­tica**: Las ventanas de tiempo son RESTRICCIONES DURAS, no objetivos de optimizació³n. Este gró¡fico es de **VERIFICACIó“N DE FACTIBILIDAD**, no de optimizació³n. Se muestra solo para soluciones con K = K_BKS para confirmar que no hay violaciones ocultas en las soluciones jeró¡rquicamente ó³ptimas. Todas las soluciones encontradas son factibles; este gró¡fico documenta esa factibilidad.

**Demuestra**: Que las soluciones con K = K_BKS respetan completamente las restricciones de tiempo, sin violaciones ocultas. Verifica la calidad de la verificació³n de factibilidad en la solució³n jeró¡rquicamente ó³ptima.

---

## Anó¡lisis de sensibilidad del paró¡metro alfa de GRASP

**Tipo**: Gró¡fico de ló­neas (dos ejes)

**Quó© se grafica**: 
- **Eje horizontal**: Valores de alfa
- **Eje vertical izquierdo**: Nóºmero de vehó­culos K promedio
- **Eje vertical derecho**: Distancia D promedio (solo para soluciones con K mó­nimo)

**Nota cró­tica**: Separar claramente el impacto en K vs impacto en D. El paró¡metro alfa puede afectar principalmente K.

**Demuestra**: Impacto jeró¡rquico del paró¡metro.

---

## Comparació³n entre GRASP base y GRASP con mejoras

**Tipo**: Gró¡fico de barras agrupadas o tabla

**Quó© se grafica**: 
- **Columna 1 por algoritmo**: K promedio
- **Columna 2 por algoritmo**: D promedio (solo para instancias/ejecuciones donde K es mó­nimo)
- **Columna 3 por algoritmo**: Porcentaje de ejecuciones con K ó³ptimo

**Nota crítica**: Mostrar tres dimensiones: K alcanzado, D en K óptimo, y robustez en alcanzar K óptimo.

**Demuestra**: Contribución de cada componente en términos jerárquicos.

---

## Conjunto mó­nimo esperado para publicació³n

Un artó­culo só³lido COHERENTE CON LA FUNCIó“N FITNESS JERóRQUICA incluye:
- Gró¡fico de convergencia en K (escalonado)
- Gró¡fico de convergencia en D (solo a K constante)
- Boxplot de K por algoritmo y boxplot de D (solo a K constante)
- Anó¡lisis de gap de distancia (solo para instancias con K = K_BKS)
- Anó¡lisis de gap de vehó­culos (diferencia en K)
- Comparació³n tiempo-calidad jeró¡rquica
- Anó¡lisis por familias (K y D separados)
- Al menos una visualizació³n de rutas de solució³n ó³ptima en K

---

# PARTE 11: ESQUEMA CANONICO DE ARCHIVOS CSV PARA GRASP-VRPTW (SOLOMON)

Esquema EXACTO y definitivo de los CSV, con nombres de columnas finales, tipos implícitos, y reglas semánticas claras.

Esto está pensado para que:
- No tengas ambigüedades después
- Puedas automatizar análisis y gráficos
- Sea directamente trazable a tablas/figuras del paper

---

## ARCHIVO 1: RESULTADOS POR EJECUCIÓN (RAW RUNS)

### Ruta
`
output/raw_runs/raw_results.csv
`

Una fila = una ejecución independiente (Algoritmo  Instancia  Run)

### Columnas

algorithm_id | instance_id | family | run_id | random_seed | K_final | D_final | K_BKS | D_BKS | delta_K | gap_distance | gap_percent | total_time_sec | iterations_executed | reached_K_BKS

### Notas

- gap_distance y gap_percent deben ser NA si delta_K  0
- reached_K_BKS = (K_final == K_BKS)

---

## ARCHIVO 2: TRAZAS DE CONVERGENCIA POR ITERACIÓN

### Ruta
`
output/convergence/convergence_trace.csv
`

Una fila = una iteración de una ejecución

### Columnas

algorithm_id | instance_id | family | run_id | iteration | elapsed_time_sec | K_best_so_far | D_best_so_far | is_K_BKS

### Notas

- is_K_BKS = (K_best_so_far == K_BKS)
- D_best_so_far se registra siempre, pero solo se analiza cuando is_K_BKS = true

---

## ARCHIVO 3: RESUMEN AGREGADO POR INSTANCIA

### Ruta
`
output/aggregated/summary_by_instance.csv
`

Una fila = (Algoritmo  Instancia)

### Columnas

algorithm_id | instance_id | family | runs_total | K_best | K_mean | K_std | K_min | K_max | percent_runs_K_min | D_mean_at_K_min | D_std_at_K_min | gap_percent_mean | gap_percent_std | time_mean_sec

### Notas

- K_min = mínimo K observado
- percent_runs_K_min = % de ejecuciones con K = K_min
- D_* se calcula solo sobre ejecuciones con K = K_min
- gap_* solo se calcula cuando K_min == K_BKS

---

## ARCHIVO 4: RESUMEN AGREGADO POR FAMILIA

### Ruta
`
output/aggregated/summary_by_family.csv
`

Una fila = (Algoritmo  Familia)

### Columnas

algorithm_id | family | instances_count | K_mean | percent_instances_K_BKS | gap_percent_mean | gap_percent_std | time_mean_sec

### Notas

- percent_instances_K_BKS = % de instancias donde K_min == K_BKS
- gap_* se calcula solo sobre esas instancias

---

## ARCHIVO 5: ANÁLISIS TEMPORAL (ANYTIME)

### Ruta
`
output/time_analysis/time_metrics.csv
`

Una fila = una ejecución

### Columnas

algorithm_id | instance_id | family | run_id | time_to_K_min_sec | iteration_to_K_min | time_to_best_D_sec | iteration_to_best_D

### Notas

- time_to_K_min_sec = primer tiempo donde K_best_so_far alcanza K_min
- time_to_best_D_sec se mide solo después de alcanzar K_min

---

## ARCHIVO 6: SOLUCIONES ESTRUCTURALES (RUTAS)

### Ruta
`
output/solutions/solutions.csv
`

Una fila = una ruta de una solución final

### Columnas

algorithm_id | instance_id | family | run_id | route_id | vehicle_load | route_distance | customer_sequence

### Notas

- customer_sequence en formato texto, por ejemplo: "0-12-5-8-0"
- Este archivo permite reconstruir rutas completas

---

## ARCHIVO 7: TIEMPOS DE LLEGADA (VENTANAS DE TIEMPO)

### Ruta
`
output/solutions/time_windows_check.csv
`

Una fila = un cliente en una solución

### Columnas

algorithm_id | instance_id | family | run_id | customer_id | arrival_time | window_start | window_end | slack_time

### Notas

- slack_time = window_end  arrival_time
- Solo se guarda para soluciones con K_final = K_BKS

---

## ARCHIVO 8: METADATOS DEL EXPERIMENTO

### Ruta
`
output/metadata/experiment_metadata.csv
`

Una fila = experimento completo

### Columnas

experiment_id | experiment_date | algorithm_id | dataset_name | instances_used | stopping_criterion | max_iterations | max_time_sec | alpha_value | hardware_cpu | hardware_ram | os | programming_language | code_version

---

## REGLAS DE CONSISTENCIA (OBLIGATORIAS)

1. Los nombres de columnas deben ser EXACTAMENTE estos
2. Nunca mezclar resultados crudos con agregados
3. Toda figura del paper debe poder reconstruirse leyendo uno o más de estos CSV
4. Toda métrica jerárquica debe poder inferirse sin ambigüedad desde los datos guardados

---

## RESUMEN RÁPIDO

- raw_results.csv  base estadística
- convergence_trace.csv  convergencia y anytime
- summary_by_instance.csv  tablas principales del paper
- summary_by_family.csv  análisis estructural
- time_metrics.csv  eficiencia
- solutions.csv  rutas
- time_windows_check.csv  factibilidad
- experiment_metadata.csv  reproducibilidad

---

# PARTE 12: ESTRUCTURA UNIFICADA DE OUTPUTS (INSPIRADA EN GAA-GCP-ILS-4)

## Principio Central

Todos los outputs de VRPTW-GRASP van dirigidos a una ÚNICA carpeta raíz output/, donde **cada ejecución genera su propia subcarpeta con TIMESTAMP único** (formato: DD-MM-YY_HH-MM-SS).

Esto garantiza:
-  Outputs diferenciados por sesión/ejecución
-  Reproducibilidad y trazabilidad
-  Compatibilidad con GAA-GCP-ILS-4
-  Escalabilidad para múltiples corridas

---

## Estructura de Directorios Unificada

\\\
output/
 01-01-26_14-23-45/                    # Timestamp de ejecución 1
    results/
       raw_results.csv               # Archivo 1: raw runs
       convergence_trace.csv         # Archivo 2: trazas
       summary_by_instance.csv       # Archivo 3: agregados instancia
       summary_by_family.csv         # Archivo 4: agregados familia
       time_metrics.csv              # Archivo 5: análisis temporal
       experiment_metadata.json      # Metadatos de la ejecución
    solutions/
       solutions.csv                 # Archivo 6: rutas
       time_windows_check.csv        # Archivo 7: ventanas de tiempo
    plots/
       convergence_K.png
       convergence_D.png
       distribution_K.png
       distribution_D.png
       gap_analysis.png
       time_quality.png
       family_analysis.png
       route_visualization_{instance}.png
       time_windows_{instance}.png
       sensitivity_analysis.png
       algorithm_comparison.png
    gaa/
       generated_algorithms.json     # Descripción de Alg-1, Alg-2, Alg-3
       grammar_specification.txt
       ast_nodes_trace.json
    logs/
        execution.log                 # Log detallado de ejecución
        errors.log                    # Errores y warnings
        session_summary.txt           # Resumen de sesión

 01-01-26_14-45-20/                    # Timestamp de ejecución 2
    results/
    solutions/
    plots/
    gaa/
    logs/

 [más ejecuciones...]
\\\

---

## Responsabilidades de cada Carpeta

### results/
Datos tabulares y estadísticos (CSV, JSON, YAML)
- raw_results.csv: Base de datos bruta de todas las ejecuciones
- convergence_trace.csv: Trazas iteración por iteración
- summary_by_instance.csv: Resumen por (algoritmo, instancia)
- summary_by_family.csv: Resumen por (algoritmo, familia)
- time_metrics.csv: Métricas de tiempo y anytime
- experiment_metadata.json: Configuración y parámetros de experimento

### solutions/
Estructuras de rutas y validación
- solutions.csv: Rutas completas y secuencias de clientes
- time_windows_check.csv: Validación de ventanas de tiempo por cliente

### plots/
Visualizaciones en formato PNG (listas para paper)
- 11 gráficos canónicos (uno por tipo de análisis)
- Nombres descriptivos y consistentes
- Compatibles con resolución de publicación (300 DPI)

### gaa/
Información sobre algoritmos generados automáticamente
- generated_algorithms.json: Descripción de Alg-1, Alg-2, Alg-3
- grammar_specification.txt: Gramática utilizada
- ast_nodes_trace.json: Traza de generación de AST

### logs/
Información de proceso y auditoría
- execution.log: Log completo de ejecución
- errors.log: Warnings y errores
- session_summary.txt: Resumen ejecutivo de la sesión

---

## Clase OutputManager para VRPTW-GRASP

Adaptada del patrón de GAA-GCP-ILS-4:

\\\python
class OutputManager:
    '''
    Gestor centralizado de outputs para VRPTW-GRASP
    
    Garantiza que:
    - Todos los outputs van a output/{timestamp}/
    - Cada ejecución es independiente
    - Archivos CSV tienen nombres exactos y columnas correctas
    - Logs se registran automáticamente
    '''
    
    TIMESTAMP_FORMAT = "%d-%m-%y_%H-%M-%S"  # Ej: 01-01-26_14-23-45
    
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.session_timestamp = None
        self.session_dir = None
        self.results_dir = None
        self.solutions_dir = None
        self.plots_dir = None
        self.gaa_dir = None
        self.logs_dir = None
    
    def create_session(self):
        '''Crea nueva sesión con timestamp único'''
        self.session_timestamp = datetime.now().strftime(self.TIMESTAMP_FORMAT)
        self.session_dir = self.base_output_dir / self.session_timestamp
        
        # Crear subdirectorios
        self.results_dir = self.session_dir / "results"
        self.solutions_dir = self.session_dir / "solutions"
        self.plots_dir = self.session_dir / "plots"
        self.gaa_dir = self.session_dir / "gaa"
        self.logs_dir = self.session_dir / "logs"
        
        for dir_path in [self.results_dir, self.solutions_dir, self.plots_dir, 
                         self.gaa_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        return self.session_dir
    
    def save_raw_results(self, data: List[Dict]) -> str:
        '''Guarda raw_results.csv en results/'''
        filepath = self.results_dir / "raw_results.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_convergence_trace(self, data: List[Dict]) -> str:
        '''Guarda convergence_trace.csv en results/'''
        filepath = self.results_dir / "convergence_trace.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_summary_by_instance(self, data: List[Dict]) -> str:
        '''Guarda summary_by_instance.csv en results/'''
        filepath = self.results_dir / "summary_by_instance.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_summary_by_family(self, data: List[Dict]) -> str:
        '''Guarda summary_by_family.csv en results/'''
        filepath = self.results_dir / "summary_by_family.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_time_metrics(self, data: List[Dict]) -> str:
        '''Guarda time_metrics.csv en results/'''
        filepath = self.results_dir / "time_metrics.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_solutions(self, data: List[Dict]) -> str:
        '''Guarda solutions.csv en solutions/'''
        filepath = self.solutions_dir / "solutions.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_time_windows_check(self, data: List[Dict]) -> str:
        '''Guarda time_windows_check.csv en solutions/'''
        filepath = self.solutions_dir / "time_windows_check.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_experiment_metadata(self, metadata: Dict) -> str:
        '''Guarda experiment_metadata.json en results/'''
        filepath = self.results_dir / "experiment_metadata.json"
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        return str(filepath)
    
    def save_generated_algorithms(self, alg_info: Dict) -> str:
        '''Guarda información de algoritmos generados en gaa/'''
        filepath = self.gaa_dir / "generated_algorithms.json"
        with open(filepath, 'w') as f:
            json.dump(alg_info, f, indent=2)
        return str(filepath)
    
    def save_plot(self, figure, filename: str) -> str:
        '''Guarda figura PNG en plots/'''
        filepath = self.plots_dir / filename
        figure.savefig(filepath, dpi=300, bbox_inches='tight')
        return str(filepath)
    
    def get_session_dir(self) -> Path:
        '''Retorna directorio de sesión actual'''
        return self.session_dir
    
    def get_timestamp(self) -> str:
        '''Retorna timestamp de sesión'''
        return self.session_timestamp
\\\

---

## Patrón de Uso en Código Principal

\\\python
# En main script o demo_experimentation_quick.py

from utils.output_manager import OutputManager

# Crear gestor de outputs
output_mgr = OutputManager(base_output_dir="output")

# Iniciar nueva sesión (crea estructura con timestamp)
session_dir = output_mgr.create_session()
print(f"Session directory: {session_dir}")

# Ejecutar experimentos (loop principal)
raw_results = []
convergence_traces = []

for algo in [Alg-1, Alg-2, Alg-3]:
    for instance in instances:
        for run in range(30):
            # Ejecutar GRASP
            solution = algo.run(instance)
            
            # Guardar datos crudos
            raw_results.append({
                'algorithm_id': algo.name,
                'instance_id': instance.name,
                'family': instance.family,
                'run_id': run,
                'K_final': solution.num_vehicles,
                'D_final': solution.distance,
                # ... más campos
            })
            
            # Guardar trazas
            convergence_traces.extend(solution.convergence_trace)

# Después de todas las ejecuciones, agregar datos
output_mgr.save_raw_results(raw_results)
output_mgr.save_convergence_trace(convergence_traces)

# Generar agregados
summary_instance = aggregate_by_instance(raw_results)
summary_family = aggregate_by_family(raw_results)

output_mgr.save_summary_by_instance(summary_instance)
output_mgr.save_summary_by_family(summary_family)

# Guardar metadatos
metadata = {
    'experiment_date': datetime.now().isoformat(),
    'algorithms': [Alg-1, Alg-2, Alg-3],
    'instances_count': 56,
    'max_iterations': 500,
    'code_version': '1.0.0',
}
output_mgr.save_experiment_metadata(metadata)

# Generar plots (después)
plots_mgr = PlotManager(output_mgr)
plots_mgr.plot_all_canonical_graphics(raw_results)

print(f"All outputs saved in: {output_mgr.get_session_dir()}")
\\\

---

## Compatibilidad con GAA-GCP-ILS-4

La estructura es **completamente compatible** porque:

1.  Misma estructura de carpetas base: output/{timestamp}/
2.  Mismo patrón de timestamps: DD-MM-YY_HH-MM-SS
3.  Mismo patrón de OutputManager unificado
4.  Mismo sistema de logging centralizado
5.  Mismo patrón de metadata.json para reproducibilidad

**Diferencias adaptadas a VRPTW:**
- Archivos CSV específicos para VRPTW (no GCP)
- 11 gráficos canónicos para VRPTW (no GCP)
- Campos específicos: K_final, D_final, K_BKS, ventanas de tiempo (no colores de nodos)

---

## Validación de Estructura

Después de cada ejecución, validar:

\\\python
def validate_output_structure(session_dir: Path) -> bool:
    '''Valida que estructura de outputs sea correcta'''
    required_dirs = ['results', 'solutions', 'plots', 'gaa', 'logs']
    required_files = {
        'results': ['raw_results.csv', 'convergence_trace.csv', 
                   'summary_by_instance.csv', 'summary_by_family.csv',
                   'time_metrics.csv', 'experiment_metadata.json'],
        'solutions': ['solutions.csv', 'time_windows_check.csv'],
    }
    
    for dir_name in required_dirs:
        dir_path = session_dir / dir_name
        if not dir_path.exists():
            print(f"ERROR: Missing directory {dir_path}")
            return False
    
    for dir_name, files in required_files.items():
        for filename in files:
            filepath = session_dir / dir_name / filename
            if not filepath.exists():
                print(f"ERROR: Missing file {filepath}")
                return False
    
    print(f" Output structure validated: {session_dir}")
    return True
\\\


---

# PARTE 13: MÉTRICAS CANÓNICAS PARA VRPTW (SOLOMON) CON GRASP

## Contexto General (CRÍTICO)

El VRPTW de Solomon es un problema **jerárquico estricto**:

- **Objetivo Primario**: Minimizar número de vehículos (K)
- **Objetivo Secundario**: Minimizar distancia total (D), SOLO SI K es igual

Las métricas deben respetar esta jerarquía en **TODOS LOS NIVELES**:
- Individual (por instancia)
- Agregado (por algoritmo e instancia)
- Por familia (C, R, RC)

---

## ANÁLISIS POR FAMILIAS DE INSTANCIAS (C, R, RC)

### Características de cada Familia

| Familia | Características | K típico | D típico | Dificultad |
|---------|-----------------|----------|----------|-----------|
| **C** (Clustered) | Clientes agrupados geográficamente; ventanas de tiempo amplias | 10 | 800-1200 | Baja |
| **R** (Random) | Clientes distribuidos aleatoriamente; ventanas de tiempo estrictas | 12-15 | 1200-1600 | Alta |
| **RC** (Mixed) | Combinación de clustering y aleatoriedad; ventanas variadas | 13-16 | 1400-1800 | Alta |

Nota: K típico es referencia; K_BKS actual varía por instancia específica.

---

## MÉTRICAS PRIMARIAS POR FAMILIA (OBLIGATORIAS)

### 1.1 Número promedio de vehículos (K_mean)

**Definición**:
Promedio del número de vehículos utilizados en todas las instancias de una familia.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.mdK\\_mean = \\frac{1}{n} \\sum_{i=1}^{n} K_{final,i}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

donde n = número de instancias en la familia.

**Uso**:
- Métrica principal de comparación entre familias
- Indica qué tan bien el algoritmo maneja la estructura de la familia

**Interpretación**:
- Familias C: K_mean ~ 10-11 (mejor desempeño esperado)
- Familias R: K_mean ~ 12-13 (más exigente)
- Familias RC: K_mean ~ 13-14 (más exigente)

**Cómo reportar**:
`
| Familia | K_mean | K_std |
|---------|--------|-------|
| C       | 10.2   | 0.4   |
| R       | 12.5   | 0.8   |
| RC      | 13.7   | 0.9   |
`

---

### 1.2 Mejor número de vehículos alcanzado (K_best)

**Definición**:
Mínimo número de vehículos alcanzado por el algoritmo en cualquier ejecución de instancias de la familia.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.mdK\\_best = \\min(K_{final}) \\text{ para todas las instancias y ejecuciones}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Mide capacidad máxima del algoritmo
- Comparación con K_BKS_best

**Interpretación**:
- Si K_best == K_BKS_best: el algoritmo es capaz de alcanzar lo mejor conocido
- Si K_best > K_BKS_best: hay margen de mejora

---

### 1.3 Porcentaje de instancias con K_BKS alcanzado

**Definición**:
Porcentaje de instancias de la familia donde el algoritmo alcanza K_BKS (en al menos una ejecución).

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{%Instancias}_K = \\frac{\\text{# instancias donde } K\\_min = K\\_BKS}{\\text{# total instancias}} \\times 100c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Métrica clave de efectividad por familia
- Estándar en comparaciones de estado del arte
- Muy utilizada en papers sobre VRPTW

**Interpretación**:
`
%Instancias_K = 100%   Excelente (alcanza BKS en todas)
%Instancias_K >= 90%   Muy bueno
%Instancias_K >= 70%   Bueno
%Instancias_K < 70%    Necesita mejora
`

**Cómo reportar**:
`
| Familia | Instancias | %K_BKS |
|---------|-----------|--------|
| C       | 9         | 100%   |
| R       | 12        | 83%    |
| RC      | 8         | 75%    |
`

---

## MÉTRICAS SECUNDARIAS POR FAMILIA (JERÁRQUICAMENTE VÁLIDAS)

### 2.1 Distancia promedio a K óptimo (D_mean_at_K)

**Definición**:
Promedio de distancia total, considerando ÚNICAMENTE instancias donde K = K_BKS.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.mdD\\_mean\\_at\\_K = \\frac{1}{m} \\sum_{i \\in \\{K\\_final = K\\_BKS\\}} D_ic:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

donde m = número de instancias/ejecuciones con K = K_BKS.

**Condición Crítica**:
- Solo calcular cuando K = K_BKS
- Si K  K_BKS, no comparar distancias

**Uso**:
- Comparación fina de calidad dentro del espacio jerárquicamente válido
- Métrica secundaria más importante

**Interpretación**:
- Menor es mejor
- Solo comparar entre algoritmos que alcanzan K_BKS en instancias similares

---

### 2.2 Porcentaje de GAP promedio (%GAP_mean)

**Definición**:
Promedio del porcentaje de GAP en distancia:

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\%GAP_i = \\frac{D_i - D\\_BKS_i}{D\\_BKS_i} \\times 100c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\%GAP\\_mean = \\frac{1}{m} \\sum_{i \\in \\{K = K\\_BKS\\}} \\%GAP_ic:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Condición Crítica**:
- Solo para instancias donde K = K_BKS
- Nunca comparar GAP entre soluciones con K diferente

**Uso**:
- Métrica estándar de comparación entre familias
- Permite comparar instancias de distinto tamaño
- Muy utilizada en literatura VRPTW

**Interpretación**:
`
%GAP_mean <= 1%    Excelente
%GAP_mean <= 5%    Muy bueno
%GAP_mean <= 10%   Bueno
%GAP_mean > 10%    Necesita mejora
`

**Cómo reportar**:
`
| Familia | %GAP_mean | %GAP_std |
|---------|-----------|----------|
| C       | 0.08%     | 0.05%    |
| R       | 0.44%     | 0.22%    |
| RC      | 0.61%     | 0.38%    |
`

---

### 2.3 Desviación estándar del %GAP (%GAP_std)

**Definición**:
Variabilidad del %GAP dentro de la familia (solo para K = K_BKS).

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\%GAP\\_std = \\sqrt{\\frac{1}{m} \\sum_{i \\in \\{K = K\\_BKS\\}} (\\%GAP_i - \\%GAP\\_mean)^2}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Evalúa estabilidad de la optimización secundaria
- Diferencia algoritmos consistentes de inestables

**Interpretación**:
- Bajo %GAP_std: Algoritmo muy consistente
- Alto %GAP_std: Algoritmo inestable o muy dependiente de aleatoriedad

---

## MÉTRICAS DE ROBUSTEZ POR FAMILIA

### 3.1 Porcentaje promedio de ejecuciones con K óptimo

**Definición**:
Para cada instancia de la familia, calcular qué % de sus 30 ejecuciones alcanzan K_BKS. Luego promediar sobre todas las instancias.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{%Ejecuciones\\_K} = \\frac{1}{n} \\sum_{i=1}^{n} \\left( \\frac{\\text{# ejecuciones con } K = K\\_BKS}{30} \\times 100 \\right)c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Mide robustez frente a aleatoriedad
- Especialmente importante en GRASP (muy dependiente de alpha y aleatoriedad)

**Interpretación**:
`
%Ejecuciones_K >= 90%   Muy robusto
%Ejecuciones_K >= 70%   Robusto
%Ejecuciones_K >= 50%   Moderado
%Ejecuciones_K < 50%    Poco robusto
`

---

### 3.2 Desviación estándar de K

**Definición**:
Variabilidad del número de vehículos entre ejecuciones para instancias de la familia.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.mdK\\_std = \\frac{1}{n} \\sum_{i=1}^{n} \\sqrt{\\frac{1}{30} \\sum_{j=1}^{30} (K_{i,j} - K\\_mean_i)^2}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Indica sensibilidad a fase constructiva aleatoria
- Valores bajos: algoritmo estable
- Valores altos: mucha variación entre runs

---

## MÉTRICAS DE CONVERGENCIA POR FAMILIA

### 4.1 Iteraciones promedio hasta K óptimo

**Definición**:
Promedio de iteraciones necesarias para alcanzar K_BKS (solo si se alcanza).

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{Iter\\_to\\_K} = \\frac{1}{m} \\sum_{i \\in \\{alcanzó K\\_BKS\\}} \\text{iteration\\_to\\_K\\_BKS}_ic:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Mide dificultad estructural de la familia
- Familias R y RC: típicamente ~150-300 iteraciones
- Familias C: típicamente ~50-100 iteraciones

---

### 4.2 Tiempo promedio hasta K óptimo

**Definición**:
Tiempo medio necesario para alcanzar K_BKS.

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{Time\\_to\\_K} = \\frac{1}{m} \\sum_{i \\in \\{alcanzó K\\_BKS\\}} \\text{time\\_to\\_K\\_BKS}_ic:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Comparación de eficiencia temporal
- Justifica presupuestos de tiempo en producción

---

## MÉTRICAS DE EFICIENCIA COMPUTACIONAL POR FAMILIA

### 5.1 Tiempo promedio total de ejecución

**Definición**:
Tiempo medio de ejecución del algoritmo (500 iteraciones o 60 segundos).

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.mdT\\_avg = \\frac{1}{n \\times 30} \\sum_{i=1}^{n} \\sum_{j=1}^{30} T_{i,j}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**:
- Evalúa costo computacional según estructura
- Ayuda a fijar presupuestos de tiempo en sistemas reales

**Interpretación**:
`
T < 5 segundos    Muy rápido
T 5-10 segundos   Rápido
T 10-20 segundos  Moderado
T > 20 segundos   Lento
`

---

## MÉTRICAS DE FACTIBILIDAD (VALIDACIÓN CRÍTICA)

Estas **NO se comparan**, se **VERIFICAN**.

### 6.1 Violaciones de ventanas de tiempo

**Definición**:
Número o magnitud de clientes servidos fuera de su ventana temporal.

**Condición Canónica**:
- En Solomon: SIEMPRE debe ser cero
- Si > 0: solución es infactible

**Verificación**:
`python
for solution in all_solutions:
    for cliente in solution:
        assert arrival_time[cliente] <= window_end[cliente], "Violación de ventana"
        assert arrival_time[cliente] >= window_start[cliente], "Violación de ventana"
`

---

### 6.2 Violaciones de capacidad

**Definición**:
Exceso de capacidad por ruta.

**Condición Canónica**:
- En Solomon: SIEMPRE debe ser cero
- Si > 0: solución es infactible

---

## MÉTRICAS DERIVADAS (OPCIONALES, NO CANÓNICAS)

Útiles para análisis cualitativo, pero NO reemplazan métricas canónicas.

### 7.1 Número promedio de clientes por ruta

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{Clients\\_per\\_route} = \\frac{\\text{Total clientes}}{K}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**: Interpretar estructura de familias (C: rutas cortas, R: rutas largas)

### 7.2 Longitud promedio de ruta

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{Route\\_length} = \\frac{D}{K}c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**: Evaluar balance entre vehículos y distancia

### 7.3 Holgura temporal promedio

c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md\\text{Slack\\_mean} = \\frac{1}{\\text{total clientes}} \\sum_{i} (\\text{window\\_end}_i - \\text{arrival\\_time}_i)c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP\problema_metaheuristica.md

**Uso**: Entender cuánto "margen" usa cada familia

---

## RESUMEN EJECUTIVO (MÍNIMO REQUERIDO POR FAMILIA)

Para cada familia (C, R, RC), un paper canónico DEBE reportar:

**Tabla Mínima**:
`
| Métrica | C | R | RC |
|---------|---|---|----|
| K_mean | 10.2 | 12.5 | 13.7 |
| %Instancias_K_BKS | 100% | 83% | 75% |
| %GAP_mean | 0.08% | 0.44% | 0.61% |
| %GAP_std | 0.05% | 0.22% | 0.38% |
| T_avg (seg) | 5.1 | 7.8 | 8.2 |
| %Ejecuciones_K_BKS | 96% | 81% | 76% |
`

---

## REGLA DE ORO: LO QUE ES Y NO ES CANÓNICO

###  ES CANÓNICO para Solomon VRPTW

- Métricas que distinguen K y D
- Comparaciones de distancia SOLO cuando K = K_BKS
- Análisis separado por familia (C, R, RC)
- Porcentaje de instancias con K_BKS alcanzado
- %GAP en distancia (condicionado)
- Tiempo hasta K óptimo

###  NO ES CANÓNICO para Solomon VRPTW

- Métricas que mezclan K y D (ej: fitness ponderado K + 0.1*D)
- Comparaciones de distancia entre soluciones con K diferente
- Tratamiento de VRPTW como problema de optimización simultánea K y D
- Pareto multiobjeto aplicado a Solomon
- Comparación de distancia sin considerar K
- GAP calculado sin la condición K = K_BKS

---

## CIERRE CONCEPTUAL

Si una métrica:

1.  No distingue K y D, O
2.  Mezcla distancia entre soluciones con distinto K, O
3.  Trata K y D como objetivos simultáneos, O
4.  Usa peso agregado (wK + dD), O
5.  Aplica Pareto multiobjeto,

**Entonces NO ES CANÓNICA para VRPTW Solomon**, aunque sea común en otros contextos (VRP general, multiobjeto, etc.).

Solomon VRPTW es **jerárquico por naturaleza**. Las métricas deben reflejar eso.


---

# PARTE 14: FUNCIÓN DE FITNESS CANÓNICA EN VRPTW CON GRASP

## Naturaleza del Problema (Fundamento)

El VRPTW de Solomon se formula como un problema de optimización jerárquica con dos objetivos, ordenados estrictamente por prioridad:

**Objetivo Primario (prioridad absoluta)**:
- Minimizar el número de vehículos utilizados.

**Objetivo Secundario (condicionado)**:
- Minimizar la distancia total recorrida, solo entre soluciones que usan el mismo número de vehículos.

Esta jerarquía es parte del benchmark y no es una elección del investigador.

---

## Definición Formal de la Función de Fitness Canónica

La función de fitness se define como una función vectorial lexicográfica:

$$\text{Fitness}(S) = (K(S), D(S))$$

donde:

- $K(S)$ = número de vehículos (rutas) utilizados por la solución $S$
- $D(S)$ = distancia total recorrida por la solución $S$

---

## Regla de Comparación (Criterio de Dominancia)

Dadas dos soluciones factibles $S_1$ y $S_2$:

**$S_1$ es mejor que $S_2$ si y solo si:**

$$K(S_1) < K(S_2) \quad \text{o bien} \quad K(S_1) = K(S_2) \wedge D(S_1) < D(S_2)$$

**No existe ningún otro criterio de comparación válido** en el contexto canónico de Solomon.

**Implicación fundamental**:

Una solución con menor distancia pero mayor número de vehículos es **SIEMPRE inferior**, sin importar la magnitud de la diferencia en distancia.

---

## Dominio de la Función Fitness

La función de fitness canónica está definida únicamente sobre soluciones **factibles**, es decir:

- Todas las ventanas de tiempo son respetadas.
- Todas las restricciones de capacidad son respetadas.
- Todas las rutas comienzan y terminan en el depósito.

**Las soluciones infeasibles no tienen fitness definido** en la formulación canónica original.

---

## Relación con GRASP (Canonicidad)

GRASP es plenamente compatible con esta función fitness porque:

1. **La fase constructiva** genera soluciones factibles (respetando restricciones).
2. **La búsqueda local** opera dentro del espacio factible (movimientos locales preservan factibilidad).
3. **La aceptación de movimientos** se rige por la comparación lexicográfica del fitness.

**Por tanto, no se requiere ninguna modificación del fitness para aplicar GRASP de manera canónica al VRPTW.**

---

## Forma Equivalente de Implementación (Nota Práctica)

Aunque el fitness es conceptualmente lexicográfico, puede implementarse internamente de forma equivalente como:

$$\text{Fitness}(S) = M \cdot K(S) + D(S)$$

donde $M$ es una constante suficientemente grande (mayor que cualquier distancia posible en el benchmark).

**IMPORTANTE**:
- Esta es **solo una implementación técnica** para acelerar comparaciones.
- El **criterio real sigue siendo lexicográfico**.
- En el paper, **la función debe describirse como jerárquica, no ponderada**.
- $M$ no es un parámetro de ajuste; es una implementación.

---

## Uso del Fitness en la Evaluación Experimental

En los resultados reportados:

- **K se reporta siempre como métrica principal** (primera en cualquier tabla o gráfico).
- **D se reporta solo cuando K coincide** (K = K_BKS).
- **GAP y %GAP se calculan únicamente sobre D y solo cuando K = K_BKS**.
- **Nunca se comparan distancias entre soluciones con distinto K.**

### Ejemplo de Reporte Correcto

| Algoritmo | Familia | K_mean | K_std | D_mean@K_BKS | %GAP_mean |
|-----------|---------|--------|-------|--------------|-----------|
| Alg-1 | C | 10.2 | 0.4 | 812.3 | +2.1% |
| Alg-1 | R | 12.8 | 0.6 | 1312.5 | +4.3% |

- K_mean es comparación principal entre familias.
- D_mean@K_BKS solo se reporta cuando la solución alcanzó K_BKS.
- Si un algoritmo nunca alcanzó K_BKS para una familia, D_mean@K_BKS se reporta como "" (no aplica).

---

## Aplicación a las Familias Solomon (C, R, RC)

**La función fitness es idéntica para todas las familias:**

- C (clustered)
- R (random)
- RC (mixed)

**No se ajusta el fitness por familia**; las diferencias emergen del problema, no de la función.

La jerarquía K  D se mantiene invariante.

---

## Resumen en una Frase (Canónica)

**La función de fitness canónica del VRPTW con GRASP es una función lexicográfica definida sobre soluciones factibles, que prioriza estrictamente la minimización del número de vehículos y, en segundo lugar, la minimización de la distancia total recorrida.**

---

## Verificación: ¿Mi Función de Fitness es Canónica?

Use esta lista de control:

| Pregunta | Sí =  | No =  |
|----------|--------|--------|
| ¿Mi fitness prioriza K sobre D? |  |  |
| ¿Dos soluciones con distinto K nunca se comparan por D? |  |  |
| ¿Mi fitness está definido solo sobre soluciones factibles? |  |  |
| ¿Mi fitness NO es una suma ponderada (wK + dD)? |  |  |
| ¿Describo el fitness como jerárquico o lexicográfico (no Pareto)? |  |  |
| ¿Solo reporto D cuando K = K_BKS? |  |  |
| ¿GRASP funciona sin modificación con mi fitness? |  |  |

**Si todas las respuestas son , su función de fitness es canónica.**

---

# PARTE 15: CÁLCULO CANÓNICO DEL GAP EN VRPTW (SOLOMON) CON GRASP

## Recordatorio Clave: Naturaleza Jerárquica del Problema

El VRPTW Solomon se evalúa con dos objetivos jerárquicos:

- **Objetivo Primario**: Minimizar el número de vehículos $K$
- **Objetivo Secundario**: Minimizar la distancia total $D$, **solo cuando $K$ es igual**

**Por tanto, el GAP solo tiene sentido para el objetivo secundario, y solo si el objetivo primario ya está satisfecho.**

---

## Condición Necesaria para Calcular GAP

El GAP en VRPTW **solo se calcula si se cumple**:

$$K_{\text{solución}} = K_{\text{BKS}}$$

donde:
- $K_{\text{solución}}$ = número de vehículos de la solución obtenida por GRASP
- $K_{\text{BKS}}$ = número de vehículos de la mejor solución conocida (Best Known Solution)

**Si esta condición NO se cumple**:

- El GAP **NO se calcula**
- El valor se reporta como "NA", "" o "not applicable"
- La solución se considera **jerárquicamente inferior**, independientemente de su distancia

**Esto es canónico.**

---

## GAP Absoluto (en Distancia)

Una vez cumplida la condición $K_{\text{solución}} = K_{\text{BKS}}$, el GAP absoluto se define como:

$$\text{GAP}_{\text{distancia}} = D_{\text{solución}} - D_{\text{BKS}}$$

donde:
- $D_{\text{solución}}$ = distancia total de la solución obtenida
- $D_{\text{BKS}}$ = distancia total de la mejor solución conocida

**Interpretación**:
- $\text{GAP}_{\text{distancia}} = 0$  se iguala la BKS
- $\text{GAP}_{\text{distancia}} > 0$  solución peor
- $\text{GAP}_{\text{distancia}} < 0$  mejora sobre la BKS (poco común, pero válido)

---

## GAP Relativo o Porcentaje de GAP (%GAP)

El %GAP canónico se define como:

$$\%\text{GAP} = \frac{D_{\text{solución}} - D_{\text{BKS}}}{D_{\text{BKS}}} \times 100$$

**Condición**: Se calcula únicamente si $K_{\text{solución}} = K_{\text{BKS}}$

**Interpretación**:
- $\%\text{GAP} = 0\%$  iguala la BKS
- $\%\text{GAP} > 0\%$  peor que la BKS
- $\%\text{GAP} < 0\%$  mejora la BKS

**Este es el indicador más usado en tablas comparativas.**

---

## Qué Hacer Cuando $K_{\text{solución}} > K_{\text{BKS}}$

**Caso jerárquicamente inferior.**

**Regla canónica**:

- No se reporta GAP de distancia
- Se reporta únicamente:
  - $K_{\text{solución}}$
  - $\Delta K = K_{\text{solución}} - K_{\text{BKS}}$

### Ejemplo Correcto de Reporte

**Instancia R101:**
- $K = 5$ (BKS = 4)
- GAP_distancia = NA
- %GAP = NA

### Ejemplo Incorrecto (Muy Común, pero MAL)

> "K = 5, distancia = 1200, GAP = 1.2 %"  **NO es canónico**

---

## GAP en Análisis Estadístico (Múltiples Ejecuciones)

En análisis con múltiples ejecuciones:

- El %GAP promedio **se calcula solo sobre ejecuciones donde $K = K_{\text{BKS}}$**
- Debe reportarse también:
  - **Porcentaje de ejecuciones que alcanzan $K_{\text{BKS}}$**

### Ejemplo de Reporte Correcto

> "Para la instancia RC101, el algoritmo alcanzó $K_{\text{BKS}}$ en el 83 % de las ejecuciones, con un %GAP promedio de 1.7 %."

**Nunca promediar GAP incluyendo ejecuciones con $K > K_{\text{BKS}}$.**

---

## GAP Agregado por Familia de Instancias

Para familias C, R y RC:

- El %GAP promedio por familia **se calcula solo sobre instancias donde $K = K_{\text{BKS}}$**
- Se debe reportar explícitamente:
  - **Porcentaje de instancias de la familia donde $K_{\text{BKS}}$ fue alcanzado**

Esto mantiene la coherencia jerárquica.

### Ejemplo de Tabla Canónica por Familia

| Familia | N Instancias | %Instancias_K_BKS | %GAP_mean | %GAP_std |
|---------|---------------|--------------------|-----------|----------|
| C | 9 | 100% | 0.08% | 0.05% |
| R | 12 | 83% | 0.44% | 0.22% |
| RC | 8 | 75% | 0.61% | 0.38% |

**Nota**: %GAP_mean y %GAP_std se calculan solo sobre instancias donde K_BKS fue alcanzado.

---

## Resumen Operativo (Regla de Oro)

**Regla canónica absoluta**:

$$\text{Si } K_{\text{solución}} \neq K_{\text{BKS}} \Rightarrow \text{GAP NO existe}$$

$$\text{Si } K_{\text{solución}} = K_{\text{BKS}} \Rightarrow \text{GAP} = \frac{D_{\text{solución}} - D_{\text{BKS}}}{D_{\text{BKS}}} \times 100$$

---

## Validación: ¿Mi Cálculo de GAP es Canónico?

Use esta lista de control:

| Pregunta | Sí =  | No =  |
|----------|--------|--------|
| ¿Verifico que $K_{\text{solución}} = K_{\text{BKS}}$ antes de calcular GAP? |  |  |
| ¿Reporto "NA" cuando la condición no se cumple? |  |  |
| ¿Calculo %GAP como $(D_{\text{solución}} - D_{\text{BKS}}) / D_{\text{BKS}} \times 100$? |  |  |
| ¿Reporto explícitamente % de instancias/ejecuciones con K_BKS? |  |  |
| ¿Promediar GAP solo sobre casos donde K = K_BKS? |  |  |
| ¿Distingo entre K_mean y distancia media (solo a K=K_BKS)? |  |  |
| ¿Nunca reporto GAP para soluciones con $K > K_{\text{BKS}}$? |  |  |

**Si todas las respuestas son , su cálculo de GAP es canónico.**

---

## Resumen en una Frase (Canónica)

**En VRPTW con GRASP, el GAP se calcula exclusivamente sobre la distancia total y únicamente cuando la solución alcanza el mismo número de vehículos que la mejor solución conocida; en caso contrario, el GAP no se define y la solución se considera jerárquicamente inferior.**


---

# PARTE 16: COMPONENTE MATEMÁTICA CANÓNICA DEL VRPTW COMPATIBLE CON SOLOMON C1, C2, R1, R2, RC1, RC2

## Grafo del Problema

El VRPTW se define sobre un grafo completo dirigido:

$$G = (V, A)$$

donde:

- $V = \{0, 1, 2, \ldots, n\}$ es el conjunto de nodos
- $A = \{(i, j) : i, j \in V, i \neq j\}$ es el conjunto de arcos

- El nodo 0 representa el **depósito**.
- Los nodos $1, \ldots, n$ representan **clientes**.

**Esta definición es idéntica para todas las familias Solomon.**

---

## Parámetros Espaciales y Temporales

Cada nodo $i \in V$ tiene coordenadas espaciales $(x_i, y_i)$.

Para cada arco $(i, j) \in A$ se definen:

- $c_{ij}$ = distancia euclidiana entre $i$ y $j$
- $t_{ij}$ = tiempo de viaje entre $i$ y $j$

**En los datasets de Solomon se cumple canónicamente**:

$$c_{ij} = t_{ij}$$

---

## Parámetros de los Clientes

Para cada cliente $i \in \{1, \ldots, n\}$:

- $q_i$ = demanda del cliente $i$
- $[a_i, b_i]$ = ventana de tiempo del cliente $i$
- $s_i$ = tiempo de servicio del cliente $i$

Para el depósito $(i = 0)$:

- $q_0 = 0$
- $s_0 = 0$
- $[a_0, b_0]$ = ventana de tiempo del depósito

**Las diferencias entre C1, C2, R1, R2, RC1 y RC2 se reflejan exclusivamente en los valores de $a_i$ y $b_i$, no en la estructura del modelo.**

---

## Parámetros de los Vehículos

- $Q$ = capacidad máxima de cada vehículo
- $K$ = número de vehículos utilizados

**En Solomon**:
- Los vehículos son homogéneos
- El número de vehículos disponibles se asume suficientemente grande
- **El objetivo es minimizar $K$**

---

## Variables de Decisión

### 5.1 Variable de Enrutamiento

$$x_{ij} = \begin{cases}
1 & \text{si un vehículo viaja directamente del nodo } i \text{ al nodo } j \\
0 & \text{en caso contrario}
\end{cases}$$

para todo $(i, j) \in A$.

### 5.2 Variable Temporal

$$t_i = \text{instante de inicio del servicio en el nodo } i$$

para todo $i \in V$.

---

## Función Objetivo (Canónica, Jerárquica)

El VRPTW Solomon se formula como un problema de optimización jerárquica:

**Objetivo Primario**:
$$\text{Minimizar } K$$

**Objetivo Secundario**:
$$\text{Minimizar } \sum_{i \in V} \sum_{j \in V} c_{ij} \cdot x_{ij}$$

**Formalmente, la función objetivo se expresa como una función lexicográfica**:

$$\text{Minimizar} \quad \left( K, \sum_{i \in V} \sum_{j \in V} c_{ij} \cdot x_{ij} \right)$$

**Esta definición es válida para C1, C2, R1, R2, RC1 y RC2.**

---

## Restricciones del Modelo

### 7.1 Restricción de Visita Única

Cada cliente debe ser visitado exactamente una vez:

$$\sum_{i \in V, i \neq j} x_{ij} = 1 \quad \forall j \in \{1, \ldots, n\}$$

### 7.2 Restricción de Salida Única

Desde cada cliente se debe salir exactamente una vez:

$$\sum_{j \in V, j \neq i} x_{ij} = 1 \quad \forall i \in \{1, \ldots, n\}$$

### 7.3 Restricciones del Depósito (Vehículos)

El número de rutas activas define $K$:

$$\sum_{j \in V, j \neq 0} x_{0j} = K$$

$$\sum_{i \in V, i \neq 0} x_{i0} = K$$

**Cada vehículo parte del depósito y regresa a él.**

### 7.4 Restricciones de Capacidad

La carga total de cada ruta no puede exceder la capacidad $Q$.

Esta restricción se implementa mediante:
- formulaciones de flujo, o
- restricciones auxiliares equivalentes.

### 7.5 Restricciones de Ventanas de Tiempo

El servicio debe comenzar dentro de la ventana permitida:

$$a_i \leq t_i \leq b_i \quad \forall i \in V$$

**Estas restricciones son más estrictas en instancias tipo 1 (C1, R1, RC1) que en tipo 2.**

### 7.6 Restricciones de Precedencia Temporal

Si un vehículo viaja de $i$ a $j$, entonces:

$$t_j \geq t_i + s_i + t_{ij} - M(1 - x_{ij}) \quad \forall (i, j) \in A$$

donde $M$ es una constante suficientemente grande.

### 7.7 Eliminación de Subtours

Se incorporan restricciones adicionales para evitar ciclos que no incluyan al depósito, tales como:

- Restricciones MTZ
- Restricciones de flujo
- U otras formulaciones equivalentes

---

## Dominio de las Variables

$$x_{ij} \in \{0, 1\}$$

$$t_i \geq 0$$

---

## Observaciones Específicas para Solomon

- **Tamaño estándar**: Todas las instancias tienen exactamente 100 clientes.
- **Vehículos**: No existe un límite explícito superior para $K$.
- **Diferencias espaciales**: Las diferencias entre C, R y RC son espaciales.
- **Diferencias temporales**: Las diferencias entre tipo 1 y tipo 2 son temporales.
- **Invarianza del modelo**: El modelo matemático **no cambia entre familias**, solo los parámetros.

---

## Resumen Final (Canónico)

**La componente matemática del VRPTW compatible con los datasets de Solomon se define como un problema de optimización jerárquica sobre un grafo dirigido, cuyo objetivo es minimizar primero el número de vehículos y luego la distancia total, sujeto a restricciones de visita única, capacidad, ventanas de tiempo y consistencia temporal.**

**Las seis familias Solomon (C1, C2, R1, R2, RC1 y RC2) comparten exactamente la misma formulación matemática; sus diferencias residen únicamente en los datos de entrada.**


---

# PARTE 17: DATASETS SOLOMON - RUTAS Y COMPATIBILIDAD TOTAL DEL PROYECTO

## Resumen: 56 Instancias Totales Clasificadas en 6 Familias

El proyecto **VRPTW-GRASP** es **100% compatible** con los datasets estándar de Solomon. Todas las 56 instancias están disponibles y organizadas en 6 familias temáticas.

| Familia | Tipo | N Instancias | Rango | Características |
|---------|------|--------------|-------|-----------------|
| **C1** | Clustered, Tight TW | 9 | C101-C109 | Clientes agrupados, ventanas estrictas |
| **C2** | Clustered, Wide TW | 8 | C201-C208 | Clientes agrupados, ventanas amplias |
| **R1** | Random, Tight TW | 12 | R101-R112 | Distribución aleatoria, ventanas estrictas |
| **R2** | Random, Wide TW | 11 | R201-R211 | Distribución aleatoria, ventanas amplias |
| **RC1** | Mixed, Tight TW | 8 | RC101-RC108 | Clustering + aleatoriedad, ventanas estrictas |
| **RC2** | Mixed, Wide TW | 8 | RC201-RC208 | Clustering + aleatoriedad, ventanas amplias |
| **TOTAL** | - | **56** | - | - |

---

## Estructura de Directorios de Datasets

La estructura recomendada para el proyecto es:

```
proyecto-raiz/
 datasets/
    C1/
       C101.csv
       C102.csv
       C103.csv
       C104.csv
       C105.csv
       C106.csv
       C107.csv
       C108.csv
       C109.csv
   
    C2/
       C201.csv
       C202.csv
       C203.csv
       C204.csv
       C205.csv
       C206.csv
       C207.csv
       C208.csv
   
    R1/
       R101.csv
       R102.csv
       R103.csv
       R104.csv
       R105.csv
       R106.csv
       R107.csv
       R108.csv
       R109.csv
       R110.csv
       R111.csv
       R112.csv
   
    R2/
       R201.csv
       R202.csv
       R203.csv
       R204.csv
       R205.csv
       R206.csv
       R207.csv
       R208.csv
       R209.csv
       R210.csv
       R211.csv
   
    RC1/
       RC101.csv
       RC102.csv
       RC103.csv
       RC104.csv
       RC105.csv
       RC106.csv
       RC107.csv
       RC108.csv
   
    RC2/
       RC201.csv
       RC202.csv
       RC203.csv
       RC204.csv
       RC205.csv
       RC206.csv
       RC207.csv
       RC208.csv
   
    documentation/
        Solomon_README.md
        best_known_solutions.txt
        instance_characteristics.csv

 src/
    core/
       problem.py
       solution.py
       evaluation.py
   
    operators/
       [22 operadores específicos para VRPTW]
   
    metaheuristic/
       grasp_core.py
   
    gaa/
       ast_nodes.py
       grammar.py
       generator.py
       interpreter.py
   
    utils/
        output_manager.py
        data_loader.py
        metrics.py

 config/
    config.yaml

 scripts/
    demo_experimentation_quick.py
    demo_experimentation_full.py
    validate_datasets.py

 output/
     [Resultados por sesión, con timestamps]
```

---

## Especificación: Familia C1 (Clustered, Tight Time Windows)

**9 instancias**: C101, C102, ..., C109

**Características**:
- Clientes geográficamente agrupados en 4 clusters
- Ventanas de tiempo **restrictivas** (tipo 1)
- Problema **menos difícil** (K_BKS bajo)
- **Dificultad esperada**: Baja-media

**Ubicación recomendada**: `datasets/C1/*.csv`

**Uso en experimentos**: 
- Validación rápida (quick experiments: 9 instancias  1 seed = 9 ejecuciones)
- Benchmark de viabilidad

---

## Especificación: Familia C2 (Clustered, Wide Time Windows)

**8 instancias**: C201, C202, ..., C208

**Características**:
- Clientes geográficamente agrupados en 4 clusters
- Ventanas de tiempo **amplias** (tipo 2)
- Problema **menos difícil** (K_BKS bajo)
- **Dificultad esperada**: Muy baja

**Ubicación recomendada**: `datasets/C2/*.csv`

**Uso en experimentos**:
- Validación rápida (quick experiments)
- Baseline de viabilidad

---

## Especificación: Familia R1 (Random, Tight Time Windows)

**12 instancias**: R101, R102, ..., R112

**Características**:
- Clientes distribuidos **aleatoriamente** (no hay clustering)
- Ventanas de tiempo **restrictivas** (tipo 1)
- Problema **muy difícil** (K_BKS alto)
- **Dificultad esperada**: Alta

**Ubicación recomendada**: `datasets/R1/*.csv`

**Uso en experimentos**:
- Evaluación completa (full experiments: 12  1 = 12 ejecuciones)
- Caso desafiante

---

## Especificación: Familia R2 (Random, Wide Time Windows)

**11 instancias**: R201, R202, ..., R211

**Características**:
- Clientes distribuidos **aleatoriamente**
- Ventanas de tiempo **amplias** (tipo 2)
- Problema **muy difícil** (K_BKS alto)
- **Dificultad esperada**: Media-alta

**Ubicación recomendada**: `datasets/R2/*.csv`

**Uso en experimentos**:
- Evaluación completa (full experiments)
- Caso desafiante

---

## Especificación: Familia RC1 (Mixed, Tight Time Windows)

**8 instancias**: RC101, RC102, ..., RC108

**Características**:
- Clientes con **clustering parcial** + distribución aleatoria
- Ventanas de tiempo **restrictivas** (tipo 1)
- Problema **muy difícil** (K_BKS medio-alto)
- **Dificultad esperada**: Alta

**Ubicación recomendada**: `datasets/RC1/*.csv`

**Uso en experimentos**:
- Evaluación completa (full experiments)
- Caso equilibrado (clustering + aleatoriedad)

---

## Especificación: Familia RC2 (Mixed, Wide Time Windows)

**8 instancias**: RC201, RC202, ..., RC208

**Características**:
- Clientes con **clustering parcial** + distribución aleatoria
- Ventanas de tiempo **amplias** (tipo 2)
- Problema **muy difícil** (K_BKS medio-alto)
- **Dificultad esperada**: Media-alta

**Ubicación recomendada**: `datasets/RC2/*.csv`

**Uso en experimentos**:
- Evaluación completa (full experiments)
- Caso equilibrado

---

## Garantía de Compatibilidad: 100% VRPTW Solomon

**El proyecto VRPTW-GRASP es 100% compatible con**:

 **Formato de datos**: CSV estándar Solomon  
 **100 clientes por instancia**: Verificado en todas las 56  
 **Parámetros estándar**: q_i, [a_i, b_i], s_i, (x_i, y_i)  
 **Modelo matemático único**: Idéntico para C, R, RC (diferencias solo en datos)  
 **Función de fitness jerárquica**: K  D validada para todas las familias  
 **Métrica canónica**: %GAP calculado condicionalmente a K = K_BKS  
 **Restricciones**: Factibilidad garantizada (capacidad + ventanas de tiempo)  
 **Distancia euclidiana**: c_ij = t_ij confirmado en Solomon  

---

## Flujo de Carga de Datos Recomendado

```python
# Pseudocódigo
from pathlib import Path
from data_loader import load_solomon_instance

# Definir ruta base
dataset_root = Path("datasets")

# Cargar familia
families = ["C1", "C2", "R1", "R2", "RC1", "RC2"]

for family in families:
    family_path = dataset_root / family
    instances = family_path.glob("*.csv")
    
    for instance_file in instances:
        instance = load_solomon_instance(instance_file)
        # instance.n_customers = 100
        # instance.parameters = {q_i, [a_i, b_i], s_i, c_ij}
        # instance.is_feasible() -> True/False después de evaluar
```

---

## Conteo Total: Verificación Aritmética

| Familia | Instancias |
|---------|-----------|
| C1 | 9 |
| C2 | 8 |
| R1 | 12 |
| R2 | 11 |
| RC1 | 8 |
| RC2 | 8 |
| **TOTAL** | **56** |

**Benchmark estándar**: 56 instancias  100 clientes = 5,600 clientes totales en evaluación

---

## Declaración de Compatibilidad

> **Este proyecto VRPTW-GRASP es un solver de propósito general para el VRPTW basado en GRASP y diseñado específicamente para ser completamente compatible con los 56 datasets estándar de Solomon (C1, C2, R1, R2, RC1, RC2). Todas las restricciones matemáticas, parámetros de entrada y criterios de evaluación se adhieren a la especificación canónica de Solomon VRPTW.**

