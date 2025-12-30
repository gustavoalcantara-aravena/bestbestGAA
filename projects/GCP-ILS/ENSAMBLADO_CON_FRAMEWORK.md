# GCP-ILS: Plan de Ensamblado con Framework GAA

**Fecha**: 2025-12-30  
**Método**: Usar sistema de sincronización automático del framework GAA  
**Estado**: 📋 Listo para ejecutar

---

## 🎯 CÓMO FUNCIONA EL FRAMEWORK

### Flujo de Sincronización Automática

```
1. Editar archivos TRIGGER en 00-Core/:
   ├─ Problem.md (especificación del problema)
   └─ Metaheuristic.md (metaheurística seleccionada)

2. Ejecutar sync-engine.py:
   python 05-Automation/sync-engine.py --sync

3. El sistema AUTO-SINCRONIZA:
   Problem.md → 01-System/Grammar.md (terminales)
            → 02-Components/Fitness-Function.md
            → 02-Components/Evaluator.md
            → 03-Experiments/Instances.md
            → 03-Experiments/Metrics.md
            → 06-Datasets/Dataset-Specification.md
            → 04-Generated/scripts/problem.py (marca para generar)

Metaheuristic.md → 02-Components/Search-Operators.md
                → 02-Components/Fitness-Function.md
                → 03-Experiments/Experimental-Design.md
                → 04-Generated/scripts/metaheuristic.py (marca para generar)
```

### Archivos Sincronizados vs Manuales

```
00-Core/
├─ Problem.md ......................... ✏️  EDITAR (trigger)
├─ Metaheuristic.md ................... ✏️  EDITAR (trigger)
└─ Project-Config.md .................. 🔄 AUTO (generado)

01-System/
└─ Grammar.md ......................... 🔄 AUTO (sync desde Problem.md)

02-Components/
├─ Fitness-Function.md ................ 🔄 AUTO (sync)
├─ Evaluator.md ....................... 🔄 AUTO
└─ Search-Operators.md ................ 🔄 AUTO

03-Experiments/
├─ Experimental-Design.md ............. 🔄 AUTO
├─ Instances.md ....................... 🔄 AUTO
└─ Metrics.md ......................... 🔄 AUTO

04-Generated/scripts/
├─ problem.py ......................... ✏️ MANUAL (o 🔄 AUTO)
├─ ast_nodes.py ....................... ✏️ MANUAL
├─ fitness.py ......................... ✏️ MANUAL
├─ metaheuristic.py ................... ✏️ MANUAL
└─ data_loader.py ..................... ✏️ MANUAL

06-Datasets/
└─ Dataset-Specification.md ........... 🔄 AUTO
```

---

## 📋 PLAN ESPECÍFICO PARA GCP-ILS

### FASE 1: Usar Framework de Sincronización

#### Paso 1a: Crear Files Triggers en 00-Core
NO NECESITAMOS - Ya existen como templates

#### Paso 1b: Revisar/Completar `00-Core/Problem.md`

**Secciones a completar:**
- [x] Nombre: Graph Coloring Problem ✓
- [x] Tipo: Minimización ✓
- [x] Modelo matemático ✓
- [x] Domain-Operators (15 terminales) ✓
- [x] Solution-Representation ✓
- [x] Constraints ✓
- [x] Evaluation-Criteria ✓

**Archivo a actualizar**: `projects/GCP-ILS/problema_metaheuristica.md`  
→ Ya lo tenemos, pero está en `projects/GCP-ILS/`, no en `00-Core/`

#### Paso 1c: Revisar/Completar `00-Core/Metaheuristic.md`

**Secciones a completar:**
- [ ] Selected-Metaheuristic: ILS (ya lo tenemos)
- [ ] Configuration: Parámetros ILS (ya está en config.yaml)
- [ ] Search-Strategy: Operadores de búsqueda

**Archivo a actualizar**: Crear template si es proyecto específico

#### Paso 1d: Ejecutar Sincronización

```bash
python 05-Automation/sync-engine.py --sync
```

---

### FASE 2: Implementación de Código Core

El framework espera código en:
```
04-Generated/scripts/
├─ problem.py ........... Clases Problem, Solution
├─ ast_nodes.py ......... Nodos AST
├─ fitness.py ........... Evaluador, FitnessFunction
├─ metaheuristic.py ..... Algoritmo principal (ILS)
└─ data_loader.py ....... Carga de instancias
```

**Pero GCP-ILS está en**:
```
projects/GCP-ILS/
├─ core/ ................ problema.py, solution.py, evaluation.py
├─ operators/ ........... constructive.py, local_search.py, etc.
├─ metaheuristic/ ....... ils_core.py
├─ data/ ................ parser.py, loader.py
└─ scripts/ ............. main scripts
```

**Estrategia**: Seguir patrón KBP-SA, pero usar datos GCP

---

## 🚀 SECUENCIA DE ENSAMBLADO RECOMENDADA

### Paso 1: DATOS (YA COMPLETADO ✓)

```bash
# Instancias en:
projects/GCP-ILS/datasets/{CUL,DSJ,LEI,MYC,REG,SCH,SGB}/
# Total: 79 .col files (menos myciel2.col que está incompleto)
# Metadata: projects/GCP-ILS/datasets/documentation/metadata.json
# Loader: projects/GCP-ILS/datasets/documentation/loader.py
```

### Paso 2: ESPECIFICACIÓN (YA COMPLETADA ✓)

```bash
# Problema: projects/GCP-ILS/problema_metaheuristica.md
# Config: projects/GCP-ILS/config.yaml
# 15 terminales documentados
# Parámetros ILS definidos
```

### Paso 3: CREAR ESTRUCTURA CORE (EN PROGRESO)

```bash
# Crear directorios
mkdir -p projects/GCP-ILS/core
mkdir -p projects/GCP-ILS/data
mkdir -p projects/GCP-ILS/operators
mkdir -p projects/GCP-ILS/metaheuristic
mkdir -p projects/GCP-ILS/gaa
mkdir -p projects/GCP-ILS/experimentation
mkdir -p projects/GCP-ILS/utils
mkdir -p projects/GCP-ILS/tests
mkdir -p projects/GCP-ILS/scripts

# Crear __init__.py en cada directorio
```

### Paso 4: IMPLEMENTAR MÓDULOS CORE

**Orden de implementación:**

1. **data/parser.py** (150 líneas)
   - DIMACParser.parse(filepath) → (n, edges)
   - Validación de formato

2. **core/problem.py** (250 líneas)
   - GraphColoringProblem class
   - Métodos: get_neighbors(), is_adjacent(), get_degree()
   - Load from DIMACS

3. **core/solution.py** (200 líneas)
   - ColoringSolution class
   - count_conflicts(), is_feasible(), copy()

4. **core/evaluation.py** (150 líneas)
   - ColoringEvaluator class
   - evaluate(solution) → fitness
   - gap_to_optimal()

5. **data/loader.py** (100 líneas)
   - DataLoader class
   - Integración con datasets/documentation/loader.py

### Paso 5: IMPLEMENTAR OPERADORES

6. **operators/constructive.py** (350 líneas)
   - GreedyDSATUR
   - GreedyLargestFirst
   - RandomSequential
   - [hasta 5 constructivos]

7. **operators/local_search.py** (350 líneas)
   - KempeChain
   - TabuCol
   - OneVertexMove
   - [hasta 4-5 mejora]

8. **operators/perturbation.py** (200 líneas)
   - RandomRecolor
   - PartialDestroy
   - [hasta 3 perturbación]

9. **operators/repair.py** (150 líneas)
   - RepairConflicts
   - BacktrackRepair

### Paso 6: IMPLEMENTAR METAHEURÍSTICA

10. **metaheuristic/ils_core.py** (350 líneas)
    - IteratedLocalSearch class
    - run() método completo
    - Statistics tracking

### Paso 7: SCRIPTS EJECUTABLES

11. **scripts/run.py** (150 líneas)
    - CLI interface
    - Instance loading
    - ILS execution

12. **scripts/demo_complete.py** (100 líneas)
    - Load 3-4 instances
    - Run ILS
    - Print results

### Paso 8: VALIDACIÓN

13. **tests/test_core.py** (250 líneas)
    - Test parsing, solution, evaluation
    - Test operators
    - Test ILS basic

---

## 📊 ARQUITECTURA DE CÓDIGO FINAL

```
projects/GCP-ILS/
│
├─ 📁 datasets/                          ✅ (79 instancias)
│  ├─ CUL/, DSJ/, LEI/, MYC/, REG/, SCH/, SGB/
│  └─ documentation/
│     ├─ loader.py
│     └─ metadata.json
│
├─ 📁 core/                              ❌ (CREAR)
│  ├─ __init__.py
│  ├─ problem.py                        → GraphColoringProblem
│  ├─ solution.py                       → ColoringSolution
│  └─ evaluation.py                     → ColoringEvaluator
│
├─ 📁 data/                              ❌ (CREAR)
│  ├─ __init__.py
│  ├─ parser.py                         → DIMACParser
│  └─ loader.py                         → DataLoader
│
├─ 📁 operators/                         ❌ (CREAR)
│  ├─ __init__.py
│  ├─ constructive.py                   → GreedyDSATUR, etc.
│  ├─ local_search.py                   → KempeChain, etc.
│  ├─ perturbation.py                   → RandomRecolor, etc.
│  └─ repair.py                         → RepairConflicts, etc.
│
├─ 📁 metaheuristic/                     ❌ (CREAR)
│  ├─ __init__.py
│  └─ ils_core.py                       → IteratedLocalSearch
│
├─ 📁 gaa/                               ❌ (CREAR)
│  ├─ __init__.py
│  ├─ ast_nodes.py                      → Nodos AST
│  └─ grammar.py                        → Gramática BNF
│
├─ 📁 experimentation/                   ❌ (CREAR)
│  ├─ __init__.py
│  ├─ runner.py                         → ExperimentRunner
│  ├─ metrics.py                        → ColoringMetrics
│  └─ visualization.py                  → Gráficas
│
├─ 📁 utils/                             ❌ (CREAR)
│  ├─ __init__.py
│  ├─ config.py                         → Config loader
│  └─ logging.py                        → Logging
│
├─ 📁 tests/                             ❌ (CREAR)
│  ├─ __init__.py
│  └─ test_core.py                      → Unit tests
│
├─ 📁 scripts/                           ❌ (CREAR)
│  ├─ demo_complete.py
│  ├─ demo_experimentation.py
│  ├─ run.py
│  ├─ validate_datasets.py
│  └─ test_quick.py
│
├─ problema_metaheuristica.md            ✅ (especificación)
├─ config.yaml                            ✅ (configuración)
├─ README.md                              ✅ (overview)
├─ requirements.txt                       ❌ (CREAR local)
└─ __init__.py                            ❌ (CREAR)
```

---

## 🔄 CICLO DE DESARROLLO CON FRAMEWORK

```
1. EDITAR: 00-Core/Problem.md, 00-Core/Metaheuristic.md
   ↓
2. SINCRONIZAR: python 05-Automation/sync-engine.py --sync
   ↓
3. DOCUMENTACIÓN SE AUTO-ACTUALIZA: 01-System/, 02-Components/, 03-Experiments/
   ↓
4. IMPLEMENTAR CÓDIGO: projects/GCP-ILS/core/, operators/, metaheuristic/
   ↓
5. VALIDAR: python 05-Automation/sync-engine.py --validate
   ↓
6. EXPERIMENTAR: python projects/GCP-ILS/scripts/demo_complete.py
   ↓
7. ANÁLISIS: python projects/GCP-ILS/scripts/demo_experimentation.py
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Preparación (Día 1)
- [x] Revisar 00-Core/Problem.md, Metaheuristic.md
- [x] Entender sync-engine.py
- [x] Documentación dataset lista
- [x] 79 instancias descargadas (excepto myciel2.col)
- [ ] Crear estructura de directorios

### Core (Días 1-2)
- [ ] data/parser.py
- [ ] core/problem.py
- [ ] core/solution.py
- [ ] core/evaluation.py
- [ ] data/loader.py

### Operadores (Días 2-3)
- [ ] operators/constructive.py (al menos 3)
- [ ] operators/local_search.py (al menos 2)
- [ ] operators/perturbation.py
- [ ] operators/repair.py

### Metaheurística (Día 3)
- [ ] metaheuristic/ils_core.py

### Scripts (Día 3-4)
- [ ] scripts/run.py
- [ ] scripts/demo_complete.py
- [ ] tests/test_core.py

### Experimentos (Día 4-5)
- [ ] experimentation/runner.py
- [ ] experimentation/metrics.py
- [ ] scripts/demo_experimentation.py

### GAA (Día 5+)
- [ ] gaa/ast_nodes.py
- [ ] gaa/grammar.py

---

## 📌 REFERENCIAS DURANTE IMPLEMENTACIÓN

**Para cada módulo, copiar patrón de:**
```
KBP-SA/core/ → GCP-ILS/core/
KBP-SA/operators/ → GCP-ILS/operators/
KBP-SA/metaheuristic/sa_core.py → GCP-ILS/metaheuristic/ils_core.py
KBP-SA/experimentation/ → GCP-ILS/experimentation/
KBP-SA/scripts/ → GCP-ILS/scripts/
KBP-SA/tests/ → GCP-ILS/tests/
```

**Adaptando:**
- Knapsack Problem → Graph Coloring Problem
- SA parámetros → ILS parámetros
- KnapsackSolution → ColoringSolution
- KnapsackEvaluator → ColoringEvaluator

---

**¿Listo para comenzar Fase 1 - Estructura de directorios? ✓**
