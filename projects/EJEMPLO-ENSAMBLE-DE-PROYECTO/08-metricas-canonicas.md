---
title: "Métricas Canónicas VRPTW"
version: "1.0.0"
created: "2026-01-01"
---

# 8️⃣ MÉTRICAS CANÓNICAS

**Documento**: Métricas  
**Contenido**: Métricas jerárquicas por familia, análisis estadístico, cálculo de GAP

---

## Principio Fundamental

**Todas las métricas deben respetar la jerarquía del problema**:

1. Primero analizar K (número vehículos)
2. Luego analizar D (distancia), SOLO si K es igual
3. Nunca mezclar K y D en una métrica única

---

## MÉTRICAS PRIMARIAS (Objetivo: Minimizar K)

### K_mean: Número Promedio de Vehículos

$$K_{mean} = \frac{1}{n} \sum_{i=1}^{n} K_{final,i}$$

donde n = número de instancias de la familia.

**Uso**: Comparación principal entre familias  
**Interpretación**: Menor es mejor  

**Tabla Ejemplo**:

| Familia | K_mean | K_std |
|---------|--------|-------|
| C | 10.2 | 0.4 |
| R | 12.5 | 0.8 |
| RC | 13.7 | 0.9 |

---

### K_best: Mejor K Alcanzado

$$K_{best} = \min(K_{final}) \text{ para familia}$$

**Uso**: Capacidad máxima del algoritmo  
**Interpretación**: Cómo mejor de lo posible  

---

### %Instancias_K_BKS: Porcentaje con K Óptimo

$$\%\text{Instancias}_K = \frac{\text{# instancias donde } K_{min} = K_{BKS}}{\text{# total instancias}} \times 100$$

**Uso**: Métrica clave de efectividad  
**Interpretación**:
- 100% = Excelente
- ≥ 90% = Muy bueno
- ≥ 70% = Bueno
- < 70% = Necesita mejora

**Tabla Ejemplo**:

| Familia | %K_BKS |
|---------|--------|
| C | 100% |
| R | 83% |
| RC | 75% |

---

### K_std: Desviación Estándar de K

$$K_{std} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (K_i - K_{mean})^2}$$

**Uso**: Robustez y variabilidad  
**Interpretación**: K_std bajo = algoritmo estable

---

## MÉTRICAS SECUNDARIAS (Objetivo: Minimizar D, solo si K = K_BKS)

### Condición Crítica

**Todas las métricas D requieren**:

$$K_{final} = K_{BKS}$$

Si esta condición no se cumple, reportar "NA" (no aplica).

---

### D_mean_at_K: Distancia Promedio a K Óptimo

$$D_{mean@K} = \frac{1}{m} \sum_{i \in \{K_{final} = K_{BKS}\}} D_i$$

donde m = número instancias/ejecuciones con K = K_BKS.

**Uso**: Optimización secundaria  
**Nota Crítica**: Solo calcular cuando K = K_BKS

---

### %GAP: Porcentaje de GAP en Distancia

**Definición de GAP**:

$$\text{GAP}_{\text{distancia}} = D_{final} - D_{BKS}$$

**Definición de %GAP**:

$$\%\text{GAP} = \frac{D_{final} - D_{BKS}}{D_{BKS}} \times 100$$

**Condición**: Solo calcular si $K_{final} = K_{BKS}$

**Interpretación**:
- %GAP = 0% → Iguala BKS
- %GAP > 0% → Peor que BKS
- %GAP < 0% → Mejora BKS (raro)

**Tabla Ejemplo**:

| Familia | %GAP_mean | %GAP_std |
|---------|-----------|----------|
| C | 0.08% | 0.05% |
| R | 0.44% | 0.22% |
| RC | 0.61% | 0.38% |

---

### %GAP_std: Desviación del GAP

$$\%\text{GAP}_{std} = \sqrt{\frac{1}{m} \sum_{i \in \{K=K_{BKS}\}} (\%\text{GAP}_i - \%\text{GAP}_{mean})^2}$$

**Uso**: Estabilidad de optimización secundaria  
**Interpretación**: Bajo %GAP_std = consistente

---

## MÉTRICAS DE ROBUSTEZ

### %Ejecuciones_K_BKS: Robustez del Objetivo Primario

Para cada instancia, calcular qué % de sus ejecuciones alcanzan K_BKS:

$$\%\text{Ejecuciones}_K = \frac{1}{n} \sum_{i=1}^{n} \left( \frac{\text{# ejecuciones con } K = K_{BKS}}{30} \times 100 \right)$$

**Interpretación**:
- ≥ 90% = Muy robusto
- ≥ 70% = Robusto
- ≥ 50% = Moderado
- < 50% = Poco robusto

---

## MÉTRICAS DE CONVERGENCIA

### Iteraciones hasta K Óptimo

$$\text{Iter}\_to\_K = \frac{1}{m} \sum_{i \in \{alcanzó K_{BKS}\}} \text{iteration}\_to\_K\_{BKS}_i$$

**Uso**: Dificultad de la familia  
**Interpretación**: 
- Familias C: típicamente 50-100 iteraciones
- Familias R/RC: típicamente 150-300 iteraciones

---

### Tiempo hasta K Óptimo

$$\text{Time}\_to\_K = \frac{1}{m} \sum_{i \in \{alcanzó K_{BKS}\}} \text{time}\_to\_K\_{BKS}_i$$

**Uso**: Eficiencia temporal

---

## MÉTRICAS DE EFICIENCIA

### Tiempo Promedio Total

$$T_{avg} = \frac{1}{n \times 30} \sum_{i,j} T_{i,j}$$

**Interpretación**:
- < 5 seg = Muy rápido
- 5-10 seg = Rápido
- 10-20 seg = Moderado
- > 20 seg = Lento

---

## MÉTRICAS DE FACTIBILIDAD (VALIDACIÓN)

### Violaciones de Ventanas de Tiempo

$$\text{Violations}_{time} = |\{(i,j) : arrival\_time_{j} \notin [a_j, b_j]\}|$$

**Condición Canónica**: Debe ser 0 en TODAS las soluciones  
**Si > 0**: Solución infactible

---

### Violaciones de Capacidad

$$\text{Violations}_{capacity} = |\{rutas : carga > Q\}|$$

**Condición Canónica**: Debe ser 0 en TODAS las soluciones  
**Si > 0**: Solución infactible

---

## RESUMEN: TABLA MÍNIMA POR FAMILIA

Para cada familia (C, R, RC), reportar:

| Métrica | C | R | RC |
|---------|---|---|----|
| **K_mean** | 10.2 | 12.5 | 13.7 |
| **K_std** | 0.4 | 0.8 | 0.9 |
| **%Instancias_K_BKS** | 100% | 83% | 75% |
| **D_mean@K_BKS** | 812.3 | 1312.5 | 1450.2 |
| **%GAP_mean** | 0.08% | 0.44% | 0.61% |
| **%GAP_std** | 0.05% | 0.22% | 0.38% |
| **%Ejecuciones_K_BKS** | 96% | 81% | 76% |
| **T_avg (seg)** | 5.1 | 7.8 | 8.2 |

---

## ¿QUÉ NUNCA REPORTAR?

❌ Métricas ponderadas como: $w_1 K + w_2 D$  
❌ Comparaciones de D entre instancias con K diferente  
❌ GAP sin verificar condición K = K_BKS  
❌ Multiobjeto Pareto (NO aplica a Solomon jerárquico)  
❌ Promedio de %GAP incluyendo ejecuciones con K > K_BKS  

---

## ANÁLISIS POR FAMILIA

Realizar comparación entre C, R, RC:

**Pregunta 1**: ¿Qué familia es más fácil?  
→ La con menor K_mean

**Pregunta 2**: ¿Dónde es más consistente el algoritmo?  
→ La con mayor %Instancias_K_BKS

**Pregunta 3**: ¿Cuál es la dificultad de optimizar D?  
→ Comparar %GAP_mean entre familias

---

## COMPARACIÓN ENTRE ALGORITMOS

Realizar test estadístico sobre:

1. **Kruskal-Wallis** en K (comparación múltiple de 3 algoritmos)
2. **Wilcoxon** entre los dos mejores en K
3. **Cohen's d** para tamaño del efecto

**Resultados**:
- p-value < 0.05 → Diferencia significativa
- p-value ≥ 0.05 → No hay diferencia significativa

---

**Siguiente documento**: [09-outputs-estructura.md](09-outputs-estructura.md)  
**Volver a**: [INDEX.md](INDEX.md)
