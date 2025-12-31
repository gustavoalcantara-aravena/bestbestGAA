# Checklist Práctico: Aplicar Buenas Prácticas de KBP-SA

## 📋 Guía Paso a Paso para Nuevos Proyectos

Use este checklist cuando cree un nuevo proyecto de optimización. Cada item está validado por la estructura exitosa de KBP-SA.

---

## ✅ FASE 1: Diseño y Planificación (Antes de Código)

- [ ] **Definir el problema matemático**
  - [ ] ¿Qué se optimiza? (minimizar/maximizar)
  - [ ] ¿Cuáles son las restricciones?
  - [ ] ¿Cuál es la representación de solución?
  - [ ] Documentar en `problema_metaheuristica.md`
  
  ```markdown
  # Definición Matemática
  Maximizar: Z = f(x)
  Sujeto a: g(x) ≤ 0
  Donde: x ∈ S (espacio de soluciones)
  ```

- [ ] **Identificar operadores necesarios**
  - [ ] ¿Cómo crear solución inicial? (constructive)
  - [ ] ¿Cómo mejorar localmente? (improvement)
  - [ ] ¿Cómo escapar de mínimos? (perturbation)
  - [ ] ¿Cómo reparar infactibilidad? (repair)

- [ ] **Elegir metaheurística**
  - [ ] ¿Simulated Annealing? (temperatura)
  - [ ] ¿Tabu Search? (lista tabú)
  - [ ] ¿Genético? (población)
  - [ ] Documentar en `config/problema_metaheuristica.md`

- [ ] **Preparar datasets**
  - [ ] Instancias pequeñas para desarrollo (5-20 items)
  - [ ] Instancias medianas para pruebas (20-100 items)
  - [ ] Instancias grandes para experimentos (100+ items)
  - [ ] Guardar en `datasets/low_dimensional/` y `datasets/large_scale/`

---

## ✅ FASE 2: Estructura de Carpetas

```
Tu_Proyecto/
├── core/                      # ← EMPIEZA AQUÍ
│   ├── __init__.py           # from .problem import MyProblem
│   ├── problem.py            # @dataclass MyProblem
│   ├── solution.py           # @dataclass MySolution
│   └── evaluation.py         # class MyEvaluator
│
├── operators/
│   ├── __init__.py
│   ├── constructive.py       # class Greedy1, Greedy2, ...
│   ├── improvement.py        # class LocalSearch1, LocalSearch2, ...
│   ├── perturbation.py       # class Shake, Destroy, ...
│   └── repair.py             # class Repair1, Repair2, ...
│
├── metaheuristic/
│   ├── __init__.py
│   ├── sa_core.py            # class SimulatedAnnealing (si usas SA)
│   ├── cooling_schedules.py  # class GeometricCooling, ...
│   └── acceptance.py         # class MetropolisCriterion, ...
│
├── gaa/
│   ├── __init__.py
│   ├── grammar.py            # class MyGrammar
│   ├── ast_nodes.py          # class ASTNode, ...
│   ├── generator.py          # def generate_algorithm()
│   └── interpreter.py        # class Interpreter
│
├── data/
│   ├── __init__.py
│   ├── loader.py             # class MyLoader
│   └── validator.py          # class MyValidator
│
├── experimentation/
│   ├── __init__.py
│   ├── runner.py             # class BatchRunner
│   ├── metrics.py            # class MyMetrics
│   ├── visualization.py      # def plot_*()
│   ├── statistics.py         # def mean, std, ...
│   └── tracking.py           # class ExecutionTracker
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py          # 10-20 tests
│   ├── test_*.py             # por módulo
│   └── TEST_RESULTS.md       # resultados documentados
│
├── scripts/
│   ├── test_quick.py         # ✅ ~10 segundos
│   ├── demo_complete.py      # ✅ ~30 segundos
│   ├── demo_experimentation.py # ✅ 2-5 minutos
│   ├── test_all_instances.py # ✅ benchmarks
│   └── experiment_large_scale.py # ✅ experimentos serios
│
├── config/
│   ├── config.yaml           # Todos los parámetros
│   └── problema_metaheuristica.md
│
├── docs/
│   ├── QUICKSTART.md         # Copia/pega listo
│   ├── README_SISTEMA.md     # Arquitectura completa
│   ├── ARCHITECTURE.md       # Diagramas
│   └── ploteos.md            # Especificación de gráficas
│
├── datasets/
│   ├── low_dimensional/      # Instancias pequeñas
│   │   ├── f1.json
│   │   ├── f2.json
│   │   └── ...
│   └── large_scale/          # Instancias grandes
│       ├── large1.json
│       └── ...
│
├── output/                    # .gitignore esto
│   ├── results.csv
│   └── figures/
│
├── .gitignore
├── requirements.txt
├── README.md
└── __init__.py
```

- [ ] **Crear estructura de carpetas**
  ```bash
  mkdir -p Tu_Proyecto/{core,operators,metaheuristic,gaa,data,experimentation,tests,scripts,config,docs,datasets/low_dimensional,datasets/large_scale,output}
  touch Tu_Proyecto/__init__.py
  ```

- [ ] **Crear `__init__.py` en cada carpeta**
  ```python
  # core/__init__.py
  from .problem import MyProblem
  from .solution import MySolution
  from .evaluation import MyEvaluator
  __all__ = ['MyProblem', 'MySolution', 'MyEvaluator']
  ```

---

## ✅ FASE 3: Implementar Core (Base Matemática)

### Paso 1: `core/problem.py`

- [ ] Crear clase Problem con `@dataclass`
  ```python
  from dataclasses import dataclass
  from typing import Optional
  import numpy as np
  
  @dataclass
  class MyProblem:
      """Descripción matemática del problema"""
      
      # Atributos del problema
      param1: int
      param2: np.ndarray
      param3: float = 1.0
      
      def __post_init__(self):
          """Validar después de __init__"""
          # Validaciones aquí
          assert self.param1 > 0
  ```

- [ ] Agregar métodos helper:
  - `from_dict(cls, data)` - crear desde diccionario/JSON
  - `to_dict(self)` - serializar a diccionario
  - `validate(self)` - chequeos adicionales

- [ ] Documentar con docstring:
  ```python
  """
  Mi Problema (0/1)
  
  Modelo Matemático:
  ------------------
  Maximizar: Z = f(x)
  
  Sujeto a:
      g(x) ≤ 0    (restricción)
      x ∈ {0,1}   (binario)
  
  Referencias:
      - Paper 2025: "..."
  """
  ```

### Paso 2: `core/solution.py`

- [ ] Crear clase Solution con `@dataclass`
  ```python
  @dataclass
  class MySolution:
      """Representación de una solución"""
      
      x: np.ndarray       # Decisión (binario, entero, real)
      value: float = None # Cache de fitness
      
      def __post_init__(self):
          # Validar que x es válido
          pass
      
      def copy(self):
          """Crear copia profunda"""
          return MySolution(x=self.x.copy())
      
      def is_feasible(self, problem: MyProblem) -> bool:
          """¿Respeta restricciones?"""
          pass
  ```

### Paso 3: `core/evaluation.py`

- [ ] Crear clase Evaluator
  ```python
  class MyEvaluator:
      """Calcula métricas de calidad"""
      
      @staticmethod
      def evaluate(solution: MySolution,
                   problem: MyProblem) -> Dict[str, Any]:
          """
          Evaluar solución
          
          Retorna Dict con:
              'fitness': valor objetivo
              'feasible': ¿respeta restricciones?
              'infeasibility': medida de violación
              ...
          """
          pass
  ```

- [ ] Chequear con `test_quick.py`:
  ```python
  # test_quick.py
  from core import MyProblem, MySolution, MyEvaluator
  
  problem = MyProblem(...)
  solution = MySolution(...)
  metrics = MyEvaluator.evaluate(solution, problem)
  
  assert 'fitness' in metrics
  assert 'feasible' in metrics
  print("✅ Core works!")
  ```

---

## ✅ FASE 4: Implementar Operadores

### Paso 1: `operators/constructive.py`

- [ ] Crear clase base abstracta
  ```python
  from abc import ABC, abstractmethod
  
  class ConstructiveOperator(ABC):
      @abstractmethod
      def construct(self, problem: MyProblem) -> MySolution:
          """Crear solución inicial"""
          pass
  ```

- [ ] Implementar 2-3 estrategias
  ```python
  class GreedyHeuristic1(ConstructiveOperator):
      """Heurística 1"""
      @staticmethod
      def construct(problem: MyProblem) -> MySolution:
          # Lógica específica
          pass
  
  class GreedyHeuristic2(ConstructiveOperator):
      """Heurística 2 (diferente)"""
      @staticmethod
      def construct(problem: MyProblem) -> MySolution:
          # Lógica diferente
          pass
  
  class RandomConstruct(ConstructiveOperator):
      """Solución aleatoria (para control)"""
      @staticmethod
      def construct(problem: MyProblem) -> MySolution:
          pass
  ```

### Paso 2: `operators/improvement.py`

- [ ] Crear clase base abstracta
  ```python
  class ImprovementOperator(ABC):
      @abstractmethod
      def move(self, solution: MySolution, 
               problem: MyProblem) -> MySolution:
          """Generar solución vecina"""
          pass
  ```

- [ ] Implementar 2-3 movimientos
  ```python
  class Move1(ImprovementOperator):
      """Operador de movimiento 1"""
      @staticmethod
      def move(solution, problem):
          neighbor = solution.copy()
          # Aplicar operación local
          return neighbor
  
  class Move2(ImprovementOperator):
      """Operador de movimiento 2"""
      @staticmethod
      def move(solution, problem):
          neighbor = solution.copy()
          # Otra operación
          return neighbor
  ```

### Paso 3: `operators/perturbation.py` y `repair.py`

- [ ] Crear operadores de perturbación (cambios grandes)
- [ ] Crear operadores de reparación (si hay restricciones)

---

## ✅ FASE 5: Implementar Metaheurística

### Paso 1: `metaheuristic/sa_core.py` (si usas SA)

- [ ] Crear clase SimulatedAnnealing con inyección
  ```python
  class SimulatedAnnealing:
      def __init__(self, problem, 
                   cooling_schedule=None,
                   acceptance=None,
                   initial_constructor=None,
                   **params):
          # Inyectar estrategias
          self.problem = problem
          self.cooling = cooling_schedule or DefaultCooling()
          self.acceptance = acceptance or MetropolisCriterion()
          self.initial = initial_constructor or DefaultConstructor
      
      def run(self) -> Dict:
          """Bucle principal SA"""
          # Implementar
          return results
  ```

- [ ] Implementar bucle principal
- [ ] Rastrear `temperature_history`, `best_value_history`

### Paso 2: `metaheuristic/cooling_schedules.py` y `acceptance.py`

- [ ] Crear clases para diferentes esquemas de enfriamiento
- [ ] Implementar criterios de aceptación

---

## ✅ FASE 6: Validación y Testing

- [ ] Crear `tests/test_core.py`
  ```python
  import pytest
  from core import MyProblem, MySolution, MyEvaluator
  from operators.constructive import GreedyHeuristic1
  
  def test_problem_initialization():
      p = MyProblem(...)
      assert p.param1 > 0
  
  def test_solution_feasibility():
      p = MyProblem(...)
      s = GreedyHeuristic1.construct(p)
      assert s.is_feasible(p)
  
  def test_evaluator():
      p = MyProblem(...)
      s = GreedyHeuristic1.construct(p)
      metrics = MyEvaluator.evaluate(s, p)
      assert 'fitness' in metrics
  
  # Correr: pytest tests/test_core.py -v
  ```

- [ ] Ejecutar `python scripts/test_quick.py`
  ```python
  # scripts/test_quick.py
  from data.loader import load_problem
  from operators.constructive import GreedyHeuristic1
  
  try:
      problem = load_problem('datasets/low_dimensional/f1.json')
      solution = GreedyHeuristic1.construct(problem)
      print("✅ Core works!")
  except Exception as e:
      print(f"❌ Error: {e}")
  ```

---

## ✅ FASE 7: Experimentación Progresiva

### Paso 1: Demo Simple

- [ ] Crear `scripts/demo_complete.py`
  ```python
  from data.loader import load_problem
  from metaheuristic.sa_core import SimulatedAnnealing
  from operators.constructive import GreedyHeuristic1
  
  # 1. Cargar problema
  problem = load_problem('datasets/low_dimensional/f1.json')
  
  # 2. Ejecutar SA
  sa = SimulatedAnnealing(problem, initial_constructor=GreedyHeuristic1)
  result = sa.run()
  
  # 3. Mostrar resultado
  print(f"Best value: {result['best_value']}")
  print(f"Time: {result['execution_time']:.2f}s")
  ```

### Paso 2: Experimentos

- [ ] Crear `scripts/demo_experimentation.py`
  ```python
  # Correr SA múltiples veces
  # Generar gráficas comparativas
  # Guardar resultados en CSV
  ```

### Paso 3: Benchmarks a Gran Escala

- [ ] Crear `scripts/experiment_large_scale.py`
  ```python
  # Correr en todas las instancias
  # Recopilar estadísticas
  # Análisis comparativo
  ```

---

## ✅ FASE 8: Documentación

- [ ] **QUICKSTART.md** (para que otros usen tu código)
  ```markdown
  ## Quick Start
  
  ```bash
  pip install -r requirements.txt
  python scripts/test_quick.py      # ✅ Validación
  python scripts/demo_complete.py   # ✅ Demo
  python scripts/demo_experimentation.py  # Experimentos
  ```
  ```

- [ ] **README.md** (presentación general)
  - Descripción del problema
  - Resultados clave
  - Instrucciones de instalación
  - Link a documentación

- [ ] **config/problema_metaheuristica.md**
  - Definición matemática del problema
  - Operadores disponibles
  - Parámetros de metaheurística

- [ ] **docs/ARCHITECTURE.md**
  - Diagrama de capas
  - Flujo de datos
  - Cómo extender

---

## ✅ FASE 9: Configuración Final

- [ ] **config/config.yaml**
  ```yaml
  project:
    name: "Mi Proyecto"
    version: "1.0.0"
  
  problem:
    type: "mi_problema"
    optimization: "maximize"
  
  metaheuristic:
    parameters:
      T0: 100.0
      alpha: 0.95
      iterations_per_temp: 100
  ```

- [ ] **requirements.txt**
  ```
  numpy>=1.21.0
  scipy>=1.7.0
  pandas>=1.3.0
  matplotlib>=3.4.0
  graphviz>=0.20.0
  pyyaml>=5.4
  ```

- [ ] **.gitignore**
  ```
  __pycache__/
  *.pyc
  output/
  .pytest_cache/
  .vscode/
  logs/
  *.egg-info/
  ```

---

## ✅ FASE 10: Validación Final

- [ ] [ ] `test_quick.py` pasa (10s)
- [ ] [ ] `demo_complete.py` funciona (30s)
- [ ] [ ] `demo_experimentation.py` genera gráficas (2-5min)
- [ ] [ ] Todos los tests en `tests/` pasan (`pytest tests/`)
- [ ] [ ] README.md es claro y ejecutable
- [ ] [ ] QUICKSTART.md tiene comandos listos para copiar/pegar
- [ ] [ ] Código tiene type hints completos
- [ ] [ ] Docstrings con parámetros, retorno, ejemplo
- [ ] [ ] Configuración centralizada en `config.yaml`
- [ ] [ ] Logging funciona y genera logs detallados

---

## 🎯 Checklist Rápido (5 minutos)

Use esto para verificación final:

```
ESTRUCTURA:
  ☐ core/ (problem.py, solution.py, evaluation.py)
  ☐ operators/ (constructive.py, improvement.py, perturbation.py)
  ☐ metaheuristic/ (sa_core.py, cooling, acceptance)
  ☐ tests/ (test_core.py)
  ☐ scripts/ (test_quick.py, demo_*.py)
  ☐ config/ (config.yaml)
  ☐ docs/ (QUICKSTART.md, README.md)

CÓDIGO:
  ☐ Type hints en todas partes
  ☐ Docstrings con ejemplo
  ☐ Validaciones en __post_init__
  ☐ Inyección de dependencias
  ☐ Sin hardcodeo de parámetros

DOCUMENTACIÓN:
  ☐ QUICKSTART.md con comandos listos
  ☐ README.md con descripción
  ☐ ARCHITECTURE.md con diagramas
  ☐ problema_metaheuristica.md con matemática

VALIDACIÓN:
  ☐ pytest tests/ -v ✅
  ☐ python scripts/test_quick.py ✅
  ☐ python scripts/demo_complete.py ✅
  ☐ python scripts/demo_experimentation.py ✅
```

---

## 📞 Si algo No Funciona

1. **Verifica estructura de carpetas**
   ```bash
   find . -type d | head -20
   ```

2. **Verifica imports**
   ```bash
   python -c "from core import MyProblem; print('OK')"
   ```

3. **Verifica tipos**
   ```bash
   python -m mypy core/ --ignore-missing-imports
   ```

4. **Verifica documentación**
   ```bash
   grep -r "def " core/ | grep -v "    #"
   ```

---

## 🎓 Notas Finales

- Sigue este checklist **secuencialmente** (no saltes fases)
- Prueba en cada paso con `test_quick.py`
- Mantén estructura limpia: 1 responsabilidad por módulo
- Documenta mientras codificas (no después)
- Usa el código de KBP-SA como referencia constantemente

**¡Buena suerte!** 🚀

