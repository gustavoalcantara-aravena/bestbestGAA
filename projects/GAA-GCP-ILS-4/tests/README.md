# Testing - GCP con Iterated Local Search

**Directorio**: `tests/`  
**Suite de tests**: 42+ tests unitarios y de integración  
**Cobertura objetivo**: >90%

---

## 📋 Descripción General

Esta suite de tests valida la correctitud de todos los componentes del proyecto GCP-ILS:

- **Core**: Problema, Solución, Evaluador
- **Operadores**: Constructivos, Mejora, Perturbación
- **Metaheurística**: Iterated Local Search
- **Integración**: Flujos completos end-to-end

---

## 📂 Estructura de Archivos

```
tests/
├── __init__.py              # Inicializador del paquete
├── conftest.py              # Configuración y fixtures compartidas (opcional)
├── test_core.py             # Tests de Core (15+ tests)
├── test_operators.py        # Tests de Operadores (20+ tests)
├── test_ils.py              # Tests de ILS (10+ tests)
└── test_integration.py      # Tests de integración (opcional)

scripts/
├── test_quick.py            # Validación rápida (~10s)
└── run_tests.py             # Script para ejecutar tests con opciones

PROJECT_ROOT/
├── run_tests.py             # Alias para script de tests
└── TESTING_SUMMARY.md       # Documentación completa
```

---

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias

```bash
pip install pytest pytest-cov numpy
```

### 2. Validación Rápida (10 segundos)

```bash
python scripts/test_quick.py
```

**Salida esperada**:
```
============================================================
  VALIDACIÓN RÁPIDA - GCP con ILS
  Verifica funcionamiento básico de componentes
============================================================

[1/5] Imports...
✓ Imports de core exitosos

[2/5] Problema simple...
✓ Problema simple (triángulo) creado correctamente

[3/5] Creación de solución...
✓ Solución válida creada y validada

[4/5] Carga DIMACS...
⊘ Archivo DIMACS no encontrado (opcional)

[5/5] Evaluador...
✓ Evaluador funcionando: 3 colores, 0 conflictos

============================================================
  RESULTADO: 4/5 tests pasados  ✓ EXITOSO
  Tiempo total: 0.15s
============================================================
```

### 3. Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

---

## 📊 Cobertura de Tests

### Por Módulo

| Módulo | Tests | Métodos | Cobertura |
|--------|-------|---------|-----------|
| `core/problem.py` | 10 | 12 | >95% |
| `core/solution.py` | 8 | 8 | >95% |
| `core/evaluation.py` | 4 | 6 | >90% |
| `operators/constructive.py` | 3 | 3 | >90% |
| `operators/improvement.py` | 5 | 3 | >90% |
| `operators/perturbation.py` | 5 | 2 | >90% |
| `metaheuristic/ils_core.py` | 6 | 5 | >85% |
| **TOTAL** | **42+** | **39** | **>90%** |

### Por Tipo

- **Unit Tests**: 19
- **Integration Tests**: 12
- **Validation Tests**: 8
- **Performance Tests**: 3+

---

## 🔍 Guía Detallada de Ejecución

### Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

**Opciones útiles**:
```bash
# Con reporte de cobertura
pytest tests/ --cov=core --cov=operators --cov=metaheuristic --cov-report=html

# Con traceback largo
pytest tests/ -v --tb=long

# Mostrar estadísticas
pytest tests/ -v --durations=10

# Generar reporte en XML
pytest tests/ --junit-xml=report.xml

# Modo watch (ejecutar cuando cambian archivos)
pytest-watch tests/
```

### Ejecutar Tests Específicos

```bash
# Solo tests de una clase
pytest tests/test_core.py::TestGraphColoringProblem -v

# Solo tests que coincidan con patrón
pytest tests/ -k "feasible" -v

# Tests excepto los que coincidan con patrón
pytest tests/ -k "not dimacs" -v

# Solo los primeros 5 tests que fallen
pytest tests/ --maxfail=5 -v

# Salir en el primer fallo
pytest tests/ -x
```

### Uso del Script `run_tests.py`

```bash
# Validación rápida
python run_tests.py --quick

# Solo tests de Core
python run_tests.py --core

# Solo tests de Operadores
python run_tests.py --operators

# Solo tests de ILS
python run_tests.py --ils

# Con reporte de cobertura
python run_tests.py --coverage

# Verbose completo
python run_tests.py --verbose

# Combinaciones
python run_tests.py --core --verbose   # Tests de Core con traceback largo
python run_tests.py --coverage --verbose  # Con cobertura y traceback
```

---

## 📝 Ejemplos de Tests

### Test Simple: Carga de Problema

```python
def test_vertices_count(self, triangle_problem):
    """Validar que el problema registra el número correcto de vértices"""
    assert triangle_problem.n_vertices == 3
```

### Test con Fixture

```python
@pytest.fixture
def triangle_problem(self):
    """Fixture: Problema simple (triángulo)"""
    edges = [(1, 2), (2, 3), (1, 3)]
    return GraphColoringProblem(vertices=3, edges=edges, colors_known=3)

def test_vertices_count(self, triangle_problem):
    assert triangle_problem.n_vertices == 3
```

### Test Parametrizado

```python
@pytest.mark.parametrize("vertices,edges,expected_colors", [
    (3, [(1,2), (2,3), (1,3)], 3),  # Triángulo
    (4, [(1,2), (2,3), (3,4), (4,1)], 2),  # Ciclo par
])
def test_various_graphs(self, vertices, edges, expected_colors):
    problem = GraphColoringProblem(vertices=vertices, edges=edges)
    # ...
```

### Test con Skip

```python
@pytest.mark.skip(reason="Requiere archivo DIMACS")
def test_load_from_dimacs(self):
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    assert problem.n_vertices == 11
```

---

## ✅ Checklist Pre-Testing

Antes de ejecutar los tests, asegurar que:

- [ ] `core/problem.py` está implementado
- [ ] `core/solution.py` está implementado
- [ ] `core/evaluation.py` está implementado
- [ ] `operators/constructive.py` está implementado
- [ ] `operators/improvement.py` está implementado
- [ ] `operators/perturbation.py` está implementado
- [ ] `metaheuristic/ils_core.py` está implementado
- [ ] Dependencias instaladas: `pip install pytest pytest-cov numpy`
- [ ] Permisos de lectura en archivos DIMACS (si aplica)
- [ ] Python 3.7+

---

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'core'`

**Solución**: Ejecutar desde el directorio raíz del proyecto:
```bash
cd projects/GAA-GCP-ILS-4
pytest tests/ -v
```

### Error: `ImportError` en los tests

**Solución**: Verificar que los módulos están implementados:
```bash
ls -la core/
ls -la operators/
ls -la metaheuristic/
```

### Tests lentos

**Solución**: Ejecutar solo tests rápidos:
```bash
pytest tests/ -k "not dimacs" -v
```

### Falta `pytest`

**Solución**: Instalar dependencias:
```bash
pip install pytest pytest-cov
```

---

## 📚 Recursos Adicionales

### Documentación de Pytest
- [Guía oficial](https://docs.pytest.org/)
- [Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Parametrización](https://docs.pytest.org/en/stable/how-to-parametrize.html)
- [Markers](https://docs.pytest.org/en/stable/how-to-mark.html)

### En este proyecto
- `problema_metaheuristica.md` - Especificación completa
- `TESTING_SUMMARY.md` - Resumen de testing
- `scripts/test_quick.py` - Validación rápida
- `scripts/run_tests.py` - Script de ejecución

---

## 🎯 Objetivos de Testing

1. **Correctitud**: Validar que componentes funcionan según especificación
2. **Robustez**: Detectar casos edge y manejar errores
3. **Reproducibilidad**: Permitir experimentos reproducibles con seeds
4. **Documentación**: Tests sirven como ejemplos de uso
5. **Regresión**: Prevenir cambios no deseados
6. **Confianza**: Permitir refactoring seguro

---

## 📞 Contacto y Reportes

Para reportar problemas con los tests:

1. Ejecutar con verbose: `pytest tests/ -v --tb=long`
2. Copiar el traceback completo
3. Verificar que las dependencias están instaladas
4. Verificar que los módulos están implementados

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: Documentación completa, tests listos para implementación  
**Cobertura objetivo**: >90%
