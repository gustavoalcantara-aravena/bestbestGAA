# VERIFICACIÓN PENDIENTE DE SCRIPTS - GCP-ILS

## Resumen Ejecutivo

Los scripts **existen y parecen estar bien implementados**, pero requieren **verificación práctica** para asegurar que funcionan correctamente de extremo a extremo.

---

## Scripts Identificados

### 1. `scripts/run.py` ✅ (154 líneas)
**Estado**: Implementado, **necesita prueba**

**Características**:
- CLI con argparse completo
- Parámetros configurables: constructive, local_search, perturbation
- Opciones: max-iterations, seed, dataset-root, verbose
- Manejo de errores estructurado
- Output formateado con resultados

**Validaciones pendientes**:
```
✓ ¿Carga correctamente las instancias DIMACS?
✓ ¿Los 5 constructivos (dsatur, lf, sl, rs, rlf) funcionan todos?
✓ ¿Los 4 local search (kempe, tabu, ovm, swap) funcionan todos?
✓ ¿Las 2+ perturbaciones (random_recolor, partial_destroy) funcionan?
✓ ¿Maneja correctamente parámetros inválidos?
✓ ¿Genera output correcto cuando encuentra óptimo conocido?
```

**Ejemplo de comando a validar**:
```bash
python scripts/run.py CUL10
python scripts/run.py DSJ10 --constructive lf --local-search tabu
python scripts/run.py LEI10 --max-iterations 1000 --seed 42 --verbose
```

### 2. `scripts/demo_complete.py` ✅ (208 líneas)
**Estado**: Implementado, **necesita prueba**

**Características**:
- Demo en múltiples instancias
- Muestra disponibilidad de familias
- Ejecuta en 4 instancias de prueba (CUL10, DSJ10, LEI10, REG10)
- Colecta y muestra estadísticas
- Valida factibilidad de soluciones

**Validaciones pendientes**:
```
✓ ¿Se ejecuta sin errores?
✓ ¿Detecta correctamente las familias disponibles?
✓ ¿Carga las 4 instancias de prueba correctamente?
✓ ¿Los resultados son sensatos (k > 0, k finito)?
✓ ¿Se valida factibilidad correctamente?
✓ ¿El output es legible y completo?
```

**Comando a validar**:
```bash
python scripts/demo_complete.py
```

---

## Problemas Específicos a Verificar

### 1. Cargador de Datasets
**Archivo**: `data/loader.py`

**Verificación crítica**:
- ¿Parsea correctamente el formato DIMACS (.col)?
- ¿Lee todas las 45+ instancias?
- ¿Mapea correctamente aristas (1-indexed en DIMACS → 0-indexed en código)?
- ¿Calcula correctamente grado, densidad, lower bound?

**Instancias a probar**:
```
CUL/CUL10.col          (pequeña, verificación básica)
DSJ/DSJ10.col          (pequeña, verificación básica)
MYC/MYC03.col          (myciel, estructura específica)
SGB/SGB001.col         (Johnson grafo, aristas múltiples)
```

### 2. Evaluador
**Archivo**: `core/evaluation.py`

**Verificación crítica**:
- ¿Cuenta conflictos correctamente?
- ¿Identifica soluciones factibles vs infactibles?
- ¿Calcula k (número de colores) correctamente?
- ¿Penaliza correctamente soluciones infactibles?

**Prueba manual**:
```python
# Prueba: coloración con k=1 debe tener muchos conflictos
coloring_invalid = [1] * n  # Todos el mismo color
conflicts = evaluator.count_conflicts(coloring_invalid)
assert conflicts > 0  # Debería haber conflictos

# Prueba: coloración valida debe tener 0 conflictos
coloring_valid = [1, 2, 1, 2]  # Bipartito
conflicts = evaluator.count_conflicts(coloring_valid)
assert conflicts == 0  # No debería haber conflictos
```

### 3. Operadores de Dominio

**Verificación por tipo**:

#### Constructivos
```
✓ GreedyDSATUR: ¿Genera coloración válida cada vez?
✓ GreedyLF (Largest First): ¿Ordena por grado correctamente?
✓ GreedySL (Smallest Last): ¿Elimina en orden inverso correctamente?
✓ RandomSequential: ¿Orden aleatorio + colores válidos?
✓ RLF (Recursive LF): ¿Subconjuntos independientes correctamente?
```

**Test esperado**:
```python
for constructive in ['dsatur', 'lf', 'sl', 'rs', 'rlf']:
    solution = get_constructive(constructive).build(problem)
    conflicts = solution.count_conflicts()
    assert conflicts == 0  # Debe ser factible
    assert solution.num_colors > 0
```

#### Búsqueda Local
```
✓ KempeChain: ¿Intercambia colores validos?
✓ TabuCol: ¿Mantiene memoria tabú correctamente?
✓ OneVertexMove: ¿Mejora soluciones en la mayoría de casos?
✓ SwapColors: ¿Intercambia dos colores sin crear conflictos?
```

#### Perturbación
```
✓ RandomRecolor: ¿Recolorea k% de vértices aleatoriamente?
✓ PartialDestroy: ¿Destruye y reconstruye subgrafo?
✓ ColorClassMerge: ¿Fusiona clases y repara?
```

### 4. Metaheurística ILS
**Archivo**: `metaheuristic/ils_core.py`

**Verificación crítica**:
- ¿Ejecuta todas las iteraciones?
- ¿Mejora solución inicial en la mayoría de casos?
- ¿Converge a óptimo en instancias pequeñas?
- ¿Respeta max_iterations y restart_threshold?

**Test específico**:
```python
ils = IteratedLocalSearch(problem, max_iterations=10)
solution, stats = ils.run()
assert stats['iterations_completed'] == 10  # Debe ejecutar todas
assert stats['best_k'] > 0
assert stats['best_k'] <= problem.n  # k no puede ser > n
```

---

## Matriz de Verificación Necesaria

| Componente | Script | Test Requerido | Tipo | Prioridad |
|---|---|---|---|---|
| **run.py** | Ejecución CLI | Comandos básicos + parámetros | Funcional | ALTA |
| **demo_complete.py** | Demostración | Ejecutar sin errores | Funcional | ALTA |
| **DataLoader** | Parseo DIMACS | Cargar 45+ instancias | Unitario | ALTA |
| **ColoringEvaluator** | Evaluación | Contar conflictos | Unitario | ALTA |
| **Constructivos** | 5 operadores | build() genera factible | Unitario | ALTA |
| **Local Search** | 4 operadores | Mejora o mantiene | Unitario | MEDIA |
| **Perturbación** | 2+ operadores | Diversifica solución | Unitario | MEDIA |
| **ILS** | Metaheurística | Ejecuta iteraciones | Integración | ALTA |
| **QUICKSTART** | Documentación | Pasos funcionan de extremo a extremo | Integración | ALTA |

---

## Pruebas Específicas a Realizar

### Test 1: Carga de Dataset (CRÍTICO)
```bash
# Verificar que CUL10 se carga correctamente
python scripts/run.py CUL10 --verbose

# Verificación esperada:
# - "Instance loaded: n=?, m=?"
# - "Lower bound: ?"
# - "Result: k = ?"
```

### Test 2: Todos los Constructivos
```bash
for c in dsatur lf sl rs rlf; do
    python scripts/run.py CUL10 --constructive $c
    # Cada uno debe generar solución factible
done
```

### Test 3: Todos los Local Search
```bash
for ls in kempe tabu ovm swap; do
    python scripts/run.py CUL10 --local-search $ls
    # Cada uno debe mejorar o mantener
done
```

### Test 4: Demo Completa
```bash
python scripts/demo_complete.py

# Debe mostrar:
# - Lista de familias disponibles
# - Instancias probadas con resultados
# - Tabla resumen
```

### Test 5: QUICKSTART de Extremo a Extremo
```bash
# Seguir exactamente lo que dice QUICKSTART.md
cd projects/GCP-ILS
python scripts/run.py CUL10

# Debe funcionar sin errores
```

---

## Problemas Potenciales a Investigar

### 1. **Indexing de vértices**
⚠️ **Posible problema**: DIMACS usa 1-indexed, código usa 0-indexed
- **Verificar**: ¿Los vecinos se cargan correctamente?
- **Test**: Comparar adjlist en memory vs archivo

### 2. **Parámetros de operadores**
⚠️ **Posible problema**: Operadores pueden tener parámetros duros codificados
- **Verificar**: ¿`perturbation_strength` se usa realmente?
- **Test**: Variar strength y ver si afecta resultados

### 3. **Factibilidad de soluciones**
⚠️ **Posible problema**: Operadores pueden generar soluciones infactibles
- **Verificar**: ¿Todos los operadores retornan soluciones factibles?
- **Test**: `assert best_solution.is_feasible()`

### 4. **Reproducibilidad**
⚠️ **Posible problema**: Con `--seed` ¿se obtienen mismos resultados?
- **Verificar**: ¿Las semillas se usan correctamente?
- **Test**: Ejecutar 2x con mismo seed, comparar resultados

---

## Checklist de Verificación Propuesto

```
ANTES DE DECLARAR 100% CUMPLIMIENTO:

□ Test 1: run.py CUL10 funciona sin errores
□ Test 2: Todos los 5 constructivos funcionan
□ Test 3: Todos los 4 local search funcionan
□ Test 4: demo_complete.py muestra resultados sensatos
□ Test 5: QUICKSTART.md instrucciones funcionan de extremo a extremo
□ Test 6: Instancia con óptimo conocido → gap calculado correctamente
□ Test 7: --seed 42 reproducible (mismos resultados)
□ Test 8: --verbose muestra debug info útil
□ Test 9: Soluciones siempre factibles (0 conflictos)
□ Test 10: ILS itera correctamente (--max-iterations 10 → 10 iteraciones)
```

---

## Tiempo Estimado de Verificación

| Test | Tiempo |
|---|---|
| Ejecutar run.py básico | 2 min |
| Probar 5 constructivos | 5 min |
| Probar 4 local search | 5 min |
| Ejecutar demo completa | 5 min |
| Verificar QUICKSTART | 5 min |
| Análisis de resultados | 5 min |
| **TOTAL** | **~25-30 min** |

---

## Conclusión

**Los scripts están bien estructurados pero requieren validación práctica** para asegurar que:

1. ✅ Todas las funcionalidades funcionan sin errores
2. ✅ El parseo DIMACS es correcto (índices, aristas, etc.)
3. ✅ Todos los operadores generan soluciones válidas
4. ✅ ILS converge correctamente
5. ✅ QUICKSTART.md es funcional de extremo a extremo

**Recomendación**: Ejecutar los 5 tests principales (~25 minutos) para alcanzar 100% de confianza en los scripts.

---

**Documento creado**: 30 de Diciembre, 2025  
**Propósito**: Detalle de verificaciones pendientes en GCP-ILS
