# ITER-4: Optimización Científica para Familias Clustered

**Fecha**: 03-01-2026  
**Status**: PLANIFICACIÓN → EJECUCIÓN  
**Método**: Modificación directa del Algoritmo 2 (que es el ganador)  
**Hipótesis**: Mayor perturbación + más iteraciones = escape de mínimos locales en C2

---

## 📊 Problema Identificado

### Análisis de Resultados FULL (ITER-3)

**Algoritmo 2 - Fortalezas y Debilidades:**

| Familia | Promedio GAP | Estado | Diagnosis |
|---------|-------------|--------|-----------|
| **R1** (Random 100) | **-0.60%** ✅ | EXCELENTE | Supera BKS |
| **R2** (Random 1000) | +25.90% ✅ | BUENO | Aceptable |
| **RC1** (Mixed 100) | **-7.06%** ✅ | EXCELENTE | Supera BKS |
| **RC2** (Mixed largo) | +16.98% ✅ | MUY BUENO | Competitivo |
| **C1** (Clustered 100) | +33.09% ⚠️ | MODERADO | Aceptable |
| **C2** (Clustered largo) | **+94.76%** ❌ | **CRÍTICO** | **FALLO SISTEMÁTICO** |

### 🔴 CRÍTICA: Familia C2

```
Hallazgo:
- Algoritmo 2 produce SIEMPRE distancia = 1148.78
- BKS publicado = 589.86
- GAP = +94.76%
- Todas 8 instancias C2 (C201-C208) tienen el MISMO valor

Interpretación:
✗ El algoritmo está atrapado en un mínimo local único
✗ No está explorando suficientemente el espacio de soluciones
✗ Perturbación DoubleBridge(3.0) es INSUFICIENTE para escapar
```

---

## 🔬 Estrategia ITER-4 (Método Directo)

### Cambios al Algoritmo 2

**ITER-3 (Baseline - FUNCIONA PARA R/RC):**
```python
Seq(body=[
    GreedyConstruct(heuristic='NearestNeighbor'),
    While(max_iterations=80,  # Iteraciones
        body=Seq(body=[
            LocalSearch(operator='TwoOpt', max_iterations=50),
            Perturbation(operator='DoubleBridge', strength=3),  # ← Insuficiente para C2
            LocalSearch(operator='TwoOpt', max_iterations=35),
            LocalSearch(operator='Relocate', max_iterations=20)
        ])
    )
])
```

**ITER-4 (PROPUESTA - MÁS FUERTE):**
```python
Seq(body=[
    GreedyConstruct(heuristic='NearestNeighbor'),
    While(max_iterations=120,  # +50% más iteraciones (de 80 a 120)
        body=Seq(body=[
            LocalSearch(operator='TwoOpt', max_iterations=60),  # +20% (50→60)
            Perturbation(operator='DoubleBridge', strength=5),  # ← MÁS AGRESIVA (3→5)
            LocalSearch(operator='TwoOpt', max_iterations=40),  # +14% (35→40)
            LocalSearch(operator='Relocate', max_iterations=25)  # +25% (20→25)
        ])
    )
])
```

### Cambios Específicos

| Componente | ITER-3 | ITER-4 | Cambio | Objetivo |
|-----------|--------|--------|--------|----------|
| While Iteraciones | 80 | 120 | +50% | Más exploración |
| TwoOpt #1 | 50 | 60 | +20% | Mejorar más después de construcción |
| DoubleBridge strength | 3.0 | 5.0 | +67% | Escape más agresivo |
| TwoOpt #2 | 35 | 40 | +14% | Mejorar más después de perturbar |
| Relocate | 20 | 25 | +25% | Mayor diversidad de operadores |

**Justificación:**
- Algoritmo 2 es excelente en R/RC (no tocar constructor)
- El problema es escape de mínimos locales en C2
- Solución: perturbación más fuerte + más iteraciones = mayor exploración

---

## 📋 Hipótesis Formales

### H0 (Nula)
Aumentar perturbación y iteraciones NO mejora significativamente C2

### H1 (Alternativa)
Aumentar perturbación y iteraciones MEJORA significativamente C2 (GAP reducido > 20%)

### Métrica de Decisión
```
Δ GAP = GAP_ITER3 - GAP_ITER4
Éxito si: Δ GAP > 20 puntos porcentuales
  (Significa reducir +94.76% a < 75%)
```

---

## 🛠️ Plan de Ejecución

### Fase 1: Modificación (Esta sesión)
- [x] Documentar cambios esperados
- [ ] Modificar `algorithm_generator.py` con Algo2 ITER-4
- [ ] Verificar que código compila correctamente

### Fase 2: Experimentación
- [ ] Ejecutar QUICK experiment en C2 (8 instancias)
- [ ] Ejecutar FULL experiment (56 instancias, validar R/RC no empeoraron)
- [ ] Registrar resultados en CSV

### Fase 3: Análisis
- [ ] Calcular mejora en C2
- [ ] Validar que R/RC no empeoraron significativamente
- [ ] Test de hipótesis

### Fase 4: Documentación
- [ ] Completar `ITER4_PLAN.md` Sección de Resultados
- [ ] Actualizar `ITERACIONES_COMPLETAS_ANALISIS.md` Sección 11
- [ ] Crear tabla comparativa ITER-3 vs ITER-4

---

## 📊 Métricas de Éxito

| Métrica | Baseline ITER-3 | Target ITER-4 | Status |
|---------|-----------------|---------------|--------|
| **C2 Avg GAP** | +94.76% | < 75% (Δ>20%) | Hipótesis |
| **C2 Std Dev** | 0% (todas iguales) | > 5% | Exploración |
| **C1 Avg GAP** | +33.09% | No empeorar (< 35%) | Constraint |
| **R1 Avg GAP** | -0.60% | No empeorar (< 5%) | Constraint |
| **R2 Avg GAP** | +25.90% | No empeorar (< 30%) | Constraint |
| **RC1 Avg GAP** | -7.06% | No empeorar (< 5%) | Constraint |
| **RC2 Avg GAP** | +16.98% | No empeorar (< 20%) | Constraint |

---

## 🎯 Decisiones Post-ITER-4

### Escenario 1: ÉXITO (Δ GAP > 20%)
✅ **Acción**: Aceptar ITER-4 como final
- Algoritmo 2 mejorado es la versión final
- Listo para PUBLICACIÓN
- Documentar que "perturbación más agresiva resuelve C2"

### Escenario 2: ÉXITO PARCIAL (10% < Δ GAP ≤ 20%)
⚠️ **Acción**: Investigación adicional
- ITER-5: Probar DoubleBridge(strength=6-7)
- O: Añadir nuevo operador de perturbación (EjectionChain)
- Decisión: ¿Continuar o aceptar limitación?

### Escenario 3: FRACASO (Δ GAP ≤ 10%)
❌ **Acción**: Aceptar limitación
- Documentar que C2 es límite fundamental del algoritmo
- Publicar con especialidad clara: EXCELENTE en R/RC, MODERADO en C
- Recomendar: Para aplicaciones reales con clustering, considerar híbridos

---

## 📚 Documentación Esperada

Al completar ITER-4:

1. **Este documento** - Plan científico y resultados
2. **algorithm_generator.py** - Código modificado con Algo2 ITER-4
3. **output/ITER4_C2_*/results.csv** - Datos experimentales
4. **ITERACIONES_COMPLETAS_ANALISIS.md** Sección 11 - Análisis final

---

## 🔗 Próximos Pasos

1. Modificar `algorithm_generator.py`
2. Ejecutar `python scripts/experiments.py --mode QUICK` (validación rápida en R1)
3. Ejecutar `python scripts/experiments.py --mode FULL` (validación completa)
4. Analizar resultados
5. Documentar conclusiones

