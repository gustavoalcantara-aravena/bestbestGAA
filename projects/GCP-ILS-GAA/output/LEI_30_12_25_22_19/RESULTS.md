# Resultados - LEI

**Fecha:** 2025-12-30T22:19:13.336121

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 12 |
| Completadas | 12 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 18.0000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | le450_15a | 450 | 8168 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 2 | le450_15b | 450 | 8169 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 3 | le450_15c | 450 | 16680 | 27.0000 | 50 | 0.000010 | ⏱️ |
| 4 | le450_15d | 450 | 16750 | 27.0000 | 50 | 0.000010 | ⏱️ |
| 5 | le450_25a | 450 | 8260 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 6 | le450_25b | 450 | 8263 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 7 | le450_25c | 450 | 17343 | 28.0000 | 50 | 0.000010 | ⏱️ |
| 8 | le450_25d | 450 | 17425 | 28.0000 | 50 | 0.000010 | ⏱️ |
| 9 | le450_5a | 450 | 5714 | 9.0000 | 50 | 0.000010 | ⏱️ |
| 10 | le450_5b | 450 | 5734 | 9.0000 | 50 | 0.000010 | ⏱️ |
| 11 | le450_5c | 450 | 9803 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 12 | le450_5d | 450 | 9757 | 16.0000 | 50 | 0.000010 | ⏱️ |

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
| le450_15a | 14 | 15 | ÓPTIMO (Garantizado) | -6.67% | ❌ |
| le450_15b | 14 | 15 | ÓPTIMO (Garantizado) | -6.67% | ❌ |
| le450_15c | 27 | 15 | ÓPTIMO (Garantizado) | +80.00% | ❌ |
| le450_15d | 27 | 15 | ÓPTIMO (Garantizado) | +80.00% | ❌ |
| le450_25a | 14 | 25 | ÓPTIMO (Garantizado) | -44.00% | ❌ |
| le450_25b | 14 | 25 | ÓPTIMO (Garantizado) | -44.00% | ❌ |
| le450_25c | 28 | 25 | ÓPTIMO (Garantizado) | +12.00% | ❌ |
| le450_25d | 28 | 25 | ÓPTIMO (Garantizado) | +12.00% | ❌ |
| le450_5a | 9 | 5 | ÓPTIMO (Garantizado) | +80.00% | ❌ |
| le450_5b | 9 | 5 | ÓPTIMO (Garantizado) | +80.00% | ❌ |
| le450_5c | 16 | 5 | ÓPTIMO (Garantizado) | +220.00% | ❌ |
| le450_5d | 16 | 5 | ÓPTIMO (Garantizado) | +220.00% | ❌ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | +56.89% |
| Instancias Óptimas | 0/12 |
| Tasa Optimalidad | 0.0% |

### Interpretación

🔴 **Mejorable**: El algoritmo se aleja del óptimo (GAP ≥ 10%).

## Análisis Visual

![Análisis de Convergencia y Calidad](convergence_analysis.png)

El gráfico anterior muestra el comportamiento típico del algoritmo en instancias de GCP:
- **Panel Superior Izquierdo**: Convergencia del fitness (mejora progresiva con estabilización)
- **Panel Superior Derecho**: Distribución de calidad de soluciones encontradas
- **Panel Inferior Izquierdo**: GAP relativo a óptimo/BKS por instancia
- **Panel Inferior Derecho**: Relación tiempo vs tasa de éxito

## Información Técnica

- **Familia:** LEI
- **Timestamp:** 2025-12-30T22:19:13.336121

---

*Generado automáticamente por execute_experiments.py*