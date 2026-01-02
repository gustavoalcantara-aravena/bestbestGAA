# 📊 Checklist de Implementación - VRPTW-GRASP

**Fecha**: 1 de Enero de 2026  
**Status**: Checklist Detallado para Desarrollo  
**Referencia**: GAA-GCP-ILS-4 como modelo

---

## 🎯 Resumen Ejecutivo

**Total de Módulos a Crear/Actualizar**: 12 carpetas principales

| Estado | Carpeta | Archivos | Líneas Est. | Prioridad |
|--------|---------|----------|------------|-----------|
| ✅ Existe | `core/` | 3 | 1300+ | P0 - Validar |
| ✅ Existe | `data/` | 2 | 300+ | P0 - Validar |
| ✅ Existe | `datasets/` | 56 instancias | - | P0 - Listo |
| ✅ Existe | `operators/` | 22 operadores | 2000+ | P1 - Reestructurar |
| ✅ Existe | `metaheuristic/` | GRASP | 300+ | P1 - Expandir |
| 🆕 Crear | `gaa/` | 5 archivos | 1350+ | **P0 - CRÍTICO** |
| 🆕 Crear | `utils/` | 3 archivos | 450+ | P0 - CRÍTICO |
| 🆕 Crear | `config/` | 2 archivos | 150+ | P1 |
| 🆕 Crear | `tests/` | 6 archivos | 1500+ | P1 |
| 🆕 Crear | `visualization/` | 4 archivos | 900+ | P2 |
| 🆕 Crear | `experimentation/` | 2 archivos | 550+ | P2 |
| ✅ Existe | `scripts/` | 2+ archivos | 900+ | **P0 - CRÍTICO** |

**Total Estimado**: ~10,000 líneas de código

---

## ✅ MÓDULOS EXISTENTES - Validación Requerida

### 1. `core/` - DEBE VALIDARSE

**Estado**: ✅ Existe

**Archivos**:
```
core/
├── __init__.py                    ✅
├── problem.py                     ✅ [VRPTWProblem]
├── solution.py                    ✅ [VRPTWSolution]
└── evaluation.py                  ✅ [VRPTWEvaluator]
```

**Validaciones Necesarias**:
- [ ] `VRPTWProblem` tiene método `.summary()` similar a GraphColoringProblem
- [ ] `VRPTWSolution` tiene propiedades: `.num_vehicles`, `.total_distance`, `.is_feasible()`
- [ ] `VRPTWEvaluator` puede calcular gaps respecto a BKS
- [ ] Carga correcto formato de instancias Solomon (`.txt`)
- [ ] Serializable a JSON (para almacenar con GAA)

**Checklist**:
```
✓ problema_vrptw_class = exists and has necessary methods
✓ solution_vrptw_class = exists and has necessary properties
✓ evaluator_vrptw_class = exists and can compute metrics
✓ solomon_loader_works = works with all 56 instances
✓ serialization = can save/load to JSON
```

**Acciones Recomendadas**:
- Si falta método `.summary()`, agregarlo (5 líneas)
- Si falta serialización JSON, implementar (20 líneas)
- Tests unitarios: verificar con 3 instancias (5 tests)

---

### 2. `data/` - Validación Rápida

**Estado**: ✅ Existe

**Archivos**:
```
data/
├── __init__.py                    ✅
└── loader.py                      ✅ [DatasetLoader]
```

**Validación**:
- [ ] `DatasetLoader` puede cargar cada familia (R1, R2, C1, C2, RC1, RC2)
- [ ] Retorna lista de `VRPTWInstance` con atributos: `name`, `locations`, `demands`, `time_windows`, `bks`
- [ ] Maneja Solomon format correctamente
- [ ] Es usado por scripts

**Checklist**:
```
✓ load_family("R1") = returns 12 instances
✓ load_all_families() = returns 56 instances
✓ instance.bks = has best known solution
✓ instance.locations = has coordinates
✓ instance.time_windows = has [a_i, b_i]
```

---

### 3. `datasets/` - DATOS Listos

**Estado**: ✅ Existe (56 instancias Solomon)

**Estructura**:
```
datasets/
├── R1/      12 instancias (baja demanda, zonas aleatorias)
├── R2/      12 instancias (alta demanda, zonas aleatorias)
├── C1/      9 instancias (baja demanda, zonas clustering)
├── C2/      10 instancias (alta demanda, zonas clustering)
├── RC1/     8 instancias (baja demanda, zonas mixtas)
└── RC2/     8 instancias (alta demanda, zonas mixtas)
```

**Validación**:
- [ ] Todas instancias presentes y legibles
- [ ] Formato consistente
- [ ] BKS values incluidos en descripción

---

### 4. `operators/` - REESTRUCTURACIÓN Requerida

**Estado**: ✅ Existen 22 operadores

**Problema**: Están desordenados, no están en estructura de módulo formal

**Archivos Actuales**:
```
operators/
├── [múltiples archivos sin estructura clara]
```

**Reestructuración Necesaria**:
```
operators/
├── __init__.py                    🆕 [Crear]
├── base.py                        🆕 [Crear 100 líneas]
│   └── class Operator (abstracta)
│
├── constructive.py                🔄 [Reestructurar]
│   ├── RandomizedInsertion       (¿EXISTE?)
│   ├── TimeOrientedNN            (¿EXISTE?)
│   ├── RegretInsertion           (¿EXISTE?)
│   └── NearestNeighbor           (¿EXISTE?)
│
├── improvement.py                 🔄 [Reestructurar]
│   ├── TwoOpt                     (¿EXISTE?)
│   ├── OrOpt                      (¿EXISTE?)
│   ├── ThreeOpt                   (¿EXISTE?)
│   ├── Relocate                   (¿EXISTE?)
│   ├── CrossExchange              (¿EXISTE?)
│   ├── TwoOptStar                 (¿EXISTE?)
│   ├── SwapCustomers              (¿EXISTE?)
│   └── RelocateInter              (¿EXISTE?)
│
├── repair.py                      🆕 [Crear/mover]
│   ├── RepairTimeWindows          (¿EXISTE?)
│   ├── RepairCapacity             (¿EXISTE?)
│   └── GreedyRepair               (¿EXISTE?)
│
└── README.md                      🆕 [Crear]
```

**Acciones Necesarias**:
1. Audit: listar qué operadores EXISTEN
2. Reorganizar por tipo (constructive, improvement, repair)
3. Crear clase base `Operator`
4. Crear `__init__.py` con exports
5. Actualizar imports en `gaa/`

---

### 5. `metaheuristic/` - EXPANSIÓN Simple

**Estado**: ✅ GRASP parcialmente implementado

**Archivos Actuales**:
```
metaheuristic/
├── [archivos actuales]
```

**Necesario**:
```
metaheuristic/
├── __init__.py                    ✅/🔄 [Validar/actualizar]
├── grasp_core.py                  🔄 [Expandir/validar]
│   └── class GRASP:
│       - constructor(problem, seed=42)
│       - execute(algorithm_ast, num_iterations)
│       - get_best_solution()
│
└── README.md                      🆕 [Crear]
```

**Checklist**:
```
✓ GRASP class exists
✓ Has execute(algorithm_ast) method
✓ Can run with AST as input
✓ Returns feasible solution or None
✓ Tracks iterations and best solution
```

---

## 🆕 MÓDULOS A CREAR - Críticos

### **PRIORIDAD 0 - CRÍTICO (Semana 1)**

#### 1. `gaa/` - Módulo de Generación (1350 líneas)

**Crear estructura completa**:

```
gaa/
├── __init__.py                    🆕 [Crear 50 líneas]
│   from .ast_nodes import *
│   from .grammar import Grammar
│   from .generator import AlgorithmGenerator
│   from .interpreter import ASTInterpreter
│
├── ast_nodes.py                   🆕 [Crear 450 líneas]
│   ├── class ASTNode (base)
│   ├── class Seq(ASTNode)
│   ├── class While(ASTNode)
│   ├── class For(ASTNode)
│   ├── class If(ASTNode)
│   ├── class Call(ASTNode)
│   ├── class ChooseBestOf(ASTNode)
│   ├── class ApplyUntilNoImprove(ASTNode)
│   ├── class Construction(ASTNode)
│   └── class Repair(ASTNode)
│
├── grammar.py                     🆕 [Crear 250 líneas]
│   ├── class Grammar
│   ├── CONSTRUCTIVE_TERMINALS
│   ├── IMPROVEMENT_TERMINALS
│   ├── REPAIR_TERMINALS
│   └── validate_algorithm()
│
├── generator.py                   🆕 [Crear 300 líneas]
│   ├── class AlgorithmGenerator
│   ├── __init__(self, grammar, seed=42)
│   ├── generate_with_validation()
│   ├── _generate_grasp_structure()
│   ├── _validate_vrptw_criteria()
│   └── generate_population(size)
│
├── interpreter.py                 🆕 [Crear 350 líneas]
│   ├── class ExecutionContext
│   ├── class ASTInterpreter
│   ├── execute(ast)
│   ├── _execute_node(node)
│   └── get_execution_report()
│
└── README.md                      🆕 [Crear 150 líneas]
    └── Documentación de uso
```

**Timeline**: 40-60 horas de implementación
**Dependencias**: Operadores deben estar listos

---

#### 2. `utils/` - Utilidades Compartidas (450 líneas)

```
utils/
├── __init__.py                    🆕 [Crear 30 líneas]
│
├── config.py                      🆕 [Crear 150 líneas]
│   ├── class Config (singleton)
│   ├── load_from_yaml()
│   ├── get_parameter()
│   └── create_output_directories()
│
├── output_manager.py              🆕 [Crear 250 líneas]
│   │   [ADAPTAR de GAA-GCP-ILS-4/utils/output_manager.py]
│   ├── class OutputManager
│   ├── create_session()
│   ├── print_header()
│   ├── print_section()
│   ├── save_json()
│   ├── save_markdown()
│   └── format utilities (emojis, dashes)
│
├── algorithm_visualizer.py        🆕 [Crear 150 líneas]
│   ├── ast_to_pseudocode()
│   ├── ast_to_dict()
│   └── print_algorithm_stats()
│
└── README.md                      🆕 [Crear 50 líneas]
```

**Timeline**: 20-30 horas
**Dependencias**: GAA debe estar lista

---

### **PRIORIDAD 1 - Alta (Semana 2)**

#### 3. `scripts/demo_experimentation_quick.py` (400 líneas)

```python
#!/usr/bin/env python
"""
Test QUICK: Validación rápida con familia R1 (12 instancias)
- 3 algoritmos × 12 instancias = 36 experimentos
- Tiempo estimado: 5-10 minutos
- Output: 20 archivos
"""

import sys
from pathlib import Path

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import ASTInterpreter
from data.loader import DatasetLoader
from utils import OutputManager
from metaheuristic.grasp_core import GRASP

def main():
    # 1. Setup
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="quick")
    
    # 2. Generar 3 algoritmos (UNA SOLA VEZ)
    algorithms = generate_algorithms_once()
    
    # 3. Cargar instancias R1
    loader = DatasetLoader("datasets")
    instances = loader.load_folder("R1")
    
    # 4. Ejecutar experimentos
    results = run_experiments(algorithms, instances, output_mgr)
    
    # 5. Analizar y generar gráficas
    analyze_results(results, session_dir)

if __name__ == "__main__":
    main()
```

**Timeline**: 20-30 horas
**Dependencias**: Todos los módulos anteriores listos

---

#### 4. `scripts/demo_experimentation_full.py` (500 líneas)

```python
#!/usr/bin/env python
"""
Test FULL: Validación exhaustiva con todas familias
- 3 algoritmos × 56 instancias = 168 experimentos
- Tiempo estimado: 40-60 minutos
- Output: 70+ archivos
"""

def main():
    # 1. Reutilizar 3 algoritmos de quick
    algorithms = load_generated_algorithms()
    
    # 2. Cargar TODAS instancias
    loader = DatasetLoader("datasets")
    instances = loader.load_all_families()
    
    # 3. Ejecutar experimentos
    results = run_experiments(algorithms, instances, output_mgr)
    
    # 4. Análisis POR FAMILIA
    analyze_by_family(results, session_dir)
    
    # 5. Comparativas inter-familia
    generate_comparative_plots(results)
```

**Timeline**: 30-40 horas (extiende quick)
**Dependencias**: `demo_experimentation_quick.py` completado

---

### **PRIORIDAD 1 - Media (Semana 2-3)**

#### 5. `config/config.yaml` (150 líneas)

```yaml
# Parámetros centralizados del proyecto

problem:
  name: "VRPTW-Solomon"
  time_windows: true
  capacity_constraint: true
  max_vehicles: 20
  planning_horizon: 1440  # minutos

grasp:
  iterations: 100
  alpha_parameter: 0.15
  time_limit_seconds: 300

operators:
  constructive_timeout: 30
  local_search_max_iterations: 100
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
```

**Timeline**: 5-10 horas
**Dependencias**: Ninguna

---

#### 6. `tests/` - Suite Básica (1500 líneas)

```
tests/
├── conftest.py                    🆕 [300 líneas]
├── test_core.py                   🆕 [250 líneas]
├── test_gaa.py                    🆕 [350 líneas]
├── test_operators.py              🆕 [300 líneas]
├── test_grasp.py                  🆕 [250 líneas]
└── test_integration.py            🆕 [150 líneas]
```

**Timeline**: 30-40 horas (paralelo con implementación)
**Dependencias**: Cada módulo que testea

---

### **PRIORIDAD 2 - Media (Semana 3-4)**

#### 7. `visualization/` - Gráficas (900 líneas)

```
visualization/
├── plotter.py                     🆕 [400 líneas]
│   ├── plot_gap_comparison()
│   ├── plot_quality_vs_time()
│   ├── plot_convergence()
│   └── plot_vehicles_comparison()
│
├── route_visualizer.py            🆕 [300 líneas]
│   ├── plot_route()
│   ├── plot_solution()
│   └── highlight_conflicts()
│
├── convergence.py                 🆕 [200 líneas]
│   └── plot_convergence_grid()
│
└── README.md                      🆕 [100 líneas]
```

**Timeline**: 30-40 horas
**Dependencias**: Módulos anteriores completados

---

#### 8. `experimentation/` - Análisis (550 líneas)

```
experimentation/
├── statistics.py                  🆕 [300 líneas]
│   ├── compute_descriptive_stats()
│   ├── significance_test()
│   └── effect_size()
│
├── comparative_analysis.py        🆕 [250 líneas]
│   ├── compare_algorithms()
│   ├── analyze_by_family()
│   └── generate_comparison_report()
│
└── README.md                      🆕 [50 líneas]
```

**Timeline**: 20-30 horas
**Dependencias**: Scripts de experimentos completados

---

## 📋 Checklist de Implementación por Fase

### ✅ FASE 0: Pre-Implementación (YA HECHO)
- [x] Especificación GAA creada (GAA_IMPLEMENTACION_VRPTW.md)
- [x] Estructura de carpetas documentada (ESTRUCTURA_CARPETAS_FUNCIONALES.md)
- [x] Este checklist creado

### 📍 FASE 1: Infraestructura Crítica (Semana 1)

**Hito 1.1: Validar módulos existentes**
- [ ] Revisar `core/` - ¿tiene `.summary()` y serialización JSON?
- [ ] Revisar `data/` - ¿carga correctamente 56 instancias?
- [ ] Revisar `operators/` - listar qué operadores existen
- [ ] Revisar `metaheuristic/` - ¿tiene GRASP class?

**Hito 1.2: Crear `gaa/`**
- [ ] Crear `gaa/__init__.py` (50 líneas)
- [ ] Crear `gaa/ast_nodes.py` (450 líneas)
- [ ] Crear `gaa/grammar.py` (250 líneas)
- [ ] Crear `gaa/generator.py` (300 líneas)
- [ ] Crear `gaa/interpreter.py` (350 líneas)
- [ ] Tests básicos para gaa

**Hito 1.3: Crear `utils/`**
- [ ] Crear `utils/__init__.py` (30 líneas)
- [ ] Crear `utils/config.py` (150 líneas)
- [ ] Copiar/adaptar `utils/output_manager.py` (250 líneas) de GAA-GCP-ILS-4
- [ ] Crear `utils/algorithm_visualizer.py` (150 líneas)

**Hito 1.4: Crear `config/`**
- [ ] Crear `config/config.yaml` (150 líneas)
- [ ] Crear `config/README.md` (50 líneas)

### 📍 FASE 2: Operadores y Scripts (Semana 2)

**Hito 2.1: Reestructurar `operators/`**
- [ ] Crear `operators/__init__.py` con exports
- [ ] Crear `operators/base.py` (100 líneas)
- [ ] Reorganizar en `constructive.py`, `improvement.py`, `repair.py`
- [ ] Validar que 22 operadores funcionan

**Hito 2.2: Scripts experimentales**
- [ ] Crear `scripts/demo_experimentation_quick.py` (400 líneas)
- [ ] Validar que ejecuta 36 experimentos
- [ ] Crear `scripts/demo_experimentation_full.py` (500 líneas)
- [ ] Validar que ejecuta 168 experimentos

**Hito 2.3: Tests**
- [ ] Tests para `core/` (15 tests)
- [ ] Tests para `gaa/` (20 tests)
- [ ] Tests para `operators/` (25 tests)
- [ ] Coverage mínimo: 70%

### 📍 FASE 3: Visualización y Análisis (Semana 3)

**Hito 3.1: `visualization/`**
- [ ] Crear gráficas de gaps (boxplot, barplot)
- [ ] Crear visualización de rutas
- [ ] Crear curvas de convergencia

**Hito 3.2: `experimentation/`**
- [ ] Análisis estadístico por algoritmo
- [ ] Análisis por familia de instancias
- [ ] Reporte comparativo

### ✅ FASE 4: Validación y Documentación (Semana 4)

- [ ] End-to-end testing: `demo_quick.py` completo
- [ ] End-to-end testing: `demo_full.py` completo
- [ ] Documentación en cada módulo
- [ ] README actualizado

---

## 🎯 Próximos Pasos Inmediatos

**Acción 1: AUDITORÍA rápida (1 hora)**
```bash
# Ver estructura actual de operators/
ls -la projects/VRPTW-GRASP/operators/

# Ver qué tiene metaheuristic/
ls -la projects/VRPTW-GRASP/metaheuristic/

# Ver qué tiene core/
ls -la projects/VRPTW-GRASP/core/
```

**Acción 2: Validar módulos existentes (2-3 horas)**
- Revisar `core/problem.py` → ¿tiene `.summary()`?
- Revisar `core/solution.py` → ¿tiene `.is_feasible()`?
- Revisar `data/loader.py` → ¿carga 56 instancias?

**Acción 3: Comenzar Implementación**
- Empezar con `gaa/` (módulo crítico)
- Paralelo: crear `utils/` y `config/`
- Después: reestructurar `operators/`

---

## 📊 Métricas de Éxito

| Métrica | Objetivo | Validación |
|---------|----------|-----------|
| Algoritmos Generados | 3 (seed=42) | `demo_quick.py` exitoso |
| Experimentos QUICK | 36 (R1) | Todos completan sin error |
| Experimentos FULL | 168 (6 familias) | Todos completan sin error |
| Soluciones Factibles | 100% | Cero violaciones en output |
| Coverage Código | ≥70% | `pytest --cov` |
| Tiempo QUICK | 5-10 min | Validado en máquina local |
| Tiempo FULL | 40-60 min | Validado en máquina local |

---

**Documento**: Checklist de Implementación VRPTW-GRASP  
**Status**: Listo para Desarrollo  
**Próximo**: Ejecutar Auditoría de módulos existentes
