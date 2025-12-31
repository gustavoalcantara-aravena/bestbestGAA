# ❓ ¿Cómo Genera y Prueba GAA los Algoritmos?

## Tu Pregunta Exacta

> "¿Se generan varios algoritmos y se prueba qué tal anduvo cada uno? ¿O se usa un solo algoritmo que va variando?"

**Respuesta**: **Ambas cosas a la vez**, pero se mezcla de forma que puede confundir.

---

## 📊 Lo Que Está Ocurriendo Realmente

### Nivel 1: ILS Busca en Espacio de Configuraciones

```
GAA = Sistema de Generación Automática de Algoritmos
  ↓
Usa ILS (Iterated Local Search) para buscar
  ↓
Busca en ESPACIO DE CONFIGURACIONES (no en población)
  ↓
Cada punto en el espacio = una configuración diferente de algoritmo
```

**Concretamente**:

```
Iteración 1: Config A
├─ Ordering: LargestDegreeFirst
├─ Perturbation: Remove3
├─ LS: ColorSwap
└─ [Se prueba en instancias de entrenamiento]
   → Fitness = 0.75

Iteración 2: Config B (vecino de A)
├─ Ordering: SmallerDegreeLast  ← Cambió
├─ Perturbation: Remove3
├─ LS: ColorSwap
└─ [Se prueba en instancias de entrenamiento]
   → Fitness = 0.78 (mejor que A)

Iteración 3: Config C (vecino de B)
├─ Ordering: SmallerDegreeLast
├─ Perturbation: Remove5  ← Cambió
├─ LS: ColorSwap
└─ [Se prueba en instancias de entrenamiento]
   → Fitness = 0.74 (peor que B)

...
[500 iteraciones total]

Resultado Final: MEJOR CONFIG = (SmallerDegreeLast, Remove3, ColorSwap)
```

---

## 🎯 Las 3 Niveles de Búsqueda/Prueba

### Nivel 1: BÚSQUEDA (ILS sobre configuraciones)

**¿Qué busca ILS?**
- Diferentes combinaciones de operadores
- Diferentes parámetros
- Diferentes estrategias de control

**¿Cuántos "algoritmos" genera?**
- 500 configuraciones diferentes (en 500 iteraciones)
- Pero muchas se descartan porque tienen fitness peor

**¿Se prueba cada uno?**
- SÍ, se prueba en instancias de entrenamiento
- Pero en UN SUBCONJUNTO de instancias (rápido)

### Nivel 2: EVALUACIÓN (Función de Fitness)

Cada configuración se prueba ejecutando:
- El algoritmo ILS con esa configuración
- En MÚLTIPLES instancias de entrenamiento
- Se calcula un fitness promedio

**Ejemplo con CUL**:
```
Config A se prueba en:
├─ flat1000_50_0.col
├─ flat1000_60_0.col
├─ flat1000_76_0.col
├─ flat300_20_0.col
├─ flat300_26_0.col
└─ flat300_28_0.col

Fitness = promedio de colores usados en los 6 instances
```

### Nivel 3: VALIDACIÓN (Después de encontrar mejor)

Una vez que ILS encuentra la MEJOR CONFIGURACIÓN:
- Se prueba nuevamente en INSTANCIAS DE VALIDACIÓN/TEST
- (Instancias que no vio durante búsqueda)
- Para ver si generaliza bien

---

## 🏗️ Estructura del Espacio de Configuraciones (AST)

Lo que GAA genera y explora:

```yaml
Configuración = AlgorithmNode (Abstract Syntax Tree)
  ├─ Initialization Strategy
  │   └─ LargestDegreeFirst | RandomOrder | SmallerDegreeLast | ...
  │
  ├─ Local Search Strategy
  │   └─ ColorSwap | TABUCOL-like | RandomRecoloring | ...
  │
  ├─ Perturbation Strategy
  │   └─ Remove2 | Remove3 | Remove5 | Remove10 | ...
  │
  ├─ Acceptance Criterion
  │   └─ BetterOrEqual | FirstImprovement | SimulatedAnnealing | ...
  │
  └─ Parameters
      └─ perturbation_strength, max_iterations, etc.
```

**Total de puntos en el espacio**: 
- Si hay 4 opciones × 5 opciones × 5 opciones × 3 opciones
- = 300 configuraciones posibles
- ILS explora 500 iteraciones en este espacio
- Prueba muchas, descarta las peores, mantiene las mejores

---

## 📈 Flujo Completo de Una Corrida

```
┌─────────────────────────────────────────────────────────────┐
│ ENTRADA: Instancias de entrenamiento (CUL: 6 archivos .col) │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ ILS SEARCH (500 iteraciones)                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Para cada iteración i = 1..500:                           │
│                                                             │
│  1. Generar/Modificar configuración i                      │
│     Config_i = (Ordering, LS, Perturbation, Acceptance)   │
│                                                             │
│  2. Ejecutar Config_i en instancias de entrenamiento       │
│     Para cada instancia (flat1000_50_0.col, ...):          │
│       - Ejecutar ILS con Config_i                          │
│       - Medir # colores usado                              │
│       - Registrar tiempo                                   │
│                                                             │
│  3. Calcular fitness de Config_i                           │
│     fitness = f(colores, tiempo, robustez, ...)           │
│                                                             │
│  4. Decidir si Config_i es mejor que actual               │
│     if fitness_i > fitness_actual:                         │
│        mejor_encontrado = Config_i                         │
│                                                             │
│  5. Aceptar o rechazar Config_i (ILS acceptance)          │
│     Genera "perturbación" para próxima config              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ RESULTADO: MEJOR_CONFIGURACIÓN                              │
│ Ej: (SmallerDegreeLast, ColorSwap, Remove3, BetterOrEqual) │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ VALIDACIÓN (Prueba en nuevas instancias)                    │
├─────────────────────────────────────────────────────────────┤
│ Ejecutar MEJOR_CONFIGURACIÓN en test instances             │
│ (instancias que ILS nunca vio)                             │
│ → Ver si generaliza bien                                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ SALIDA: REPORTE con                                         │
│  - Mejor configuración encontrada                           │
│  - Su fitness en training                                   │
│  - Su fitness en validation/test                            │
│  - Pseudocódigo del algoritmo                               │
│  - Evolución de búsqueda (gráfica)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## ❌ El Problema: Outputs No Documentan QUÉ Configuración Se Generó

**Actualmente imprime**:
```
[ILS 010] best=0.7542, current=0.7489, time=1.23s
[ILS 020] best=0.7634, current=0.7612, time=1.15s
[ILS 030] best=0.7634, current=0.7589, time=0.98s
```

**No muestra**:
```
❌ Qué componentes tiene la mejor config encontrada
❌ Qué cambió desde iteración anterior
❌ Cuál fue la "perturbación" aplicada
❌ Por qué mejoró (cual operador fue clave)
```

**Debería imprimir algo como**:
```
[ILS 010] best=0.7542
├─ Config: Ordering=LargestDegreeFirst, LS=ColorSwap, Pert=Remove3
├─ Change: Ordering (was RandomOrder)
├─ Accepted: YES (improvement)
└─ Time: 1.23s

[ILS 020] best=0.7634 ✓ (IMPROVED)
├─ Config: Ordering=SmallerDegreeLast, LS=ColorSwap, Pert=Remove3
├─ Change: Ordering (LargestDegreeFirst → SmallerDegreeLast)
├─ Accepted: YES (better)
└─ Time: 1.15s
```

---

## 📋 Plan de Mejora: Documentar Características de GAA

### A Corto Plazo (Este Proyecto)

1. **Mejorar outputs de ILS**:
   - Mostrar configuración en cada iteración
   - Mostrar qué cambió vs iteración anterior
   - Mostrar por qué se aceptó/rechazó

2. **Reportes más detallados**:
   - Número de configuraciones evaluadas
   - Evolución de cada componente del algoritmo
   - Árbol de decisiones de la búsqueda

3. **Visualización de espacio de búsqueda**:
   - Gráfico de fitness vs iteración
   - Gráfico de componentes elegidos vs iteración
   - Mapa de calor de cual operador fue más efectivo

### A Mediano Plazo

1. **Análisis de sensibilidad**:
   - ¿Cuál operador tiene mayor impacto?
   - ¿Cuál parámetro es más importante?

2. **Entender convergencia**:
   - ¿A qué iteración converge ILS?
   - ¿Cuánto mejora la búsqueda vs aleatorio?

3. **Comparativa generación vs fijo**:
   - GAA-generado vs algoritmo manual
   - GAA-generado para CUL vs para DSJ vs para LEI

### A Largo Plazo

1. **Metaanálisis**:
   - ¿Qué configuraciones funcionan para qué familias?
   - ¿Hay patrones en las soluciones encontradas?

2. **Transferencia**:
   - ¿Puede la config de CUL usarse en DSJ?
   - ¿Necesita reentrenamiento por familia?

---

## 🎓 Ejemplo Concreto: Una Corrida Completa

### Escenario: GAA en familia CUL

```
INPUT: 6 instancias CUL (flat1000_50_0.col, ..., flat300_28_0.col)

SEARCH PHASE (500 iterations):

Iter 1:  Config=(LDF, ColorSwap, Remove2, BE)   → F=0.72 [INICIAL]
Iter 2:  Config=(LDF, ColorSwap, Remove3, BE)   → F=0.75 ✓ MEJOR
Iter 3:  Config=(LDF, RandomRecoloring, Rm3, BE) → F=0.71 ✗ Peor
Iter 4:  Config=(SDL, ColorSwap, Remove3, BE)   → F=0.78 ✓ MEJOR
Iter 5:  Config=(SDL, ColorSwap, Remove5, BE)   → F=0.76  (aceptado igual)
...
Iter 500: Config=(SDL, TabuColorSwap, Rm3, BE)  → F=0.81 MEJOR FINAL

BEST FOUND: (SmallerDegreeLast, TabuColorSwap, Remove3, BetterOrEqual)
            Fitness training = 0.81

VALIDATION PHASE:
Ejecutar mejor config en nuevas instancias (CUL test set)
→ Resultado: 0.80 (generaliza bien)

OUTPUT:
- Pseudocode del algoritmo encontrado
- Configuración completa en YAML/JSON
- Evolución de búsqueda
- Análisis de robustez
```

---

## 🔧 Cómo GAA es Diferente de GA

```
         │ GA (Genetic Algorithm)    │ GAA (nuestro sistema)
─────────┼───────────────────────────┼─────────────────────────
Población│ 100 individuos            │ 1 configuración actual
Generación│ Reproduce/Cruza N veces   │ ILS perturba/busca localmente
Fitness  │ Cada individuo             │ Config actual
Selección│ Mejor 50 sobreviven        │ Mejor encontrado hasta ahora
Resultado│ Población final            │ Una configuración (mejor)

En GA: ves evolucionar una población
En GAA: ves evolucionar UNA SOLUCIÓN en espacio de configs
```

**La confusión**: 
- ILS hace 500 iteraciones
- En cada iteración, toca/prueba 1 configuración
- Entonces sí genera 500 "variantes"
- Pero no es población (no coexisten)
- Es más como "trayectoria de búsqueda"

---

## 📝 TABLA RESUMEN

| Aspecto | ¿Qué ocurre? |
|---------|-------------|
| **¿Cuántos algoritmos?** | 500 candidatos generados, 1 mejor seleccionado al final |
| **¿Se prueban todos?** | SÍ, en instancias de entrenamiento |
| **¿En qué instancias?** | Entrenamiento (búsqueda) → Validación (evaluación final) |
| **¿Se varia algo?** | SÍ, cada iteración varía componentes del algoritmo |
| **¿Es determinista?** | No, perturbaciones son estocásticas, pero con seed=42 es reproducible |
| **¿Qué se reporta?** | Solo el MEJOR algoritmo encontrado (no los 499 desechados) |
| **¿Falta documentar?** | ✅ SÍ - cuáles were los 500 candidatos, cómo evolucionaron |

---

## 🚀 Qué Falta en Outputs Actuales

1. **Historial de configuraciones** ❌
   - No se guarda qué config se probó en cada iteración
   - No se muestra evolución de cada componente

2. **Justificación de cambios** ❌
   - No explica POR QUÉ la nueva config es mejor
   - No identifica cuál operador causó mejora

3. **Análisis de espacio** ❌
   - No muestra cuántos candidatos eran inviables
   - No muestra distribución de fitness

4. **Comparativa histórica** ❌
   - No compara mejor config encontrada vs inicial
   - No muestra convergencia

---

## ✅ Lo Que Bien Está Documentado

1. Mejor configuración final → SÍ (gaa_report.json)
2. Fitness en training → SÍ
3. Fitness en validation → SÍ
4. Pseudocódigo del algoritmo → SÍ
5. Historial de iteraciones → Parcial (últimas 50)

---

## Conclusión

**Tu pregunta era excelente**:

> GAA SÍ genera múltiples algoritmos (500)
> GAA SÍ prueba cada uno
> GAA SÍ selecciona el mejor
> 
> PERO: Los outputs no lo documentan claramente

**Necesitamos agregar al plan de mejora**:
1. Logging detallado de configuraciones por iteración
2. Visualización de evolución del algoritmo
3. Análisis comparativo entre candidatos
4. Métricas de calidad del espacio de búsqueda
