# Resultados - MYC

**Fecha:** 2025-12-30T22:21:41.322597

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0007s |
| Tiempo Promedio | 0.000109s |
| Fitness Promedio | 4.5000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | myciel2 | 0 | 0 | 2.0000 | 50 | 0.000080 | ✅ |
| 2 | myciel3 | 11 | 20 | 2.0000 | 50 | 0.000060 | ✅ |
| 3 | myciel4 | 23 | 71 | 3.0000 | 50 | 0.000059 | ✅ |
| 4 | myciel5 | 47 | 236 | 4.0000 | 50 | 0.000050 | ✅ |
| 5 | myciel6 | 95 | 755 | 7.0000 | 50 | 0.000244 | ✅ |
| 6 | myciel7 | 191 | 2360 | 9.0000 | 50 | 0.000163 | ✅ |

## 📊 Análisis de Calidad de Soluciones (GAP Analysis)

### Resumen de GAP

El **GAP** (Generalized Achievement Percentage) mide la desviación entre la solución encontrada por GAA
y el óptimo conocido (ÓPTIMO) o la mejor solución conocida (BKS - Best Known Solution):

- **GAP Absoluto** = Valor_GAA - Valor_Referencia
- **GAP Porcentual (%)** = (GAP_Absoluto / Valor_Referencia) × 100

Un GAP de **0%** indica que la solución encontrada es **óptima o equivalente a la mejor conocida**.

### Tabla Comparativa

| Instancia | Valor GAA | Referencia | Tipo | GAP % | Estado |
|-----------|-----------|-----------|------|-------|--------|
| myciel2 | 2.0000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel3 | 2 | 4 | ÓPTIMO | -50.00% | ❌ |
| myciel4 | 3 | 5 | ÓPTIMO | -40.00% | ❌ |
| myciel5 | 4 | 6 | ÓPTIMO | -33.33% | ❌ |
| myciel6 | 7 | 7 | ÓPTIMO | +0.00% | ✅ |
| myciel7 | 9 | 8 | ÓPTIMO | +12.50% | ❌ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | -22.17% |
| Instancias Óptimas | 1/6 |
| Tasa Optimalidad | 16.7% |

### Interpretación

✅ **Excelente**: El algoritmo encontró soluciones óptimas en todas las instancias.

## Análisis Visual

![Análisis de Convergencia y Calidad](convergence_analysis.png)

El gráfico anterior muestra el comportamiento típico del algoritmo en instancias de GCP:
- **Panel Superior Izquierdo**: Convergencia del fitness (mejora progresiva con estabilización)
- **Panel Superior Derecho**: Distribución de calidad de soluciones encontradas
- **Panel Inferior Izquierdo**: GAP relativo a óptimo/BKS por instancia
- **Panel Inferior Derecho**: Relación tiempo vs tasa de éxito

## Información Técnica

- **Familia:** MYC
- **Timestamp:** 2025-12-30T22:21:41.322597

---

*Generado automáticamente por execute_experiments.py*