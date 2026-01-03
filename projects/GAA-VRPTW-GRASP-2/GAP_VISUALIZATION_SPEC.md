# Especificación de Gráficos GAP - VRPTW-GRASP

## Objetivo
Generar visualizaciones que muestren cómo cada algoritmo se desempeña vs BKS (Best Known Solution)
usando el métrica de GAP (%) en cada instancia del benchmark Solomon.

---

## 1. GAP Comparison All Instances
**Archivo**: `01_gap_comparison_all_instances.png`
**Tipo**: Bar chart (barras agrupadas)
**Contenido**:
- X: 56 instancias Solomon (C1, C2, R1, R2, RC1, RC2)
- Y: GAP (%) = (Solución - BKS) / BKS * 100
- 3 barras por instancia (Algo1, Algo2, Algo3)
- Línea horizontal en GAP=0 (BKS)
- Fondo alternado por familia
- Escala: 24" x 8"

**Métricas Clave**:
- Rojo: Algo1 (GRASP Puro)
- Verde: Algo2 (CONTROL)
- Amarillo: Algo3 (GRASP Adaptativo)

---

## 2. GAP Evolution Lines
**Archivo**: `02_gap_evolution_lines.png`
**Tipo**: Line chart (líneas con marcadores)
**Contenido**:
- X: 56 instancias en orden (C1...C2...R1...R2...RC1...RC2)
- Y: GAP (%)
- 3 líneas (una por algoritmo)
- Marcadores diferentes (círculo, cuadrado, triángulo)
- Línea horizontal en GAP=0 (BKS)
- Escala: 24" x 8"

**Propósito**: Mostrar tendencia y comportamiento relativo entre algoritmos

---

## 3. GAP Distribution by Family
**Archivo**: `03_gap_boxplot_by_family.png`
**Tipo**: Boxplot (caja y bigotes)
**Contenido**:
- X: 6 familias (C1, C2, R1, R2, RC1, RC2)
- Y: GAP (%)
- 3 boxplots por familia (uno por algoritmo)
- Línea en GAP=0 (BKS)
- Escala: 14" x 8"

**Estadísticas mostradas**:
- Mediana (línea en caja)
- Q1-Q3 (caja)
- Rango (bigotes)
- Outliers (puntos)

**Propósito**: Comparar distribución y variabilidad por familia

---

## 4. GAP Heatmap
**Archivo**: `04_gap_heatmap.png`
**Tipo**: Heatmap (colores)
**Contenido**:
- X: 3 algoritmos (Algo1, Algo2, Algo3)
- Y: 56 instancias (filas)
- Colores: Escala RdYlGn_r (Rojo=peor, Verde=mejor)
- Valores numéricos en celdas (GAP %)
- Centro en 0 (BKS)
- Escala: 12" x 16"

**Propósito**: Visualizar patrones de desempeño por instancia

---

## 5. GAP by Family Grid
**Archivo**: `05_gap_by_family_grid.png`
**Tipo**: Subplot grid (6 subplots, 2x3)
**Contenido**:
- 6 subplots (uno por familia)
- Cada subplot:
  - X: Instancias de esa familia
  - Y: GAP (%)
  - 3 barras agrupadas (Algo1, Algo2, Algo3)
  - Línea horizontal en GAP=0
  - Título: "Familia XY (N instancias)"
- Leyenda compartida
- Escala: 18" x 10"

**Propósito**: Análisis detallado por familia

---

## Datos Utilizados
**Fuente**: `gap_data.json` generado por `gap_data_generator.py`

**Estructura JSON**:
```json
{
  "metadata": {...},
  "instances": {
    "C101": {
      "family": "C1",
      "bks": 828.94,
      "algorithms": {
        "algo1": {"distance": 1521.98, "gap_percent": 83.61, ...},
        "algo2": {"distance": 1103.20, "gap_percent": 33.09, ...},
        "algo3": {"distance": 1835.92, "gap_percent": NaN, ...}
      }
    },
    ...
  },
  "summary_by_algorithm": {
    "1": {"avg_distance": 1536.86, "avg_gap": 79.29, ...},
    "2": {"avg_distance": 1182.19, "avg_gap": 33.18, ...},
    "3": {"avg_distance": 1408.04, "avg_gap": NaN, ...}
  }
}
```

---

## Directorios de Salida
- **QUICK**: `output/vrptw_experiments_QUICK_[timestamp]/plots/`
- **FULL**: `output/vrptw_experiments_FULL_[timestamp]/plots/`

Todos los gráficos se guardan en `plots/` con nombres `0X_gap_*.png`

---

## Comparación entre Iteraciones
Los JSON se almacenan en `results/gap_data.json`, permitiendo:
1. Comparar resultados de múltiples iteraciones
2. Generar gráficos comparativos (ITER-3 vs ITER-4 vs ITER-5 vs ITER-6)
3. Análisis histórico sin re-ejecutar

---

## Tabla Resumen Estadístico
**Archivo**: Impreso en stdout durante generación
**Contenido**:
- Tabla con estadísticas por algoritmo:
  - Promedio GAP (%)
  - Mediana GAP (%)
  - Desviación estándar
  - Min/Max GAP
  - Instancias mejor que BKS
  - Instancias < 5% GAP

---

## Colores Estándar
- **Algo1** (GRASP Puro): #FF6B6B (Rojo)
- **Algo2** (CONTROL): #4ECDC4 (Verde/Turquesa)
- **Algo3** (GRASP Adaptativo): #FFE66D (Amarillo)
- **BKS**: Red line, dashed

---

## Validación
✓ JSON generado con gap_data_generator.py
✓ Gráficos generados con plot_gap_comparison_from_json.py (NUEVO)
✓ Todos los gráficos en carpeta plots/
✓ Nombres estandarizados: 0X_gap_*.png
✓ Resolución: 300 DPI para publicación
