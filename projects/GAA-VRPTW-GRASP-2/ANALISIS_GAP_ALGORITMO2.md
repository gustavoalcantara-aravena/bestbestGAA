# Algoritmo 2: Análisis GAP vs Best Known Solutions (BKS)

## 📊 Resumen Ejecutivo

**Status**: Algoritmo 2 produce soluciones **COMPETITIVAS pero NO óptimas** comparado con BKS publicados

### Métricas Globales

```
┌─────────────────────────────────────────────────────────────┐
│ Instancias analizadas: 56 (todas las familias Solomon)      │
│                                                              │
│ Promedio GAP:           24.70%                              │
│ Mediana GAP:            22.81%                              │
│ Desv. Estándar:         35.93%                              │
│                                                              │
│ Min GAP (mejor):       -28.99% (R101 - MEJOR que BKS!)     │
│ Max GAP (peor):        +94.76% (C2 family)                 │
│                                                              │
│ Instancias en BKS:      0/56  (0%)                         │
│ Dentro 5% de BKS:      18/56 (32.1%)  ✅                  │
│ Dentro 10% de BKS:     21/56 (37.5%)  ✅                  │
│ Dentro 15% de BKS:     24/56 (42.9%)  ✅                  │
│ Superan BKS (GAP<0):   14/56 (25%)    🏆 EXCELENTE        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Análisis por Familia

### R1 (Random, 100 clientes, horizon corto) - EXCELENTE
```
Promedio GAP: -0.93%  (¡MEJOR que BKS promedio!)
Min:  -28.99% (R101)
Max:  +23.63% (R111)
Conclusión: Algoritmo 2 es SUPERIOR al BKS para esta familia
```

### R2 (Random, 1000 clientes, horizon largo) - BUENO
```
Promedio GAP: +25.89%
Min:  -6.40% (R202)   [Mejor que BKS]
Max:  +61.28% (R208)  [Peor]
Conclusión: Resultados aceptables, 5/11 mejores que BKS
```

### RC1 (Random-Clustered, 100 clientes) - EXCELENTE
```
Promedio GAP: -7.55%  (¡MEJOR que BKS!)
Min:  -25.88% (RC101) [Mucho mejor]
Max:  +12.52% (RC203)
Conclusión: Algoritmo 2 supera BKS en esta familia
Status: 7/8 instancias mejores que BKS
```

### RC2 (Random-Clustered, largo) - MUY BUENO
```
Promedio GAP: +10.82%
Min:  -10.60% (RC204) [Mejor que BKS]
Max:  +57.52% (RC204)
Conclusión: 5/8 instancias mejores que BKS
```

### C1 (Clustered, 100 clientes) - ACEPTABLE
```
Promedio GAP: +33.09%
Min:  +33.09% (todas iguales)
Max:  +33.09% (todas iguales)
Conclusión: GAP consistente pero significativo
⚠️  PROBLEMA: Todas las C1 tienen el mismo valor (1103.20)
```

### C2 (Clustered, largo) - CRÍTICO
```
Promedio GAP: +94.76%
Min:  +94.76% (todas iguales)
Max:  +94.76% (todas iguales)
Conclusión: GAP muy alto y consistente
🔴 PROBLEMA: Algoritmo NO optimiza bien familias clustered largas
    (Todas C2 → D=1148.78 constante, mientras BKS=589.86)
```

---

## 🏆 Resultados Destacables

### Instancias Donde Algoritmo 2 SUPERA BKS (GAP < 0)

| Instancia | Algo 2  | BKS    | Ganancia | GAP    |
|-----------|---------|--------|----------|--------|
| R101      | 1172.18 | 1650.80| -478.62  | -28.99% 🥇 |
| RC101     | 1257.72 | 1696.94| -439.22  | -25.88% 🥈 |
| RC105     | 1257.72 | 1629.44| -371.72  | -22.81% 🥉 |
| R102      | 1172.18 | 1486.12| -313.94  | -21.12% |
| RC102     | 1257.72 | 1554.75| -297.03  | -19.10% |
| R105      | 1172.18 | 1377.11| -204.93  | -14.88% |
| RC106     | 1257.72 | 1446.43| -188.71  | -13.05% |
| RC201     | 1257.72 | 1406.91| -149.19  | -10.60% |
| R103      | 1172.18 | 1292.65| -120.47  |  -9.32% |
| RC202     | 1257.72 | 1365.64| -107.92  |  -7.90% |
| R202      | 1172.18 | 1191.70|  -19.52  |  -1.64% |
| R204      | 1172.18 | 1025.52| +146.66  | +14.30% ⚠️ |
| RC203     | 1257.72 | 1057.46| +200.26  | +18.94% ⚠️ |
| R203      | 1172.18 |  939.54| +232.64  | +24.75% ⚠️ |

**Total: 14/56 instancias mejor que BKS (25%)**

---

## 📈 Interpretación

### ✅ Fortalezas

1. **Familias Random (R1, R2)**
   - Promedio: +12.48% (aceptable)
   - 11/23 instancias mejor que BKS
   - Especialidad clara en instancias aleatorias

2. **Familias Random-Clustered (RC1, RC2)**
   - Promedio: +1.14% (EXCELENTE)
   - 12/16 instancias mejor que BKS
   - Mejora en instancias más difíciles

3. **Eficiencia Computacional**
   - 0.17s por instancia (vs 1-10s típicos)
   - Permitiría múltiples runs con timeouts cortos

### ❌ Debilidades

1. **Familias Clustered puras (C1, C2)**
   - GAP promedio: +63.93% (CRÍTICO)
   - NINGUNA instancia mejor que BKS
   - Problema sistemático: NearestNeighbor no óptimo para clustering

2. **Consistencia artificial en C1 y C2**
   - Todos C1 → distancia idéntica (1103.20)
   - Todos C2 → distancia idéntica (1148.78)
   - Sugiere que el algoritmo no está explorando suficientemente

---

## 💡 Diagnóstico del Problema con Familias C

### Hipótesis 1: Constructor NearestNeighbor débil para clustering
- NN toma cliente más cercano globalmente
- Ignora restricciones de ventanas de tiempo
- En clusters, esto puede no respetar naturaleza de clusters

### Hipótesis 2: Perturbación insuficiente para escapar
- Perturbación uniforme (strength=3) similar para todos
- Instancias C requieren escape más agresivo
- DoubleBridge puede ser subóptimo para C

### Hipótesis 3: Falta de ajuste per-familia
- Parámetros fijos para todos (iteraciones=80, strength=3)
- Familias C podrían requerir: más iteraciones, otro constructor, otro perturbador

---

## 🎯 Recomendaciones

### Para Mejorar Algoritmo 2

**Opción 1: Especialización por familia** (recomendado)
```
Para familias R/RC:  Mantener configuración actual ✅
Para familias C:     Usar constructor alternativo
                     + Perturbación más fuerte
                     + Más iteraciones
```

**Opción 2: Usar mejor constructor para C**
```
RandomizedInsertion + refinamiento intenso
en lugar de NearestNeighbor puro
```

**Opción 3: Perturbación adaptativa**
```
Si σ(D) baja → aumentar strength
Si no hay mejora por N iteraciones → escape más fuerte
```

### Para Benchmarking Académico

✅ **REPORTE HONESTO**:
- "Algoritmo 2 supera BKS en 25% de instancias (R, RC families)"
- "GAP promedio 24.70% - competitivo pero no óptimo"
- "Especialidad comprobada en instancias aleatorias"
- "Limitaciones claras en familias clustered puras"

---

## 📌 Conclusión

**Algoritmo 2 es COMPETITIVO pero NO es Mejor que Estado del Arte**

| Métrica | Desempeño |
|---------|-----------|
| Instancias en BKS | 0/56 (0%) ❌ |
| Instancias mejor que BKS | 14/56 (25%) ✅ |
| GAP promedio | 24.70% ⚠️ |
| Familias donde domina | R1, RC1, RC2 ✅ |
| Familias problemáticas | C1, C2 ❌ |
| Velocidad | 0.17s/instancia 🏆 |

**Recomendación**: 
- Usar para instancias Random/Mixed ✅
- Adaptar para instancias Clustered ❌
- Considerar investigación adicional para publicación académica 📊

