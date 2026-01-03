# ESTRATEGIA DE OPTIMIZACIÓN: ALGORITMO 1 Y 3

**Fecha**: Enero 3, 2026  
**Responsabilidad**: Optimizar Algoritmo 1 y 3 mientras Algoritmo 2 permanece como CONTROL (ITER-3)

---

## 1. SITUACIÓN ACTUAL (ITER-3)

### Resultados FULL (56 instancias):

| Algoritmo | Distancia (D) | Tiempo (s) | GAP Promedio | Estado |
|-----------|---------------|-----------|--------------|---------|
| **Algo 2** | **1172.18** | **0.18** | **24.70%** | **CONTROL** ✓ |
| Algo 1 | 1391.51 | 3.41 | 42.15% | A OPTIMIZAR |
| Algo 3 | 1504.34 | 0.69 | 52.31% | A OPTIMIZAR |

### Composición actual:

**ALGORITMO 1: GRASP Puro**
```
NearestNeighbor
  → While(75 iteraciones)
     → TwoOpt(52)
     → OrOpt(28)
     → DoubleBridge(strength=2.0)
     → TwoOpt(32)
     → Relocate(18)
```
**Problema**: Demasiadas iteraciones de control, perturbación débil, no mejora después de la perturbación

**ALGORITMO 3: GRASP Adaptativo**
```
NearestNeighbor
  → While(68 iteraciones)
     → TwoOpt(50)
     → OrOpt(20)
     → DoubleBridge(strength=1.0) ← DEMASIADO DÉBIL
     → TwoOpt(35)
     → Relocate(15)
```
**Problema**: Perturbación MUY débil (strength=1), pocas iteraciones de control

---

## 2. ANÁLISIS COMPARATIVO: ¿POR QUÉ ALGO2 GANA?

### Ventajas de Algoritmo 2:

1. **Construcción determinista** (NearestNeighbor)
   - Garantiza solución inicial de calidad
   - Reproducible y predecible
   
2. **Ciclo ILS bien balanceado**
   - LocalSearch → Perturbation → LocalSearch
   - Ciclo cerrado y potente
   
3. **Perturbación moderada y efectiva**
   - DoubleBridge(strength=3) suficientemente agresiva
   - Escapa mínimos locales sin aleatorizar demasiado
   
4. **Menos iteraciones de control**
   - While(80) es suficiente
   - Tiempo de ejecución bajo (0.18s)
   
5. **Post-mejora inmediata**
   - TwoOpt(35) después de cada perturbación
   - Aprovecha el espacio nuevo

### Desventajas de Algoritmo 1 y 3:

**Algo 1**:
- TwoOpt(52) → OrOpt(28) → Perturba → TwoOpt(32) → Relocate(18)
- Gasta recursos en TwoOpt ANTES de la perturbación
- Perturbación weak (2.0)
- Mucho tiempo sin mejorar

**Algo 3**:
- Perturbación EXTREMADAMENTE débil (1.0)
- No escapa efectivamente los mínimos locales
- While(68) no compensa

---

## 3. ESTRATEGIA DE OPTIMIZACIÓN

### Principio rector:
**"Aprender de Algo2 pero mantener identidad de Algo1 y Algo3"**

---

## 3.1 OPTIMIZACIÓN ALGORITMO 1

**Objetivo**: Mejorar de D=1391.51 a D<1250 (Δ ≈ -10%)

### Cambios propuestos:

**ITER-4A: Perturbación más fuerte y mejor posicionada**

```python
algo1 = Seq(body=[
    GreedyConstruct(heuristic='NearestNeighbor'),
    While(
        max_iterations=80,  # Reducir: 75→80 (más iteraciones del ciclo)
        body=Seq(body=[
            # Reducir TwoOpt inicial: menos gasto de recursos
            LocalSearch(operator='TwoOpt', max_iterations=40),     # 52→40 (-23%)
            
            # Mantener OrOpt pero más leve
            LocalSearch(operator='OrOpt', max_iterations=18),      # 28→18 (-36%)
            
            # AUMENTAR perturbación: más agresiva
            Perturbation(operator='DoubleBridge', strength=3.5),  # 2.0→3.5 (+75%)
            
            # Mejor re-mejora después de perturbar
            LocalSearch(operator='TwoOpt', max_iterations=40),     # 32→40 (+25%)
            
            # Mantener Relocate
            LocalSearch(operator='Relocate', max_iterations=18)    # 18→18 (sin cambio)
        ])
    )
])
```

**Rationale**:
- Menos gasto en búsqueda local ANTES de perturbar
- Perturbación más fuerte (3.5 similar a Algo2's 3.0)
- Mejor re-explotación después de perturbar
- Mantiene identidad GRASP (múltiples operadores)

**Métricas esperadas**:
- Δ GAP: -12% a -15%
- Δ Tiempo: +10% a +15% (4.0s máximo)
- Δ Distancia: 1391.51 → ~1210-1240

---

## 3.2 OPTIMIZACIÓN ALGORITMO 3

**Objetivo**: Mejorar de D=1504.34 a D<1280 (Δ ≈ -15%)

### Cambios propuestos:

**ITER-4B: Perturbación competitiva y ciclos más cortos**

```python
algo3 = Seq(body=[
    GreedyConstruct(heuristic='NearestNeighbor'),
    While(
        max_iterations=90,  # Aumentar: 68→90 (más exploración)
        body=Seq(body=[
            # TwoOpt inicial robusto
            LocalSearch(operator='TwoOpt', max_iterations=50),     # 50→50 (sin cambio)
            
            # Reducir OrOpt (menos deshabilita el espacio)
            LocalSearch(operator='OrOpt', max_iterations=12),      # 20→12 (-40%)
            
            # AUMENTAR SIGNIFICATIVAMENTE perturbación
            Perturbation(operator='DoubleBridge', strength=3.0),  # 1.0→3.0 (+200%)
            
            # Re-mejora fuerte después de perturbar
            LocalSearch(operator='TwoOpt', max_iterations=45),     # 35→45 (+29%)
            
            # Mantener Relocate
            LocalSearch(operator='Relocate', max_iterations=15)    # 15→15 (sin cambio)
        ])
    )
])
```

**Rationale**:
- Perturbación CRÍTICA: strength=1 es inutilizable
- strength=3 es competitiva con Algo2
- Menos OrOpt (operador caro) pero más exploración global
- While(90) permite más ciclos (time penalty mínimo)

**Métricas esperadas**:
- Δ GAP: -18% a -22%
- Δ Tiempo: +20% a +30% (0.95s máximo)
- Δ Distancia: 1504.34 → ~1190-1240

---

## 4. PLAN DE EJECUCIÓN

### Fase 1: ITER-4A (Algoritmo 1)

```bash
# 1. Crear rama experimental
git checkout -b feat/iter4a-algo1-optimization

# 2. Modificar solo Algo 1 en algorithm_generator.py
#    - Strength: 2.0 → 3.5
#    - TwoOpt(52) → TwoOpt(40)
#    - OrOpt(28) → OrOpt(18)
#    - TwoOpt(32) → TwoOpt(40)
#    - While(75) → While(80)

# 3. Ejecutar QUICK validation (R1 family)
python scripts/experiments.py --mode QUICK

# 4. Si GAP mejora > 10%, ejecutar FULL validation
python scripts/experiments.py --mode FULL

# 5. Comparar vs ITER-3:
#    Expected: D: 1391.51 → ~1210-1240
#    Expected: Tiempo: 3.41s → ~3.6-4.0s
```

### Fase 2: ITER-4B (Algoritmo 3)

```bash
# 1. Merge ITER-4A si es exitoso
# 2. Crear rama para Algo 3
git checkout -b feat/iter4b-algo3-optimization

# 3. Modificar solo Algo 3 en algorithm_generator.py
#    - Strength: 1.0 → 3.0 ← CRÍTICO
#    - While(68) → While(90)
#    - TwoOpt(35) → TwoOpt(45)
#    - OrOpt(20) → OrOpt(12)

# 4. Ejecutar QUICK validation
python scripts/experiments.py --mode QUICK

# 5. Ejecutar FULL validation si mejora > 15%
python scripts/experiments.py --mode FULL

# Expected: D: 1504.34 → ~1190-1240
# Expected: Tiempo: 0.69s → ~0.90-1.05s
```

### Fase 3: CONSOLIDACIÓN

```bash
# Merge both successful iterations
git merge feat/iter4a-algo1-optimization
git merge feat/iter4b-algo3-optimization

# Final comparison table
# ITER-3 → ITER-4A/4B results
```

---

## 5. MÉTRICAS DE ÉXITO

### Criterios de aceptación:

| Métrica | Umbral mínimo | Umbral óptimo |
|---------|---------------|---------------|
| **Algo 1 GAP reduction** | > 8% | > 12% |
| **Algo 1 Distancia** | < 1280 | < 1240 |
| **Algo 1 Tiempo** | < 4.5s | < 4.0s |
| **Algo 3 GAP reduction** | > 12% | > 18% |
| **Algo 3 Distancia** | < 1300 | < 1250 |
| **Algo 3 Tiempo** | < 1.0s | < 0.95s |
| **Algo 2 (Control)** | Unchanged | **NO TOCAR** |

---

## 6. ESCENARIOS POSIBLES

### Escenario A: Ambos algoritmos mejoran > 10%
✓ **Acción**: Mantener ITER-4A y ITER-4B como nuevos baselines
✓ **Documentación**: Crear ITER4_RESULTADOS.md
✓ **Next**: Considerar ITER-5 si aún hay margen

### Escenario B: Solo Algo 1 mejora > 10%
✓ **Acción**: Mantener ITER-4A, revisar Algo 3 diferentemente
⚠ **Issue**: Algo 3 strength=3 puede no ser suficiente
✓ **Next**: Probar strength=4 o cambiar operadores

### Escenario C: Ambos mejoran < 5%
⚠ **Acción**: Investigar si parámetros ITER-3 ya están optimizados
✓ **Alternativa**: Prueba constructor adaptativo (RandomizedInsertion para familias C)

### Escenario D: Empeoran (raro)
✗ **Acción**: Revertir cambios inmediatamente
✓ **Investigación**: Parámetros conflictivos o efectos secundarios

---

## 7. PRÓXIMAS INVESTIGACIONES (Post ITER-4)

Si ITER-4 es exitoso:

1. **Constructor adaptativo** para familias clustered (C1, C2)
   - NearestNeighbor para R/RC (bueno)
   - RandomizedInsertion para C (adaptarse a clustered structure)

2. **Operadores alternativos**
   - Three-opt para Algo 1 (explore if time permits)
   - VND-like secuencing para Algo 3 (como está, pero mejor)

3. **Hiperparámetros de Algo 2**
   - Si Algo 1/3 se acercan a Algo 2, revisar si Algo 2 tiene ceiling
   - Potencial fine-tuning final

---

## 8. DOCUMENTACIÓN REQUERIDA

Crear archivo `ITER4_RESULTADOS.md` después de cada fase:
- Tabla de comparación ITER-3 vs ITER-4A/4B
- Gráficos GAP por familia
- Análisis de qué cambios funcionaron
- Recomendaciones para futuro

---

## RESUMEN EJECUTIVO

| Fase | Objetivo | Cambio CLAVE | Meta |
|------|----------|--------------|------|
| **ITER-4A** | Mejorar Algo 1 | Strength 2.0→3.5 | D < 1240 |
| **ITER-4B** | Mejorar Algo 3 | Strength 1.0→3.0 | D < 1250 |
| **CONTROL** | Mantener Algo 2 | ❌ NO CAMBIAR | D = 1172.18 |

**Filosofía**: Aprender de Algo 2 (perturbación + ILS cycle) sin perder identidad de GRASP puro/adaptativo.
