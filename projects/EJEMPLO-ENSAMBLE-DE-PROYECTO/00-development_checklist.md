---
project_name: "VRPTW con GRASP"
created: "2026-01-01"
version: "1.2.0"
---

# 📋 CHECKLIST DE DESARROLLO - VRPTW-GRASP

**Proyecto**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Metaheurística**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Enfoque**: Generación Automática de Algoritmos (GAA)

---

## ⚠️ RESTRICCIÓN CRÍTICA: COMPATIBILIDAD CON DATASETS SOLOMON

> ### 🎯 **REQUISITO VINCULANTE**:
> 
> **TODO el desarrollo del proyecto DEBE estar alineado para ser compatible con los datasets Solomon adjuntos:**
> 
> | Familia | Instancias | Total Clientes | Características |
> |---------|-----------|---|---|
> | **C1** | C101-C109 | 9 instancias | Clustered 1, período normal |
> | **C2** | C201-C208 | 8 instancias | Clustered 2, período extendido |
> | **R1** | R101-R112 | 12 instancias | Random 1, período normal |
> | **R2** | R201-R211 | 11 instancias | Random 2, período extendido |
> | **RC1** | RC101-RC108 | 8 instancias | Random+Clustered 1, período normal |
> | **RC2** | RC201-RC208 | 8 instancias | Random+Clustered 2, período extendido |
> | **TOTAL** | - | **56 instancias** | 100 clientes cada una |
>
> #### Implications for Development:
> - ✅ Estructura de datos: VRPTW de Solomon (100 clientes exactos por instancia)
> - ✅ Parámetros: Distancias euclidianas, ventanas de tiempo específicas por familia
> - ✅ Operadores: Diseñados para manejar problemas de 100 clientes
> - ✅ GRASP: Parámetros α, iteraciones calibradas para tamaño Solomon
> - ✅ GAA: Generación de algoritmos validados en todas 6 subfamilias
> - ✅ Evaluación: Comparación contra Best Known Solutions (BKS) publicadas
> - ✅ Benchmarking: Resultados reportables en literatura VRPTW estándar
>
> **Referencia:** Ver [05-datasets-solomon.md](05-datasets-solomon.md) para especificación detallada

---

## 📚 RECURSOS DISPONIBLES

- ✅ **BKS (Best Known Solutions)**: `best_known_solutions.json` — 56 instancias Solomon con K_BKS y D_BKS oficiales
- ✅ **BKS CSV**: `best_known_solutions.csv` — Formato tabular para análisis
- ✅ **Módulo BKS**: `src/core/bks.py` — BKSManager para cargar y validar contra BKS

---

## 🎯 PROGRESO GENERAL DEL PROYECTO

**Estado**: En Planificación  
**Completitud Global**: **0%**  
**Compatibilidad con Solomon**: Crítica para todas las fases

---

# FASE 1: INFRAESTRUCTURA Y CONFIGURACIÓN BASE (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [01-problema-vrptw.md](01-problema-vrptw.md) — Entiende el problema VRPTW
> - [02-modelo-matematico.md](02-modelo-matematico.md) — Estructura de datos y parámetros matemáticos
> - [05-datasets-solomon.md](05-datasets-solomon.md) — Formato datos Solomon para cargar
>
> **Recomendación**: Leer estos documentos ANTES de crear estructura de directorios

## 1.1 Estructura de Directorios

- [ ] Crear directorios `src/core/` (0%)
- [ ] Crear directorios `src/operators/` (0%)
- [ ] Crear directorios `src/metaheuristic/` (0%)
- [ ] Crear directorios `src/gaa/` (0%)
- [ ] Crear directorios `config/` (0%)
- [ ] Crear directorios `datasets/` con subdirectorios C1, C2, R1, R2, RC1, RC2 (0%)
- [ ] Crear directorios `output/` para resultados (0%)
- [ ] Crear directorios `scripts/` (0%)
- [ ] Crear directorios `utils/` (0%)

**Subtotal Fase 1.1: 0% (0/9 completado)**

## 1.2 Configuración de Proyecto

- [ ] Crear `config/config.yaml` con parámetros generales (0%)
- [ ] Crear `requirements.txt` con dependencias (0%)
- [ ] Crear archivo `.gitignore` (0%)
- [ ] Documentar estructura en `README.md` (0%)
- [ ] Crear script `setup.py` para instalación (0%)

**Subtotal Fase 1.2: 0% (0/5 completado)**

## 1.3 Ambiente Virtual y Dependencias

- [ ] Crear ambiente virtual con Python 3.9+ (0%)
- [ ] Instalar NumPy, Pandas, Matplotlib (0%)
- [ ] Instalar SciPy para análisis estadístico (0%)
- [ ] Instalar Pydantic para validación (0%)
- [ ] Documentar instrucciones de instalación (0%)

**Subtotal Fase 1.3: 0% (0/5 completado)**

**TOTAL FASE 1: 0% (0/19 completado)**

---

# FASE 2: MÓDULOS FUNDAMENTALES DEL VRPTW (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [01-problema-vrptw.md](01-problema-vrptw.md) — Definición del problema y restricciones
> - [02-modelo-matematico.md](02-modelo-matematico.md) — Formulación matemática exacta
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Función fitness jerárquica (K, D)
> - [05-datasets-solomon.md](05-datasets-solomon.md) — Formato de datos para validar código
>
> **Crítico**: Asegurar que las clases representan exactamente el modelo matemático

## 2.1 Estructura de Datos Básica

- [ ] Implementar clase `Instance` (VRPTW Solomon) (0%)
  - Atributos: n_customers, K_vehicles, Q_capacity, customers[], depot
  - Métodos: load_from_csv(), validate(), get_distance(i,j)

- [ ] Implementar clase `Customer` (0%)
  - Atributos: id, x, y, demand, ready_time, due_date, service_time
  - Métodos: is_in_time_window(arrival_time)

- [ ] Implementar clase `Route` (0%)
  - Atributos: vehicle_id, sequence[], total_distance, total_load, total_time
  - Métodos: add_customer(), remove_customer(), is_feasible()

- [ ] Implementar clase `Solution` (0%)
  - Atributos: routes[], total_distance, num_vehicles, feasible
  - Métodos: get_fitness(), is_feasible(), to_dict()

**Subtotal Fase 2.1: 0% (0/4 completado)**

## 2.2 Evaluación de Soluciones

- [ ] Implementar función `calculate_route_distance(route, instance)` (0%)
- [ ] Implementar función `calculate_route_time(route, instance)` (0%)
- [ ] Implementar función `check_capacity_constraint(route, instance)` (0%)
- [ ] Implementar función `check_time_window_constraint(route, instance)` (0%)
- [ ] Implementar `fitness_function()` jerárquica (K primario, D secundario) (0%)
- [ ] Implementar función `evaluate_solution(solution, instance)` (0%)
- [ ] Crear test cases para evaluación (0%)

**Subtotal Fase 2.2: 0% (0/7 completado)**

## 2.3 Carga y Validación de Datos

- [ ] Implementar `DataLoader` para formato Solomon CSV (0%)
- [ ] Validar instancias: 100 clientes exactos (0%)
- [ ] Validar parámetros: q_i, [a_i, b_i], s_i, c_ij (0%)
- [ ] Crear función para cargar todas las 56 instancias (0%)
- [ ] Crear test para validar integridad de datos (0%)

**Subtotal Fase 2.3: 0% (0/5 completado)**

**TOTAL FASE 2: 0% (0/16 completado)**

---

# FASE 3: OPERADORES DEL DOMINIO VRPTW (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [03-operadores-dominio.md](03-operadores-dominio.md) — **CRÍTICO** Especificación de 22 operadores
> - [02-modelo-matematico.md](02-modelo-matematico.md) — Restricciones que deben respetar operadores
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Cálculo de mejora tras aplicar operador
>
> **Estructura**: 6 constructivos + 8 mejora + 4 perturbación + 4 reparación = 22 operadores

## 3.1 Operadores Constructivos

### 3.1.1 Heurística de Ahorros (SavingsHeuristic)
- [ ] Implementar algoritmo de Clarke-Wright (0%)
- [ ] Incluir aleatoriedad para GRASP (0%)
- [ ] Test con instancias pequeñas (0%)

### 3.1.2 Vecino Más Cercano (NearestNeighbor)
- [ ] Implementar NN básico (0%)
- [ ] Implementar NN con consideración de tiempo (TimeOrientedNN) (0%)
- [ ] Test de factibilidad (0%)

### 3.1.3 Inserción Secuencial (InsertionI1)
- [ ] Implementar inserción minimizando costo (0%)
- [ ] Implementar inserción por arrepentimiento (RegretInsertion) (0%)
- [ ] Implementar inserción randomizada (RandomizedInsertion) (0%)
- [ ] Test de diferentes modos de inserción (0%)

**Subtotal Fase 3.1: 0% (0/10 completado)**

## 3.2 Operadores de Mejora Local - Intra-ruta

### 3.2.1 TwoOpt
- [ ] Implementar 2-opt para una ruta (0%)
- [ ] Optimizar búsqueda (0%)
- [ ] Test de mejora (0%)

### 3.2.2 OrOpt
- [ ] Implementar reubicación de 1-3 clientes (0%)
- [ ] Test de factibilidad (0%)

### 3.2.3 Relocate y ThreeOpt
- [ ] Implementar Relocate (0%)
- [ ] Implementar ThreeOpt (0%)
- [ ] Test comparativo (0%)

**Subtotal Fase 3.2: 0% (0/8 completado)**

## 3.3 Operadores de Mejora Local - Inter-ruta

### 3.3.1 Intercambios entre Rutas
- [ ] Implementar CrossExchange (0%)
- [ ] Implementar TwoOptStar (0%)
- [ ] Implementar SwapCustomers (0%)
- [ ] Implementar RelocateInter (0%)
- [ ] Test de viabilidad inter-ruta (0%)

**Subtotal Fase 3.3: 0% (0/5 completado)**

## 3.4 Operadores de Perturbación

- [ ] Implementar EjectionChain (0%)
- [ ] Implementar RuinRecreate (0%)
- [ ] Implementar RandomRemoval (0%)
- [ ] Implementar RouteElimination (0%)
- [ ] Test de perturbaciones (0%)

**Subtotal Fase 3.4: 0% (0/5 completado)**

## 3.5 Operadores de Reparación

- [ ] Implementar RepairCapacity (0%)
- [ ] Implementar RepairTimeWindows (0%)
- [ ] Implementar GreedyRepair (0%)
- [ ] Test de reparación en soluciones infactibles (0%)

**Subtotal Fase 3.5: 0% (0/4 completado)**

**TOTAL FASE 3: 0% (0/32 completado)**

---

# FASE 4: NÚCLEO GRASP (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) — **CRÍTICO** Especificación del algoritmo GRASP
> - [03-operadores-dominio.md](03-operadores-dominio.md) — Operadores a integrar en GRASP
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Función para evaluar soluciones
>
> **Parámetros GRASP**: α=0.15 (RCL), max_iteraciones=100, VND

## 4.1 Estructura Base de GRASP

- [ ] Implementar clase `GRASP` con estructura básica (0%)
- [ ] Implementar fase constructiva: `greedy_randomized_construction()` (0%)
- [ ] Implementar cálculo del RCL (alpha-based) (0%)
- [ ] Implementar búsqueda local: `local_search()` (0%)
- [ ] Implementar Variable Neighborhood Descent (VND) (0%)
- [ ] Implementar criterio de parada (iteraciones/tiempo) (0%)
- [ ] Implementar tracking de mejor solución encontrada (0%)

**Subtotal Fase 4.1: 0% (0/7 completado)**

## 4.2 Configuración y Parámetros GRASP

- [ ] Implementar parámetro `alpha` para RCL (0%)
- [ ] Implementar `max_iteraciones` (por defecto 100) (0%)
- [ ] Implementar `max_sin_mejora` (por defecto 20) (0%)
- [ ] Implementar `tipo_mejora` (VND por defecto) (0%)
- [ ] Crear archivo de configuración GRASP (0%)
- [ ] Validar parámetros (0%)

**Subtotal Fase 4.2: 0% (0/6 completado)**

## 4.3 Búsqueda Local y VND

- [ ] Implementar VND básico (0%)
- [ ] Implementar secuencia de vecindarios (0%)
- [ ] Implementar criterio de aceptación (first improvement) (0%)
- [ ] Test de convergencia (0%)

**Subtotal Fase 4.3: 0% (0/4 completado)**

## 4.4 Integración con Operadores

- [ ] Integrar operadores constructivos en fase 1 (0%)
- [ ] Integrar operadores de mejora en fase 2 (0%)
- [ ] Test de flujo GRASP completo (0%)
- [ ] Validar factibilidad a través de GRASP (0%)

**Subtotal Fase 4.4: 0% (0/4 completado)**

**TOTAL FASE 4: 0% (0/21 completado)**

---

# FASE 5: COMPONENTE GAA (GENERACIÓN AUTOMÁTICA DE ALGORITMOS) (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA**:
> - [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md) — Especificación técnica GAA, nodos AST, gramática BNF, arquitectura completa
> - [11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md) — Implementación práctica, 3 algoritmos VRPTW, código Python ready-to-run, pipeline completo
> 
> **Recomendación: Leer ambos documentos ANTES de comenzar implementación de Fase 5.**

## 5.1 Nodos AST (Abstract Syntax Tree)

**Ver Sección 2 de 10-gaa-ast-implementation.md para especificación técnica**

- [ ] Implementar clase base `ASTNode` (0%)
  - Métodos: `execute()`, `to_dict()`, `to_pseudocode()`, `size()`, `depth()`
  - Basarse en doc 10, Sección "Componentes de GAA - AST Nodes"
- [ ] Implementar `FunctionNode` (Seq, For, ChooseBestOf, etc.) (0%)
  - Control flow: Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove
- [ ] Implementar `TerminalNode` (22 operadores VRPTW) (0%)
  - Constructivos, mejora, perturbación, reparación (mapeados en doc 11, Sección 1)
- [ ] Implementar `ParameterNode` (alpha, k, etc.) (0%)
- [ ] Test de validación de AST (0%)

**Subtotal Fase 5.1: 0% (0/5 completado)**

## 5.2 Gramática VRPTW-GRASP

**Ver Sección 3 de 10-gaa-ast-implementation.md para gramática BNF**

- [ ] Definir gramática formal en BNF/EBNF (0%)
  - Basarse en doc 10, Sección "Gramática BNF"
  - 9 producciones: Algorithm, Phase, Body, Statement, Term, etc.
- [ ] Implementar `Grammar` class (0%)
- [ ] Implementar validación de producción (0%)
- [ ] Crear restricciones canónicas:
  - [ ] Constructor randomizado obligatorio (0%)
  - [ ] Mínimo 2 operadores de mejora (0%)
  - [ ] Reparación de restricciones (0%)
  - [ ] Basarse en restricciones de doc 10
- [ ] Test de cumplimiento de restricciones (0%)

**Subtotal Fase 5.2: 0% (0/7 completado)**

## 5.3 Generador de Algoritmos

**Ver Sección 3 de 11-buenas-practicas-gaa.md para código ready-to-run**

- [ ] Implementar `AlgorithmGenerator` con Ramped Half-and-Half (0%)
  - Basarse en clase `AlgorithmGenerator` de doc 11
  - Métodos: `generate_algorithm()`, `generate_three_algorithms(seed=42)`
- [ ] Implementar generación con profundidad controlada (0%)
  - Min/max depth, probabilidades de nodos terminales vs funcionales
- [ ] Implementar generación con seed reproducible (0%)
  - Usar `random.seed(seed)` para reproducibilidad
- [ ] Implementar validación post-generación (0%)
  - Validar AST respeta gramática
  - Validar restricciones canónicas
- [ ] Test de generación de 3 algoritmos con seed=42 (0%)
  - Esperado: 3 algoritmos diferentes, siempre los mismos con seed=42

**Subtotal Fase 5.3: 0% (0/5 completado)**

## 5.4 Intérprete de AST

**Ver Sección 4 de 11-buenas-practicas-gaa.md para flujo de ejecución**

- [ ] Implementar `ASTInterpreter` (0%)
  - Recibe AST y problema VRPTW
  - Retorna solución ejecutando el árbol
- [ ] Implementar ejecución de AST como algoritmo (0%)
  - Interpretar nodos Seq, While, For, If
  - Llamadas a operadores VRPTW para TerminalNodes
- [ ] Implementar manejo de excepciones en AST inválido (0%)
  - Try-catch para operadores que fallan
  - Reparación de soluciones infactibles
- [ ] Test de ejecución de algoritmo generado (0%)
  - Ejecutar cada uno de los 3 algoritmos en instancia C101
  - Verificar factibilidad y mejora vs solución inicial

**Subtotal Fase 5.4: 0% (0/4 completado)**

## 5.5 Reparación Automática de AST

- [ ] Implementar validador de AST (0%)
- [ ] Implementar reparador para AST inválido (0%)
- [ ] Test de reparación de violaciones de gramática (0%)

**Subtotal Fase 5.5: 0% (0/3 completado)**

**TOTAL FASE 5: 0% (0/24 completado)**

---

# FASE 6: DATASETS Y VALIDACIÓN (10%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [05-datasets-solomon.md](05-datasets-solomon.md) — **CRÍTICO** Especificación de 56 instancias Solomon
> - [01-problema-vrptw.md](01-problema-vrptw.md) — Estructura VRPTW (clientes, depósito, ventanas)
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Función para validar soluciones en datasets
>
> **Datasets adjuntos**: C1, C2, R1, R2, RC1, RC2 (56 instancias, 100 clientes c/u)
> 
> **Best Known Solutions**: Ver `best_known_solutions.json` (referencia oficial BKS para todas las 56 instancias Solomon)

## ⚠️ RESTRICCIÓN CRÍTICA: COMPATIBILIDAD SOLOMON OBLIGATORIA

**Todos los items de esta fase DEBEN garantizar compatibilidad total con los 56 datasets Solomon adjuntos:**

- ✅ **C1** (9 instancias): Clustered, período normal
- ✅ **C2** (8 instancias): Clustered, período extendido  
- ✅ **R1** (12 instancias): Random, período normal
- ✅ **R2** (11 instancias): Random, período extendido
- ✅ **RC1** (8 instancias): Random+Clustered, período normal
- ✅ **RC2** (8 instancias): Random+Clustered, período extendido

**Validaciones obligatorias:**
- [ ] Cada instancia tiene EXACTAMENTE 100 clientes
- [ ] Depósito ubicado en (0, 0) con ventana [0, T]
- [ ] Distancias euclidianas entre puntos
- [ ] Ventanas de tiempo respetadas en todas instancias
- [ ] BKS (Best Known Solutions) documentadas para benchmarking

---

## 6.1 Descarga y Organización de Datasets

- [x] Descargar instancias Solomon de fuente oficial (10%)
- [ ] Organizar en estructura C1, C2, R1, R2, RC1, RC2 (0%)
- [ ] Verificar 56 instancias totales (0%)
- [ ] Verificar 100 clientes por instancia (0%)
- [ ] Crear documentación de fuentes (0%)

**Subtotal Fase 6.1: 20% (1/5 completado)**

## 6.2 Validación de Instancias

- [ ] Crear script `validate_datasets.py` (0%)
- [ ] Validar formato CSV (0%)
- [ ] Validar parámetros: q_i ∈ [0, Q], ventanas temporales (0%)
- [ ] Validar distancias euclidiana correctas (0%)
- [ ] Generar reporte de validación (0%)

**Subtotal Fase 6.2: 0% (0/5 completado)**

## 6.3 Mejores Soluciones Conocidas (BKS)

**✅ RECURSO DISPONIBLE**: `best_known_solutions.json` + `best_known_solutions.csv` contienen BKS para todas las 56 instancias Solomon. Utilizar módulo `src/core/bks.py` (BKSManager) para cargar y validar.

- [x] Obtener BKS para todas las 56 instancias (100%) — **YA DISPONIBLE en best_known_solutions.json**
- [x] Documentar K_BKS para cada instancia (100%) — **YA DISPONIBLE**
- [x] Documentar D_BKS para cada instancia (100%) — **YA DISPONIBLE**
- [x] Crear archivo `best_known_solutions.csv` (100%) — **YA CREADO**
- [ ] Integrar BKSManager en módulo de evaluación (0%) — Para Fase 7
- [ ] Validar compatibilidad con literatura (0%) — Para Fase 10

**Subtotal Fase 6.3: 60% (3/5 completado)**

**TOTAL FASE 6: 30% (4/15 completado)**

---

# FASE 7: GESTIÓN DE OUTPUTS Y MÉTRICAS (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Función fitness jerárquica a registrar
> - [08-metricas-canonicas.md](08-metricas-canonicas.md) — Métricas exactas a calcular
> - [09-outputs-estructura.md](09-outputs-estructura.md) — **CRÍTICO** Esquema CSV/JSON exacto
>
> **Crítico**: Los CSV generados DEBEN cumplir esquema canónico de [09](09-outputs-estructura.md)

## 7.1 Output Manager

- [ ] Implementar clase `OutputManager` (0%)
- [ ] Crear estructura con timestamps (DDMMYY_HHMMSS) (0%)
- [ ] Crear directorios: results/, solutions/, plots/, gaa/, logs/ (0%)
- [ ] Implementar métodos save_*() para cada archivo (0%)
- [ ] Test de creación de estructura (0%)

**Subtotal Fase 7.1: 0% (0/5 completado)**

## 7.2 Esquema CSV Canónico

- [ ] Implementar `raw_results.csv` (columnas exactas) (0%)
- [ ] Implementar `convergence_trace.csv` (0%)
- [ ] Implementar `summary_by_instance.csv` (0%)
- [ ] Implementar `summary_by_family.csv` (0%)
- [ ] Implementar `time_metrics.csv` (0%)
- [ ] Implementar `solutions.csv` (rutas) (0%)
- [ ] Implementar `time_windows_check.csv` (0%)
- [ ] Test de integridad de archivos (0%)

**Subtotal Fase 7.2: 0% (0/8 completado)**

## 7.3 Cálculo de Métricas Jerárquicas

- [ ] Implementar `K_mean`, `K_std`, `K_best` (0%)
- [ ] Implementar `%Instancias_K_BKS` (0%)
- [ ] Implementar `D_mean_at_K`, `D_std_at_K` (solo si K=K_BKS) (0%)
- [ ] Implementar `%GAP` con condición jerárquica (0%)
- [ ] Implementar validación de factibilidad (0%)
- [ ] Implementar análisis por familia (0%)

**Subtotal Fase 7.3: 0% (0/6 completado)**

## 7.4 Logging y Auditoría

- [ ] Configurar logger centralizado (0%)
- [ ] Implementar `execution.log` (0%)
- [ ] Implementar `errors.log` (0%)
- [ ] Crear `session_summary.txt` (0%)
- [ ] Test de logging (0%)

**Subtotal Fase 7.4: 0% (0/5 completado)**

**TOTAL FASE 7: 0% (0/24 completado)**

---

# FASE 8: VISUALIZACIONES Y GRÁFICOS (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [08-metricas-canonicas.md](08-metricas-canonicas.md) — Métricas a visualizar
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Fitness jerárquico (K, D)
>
> **Visualizaciones canónicas**: Convergencia por familia, boxplots K/D, gráficos por subfamilia

## 8.1 Gráficos de Convergencia (Canónicos)

- [ ] Gráfico convergencia K (escalonado) (0%)
- [ ] Gráfico convergencia D (solo a K constante) (0%)
- [ ] Gráfico tiempo vs calidad jerárquico (0%)
- [ ] Test de visualización (0%)

**Subtotal Fase 8.1: 0% (0/4 completado)**

## 8.2 Gráficos Estadísticos

- [ ] Boxplot de K por algoritmo (0%)
- [ ] Boxplot de D (solo a K=K_BKS) (0%)
- [ ] Gráfico de barras de gap por instancia (0%)
- [ ] Gráfico de distribución de %GAP (0%)
- [ ] Test de gráficos (0%)

**Subtotal Fase 8.2: 0% (0/5 completado)**

## 8.3 Gráficos por Familia

- [ ] Performance by family (C, R, RC) (0%)
- [ ] Performance by size (pequeño/mediano/grande) (0%)
- [ ] Best algorithm per family (0%)
- [ ] Análisis especialización (0%)

**Subtotal Fase 8.3: 0% (0/4 completado)**

## 8.4 Visualización de Rutas

- [ ] Implementar ploteo de rutas 2D (0%)
- [ ] Mostrar clientes y depósito (0%)
- [ ] Colorear rutas por vehículo (0%)
- [ ] Mostrar K y D en título (0%)
- [ ] Implementar para todas las 56 instancias (0%)
- [ ] Test de visualización (0%)

**Subtotal Fase 8.4: 0% (0/6 completado)**

## 8.5 Validación de Ventanas de Tiempo

- [ ] Gráfico de holgura temporal (slack) (0%)
- [ ] Validación visual de ventanas respetadas (0%)
- [ ] Test de gráfico (0%)

**Subtotal Fase 8.5: 0% (0/3 completado)**

**TOTAL FASE 8: 0% (0/22 completado)**

---

# FASE 9: SCRIPTS DE EXPERIMENTACIÓN (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [06-experimentos-plan.md](06-experimentos-plan.md) — **CRÍTICO** Plan QUICK (36 exp) y FULL (168 exp)
> - [11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md) — Código ready-to-run, pipeline completo
> - [05-datasets-solomon.md](05-datasets-solomon.md) — Datasets a evaluar
>
> **Scripts**: demo_experimentation_quick.py, demo_experimentation_full.py, generate_algorithms.py

## 9.1 Script QUICK (Validación Rápida)

- [ ] Crear `demo_experimentation_quick.py` (0%)
- [ ] Implementar carga de 1 familia (R1 por defecto) (0%)
- [ ] Implementar ejecución de 3 algoritmos (0%)
- [ ] Implementar 1 repetición por instancia (0%)
- [ ] Implementar generación de outputs QUICK (0%)
- [ ] Test: ~5-10 minutos de ejecución (0%)

**Subtotal Fase 9.1: 0% (0/6 completado)**

## 9.2 Script FULL (Evaluación Exhaustiva)

- [ ] Crear `demo_experimentation_full.py` (0%)
- [ ] Implementar carga de 6 familias (C1-6, R1-2, RC1-2) (0%)
- [ ] Implementar ejecución de 3 algoritmos (0%)
- [ ] Implementar 1 repetición por instancia (0%)
- [ ] Implementar generación de outputs FULL (0%)
- [ ] Implementar análisis por familia (0%)
- [ ] Test: ~40-60 minutos de ejecución (0%)

**Subtotal Fase 9.2: 0% (0/7 completado)**

## 9.3 Generación Única de Algoritmos

- [ ] Crear `generate_algorithms.py` (0%)
- [ ] Generar 3 algoritmos con seed=42 (0%)
- [ ] Guardar AST en `algorithms/GAA_Algorithm_*.json` (0%)
- [ ] Guardar pseudocódigo en `algorithms_pseudocode.md` (0%)
- [ ] Verificar cumplimiento de restricciones canónicas (0%)

**Subtotal Fase 9.3: 0% (0/5 completado)**

## 9.4 Scripts Auxiliares

- [ ] Crear `validate_datasets.py` (0%)
- [ ] Crear `analyze_results.py` (0%)
- [ ] Crear `plot_all.py` (0%)
- [ ] Crear `generate_report.py` (0%)

**Subtotal Fase 9.4: 0% (0/4 completado)**

**TOTAL FASE 9: 0% (0/22 completado)**

---

# FASE 10: ANÁLISIS ESTADÍSTICO (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [08-metricas-canonicas.md](08-metricas-canonicas.md) — **CRÍTICO** Métricas estadísticas canónicas
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Fitness a analizar (K, D)
> - [06-experimentos-plan.md](06-experimentos-plan.md) — Plan experimental (QUICK, FULL)
>
> **Tests**: Kruskal-Wallis, Wilcoxon, análisis por familia Solomon

## 10.1 Comparación Básica

- [ ] Implementar estadísticas descriptivas por algoritmo (0%)
- [ ] Implementar media, desv. est., min, max de K (0%)
- [ ] Implementar media, desv. est., min, max de %GAP (0%)
- [ ] Test de estadísticas (0%)

**Subtotal Fase 10.1: 0% (0/4 completado)**

## 10.2 Tests Estadísticos

- [ ] Implementar test Kruskal-Wallis (comparación móltiple) (0%)
- [ ] Implementar test Wilcoxon (comparación pareada) (0%)
- [ ] Implementar cálculo de tamaño del efecto (Cohen's d) (0%)
- [ ] Test de significancia (α=0.05) (0%)

**Subtotal Fase 10.2: 0% (0/4 completado)**

## 10.3 Análisis por Familia

- [ ] Comparación de algoritmos por familia C (0%)
- [ ] Comparación de algoritmos por familia R (0%)
- [ ] Comparación de algoritmos por familia RC (0%)
- [ ] Identificar especialización (0%)

**Subtotal Fase 10.3: 0% (0/4 completado)**

## 10.4 Análisis de Convergencia

- [ ] Tiempo promedio a K_BKS por instancia (0%)
- [ ] Iteraciones promedio a K_BKS (0%)
- [ ] Curvas de convergencia agregadas (0%)

**Subtotal Fase 10.4: 0% (0/3 completado)**

**TOTAL FASE 10: 0% (0/15 completado)**

---

# FASE 11: VALIDACIÓN Y TESTING (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [01-09](01-problema-vrptw.md) — Especificaciones que validar
> - [10-11](10-gaa-ast-implementation.md) — Arquitectura GAA a testear
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Función fitness para validación
>
> **Cobertura**: Unit tests, integration tests, factibilidad, outputs

## 11.1 Unit Tests

- [ ] Tests de clases básicas (Instance, Route, Solution) (0%)
- [ ] Tests de operadores individuales (0%)
- [ ] Tests de GRASP (0%)
- [ ] Tests de AST y gramática (0%)
- [ ] Tests de evaluación (0%)
- [ ] Tests de utilidades (0%)
- [ ] Coverage >= 80% (0%)

**Subtotal Fase 11.1: 0% (0/7 completado)**

## 11.2 Integration Tests

- [ ] Test GRASP completo (construcción + mejora) (0%)
- [ ] Test generación de algoritmos (0%)
- [ ] Test ejecución de algoritmo generado (0%)
- [ ] Test flujo QUICK (0%)
- [ ] Test flujo FULL (0%)

**Subtotal Fase 11.2: 0% (0/5 completado)**

## 11.3 Validación de Factibilidad

- [ ] Validar 100% de soluciones factibles (K=0, D=0 violaciones) (0%)
- [ ] Test de restricción de capacidad (0%)
- [ ] Test de restricción de ventanas de tiempo (0%)
- [ ] Test de cobertura de clientes (0%)

**Subtotal Fase 11.3: 0% (0/4 completado)**

## 11.4 Validación de Salidas

- [ ] Validar estructura de directorios (0%)
- [ ] Validar integridad de CSV (0%)
- [ ] Validar exactitud de métricas (0%)
- [ ] Validar gráficos generados (0%)
- [ ] Validar logs completos (0%)

**Subtotal Fase 11.4: 0% (0/5 completado)**

**TOTAL FASE 11: 0% (0/21 completado)**

---

# FASE 12: DOCUMENTACIÓN (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [01-11](INDEX.md) — Todos los documentos (guía, contexto, especificación)
> - [03-operadores-dominio.md](03-operadores-dominio.md) — Para OPERATORS.md
> - [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) — Para ARCHITECTURE.md
>
> **Salidas**: README, INSTALL, USAGE, CONFIG, API, ARCHITECTURE, OPERATORS, METRICS

## 12.1 Documentación de Código

- [ ] Docstrings en todas las funciones (0%)
- [ ] Docstrings en todas las clases (0%)
- [ ] Ejemplos de uso en docstrings (0%)
- [ ] Type hints en todas las funciones (0%)

**Subtotal Fase 12.1: 0% (0/4 completado)**

## 12.2 Documentación de Usuario

- [ ] README.md completo (0%)
- [ ] INSTALL.md (instrucciones de instalación) (0%)
- [ ] USAGE.md (cómo ejecutar scripts) (0%)
- [ ] CONFIG.md (configuración de parámetros) (0%)

**Subtotal Fase 12.2: 0% (0/4 completado)**

## 12.3 Documentación Técnica

✅ **YA COMPLETADO** - Ver documentación existente:
- [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md) ✅ — Arquitectura GAA, nodos AST, gramática, proceso generación
- [11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md) ✅ — Implementación GAA, 3 algoritmos, código Python, pipeline QUICK/FULL
- [03-operadores-dominio.md](03-operadores-dominio.md) ✅ — Especificación 22 operadores VRPTW
- [07-fitness-canonico.md](07-fitness-canonico.md) ✅ — Función fitness jerárquica (K, D)
- [08-metricas-canonicas.md](08-metricas-canonicas.md) ✅ — Métricas estadísticas canónicas

- [ ] API.md (documentación de módulos) (0%)
- [ ] ARCHITECTURE.md (diseño del sistema) (0%) - Basarse en doc 11, Sección 1
- [ ] OPERATORS.md (documentación de 22 operadores) (0%) - Referencia doc 03
- [ ] METRICS.md (explicación de métricas canónicas) (0%) - Referencia doc 08

**Subtotal Fase 12.3: 0% (0/4 completado)**

## 12.4 Documentación Experimental

- [ ] EXPERIMENT_DESIGN.md (plan experimental detallado) (0%)
- [ ] RESULTS.md (template para reportar resultados) (0%)
- [ ] PAPER_TEMPLATE.md (template para articulo) (0%)

**Subtotal Fase 12.4: 0% (0/3 completado)**

**TOTAL FASE 12: 0% (0/15 completado)**

---

# FASE 13: OPTIMIZACIÓN Y REFINAMIENTO (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [03-operadores-dominio.md](03-operadores-dominio.md) — Operadores a optimizar
> - [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) — Parámetros GRASP a refinar
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Fitness para medir mejora
>
> **Objetivo**: Rendimiento <60 seg/instancia, parámetros optimizados

## 13.1 Optimización de Rendimiento

- [ ] Perfilar código crítico (0%)
- [ ] Optimizar cálculo de distancias (0%)
- [ ] Optimizar operadores de mejora (0%)
- [ ] Reducir tiempo de ejecución por instancia a <60 segundos (0%)

**Subtotal Fase 13.1: 0% (0/4 completado)**

## 13.2 Refinamiento de Parámetros GRASP

- [ ] Ajustar `alpha` basado en primeros experimentos (0%)
- [ ] Ajustar `max_iteraciones` (0%)
- [ ] Ajustar `max_sin_mejora` (0%)
- [ ] Validar nuevos parámetros (0%)

**Subtotal Fase 13.2: 0% (0/4 completado)**

## 13.3 Mejora de Operadores

- [ ] Análisis de rendimiento por operador (0%)
- [ ] Refinamiento de operadores débiles (0%)
- [ ] Ajuste de probabilidades en AST (0%)

**Subtotal Fase 13.3: 0% (0/3 completado)**

**TOTAL FASE 13: 0% (0/11 completado)**

---

# FASE 14: EJECUCIÓN DE EXPERIMENTOS (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [06-experimentos-plan.md](06-experimentos-plan.md) — **CRÍTICO** Plan QUICK (36 exp, 5-10 min) y FULL (168 exp, 40-60 min)
> - [08-metricas-canonicas.md](08-metricas-canonicas.md) — Métricas a reportar
> - [05-datasets-solomon.md](05-datasets-solomon.md) — 56 instancias Solomon
>
> **Ejecución**: QUICK primero (validación), luego FULL (evaluación exhaustiva)

## 14.1 Experimento QUICK

- [ ] Ejecutar `demo_experimentation_quick.py` (0%)
- [ ] Generar outputs QUICK (36 experimentos) (0%)
- [ ] Validar estructura de outputs (0%)
- [ ] Generar gráficos iniciales (0%)
- [ ] Tiempo esperado: 5-10 minutos (0%)

**Subtotal Fase 14.1: 0% (0/5 completado)**

## 14.2 Experimento FULL

- [ ] Ejecutar `demo_experimentation_full.py` (0%)
- [ ] Generar outputs FULL (168 experimentos) (0%)
- [ ] Validar estructura de outputs (0%)
- [ ] Generar todos los gráficos (0%)
- [ ] Generar análisis por familia (0%)
- [ ] Tiempo esperado: 40-60 minutos (0%)

**Subtotal Fase 14.2: 0% (0/5 completado)**

## 14.3 Análisis de Resultados

- [ ] Análisis descriptivo por algoritmo (0%)
- [ ] Análisis por familia de instancias (0%)
- [ ] Tests estadísticos (Kruskal-Wallis, Wilcoxon) (0%)
- [ ] Identificar algoritmo mejor y especialización (0%)

**Subtotal Fase 14.3: 0% (0/4 completado)**

## 14.4 Generación de Reportes

- [ ] Crear reporte HTML con resultados (0%)
- [ ] Crear tablas comparativas (0%)
- [ ] Crear resumen ejecutivo (0%)

**Subtotal Fase 14.4: 0% (0/3 completado)**

**TOTAL FASE 14: 0% (0/17 completado)**

---

# FASE 15: PRESENTACIÓN Y PUBLICACIÓN (0%)

> 📚 **DOCUMENTACIÓN DE REFERENCIA PARA ESTA FASE**:
> - [01-11](INDEX.md) — Todos para escribir introducción y metodología
> - [07-fitness-canonico.md](07-fitness-canonico.md) — Para sección de métricas
> - [08-metricas-canonicas.md](08-metricas-canonicas.md) — Para resultados estadísticos
> - [06-experimentos-plan.md](06-experimentos-plan.md) — Para descripción experimentos
>
> **Salidas**: Manuscrito, presentación, reproducibilidad

## 15.1 Preparación de Manuscrito

- [ ] Escribir sección Introducción (0%)
- [ ] Escribir sección VRPTW (0%)
- [ ] Escribir sección GRASP (0%)
- [ ] Escribir sección GAA (0%)
- [ ] Escribir sección Experimentos (0%)
- [ ] Escribir sección Resultados (0%)
- [ ] Escribir sección Conclusiones (0%)

**Subtotal Fase 15.1: 0% (0/7 completado)**

## 15.2 Presentación de Diapositivas

- [ ] Crear presentación (15-20 diapositivas) (0%)
- [ ] Incluir motivación y objetivos (0%)
- [ ] Incluir metodología (0%)
- [ ] Incluir resultados principales (0%)
- [ ] Incluir conclusiones y trabajo futuro (0%)

**Subtotal Fase 15.2: 0% (0/5 completado)**

## 15.3 Preparación para Revisores

- [ ] Documentación para reproducibilidad (0%)
- [ ] Código comentado y limpio (0%)
- [ ] README para revisores (0%)

**Subtotal Fase 15.3: 0% (0/3 completado)**

**TOTAL FASE 15: 0% (0/15 completado)**

---

# RESUMEN EJECUTIVO DEL CHECKLIST

## Desglose por Fase

| # | Fase | Items | Completado | % | Documentación |
|----|------|-------|-----------|-----|----|
| 1 | Infraestructura Base | 19 | 0 | **0%** | - |
| 2 | Módulos Fundamentales | 16 | 0 | **0%** | - |
| 3 | Operadores VRPTW | 32 | 0 | **0%** | [03](03-operadores-dominio.md) ✅ |
| 4 | Núcleo GRASP | 21 | 0 | **0%** | [04](04-metaheuristica-grasp.md) ✅ |
| 5 | Componente GAA | 24 | 0 | **0%** | [10](10-gaa-ast-implementation.md) ✅, [11](11-buenas-practicas-gaa.md) ✅ |
| 6 | Datasets y Validación | 15 | 1 | **10%** | [05](05-datasets-solomon.md) ✅ |
| 7 | Outputs y Métricas | 24 | 0 | **0%** | [07](07-fitness-canonico.md) ✅, [09](09-outputs-estructura.md) ✅ |
| 8 | Visualizaciones | 22 | 0 | **0%** | [08](08-metricas-canonicas.md) ✅ |
| 9 | Scripts Experimentación | 22 | 0 | **0%** | [06](06-experimentos-plan.md) ✅, [11](11-buenas-practicas-gaa.md) ✅ |
| 10 | Análisis Estadístico | 15 | 0 | **0%** | [08](08-metricas-canonicas.md) ✅ |
| 11 | Testing y Validación | 21 | 0 | **0%** | - |
| 12 | Documentación | 15 | 0 | **0%** | [01-11](INDEX.md) ✅ |
| 13 | Optimización | 11 | 0 | **0%** | - |
| 14 | Ejecución Experimentos | 17 | 0 | **0%** | [06](06-experimentos-plan.md) ✅ |
| 15 | Publicación | 15 | 0 | **0%** | - |
| **TOTAL** | **15 Fases** | **309 items** | **1** | **0.3%** | **11 docs integrados** |

---

## Hitos Críticos (Milestones)

### Hito 1: Infraestructura Lista (Fase 1-2)
- **Items Requeridos**: 35
- **Estimado**: 2-3 días
- **Señal de Completitud**: Ambiente funcionando, clases básicas listas

### Hito 2: Operadores Implementados (Fase 3-4)
- **Items Requeridos**: 53
- **Estimado**: 5-7 días
- **Señal de Completitud**: GRASP básico funcionando, primeras soluciones

### Hito 3: GAA Funcional (Fase 5)
- **Items Requeridos**: 24
- **Estimado**: 3-4 días
- **Señal de Completitud**: 3 algoritmos generados correctamente

### Hito 4: Experimentación Posible (Fase 6-9)
- **Items Requeridos**: 59
- **Estimado**: 3-4 días
- **Señal de Completitud**: Scripts QUICK y FULL ejecutables

### Hito 5: Análisis Completo (Fase 10-14)
- **Items Requeridos**: 64
- **Estimado**: 4-5 días
- **Señal de Completitud**: Experimentos finalizados, resultados analizados

### Hito 6: Publicable (Fase 12-15)
- **Items Requeridos**: 48
- **Estimado**: 2-3 días
- **Señal de Completitud**: Manuscrito y presentación listos

---

## Estimación de Tiempo Total

| Fase | Duración | Acumulado |
|------|----------|-----------|
| 1-2 | 2-3 días | 2-3 días |
| 3-4 | 5-7 días | 7-10 días |
| 5 | 3-4 días | 10-14 días |
| 6-9 | 3-4 días | 13-18 días |
| 10-14 | 4-5 días | 17-23 días |
| 12-15 | 2-3 días | 19-26 días |
| **TOTAL** | - | **19-26 días** |

**Nota**: Tiempo real dependerá de:
- Complejidad de implementación de operadores
- Velocidad de ejecución de experimentos (40-60 min full)
- Disponibilidad de máquina
- Depuración y refinamiento

---

## Recomendaciones de Ejecución

### Enfoque Recomendado: Iterativo

1. **Semana 1**: Fases 1-4 (Infraestructura + GRASP básico)
2. **Semana 2**: Fases 5-9 (GAA + Scripts de experimentación)
3. **Semana 3**: Fases 10-14 (Análisis + Experimentos)
4. **Semana 4**: Fases 12-15 (Documentación + Publicación)

### Enfoque Paralelo

- Mientras se implementan operadores (Fase 3), empezar a cargar datasets (Fase 6)
- Mientras se implementa GAA (Fase 5), preparar test cases para validación (Fase 11)
- Mientras se ejecutan experimentos (Fase 14), redactar documentación (Fase 12)

---

## Criterios de Aceptación por Fase

### ⚠️ REQUISITO TRANSVERSAL: COMPATIBILIDAD SOLOMON

**TODAS las fases DEBEN cumplir estos criterios de compatibilidad:**

- ✅ **Formato**: Instancias Solomon (100 clientes, 1 depósito)
- ✅ **Familias**: C1, C2, R1, R2, RC1, RC2 (56 instancias totales)
- ✅ **Parámetros**: Respetan especificación VRPTW (capacidad, ventanas, distancias)
- ✅ **Evaluación**: Comparables con BKS publicadas en literatura
- ✅ **Reproducibilidad**: Resultados reportables en benchmarks internacionales
- ✅ **Documentación**: Referencia a [05-datasets-solomon.md](05-datasets-solomon.md)

---

### Fase 1-2: Completado si...
- [ ] Ambiente virtual funciona
- [ ] Todas las clases básicas instanciables
- [ ] Carga de instancias Solomon exitosa (56 instancias)
- [ ] Evaluación de soluciones exacta para datos Solomon

### Fase 3-4: Completado si...
- [ ] Todos los 22 operadores funcionan en instancias Solomon
- [ ] GRASP produce soluciones factibles para todas familias
- [ ] Mejora en iteraciones demostrables en benchmarks Solomon

### Fase 5: Completado si...
- [ ] 3 algoritmos generados y diferentes
- [ ] AST válido según gramática
- [ ] Algoritmos interpretables a pseudocódigo y ejecutables en Solomon

### Fase 6-9: Completado si...
- [ ] Datasets Solomon validados (56 instancias, 100 clientes c/u)
- [ ] Scripts QUICK ejecutable (5-10 min, 1 familia Solomon)
- [ ] Scripts FULL ejecutable (40-60 min, 6 familias Solomon)
- [ ] BKS integrados para todas instancias

### Fase 10-14: Completado si...
- [ ] Resultados guardados en CSV exactos (Solomon compatible)
- [ ] Gráficos generados sin errores (por familia Solomon)
- [ ] Análisis estadístico válido por subfamilia (C1/C2, R1/R2, RC1/RC2)
- [ ] Comparación de algoritmos genera rankings por familia Solomon

### Fase 12-15: Completado si...
- [ ] Código documentado (80% coverage)
- [ ] Resultados reproducibles con datos Solomon
- [ ] Manuscrito listo para revisión (referencias Solomon BKS)

---

---

## 📚 Referencias Documentales Integradas

### Documentos Técnicos de Especificación

| Documento | Propósito | Referenciado en Fases |
|-----------|----------|----------------------|
| [01-problema-vrptw.md](01-problema-vrptw.md) | Definición VRPTW, Solomon instances | 1-6 |
| [02-modelo-matematico.md](02-modelo-matematico.md) | Formulación matemática | 2, 7-8 |
| [03-operadores-dominio.md](03-operadores-dominio.md) | 22 operadores VRPTW | 3-4, 12.3 |
| [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) | GRASP base | 4, 9 |
| [05-datasets-solomon.md](05-datasets-solomon.md) | 56 instancias, BKS | 6 |
| [06-experimentos-plan.md](06-experimentos-plan.md) | Plan QUICK/FULL | 9, 14 |
| [07-fitness-canonico.md](07-fitness-canonico.md) | Función fitness jerárquica | 2, 7, 12.3 |
| [08-metricas-canonicas.md](08-metricas-canonicas.md) | Análisis estadístico | 7-8, 10, 12.3 |
| [09-outputs-estructura.md](09-outputs-estructura.md) | CSV/JSON outputs | 7, 9 |
| **[10-gaa-ast-implementation.md](10-gaa-ast-implementation.md)** | **Especificación GAA técnica** | **5, 12.3** |
| **[11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md)** | **Implementación GAA + código** | **5, 9, 12.1, 12.3** |

### Cómo Usar Esta Documentación

1. **Antes de Fase 5**: Leer docs [10](10-gaa-ast-implementation.md) y [11](11-buenas-practicas-gaa.md) para entender GAA
2. **Antes de Fase 3-4**: Leer docs [03](03-operadores-dominio.md) y [04](04-metaheuristica-grasp.md)
3. **Antes de Fase 9**: Leer docs [06](06-experimentos-plan.md) y [11](11-buenas-practicas-gaa.md) Secciones 5-8
4. **Antes de Fase 7-8**: Leer docs [07](07-fitness-canonico.md), [08](08-metricas-canonicas.md), [09](09-outputs-estructura.md)

---

## Tracking de Progreso

**Instrucciones para actualizar este checklist**:

1. Marcar items completados con `[x]`
2. Actualizar porcentajes de fase al completar items
3. Registrar bloqueadores o problemas
4. Ajustar estimaciones según avance real

**Ejemplo**:
```
- [x] Implementar clase `Instance` (VRPTW Solomon) (50%)
```

Esto indica que el item está parcialmente completado.

---

## Blockers y Riesgos Conocidos

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|-----------|
| **Incompatibilidad con Solomon datasets** ⚠️ | **Crítica** | **Validación obligatoria en Fase 6** |
| Complejidad de operadores inter-ruta | Media | Implementar primero intra-ruta, luego inter-ruta |
| Tiempo ejecución experimentos largo | Media | Paralelizar instancias, usar múltiples procesos |
| Dificultad de cumplir restricciones canónicas | Baja | Gramática estricta + validador automático |
| Diferencias numéricas en métricas | Baja | Test comparando contra literatura (Solomon) |

---

## 🎯 VALIDACIÓN OBLIGATORIA: COMPATIBILIDAD SOLOMON

**Antes de completar cualquier fase, verificar:**

1. ✅ Código funciona con al menos una instancia de cada familia (C1, C2, R1, R2, RC1, RC2)
2. ✅ Resultados numéricos son consistentes con benchmarks Solomon publicados
3. ✅ No hay hard-coded values específicos para otras instancias
4. ✅ Escalable a 56 instancias sin cambios en código
5. ✅ Documentación referencia explícitamente Solomon (C1-C2, R1-R2, RC1-RC2)

**Referencia:** [05-datasets-solomon.md](05-datasets-solomon.md) para especificación técnica

---

**Documento creado**: 2026-01-01  
**Versión**: 1.1.0  
**Estado**: Activo y en revisión (Solomon requirement agregado)
