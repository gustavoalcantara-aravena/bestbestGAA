# Estado Actual de Experimentos - ITER-4A/4B

**Fecha**: Enero 3, 2026  
**Hora**: 03:25 UTC  
**Estado**: EN PROGRESO

---

## 1. RESUMEN EJECUTIVO

✅ **ITER-4A y ITER-4B ya están implementados y activos**
- Algoritmo 1: Strength 2.0 → 3.5, TwoOpt reducido 52→40
- Algoritmo 2: CONTROL inmutable (D=1172.18, t=0.18s)  
- Algoritmo 3: Strength 1.0 → 3.0 (CRÍTICO), While 68→90

🔄 **FULL Experiment en ejecución**
- Timestamp: 2026-01-03T03:16:16
- Progreso: ~50% (84/168 esperado después de 8+ minutos)
- Estimado: Terminará en ~4 minutos más

---

## 2. AUTOMATIZACIÓN CONFIRMADA

### ✅ Gráficas GAP en QUICK (03:12:17)
- 01_gap_comparison_all_instances.png (215 KB)
- 02_gap_evolution_lines.png (502 KB)
- 03_gap_boxplot_by_family.png (134 KB)
- 04_gap_heatmap.png (263 KB)
- 05_gap_by_family_grid.png (254 KB)

**Encoding Fix**: Emoji ✅ → ASCII [MEJOR] en línea 337 de `plot_gap_comparison.py`

### ✅ Gráficas GAP en FULL (en progreso)
- Esperado: Mismo set de 5 gráficas al finalizar
- Ruta: `output/vrptw_experiments_FULL_03-01-26_03-16-16/plots/`

---

## 3. CONFIGURACIÓN ACTUAL (ITER-4A/4B)

### Algoritmo 1: GRASP Puro (OPTIMIZADO ITER-4A)
```
NearestNeighbor
  → While(80 iteraciones)  # +5: 75→80
     → TwoOpt(40)          # -23%: 52→40
     → OrOpt(18)           # -36%: 28→18
     → DoubleBridge(3.5)   # +75%: 2.0→3.5 ← KEY
     → TwoOpt(40)          # +25%: 32→40
     → Relocate(18)        # sin cambio
```

**Meta ITER-4A**: D 1391.51 → < 1240 (Δ -10%)

### Algoritmo 2: CONTROL (ITER-3 - INMUTABLE)
```
NearestNeighbor
  → While(80 iteraciones)
     → TwoOpt(50)
     → DoubleBridge(3)
     → TwoOpt(35)
     → Relocate(20)
```

**Baseline**: D=1172.18, t=0.18s, GAP=24.70% ← REFERENCIA

### Algoritmo 3: GRASP Adaptativo (OPTIMIZADO ITER-4B)
```
NearestNeighbor
  → While(90 iteraciones)   # +32%: 68→90
     → TwoOpt(50)           # sin cambio
     → OrOpt(12)            # -40%: 20→12
     → DoubleBridge(3.0)    # +200%: 1.0→3.0 ← CRÍTICO
     → TwoOpt(45)           # +29%: 35→45
     → Relocate(15)         # sin cambio
```

**Meta ITER-4B**: D 1504.34 → < 1250 (Δ -15%)

---

## 4. LÍNEA TEMPORAL DE EXPERIMENTOS

| Fecha | Hora | Modo | Algoritmos | Estado | Artefactos |
|-------|------|------|-----------|--------|-----------|
| 01-03 | 03:12 | QUICK | ITER-4 | ✅ Completado | 11 canonical + 5 gap plots |
| 01-03 | 03:16 | FULL | ITER-4 | 🔄 En progreso (50%) | Esperado: 11 + 5 plots |
| **PRÓXIMO** | TBD | QUICK | ITER-5+ | ⏳ Planificado | Análisis de resultados |
| **PRÓXIMO** | TBD | FULL | ITER-5+ | ⏳ Planificado | Decisión según ITER-4 |

---

## 5. MÉTRICAS ESPERADAS DESPUÉS DE FULL

### Benchmarks ITER-3 (baseline anterior)
```
Algoritmo 1:
  - Distancia: 1391.51 → ? (meta: < 1240)
  - Tiempo: 3.41s → ? (esperado: 3.6-4.0s)
  - GAP: 42.15% → ?

Algoritmo 2 (CONTROL):
  - Distancia: 1172.18 (SIN CAMBIO)
  - Tiempo: 0.18s (SIN CAMBIO)
  - GAP: 24.70% (SIN CAMBIO)

Algoritmo 3:
  - Distancia: 1504.34 → ? (meta: < 1250)
  - Tiempo: 0.69s → ? (esperado: 0.90-1.05s)
  - GAP: 52.31% → ?
```

### Criterios de éxito ITER-4
- ✅ Algo 1: GAP reduction > 10% O Distancia < 1280
- ✅ Algo 3: GAP reduction > 12% O Distancia < 1300
- ⚠️ Ambos: Tiempo < límite de máquina (< 5s para Algo1, < 1s para Algo3)

---

## 6. GIT STATUS

**Branch**: main  
**HEAD**: d1014a3 (Documentación: Verificación final de automatización)  
**Commits recientes**:
```
d1014a3 Documentación: Verificación final de automatización de gráficas GAP
400a1d6 Automatización: Generación de gráficas GAP en cada ejecución
41b53a3 Documentación: ITER-4A/4B implementación completa
9ac8e19 ITER-4B: Algoritmo 3 optimizado (strength 1.0→3.0, CRÍTICO)
41b53a3 ITER-4A: Algoritmo 1 optimizado (strength 2.0→3.5)
```

**No hay cambios pendientes en algorithm_generator.py**
- ITER-4A/4B ya están activos en código
- Listos para validación vía experimentos

---

## 7. PRÓXIMOS PASOS

### Fase 1: Validación ITER-4 (ACTUAL)
```
✅ 1. QUICK 03:12:17 completado con ITER-4
✅ 2. 5 gráficas GAP generadas automáticamente (encoding fix OK)
🔄 3. FULL 03:16:16 en progreso (~50%, termina en 3-4 min)
⏳ 4. Generar resumen comparativo ITER-3 vs ITER-4
⏳ 5. Decidir: ¿Proceder con ITER-5?
```

### Fase 2: Análisis Post-FULL
- Extraer CSV resultados desde `output/vrptw_experiments_FULL_03-01-26_03-16-16/results/raw_results.csv`
- Generar tabla comparativa vs ITER-3
- Evaluar si criterios de éxito se cumplen
- Documentar hallazgos en `ITER4_RESULTADOS.md`

### Fase 3: Decisión ITER-5 (Condicional)
**Si Algo1 mejora > 10%**:
- Considerar ITER-5A: Explorar strength > 3.5 para Algo1
- Buscar sweet spot tiempo vs distancia

**Si Algo3 mejora > 15%**:
- Considerar ITER-5B: Fine-tuning de While(90) a While(100)
- Optimizar distribución de operadores

**Si ambos < 5%**:
- ITER-4 fue ceiling de optimización con estructura actual
- Explorar constructores adaptativos (RandomizedInsertion para familias C)

---

## 8. ARTEFACTOS GENERADOS HOY

### QUICK (03-01-26_03-12-17)
```
output/vrptw_experiments_QUICK_03-01-26_03-12-17/
├── results/raw_results.csv (36 filas, 3 algos × 12 inst)
├── plots/
│   ├── 01-11_canonical_plots (11 PNG)
│   ├── 01_gap_comparison_all_instances.png ✅
│   ├── 02_gap_evolution_lines.png ✅
│   ├── 03_gap_boxplot_by_family.png ✅
│   ├── 04_gap_heatmap.png ✅
│   └── 05_gap_by_family_grid.png ✅
└── logs/...
```

### FULL (03-01-26_03-16-16) - EN PROGRESO
```
output/vrptw_experiments_FULL_03-01-26_03-16-16/
├── results/raw_results.csv (168 filas esperadas)
├── plots/
│   ├── 01-11_canonical_plots (11 PNG)
│   ├── 01_gap_comparison_all_instances.png (esperado)
│   ├── 02_gap_evolution_lines.png (esperado)
│   ├── 03_gap_boxplot_by_family.png (esperado)
│   ├── 04_gap_heatmap.png (esperado)
│   └── 05_gap_by_family_grid.png (esperado)
└── logs/...
```

---

## 9. OBSERVACIONES TÉCNICAS

### Encoding Fix Aplicado
- **Archivo**: `plot_gap_comparison.py`, línea 337
- **Cambio**: `print(f"  ✅ MEJOR: ...")` → `print(f"  [MEJOR] ...")`
- **Razón**: Windows cp1252 no soporta emoji U+2705
- **Status**: ✅ Validado en QUICK, esperando confirmación en FULL

### Automatización Activa
- **Trigger**: Al final de QUICK y FULL experiments
- **Proceso**: `scripts/experiments.py` llama `plot_gap_comparison.py` automáticamente
- **Detección CSV**: Dynamic - busca archivo más reciente en `output/*/results/`
- **Salida**: Plots guardados en carpeta del experimento actual
- **Status**: ✅ Funcionando como se esperaba

---

## 10. RESUMEN DE ESTADO

| Componente | Estado | Notas |
|------------|--------|-------|
| **ITER-4A (Algo1)** | 🔄 Validando | En FULL experiment 03:16 |
| **ITER-4B (Algo3)** | 🔄 Validando | En FULL experiment 03:16 |
| **Algo 2 (Control)** | ✅ Estable | Inmutable, sin cambios |
| **Automatización GAP** | ✅ Operativa | 5 gráficas generadas cada experimento |
| **Encoding** | ✅ Fijo | Emoji→ASCII, Windows compatible |
| **Git** | ✅ Limpio | Commits al día, ITER-4A/4B registrados |

**Conclusión**: Sistema ready for ITER-4 validation. FULL experiment está en progreso y debe terminar exitosamente con todas las gráficas GAP generadas automáticamente.

