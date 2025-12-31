# 🎯 RESPUESTA: ¿Cómo GAA Genera y Prueba Algoritmos?

## Tu Pregunta Exacta

> "¿Se generan varios algoritmos y se prueba qué tal anduvo cada uno? ¿O se usa un solo algoritmo que va variando?"

---

## 📊 LA RESPUESTA: Ambas Cosas

### Visualización del Proceso

```
┌─────────────────────────────────────────────────────────────────┐
│                    GAA EN 3 FASES                               │
└─────────────────────────────────────────────────────────────────┘

FASE 1: BÚSQUEDA (ILS explora 500 configuraciones)
═══════════════════════════════════════════════════════════════════

Iter 1:  Config_A = (LDF, ColorSwap, Remove2, BE)
         └─ Se ejecuta en CUL instances → Fitness = 0.72
         └─ Genera "vecino" (perturbación)

Iter 2:  Config_B = (LDF, ColorSwap, Remove3, BE)  ← Cambió Remove2→Remove3
         └─ Se ejecuta en CUL instances → Fitness = 0.75 ✓ MEJOR
         └─ Se acepta. Genera siguiente vecino

Iter 3:  Config_C = (SDL, ColorSwap, Remove3, BE)  ← Cambió LDF→SDL
         └─ Se ejecuta en CUL instances → Fitness = 0.78 ✓ MEJOR
         └─ Se acepta. Genera siguiente vecino

...
[Iteraciones 4-500 de forma similar]
...

Iter 500: Config_Z = (SDL, TabuColorSwap, Remove3, BE)
          └─ Se ejecuta en CUL instances → Fitness = 0.81 ✓ MEJOR GLOBAL


FASE 2: SELECCIÓN (Toma el mejor)
═══════════════════════════════════════════════════════════════════

Mejor encontrado en 500 iteraciones:
  → ALGORITMO = (SmallerDegreeLast, TabuColorSwap, Remove3, BetterOrEqual)
  → FITNESS = 0.81 en training


FASE 3: VALIDACIÓN (Prueba en nuevas instancias)
═══════════════════════════════════════════════════════════════════

Ejecuta el ALGORITMO MEJOR en instancias de test que nunca vio:
  → Confirma que generaliza: Fitness = 0.80 en test
  → Genera reportes, pseudocódigo, análisis
```

---

## 🎓 Ejemplo Concreto: Familia CUL

### Setup
```
Instancias de ENTRENAMIENTO (6 archivos .col):
├─ flat1000_50_0.col    (1000 nodos, 50 colores)
├─ flat1000_60_0.col    (1000 nodos, 60 colores)
├─ flat1000_76_0.col    (1000 nodos, 76 colores)
├─ flat300_20_0.col     (300 nodos, 20 colores)
├─ flat300_26_0.col     (300 nodos, 26 colores)
└─ flat300_28_0.col     (300 nodos, 28 colores)
```

### Ejecución

**Iteración 1** (Inicial):
```
Config:       Ordering=LargestDegreeFirst
              LocalSearch=ColorSwap
              Perturbation=Remove2
              Acceptance=BetterOrEqual

Se ejecuta en 6 instancias CUL:
  flat1000_50_0.col → 45 colores
  flat1000_60_0.col → 47 colores
  flat1000_76_0.col → 51 colores
  flat300_20_0.col  → 18 colores
  flat300_26_0.col  → 21 colores
  flat300_28_0.col  → 22 colores

Fitness = promedio de colores = (45+47+51+18+21+22)/6 = 34.0
Status: INICIAL, aceptado

Siguiente iteración: Perturba LS (ColorSwap → RandomRecoloring)
```

**Iteración 2**:
```
Config:       Ordering=LargestDegreeFirst  (igual)
              LocalSearch=RandomRecoloring  (CAMBIÓ)
              Perturbation=Remove2
              Acceptance=BetterOrEqual

Se ejecuta en 6 instancias CUL:
  flat1000_50_0.col → 46 colores
  flat1000_60_0.col → 48 colores
  flat1000_76_0.col → 52 colores
  flat300_20_0.col  → 19 colores
  flat300_26_0.col  → 22 colores
  flat300_28_0.col  → 23 colores

Fitness = (46+48+52+19+22+23)/6 = 35.0
Status: PEOR que iteración anterior (35.0 > 34.0)
Decision: RECHAZO (no es mejor)

Siguiente iteración: Perturba Perturbation (Remove2 → Remove3)
```

**Iteración 3**:
```
Config:       Ordering=LargestDegreeFirst
              LocalSearch=ColorSwap        (vuelve a anterior)
              Perturbation=Remove3         (CAMBIÓ)
              Acceptance=BetterOrEqual

Se ejecuta en 6 instancias CUL:
  flat1000_50_0.col → 44 colores
  flat1000_60_0.col → 46 colores
  flat1000_76_0.col → 50 colores
  flat300_20_0.col  → 17 colores
  flat300_26_0.col  → 20 colores
  flat300_28_0.col  → 21 colores

Fitness = (44+46+50+17+20+21)/6 = 33.0
Status: MEJOR (33.0 < 34.0) ✓
Decision: ACEPTADO

Siguiente iteración: Perturba Ordering (LDF → SmallerDegreeLast)
```

**... (Iteraciones 4-500 continúan de forma similar) ...**

**Iteración 487** (Mejor encontrado):
```
Config:       Ordering=SmallerDegreeLast
              LocalSearch=TabuColorSwap
              Perturbation=Remove3
              Acceptance=BetterOrEqual

Se ejecuta en 6 instancias CUL:
  flat1000_50_0.col → 40 colores
  flat1000_60_0.col → 42 colores
  flat1000_76_0.col → 45 colores
  flat300_20_0.col  → 15 colores
  flat300_26_0.col  → 16 colores
  flat300_28_0.col  → 17 colores

Fitness = (40+42+45+15+16+17)/6 = 29.17  ✓✓✓ MEJOR HASTA AQUÍ
Status: ACEPTADO Y GUARDADO COMO MEJOR
```

**Iteraciones 488-500**:
```
Se continúa buscando pero no se encuentra mejor que 29.17
Iteración 500 termina.
```

### Resultado Final

```
MEJOR CONFIGURACIÓN ENCONTRADA:
═══════════════════════════════════════════════════════════════
  Ordering Strategy:      SmallerDegreeLast
  Local Search:           TabuColorSwap
  Perturbation:           Remove3 (remueve 3 nodos)
  Acceptance Criterion:   BetterOrEqual

  Fitness (training CUL): 29.17 colores en promedio
  
VALIDACIÓN en test instances (nuevas instancias CUL):
  Ejecutar el algoritmo anterior en instancias nunca vistas
  → Resultado: 28.95 colores promedio
  → Generaliza bien ✓

OUTPUT:
  - gaa_report.json (datos completos)
  - best_algorithm.txt (pseudocódigo del algoritmo)
  - best_configuration.json (configuración en JSON)
  - search_history.csv (evolución de 500 iteraciones)
  - best_configuration.yaml (para ejecutar luego)
```

---

## ❓ Diferencia GAA vs Algoritmo Genético

| Aspecto | GA (Algoritmo Genético) | GAA (nuestro sistema) |
|---------|------------------------|-----------------------|
| **Población** | 100 individuos (soluciones a problema) | 1 configuración (punto en espacio de algoritmos) |
| **Qué varía** | Los individuos evolucionan | LA CONFIGURACIÓN del algoritmo evoluciona |
| **Crucible** | Reproducción + Mutación | Perturbación (ILS) |
| **Selección** | Mejor 50 individuos | Mejor configuración encontrada |
| **Output** | Población final | 1 algoritmo (mejor encontrado) |
| **Cantidad final** | 100 soluciones | 1 algoritmo |
| **Se prueba** | Cada individuo se evalúa | Cada configuración se evalúa |

**Ejemplo Visual**:

```
GA: [Solución1, Solución2, ..., Solución100]
    (todos coexisten en población final)

GAA: Trayectoria: Config1 → Config2 → ... → ConfigMejor
     (solo guardas la mejor)
```

---

## 🔍 Lo Que Ocurre en Cada Iteración de GAA

```python
# Pseudocódigo simplificado de una iteración ILS

for iteracion in 1..500:
    
    # 1. Generar/obtener configuración
    if iteracion == 1:
        config = config_inicial()
    else:
        config = perturbar(mejor_config_encontrado)
    
    # 2. PROBAR esta configuración
    resultados = []
    for instancia in instancias_entrenamiento:  # CUL: 6 instancias
        
        # Ejecutar algoritmo ILS con esta configuración
        resultado = ejecutar_ils_con_config(instancia, config)
        # Ej: resultado = {"colores": 45, "tiempo": 0.23}
        resultados.append(resultado)
    
    # 3. Calcular fitness de la configuración
    fitness = calcular_fitness(resultados)
    # Fitness = f(# colores, tiempo, robustez, ...)
    # Ej: 0.75
    
    # 4. Decidir si es mejor
    if fitness > mejor_fitness_encontrado:
        mejor_fitness_encontrado = fitness
        mejor_config_encontrado = config
        print(f"[ILS {iteracion}] MEJOR encontrado = {fitness}")
    
    # 5. Generar siguiente configuración (perturbación)
    siguiente_config = perturbar(mejor_config_encontrado)
```

---

## ❌ El Problema: Outputs No Documentan QUÉ Algoritmos Se Generaron

### Actual (Incompleto)
```
[ILS 010] best=0.7542, current=0.7489, time=1.23s
[ILS 020] best=0.7634, current=0.7612, time=1.15s
[ILS 030] best=0.7634, current=0.7589, time=0.98s
```

❌ NO muestra:
- Qué configuración es esa
- Qué cambió desde la iteración anterior
- Cuáles componentes tiene el algoritmo

### Debería ser (Completo)
```
[ILS 010] best=0.7542
├─ Algorithm: Ordering=LDF, LS=ColorSwap, Pert=Remove2
├─ Why accepted: INITIAL
└─ Time: 1.23s

[ILS 020] best=0.7634 ✓ (IMPROVED from 0.7542)
├─ Algorithm: Ordering=LDF, LS=ColorSwap, Pert=Remove3 ← CAMBIÓ Perturbation
├─ Change from previous: Remove2 → Remove3
├─ Why accepted: Better fitness (0.7634 > 0.7542)
└─ Time: 1.15s

[ILS 030] best=0.7634 (no improvement)
├─ Algorithm: Ordering=SDL, LS=ColorSwap, Pert=Remove3 ← CAMBIÓ Ordering
├─ Change from previous: LDF → SDL
├─ Why accepted: ILS acceptance criterion met
└─ Time: 0.98s
```

---

## ✅ Lo Que GAA Hace Bien

1. **Genera automáticamente múltiples algoritmos**: ✓ Crea 500 configuraciones
2. **Prueba cada uno**: ✓ En instancias de entrenamiento
3. **Selecciona el mejor**: ✓ Guarda el de mayor fitness
4. **Generaliza**: ✓ Valida en instancias nuevas

## ❌ Lo Que GAA No Documenta Bien

1. **Qué se generó**: ✗ No muestra componentes de cada algoritmo
2. **Cómo evolucionó**: ✗ No muestra trayectoria completa
3. **Por qué mejoró**: ✗ No explica causa de mejora
4. **Historial completo**: ✗ Solo muestra últimas 50 iteraciones

---

## 🎯 Solución

**Se agregó al FRAMEWORK_STATUS.md un plan de mejoras CRÍTICO**:

1. **A corto plazo**: 
   - [ ] Guardar configuración completa en cada iteración
   - [ ] Mostrar componentes en outputs
   - [ ] Registrar qué cambió vs anterior

2. **A mediano plazo**:
   - [ ] Análisis de sensibilidad (qué operador impacta más)
   - [ ] Visualización de evolución
   - [ ] Tabla comparativa de 500 configuraciones

3. **A largo plazo**:
   - [ ] Metaanálisis: patrones en soluciones exitosas
   - [ ] Transferencia: ¿qué config de CUL sirve para DSJ?

---

## 📝 Resumen

| Pregunta | Respuesta |
|----------|-----------|
| ¿Se generan varios algoritmos? | **SÍ**: 500 configuraciones diferentes |
| ¿Se prueba cada uno? | **SÍ**: en instancias de entrenamiento |
| ¿Se varía algo? | **SÍ**: operadores y parámetros varían |
| ¿Cuántos se reportan? | Solo 1: el MEJOR encontrado |
| ¿Se documenta el proceso? | **NO**: eso falta mejorar |
| ¿Hay un solo algoritmo que varía? | En cierto sentido SÍ: es una trayectoria |
| ¿Hay múltiples algoritmos probados? | SÍ: 500 candidatos explorados |

**Respuesta Única**: GAA explora 500 variantes de algoritmos, evalúa cada una, y reporta la mejor. Pero los outputs no documentan claramente este proceso de generación automática de algoritmos.

---

**Referencia**: [EXPLICACION_GAA_ALGORITMOS.md](EXPLICACION_GAA_ALGORITMOS.md) para detalles más profundos.
