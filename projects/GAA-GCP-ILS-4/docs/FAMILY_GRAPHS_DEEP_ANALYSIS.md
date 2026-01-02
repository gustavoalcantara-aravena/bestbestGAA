# Análisis Profundo: Gráficos de Familia (2_family/)

## 📋 Resumen Ejecutivo

Los gráficos de familia agregan datos de múltiples instancias DIMACS pertenecientes a la misma familia (ej: MYC, DSJ, LEI) para mostrar patrones y comportamientos a nivel de familia. Cada gráfico presenta una dimensión diferente del análisis.

---

## 🔬 Gráfico 01: Computational Scalability (Execution Time) across {family} Instances

### Objetivo
Mostrar cómo escala el **tiempo de ejecución** del algoritmo ILS con el **tamaño del problema** (número de vértices).

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~200-250

for idx, dataset_path in enumerate(test_datasets, 1):
    problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
    
    # Recolectar datos
    vertices_list.append(problem.n_vertices)  # Número de vértices
    times_list.append(ils_time)               # Tiempo de ejecución ILS
    instance_names.append(problem.name)       # Nombre de instancia
```

### Estructura de Datos

```python
# En plotter_v2.py, método plot_family_scalability_time()

def plot_family_scalability_time(self,
                                family_name: str,
                                instances: List[str],      # ["myciel3", "myciel4", ...]
                                vertices: List[int],       # [11, 23, 47, 95, 191]
                                times: List[float]):       # [0.45, 1.23, 5.67, 23.45, 89.12]
```

### Matemática de Presentación

```
Eje X: Número de vértices (escala logarítmica)
Eje Y: Tiempo de ejecución en segundos (escala logarítmica)

Relación esperada: T(n) ∝ n^k  (ley de potencia)

En escala log-log:
  log(T) = k·log(n) + c
  
Esto aparece como una línea recta en el gráfico log-log
```

### Código de Generación

```python
# visualization/plotter_v2.py, líneas 286-321

fig, ax = plt.subplots(figsize=(12, 7))

# Plotear puntos conectados
ax.plot(vertices, times, 'o-', linewidth=2.5, markersize=8, color='#1f77b4')

# Anotar cada punto con el nombre de la instancia
for i, (v, t, inst) in enumerate(zip(vertices, times, instances)):
    ax.annotate(inst, (v, t), textcoords="offset points", 
               xytext=(0,10), ha='center', fontsize=9)

# Configurar escalas logarítmicas
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('Number of Vertices', fontsize=12)
ax.set_ylabel('Execution Time (s)', fontsize=12)
ax.set_title(f'Computational Scalability (Execution Time) across {family_name} Instances', 
            fontsize=14, fontweight='bold')
```

### Interpretación

```
Pendiente positiva (línea sube):
  → El tiempo crece con el tamaño
  → Algoritmo es computacionalmente costoso
  → Pendiente = exponente k

Pendiente suave (k ≈ 1-2):
  → Escalabilidad razonable
  → Algoritmo es eficiente

Pendiente pronunciada (k > 3):
  → Escalabilidad pobre
  → Algoritmo es muy costoso
```

### Ejemplo Concreto: Familia MYC

```
Instancia  Vértices  Tiempo (s)
myciel3    11        0.45
myciel4    23        1.23
myciel5    47        5.67
myciel6    95        23.45
myciel7    191       89.12

En log-log:
  log(11) ≈ 1.04    log(0.45) ≈ -0.35
  log(23) ≈ 1.36    log(1.23) ≈ 0.09
  log(47) ≈ 1.67    log(5.67) ≈ 0.75
  log(95) ≈ 1.98    log(23.45) ≈ 1.37
  log(191) ≈ 2.28   log(89.12) ≈ 1.95

Pendiente ≈ (1.95 - (-0.35)) / (2.28 - 1.04) ≈ 1.65
```

---

## 🔬 Gráfico 02: Solution Quality Scalability (Optimality Gap) across {family} Instances

### Objetivo
Mostrar cómo varía la **calidad de la solución** (gap respecto a BKS) con el **tamaño del problema**.

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~200-250

for idx, dataset_path in enumerate(test_datasets, 1):
    problem = GraphColoringProblem.load_from_dimacs(str(dataset_file))
    best_solution, history = ils.solve()
    
    # Recolectar datos
    vertices_list.append(problem.n_vertices)
    
    # Calcular gap
    n_colors_obtained = best_solution.num_colors
    bks = problem.colors_known  # Best Known Solution
    gap = ((n_colors_obtained - bks) / bks) * 100  # Gap en porcentaje
    gaps_list.append(gap)
```

### Estructura de Datos

```python
# En plotter_v2.py, método plot_family_scalability_quality()

def plot_family_scalability_quality(self,
                                   family_name: str,
                                   instances: List[str],      # ["myciel3", "myciel4", ...]
                                   vertices: List[int],       # [11, 23, 47, 95, 191]
                                   gaps: List[float]):        # [0.0, 0.0, 0.0, 0.0, 0.0]
```

### Matemática del Gap

```
Gap (%) = ((f_obtained - f_optimal) / f_optimal) × 100

Donde:
  f_obtained = número de colores obtenidos por ILS
  f_optimal = BKS (Best Known Solution)

Interpretación:
  Gap = 0%   → Solución óptima encontrada ✅
  Gap > 0%   → Solución subóptima
  Gap < 0%   → Mejor que BKS conocido (raro)
```

### Código de Generación

```python
# visualization/plotter_v2.py, líneas 323-360

fig, ax = plt.subplots(figsize=(12, 7))

# Colorear puntos según gap
colors = ['green' if g == 0 else 'orange' if g > 0 else 'red' for g in gaps]
ax.scatter(vertices, gaps, s=200, c=colors, edgecolor='black', 
          linewidth=1.5, alpha=0.7, zorder=3)

# Conectar puntos
ax.plot(vertices, gaps, 'b-', alpha=0.3, linewidth=1)

# Línea de referencia (gap = 0)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1, zorder=1)

# Anotar instancias
for i, (v, g, inst) in enumerate(zip(vertices, gaps, instances)):
    ax.annotate(inst, (v, g), textcoords="offset points",
               xytext=(0,10), ha='center', fontsize=9)

# Escala logarítmica en X (tamaño)
ax.set_xscale('log')

ax.set_xlabel('Number of Vertices', fontsize=12)
ax.set_ylabel('Optimality Gap (%)', fontsize=12)
ax.set_title(f'Solution Quality Scalability (Optimality Gap): {family_name} Family',
            fontsize=14, fontweight='bold')
```

### Interpretación

```
Puntos verdes (gap = 0):
  → Solución óptima encontrada
  → Excelente rendimiento del algoritmo

Puntos naranjas (gap > 0):
  → Solución subóptima
  → Algoritmo no encontró el óptimo

Tendencia con tamaño:
  - Gap constante → Algoritmo mantiene calidad
  - Gap creciente → Algoritmo pierde calidad en instancias grandes
  - Gap decreciente → Algoritmo mejora en instancias grandes
```

### Ejemplo Concreto: Familia MYC

```
Instancia  Vértices  BKS  Obtenido  Gap (%)
myciel3    11        4    4         0.0%    ✅
myciel4    23        5    5         0.0%    ✅
myciel5    47        6    6         0.0%    ✅
myciel6    95        7    7         0.0%    ✅
myciel7    191       8    8         0.0%    ✅

Conclusión: ILS encuentra óptimo en todas las instancias
```

---

## 🔬 Gráfico 03: Robustness (Color Count Distribution) across {family} Instances

### Objetivo
Mostrar la **variabilidad** de las soluciones entre los 3 algoritmos GAA generados para cada instancia.

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~250-300

# Para cada instancia, ejecutar 3 algoritmos GAA
for algo_idx in range(3):
    best_solution, history = ils.solve()
    n_colors = best_solution.num_colors
    algorithm_results[f"GAA_Algorithm_{algo_idx+1}"].append(n_colors)

# Resultado: 3 listas de valores (una por algoritmo)
# Cada lista contiene el número de colores para cada instancia
```

### Estructura de Datos

```python
# En plotter_v2.py, método plot_family_robustness_boxplot()

def plot_family_robustness_boxplot(self,
                                  family_name: str,
                                  instances: List[str],                    # ["myciel3", "myciel4", ...]
                                  algorithm_results: Dict[str, List[int]]):  # {"GAA_Algorithm_1": [4,5,6,7,8], ...}
```

### Matemática de Box Plot

```
Para cada algoritmo y instancia:

Box plot muestra:
  - Mínimo (whisker inferior)
  - Q1 (cuartil 25%)
  - Mediana (línea en la caja)
  - Q3 (cuartil 75%)
  - Máximo (whisker superior)
  - Outliers (puntos fuera de 1.5×IQR)

IQR = Q3 - Q1  (Rango Intercuartil)
```

### Código de Generación

```python
# visualization/plotter_v2.py, líneas 362-396

fig, ax = plt.subplots(figsize=(12, 7))

# Preparar datos para box plot
data = []
labels = []
for instance in instances:
    for algo_name in sorted(algorithm_results.keys()):
        values = algorithm_results[algo_name]
        # Obtener valor para esta instancia
        data.append([values[instances.index(instance)]])
        labels.append(f"{instance}\n{algo_name}")

# Crear box plot
bp = ax.boxplot(data, labels=labels, patch_artist=True,
               notch=True, showmeans=True)

# Colorear cajas
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('Number of Colors', fontsize=12)
ax.set_title(f'Robustness (Color Count Distribution): {family_name} Family',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
```

### Interpretación

```
Caja pequeña (IQR pequeño):
  → Algoritmos producen soluciones similares
  → Robustez alta (consistencia)

Caja grande (IQR grande):
  → Algoritmos producen soluciones muy diferentes
  → Robustez baja (variabilidad)

Mediana en el centro de la caja:
  → Distribución simétrica
  → Comportamiento equilibrado

Mediana cerca de Q1 o Q3:
  → Distribución asimétrica
  → Comportamiento sesgado
```

### Ejemplo Concreto: Familia MYC

```
Si todos los algoritmos encuentran el óptimo:
  myciel3: [4, 4, 4]  → Caja degenerada (un punto)
  myciel4: [5, 5, 5]  → Caja degenerada (un punto)
  ...
  
Conclusión: Robustez perfecta (todos encuentran óptimo)
```

---

## 🔬 Gráfico 04: Average Ranking (Lower is Better) across {family} Instances

### Objetivo
Mostrar el **ranking promedio** de cada algoritmo GAA basado en su desempeño en todas las instancias.

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~250-300

# Para cada instancia, rankear los 3 algoritmos
for instance in instances:
    colors_per_algo = [algo_results[algo][instance_idx] for algo in algorithms]
    
    # Rankear (1 = mejor, 3 = peor)
    rankings = rank(colors_per_algo)  # [1, 2, 3] o similar
    
    # Acumular rankings
    for algo_idx, rank in enumerate(rankings):
        total_rankings[algo_idx].append(rank)

# Calcular ranking promedio
average_rankings = [sum(ranks) / len(ranks) for ranks in total_rankings]
```

### Estructura de Datos

```python
# En plotter_v2.py, método plot_family_algorithm_ranking()

def plot_family_algorithm_ranking(self,
                                 family_name: str,
                                 instances: List[str],
                                 algorithm_results: Dict[str, List[int]]):
    
    # Calcular rankings promedio
    rankings = {}
    for algo_name in algorithm_results.keys():
        # Rankear para cada instancia y promediar
        rankings[algo_name] = average_rank
```

### Matemática de Ranking

```
Para cada instancia:
  Algoritmo con menor número de colores → Rank 1
  Algoritmo con segundo menor → Rank 2
  Algoritmo con mayor → Rank 3

Ranking promedio = Σ(ranks) / n_instancias

Interpretación:
  Ranking = 1.0  → Mejor algoritmo (siempre gana)
  Ranking = 2.0  → Algoritmo medio
  Ranking = 3.0  → Peor algoritmo (siempre pierde)
```

### Código de Generación

```python
# visualization/plotter_v2.py, líneas 398-434

fig, ax = plt.subplots(figsize=(12, 7))

# Preparar datos
algorithms = sorted(algorithm_results.keys())
rankings = []

for algo_name in algorithms:
    # Calcular ranking promedio para este algoritmo
    algo_rankings = []
    for inst_idx in range(len(instances)):
        # Obtener valores de todos los algoritmos para esta instancia
        values = [algorithm_results[a][inst_idx] for a in algorithms]
        # Rankear
        rank = sorted(values).index(values[algorithms.index(algo_name)]) + 1
        algo_rankings.append(rank)
    
    # Promedio
    avg_rank = sum(algo_rankings) / len(algo_rankings)
    rankings.append(avg_rank)

# Gráfico de barras horizontal
bars = ax.barh(algorithms, rankings, color=['#1f77b4', '#ff7f0e', '#2ca02c'],
              edgecolor='black', linewidth=1.5)

# Agregar valores en las barras
for bar, value in zip(bars, rankings):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
           f'{value:.2f}',
           ha='left', va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Average Ranking (lower = better)', fontsize=12)
ax.set_title(f'Average Ranking (Lower is Better): {family_name} Family',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
```

### Interpretación

```
Barra más corta (ranking más bajo):
  → Mejor algoritmo en promedio
  → Ganador del torneo

Barra más larga (ranking más alto):
  → Peor algoritmo en promedio
  → Perdedor del torneo

Diferencias pequeñas:
  → Algoritmos similares
  → Competencia cerrada

Diferencias grandes:
  → Algoritmos muy diferentes
  → Ganador claro
```

### Ejemplo Concreto: Familia MYC

```
Si todos los algoritmos encuentran óptimo:
  GAA_Algorithm_1: 1.0
  GAA_Algorithm_2: 1.0
  GAA_Algorithm_3: 1.0
  
Conclusión: Empate perfecto (todos igualmente buenos)
```

---

## 🔬 Gráfico 06: Optimality Gap across {family} Instances

### Objetivo
Mostrar el **gap de optimalidad** de cada algoritmo GAA para cada instancia en la familia.

### Datos Base

```python
# Fuente: test_experiment_quick.py, líneas ~250-300

for algo_idx in range(3):
    for inst_idx, instance in enumerate(instances):
        best_solution, history = ils.solve()
        
        # Calcular gap
        n_colors = best_solution.num_colors
        bks = problem.colors_known
        gap = ((n_colors - bks) / bks) * 100
        
        algorithm_gaps[f"GAA_Algorithm_{algo_idx+1}"].append(gap)
```

### Estructura de Datos

```python
# En plotter_v2.py, método plot_family_gap_analysis()

def plot_family_gap_analysis(self,
                            family_name: str,
                            instances: List[str],              # ["myciel3", "myciel4", ...]
                            algorithm_gaps: Dict[str, List]):  # {"GAA_Algorithm_1": [0.0, 0.0, ...], ...}
```

### Matemática del Gap

```
Para cada algoritmo y instancia:

Gap (%) = ((f_obtained - f_optimal) / f_optimal) × 100

Visualización:
  - Eje X: Instancias
  - Eje Y: Gap (%)
  - Barras agrupadas: Una barra por algoritmo
  - Línea horizontal en y=0: Referencia de optimalidad
```

### Código de Generación

```python
# visualization/plotter_v2.py, líneas 436-472

fig, ax = plt.subplots(figsize=(14, 7))

x = np.arange(len(instances))
width = 0.25

# Plotear barras para cada algoritmo
for i, (algo, gaps) in enumerate(sorted(algorithm_gaps.items())):
    offset = (i - 1) * width
    ax.bar(x + offset, gaps, width, label=algo, alpha=0.8)

# Línea de referencia (gap = 0)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

ax.set_xlabel('Instance', fontsize=12)
ax.set_ylabel('Optimality Gap (%)', fontsize=12)
ax.set_title(f'Optimality Gap across {family_name} Instances',
            fontsize=14, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(instances, rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
```

### Interpretación

```
Barras en y=0:
  → Solución óptima encontrada
  → Excelente rendimiento

Barras positivas (arriba de y=0):
  → Solución subóptima
  → Algoritmo no encontró óptimo

Barras negativas (abajo de y=0):
  → Mejor que BKS conocido
  → Descubrimiento nuevo (raro)

Comparación entre algoritmos:
  - Mismo color, diferentes alturas → Variabilidad entre algoritmos
  - Todas en y=0 → Todos encuentran óptimo
  - Patrón consistente → Comportamiento predecible
```

### Ejemplo Concreto: Familia MYC

```
Instancia  GAA_Algo_1  GAA_Algo_2  GAA_Algo_3
myciel3    0.0%        0.0%        0.0%
myciel4    0.0%        0.0%        0.0%
myciel5    0.0%        0.0%        0.0%
myciel6    0.0%        0.0%        0.0%
myciel7    0.0%        0.0%        0.0%

Conclusión: Todos los algoritmos encuentran óptimo en todas las instancias
```

---

## 📊 Flujo de Datos Completo

```
test_experiment_quick.py
    ↓
    ├─ Cargar instancias DIMACS
    ├─ Ejecutar ILS (3 algoritmos GAA)
    ├─ Recolectar:
    │   ├─ Número de vértices
    │   ├─ Tiempo de ejecución
    │   ├─ Número de colores obtenidos
    │   ├─ BKS (Best Known Solution)
    │   └─ Calcular gaps
    │
    └─ Pasar datos a PlotManagerV2
        ↓
        ├─ plot_family_scalability_time()
        │   └─ Gráfico 01: Tiempo vs Tamaño
        │
        ├─ plot_family_scalability_quality()
        │   └─ Gráfico 02: Gap vs Tamaño
        │
        ├─ plot_family_robustness_boxplot()
        │   └─ Gráfico 03: Distribución de colores
        │
        ├─ plot_family_algorithm_ranking()
        │   └─ Gráfico 04: Ranking promedio
        │
        └─ plot_family_gap_analysis()
            └─ Gráfico 06: Gap por instancia
```

---

## 🎯 Resumen de Dimensiones Analizadas

| Gráfico | Dimensión X | Dimensión Y | Propósito |
|---------|-------------|-------------|----------|
| **01** | Tamaño (vértices) | Tiempo (s) | Escalabilidad computacional |
| **02** | Tamaño (vértices) | Gap (%) | Escalabilidad de calidad |
| **03** | Instancia | Colores | Robustez entre algoritmos |
| **04** | Algoritmo | Ranking promedio | Comparación de desempeño |
| **06** | Instancia | Gap (%) | Análisis detallado de gaps |

---

## 💡 Conclusión

Los gráficos de familia proporcionan una vista agregada del comportamiento del algoritmo a nivel de familia de instancias, permitiendo:

1. ✅ Identificar patrones de escalabilidad
2. ✅ Comparar calidad de soluciones
3. ✅ Evaluar robustez entre algoritmos
4. ✅ Rankear algoritmos por desempeño
5. ✅ Analizar gaps de optimalidad

Todos los gráficos se basan en datos reales extraídos durante la ejecución del algoritmo ILS con diferentes semillas y configuraciones GAA.

---

**Documento generado:** 2026-01-02
**Versión:** 1.0
**Estado:** ✅ COMPLETADO
