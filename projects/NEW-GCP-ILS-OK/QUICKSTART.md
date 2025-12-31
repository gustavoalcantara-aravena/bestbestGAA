# NEW-GCP-ILS-OK - Quick Start Guide

Guía rápida para comenzar con el framework de Graph Coloring con Iterated Local Search.

## Instalación

### Requisitos
- Python 3.8+
- pip (gestor de paquetes)

### Pasos de instalación

1. Clonar o descargar el proyecto:
```bash
cd NEW-GCP-ILS-OK
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Primeros pasos

### Validación rápida (10 segundos)

Verificar que todo está funcionando correctamente:

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

Ver capacidades del framework:

```bash
python scripts/demo_complete.py
```

Esto demuestra:
- Operadores constructivos (DSATUR, Largest First)
- Búsqueda local (One Vertex Move)
- Metaheurística ILS
- Soporte para instancias DIMACS

## Uso básico en Python

### Ejemplo simple: resolver un grafo pequeño

```python
from core.problem import GraphColoringProblem
from metaheuristic.ils_core import IteratedLocalSearch

# Crear problema (grafo con 5 vértices)
vertices = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
problem = GraphColoringProblem(vertices, edges)

# Ejecutar ILS
ils = IteratedLocalSearch(
    problem,
    seed=42,
    max_iterations=100,
    max_no_improve=30,
    verbose=True
)

solution = ils.run()

# Ver resultados
print(f"Colores: {solution.num_colors}")
print(f"Conflictos: {solution.num_conflicts}")
print(f"Factible: {solution.is_feasible()}")
```

### Ejemplo: cargar instancia DIMACS

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

print(f"Mejor solución: {solution.num_colors} colores")
```

### Ejemplo: comparar diferentes operadores

```python
from core.problem import GraphColoringProblem
from operators.constructive import GreedyDSATUR, GreedyLargestFirst, RandomSequential

problem = GraphColoringProblem(10, [(i, (i+1)%10) for i in range(10)])

# Probar diferentes constructivos
operators = [
    ("DSATUR", GreedyDSATUR()),
    ("Largest First", GreedyLargestFirst()),
    ("Random Sequential", RandomSequential()),
]

for name, op in operators:
    solution = op.construct(problem, seed=42)
    print(f"{name}: {solution.num_colors} colores")
```

## Estructura del proyecto

```
NEW-GCP-ILS-OK/
├── core/                    # Modulo CORE (problema, solucion, evaluador)
│   ├── problem.py
│   ├── solution.py
│   └── evaluation.py
├── operators/               # Modulo OPERATORS
│   ├── constructive.py      # DSATUR, Largest First, Random Sequential
│   ├── improvement.py       # One Vertex Move, Kempe Chain, Tabu
│   ├── perturbation.py      # Random Recolor, Partial Destroy, etc.
│   └── repair.py            # Greedy Repair, Constraint Propagation
├── metaheuristic/           # Modulo METAHEURISTIC
│   ├── ils_core.py          # ILS principal
│   └── schedules.py         # Estrategias de perturbación
├── tests/                   # FASE 4: Tests
│   ├── test_core.py
│   ├── test_operators.py
│   └── test_ils.py
├── scripts/                 # FASE 5: Scripts
│   ├── test_quick.py        # Validación rápida
│   ├── demo_complete.py     # Demo completo
│   └── experiment.py        # Experimentación
├── config/                  # FASE 6: Configuración
│   └── config.yaml          # Archivo de configuración
├── datasets/                # Instancias DIMACS
│   ├── CUL/
│   ├── DSJ/
│   ├── LEI/
│   ├── MYC/
│   ├── REG/
│   ├── SCH/
│   └── SGB/
├── results/                 # Resultados de experimentos
└── requirements.txt         # Dependencias Python
```

## Configuración

Editar `config/config.yaml` para:
- Cambiar parámetros del ILS
- Ajustar operadores utilizados
- Configurar directorios de entrada/salida
- Cambiar niveles de log

Ejemplo de configuración para búsqueda rápida:
```yaml
metaheuristic:
  max_iterations: 50
  max_no_improve: 20

perturbation:
  strength: 0.2
  use_adaptive: false
```

## Ejecutar tests

Ejecutar todos los tests:
```bash
pytest tests/ -v
```

Tests específicos:
```bash
pytest tests/test_core.py -v
pytest tests/test_operators.py -v
pytest tests/test_ils.py -v
```

## Experimentación

Ejecutar experimento completo (5+ minutos):
```bash
python scripts/experiment.py
```

Los resultados se guardan en `results/experiment_results_*.csv`

## Solución de problemas

### Error: "ModuleNotFoundError: No module named 'core'"

Asegurase de estar en el directorio correcto y de que Python puede encontrar los módulos:
```bash
cd NEW-GCP-ILS-OK
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # En Windows usar set en lugar de export
```

### Error: "datasets not found"

Las instancias DIMACS no están incluidas. Se pueden:
1. Descargar de: http://www.cs.hbg.psu.edu/benchmarks/
2. El framework usará instancias sintéticas automáticamente si no las encuentra

### Problemas de rendimiento

Si la búsqueda es lenta:
1. Reducir `max_iterations` en config.yaml
2. Usar el script `test_quick.py` en lugar de `experiment.py`
3. Aumentar `perturbation_strength` para escapar más rápido de óptimos locales

## Próximos pasos

- [Leer ARCHITECTURE.md para entender el diseño](ARCHITECTURE.md)
- [Ver ejemplos de uso en examples/](examples/)
- [Revisar los tests para más uso](tests/)
- [Configurar según necesidades específicas](config/config.yaml)

## Referencias

- Graph Coloring Problem: Classic NP-hard problem
- ILS (Iterated Local Search): Metaheurística de búsqueda local
- DIMACS: Benchmark estándar para GCP
- Brelaz's DSATUR: Algoritmo clásico de coloreo greedy

## Licencia

MIT License - Ver LICENSE archivo

## Contacto y soporte

Para problemas o preguntas, consulta la documentación en `docs/`
