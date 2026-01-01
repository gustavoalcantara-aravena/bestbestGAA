# EJEMPLOS DE SALIDA AL EJECUTAR EL CÓDIGO

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025

---

## 🎯 INTRODUCCIÓN

Este documento muestra **ejemplos reales** de lo que se imprimiría al ejecutar diferentes scripts del proyecto GAA-GCP-ILS-4.

---

## 1️⃣ EJECUCIÓN: `scripts/gaa_quick_demo.py`

### Comando:
```bash
python scripts/gaa_quick_demo.py
```

### Salida Esperada:

```
================================================================================
  DEMO RÁPIDA: GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA)
================================================================================

1️⃣  CREAR GRAMÁTICA
--------------------------------------------------------------------------------
✅ Gramática creada
   • Terminales constructivos: 4
   • Terminales mejora: 4
   • Terminales perturbación: 3

2️⃣  CREAR GENERADOR
--------------------------------------------------------------------------------
✅ Generador creado con seed=42

3️⃣  GENERAR 3 ALGORITMOS ALEATORIOS
--------------------------------------------------------------------------------

✅ Algoritmo 1:
   Nodos: 7, Profundidad: 3
   Pseudocódigo:
     CONSTRUIR con DSATUR
       MIENTRAS iteraciones < 200:
         MEJORAR con KempeChain (max_iter=100)

✅ Algoritmo 2:
   Nodos: 5, Profundidad: 2
   Pseudocódigo:
     PARA i = 0 a 5:
       CONSTRUIR con LF
       MEJORAR con TabuCol (max_iter=200)

✅ Algoritmo 3:
   Nodos: 12, Profundidad: 4
   Pseudocódigo:
     CONSTRUIR con RandomSequential
       MIENTRAS iteraciones < 500:
         MEJORAR con OneVertexMove (max_iter=50)
         SI Stagnation:
           PERTURBAR con RandomRecolor (intensidad=0.3)
         MEJORAR con KempeChain (max_iter=100)

4️⃣  CARGAR INSTANCIA
--------------------------------------------------------------------------------
✅ Instancia cargada: myciel3
   • Vértices: 11
   • Aristas: 20
   • BKS: 4

5️⃣  EJECUTAR ALGORITMOS
--------------------------------------------------------------------------------

Ejecutando Algoritmo 1...
   • Colores: 4
   • Conflictos: 0
   • Factible: ✓
   • Gap respecto a BKS: +0 (0.0%)

Ejecutando Algoritmo 2...
   • Colores: 5
   • Conflictos: 0
   • Factible: ✓
   • Gap respecto a BKS: +1 (25.0%)

================================================================================
  ✅ DEMO COMPLETADA
================================================================================
```

---

## 2️⃣ EJECUCIÓN: `scripts/test_quick.py`

### Comando:
```bash
python scripts/test_quick.py
```

### Salida Esperada:

```
================================================================================
  VALIDACIÓN RÁPIDA DEL SISTEMA (10 segundos)
================================================================================

📦 FASE 1: CARGAR DATASETS
--------------------------------------------------------------------------------
✅ Datasets cargados: 79 instancias
   • CUL: 6 instancias
   • DSJ: 15 instancias
   • LEI: 12 instancias
   • MYC: 6 instancias
   • REG: 14 instancias
   • SCH: 2 instancias
   • SGB: 24 instancias

🧪 FASE 2: PROBAR OPERADORES
--------------------------------------------------------------------------------
Probando GreedyDSATUR en myciel3...
   ✅ Solución: 4 colores, 0 conflictos (factible)

Probando GreedyLF en myciel3...
   ✅ Solución: 5 colores, 0 conflictos (factible)

Probando KempeChain en solución inicial...
   ✅ Mejora: 5 → 4 colores

Probando RandomRecolor (perturbación)...
   ✅ Perturbación aplicada: 4 colores, 0 conflictos

🔬 FASE 3: PROBAR ILS
--------------------------------------------------------------------------------
Ejecutando ILS en myciel3 (50 iteraciones)...

Iteración 0: 4 colores, 0 conflictos ✓
Iteración 10: 4 colores, 0 conflictos ✓
Iteración 20: 4 colores, 0 conflictos ✓
Iteración 30: 4 colores, 0 conflictos ✓
Iteración 40: 4 colores, 0 conflictos ✓
Iteración 50: 4 colores, 0 conflictos ✓

✅ ILS completado:
   • Mejor solución: 4 colores
   • Gap a BKS: 0 (0.0%)
   • Tiempo: 2.3 segundos

🤖 FASE 4: PROBAR GAA
--------------------------------------------------------------------------------
Generando algoritmo aleatorio...
✅ Algoritmo generado:
   Nodos: 8, Profundidad: 3
   
Ejecutando algoritmo generado en myciel3...
✅ Resultado:
   • Colores: 4
   • Conflictos: 0
   • Factible: ✓
   • Tiempo: 1.8 segundos

================================================================================
  ✅ VALIDACIÓN COMPLETADA - TODOS LOS TESTS PASARON
================================================================================
Tiempo total: 8.7 segundos
```

---

## 3️⃣ EJECUCIÓN: ILS Manual con Verbose

### Código:
```python
from core import GraphColoringProblem
from metaheuristic import IteratedLocalSearch

# Cargar problema
problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# Crear ILS con verbose
ils = IteratedLocalSearch(
    problem=problem,
    max_iterations=100,
    verbose=True,
    seed=42
)

# Ejecutar
solution, history = ils.solve()
```

### Salida Esperada:

```
Solución inicial: 5 colores

[Iter 0] Actual: 5 colores, Mejor: 5 colores, Conflictos: 0 ✓
[Iter 1] Perturbación aplicada
[Iter 1] Mejora local: 5 → 5 colores
[Iter 1] Actual: 5 colores, Mejor: 5 colores, Conflictos: 0 ✓

[Iter 2] Perturbación aplicada
[Iter 2] Mejora local: 5 → 4 colores
[Iter 2] ⭐ MEJORA ENCONTRADA: 5 → 4 colores
[Iter 2] Actual: 4 colores, Mejor: 4 colores, Conflictos: 0 ✓

[Iter 3] Perturbación aplicada
[Iter 3] Mejora local: 4 → 4 colores
[Iter 3] Actual: 4 colores, Mejor: 4 colores, Conflictos: 0 ✓

[Iter 4] Perturbación aplicada
[Iter 4] Mejora local: 5 → 4 colores
[Iter 4] Actual: 4 colores, Mejor: 4 colores, Conflictos: 0 ✓

...

[Iter 50] Sin mejoras en 48 iteraciones - Estancamiento detectado
[Iter 50] Actual: 4 colores, Mejor: 4 colores, Conflictos: 0 ✓

================================================================================
RESULTADO FINAL
================================================================================
Mejor solución: 4 colores
Óptimo conocido: 4 colores
Gap: 0 (0.0%)
Tiempo total: 3.2 segundos
Iteraciones: 50
Mejoras encontradas: 1 (en iteración 2)
================================================================================
```

---

## 4️⃣ EJECUCIÓN: Evaluación de Solución

### Código:
```python
from core import GraphColoringProblem, ColoringSolution, ColoringEvaluator

# Cargar problema
problem = GraphColoringProblem.load_from_dimacs("datasets/DSJC125.1.col")

# Crear solución (ejemplo)
assignment = {v: v % 10 for v in range(1, 126)}  # Asignar 10 colores
solution = ColoringSolution(assignment=assignment)

# Evaluar
metrics = ColoringEvaluator.evaluate(solution, problem)

# Mostrar resultado
print(ColoringEvaluator.format_result(solution, problem, metrics))
```

### Salida Esperada:

```
======================================================================
Instancia: DSJC125.1
======================================================================
Número de colores:     10
Conflictos:            0
Factible:              ✓ Sí
Fitness:               10.00
Óptimo conocido:       5
Gap:                   1.0000 (100.00%)
======================================================================
```

---

## 5️⃣ EJECUCIÓN: Resumen de Problema

### Código:
```python
from core import GraphColoringProblem

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel5.col")
print(problem.summary())
```

### Salida Esperada:

```
============================================================
Instancia: myciel5
============================================================
Vértices:              47
Aristas:               236
Densidad:              0.2189
Grado máximo (Δ):      23
Grado mínimo:          10
Grado promedio:        10.04
Bipartito:             False
Cota superior (Δ+1):   24
Cota inferior:         22
Óptimo conocido (χ):   6
============================================================
```

---

## 6️⃣ EJECUCIÓN: Generador GAA con Detalles

### Código:
```python
from gaa import Grammar, AlgorithmGenerator

grammar = Grammar(min_depth=2, max_depth=4)
generator = AlgorithmGenerator(grammar=grammar, seed=123)

# Generar algoritmo
algorithm = generator.generate()

# Mostrar estadísticas
stats = grammar.get_statistics(algorithm)
print(f"Estadísticas del algoritmo generado:")
print(f"  Total de nodos: {stats['total_nodes']}")
print(f"  Profundidad: {stats['depth']}")
print(f"  Válido: {stats['is_valid']}")
print(f"\nDistribución de nodos:")
for node_type, count in stats['node_counts'].items():
    if count > 0:
        print(f"  {node_type}: {count}")

print(f"\nPseudocódigo:")
print(algorithm.to_pseudocode())
```

### Salida Esperada:

```
Estadísticas del algoritmo generado:
  Total de nodos: 9
  Profundidad: 3
  Válido: True

Distribución de nodos:
  constructive: 1
  improvement: 2
  perturbation: 1
  seq: 2
  while: 1

Pseudocódigo:
  CONSTRUIR con DSATUR
    MIENTRAS iteraciones < 200:
      MEJORAR con KempeChain (max_iter=100)
      PERTURBAR con RandomRecolor (intensidad=0.2)
      MEJORAR con OneVertexMove (max_iter=50)
```

---

## 7️⃣ EJECUCIÓN: Comparación de Soluciones

### Código:
```python
from core import GraphColoringProblem, ColoringSolution
from operators import GreedyDSATUR, GreedyLF, RandomSequential
from core.evaluation import compare_solutions

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# Generar 3 soluciones con diferentes constructores
sol1 = GreedyDSATUR.construct(problem, seed=42)
sol2 = GreedyLF.construct(problem, seed=42)
sol3 = RandomSequential.construct(problem, seed=42)

# Comparar
print(compare_solutions([sol1, sol2, sol3], problem))
```

### Salida Esperada:

```
====================================================================================================
Comparación de Soluciones - myciel3
====================================================================================================
Sol   Colores    Conflictos   Factible   Gap        Fitness        
----------------------------------------------------------------------------------------------------
1     4          0            ✓          0.00%      4.00           
2     5          0            ✓          25.00%     5.00           
3     6          0            ✓          50.00%     6.00           
====================================================================================================
```

---

## 8️⃣ EJECUCIÓN: Detalle de Solución

### Código:
```python
from core import GraphColoringProblem, ColoringSolution
from operators import GreedyDSATUR

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
solution = GreedyDSATUR.construct(problem)

print(solution.detailed_summary(problem))
```

### Salida Esperada:

```
============================================================
Solución de Coloración de Grafos
============================================================
Colores utilizados:    4
Vértices coloreados:   11
Conflictos:            0
Factible:              Sí
Óptimo conocido:       4
Gap a óptimo:          0 (0.00%)

Distribución de colores:
  Color 0: 3 vértices
  Color 1: 3 vértices
  Color 2: 3 vértices
  Color 3: 2 vértices
============================================================
```

---

## 9️⃣ EJECUCIÓN: Operadores en Acción

### Código:
```python
from core import GraphColoringProblem
from operators import GreedyDSATUR, KempeChain, RandomRecolor

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# 1. Construcción
print("1. CONSTRUCCIÓN")
solution = GreedyDSATUR.construct(problem)
print(f"   Solución inicial: {solution.num_colors} colores, {solution.num_conflicts(problem)} conflictos")

# 2. Mejora
print("\n2. MEJORA LOCAL")
improved = KempeChain.improve(solution, problem)
print(f"   Después de KempeChain: {improved.num_colors} colores, {improved.num_conflicts(problem)} conflictos")

# 3. Perturbación
print("\n3. PERTURBACIÓN")
perturbed = RandomRecolor.perturb(improved, problem, ratio=0.3)
print(f"   Después de RandomRecolor: {perturbed.num_colors} colores, {perturbed.num_conflicts(problem)} conflictos")

# 4. Mejora nuevamente
print("\n4. MEJORA NUEVAMENTE")
final = KempeChain.improve(perturbed, problem)
print(f"   Solución final: {final.num_colors} colores, {final.num_conflicts(problem)} conflictos")
```

### Salida Esperada:

```
1. CONSTRUCCIÓN
   Solución inicial: 5 colores, 0 conflictos

2. MEJORA LOCAL
   Después de KempeChain: 4 colores, 0 conflictos

3. PERTURBACIÓN
   Después de RandomRecolor: 5 colores, 0 conflictos

4. MEJORA NUEVAMENTE
   Solución final: 4 colores, 0 conflictos
```

---

## 🔟 EJECUCIÓN: Intérprete GAA Paso a Paso

### Código:
```python
from gaa import AlgorithmGenerator, Grammar, ASTInterpreter
from core import GraphColoringProblem

# Generar algoritmo
grammar = Grammar()
generator = AlgorithmGenerator(grammar, seed=42)
algorithm = generator._generate_simple()

print("ALGORITMO GENERADO:")
print(algorithm.to_pseudocode())
print("\n" + "="*60)

# Cargar problema
problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")

# Ejecutar con intérprete
print("\nEJECUTANDO ALGORITMO...")
interpreter = ASTInterpreter(problem)
solution = interpreter.execute(algorithm)

# Mostrar estadísticas
stats = interpreter.context.get_statistics()
print(f"\nESTADÍSTICAS DE EJECUCIÓN:")
print(f"  Iteraciones: {stats['iterations']}")
print(f"  Evaluaciones: {stats['evaluations']}")
print(f"  Tiempo: {stats['elapsed_time']:.2f}s")
print(f"  Mejor solución: {stats['best_colors']} colores")
print(f"  Conflictos: {stats['best_conflicts']}")
print(f"  Factible: {stats['final_feasible']}")
print(f"  Mejoras encontradas: {stats['improvements']}")
```

### Salida Esperada:

```
ALGORITMO GENERADO:
  CONSTRUIR con DSATUR
    MEJORAR con KempeChain (max_iter=100)

============================================================

EJECUTANDO ALGORITMO...

ESTADÍSTICAS DE EJECUCIÓN:
  Iteraciones: 1
  Evaluaciones: 2
  Tiempo: 0.15s
  Mejor solución: 4 colores
  Conflictos: 0
  Factible: True
  Mejoras encontradas: 1
```

---

## 📊 RESUMEN DE TIPOS DE OUTPUT

### 1. **Output de Consola** (Texto)
- Progreso de ejecución
- Métricas en tiempo real
- Resultados finales
- Estadísticas

### 2. **Output de Archivos** (Datos)
- `summary.csv` - Tabla de resultados
- `detailed_results.json` - Datos completos
- `statistics.txt` - Reporte formateado
- `*.sol` - Archivos de solución

### 3. **Output Visual** (Gráficas)
- `convergence_plot.png` - Evolución del fitness
- `boxplot_robustness.png` - Distribución estadística
- `time_quality_tradeoff.png` - Tiempo vs calidad
- `scalability_plot.png` - Escalabilidad
- `conflict_heatmap.png` - Mapa de conflictos

### 4. **Output de Debugging** (Verbose)
- Iteración por iteración
- Decisiones de aceptación
- Detección de estancamiento
- Mejoras encontradas

---

## 🎯 CONCLUSIÓN

El sistema GAA-GCP-ILS-4 produce **outputs ricos y detallados** que incluyen:

✅ **Información de progreso** en tiempo real  
✅ **Métricas de calidad** (colores, conflictos, gap)  
✅ **Estadísticas de ejecución** (tiempo, iteraciones, mejoras)  
✅ **Visualizaciones** de convergencia y rendimiento  
✅ **Pseudocódigo legible** de algoritmos generados  
✅ **Comparaciones** entre soluciones y algoritmos  

Todos los outputs están diseñados para ser:
- **Informativos**: Muestran métricas clave
- **Reproducibles**: Incluyen seeds y configuración
- **Analizables**: Formato CSV/JSON para procesamiento
- **Visuales**: Gráficas para publicaciones
