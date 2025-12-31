# 📊 Guía: Cómo Comparar GAA vs Literatura

**Documento que explica cómo usar los Best Known Solutions (BKS) para validar resultados de GAA**

---

## 🎯 ¿Por Qué Comparar con Literatura?

Cuando GAA genera y prueba algoritmos, necesitas validar que están **funcionando bien**. La literatura académica contiene:

1. **Best Known Solutions (BKS)** - Los mejores valores encontrados hasta ahora
2. **Óptimos Teóricos** - Valores matemáticamente garantizados
3. **Benchmarks Abiertos** - Instancias sin solución conocida (oportunidad de descubrir algo nuevo)

Comparar contra estos valores te permite:
- ✅ Validar que GAA es COMPETITIVO
- 🎉 Descubrir si GAA encuentra soluciones NUEVAS
- 📈 Medir mejoras del algoritmo generado vs baseline
- 🏆 Potencialmente PUBLICAR si descubre algo novedoso

---

## 📂 Archivos Creados

### 1. **BKS.json** - Base de datos de valores de referencia

📍 Ubicación: `projects/GCP-ILS-GAA/datasets/BKS.json`

```json
{
  "CUL": {
    "flat300_20_0": {
      "bks": 20,
      "optimal": true
    },
    "flat300_26_0": {
      "bks": 26,
      "optimal": true
    },
    ...
  },
  "DSJ": {
    "DSJC125.1": {
      "bks": null,
      "open": true
    },
    ...
  },
  ...
}
```

**Contiene**:
- 81 instancias en total
- 55 instancias con BKS conocido (67.9%)
- 26 instancias abiertas (32.1%)
- Información de qué son óptimos garantizados vs mejores encontrados

### 2. **compare_with_bks.py** - Script de análisis

📍 Ubicación: `projects/GCP-ILS-GAA/compare_with_bks.py`

**Funcionalidad**:
- Carga resultados de GAA
- Compara contra BKS
- Calcula gaps (diferencia porcentual)
- Genera reportes de análisis

---

## 🚀 Cómo Usar

### Paso 1: Ejecutar Experimentos GAA

Primero, ejecuta los experimentos con GAA para generar resultados:

```bash
cd projects/GCP-ILS-GAA

# Ejecutar experimentos por familia
python 04-Generated/scripts/gaa_family_experiments.py \
    --families CUL LEI REG \
    --output results/

# Esto crea una estructura como:
# results/
#   CUL/
#     results.json  (con resultados de CUL)
#   LEI/
#     results.json  (con resultados de LEI)
#   REG/
#     results.json  (con resultados de REG)
```

**Formato esperado de results.json**:
```json
{
  "flat300_20_0": 20,
  "flat300_26_0": 26,
  "flat300_28_0": 29,
  "flat1000_50_0": 51,
  "flat1000_60_0": 60,
  "flat1000_76_0": 78
}
```

### Paso 2: Comparar con Literatura

Una vez tengas resultados, compara:

```bash
# Comparar todas las familias
python compare_with_bks.py --results-dir results/ --verbose

# Comparar una familia específica
python compare_with_bks.py --results-dir results/ --family CUL

# Exportar a JSON para análisis posterior
python compare_with_bks.py --results-dir results/ \
    --output-format json \
    --output-file comparison.json
```

### Paso 3: Interpretar Resultados

El output se vería así:

```
================================================================================
COMPARISON: CUL Family vs Best Known Solutions
================================================================================

Instance             │ BKS   │ GAA   │ Gap      │ Status
─────────────────────┼───────┼───────┼──────────┼─────────────────────
flat300_20_0         │    20 │    20 │   0.0%   │ ✅ OPTIMAL
flat300_26_0         │    26 │    26 │   0.0%   │ ✅ OPTIMAL
flat300_28_0         │    28 │    29 │  +3.6%   │ ⚠️  NEAR BKS
flat1000_50_0        │    50 │    51 │  +2.0%   │ ⚠️  NEAR BKS
flat1000_60_0        │    60 │    60 │   0.0%   │ ✅ OPTIMAL
flat1000_76_0        │    76 │    78 │  +2.6%   │ ⚠️  NEAR BKS

────────────────────────────────────────────────────────────────────────────
SUMMARY for CUL
────────────────────────────────────────────────────────────────────────────
  Total instances:        6
  Closed instances:       6 (100.0%)
  Open instances:         0 (0.0%)

  Optimality Results:
    Found optimal:      3/6 (50.0%)
    Beat BKS:           0/6 (0.0%)

  Gap Statistics:
    Average gap:        +2.13%
    Max gap:            +3.6%
    Min gap:             0.0%


════════════════════════════════════════════════════════════════════════════════
OVERALL SUMMARY: GAA vs Literature (All Families)
════════════════════════════════════════════════════════════════════════════════

  CUL       │  6 instances │ Optimal: 3/6 (50.0%) │ Beat BKS: 0
  LEI       │ 12 instances │ Optimal: 12/12 (100.0%) │ Beat BKS: 0
  REG       │ 14 instances │ Optimal: 14/14 (100.0%) │ Beat BKS: 0

────────────────────────────────────────────────────────────────────────────
  TOTALS:
    Total instances:      32
    Closed instances:     32
    Found optimal:        29/32 (90.6%)
    Beat BKS:             0/32 (0.0%)
    Average gap:          +0.84%

  CONCLUSION:
    ✅ EXCELLENT - Found optimal on majority of instances
```

---

## 📊 Interpretación de Símbolos

| Símbolo | Significado | Interpretación |
|---------|------------|-----------------|
| ✅ OPTIMAL | GAA = BKS | Perfecto - encontró el óptimo conocido |
| 🎉 BEAT BKS | GAA < BKS | ¡Excelente! GAA SUPERÓ la literatura |
| ⚠️ NEAR BKS | GAA ≈ BKS | Bueno - gap pequeño (< 1%) |
| ⚠️ GAP OK | Aceptable | Gap moderado (1-5%), aún competitivo |
| ❌ GAP LARGE | GAA >> BKS | Pobre - gap grande (> 5%) |
| ❓ OPEN | BKS desconocido | No hay referencia; cualquier solución vale |

---

## 🔍 Escenarios de Interpretación

### Escenario 1: GAA = BKS (Optimal Found) ✅

```
flat300_20_0: BKS=20, GAA=20
Status: ✅ OPTIMAL
Gap: 0.0%
```

**Interpretación**:
- GAA encontró la solución óptima conocida
- Valida que GAA puede ser tan bueno como la mejor solución documentada
- Excelente validación

---

### Escenario 2: GAA < BKS (Beat BKS) 🎉

```
DSJC125.1: BKS=?, GAA=13
Status: 🎉 BEAT BKS
Gap: -13% (comparado con mejor conocido anterior)
```

**Interpretación**:
- ¡GAA descubrió una solución MEJOR que la documentada!
- Posible contribución a la literatura
- Resultado PUBLICABLE si es en instancia abierta

---

### Escenario 3: GAA > BKS pero pequeño (Near BKS) ⚠️

```
flat300_28_0: BKS=28, GAA=29
Status: ⚠️ NEAR BKS
Gap: +3.6%
```

**Interpretación**:
- GAA está a 3.6% del óptimo
- Depende de tiempo disponible y parámetros
- Es normal - los metaheurísticos no garantizan óptimo
- Aún es competitivo

---

### Escenario 4: Instancia Abierta (Unknown) ❓

```
DSJC125.1: BKS=?, GAA=13
Status: ❓ OPEN
```

**Interpretación**:
- No hay valor de referencia en la literatura
- La solución de GAA es contribución potencial
- Compara solo contra baselines, no contra óptimo

---

## 📈 Métricas Clave

### Optimality Gap

```
Gap(%) = (GAA - BKS) / BKS × 100

Intrepretación:
  0%      → Óptimo encontrado ✅
  0-1%    → Excelente ✅
  1-5%    → Bueno ⚠️
  5-10%   → Aceptable ⚠️
  >10%    → Pobre ❌
  Negativo → BEAT BKS 🎉
```

### Success Rate

```
Success Rate = (Instancias con óptimo) / (Total instancias) × 100

Ejemplo:
  3/6 = 50% - Encontró óptimo en la mitad de instancias
```

### Beat Rate

```
Beat Rate = (Instancias que superan BKS) / (Instancias cerradas) × 100

Ejemplo:
  2/38 = 5.3% - Superó BKS en 5.3% de instancias
  (Indica si GAA descubre soluciones nuevas)
```

---

## 🏗️ Flujo Completo de Análisis

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Ejecutar Experimentos GAA                                │
│    └─ Genera: results/FAMILY/results.json                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Cargar BKS desde literatura                              │
│    └─ Archivo: datasets/BKS.json                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Comparar GAA vs BKS                                      │
│    python compare_with_bks.py                               │
│    └─ Para cada instancia: calcular gap                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Generar reporte                                          │
│    ├─ Familia: CUL (50% óptimo, +2.13% gap)               │
│    ├─ Familia: LEI (100% óptimo, 0.00% gap)               │
│    ├─ Familia: DSJ (X instancias nuevas encontradas)        │
│    └─ TOTAL: competitivo vs literatura                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Interpretación                                           │
│    ✅ ¿GAA es competitivo?                                  │
│    🎉 ¿GAA descubrió soluciones nuevas?                     │
│    📚 ¿Resultados son publicables?                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Casos de Uso Prácticos

### Caso 1: Validar que GAA funciona

```bash
# Ejecutar en instancias con óptimo conocido
python compare_with_bks.py --results-dir results/ --family CUL

# Esperado: > 50% de instancias con óptimo
# Si se logra: ✅ GAA está funcionando bien
```

### Caso 2: Descubrir soluciones nuevas

```bash
# Ejecutar en instancias abiertas
python compare_with_bks.py --results-dir results/ --family DSJ

# Si encuentra gap < 0: 🎉 Solución nueva
# Resultado publicable en conferencia
```

### Caso 3: Comparar diferentes algoritmos generados

```bash
# Ejecuta GAA con parámetros A
python gaa_family_experiments.py --params params_A.json \
    --output results_A/

# Ejecuta GAA con parámetros B
python gaa_family_experiments.py --params params_B.json \
    --output results_B/

# Compara cuál es mejor
python compare_with_bks.py --results-dir results_A/
python compare_with_bks.py --results-dir results_B/

# El que tiene menor gap promedio es mejor
```

---

## 🎯 Checkpoints de Validación

- [ ] Verificar que `datasets/BKS.json` existe y está poblado
- [ ] Ejecutar `gaa_family_experiments.py` para generar resultados
- [ ] Verificar que `results/FAMILY/results.json` se creó
- [ ] Ejecutar `compare_with_bks.py --results-dir results/`
- [ ] Revisar output y buscar:
  - ✅ Óptimos encontrados?
  - 🎉 Soluciones nuevas descubiertas?
  - ⚠️ Gaps aceptables (<5%)?
- [ ] Documentar conclusiones en reporte final

---

## 📝 Template: Documentar Resultados

Cuando ejecutes los experimentos, documenta así:

```markdown
## Resultados de Validación vs Literatura

**Fecha**: 2024-01-15
**Algoritmo Generado**: ILS-GAA-v3
**Instancias Probadas**: CUL, LEI, REG

### Resumen General
- Total Instancias: 32
- Con Óptimo: 29/32 (90.6%)
- Superó BKS: 0/32 (0.0%)
- Gap Promedio: +0.84%

### Por Familia

**CUL (Culberson)**: 
- Óptimo: 3/6 (50%)
- Gap promedio: +2.13%
- Nota: Resultados competitivos

**LEI (Leighton)**:
- Óptimo: 12/12 (100%) ✅
- Gap promedio: 0.00%
- Nota: Alcanzó garantías teóricas

**REG (Register Allocation)**:
- Óptimo: 14/14 (100%) ✅
- Gap promedio: 0.00%
- Nota: Óptimo en todas las instancias

### Conclusión
✅ GAA es COMPETITIVO con el estado del arte
- Encuentra óptimos en 90.6% de instancias con BKS conocido
- Mantiene gap < 5% en todas las instancias
- Apto para usar en producción
```

---

## 🔗 Integración con Flujos Automáticos

Para automatizar la comparación en cada ejecución, agregar al orchestrator:

```python
# En gaa_orchestrator.py
def run_complete_workflow_with_comparison(self):
    """Run GAA workflow and compare against BKS"""
    
    # ... ejecutar experimentos ...
    
    # Comparar contra literatura
    from compare_with_bks import BKSComparator
    comparator = BKSComparator()
    
    results = comparator.compare_family('CUL', gaa_results)
    analysis = comparator.analyze_results(results)
    
    print(f"\n✅ Comparison Summary:")
    print(f"   Found optimal: {analysis['optimal_found']}/{analysis['closed_instances']}")
    print(f"   Average gap: {analysis['average_gap_percent']:.2f}%")
```

---

## 🎓 Conclusión

Con esta framework de comparación:

1. **Validas** que GAA genera algoritmos competitivos
2. **Descubres** si encontró soluciones nuevas
3. **Documentas** resultados contra benchmarks abiertos
4. **Publicas** contribuciones si aplica

**Próximo paso**: Ejecuta `compare_with_bks.py` después de cada run de GAA.
