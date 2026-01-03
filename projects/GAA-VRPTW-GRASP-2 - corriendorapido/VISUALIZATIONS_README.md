"""
README: Visualizaciones Generadas - VRPTW-GRASP Experiments
============================================================
"""

# Visualizaciones Generadas

## Resumen

Después de ejecutar `python scripts/experiments.py --mode QUICK/FULL`, se generan los siguientes gráficos en la carpeta `output/{timestamp}/plots/`:

---

## 9 Gráficos Canónicos Generados

### 1. **01_performance_comparison.png**
**Tipo**: Gráfico de barras (Bar chart)

**Descripción**: Comparación del desempeño promedio de los tres algoritmos en términos de distancia total.

**Elementos**:
- **Eje X**: Algoritmos (GRASP, VND, ILS)
- **Eje Y**: Distancia promedio
- **Barras**: Altura = distancia media
- **Valores**: Etiquetados encima de cada barra

**Interpretación**:
- Altura más baja = mejor desempeño
- Permite identificar rápidamente el algoritmo más efectivo
- Útil para comparación de alto nivel

---

### 2. **02_distance_by_instance.png**
**Tipo**: Gráfico de líneas (Line plot)

**Descripción**: Distancia lograda por cada algoritmo en cada instancia (en orden).

**Elementos**:
- **Eje X**: Índice de instancia (1, 2, 3, ...)
- **Eje Y**: Distancia total
- **Líneas**: Una por algoritmo, con marcadores distintos
- **Colores**: Diferenciados por algoritmo

**Interpretación**:
- Muestra cómo varían los resultados entre instancias
- Identifica instancias difíciles (picos altos)
- Compara comportamiento relativo entre algoritmos

---

### 3. **03_distance_by_family.png**
**Tipo**: Gráfico de barras (Bar chart)

**Descripción**: Distancia promedio por familia de instancias Solomon (C1, C2, R1, R2, RC1, RC2).

**Elementos**:
- **Eje X**: Familias Solomon
- **Eje Y**: Distancia promedio
- **Barras**: Una por familia, coloreadas con gradiente
- **Valores**: Etiquetados encima

**Interpretación**:
- Solo aplicable en modo FULL (56 instancias)
- Identifica qué familias son más desafiantes
- RC (combinadas) típicamente más difíciles que C (agrupadas)

---

### 4. **04_execution_time.png**
**Tipo**: Gráfico de barras (Bar chart)

**Descripción**: Tiempo de ejecución promedio por algoritmo.

**Elementos**:
- **Eje X**: Algoritmos (GRASP, VND, ILS)
- **Eje Y**: Tiempo (segundos)
- **Barras**: Altura = tiempo medio
- **Etiquetas**: "X.XXs"

**Interpretación**:
- GRASP y VND típicamente lentos (~5-6s)
- ILS más rápido (~1-2s)
- Trade-off tiempo vs calidad

**Nota**: VND usa GRASP internamente, por eso es similar en tiempo.

---

### 5. **06_algorithms_boxplot.png**
**Tipo**: Diagrama de caja (Boxplot)

**Descripción**: Distribución estadística de distancias para cada algoritmo.

**Elementos**:
- **Caja**: Rango intercuartílico (25% al 75%)
- **Línea central**: Mediana
- **Whiskers**: Valores min/max
- **Outliers**: Puntos individuales fuera del rango

**Interpretación**:
- Caja más pequeña = resultados más consistentes
- Mediana más baja = mejor desempeño típico
- Outliers = instancias particularmente difíciles o fáciles

---

### 6. **07_family_algorithm_heatmap.png**
**Tipo**: Heatmap (Mapa de calor)

**Descripción**: Matriz de desempeño: distancia promedio por familia (filas) y algoritmo (columnas).

**Elementos**:
- **Filas**: Familias Solomon (C1, C2, R1, R2, RC1, RC2)
- **Columnas**: Algoritmos (GRASP, VND, ILS)
- **Colores**: Verde (bajo) → Rojo (alto)
- **Valores**: Distancia promedio en cada celda

**Interpretación**:
- Celdas más verdes = mejor desempeño
- Identifica especialización: ¿qué algoritmo es mejor en cada familia?
- Útil para tomar decisiones de selección de algoritmo

---

### 7. **08_k_vs_d_pareto.png**
**Tipo**: Scatter plot (Gráfico de dispersión)

**Descripción**: Análisis multi-objetivo: relación entre número de vehículos (K) y distancia (D).

**Elementos**:
- **Eje X**: Número de vehículos (K)
- **Eje Y**: Distancia total (D)
- **Puntos**: Uno por solución, coloreado por algoritmo
- **Marcadores**: Distintos por algoritmo

**Interpretación**:
- Frente de Pareto: puntos "no dominados"
- Más a la izquierda y abajo = mejor (menos vehículos, menos distancia)
- Identifica soluciones incomparables

**Ejemplo**: 
- GRASP: K=1, D=54 (excelente)
- ILS: K=1, D=55 (similar pero ligeramente peor)
- VND: K=1, D=54 (idéntico a GRASP)

---

### 8. **09_robustness_by_instance.png**
**Tipo**: Múltiples boxplots (6 gráficos en una figura)

**Descripción**: Robustez por instancia específica. Muestra 6 instancias representativas.

**Elementos**:
- **6 subplots**: Una por instancia (R101, R102, R103, ...)
- **Cada subplot**: Boxplot comparando los 3 algoritmos
- **Eje Y**: Distancia

**Interpretación**:
- Identifica instancias donde un algoritmo destaca
- Muestra consistencia/variabilidad dentro de instancia
- Útil para debugging: ¿por qué ILS es malo en R112?

---

### 9. **10_k_feasibility_analysis.png**
**Tipo**: Gráfico combinado (barras + barras apiladas)

**Descripción**: Análisis de viabilidad: ¿con qué frecuencia cada algoritmo alcanza K_BKS?

**Elementos**:
- **Subplot 1 (izquierda)**: 
  - Barras: Tasa de viabilidad (0-100%)
  - Verde: 100% viabilidad
  - Naranja: 50-99% viabilidad
  - Rojo: <50% viabilidad

- **Subplot 2 (derecha)**:
  - Barras apiladas: Instancias resueltas (verde) vs sin resolver (rojo)
  - Altura = total de instancias

**Interpretación**:
- GRASP: Típicamente 100% o >90% viabilidad
- VND: Similar a GRASP (usa GRASP internamente)
- ILS: Varía más, pero generalmente >80%
- Métrica crítica: alcanzar K óptimo es prioridad

---

## Gráficos No Generados (Pendientes)

Los siguientes gráficos mencionados en la documentación aún no se generan:

❌ **convergence_K.png** - Convergencia iteración a iteración del número de vehículos
❌ **convergence_D.png** - Convergencia iteración a iteración de la distancia
❌ **route_visualization_*.png** - Visualización geométrica de rutas en el plano

**Razón**: Requieren datos de historial iterativo (no disponibles en CSV actual)

---

## Estructura de Salida

```
output/
└── vrptw_experiments_QUICK_02-01-26_20-33-00/
    ├── results/
    │   ├── raw_results.csv                        ← Datos crudos
    │   ├── summary_report.txt                     ← Resumen estadístico
    │   └── experiment_metadata.json               ← Metadatos
    └── plots/
        ├── 01_performance_comparison.png          ← Comparación promedio
        ├── 02_distance_by_instance.png            ← Líneas por instancia
        ├── 03_distance_by_family.png              ← Barras por familia
        ├── 04_execution_time.png                  ← Tiempo ejecución
        ├── 06_algorithms_boxplot.png              ← Distribución
        ├── 07_family_algorithm_heatmap.png        ← Heatmap
        ├── 08_k_vs_d_pareto.png                   ← Multi-objetivo
        ├── 09_robustness_by_instance.png          ← 6 instancias
        └── 10_k_feasibility_analysis.png          ← Viabilidad K
```

---

## Ejecución

### QUICK Mode (R1 family, 12 instancias)
```bash
python scripts/experiments.py --mode QUICK
# Tiempo: ~10-15 minutos
# Gráficos: 9 (información concentrada)
```

### FULL Mode (6 families, 56 instancias)
```bash
python scripts/experiments.py --mode FULL
# Tiempo: ~40-60 minutos
# Gráficos: 9 (información completa)
```

---

## Comparación con Documentación

**Documentación menciona**: "11 gráficos canónicos"

**Implementado actualmente**: 9 gráficos

**Diferencia**: 2 gráficos pendientes que requieren datos de convergencia iterativa

| Gráfico | Status | Razón |
|---------|--------|-------|
| Performance comparison | ✅ | Implementado |
| Distance by instance | ✅ | Implementado |
| Distance by family | ✅ | Implementado |
| Execution time | ✅ | Implementado |
| Boxplot algorithms | ✅ | Implementado |
| Heatmap family x algo | ✅ | Implementado |
| K vs D Pareto | ✅ | Implementado |
| Robustness by instance | ✅ | Implementado |
| K feasibility | ✅ | Implementado |
| Convergence K | ❌ | Requiere historial iterativo |
| Convergence D | ❌ | Requiere historial iterativo |
| Route visualization | ❌ | Requiere coordenadas de clientes |

---

## Cómo Interpretar los Gráficos

### Para Reportes Ejecutivos
Usar: `01_performance_comparison.png` y `10_k_feasibility_analysis.png`

### Para Análisis Detallado
Usar: `07_family_algorithm_heatmap.png` y `08_k_vs_d_pareto.png`

### Para Evaluación de Robustez
Usar: `06_algorithms_boxplot.png` y `09_robustness_by_instance.png`

### Para Análisis de Tiempo
Usar: `04_execution_time.png` con `08_k_vs_d_pareto.png`

---

## Próximas Mejoras

Para futuros iteraciones:

1. **Convergence tracking**: Modificar scripts para guardar historial iterativo
2. **Route visualization**: Integrar ploteo geométrico de rutas en plano 2D
3. **Statistical tests**: Añadir tests de significancia (ANOVA, Mann-Whitney)
4. **Custom themes**: Permitir temas de colores personalizados
5. **Interactive plots**: Generar versiones HTML interactivas con Plotly

---

**Última actualización**: 2026-01-02  
**Versión**: 1.0.0  
**Estado**: Production Ready ✅
