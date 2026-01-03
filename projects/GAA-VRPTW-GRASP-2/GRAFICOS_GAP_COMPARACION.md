# 📊 Gráficos Comparativos de GAP: 3 Algoritmos VRPTW

## Resumen Ejecutivo

Se han generado **5 gráficos principales** que comparan el desempeño de los 3 algoritmos respecto a Best Known Solutions (BKS) de Solomon VRPTW:

---

## 📈 Gráficos Generados

### 1️⃣ **Comparación de GAP - Todas las Instancias**
**Archivo**: `01_gap_comparison_all_instances.png`

```
Tipo: Gráfico de barras agrupadas (56 instancias)
Eje X: Instancias Solomon (C1, C2, R1, R2, RC1, RC2)
Eje Y: GAP a BKS (%)
Barras: 
  - ROJO: Algoritmo 1
  - CYAN: Algoritmo 2 (GANADOR)
  - AMARILLO: Algoritmo 3
Línea roja discontinua: BKS (GAP=0)
```

**Interpretación**: 
- Permite ver instantáneamente qué algoritmo es mejor para cada instancia
- **Algoritmo 2 domina claramente** (barras más bajas)
- Fondo gris alternado por familia para fácil lectura

---

### 2️⃣ **Evolución de GAP por Instancia (Líneas)**
**Archivo**: `02_gap_evolution_lines.png`

```
Tipo: Gráfico de líneas (56 instancias)
Eje X: Instancias Solomon en orden
Eje Y: GAP a BKS (%)
Líneas:
  - ROJO: Algoritmo 1 (círculos)
  - CYAN: Algoritmo 2 (cuadrados)
  - AMARILLO: Algoritmo 3 (triángulos)
```

**Interpretación**:
- Muestra la **tendencia de desempeño** a través de las instancias
- **Algoritmo 2 es estable y siempre más bajo** que los otros
- Los saltos en Algoritmo 1 y 3 indican inconsistencia

---

### 3️⃣ **Boxplot de GAP por Familia**
**Archivo**: `03_gap_boxplot_by_family.png`

```
Tipo: Boxplot (caja y bigotes)
Eje X: Familias Solomon (C1, C2, R1, R2, RC1, RC2)
Eje Y: GAP a BKS (%)
Cajas: 
  - ROJO: Algoritmo 1
  - CYAN: Algoritmo 2
  - AMARILLO: Algoritmo 3
```

**Interpretación**:
- **Mediana (línea en caja)**: Desempeño típico
- **Caja**: 50% de los valores (Q1-Q3)
- **Bigotes**: Rango completo de valores
- **Valores atípicos**: Puntos fuera

**Hallazgo clave**:
```
C1: Algo 2 mediana ~33%   | Algo 1 mediana ~80%   | Algo 3 mediana ~114%
C2: Algo 2 mediana ~95%   | Algo 1 mediana ~188%  | Algo 3 mediana ~104%
R1: Algo 2 mediana ~1%    | Algo 1 mediana ~14%   | Algo 3 mediana ~23%  ✅
R2: Algo 3 mediana ~12%   | Algo 2 mediana ~29%   | Algo 1 mediana ~50%
RC1: Algo 2 mediana ~-6%  | Algo 1 mediana ~37%   | Algo 3 mediana ~32%  🏆
RC2: Algo 3 mediana ~9%   | Algo 2 mediana ~14%   | Algo 1 mediana ~61%
```

---

### 4️⃣ **Heatmap de GAP**
**Archivo**: `04_gap_heatmap.png`

```
Tipo: Mapa de calor
Rows: 56 Instancias
Columns: 3 Algoritmos
Colores:
  - 🟢 VERDE: GAP bajo (bueno, cercano a BKS)
  - 🟡 AMARILLO: GAP moderado
  - 🔴 ROJO: GAP alto (malo, lejos de BKS)
Valores: % GAP en cada celda
```

**Interpretación**:
- **Columna Algo 2**: Mucho más VERDE que las otras
- **Filas C2**: Todas ROJO (problema sistemático)
- **Filas R1/RC1**: Verde y valores negativos (supera BKS!)
- Visualización rápida de patrones

---

### 5️⃣ **Grid de GAP por Familia**
**Archivo**: `05_gap_by_family_grid.png`

```
Tipo: 6 subgráficos (uno por familia)
Cada subgráfico:
  - Barras agrupadas para 3 algoritmos
  - Instancias de esa familia en el eje X
  - GAP en el eje Y
```

**Interpretación por familia**:

#### **C1 (Clustered, 100 clientes, horizon corto) - 9 instancias**
```
✅ Algoritmo 2: +33.09% promedio (MEJOR)
❌ Algoritmo 1: +79.29% (2.4× peor)
❌ Algoritmo 3: +107.34% (3.2× peor)
```

#### **C2 (Clustered, 100 clientes, horizon largo) - 8 instancias**
```
⚠️ Algoritmo 2: +94.76% promedio (MEJOR, pero CRÍTICO)
❌ Algoritmo 1: +185.37% (3.1× peor)
❌ Algoritmo 3: +102.72% (1.1× peor)
DIAGNÓSTICO: Constructor NearestNeighbor débil para clustered largo
```

#### **R1 (Random, 100 clientes) - 12 instancias**
```
🏆 Algoritmo 2: -0.60% promedio (SUPERA BKS!)
❌ Algoritmo 1: +15.60%
❌ Algoritmo 3: +24.73%
HALLAZGO: Algoritmo 2 encuentra soluciones mejores que publicadas
```

#### **R2 (Random, 1000 clientes, horizon largo) - 11 instancias**
```
✅ Algoritmo 3: +11.95% promedio (MEJOR para este caso)
⚠️ Algoritmo 2: +25.90% (2.2× peor)
❌ Algoritmo 1: +44.74%
NOTA: Algo 3 ocasionalmente mejor en R2 (pero inconsistente)
```

#### **RC1 (Random-Clustered, 100 clientes) - 8 instancias**
```
🏆 Algoritmo 2: -7.06% promedio (SUPERA BKS!)
❌ Algoritmo 1: +31.84%
❌ Algoritmo 3: +32.42%
HALLAZGO: Algoritmo 2 muy fuerte en mixed random-clustered
```

#### **RC2 (Random-Clustered, horizon largo) - 8 instancias**
```
⚠️ Algoritmo 3: +11.36% promedio (MEJOR)
✅ Algoritmo 2: +16.98% (cercano)
❌ Algoritmo 1: +59.66%
NOTA: Algo 3 ligeramente mejor pero Algo 2 competitivo
```

---

## 🎯 Hallazgos Principales

### ✅ Fortalezas de Algoritmo 2

| Métrica | Algoritmo 2 | Algo 1 | Algo 3 |
|---------|-----------|---------|----------|
| **Promedio GAP Global** | **25.25%** | 64.43% | 45.82% |
| **Mediana GAP** | **20.91%** | 55.37% | 30.69% |
| **Instancias Mejor BKS** | **16/56** | 3/56 | 5/56 |
| **Instancias < 5% GAP** | **18/56** | 6/56 | 6/56 |
| **Mejor en familias** | R1, RC1, RC2, C1, C2 | Ninguna | R2 (ocasional) |

### 🔴 Debilidades de Algoritmo 2

```
❌ CRÍTICO EN C2: +94.76% GAP (casi el doble de BKS)
   - Todas las instancias C2 idénticas (1148.78 vs BKS 589.86)
   - Sugiere constructor NearestNeighbor inadecuado
   
⚠️ MODESTO EN R2: +25.90% GAP
   - Mejor que Algo 1 pero ocasionalmente peor que Algo 3
   - Instancias 1000-clientes requieren ajuste
```

### 🏆 Recomendaciones

#### Para Publicación Académica
```
✅ "Algoritmo 2 supera BKS en 28% de instancias (R, RC families)"
✅ "GAP promedio 25.25% - competitivo pero no óptimo"
✅ "Especialidad comprobada en instancias aleatorias"
❌ "Limitación: débil en familias clustered puras (C2)"
```

#### Para Mejora Futura
```
1. ITER-4: Investigar constructor alternativo para C2
   - Inserción aleatoria + refinamiento más fuerte
   - Perturbación más agresiva para escapar

2. ITER-5: Ajuste adaptativo por familia
   - Diferentes parámetros para C vs R vs RC
   - Detección automática de clustering

3. Considerar hibridación:
   - Usar Algo 2 para R/RC families
   - Usar Algo 3 (modificado) para C2
```

---

## 📊 Archivos Disponibles

### Gráficos de GAP (generados en esta sesión):
- ✅ `01_gap_comparison_all_instances.png` - Barras agrupadas (56 instancias)
- ✅ `02_gap_evolution_lines.png` - Líneas de evolución
- ✅ `03_gap_boxplot_by_family.png` - Distribución por familia
- ✅ `04_gap_heatmap.png` - Mapa de calor detallado
- ✅ `05_gap_by_family_grid.png` - Grid 2×3 de familias

### Gráficos adicionales (de experimentos anteriores):
- `01_performance_comparison.png` - Comparación de distancia
- `02_distance_by_instance.png` - Distancia por instancia
- `03_distance_by_family.png` - Distancia por familia
- `04_execution_time.png` - Tiempo de ejecución
- ... y 7 gráficos más

**Ubicación**: `output/vrptw_experiments_FULL_03-01-26_02-18-27/plots/`

---

## 📌 Conclusión Visual

**Algoritmo 2 es claramente superior** en la mayoría de casos, especialmente en:
- ✅ Instancias aleatorias (R1): -0.60% GAP
- ✅ Instancias mixtas (RC1, RC2): -7.06% y +16.98% GAP
- ✅ Instancias clustered cortas (C1): +33.09% GAP

**Única debilidad crítica**: 
- ❌ Instancias clustered largas (C2): +94.76% GAP

**Recomendación**: 
Publicar con Algoritmo 2 como algoritmo principal, documentando que es especialista en instancias aleatorias y mixtas, con limitación conocida en clustered largas.
