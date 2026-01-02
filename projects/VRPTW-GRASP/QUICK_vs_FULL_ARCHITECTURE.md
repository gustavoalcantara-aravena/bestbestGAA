# Estructura de Experimentación: QUICK vs FULL

**Fecha**: 1 de Enero de 2026  
**Proyecto**: VRPTW-GRASP  
**Basado en**: KBP-SA architecture adaptada para Solomon instances  
**Modificación clave**: De "both" (2 grupos) → "quick" + "full" (1 familia vs 6 subfamilias)

---

## 📊 Comparativa: KBP-SA vs VRPTW-GRASP

### KBP-SA Approach (Original)

```
1 Script: demo_experimentation_both.py
├── Grupo 1: LOW-DIMENSIONAL (10 instancias)
│   └─ 10 × 3 algoritmos × 1 rep = 30 experimentos
├── Grupo 2: LARGE-SCALE (21 instancias)
│   └─ 21 × 3 algoritmos × 1 rep = 63 experimentos
└─ TOTAL: 93 experimentos (~40 segundos)
```

**Estructura fija**: Siempre ejecuta ambos grupos secuencialmente.  
**Datos**: 2 carpetas (low_dimensional/ + large_scale/)

---

### VRPTW-GRASP Approach (Nuevo)

```
2 Scripts: demo_experimentation_quick.py + demo_experimentation_full.py

Script 1: QUICK Test
├── Familia: R1 solamente (12 instancias)
│   └─ 12 × 3 algoritmos × 1 rep = 36 experimentos (~5-10 min)
└─ Propósito: Validación rápida del sistema

Script 2: FULL Test
├── Familia R1: 12 instancias × 3 = 36 experimentos
├── Familia R2: 11 instancias × 3 = 33 experimentos
├── Familia C1:  9 instancias × 3 = 27 experimentos
├── Familia C2:  8 instancias × 3 = 24 experimentos
├── Familia RC1: 8 instancias × 3 = 24 experimentos
├── Familia RC2: 8 instancias × 3 = 24 experimentos
└─ TOTAL: 168 experimentos (~40-60 min)
   Propósito: Análisis exhaustivo + especialización por familia
```

**Estructura flexible**: Usuario elige ejecutar quick, full, o custom.  
**Datos**: 6 carpetas en datasets/ (R1/, R2/, C1/, C2/, RC1/, RC2/)

---

## 🗂️ Estructura de Datasets

### Carpeta datasets/

```
datasets/
├── R1/              ← Instancias Random 1
│   ├── R101.csv     (25 clientes)
│   ├── R102.csv     (25 clientes)
│   ├── ...
│   └── R112.csv     (100 clientes)
│   └─ Total: 12 instancias
│
├── R2/              ← Instancias Random 2 (período de tiempo diferente)
│   ├── R201.csv
│   ├── ...
│   └── R211.csv
│   └─ Total: 11 instancias
│
├── C1/              ← Instancias Clustered 1
│   ├── C101.csv
│   ├── ...
│   └── C109.csv
│   └─ Total: 9 instancias
│
├── C2/              ← Instancias Clustered 2 (período diferente)
│   ├── C201.csv
│   ├── ...
│   └── C208.csv
│   └─ Total: 8 instancias
│
├── RC1/             ← Instancias Random+Clustered 1
│   ├── RC101.csv
│   ├── ...
│   └── RC108.csv
│   └─ Total: 8 instancias
│
├── RC2/             ← Instancias Random+Clustered 2 (período diferente)
│   ├── RC201.csv
│   ├── ...
│   └── RC208.csv
│   └─ Total: 8 instancias
│
└── documentation/   ← Documentación de datasets
    └── *.md files
```

### Características por Familia Solomon

| Familia | Patrón Espacial | Ventanas Tiempo | Clientes | Aplicación |
|---------|---|---|---|----|
| **R** | Aleatorio | Largas (periodo T) | 25-100 | Distribución sin estructura |
| **C** | Clustered | Largas (periodo T) | 25-100 | Centros urbanos definidos |
| **RC** | Mixto | Largas (periodo T) | 25-100 | Mezcla realista (aglomerados + dispersos) |

**Subfamilias**:
- **Subfamilia 1** (R1, C1, RC1): Período de tiempo normal (T)
- **Subfamilia 2** (R2, C2, RC2): Período de tiempo extendido (2T o 3T)

---

## ⚙️ Script 1: demo_experimentation_quick.py

### Propósito
Validación rápida del sistema GAA antes de experimento exhaustivo.

### Parámetros
```python
# Defaults
QUICK_CONFIG = {
    'families': ['R1'],              # Solo R1 (12 instancias)
    'num_algorithms': 3,              # Generar 3 algoritmos
    'max_iterations_grasp': 100,      # Iteraciones por algoritmo
    'timeout_per_instance': 60.0,     # Timeout
    'random_seed': 42,                # Reproducibilidad
    'verbose': True,                  # Mostrar progreso
}
```

### Ejecución
```bash
# Modo por defecto (usa R1)
python scripts/demo_experimentation_quick.py

# Especificar otra familia para testing
python scripts/demo_experimentation_quick.py --family C1

# Con límite de instancias (para debugging)
python scripts/demo_experimentation_quick.py --family R1 --limit 5
```

### Matriz de Experimentos
```
┌──────────────────────────────┐
│ Familia R1:                  │
│ 12 instancias × 3 alg × 1   │
│ = 36 experimentos            │
├──────────────────────────────┤
│ Tiempo: ~5-10 minutos        │
│ Archivos salida: ~20         │
└──────────────────────────────┘
```

### Salidas
```
output/vrptw_experiments_QUICK_20260101_120000/
├── experiment_quick_20260101_120000.json        (36 resultados)
└── plots_vrptw_QUICK_20260101_120000/
    ├── gap_comparison_boxplot.png
    ├── gap_comparison_bars.png
    ├── quality_vs_time_scatter.png
    ├── convergence_curves.png
    ├── vehicles_used_comparison.png
    ├── best_algorithm_ast.png
    ├── routes_detailed_R101.png
    ├── ... (12 gráficas rutas, 1 por instancia)
    ├── README.md
    ├── time_tracking.md
    └── algorithms/
        ├── GAA_Algorithm_1.json
        ├── GAA_Algorithm_2.json
        ├── GAA_Algorithm_3.json
        └── algorithms_pseudocode.md
```

### Verificación
```bash
# Contar experimentos completados
$dir = Get-ChildItem "output\vrptw_experiments_QUICK_*" -Directory | Select-Object -First 1
$results = Get-Content "$($dir.FullName)\experiment_quick_*.json" | ConvertFrom-Json
$results.Count  # Should be 36
```

---

## ⚙️ Script 2: demo_experimentation_full.py

### Propósito
Análisis exhaustivo de desempeño en todas las familias Solomon.  
Identificar especialización, robustez, y escalabilidad de algoritmos.

### Parámetros
```python
# Defaults
FULL_CONFIG = {
    'families': ['R1', 'R2', 'C1', 'C2', 'RC1', 'RC2'],  # TODAS
    'num_algorithms': 3,              # Reutilizar mismos 3
    'max_iterations_grasp': 100,
    'timeout_per_instance': 60.0,
    'random_seed': 42,
    'verbose': True,
    'aggregate_by_family': True,      # Análisis separado R/C/RC
    'compare_families': True,         # Comparación entre familias
}
```

### Ejecución
```bash
# Modo completo (todas las familias)
python scripts/demo_experimentation_full.py

# Subset de familias (para testing)
python scripts/demo_experimentation_full.py --families R1 C1 RC1

# Con almacenamiento de soluciones
python scripts/demo_experimentation_full.py --save-solutions
```

### Matriz de Experimentos
```
┌─────────────────────────────────────────┐
│ Familia R1:  12 × 3 = 36 experimentos   │
│ Familia R2:  11 × 3 = 33 experimentos   │
│ Familia C1:   9 × 3 = 27 experimentos   │
│ Familia C2:   8 × 3 = 24 experimentos   │
│ Familia RC1:  8 × 3 = 24 experimentos   │
│ Familia RC2:  8 × 3 = 24 experimentos   │
├─────────────────────────────────────────┤
│ TOTAL: 56 × 3 = 168 experimentos        │
│ Tiempo: ~40-60 minutos                  │
│ Archivos salida: ~70                    │
└─────────────────────────────────────────┘
```

### Salidas
```
output/vrptw_experiments_FULL_20260101_120000/
├── experiment_full_20260101_120000.json        (168 resultados)
└── plots_vrptw_FULL_20260101_120000/
    ├── ─── GRÁFICAS GLOBALES ───
    ├── gap_comparison_boxplot.png
    ├── gap_comparison_bars.png
    ├── quality_vs_time_scatter.png
    ├── convergence_curves.png
    ├── vehicles_used_comparison.png
    ├── best_algorithm_ast.png
    │
    ├── ─── ANÁLISIS POR FAMILIA ───
    ├── performance_by_family.png           (¿Qué familia es más difícil?)
    ├── performance_by_size.png             (¿Cómo escalan?)
    ├── best_algorithm_per_family.png       (¿Quién domina en R vs C vs RC?)
    │
    ├── ─── ESTADÍSTICAS POR FAMILIA ───
    ├── family_R_statistics.md              (R1 + R2 agregados)
    ├── family_C_statistics.md              (C1 + C2 agregados)
    ├── family_RC_statistics.md             (RC1 + RC2 agregados)
    │
    ├── ─── GRÁFICAS DE RUTAS (56 TOTAL) ───
    ├── routes_detailed_R101.png
    ├── ... (12 para R1)
    ├── routes_detailed_R201.png
    ├── ... (11 para R2)
    ├── routes_detailed_C101.png
    ├── ... (9 para C1)
    ├── routes_detailed_C201.png
    ├── ... (8 para C2)
    ├── routes_detailed_RC101.png
    ├── ... (8 para RC1)
    ├── routes_detailed_RC201.png
    ├── ... (8 para RC2)
    │
    ├── README.md                           (Resumen análisis)
    ├── time_tracking.md                    (Tiempos por familia)
    ├── statistics_summary.md               (Tabla global 56 instancias)
    └── algorithms/                         (Mismos 3 algoritmos de QUICK)
        ├── GAA_Algorithm_1.json
        ├── GAA_Algorithm_2.json
        ├── GAA_Algorithm_3.json
        └── algorithms_pseudocode.md
```

### Verificación
```bash
# Contar experimentos completados
$dir = Get-ChildItem "output\vrptw_experiments_FULL_*" -Directory | Select-Object -First 1
$results = Get-Content "$($dir.FullName)\experiment_full_*.json" | ConvertFrom-Json
$results.Count  # Should be 168
```

---

## 🔄 Flujo de Ejecución Recomendado

### Primera Ejecución (Completa)

```
PASO 1: Validación
$ python scripts/demo_experimentation_quick.py
  ✓ Genera 3 algoritmos (seed=42)
  ✓ Ejecuta 36 experimentos (R1, 12 instancias)
  ✓ Crea 20 archivos de salida
  ⏱️ Tiempo: 5-10 minutos
  
  → Verificar que no haya errores
  → Revisar archivos en output/plots_vrptw_QUICK_*/

PASO 2: Análisis Exhaustivo
$ python scripts/demo_experimentation_full.py
  ✓ Reutiliza los 3 algoritmos de QUICK
  ✓ Ejecuta 168 experimentos (todas familias)
  ✓ Crea 70 archivos de salida
  ✓ Incluye análisis por familia
  ⏱️ Tiempo: 40-60 minutos
  
  → Esperar a completación
  → Revisar archivos en output/plots_vrptw_FULL_*/

PASO 3: Análisis de Resultados
$ cd output/plots_vrptw_FULL_*/
- Abrir performance_by_family.png
- Abrir statistics_summary.md
- Comparar gap entre R, C, RC
- Verificar especialización de algoritmos
```

### Ejecución Iterativa (Debugging)

```
Si hay problemas en QUICK:
$ python scripts/demo_experimentation_quick.py --family R1 --limit 3
  → Ejecuta solo 3 instancias (9 experimentos)
  → Muy rápido para debugging
  → NO ejecutar FULL hasta que QUICK funcione

Si necesitas solo una familia en FULL:
$ python scripts/demo_experimentation_full.py --families R1 C1
  → Ejecuta solo R1 y C1
  → 21 instancias, 63 experimentos
  → Tiempo: ~10-15 minutos
```

---

## 📊 Comparativa de Resultados Esperados

### QUICK Test (Modo Rápido)

**Inputs**: 12 instancias (R1)  
**Outputs**: 36 experimentos × 3 algoritmos

```
Ejemplo de reporte QUICK:
┌────────────────────────────────────┐
│ Family: R (Random)                 │
│ Instancias: R101 - R112 (12 total) │
├────────────────────────────────────┤
│ GAA_Algorithm_1: Gap 6.2% ± 1.3%   │
│ GAA_Algorithm_2: Gap 5.8% ± 1.1%   │
│ GAA_Algorithm_3: Gap 6.5% ± 1.4%   │
└────────────────────────────────────┘
```

**Uso**: Validación de sistema antes de experimento largo.

---

### FULL Test (Análisis Exhaustivo)

**Inputs**: 56 instancias (R1+R2+C1+C2+RC1+RC2)  
**Outputs**: 168 experimentos × 3 algoritmos + análisis por familia

```
Ejemplo de reporte FULL:
┌────────────────────────────────────────────────────────────┐
│ Global Results:                                            │
│ Best Algorithm: GAA_Algorithm_2 (gap 5.9% all families)   │
├────────────────────────────────────────────────────────────┤
│ By Family:                                                 │
│ • R (Random, 23 inst):    GAA_Alg_2 best (6.2% gap)       │
│ • C (Clustered, 17 inst): GAA_Alg_1 best (4.1% gap)       │
│ • RC (Mixed, 16 inst):    GAA_Alg_3 best (6.8% gap)       │
├────────────────────────────────────────────────────────────┤
│ Insights:                                                  │
│ - Especialización clara por familia                        │
│ - C (clustered) es más fácil (gap menor)                   │
│ - R (random) es más difícil                                │
│ - Combinación de algoritmos podría mejorar               │
└────────────────────────────────────────────────────────────┘
```

**Uso**: Análisis exhaustivo, publicación, toma de decisiones.

---

## 🎯 Decisión: ¿Cuándo usar QUICK vs FULL?

| Situación | Usar QUICK | Usar FULL |
|-----------|-----------|-----------|
| Primera ejecución | ✅ SÍ | Después |
| Debugging de código | ✅ SÍ | NO |
| Testing de parámetros | ✅ SÍ | Después OK |
| Análisis estadístico | NO | ✅ SÍ |
| Comparación familias | NO | ✅ SÍ |
| Paper/publicación | NO | ✅ SÍ |
| Presupuesto tiempo limitado | ✅ SÍ | NO |
| Presupuesto tiempo suficiente | Opcional | ✅ SÍ |

---

## 📝 Notas Importantes

1. **Reproducibilidad**: Ambos scripts usan `seed=42` → mismos 3 algoritmos generados
2. **Reutilización**: FULL reutiliza los algoritmos generados en QUICK
3. **Independencia**: Scripts pueden ejecutarse independientemente (ej: solo FULL)
4. **Escalabilidad**: Estructura permite agregar más familias sin cambiar código
5. **Análisis**: FULL proporciona análisis por familia que QUICK no incluye

---

**Estado**: ✅ Arquitectura QUICK vs FULL completamente especificada  
**Próxima fase**: Implementación de ambos scripts
