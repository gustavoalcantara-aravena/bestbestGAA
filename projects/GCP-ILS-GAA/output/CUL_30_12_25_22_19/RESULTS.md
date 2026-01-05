# Resultados - CUL

**Fecha:** 2025-12-30T22:19:12.129400

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Fallidas | 0 ❌ |
| Tasa Éxito | 100% |
| Tiempo Total | 0.0001s |
| Tiempo Promedio | 0.000010s |
| Fitness Promedio | 111.8333 |

## Detalle de Instancias

| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |
|---|-----------|----------|-------|---------|-------------|-----------|--------|
| 1 | flat1000_50_0 | 1000 | 245000 | 172.0000 | 50 | 0.000010 | ⏱️ |
| 2 | flat1000_60_0 | 1000 | 245830 | 173.0000 | 50 | 0.000010 | ⏱️ |
| 3 | flat1000_76_0 | 1000 | 246708 | 173.0000 | 50 | 0.000010 | ⏱️ |
| 4 | flat300_20_0 | 300 | 21375 | 51.0000 | 50 | 0.000010 | ⏱️ |
| 5 | flat300_26_0 | 300 | 21633 | 51.0000 | 50 | 0.000010 | ⏱️ |
| 6 | flat300_28_0 | 300 | 21695 | 51.0000 | 50 | 0.000010 | ⏱️ |

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
| flat1000_50_0 | 172 | 50 | ÓPTIMO | +244.00% | ❌ |
| flat1000_60_0 | 173 | 60 | ÓPTIMO | +188.33% | ❌ |
| flat1000_76_0 | 173 | 76 | ÓPTIMO | +127.63% | ❌ |
| flat300_20_0 | 51 | 20 | ÓPTIMO | +155.00% | ❌ |
| flat300_26_0 | 51 | 26 | ÓPTIMO | +96.15% | ❌ |
| flat300_28_0 | 51 | 28 | ÓPTIMO | +82.14% | ❌ |

### Estadísticas de GAP

| Métrica | Valor |
|---------|-------|
| GAP Promedio (%) | +148.88% |
| Instancias Óptimas | 0/6 |
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

- **Familia:** CUL
- **Timestamp:** 2025-12-30T22:19:12.129400

---

*Generado automáticamente por execute_experiments.py*