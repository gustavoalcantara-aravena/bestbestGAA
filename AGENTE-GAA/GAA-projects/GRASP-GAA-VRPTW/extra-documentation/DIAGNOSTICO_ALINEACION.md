# 📊 DIAGNOSTICO DE ALINEACIÓN: Generator ↔ Validator ↔ Parser

**Fecha:** 4 Enero, 2026  
**Status:** Análisis realizado  
**Resultado:** ⚠️ ALINEACIÓN PARCIAL - 10 problemas identificados

---

## ✅ ALINEADO CORRECTAMENTE (11/21)

| Tipo | Generator | Validator | Parser | Estado |
|------|-----------|-----------|--------|--------|
| Const | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Feature | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Add | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Sub | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Mul | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Div | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Less | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Greater | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| And | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| Or | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |
| If | ✅ genera | ✅ permite | ✅ evalúa | ✅ OK |

---

## ❌ PROBLEMAS IDENTIFICADOS

### 🔴 PROBLEMA #1: WeightedSum en Generator

**Estado:**
- ✅ Validator: Permitido en DEFAULT_ALLOWED_NODE_TYPES
- ✅ Parser: Implementado (lines 59-62)
- ❓ Generator: ¿SE GENERA?

**Búsqueda en generator.py:**
```
Line 233: return {"type": "WeightedSum", "terms": terms}
```

**Conclusión:** ✅ SE GENERA (en _gen_numeric_expr)

**Status:** ✅ ALINEADO

---

### 🔴 PROBLEMA #2: Normalize en Generator

**Estado:**
- ✅ Validator: Permitido
- ✅ Parser: Implementado (lines 64-69)
- ❓ Generator: ¿SE GENERA?

**Búsqueda en generator.py:**
```
No hay línea que genere "type": "Normalize"
```

**Conclusión:** ❌ NO SE GENERA (aunque Validator permite)

**Status:** ⚠️ MISALIGNED - Generator no produce Normalize

**Impacto:** Si Validator ve un Normalize, probablemente vino de otro lado (error del usuario)

---

### 🔴 PROBLEMA #3: Clip en Generator

**Estado:**
- ✅ Validator: Permitido
- ✅ Parser: Implementado (lines 71-72)
- ❓ Generator: ¿SE GENERA?

**Conclusión:** ❌ NO SE GENERA

**Status:** ⚠️ MISALIGNED

---

### 🔴 PROBLEMA #4: Choose en Generator

**Estado:**
- ✅ Validator: Permitido
- ✅ Parser: Implementado (lines 111-116)
- ✅ Generator: Line 385 - se genera

**Pero:** Parser devuelve `options[0]` siempre (línea 115)

```python
# línea 115 en parser.py
return self.evaluate(options[0], state)  # ← SIEMPRE OPCIÓN 0!
```

**Problema:** Choose debe seleccionar ALEATORIAMENTE basado en pesos, pero Parser SIEMPRE elige opción 0.

**Status:** 🔴 CRÍTICO - Choose es inútil así

**Impacto:** Local search NUNCA variará entre operadores

---

### 🔴 PROBLEMA #5: Estructura de Choose en Generator

**Generator genera:**
```python
"type": "Choose",
"options": [{"type": "Const", "value": op} for op in chosen_ops]
```

**Pero Validator espera:**
```python
"options": [
  {"weight": 0.3, "value": "TwoOpt"},
  {"weight": 0.5, "value": "Relocate"},
  ...
]
```

**Conclusión:** ❌ GENERATOR PRODUCE ESTRUCTURA INCORRECTA

**Status:** 🔴 CRÍTICO - Choose tiene estructura incompatible

---

### 🔴 PROBLEMA #6: Parser.parse() no existe

**Estado:**
- Generator llama a: `parser.parse(ast)` (línea 26 en generator.py)
- Parser actual: NO tiene método `parse()`
- Parser solo tiene: `evaluate(node, state)`

**Conclusión:** ❌ FALTA MÉTODO

**Status:** 🔴 CRÍTICO - Generator espera parse(), Parser no lo tiene

---

### 🔴 PROBLEMA #7: Generator constructor

**Estado:**
```python
def __init__(
    self,
    rng: random.Random,
    construction_features: List[str],
    ls_features: List[str],
    ls_operators: List[str],
    limits: GenLimits,
    const_float_range: Tuple[float, float] = (-5.0, 5.0),
):
```

**Pero test llama:**
```python
gen = RandomASTGenerator(seed=42)
```

**Conclusión:** ❌ Constructor NO COINCIDE

**Status:** 🔴 CRÍTICO - Test espera constructor distinto

---

### 🔴 PROBLEMA #8: Validator no checa features contra estado

**Validator permite:**
- Features definidas manualmente
- NO verifica que existan en estado correspondiente (construction vs local_search)

**Conclusión:** ❌ VALIDATOR INCOMPLETO

**Status:** ⚠️ RIESGO - Validator acepta ASTs inválidos (features que no existen en estado)

---

### 🔴 PROBLEMA #9: Parser Choose sin RNG

**Parser.evaluate() NO tiene RNG:**
```python
def evaluate(self, node: Dict[str, Any], state: Dict[str, Any]) -> Any:
    # No hay parámetro rng
```

**Pero Choose necesita RNG para seleccionar:**
```python
if t == "Choose":
    # ← Necesitaría RNG aquí para weighted selection
    return self.evaluate(options[0], state)
```

**Conclusión:** ❌ PARSER NO PUEDE HACER RANDOM CHOICE

**Status:** 🔴 CRÍTICO - Choose siempre elige opción 0

---

### 🔴 PROBLEMA #10: Generator sin método generate()

**Test llama:**
```python
ast = gen.generate(phase="construction", seed=42)
```

**Pero Generator tiene:**
```python
def generate_algorithm_json(self, algorithm_id: str, seed: int) -> Dict[str, Any]:
```

**Conclusión:** ❌ MÉTODO NO EXISTE

**Status:** 🔴 CRÍTICO - Test espera `generate()`, no existe

---

## 📋 RESUMEN DE SEVERIDAD

| Severidad | Cantidad | Problemas |
|-----------|----------|-----------|
| 🔴 CRÍTICO | 5 | #4, #5, #6, #7, #10 |
| ⚠️ ALTO | 3 | #2, #3, #8 |
| 🟡 MEDIO | 2 | #9, #1 |

---

## 🎯 PLAN DE ACCIÓN

### PRIMERO (Bloquea todo)

**Paso 1: Arreglar Constructor de Generator**

Current:
```python
def __init__(self, rng, construction_features, ls_features, ...):
```

Target:
```python
def __init__(self, seed=42):
    self.rng = random.Random(seed)
    self.construction_features = [...]  # Hardcoded or from config
    self.ls_features = [...]
    self.ls_operators = [...]
    self.limits = GenLimits(max_depth=10, max_function_nodes=50)
```

**Paso 2: Agregar método `generate()`**

```python
def generate(self, phase: str, seed: int) -> Dict[str, Any]:
    """phase: 'construction' | 'local_search'"""
    ctx = GenContext(
        rng=random.Random(seed),
        limits=self.limits
    )
    if phase == "construction":
        return self._gen_numeric_expr(ctx, depth=0, ...)
    else:  # local_search
        return self._gen_operator_selector(ctx, ...)
```

**Paso 3: Arreglar estructura de Choose**

Generator debe producir:
```python
{
    "type": "Choose",
    "options": [
        {"weight": 0.3, "value": "TwoOpt"},
        {"weight": 0.5, "value": "Relocate"},
        {"weight": 0.2, "value": "OrOpt"},
    ]
}
```

No esto:
```python
{
    "type": "Choose",
    "options": [{"type": "Const", "value": op}]
}
```

**Paso 4: Implementar Parser.parse() que retorna Node**

```python
def parse(self, ast: Dict[str, Any]) -> Node:
    """Convierte JSON AST a objeto Node executable."""
    # Retorna ConstNode, FeatureNode, AddNode, etc
```

**Paso 5: Agregar RNG a Parser.evaluate()**

```python
def evaluate(self, node: Dict[str, Any], state: Dict[str, Any], rng: random.Random = None) -> Any:
    # Si node es Choose y rng existe, hacer weighted selection
    if t == "Choose":
        options = node.get("options", [])
        weights = [opt["weight"] for opt in options]
        values = [opt["value"] for opt in options]
        selected = rng.choices(values, weights=weights, k=1)[0]
        return selected
```

**Paso 6: Hacer Validator chequee features contra estado**

En validator.py, agregar:
```python
def validate_features_in_state(self, ast: Dict, phase: str) -> List[str]:
    """Retorna lista de features que NO existen en estado."""
    features_used = self._collect_features(ast)
    
    if phase == "construction":
        valid_features = CONSTRUCTION_STATE_KEYS
    else:
        valid_features = LOCAL_SEARCH_STATE_KEYS
    
    missing = features_used - valid_features
    return list(missing)
```

---

## 🧪 TESTS AFECTADOS

- ✅ TestASTLanguageAlignment.test_generator_produces_only_allowed_types() → PASA (tipos OK)
- ❌ TestASTLanguageAlignment.test_parser_supports_all_allowed_types() → FALLA (falta Normalize/Clip)
- ❌ TestASTRoundTrip.test_construction_ast_roundtrip() → FALLA (constructor diferente)
- ❌ TestASTRoundTrip.test_local_search_ast_roundtrip() → FALLA (Choose roto)
- ❌ TestDeterminism.test_generator_determinism() → FALLA (método no existe)
- ❌ TestDeterminism.test_parser_no_rng() → FALLA (Parser no es puro)

---

## ✅ CONCLUSIÓN

**Actual:** Validator y Parser están ~80% correctos, pero Generator está ~40% alineado

**Necesario:** 
1. Arreglar constructor Generator (30 min)
2. Agregar método generate() (20 min)
3. Arreglar estructura Choose (20 min)
4. Implementar Parser.parse() (40 min)
5. Agregar RNG a Parser.evaluate() (20 min)
6. Validator chequee features (30 min)

**Total: ~2-3 horas de work**

**Orden crítico:**
1. Constructor Generator → generates() (50 min)
2. Parser.parse() + RNG (60 min)
3. Validator features (30 min)

Luego: Tests deben pasar 100%
