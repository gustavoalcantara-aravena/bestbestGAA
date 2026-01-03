# 🚀 CÓMO EJECUTAR - RESUMEN RÁPIDO

## 📊 El Código Actual

Existe un **framework de experimentos** en `scripts/experiments.py` con:

### **Código General = 2 Modos Predefinidos + 1 Personalizable**

```
┌─────────────────────────────────────────────────────┐
│          CÓDIGO GENERAL (experiments.py)            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  QuickExperiment.run()                              │
│  └─ 1 familia (R1) × 12 instancias × 3 algos       │
│     = 36 experimentos en 2-5 minutos                │
│                                                     │
│  FullExperiment.run()                               │
│  └─ 6 familias × 56 instancias × 3 algos           │
│     = 168 experimentos en 15-25 minutos             │
│                                                     │
│  ExperimentExecutor (personalizable)                │
│  └─ Cualquier configuración de familias             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 TRES FORMAS DE EJECUTAR

### **OPCIÓN 1️⃣: RÁPIDO (2-5 min)** ⚡ ← RECOMENDADO

```bash
python script_quick.py
```

Qué hace:
- 1 familia (R1)
- 12 instancias
- 3 algoritmos
- **36 experimentos totales**

✅ Perfecto para probar que todo funciona

---

### **OPCIÓN 2️⃣: PERSONALIZADO (2-5 min)** 🎨

```bash
# Abre script_custom.py, edita esta línea:
FAMILIA_A_USAR = 'C1'  # Cambia a C1, C2, R1, R2, RC1, o RC2

python script_custom.py
```

Qué hace:
- **TÚ ELIGES la familia**: C1, C2, R1, R2, RC1, RC2
- 8-12 instancias (depende de familia)
- 3 algoritmos
- **24-36 experimentos totales**

✅ Perfecto para testear una familia específica

| Familia | Instancias | Tipo | Ejemplo |
|---------|-----------|------|---------|
| C1 | 9 | Clustered | Clientes en grupos |
| C2 | 8 | Clustered | Clientes en grupos, ventanas largas |
| R1 | 12 | Random | Clientes dispersos |
| R2 | 11 | Random | Clientes dispersos, ventanas largas |
| RC1 | 8 | Mezcla | 50% clustered, 50% random |
| RC2 | 8 | Mezcla | 50% clustered, 50% random, ventanas largas |

---

### **OPCIÓN 3️⃣: COMPLETO (15-25 min)** 🔬

```bash
python script_full.py
```

Qué hace:
- Todas 6 familias
- 56 instancias
- 3 algoritmos
- **168 experimentos totales**

✅ Perfecto para investigación/papers

---

## 📋 COMPARACIÓN RÁPIDA

| Aspecto | QUICK | CUSTOM (1 familia) | FULL (todas) |
|---------|-------|-------------------|--------------|
| **Script** | `script_quick.py` | `script_custom.py` | `script_full.py` |
| **Familias** | 1 | 1 | 6 |
| **Instancias** | 12 | 8-12 | 56 |
| **Algoritmos** | 3 | 3 | 3 |
| **Total experimentos** | 36 | 24-36 | 168 |
| **Tiempo** | 2-5 min | 2-5 min | 15-25 min |
| **Uso típico** | Testing | Debug | Investigación |

---

## 🏃 QUICKSTART (30 segundos)

### **Paso 1: Ejecuta QUICK**
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python script_quick.py
```

**Resultado**: 36 experimentos en 2-5 minutos

### **Paso 2: Mira los resultados**
```bash
# Abre esto en Excel o Python:
output/vrptw_experiments_QUICK_*/results/raw_results.csv
```

**Verás**: Columnas K_final, D_final, total_time_sec, etc.

### **Paso 3: (Opcional) Prueba CUSTOM**
```bash
# Edita script_custom.py, línea 19:
FAMILIA_A_USAR = 'C1'  # Cambia esta línea

python script_custom.py
```

---

## 🔧 PERSONALIZACIÓN AVANZADA

### Ejecutar SOLO 1 familia Y 1 algoritmo (ultra-rápido)

```python
# En script_quick.py, reemplaza la ejecución con:

from scripts.experiments import ExperimentExecutor, ExperimentConfig, AlgorithmGenerator

# Genera algoritmos
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(num_algorithms=1)  # ← Solo 1

# Configuración mini
config = ExperimentConfig(
    mode='MICRO',
    families=['R1'],          # ← Una familia
    algorithms=algorithms,    # ← Un algoritmo
    repetitions=1,
    seed=42
)

executor = ExperimentExecutor(config)
# ... (completar como en script_custom.py)
# Total: 12 experimentos = 30 segundos
```

---

## 📊 QUÉ VERÁS COMO SALIDA

### Estructura de carpetas creada:
```
output/
└── vrptw_experiments_QUICK_02-01-26_14-30-45/
    ├── results/
    │   ├── raw_results.csv          ← LOS DATOS PRINCIPALES
    │   └── experiment_metadata.json
    ├── plots/                       ← (para después)
    └── logs/                        ← (para después)
```

### Contenido de `raw_results.csv`:
```
algorithm_id,instance_id,family,K_final,K_BKS,D_final,D_BKS,gap_percent,total_time_sec,reached_K_BKS
GAA_Algorithm_1,R101,R1,11,10,1650.5,1645.3,0.31,5.2,False
GAA_Algorithm_1,R102,R1,10,10,1460.2,1460.2,0.0,4.8,True
...
```

---

## 💡 ENTENDER LAS COLUMNAS

| Columna | Significado | Ejemplo |
|---------|------------|---------|
| `algorithm_id` | Qué algoritmo | GAA_Algorithm_1 |
| `instance_id` | Qué instancia | R101 |
| `family` | Familia Solomon | R1, C1, etc. |
| `K_final` | Rutas encontradas | 11 |
| `K_BKS` | Mejor conocido | 10 |
| `D_final` | Distancia encontrada | 1650.5 km |
| `D_BKS` | Mejor distancia conocida | 1645.3 km |
| `gap_percent` | % por encima de BKS | 0.31% |
| `total_time_sec` | Tiempo de cálculo | 5.2 segundos |
| `reached_K_BKS` | ¿Encontró solución óptima? | True/False |

---

## 🎓 CONCEPTOS CLAVE

### **Qué es cada familia?**

**C1/C2** (Clustered):
- Clientes agrupados en clusters
- Más fácil de resolver
- Típicamente 10-14 rutas necesarias

**R1/R2** (Random):
- Clientes distribuidos aleatoriamente
- Más difícil que clustered
- Típicamente 18-25 rutas necesarias

**RC1/RC2** (Random + Clustered):
- Mezcla de ambos
- Dificultad intermedia
- Típicamente 14-18 rutas necesarias

**C1 vs C2, R1 vs R2, RC1 vs RC2**:
- Versión "1": Ventanas de tiempo estrictas
- Versión "2": Ventanas de tiempo relajadas

---

## ⚡ CASOS DE USO

### **Caso 1: "Quiero testear rápido"**
```bash
python script_quick.py  # 2-5 minutos
```

### **Caso 2: "Quiero probar solo con clustered"**
```bash
# Edita script_custom.py:
FAMILIA_A_USAR = 'C1'
python script_custom.py
```

### **Caso 3: "Quiero ver rendimiento en random"**
```bash
# Edita script_custom.py:
FAMILIA_A_USAR = 'R1'
python script_custom.py
```

### **Caso 4: "Quiero datos para un paper"**
```bash
python script_full.py  # 168 experimentos, todas las familias
```

### **Caso 5: "Quiero uber-rápido (30 seg)"**
Ver sección "PERSONALIZACIÓN AVANZADA" arriba

---

## 🔍 DESPUÉS DE EJECUTAR

Tienes dos archivos importantes:

### **1. raw_results.csv**
```python
import pandas as pd

df = pd.read_csv('output/.../results/raw_results.csv')

# Ver promedio de rutas encontradas
print(df['K_final'].mean())  # Ej: 11.2

# Ver % que alcanzaron BKS
bks_pct = df['reached_K_BKS'].mean()
print(f"{bks_pct*100:.1f}% alcanzaron solución óptima")

# Ver gap de distancia
print(df['gap_percent'].mean())  # Ej: 0.45%

# Por familia
print(df.groupby('family')['reached_K_BKS'].mean())
```

### **2. experiment_metadata.json**
```json
{
  "experiment_id": "vrptw_experiments_QUICK_02-01-26_14-30-45",
  "mode": "QUICK",
  "families": ["R1"],
  "algorithms": ["GAA_Algorithm_1", "GAA_Algorithm_2", "GAA_Algorithm_3"],
  "total_experiments": 36,
  "seed": 42
}
```

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Dónde están los scripts?**
R: En `/projects/GAA-VRPTW-GRASP-2/` (3 archivos):
- `script_quick.py`
- `script_custom.py`
- `script_full.py`

**P: ¿Cuál debo usar primero?**
R: `script_quick.py` (es el más rápido para verificar que todo funciona)

**P: ¿Puedo cambiar parámetros?**
R: Sí, en `script_custom.py` puedes cambiar qué familia y cuántas repeticiones

**P: ¿Cuánto tiempo toma cada uno?**
R: QUICK=2-5 min, CUSTOM(1 fam)=2-5 min, FULL(todas)=15-25 min

**P: ¿Dónde aparecen los resultados?**
R: En la carpeta `output/` con timestamp, archivo CSV con todos los datos

**P: ¿Puedo paralelizar?**
R: No en el código actual, pero podrías usar ThreadPoolExecutor

---

## 📚 REFERENCIAS TÉCNICAS

- **Code**: `scripts/experiments.py` (líneas 1-330)
- **Doc**: `USAGE.md` (ejemplos completos)
- **Config**: `CONFIG_REFERENCE.md` (parámetros)
- **Guide**: `PERFORMANCE.md` (optimización)

---

**Versión**: 1.0 | **Fecha**: Enero 2, 2026 | **Estado**: Listo ✅
