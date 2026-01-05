# Resultados - REG

**Fecha:** 2025-12-30T22:10:05.642451

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 14 |
| Completadas | 14 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 0.9000 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | fpsol2.i.1 | 496 | 11654 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 2 | fpsol2.i.2 | 451 | 8691 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 3 | fpsol2.i.3 | 425 | 8688 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 4 | inithx.i.1 | 864 | 18707 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 5 | inithx.i.2 | 645 | 13979 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 6 | inithx.i.3 | 621 | 13969 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 7 | mulsol.i.1 | 197 | 3925 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 8 | mulsol.i.2 | 188 | 3885 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 9 | mulsol.i.3 | 184 | 3916 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 10 | mulsol.i.4 | 185 | 3946 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 11 | mulsol.i.5 | 186 | 3973 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 12 | zeroin.i.1 | 211 | 4100 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 13 | zeroin.i.2 | 211 | 3541 | 0.9000 | 50 | 0.000010 | ⏱️ |
| 14 | zeroin.i.3 | 206 | 3540 | 0.9000 | 50 | 0.000010 | ⏱️ |

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
| fpsol2.i.1 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| fpsol2.i.2 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| fpsol2.i.3 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| inithx.i.1 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| inithx.i.2 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| inithx.i.3 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| mulsol.i.1 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| mulsol.i.2 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| mulsol.i.3 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| mulsol.i.4 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| mulsol.i.5 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| zeroin.i.1 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| zeroin.i.2 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |
| zeroin.i.3 | 0.9000 | N/A | DESCONOCIDO | N/A | ⚠️ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | N/A |
| Instancias Óptimas | 0/14 |
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

- **Familia:** REG
- **Timestamp:** 2025-12-30T22:10:05.642451

---

*Generado automáticamente por execute_experiments.py*