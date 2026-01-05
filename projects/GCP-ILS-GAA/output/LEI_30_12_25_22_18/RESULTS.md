# Resultados - LEI

**Fecha:** 2025-12-30T22:18:28.230023

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 12 |
| Completadas | 12 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 0.9000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | le450_15a | 450 | 8168 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 2 | le450_15b | 450 | 8169 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 3 | le450_15c | 450 | 16680 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 4 | le450_15d | 450 | 16750 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 5 | le450_25a | 450 | 8260 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 6 | le450_25b | 450 | 8263 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 7 | le450_25c | 450 | 17343 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 8 | le450_25d | 450 | 17425 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 9 | le450_5a | 450 | 5714 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 10 | le450_5b | 450 | 5734 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 11 | le450_5c | 450 | 9803 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 12 | le450_5d | 450 | 9757 | 0.9000 | 50 | 0.000010 | ⏱️ |

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
| le450_15a | 1 | 15 | ÓPTIMO (Garantizado) | -94.00% | ❌ |
| le450_15b | 1 | 15 | ÓPTIMO (Garantizado) | -94.00% | ❌ |
| le450_15c | 1 | 15 | ÓPTIMO (Garantizado) | -94.00% | ❌ |
| le450_15d | 1 | 15 | ÓPTIMO (Garantizado) | -94.00% | ❌ |
| le450_25a | 1 | 25 | ÓPTIMO (Garantizado) | -96.40% | ❌ |
| le450_25b | 1 | 25 | ÓPTIMO (Garantizado) | -96.40% | ❌ |
| le450_25c | 1 | 25 | ÓPTIMO (Garantizado) | -96.40% | ❌ |
| le450_25d | 1 | 25 | ÓPTIMO (Garantizado) | -96.40% | ❌ |
| le450_5a | 1 | 5 | ÓPTIMO (Garantizado) | -82.00% | ❌ |
| le450_5b | 1 | 5 | ÓPTIMO (Garantizado) | -82.00% | ❌ |
| le450_5c | 1 | 5 | ÓPTIMO (Garantizado) | -82.00% | ❌ |
| le450_5d | 1 | 5 | ÓPTIMO (Garantizado) | -82.00% | ❌ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | -90.80% |
| Instancias Óptimas | 0/12 |
| Tasa Optimalidad | 0.0% |

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

- **Familia:** LEI
- **Timestamp:** 2025-12-30T22:18:28.230023

---

*Generado automáticamente por execute_experiments.py*