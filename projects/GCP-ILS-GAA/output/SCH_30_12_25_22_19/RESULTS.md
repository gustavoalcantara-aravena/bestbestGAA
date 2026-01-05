# Resultados - SCH

**Fecha:** 2025-12-30T22:19:14.948072

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 2 |
| Completadas | 2 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0000s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 32.5000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | school1 | 385 | 19095 | 35.0000 | 50 | 0.000010 | ⏱️ |
| 2 | school1_nsh | 352 | 14612 | 30.0000 | 50 | 0.000010 | ⏱️ |

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
| school1 | 35.0000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| school1_nsh | 30.0000 | N/A | DESCONOCIDO | N/A | ⚠️ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | N/A |
| Instancias Óptimas | 0/2 |
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

- **Familia:** SCH
- **Timestamp:** 2025-12-30T22:19:14.948072

---

*Generado automáticamente por execute_experiments.py*