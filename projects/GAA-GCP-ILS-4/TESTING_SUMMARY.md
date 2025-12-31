# Generación de Suite de Tests Unitarios - GCP con ILS

**Fecha**: 31 de Diciembre, 2025  
**Proyecto**: Graph Coloring Problem con Iterated Local Search  
**Cambios**: Agregación de estructura completa de tests unitarios

---

## 📋 Resumen de Cambios

Se ha agregado una **PARTE 5: TESTING Y VALIDACION UNITARIA** al documento `problema_metaheuristica.md` con una estrategia exhaustiva de testing que incluye:

### 1. **Documento Principal Actualizado**
- Archivo: `problema_metaheuristica.md`
- Sección nueva: **PARTE 5** (línea ~909)
- Contenido: 300+ líneas de estrategia, especificaciones y código de tests

### 2. **Archivos de Test Creados**

#### A. Script de Validación Rápida
- **Archivo**: `scripts/test_quick.py`
- **Propósito**: Validación rápida en ~10 segundos
- **Tests**:
  - ✓ Imports de módulos core
  - ✓ Creación de problema simple
  - ✓ Creación de solución
  - ✓ Carga de archivos DIMACS
  - ✓ Evaluación de métricas
- **Ejecución**: `python scripts/test_quick.py`

#### B. Tests de Core
- **Archivo**: `tests/test_core.py`
- **Cobertura**: 15+ tests
- **Clases testeadas**:
  - `GraphColoringProblem`: Carga, validación, propiedades (10 tests)
  - `ColoringSolution`: Asignación, factibilidad, conflictos (7 tests)
  - `ColoringEvaluator`: Métricas, evaluación (4 tests)
- **Ejecución**: `pytest tests/test_core.py -v`

#### C. Tests de Operadores
- **Archivo**: `tests/test_operators.py`
- **Cobertura**: 20+ tests
- **Operadores testeados**:
  - **Constructivos** (3 tests): GreedyDSATUR, GreedyLF, RandomSequential
  - **Mejora** (5 tests): KempeChain, OneVertexMove, TabuCol
  - **Perturbación** (5 tests): RandomRecolor, PartialDestroy
  - **Composición** (2 tests): Pipeline de operadores
- **Ejecución**: `pytest tests/test_operators.py -v`

#### D. Tests de Metaheurística ILS
- **Archivo**: `tests/test_ils.py`
- **Cobertura**: 15+ tests
- **Aspectos testeados**:
  - Inicialización correcta
  - Ejecución y convergencia
  - Rastreo de mejor solución
  - Reproducibilidad con seed
  - Respeto de budgets (iteraciones, tiempo)
  - Calidad de soluciones
  - Integración con componentes
- **Ejecución**: `pytest tests/test_ils.py -v`

---

## 🎯 Cobertura de Tests

### Matriz de Componentes

| Módulo | Métodos | Tests | Cobertura Target |
|--------|---------|-------|------------------|
| `core/problem.py` | 12 | 10 | >95% |
| `core/solution.py` | 8 | 8 | >95% |
| `core/evaluation.py` | 6 | 6 | >90% |
| `operators/constructive.py` | 3 | 3 | >90% |
| `operators/improvement.py` | 3 | 3 | >90% |
| `operators/perturbation.py` | 2 | 3 | >90% |
| `metaheuristic/ils_core.py` | 5 | 6 | >85% |
| **TOTAL** | **39** | **42** | **>90%** |

### Categorías de Tests

#### Unit Tests (19 tests)
- Tests individuales de clases y métodos
- Pruebas de propiedades básicas
- Validaciones de entrada/salida

#### Integration Tests (12 tests)
- Composición de operadores
- Flujos completos (Constructor → Mejora → Perturbación)
- Validación de pipelines

#### Validation Tests (8 tests)
- Correctitud matemática
- Respeto de restricciones
- Cotas superiores/inferiores

#### Performance Tests (3 tests)
- Reproducibilidad con seed
- Respeto de budgets de tiempo/iteraciones
- Escalabilidad

---

## 📝 Estructura de la Documentación

### En `problema_metaheuristica.md`

```
# PARTE 5: TESTING Y VALIDACION UNITARIA
├── 5.1 Estrategia de Testing
├── 5.2 Test Suite: Core (15+ Tests)
│   ├── 5.2.1 Tests para GraphColoringProblem
│   ├── 5.2.2 Tests para ColoringSolution
│   └── 5.2.3 Tests para ColoringEvaluator
├── 5.3 Test Suite: Operadores (20+ Tests)
│   ├── 5.3.1 Operadores Constructivos
│   ├── 5.3.2 Operadores de Mejora
│   └── 5.3.3 Operadores de Perturbación
├── 5.4 Test Suite: Metaheurística ILS (10+ Tests)
├── 5.5 Test Suite: Validación Integral
├── 5.6 Ejecución de Tests
│   ├── 5.6.1 Ejecutar Todos los Tests
│   ├── 5.6.2 Script: test_quick.py
│   └── 5.6.3 Matriz de Cobertura
```

---

## 🔧 Uso de Tests

### Ejecución Rápida (10 segundos)
```bash
python scripts/test_quick.py
```

### Ejecutar Todos los Tests
```bash
pytest tests/ -v
```

### Con Reporte de Cobertura
```bash
pytest tests/ --cov=core --cov=operators --cov=metaheuristic --cov-report=html
```

### Tests Específicos
```bash
# Solo tests de Core
pytest tests/test_core.py -v

# Solo tests de GraphColoringProblem
pytest tests/test_core.py::TestGraphColoringProblem -v

# Tests que contienen "convergence"
pytest tests/test_ils.py -k "convergence" -v
```

### Con Traceback Detallado
```bash
pytest tests/ -v --tb=long
```

---

## 📦 Dependencias Requeridas

Para ejecutar los tests:

```bash
pip install pytest pytest-cov numpy
```

**Versiones recomendadas**:
- `pytest>=7.0`
- `pytest-cov>=4.0`
- `numpy>=1.20`

---

## ✅ Checklist de Implementación

Para que los tests sean funcionales, se requiere implementar:

### Fase 1: Core (Crítico)
- [ ] `core/problem.py` - Clase `GraphColoringProblem`
- [ ] `core/solution.py` - Clase `ColoringSolution`
- [ ] `core/evaluation.py` - Clase `ColoringEvaluator`

### Fase 2: Operadores
- [ ] `operators/constructive.py` - GreedyDSATUR, GreedyLF, RandomSequential
- [ ] `operators/improvement.py` - KempeChain, OneVertexMove, TabuCol
- [ ] `operators/perturbation.py` - RandomRecolor, PartialDestroy

### Fase 3: Metaheurística
- [ ] `metaheuristic/ils_core.py` - Clase `IteratedLocalSearch`

### Fase 4: Configuración
- [ ] `requirements.txt` - Dependencias Python
- [ ] Fixtures de pytest en conftest.py (opcional)

---

## 📚 Referencia Rápida de Tests

### Validar Problema Carga Correctamente
```python
problem = GraphColoringProblem(vertices=3, edges=[(1,2), (2,3), (1,3)])
assert problem.n_vertices == 3
assert problem.n_edges == 3
```

### Validar Solución es Factible
```python
solution = ColoringSolution(assignment={1: 0, 2: 1, 3: 2})
assert solution.is_feasible(problem) == True
assert solution.num_conflicts(problem) == 0
```

### Validar Operador Constructivo
```python
sol = GreedyDSATUR.construct(problem)
assert sol.is_feasible(problem) == True
```

### Validar ILS Converge
```python
ils = IteratedLocalSearch(GreedyDSATUR, KempeChain, RandomRecolor, 100)
best, history = ils.solve(problem)
assert best.is_feasible(problem)
assert all(history[i] >= history[i+1] for i in range(len(history)-1))
```

---

## 🎓 Beneficios de esta Estrategia

1. **Confiabilidad**: 42+ tests garantizan correctitud de componentes
2. **Mantenibilidad**: Tests sirven como especificación ejecutable
3. **Reproducibilidad**: Control de seed permite experimentos reproducibles
4. **Escalabilidad**: Tests parametrizados funcionan con diferentes tamaños
5. **Documentación**: Los tests son ejemplos de uso de la API
6. **Regresión**: Detecta cambios no deseados en futuras modificaciones

---

## 📞 Notas de Implementación

### Fixtures en pytest
Los archivos de test usan fixtures de pytest para reutilizar objetos:
```python
@pytest.fixture
def simple_problem(self):
    edges = [(1, 2), (2, 3), (1, 3)]
    return GraphColoringProblem(vertices=3, edges=edges, colors_known=3)
```

### Parametrización
Para probar múltiples casos:
```python
@pytest.mark.parametrize("ratio", [0.1, 0.3, 0.5, 0.7, 0.9])
def test_random_recolor_with_ratios(self, simple_graph, ratio):
    ...
```

### Skip Condicional
Tests que requieren archivos:
```python
@pytest.mark.skip(reason="Requiere archivo DIMACS")
def test_load_from_dimacs(self):
    ...
```

---

## 🔗 Enlaces Relacionados

- Documentación completa: `problema_metaheuristica.md`
- Especificación de Core: `problema_metaheuristica.md` (Sección: Implementación de Core)
- Especificación de Operadores: `problema_metaheuristica.md` (Sección: Operadores del Dominio)
- Configuración de ILS: `problema_metaheuristica.md` (Sección: PARTE 2 - Metaheurística)

---

**Estado**: ✅ Suite de tests completamente documentada y lista para implementación  
**Próximo paso**: Implementar módulos `core/`, `operators/`, `metaheuristic/` y ejecutar pytest
