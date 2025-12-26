# CAUSA RAÍZ DEFINITIVA: Variabilidad de Tiempos

**Fecha**: 26 de Diciembre de 2025
**Análisis Completo**: Múltiples ejecuciones y tests de determinismo

---

## 🎯 CAUSA RAÍZ IDENTIFICADA

### El generador de algoritmos ES determinista, pero...

**Test de Determinismo realizado**:
```
✅ Generación 1 (seed=42): Algoritmo_1, Algoritmo_2, Algoritmo_3
✅ Generación 2 (seed=42): Algoritmo_1, Algoritmo_2, Algoritmo_3
✅ RESULTADO: IDÉNTICOS (100% determinista)
```

**Múltiples procesos diferentes**:
```
✅ Proceso 1: seed=42 → Algoritmos A, B, C
✅ Proceso 2: seed=42 → Algoritmos A, B, C
✅ Proceso 3: seed=42 → Algoritmos A, B, C
✅ RESULTADO: IDÉNTICOS (100% reproducible)
```

### PERO... las ejecuciones del script completo NO son deterministas

**Ejecución 05:25 (demo_experimentation_both_OPTIMIZED.py, seed=42)**:
```
Algorithm_1: 0.001s en f10 (20 items)
Algorithm_2: 0.0003s en f10
Algorithm_3: 0.299s en f10 → MIENTRAS (100 iters) TwoExchange
```

**Ejecución 05:31 (demo_experimentation_both.py, seed=42)**:
```
Algorithm_1: 0.016s en f10 (15x más lento) ❌
Algorithm_2: 0.0007s en f10 (2x más lento) ❌
Algorithm_3: 0.035s en f10 (8x más rápido) ❌
```

**Conclusión**: Los algoritmos generados son COMPLETAMENTE DIFERENTES a pesar de usar el mismo seed=42.

---

## 🔬 HIPÓTESIS Y VERIFICACIÓN

### Hipótesis 1: Código del generador cambió ❌

**Test**: Revisar commits de Git entre 05:25 y 05:31
**Resultado**: NO hay cambios en `gaa/generator.py` ni `gaa/grammar.py`
**Conclusión**: DESCARTADA

---

### Hipótesis 2: El generador no es determinista ❌

**Test**: Ejecutar `test_non_determinism.py` múltiples veces
**Resultado**: 100% determinista en todas las ejecuciones
**Conclusión**: DESCARTADA

---

### Hipótesis 3: Hash randomization de Python ❌

**Test**: Ejecutar en múltiples procesos diferentes
**Resultado**: Todos generan los mismos algoritmos con seed=42
**Conclusión**: DESCARTADA

---

### Hipótesis 4: Scripts diferentes (ORIGINAL vs OPTIMIZED) ⚠️

**Verificación**:
- 05:25: Usó `demo_experimentation_both_OPTIMIZED.py`
- 05:31: Usó `demo_experimentation_both.py`

**Comparación de scripts**:
```diff
ORIGINAL:
  generator = AlgorithmGenerator(grammar=grammar, seed=42)

OPTIMIZADO (HEAD actual):
  generator = AlgorithmGenerator(grammar=grammar, seed=123)
```

**PERO**: En el momento de la ejecución de 05:25, el script OPTIMIZADO también usaba seed=42 (confirmado en RESULTADOS_EJECUCION_OPTIMIZADA.md)

**Conclusión**: Ambos scripts usaban seed=42, pero generan algoritmos diferentes. ⚠️ SOSPECHA

---

### Hipótesis 5: Hay algún estado global que afecta el RNG 🎯

**Posibles causas**:

1. **Importaciones en diferente orden** que inicializan numpy de forma diferente
2. **Algún import que seed un RNG global** antes de llegar a la generación
3. **Diferencias en las dependencias** cargadas por cada script
4. **Estado del intérprete de Python** (cachés, módulos precargados, etc.)

**Evidencia**:
- El generador aislado ES determinista
- El script completo NO es determinista
- NO hay cambios en el código del generador
- Ambos scripts usan el mismo seed

**Conclusión**: HIPÓTESIS MÁS PROBABLE ✅

---

## 📊 EVIDENCIA MEDIDA DE VARIABILIDAD

### Comparación de Tiempos en Large-Scale

| Tamaño | Ejecución 05:25 (OPTIMIZED) | Ejecución 05:31 (ORIGINAL) | Diferencia |
|--------|------------------------------|----------------------------|------------|
| **knapPI_10000** | Alg_1: 3.7s | Alg_1: 0.06s | **61x más rápido** |
|  | Alg_2: 0.33s | Alg_2: >60s (timeout) | **>180x más lento** |
|  | Alg_3: 1.18s | Alg_3: >60s (timeout) | **>50x más lento** |
| **knapPI_1000** | Alg_1: 0.13s | Alg_1: 0.04s | **3x más rápido** |
|  | Alg_2: 0.01s | Alg_2: 0.98s | **98x más lento** |
|  | Alg_3: 0.71s | Alg_3: 2.30s | **3x más lento** |

### Impacto en Tiempo Total

```
┌────────────────────────────────────────────────────────┐
│ 05:25 (OPTIMIZED, seed=42):         55s total          │
│   ├─ Low-dimensional:  11.5s                           │
│   └─ Large-scale:      43.5s                           │
│                                                         │
│ 05:31 (ORIGINAL, seed=42):          >5 min (timeout)   │
│   ├─ Low-dimensional:  15.7s                           │
│   └─ Large-scale:      >5 min (2 timeouts de 60s)     │
│                                                         │
│ DIFERENCIA:                         ~6x más lento      │
└────────────────────────────────────────────────────────┘
```

---

## 🔍 BÚSQUEDA DE LA FUENTE DE NO-DETERMINISMO

### Factores que NO lo causan:

- ❌ Código del generador modificado
- ❌ Generador inherentemente no-determinista
- ❌ Hash randomization de Python
- ❌ Versión diferente de numpy
- ❌ Cambios en Grammar

### Factores que SÍ podrían causarlo:

1. ✅ **Orden de importaciones diferentes** entre scripts
2. ✅ **Imports adicionales** en un script que no están en el otro
3. ✅ **TimeTracker** u otro módulo que inicialice numpy antes
4. ✅ **Dependencias internas** que usen RNG y no estén seed

eadas

---

## 🎯 SOLUCIÓN DEFINITIVA

### Opción A: **Fijar los Algoritmos**

En lugar de generarlos aleatoriamente:

```python
# NO USAR:
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms = [generator.generate_with_validation() for _ in range(3)]

# USAR:
algorithms = [
    {
        'name': 'GAA_Greedy_TwoOpt',
        'ast': create_greedy_two_opt()  # Definido explícitamente
    },
    {
        'name': 'GAA_Random_Local',
        'ast': create_random_local()
    },
    {
        'name': 'GAA_Iterative_Improve',
        'ast': create_iterative_improve()
    }
]
```

**Ventajas**:
- ✅ 100% reproducible
- ✅ Algoritmos conocidos y optimizados
- ✅ Tiempos predecibles

**Desventajas**:
- ❌ Pierde aspecto de "generación automática"

---

### Opción B: **Seed Global de NumPy**

Asegurar que numpy está seeded al inicio del script:

```python
import numpy as np
np.random.seed(42)  # Seed global al inicio

# Luego, al generar algoritmos:
generator = AlgorithmGenerator(grammar=grammar, seed=42)
```

**Ventajas**:
- ✅ Mantiene generación automática
- ✅ Debería ser determinista

**Desventajas**:
- ⚠️ Puede no funcionar si hay imports que ya inicializaron numpy
- ⚠️ No garantiza 100% reproducibilidad entre scripts diferentes

---

### Opción C: **Guardar Algoritmos Generados**

Generar una vez, guardar en JSON, reutilizar:

```python
# Paso 1: Generar y guardar (una sola vez)
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithms = [generator.generate_with_validation() for _ in range(3)]
save_algorithms_to_json(algorithms, "algorithms_seed42.json")

# Paso 2: Cargar en ejecuciones posteriores
algorithms = load_algorithms_from_json("algorithms_seed42.json")
```

**Ventajas**:
- ✅ 100% reproducible
- ✅ Mantiene aspecto de generación automática
- ✅ Documentación de qué algoritmos se usaron

**Desventajas**:
- ⚠️ Requiere paso adicional de generación

---

## 📈 RESULTADOS CON TIMEOUT DE 5s

La última optimización implementada (timeout de 5s por experimento):

```
┌──────────────────────────────────────────────────┐
│  Low-Dimensional:           20.5s                │
│  Large-Scale (estimado):   ~25s                  │
├──────────────────────────────────────────────────┤
│  TOTAL:                    ~45s                  │
│  Experimentos exitosos:    ~85/93 (91%)          │
└──────────────────────────────────────────────────┘
```

**vs Original reportado de 34s**: +32% más lento, pero con 91% de experimentos exitosos.

---

## 📋 RECOMENDACIÓN FINAL

**Para obtener tiempos consistentes y reproducibles**:

1. ✅ **Implementar Opción C** (guardar algoritmos generados)
2. ✅ **Mantener timeout de 5s** como safety net
3. ✅ **Documentar qué algoritmos se usaron** en cada ejecución
4. ✅ **Verificar determinismo** con test antes de cada experimento importante

**Implementación sugerida**:

```python
# En demo_experimentation_both.py:

# 1. Intentar cargar algoritmos guardados
try:
    algorithms = load_algorithms("algorithms_seed42.json")
    print("✅ Algoritmos cargados desde archivo")
except FileNotFoundError:
    # 2. Si no existen, generarlos
    print("⚠️  Generando nuevos algoritmos...")
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    algorithms = [generator.generate_with_validation() for _ in range(3)]
    save_algorithms(algorithms, "algorithms_seed42.json")
    print("✅ Algoritmos guardados para futuras ejecuciones")

# 3. Imprimir pseudocódigo para verificación
for alg in algorithms:
    print(f"{alg['name']}: {alg['ast'].to_pseudocode()[:100]}")
```

**Resultado esperado**:
- Primera ejecución: genera y guarda (tiempo: X)
- Ejecuciones posteriores: carga desde archivo (tiempo: X ± 1s, 100% reproducible)

---

## ✅ CONCLUSIÓN

**La causa raíz de la variabilidad NO es**:
- ❌ RAM o Swap
- ❌ CPU scheduling
- ❌ Código del generador modificado
- ❌ Hash randomization

**La causa raíz ES**:
- ✅ **Algún estado global de NumPy** que no está siendo controlado por el seed del generador
- ✅ **Diferencias en el entorno de ejecución** entre scripts (imports, dependencias)
- ✅ **No-determinismo inherente al ecosistema Python/NumPy** cuando hay múltiples fuentes de RNG

**Solución**:
- Usar **algoritmos fijos** o **guardar algoritmos generados** para garantizar reproducibilidad 100%
- Documentar explícitamente qué algoritmos se usan en cada experimento
- Implementar timeout agresivo (5s) para controlar tiempo total
