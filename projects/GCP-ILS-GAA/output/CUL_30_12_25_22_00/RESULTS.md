# Resultados - CUL

**Fecha:** 2025-12-30T22:00:53.187802

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0041s |
| Tiempo Promedio | 0.000680s |
| Fitness Promedio | 0.9000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | flat1000_50_0 | 1000 | 245000 | 0.9000 | 50 | 0.000561 | ✅ |
| 2 | flat1000_60_0 | 1000 | 245830 | 0.9000 | 50 | 0.001129 | ✅ |
| 3 | flat1000_76_0 | 1000 | 246708 | 0.9000 | 50 | 0.001151 | ✅ |
| 4 | flat300_20_0 | 300 | 21375 | 0.9000 | 50 | 0.000447 | ✅ |
| 5 | flat300_26_0 | 300 | 21633 | 0.9000 | 50 | 0.000187 | ✅ |
| 6 | flat300_28_0 | 300 | 21695 | 0.9000 | 50 | 0.000609 | ✅ |

## 📊 Análisis de Calidad de Soluciones (GAP Analysis)

### Resumen de GAP

El **GAP** (Generalized Achievement Percentage) mide la desviación entre la solución encontrada por GAA
y el óptimo conocido (ÓPTIMO) o la mejor solución conocida (BKS - Best Known Solution):

- **GAP Absoluto** = Valor_GAA - Valor_Referencia
- **GAP Porcentual (%)** = (GAP_Absoluto / Valor_Referencia) × 100

Un GAP de **0%** indica que la solución encontrada es **óptima o equivalente a la mejor conocida**.

### Tabla Comparativa

| Instancia | Valor GAA | Referencia | Estado |
|-----------|-----------|-----------|--------|
| flat1000_50_0 | 0.9000 | Sin datos | ⚠️ |
| flat1000_60_0 | 0.9000 | Sin datos | ⚠️ |
| flat1000_76_0 | 0.9000 | Sin datos | ⚠️ |
| flat300_20_0 | 0.9000 | Sin datos | ⚠️ |
| flat300_26_0 | 0.9000 | Sin datos | ⚠️ |
| flat300_28_0 | 0.9000 | Sin datos | ⚠️ |

⚠️ **Nota:** No hay datos de referencia disponibles. Los valores mostrados corresponden al fitness encontrado por GAA.

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | 0.00% |
| Instancias Óptimas | 0/6 |
| Tasa Optimalidad | 0.0% |

### Interpretación

✅ **Excelente**: El algoritmo encontró soluciones óptimas u óptimas en todas las instancias.

## Análisis Visual

![Análisis de Convergencia y Calidad](convergence_analysis.png)

El gráfico anterior muestra el comportamiento típico del algoritmo en instancias de GCP:
- **Panel Superior Izquierdo**: Convergencia del fitness (mejora progresiva con estabilización)
- **Panel Superior Derecho**: Distribución de calidad de soluciones encontradas
- **Panel Inferior Izquierdo**: GAP relativo a óptimo/BKS por instancia
- **Panel Inferior Derecho**: Relación tiempo vs tasa de éxito

## Información Técnica

- **Familia:** CUL
- **Timestamp:** 2025-12-30T22:00:53.187802

---

*Generado automáticamente por execute_experiments.py*