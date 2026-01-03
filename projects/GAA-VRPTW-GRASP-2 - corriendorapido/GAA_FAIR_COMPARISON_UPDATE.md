# ACTUALIZACIÓN: GAA con Comparación Justa (depth=3, size=4)

**Fecha:** 2 de Enero, 2026  
**Estado:** ✅ IMPLEMENTADO Y VERIFICADO  
**Objetivo:** Asegurar comparación justa entre GAA y algoritmos estándar

---

## 🎯 Cambio Realizado

### Antes:
```python
# Algoritmos generados con patrones ALEATORIOS
- GAA_Algorithm_1: patrón=simple, depth=2, size=3
- GAA_Algorithm_2: patrón=iterative, depth=4, size=6  
- GAA_Algorithm_3: patrón=multistart, depth=3-4, size=4-8
# ❌ Variabilidad en estructura confunde resultados
```

### Ahora:
```python
# Algoritmos generados con estructura IDÉNTICA
- GAA_Algorithm_1: patrón=iterative-simple, depth=3, size=4
- GAA_Algorithm_2: patrón=iterative-simple, depth=3, size=4
- GAA_Algorithm_3: patrón=iterative-simple, depth=3, size=4
# ✅ Solo varían heurísticas y parámetros
```

---

## 📊 Estructura GAA Fija

### Patrón Seleccionado: `Seq(GreedyConstruct, While(LocalSearch))`

```
Árbol de Sintaxis Abstracta:
─────────────────────────────

    Seq (nivel 0)
    ├─ GreedyConstruct (nivel 1)
    │  └─ {heuristic, alpha}
    └─ While (nivel 1)
       └─ LocalSearch (nivel 2)
          └─ {operator, max_iterations}

Métricas:
- depth = 3 (máxima distancia del nodo raíz)
- size = 4 (total de nodos)
```

### Variabilidad Controlada

**Lo que SÍ varía (seeded random):**
- `GreedyConstruct.heuristic`: 6 opciones (NearestNeighbor, Savings, etc.)
- `GreedyConstruct.alpha`: [0.1, 0.5] con seed determinista
- `LocalSearch.operator`: 8 opciones (TwoOpt, OrOpt, etc.)
- `LocalSearch.max_iterations`: {50, 100, 150, 200}

**Lo que NO varía:**
- Patrones de control de flujo
- Profundidad del árbol (siempre 3)
- Tamaño del árbol (siempre 4)
- Número de operadores en secuencia

---

## 🔧 Cambios en el Código

### Archivo: `gaa/generator.py`

**Método: `generate_three_algorithms()`**

#### Antes (Pseudocódigo):
```python
def generate_three_algorithms(self):
    algorithms = []
    for i in range(3):
        # Generar patrón ALEATORIO
        pattern = random.choice(['simple', 'iterative', 'multistart', 'complex'])
        ast = self.generate_pattern(pattern)  # <-- VARIABLE
        algorithms.append(ast)
    return algorithms
```

#### Después (Pseudocódigo):
```python
def generate_three_algorithms(self):
    algorithms = []
    for i in range(3):
        # PATRÓN FIJO: Seq(GreedyConstruct, While(LocalSearch))
        construction = GreedyConstruct(
            heuristic=random.choice([NearestNeighbor, Savings, ...]),
            alpha=random.uniform(0.1, 0.5)
        )
        
        improvement = LocalSearch(
            operator=random.choice([TwoOpt, OrOpt, ...]),
            max_iterations=random.choice([50, 100, 150, 200])
        )
        
        while_loop = While(condition='iterations < max_iter', body=improvement)
        ast = Seq(body=[construction, while_loop])
        
        algorithms.append(ast)
    return algorithms
```

### Cambios Exactos:

**Línea ~230 en `gaa/generator.py`:**

Reemplazado:
```python
# Generar AST válido
ast = self.generate_with_validation(max_attempts=20)
```

Con:
```python
# Generar AST con estructura fija (depth=3, size=4)
construction = GreedyConstruct(...)
improvement = LocalSearch(...)
while_loop = While(condition='iterations < max_iter', body=improvement)
ast = Seq(body=[construction, while_loop])
```

---

## ✅ Verificación

### Ejecución del Test:

```bash
$ python test_gaa_fair_comparison.py

=== GENERATED ALGORITHMS WITH FAIR COMPARISON ===
Total: 3
Configuration: depth=3, size=4 (FIXED for all)

[1] GAA_Algorithm_1
    Pattern: iterative-simple
    Depth: 3
    Size: 4

[2] GAA_Algorithm_2
    Pattern: iterative-simple
    Depth: 3
    Size: 4

[3] GAA_Algorithm_3
    Pattern: iterative-simple
    Depth: 3
    Size: 4

✓ All algorithms have identical depth and size
✓ Only heuristics and parameters vary
✓ Fair comparison with GRASP/VND/ILS
```

### Ejecución de Experimento:

```
[OK] 3 algoritmos GAA generados
  - GAA_Algorithm_1: patrón=iterative-simple, depth=3, size=4
  - GAA_Algorithm_2: patrón=iterative-simple, depth=3, size=4
  - GAA_Algorithm_3: patrón=iterative-simple, depth=3, size=4
```

---

## 📋 Beneficios

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Profundidad** | 2-5 (variable) | **3 (fija)** |
| **Tamaño** | 3-8 (variable) | **4 (fija)** |
| **Comparación** | Confundida por estructura | **Aislada a heurísticas** |
| **Reproducibilidad** | Parcial | **Total** |
| **Justicia** | ❌ No | **✅ Sí** |

---

## 🚀 Próximas Ejecuciones

Ahora todas las futuras ejecuciones de experimentos usarán:
```bash
python scripts/experiments.py --mode QUICK
# o
python scripts/experiments.py --mode FULL
```

Con **GAA algorithms garantizados depth=3, size=4**

Esto permite una comparación justa entre:
- **GRASP**: metaheurística constructiva estándar
- **VND**: búsqueda local variable neighborhood descent
- **ILS**: búsqueda local con perturbación
- **GAA_1, GAA_2, GAA_3**: algoritmos auto-generados con estructura controlada

---

## 📝 Metadata en Resultados

El CSV ahora incluye en `characteristics`:
```json
"characteristics": {
    "depth": 3,
    "size": 4,
    "note": "Fixed for fair comparison with GRASP/VND/ILS"
}
```

Esto documenta que la estructura fue controlada intencionalmente.

---

## ✨ Conclusión

**Los 3 algoritmos GAA ahora tienen:**
- ✅ Misma profundidad: 3
- ✅ Mismo tamaño: 4
- ✅ Patrón coherente: Seq(Greedy, While(LocalSearch))
- ✅ Variabilidad controlada: solo en heurísticas/parámetros
- ✅ Reproducibilidad: seed determinista

**Esto asegura una comparación COMPLETAMENTE JUSTA con GRASP/VND/ILS** ✨

