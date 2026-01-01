# 📦 CONTENIDO DE LA CARPETA DE SESIÓN

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025

---

## 🎯 RESUMEN RÁPIDO

Cuando ejecutas:
```bash
python scripts/run_full_experiment.py --mode all
```

Se crea una carpeta con timestamp y se guardan **TODOS** estos archivos:

```
output/results/all_datasets/31-12-25_21-46-59/
├── summary.csv                    ← Tabla resumen (1 archivo)
├── detailed_results.json          ← Datos JSON (1 archivo)
├── statistics.txt                 ← Reporte estadístico (1 archivo)
├── timing_report.txt              ← Tiempos por etapa (1 archivo)
├── timing_report.json             ← Tiempos en JSON (1 archivo)
├── myciel3_31-12-25_21-46-59.sol  ← Solución 1
├── myciel4_31-12-25_21-46-59.sol  ← Solución 2
├── myciel5_31-12-25_21-46-59.sol  ← Solución 3
└── ... (79 archivos .sol en total)

output/plots/all_datasets/31-12-25_21-46-59/
├── convergence_plot.png           ← Gráfica de convergencia
├── scalability_plot.png           ← Gráfica de escalabilidad
├── boxplot_robustness.png         ← Boxplot de robustez
├── conflict_heatmap.png           ← Heatmap de conflictos
└── time_quality_tradeoff.png      ← Gráfica tiempo vs calidad
```

---

## 📊 ARCHIVOS EN `output/results/{timestamp}/`

### 1. `summary.csv`
**Tabla resumen de todas las instancias**

```csv
Instance,Family,Vertices,Edges,BKS,Colors,Conflicts,Feasible,Time,Gap
myciel3,MYC,11,20,4,4,0,True,0.01s,0.0%
myciel4,MYC,23,71,5,5,0,True,0.03s,0.0%
myciel5,MYC,47,236,6,6,0,True,0.45s,0.0%
DSJC125.1,DSJ,125,736,5,6,12,False,12.30s,+20.0%
DSJC125.5,DSJ,125,3891,17,18,5,False,45.20s,+5.9%
... (79 filas en total)
```

**Contenido**:
- Nombre de instancia
- Familia (MYC, DSJ, LEI, etc.)
- Número de vértices y aristas
- BKS (Best Known Solution)
- Colores encontrados
- Conflictos
- Si es factible (✓/✗)
- Tiempo de ejecución
- Gap respecto a BKS

---

### 2. `detailed_results.json`
**Datos estructurados en JSON**

```json
{
  "metadata": {
    "timestamp": "31-12-25_21-46-59",
    "mode": "all_datasets",
    "family": null,
    "total_instances": 79,
    "total_time": 1252.81,
    "num_replicas": 1
  },
  "results": [
    {
      "instance": "myciel3",
      "family": "MYC",
      "vertices": 11,
      "edges": 20,
      "colors": [4],
      "conflicts": [0],
      "feasible": [true],
      "times": [0.01],
      "gaps": [0.0],
      "best_colors": 4,
      "avg_colors": 4.0,
      "std_colors": 0.0,
      "avg_time": 0.01,
      "avg_gap": 0.0
    },
    {
      "instance": "myciel4",
      "family": "MYC",
      "vertices": 23,
      "edges": 71,
      "colors": [5],
      "conflicts": [0],
      "feasible": [true],
      "times": [0.03],
      "gaps": [0.0],
      "best_colors": 5,
      "avg_colors": 5.0,
      "std_colors": 0.0,
      "avg_time": 0.03,
      "avg_gap": 0.0
    },
    ... (79 instancias)
  ],
  "statistics": {
    "total_instances": 79,
    "total_feasible": 75,
    "avg_colors": 12.5,
    "std_colors": 3.2,
    "avg_time": 15.8,
    "avg_gap": 2.3
  }
}
```

**Contenido**:
- Metadatos (timestamp, modo, total de instancias)
- Resultados detallados de cada instancia
- Estadísticas generales

---

### 3. `statistics.txt`
**Reporte estadístico legible**

```
REPORTE ESTADÍSTICO
================================================================================

RESUMEN GENERAL:
Timestamp: 31-12-25_21-46-59
Modo: all_datasets
Instancias procesadas: 79
Tiempo total: 20.88m (1252.81s)
Tiempo promedio por instancia: 15.8s
Réplicas por instancia: 1

ESTADÍSTICAS GENERALES:
Instancias factibles: 75/79 (94.9%)
Colores promedio: 12.5 ± 3.2
Tiempo promedio: 15.8s ± 45.2s
Gap promedio: +2.3%

DESGLOSE POR FAMILIA:
MYC:  11 instancias, 11/11 factibles (100.0%)
DSJ:  15 instancias, 12/15 factibles (80.0%)
LEI:  10 instancias,  9/10 factibles (90.0%)
REG:  12 instancias, 11/12 factibles (91.7%)
SGB:  15 instancias, 15/15 factibles (100.0%)
SCH:   8 instancias,  8/8 factibles (100.0%)
CUL:   8 instancias,  9/8 factibles (100.0%)

RESULTADOS POR INSTANCIA:
Instance             Colors  Time      Gap
myciel3                  4  0.01s    0.0%
myciel4                  5  0.03s    0.0%
myciel5                  6  0.45s    0.0%
DSJC125.1                6  12.30s  +20.0%
DSJC125.5               18  45.20s   +5.9%
... (79 instancias)

================================================================================
```

---

### 4. `timing_report.txt`
**Tiempos de cada etapa**

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

================================================================================
```

---

### 5. `timing_report.json`
**Tiempos en formato JSON**

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
    "Guardado de resultados": {
      "seconds": 3.21,
      "formatted": "3.21s",
      "percentage": 0.3
    },
    "Generación de gráficas": {
      "seconds": 1.85,
      "formatted": "1.85s",
      "percentage": 0.1
    }
  }
}
```

---

### 6. Archivos `.sol` (79 archivos)
**Soluciones de cada instancia**

```
myciel3_31-12-25_21-46-59.sol
myciel4_31-12-25_21-46-59.sol
myciel5_31-12-25_21-46-59.sol
DSJC125.1_31-12-25_21-46-59.sol
DSJC125.5_31-12-25_21-46-59.sol
... (79 archivos en total)
```

**Formato**: Archivo de texto con asignación de colores por vértice
```
c 1 2
c 2 3
c 3 1
c 4 2
...
```

---

## 📈 ARCHIVOS EN `output/plots/{timestamp}/`

### 1. `convergence_plot.png`
**Gráfica de convergencia del algoritmo ILS**

```
Número de Colores
     ^
   10 |     ___
     |    /   \___
    8 |   /       \___
     |  /            \___
    6 | /                 \___
     |/                       \___
    4 |_____________________________
     +--+--+--+--+--+--+--+--+--+--+-> Iteraciones
     0  10 20 30 40 50 60 70 80 90 100
```

**Muestra**: Cómo converge el número de colores a lo largo de las iteraciones

---

### 2. `scalability_plot.png`
**Gráfica de escalabilidad (tiempo vs tamaño)**

```
Tiempo (s)
     ^
 300 |                          *
     |                       *
 200 |                    *
     |                 *
 100 |              *
     |           *
  50 |        *
     |     *
  10 |  *
     |*
   0 +--+--+--+--+--+--+--+--+--+--+-> Vértices
     0  100 200 300 400 500 600 700 800 900 1000
```

**Muestra**: Relación entre tamaño del problema y tiempo de ejecución

---

### 3. `boxplot_robustness.png`
**Boxplot de robustez (si hay múltiples réplicas)**

```
Colores
     ^
   10 |    +---+
     |    |   |
    8 |    | * |
     |    |   |
    6 |    +---+
     |
    4 |
     +--+--+--+--+--+--+--+--+--+--+
     myciel3  myciel4  myciel5  ...
```

**Muestra**: Variabilidad de resultados entre réplicas (min, Q1, mediana, Q3, max)

---

### 4. `conflict_heatmap.png`
**Heatmap de conflictos**

```
Matriz de conflictos entre vértices
Vértice
     ^
   10 |████░░░░░░
     |████░░░░░░
    8 |░░░░████░░
     |░░░░████░░
    6 |░░░░░░░░██
     |░░░░░░░░██
    4 |░░░░░░░░░░
     |░░░░░░░░░░
    2 |░░░░░░░░░░
     |░░░░░░░░░░
    0 +--+--+--+--+--+--+--+--+--+--+
     0  2  4  6  8 10 12 14 16 18 20
     Vértice
```

**Muestra**: Matriz de conflictos entre vértices (intensidad de color = número de conflictos)

---

### 5. `time_quality_tradeoff.png`
**Gráfica tiempo vs calidad**

```
Calidad (Colores)
     ^
   20 |                          *
     |                       *
   15 |                    *
     |                 *
   10 |              *
     |           *
    5 |        *
     |     *
    0 +--+--+--+--+--+--+--+--+--+--+-> Tiempo (s)
     0  10 20 30 40 50 60 70 80 90 100
```

**Muestra**: Relación entre tiempo de ejecución y calidad de la solución

---

## 📋 RESUMEN TOTAL DE ARCHIVOS

### En `output/results/{timestamp}/`:
- **1** archivo CSV
- **1** archivo JSON (detailed_results)
- **1** archivo TXT (statistics)
- **1** archivo TXT (timing_report)
- **1** archivo JSON (timing_report)
- **79** archivos SOL (soluciones)

**Total**: 84 archivos

### En `output/plots/{timestamp}/`:
- **5** archivos PNG (gráficas)

**Total**: 5 archivos

---

## 🎯 TAMAÑO APROXIMADO

| Tipo | Cantidad | Tamaño Aprox. |
|------|----------|---------------|
| CSV | 1 | 5-10 KB |
| JSON (results) | 1 | 50-100 KB |
| JSON (timing) | 1 | 2-5 KB |
| TXT (statistics) | 1 | 10-20 KB |
| TXT (timing) | 1 | 2-5 KB |
| SOL | 79 | 1-10 KB c/u |
| PNG | 5 | 100-500 KB c/u |

**Total aproximado**: 1-2 MB por sesión

---

## ✅ CONCLUSIÓN

Cada corrida genera:

✅ **5 archivos de datos** (CSV, JSON, TXT)  
✅ **79 archivos de soluciones** (SOL)  
✅ **5 gráficas** (PNG)  
✅ **Reporte de tiempos** (TXT + JSON)  

**Total: 89 archivos por sesión**

Todos organizados en:
- `output/results/{timestamp}/` - Datos y soluciones
- `output/plots/{timestamp}/` - Gráficas

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Contenido de carpeta completamente documentado
