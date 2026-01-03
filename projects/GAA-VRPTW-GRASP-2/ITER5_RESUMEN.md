# ITER-5: Resumen Ejecutivo

**Fecha**: Enero 3, 2026  
**Estado**: FULL experiment en ejecución (ETA: ~4 minutos)

---

## Cambios ITER-5

### ✅ ITER-5A: Revertir Algo1 a ITER-3
```
Cambio         | ITER-4 | ITER-5 | Razón
----------------|--------|---------|------------------
DoubleBridge    | 3.5    | 2.0    | Demasiado agresiva
While           | 80     | 75     | Menos iteraciones
TwoOpt (pre)    | 40     | 52     | Mantener trabajo base
OrOpt           | 18     | 28     | Balance
TwoOpt (post)   | 40     | 32     | Balance
```

**QUICK Results**:
- D: 1536.86 → 1391.51 ✅ RESTORED
- Éxito: Revertir cambios agresivos restauró baseline

### ✅ ITER-5B: Fine-tune Algo3 ITER-4B
```
Parámetro       | ITER-4B | ITER-5 | Razón
----------------|---------|---------|------------------
DoubleBridge    | 3.0     | 3.0    | MANTENER fix crítico
While           | 90      | 90     | MANTENER exploración
OrOpt           | 12      | 15     | Better balance
TwoOpt (post)   | 45      | 40     | Reduce overhead
```

**Status**: Pendiente validación en FULL

### ✅ ITER-5C: Algo2 Sin cambios
- CONTROL inmutable
- D: 1172.18 (esperado sin cambio)

---

## Lecciones ITER-4

1. **No todos los parámetros responden igual**
   - Algo1: strength=2.0 es correcto
   - Algo2: strength=3.0 es correcto
   - Algo3: strength=3.0 es correcto (no 1.0)

2. **Cambios simultáneos complican diagnosis**
   - ITER-4 cambió 5+ parámetros a la vez
   - Resultó en empeoramiento sin saber cuál fue

3. **Algoritmo 2 es ceiling natural**
   - D=1172.18 es muy fuerte
   - Esperar que Algo1/3 la igualen es poco realista
   - Mejor enfoque: aceptar diferencias, optimizar dentro de límites

---

## Próximos Pasos

1. **FULL execution (en progreso)**
   - Validar que ITER-5 restauró baseline ITER-3
   - Confirmar Algo3 fine-tune no causa regresión

2. **Análisis Post-FULL**
   - Comparar ITER-3 vs ITER-4 vs ITER-5
   - Decidir si continuar o consolidar

3. **ITER-6 (Condicional)**
   - Si Algo3 mejora con fine-tune: explorar más
   - Si no: aceptar ITER-5 como consolidación
   - Posible exploración de constructores adaptativos

---

## Métricas de Éxito ITER-5

| Métrica | Meta | Status |
|---------|------|--------|
| Algo1 restore | D ≈ 1391.51 | ✅ QUICK OK |
| Algo2 stable | D ≈ 1172.18 | ⏳ Pending FULL |
| Algo3 fine-tune | D < 1450 | ⏳ Pending FULL |

---

**Conclusión esperada**: ITER-5 fue más conservador y el éxito en QUICK (Algo1 restaurado) sugiere que fue el enfoque correcto.

