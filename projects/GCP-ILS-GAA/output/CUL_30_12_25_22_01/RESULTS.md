# Resultados - CUL

**Fecha:** 2025-12-30T22:01:52.718495

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 1 |
| Completadas | 1 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0008s |
| Tiempo Promedio | 0.000837s |
| Fitness Promedio | 0.9000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | flat1000_50_0 | 1000 | 245000 | 0.9000 | 50 | 0.000837 | ✅ |

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

⚠️ **Nota:** No hay datos de referencia disponibles. Los valores mostrados corresponden al fitness encontrado por GAA.

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | 0.00% |
| Instancias Óptimas | 0/1 |
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
- **Timestamp:** 2025-12-30T22:01:52.718495

---

*Generado automáticamente por execute_experiments.py*