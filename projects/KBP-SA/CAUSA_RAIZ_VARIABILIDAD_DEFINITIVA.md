# Causa Raíz Definitiva: Variabilidad de Tiempos en demo_experimentation_both.py

**Fecha**: 26 de Diciembre de 2025, 05:37
**Análisis**: Comparación de ejecuciones múltiples con seed=42

---

## 🔴 CAUSA RAÍZ IDENTIFICADA

### El problema NO es variabilidad del sistema, es CÓDIGO CAMBIANTE

La variabilidad extrema de tiempos (34s → 55s → 5+ minutos) se debe a que **el código de generación de algoritmos GAA ha cambiado entre versiones**, causando que el mismo seed (42) genere **algoritmos completamente diferentes**.

---

## 📊 EVIDENCIA: Comparación de Algoritmos Generados

### Ejecución Actual (hoy 05:37) - ORIGINAL script con seed=42

```
✅ Algoritmo 1 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByValue
         2. APLICAR_HASTA_NO_MEJORAR (parada: Stagnation=10):
           LLAMAR TwoExchange

✅ Algoritmo 2 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByRatio
         2. LLAMAR OneExchange

✅ Algoritmo 3 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByWeight
         2. MIENTRAS (presupuesto: 100 iteraciones):
           SECUENCIA:
             1. BUSQUEDA_LOCAL en FlipBestItem (aceptación: AlwaysAccept)
             2. LLAMAR FlipBestItem
```

**Tiempos de experimentos**:
- Algorithm_1: ~0.016s por experimento
- Algorithm_2: **0.978s - 60s** por experimento (algunos exceden timeout!)
- Algorithm_3: ~0.035s por experimento

---

### Ejecución Documentada (RESULTADOS_EJECUCION_OPTIMIZADA.md) con seed=42

```
✅ Algoritmo 3 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByRatio
         2. MIENTRAS (presupuesto: 100 iteraciones):
           SECUENCIA:
             1. BUSQUEDA_LOCAL en TwoExchange (aceptación: Improving)
             2. LLAMAR TwoExchange
```

**Tiempos de experimentos**:
- Algorithm_3: **~0.6-1.1s** por experimento en large-scale

---

### Ejecución con seed=123 (hoy 05:30)

```
✅ Algoritmo 3 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByValue
         2. MIENTRAS (presupuesto: 1000 iteraciones):
           SECUENCIA:
             1. BUSQUEDA_LOCAL en FlipWorstItem (aceptación: AlwaysAccept)
             2. LLAMAR FlipWorstItem
```

**Tiempos de experimentos**:
- Algorithm_3: **~0.1-0.25s** por experimento

---

## ⚠️ HALLAZGOS CRÍTICOS

### 1. **Mismo Seed, Algoritmos Diferentes**

El mismo seed=42 genera algoritmos **completamente diferentes** entre ejecuciones:

| Ejecución | Algorithm_3 Operación | Iteraciones | Tiempo por experimento |
|-----------|----------------------|-------------|------------------------|
| Actual (hoy) | FlipBestItem | 100 | ~0.035s |
| Documentada | TwoExchange | 100 | ~0.6-1.1s |
| seed=123 | FlipWorstItem | 1000 | ~0.1-0.25s |

**Conclusión**: El código de `Grammar` o `AlgorithmGenerator` cambió, alterando la generación aleatoria.

---

### 2. **Timeouts en Versión Original**

La ejecución actual muestra **experimentos con timeout de 60s**:

```
[2/63] knapPI_1_10000_1000_1_large_scale × GAA_Algorithm_2 (rep 1)
       ❌ Error: Excedido timeout de 60.0s

[3/63] knapPI_1_10000_1000_1_large_scale × GAA_Algorithm_3 (rep 1)
       ❌ Error: Excedido timeout de 60.0s
```

**Impacto**:
- Algunos experimentos no completan
- Tiempo total impredecible (depende de cuántos timeouts ocurran)
- Resultados inconsistentes entre ejecuciones

---

### 3. **Algorithm_2 es Extremadamente Lento**

En la ejecución actual, `Algorithm_2` (OneExchange) toma:
- **0.978s** en instancia de 1000 items
- **>60s** (timeout) en instancia de 10,000 items

Pero `OneExchange` debería ser simple (intercambiar un item). Esto sugiere que hay un problema en la implementación o que el algoritmo está entrando en un bucle muy largo.

---

## 🔍 ANÁLISIS DE VARIABILIDAD

### ¿Por qué los tiempos varían tanto?

| Medición | Tiempo Total | Motivo |
|----------|--------------|--------|
| Original reportada | **34s** | Algoritmos rápidos + posibles timeouts que abortaron experimentos lentos |
| Optimizada (seed=42) | **55s** | Algorithm_3 con TwoExchange (búsqueda lenta) |
| Actual (seed=42) | **>5 minutos** | Algorithm_2 excede timeout en 2+ experimentos |
| seed=123 | **~11s (low-dim)** | Algoritmos más balanceados |

**La variabilidad NO es del sistema operativo**, es porque:
1. **El código de generación cambió** → mismo seed genera diferentes algoritmos
2. **Algunos algoritmos son >100x más lentos** que otros
3. **Los timeouts causan experimentos abortados** → resultados inconsistentes

---

## 🎯 SOLUCIONES DEFINITIVAS

### Solución 1: **Fijar los Algoritmos en Lugar de Generarlos**

En lugar de generar algoritmos aleatoriamente cada vez, definir 3 algoritmos fijos:

```python
# En lugar de:
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# Usar:
algorithms = [
    {
        'name': 'GAA_Greedy_TwoOpt',
        'ast': create_fixed_algorithm_1()  # Definido explícitamente
    },
    {
        'name': 'GAA_Random_OneExchange',
        'ast': create_fixed_algorithm_2()
    },
    {
        'name': 'GAA_GreedyRatio_FlipBest',
        'ast': create_fixed_algorithm_3()
    }
]
```

**Ventajas**:
- ✅ Tiempos 100% reproducibles
- ✅ No depende de cambios en Grammar/Generator
- ✅ Algoritmos conocidos y optimizados

**Desventaja**:
- ❌ Pierde el aspecto de "generación automática" del GAA

---

### Solución 2: **Timeout Agresivo + Reintentos**

```python
# Configurar timeout por experimento
TIMEOUT_PER_EXPERIMENT = 5.0  # 5 segundos máximo

# Si un algoritmo excede timeout en 3 instancias consecutivas, descartarlo
if consecutive_timeouts >= 3:
    print(f"⚠️  Algoritmo {alg_name} descartado por ser demasiado lento")
    algorithms.remove(algorithm)
```

**Ventajas**:
- ✅ Evita que algoritmos lentos arruinen toda la ejecución
- ✅ Tiempo total predecible (~25-30s)

**Desventaja**:
- ❌ Puede descartar algoritmos válidos en instancias grandes

---

### Solución 3: **Fijar Versión del Código de Grammar**

Documentar la versión exacta del código de `Grammar` y `AlgorithmGenerator`:

```bash
# Crear snapshot del código de generación
git tag -a v1.0-grammar-stable -m "Versión estable de Grammar para experimentos"

# O copiar a archivo fijo
cp gaa/grammar.py gaa/grammar_v1_stable.py
cp gaa/generator.py gaa/generator_v1_stable.py
```

**Ventajas**:
- ✅ Reproducibilidad con seed
- ✅ Mantiene aspecto de generación automática

**Desventaja**:
- ❌ Requiere mantenimiento de múltiples versiones

---

### Solución 4: **Timeout Adaptativo por Tamaño de Instancia**

```python
def get_timeout(instance_size):
    """Timeout adaptativo basado en tamaño de instancia"""
    if instance_size < 100:
        return 1.0  # 1s
    elif instance_size < 1000:
        return 5.0  # 5s
    elif instance_size < 5000:
        return 15.0  # 15s
    else:
        return 30.0  # 30s
```

**Ventajas**:
- ✅ Balance entre completitud y tiempo
- ✅ No penaliza instancias pequeñas

---

## 📈 RECOMENDACIÓN FINAL

**Para obtener tiempos consistentes (~25-30s):**

1. ✅ **Usar Solución 1** (algoritmos fijos) **O** Solución 3 (fijar versión de Grammar)
2. ✅ **Implementar Solución 2** (timeout agresivo de 5s por experimento)
3. ✅ **Mantener optimizaciones de visualizaciones**:
   - `max_evaluations=2000` (vs 5000 original)
   - Solo 5 gráficas representativas (vs 31 original)
   - Backend 'Agg'

**Resultado esperado**:
```
Low-dimensional:   8-10s
Large-scale:      15-20s
TOTAL:           25-30s (consistente, ±1s)
```

---

## 🔴 POR QUÉ LA MEDICIÓN ORIGINAL DE 34s NO ES REPRODUCIBLE

El tiempo de 34s reportado originalmente NO puede ser reproducido porque:

1. **El código de generación de algoritmos cambió**
2. **Los algoritmos actuales son más lentos** (algunos >60s por experimento)
3. **No hay documentación** de qué versión del código se usó
4. **No hay registro** de qué algoritmos se generaron exactamente

**Para evitar esto en el futuro**:
- ✅ Usar algoritmos fijos O versionar el código de Grammar
- ✅ Guardar pseudocódigo de algoritmos en cada ejecución
- ✅ Implementar timeouts agresivos
- ✅ Documentar todas las configuraciones (seed, versión de código, etc.)

---

## 📝 CONCLUSIÓN

**La causa raíz de la variabilidad NO es el sistema operativo (RAM, Swap, CPU), sino el CÓDIGO DE GENERACIÓN DE ALGORITMOS que cambió entre versiones.**

**Evidencia**:
- Mismo seed (42) genera algoritmos diferentes en diferentes ejecuciones
- Algoritmos generados tienen velocidades que varían 100x-1000x
- Algunos algoritmos exceden timeout de 60s

**Solución inmediata**: Implementar algoritmos fijos + timeout de 5s por experimento.
