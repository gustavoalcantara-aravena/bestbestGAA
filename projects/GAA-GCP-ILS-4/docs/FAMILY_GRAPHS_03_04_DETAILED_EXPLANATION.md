# Explicación Detallada: Gráficos 03 y 04 de Familia

## 📋 Resumen Ejecutivo

Los gráficos 03 y 04 muestran la **variabilidad y consistencia** de los algoritmos GAA generados. Ambos gráficos comparan el desempeño de los 3 algoritmos GAA diferentes, pero desde perspectivas distintas.

---

## 🔬 Gráfico 03: Robustness of Solution Quality (Color Count Distribution) across {family} Instances

### ¿Qué es este gráfico?

Un **box plot** (gráfico de cajas) que muestra la **distribución de valores** (número de colores) obtenidos por cada algoritmo GAA en todas las instancias de la familia.

### ¿Qué significa "replica"?

En el contexto de este gráfico, **"replica" NO significa una ejecución repetida**. Significa:

```
Cada algoritmo GAA es una "réplica" diferente generada automáticamente
por el sistema GAA (Grammatical Algorithm Analyzer).

- GAA_Algorithm_1 = Réplica 1 (primer algoritmo generado)
- GAA_Algorithm_2 = Réplica 2 (segundo algoritmo generado)
- GAA_Algorithm_3 = Réplica 3 (tercer algoritmo generado)

Cada réplica es un algoritmo DIFERENTE con estructura y parámetros distintos,
pero todos resuelven el mismo problema (GCP).
```

### Estructura de Datos

```python
# test_experiment_quick.py, líneas ~250-300

# Generar 3 algoritmos GAA diferentes
for algo_idx in range(3):
    gaa_generator = GrammaticalAlgorithmGenerator()
    algorithm = gaa_generator.generate()  # Genera algoritmo DIFERENTE
    
    # Ejecutar este algoritmo en TODAS las instancias
    for instance in instances:
        problem = load_instance(instance)
        solution, history = algorithm.solve(problem)
        n_colors = solution.num_colors
        
        # Guardar resultado
        algorithm_results[f"GAA_Algorithm_{algo_idx+1}"].append(n_colors)

# Resultado: 3 listas de valores
# GAA_Algorithm_1: [4, 5, 6, 7, 8]  (5 instancias)
# GAA_Algorithm_2: [4, 5, 6, 7, 8]  (5 instancias)
# GAA_Algorithm_3: [4, 5, 6, 7, 8]  (5 instancias)
```

### Visualización del Box Plot

```
Gráfico 03: Robustness of Solution Quality (Color Count Distribution)

        GAA_Algorithm_1    GAA_Algorithm_2    GAA_Algorithm_3
        
        ┌─────────┐        ┌─────────┐        ┌─────────┐
      9 │         │        │         │        │    ●    │  ← Outlier
        │         │        │         │        │         │
      8 │    ●    │        │    ●    │        │    ●    │
        │    │    │        │    │    │        │    │    │
      7 │ ┌──┼──┐ │     ┌──┼──┐ │ ┌──┼──┐ │
        │ │  │  │ │     │  │  │ │ │  │  │ │
      6 │ │  ●  │ │     │  ●  │ │ │  ●  │ │  ← Mediana (línea en caja)
        │ │  │  │ │     │  │  │ │ │  │  │ │
      5 │ └──┼──┘ │     └──┼──┘ │ └──┼──┘ │
        │    │    │        │    │    │    │
      4 │    ●    │        ●    │    ●    │
        │         │        │    │        │
      3 └─────────┘        └─────────┘        └─────────┘

Elementos del Box Plot:
  ● = Punto individual (outlier o valor extremo)
  ─ = Whisker (línea que conecta min/max)
  ┌─┐ = Caja (contiene 50% de los datos)
  ● = Mediana (línea dentro de la caja)
```

### Interpretación Detallada

```
CAJA (Box):
  - Representa el 50% central de los datos
  - Q1 (cuartil inferior): 25% de los datos están por debajo
  - Q3 (cuartil superior): 75% de los datos están por debajo
  - IQR = Q3 - Q1 (rango intercuartil)

MEDIANA (línea dentro de la caja):
  - Valor central: 50% de datos por debajo, 50% por encima
  - Si está en el centro de la caja → distribución simétrica
  - Si está cerca de Q1 → distribución sesgada hacia abajo
  - Si está cerca de Q3 → distribución sesgada hacia arriba

WHISKERS (líneas que salen de la caja):
  - Conectan la caja con los valores extremos
  - Rango típico: [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
  - Valores fuera de este rango son outliers

OUTLIERS (puntos individuales):
  - Valores anómalos o extremos
  - Pueden indicar comportamiento inusual del algoritmo
```

### Ejemplo Concreto: Familia MYC

```
Supongamos que ejecutamos los 3 algoritmos GAA en 5 instancias:

Instancia  GAA_Algo_1  GAA_Algo_2  GAA_Algo_3
myciel3    4           4           4
myciel4    5           5           5
myciel5    6           6           6
myciel6    7           7           7
myciel7    8           8           8

Box Plot para GAA_Algorithm_1:
  Valores: [4, 5, 6, 7, 8]
  Min: 4
  Q1: 5
  Mediana: 6
  Q3: 7
  Max: 8
  IQR: 2
  Whiskers: [5-3=2, 7+3=10] → [2, 10]
  Outliers: Ninguno (todos dentro del rango)

Resultado: Caja simétrica, sin outliers
Interpretación: Algoritmo consistente, comportamiento predecible
```

### ¿Qué Significa Robustness?

```
ROBUSTEZ = Consistencia del algoritmo

Caja PEQUEÑA (IQR pequeño):
  → Algoritmo produce soluciones SIMILARES
  → Comportamiento CONSISTENTE
  → ROBUSTEZ ALTA ✅

Caja GRANDE (IQR grande):
  → Algoritmo produce soluciones MUY DIFERENTES
  → Comportamiento VARIABLE
  → ROBUSTEZ BAJA ❌

Outliers presentes:
  → Algunas instancias causan comportamiento anómalo
  → Algoritmo no es robusto en esos casos
```

### Comparación entre Algoritmos (Gráfico 03)

```
Si comparamos 3 algoritmos GAA:

GAA_Algorithm_1: Caja pequeña, sin outliers
  → Algoritmo robusto y consistente

GAA_Algorithm_2: Caja mediana, 1 outlier
  → Algoritmo moderadamente robusto
  → Tiene problemas en algunos casos

GAA_Algorithm_3: Caja grande, múltiples outliers
  → Algoritmo poco robusto
  → Comportamiento muy variable

Conclusión: GAA_Algorithm_1 es el más robusto
```

---

## 🔬 Gráfico 04: Average Algorithm Ranking (Lower is Better) across {family} Instances

### ¿Qué es este gráfico?

Un **gráfico de barras horizontal** que muestra el **ranking promedio** de cada algoritmo GAA basado en su desempeño en todas las instancias.

### Concepto de Ranking

```
Para cada instancia, se rankean los 3 algoritmos:

Instancia myciel3:
  GAA_Algorithm_1: 4 colores → Rank 1 (mejor)
  GAA_Algorithm_2: 4 colores → Rank 1 (empate)
  GAA_Algorithm_3: 4 colores → Rank 1 (empate)

Instancia myciel4:
  GAA_Algorithm_1: 5 colores → Rank 1 (mejor)
  GAA_Algorithm_2: 5 colores → Rank 1 (empate)
  GAA_Algorithm_3: 5 colores → Rank 1 (empate)

...

Ranking Promedio:
  GAA_Algorithm_1: (1+1+1+1+1) / 5 = 1.0
  GAA_Algorithm_2: (1+1+1+1+1) / 5 = 1.0
  GAA_Algorithm_3: (1+1+1+1+1) / 5 = 1.0
```

### Estructura de Datos

```python
# visualization/plotter_v2.py, método plot_family_algorithm_ranking()

def plot_family_algorithm_ranking(self,
                                 family_name: str,
                                 instances: List[str],
                                 algorithm_results: Dict[str, List[int]]):
    
    # Para cada algoritmo, calcular ranking promedio
    rankings = {}
    
    for algo_name in algorithm_results.keys():
        algo_rankings = []
        
        # Para cada instancia
        for inst_idx in range(len(instances)):
            # Obtener valores de todos los algoritmos para esta instancia
            values = [algorithm_results[a][inst_idx] for a in algorithms]
            
            # Rankear (1 = mejor, 3 = peor)
            sorted_values = sorted(values)
            rank = sorted_values.index(values[algorithms.index(algo_name)]) + 1
            algo_rankings.append(rank)
        
        # Calcular ranking promedio
        avg_rank = sum(algo_rankings) / len(algo_rankings)
        rankings[algo_name] = avg_rank
```

### Visualización del Gráfico de Barras

```
Gráfico 04: Average Algorithm Ranking (Lower is Better)

GAA_Algorithm_1  ████████████████ 1.0
GAA_Algorithm_2  ██████████████████ 1.5
GAA_Algorithm_3  ████████████████████ 2.0

← Mejor (ranking bajo)          Peor (ranking alto) →

Escala: 1.0 = Mejor, 3.0 = Peor
```

### Interpretación

```
Ranking = 1.0:
  → Algoritmo SIEMPRE gana (mejor en todas las instancias)
  → Desempeño excelente

Ranking = 1.5:
  → Algoritmo gana en promedio
  → Desempeño bueno

Ranking = 2.0:
  → Algoritmo es mediocre
  → Desempeño medio

Ranking = 3.0:
  → Algoritmo SIEMPRE pierde (peor en todas las instancias)
  → Desempeño pobre

Diferencias pequeñas (< 0.5):
  → Algoritmos similares
  → Competencia cerrada

Diferencias grandes (> 1.0):
  → Algoritmos muy diferentes
  → Ganador claro
```

### Ejemplo Concreto: Familia MYC

```
Supongamos resultados diferentes:

Instancia  GAA_Algo_1  GAA_Algo_2  GAA_Algo_3  Rankings
myciel3    4           4           5           1, 1, 3
myciel4    5           5           6           1, 1, 3
myciel5    6           6           7           1, 1, 3
myciel6    7           7           8           1, 1, 3
myciel7    8           8           9           1, 1, 3

Ranking Promedio:
  GAA_Algorithm_1: (1+1+1+1+1) / 5 = 1.0 ← MEJOR
  GAA_Algorithm_2: (1+1+1+1+1) / 5 = 1.0 ← MEJOR
  GAA_Algorithm_3: (3+3+3+3+3) / 5 = 3.0 ← PEOR

Gráfico:
  GAA_Algorithm_1  ████████████████ 1.0  ← Ganador
  GAA_Algorithm_2  ████████████████ 1.0  ← Ganador
  GAA_Algorithm_3  ████████████████████ 3.0  ← Perdedor
```

---

## 📊 Diferencia entre Gráfico 03 y Gráfico 04

### Gráfico 03: Robustness (Box Plot)

```
¿QUÉ MIDE?
  → Variabilidad de cada algoritmo
  → Consistencia en sus resultados
  → Distribución de valores

¿CÓMO?
  → Muestra todos los valores individuales
  → Calcula estadísticas (Q1, mediana, Q3)
  → Identifica outliers

PREGUNTA QUE RESPONDE:
  "¿Qué tan consistente es cada algoritmo?
   ¿Produce siempre soluciones similares?"

EJEMPLO:
  Si GAA_Algorithm_1 produce [4, 5, 6, 7, 8]
  y GAA_Algorithm_2 produce [4, 4, 4, 4, 4]
  
  → GAA_Algorithm_2 es más robusto (menos variabilidad)
```

### Gráfico 04: Ranking (Barras)

```
¿QUÉ MIDE?
  → Desempeño relativo de cada algoritmo
  → Quién gana más instancias
  → Ranking promedio

¿CÓMO?
  → Rankea algoritmos en cada instancia
  → Calcula ranking promedio
  → Compara algoritmos

PREGUNTA QUE RESPONDE:
  "¿Cuál algoritmo es mejor en promedio?
   ¿Quién gana más competiciones?"

EJEMPLO:
  Si en 5 instancias:
  - GAA_Algorithm_1 gana 4 veces (rank 1)
  - GAA_Algorithm_2 gana 1 vez (rank 1)
  
  → GAA_Algorithm_1 es mejor (ranking promedio más bajo)
```

### Comparación Visual

```
GRÁFICO 03 (Robustness):
  Responde: ¿Qué tan variable es cada algoritmo?
  Muestra: Distribución de valores
  Eje Y: Número de colores
  
  GAA_Algorithm_1: [4, 5, 6, 7, 8]  → Caja grande
  GAA_Algorithm_2: [4, 4, 4, 4, 4]  → Caja pequeña
  
  Conclusión: Algo_2 es más robusto (menos variable)

GRÁFICO 04 (Ranking):
  Responde: ¿Cuál algoritmo es mejor?
  Muestra: Ranking promedio
  Eje X: Ranking (1 = mejor, 3 = peor)
  
  GAA_Algorithm_1: 1.8 (gana a veces)
  GAA_Algorithm_2: 1.2 (gana más veces)
  
  Conclusión: Algo_2 es mejor (ranking más bajo)
```

---

## 🎯 Resumen: ¿Qué Significa "Replica"?

```
En el contexto de estos gráficos:

REPLICA = Algoritmo diferente generado automáticamente

GAA_Algorithm_1 (Replica 1):
  - Estructura diferente
  - Parámetros diferentes
  - Comportamiento diferente
  - Pero resuelve el mismo problema

GAA_Algorithm_2 (Replica 2):
  - Estructura diferente
  - Parámetros diferentes
  - Comportamiento diferente
  - Pero resuelve el mismo problema

GAA_Algorithm_3 (Replica 3):
  - Estructura diferente
  - Parámetros diferentes
  - Comportamiento diferente
  - Pero resuelve el mismo problema

OBJETIVO:
  Comparar 3 algoritmos DIFERENTES generados automáticamente
  para ver cuál es más robusto y cuál tiene mejor desempeño
```

---

## 💡 Conclusión

| Aspecto | Gráfico 03 | Gráfico 04 |
|---------|-----------|-----------|
| **Nombre** | Robustness (Box Plot) | Average Ranking (Barras) |
| **Mide** | Variabilidad | Desempeño relativo |
| **Pregunta** | ¿Qué tan consistente? | ¿Cuál es mejor? |
| **Visualización** | Cajas con distribución | Barras horizontales |
| **Eje Principal** | Número de colores | Ranking promedio |
| **Interpretación** | Caja pequeña = robusto | Barra corta = mejor |

Ambos gráficos son complementarios:
- **Gráfico 03** muestra **cómo varía** cada algoritmo
- **Gráfico 04** muestra **cuál gana** en promedio

---

**Documento generado:** 2026-01-02
**Versión:** 1.0
**Estado:** ✅ COMPLETADO
