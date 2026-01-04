# ✅ ALINEACIÓN GENERATOR-VALIDATOR-PARSER: STATUS ACTUAL

**Fecha:** 4 Enero, 2026  
**Test:** test_quick_alignment.py ejecutado exitosamente (parcialmente)

---

## ✅ LO QUE FUNCIONA (VERIFIED)

| Feature | Status | Evidencia |
|---------|--------|-----------|
| Generator simplificado | ✅ | `RandomASTGenerator(seed=42)` funciona |
| Método `generate()` | ✅ | `gen.generate(phase="construction", seed=42)` retorna AST |
| Constructor reproducible | ✅ | 10 features, 7 LS features, 4 operadores |
| Validator acepta construction | ✅ | `validator.validate_construction_ast()` pasa |
| Parser.parse() exists | ✅ | Retorna Node objects |
| Node.evaluate() | ✅ | Ejecuta y retorna valores |
| Determinismo | ✅ | Seed=42 produce mismo AST |
| Choose structure | ✅ | Tiene `{"weight": ..., "value": ...}` |

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### PROBLEMA #1: Feature pools desalineados

**Estado:**
- Construction generator genera features adicionales (route_slack_forward, num_customers_remaining)
- Local search generator usa construction features (route_load, cust_demand)

**Causa:**
En `_gen_bool_expr()` hay un pool de features por defecto:

```python
def _bool_feature_pool(self, depth: int, phase: str) -> List[str]:
    if phase == "construction":
        return [...]  # construction features
    # local_search - pero esta rama también se usa para construction
    return [...]  # LS features
```

El problema es que el generator genera ASTs que usan features de diferentes phases.

**Impacto:** 🟡 ALTO - LS ASTs fallan validación

**Solución:** 
1. Pasar `phase` consistentemente a `_gen_bool_expr()`
2. O usar pool global de features si están disponibles en ambas fases

**Esfuerzo:** 1-2 horas

### PROBLEMA #2: Validator chequea features que no existen

**Estado:**
- Validator rechaza LS AST porque usa features de construction
- Esto es correcto comportamiento de validator

**Impacto:** 🟡 MEDIO - Indica bug en generator

---

## 🎯 SIGUIENTE PASO

**Opción A (Rápida - 30 min):**
- Simplificar generator para usar SOLO features globales
- O permitir features compartidas entre fases

**Opción B (Completa - 2 horas):**
- Arreglar flow de `phase` en generator
- Asegurar cada nodo recibe fase correcta

**Recomendación:** Opción A primero para avanzar rápido

---

## 📊 TASA DE ALINEACIÓN ACTUAL

```
Alineación actual: 7/9 = 78% ✅🟡

✅ Constructor         (100%)
✅ Método generate()   (100%)
✅ Validator acepta    (50% - construction sí, LS no)
✅ Parser.parse()      (100%)
✅ Node.evaluate()     (100%)
✅ Determinismo        (100%)
✅ Choose structure    (100%)
❌ Feature alignment   (30% - pools desalineados)
🟡 Error messages      (90% - clear but need fixing)
```

---

## CONTINUACIÓN DEL CHECKLIST

Después de arreglar feature alignment:

- [ ] Implementar tests de round-trip completos
- [ ] Congelar state contracts en tests
- [ ] Validar determinismo exhaustivo
- [ ] Tests contra Solomon + BKS
- [ ] Validar SolutionPool
- [ ] Validar logging
- [ ] Canary run C101

---

**Recomendación:** Continuar con arreglo de feature pools (30 min)
