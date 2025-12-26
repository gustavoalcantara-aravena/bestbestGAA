# Metodología Experimental: Aprendizaje de Patrones de Algoritmos

**Fecha**: 26 de Diciembre de 2025
**Investigador**: Claude (IA)
**Objetivo**: Identificar qué características de algoritmos generados automáticamente propician tiempos de ejecución óptimos

---

## 🎯 Hipótesis

La variabilidad extrema en tiempos de ejecución (34s vs 300s) con el mismo seed=42 se debe a que diferentes algoritmos generados tienen características específicas que los hacen significativamente más rápidos o lentos.

**Hipótesis específica**: Ciertos constructores, operadores y criterios de aceptación correlacionan fuertemente con tiempos de ejecución bajos.

---

## 🔬 Diseño Experimental

### Fase 1: Experimentación Masiva (EN CURSO)

#### Configuración:
- **Script**: `demo_experimentation_both.py` (original, sin modificaciones)
- **Número de corridas**: 15
- **Timeout**: 120 segundos
- **Seed**: 42 (original)
- **Meta óptima**: ≤40 segundos (basado en observaciones previas de ~34s)

#### Criterios de Evaluación:
1. **RÁPIDA**: ≤40s - Tiempo óptimo observado
2. **MEDIA**: 40-80s - Tiempo aceptable
3. **LENTA**: 80-120s - Tiempo subóptimo
4. **TIMEOUT**: >120s - Descartado como demasiado lento

#### Variables Medidas:
- Tiempo total de ejecución
- Algoritmos generados (3 por corrida)
- Características de cada algoritmo:
  - Constructor (GreedyByRatio, GreedyByWeight, GreedyByValue, RandomConstruct)
  - Operadores (FlipWorstItem, FlipBestItem, TwoExchange, OneExchange)
  - Criterio de aceptación (Metropolis, Improving, None)
  - Presupuesto de iteraciones
  - Límite de estancamiento

---

## 📊 Metodología de Análisis

### 1. Clasificación de Corridas

Cada corrida se clasifica según su tiempo total:
```
RÁPIDA  (≤40s):   Algoritmos generados → "Patrones óptimos"
MEDIA   (40-80s): Algoritmos generados → "Patrones aceptables"
LENTA   (80-120s): Algoritmos generados → "Patrones subóptimos"
TIMEOUT (>120s):  Algoritmos generados → "Patrones problemáticos"
```

### 2. Extracción de Características

Para cada algoritmo en cada corrida:
```python
features = {
    'constructor': str,          # Tipo de constructor voraz
    'operators': List[str],      # Lista de operadores usados
    'acceptance': str or None,   # Criterio de aceptación
    'loop_budget': int or None,  # Iteraciones del bucle
    'stagnation': int or None,   # Límite de estancamiento
    'complexity_score': float    # Score calculado de complejidad
}
```

### 3. Análisis Estadístico

#### A. Distribución de Tiempos
- Media, mediana, desviación estándar
- Percentiles (p25, p50, p75, p90)
- Identificación de outliers

#### B. Frecuencia de Características
Para corridas RÁPIDAS vs LENTAS, calcular:
```
Frecuencia(característica) = count(característica) / total_algoritmos
```

#### C. Correlación Característica-Tiempo
Para cada característica:
```
Tiempo_promedio(característica) = mean(tiempos donde aparece característica)
```

#### D. Patrones Combinados
Identificar combinaciones de características que aparecen juntas en corridas rápidas:
```
Pattern = (Constructor, Operador, Aceptación)
Frecuencia_en_rápidas vs Frecuencia_en_lentas
```

---

## 📈 Métricas de Éxito

### Métrica 1: Tasa de Éxito
```
Tasa_éxito = (Corridas_exitosas / Total_corridas) × 100%
```
**Objetivo**: ≥80% de corridas completadas en <120s

### Métrica 2: Tasa de Óptimos
```
Tasa_óptima = (Corridas_rápidas / Corridas_exitosas) × 100%
```
**Objetivo**: ≥30% de corridas en ≤40s

### Métrica 3: Precisión de Predicción
```
Precisión = (Predicciones_correctas / Total_predicciones) × 100%
```
**Objetivo**: ≥90% de precisión en categorizar RÁPIDO/MEDIO/LENTO

### Métrica 4: Factor de Mejora
```
Mejora = Tiempo_promedio_sin_filtro / Tiempo_promedio_con_filtro
```
**Objetivo**: ≥2x mejora al usar selector inteligente

---

## 🔍 Análisis Comparativo

### Comparación Rápidas vs Lentas

| Aspecto | Corridas RÁPIDAS | Corridas LENTAS |
|---------|------------------|-----------------|
| **Constructores** | Distribución de frecuencia | Distribución de frecuencia |
| **Operadores** | Distribución de frecuencia | Distribución de frecuencia |
| **Aceptación** | Distribución de frecuencia | Distribución de frecuencia |
| **Complejidad** | Score promedio | Score promedio |

### Tests Estadísticos

1. **Test Chi-cuadrado**: Independencia entre característica y categoría de velocidad
2. **Test T de Student**: Diferencia significativa entre tiempos RÁPIDAS vs LENTAS
3. **ANOVA**: Diferencia entre múltiples categorías de características

---

## 🎓 Protocolo de Documentación

### Para cada corrida:
1. ✅ Timestamp de inicio
2. ✅ Log completo de salida
3. ✅ Tiempo total de ejecución
4. ✅ Algoritmos generados (pseudocódigo completo)
5. ✅ Características extraídas
6. ✅ Clasificación (RÁPIDA/MEDIA/LENTA/TIMEOUT)

### Reportes generados:
1. `results_complete.json` - Datos crudos de todas las corridas
2. `pattern_learning_report.md` - Análisis de patrones aprendidos
3. `comparative_analysis.md` - Comparación rápidas vs lentas
4. `logs/run_XX_timestamp.log` - Log individual de cada corrida

---

## 🚀 Fases del Proyecto

### ✅ Fase 0: Exploración Inicial (COMPLETADO)
- Identificación del problema de variabilidad
- Análisis de 2 ejecuciones (79s vs 300s)
- Identificación de causa raíz: algoritmos generados diferentes

### ✅ Fase 1: Desarrollo de Herramientas (COMPLETADO)
- AlgorithmPatternAnalyzer
- SmartAlgorithmSelector
- Scripts de análisis

### ⏳ Fase 2: Experimentación Masiva (EN CURSO)
- 15 corridas con timeout 120s
- Extracción de patrones
- Análisis estadístico

### 🔜 Fase 3: Validación (PRÓXIMO)
- Implementar selector inteligente en script principal
- Ejecutar 10 corridas adicionales con selección inteligente
- Validar mejora de tiempos

### 🔜 Fase 4: Publicación (FUTURO)
- Documentación completa de resultados
- Paper científico
- Integración permanente en el framework

---

## 📊 Resultados Esperados

### Hallazgos Anticipados:

1. **Constructor más rápido**: GreedyByValue o RandomConstruct
   - Hipótesis: Menos overhead computacional
   - Evidencia preliminar: GreedyByValue @ 0.048s

2. **Operador más rápido**: TwoExchange
   - Hipótesis: Balance entre exploración y eficiencia
   - Evidencia preliminar: TwoExchange @ 0.292s

3. **Mejor criterio de aceptación**: None o Improving
   - Hipótesis: Metropolis acepta soluciones peores, aumentando evaluaciones
   - Evidencia preliminar: None @ 0.250s vs Metropolis @ 5.045s

4. **Combinación óptima predicha**:
   ```
   Constructor:  GreedyByValue
   Operador:     TwoExchange
   Aceptación:   None o Improving
   ───────────────────────────────
   Tiempo estimado: 30-50s
   ```

5. **Combinación a evitar**:
   ```
   Constructor:  GreedyByRatio
   Operador:     FlipWorstItem
   Aceptación:   Metropolis
   ───────────────────────────────
   Tiempo estimado: >120s (timeout probable)
   ```

---

## 🎯 Aplicación Práctica

### Una vez completado el aprendizaje:

1. **Modificar generación de algoritmos**:
   ```python
   # En lugar de:
   algorithms = [generator.generate_with_validation() for _ in range(3)]

   # Usar:
   selector = SmartAlgorithmSelector(grammar, seed)
   algorithms = selector.generate_and_select_fast_algorithms(
       num_candidates=30,
       num_selected=3,
       max_complexity_score=10.0
   )
   ```

2. **Resultado esperado**:
   - Tiempos consistentes: 30-50s
   - Eliminación de outliers extremos (>120s)
   - Reducción de variabilidad de 381% → <30%

3. **Validación**:
   - 10 corridas adicionales con selector inteligente
   - Todas deberían completar en 30-60s
   - Variabilidad < 2x (vs 4x actual)

---

## 📝 Notas Metodológicas

### Limitaciones:
1. **Muestra**: 15 corridas puede no capturar todos los patrones
2. **Seed fijo**: Solo seed=42, no generalizable a otros seeds
3. **Instancias fijas**: Mismas 31 instancias en todas las corridas

### Supuestos:
1. El non-determinismo con seed=42 persiste (validado previamente)
2. Las características de algoritmos son la variable principal
3. Factores externos (CPU, memoria) son constantes

### Validez:
- **Interna**: Alta (experimento controlado, mismo entorno)
- **Externa**: Media (limitado a este framework, seed=42)
- **Constructo**: Alta (medimos exactamente lo que queremos)

---

**Estado**: ⏳ Fase 2 en ejecución (Experimentación Masiva)
**Próxima actualización**: Al completar las 15 corridas
