# Resultados - MYC

**Fecha:** 2025-12-30T22:10:05.136539

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 0.9000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | myciel2 | 0 | 0 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 2 | myciel3 | 11 | 20 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 3 | myciel4 | 23 | 71 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 4 | myciel5 | 47 | 236 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 5 | myciel6 | 95 | 755 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 6 | myciel7 | 191 | 2360 | 0.9000 | 50 | 0.000010 | ⏱️ |

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
| myciel2 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel3 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel4 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel5 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel6 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| myciel7 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | N/A |
| Instancias Óptimas | 0/6 |
| Tasa Optimalidad | 0.0% |

### Interpretación

⚠️ **Nota:** No hay valores de referencia disponibles en esta ejecución.

## Análisis Visual

![Análisis de Convergencia y Calidad](convergence_analysis.png)

El gráfico anterior muestra el comportamiento típico del algoritmo en instancias de GCP:
- **Panel Superior Izquierdo**: Convergencia del fitness (mejora progresiva con estabilización)
- **Panel Superior Derecho**: Distribución de calidad de soluciones encontradas
- **Panel Inferior Izquierdo**: GAP relativo a óptimo/BKS por instancia
- **Panel Inferior Derecho**: Relación tiempo vs tasa de éxito

## Información Técnica

- **Familia:** MYC
- **Timestamp:** 2025-12-30T22:10:05.136539

---

*Generado automáticamente por execute_experiments.py*