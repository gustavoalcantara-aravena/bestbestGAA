# 📺 OUTPUTS ESPERADOS: Visualización de Resultados

**Cuando ejecutes**: `python 04-Generated/scripts/gaa_orchestrator.py`

**Esto es lo que verás y generarás**:

---

## 1. SALIDA EN CONSOLA (Lo que ves en pantalla)

```
╔════════════════════════════════════════════════════════════════╗
║                  GAA-ILS CONFIGURATION SEARCH                  ║
║                  Graph Coloring Problem (GCP)                  ║
║                                                                ║
║  Metaheuristic: Iterated Local Search (ILS)                   ║
║  Generative Algorithm Architecture (GAA)                       ║
╚════════════════════════════════════════════════════════════════╝

[14:32:15] Loading configuration from config.yaml...
[14:32:15] Configuration loaded:
           - Max iterations: 500
           - Perturbation strength: 0.20
           - Seed: 42
           - Fitness weights: {quality: 0.5, time: 0.2, robustness: 0.2, feasibility: 0.1}

[14:32:16] Loading problem instances...
[14:32:17] Training set (70 instances):
           ✓ instance_1_n100_d0.5.gcp
           ✓ instance_2_n100_d0.5.gcp
           ✓ instance_3_n100_d0.6.gcp
           ... (67 more instances)
           
[14:32:22] Validation set (15 instances):
           ✓ instance_validation_1.gcp
           ... (14 more instances)
           
[14:32:24] Test set (15 instances):
           ✓ instance_test_1.gcp
           ... (14 more instances)

[14:32:25] Loaded: 70 training + 15 validation + 15 test = 100 instances ✓

[14:32:26] Initializing ILS-based configuration search...
[14:32:26] Initial configuration:
           Constructor: RandomConstruct
           LocalSearch: Swaps
           Perturbation: RemoveSingle
           Iterations: 350

[14:32:27] Starting ILS optimization loop (500 iterations)...

════════════════════════════════════════════════════════════════

ITERATION PROGRESS (showing every 10 iterations):

[Iter   0] Current: 0.6234 | Best: 0.6234 | Improve: No
[Iter  10] Current: 0.7021 | Best: 0.7451 ⭐ NEW BEST (improvement: +4.8%)
[Iter  20] Current: 0.7156 | Best: 0.7451 | Improve: No
[Iter  30] Current: 0.7834 | Best: 0.7834 ⭐ NEW BEST (improvement: +5.1%)
[Iter  40] Current: 0.7612 | Best: 0.7834 | Improve: No
[Iter  50] Current: 0.7923 | Best: 0.7923 ⭐ NEW BEST (improvement: +1.1%)
[Iter  60] Current: 0.7645 | Best: 0.7923 | Improve: No
[Iter  70] Current: 0.8012 | Best: 0.8012 ⭐ NEW BEST (improvement: +1.1%)
[Iter  80] Current: 0.7834 | Best: 0.8012 | Improve: No
[Iter  90] Current: 0.8145 | Best: 0.8145 ⭐ NEW BEST (improvement: +1.7%)
[Iter 100] Current: 0.7956 | Best: 0.8145 | Improve: No
         └─ 100 iterations done in 9.3 seconds (0.093 s/iter)

[Iter 110] Current: 0.8234 | Best: 0.8234 ⭐ NEW BEST (improvement: +1.1%)
[Iter 120] Current: 0.8123 | Best: 0.8234 | Improve: No
[Iter 130] Current: 0.8345 | Best: 0.8345 ⭐ NEW BEST (improvement: +1.3%)
... (iterations 140-300, best improves to 0.8412) ...
[Iter 330] Current: 0.8421 | Best: 0.8542 ⭐ NEW BEST (improvement: +1.5%)
[Iter 340] Current: 0.8512 | Best: 0.8542 | Improve: No
[Iter 350] Current: 0.8234 | Best: 0.8542 | Improve: No
... (iterations 360-490 sin mejoras) ...
[Iter 500] Current: 0.8156 | Best: 0.8542 | Improve: No
         └─ 500 iterations completed in 47.3 seconds

════════════════════════════════════════════════════════════════

ILS SEARCH SUMMARY:

  Total iterations:           500
  Improvements found:         87
  Best fitness achieved:      0.8542 ⭐
  Iteration of best:          342
  Acceptance rate:            18.2% (91/500)
  Search duration:            47.3 seconds
  Configurations evaluated:   50,000 (500 configs × 100 instances)
  
════════════════════════════════════════════════════════════════

[14:33:15] Evaluating TOP-3 configurations on test set...

Configuration #1 (ILS Best):
┌─────────────────────────────────────────────────────┐
│ Fitness: 0.8542 ⭐ BEST                             │
├─────────────────────────────────────────────────────┤
│ Constructor:     LargestDegreeFirst                 │
│ LocalSearch:     ColorSwap                          │
│ Perturbation:    Remove3                            │
│ Iterations:      450                                │
├─────────────────────────────────────────────────────┤
│ Quality Metrics:                                     │
│   Mean colors:   24.3 ± 1.2 (σ)                     │
│   Min:           22 colors                          │
│   Max:           27 colors                          │
│   Success:       98.5% (148/150 successful)         │
│   Time:          245 ms average                     │
│   Consistency:   High (low σ)                       │
└─────────────────────────────────────────────────────┘

Configuration #2 (Second Best):
┌─────────────────────────────────────────────────────┐
│ Fitness: 0.8201                                      │
├─────────────────────────────────────────────────────┤
│ Constructor:     GreedyByWeight                      │
│ LocalSearch:     Relocate                           │
│ Perturbation:    Remove2                            │
│ Iterations:      480                                │
├─────────────────────────────────────────────────────┤
│ Quality Metrics:                                     │
│   Mean colors:   25.1 ± 2.3 (σ)                     │
│   Success:       97.2% (146/150 successful)         │
│   Time:          312 ms average                     │
│   Consistency:   Medium (medium σ)                  │
└─────────────────────────────────────────────────────┘

Configuration #3 (Third Best):
┌─────────────────────────────────────────────────────┐
│ Fitness: 0.7956                                      │
├─────────────────────────────────────────────────────┤
│ Constructor:     GreedyByRatio                       │
│ LocalSearch:     Swaps                              │
│ Perturbation:    RemoveSingle                       │
│ Iterations:      420                                │
├─────────────────────────────────────────────────────┤
│ Quality Metrics:                                     │
│   Mean colors:   25.8 ± 1.5 (σ)                     │
│   Success:       96.8% (145/150 successful)         │
│   Time:          198 ms average                     │
│   Consistency:   Medium (medium σ)                  │
└─────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════

[14:33:45] Generating reports...

[14:33:45] ✓ Created: results/summary.txt (2.3 KB)
[14:33:45] ✓ Created: results/results.json (45.7 KB)
[14:33:45] ✓ Created: results/results.csv (18.2 KB)
[14:33:45] ✓ Created: results/configuration_top_1.yaml (3.1 KB)
[14:33:45] ✓ Created: results/configuration_top_2.yaml (3.0 KB)
[14:33:45] ✓ Created: results/configuration_top_3.yaml (3.0 KB)
[14:33:45] ✓ Created: results/convergence_plot.json (12.4 KB)
[14:33:45] ✓ Created: results/comparison_table.txt (4.5 KB)

════════════════════════════════════════════════════════════════

EXPERIMENT COMPLETED SUCCESSFULLY ✓

  Start time:       2025-12-30 14:32:15
  End time:         2025-12-30 14:33:45
  Total duration:   90 seconds (1.5 minutes)
  
  Phase breakdown:
    - Loading instances:     10 seconds
    - ILS search:            47 seconds
    - Evaluation:            20 seconds
    - Report generation:     13 seconds

RECOMMENDATION:
  ┌─────────────────────────────────────────────────┐
  │ Use Configuration #1 for production:             │
  │                                                  │
  │ ✓ Highest fitness (0.8542)                       │
  │ ✓ Best quality (24.3 colors average)             │
  │ ✓ Excellent success rate (98.5%)                 │
  │ ✓ Good performance (245ms average)               │
  │ ✓ Highly consistent (±1.2 σ)                     │
  └─────────────────────────────────────────────────┘

All results saved to: results/
```

---

## 2. ARCHIVOS GENERADOS EN `results/`

```
results/
│
├── 📄 summary.txt                    ← Resumen legible para humanos
├── 📊 results.json                   ← Datos completos en JSON
├── 📈 results.csv                    ← Tabla para Excel/análisis
├── ⚙️ configuration_top_1.yaml       ← Config mejor (YAML)
├── ⚙️ configuration_top_2.yaml       ← Segunda mejor
├── ⚙️ configuration_top_3.yaml       ← Tercera mejor
├── 📉 convergence_plot.json          ← Datos para gráfico de convergencia
└── 📋 comparison_table.txt           ← Tabla comparativa texto
```

---

## 3. CONTENIDO: `results/summary.txt`

```
═══════════════════════════════════════════════════════════════════
               GAA-ILS EXPERIMENTACIÓN COMPLETA
═══════════════════════════════════════════════════════════════════

INFORMACIÓN DEL PROYECTO
────────────────────────
Project:              GCP-ILS-GAA
Problem:              Graph Coloring Problem (GCP)
Metaheuristic:        Iterated Local Search (ILS)
Framework:            Generative Algorithm Architecture (GAA)
Executed:             2025-12-30 14:32:15 UTC
Duration:             90 seconds

CONFIGURACIÓN DE ILS
───────────────────
Max Iterations:       500
Perturbation Strength: 0.20
Acceptance Criterion: Better or Equal
Initial Seed:        42
Enable Local Search:  True
LS Max Moves:        10

FITNESS WEIGHTS
──────────────
Quality (Colores):   0.5000 (50%)
Time Execution:      0.2000 (20%)
Robustness (Éxito):  0.2000 (20%)
Feasibility:         0.1000 (10%)

INSTANCIAS CARGADAS
──────────────────
Training set:    70 instances (70%)
Validation set:  15 instances (15%)
Test set:        15 instances (15%)
TOTAL:          100 instances

ILS BÚSQUEDA - RESULTADOS
─────────────────────────
Total Configurations Evaluadas: 50,000 (500 iteraciones × 100 instancias)

Configuraciones Mejoradas:      87
Fitness Máximo Logrado:         0.8542
Iteración de Mejor Config:      342 / 500
Tasa de Aceptación:             18.2% (91 aceptadas de 500)
Tiempo de Búsqueda:             47.3 segundos
Mejoras por Segundo:            1.84 mejoras/seg

ESTADÍSTICAS DE CONVERGENCIA
──────────────────────────────
Inicio (Iter 0):                Fitness 0.6234
Mejor a 100 iters:              Fitness 0.7921
Mejor a 250 iters:              Fitness 0.8312
Mejor a 500 iters:              Fitness 0.8542 ⭐

Convergencia: Rápida y consistente (87 mejoras distribuidas)

TOP-3 CONFIGURACIONES ENCONTRADAS
──────────────────────────────────

╔══════════════════════════════════════════════════════════════════╗
║ CONFIGURACIÓN #1 ⭐ MEJOR - Fitness: 0.8542                     ║
╠══════════════════════════════════════════════════════════════════╣
║ Constructor:        LargestDegreeFirst                           ║
║ Local Search:       ColorSwap                                    ║
║ Perturbation:       Remove3                                      ║
║ Iteraciones:        450                                          ║
╠══════════════════════════════════════════════════════════════════╣
║ ESTADÍSTICAS DE CALIDAD                                          ║
║ ─────────────────────                                            ║
║ Media Colores:      24.3  (±1.2)                                 ║
║ Mín Colores:        22                                           ║
║ Máx Colores:        27                                           ║
║ Rango:              5 colores                                    ║
║ Mediana:            24                                           ║
║                                                                  ║
║ ESTADÍSTICAS DE ROBUSTEZ                                         ║
║ ────────────────────────                                         ║
║ Tasa de Éxito:      98.5% (148/150 ejecuciones)                  ║
║ Fallos:             2 (sobre 150 intentos)                       ║
║ Consistencia:       EXCELENTE ✓ (baja variabilidad)              ║
║                                                                  ║
║ ESTADÍSTICAS DE TIEMPO                                           ║
║ ────────────────────                                             ║
║ Tiempo Promedio:    245 ms                                       ║
║ Desv. Estándar:     ±32 ms                                       ║
║ Mín Tiempo:         198 ms                                       ║
║ Máx Tiempo:         312 ms                                       ║
║ Velocidad:          RÁPIDO ✓                                     ║
║                                                                  ║
║ RESUMEN                                                          ║
║ ──────                                                           ║
║ ✓ Mayor fitness (0.8542)                                         ║
║ ✓ Mejor calidad (24.3 colores)                                   ║
║ ✓ Mejor robustez (98.5% éxito)                                   ║
║ ✓ Buena velocidad (245 ms)                                       ║
║ ✓ Muy consistente (±1.2 σ)                                       ║
║ ✓ RECOMENDADO PARA PRODUCCIÓN                                    ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║ CONFIGURACIÓN #2 - Fitness: 0.8201                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Constructor:        GreedyByWeight                               ║
║ Local Search:       Relocate                                     ║
║ Perturbation:       Remove2                                      ║
║ Iteraciones:        480                                          ║
║                                                                  ║
║ Media Colores:      25.1 (±2.3)  | Éxito: 97.2% | Tiempo: 312ms ║
║ Desv. Estándar:     MEDIA        | Fallos: 4    | (±41 ms)       ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║ CONFIGURACIÓN #3 - Fitness: 0.7956                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Constructor:        GreedyByRatio                                ║
║ Local Search:       Swaps                                        ║
║ Perturbation:       RemoveSingle                                 ║
║ Iteraciones:        420                                          ║
║                                                                  ║
║ Media Colores:      25.8 (±1.5)  | Éxito: 96.8% | Tiempo: 198ms ║
║ Desv. Estándar:     BAJA         | Fallos: 5    | (±25 ms)       ║
╚══════════════════════════════════════════════════════════════════╝

ESTADÍSTICAS POR TIPO DE INSTANCIA
──────────────────────────────────

TRAINING SET (70 instancias - Usadas en búsqueda)
  Colores Promedio:      24.2 (min: 22, max: 27)
  Desv. Est:             1.1
  Tasa Éxito:            98.7%
  Tiempo Promedio:       242 ms
  Fitness Agregado:      0.8567 ← Mejor en training

VALIDATION SET (15 instancias - Usadas durante búsqueda para validación)
  Colores Promedio:      24.5 (min: 23, max: 28)
  Desv. Est:             1.3
  Tasa Éxito:            97.8%
  Tiempo Promedio:       251 ms
  Fitness Agregado:      0.8412

TEST SET (15 instancias - Nunca vistas durante búsqueda)
  Colores Promedio:      24.3 (min: 22, max: 26)  
  Desv. Est:             1.2
  Tasa Éxito:            98.5%
  Tiempo Promedio:       245 ms
  Fitness Agregado:      0.8542 ← Generalización buena ✓

ANÁLISIS DE GENERALIZACIÓN
──────────────────────────
Training → Test Delta:   -0.0025 (0.25% peor)
Variación Esperada:      < 2% ← EXCELENTE
Conclusión:              Modelo generaliza muy bien ✓

═══════════════════════════════════════════════════════════════════

RECOMENDACIÓN FINAL
──────────────────
✓ USAR CONFIGURACIÓN #1 PARA PRODUCCIÓN

Razones:
  1. Fitness más alto (0.8542)
  2. Mejor calidad de solución (24.3 colores)
  3. Mejor tasa de éxito (98.5%)
  4. Excelente consistencia (±1.2)
  5. Tiempo de ejecución aceptable (245ms)
  6. Generaliza bien a instancias nuevas

═══════════════════════════════════════════════════════════════════
```

---

## 4. CONTENIDO: `results/results.json` (Estructura)

```json
{
  "metadata": {
    "project_name": "GCP-ILS-GAA",
    "timestamp": "2025-12-30T14:33:45Z",
    "version": "1.0.0",
    "experiment_duration_seconds": 90
  },
  "search_configuration": {
    "max_iterations": 500,
    "perturbation_strength": 0.2,
    "acceptance_criterion": "better_or_equal",
    "seed": 42
  },
  "search_results": {
    "total_iterations": 500,
    "improvements_found": 87,
    "best_fitness": 0.8542,
    "best_fitness_iteration": 342,
    "acceptance_rate": 0.182,
    "search_time_seconds": 47.3
  },
  "top_configurations": [
    {
      "rank": 1,
      "fitness": 0.8542,
      "configuration": {
        "constructor": "LargestDegreeFirst",
        "local_search": "ColorSwap",
        "perturbation": "Remove3",
        "iterations": 450
      },
      "statistics": {
        "mean_colors": 24.3,
        "std_colors": 1.2,
        "min_colors": 22,
        "max_colors": 27,
        "success_rate": 0.985,
        "failed_instances": 2,
        "total_instances": 150,
        "mean_time_ms": 245.0,
        "std_time_ms": 32.0
      },
      "dataset_breakdown": {
        "training": {
          "mean_colors": 24.2,
          "success_rate": 0.987,
          "instances": 70
        },
        "validation": {
          "mean_colors": 24.5,
          "success_rate": 0.978,
          "instances": 15
        },
        "test": {
          "mean_colors": 24.3,
          "success_rate": 0.985,
          "instances": 15
        }
      }
    },
    // ... configurations 2 and 3 ...
  ]
}
```

---

## 5. CONTENIDO: `results/results.csv`

```csv
rank,fitness,constructor,local_search,perturbation,iterations,mean_colors,std_colors,min_colors,max_colors,success_rate,failed,total_runs,mean_time_ms,std_time_ms,recommendation
1,0.8542,LargestDegreeFirst,ColorSwap,Remove3,450,24.3,1.2,22,27,0.985,2,150,245.0,32.0,✓ USE FOR PRODUCTION
2,0.8201,GreedyByWeight,Relocate,Remove2,480,25.1,2.3,23,28,0.972,4,150,312.0,41.0,Consider as backup
3,0.7956,GreedyByRatio,Swaps,RemoveSingle,420,25.8,1.5,22,26,0.968,5,150,198.0,25.0,Faster but lower quality
```

---

## 6. CONTENIDO: `results/configuration_top_1.yaml`

```yaml
metadata:
  rank: 1
  fitness_score: 0.8542
  iteration_found: 342
  seed: 42
  total_configurations_evaluated: 50000

configuration:
  name: "LargestDegreeFirst + ColorSwap + Remove3"
  
  constructor:
    name: LargestDegreeFirst
    description: "Ordena vértices por grado descendente. 
                   Vertices de mayor grado se colorean primero."
  
  local_search:
    operator: ColorSwap
    max_moves: 10
    description: "Intenta intercambiar colores entre vértices adyacentes
                   para mejorar la solución."
  
  perturbation:
    operator: Remove3
    strength: 0.20
    description: "Remueve la asignación de color de 3 vértices aleatorios
                   para escapar del óptimo local."
  
  parameters:
    iterations: 450
    seed: 42

performance_metrics:
  quality:
    mean_colors: 24.3
    std_colors: 1.2
    min_colors: 22
    max_colors: 27
    improvement_potential: "Low (near optimal)"
  
  robustness:
    success_rate: 0.985
    failed_instances: 2
    total_instances: 150
    reliability_index: 0.985
  
  efficiency:
    mean_time_ms: 245
    std_time_ms: 32
    min_time_ms: 198
    max_time_ms: 312
    speed_rating: "Good"
  
  consistency:
    coefficient_of_variation: 0.049
    stability_rating: "Excellent"

dataset_performance:
  training_set:
    instances: 70
    mean_colors: 24.2
    success_rate: 0.987
    avg_time_ms: 242
    
  validation_set:
    instances: 15
    mean_colors: 24.5
    success_rate: 0.978
    avg_time_ms: 251
    
  test_set:
    instances: 15
    mean_colors: 24.3
    success_rate: 0.985
    avg_time_ms: 245

recommendations:
  production_ready: true
  reason: "Excellent fitness, high success rate, good speed, and low variance"
  expected_performance: "Mean 24 colors, 98%+ success, ~250ms per instance"
  notes:
    - "Generalizes well to unseen test instances"
    - "Consistent performance across different instance sizes"
    - "Recommended for immediate deployment"
```

---

## 7. RESUMEN DE OUTPUTS

| Output | Tipo | Tamaño | Propósito |
|--------|------|--------|-----------|
| **summary.txt** | Texto | 2-3 KB | Lectura humana |
| **results.json** | JSON | 40-50 KB | Análisis automatizado |
| **results.csv** | CSV | 15-20 KB | Excel/Pandas/R |
| **config_top_1.yaml** | YAML | 3-4 KB | Reproducibilidad |
| **config_top_2.yaml** | YAML | 3-4 KB | Comparación |
| **config_top_3.yaml** | YAML | 3-4 KB | Alternativas |
| **convergence_plot.json** | JSON | 10-15 KB | Gráfico de convergencia |

**Total generado**: ~100-150 KB de resultados

---

## ✨ Conclusión

Cuando ejecutes `gaa_orchestrator.py`:

1. **Verás en pantalla**: Progreso en tiempo real, mejoras encontradas, top-3 configuraciones
2. **Se crearán archivos**: 8 archivos en carpeta `results/`
3. **Tendrás**:
   - ✅ Resumen legible (summary.txt)
   - ✅ Datos completos (results.json)
   - ✅ Tabla para análisis (results.csv)
   - ✅ Configuraciones reproducibles (YAML)
   - ✅ Datos para gráficos (convergence_plot.json)

**Todo automatizado, sin intervención manual.**
