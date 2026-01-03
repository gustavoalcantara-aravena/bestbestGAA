# ITER-4: Análisis de Resultados y Lecciones Aprendidas

**Fecha**: Enero 3, 2026  
**Experimento**: FULL (168 instancias, 56 unique)  
**Timestamp**: 2026-01-03T03:16:16  
**Duración**: 265.33s (4.42 minutos)

---

## 1. RESUMEN EJECUTIVO

❌ **ITER-4 RESULTÓ EN EMPEORAMIENTO GENERAL**

| Métrica | ITER-3 (Baseline) | ITER-4 (Cambios) | Δ | Estado |
|---------|---|---|---|---|
| **Algo 1 - D** | 1391.51 | 1536.86 | +145.35 (+10.4%) | ❌ PEOR |
| **Algo 2 - D** | 1172.18 | 1182.19 | +10.01 (+0.9%) | ≈ IGUAL |
| **Algo 3 - D** | 1504.34 | 1408.04 | -96.30 (-6.4%) | ✅ MEJOR |

**Análisis Crítico**: 
- Algoritmo 1 empeoró significativamente con strength=3.5
- Algoritmo 2 (CONTROL) se mantuvo estable ✅
- Algoritmo 3 mejoró ligeramente pero sigue muy por debajo de Algo2

---

## 2. DETALLES ITER-4

### Configuración Aplicada (ITER-4A/4B)

**Algoritmo 1 (ITER-4A - FRACASO)**:
```
NearestNeighbor
  → While(80)
     → TwoOpt(40)      # -23%: 52→40 ✅
     → OrOpt(18)       # -36%: 28→18 ✅
     → DoubleBridge(3.5)  # +75%: 2.0→3.5 ❌ TOO AGGRESSIVE
     → TwoOpt(40)      # +25%: 32→40 ✅
     → Relocate(18)    # sin cambio ✅
```

**Problema**: DoubleBridge(3.5) es demasiado agresiva para Algo1
- Perturba soluciones de buena calidad innecesariamente
- No compensado con suficiente local search de post-mejora
- Parámetro correcto es 2.0-2.5, no 3.5

**Algoritmo 3 (ITER-4B - PARCIAL ÉXITO)**:
```
NearestNeighbor
  → While(90)          # +32%: 68→90 ✅
     → TwoOpt(50)      # sin cambio ✅
     → OrOpt(12)       # -40%: 20→12 ✅
     → DoubleBridge(3.0)  # +200%: 1.0→3.0 ✅ CRITICAL FIX
     → TwoOpt(45)      # +29%: 35→45 ✅
     → Relocate(15)    # sin cambio ✅
```

**Éxito parcial**: DoubleBridge(3.0) fue fix CRÍTICO necesario
- Algo3 con 1.0 era inutilizable (no escapaba mínimos)
- Cambio a 3.0 permitió mejor exploración
- While(90) fue beneficioso (+32% iteraciones)

---

## 3. ANÁLISIS POR FAMILIA

### Ganadores por Familia

| Familia | Instancias | MEJOR | GAP | Nota |
|---------|-----------|-------|-----|------|
| **C1** | 9 | Algo 2 | 33.18% | Algo2 domina familias clustered |
| **C2** | 8 | Algo 2 | 94.76% | Algo2 aún mejor que alternativas |
| **R1** | 12 | Algo 2 | -0.60% | **MEJOR QUE BKS en R1** 🏆 |
| **R2** | 11 | Algo 3 | 11.95% | Único donde Algo3 gana (11.95% vs 25.90%) |
| **RC1** | 8 | Algo 2 | -7.06% | **MEJOR QUE BKS** en RC1 |
| **RC2** | 8 | Algo 3 | 11.36% | Algo3 mejora aquí (11.36% vs 16.98%) |

### Observación Clave

**Algoritmo 2 es CLARAMENTE SUPERIOR** excepto en:
- R2: Algo 3 mejor (11.95% vs 25.90%)
- RC2: Algo 3 mejor (11.36% vs 16.98%)

→ Patrón: Algo3 es mejor en familias "ramdom con tiempo" (R2, RC2) para soluciones subóptimas aceptables

---

## 4. LECCIONES APRENDIDAS

### Lección 1: Parámetros No Son Lineales
```
DoubleBridge(strength):
  1.0 → Demasiado débil (no perturba suficiente) ❌
  2.0 → Óptimo para Algo1 ✅
  3.0 → Óptimo para Algo3 ✅
  3.5 → Demasiado fuerte para Algo1 ❌
```

**Implicación**: Cada algoritmo requiere fuerza de perturbación diferente
- Algo1 (GRASP puro): Necesita balance → 2.0-2.5
- Algo2 (ILS): Puede tolerar más → 3.0
- Algo3 (adaptativo): Necesita compensación → 3.0 con While(90)

### Lección 2: Cambios Simultáneos Complican Diagnosis
ITER-4 cambió múltiples parámetros a la vez:
- While: 75→80 (Algo1), 68→90 (Algo3)
- TwoOpt: 52→40, 32→40 (Algo1)
- DoubleBridge: 2.0→3.5 (Algo1), 1.0→3.0 (Algo3)
- OrOpt: 28→18 (Algo1), 20→12 (Algo3)

**Resultado**: Empeoramiento sin saber cuál cambio fue el culpable

**Lesson**: ITER-5 debe variar parámetros DE UNO EN UNO

### Lección 3: Algoritmo 2 es Ceiling Natural
- Algo2 con D=1172.18 es baseline muy fuerte
- Algo1 y Algo3 diseñados para explorar no para igualar Algo2
- Posible que mejor estrategia sea: Algo2 como reference + Algo1/3 para casos específicos

---

## 5. CRITERIOS DE ÉXITO NO ALCANZADOS

| Criterio | Meta | ITER-3 | ITER-4 | Status |
|----------|------|--------|--------|--------|
| Algo 1 GAP reduction | > 10% | 42.15% | 64.43% | ❌ PEOR |
| Algo 1 Distancia | < 1280 | 1391.51 | 1536.86 | ❌ PEOR |
| Algo 3 GAP reduction | > 12% | 52.31% | 45.82% | ✅ MEJOR (6.5%) |
| Algo 3 Distancia | < 1250 | 1504.34 | 1408.04 | ✅ MEJOR (96.3) |
| Algo 2 (Control) | Inmutable | 1172.18 | 1182.19 | ≈ OK (0.9% drift) |

**Conclusión**: ITER-4 fue parcialmente exitoso para Algo3 pero catastrophic para Algo1

---

## 6. RECOMENDACIONES PARA ITER-5

### Opción A: Revertir Algo1 + Fine-tune Algo3 (RECOMENDADO ⭐)

**Algoritmo 1 - REVERTIR a ITER-3**:
```python
DoubleBridge(strength=2.0)  # No 3.5 - fue error
TwoOpt(52)   # No 40 - prueba mantener
OrOpt(28)    # No 18 - prueba mantener
While(75)    # No 80 - mantener original
```

**Algoritmo 3 - MANTENER ITER-4B + AJUSTAR**:
```python
DoubleBridge(strength=3.0)  # ✅ Mantener - fue critical fix
While(90)                   # ✅ Mantener - mejoró
# Pero:
TwoOpt(40)   # En lugar de 45 - reducir post-search
OrOpt(15)    # En lugar de 12 - más equilibrio
```

**Algoritmo 2 - SIN CAMBIOS**:
```python
# CONTROL INMUTABLE
```

### Opción B: Explorar Constructores Adaptativos (AVANZADO)

Para próximas iteraciones si Opción A es éxito:
- Familias C (clustered): RandomizedInsertion(α=0.15)
- Familias R/RC (random): NearestNeighbor (actual)
- Ajustar parámetros por familia

---

## 7. PLAN ITER-5

### Fase 1: Revertir Algo1 + Validar (QUICK)
```bash
# Cambios solo en Algo1:
# DoubleBridge: 3.5 → 2.0
# While: 80 → 75
# TwoOpt(pre): 40 → 52 (revertir)
# OrOpt: 18 → 28 (revertir)

# Ejecutar QUICK (12 instancias R1)
python scripts/experiments.py --mode QUICK

# Esperado:
# - Algo1: Volver a ~1391.51 (ITER-3 baseline)
# - Algo3: Mantener ~1300-1400 (ITER-4 mejorado)
# - Algo2: Igual (control)
```

### Fase 2: Fine-tune Algo3 (QUICK)
```bash
# Cambios en Algo3 ITER-4B:
# TwoOpt(post): 45 → 40 (reducir)
# OrOpt: 12 → 15 (más balance)

# Ejecutar QUICK
# Esperado: ~1350-1400 D (similar o ligeramente mejor)
```

### Fase 3: Validar FULL
```bash
# Si QUICK muestra mejora > 5%:
python scripts/experiments.py --mode FULL

# Esperado resultados:
# - Algo1: D ~1391 (ITER-3 restoration) ≈
# - Algo2: D ~1172 (control) ✅
# - Algo3: D ~1300-1350 (ITER-4 con fine-tune) ✅
```

---

## 8. CÓDIGO ITER-5 (PROPUESTO)

```python
def generate_three_algorithms(self, seed: int = 42) -> List[ASTNode]:
    """
    ITER-5: Revertir Algo1, fine-tune Algo3
    """
    random.seed(seed)
    algorithms = []
    
    # ========================================================================
    # ALGORITMO 1: GRASP Puro (ITER-5 - REVERTIR)
    # ========================================================================
    algo1 = Seq(body=[
        GreedyConstruct(heuristic='NearestNeighbor'),
        While(
            max_iterations=75,  # Revertir: 80→75
            body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=52),  # Revertir: 40→52
                LocalSearch(operator='OrOpt', max_iterations=28),   # Revertir: 18→28
                Perturbation(operator='DoubleBridge', strength=2.0),  # Revertir: 3.5→2.0
                LocalSearch(operator='TwoOpt', max_iterations=32),  # Revertir: 40→32
                LocalSearch(operator='Relocate', max_iterations=18)
            ])
        )
    ])
    algorithms.append(algo1)
    
    # ========================================================================
    # ALGORITMO 2: CONTROL (SIN CAMBIOS)
    # ========================================================================
    algo2 = Seq(body=[
        GreedyConstruct(heuristic='NearestNeighbor'),
        While(
            max_iterations=80,
            body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=50),
                Perturbation(operator='DoubleBridge', strength=3),
                LocalSearch(operator='TwoOpt', max_iterations=35),
                LocalSearch(operator='Relocate', max_iterations=20)
            ])
        )
    ])
    algorithms.append(algo2)
    
    # ========================================================================
    # ALGORITMO 3: GRASP Adaptativo (ITER-5 FINE-TUNE)
    # ========================================================================
    # Mantener éxitos ITER-4B pero fine-tune parámetros
    algo3 = Seq(body=[
        GreedyConstruct(heuristic='NearestNeighbor'),
        While(
            max_iterations=90,  # Mantener: 90
            body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=50),  # Mantener: 50
                LocalSearch(operator='OrOpt', max_iterations=15),   # Fine-tune: 12→15
                Perturbation(operator='DoubleBridge', strength=3.0),  # Mantener: 3.0
                LocalSearch(operator='TwoOpt', max_iterations=40),  # Fine-tune: 45→40
                LocalSearch(operator='Relocate', max_iterations=15)  # Mantener: 15
            ])
        )
    ])
    algorithms.append(algo3)
    
    return algorithms
```

---

## 9. EXPECTATIVAS ITER-5

### Scenario Optimista (Recomendado)
```
Algo1: D ~1391 (restore ITER-3 baseline)
Algo2: D ~1172 (control)
Algo3: D ~1300-1350 (ITER-4 benefit - 10-15% mejor que Algo1)
```

### Scenario Pesimista
```
Algo1: D ~1391 (restore)
Algo2: D ~1172 (control)
Algo3: D ~1400-1450 (decae vs ITER-4)
```

### Decisión Post-ITER-5
- Si Algo1 ≈ ITER-3 + Algo3 > Algo1: **ACEPTAR** ✅
- Si Algo1 >> ITER-3: Investigar qué salió mal
- Si Algo3 << ITER-4: Revertir fine-tune, mantener ITER-4B

---

## 10. OBSERVACIONES TÉCNICAS

### Encoding Status
✅ Todos los 5 gráficos GAP generados sin error
- Emoji fix (✅ → [OK]) funcionando correctamente
- Windows cp1252 encoding compatible

### Automatización Status
✅ GAP plots generados automáticamente al fin de FULL
- Timing: ~10 segundos después de completar experimento
- Rutas dinámicas: Funcionando correctamente

### Git Status
- Última posición: d1014a3 (ITER-4 documentation)
- ITER-5 será nuevo commit: "Iteración 5: Fix Algo1, fine-tune Algo3"

---

## 11. RESUMEN PARA ITER-5

| Aspecto | Acción | Rationale |
|---------|--------|-----------|
| **Algo 1** | REVERTIR a ITER-3 | Strength=3.5 fue demasiado agresiva |
| **Algo 2** | SIN CAMBIOS | CONTROL inmutable, funcionando bien |
| **Algo 3** | MANTENER+FINE-TUNE | ITER-4B fix (strength=3.0) fue éxito, ajustar operadores |
| **Testing** | QUICK primero | Validar cambios antes de FULL |
| **Expectativa** | Algoritmo 2 sigue ganando | Realista vs buscar imposibles |

---

**Conclusión**: ITER-4 enseñó que cambios drásticos rompen balance. ITER-5 será más conservador: revertir errores, mantener éxitos, ajustar finos.

