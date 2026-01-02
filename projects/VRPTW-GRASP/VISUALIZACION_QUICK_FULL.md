# 📊 Visualización: Arquitectura QUICK vs FULL - VRPTW-GRASP

## Comparativa Visual: KBP-SA vs VRPTW-GRASP

### KBP-SA Architecture (Original)

```
┌─────────────────────────────────────────────────────────────┐
│ demo_experimentation_both.py (1 script único)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─── FASE 1: Generar Algoritmos (1 vez) ────┐              │
│ │ 3 algoritmos KBP con seed=42              │              │
│ │ Tiempo: ~0.00s                            │              │
│ └────────────────────────────────────────────┘              │
│                    ↓                                         │
│ ┌─── FASE 2: Grupo 1 (LOW-DIM) ──────────────┐             │
│ │ 10 instancias × 3 algoritmos × 1 rep       │             │
│ │ = 30 experimentos                          │             │
│ │ Tiempo: ~17 segundos                       │             │
│ │ Output: plots_low_dimensional_*/           │             │
│ └────────────────────────────────────────────┘             │
│                    ↓                                         │
│ ┌─── FASE 3: Grupo 2 (LARGE-SCALE) ──────────┐            │
│ │ 21 instancias × 3 algoritmos × 1 rep       │             │
│ │ = 63 experimentos                          │             │
│ │ Tiempo: ~17 segundos                       │             │
│ │ Output: plots_large_scale_*/               │             │
│ └────────────────────────────────────────────┘             │
│                    ↓                                         │
│ ┌─── SALIDA FINAL ─────────────────────────────┐            │
│ │ Experimentos totales: 93                   │             │
│ │ Tiempo total: ~34 segundos                 │             │
│ │ Archivos: ~45 PNG + 2 JSON + 2 MD         │             │
│ └────────────────────────────────────────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Características:
✓ Ejecución SECUENCIAL fija (ambos grupos siempre)
✓ Usuario NO elige: corre bajo/grande automáticamente
✓ Presupuesto: ~34 segundos siempre
✗ No flexible para validación rápida
```

---

### VRPTW-GRASP Architecture (Nueva)

```
┌──────────────────────────────────────────────────────────────────┐
│ OPCIÓN A: demo_experimentation_quick.py (Script 1: RÁPIDO)       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ┌─ FASE 1: Generar Algoritmos (1 vez, si no existen) ─┐         │
│ │ 3 algoritmos GRASP con seed=42                       │         │
│ │ Tiempo: ~0.00s                                       │         │
│ └──────────────────────────────────────────────────────┘         │
│                    ↓                                              │
│ ┌─ FASE 2: Ejecutar QUICK Test ──────────────────────┐          │
│ │ Familia: R1 (Random 1)                             │          │
│ │ 12 instancias × 3 algoritmos × 1 rep               │          │
│ │ = 36 experimentos                                  │          │
│ │ Tiempo: 5-10 minutos                               │          │
│ │ Output: plots_vrptw_QUICK_YYYYMMDD_*/              │          │
│ │ • gap_comparison_boxplot.png                       │          │
│ │ • gap_comparison_bars.png                          │          │
│ │ • quality_vs_time_scatter.png                      │          │
│ │ • convergence_curves.png                           │          │
│ │ • vehicles_used_comparison.png                     │          │
│ │ • routes_detailed_R101.png ... R112.png (12)       │          │
│ │ • README.md + time_tracking.md                     │          │
│ └──────────────────────────────────────────────────────┘         │
│                                                                   │
│ ✅ Uso: Validación rápida, debugging, estimación tiempos        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

FLUJO: python scripts/demo_experimentation_quick.py

```

```
┌──────────────────────────────────────────────────────────────────┐
│ OPCIÓN B: demo_experimentation_full.py (Script 2: EXHAUSTIVO)    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ┌─ FASE 1: Generar Algoritmos (reutilizar de QUICK) ──┐         │
│ │ 3 algoritmos GRASP seed=42 (mismos que QUICK)       │         │
│ │ Tiempo: ~0.00s                                      │         │
│ └─────────────────────────────────────────────────────┘         │
│                    ↓                                              │
│ ┌─ FASE 2: Ejecutar FULL Test (6 subfamilias) ────────────────┐ │
│ │                                                              │ │
│ │ Familia R (Random):                                        │ │
│ │  • R1: 12 instancias × 3 alg = 36 experimentos           │ │
│ │  • R2: 11 instancias × 3 alg = 33 experimentos           │ │
│ │  ├─ Subtotal R: 69 experimentos                          │ │
│ │                                                              │ │
│ │ Familia C (Clustered):                                     │ │
│ │  • C1:  9 instancias × 3 alg = 27 experimentos           │ │
│ │  • C2:  8 instancias × 3 alg = 24 experimentos           │ │
│ │  ├─ Subtotal C: 51 experimentos                          │ │
│ │                                                              │ │
│ │ Familia RC (Random+Clustered):                            │ │
│ │  • RC1: 8 instancias × 3 alg = 24 experimentos           │ │
│ │  • RC2: 8 instancias × 3 alg = 24 experimentos           │ │
│ │  ├─ Subtotal RC: 48 experimentos                         │ │
│ │                                                              │ │
│ │ TOTAL: 56 instancias × 3 algoritmos × 1 rep = 168 exp     │ │
│ │ Tiempo: 40-60 minutos                                      │ │
│ │                                                              │ │
│ │ Output: plots_vrptw_FULL_YYYYMMDD_*/                      │ │
│ │ • gap_comparison_boxplot.png                             │ │
│ │ • gap_comparison_bars.png                                │ │
│ │ • quality_vs_time_scatter.png                            │ │
│ │ • convergence_curves.png                                 │ │
│ │ • vehicles_used_comparison.png                           │ │
│ │ • performance_by_family.png         ← NUEVO              │ │
│ │ • performance_by_size.png           ← NUEVO              │ │
│ │ • best_algorithm_per_family.png     ← NUEVO              │ │
│ │ • family_R_statistics.md            ← NUEVO              │ │
│ │ • family_C_statistics.md            ← NUEVO              │ │
│ │ • family_RC_statistics.md           ← NUEVO              │ │
│ │ • routes_detailed_R101.png ... RC208.png (56 total)      │ │
│ │ • statistics_summary.md                                  │ │
│ │ • README.md + time_tracking.md                           │ │
│ │                                                              │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                                   │
│ ✅ Uso: Análisis exhaustivo, paper, decisiones estratégicas     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

FLUJO: python scripts/demo_experimentation_full.py

```

---

## Características QUICK vs FULL

### Dimensiones Clave

```
                        QUICK           FULL
────────────────────────────────────────────────────
Familias               1 (R1)          6 (R1+R2+C1+C2+RC1+RC2)
Instancias            12              56
Experimentos          36              168
Tiempo                5-10 min         40-60 min
Archivos salida       ~20             ~70

Propósito          VALIDACIÓN      ANÁLISIS EXHAUSTIVO
Uso                Debugging       Publicación
Especial análisis  NO              SÍ (por familia)
```

---

## Matriz de Decisión: ¿QUICK o FULL?

```
Situación                               → QUICK  │ FULL
──────────────────────────────────────────────────┼──────
Primera ejecución                       →  ✅    │ Después
Cambiar código/parámetros               →  ✅    │ NO
Debugging rápido                        →  ✅    │ NO
Estimación de tiempos                   →  ✅    │ NO
Análisis estadístico robusto            →  ❌    │  ✅
Comparación entre familias              →  ❌    │  ✅
Especialización de algoritmos           →  ❌    │  ✅
Paper/publicación                       →  ❌    │  ✅
Presupuesto <15 minutos                 →  ✅    │ NO
Presupuesto >45 minutos                 →  ✅    │  ✅
```

---

## Flujo de Ejecución Recomendado

```
PRIMERA VEZ (Setup):
│
├─ python scripts/demo_experimentation_quick.py
│  │
│  ├─ Genera 3 algoritmos (seed=42)
│  ├─ Ejecuta 36 experimentos (R1)
│  ├─ Crea 20 archivos
│  ├─ Tiempo: 5-10 minutos
│  │
│  ├─ ✓ Sin errores?
│  │  │
│  │  └─ SÍ → Continuar con FULL
│  │     NO → Debuggear
│  │
│  └─ Salida: output/plots_vrptw_QUICK_*/
│
├─ python scripts/demo_experimentation_full.py
│  │
│  ├─ Reutiliza 3 algoritmos de QUICK
│  ├─ Ejecuta 168 experimentos (todas familias)
│  ├─ Crea 70 archivos
│  │  - 6 gráficas estadísticas globales
│  │  - 3 gráficas análisis por familia (NUEVO)
│  │  - 56 gráficas rutas (1 por instancia)
│  │  - 3 archivos estadísticas por familia
│  ├─ Tiempo: 40-60 minutos
│  │
│  └─ Salida: output/plots_vrptw_FULL_*/
│
└─ Análisis de Resultados
   │
   ├─ Abrir: performance_by_family.png
   ├─ Abrir: statistics_summary.md
   ├─ Comparar gap entre R, C, RC
   ├─ Identificar especialización
   └─ Tomar decisiones sobre algoritmos
```

---

## Comparativa de Salidas

### QUICK Output (~20 archivos)

```
plots_vrptw_QUICK_20260101_120000/
├── Gráficas Estadísticas (8):
│   ├── gap_comparison_boxplot.png
│   ├── gap_comparison_bars.png
│   ├── quality_vs_time_scatter.png
│   ├── convergence_curves.png
│   ├── vehicles_used_comparison.png
│   ├── best_algorithm_ast.png
│   └── README.md + time_tracking.md
│
├── Gráficas de Rutas (12):
│   ├── routes_detailed_R101.png
│   ├── routes_detailed_R102.png
│   └── ... (12 total, 1 por instancia R1)
│
└── Algoritmos:
    ├── GAA_Algorithm_1.json
    ├── GAA_Algorithm_2.json
    ├── GAA_Algorithm_3.json
    └── algorithms_pseudocode.md
```

### FULL Output (~70 archivos)

```
plots_vrptw_FULL_20260101_120000/
├── Gráficas Estadísticas Globales (8):
│   ├── gap_comparison_boxplot.png
│   ├── gap_comparison_bars.png
│   ├── quality_vs_time_scatter.png
│   ├── convergence_curves.png
│   ├── vehicles_used_comparison.png
│   ├── best_algorithm_ast.png
│   └── README.md + time_tracking.md
│
├── Análisis por Familia (6):       ← ÚNICO DE FULL
│   ├── performance_by_family.png
│   ├── performance_by_size.png
│   ├── best_algorithm_per_family.png
│   ├── family_R_statistics.md  (R1+R2)
│   ├── family_C_statistics.md  (C1+C2)
│   └── family_RC_statistics.md (RC1+RC2)
│
├── Gráficas de Rutas (56):
│   ├── routes_detailed_R101.png
│   ├── ... (12 para R1)
│   ├── routes_detailed_R201.png
│   ├── ... (11 para R2)
│   ├── routes_detailed_C101.png
│   ├── ... (9 para C1)
│   ├── routes_detailed_C201.png
│   ├── ... (8 para C2)
│   ├── routes_detailed_RC101.png
│   ├── ... (8 para RC1)
│   ├── routes_detailed_RC201.png
│   └── ... (8 para RC2)
│
├── Resumen:
│   ├── statistics_summary.md (tabla 56 instancias)
│   └── README.md
│
└── Algoritmos:
    ├── GAA_Algorithm_1.json  (reutilizado)
    ├── GAA_Algorithm_2.json
    ├── GAA_Algorithm_3.json
    └── algorithms_pseudocode.md
```

---

## Parámetros Configurables

### QUICK Script

```python
# Defaults
families=['R1'],                    # Solo R1
num_algorithms=3,
max_iterations_grasp=100,
timeout_per_instance=60.0,
random_seed=42,
verbose=True,

# Opcionales
limit=None,                         # Limitador de instancias
generate_visualizations=True,
```

### FULL Script

```python
# Defaults
families=['R1', 'R2', 'C1', 'C2', 'RC1', 'RC2'],  # TODAS
num_algorithms=3,
max_iterations_grasp=100,
timeout_per_instance=60.0,
random_seed=42,
verbose=True,

# Adicionales FULL
aggregate_by_family=True,           # Análisis por familia
compare_families=True,              # Comparación entre familias
save_solutions=False,               # Guardar soluciones
```

---

## Línea de Tiempo Típica

```
Tiempo      Evento                              Script
──────────────────────────────────────────────────────
T+0s        Inicio QUICK                        quick.py
T+5-10m     Generación 3 algoritmos             (seed=42)
T+5-10m     Ejecución 36 experimentos (R1)      12×3
T+5-10m     Generación 20 archivos              plots/
T+10-15m    Usuario revisa QUICK results        ✓
T+15m       Inicio FULL (sin regenerar algs)    full.py
T+15m       Ejecución 168 experimentos          56×3
T+15m       + 40-50 min de cálculo              (40-60m est)
T+55-65m    Generación 70 archivos              plots/
T+55-65m    Análisis por familia                family_*.md
T+65m       Usuario revisa FULL results         ✓

TIEMPO TOTAL AMBOS: 65 minutos
QUICKE ONLY: 15 minutos
```

---

## 🎯 Conclusión Visual

**VRPTW-GRASP implementa arquitectura flexible de experimentación**:

```
┌─────────────────────────────────────────────────────┐
│ Usuario elige:                                      │
│                                                     │
│ ✓ Validación rápida (5-10 min)   → QUICK script   │
│   Debugging, estimación, testing                   │
│                                                     │
│ ✓ Análisis exhaustivo (40-60 min) → FULL script   │
│   Comparación familias, paper, decisiones          │
│                                                     │
│ ✓ Ambos secuencialmente (65 min) → Corre QUICK   │
│   Luego FULL                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Diferencia clave respecto a KBP-SA "both"**:
- KBP-SA: Ejecución fija 1 script (siempre 93 experimentos ~34s)
- VRPTW-GRASP: Flexible 2 scripts (36 o 168 experimentos, usuario decide)

---

**Documento generado**: 1 de Enero de 2026  
**Versión**: 1.0  
**Formato**: Visualización ASCII
