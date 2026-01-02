---
title: "Función Fitness Canónica y Gráficos"
version: "1.0.0"
created: "2026-01-01"
---

# 7️⃣ FUNCIÓN FITNESS CANÓNICA

**Documento**: Fitness  
**Contenido**: Función fitness jerárquica, gráficos canónicos

---

## Naturaleza del Problema

El VRPTW Solomon es un **problema de optimización jerárquica** (NO multiobjetivo Pareto):

- **Objetivo Primario (máxima prioridad)**: Minimizar número vehículos K
- **Objetivo Secundario (condicionado)**: Minimizar distancia D, solo cuando K es igual

**Esta jerarquía es fundamental y no debe modificarse.**

---

## Definición Formal

### Función Fitness Lexicográfica

$$\text{Fitness}(S) = (K(S), D(S))$$

donde:
- $K(S)$ = número de vehículos en solución $S$
- $D(S)$ = distancia total en solución $S$

### Regla de Comparación

Dadas dos soluciones $S_1$ y $S_2$ factibles:

$$S_1 \text{ es mejor que } S_2 \iff K(S_1) < K(S_2) \text{ ó } (K(S_1) = K(S_2) \text{ ∧ } D(S_1) < D(S_2))$$

**Corolario Crítico**: 

Una solución con menor distancia pero mayor número de vehículos es **SIEMPRE inferior**, sin importar la magnitud de la diferencia en distancia.

---

## Dominio de Definición

La función fitness está definida **únicamente sobre soluciones factibles**:

- ✅ Todas las ventanas de tiempo respetadas
- ✅ Todas las restricciones de capacidad respetadas
- ✅ Todos los clientes visitados exactamente una vez
- ✅ Todas las rutas inician y terminan en depósito

**Las soluciones infactibles no tienen fitness definido.**

---

## Implementación Técnica Equivalente

Aunque el fitness es conceptualmente lexicográfico, puede implementarse como:

$$\text{Fitness}(S) = M \cdot K(S) + D(S)$$

donde $M$ es una constante suficientemente grande (ej: $M = 100,000$).

**NOTA CRÍTICA**: 
- Esta es **solo una implementación técnica** para cálculos rápidos
- El **criterio real sigue siendo jerárquico**, no ponderado
- En el paper, describir como **jerárquico**, no como suma ponderada

---

## Compatibilidad con GRASP

GRASP es **completamente compatible** con esta función fitness porque:

1. La fase constructiva genera soluciones factibles
2. La búsqueda local opera dentro del espacio factible
3. La aceptación de movimientos respeta la comparación jerárquica

**No se requiere modificación del fitness para aplicar GRASP canónicamente.**

---

## Uso en Evaluación Experimental

### Reporte de Fitness

En cualquier tabla o figura:

1. **K se reporta SIEMPRE como métrica principal** (primera columna/eje)
2. **D se reporta SOLO cuando K coincide** (K = K_BKS)
3. **Nunca comparar distancias entre soluciones con K diferente**

### Ejemplo Correcto

| Algoritmo | Familia | K_mean | D_mean@K_BKS | %GAP |
|-----------|---------|--------|--------------|------|
| Alg-1 | C | 10.2 | 812.3 | 2.1% |
| Alg-1 | R | 12.8 | 1312.5 | 4.3% |

### Ejemplo INCORRECTO ❌

```
"Algoritmo 1 conseguiu 1200 de distancia con 14 vehículos,
mientras que Algoritmo 2 consiguió 1150 con 15 vehículos.
Algoritmo 2 es mejor."

❌ INCORRECTO: Nunca comparar D si K diferente
```

---

## Gráficos Canónicos para VRPTW (11 tipos)

### 1. Convergencia en K (Escalonado)

**Tipo**: Línea escalonada  
**Qué**: K(t) mejor solución hasta iteración t  
**Propósito**: Mostrar mejora en objetivo primario  
**Esperado**: Descensos discretos en K

### 2. Convergencia en D (Solo a K Constante)

**Tipo**: Línea continua  
**Qué**: D(t) mejor solución, SOLO desde que K = K_final  
**Propósito**: Mostrar mejora en objetivo secundario  
**Nota**: Eje X comienza donde K se estabiliza

### 3. Tiempo vs Calidad Jerárquica

**Tipo**: Línea con dos ejes  
**Eje izquierdo**: K(tiempo)  
**Eje derecho**: D(tiempo) solo a K óptimo  
**Propósito**: Comportamiento anytime respetando jerarquía

### 4. Boxplot de K por Algoritmo

**Tipo**: Boxplot  
**Qué**: Distribución de K_final por algoritmo  
**Propósito**: Robustez en objetivo primario  
**Etiquetas**: Incluir % que alcanzan K_BKS

### 5. Boxplot de D (Solo a K_BKS)

**Tipo**: Boxplot  
**Qué**: Distribución de D, SOLO ejecuciones con K = K_BKS  
**Propósito**: Estabilidad en objetivo secundario  
**Nota**: Excluir ejecuciones con K > K_BKS

### 6. Barras de Gap por Instancia

**Tipo**: Barras  
**Panel superior**: Diferencia en K (K_sol - K_BKS)  
**Panel inferior**: %GAP en D, SOLO si K_sol = K_BKS  
**Propósito**: Calidad absoluta respetando jerarquía

### 7. Análisis por Familia

**Tipo**: Barras agrupadas  
**Grupo 1**: K_mean por familia  
**Grupo 2**: %GAP_mean por familia (solo a K_BKS)  
**Propósito**: Comparación inter-familias

### 8. Performance by Size

**Tipo**: Línea o barras  
**Categorías**: Instancias pequeñas (25-50), medianas (50-75), grandes (75-100)  
**Qué**: K y D por tamaño  
**Propósito**: Escalabilidad

### 9. Visualización de Rutas

**Tipo**: 2D scatter  
**Qué**: Clientes como puntos, rutas como líneas coloreadas  
**Título**: Incluir "K={}, D={}, GAP={}"  
**Propósito**: Validación visual, factibilidad

### 10. Validación de Ventanas Temporales

**Tipo**: Scatter o histograma  
**Qué**: Tiempo llegada vs ventana permitida por cliente  
**Propósito**: Verificación de factibilidad (restricción dura)  
**Nota**: Gráfico de validación, todas deben respetar ventana

### 11. Sensibilidad del Parámetro α

**Tipo**: Línea con dos ejes  
**Eje X**: Valores de α ∈ [0, 1]  
**Eje izquierdo**: K_mean(α)  
**Eje derecho**: %GAP_mean(α) a K_BKS  
**Propósito**: Impacto de parámetro GRASP

---

## Conjunto Mínimo para Publicación

Un artículo sólido debe incluir:

- ✅ Gráfico convergencia en K (escalonado)
- ✅ Gráfico convergencia en D (a K constante)
- ✅ Boxplot de K, Boxplot de D (condicionado)
- ✅ Análisis de gap (solo K_BKS)
- ✅ Comparación tiempo-calidad jerárquica
- ✅ Análisis por familia (K y D separados)
- ✅ Visualización de rutas (mínimo 2)

---

## Resumen: Propiedades de Fitness Canónica

| Propiedad | Valor |
|-----------|-------|
| **Tipo** | Lexicográfica |
| **Dominio** | Soluciones factibles |
| **Jerarquía** | K ≫ D (estricta) |
| **Peso** | Sin pesos (binaria en K) |
| **Multiobjetivo** | NO (jerárquico) |
| **Compatible GRASP** | Sí |
| **Compatible Solomon** | 100% |

---

**Siguiente documento**: [08-metricas-canonicas.md](08-metricas-canonicas.md)  
**Volver a**: [INDEX.md](INDEX.md)
