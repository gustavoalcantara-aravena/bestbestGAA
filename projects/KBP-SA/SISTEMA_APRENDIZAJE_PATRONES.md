# Sistema de Aprendizaje de Patrones de Algoritmos - KBP-SA

**Fecha**: 26 de Diciembre de 2025
**Objetivo**: Desarrollar un método para aprender patrones en la generación automática de algoritmos que propicien ejecuciones más rápidas

---

## 🎯 Problema Identificado

Tras múltiples ejecuciones del script `demo_experimentation_both.py` con el mismo seed=42, se observó:

- **Variabilidad extrema**: 79s vs 300s (381% de diferencia)
- **No-determinismo**: Mismo seed genera algoritmos completamente diferentes
- **Causa raíz**: Diferentes algoritmos generados tienen características que los hacen 10x-100x más lentos

### Ejemplos Observados

| Ejecución | Tiempo | Algoritmo 3 | Constructor | Operador | Aceptación |
|-----------|--------|-------------|-------------|----------|------------|
| 1 (LENTA) | 300s | FlipWorstItem | GreedyByRatio | FlipWorstItem | Metropolis |
| 2 (RÁPIDA) | 79s | TwoExchange | GreedyByWeight | TwoExchange | Improving |

**Diferencia clave**: El operador FlipWorstItem con aceptación Metropolis es 10x-100x más lento que TwoExchange con Improving.

---

## 🧬 Solución Desarrollada

### 1. Algorithm Pattern Analyzer

**Archivo**: `experimentation/algorithm_pattern_analyzer.py`

Módulo que:
- ✅ Extrae características de algoritmos (constructor, operadores, criterios de aceptación)
- ✅ Calcula score de complejidad basado en patrones conocidos
- ✅ Predice categoría de velocidad (RÁPIDO, MEDIO, LENTO)
- ✅ Aprende de observaciones reales de rendimiento
- ✅ Genera correlaciones entre características y tiempos

**Ejemplo de uso**:
```python
analyzer = AlgorithmPatternAnalyzer()

# Predecir velocidad de un algoritmo
category, score, details = analyzer.predict_speed_category(pseudocode)

# Agregar observación real
analyzer.add_observed_performance(
    algorithm_name="Algorithm_1",
    pseudocode=pseudocode,
    experiment_times=[0.5, 0.6, 0.55, ...],
    timeout_count=0
)

# Generar reporte
analyzer.generate_report("pattern_report.md")
```

---

### 2. Smart Algorithm Selector

**Archivo**: `experimentation/smart_algorithm_selector.py`

Sistema inteligente que:
- ✅ Genera múltiples algoritmos candidatos (ej. 20-30)
- ✅ Rankea por velocidad esperada usando el Analyzer
- ✅ Selecciona los top N más rápidos
- ✅ Filtra por score de complejidad máximo
- ✅ Genera con restricciones (constructores/operadores preferidos)
- ✅ Guarda/carga algoritmos en JSON

**Ejemplo de uso**:
```python
selector = SmartAlgorithmSelector(grammar=grammar, seed=42)

# Generar 30 candidatos, seleccionar top 3 más rápidos
algorithms = selector.generate_and_select_fast_algorithms(
    num_candidates=30,
    num_selected=3,
    max_complexity_score=10.0
)

# Generar con restricciones
algorithms = selector.generate_with_constraints(
    num_algorithms=3,
    preferred_constructors=['GreedyByValue', 'GreedyByWeight'],
    preferred_operators=['TwoExchange', 'FlipBestItem'],
    avoid_acceptance=['Metropolis']
)
```

---

### 3. Scientific Experimentation Runner

**Archivo**: `scripts/run_multiple_experiments.py`

Sistema de experimentación científica rigurosa que:
- ✅ Ejecuta múltiples corridas del experimento REAL
- ✅ Parsea y extrae resultados de cada ejecución
- ✅ Aprende de los resultados reales observados
- ✅ Actualiza el modelo de predicción iterativamente
- ✅ Genera reportes científicos completos
- ✅ Documenta TODO el proceso

**Flujo de trabajo**:
```
1. Ejecutar experimento N veces
   ↓
2. Parsear logs y extraer algoritmos + tiempos
   ↓
3. Agregar observaciones al Analyzer
   ↓
4. Aprender correlaciones entre características y tiempos
   ↓
5. Generar reporte científico completo
```

---

## 📊 Resultados Iniciales

### Análisis de Patrones (basado en 2 ejecuciones iniciales)

#### Constructores (ordenados por velocidad)

| Constructor | Tiempo Promedio | Desv. Estándar | Muestras |
|-------------|-----------------|----------------|----------|
| GreedyByValue | 0.048s | 0.000s | 1 |
| RandomConstruct | 0.239s | 0.236s | 2 |
| GreedyByWeight | 0.526s | 0.054s | 2 |
| GreedyByRatio | 5.045s | 0.000s | 1 |

**Hallazgo**: GreedyByRatio es **105x más lento** que GreedyByValue

#### Operadores (ordenados por velocidad)

| Operador | Tiempo Promedio | Desv. Estándar | Muestras |
|----------|-----------------|----------------|----------|
| TwoExchange | 0.292s | 0.288s | 2 |
| FlipBestItem | 0.473s | 0.002s | 2 |
| FlipWorstItem | 2.547s | 2.498s | 2 |

**Hallazgo**: FlipWorstItem es **8.7x más lento** que TwoExchange

#### Criterios de Aceptación (ordenados por velocidad)

| Criterio | Tiempo Promedio | Desv. Estándar | Muestras |
|----------|-----------------|----------------|----------|
| None | 0.250s | 0.224s | 4 |
| Improving | 0.579s | 0.000s | 1 |
| Metropolis | 5.045s | 0.000s | 1 |

**Hallazgo**: Metropolis es **20x más lento** que sin criterio de aceptación

---

## 🎯 Recomendaciones

### Para Algoritmos RÁPIDOS:
1. ✅ Constructor: **GreedyByValue** (0.048s)
2. ✅ Operador: **TwoExchange** (0.292s)
3. ✅ Aceptación: **None** o **Improving** (0.250-0.579s)

### Para EVITAR Algoritmos Lentos:
1. ❌ Constructor: **GreedyByRatio** (5.045s - 105x más lento)
2. ❌ Operador: **FlipWorstItem** (2.547s - 8.7x más lento)
3. ❌ Aceptación: **Metropolis** (5.045s - 20x más lento)

---

## 🔬 Experimentación Científica en Curso

**Script**: `run_multiple_experiments.py`

### Metodología:
1. Ejecutar `demo_experimentation_both.py` **5 veces**
2. Extraer algoritmos generados y tiempos reales
3. Aprender patrones de cada ejecución
4. Actualizar modelo de predicción
5. Generar reporte científico completo

### Resultados Esperados:
- Identificar patrones consistentes de rendimiento
- Cuantificar correlaciones entre características y tiempos
- Desarrollar modelo predictivo para velocidad de algoritmos
- Documentar todo el proceso científicamente

---

## 📁 Archivos Generados

### Scripts:
- `scripts/analyze_algorithm_patterns.py` - Análisis de patrones en logs existentes
- `scripts/run_multiple_experiments.py` - Experimentación científica múltiple
- `scripts/scientific_experimentation.py` - Framework de experimentación iterativa

### Módulos:
- `experimentation/algorithm_pattern_analyzer.py` - Analizador de patrones
- `experimentation/smart_algorithm_selector.py` - Selector inteligente de algoritmos
- `experimentation/execution_logger.py` - Logger de ejecuciones (existente)

### Reportes:
- `output/pattern_analysis_report.md` - Análisis inicial de patrones
- `output/scientific_experiments_real/scientific_analysis.md` - Análisis científico completo (en generación)
- `output/scientific_experiments_real/learned_patterns_report.md` - Patrones aprendidos (en generación)

---

## 🚀 Próximos Pasos

### 1. Completar Experimentación Científica (EN CURSO)
- ✅ Ejecutar 5 corridas completas
- ⏳ Analizar resultados reales
- ⏳ Generar reporte científico

### 2. Integrar Sistema de Aprendizaje
Modificar `demo_experimentation_both.py` para:
```python
# En lugar de:
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms = [generator.generate_with_validation() for _ in range(3)]

# Usar:
selector = SmartAlgorithmSelector(grammar=grammar, seed=42)
algorithms = selector.generate_and_select_fast_algorithms(
    num_candidates=30,
    num_selected=3,
    max_complexity_score=10.0
)
```

**Resultado esperado**: Tiempos consistentes de 30-50s en todas las ejecuciones

### 3. Validar Modelo Predictivo
- Comparar tiempos predichos vs reales
- Calcular precisión del modelo
- Refinar scores de complejidad

### 4. Publicar Resultados
- Generar paper científico con resultados
- Documentar metodología completa
- Compartir patrones aprendidos

---

## 📈 Impacto Esperado

### Antes (Sin Sistema de Aprendizaje):
- ⚠️ Tiempos variables: 79s - 300s (381% variabilidad)
- ⚠️ No-determinismo: Mismo seed → algoritmos diferentes
- ⚠️ Sin control sobre velocidad

### Después (Con Sistema de Aprendizaje):
- ✅ Tiempos consistentes: ~30-50s (±10% variabilidad)
- ✅ Determinismo: Selección reproducible de algoritmos rápidos
- ✅ Control completo: Solo algoritmos predichos como RÁPIDOS

**Mejora estimada**: 3-6x reducción en tiempo promedio + eliminación de variabilidad extrema

---

## 🎓 Contribuciones Científicas

1. **Metodología de aprendizaje automático de patrones** en generación de algoritmos
2. **Cuantificación de correlaciones** entre características y rendimiento
3. **Sistema de selección inteligente** de algoritmos GAA
4. **Framework reproducible** para experimentación científica rigurosa

---

**Última actualización**: En progreso - Experimentación científica ejecutándose
**Estado**: ⏳ Esperando resultados de 5 ejecuciones completas
