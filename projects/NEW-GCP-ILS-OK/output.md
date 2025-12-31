# Output y Almacenamiento de Resultados - NEW-GCP-ILS-OK

## 📋 Resumen

Después de **cada ejecución**, todos los resultados se guardan automáticamente en la carpeta `output/` con **timestamp único** (DD-MM-YY_HH-MM-SS) para evitar sobrescrituras.

---

## 📁 Estructura de carpetas

```
output/
├── results/
│   ├── all_datasets/              ← Ejecución COMPLETA (todos 79 datasets)
│   │   └── 31-12-25_14-35-42/     ← Timestamp: DD-MM-YY_HH-MM-SS
│   │       ├── summary.csv
│   │       ├── detailed_results.json
│   │       └── statistics.txt
│   │
│   └── specific_datasets/         ← Ejecución ESPECÍFICA (una familia)
│       ├── CUL/
│       │   └── 31-12-25_14-35-42/
│       ├── DSJ/
│       │   └── 31-12-25_14-35-42/
│       ├── LEI/
│       │   └── 31-12-25_14-35-42/
│       ├── MYC/
│       │   └── 31-12-25_14-35-42/
│       ├── REG/
│       │   └── 31-12-25_14-35-42/
│       ├── SCH/
│       │   └── 31-12-25_14-35-42/
│       └── SGB/
│           └── 31-12-25_14-35-42/
│
├── solutions/                      ← Archivos de solución
│   └── DSJC125_31-12-25_14-35-42.sol
│
└── logs/                          ← Logs de ejecución
    └── execution_31-12-25_14-35-42.log
```

---

## 🔍 Formato del Timestamp: DD-MM-YY_HH-MM-SS

```
31-12-25_14-35-42
DD MM YY HH MM SS
│  │  │  │  │  └─ SS: Segundo (00-59)
│  │  │  │  └───── MM: Minuto (00-59)
│  │  │  └────── HH: Hora (00-23)
│  │  └──────── YY: Año (25 = 2025)
│  └──────────── MM: Mes (01-12)
└───────────────── DD: Día (01-31)
```

**Ejemplo**: `31-12-25_14-35-42` = 31 diciembre 2025 a las 14:35:42 horas

---

## 🎯 DOS MODOS DE EJECUCIÓN

### ✅ MODO 1: ALL (Todos los datasets)

Ejecuta el framework sobre **todos los 79 datasets DIMACS**.

```bash
python scripts/experiment.py --mode all
```

**Resultado en**:
```
output/results/all_datasets/31-12-25_14-35-42/
├── summary.csv              # Tabla con 79 instancias
├── detailed_results.json    # Resultados detallados
└── statistics.txt           # Reporte formateado
```

**Datasets procesados**: CUL (6) + DSJ (15) + LEI (12) + MYC (6) + REG (14) + SCH (2) + SGB (24) = **79 instancias**

---

### ✅ MODO 2: SPECIFIC (Dataset específico)

Ejecuta sobre **una familia particular** de datasets.

```bash
python scripts/experiment.py --mode specific --dataset DSJ
```

**Familias disponibles**:
- `CUL` → 6 instancias (Color University of Leeds)
- `DSJ` → 15 instancias (David S. Johnson)
- `LEI` → 12 instancias (Leighton)
- `MYC` → 6 instancias (Mycielski)
- `REG` → 14 instancias (Regular)
- `SCH` → 2 instancias (School)
- `SGB` → 24 instancias (Stanford GraphBase)

**Ejemplo - Ejecutar solo DSJ**:
```bash
python scripts/experiment.py --mode specific --dataset DSJ
```

**Resultado en**:
```
output/results/specific_datasets/DSJ/31-12-25_14-35-42/
├── summary.csv              # Tabla con 15 instancias de DSJ
├── detailed_results.json    # Resultados detallados
└── statistics.txt           # Reporte formateado
```

---

## 📊 Contenido de archivos (igual para ambos modos)

### 1️⃣ summary.csv
Tabla rápida e importable

```csv
Instance,Dataset,Vertices,Edges,BKS,Colors,Feasible,Gap,Time(s)
DSJC125.col,DSJ,125,736,45,48,True,+3,12.5
myciel3.col,MYC,11,20,4,4,True,0,0.5
CUL_100.col,CUL,100,850,5,7,True,+2,8.3
```

### 2️⃣ detailed_results.json
Información completa (máquina-legible)

- Configuración del algoritmo
- Resultados detallados por instancia
- Historial iteración a iteración
- Estadísticas agregadas

### 3️⃣ statistics.txt
Reporte legible para humanos

```
═══════════════════════════════════════════════════════════════
                   NEW-GCP-ILS-OK - REPORT
═══════════════════════════════════════════════════════════════
Execution: all_datasets_31-12-25_14-35-42
Dataset Type: ALL (79 instances)
Total Time: 945.3 seconds

Total Instances:  79
Feasible:         79/79 (100%)
Average Time:     11.96 seconds
Average Colors:   22.4
Average Gap:      +1.8 colors

Best:   myciel3.col - 4 colors (optimal)
Worst:  DSJC500.col - 185 colors (gap +5)
═══════════════════════════════════════════════════════════════
```

---

## 💾 Archivos adicionales

### 🔹 Soluciones (.sol)
```
output/solutions/DSJC125_31-12-25_14-35-42.sol
output/solutions/myciel3_31-12-25_14-35-42.sol
```

Contiene: Asignación de colores vértice por vértice

### 🔹 Logs (.log)
```
output/logs/execution_31-12-25_14-35-42.log
```

Contiene: Progreso detallado de la ejecución

---

## ✨ Ejemplo completo

### Paso 1: Ejecutar (modo ALL)
```bash
python scripts/experiment.py --mode all
```

### Paso 2: Se genera automáticamente
```
output/
├── results/all_datasets/31-12-25_14-35-42/
│   ├── summary.csv
│   ├── detailed_results.json
│   └── statistics.txt
├── solutions/
│   ├── DSJC125_31-12-25_14-35-42.sol
│   ├── CUL_100_31-12-25_14-35-42.sol
│   └── ... (más 77 soluciones)
└── logs/
    └── execution_31-12-25_14-35-42.log
```

### Paso 3: Revisar resultados
```bash
# Ver resumen
cat output/results/all_datasets/31-12-25_14-35-42/summary.csv

# Ver reporte
cat output/results/all_datasets/31-12-25_14-35-42/statistics.txt

# Analizar con Python
import pandas as pd
df = pd.read_csv("output/results/all_datasets/31-12-25_14-35-42/summary.csv")
print(df.sort_values('Gap'))
```

---

## ✅ Verificación

Después de cada ejecución confirma que:

- ✓ Carpeta `output/results/` existe
- ✓ Subcarpeta con timestamp correcto (DD-MM-YY_HH-MM-SS)
- ✓ 3 archivos (CSV, JSON, TXT)
- ✓ Archivos .sol en `solutions/`
- ✓ Log en `logs/`
- ✓ **Sin sobrescritura** (cada ejecución = carpeta nueva)

---

## 📝 Resumen

| Aspecto | Detalle |
|---------|---------|
| **Ubicación** | `output/` |
| **Carpeta** | `all_datasets/` o `specific_datasets/[FAMILIA]/` |
| **Subcarpeta** | Nombre del timestamp (DD-MM-YY_HH-MM-SS) |
| **Archivos** | summary.csv, detailed_results.json, statistics.txt |
| **Formato fecha-hora** | DD-MM-YY_HH-MM-SS (ej: 31-12-25_14-35-42) |
| **Sobrescritura** | **NO** - cada ejecución crea carpeta nueva |
| **Tamaño** | ~50-100 MB por ejecución completa |
