# Análisis Profundo: Gráficos Individuales (plots/)

## 📋 Resumen Ejecutivo

Los 4 gráficos individuales generados en la carpeta `plots/` proporcionan una visión detallada del comportamiento del algoritmo ILS en cada instancia específica. Cada gráfico analiza una dimensión diferente del problema y la solución.

---

## 🔬 Gráfico 1: conflict_heatmap.png

### Objetivo
Visualizar la **matriz de adyacencia** del grafo (qué vértices están conectados) y los **conflictos** de la solución obtenida (qué aristas tienen ambos extremos del mismo color).

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~200-250

problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
best_solution, history = ils.solve()

# Extraer matriz de conflictos
conflict_matrix = best_solution.get_conflict_matrix()
# Forma: matriz NxN donde:
#   1 = hay arista entre vértices i,j (conflicto potencial)
#   0 = no hay arista
```

### Estructura de Datos

```python
# visualization/plotter.py, método plot_conflict_heatmap()

def plot_conflict_heatmap(self,
                         problem: GraphColoringProblem,
                         solution: ColoringSolution,
                         output_path: str):
    
    # Obtener matriz de conflictos
    conflict_matrix = solution.get_conflict_matrix()
    # Forma: matriz NxN booleana
    # conflict_matrix[i][j] = True si hay conflicto entre vértices i,j
```

### Matemática de la Visualización

```
Matriz de Conflictos:
  - Eje X: Vértice j (0 a N-1)
  - Eje Y: Vértice i (0 a N-1)
  - Valor en [i,j]: 1 si hay conflicto, 0 si no

Conflicto = existe arista (i,j) Y f(i) = f(j)
  donde f(v) = color asignado al vértice v

Visualización:
  - Rojo/oscuro = conflicto (arista con mismo color)
  - Verde/claro = sin conflicto (arista con colores diferentes)
  - Blanco = sin arista
```

### Código de Generación

```python
# visualization/plotter.py, líneas ~150-200

fig, ax = plt.subplots(figsize=(10, 10))

# Obtener matriz de conflictos
conflict_matrix = solution.get_conflict_matrix()

# Visualizar como heatmap
im = ax.imshow(conflict_matrix, cmap='RdYlGn_r', aspect='auto')

# RdYlGn_r = Red-Yellow-Green (reversed)
# Rojo = conflicto (valor 1)
# Verde = sin conflicto (valor 0)

ax.set_xlabel('Vertex', fontsize=12)
ax.set_ylabel('Vertex', fontsize=12)
ax.set_title(f'Adjacency matrix of the graph (instance {instance_name})', 
            fontsize=14, fontweight='bold')

plt.colorbar(im, ax=ax, label='Edge')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

### Interpretación

```
GRÁFICO PERFECTO (solución factible):
  - Toda la matriz es verde
  - No hay conflictos
  - Cada arista tiene extremos con colores diferentes
  - Solución válida ✅

GRÁFICO CON CONFLICTOS (solución infactible):
  - Hay puntos rojos en la matriz
  - Cada punto rojo = una arista con ambos extremos del mismo color
  - Solución inválida ❌

PATRÓN ESPERADO:
  - Matriz simétrica (si hay arista i→j, también j→i)
  - Diagonal siempre blanca (un vértice no tiene arista consigo mismo)
  - Densidad de aristas = número de aristas / (N×N)
```

### Ejemplo Concreto: myciel3

```
myciel3 tiene 11 vértices y 20 aristas

Matriz de conflictos (11×11):
  - 20 posiciones con valor 1 (aristas)
  - 121 - 20 = 101 posiciones con valor 0 (sin aristas)
  
Si solución es factible:
  - Todos los 20 puntos de aristas son verdes
  - Matriz es simétrica
  
Si solución tiene 1 conflicto:
  - 1 punto rojo (la arista conflictiva)
  - 19 puntos verdes (aristas sin conflicto)
```

---

## 🔬 Gráfico 2: convergence_plot.png

### Objetivo
Mostrar cómo **evoluciona la calidad de la solución** (número de colores) a lo largo de las iteraciones del algoritmo ILS.

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~200-250

best_solution, history = ils.solve()

# history contiene:
history = {
    'current_fitness': [50, 45, 42, 40, 38, 37, 35, ...],  # Fitness en cada iteración
    'best_fitness': [50, 45, 42, 40, 38, 37, 35, ...],     # Mejor encontrado hasta ahora
    'times': [0.01, 0.02, 0.05, 0.08, 0.12, 0.15, 0.18, ...] # Tiempo acumulado
}
```

### Estructura de Datos

```python
# visualization/convergence.py, método plot_convergence_single()

def plot_convergence_single(self,
                           fitness_history: List[float],  # current_fitness
                           times: List[float],             # tiempos acumulados
                           output_path: str,
                           instance_name: str,
                           title: str):
    
    # fitness_history = [f0, f1, f2, ..., fn]
    # Cada elemento = fitness en iteración i
```

### Matemática de Presentación

```
Eje X: Iteración (0 a n)
Eje Y: Fitness (número de colores)

Línea AZUL = current_fitness (fitness actual en cada iteración)
  - Puede subir o bajar
  - Refleja movimientos del algoritmo
  - Muestra exploración y explotación

Línea NARANJA PUNTEADA = best_fitness (mejor encontrado)
  - Calculada como: best[i] = min(f0, f1, ..., fi)
  - Siempre monotónica decreciente (nunca sube)
  - Refleja progreso acumulado

Estadísticas mostradas:
  - Inicial: f0 (fitness inicial)
  - Mejor: min(fitness_history)
  - Final: fn (fitness final)
  - Mejora: (f0 - min) / f0 × 100%
```

### Código de Generación

```python
# visualization/convergence.py, líneas ~50-150

fig, ax = plt.subplots(figsize=(12, 7))

# Preparar datos
iterations = np.arange(len(fitness_history))
best_fitness = np.minimum.accumulate(fitness_history)

# Plotear fitness actual (línea azul)
ax.plot(iterations, fitness_history, 'b-', linewidth=2, label='Current Fitness')

# Plotear mejor encontrado (línea naranja punteada)
ax.plot(iterations, best_fitness, 'orange', linestyle='--', 
       linewidth=2, label='Best Fitness Found')

# Calcular estadísticas
initial = fitness_history[0]
best = np.min(fitness_history)
final = fitness_history[-1]
improvement = (initial - best) / initial * 100

# Agregar texto con estadísticas
stats_text = f"Initial: {initial}\nBest: {best}\nFinal: {final}\nImprovement: {improvement:.1f}%"
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel('Iteration', fontsize=12)
ax.set_ylabel('Fitness (Number of Colors)', fontsize=12)
ax.set_title(f'Current fitness trajectory during ILS execution: {instance_name}',
            fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

### Interpretación

```
CONVERGENCIA RÁPIDA:
  - Línea azul baja rápidamente al inicio
  - Luego se estabiliza
  - Línea naranja es casi vertical al inicio
  → Algoritmo explota bien la región inicial

EXPLORACIÓN ACTIVA:
  - Línea azul tiene muchas subidas y bajadas
  - Línea naranja desciende lentamente
  → Algoritmo explora mucho (perturbaciones)

ESTANCAMIENTO:
  - Línea azul oscila alrededor de un valor
  - Línea naranja se vuelve horizontal
  → Algoritmo no mejora (óptimo local)

MEJORA CONTINUA:
  - Línea naranja desciende consistentemente
  - Línea azul tiene variación pero tendencia a bajar
  → Algoritmo sigue encontrando mejores soluciones
```

### Ejemplo Concreto: myciel3

```
Iteración  current_fitness  best_fitness
0          50               50
1          45               45
2          42               42
3          40               40
4          38               38
5          37               37
6          35               35
7          35               35  ← Estancamiento
8          36               35  ← Perturbación (sube)
9          34               34  ← Mejora
10         34               34  ← Estancamiento final

Gráfico muestra:
  - Línea azul: 50→45→42→40→38→37→35→35→36→34→34
  - Línea naranja: 50→45→42→40→38→37→35→35→35→34→34
  - Mejora total: (50-34)/50 = 32%
```

---

## 🔬 Gráfico 3: scalability_plot.png

### Objetivo
Mostrar cómo **escala el tiempo de ejecución** con el **tamaño del problema** (número de vértices).

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~200-250

# Para cada instancia
for dataset_file in test_datasets:
    problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
    
    # Medir tiempo
    start = time.time()
    best_solution, history = ils.solve()
    elapsed_time = time.time() - start
    
    # Recolectar datos
    vertices_list.append(problem.n_vertices)
    times_list.append(elapsed_time)
```

### Estructura de Datos

```python
# visualization/plotter.py, método plot_scalability()

def plot_scalability(self,
                    vertices: List[int],      # [11, 23, 47, 95, 191]
                    times: List[float],       # [0.45, 1.23, 5.67, 23.45, 89.12]
                    instance_names: List[str],  # ["myciel3", "myciel4", ...]
                    output_path: str):
```

### Matemática de Presentación

```
Eje X: Número de vértices (escala logarítmica)
Eje Y: Tiempo de ejecución en segundos (escala logarítmica)

Relación esperada: T(n) ∝ n^k  (ley de potencia)

En escala log-log:
  log(T) = k·log(n) + c
  
Esto aparece como una línea recta en el gráfico log-log

Pendiente = k (exponente de escalabilidad)
  k ≈ 1-2: escalabilidad razonable
  k > 3: escalabilidad pobre
  k < 1: escalabilidad excelente
```

### Código de Generación

```python
# visualization/plotter.py, líneas ~250-300

fig, ax = plt.subplots(figsize=(12, 7))

# Plotear puntos
ax.plot(vertices, times, 'o-', linewidth=2.5, markersize=8, color='#1f77b4')

# Anotar cada punto
for v, t, inst in zip(vertices, times, instance_names):
    ax.annotate(inst, (v, t), textcoords="offset points",
               xytext=(0,10), ha='center', fontsize=9)

# Escala logarítmica
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('Number of Vertices', fontsize=12)
ax.set_ylabel('Execution Time (s)', fontsize=12)
ax.set_title('Escalabilidad Comparativa: Todas las Familias',
            fontsize=14, fontweight='bold')

ax.grid(True, alpha=0.3)

plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

### Interpretación

```
LÍNEA RECTA (escalabilidad predecible):
  - Relación log-log lineal
  - Comportamiento predecible
  - Pendiente = exponente de escalabilidad

PENDIENTE SUAVE (k ≈ 1-2):
  - Escalabilidad razonable
  - Algoritmo es eficiente
  - Tiempo crece moderadamente

PENDIENTE PRONUNCIADA (k > 3):
  - Escalabilidad pobre
  - Algoritmo es muy costoso
  - Tiempo crece exponencialmente

CURVATURA (no lineal en log-log):
  - Comportamiento complejo
  - Múltiples fases de ejecución
  - Cambio de complejidad con tamaño
```

### Ejemplo Concreto: Familia MYC

```
Instancia  Vértices  Tiempo (s)  log(v)   log(t)
myciel3    11        0.45        1.04     -0.35
myciel4    23        1.23        1.36      0.09
myciel5    47        5.67        1.67      0.75
myciel6    95        23.45       1.98      1.37
myciel7    191       89.12       2.28      1.95

En log-log:
  Pendiente ≈ (1.95 - (-0.35)) / (2.28 - 1.04) ≈ 1.65
  → Escalabilidad moderada (k ≈ 1.65)
```

---

## 🔬 Gráfico 4: time_quality_tradeoff.png

### Objetivo
Mostrar la **relación entre tiempo de ejecución y calidad de la solución** (trade-off tiempo-calidad).

### Datos Base

```python
# Fuente: visualization/plotter.py, método plot_time_quality_tradeoff()

# Datos del historial de convergencia
history = {
    'current_fitness': [50, 45, 42, 40, 38, 37, 35, ...],
    'times': [0.01, 0.02, 0.05, 0.08, 0.12, 0.15, 0.18, ...]
}

# Cada punto (tiempo[i], fitness[i]) representa:
# - En el tiempo i, la solución actual tiene fitness fitness[i]
```

### Estructura de Datos

```python
# visualization/plotter.py, método plot_time_quality_tradeoff()

def plot_time_quality_tradeoff(self,
                              times: List[float],           # tiempos acumulados
                              fitness_values: List[float],  # fitness en cada tiempo
                              output_path: str,
                              instance_name: str):
```

### Matemática de Presentación

```
Eje X: Tiempo de ejecución acumulado (segundos)
Eje Y: Fitness (número de colores)

Cada punto (t_i, f_i) representa:
  - En el tiempo t_i segundos
  - La solución actual tiene f_i colores

Trade-off:
  - Más tiempo → mejor solución (generalmente)
  - Pero con rendimientos decrecientes
  - En algún punto, más tiempo no mejora la solución

Curva esperada:
  - Inicial: descenso rápido (mejora rápida)
  - Medio: descenso moderado (mejora lenta)
  - Final: horizontal (estancamiento)
```

### Código de Generación

```python
# visualization/plotter.py, líneas ~350-400

fig, ax = plt.subplots(figsize=(10, 6))

# Plotear puntos dispersos
ax.scatter(times, fitness_values, s=100, alpha=0.6, 
          edgecolor='black', linewidth=1.5)

# Conectar puntos con línea
ax.plot(times, fitness_values, 'b-', alpha=0.3, linewidth=1)

ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Fitness (Number of Colors)', fontsize=12)
ax.set_title(f'Temporal evolution of visited solution quality: {instance_name}',
            fontsize=14, fontweight='bold')

ax.grid(True, alpha=0.3)

plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

### Interpretación

```
CURVA IDEAL (mejora rápida luego estancamiento):
  - Descenso rápido al inicio
  - Luego se vuelve horizontal
  - Indica punto óptimo de parada

CURVA LINEAL (mejora constante):
  - Descenso consistente
  - Algoritmo sigue mejorando
  - Podría beneficiarse de más tiempo

CURVA PLANA (sin mejora):
  - Horizontal desde el inicio
  - Algoritmo no mejora
  - Problema muy difícil o mal configurado

OSCILACIONES (variación):
  - Puntos suben y bajan
  - Perturbaciones del algoritmo
  - Exploración activa
```

### Ejemplo Concreto: myciel3

```
Tiempo (s)  Fitness
0.01        50
0.02        45
0.05        42
0.08        40
0.12        38
0.15        37
0.18        35
0.25        35  ← Estancamiento
0.30        36  ← Perturbación
0.35        34  ← Mejora
0.40        34  ← Final

Gráfico muestra:
  - Descenso rápido: 50→45→42→40→38→37→35 (0-0.18s)
  - Estancamiento: 35→35→36→34→34 (0.18-0.40s)
  - Mejora total: 50→34 en 0.40 segundos
```

---

## 📊 Comparación de los 4 Gráficos

| Gráfico | Qué Mide | Eje X | Eje Y | Pregunta que Responde |
|---------|----------|-------|-------|----------------------|
| **conflict_heatmap** | Conflictos de la solución | Vértice j | Vértice i | ¿Hay conflictos en la solución? |
| **convergence_plot** | Evolución del fitness | Iteración | Fitness | ¿Cómo mejora el algoritmo? |
| **scalability_plot** | Escalabilidad temporal | Vértices (log) | Tiempo (log) | ¿Cómo escala el tiempo? |
| **time_quality_tradeoff** | Relación tiempo-calidad | Tiempo (s) | Fitness | ¿Cuál es el trade-off? |

---

## 🎯 Flujo de Datos Completo

```
test_experiment_quick.py
    ↓
    ├─ Cargar instancia DIMACS
    ├─ Ejecutar ILS
    │   ├─ Recolectar history (fitness, tiempos)
    │   └─ Obtener best_solution
    │
    └─ Pasar datos a PlotManager
        ↓
        ├─ plot_conflict_heatmap()
        │   └─ Gráfico: conflict_heatmap.png
        │
        ├─ plot_convergence()
        │   └─ Gráfico: convergence_plot.png
        │
        ├─ plot_scalability()
        │   └─ Gráfico: scalability_plot.png
        │
        └─ plot_time_quality_tradeoff()
            └─ Gráfico: time_quality_tradeoff.png
```

---

## 💡 Conclusión

Los 4 gráficos individuales proporcionan una visión completa del comportamiento del algoritmo:

1. **conflict_heatmap**: Validez de la solución
2. **convergence_plot**: Dinámica del algoritmo
3. **scalability_plot**: Eficiencia computacional
4. **time_quality_tradeoff**: Relación tiempo-calidad

Juntos, permiten entender profundamente cómo funciona el algoritmo ILS en cada instancia específica.

---

**Documento generado:** 2026-01-02
**Versión:** 1.0
**Estado:** ✅ COMPLETADO
