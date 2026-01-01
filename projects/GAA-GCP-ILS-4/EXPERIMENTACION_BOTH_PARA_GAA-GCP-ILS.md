# Experimentación "BOTH" para GAA-GCP-ILS-4

**Basado en**: Análisis de `ESTRUCTURA_EJECUCION_BOTH.md` de KBP-SA  
**Fecha**: 01 Enero 2026

---

## 🎯 CONCEPTO "BOTH" EN KBP-SA

En KBP-SA, "BOTH" significa ejecutar **dos grupos de datasets** con **los mismos algoritmos GAA** generados:

```
Algoritmos GAA (generados UNA SOLA VEZ)
    ↓
├─ Grupo 1: LOW-DIMENSIONAL (10 instancias)
│   └─ Ejecutar 3 algoritmos × 10 instancias = 30 experimentos
│
└─ Grupo 2: LARGE-SCALE (21 instancias)
    └─ Ejecutar 3 algoritmos × 21 instancias = 63 experimentos

TOTAL: 93 experimentos con 3 algoritmos compartidos
```

### Ventajas del enfoque BOTH

1. **Reutilización de algoritmos**: Se generan UNA SOLA VEZ
2. **Comparación justa**: Mismos algoritmos en ambos grupos
3. **Análisis completo**: Comportamiento en instancias pequeñas y grandes
4. **Eficiencia**: No regenerar algoritmos para cada grupo

---

## 🔄 APLICACIÓN A GAA-GCP-ILS-4

### Estructura Propuesta

```
Algoritmos GAA (generados UNA SOLA VEZ con seed=42)
    ↓
├─ Grupo 1: PEQUEÑOS (myciel3, myciel4, myciel5)
│   └─ Ejecutar 5 algoritmos × 3 instancias = 15 experimentos
│
└─ Grupo 2: MEDIANOS (le450_5a, le450_5b, le450_5c)
    └─ Ejecutar 5 algoritmos × 3 instancias = 15 experimentos

TOTAL: 30 experimentos con 5 algoritmos compartidos
```

### Matriz de Ejecución

```
┌─────────────────────────────────────────────────┐
│ GRUPO 1: PEQUEÑOS (3 instancias)                │
├─────────────────────────────────────────────────┤
│ myciel3:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ myciel4:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ myciel5:  GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ SUBTOTAL: 15 experimentos
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ GRUPO 2: MEDIANOS (3 instancias)                │
├─────────────────────────────────────────────────┤
│ le450_5a: GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ le450_5b: GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ le450_5c: GAA_Alg_1 | GAA_Alg_2 | GAA_Alg_3 | GAA_Alg_4 | GAA_Alg_5
│ SUBTOTAL: 15 experimentos
└─────────────────────────────────────────────────┘

TOTAL: 30 experimentos
```

---

## 📊 PIPELINE DE EXPERIMENTACIÓN "BOTH"

### Paso 1: Generar Algoritmos (UNA SOLA VEZ)

```python
# experimentation/runner.py
def generate_gaa_algorithms(pop_size=5, seed=42):
    """Generar población de algoritmos GAA"""
    grammar = Grammar(min_depth=2, max_depth=4)
    generator = AlgorithmGenerator(grammar=grammar, seed=seed)
    
    population = []
    for i in range(pop_size):
        algo = generator.generate_with_validation()
        if algo:
            population.append(algo)
    
    return population  # 5 algoritmos compartidos para AMBOS grupos
```

**Tiempo**: ~0.00s (negligible)

### Paso 2: Ejecutar Grupo 1 (PEQUEÑOS)

```python
def run_group_1_experiments(algorithms, output_dir):
    """Ejecutar 5 algoritmos × 3 instancias = 15 experimentos"""
    
    instances = [
        "datasets/MYC/myciel3.col",
        "datasets/MYC/myciel4.col",
        "datasets/MYC/myciel5.col"
    ]
    
    results_group1 = []
    
    for instance_path in instances:
        problem = GraphColoringProblem.load_from_dimacs(instance_path)
        
        for algo_idx, algorithm in enumerate(algorithms):
            # Ejecutar algoritmo GAA en instancia
            solution = execute_algorithm(algorithm, problem, seed=42)
            
            results_group1.append({
                'instance': problem.name,
                'algorithm': f"GAA_Algorithm_{algo_idx+1}",
                'colors': solution.num_colors,
                'time': execution_time
            })
    
    return results_group1  # 15 resultados
```

**Tiempo estimado**: ~2-3 segundos

### Paso 3: Ejecutar Grupo 2 (MEDIANOS)

```python
def run_group_2_experiments(algorithms, output_dir):
    """Ejecutar 5 algoritmos × 3 instancias = 15 experimentos"""
    
    instances = [
        "datasets/LEI/le450_5a.col",
        "datasets/LEI/le450_5b.col",
        "datasets/LEI/le450_5c.col"
    ]
    
    results_group2 = []
    
    for instance_path in instances:
        problem = GraphColoringProblem.load_from_dimacs(instance_path)
        
        for algo_idx, algorithm in enumerate(algorithms):
            solution = execute_algorithm(algorithm, problem, seed=42)
            
            results_group2.append({
                'instance': problem.name,
                'algorithm': f"GAA_Algorithm_{algo_idx+1}",
                'colors': solution.num_colors,
                'time': execution_time
            })
    
    return results_group2  # 15 resultados
```

**Tiempo estimado**: ~2-3 segundos

### Paso 4: Análisis Comparativo

```python
def analyze_both_groups(results_group1, results_group2):
    """Análisis comparativo entre grupos"""
    
    analysis = {
        'group1_stats': calculate_stats(results_group1),
        'group2_stats': calculate_stats(results_group2),
        'algorithm_ranking': rank_algorithms(results_group1 + results_group2),
        'instance_difficulty': analyze_instance_difficulty(results_group1, results_group2)
    }
    
    return analysis
```

**Tiempo**: ~0.1 segundos

### Paso 5: Visualizaciones

```python
def generate_visualizations(results_group1, results_group2, output_dir):
    """Generar gráficas comparativas"""
    
    # Gráficas de comparación (3)
    plot_algorithm_comparison_boxplot(results_group1, results_group2)
    plot_algorithm_performance_bars(results_group1, results_group2)
    plot_instance_difficulty_scatter(results_group1, results_group2)
    
    # Gráficas de AST (1)
    visualize_best_algorithm_ast(best_algorithm)
    
    # Gráficas por grupo (6)
    plot_group1_convergence()
    plot_group1_algorithm_ranking()
    plot_group1_instance_difficulty()
    plot_group2_convergence()
    plot_group2_algorithm_ranking()
    plot_group2_instance_difficulty()
    
    # TOTAL: 10 gráficas
```

**Tiempo**: ~3-4 segundos

---

## ⏱️ DESGLOSE DE TIEMPOS

### Versión Original

```
┌──────────────────────────────────────────┐
│ Paso 1: Generar 5 algoritmos   0.00s    │
│ Paso 2: Grupo 1 (15 exp)       ~2.5s    │
│ Paso 3: Grupo 2 (15 exp)       ~2.5s    │
│ Paso 4: Análisis               ~0.1s    │
│ Paso 5: Visualizaciones        ~3.5s    │
├──────────────────────────────────────────┤
│ TOTAL:                         ~8.6s    │
└──────────────────────────────────────────┘
```

### Versión Optimizada (inspirada en KBP-SA)

**Optimizaciones**:
1. Backend matplotlib 'Agg': +5% mejora
2. Reducir gráficas individuales: 10 → 6 representativas (-40%)
3. Caché de instancias cargadas

```
┌──────────────────────────────────────────┐
│ Paso 1: Generar 5 algoritmos   0.00s    │
│ Paso 2: Grupo 1 (15 exp)       ~1.8s    │
│ Paso 3: Grupo 2 (15 exp)       ~1.8s    │
│ Paso 4: Análisis               ~0.1s    │
│ Paso 5: Visualizaciones        ~2.0s    │
├──────────────────────────────────────────┤
│ TOTAL:                         ~5.7s    │
│ MEJORA:                        34%      │
└──────────────────────────────────────────┘
```

---

## 📈 GRÁFICAS GENERADAS

### Versión Original (10 gráficas)

**Comparativas** (3):
- Boxplot de algoritmos (ambos grupos)
- Barras de desempeño (ambos grupos)
- Scatter de dificultad de instancias

**AST** (1):
- Árbol sintáctico del mejor algoritmo

**Por Grupo** (6):
- Grupo 1: Convergencia, ranking, dificultad
- Grupo 2: Convergencia, ranking, dificultad

### Versión Optimizada (8 gráficas)

**Comparativas** (3):
- Boxplot
- Barras
- Scatter

**AST** (1):
- Árbol sintáctico

**Representativas** (4):
- Convergencia agregada (ambos grupos)
- Ranking agregado (ambos grupos)

---

## 🗂️ ESTRUCTURA DE OUTPUTS

```
output/{timestamp}/
├── results/                    (ILS)
├── plots/                      (ILS)
├── gaa/
│   ├── algorithms/
│   │   ├── generation_0/
│   │   │   ├── algorithm_0.json
│   │   │   ├── algorithm_1.json
│   │   │   ├── algorithm_2.json
│   │   │   ├── algorithm_3.json
│   │   │   └── algorithm_4.json
│   │   └── ...
│   ├── best_algorithm.json
│   ├── best_algorithm.png (AST)
│   ├── evolution_history.json
│   └── evolution_summary.txt
├── both_experiments/           (NUEVO)
│   ├── group1_results.json
│   ├── group2_results.json
│   ├── comparison_analysis.json
│   ├── algorithm_comparison_boxplot.png
│   ├── algorithm_performance_bars.png
│   ├── instance_difficulty_scatter.png
│   ├── convergence_aggregated.png
│   ├── algorithm_ranking_aggregated.png
│   └── both_experiments_summary.txt
├── solutions/
└── logs/
```

---

## 🔧 IMPLEMENTACIÓN EN CÓDIGO

### Script Principal: `scripts/experiment_both.py`

```python
#!/usr/bin/env python3
"""
Experimentación BOTH para GAA-GCP-ILS-4

Ejecuta los mismos algoritmos GAA en dos grupos de instancias:
- Grupo 1: Pequeñas (myciel3, myciel4, myciel5)
- Grupo 2: Medianas (le450_5a, le450_5b, le450_5c)
"""

from experimentation.runner import ExperimentRunner
from experimentation.visualization import generate_both_visualizations
from experimentation.statistics import analyze_both_groups

def main():
    runner = ExperimentRunner(output_dir="output")
    
    # Paso 1: Generar algoritmos (UNA SOLA VEZ)
    print("🧬 Generando algoritmos GAA...")
    algorithms = runner.generate_gaa_algorithms(pop_size=5, seed=42)
    print(f"✅ {len(algorithms)} algoritmos generados\n")
    
    # Paso 2: Ejecutar Grupo 1
    print("📊 Ejecutando Grupo 1 (PEQUEÑOS)...")
    results_group1 = runner.run_group_experiments(
        algorithms=algorithms,
        group_name="small",
        instances=["myciel3", "myciel4", "myciel5"]
    )
    print(f"✅ {len(results_group1)} experimentos completados\n")
    
    # Paso 3: Ejecutar Grupo 2
    print("📊 Ejecutando Grupo 2 (MEDIANOS)...")
    results_group2 = runner.run_group_experiments(
        algorithms=algorithms,
        group_name="medium",
        instances=["le450_5a", "le450_5b", "le450_5c"]
    )
    print(f"✅ {len(results_group2)} experimentos completados\n")
    
    # Paso 4: Análisis
    print("📈 Analizando resultados...")
    analysis = analyze_both_groups(results_group1, results_group2)
    print(f"✅ Análisis completado\n")
    
    # Paso 5: Visualizaciones
    print("🎨 Generando visualizaciones...")
    generate_both_visualizations(
        results_group1=results_group1,
        results_group2=results_group2,
        analysis=analysis,
        output_dir=runner.output_dir
    )
    print(f"✅ Visualizaciones generadas\n")
    
    print("=" * 80)
    print("✅ EXPERIMENTACIÓN BOTH COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
```

---

## 📝 CONCLUSIÓN

El enfoque "BOTH" de KBP-SA aplicado a GAA-GCP-ILS-4:

1. **Genera algoritmos UNA SOLA VEZ** (reutilización)
2. **Ejecuta en dos grupos de instancias** (análisis completo)
3. **Compara desempeño** entre grupos
4. **Genera visualizaciones** comparativas
5. **Tiempo total**: ~5-8 segundos (optimizado)

**Ventajas**:
- ✅ Análisis justo (mismos algoritmos)
- ✅ Eficiente (no regenerar)
- ✅ Completo (pequeñas y medianas)
- ✅ Reproducible (seed fijo)

---

**Próximo paso**: Implementar `experimentation/runner.py` con este enfoque.
