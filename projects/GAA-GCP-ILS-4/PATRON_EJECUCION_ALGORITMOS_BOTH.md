# Patrón de Ejecución de Algoritmos BOTH (Inspirado en KBP-SA)

**Basado en**: `demo_experimentation_both.py` de KBP-SA  
**Fecha**: 01 Enero 2026

---

## 🎯 PATRÓN CLAVE DE KBP-SA

En KBP-SA, el patrón BOTH funciona así:

```
1. GENERAR algoritmos UNA SOLA VEZ
   └─ 3 algoritmos GAA con seed=42

2. PROCESAR GRUPO 1 (low_dimensional)
   ├─ Cargar 10 instancias
   ├─ Para cada instancia:
   │  └─ Ejecutar 3 algoritmos × 1 repetición = 3 experimentos
   ├─ Ejecutar SA en cada instancia con tracking completo
   ├─ Agregar datos de todas las instancias
   └─ Generar visualizaciones agregadas + por instancia

3. PROCESAR GRUPO 2 (large_scale)
   ├─ Cargar 21 instancias
   ├─ Para cada instancia:
   │  └─ Ejecutar 3 algoritmos × 1 repetición = 3 experimentos
   ├─ Ejecutar SA en cada instancia con tracking completo
   ├─ Agregar datos de todas las instancias
   └─ Generar visualizaciones agregadas + por instancia

4. ANÁLISIS COMPARATIVO
   ├─ Estadísticas descriptivas por algoritmo
   ├─ Test de Friedman (comparación global)
   ├─ Test de Wilcoxon pareado
   ├─ Cohen's d (tamaño de efecto)
   └─ Ranking de algoritmos
```

---

## 🔄 ESTRUCTURA DE EJECUCIÓN DETALLADA

### Paso 1: Generar Algoritmos (UNA SOLA VEZ)

```python
def generate_algorithms(pop_size=3, seed=42):
    """Generar población de algoritmos GAA"""
    grammar = Grammar(min_depth=2, max_depth=3, seed=seed)
    generator = AlgorithmGenerator(grammar=grammar, seed=seed)
    
    algorithms = []
    for i in range(pop_size):
        algo = generator.generate_with_validation()
        if algo:
            algorithms.append({
                'name': f'GAA_Algorithm_{i+1}',
                'ast': algo,
                'interpreter': execute_algorithm
            })
    
    return algorithms  # 3 algoritmos compartidos para AMBOS grupos
```

**Tiempo**: ~0.00s (negligible)  
**Output**: Lista de 3 algoritmos con AST, nombre e intérprete

---

### Paso 2: Procesar Grupo 1

```python
def process_group(group_name, instances, algorithms, timestamp):
    """
    Procesa un grupo completo:
    1. Ejecuta experimentos
    2. Análisis estadístico
    3. Visualizaciones
    """
    
    # 2.1: Cargar instancias
    loader = DatasetLoader()
    all_instances = loader.load_folder(group_name)
    # Resultado: 10 instancias (low_dimensional) o 21 (large_scale)
    
    # 2.2: Ejecutar experimentos
    results = []
    for instance in all_instances:
        for algo in algorithms:
            # Ejecutar algoritmo en instancia
            solution = algo['interpreter'](algo['ast'], instance, seed=42)
            
            results.append({
                'instance': instance.name,
                'algorithm': algo['name'],
                'value': solution.value,
                'time': execution_time,
                'gap': calculate_gap(solution, instance)
            })
    
    # Resultado: 10×3=30 experimentos (low_dim) o 21×3=63 (large_scale)
    
    # 2.3: Análisis estadístico
    analyzer = StatisticalAnalyzer()
    
    # Agrupar por algoritmo
    algorithm_results = {}
    for algo in algorithms:
        algo_name = algo['name']
        algo_data = [r for r in results if r['algorithm'] == algo_name]
        gaps = [r['gap'] for r in algo_data]
        
        algorithm_results[algo_name] = gaps
        
        # Estadísticas descriptivas
        stats = analyzer.descriptive_statistics(gaps)
        print(f"{algo_name}: media={stats['mean']:.2f}%, std={stats['std']:.2f}%")
    
    # Test de Friedman (comparación global)
    comparison = analyzer.compare_multiple_algorithms(
        algorithm_results,
        test_type="friedman"
    )
    
    # Resultado: Ranking de algoritmos, p-value, mejor algoritmo
    
    # 2.4: Visualizaciones
    visualizer = ResultsVisualizer()
    
    # Gráficas agregadas (promedio de todas las instancias)
    visualizer.plot_gap_evolution(...)
    visualizer.plot_acceptance_rate(...)
    visualizer.plot_delta_e_distribution(...)
    
    # Gráficas por instancia (una para cada instancia)
    for instance in all_instances:
        visualizer.plot_exploration_exploitation_balance(...)
    
    # Resultado: 3 gráficas agregadas + N gráficas por instancia
    
    return {
        'results': results,
        'analysis': comparison,
        'best_algorithm': comparison['best_algorithm']
    }
```

**Tiempo**: ~2-3 segundos por grupo  
**Output**: Resultados, análisis, visualizaciones

---

## 📊 MATRIZ DE EJECUCIÓN DETALLADA

### Grupo 1: LOW-DIMENSIONAL (10 instancias)

```
Instancia 1 (f1):
  ├─ GAA_Algorithm_1 → Ejecutar SA → Gap: 2.5%
  ├─ GAA_Algorithm_2 → Ejecutar SA → Gap: 1.8%
  └─ GAA_Algorithm_3 → Ejecutar SA → Gap: 3.2%

Instancia 2 (f2):
  ├─ GAA_Algorithm_1 → Ejecutar SA → Gap: 1.5%
  ├─ GAA_Algorithm_2 → Ejecutar SA → Gap: 0.9%
  └─ GAA_Algorithm_3 → Ejecutar SA → Gap: 2.1%

...

Instancia 10 (f10):
  ├─ GAA_Algorithm_1 → Ejecutar SA → Gap: 1.2%
  ├─ GAA_Algorithm_2 → Ejecutar SA → Gap: 0.6%
  └─ GAA_Algorithm_3 → Ejecutar SA → Gap: 1.8%

TOTAL: 30 experimentos (10 instancias × 3 algoritmos × 1 repetición)
```

### Grupo 2: LARGE-SCALE (21 instancias)

```
Instancia 1 (knapPI_1_100):
  ├─ GAA_Algorithm_1 → Ejecutar SA → Gap: 3.2%
  ├─ GAA_Algorithm_2 → Ejecutar SA → Gap: 2.5%
  └─ GAA_Algorithm_3 → Ejecutar SA → Gap: 4.1%

...

Instancia 21 (knapPI_3_10000):
  ├─ GAA_Algorithm_1 → Ejecutar SA → Gap: 5.2%
  ├─ GAA_Algorithm_2 → Ejecutar SA → Gap: 4.8%
  └─ GAA_Algorithm_3 → Ejecutar SA → Gap: 6.1%

TOTAL: 63 experimentos (21 instancias × 3 algoritmos × 1 repetición)
```

---

## 🔬 ANÁLISIS ESTADÍSTICO POR GRUPO

### Paso 1: Estadísticas Descriptivas

```python
# Para cada algoritmo, calcular:
- Media de gaps
- Desviación estándar
- Mínimo y máximo
- Intervalo de confianza 95%

Ejemplo:
GAA_Algorithm_1:
  Gap (%): media=2.45 ± 1.23, min=0.6, max=5.2
  IC 95%: [1.85, 3.05]

GAA_Algorithm_2:
  Gap (%): media=1.92 ± 0.98, min=0.5, max=4.8
  IC 95%: [1.42, 2.42]

GAA_Algorithm_3:
  Gap (%): media=3.12 ± 1.45, min=1.2, max=6.1
  IC 95%: [2.45, 3.79]
```

### Paso 2: Test de Friedman (Comparación Global)

```python
# Comparar los 3 algoritmos en todas las instancias
comparison = analyzer.compare_multiple_algorithms(
    algorithm_results,
    test_type="friedman"
)

# Resultado:
Test: Friedman
  p-value: 0.0234
  Hay diferencias significativas entre algoritmos (p < 0.05)

Rankings promedio (menor = mejor):
  1.45  GAA_Algorithm_2  ← MEJOR
  2.12  GAA_Algorithm_1
  2.43  GAA_Algorithm_3
```

### Paso 3: Test Pareado (Wilcoxon)

```python
# Comparar pares de algoritmos
wilcoxon = analyzer.wilcoxon_signed_rank_test(
    algorithm_results['GAA_Algorithm_2'],
    algorithm_results['GAA_Algorithm_3']
)

# Resultado:
Comparación pareada: GAA_Algorithm_2 vs GAA_Algorithm_3
  Wilcoxon: p=0.0156
  GAA_Algorithm_2 es significativamente mejor (p < 0.05)
  Cohen's d: 0.65 (efecto mediano)
```

---

## 📈 VISUALIZACIONES GENERADAS

### Por Grupo (Agregadas)

```
Grupo LOW-DIMENSIONAL:
├─ gap_evolution.png
│  └─ Evolución del gap promedio (todas las 10 instancias)
├─ acceptance_rate.png
│  └─ Tasa de aceptación promedio
├─ delta_e_distribution.png
│  └─ Distribución de ΔE (todas las instancias)
└─ exploration_exploitation_*.png (10 gráficas)
   └─ Una por cada instancia

Grupo LARGE-SCALE:
├─ gap_evolution.png
├─ acceptance_rate.png
├─ delta_e_distribution.png
└─ exploration_exploitation_*.png (21 gráficas)

TOTAL: 6 + 10 + 6 + 21 = 43 gráficas
```

---

## 🔄 APLICACIÓN A GAA-GCP-ILS-4

### Adaptación del Patrón

```python
def experiment_both_gcp():
    """Experimentación BOTH para GAA-GCP-ILS-4"""
    
    # Paso 1: Generar algoritmos (UNA SOLA VEZ)
    algorithms = generate_gaa_algorithms(pop_size=5, seed=42)
    # Resultado: 5 algoritmos GAA
    
    # Paso 2: Procesar Grupo 1 (PEQUEÑOS)
    group1_results = process_group(
        group_name="small",
        instances=["myciel3", "myciel4", "myciel5"],
        algorithms=algorithms
    )
    # Resultado: 15 experimentos (3 inst × 5 alg × 1 rep)
    
    # Paso 3: Procesar Grupo 2 (MEDIANOS)
    group2_results = process_group(
        group_name="medium",
        instances=["le450_5a", "le450_5b", "le450_5c"],
        algorithms=algorithms
    )
    # Resultado: 15 experimentos (3 inst × 5 alg × 1 rep)
    
    # Paso 4: Análisis Comparativo
    comparison = compare_groups(group1_results, group2_results)
    
    # Paso 5: Visualizaciones
    generate_visualizations(group1_results, group2_results, comparison)
    
    # TOTAL: 30 experimentos
```

### Matriz de Ejecución para GAA-GCP-ILS-4

```
GRUPO 1: PEQUEÑOS (3 instancias)
┌──────────────────────────────────────────────────────┐
│ myciel3:  Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ myciel4:  Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ myciel5:  Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ SUBTOTAL: 15 experimentos                            │
└──────────────────────────────────────────────────────┘

GRUPO 2: MEDIANOS (3 instancias)
┌──────────────────────────────────────────────────────┐
│ le450_5a: Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ le450_5b: Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ le450_5c: Alg1 | Alg2 | Alg3 | Alg4 | Alg5          │
│ SUBTOTAL: 15 experimentos                            │
└──────────────────────────────────────────────────────┘

TOTAL: 30 experimentos (mismos 5 algoritmos en ambos grupos)
```

---

## 📊 OUTPUTS ESPERADOS

```
output/{timestamp}/
├── both_experiments/
│   ├── group_small/
│   │   ├── gap_evolution.png
│   │   ├── algorithm_ranking.png
│   │   ├── instance_difficulty.png
│   │   ├── exploration_exploitation_myciel3.png
│   │   ├── exploration_exploitation_myciel4.png
│   │   ├── exploration_exploitation_myciel5.png
│   │   └── results.json
│   │
│   ├── group_medium/
│   │   ├── gap_evolution.png
│   │   ├── algorithm_ranking.png
│   │   ├── instance_difficulty.png
│   │   ├── exploration_exploitation_le450_5a.png
│   │   ├── exploration_exploitation_le450_5b.png
│   │   ├── exploration_exploitation_le450_5c.png
│   │   └── results.json
│   │
│   ├── comparison_analysis.json
│   ├── friedman_test_results.json
│   ├── algorithm_comparison_boxplot.png
│   ├── algorithm_ranking_aggregated.png
│   └── both_experiments_summary.txt
```

---

## 🎯 CLAVE DEL ÉXITO EN KBP-SA

1. **Algoritmos generados UNA SOLA VEZ** → Reutilización eficiente
2. **Mismos algoritmos en ambos grupos** → Comparación justa
3. **Tracking completo de variables** → Análisis detallado
4. **Agregación de datos** → Visualizaciones significativas
5. **Análisis estadístico robusto** → Conclusiones válidas
6. **Documentación automática** → Reproducibilidad

---

## 🔧 IMPLEMENTACIÓN EN GAA-GCP-ILS-4

**Próximo paso**: Crear `experimentation/runner.py` siguiendo este patrón exacto.

**Archivo a crear**: `scripts/experiment_both_gcp.py`

```python
#!/usr/bin/env python3
"""
Experimentación BOTH para GAA-GCP-ILS-4

Ejecuta los mismos algoritmos GAA en dos grupos de instancias:
- Grupo 1: Pequeñas (myciel3, myciel4, myciel5)
- Grupo 2: Medianas (le450_5a, le450_5b, le450_5c)

Patrón basado en KBP-SA demo_experimentation_both.py
"""

from experimentation.runner import ExperimentRunner
from experimentation.statistics import StatisticalAnalyzer
from experimentation.visualization import ResultsVisualizer

def main():
    # Paso 1: Generar algoritmos
    algorithms = generate_gaa_algorithms(pop_size=5, seed=42)
    
    # Paso 2: Procesar Grupo 1
    group1_results = process_group("small", algorithms)
    
    # Paso 3: Procesar Grupo 2
    group2_results = process_group("medium", algorithms)
    
    # Paso 4: Análisis comparativo
    analyzer = StatisticalAnalyzer()
    comparison = analyzer.compare_groups(group1_results, group2_results)
    
    # Paso 5: Visualizaciones
    visualizer = ResultsVisualizer()
    visualizer.generate_both_visualizations(group1_results, group2_results, comparison)
    
    print("✅ Experimentación BOTH completada")

if __name__ == "__main__":
    main()
```

---

**Conclusión**: El patrón BOTH de KBP-SA es altamente eficiente y reproducible. Aplicarlo a GAA-GCP-ILS-4 permitirá análisis comparativos robustos de algoritmos generados automáticamente.
