# Buenas Prácticas en la Estructura del KBP-SA

## 📋 Resumen Ejecutivo

El proyecto **KBP-SA** implementa un framework robusto y reutilizable para resolver el Problema de la Mochila (Knapsack 0/1) usando Simulated Annealing. Su estructura es un **modelo de referencia** para proyectos de optimización combinatoria.

---

## 🏗️ Principios Fundamentales de Diseño

### 1. **Separación de Responsabilidades (SoC)**

```
Principio: Cada carpeta/módulo tiene una responsabilidad clara y única
```

| Carpeta | Responsabilidad | Dependencias |
|---------|-----------------|--------------|
| `core/` | Definición matemática del problema | Ninguna |
| `operators/` | Transformaciones de soluciones | Depende de `core/` |
| `metaheuristic/` | Lógica de búsqueda | Depende de `core/` |
| `gaa/` | Generación de algoritmos | Depende de `core/` |
| `experimentation/` | Análisis y métricas | Depende de todo |
| `utils/` | Funciones transversales | Independiente |

**✅ Beneficio**: Cambios en un módulo no afectan otros (bajo acoplamiento)

---

## 🎯 Estructura en Capas

### **Capa 1: Core (Definición del Problema)**

```python
# core/problem.py - Define QUÉ queremos resolver
@dataclass
class KnapsackProblem:
    n: int                          # Número de ítems
    capacity: int                   # Capacidad
    values: np.ndarray              # Valores
    weights: np.ndarray             # Pesos
    optimal_value: int = None       # Valor óptimo conocido

# core/solution.py - Cómo representamos una solución
@dataclass
class KnapsackSolution:
    x: np.ndarray                   # Vector binario [0,1,1,0,...]
    value: int                      # Valor total
    weight: int                     # Peso total
    is_feasible: bool               # ¿Respeta capacidad?

# core/evaluation.py - Métricas de calidad
class KnapsackEvaluator:
    @staticmethod
    def evaluate(solution, problem) -> Dict:
        return {
            'fitness': solution.value,
            'feasibility': solution.is_feasible,
            'gap': (optimal - solution.value) / optimal
        }
```

**Características clave**:
- 📝 Usa `@dataclass` para claridad y serialización
- ✅ Incluye validaciones en `__post_init__`
- 📖 Documenta el modelo matemático en docstrings
- 🔒 Tipos explícitos (Type Hints)

---

### **Capa 2: Operadores (Transformaciones Elementales)**

Estructura modular de operadores especializados:

```
operators/
├── constructive.py   # Cómo generar soluciones iniciales
├── improvement.py    # Búsqueda local (flip, swap)
├── perturbation.py   # Cambios grandes (shake)
└── repair.py         # Reparación de infactibilidad
```

**Patrón de Diseño: Strategy**

```python
# operators/improvement.py
class FlipBestItem:
    """Estrategia: Flip del ítem que más mejora fitness"""
    def operate(self, solution: KnapsackSolution, problem: KnapsackProblem):
        # Implementación específica
        pass

class FlipWorstItem:
    """Estrategia: Flip del ítem con peor ratio valor/peso"""
    def operate(self, solution: KnapsackSolution, problem: KnapsackProblem):
        # Implementación diferente
        pass
```

**✅ Beneficios**:
- Fácil de agregar nuevos operadores (Open/Closed Principle)
- Cada operador es testeable independientemente
- Código reutilizable en diferentes metaheurísticas

---

### **Capa 3: Metaheurística (Lógica de Búsqueda)**

```
metaheuristic/
├── sa_core.py              # Motor principal SA
├── cooling_schedules.py    # Esquemas de enfriamiento
└── acceptance.py           # Criterios de aceptación
```

**Estructura del Motor SA**:

```python
class SimulatedAnnealing:
    def __init__(self, problem: KnapsackProblem, T0=100, alpha=0.95, ...):
        self.problem = problem
        self.temperature = T0
        self.alpha = alpha
        
    def run(self) -> ExecutionResult:
        """Bucle principal de SA"""
        # 1. Solución inicial (usar operadores constructivos)
        # 2. Bucle de temperatura
        # 3. Bucle de aceptación (Metropolis)
        # 4. Enfriamiento
        # 5. Retornar mejor solución encontrada
```

**Inyección de Dependencias**:

```python
class SimulatedAnnealing:
    def __init__(self,
                 problem: KnapsackProblem,
                 cooling_schedule: CoolingSchedule = GeometricCooling(),
                 acceptance: AcceptanceCriterion = MetropolisCriterion(),
                 initial_constructor: Callable = GreedyByValue):
        # Estrategias inyectadas = máxima flexibilidad
```

**✅ Beneficios**:
- Prueba con diferentes combinaciones sin modificar código
- Integración limpia con el sistema GAA

---

### **Capa 4: GAA (Generación Automática de Algoritmos)**

```
gaa/
├── grammar.py          # Define qué es válido (BNF)
├── ast_nodes.py        # Nodos del árbol de sintaxis
├── generator.py        # Crea algoritmos aleatorios
└── interpreter.py      # Ejecuta el algoritmo generado
```

**Modelo de Compilador**:

```
[Algoritmo Candidato]
        ↓
  [Grammar.validate()]
        ↓
    [AST Nodes]
        ↓
[Interpreter.execute()]
        ↓
    [Ejecución]
```

**Ejemplo de Algoritmo Generado**:

```python
# Representación en AST (árbol de sintaxis)
Seq([
    GreedyConstruct(GreedyByRatio),              # Solución inicial
    While(IterBudget(100), [                     # Mientras iteraciones < 100
        LocalSearch(FlipBestItem, Metropolis),   # Búsqueda local
        If(Stagnation(20), [                     # Si no mejora en 20 pasos
            DestroyRepair(ShakeByRemoval, RepairByGreedy)  # Perturbación
        ])
    ])
])
```

---

## 🔄 Flujo de Datos

```
[Datasets] ──→ [Loader] ──→ [KnapsackProblem] 
                                     ↓
[GAA Generator] ──→ [Algorithm AST] ──→ [Interpreter]
                                           ↓
[SimulatedAnnealing] ──→ [Operators] ──→ [Solution]
                                           ↓
[Evaluator] ──→ [Metrics] ──→ [Visualization]
```

**Ventajas de este flujo**:
1. **Modular**: Cada componente es independiente
2. **Testeable**: Se puede mockear cualquier componente
3. **Extensible**: Nuevos operadores/métricas sin cambiar otros

---

## 📊 Gestión de Configuración

### **config/config.yaml**

```yaml
project:
  name: "KBP-SA"
  version: "1.0.0"

problem:
  type: "knapsack"
  optimization: "maximize"
  
metaheuristic:
  T0: 100.0
  alpha: 0.95
  iterations_per_temp: 100
  
gaa:
  max_depth: 5
  population_size: 50
  n_generations: 100
```

**✅ Patrón**: Centraliza todos los parámetros ajustables

```python
# Uso en código
from utils.config import load_config
config = load_config('config.yaml')
sa = SimulatedAnnealing(problem, **config['metaheuristic'])
```

---

## 📁 Organización de Datos

```
datasets/
├── low_dimensional/     # n = 4 a 23 (problemas pequeños)
│   ├── f1.json
│   ├── f2.json
│   └── ...
├── large_scale/         # n = 100 a 10,000 (problemas grandes)
│   ├── large1.json
│   └── ...
└── metadata/            # Información de instancias
    └── instances_info.json

output/                 # Resultados (no versionado)
├── low_dimensional_YYYYMMDD_HHMMSS/
│   ├── results.csv
│   ├── statistics.json
│   ├── figures/
│   │   ├── boxplot.png
│   │   ├── gap_evolution.png
│   │   └── algorithm_ast.png
```

**✅ Buena práctica**:
- Datasets separados por tamaño
- Metadata clara de instancias
- Output en timestamps para trazabilidad

---

## 🧪 Testing y Validación

### **Estructura de Tests**

```
tests/
├── test_core.py              # 18 tests para core
├── TEST_RESULTS.md           # Documentación de resultados
└── test_*.py                 # Tests específicos
```

**Cobertura integral**:

```python
# tests/test_core.py
def test_problem_initialization():
    problem = KnapsackProblem(n=10, capacity=50, ...)
    assert problem.n == 10
    
def test_solution_feasibility():
    solution = KnapsackSolution(x=[1,0,1,...])
    assert solution.is_feasible == True or False
    
def test_evaluator():
    metrics = evaluator.evaluate(solution, problem)
    assert 'fitness' in metrics
    assert 'gap' in metrics
```

**✅ Características**:
- Tests enfocados en clases principales
- Validaciones de invariantes
- Cobertura de casos límite

---

## 🚀 Scripts Ejecutables

### **Jerarquía de Scripts**

```
scripts/
├── test_quick.py                    # ✅ Validación rápida (10s)
├── demo_complete.py                 # ✅ Demo funcional (30s)
├── demo_experimentation.py          # ✅ Experimentos con gráficas (2-5min)
├── test_ast_visualization.py        # ✅ Visualización de algoritmos
└── experiment_large_scale.py        # ✅ Experiments a escala
```

**Patrón: Escalera de Confianza**

```
1. test_quick.py
   └─ Valida que todo funciona
   
2. demo_complete.py
   └─ Demuestra flujo completo
   
3. demo_experimentation.py
   └─ Genera resultados con visualizaciones
   
4. experiment_large_scale.py
   └─ Experimenta a escala real
```

**✅ Ventajas**:
- Desarrollador novel: empieza con `test_quick.py`
- Validación antes de escalar
- Documentación ejecutable

---

## 📚 Documentación

### **Estructura de Docs**

```
docs/
├── QUICKSTART_EJECUTABLE.md         # Comandos listos para copiar/pegar
├── README_SISTEMA.md                # Documentación arquitectónica
├── COMO_EJECUTAR_EXPERIMENTOS.md    # Guía paso a paso
├── TRACKING_LOGS.md                 # Sistema de logs
└── ploteos.md                       # Especificación de gráficas
```

**✅ Características**:
- **QUICKSTART con ejemplos listos** para ejecutar
- **Documentación de requisitos** claros (Graphviz, Python 3.8+)
- **Logs detallados** de cada ejecución

---

## 🔗 Patrón de Integración GAA

El GAA permite **generar automáticamente algoritmos válidos**:

```python
# 1. Definir gramática
grammar = Grammar()

# 2. Generar algoritmo aleatorio
algorithm_ast = generate_algorithm(grammar)

# 3. Validar
assert grammar.validate(algorithm_ast)

# 4. Ejecutar
interpreter = Interpreter()
result = interpreter.execute(algorithm_ast, problem)

# 5. Evaluar
metrics = evaluator.evaluate(result)
```

**Ventajas**:
- Algoritmos **garantizados correctos** por gramática
- Exploración automática del espacio de algoritmos
- Cada algoritmo ejecutable y evaluable

---

## 💡 Lecciones para Otros Proyectos

### **1. Establece Capas Claras**
```
Core → Operators → Metaheuristic → GAA → Experimentation
```

### **2. Usa Inyección de Dependencias**
```python
# ✅ Flexible
algorithm = SA(problem, cooling=GeometricCooling(), acceptance=Metropolis())

# ❌ Rígido
algorithm = SA(problem)  # cooling hardcoded internamente
```

### **3. Centraliza Configuración**
```yaml
# config.yaml - todos los parámetros
T0: 100
alpha: 0.95
max_depth: 5
```

### **4. Crea Escalera de Ejecución**
```
quick_test (10s) → demo (30s) → experiments (min) → large_scale (hours)
```

### **5. Separa Datos y Código**
```
code/        ← Controlado en Git
datasets/    ← Referenciado
output/      ← Generado dinámicamente
```

### **6. Documenta con Ejemplos Ejecutables**
```markdown
## Quick Start
```bash
python scripts/test_quick.py
```
```

### **7. Usa Type Hints Extensivamente**
```python
def run(self, problem: KnapsackProblem) -> ExecutionResult:
    """Type hints ayudan IDE + documentación automática"""
```

### **8. Implementa Logging Detallado**
```python
logger.info(f"Temp: {T:.2f}, Aceptación: {accept_rate:.2%}")
logger.debug(f"ΔE = {delta_e}, P = {probability:.4f}")
```

---

## 📊 Resumen Comparativo

| Aspecto | KBP-SA | Lo que buscar en otros proyectos |
|---------|--------|----------------------------------|
| **Estructura** | 4 capas (Core→Op→Meta→GAA) | Jerarquía clara |
| **Testabilidad** | Mock-friendly | Dependencies inyectadas |
| **Extensibilidad** | Strategy pattern | Open/Closed Principle |
| **Configuración** | YAML centralizado | Single source of truth |
| **Documentación** | Scripts ejecutables | Ejemplos reales |
| **Datos** | Separados del código | Versionamiento limpio |
| **Tipos** | Type hints completos | Autocomplete + validación |

---

## 🎓 Próximos Pasos para Replicar

Para crear un nuevo proyecto basado en KBP-SA:

1. **Definir problema** → `core/problem.py`
2. **Operadores específicos** → `operators/`
3. **Metaheurística** → `metaheuristic/`
4. **Gramática GAA** → `gaa/grammar.py`
5. **Tests** → `tests/`
6. **Scripts ejecutables** → `scripts/`
7. **Documentación** → `docs/` + `README.md`

---

## 📞 Referencias

- **Patrón Strategy**: Operators intercambiables
- **Inyección de Dependencias**: Constructor-based injection
- **Arquitectura en Capas**: Core → Aplicación → Presentación
- **Domain-Driven Design**: Core define el lenguaje del dominio

