# Arquitectura KBP-SA: Guía Visual para Replicar

## 🗺️ Mapa de la Arquitectura

```
╔════════════════════════════════════════════════════════════════════╗
║                     KBP-SA Architecture Map                       ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  ┌─────────────────────────────────────────────────────────────┐ ║
║  │  CAPA 0: DATA LAYER                                         │ ║
║  │  ├── datasets/low_dimensional/ (n=4-23)                     │ ║
║  │  ├── datasets/large_scale/ (n=100-10000)                    │ ║
║  │  └── config/config.yaml (parámetros)                        │ ║
║  └─────────────────────────────────────────────────────────────┘ ║
║           │                                   │                   ║
║           ▼                                   ▼                   ║
║  ┌──────────────────────────┐      ┌──────────────────────────┐ ║
║  │ CAPA 1: CORE             │      │ CAPA 4: GAA             │ ║
║  ├──────────────────────────┤      ├──────────────────────────┤ ║
║  │ problem.py               │      │ grammar.py               │ ║
║  │  ↓ KnapsackProblem       │      │  ↓ Define qué es válido  │ ║
║  │  ├─ n, capacity, values  │      │                          │ ║
║  │  └─ weights              │      │ ast_nodes.py             │ ║
║  │                          │      │  ↓ Nodos de árbol        │ ║
║  │ solution.py              │      │                          │ ║
║  │  ↓ KnapsackSolution      │      │ generator.py             │ ║
║  │  ├─ x (binario)          │      │  ↓ Genera algoritmos     │ ║
║  │  ├─ value, weight        │      │                          │ ║
║  │  └─ is_feasible          │      │ interpreter.py           │ ║
║  │                          │      │  ↓ Ejecuta AST           │ ║
║  │ evaluation.py            │      │                          │ ║
║  │  ↓ Métricas             │      └──────────────────────────┘ ║
║  │  ├─ fitness             │              │                     ║
║  │  ├─ gap                 │              │                     ║
║  │  └─ infeasibility       │              │                     ║
║  └──────────────────────────┘              │                     ║
║           │                                 │                     ║
║           ▼                                 ▼                     ║
║  ┌──────────────────────────────────────────────────────────────┐ ║
║  │ CAPA 2: OPERATORS                                            │ ║
║  ├──────────────────────────────────────────────────────────────┤ ║
║  │ constructive.py          improvement.py   perturbation.py  │ ║
║  │ ├─ GreedyByValue        ├─ FlipBestItem  ├─ RandomFlip    │ ║
║  │ ├─ GreedyByWeight       ├─ FlipWorstItem ├─ ShakeByRemoval│ ║
║  │ ├─ GreedyByRatio        ├─ OneExchange   └─ DestroyRepair │ ║
║  │ └─ RandomConstruct      └─ TwoExchange                      │ ║
║  │                                                             │ ║
║  │ repair.py                                                  │ ║
║  │ ├─ RepairByRemoval                                         │ ║
║  │ └─ RepairByGreedy                                          │ ║
║  └──────────────────────────────────────────────────────────────┘ ║
║           │                                                       ║
║           ▼                                                       ║
║  ┌──────────────────────────────────────────────────────────────┐ ║
║  │ CAPA 3: METAHEURISTIC (Simulated Annealing)                 │ ║
║  ├──────────────────────────────────────────────────────────────┤ ║
║  │ sa_core.py                                                 │ ║
║  │  SimulatedAnnealing (Motor principal)                       │ ║
║  │  ├─ run()  [Bucle principal]                               │ ║
║  │  │  ├─ Solución inicial (constructive)                     │ ║
║  │  │  ├─ While T > T_min:                                     │ ║
║  │  │  │  ├─ For iter in range(iter_per_temp):               │ ║
║  │  │  │  │  ├─ neighbor = Operator.move(solution)            │ ║
║  │  │  │  │  ├─ ΔE = fitness(neighbor) - fitness(solution)   │ ║
║  │  │  │  │  ├─ if Metropolis.accept(ΔE, T):                │ ║
║  │  │  │  │  │  └─ solution = neighbor                        │ ║
║  │  │  │  │  └─ track metrics                                 │ ║
║  │  │  │  └─ T = cooling_schedule.next_temp(T)               │ ║
║  │  │  └─ return best_solution                                │ ║
║  │                                                             │ ║
║  │ cooling_schedules.py         acceptance.py                 │ ║
║  │ ├─ GeometricCooling          ├─ MetropolisCriterion       │ ║
║  │ ├─ LinearCooling             └─ Prob = exp(-ΔE/T)         │ ║
║  │ └─ ExponentialCooling                                      │ ║
║  └──────────────────────────────────────────────────────────────┘ ║
║           │                                                       ║
║           ▼                                                       ║
║  ┌──────────────────────────────────────────────────────────────┐ ║
║  │ CAPA 5: EXPERIMENTATION                                    │ ║
║  ├──────────────────────────────────────────────────────────────┤ ║
║  │ runner.py          metrics.py          visualization.py    │ ║
║  │ ├─ BatchRunner     ├─ compute_gap      ├─ plot_boxplot     │ ║
║  │ ├─ ExecutionLog    ├─ compute_quality  ├─ plot_gap_evolution
║  │ └─ track_stats     └─ compute_time     ├─ plot_acceptance  │ ║
║  │                                        └─ export_ast       │ ║
║  │                                                             │ ║
║  │ statistics.py      tracking.py         ast_visualization.py│ ║
║  │ ├─ mean, std       ├─ log_variable     └─ render_ast       │ ║
║  │ ├─ percentiles     ├─ log_iteration                        │ ║
║  │ └─ correlation     └─ get_execution_log                    │ ║
║  └──────────────────────────────────────────────────────────────┘ ║
║           │                                                       ║
║           ▼                                                       ║
║  ┌──────────────────────────────────────────────────────────────┐ ║
║  │ OUTPUT                                                      │ ║
║  ├──────────────────────────────────────────────────────────────┤ ║
║  │ output/                                                     │ ║
║  │ ├── low_dimensional_20251231_120000/                       │ ║
║  │ │   ├── results.csv           (todas las métricas)         │ ║
║  │ │   ├── statistics.json       (agregadas)                  │ ║
║  │ │   └── figures/                                           │ ║
║  │ │       ├── boxplot.png       (comparación algoritmos)     │ ║
║  │ │       ├── gap_evolution.png (progreso temporal)          │ ║
║  │ │       ├── acceptance.png    (tasas de aceptación)        │ ║
║  │ │       └── best_algorithm_ast.png (árbol del mejor)       │ ║
║  │ └── large_scale_20251231_120000/ (idem)                    │ ║
║  └──────────────────────────────────────────────────────────────┘ ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Flujo de Ejecución

```
┌─────────────────────────────────────┐
│   1. Load Dataset                   │
│   data = loader.load('f1.json')     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   2. Create Problem                 │
│   problem = KnapsackProblem.from_dict(data)
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   3a. Generate Algorithm (GAA)      │  OR  │  3b. Use Fixed SA
│   ast = generator.random_algorithm()│     │   sa = SA(problem)
│   ✓ validate(ast)                   │     │
└────────────┬────────────────────────┘     │
             │                              │
             └──────────────┬───────────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │ 4. Execute       │
                    │ result = sa.run()│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ 5. Evaluate      │
                    │ metrics =        │
                    │  evaluator.eval()│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ 6. Visualize     │
                    │ plot(metrics)    │
                    │ export_ast()     │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ output/          │
                    │ ├── results.csv  │
                    │ ├── *.json       │
                    │ └── figures/*.png│
                    └──────────────────┘
```

---

## 🎯 Comparación: KBP-SA vs Estructura Deficiente

### **Ejemplo: Proyecto SIN Buenas Prácticas**

```python
# ❌ MALO: Todo en un archivo
# main.py (2000+ líneas)

import numpy as np
import matplotlib.pyplot as plt

# Problema hardcodeado
CAPACITY = 100
VALUES = [10, 20, 30, 40, 50, 15, 25, 35, 45, 55]
WEIGHTS = [5, 10, 15, 20, 25, 8, 12, 18, 22, 28]

# Parámetros hardcodeados
T0 = 100
ALPHA = 0.95
T_MIN = 0.01

class SimulatedAnnealing:
    def run(self):
        # Mezcla de responsabilidades:
        # - Crear solución inicial
        # - Aplicar operadores
        # - Calcular fitness
        # - Aceptar/rechazar
        # - Guardar gráficas
        # - Logging
        pass

def main():
    # Acoplamiento fuerte
    sa = SimulatedAnnealing()
    results = sa.run()
    # Análisis hardcodeado
    plt.plot(results['fitness'])
    plt.savefig('output.png')

if __name__ == '__main__':
    main()
```

**Problemas**:
- ❌ Imposible rehusar código
- ❌ Difícil de testear
- ❌ Cambios cascada
- ❌ Sin documentación clara
- ❌ Parámetros hardcodeados

---

### **Ejemplo: KBP-SA (BUENO)**

```python
# ✅ BUENO: Separación clara

# 1. core/problem.py
from dataclasses import dataclass
import numpy as np

@dataclass
class KnapsackProblem:
    n: int
    capacity: int
    values: np.ndarray
    weights: np.ndarray
    
    def __post_init__(self):
        # Validaciones
        assert len(self.values) == self.n

# 2. operators/constructive.py
class GreedyByRatio:
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Solo responsabilidad: construir solución
        pass

# 3. metaheuristic/sa_core.py
class SimulatedAnnealing:
    def __init__(self, problem: KnapsackProblem, 
                 cooling: CoolingSchedule,
                 acceptance: AcceptanceCriterion,
                 initial_constructor: Callable):
        # Inyección de dependencias
        self.problem = problem
        self.cooling = cooling
        self.acceptance = acceptance
        self.initial_constructor = initial_constructor
    
    def run(self) -> ExecutionResult:
        # Solo responsabilidad: algoritmo SA

# 4. data/loader.py
class DataLoader:
    @staticmethod
    def load(path: str) -> Dict:
        # Solo responsabilidad: cargar datos

# 5. experimentation/metrics.py
class Metrics:
    @staticmethod
    def compute_gap(result, optimal):
        # Solo responsabilidad: calcular métricas

# 6. experimentation/visualization.py
class Visualizer:
    @staticmethod
    def plot_boxplot(results, output_dir):
        # Solo responsabilidad: visualizar

# 7. scripts/demo_experimentation.py
def main():
    # Orquestación clara
    problem = loader.load('f1.json')
    sa = SimulatedAnnealing(problem, 
                            GeometricCooling(),
                            MetropolisCriterion(),
                            GreedyByRatio)
    result = sa.run()
    metrics = evaluator.evaluate(result)
    visualizer.plot_boxplot(metrics, 'output/')
```

**Ventajas**:
- ✅ Cada clase una responsabilidad
- ✅ Fácil de testear (cada componente aislado)
- ✅ Reutilizable (usar en otro proyecto)
- ✅ Mantenible (cambios localizados)
- ✅ Extensible (nuevos operadores sin tocar nada)

---

## 🏗️ Cómo Replicar para Otro Problema

### **Caso de Uso: Crear GCP-SA (Graph Coloring + SA)**

```
gcp-sa/                          (copia estructura de kbp-sa/)
├── core/
│   ├── __init__.py
│   ├── problem.py               (adaptado: ColoringProblem)
│   ├── solution.py              (adaptado: ColoringSolution)
│   └── evaluation.py            (adaptado: ColoringEvaluator)
│
├── operators/
│   ├── __init__.py
│   ├── constructive.py          (ColoringGreedy, RandomColoring)
│   ├── improvement.py           (MoveVertex, SwapColors)
│   ├── perturbation.py          (RandomRecolor, KempeChain)
│   └── repair.py                (GreedyRepair, MinColorsRepair)
│
├── metaheuristic/
│   ├── __init__.py
│   ├── sa_core.py               (reutilizar con tipos genéricos)
│   ├── cooling_schedules.py     (reutilizar)
│   └── acceptance.py            (reutilizar)
│
├── gaa/
│   ├── __init__.py
│   ├── grammar.py               (ColoringGrammar)
│   ├── ast_nodes.py             (adaptar nodos)
│   ├── generator.py             (reutilizar)
│   └── interpreter.py           (reutilizar)
│
├── data/
│   ├── __init__.py
│   ├── loader.py                (ColoringLoader)
│   └── validator.py             (ColoringValidator)
│
├── experimentation/
│   ├── __init__.py
│   ├── metrics.py               (ColoringMetrics)
│   ├── visualization.py         (reutilizar)
│   ├── runner.py                (reutilizar)
│   └── tracking.py              (reutilizar)
│
├── tests/
│   └── test_core.py
│
├── scripts/
│   ├── test_quick.py
│   ├── demo_complete.py
│   ├── demo_experimentation.py
│   └── ...
│
├── datasets/
│   ├── small/                   (instancias pequeñas)
│   └── large/                   (instancias grandes)
│
├── config/
│   ├── config.yaml              (parámetros para GCP)
│   └── problema_metaheuristica.md
│
├── docs/
│   ├── QUICKSTART.md
│   ├── README_SISTEMA.md
│   └── ARCHITECTURE.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

**Adaptaciones clave por módulo**:

| Módulo | KBP-SA | GCP-SA | Cambio |
|--------|--------|--------|--------|
| `core/problem.py` | `KnapsackProblem(n, capacity, values, weights)` | `GraphColoringProblem(vertices, edges, colors)` | Problema específico |
| `core/solution.py` | `x: [0,1,1,0,...]` | `colors: [0,1,0,1,...]` | Representación específica |
| `operators/improvement.py` | `FlipBestItem` | `MoveVertex` | Operadores específicos |
| `evaluation.py` | `fitness = valor_total` | `fitness = vertices_coloreados` | Métrica específica |
| `gaa/grammar.py` | `Terminales de Knapsack` | `Terminales de Graph Coloring` | Dominio específico |
| `metaheuristic/sa_core.py` | REUTILIZAR | REUTILIZAR | Metaheurística genérica |
| `experimentation/runner.py` | REUTILIZAR | REUTILIZAR | Framework genérico |

---

## 📋 Checklist para Replicar la Estructura

- [ ] **Definir capas (Core → Operators → Metaheuristic → GAA → Experimentation)**
- [ ] **Crear `core/` con Problem, Solution, Evaluator**
- [ ] **Crear `operators/` modular (constructive, improvement, repair)**
- [ ] **Crear `metaheuristic/` con algoritmo genérico**
- [ ] **Crear `gaa/` con gramática del dominio**
- [ ] **Crear `data/` con loader y validator**
- [ ] **Crear `experimentation/` con metrics y visualization**
- [ ] **Crear `tests/` con pruebas de core**
- [ ] **Crear `scripts/` con escalera ejecutable**
- [ ] **Crear `docs/` con QUICKSTART**
- [ ] **Crear `config.yaml` centralizado**
- [ ] **Agregar type hints en todo**
- [ ] **Usar inyección de dependencias**
- [ ] **Documentar con docstrings y referencias**

---

## 🎓 Principios Clave

1. **Separación de Responsabilidades**: Cada clase/módulo = 1 cosa
2. **Inyección de Dependencias**: Constructor-based, no hardcodeado
3. **Tipos Explícitos**: Type hints en todo
4. **Configuración Centralizada**: YAML o JSON, no hardcodeado
5. **Testing Progresivo**: quick → demo → experiments → large_scale
6. **Documentación Ejecutable**: Scripts como ejemplos
7. **Modularidad**: Reutilizable en otros proyectos

