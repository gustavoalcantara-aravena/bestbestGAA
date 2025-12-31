# Resumen: Estructura de KBP-SA en 1 Página

## 🎯 Lo Más Importante

La estructura de **KBP-SA** divide el código en 4 capas independientes que puedes reutilizar en **cualquier problema de optimización**:

```
CORE (problema específico)
    ↓↓↓
OPERATORS (transformaciones genéricas)
    ↓↓↓
METAHEURISTIC (algoritmo genérico)
    ↓↓↓
EXPERIMENTATION (análisis y visualización)
```

---

## 📦 Las 4 Capas Explicadas

### **Capa 1: CORE** (define QUÉ optimizamos)
- **Función**: Definición matemática del problema
- **Archivos**: `problem.py`, `solution.py`, `evaluation.py`
- **Características**:
  - Clases con `@dataclass`
  - Validaciones en `__post_init__`
  - Type hints explícitos
  - Métodos `from_dict()` y `to_dict()`
  
```python
@dataclass
class KnapsackProblem:
    n: int                    # número de ítems
    capacity: int             # capacidad
    values: np.ndarray        # valores
    weights: np.ndarray       # pesos
```

**Ejemplo KBP-SA**:
- `KnapsackProblem(n=100, capacity=500, values=[...], weights=[...])`
- Para replicar en otro proyecto: cambia solo esto

---

### **Capa 2: OPERATORS** (transformaciones elementales)
- **Función**: Crear, mejorar y reparar soluciones
- **Archivos**: `constructive.py`, `improvement.py`, `perturbation.py`, `repair.py`
- **Patrón**: Strategy Pattern (clases intercambiables)

```python
class GreedyByValue:
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Crear solución ordenando por valor

class GreedyByRatio:
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Crear solución ordenando por ratio valor/peso

class FlipBestItem:
    @staticmethod
    def move(solution: KnapsackSolution) -> KnapsackSolution:
        # Mejorar solución flipeando el mejor ítem
```

**Característica clave**: Cambiar operador NO requiere modificar SA

---

### **Capa 3: METAHEURISTIC** (algoritmo de búsqueda)
- **Función**: Orquestar la búsqueda
- **Archivos**: `sa_core.py`, `cooling_schedules.py`, `acceptance.py`
- **Patrón**: Inyección de dependencias

```python
sa = SimulatedAnnealing(
    problem=problem,
    cooling_schedule=GeometricCooling(alpha=0.95),
    acceptance=MetropolisCriterion(),
    initial_constructor=GreedyByRatio.construct,
    perturbation_operator=FlipBestItem.move
)

result = sa.run()  # Retorna {'best_value': X, 'time': Y, ...}
```

**Característica clave**: Todas las estrategias inyectadas = máxima flexibilidad

---

### **Capa 4: EXPERIMENTATION** (análisis y visualización)
- **Función**: Recopilar resultados, generar gráficas, estadísticas
- **Archivos**: `runner.py`, `metrics.py`, `visualization.py`, `statistics.py`

```python
runner = BatchRunner(problem)
results = runner.run_experiments(
    algorithms=[algo1, algo2, algo3],
    repetitions=10,
    output_dir='output/'
)

visualizer.plot_boxplot(results)     # Gráfica comparativa
visualizer.plot_gap_evolution(results)  # Progreso temporal
visualizer.export_ast(best_algorithm)   # Árbol sintáctico
```

---

## 🔄 Flujo de Ejecución Típico

```
1. LOAD PROBLEM
   ├─ datasets/low_dimensional/f1.json
   └─ → KnapsackProblem(n=100, capacity=500, ...)

2. CREATE SOLUTION
   ├─ operators.constructive.GreedyByRatio
   └─ → KnapsackSolution(x=[0,1,1,0,...], value=450, ...)

3. IMPROVE SOLUTION
   ├─ operators.improvement.FlipBestItem
   ├─ operators.improvement.OneExchange
   └─ → mejor KnapsackSolution(value=475)

4. RUN METAHEURISTIC
   ├─ metaheuristic.SimulatedAnnealing
   └─ → ExecutionResult(best=485, time=2.3s, ...)

5. ANALYZE RESULTS
   ├─ experimentation.metrics (gap, time, feasibility)
   ├─ experimentation.visualization (gráficas)
   └─ output/results.csv + figures/
```

---

## ✅ Patrones Clave a Memorizar

| Patrón | Dónde | Beneficio | Ejemplo |
|--------|-------|-----------|---------|
| `@dataclass` | Clases de datos | Validación + serialización | `KnapsackProblem(...)` |
| **Strategy** | Operadores | Intercambiables sin editar | `GreedyByValue`, `GreedyByRatio` |
| **Inyección** | Constructor | Máxima flexibilidad | `SimulatedAnnealing(..., cooling=X)` |
| **Type Hints** | Todas partes | IDE autocomplete | `def run(self, problem: KnapsackProblem)` |
| **Config.yaml** | Parámetros | Sin hardcodeo | `T0: 100, alpha: 0.95` |

---

## 🚀 Escalera de Ejecución

| Script | Tiempo | Propósito |
|--------|--------|----------|
| `test_quick.py` | 10s | ✅ Verificación rápida |
| `demo_complete.py` | 30s | ✅ Demo funcional |
| `demo_experimentation.py` | 2-5min | ✅ Experimentos + gráficas |
| `experiment_large_scale.py` | horas | ✅ Benchmark serio |

**Estrategia**: Cada script + verificador. El anterior debe pasar antes de correr el siguiente.

---

## 📋 Carpetas Importantes

```
core/
├── problem.py      ← Donde definir tu problema
├── solution.py     ← Representación de solución
└── evaluation.py   ← Cálculo de métricas

operators/
├── constructive.py ← Crear soluciones
├── improvement.py  ← Mejorar localmente
├── perturbation.py ← Escapar de mínimos
└── repair.py       ← Reparar infactibilidad

metaheuristic/
├── sa_core.py      ← Motor SA (reutilizable)
├── cooling_schedules.py
└── acceptance.py

scripts/
├── test_quick.py         ← 10s
├── demo_complete.py      ← 30s
├── demo_experimentation.py ← 5min
└── experiment_large_scale.py ← horas

config/
└── config.yaml     ← TODOS los parámetros
```

---

## 🎓 Cómo Replicar para Nuevo Problema

### Paso 1: Adaptar CORE
```python
# Cambiar SOLO esto
@dataclass
class GraphColoringProblem:
    vertices: int
    edges: List[Tuple[int, int]]
    colors: int
    
@dataclass
class ColoringSolution:
    assignment: np.ndarray  # [0,1,0,1,2,...]
```

### Paso 2: Adaptar OPERATORS
```python
# Cambiar SOLO lógica específica del dominio
class ColoringGreedyHeuristic:
    @staticmethod
    def construct(problem: GraphColoringProblem):
        # Lógica de coloring, no de knapsack
        pass

class MoveVertex:
    @staticmethod
    def move(solution: ColoringSolution):
        # Mover un vértice a otro color
        pass
```

### Paso 3: REUTILIZAR TODO LO DEMÁS
```python
# ✅ Usar tal cual
class SimulatedAnnealing:  # MISMO CÓDIGO
class GeometricCooling:    # MISMO CÓDIGO
class BatchRunner:         # MISMO CÓDIGO
class Visualizer:          # MISMO CÓDIGO
```

---

## 🎯 Lo Que Debes Hacer HOY

1. **Leer** [BUENAS_PRACTICAS_ESTRUCTURA.md](BUENAS_PRACTICAS_ESTRUCTURA.md)
   - Entiende separación de capas

2. **Mirar** [ARQUITECTURA_VISUAL_Y_REPLICACION.md](ARQUITECTURA_VISUAL_Y_REPLICACION.md)
   - Visualiza el flujo de datos

3. **Estudiar** [PATRONES_DE_CODIGO.md](PATRONES_DE_CODIGO.md)
   - Aprende @dataclass, Strategy, Inyección

4. **Usar** [CHECKLIST_PRACTICO.md](CHECKLIST_PRACTICO.md)
   - Paso a paso para tu proyecto

5. **Ejecutar** en KBP-SA:
   ```bash
   python scripts/test_quick.py              # Validación
   python scripts/demo_complete.py           # Demo
   python scripts/demo_experimentation.py    # Experimentos
   ```

---

## 📊 Métrica de Éxito

Tu proyecto tiene **buena estructura** cuando:

- ✅ Cambiar parámetro = editar `config.yaml`
- ✅ Agregar operador = crear nueva clase (sin tocar SA)
- ✅ Testear algoritmo = correr `test_quick.py`
- ✅ Generar gráficas = correr `demo_experimentation.py`
- ✅ Entender código = leer `ARCHITECTURE.md`
- ✅ Extender proyecto = copia estructura completa

Si alguno de esto requiere **editar código existente**, necesitas refactorizar.

---

## 🎓 Principios Finales

1. **Separación de Responsabilidades**: Cada clase = 1 cosa
2. **Abierto/Cerrado**: Agregar, no editar (Open/Closed Principle)
3. **Inversión de Control**: Inyectar estrategias (no hardcodear)
4. **Documentación Ejecutable**: Scripts como ejemplos
5. **Configuración Centralizada**: YAML, no código

**Aplica estos 5 principios y tu código será mantenible, testeable y reutilizable.**

---

## 🚀 ¡Listo para Empezar!

KBP-SA es un **blueprint probado** para proyectos de optimización. Úsalo como referencia para:

- ✅ Tus propios proyectos de optimización
- ✅ Mostrar buenas prácticas a colegas
- ✅ Enseñar arquitectura de software
- ✅ Documentar cómo trabajas

**Las carpetas y archivos que creé explican cada aspecto en detalle. Léelos en este orden:**

1. Este archivo (visión general)
2. `BUENAS_PRACTICAS_ESTRUCTURA.md` (principios)
3. `ARQUITECTURA_VISUAL_Y_REPLICACION.md` (visualización)
4. `PATRONES_DE_CODIGO.md` (implementación)
5. `CHECKLIST_PRACTICO.md` (paso a paso)

**¡Mucho éxito!** 🎉

