# 📁 ESTRUCTURA COMPLETA DE OUTPUT

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025

---

## 📋 ESTRUCTURA DE DIRECTORIOS

Toda la salida del proyecto se organiza en la carpeta `output/` con la siguiente estructura:

```
output/
├── results/                          # Resultados de ejecuciones (CSV, JSON, TXT, SOL)
│   ├── all_datasets/                 # Experimentos con todos los datasets
│   │   └── 31-12-25_21-46-59/        # Timestamp de la sesión
│   │       ├── summary.csv           # Tabla resumen
│   │       ├── detailed_results.json # Resultados detallados
│   │       ├── statistics.txt        # Reporte estadístico
│   │       ├── timing_report.txt     # Tiempos por etapa
│   │       ├── timing_report.json    # Tiempos en JSON
│   │       └── *.sol                 # Archivos de soluciones
│   │
│   └── specific_datasets/            # Experimentos con familia específica
│       └── DSJ/                      # Familia (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
│           └── 31-12-25_21-46-59/
│               ├── summary.csv
│               ├── detailed_results.json
│               ├── statistics.txt
│               ├── timing_report.txt
│               ├── timing_report.json
│               └── *.sol
│
├── plots/                            # TODAS LAS GRÁFICAS VAN AQUÍ
│   ├── all_datasets/                 # Gráficas de experimentos completos
│   │   └── 31-12-25_21-46-59/
│   │       ├── convergence_plot.png
│   │       ├── scalability_plot.png
│   │       ├── boxplot_robustness.png
│   │       ├── conflict_heatmap.png
│   │       └── time_quality_tradeoff.png
│   │
│   └── specific_datasets/            # Gráficas de familia específica
│       └── DSJ/
│           └── 31-12-25_21-46-59/
│               ├── convergence_plot.png
│               ├── scalability_plot.png
│               └── ...
│
├── solutions/                        # Archivos .sol (también en results/)
│   └── *.sol
│
└── logs/                             # Archivos de log
    └── experiment_*.log
```

---

## 🎯 DÓNDE VA CADA TIPO DE ARCHIVO

### 📊 Resultados Numéricos
```
output/results/{mode}/{timestamp}/
├── summary.csv              ← Tabla resumen
├── detailed_results.json    ← Datos JSON detallados
├── statistics.txt           ← Reporte estadístico
├── timing_report.txt        ← Tiempos por etapa
└── timing_report.json       ← Tiempos en JSON
```

### 📈 Visualizaciones (GRÁFICAS)
```
output/plots/{mode}/{timestamp}/
├── convergence_plot.png         ← Convergencia de ILS
├── scalability_plot.png         ← Escalabilidad (tiempo vs tamaño)
├── boxplot_robustness.png       ← Robustez (múltiples ejecuciones)
├── conflict_heatmap.png         ← Matriz de conflictos
└── time_quality_tradeoff.png    ← Tiempo vs Calidad
```

### 📄 Soluciones
```
output/results/{mode}/{timestamp}/
└── {instance_name}_{timestamp}.sol

output/solutions/
└── {instance_name}_{timestamp}.sol
```

### 📋 Logs
```
output/logs/
└── experiment_{timestamp}.log
```

---

## 🔄 MODOS DE EJECUCIÓN

### Modo: all_datasets
```
output/results/all_datasets/31-12-25_21-46-59/
output/plots/all_datasets/31-12-25_21-46-59/
```

### Modo: specific_datasets (familia DSJ)
```
output/results/specific_datasets/DSJ/31-12-25_21-46-59/
output/plots/specific_datasets/DSJ/31-12-25_21-46-59/
```

---

## 📊 TIPOS DE ARCHIVOS GENERADOS

### 1. CSV (Tabular)
**Ubicación**: `output/results/{mode}/{timestamp}/summary.csv`

```csv
Instance,Family,Vertices,Edges,BKS,Colors,Conflicts,Feasible,Time,Gap
myciel3,MYC,11,20,4,4,0,True,0.01s,0.0%
myciel4,MYC,23,71,5,5,0,True,0.03s,0.0%
DSJC125.1,DSJ,125,736,5,6,12,False,12.30s,+20.0%
```

### 2. JSON (Estructurado)
**Ubicación**: `output/results/{mode}/{timestamp}/detailed_results.json`

```json
{
  "metadata": {
    "timestamp": "31-12-25_21-46-59",
    "mode": "all_datasets",
    "total_instances": 79,
    "total_time": 1252.81,
    "num_replicas": 1
  },
  "results": [
    {
      "instance": "myciel3",
      "vertices": 11,
      "edges": 20,
      "colors": 4,
      "conflicts": 0,
      "feasible": true,
      "time": 0.01,
      "gap": 0.0
    }
  ],
  "statistics": {
    "total_instances": 79,
    "total_feasible": 75,
    "avg_colors": 12.5,
    "std_colors": 3.2
  }
}
```

### 3. TXT (Legible)
**Ubicación**: `output/results/{mode}/{timestamp}/statistics.txt`

```
REPORTE ESTADÍSTICO
================================================================================

RESUMEN GENERAL:
Instancias procesadas: 79
Tiempo total: 20.88m (1252.81s)
Instancias factibles: 75/79 (94.9%)

ESTADÍSTICAS:
Colores promedio: 12.5 ± 3.2
Tiempo promedio: 15.8s
Gap promedio: +2.3%

DESGLOSE POR INSTANCIA:
...
```

### 4. PNG (Gráficas)
**Ubicación**: `output/plots/{mode}/{timestamp}/`

- `convergence_plot.png` - Convergencia de ILS
- `scalability_plot.png` - Escalabilidad
- `boxplot_robustness.png` - Robustez
- `conflict_heatmap.png` - Conflictos
- `time_quality_tradeoff.png` - Tiempo vs Calidad

### 5. SOL (Soluciones)
**Ubicación**: `output/results/{mode}/{timestamp}/` y `output/solutions/`

```
myciel3_31-12-25_21-46-59.sol
myciel4_31-12-25_21-46-59.sol
DSJC125.1_31-12-25_21-46-59.sol
...
```

### 6. LOG (Logs)
**Ubicación**: `output/logs/`

```
experiment_31-12-25_21-46-59.log
```

---

## 🎨 VISUALIZACIONES DISPONIBLES

### 1. Convergence Plot
- **Archivo**: `convergence_plot.png`
- **Ubicación**: `output/plots/{mode}/{timestamp}/`
- **Descripción**: Muestra cómo converge el algoritmo ILS
- **Eje X**: Iteraciones
- **Eje Y**: Número de colores

### 2. Scalability Plot
- **Archivo**: `scalability_plot.png`
- **Ubicación**: `output/plots/{mode}/{timestamp}/`
- **Descripción**: Tiempo vs tamaño del problema
- **Eje X**: Número de vértices
- **Eje Y**: Tiempo de ejecución

### 3. Robustness Boxplot
- **Archivo**: `boxplot_robustness.png`
- **Ubicación**: `output/plots/{mode}/{timestamp}/`
- **Descripción**: Variabilidad entre réplicas
- **Muestra**: Min, Q1, Mediana, Q3, Max

### 4. Conflict Heatmap
- **Archivo**: `conflict_heatmap.png`
- **Ubicación**: `output/plots/{mode}/{timestamp}/`
- **Descripción**: Matriz de conflictos entre vértices
- **Colores**: Intensidad de conflictos

### 5. Time-Quality Tradeoff
- **Archivo**: `time_quality_tradeoff.png`
- **Ubicación**: `output/plots/{mode}/{timestamp}/`
- **Descripción**: Relación tiempo vs calidad
- **Eje X**: Tiempo
- **Eje Y**: Calidad (colores)

---

## 📝 TIMING REPORT

### timing_report.txt
```
REPORTE DE TIEMPOS DE EJECUCIÓN
================================================================================

RESUMEN GENERAL:
Tiempo total: 20.88m (1252.81s)

DESGLOSE POR ETAPA:
Etapa                          Tiempo               % Total
Ejecución de ILS               20.75m (1245.3s)      98.2%
Guardado de resultados         3.21s                  0.3%
Generación de gráficas         1.85s                  0.1%
Carga de datasets              2.45s                  0.2%
```

### timing_report.json
```json
{
  "total_time_seconds": 1252.81,
  "total_time_formatted": "20.88m (1252.81s)",
  "stages": {
    "Carga de datasets": {
      "seconds": 2.45,
      "formatted": "2.45s",
      "percentage": 0.2
    },
    "Ejecución de ILS": {
      "seconds": 1245.3,
      "formatted": "20.75m (1245.3s)",
      "percentage": 98.2
    },
    ...
  }
}
```

---

## 🚀 CÓMO USAR

### Ejecutar experimento completo
```bash
python scripts/run_full_experiment.py --mode all
```

**Genera**:
- `output/results/all_datasets/{timestamp}/` - Resultados
- `output/plots/all_datasets/{timestamp}/` - Gráficas

### Ejecutar familia específica
```bash
python scripts/run_full_experiment.py --mode family --family DSJ
```

**Genera**:
- `output/results/specific_datasets/DSJ/{timestamp}/` - Resultados
- `output/plots/specific_datasets/DSJ/{timestamp}/` - Gráficas

### Test rápido
```bash
python scripts/test_experiment_quick.py
```

**Genera**:
- `output/results/all_datasets/{timestamp}/` - Resultados
- Archivos: CSV, JSON, TXT

---

## 📊 RESUMEN DE ARCHIVOS

| Tipo | Ubicación | Cantidad | Formato |
|------|-----------|----------|---------|
| CSV | `output/results/` | 1 | Tabular |
| JSON | `output/results/` | 2 | Estructurado |
| TXT | `output/results/` | 2 | Texto |
| PNG | `output/plots/` | 5 | Imagen |
| SOL | `output/results/` + `output/solutions/` | 79 | Solución |
| LOG | `output/logs/` | 1 | Log |

---

## ✅ CONCLUSIÓN

**Toda la salida está centralizada en `output/`**:
- ✅ Resultados numéricos → `output/results/`
- ✅ Gráficas → `output/plots/`
- ✅ Soluciones → `output/solutions/` + `output/results/`
- ✅ Logs → `output/logs/`

**Estructura clara y organizada por timestamp y modo de ejecución.**

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Estructura de output completamente documentada
