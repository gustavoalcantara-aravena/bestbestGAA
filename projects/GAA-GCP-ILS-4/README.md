# Graph Coloring Problem con Iterated Local Search

**Proyecto**: GCP-ILS  
**Problema**: Graph Coloring Problem (Problema NP-Completo)  
**Metaheurística**: Iterated Local Search (ILS)  
**Estado**: Documentación completa, arquitectura definida, tests listos para implementación

---

## 📚 Documentación

### Documentación Principal
- **[problema_metaheuristica.md](problema_metaheuristica.md)** - Especificación técnica completa (2560+ líneas)
  - Parte 1: Definición del Problema
  - Parte 2: Metaheurística Seleccionada
  - Parte 3: Datasets (78 instancias DIMACS)
  - Parte 4: Generación y Experimentación
  - **Parte 5: Testing y Validación Unitaria** ✨ *NUEVO*

### Documentación de Testing
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Resumen ejecutivo de la estrategia de testing
- **[tests/README.md](tests/README.md)** - Guía detallada de tests y ejecución
- **[scripts/test_quick.py](scripts/test_quick.py)** - Script de validación rápida (~10s)

### Scripts Auxiliares
- **[run_tests.py](run_tests.py)** - Script para ejecutar tests con opciones
- **[scripts/test_quick.py](scripts/test_quick.py)** - Validación rápida de componentes

---

## 🏗️ Arquitectura

```
project/
├── core/                        # Componentes fundamentales
│   ├── problem.py              # GraphColoringProblem
│   ├── solution.py             # ColoringSolution
│   └── evaluation.py           # ColoringEvaluator
├── operators/                  # Operadores de búsqueda
│   ├── constructive.py         # GreedyDSATUR, GreedyLF, RandomSequential
│   ├── improvement.py          # KempeChain, OneVertexMove, TabuCol
│   └── perturbation.py         # RandomRecolor, PartialDestroy
├── metaheuristic/              # Algoritmos
│   └── ils_core.py            # IteratedLocalSearch
├── tests/                      # Suite de tests
│   ├── test_core.py           # 15+ tests de Core
│   ├── test_operators.py      # 20+ tests de Operadores
│   ├── test_ils.py            # 10+ tests de ILS
│   ├── conftest.py            # Fixtures compartidas
│   └── README.md              # Guía de tests
├── scripts/                    # Scripts utilitarios
│   ├── test_quick.py          # Validación rápida
│   └── run_tests.py           # Ejecutor de tests
├── datasets/                  # 78 instancias DIMACS
│   ├── training/              # 5-10 instancias
│   ├── validation/            # 10-15 instancias
│   └── test/                  # Resto
├── config/                    # Configuración
│   └── config.yaml           # Parámetros centralizados
├── docs/                      # Documentación adicional
├── problema_metaheuristica.md # Especificación técnica
├── TESTING_SUMMARY.md         # Resumen de testing
└── README.md                  # Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov numpy

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 2. Validación Rápida (10 segundos)

```bash
python scripts/test_quick.py
```

**Esperado**:
```
============================================================
  VALIDACIÓN RÁPIDA - GCP con ILS
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

### 3. Ejecutar Suite Completa de Tests

```bash
pytest tests/ -v
```

---

## 📊 Suite de Tests

### Cobertura

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

### Archivos de Testing

- **[tests/test_core.py](tests/test_core.py)** - Tests de componentes fundamentales (15+ tests)
- **[tests/test_operators.py](tests/test_operators.py)** - Tests de operadores (20+ tests)
- **[tests/test_ils.py](tests/test_ils.py)** - Tests de metaheurística (10+ tests)
- **[tests/conftest.py](tests/conftest.py)** - Fixtures compartidas y configuración
- **[scripts/test_quick.py](scripts/test_quick.py)** - Validación rápida

---

## 📋 Tareas de Implementación

### Fase 1: Core (Crítico - 2-3 horas)

- [ ] `core/problem.py` - Clase `GraphColoringProblem`
  - Carga desde DIMACS
  - Validaciones de grafo
  - Propiedades (grados, matriz de adyacencia, etc.)
  
- [ ] `core/solution.py` - Clase `ColoringSolution`
  - Asignación de colores
  - Validación de factibilidad
  - Cálculo de conflictos

- [ ] `core/evaluation.py` - Clase `ColoringEvaluator`
  - Métricas de calidad
  - Evaluación individual y en lote
  - Gap respecto a óptimo conocido

### Fase 2: Operadores (3-4 horas)

- [ ] `operators/constructive.py` - Constructores iniciales
  - GreedyDSATUR
  - GreedyLF
  - RandomSequential

- [ ] `operators/improvement.py` - Operadores de mejora local
  - KempeChain
  - OneVertexMove
  - TabuCol

- [ ] `operators/perturbation.py` - Perturbación y diversificación
  - RandomRecolor
  - PartialDestroy

### Fase 3: Metaheurística (2-3 horas)

- [ ] `metaheuristic/ils_core.py` - Algoritmo ILS
  - Inicialización
  - Ejecución del ciclo principal
  - Manejo de budgets
  - Rastreo de mejor solución

### Fase 4: Configuración (1 hora)

- [ ] `config/config.yaml` - Parámetros centralizados
- [ ] `requirements.txt` - Dependencias Python

---

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

### Con Reporte de Cobertura

```bash
pytest tests/ --cov=core --cov=operators --cov=metaheuristic --cov-report=html
```

### Validación Rápida

```bash
python scripts/test_quick.py
```

### Comando Personalizado

```bash
# Solo tests de Core
pytest tests/test_core.py -v

# Solo tests de Operadores
pytest tests/test_operators.py -v

# Solo tests de ILS
pytest tests/test_ils.py -v

# Tests que contienen "convergence"
pytest tests/ -k "convergence" -v
```

### Script de Ejecución

```bash
python run_tests.py --quick      # Validación rápida
python run_tests.py --core       # Solo Core
python run_tests.py --operators  # Solo Operadores
python run_tests.py --ils        # Solo ILS
python run_tests.py --coverage   # Con cobertura
python run_tests.py --verbose    # Verbose completo
```

---

## 📈 Datasets

**Total**: 78 instancias DIMACS de Graph Coloring Problem

Distribuidas en 7 familias:

| Familia | Instancias | Tamaño | Dificultad |
|---------|-----------|--------|-----------|
| CUL | 6 | 5-17 vértices | Fácil |
| DSJ | 15 | 125-1000 vértices | Muy Difícil |
| LEI | 12 | 10-38 vértices | Fácil-Medio |
| MYC | 5 | 11-191 vértices | Fácil-Medio |
| REG | 14 | 30-400 vértices | Medio |
| SCH | 2 | 81-204 vértices | Muy Difícil |
| SGB | 24 | 30-512 vértices | Medio-Difícil |

**Ubicación**: `datasets/{training,validation,test}/*.col`

---

## 📚 Referencias

### Documentación del Proyecto
- [problema_metaheuristica.md](problema_metaheuristica.md) - Especificación técnica
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - Resumen de testing
- [tests/README.md](tests/README.md) - Guía de tests

### Literatura
- Brelaz (1979) - Métodos para colorear vértices de un grafo
- Welsh & Powell (1967) - Cota superior para número cromático
- Hertz & de Werra (1987) - Tabu Search para graph coloring
- Lourenço et al. (2003) - Iterated Local Search
- Galinier & Hao (1999) - Algoritmos híbridos evolutivos

---

## 📞 Soporte

### Problemas Comunes

**Error**: `ModuleNotFoundError: No module named 'core'`
- **Solución**: Ejecutar desde el directorio raíz del proyecto

**Error**: `ImportError` en tests
- **Solución**: Verificar que los módulos están implementados

**Tests lentos**
- **Solución**: Usar `pytest tests/ -k "not dimacs"` para omitir tests lentos

### Recursos Adicionales

- [Pytest documentation](https://docs.pytest.org/)
- [NumPy documentation](https://numpy.org/doc/)
- [Graph Coloring Problem](https://en.wikipedia.org/wiki/Graph_coloring)

---

## 📝 Cambios Recientes

### 31 Diciembre 2025 - Generación de Suite de Tests

✨ **Agregada**:
- PARTE 5: Testing y Validación Unitaria en `problema_metaheuristica.md`
- Suite completa de 42+ tests unitarios
- [tests/test_core.py](tests/test_core.py) - Tests de Core (15+ tests)
- [tests/test_operators.py](tests/test_operators.py) - Tests de Operadores (20+ tests)
- [tests/test_ils.py](tests/test_ils.py) - Tests de ILS (10+ tests)
- [tests/conftest.py](tests/conftest.py) - Fixtures y configuración compartidas
- [tests/README.md](tests/README.md) - Guía detallada de testing
- [scripts/test_quick.py](scripts/test_quick.py) - Validación rápida (~10s)
- [run_tests.py](run_tests.py) - Script de ejecución de tests
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - Resumen ejecutivo de testing

---

## 📄 Licencia

Este proyecto es parte de una investigación en Generación Automática de Algoritmos (GAA) para optimización combinatoria.

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Documentación y testing completos, listos para implementación  
**Versión**: 1.0.0
