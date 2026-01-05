# 📊 RESUMEN DE GAP - TODAS LAS FAMILIAS

**Fecha de Ejecución:** 2025-12-30  
**Total Instancias:** 55  
**Total Familias:** 6

---

## 📈 RESULTADOS CONSOLIDADOS

| Familia | Instancias | Con Referencia | Óptimas | GAP Promedio | Estado |
|---------|-----------|--------|---------|--------------|--------|
| **CUL** | 6 | 0/6 | 0 | N/A | ⚠️ Sin referencias |
| **DSJ** | 15 | 0/15 | 0 | N/A | 🔓 Problemas abiertos |
| **LEI** | 12 | 12/12 | 0 | -90.80% | 📋 Garantizadas |
| **MYC** | 6 | 5/6 | 0 | -84.08% | 📋 Óptimos conocidos |
| **REG** | 14 | 14/14 | 0 | -97.42% | 📋 Óptimos conocidos |
| **SCH** | 2 | 0/2 | 0 | N/A | 🔓 Problemas abiertos |
| **TOTAL** | **55** | **45/55** | **0** | **-91.83%*** | - |

*Promedio considerando solo familias con referencias

---

## 🎯 ANÁLISIS POR FAMILIA

### 1. **CUL** (6 instancias)
- **Estado:** ⚠️ Sin valores de referencia en BKS.json
- **Instancias:** flat1000_50_0, flat1000_60_0, flat1000_76_0, flat300_20_0, flat300_26_0, flat300_28_0
- **GAP:** N/A
- **Observación:** Las instancias no tienen referencias en el archivo BKS.json

### 2. **DSJ** (15 instancias)
- **Estado:** 🔓 Problemas abiertos (sin óptimo conocido)
- **Instancias:** DSJC125.1-9, DSJC250.1-9, DSJC500.1-9, DSJC1000.1-9, DSJR500.1, DSJR500.1c, DSJR500.5
- **GAP:** N/A (sin referencias)
- **Observación:** Todas las instancias están marcadas como DESCONOCIDO (problemas abiertos)

### 3. **LEI** (12 instancias) ✅
- **Estado:** 📋 ÓPTIMO (Garantizado)
- **Instancias:** le450_5a-5d, le450_15a-15d, le450_25a-25d
- **GAP Promedio:** **-90.80%**
- **Óptimas Encontradas:** 0/12
- **Detalle GAP:**
  - le450_5a-5d: -82.00% (referencia: 5)
  - le450_15a-15d: -94.00% (referencia: 15)
  - le450_25a-25d: -96.40% (referencia: 25)
- **Observación:** Todas las instancias tienen referencias garantizadas con límites teóricos

### 4. **MYC** (6 instancias) ✅
- **Estado:** 📋 ÓPTIMO
- **Instancias:** myciel2-7
- **GAP Promedio:** **-84.08%**
- **Óptimas Encontradas:** 0/6
- **Detalle GAP:**
  - myciel2: N/A (sin referencia)
  - myciel3: -77.50% (referencia: 4)
  - myciel4: -82.00% (referencia: 5)
  - myciel5: -85.00% (referencia: 6)
  - myciel6: -87.14% (referencia: 7)
  - myciel7: -88.75% (referencia: 8)

### 5. **REG** (14 instancias) ✅
- **Estado:** 📋 ÓPTIMO
- **Instancias:** fpsol2.i.1-3, inithx.i.1-3, mulsol.i.1-5, zeroin.i.1-3
- **GAP Promedio:** **-97.42%**
- **Óptimas Encontradas:** 0/14
- **Detalle GAP (por grupo):**
  - fpsol2: -97.50% (referencias: 65, 30, 30)
  - inithx: -97.51% (referencias: 54, 31, 31)
  - mulsol: -97.13% (referencias: 49, 31, 31, 31, 31)
  - zeroin: -97.42% (referencias: 49, 30, 30)

### 6. **SCH** (2 instancias)
- **Estado:** 🔓 Problemas abiertos
- **Instancias:** school1, school1_nsh
- **GAP:** N/A (sin referencias)
- **Observación:** Todas las instancias están marcadas como DESCONOCIDO

---

## 📊 ESTADÍSTICAS CLAVE

### Distribución de Instancias por Tipo de Referencia
- **Con Óptimo Conocido:** 45 instancias (81.8%)
- **Sin Referencia:** 10 instancias (18.2%)

### Distribución de Óptimos Garantizados
- **LEI:** 12 instancias con límites teóricos garantizados

### GAP Promedio General
- **LEI:** -90.80%
- **MYC:** -84.08%
- **REG:** -97.42%
- **Promedio Ponderado:** -91.83%

### Instancias Óptimas Encontradas
- **Total:** 0 de 45 instancias con referencia
- **Tasa de Optimalidad:** 0.0%

---

## 📁 ARCHIVOS GENERADOS

Cada familia cuenta con:
- ✅ **RESULTS.md** - Reporte detallado con tabla GAP
- ✅ **COMPARISON_GAP_ANALYSIS.json** - Datos de GAP en formato JSON
- ✅ **COMPARISON_GAP_ANALYSIS.csv** - Datos de GAP en formato CSV para Excel
- ✅ **convergence_analysis.png** - Gráficos de convergencia y análisis
- ✅ **analysis_report.json** - Reporte de análisis completo
- ✅ **analysis_report.csv** - Reporte de análisis en CSV
- ✅ **validation_report.json** - Reporte de validación
- ✅ **EXECUTIVE_SUMMARY.md** - Resumen ejecutivo

---

## 🔗 LOCALIZACIÓN DE ARCHIVOS

Todos los resultados se encuentran en:
```
output/
├── CUL_30_12_25_22_11/
├── DSJ_30_12_25_22_11/
├── LEI_30_12_25_22_11/
├── MYC_30_12_25_22_11/
├── REG_30_12_25_22_11/
└── SCH_30_12_25_22_11/
```

---

## 🎯 PRÓXIMOS PASOS

1. **Mejorar el algoritmo:** Aumentar iteraciones para acercarse al óptimo
2. **Analizar por familia:** Las familias REG y LEI tienen GAP más negativos
3. **Investigar LEI:** Verificar por qué todas las instancias están garantizadas
4. **Exploración DSJ/SCH:** Implementar análisis especiales para problemas abiertos

---

**Generado automáticamente por GAA Sistema de Experimentación**
