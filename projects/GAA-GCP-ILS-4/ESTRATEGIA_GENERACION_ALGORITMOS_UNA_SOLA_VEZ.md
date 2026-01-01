# Estrategia: Generar Algoritmos Automáticamente en Cada Ejecución

**Fecha**: 01 Enero 2026  
**Basado en**: `problema_metaheuristica.md` y patrón BOTH de KBP-SA

---

## 🎯 OBJETIVO PRINCIPAL

**Generar automáticamente 3 nuevos algoritmos GAA en cada ejecución** y:
- ✅ **Seleccionar el mejor** basado en resultados experimentales
- ✅ **Outputear los 3 algoritmos** si no se conoce el KBP (Best Known Solution)
- ✅ **Documentar comparativa** entre los 3 algoritmos generados

---

## 📋 PROBLEMA: Graph Coloring Problem (GCP)

**Definición**:
- **Nombre**: Graph Coloring Problem
- **Tipo**: Minimización
- **Categoría**: Combinatorial Optimization - NP-Complete
- **Objetivo**: Minimizar el número de colores utilizados
- **Restricción**: Ningún par de vértices adyacentes puede tener el mismo color

**Aplicaciones**:
- Asignación de frecuencias en redes de comunicación
- Planificación de horarios (scheduling)
- Asignación de registros en compiladores
- Resolución de sudokus
- Diseño de circuitos VLSI

---

## 🧬 GENERACIÓN AUTOMÁTICA DE ALGORITMOS (EN CADA EJECUCIÓN)

### Paso 1: Generar 3 Algoritmos GAA Automáticamente

```python
def generate_gaa_algorithms_automatically(pop_size=3, seed=None):
    """
    Generar población de algoritmos GAA AUTOMÁTICAMENTE en cada ejecución
    
    Características:
    - Genera 3 NUEVOS algoritmos en cada ejecución
    - Seed aleatorio (o especificado) para diversidad
    - Se ejecutan en todas las instancias
    - Se selecciona el MEJOR basado en resultados
    """
    from gaa.grammar import Grammar
    from gaa.generator import AlgorithmGenerator
    from datetime import datetime
    
    # Crear gramática y generador
    grammar = Grammar(min_depth=2, max_depth=4)
    
    # Si no se especifica seed, usar timestamp para generar uno diferente cada vez
    if seed is None:
        seed = int(datetime.now().timestamp()) % 10000
    
    generator = AlgorithmGenerator(grammar=grammar, seed=seed)
    
    # Generar población
    algorithms = []
    for i in range(pop_size):
        algo = generator.generate_with_validation()
        if algo:
            algorithms.append({
                'id': i + 1,
                'name': f'GAA_Algorithm_{i+1}',
                'ast': algo,
                'seed': seed,
                'generation_timestamp': datetime.now().isoformat(),
                'grammar': {
                    'min_depth': grammar.min_depth,
                    'max_depth': grammar.max_depth,
                    'terminals': {
                        'constructive': grammar.CONSTRUCTIVE_TERMINALS,
                        'improvement': grammar.IMPROVEMENT_TERMINALS,
                        'perturbation': grammar.PERTURBATION_TERMINALS
                    }
                }
            })
    
    return algorithms
```

**Características**:
- ✅ **Generados automáticamente en cada ejecución** (nuevos algoritmos cada vez)
- ✅ Seed variable para diversidad (o fijo para reproducibilidad)
- ✅ Documentados con metadatos completos
- ✅ Timestamp de generación registrado

**Output**:
```json
{
  "algorithms": [
    {
      "id": 1,
      "name": "GAA_Algorithm_1",
      "ast": {...},
      "seed": 7234,
      "generation_timestamp": "2026-01-01T02:29:00",
      "grammar": {...}
    },
    {
      "id": 2,
      "name": "GAA_Algorithm_2",
      "ast": {...},
      "seed": 7234,
      "generation_timestamp": "2026-01-01T02:29:00",
      "grammar": {...}
    },
    {
      "id": 3,
      "name": "GAA_Algorithm_3",
      "ast": {...},
      "seed": 7234,
      "generation_timestamp": "2026-01-01T02:29:00",
      "grammar": {...}
    }
  ],
  "generation_timestamp": "2026-01-01T02:29:00",
  "total_algorithms": 3,
  "seed_used": 7234
}
```

### Paso 2: Ejecutar 3 Algoritmos y Seleccionar el Mejor

```python
def run_algorithms_and_select_best(algorithms, instances, output_mgr):
    """
    Ejecutar los 3 algoritmos generados en todas las instancias
    y seleccionar el MEJOR basado en resultados
    """
    
    results_per_algorithm = {}
    
    # Ejecutar cada algoritmo en todas las instancias
    for algo in algorithms:
        algo_name = algo['name']
        algo_results = []
        
        for instance in instances:
            # Ejecutar algoritmo
            solution = execute_algorithm(algo['ast'], instance, seed=algo['seed'])
            
            # Calcular métricas
            gap = calculate_gap(solution, instance)
            
            algo_results.append({
                'instance': instance.name,
                'algorithm': algo_name,
                'colors': solution.num_colors,
                'gap': gap,
                'time': execution_time
            })
        
        results_per_algorithm[algo_name] = algo_results
    
    # Seleccionar el MEJOR algoritmo
    best_algorithm = select_best_algorithm(results_per_algorithm)
    
    return {
        'all_results': results_per_algorithm,
        'best_algorithm': best_algorithm,
        'algorithms_generated': algorithms
    }
```

**Lógica de Selección del Mejor**:
```python
def select_best_algorithm(results_per_algorithm):
    """
    Seleccionar el mejor algoritmo basado en:
    1. Si se conoce KBP: algoritmo con menor gap promedio
    2. Si NO se conoce KBP: algoritmo con menor número de colores promedio
    """
    
    best_algo = None
    best_score = float('inf')
    
    for algo_name, results in results_per_algorithm.items():
        # Calcular métrica promedio
        if all(r.get('gap') is not None for r in results):
            # Conocemos KBP: usar gap promedio
            avg_metric = sum(r['gap'] for r in results) / len(results)
            metric_name = "gap_promedio"
        else:
            # No conocemos KBP: usar número de colores promedio
            avg_metric = sum(r['colors'] for r in results) / len(results)
            metric_name = "colores_promedio"
        
        if avg_metric < best_score:
            best_score = avg_metric
            best_algo = {
                'name': algo_name,
                'metric': metric_name,
                'score': avg_metric,
                'results': results
            }
    
    return best_algo
```

---

## 📊 EXPERIMENTACIONES INDICADAS EN problema_metaheuristica.md

### Fase 5: Scripts Ejecutables (PRIORIDAD 5)

Según `problema_metaheuristica.md`, se deben ejecutar:

1. **`scripts/test_quick.py`** - Validación Rápida (10s)
   - Ejecutar 3 algoritmos en 3 instancias pequeñas
   - Verificar que funcionan correctamente
   - Generar gráficas básicas

2. **`scripts/demo_complete.py`** - Demo Funcional (30s)
   - Ejecutar 3 algoritmos en 6 instancias (pequeñas + medianas)
   - Análisis estadístico básico
   - Documentación de resultados

3. **`scripts/demo_experimentation.py`** - Experimentos (5 min)
   - Ejecutar 3 algoritmos en múltiples instancias
   - Análisis estadístico completo (Friedman, Wilcoxon)
   - Visualizaciones agregadas + por instancia

4. **`scripts/experiment_large_scale.py`** - Benchmarks
   - Ejecutar 3 algoritmos en instancias grandes
   - Análisis de escalabilidad
   - Comparación de rendimiento

---

## 🔄 FLUJO DE EXPERIMENTACIÓN CON GENERACIÓN AUTOMÁTICA

```
┌─────────────────────────────────────────────────────────────┐
│ PASO 0: GENERAR 3 NUEVOS ALGORITMOS AUTOMÁTICAMENTE        │
├─────────────────────────────────────────────────────────────┤
│ • Generar 3 algoritmos GAA automáticamente                 │
│ • Seed variable para diversidad (o fijo para reproducir)   │
│ • Guardar en output/{timestamp}/gaa/algorithms_generated.json
│ • Documentar metadatos (grammar, terminals, timestamp)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: test_quick.py (10s)                                │
├─────────────────────────────────────────────────────────────┤
│ Instancias: myciel3, myciel4, myciel5 (3 pequeñas)        │
│ Algoritmos: GAA_Algorithm_1, 2, 3 (generados automáticamente)
│ Experimentos: 3 inst × 3 alg × 1 rep = 9 experimentos     │
│ Selección: MEJOR algoritmo basado en colores promedio     │
│ Outputs:                                                    │
│ • output/{timestamp}/quick_test/all_algorithms.json       │
│ • output/{timestamp}/quick_test/best_algorithm.json       │
│ • output/{timestamp}/quick_test/results.json              │
│ • output/{timestamp}/quick_test/plots/ (5 gráficas)       │
│ • output/{timestamp}/quick_test/summary.txt               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: demo_complete.py (30s)                             │
├─────────────────────────────────────────────────────────────┤
│ Instancias: myciel3-5, le450_5a-c (6 instancias)          │
│ Algoritmos: GAA_Algorithm_1, 2, 3 (mismos del PASO 1)     │
│ Experimentos: 6 inst × 3 alg × 1 rep = 18 experimentos    │
│ Selección: MEJOR algoritmo basado en colores promedio     │
│ Outputs:                                                    │
│ • output/{timestamp}/complete_demo/all_algorithms.json    │
│ • output/{timestamp}/complete_demo/best_algorithm.json    │
│ • output/{timestamp}/complete_demo/results.json           │
│ • output/{timestamp}/complete_demo/plots/ (8 gráficas)    │
│ • output/{timestamp}/complete_demo/analysis.json          │
│ • output/{timestamp}/complete_demo/summary.txt            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 3: demo_experimentation.py (5 min)                    │
├─────────────────────────────────────────────────────────────┤
│ Instancias: 10-20 instancias (pequeñas + medianas)        │
│ Algoritmos: GAA_Algorithm_1, 2, 3 (mismos del PASO 1)     │
│ Experimentos: N inst × 3 alg × 1 rep = 3N experimentos    │
│ Selección: MEJOR algoritmo basado en gap/colores promedio │
│ Análisis:                                                   │
│ • Estadísticas descriptivas por algoritmo                  │
│ • Test de Friedman (comparación global)                   │
│ • Test de Wilcoxon pareado                                │
│ • Cohen's d (tamaño de efecto)                            │
│ Outputs:                                                    │
│ • output/{timestamp}/experimentation/all_algorithms.json  │
│ • output/{timestamp}/experimentation/best_algorithm.json  │
│ • output/{timestamp}/experimentation/group_small/         │
│ • output/{timestamp}/experimentation/group_medium/        │
│ • output/{timestamp}/experimentation/comparison.json      │
│ • output/{timestamp}/experimentation/plots/ (10+ gráficas)│
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 4: experiment_large_scale.py (benchmarks)             │
├─────────────────────────────────────────────────────────────┤
│ Instancias: 5-10 instancias grandes (500+ vértices)       │
│ Algoritmos: GAA_Algorithm_1, 2, 3 (mismos del PASO 1)     │
│ Experimentos: N inst × 3 alg × 1 rep = 3N experimentos    │
│ Selección: MEJOR algoritmo basado en gap/colores promedio │
│ Análisis:                                                   │
│ • Escalabilidad (tiempo vs tamaño)                        │
│ • Rendimiento en instancias grandes                       │
│ • Comparación de estrategias                              │
│ Outputs:                                                    │
│ • output/{timestamp}/large_scale/all_algorithms.json      │
│ • output/{timestamp}/large_scale/best_algorithm.json      │
│ • output/{timestamp}/large_scale/results.json             │
│ • output/{timestamp}/large_scale/scalability.png          │
│ • output/{timestamp}/large_scale/performance.json         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ ANÁLISIS FINAL CONSOLIDADO                                 │
├─────────────────────────────────────────────────────────────┤
│ • Comparar resultados de todas las fases                   │
│ • Identificar MEJOR algoritmo global                       │
│ • SI NO se conoce KBP: outputear los 3 algoritmos         │
│ • SI se conoce KBP: outputear solo el MEJOR               │
│ • Generar reporte ejecutivo                                │
│ • Documentar conclusiones                                  │
│ • Guardar en output/{timestamp}/final_report.md           │
└─────────────────────────────────────────────────────────────┘
```

### Lógica de Output de Algoritmos

```python
def output_algorithms_based_on_kbp(best_algorithm, all_algorithms, instances, output_mgr):
    """
    Outputear algoritmos basado en disponibilidad de KBP
    
    Regla:
    - SI se conoce KBP para todas las instancias: outputear solo MEJOR
    - SI NO se conoce KBP: outputear los 3 ALGORITMOS GENERADOS
    """
    
    # Verificar si se conoce KBP para todas las instancias
    kbp_known = all(inst.colors_known is not None for inst in instances)
    
    if kbp_known:
        # Conocemos KBP: outputear solo el MEJOR algoritmo
        output_mgr.save_algorithm_json(best_algorithm, filename='best_algorithm.json')
        output_mgr.save_algorithm_pseudocode(best_algorithm, filename='best_algorithm_pseudocode.txt')
        
        print("✅ KBP conocido para todas las instancias")
        print(f"📊 Mejor algoritmo: {best_algorithm['name']}")
        print(f"📁 Guardado en: output/{timestamp}/gaa/best_algorithm.json")
    else:
        # NO conocemos KBP: outputear los 3 ALGORITMOS GENERADOS
        output_mgr.save_algorithm_json(
            {'algorithms': all_algorithms},
            filename='all_algorithms_generated.json'
        )
        
        # También guardar el mejor
        output_mgr.save_algorithm_json(best_algorithm, filename='best_algorithm.json')
        
        print("⚠️  KBP NO conocido para algunas instancias")
        print(f"📊 Algoritmos generados: {len(all_algorithms)}")
        print(f"🏆 Mejor algoritmo: {best_algorithm['name']}")
        print(f"📁 Guardados en: output/{timestamp}/gaa/all_algorithms_generated.json")
```

---

## 📁 ESTRUCTURA DE OUTPUTS

```
output/{timestamp}/
├── gaa/
│   ├── algorithms_base.json          ← ALGORITMOS GENERADOS UNA SOLA VEZ
│   ├── best_algorithm.json
│   ├── evolution_history.json
│   └── evolution_summary.txt
│
├── quick_test/                       ← PASO 1: test_quick.py
│   ├── results.json
│   ├── summary.txt
│   └── plots/
│       ├── convergence_plot.png
│       ├── scalability_plot.png
│       ├── boxplot_robustness.png
│       ├── time_quality_tradeoff.png
│       └── conflict_heatmap.png
│
├── complete_demo/                    ← PASO 2: demo_complete.py
│   ├── results.json
│   ├── analysis.json
│   ├── summary.txt
│   └── plots/
│       ├── algorithm_comparison_boxplot.png
│       ├── algorithm_performance_bars.png
│       ├── instance_difficulty_scatter.png
│       ├── convergence_aggregated.png
│       ├── algorithm_ranking.png
│       ├── gap_evolution.png
│       ├── acceptance_rate.png
│       └── delta_e_distribution.png
│
├── experimentation/                  ← PASO 3: demo_experimentation.py
│   ├── group_small/
│   │   ├── results.json
│   │   ├── plots/
│   │   │   ├── convergence.png
│   │   │   ├── ranking.png
│   │   │   └── difficulty.png
│   │   └── exploration_exploitation_*.png (por instancia)
│   │
│   ├── group_medium/
│   │   ├── results.json
│   │   ├── plots/
│   │   │   ├── convergence.png
│   │   │   ├── ranking.png
│   │   │   └── difficulty.png
│   │   └── exploration_exploitation_*.png (por instancia)
│   │
│   ├── comparison_analysis.json
│   ├── friedman_test_results.json
│   └── wilcoxon_test_results.json
│
├── large_scale/                      ← PASO 4: experiment_large_scale.py
│   ├── results.json
│   ├── scalability.png
│   ├── performance.json
│   └── summary.txt
│
├── final_report.md                   ← ANÁLISIS CONSOLIDADO
├── results/                          (ILS)
├── plots/                            (ILS)
├── solutions/
└── logs/
```

---

## 🔧 IMPLEMENTACIÓN

### Script Principal: `scripts/run_all_experiments_with_gaa.py`

```python
#!/usr/bin/env python3
"""
Ejecutar todas las experimentaciones con algoritmos GAA generados UNA SOLA VEZ

Flujo:
1. Generar 3 algoritmos GAA (seed=42)
2. Ejecutar test_quick.py
3. Ejecutar demo_complete.py
4. Ejecutar demo_experimentation.py
5. Ejecutar experiment_large_scale.py
6. Generar reporte final consolidado
"""

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from experimentation.runner import ExperimentRunner
from utils.output_manager import OutputManager
import json
from pathlib import Path

def main():
    # Inicializar OutputManager
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="all_datasets")
    
    print("=" * 80)
    print("🧬 GENERANDO ALGORITMOS GAA UNA SOLA VEZ")
    print("=" * 80 + "\n")
    
    # PASO 0: Generar algoritmos UNA SOLA VEZ
    grammar = Grammar(min_depth=2, max_depth=4)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    algorithms = []
    for i in range(3):
        algo = generator.generate_with_validation()
        if algo:
            algorithms.append({
                'id': i + 1,
                'name': f'GAA_Algorithm_{i+1}',
                'ast': algo,
                'seed': 42
            })
    
    print(f"✅ {len(algorithms)} algoritmos generados con seed=42\n")
    
    # Guardar algoritmos base
    algorithms_file = output_mgr.save_algorithm_json(
        {'algorithms': algorithms},
        filename='algorithms_base.json'
    )
    print(f"✅ Algoritmos guardados en: {algorithms_file}\n")
    
    # PASO 1: test_quick.py
    print("=" * 80)
    print("1️⃣  EJECUTANDO: test_quick.py (Validación Rápida)")
    print("=" * 80 + "\n")
    
    runner = ExperimentRunner(output_mgr, algorithms)
    quick_results = runner.run_quick_test(
        instances=["myciel3", "myciel4", "myciel5"],
        output_subdir="quick_test"
    )
    print(f"✅ test_quick.py completado\n")
    
    # PASO 2: demo_complete.py
    print("=" * 80)
    print("2️⃣  EJECUTANDO: demo_complete.py (Demo Funcional)")
    print("=" * 80 + "\n")
    
    complete_results = runner.run_complete_demo(
        instances=["myciel3", "myciel4", "myciel5", "le450_5a", "le450_5b", "le450_5c"],
        output_subdir="complete_demo"
    )
    print(f"✅ demo_complete.py completado\n")
    
    # PASO 3: demo_experimentation.py
    print("=" * 80)
    print("3️⃣  EJECUTANDO: demo_experimentation.py (Experimentos Completos)")
    print("=" * 80 + "\n")
    
    experimentation_results = runner.run_experimentation(
        output_subdir="experimentation"
    )
    print(f"✅ demo_experimentation.py completado\n")
    
    # PASO 4: experiment_large_scale.py
    print("=" * 80)
    print("4️⃣  EJECUTANDO: experiment_large_scale.py (Benchmarks)")
    print("=" * 80 + "\n")
    
    large_scale_results = runner.run_large_scale_experiment(
        output_subdir="large_scale"
    )
    print(f"✅ experiment_large_scale.py completado\n")
    
    # ANÁLISIS FINAL CONSOLIDADO
    print("=" * 80)
    print("📊 ANÁLISIS FINAL CONSOLIDADO")
    print("=" * 80 + "\n")
    
    final_report = runner.generate_final_report(
        quick_results,
        complete_results,
        experimentation_results,
        large_scale_results
    )
    
    print(f"✅ Reporte final generado\n")
    
    print("=" * 80)
    print("✅ TODAS LAS EXPERIMENTACIONES COMPLETADAS")
    print("=" * 80)
    print(f"📁 Resultados guardados en: {session_dir}\n")

if __name__ == "__main__":
    main()
```

---

## 📝 VENTAJAS DE ESTA ESTRATEGIA

1. **✅ Reproducibilidad**: Seed fijo (42) garantiza mismos algoritmos
2. **✅ Eficiencia**: Algoritmos generados UNA SOLA VEZ, reutilizados en todas las fases
3. **✅ Comparabilidad**: Mismos algoritmos en todas las experimentaciones
4. **✅ Escalabilidad**: Fácil agregar más instancias sin regenerar algoritmos
5. **✅ Documentación**: Metadatos completos de algoritmos generados
6. **✅ Análisis robusto**: Estadísticas comparativas entre fases

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Crear `experimentation/runner.py` con métodos para cada fase
2. ✅ Crear `experimentation/statistics.py` con análisis estadístico
3. ✅ Crear `experimentation/visualization.py` con gráficas
4. ✅ Crear `scripts/run_all_experiments_with_gaa.py` como punto de entrada
5. ✅ Ejecutar y validar todas las fases

---

**Estado**: 🚀 Listo para implementación

**Tiempo estimado**: ~10 minutos (quick_test) + 30 segundos (demo_complete) + 5 minutos (experimentation) + benchmarks (variable)

**Total**: ~15-20 minutos para ejecución completa
