# 📁 ESTRUCTURA DE OUTPUT PARA GAA

**Proyecto**: GAA-GCP-ILS-4  
**Componente**: Generative Algorithm Architecture (GAA)

---

## 📋 ESTRUCTURA DE DIRECTORIOS

Todos los outputs de GAA se guardan en `output/{timestamp}/gaa/` con la siguiente estructura:

```
output/{timestamp}/
├── results/                        # Resultados de ILS
│   ├── summary.csv
│   ├── detailed_results.json
│   ├── statistics.txt
│   ├── gaps_report.txt
│   ├── timing_report.txt
│   ├── timing_report.json
│   └── *.sol
├── plots/                          # Gráficas de ILS
│   ├── convergence_plot.png
│   ├── scalability_plot.png
│   ├── boxplot_robustness.png
│   ├── time_quality_tradeoff.png
│   └── conflict_heatmap.png
├── solutions/                      # Soluciones
│   └── *.sol
├── logs/                           # Logs de ejecución
│   └── execution_*.log
└── gaa/                            # Outputs de GAA
    ├── best_algorithm.json         # Mejor algoritmo encontrado
    ├── evolution_history.json      # Historial de evolución
    ├── population_stats.json       # Estadísticas de población
    ├── evolution_summary.txt       # Resumen de ejecución
    ├── algorithm_pseudocode.txt    # Pseudocódigo del mejor algoritmo
    └── algorithms/                 # Algoritmos por generación
        ├── generation_0/
        │   ├── algorithm_0.json
        │   ├── algorithm_1.json
        │   └── ...
        ├── generation_1/
        └── ...
```

---

## 📊 ARCHIVOS GENERADOS

### 1. `best_algorithm.json`
**Mejor algoritmo encontrado durante la evolución**

```json
{
  "algorithm_id": "gen_45_pop_3",
  "generation": 45,
  "fitness": 12.5,
  "structure": {
    "type": "Seq",
    "children": [
      {
        "type": "GreedyConstruct",
        "operator": "GreedyDSATUR"
      },
      {
        "type": "While",
        "condition": "no_improvement",
        "max_iterations": 100,
        "body": [
          {
            "type": "LocalSearch",
            "operator": "KempeChain"
          },
          {
            "type": "Perturbation",
            "operator": "RandomRecolor",
            "strength": 0.3
          }
        ]
      }
    ]
  },
  "pseudocode": "...",
  "performance": {
    "avg_colors": 12.5,
    "std_colors": 1.2,
    "feasible_rate": 0.95,
    "avg_time": 15.3
  }
}
```

### 2. `evolution_history.json`
**Historial completo de la evolución**

```json
{
  "metadata": {
    "timestamp": "31-12-25_22-40-00",
    "pop_size": 10,
    "generations": 50,
    "seed": 42,
    "training_instances": 5
  },
  "generations": [
    {
      "generation": 0,
      "population": [
        {
          "algorithm_id": "gen_0_pop_0",
          "fitness": 15.2,
          "structure": {...}
        },
        ...
      ],
      "best_fitness": 15.2,
      "avg_fitness": 16.8,
      "worst_fitness": 18.5
    },
    ...
  ],
  "best_algorithm_generation": 45,
  "best_fitness_history": [15.2, 14.8, 14.5, ..., 12.5]
}
```

### 3. `population_stats.json`
**Estadísticas de la población por generación**

```json
{
  "generation_stats": [
    {
      "generation": 0,
      "best_fitness": 15.2,
      "avg_fitness": 16.8,
      "worst_fitness": 18.5,
      "std_fitness": 1.2,
      "diversity": 0.85
    },
    ...
  ],
  "overall_stats": {
    "total_generations": 50,
    "best_fitness_overall": 12.5,
    "improvement_rate": 0.18,
    "convergence_generation": 45
  }
}
```

### 4. `summary.txt`
**Resumen legible de la ejecución**

```
RESUMEN DE EVOLUCIÓN GAA
================================================================================

CONFIGURACIÓN:
Población: 10 algoritmos
Generaciones: 50
Instancias de entrenamiento: 5
Semilla: 42

RESULTADOS:
Mejor fitness encontrado: 12.5
Generación de convergencia: 45
Mejora total: 17.8%

MEJOR ALGORITMO:
ID: gen_45_pop_3
Estructura: Seq(GreedyDSATUR, While(KempeChain, RandomRecolor))
Desempeño promedio: 12.5 colores (±1.2)
Tasa de factibilidad: 95%

ESTADÍSTICAS DE POBLACIÓN:
Fitness inicial promedio: 16.8
Fitness final promedio: 13.2
Desviación estándar final: 0.8
Diversidad final: 0.45

================================================================================
```

### 5. `timing_report.txt` y `timing_report.json`
**Tiempos de ejecución por etapa**

```
TIEMPOS DE EJECUCIÓN
================================================================================

Carga de instancias:        2.3s    (0.1%)
Generación inicial:         5.2s    (0.3%)
Evolución (50 gen):      1450.8s   (98.2%)
Evaluación final:           8.5s    (0.6%)
Guardado de resultados:     3.2s    (0.2%)

Tiempo total: 24.76m (1470.0s)

================================================================================
```

### 6. `convergence_plot.png`
**Gráfica de convergencia de fitness**

Muestra:
- Mejor fitness por generación
- Fitness promedio por generación
- Banda de desviación estándar

---

## 🎯 TIPOS DE OUTPUTS

| Archivo | Tipo | Contenido |
|---------|------|----------|
| `best_algorithm.json` | JSON | Mejor algoritmo encontrado |
| `evolution_history.json` | JSON | Historial completo de evolución |
| `population_stats.json` | JSON | Estadísticas por generación |
| `summary.txt` | TXT | Resumen legible |
| `timing_report.txt` | TXT | Tiempos de ejecución |
| `timing_report.json` | JSON | Tiempos en formato JSON |
| `convergence_plot.png` | PNG | Gráfica de convergencia |
| `algorithm_*.json` | JSON | Algoritmos individuales por generación |

---

## 📈 INFORMACIÓN CAPTURADA

### Por Algoritmo:
- ID único
- Generación y posición en población
- Fitness (desempeño)
- Estructura AST completa
- Pseudocódigo
- Estadísticas de desempeño

### Por Generación:
- Mejor fitness
- Fitness promedio
- Peor fitness
- Desviación estándar
- Diversidad de población

### Por Evolución:
- Configuración (pop_size, generations, seed)
- Instancias de entrenamiento
- Historial de mejora
- Generación de convergencia
- Tiempos de ejecución

---

## 🚀 CÓMO USAR

### Ejecutar evolución GAA:
```bash
python scripts/gaa_experiment.py --pop-size 10 --generations 50
```

### Outputs generados automáticamente:
```
output/gaa/{timestamp}/
├── best_algorithm.json
├── evolution_history.json
├── population_stats.json
├── summary.txt
├── timing_report.txt
├── timing_report.json
├── convergence_plot.png
└── algorithms/
    ├── generation_0/
    ├── generation_1/
    └── ...
```

---

## ✅ CONCLUSIÓN

Todos los outputs de GAA están centralizados en `output/gaa/` con estructura clara y documentada:
- ✅ Mejor algoritmo guardado
- ✅ Historial completo de evolución
- ✅ Estadísticas por generación
- ✅ Tiempos de ejecución
- ✅ Gráficas de convergencia
- ✅ Algoritmos individuales archivados

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Estructura de output GAA documentada
