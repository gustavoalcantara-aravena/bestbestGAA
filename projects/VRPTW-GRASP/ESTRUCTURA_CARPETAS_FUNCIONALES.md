# 📁 Estructura de Carpetas Funcionales - VRPTW-GRASP

**Inspirado en**: GAA-GCP-ILS-4  
**Fecha**: 1 de Enero de 2026  
**Status**: Especificación de Arquitectura

---

## 🎯 Principios de Diseño

La estructura de GAA-GCP-ILS-4 sigue estos principios que **adaptamos a VRPTW-GRASP**:

1. **Separación de Responsabilidades**
   - Cada carpeta = una responsabilidad clara
   - Módulos reutilizables e independientes

2. **Capas Funcionales**
   - `core/` → Clases fundamentales del problema
   - `gaa/` → Sistema de generación de algoritmos
   - `operators/` → Operadores del dominio
   - `metaheuristic/` → Algoritmos y control
   - `utils/` → Funciones auxiliares compartidas
   - `visualization/` → Gráficas y reportes
   - `scripts/` → Puntos de entrada ejecutables

3. **Escalabilidad**
   - Fácil agregar nuevos operadores
   - Reutilizar módulos para futuras mejoras
   - Estructura clara para nuevos miembros del equipo

---

## 📊 Estructura Actual vs. Propuesta

### VRPTW-GRASP ACTUAL

```
VRPTW-GRASP/
├── core/                   ✅ Existe
├── data/                   ✅ Existe (→ renombar a datasets/)
├── datasets/               ✅ Existe (instancias Solomon)
├── metaheuristic/          ✅ Existe
├── operators/              ✅ Existe (22 operadores)
├── run.py                  ✅ Existe
├── demo.py                 ✅ Existe
├── [*.md]                  📚 Documentación
└── [Config, tests, etc]
```

### VRPTW-GRASP PROPUESTA (Inspirada en GAA-GCP-ILS-4)

```
VRPTW-GRASP/
├── core/                   ✅ [Expandir]
│   ├── __init__.py
│   ├── problem.py          [Clase VRPTWProblem - similar a GraphColoringProblem]
│   ├── solution.py         [Clase VRPTWSolution - similar a ColoringSolution]
│   └── evaluation.py       [Clase VRPTWEvaluator - similar a ColoringEvaluator]
│
├── gaa/                    🆕 [CREAR]
│   ├── __init__.py
│   ├── ast_nodes.py        [Nodos sintácticos para GRASP]
│   ├── grammar.py          [Gramática BNF con operadores VRPTW]
│   ├── generator.py        [Generador de algoritmos GRASP]
│   ├── interpreter.py      [Intérprete de AST]
│   └── README.md           [Documentación del módulo]
│
├── operators/              ✅ [Restructurar]
│   ├── __init__.py
│   ├── constructive.py     [Constructor: RandomizedInsertion, etc.]
│   ├── improvement.py      [Mejora: TwoOpt, OrOpt, CrossExchange, etc.]
│   ├── perturbation.py     [Perturbación: RuinRecreate, etc.]
│   ├── repair.py           [Reparación: RepairTimeWindows, RepairCapacity]
│   └── README.md
│
├── metaheuristic/          ✅ [Usar para GRASP]
│   ├── __init__.py
│   ├── grasp_core.py       [Clase GRASP - controlador principal]
│   └── README.md
│
├── utils/                  🆕 [CREAR]
│   ├── __init__.py
│   ├── config.py           [Gestor de configuración]
│   ├── output_manager.py   [Manejo de salidas/logs (del gaa-gcp-ils)]
│   ├── algorithm_visualizer.py [Visualizador de AST]
│   └── README.md
│
├── visualization/          🆕 [CREAR]
│   ├── __init__.py
│   ├── plotter.py          [Gráficas de resultados]
│   ├── route_visualizer.py [Visualización de rutas VRPTW]
│   ├── convergence.py      [Curvas de convergencia]
│   └── README.md
│
├── config/                 🆕 [CREAR]
│   ├── config.yaml         [Parámetros centralizados]
│   └── README.md
│
├── tests/                  🆕 [CREAR]
│   ├── __init__.py
│   ├── conftest.py         [Fixtures de pytest]
│   ├── test_core.py        [Tests del módulo core]
│   ├── test_gaa.py         [Tests del módulo gaa]
│   ├── test_operators.py   [Tests de operadores]
│   ├── test_grasp.py       [Tests de GRASP]
│   └── README.md
│
├── scripts/                ✅ [Expandir]
│   ├── __init__.py
│   ├── demo_experimentation_quick.py  [Test QUICK - R1, 36 exp]
│   ├── demo_experimentation_full.py   [Test FULL - 6 familias, 168 exp]
│   ├── gaa_algorithm_showcase.py      [Mostrar algoritmos generados]
│   ├── validate_operators.py          [Validar operadores]
│   └── README.md
│
├── experimentation/        🆕 [CREAR]
│   ├── __init__.py
│   ├── statistics.py       [Análisis estadístico]
│   ├── comparative_analysis.py [Comparativas inter-familia]
│   └── README.md
│
├── datasets/               ✅ [Existe - Solomon instances]
│   ├── R1/  (12 instancias)
│   ├── R2/  (12 instancias)
│   ├── C1/  (9 instancias)
│   ├── C2/  (10 instancias)
│   ├── RC1/ (8 instancias)
│   ├── RC2/ (8 instancias)
│   └── README.md
│
├── output/                 ✅ [Expandir]
│   ├── algorithms/         [Algoritmos generados (JSON)]
│   ├── experiments/        [Resultados de experimentos]
│   │   ├── quick/         [Resultados QUICK test]
│   │   └── full/          [Resultados FULL test]
│   ├── plots/             [Gráficas PNG/SVG]
│   │   ├── quick/
│   │   └── full/
│   ├── logs/              [Logs de ejecución]
│   └── README.md
│
├── docs/                   📚 [Documentación adicional]
│   ├── ARCHITECTURE.md
│   ├── OPERATORS.md
│   ├── GRASP_ALGORITHM.md
│   └── GAA_SYSTEM.md
│
├── data/                   ✅ [MANTENER - cargadores]
│   ├── __init__.py
│   ├── loader.py          [Cargador de Solomon]
│   └── README.md
│
├── config.yaml             🆕 [Crear archivo de config]
├── requirements.txt        ✅ [Mantener/actualizar]
├── pyproject.toml          ✅ [Mantener]
├── __init__.py             ✅ [Mantener]
│
├── QUICKSTART.md           ✅ [Actualizar]
├── README.md               ✅ [Actualizar]
├── ESTRUCTURA_CARPETAS_FUNCIONALES.md  📄 [Este documento]
├── GAA_IMPLEMENTACION_VRPTW.md         📄 [Especificación GAA]
│
└── run_tests.py            🆕 [Script ejecutor de tests]
```

---

## 🏗️ Detalle de Carpetas a Crear/Expandir

### 1️⃣ `gaa/` - Sistema de Generación Automática de Algoritmos (NUEVA)

**Responsabilidad**: Generar automáticamente algoritmos GRASP válidos para VRPTW

**Archivos**:
```
gaa/
├── __init__.py                    # Exportar AST, Grammar, Generator, Interpreter
├── ast_nodes.py                   # ~450 líneas
│   ├── ASTNode (base)
│   ├── Seq, While, For, If       (control flow)
│   ├── Call, ChooseBestOf         (especializados)
│   ├── ApplyUntilNoImprove       (VND)
│   └── Construction, Repair       (GRASP fases)
│
├── grammar.py                     # ~250 líneas
│   ├── Grammar (class)
│   ├── CONSTRUCTIVE_TERMINALS    (4 operadores)
│   ├── IMPROVEMENT_TERMINALS     (8 operadores)
│   ├── REPAIR_TERMINALS          (3 operadores)
│   ├── Validación de restricciones
│   └── BNF rules
│
├── generator.py                   # ~300 líneas
│   ├── AlgorithmGenerator(class)
│   ├── generate_with_validation()
│   ├── _generate_grasp_structure()
│   ├── _validate_vrptw_criteria()
│   └── generate_population()
│
├── interpreter.py                 # ~350 líneas
│   ├── ExecutionContext
│   ├── ASTInterpreter(class)
│   ├── execute()
│   ├── _execute_node()
│   └── get_execution_report()
│
└── README.md                      # Documentación del módulo
```

**Imports**:
```python
from gaa import (
    ASTNode, Grammar, AlgorithmGenerator, ASTInterpreter
)
```

---

### 2️⃣ `utils/` - Utilidades Compartidas (NUEVA)

**Responsabilidad**: Funciones auxiliares compartidas entre módulos

**Archivos**:
```
utils/
├── __init__.py
├── config.py                      # ~150 líneas
│   ├── class Config (singleton)
│   ├── load_yaml()
│   ├── get_parameter()
│   └── create_directories()
│
├── output_manager.py              # ~300 líneas [ADAPTADO de GAA-GCP-ILS-4]
│   ├── class OutputManager
│   ├── create_session()
│   ├── print_header()
│   ├── print_section()
│   ├── save_json()
│   ├── save_markdown()
│   └── Emoji/formatting utilities
│
├── algorithm_visualizer.py        # ~200 líneas [ADAPTADO de GAA-GCP-ILS-4]
│   ├── visualize_ast()
│   ├── ast_to_pseudocode()
│   ├── ast_to_dot()
│   └── plot_ast_tree()
│
└── README.md
```

**Imports**:
```python
from utils import Config, OutputManager, AlgorithmVisualizer
```

---

### 3️⃣ `operators/` - Operadores del Dominio (REESTRUCTURAR)

**Responsabilidad**: Implementar todos los operadores VRPTW

**Archivos**:
```
operators/
├── __init__.py                    # Exportar clases de operadores
├── base.py                        # ~100 líneas
│   ├── class Operator (abstracta)
│   ├── execute()
│   └── validate()
│
├── constructive.py                # ~300 líneas
│   ├── RandomizedInsertion
│   ├── TimeOrientedNN
│   ├── RegretInsertion
│   └── NearestNeighbor
│
├── improvement.py                 # ~400 líneas
│   ├── [Intra-ruta]
│   │   ├── TwoOpt
│   │   ├── OrOpt
│   │   ├── ThreeOpt
│   │   └── Relocate
│   ├── [Inter-ruta]
│   │   ├── CrossExchange
│   │   ├── TwoOptStar
│   │   ├── SwapCustomers
│   │   └── RelocateInter
│
├── perturbation.py                # ~250 líneas
│   ├── EjectionChain
│   ├── RuinRecreate
│   ├── RandomRemoval
│   └── RouteElimination
│
├── repair.py                      # ~200 líneas
│   ├── RepairTimeWindows
│   ├── RepairCapacity
│   └── GreedyRepair
│
├── utils.py                       # ~150 líneas
│   ├── Funciones auxiliares de cálculo
│   ├── Validaciones
│   └── Conversiones
│
└── README.md
```

**Imports**:
```python
from operators import (
    RandomizedInsertion, TwoOpt, OrOpt, CrossExchange,
    RepairTimeWindows, RepairCapacity
)
```

---

### 4️⃣ `visualization/` - Visualización y Reportes (NUEVA)

**Responsabilidad**: Generar gráficas, reportes y visualizaciones

**Archivos**:
```
visualization/
├── __init__.py
├── plotter.py                     # ~400 líneas
│   ├── plot_gap_comparison()      [Boxplot/barplot de gaps]
│   ├── plot_quality_vs_time()     [Scatter plot]
│   ├── plot_convergence()         [Curvas de convergencia]
│   ├── plot_vehicles_comparison()
│   └── plot_algorithm_comparison()
│
├── route_visualizer.py            # ~300 líneas
│   ├── plot_route()               [Visualizar una ruta]
│   ├── plot_routes_grid()         [Grid de rutas]
│   ├── plot_solution()            [Solución completa]
│   └── highlight_conflicts()      [Resaltar violaciones]
│
├── convergence.py                 # ~200 líneas
│   ├── plot_convergence_curve()
│   ├── plot_convergence_grid()
│   └── plot_iteration_statistics()
│
├── README.md
└── styles/                        [Estilos matplotlib/plotly]
    └── vrptw_style.py
```

**Imports**:
```python
from visualization import (
    plot_gap_comparison, plot_routes_grid, plot_convergence
)
```

---

### 5️⃣ `config/` - Configuración Centralizada (NUEVA)

**Responsabilidad**: Parámetros centralizados del proyecto

**Archivos**:
```
config/
├── config.yaml                    # Parámetros centralizados
│   ├── [problem]                 Parámetros VRPTW
│   ├── [grasp]                   Parámetros GRASP
│   ├── [operators]               Config de operadores
│   ├── [gaa]                     Config de generación
│   ├── [experimentation]         Parámetros quick/full
│   ├── [output]                  Configuración de salidas
│   └── [logging]                 Configuración de logs
│
└── README.md
```

**Ejemplo config.yaml**:
```yaml
problem:
  name: "VRPTW-Solomon"
  time_windows: true
  capacity_constraint: true
  num_vehicles_max: 20

grasp:
  iterations: 100
  alpha_parameter: 0.15
  time_limit_seconds: 300

operators:
  constructive_timeout: 30
  local_search_iterations_max: 100
  repair_timeout: 10

gaa:
  population_size: 3
  seed: 42
  min_depth: 2
  max_depth: 3

experimentation:
  quick:
    families: ["R1"]
    repetitions: 1
    total_experiments: 36
  full:
    families: ["R1", "R2", "C1", "C2", "RC1", "RC2"]
    repetitions: 1
    total_experiments: 168

output:
  format: ["json", "csv", "markdown"]
  save_algorithms: true
  save_plots: true

logging:
  level: "INFO"
  format: "[%(levelname)s] %(name)s: %(message)s"
```

---

### 6️⃣ `tests/` - Suite de Testing (NUEVA)

**Responsabilidad**: Validar correctitud de módulos

**Archivos**:
```
tests/
├── __init__.py
├── conftest.py                    # ~300 líneas - Fixtures globales
│   ├── @fixture problem_instance()
│   ├── @fixture solution()
│   ├── @fixture small_algorithm()
│   ├── @fixture dataset_loader()
│   └── sample data fixtures
│
├── test_core.py                   # ~15 tests
│   ├── test_vrptw_problem_load()
│   ├── test_vrptw_solution_feasibility()
│   ├── test_time_window_violations()
│   └── test_capacity_violations()
│
├── test_gaa.py                    # ~20 tests
│   ├── test_grammar_creation()
│   ├── test_algorithm_generation()
│   ├── test_ast_validity()
│   ├── test_interpreter_execution()
│   └── test_pseudocode_generation()
│
├── test_operators.py              # ~25 tests
│   ├── test_randomized_insertion()
│   ├── test_two_opt()
│   ├── test_cross_exchange()
│   └── test_repair_operators()
│
├── test_grasp.py                  # ~15 tests
│   ├── test_grasp_execution()
│   ├── test_grasp_convergence()
│   └── test_solution_feasibility_after_grasp()
│
└── README.md
```

**Ejecución**:
```bash
pytest tests/               # Todos los tests
pytest tests/test_gaa.py   # Solo tests de GAA
pytest -v                  # Verbose
pytest --cov               # Con coverage
```

---

### 7️⃣ `scripts/` - Puntos de Entrada (EXPANDIR)

**Responsabilidad**: Scripts ejecutables principales

**Archivos**:
```
scripts/
├── __init__.py
├── demo_experimentation_quick.py   # ~400 líneas
│   • Genera 3 algoritmos (seed=42)
│   • Ejecuta en R1 (12 instancias)
│   • 36 experimentos totales
│   • Salida: 20 archivos
│
├── demo_experimentation_full.py    # ~500 líneas
│   • Reutiliza 3 algoritmos
│   • Ejecuta en 6 familias (56 instancias)
│   • 168 experimentos totales
│   • Análisis por familia
│   • Salida: 70 archivos
│
├── gaa_algorithm_showcase.py       # ~250 líneas
│   • Genera 10 algoritmos
│   • Muestra pseudocódigo de cada uno
│   • Valida restricciones
│   • Compara estructuras
│
├── validate_operators.py           # ~200 líneas
│   • Valida que cada operador funciona
│   • Prueba con instancias pequeñas
│   • Genera reporte de validación
│
└── README.md
```

---

### 8️⃣ `experimentation/` - Análisis de Experimentos (NUEVA)

**Responsabilidad**: Análisis estadístico y comparativo

**Archivos**:
```
experimentation/
├── __init__.py
├── statistics.py                  # ~300 líneas
│   ├── compute_descriptive_stats()
│   ├── significance_test()        [Kruskal-Wallis]
│   ├── effect_size()              [Cohen's d]
│   └── confidence_intervals()
│
├── comparative_analysis.py        # ~250 líneas
│   ├── compare_algorithms()
│   ├── analyze_by_family()
│   ├── identify_best_algorithm()
│   └── generate_comparison_report()
│
└── README.md
```

---

## 🔗 Mapeo de Responsabilidades

```
┌─────────────────────────────────────────────────────────────┐
│ scripts/ - Puntos de entrada                                │
│ (demo_experimentation_quick.py, demo_experimentation_full) │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴──────────┬──────────────┬────────────────┐
        │                    │              │                │
┌───────▼────────┐ ┌────────▼──────┐ ┌────▼──────────┐ ┌───▼──────────┐
│ gaa/           │ │ operators/    │ │ experimentation/    visualization/
│ • Generación   │ │ • Ejecución   │ │ • Análisis     │ │ • Gráficas
│ • Validación   │ │ • Validación  │ │ • Estadística  │ │ • Reportes
└────────┬───────┘ └────────┬──────┘ └────┬──────────┘ └───┬──────────┘
         │                  │             │                │
         │    ┌─────────────┴─────────────┴────────────────┘
         │    │
         │    ├──────────────────┐
         │    │                  │
┌────────▼────▼──────┐   ┌────────▼─────────┐
│ core/              │   │ utils/            │
│ • VRPTWProblem     │   │ • Config          │
│ • VRPTWSolution    │   │ • OutputManager   │
│ • VRPTWEvaluator   │   │ • Visualizer      │
└────────────────────┘   └───────────────────┘
         ▲                        │
         │                        │
┌────────┴────────────────────────▼──────────┐
│ config/                                    │
│ • Parámetros centralizados (config.yaml)   │
└────────────────────────────────────────────┘
```

---

## 📊 Comparativa: GAA-GCP-ILS-4 vs VRPTW-GRASP

| Aspecto | GAA-GCP-ILS-4 | VRPTW-GRASP | Adaptación |
|---------|---------------|-------------|-----------|
| **Problema Base** | Graph Coloring (colores) | Vehicle Routing (rutas) | ✅ Distinto dominio |
| **Solución** | `ColoringSolution` | `VRPTWSolution` | ✅ Similar estructura |
| **Operadores Constructivos** | DSATUR, LF | RandomizedInsertion, TimeOrientedNN | ✅ 4 vs 4 |
| **Operadores Mejora** | KempeChain, OneVertexMove | TwoOpt, OrOpt, CrossExchange | ✅ 3-4 vs 8 |
| **Sistema GAA** | Generación + Evolución | Generación (seed=42) | ✅ Más simple |
| **Validación** | Factibilidad (colores) | Factibilidad (capacidad + tiempo) | ✅ Más compleja |
| **Output** | OutputManager + emojis | Mismo patrón | ✅ Reutilizable |
| **Visualización** | Matrices de adyacencia | Rutas en mapa | ✅ Específica VRPTW |
| **Métrica Principal** | Número de colores | Distancia + vehículos | ✅ Multi-objetivo |
| **Tests** | pytest + fixtures | Mismo patrón | ✅ Reutilizable |

---

## 🔄 Plan de Implementación

### Fase 1: Crear Infraestructura (Semana 1)
- [x] Crear `gaa/` módulo base
- [ ] Crear `utils/` con OutputManager
- [ ] Crear `config/` con config.yaml
- [ ] Crear `tests/` con infraestructura básica
- [ ] Expandir `operators/` con estructura

### Fase 2: Implementar GAA (Semana 2)
- [ ] `gaa/ast_nodes.py` (~450 líneas)
- [ ] `gaa/grammar.py` (~250 líneas)
- [ ] `gaa/generator.py` (~300 líneas)
- [ ] `gaa/interpreter.py` (~350 líneas)
- [ ] Tests unitarios para GAA

### Fase 3: Operadores (Semana 2-3)
- [ ] `operators/constructive.py`
- [ ] `operators/improvement.py`
- [ ] `operators/repair.py`
- [ ] Tests de cada operador
- [ ] Integración con GAA

### Fase 4: Scripts Experimentales (Semana 3)
- [ ] `scripts/demo_experimentation_quick.py`
- [ ] `scripts/demo_experimentation_full.py`
- [ ] Crear `output/` estructura
- [ ] Validación end-to-end

### Fase 5: Visualización y Análisis (Semana 4)
- [ ] `visualization/plotter.py`
- [ ] `visualization/route_visualizer.py`
- [ ] `experimentation/statistics.py`
- [ ] Generación de reportes

---

## 📝 Conclusión

La estructura propuesta **adapta el éxito de GAA-GCP-ILS-4** al contexto de VRPTW-GRASP:

1. ✅ **Separación clara** de responsabilidades
2. ✅ **Reutilización** de patrones probados (OutputManager, tests)
3. ✅ **Escalabilidad** para futuras mejoras
4. ✅ **Mantenibilidad** con módulos independientes
5. ✅ **Documentación** clara en cada módulo

---

**Documento**: Estructura de Carpetas Funcionales VRPTW-GRASP  
**Basado en**: GAA-GCP-ILS-4  
**Status**: Especificación Lista para Implementación  
**Próximo**: Implementar módulo `gaa/`
