# Análisis Profundo: Gráfico de Convergencia (convergence_plot.png)

## 📊 Resumen Ejecutivo

El gráfico `convergence_plot.png` visualiza **cómo mejora la solución del algoritmo ILS a lo largo del tiempo**, mostrando:

1. **Fitness actual** (línea azul con puntos): El valor de fitness en cada iteración
2. **Mejor encontrado** (línea naranja punteada): El mejor valor encontrado hasta ese momento

Este gráfico es fundamental para entender el **comportamiento dinámico** del algoritmo durante la ejecución.

---

## 🔬 Definiciones Matemáticas

### Fitness (Función Objetivo)

En el contexto del GCP, el fitness se define como:

```
fitness(solución) = número de colores usados en la solución
```

**Objetivo:** Minimizar el fitness (usar menos colores)

```
Minimizar: f(s) = |{c ∈ colores : ∃v ∈ V, asignación(v) = c}|
```

### Historial de Convergencia

El historial de convergencia es una secuencia de valores de fitness:

```
H = [f₀, f₁, f₂, ..., fₙ]

Donde:
- fᵢ = fitness de la solución en la iteración i
- n = número total de iteraciones
- Cada fᵢ ∈ ℤ⁺ (enteros positivos)
```

### Mejor Valor Encontrado (Monotónico Decreciente)

```
B = [b₀, b₁, b₂, ..., bₙ]

Donde:
- bᵢ = min(f₀, f₁, ..., fᵢ)  (mejor valor hasta iteración i)
- b₀ ≥ b₁ ≥ b₂ ≥ ... ≥ bₙ  (monotónico decreciente)
```

**Propiedad matemática:**
```
bᵢ₊₁ = min(bᵢ, fᵢ₊₁)
```

---

## 📈 Extracción de Datos

### Fuente de Datos

Los datos provienen de la ejecución del algoritmo **Iterated Local Search (ILS)**:

```python
# En scripts/test_experiment_quick.py

ils = IteratedLocalSearch(
    problem=problem,
    constructive=GreedyDSATUR.construct,
    improvement=KempeChain.improve,
    perturbation=RandomRecolor.perturb,
    max_iterations=100,
    time_budget=30.0,
    verbose=False,
    seed=42
)

best_solution, history = ils.solve()
```

### Estructura del Historial

El objeto `history` retornado por `ils.solve()` contiene:

```python
history = {
    'current_fitness': [f₀, f₁, f₂, ..., fₙ],
    'best_fitness': [b₀, b₁, b₂, ..., bₙ],
    'times': [t₀, t₁, t₂, ..., tₙ],
    'iterations': n
}
```

### Recolección en test_experiment_quick.py

```python
# Línea ~200-250 en test_experiment_quick.py

# Ejecutar ILS
best_solution, history = ils.solve()

# Extraer historial de fitness actual (no el mejor acumulado)
current_fitness_history = history['current_fitness']

# Guardar para ploteo
current_fitness_histories.append(current_fitness_history)
```

**Nota importante:** Se usa `current_fitness` (variación real) en lugar de `best_fitness` (línea recta monotónica) para mostrar la dinámica real del algoritmo.

---

## 🎨 Presentación en el Gráfico

### Componentes del Gráfico

#### 1. **Línea Azul (Fitness Actual)**

```
Datos: H = [f₀, f₁, f₂, ..., fₙ]
Color: #1f77b4 (azul)
Estilo: Línea sólida con marcadores circulares
Ancho: 2 píxeles
Transparencia: 80%
Etiqueta: "Fitness actual"
```

**Interpretación:**
- Muestra el valor de fitness en cada iteración
- Puede subir o bajar (no es monotónico)
- Las subidas indican movimientos de perturbación (exploración)
- Las bajadas indican mejoras (explotación)

#### 2. **Línea Naranja Punteada (Mejor Encontrado)**

```
Datos: B = [b₀, b₁, b₂, ..., bₙ]
Color: #ff7f0e (naranja)
Estilo: Línea punteada (--) sin marcadores
Ancho: 2.5 píxeles
Transparencia: 80%
Etiqueta: "Mejor encontrado"
```

**Interpretación:**
- Muestra el mejor valor encontrado hasta cada iteración
- Siempre monotónico decreciente (nunca sube)
- Representa el progreso acumulado del algoritmo
- La pendiente indica velocidad de mejora

#### 3. **Ejes**

```
Eje X: Iteración (0, 1, 2, ..., n)
Eje Y: Número de colores (fitness)
Escala: Lineal en ambos ejes
```

#### 4. **Estadísticas en Caja de Texto**

```
Inicial: f₀ (fitness de la solución inicial)
Mejor: bₙ (mejor valor encontrado)
Final: fₙ (fitness de la solución final)
Mejora: f₀ - bₙ (reducción absoluta)
        (f₀ - bₙ) / f₀ × 100% (reducción porcentual)
```

---

## 📐 Algoritmo de Generación

### Paso 1: Preparar Datos

```python
# visualization/convergence.py, líneas 44-49

iterations = np.arange(len(fitness_history))
# iterations = [0, 1, 2, ..., n-1]

fitness_history = [f₀, f₁, f₂, ..., fₙ]
# Datos crudos del algoritmo
```

### Paso 2: Calcular Mejor Acumulado

```python
# visualization/convergence.py, línea 52

best_fitness = np.minimum.accumulate(fitness_history)
# Aplicar: bᵢ = min(f₀, f₁, ..., fᵢ)

# Ejemplo:
# fitness_history = [50, 48, 46, 45, 45, 47, 45, 44]
# best_fitness    = [50, 48, 46, 45, 45, 45, 45, 44]
```

**Función `np.minimum.accumulate()`:**
```
Entrada: [50, 48, 46, 45, 45, 47, 45, 44]
Salida:  [50, 48, 46, 45, 45, 45, 45, 44]
         ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
         min(50)
             min(50,48)
                 min(50,48,46)
                     min(...,45)
                         min(...,45)
                             min(...,47)→45
                                 min(...,45)
                                     min(...,44)
```

### Paso 3: Plotear Ambas Líneas

```python
# visualization/convergence.py, líneas 47-55

# Línea azul: fitness actual
ax.plot(iterations, fitness_history, 
       color='#1f77b4', linewidth=2, marker='o', markersize=4,
       label='Fitness actual', alpha=0.8)

# Línea naranja: mejor encontrado
ax.plot(iterations, best_fitness,
       color='#ff7f0e', linewidth=2.5, linestyle='--',
       label='Mejor encontrado', alpha=0.8)
```

### Paso 4: Agregar Estadísticas

```python
# visualization/convergence.py, líneas 73-86

final_fitness = fitness_history[-1]      # fₙ
best_found = best_fitness[-1]            # bₙ
improvement = fitness_history[0] - best_found  # f₀ - bₙ

stats_text = (
    f"Inicial: {fitness_history[0]:.0f}\n"
    f"Mejor: {best_found:.0f}\n"
    f"Final: {final_fitness:.0f}\n"
    f"Mejora: {improvement:.0f} ({improvement/fitness_history[0]*100:.1f}%)"
)
```

---

## 📊 Ejemplo Concreto: myciel3

### Datos de Ejecución

Supongamos que ILS ejecuta 100 iteraciones en myciel3:

```
Iteración  Fitness Actual  Mejor Encontrado
    0           50              50
    1           48              48
    2           46              46
    3           45              45
    4           45              45
    5           47              45  ← Perturbación (sube)
    6           44              44  ← Mejora
    7           44              44
    ...
   99            4               4  ← Óptimo encontrado
```

### Visualización Esperada

```
Fitness
   |
50 |●─────────────────────────────────────
   | ╲
48 |  ●─────────────────────────────────
   |   ╲
46 |    ●────────────────────────────────
   |     ╲
45 |      ●●─╱────────────────────────────
   |        ╲╱
44 |         ●────────────────────────────
   |          ╲
   |           ╲╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱
   |            ╲
 4 |             ●─────────────────────────
   |
   └─────────────────────────────────────→ Iteración
   0          25         50         75    100

   ─── Fitness actual (azul)
   ╌╌╌ Mejor encontrado (naranja)
```

### Estadísticas

```
Inicial: 50
Mejor: 4
Final: 4
Mejora: 46 (92.0%)
```

---

## 🔍 Interpretación de Patrones

### Patrón 1: Convergencia Rápida

```
Fitness
   |
50 |●
   | ╲
40 |  ●●●●●
   |       ╲
30 |        ●●●●●●●●●●●●●●●●●●●●●●●●●●●
   |
   └──────────────────────────────────→ Iteración

Interpretación:
- Mejora rápida al inicio
- Estancamiento después
- El algoritmo converge a un óptimo local
```

### Patrón 2: Exploración Activa

```
Fitness
   |
50 |●
   | ╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱
   |  ╲
20 |   ●─────────────────────────────────
   |
   └──────────────────────────────────→ Iteración

Interpretación:
- Muchas perturbaciones (subidas)
- Mejoras ocasionales (bajadas)
- El algoritmo explora activamente el espacio
```

### Patrón 3: Mejora Continua

```
Fitness
   |
50 |●
   | ╲
45 |  ●╲
   |    ╲
40 |     ●╲
   |      ╲
35 |       ●╲
   |        ╲
30 |         ●╲
   |          ╲
25 |           ●─────────────────────────
   |
   └──────────────────────────────────→ Iteración

Interpretación:
- Mejora consistente
- Pocas perturbaciones
- El algoritmo encuentra soluciones mejores regularmente
```

---

## 💻 Código Completo de Generación

```python
# visualization/convergence.py

def plot_convergence_single(
    fitness_history: List[float],
    times: Optional[List[float]] = None,
    output_path: Optional[str] = None,
    instance_name: str = "Instance",
    title: str = "Convergencia de ILS",
    figsize: tuple = (12, 7),
    dpi: int = 300
) -> Optional[str]:
    """
    Grafica la convergencia de una única ejecución.
    
    Entrada:
        fitness_history: [f₀, f₁, f₂, ..., fₙ]
    
    Salida:
        convergence_plot.png
    """
    
    # Paso 1: Preparar eje X
    iterations = np.arange(len(fitness_history))
    
    # Paso 2: Calcular mejor acumulado
    best_fitness = np.minimum.accumulate(fitness_history)
    
    # Paso 3: Crear figura
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Paso 4: Plotear fitness actual
    ax.plot(iterations, fitness_history, 
           color='#1f77b4', linewidth=2, marker='o', markersize=4,
           label='Fitness actual', alpha=0.8)
    
    # Paso 5: Plotear mejor encontrado
    ax.plot(iterations, best_fitness,
           color='#ff7f0e', linewidth=2.5, linestyle='--',
           label='Mejor encontrado', alpha=0.8)
    
    # Paso 6: Configurar ejes
    ax.set_xlabel('Iteración', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de colores (Fitness)', fontsize=12, fontweight='bold')
    ax.set_title(f"{title}\n{instance_name}", fontsize=13, fontweight='bold', pad=15)
    
    # Paso 7: Agregar grid y leyenda
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=11)
    
    # Paso 8: Calcular y mostrar estadísticas
    final_fitness = fitness_history[-1]
    best_found = best_fitness[-1]
    improvement = fitness_history[0] - best_found
    
    stats_text = (
        f"Inicial: {fitness_history[0]:.0f}\n"
        f"Mejor: {best_found:.0f}\n"
        f"Final: {final_fitness:.0f}\n"
        f"Mejora: {improvement:.0f} ({improvement/fitness_history[0]*100:.1f}%)"
    )
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Paso 9: Guardar
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        return str(output_path)
```

---

## 🎯 Qué Representa Realmente

### En Términos del Problema GCP

```
Eje Y (Fitness) = Número de colores usados

Una solución con fitness 4 significa:
  - Se usaron 4 colores para colorear el grafo
  - Todos los vértices adyacentes tienen colores diferentes
  - Es una solución válida (factible)

Una solución con fitness 50 significa:
  - Se usaron 50 colores (muy ineficiente)
  - Probablemente muchos vértices tienen colores únicos
  - Es una solución válida pero de baja calidad
```

### En Términos del Algoritmo ILS

```
Línea azul (Fitness actual):
  - Muestra cómo el algoritmo se mueve en el espacio de soluciones
  - Las subidas = perturbaciones (escapes de óptimos locales)
  - Las bajadas = mejoras (búsqueda local exitosa)

Línea naranja (Mejor encontrado):
  - Muestra el progreso acumulado
  - Nunca sube (monotónico)
  - La pendiente indica eficiencia de búsqueda
```

---

## 📊 Comparación con Otros Gráficos

| Gráfico | Qué Muestra | Eje X | Eje Y |
|---------|-------------|-------|-------|
| **convergence_plot.png** | Dinámica de una ejecución | Iteración | Fitness |
| **01_current_fitness_trajectory_ils.png** | Mismo que convergence (individual) | Iteración | Fitness |
| **06_visited_quality_time_evolution_ils.png** | Dinámica vs tiempo real | Tiempo (s) | Fitness |
| **scalability_plot.png** | Cómo escala con tamaño | Vértices | Tiempo |
| **boxplot_robustness.png** | Variabilidad entre ejecuciones | Algoritmo | Fitness |

---

## 🔬 Propiedades Matemáticas Garantizadas

### 1. Monotonía de Mejor Encontrado

```
∀i < j: best_fitness[i] ≥ best_fitness[j]
```

**Prueba:**
```
best_fitness[i] = min(f₀, f₁, ..., fᵢ)
best_fitness[j] = min(f₀, f₁, ..., fⱼ)

Como {f₀, ..., fᵢ} ⊂ {f₀, ..., fⱼ}:
  min(f₀, ..., fⱼ) ≤ min(f₀, ..., fᵢ)
  ∴ best_fitness[j] ≤ best_fitness[i]
```

### 2. Relación entre Fitness Actual y Mejor

```
∀i: best_fitness[i] ≤ fitness_history[i]
```

**Prueba:**
```
best_fitness[i] = min(f₀, f₁, ..., fᵢ)
fitness_history[i] = fᵢ

min(f₀, ..., fᵢ) ≤ fᵢ (siempre verdadero)
```

### 3. Mejora Total

```
Mejora = fitness_history[0] - best_fitness[n]
Mejora ≥ 0 (siempre no-negativa)
```

---

## 📝 Conclusión

El gráfico `convergence_plot.png` es una **visualización fundamental** que muestra:

1. ✅ **Cómo mejora el algoritmo** a lo largo del tiempo
2. ✅ **Dinámica de exploración vs explotación** (subidas vs bajadas)
3. ✅ **Eficiencia de búsqueda** (pendiente de la línea naranja)
4. ✅ **Calidad de la solución final** (valor en la última iteración)
5. ✅ **Comparabilidad** entre diferentes ejecuciones

Es esencial para **validar que el algoritmo funciona correctamente** y para **comparar diferentes estrategias de búsqueda**.

---

**Documento generado:** 2026-01-02
**Versión:** 1.0
**Estado:** ✅ COMPLETADO
