# 📚 ÓPTIMO vs BKS - Guía Completa

**Documento explicando la diferencia crítica entre ÓPTIMO (garantizado) y BKS (mejor conocido)**

---

## 🎯 Diferencia Fundamental

### ✅ ÓPTIMO
```
Definición: Valor matemáticamente GARANTIZADO
Significado: NO EXISTE una solución mejor en la literatura
Certeza: 100% - No puede haber mejor
Implicación: Si GAA encuentra el ÓPTIMO, es PERFECTO ✅

Ejemplo:
  Instancia: flat300_20_0
  ÓPTIMO: 20 colores
  Interpretación: Es imposible colorear ese grafo con <20 colores
```

### 📊 BKS (Best Known Solution)
```
Definición: Mejor solución ENCONTRADA hasta ahora
Significado: La solución más buena que se conoce PERO podría haber mejor
Certeza: NO 100% - Podría no ser óptimo
Implicación: Si GAA supera BKS, podría descubrir algo nuevo 🎉

Ejemplo:
  Instancia: DSJC125.1
  BKS: ? (desconocido)
  Interpretación: No se conoce la solución, es un benchmark abierto
```

---

## 🔍 Comparación Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    VALOR REAL DESCONOCIDO                   │
│                        (Realidad)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   ÓPTIMO = 20    │  │   BKS = 21       │  │   INCIERTO = ?   │
│                  │  │                  │  │                  │
│ ✅ Garantizado   │  │ 📊 Mejor conocido│  │ ❓ Desconocido   │
│ 100% certeza     │  │ No es óptimo     │  │ Benchmark abierto│
│                  │  │ Podría mejorar   │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘

Si GAA encuentra 20:   ✅ ÓPTIMO (excelente)
Si GAA encuentra 21:   ⚠️ Iguala BKS (bueno)
Si GAA encuentra 20:   🎉 Supera BKS (novedad!)
```

---

## 📊 Clasificación de Instancias

### Categoría 1: ÓPTIMO Conocido

```
┌─────────────────────────────────────┐
│      INSTANCIA CON ÓPTIMO CONOCIDO  │
└─────────────────────────────────────┘

Garantía matemática: SÍ ✅
Mejor posible: Conocido exactamente
Ejemplo: LEI (Leighton 1979)

Implicaciones para GAA:
  Si GAA = ÓPTIMO     → ✅ PERFECTO (validación exitosa)
  Si GAA > ÓPTIMO     → ❌ FALLO (error en experimento)
  Si GAA < ÓPTIMO     → 🎉 DESCUBRIMIENTO (refuta matemática)
```

**Ejemplos de familias con ÓPTIMO**:
- ✅ **LEI** - Leighton (1979) - Garantías teóricas
  - le450_5a = 5 colores (garantizado)
  - le450_15b = 15 colores (garantizado)
  - le450_25d = 25 colores (garantizado)

- ✅ **CUL** - Culberson
  - flat300_20_0 = 20 colores (óptimo)
  - flat1000_50_0 = 50 colores (óptimo)

- ✅ **REG** - Register Allocation (compiladores)
  - fpsol2.i.1 = 65 colores (óptimo)
  - mulsol.i.1 = 49 colores (óptimo)

- ✅ **MYC** - Mycielski
  - myciel3 = 4 colores (óptimo)
  - myciel7 = 8 colores (óptimo)

---

### Categoría 2: BKS Conocido (pero posiblemente mejorable)

```
┌──────────────────────────────────────┐
│   INSTANCIA CON BKS (NO ÓPTIMO)      │
└──────────────────────────────────────┘

Garantía matemática: NO ❌
Mejor encontrado: SÍ, pero podría mejorar
Ejemplo: SGB (Stanford GraphBase)

Implicaciones para GAA:
  Si GAA = BKS        → ✅ BUENO (iguala literatura)
  Si GAA > BKS        → ⚠️ PEOR (no compite)
  Si GAA < BKS        → 🎉 NOVEL (encuentra mejor solución!)
```

**Ejemplos de familias con BKS**:
- 📊 **SGB** (Stanford GraphBase - Literatura + Juegos)
  - anna = 11 (BKS, no garantizado óptimo)
  - homer = 13 (BKS)
  - games120 = 9 (BKS)

---

### Categoría 3: ABIERTA (Sin BKS conocido)

```
┌──────────────────────────────────────┐
│      INSTANCIA ABIERTA (BENCHMARK)   │
└──────────────────────────────────────┘

Garantía matemática: NO
BKS conocido: NO
Mejor encontrado: DESCONOCIDO
Ejemplo: DSJ (DIMACS Challenge) - ❓ TODAS ABIERTAS

Implicaciones para GAA:
  Cualquier solución que encuentre GAA es potencialmente novela
  Si compite con papers recientes: 🎉 CONTRIBUCIÓN
  Si supera papers recientes: 🏆 PUBLICABLE

Oportunidad:
  Las instancias abiertas son donde GAA puede descubrir cosas nuevas
```

**Ejemplos de familias ABIERTAS**:
- ❓ **DSJ** (DIMACS Challenge) - 15 instancias, TODAS abiertas
  - DSJC125.1 = ? (desconocido)
  - DSJC1000.9 = ? (desconocido)
  - Excelente para descubrimientos

- ❓ **SCH** (School Scheduling)
  - school1 = ? (desconocido)
  - school1_nsh = ? (desconocido)

- ❓ **LAT** (Latin Square)
  - latin_square_10 = ? (desconocido)

---

## 🗂️ Matriz de Familias: ÓPTIMO vs BKS

```
┌──────────────┬─────────────┬──────────────┬────────────────┐
│ Familia      │ Instancias  │ Tipo         │ Característica │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ LEI (✅)     │     12      │ ÓPTIMO       │ Garantizado    │
│              │             │              │ (Leighton)     │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ CUL (✅)     │      6      │ ÓPTIMO       │ Cuasi-random   │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ REG (✅)     │     14      │ ÓPTIMO       │ Compiladores   │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ MYC (✅)     │      5      │ ÓPTIMO       │ Sin triángulos │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ SGB (📊)     │     25      │ BKS (72%)    │ Literatura+    │
│              │             │              │ Juegos         │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ DSJ (❓)     │     15      │ ABIERTA      │ DIMACS (100%)  │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ SCH (❓)     │      2      │ ABIERTA      │ Scheduling     │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ LAT (❓)     │      1      │ ABIERTA      │ Latin Square   │
└──────────────┴─────────────┴──────────────┴────────────────┘

TOTALES:
  ✅ ÓPTIMO:     37 instancias (45.7%)
  📊 BKS:        18 instancias (22.2%)
  ❓ ABIERTA:    26 instancias (32.1%)
```

---

## 🎯 Qué significa cada resultado en GAA

### Escenario: Familia LEI (ÓPTIMO Garantizado)

```
LEI: le450_5a
ÓPTIMO teórico: 5 colores (garantizado por Leighton 1979)

Resultado 1: GAA encuentra 5 colores
  → ✅ ÓPTIMO ENCONTRADO (excelente!)
  → Validación exitosa de GAA
  → Puede confiar en su algoritmo

Resultado 2: GAA encuentra 6 colores
  → ❌ NO ENCONTRÓ ÓPTIMO
  → Gap: +20% sobre óptimo
  → Necesita mejorar parámetros de GAA

Resultado 3: GAA encuentra 4 colores
  → 🎉 IMPOSIBLE (error en experimento)
  → Refuta garantía matemática
  → Revisar código/instancia
```

### Escenario: Familia DSJ (ABIERTA)

```
DSJ: DSJC125.1
Óptimo conocido: DESCONOCIDO
Mejor reportado en literatura: VARÍA (depende de paper)

Resultado 1: GAA encuentra 13 colores
  → 📊 Solución válida
  → Compara contra papers recientes
  → Si es mejor: 🎉 Potencialmente publicable

Resultado 2: GAA encuentra mejor que todos los papers
  → 🏆 DESCUBRIMIENTO
  → Posible contribución a literatura
  → Oportunidad de publicación

Resultado 3: GAA encuenta igual a papers recientes
  → ✅ COMPETITIVO
  → GAA es relevante vs estado del arte
```

---

## 📈 Interpretación según el Tipo

### Si es ÓPTIMO:

```
┌─────────────────────────────────┐
│  INTERPRETANDO RESULTADOS CON   │
│        ÓPTIMO GARANTIZADO       │
└─────────────────────────────────┘

Gap = 0%:
  ✅ EXCELENTE
  → Encontró el mejor valor posible
  → Valida que GAA funciona bien
  → Confianza en algoritmo generado

Gap = +1-5%:
  ⚠️ ACEPTABLE pero mejorable
  → No encontró óptimo
  → Podría necesitar ajustes
  → Dependiendo de restricciones de tiempo

Gap = +5-10%:
  ❌ POBRE
  → Mucho peor que óptimo
  → Parámetros inadecuados
  → Revisar generación del algoritmo

Gap > 0 (imposible):
  💥 ERROR
  → Refuta matemática
  → Revisar instancia/implementación
```

### Si es BKS:

```
┌─────────────────────────────────┐
│  INTERPRETANDO RESULTADOS CON   │
│         BKS NO GARANTIZADO      │
└─────────────────────────────────┘

Gap = 0% (igual a BKS):
  ✅ BUENO
  → Iguala mejor conocido
  → Competitivo vs literatura

Gap < 0% (menor a BKS):
  🎉 EXCELENTE
  → SUPERA mejor conocido
  → Posible descubrimiento
  → Verificar contra papers recientes

Gap = +1-10%:
  ⚠️ ACEPTABLE
  → Cerca del BKS
  → Competitivo pero no superior

Gap > 10%:
  ❌ POBRE
  → Significativamente peor
  → No es competitivo
```

### Si es ABIERTA:

```
┌─────────────────────────────────┐
│  INTERPRETANDO RESULTADOS EN    │
│      INSTANCIA ABIERTA (?)      │
└─────────────────────────────────┘

Cualquier solución es contribución:
  📊 Compara contra:
     - Papers recientes en literatura
     - Otros solvers de GCP
     - Benchmarks conocidos (si existen)

Si compite bien:
  ✅ BUENO
  → GAA es competitivo en problemas abiertos

Si supera todas las referencias:
  🎉 NOVEDAD
  → Posible descubrimiento
  → Documentar bien
  → Considerar publicación

Si es el primero en la instancia:
  🏆 PRIMERA SOLUCIÓN
  → Muy valioso
  → Claramente publicable
```

---

## 🎯 Estrategia de Pruebas Recomendada

### Fase 1: VALIDAR que GAA funciona
```
Usar familias CON ÓPTIMO GARANTIZADO:
  • LEI (12 instancias)
  • CUL (6 instancias)
  • REG (14 instancias)

Objetivo:
  Encontrar óptimos en >80% de instancias
  
Si se logra:
  ✅ GAA está funcionando correctamente
  
Si falla:
  ❌ Revisar parámetros/configuración
```

### Fase 2: COMPARAR contra BKS
```
Usar familias CON BKS:
  • SGB (25 instancias, 72% con BKS)

Objetivo:
  Igualar o mejorar BKS

Resultado:
  Si iguala: ✅ Competitivo
  Si mejora: 🎉 Descubrimiento
```

### Fase 3: EXPLORAR instancias abiertas
```
Usar familias ABIERTAS:
  • DSJ (15 instancias) ← Principal
  • SCH (2 instancias)
  • LAT (1 instancia)

Objetivo:
  Encontrar soluciones competitivas
  Buscar descubrimientos
  
Valor:
  🎉 Potencial publicable
  🏆 Contribución a literatura
```

---

## 💡 Ejemplos Reales

### Ejemplo 1: LEI (ÓPTIMO)

```
Instancia: le450_5a
ÓPTIMO: 5 colores (garantizado por Leighton 1979)

Ejecución 1:
  GAA encuentra: 5 colores
  → ✅ ÓPTIMO (éxito!)
  → Valida que GAA puede alcanzar garantías teóricas

Ejecución 2:
  GAA encuentra: 6 colores
  → ⚠️ +20% sobre óptimo
  → Aún así, es competitivo
  → Gap dependería de parámetros

Ejecución 3:
  GAA encuentra: 4 colores
  → 💥 IMPOSIBLE
  → Revisa el código - hay un bug
```

### Ejemplo 2: DSJ (ABIERTA)

```
Instancia: DSJC125.1
ÓPTIMO: Desconocido en literatura

Papers recientes reportan: ~13 colores
El mejor conocido: ~12 colores

Ejecución 1:
  GAA encuentra: 13 colores
  → ✅ COMPETITIVO
  → Iguala papers recientes
  → GAA funciona bien en problemas abiertos

Ejecución 2:
  GAA encuentra: 11 colores
  → 🎉 SUPERA LITERATURA
  → Mejor que papers conocidos
  → Potencial publicable
  → Documenta bien

Ejecución 3:
  GAA encuentra: 15 colores
  → ❌ POBRE
  → Mucho peor que literatura
  → Revisa parámetros de GAA
```

### Ejemplo 3: SGB (BKS)

```
Instancia: anna
BKS: 11 colores (no garantizado óptimo)

Posible óptimo real: 11 o menos

Ejecución 1:
  GAA encuentra: 11 colores
  → ✅ IGUALA BKS
  → Competitivo con literatura

Ejecución 2:
  GAA encuentra: 10 colores
  → 🎉 SUPERA BKS
  → Encontró mejor solución
  → Posible nuevo BKS
  → Reportar en literatura

Ejecución 3:
  GAA encuentra: 12 colores
  → ⚠️ PEOR QUE BKS
  → Gap +9.1% sobre BKS
  → No es competitivo
```

---

## 📋 Checklist: Entendimiento de ÓPTIMO vs BKS

- [ ] Entiendo qué es ÓPTIMO (garantizado matemáticamente)
- [ ] Entiendo qué es BKS (mejor encontrado, no garantizado)
- [ ] Sé identificar qué familias tienen ÓPTIMO (LEI, CUL, REG)
- [ ] Sé identificar qué familias tienen BKS (SGB)
- [ ] Sé identificar qué familias son ABIERTAS (DSJ, SCH, LAT)
- [ ] Sé interpretar gap cuando se compara contra ÓPTIMO
- [ ] Sé interpretar gap cuando se compara contra BKS
- [ ] Sé interpretar resultados en instancias ABIERTAS
- [ ] Entiendo que superar ÓPTIMO = error en código/instancia
- [ ] Entiendo que superar BKS = posible descubrimiento
- [ ] Entiendo que instancias abiertas = oportunidad de publicación
- [ ] Sé qué familias usar para validar (LEI + CUL + REG)
- [ ] Sé qué familias usar para encontrar novedades (DSJ + SGB)

---

## 🎓 Conclusión

**ÓPTIMO** = Garantía matemática de que no hay mejor
- Úsalo para VALIDAR que GAA funciona
- Si GAA = ÓPTIMO: ✅ Perfecto
- Si GAA > ÓPTIMO: 💥 Error
- Si GAA < ÓPTIMO: ⚠️ Puede mejorar

**BKS** = Mejor solución encontrada (pero podría no ser óptimo)
- Úsalo para COMPARAR contra literatura
- Si GAA = BKS: ✅ Competitivo
- Si GAA < BKS: 🎉 Descubrimiento
- Si GAA > BKS: ❌ No competitivo

**ABIERTA** = Óptimo desconocido (benchmark abierto)
- Úsalo para EXPLORAR e INNOVAR
- Cualquier solución buena: 📊 Contribución
- Superar papers recientes: 🎉 Publicable
- Primera solución: 🏆 Muy valioso

**Strategy**: Valida con ÓPTIMO → Compara con BKS → Explora ABIERTAS
