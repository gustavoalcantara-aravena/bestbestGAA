# GAP Calculation - Quick Summary

**Cálculo automático de brecha respecto a Best Known Solutions**

---

## La Fórmula

```
gap_percent = ((d_final - d_bks) / d_bks) × 100%
```

| Componente | Significado | Ejemplo |
|-----------|-----------|---------|
| `d_final` | Distancia encontrada por algoritmo | 1670.5 km |
| `d_bks` | Mejor solución conocida (BKS) | 1650.8 km |
| `gap_percent` | Brecha en % | 1.19% |

---

## ¿Cuándo Se Calcula?

**Solo si:** `k_final == k_bks` (mismo número de vehículos)

```
GRASP:
  ├─ k_final = 19, k_bks = 19 ✅ → Calcular GAP
  └─ GAP = 2.22%

VND:
  ├─ k_final = 21, k_bks = 19 ❌ → NO calcular GAP
  └─ Reportar: delta_K = +2
```

---

## Flujo en Experimento

```
1. CARGAR BKS
   └─ bks.json → {"R1/R101": {"K": 19, "D": 1650.8}, ...}

2. EJECUTAR ALGORITMO
   └─ GRASP.solve() → k_final=19, d_final=1670.5

3. BUSCAR BKS
   └─ bks_data["R1/R101"] → k_bks=19, d_bks=1650.8

4. CALCULAR GAP
   ├─ Alcanzó K? 19 == 19 → SÍ ✅
   ├─ delta_K = 0
   ├─ gap_distance = 1670.5 - 1650.8 = 19.7 km
   └─ gap_percent = (19.7/1650.8)*100 = 1.19%

5. GUARDAR EN CSV
   └─ raw_results.csv con 36 resultados (12×3)
```

---

## Ejemplos de Salida

### Caso 1: Óptimo

```
algorithm | instance | k_final | d_final | k_bks | d_bks | gap_percent
GRASP     | R101     | 19      | 1650.8  | 19    | 1650.8| 0.00%       ✅
```

### Caso 2: Subóptimo

```
algorithm | instance | k_final | d_final | k_bks | d_bks | gap_percent
VND       | R101     | 19      | 1670.5  | 19    | 1650.8| 1.19%       ⚠️
```

### Caso 3: Peor (K diferente)

```
algorithm | instance | k_final | d_final | k_bks | d_bks | delta_K | gap_percent
GRASP     | R101     | 21      | 1580.0  | 19    | 1650.8| +2      | NULL        ❌
```

---

## Estadísticas por Algoritmo

Después de 36 ejecuciones (QUICK):

```
GRASP:     GAP promedio = 2.34%, alcanzó BKS en 83.3% (10/12)
VND:       GAP promedio = 0.89%, alcanzó BKS en 91.7% (11/12)
ILS:       GAP promedio = 0.12%, alcanzó BKS en 100%  (12/12)
```

---

## Interpretación

| GAP % | Significado | Evaluación |
|-------|-----------|------------|
| 0.00% | Solución óptima | ⭐⭐⭐⭐⭐ |
| <0.5% | Excelente | ⭐⭐⭐⭐ |
| 0.5-1.5% | Muy buena | ⭐⭐⭐ |
| 1.5-3% | Buena | ⭐⭐ |
| >3% | Aceptable | ⭐ |

---

## Archivos Involucrados

```
datasets/
└─ bks.json                    ← Mejor soluciones conocidas

scripts/
└─ experiments.py
   ├─ _load_bks()             ← Carga BKS
   ├─ add_result()            ← Busca BKS + calcula GAP
   └─ save_raw_results()      ← Guarda CSV con GAP

output/
├─ raw_results.csv            ← Con columnas de GAP
└─ plots/
   ├─ gap_distribution.png
   ├─ gap_by_family.png
   └─ gap_vs_time.png
```

---

## Columnas en raw_results.csv

```
algorithm | instance | k_final | d_final | k_bks | d_bks | delta_K | reached_K_BKS | gap_distance | gap_percent | time_sec | status
──────────┼──────────┼─────────┼─────────┼───────┼───────┼─────────┼───────────────┼──────────────┼─────────────┼──────────┼────────
GRASP     | R101     | 19      | 1670.5  | 19    | 1650.8| 0       | True          | 19.7         | 1.19        | 2.34     | success
```

---

**¿Preguntas?**
- **Detalle completo:** Ver [CALCULO_GAP_DETALLADO.md](CALCULO_GAP_DETALLADO.md)
- **Flujos GAA:** Ver [FLUJOS_EJECUCION_GAA_DETALLADO.md](FLUJOS_EJECUCION_GAA_DETALLADO.md)
- **Referencia rápida:** Ver [QUICK_REFERENCE_GAA.md](QUICK_REFERENCE_GAA.md)
