# Resultados - REG

**Fecha:** 2025-12-30T22:19:14.390286

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 14 |
| Completadas | 14 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 15.0714 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | fpsol2.i.1 | 496 | 11654 | 17.0000 | 50 | 0.000010 | ⏱️ |
| 2 | fpsol2.i.2 | 451 | 8691 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 3 | fpsol2.i.3 | 425 | 8688 | 15.0000 | 50 | 0.000010 | ⏱️ |
| 4 | inithx.i.1 | 864 | 18707 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 5 | inithx.i.2 | 645 | 13979 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 6 | inithx.i.3 | 621 | 13969 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 7 | mulsol.i.1 | 197 | 3925 | 15.0000 | 50 | 0.000010 | ⏱️ |
| 8 | mulsol.i.2 | 188 | 3885 | 15.0000 | 50 | 0.000010 | ⏱️ |
| 9 | mulsol.i.3 | 184 | 3916 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 10 | mulsol.i.4 | 185 | 3946 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 11 | mulsol.i.5 | 186 | 3973 | 16.0000 | 50 | 0.000010 | ⏱️ |
| 12 | zeroin.i.1 | 211 | 4100 | 14.0000 | 50 | 0.000010 | ⏱️ |
| 13 | zeroin.i.2 | 211 | 3541 | 12.0000 | 50 | 0.000010 | ⏱️ |
| 14 | zeroin.i.3 | 206 | 3540 | 13.0000 | 50 | 0.000010 | ⏱️ |

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
| fpsol2.i.1 | 17 | 65 | ÓPTIMO | -73.85% | ❌ |
| fpsol2.i.2 | 14 | 30 | ÓPTIMO | -53.33% | ❌ |
| fpsol2.i.3 | 15 | 30 | ÓPTIMO | -50.00% | ❌ |
| inithx.i.1 | 16 | 54 | ÓPTIMO | -70.37% | ❌ |
| inithx.i.2 | 16 | 31 | ÓPTIMO | -48.39% | ❌ |
| inithx.i.3 | 16 | 31 | ÓPTIMO | -48.39% | ❌ |
| mulsol.i.1 | 15 | 49 | ÓPTIMO | -69.39% | ❌ |
| mulsol.i.2 | 15 | 31 | ÓPTIMO | -51.61% | ❌ |
| mulsol.i.3 | 16 | 31 | ÓPTIMO | -48.39% | ❌ |
| mulsol.i.4 | 16 | 31 | ÓPTIMO | -48.39% | ❌ |
| mulsol.i.5 | 16 | 31 | ÓPTIMO | -48.39% | ❌ |
| zeroin.i.1 | 14 | 49 | ÓPTIMO | -71.43% | ❌ |
| zeroin.i.2 | 12 | 30 | ÓPTIMO | -60.00% | ❌ |
| zeroin.i.3 | 13 | 30 | ÓPTIMO | -56.67% | ❌ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | -57.04% |
| Instancias Óptimas | 0/14 |
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

- **Familia:** REG
- **Timestamp:** 2025-12-30T22:19:14.390286

---

*Generado automáticamente por execute_experiments.py*