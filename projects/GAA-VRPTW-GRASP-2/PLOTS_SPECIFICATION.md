# GRÁFICOS CANÓNICOS VRPTW-GRASP

## Descripción General

Se generan **11 tipos de gráficos canónicos** que cumplen con la especificación de outputs del proyecto VRPTW-GRASP. Cada gráfico proporciona un análisis diferente de los resultados experimentales.

---

## 11 GRÁFICOS CANÓNICOS

### 1. **Performance Comparison** (`01_performance_comparison.png`)
- **Tipo**: Gráfico de barras
- **Eje X**: Algoritmos (GRASP, VND, ILS, etc.)
- **Eje Y**: Distancia promedio
- **Propósito**: Comparar rendimiento general de cada algoritmo
- **Métrica**: Promedio de distancia total

---

### 2. **Distance by Instance** (`02_distance_by_instance.png`)
- **Tipo**: Gráfico de líneas con marcadores
- **Eje X**: Índice de instancia
- **Eje Y**: Distancia
- **Propósito**: Ver tendencia de rendimiento a través de diferentes instancias
- **Métrica**: Distancia por instancia individual

---

### 3. **Distance by Family** (`03_distance_by_family.png`)
- **Tipo**: Gráfico de barras
- **Eje X**: Familia de instancias (C1, C2, R1, R2, RC1, RC2)
- **Eje Y**: Distancia promedio
- **Propósito**: Comparar dificultad de diferentes familias
- **Métrica**: Distancia promedio por familia

---

### 4. **Execution Time** (`04_execution_time.png`)
- **Tipo**: Gráfico de barras
- **Eje X**: Algoritmos
- **Eje Y**: Tiempo en segundos
- **Propósito**: Analizar velocidad de ejecución
- **Métrica**: Tiempo promedio de ejecución

---

### 5. **Gap Analysis** (`05_gap_analysis.png`)
- **Tipo**: Gráfico de barras
- **Eje X**: Algoritmos
- **Eje Y**: Brecha vs BKS (%)
- **Propósito**: Evaluar calidad de soluciones respecto a Best Known Solutions
- **Métrica**: Porcentaje de desviación del BKS (solo cuando K = K_BKS)
- **Nota**: Línea roja punteada marca el BKS (0%)

---

### 6. **Distance Boxplot** (`06_algorithms_boxplot.png`)
- **Tipo**: Diagrama de caja (boxplot)
- **Eje X**: Algoritmos
- **Eje Y**: Distancia
- **Propósito**: Mostrar distribución y variabilidad de resultados
- **Métricas**: Mediana, cuartiles, mínimo, máximo, outliers

---

### 7. **Family × Algorithm Heatmap** (`07_family_algorithm_heatmap.png`)
- **Tipo**: Mapa de calor (heatmap)
- **Eje X**: Algoritmos
- **Eje Y**: Familias de instancias
- **Propósito**: Ver rendimiento en matriz de familia×algoritmo
- **Métrica**: Distancia promedio con código de colores (rojo=malo, verde=bueno)
- **Anotaciones**: Valores numéricos en cada celda

---

### 8. **K vs D Pareto** (`08_k_vs_d_pareto.png`)
- **Tipo**: Gráfico de dispersión (scatter plot)
- **Eje X**: Número de vehículos (K)
- **Eje Y**: Distancia total (D)
- **Propósito**: Mostrar trade-off entre número de vehículos y distancia
- **Códigos**: Colores por algoritmo, forma por familia
- **Línea**: Frontera Pareto (soluciones no dominadas)

---

### 9. **Robustness by Instance** (`09_robustness_by_instance.png`)
- **Tipo**: Gráfico de barras agrupadas
- **Eje X**: Instancias
- **Eje Y**: Número de algoritmos que alcanzaron K_BKS
- **Propósito**: Identificar instancias fáciles vs difíciles
- **Métrica**: Robustez = cantidad de algoritmos que encontraron K óptimo

---

### 10. **K Feasibility Analysis** (`10_k_feasibility_analysis.png`)
- **Tipo**: Gráfico de barras apiladas
- **Eje X**: Algoritmos
- **Eje Y**: Número de instancias
- **Propósito**: Evaluar capacidad de cada algoritmo
- **Desglose**: 
  - Azul: Instancias donde K = K_BKS (factibles)
  - Naranja: Instancias donde K > K_BKS (no factibles)

---

### 11. **Algorithm Radar Comparison** (`11_algorithm_radar_comparison.png`)
- **Tipo**: Gráfico de radar (polígono multidimensional)
- **Dimensiones**: 
  - Distancia (normalizada, invertida)
  - Eficiencia de tiempo (normalizada, invertida)
  - Consistencia (1 - variabilidad)
- **Propósito**: Comparación multidimensional de algoritmos
- **Escala**: 0-1 en todos los ejes (1=mejor)
- **Código de colores**: Un color por algoritmo

---

## CÓMO INTERPRETAR LOS GRÁFICOS

### Análisis de Rendimiento
1. Revisar **#1 (Performance Comparison)** para ranking general
2. Revisar **#5 (Gap Analysis)** para calidad vs BKS
3. Revisar **#4 (Execution Time)** para velocidad

### Análisis de Dificultad
1. Revisar **#3 (Distance by Family)** para familias difíciles
2. Revisar **#9 (Robustness)** para instancias problemáticas

### Análisis de Variabilidad
1. Revisar **#6 (Boxplot)** para ver consistencia
2. Revisar **#7 (Heatmap)** para patrones familia×algoritmo

### Análisis Multidimensional
1. Revisar **#8 (Pareto)** para trade-offs K-D
2. Revisar **#11 (Radar)** para comparación global

---

## ESTADÍSTICAS INCLUIDAS

Además de los gráficos, se genera **summary_report.txt** con:
- Estadísticas por algoritmo (media, min, max, desv. est.)
- Estadísticas por familia
- Top 5 mejores y peores soluciones

---

## ESPECIFICACIÓN TÉCNICA

| Aspecto | Detalle |
|--------|---------|
| **Formato** | PNG (300 DPI) |
| **Tamaño base** | 12x6 pulgadas (ajustable por gráfico) |
| **Estilo** | Seaborn whitegrid |
| **Colores** | Paleta armónica optimizada para contraste |
| **Fuentes** | Sans-serif, 10-14pt según contexto |
| **Fondo** | Blanco, sin marco de ejes |
| **Leyendas** | Presentes en todos los gráficos multi-serie |

---

## GENERACIÓN AUTOMÁTICA

Los gráficos se generan automáticamente al finalizar cada experimento:

```bash
python scripts/experiments.py --mode QUICK
# o
python scripts/experiments.py --mode FULL
```

**Ubicación**: `output/vrptw_experiments_{QUICK|FULL}_{timestamp}/plots/`

---

## VALIDACIÓN

Todos los gráficos cumplen con:
- ✅ Especificación de 11 tipos canónicos
- ✅ Formato PNG de alta resolución
- ✅ Etiquetas y títulos informativos
- ✅ Código de colores consistente
- ✅ Escalabilidad QUICK (12 inst.) y FULL (56 inst.)

---

## DEPENDENCIAS

- matplotlib (visualización)
- seaborn (estilos y heatmaps)
- numpy (cálculos)

Instalación:
```bash
pip install matplotlib seaborn numpy
```

---

*Documento de especificación de gráficos canónicos VRPTW-GRASP*
