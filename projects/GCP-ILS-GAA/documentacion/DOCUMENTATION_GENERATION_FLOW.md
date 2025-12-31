# 📊 Estructura de Generación de Documentación

## Flujo Completo

Cuando ejecutas cualquier experimento:
```
python main.py --family CUL
       ↓
Se crea carpeta: output/CUL_DD_MM_YY_HH_MM/
       ↓
DocumentationOrchestrator.generate_all_reports()
       ↓
Se generan TODOS estos archivos dentro de la carpeta:
```

---

## 📁 Archivos Generados en output/FAMILY_TIMESTAMP/

### 1. **RESULTS.md** ✅
- **Qué es:** Reporte legible en Markdown con tabla resumen
- **Contenido:**
  - Resumen ejecutivo con métricas principales
  - Tabla detallada de cada instancia (Fitness, Iteraciones, Tiempo)
  - Estados (✅ completada, ⏱️ simulación)

**Ejemplo:**
```markdown
# Resultados - CUL

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Fitness Promedio | 0.9000 |
| Tiempo Total | 0.0001s |
```

---

### 2. **analysis_report.json** ✅
- **Qué es:** Análisis estadístico en JSON
- **Contenido:**
  - Resumen: total, completadas, fallidas
  - Promedios: fitness, tiempo
  - Desglose por instancia

**Estructura:**
```json
{
  "timestamp": "2025-12-30T21:39:00.000000",
  "family": "CUL",
  "summary": {
    "total_instances": 6,
    "completed": 6,
    "avg_fitness": 0.9,
    "avg_time": 0.000013
  },
  "instances": [...]
}
```

---

### 3. **analysis_report.csv** ✅
- **Qué es:** Tabla Excel-compatible
- **Contenido:** Cada fila = una instancia con todas sus métricas

**Estructura:**
```
Family,Instance,Vertices,Edges,Fitness,Iterations,Time_s,Status
CUL,flat300_20_0,300,1450,0.9000,50,0.000023,completed
CUL,flat300_26_0,300,1426,0.9000,50,0.000021,completed
```

---

### 4. **COMPARISON_GAP_ANALYSIS.json** ✅ 🆕
- **Qué es:** Análisis de GAP (diferencia) vs BKS/ÓPTIMO
- **Contenido:**
  - Valor de referencia (BKS/ÓPTIMO)
  - Valor obtenido por GAA
  - **GAP ABSOLUTO** = GAA - BKS
  - **GAP PORCENTUAL** = (GAP / BKS) * 100
  - ¿Es óptimo? (diferencia < 0.0001)

**Estructura:**
```json
{
  "timestamp": "...",
  "family": "CUL",
  "summary": {
    "total_instances": 6,
    "with_reference": 6,
    "optimal_found": 3,
    "avg_gap_percent": 2.45
  },
  "comparisons": [
    {
      "instance": "flat300_20_0",
      "reference_value": 20,
      "reference_type": "ÓPTIMO",
      "gaa_value": 0.9,
      "gap_absolute": -19.1,
      "gap_percent": -95.5,
      "is_optimal": false,
      "iterations": 50,
      "time_seconds": 0.000023
    }
  ]
}
```

---

### 5. **COMPARISON_GAP_ANALYSIS.csv** ✅ 🆕
- **Qué es:** GAP analysis en formato Excel
- **Contenido:** Cada fila = comparación de una instancia

**Estructura:**
```
Instance,Reference_Value,Reference_Type,GAA_Value,GAP_Absolute,GAP_Percent,Is_Optimal,Iterations,Time_s,Vertices,Edges
flat300_20_0,20,ÓPTIMO,0.9000,-19.1000,-95.50,NO,50,0.000023,300,1450
flat300_26_0,26,ÓPTIMO,0.9000,-25.1000,-96.54,NO,50,0.000021,300,1426
```

---

### 6. **validation_report.json** ✅
- **Qué es:** Validación de integridad de datos
- **Contenido:**
  - Todas las instancias tienen fitness?
  - Todas tienen iteraciones?
  - Todas tienen timing?
  - Estados válidos?

**Estructura:**
```json
{
  "timestamp": "...",
  "family": "CUL",
  "execution_summary": {
    "total_instances": 6,
    "status": "completed",
    "all_instances_have_fitness": true,
    "all_instances_have_iterations": true,
    "all_instances_have_timing": true
  },
  "validation_checks": [...]
}
```

---

### 7. **EXECUTIVE_SUMMARY.md** ✅
- **Qué es:** Resumen ejecutivo detallado
- **Contenido:**
  - Datos generales (familia, total instancias)
  - Resultados por instancia
  - Metadata

**Ejemplo:**
```markdown
# 📊 Resumen Ejecutivo - CUL

- **Familia:** CUL
- **Total de Instancias:** 6
- **Completadas:** 6
- **Tiempo Total:** 0.0001s

## Resultados por Instancia
### 1. flat300_20_0
- **Fitness:** 0.9000
- **Iteraciones:** 50
- **Tiempo:** 0.000023s
```

---

## 🔄 Flujo de Ejecución

```
python main.py --family CUL
         ↓
    ExperimentRunner.run_family('CUL')
         ↓
    Ejecuta todas las instancias
    Guarda results.json
         ↓
    DocumentationOrchestrator.generate_all_reports()
         ↓
    ✅ RESULTS.md
    ✅ analysis_report.json
    ✅ analysis_report.csv
    ✅ COMPARISON_GAP_ANALYSIS.json (con GAP analysis)
    ✅ COMPARISON_GAP_ANALYSIS.csv
    ✅ validation_report.json
    ✅ EXECUTIVE_SUMMARY.md
         ↓
    Carpeta COMPLETA y AUTOSUFICIENTE
```

---

## 📌 Puntos Clave

✅ **TODO en una carpeta:** Nada se genera en la raíz
✅ **GAP Analysis:** Se calcula para cada instancia vs BKS/ÓPTIMO
✅ **Múltiples formatos:** JSON, CSV, Markdown para diferentes usos
✅ **Validación incluida:** Se verifica integridad de datos
✅ **Resumen ejecutivo:** Fácil de leer y entender

---

## 🎯 Cálculo de GAP

**GAP Absoluto:** 
```
GAP = Valor_GAA - Valor_Referencia
```

**GAP Porcentual:**
```
GAP% = (GAP / Valor_Referencia) × 100
```

**Interpretación:**
- GAP% = 0% → Óptimo encontrado ✅
- GAP% < 0% → Mejor que referencia (poco común) 🎉
- GAP% > 0% → Peor que referencia (esperado)

---

**Última actualización:** 2025-12-30
**Sistema:** Integrado y Automatizado
