# VRPTW-GRASP Quickstart Guide

Guía rápida para usar VRPTW-GRASP (Vehicle Routing Problem with Time Windows - GRASP Solver)

## Descripción General

**VRPTW-GRASP** es una implementación completa de GRASP (Greedy Randomized Adaptive Search Procedure) para resolver el Problema de Ruteo de Vehículos con Ventanas de Tiempo (VRPTW).

- **Lenguaje**: Python 3.8+
- **Benchmarks**: Solomon (56 instancias en 6 familias)
- **Operadores**: 22 operadores (6 constructivos, 8 búsqueda local, 4 perturbación, 2 reparación)
- **Algoritmo**: GRASP con Variable Neighborhood Descent (VND)

## Instalación

### Requisitos
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install pandas numpy pyyaml
```

## Uso Rápido

### 1. Resolver una Instancia Individual

```bash
python run.py --family C1 --instance C101 --iterations 100
```

Parámetros disponibles:
- `--family`: Familia de instancias (C1, C2, R1, R2, RC1, RC2)
- `--instance`: Nombre de instancia (ej: C101, R202, RC108)
- `--iterations`: Número máximo de iteraciones (default: 100)
- `--alpha`: Parámetro RCL (default: 0.15)
- `--seed`: Seed para reproducibilidad
- `--time-limit`: Límite de tiempo en segundos

### 2. Resolver Familia Completa

```bash
python run.py --family C1 --iterations 50
```

Resuelve todas las instancias de la familia C1 (9 instancias).

### 3. Uso desde Python

```python
from data.loader import VRPTWDataLoader
from metaheuristic.grasp_core import solve_vrptw

# Cargar instancia
loader = VRPTWDataLoader('./datasets')
problem = loader.load_instance('C1', 'C101')

# Resolver
solution = solve_vrptw(
    problem,
    max_iterations=100,
    alpha_rcl=0.15,
    seed=42
)

# Ver solución
print(solution.info())
```

## Estructura del Proyecto

```
VRPTW-GRASP/
├── core/                 # Clases base
│   ├── problem.py        # VRPTWProblem
│   ├── solution.py       # VRPTWSolution
│   └── evaluation.py     # VRPTWEvaluator
├── data/                 # Carga de datos
│   ├── parser.py         # SolomonParser
│   └── loader.py         # VRPTWDataLoader
├── operators/            # Operadores de solución
│   ├── constructive.py   # 6 heurísticas constructivas
│   ├── local_search.py   # 8 operadores de mejora
│   ├── perturbation.py   # 4 operadores de perturbación
│   └── repair.py         # 2 operadores de reparación
├── metaheuristic/        # Algoritmo GRASP
│   └── grasp_core.py     # Implementación principal
├── datasets/             # Benchmarks Solomon
│   ├── C1/, C2/          # Instancias agrupadas
│   ├── R1/, R2/
│   └── RC1/, RC2/
├── run.py                # Script principal
├── demo.py               # Demostración rápida
└── README.md             # Este archivo
```

## Operadores

### Constructivos (6)
- **Nearest Neighbor**: Greedy simple, rápido
- **Savings**: Clarke-Wright, buena calidad
- **Nearest Insertion**: Inserción iterativa
- **Randomized Insertion**: Greedy randomizado con RCL
- **Time-Oriented NN**: Considera ventanas de tiempo
- **Regret Insertion**: Métrica de arrepentimiento

### Búsqueda Local (8)

Intra-ruta:
- **2-opt**: Invierte segmentos
- **Or-opt**: Reubica secuencias 1-3 clientes
- **3-opt**: Reestructuración (avanzado)
- **Relocate**: Reposiciona cliente

Inter-ruta:
- **Cross-Exchange**: Intercambia entre rutas
- **2-opt***: Intercambio de segmentos
- **Relocate-Inter**: Traslada cliente entre rutas
- **Swap**: Intercambia pares de clientes

### Perturbación (4)
- **Ejection Chain**: Expulsión en cadena
- **Ruin & Recreate**: Destruye y reconstruye
- **Random Removal**: Remueve clientes aleatorios
- **Route Elimination**: Elimina ruta completa

### Reparación (2)
- **Capacity Repair**: Arregla violaciones de capacidad
- **Time Window Repair**: Arregla violaciones de tiempo

## Parámetros GRASP

```python
from metaheuristic.grasp_core import GRASPParameters

params = GRASPParameters()
params.max_iterations = 100          # Máximo iteraciones
params.alpha_rcl = 0.15              # RCL: 0=greedy, 1=random
params.stagnation_limit = 20         # Iteraciones antes de perturbar
params.time_limit = None             # Límite de tiempo (segundos)
params.construction_method = 'randomized'  # Método constructivo
params.seed = 42                     # Seed para reproducibilidad
params.log_level = 1                 # 0=silent, 1=minimal, 2=detailed
```

## Datasets

### Familias Solomon
- **C1** (9): Agrupadas, ventanas estrictas
- **C2** (8): Agrupadas, ventanas amplias
- **R1** (12): Aleatorias, ventanas estrictas
- **R2** (11): Aleatorias, ventanas amplias
- **RC1** (8): Mixtas, ventanas estrictas
- **RC2** (8): Mixtas, ventanas amplias

**Total**: 56 instancias, hasta 100 clientes cada una

### Formato
CSV con columnas: CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME

## Ejemplos de Uso

### Ejemplo 1: Resolver C101 con parámetros por defecto
```bash
python run.py --family C1 --instance C101
```

### Ejemplo 2: Resolver familia R1 con tiempo limitado
```bash
python run.py --family R1 --time-limit 300 --iterations 200
```

### Ejemplo 3: Reproducible seed
```bash
python run.py --family RC1 --instance RC101 --seed 42 --iterations 100
```

### Ejemplo 4: Desde código Python
```python
from pathlib import Path
from data.loader import VRPTWDataLoader
from metaheuristic.grasp_core import solve_vrptw, GRASPParameters

# Cargar datos
loader = VRPTWDataLoader('./datasets')

# Resolver C102
problem = loader.load_instance('C1', 'C102')

params = GRASPParameters()
params.max_iterations = 50
params.alpha_rcl = 0.2
params.seed = 123

solution = solve_vrptw(problem, 
    max_iterations=params.max_iterations,
    alpha_rcl=params.alpha_rcl,
    seed=params.seed,
    log_level=2
)

print(f"Cost: {solution.cost:.2f}")
print(f"Vehicles: {solution.num_routes()}")
```

## Evaluación

Las soluciones se evalúan de forma jerárquica:

1. **Viabilidad**: ¿Respeta todas las restricciones?
2. **Vehículos**: ¿Usa el mínimo número de vehículos?
3. **Distancia**: ¿Minimiza la distancia total?

Restricciones:
- Capacidad de vehículos
- Ventanas de tiempo de clientes
- Cobertura (todos visitados)

## Resultados Típicos

### C101 (50 iteraciones)
- Instancia: 100 clientes
- Límite inferior (vehículos): 10
- Solución GRASP: 10 vehículos, distancia 828.94
- **Calidad**: Óptimo en vehículos ✓

## Troubleshooting

### Error: "No module named 'pandas'"
```bash
pip install pandas numpy
```

### Error: "Could not load instance"
Verificar que el archivo existe en `datasets/{family}/{instance}.csv`

### Solución infactible
El GRASP incluye reparación automática. Si persiste:
- Aumentar `max_iterations`
- Cambiar `construction_method`
- Verificar dataset

## Performance Tips

1. **Iteraciones**: Más iteraciones = mejor solución, más tiempo
2. **Alpha RCL**: 
   - 0.05-0.10: Más greedy, soluciones rápidas
   - 0.15-0.20: Balance (recomendado)
   - 0.25-0.30: Más aleatorio, diversidad
3. **Seed**: Fijar seed para reproducibilidad
4. **Parallelización**: Ejecutar múltiples seeds en paralelo

## Referencias

- Solomon, M. M. (1987). "Algorithms for the Vehicle Routing and Scheduling Problems"
- Feo, T. A., & Resende, M. G. (1995). "Greedy Randomized Adaptive Search Procedures"
- Cordeau, J. F., et al. (2002). "Vehicle Routing"

## Licencia

Ver LICENSE file

## Autor

Desarrollado como parte del framework GAA (Genetic Algorithm Architect)
