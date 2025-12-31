# NEW-GCP-ILS-OK: Graph Coloring with Iterated Local Search

Framework completo para resolver el **Graph Coloring Problem** usando **Iterated Local Search** como metaheurística principal.

## 🎯 Características

✅ **Framework completo de 6 fases**:
- FASE 1: CORE (problema, solución, evaluación)
- FASE 2: OPERATORS (constructivos, mejora, perturbación, reparación)
- FASE 3: METAHEURISTIC (ILS con estrategias adaptativas)
- FASE 4: TESTING (tests unitarios e integración)
- FASE 5: SCRIPTS (validación, demo, experimentación)
- FASE 6: CONFIGURATION (config.yaml, requisitos, documentación)

✅ **Algoritmos implementados**:
- **Constructivos**: DSATUR (Brelaz), Largest First, Random Sequential
- **Mejora local**: One Vertex Move, Kempe Chain, Tabu Coloring
- **Perturbación**: Random Recolor, Partial Destroy, Color Class Merge
- **Reparación**: Greedy, Conflict Minimizing, Constraint Propagation, Backtracking

✅ **Características avanzadas**:
- Perturbación adaptativa
- Estrategias de planificación (lineal, exponencial, cíclica)
- Soporte para benchmark DIMACS con 79 instancias
- Métricas detalladas y comparación con BKS (Best Known Solutions)
- Type hints completos y documentación exhaustiva

✅ **Calidad de código**:
- Python 3.8+
- Type hints en todas las funciones
- Tests unitarios e integración (pytest)
- Docstrings con ejemplos
- Configuración centralizada (YAML)

## 📊 Benchmark DIMACS integrado

```
Dataset: 79 instancias verificadas
├── CUL (Color University of Leeds): 6 instancias
├── DSJ (David S. Johnson): 15 instancias
├── LEI (Leighton): 12 instancias
├── MYC (Mycielski): 6 instancias
├── REG (Regular): 14 instancias
├── SCH (School): 2 instancias
└── SGB (Stanford GraphBase): 24 instancias
```

Con Best Known Solutions (BKS) en `datasets/BKS.json` para comparación.

## 🚀 Quick Start

### Instalación

```bash
# Clonar y entrar al directorio
cd NEW-GCP-ILS-OK

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Validación rápida (10 segundos)

```bash
python scripts/test_quick.py
```

Salida esperada:
```
QUICK VALIDATION - SYNTHETIC INSTANCES
...
VALIDATION COMPLETE
Framework is working correctly!
```

### Demo completo (30 segundos)

```bash
python scripts/demo_complete.py
```

Muestra todos los operadores y la metaheurística en acción.

## 💻 Ejemplo de uso

### Caso simple: Resolver un grafo

```python
from core.problem import GraphColoringProblem
from metaheuristic.ils_core import IteratedLocalSearch

# Crear problema (ciclo de 5 vértices)
problem = GraphColoringProblem(
    vertices=5,
    edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
)

# Ejecutar ILS
ils = IteratedLocalSearch(
    problem,
    seed=42,
    max_iterations=100,
    max_no_improve=30,
    verbose=True
)

solution = ils.run()

# Resultados
print(f"Colores: {solution.num_colors}")
print(f"Conflictos: {solution.num_conflicts}")
print(f"Factible: {solution.is_feasible()}")
```

### Cargar instancia DIMACS

```python
from core.problem import GraphColoringProblem
from metaheuristic.ils_core import IteratedLocalSearch

def load_dimacs(filepath):
    vertices = 0
    edges = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('p'):
                vertices = int(line.split()[2])
            elif line.startswith('e'):
                u, v = int(line.split()[1]) - 1, int(line.split()[2]) - 1
                edges.append((u, v))
    return GraphColoringProblem(vertices, edges)

# Cargar y resolver
problem = load_dimacs("datasets/myciel3.col")
ils = IteratedLocalSearch(problem, seed=42, max_iterations=200)
solution = ils.run()

print(f"Resultado: {solution.num_colors} colores")
```

### Comparar operadores

```python
from core.problem import GraphColoringProblem
from operators.constructive import GreedyDSATUR, GreedyLargestFirst

problem = GraphColoringProblem(10, [(i, (i+1)%10) for i in range(10)])

for name, op in [("DSATUR", GreedyDSATUR()), ("LargestFirst", GreedyLargestFirst())]:
    solution = op.construct(problem, seed=42)
    print(f"{name}: {solution.num_colors} colors")
```

## 📁 Estructura del proyecto

```
NEW-GCP-ILS-OK/
├── core/                    # FASE 1: Núcleo (problema, solución, evaluación)
│   ├── problem.py           # GraphColoringProblem
│   ├── solution.py          # ColoringSolution  
│   ├── evaluation.py        # ColoringEvaluator
│   └── __init__.py
├── operators/               # FASE 2: Operadores
│   ├── constructive.py      # DSATUR, Largest First, Random Sequential
│   ├── improvement.py       # One Vertex Move, Kempe Chain, Tabu
│   ├── perturbation.py      # Random Recolor, Partial Destroy, etc.
│   ├── repair.py            # Greedy Repair, Constraint Propagation, etc.
│   └── __init__.py
├── metaheuristic/           # FASE 3: Metaheurística
│   ├── ils_core.py          # IteratedLocalSearch, HybridILS
│   ├── schedules.py         # Estrategias de perturbación
│   └── __init__.py
├── tests/                   # FASE 4: Tests
│   ├── test_core.py         # Tests del CORE
│   ├── test_operators.py    # Tests de operadores
│   ├── test_ils.py          # Tests de ILS
│   └── __init__.py
├── scripts/                 # FASE 5: Scripts
│   ├── test_quick.py        # Validación rápida
│   ├── demo_complete.py     # Demo completo
│   ├── experiment.py        # Experimentación
│   └── __init__.py
├── config/                  # FASE 6: Configuración
│   └── config.yaml          # Parámetros centralizados
├── datasets/                # Instancias DIMACS
│   ├── CUL/, DSJ/, LEI/, etc.
│   └── BKS.json            # Best Known Solutions
├── results/                 # Resultados de experimentos
├── QUICKSTART.md           # Guía rápida
├── ARCHITECTURE.md         # Documentación de arquitectura
├── README.md               # Este archivo
├── LICENSE                 # MIT License
└── requirements.txt        # Dependencias Python
```

## 🧪 Testing

Ejecutar todos los tests:
```bash
pytest tests/ -v
```

Tests específicos:
```bash
pytest tests/test_core.py::TestGraphColoringProblem -v
pytest tests/test_operators.py::TestConstructive -v
pytest tests/test_ils.py::TestIteratedLocalSearch -v
```

Cobertura:
```bash
pytest tests/ --cov=core --cov=operators --cov=metaheuristic --cov-report=html
```

## 📈 Experimentación

Ejecutar experimento completo (5+ minutos):
```bash
python scripts/experiment.py
```

Genera CSV con resultados en `results/experiment_results_*.csv`

Configuraciones probadas:
- **Fast** (50 iter): Búsqueda rápida para prototipos
- **Balanced** (100 iter): Balance velocidad/calidad
- **Thorough** (200 iter): Búsqueda profunda para benchmark

## ⚙️ Configuración

Editar `config/config.yaml` para personalizar:

```yaml
metaheuristic:
  max_iterations: 500
  max_no_improve: 150

local_search:
  operator: "OneVertexMove"
  max_iterations: 100

perturbation:
  strength: 0.15
  use_adaptive: true

constructive:
  operator: "GreedyDSATUR"
```

## 📊 Rendimiento esperado

| Instancia | Vértices | Tiempo | Resultado |
|-----------|----------|--------|-----------|
| myciel3   | 11       | < 1s   | 4 colores |
| myciel4   | 23       | 2-3s   | 5 colores |
| CUL_100   | 100      | 10-15s | 5-7 colores |
| DSJC125   | 125      | 15-20s | 45-55 colores |
| DSJ500    | 500      | 60-120s| ~180 colores |

## 🎓 Conceptos clave

### Graph Coloring Problem
Asignar colores a vértices de un grafo tal que no hay adyacentes con el mismo color, minimizando el número de colores.

### Iterated Local Search
Metaheurística que alterna entre:
1. Búsqueda local para convergencia
2. Perturbación para escapar óptimos locales
3. Criterio de aceptación (first improvement / best improvement)

### DIMACS Benchmark
Estándar de benchmark para problemas NP-hard, con formato .col e instancias variadas.

## 📚 Referencias

- Lourenço, H. R., Martin, O. C., & Stützle, T. (2019). Iterated Local Search: Framework and applications. Handbook of Metaheuristics
- Brelaz, D. (1979). New methods to color the vertices of a graph. Communications of the ACM
- DIMACS Benchmark: http://www.cs.hbg.psu.edu/benchmarks/
- Lewis, R. (2015). A Guide to Graph Coloring. Springer

## 🤝 Contribución

Contribuciones bienvenidas. Para reportar bugs o sugerir features, crear un issue.

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) archivo

## 🔗 Links útiles

- [Quick Start Guide](QUICKSTART.md) - Guía rápida de inicio
- [Architecture Guide](ARCHITECTURE.md) - Documentación de diseño
- [Test Suite](tests/) - Tests unitarios y de integración
- [DIMACS Benchmark](http://www.cs.hbg.psu.edu/benchmarks/) - Dataset estándar

## ✨ Características futuras

- [ ] Paralelización de runs
- [ ] Warm start con soluciones previas
- [ ] Algoritmos adicionales (Genetic Algorithm, Ant Colony)
- [ ] Visualización de progreso
- [ ] Integración con solucionadores ILP
- [ ] API REST para servidor

## 📞 Contacto

Para preguntas, sugerencias o reportes de bugs:
- Crear un issue en el repositorio
- Revisar la documentación en `docs/`
- Consultar ejemplos en `scripts/`

---

**Última actualización**: Enero 2025  
**Versión**: 1.0.0  
**Estado**: Production Ready ✅
