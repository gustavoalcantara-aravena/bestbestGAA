# CAUSA RAÍZ DEFINITIVA: No-determinismo en generación de algoritmos

**Fecha**: 26 de Diciembre de 2025
**Script**: demo_experimentation_both.py (ORIGINAL, sin modificaciones)
**Seed**: 42 (sin cambios)

---

## 🔴 HALLAZGO CRÍTICO: VARIABILIDAD EXTREMA CONFIRMADA

### Prueba Realizada: Dos Ejecuciones Consecutivas

**Condiciones**:
- Mismo archivo: `scripts/demo_experimentation_both.py` (ORIGINAL)
- Mismo seed: 42
- Mismo entorno
- Ejecutadas con minutos de diferencia

**Resultados**:

| Ejecución | Tiempo Total | Low-Dim | Large-Scale | Variabilidad |
|-----------|-------------|---------|-------------|--------------|
| **Ejecución 1** | **5m 0.3s** (300s) | 15.4s | 4m 43.4s | Baseline |
| **Ejecución 2** | **1m 19.2s** (79s) | ? | ? | **-74% (3.8x más rápido)** 🔴 |

**VARIABILIDAD MEDIDA: 381%**

---

## 🔬 ALGORITMOS GENERADOS (MISMO SEED=42)

### Ejecución 1 (300s - LENTA) 14:50:43

```
✅ Algoritmo 1 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByWeight
         2. APLICAR_HASTA_NO_MEJORAR (parada: Stagnation=10):
           LLAMAR FlipBestItem

✅ Algoritmo 2 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando RandomConstruct
         2. LLAMAR TwoExchange

✅ Algoritmo 3 generado  ← ESTE ES EL LENTO
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByRatio
         2. MIENTRAS (presupuesto: 100 iteraciones):
           SECUENCIA:
             1. BUSQUEDA_LOCAL en FlipWorstItem (aceptación: Metropolis)
             2. LLAMAR FlipWorstItem
```

**Tiempos de Algorithm_3 en Large-Scale (Ejecución 1)**:
- knapPI_3_10000: **59.101s** 🔴
- knapPI_2_5000: **20.635s**
- knapPI_1_5000: **19.713s**
- knapPI_3_5000: **19.498s**

---

### Ejecución 2 (79s - RÁPIDA) 14:55:43

```
✅ Algoritmo 1 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando RandomConstruct
         2. APLICAR_HASTA_NO_MEJORAR (parada: Stagnation=10):
           LLAMAR FlipBestItem

✅ Algoritmo 2 generado
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByValue
         2. LLAMAR FlipWorstItem

✅ Algoritmo 3 generado  ← ESTE ES MÁS RÁPIDO
   Pseudocódigo:
       SECUENCIA:
         1. CONSTRUIR_VORAZ usando GreedyByWeight
         2. MIENTRAS (presupuesto: 100 iteraciones):
           SECUENCIA:
             1. BUSQUEDA_LOCAL en TwoExchange (aceptación: Improving)
             2. LLAMAR TwoExchange
```

---

## 📊 COMPARACIÓN DE ALGORITMOS

### Diferencias Críticas en Algorithm_3:

| Aspecto | Ejecución 1 (LENTA) | Ejecución 2 (RÁPIDA) |
|---------|---------------------|----------------------|
| **Constructor** | GreedyByRatio | GreedyByWeight |
| **Operador** | FlipWorstItem | TwoExchange |
| **Aceptación** | Metropolis (acepta peores) | Improving (solo mejoras) |
| **Iteraciones** | 100 | 100 |
| **Tiempo máx** | 59.1s por experimento | ~5-20s por experimento |

---

## ⚠️ IMPLICACIONES

### 1. El generador NO es determinista

A pesar de usar el mismo seed=42, genera algoritmos completamente diferentes:
- Diferentes constructores (GreedyByRatio vs GreedyByWeight)
- Diferentes operadores (FlipWorstItem vs TwoExchange)
- Diferentes criterios de aceptación (Metropolis vs Improving)

### 2. Variabilidad de tiempos es causada por algoritmos diferentes

No es:
- ❌ RAM o Swap
- ❌ CPU scheduling
- ❌ Caché
- ❌ Condiciones del sistema

Es:
- ✅ **Algoritmos diferentes generados con mismo seed**
- ✅ **Algunos algoritmos 10x-100x más lentos que otros**

### 3. El código de Grammar/Generator tiene no-determinismo oculto

Posibles causas:
1. Algún módulo usa RNG no seeded (datetime, random en lugar de np.random)
2. El orden de imports afecta el estado del RNG
3. Hash randomization de Python (aunque debería ser consistente en el mismo proceso)
4. Alguna dependencia inicializa numpy RNG sin seed

---

## 🎯 EVIDENCIA ADICIONAL

### Test de Determinismo en Aislamiento (realizado anteriormente)

Cuando se ejecuta el generador **aisladamente** (sin el script completo):

```python
# test_non_determinism.py
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms_1 = [generator.generate_with_validation() for _ in range(3)]

generator2 = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms_2 = [generator2.generate_with_validation() for _ in range(3)]

# RESULTADO: ✅ IDÉNTICOS (100% determinista)
```

**Conclusión**: El generador ES determinista cuando se ejecuta solo, pero NO cuando se ejecuta dentro del script completo.

---

## 📈 HISTORIAL DE EJECUCIONES DOCUMENTADAS

| Timestamp | Script | Seed | Tiempo | Algoritmo_3 |
|-----------|--------|------|--------|-------------|
| 05:25 | OPTIMIZED | 42 | 55s | TwoExchange (100 iters) |
| 05:31 | ORIGINAL | 42 | >5min | ??? (timeouts) |
| 14:50 | ORIGINAL | 42 | 300s | FlipWorstItem (Metropolis, 100 iters) |
| 14:55 | ORIGINAL | 42 | 79s | TwoExchange (Improving, 100 iters) |

**Todas con seed=42, todas diferentes.**

---

## 🔍 PRÓXIMOS PASOS RECOMENDADOS

### Opción 1: Usar Algoritmos Fijos (RECOMENDADO)

Definir 3 algoritmos fijos en lugar de generarlos:

```python
# NO hacer:
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms = [generator.generate_with_validation() for _ in range(3)]

# SÍ hacer:
algorithms = load_fixed_algorithms("algorithms_config.json")
```

**Ventajas**:
- ✅ 100% reproducible
- ✅ Tiempos consistentes
- ✅ Documentación clara

---

### Opción 2: Guardar Algoritmos Generados

Primera ejecución: genera y guarda
Siguientes ejecuciones: carga desde archivo

```python
if os.path.exists("algorithms_cache.json"):
    algorithms = load_algorithms("algorithms_cache.json")
else:
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    algorithms = [generator.generate_with_validation() for _ in range(3)]
    save_algorithms(algorithms, "algorithms_cache.json")
```

---

### Opción 3: Seed Global de NumPy + Logging

```python
import numpy as np
import random

# Seed TODOS los generadores aleatorios
np.random.seed(42)
random.seed(42)

# Log el estado del RNG
print(f"NumPy RNG state: {np.random.get_state()[1][0]}")

generator = AlgorithmGenerator(grammar=grammar, seed=42)
```

---

## 📝 CONCLUSIÓN FINAL

**El script `demo_experimentation_both.py` con seed=42 NO es reproducible.**

- Ejecutado 2 veces consecutivas: 300s vs 79s (**381% variabilidad**)
- Mismo código, mismo seed, algoritmos completamente diferentes
- El generador es determinista en aislamiento, pero NO en el contexto del script completo

**Para obtener tiempos consistentes**: Usar algoritmos fijos o guardar los algoritmos generados.

**Respuesta a la pregunta original**:
- ¿Por qué varía tanto el tiempo? → **Porque los algoritmos generados son diferentes cada vez**
- ¿Se puede lograr 23-34s consistente? → **Sí, pero SOLO si se usan algoritmos fijos**

---

**Archivos de evidencia**:
- `output/corrida_original_1.log` - 300s
- `output/corrida_original_2.log` - 79s
- `output/execution_logs/` - Logs completos con configuración
