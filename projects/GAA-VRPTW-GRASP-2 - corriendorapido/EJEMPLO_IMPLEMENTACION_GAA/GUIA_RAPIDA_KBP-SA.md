# Guía Rápida: Cómo Ejecutar KBP-SA con 3 Algoritmos Generados

## 🚀 Inicio Rápido

### Opción 1: Script Listo para Ejecutar (RECOMENDADO)
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\KBP-SA

# Ejecutar demo optimizada con 3 algoritmos generados automáticamente
python scripts/demo_experimentation_both_OPTIMIZED.py
```

**Qué hace:**
1. Genera 3 algoritmos automáticamente con `AlgorithmGenerator`
2. Prueba cada uno en 10 instancias low-dimensional
3. Prueba cada uno en 21 instancias large-scale
4. Guarda resultados en JSON
5. Realiza análisis estadístico y genera gráficas

**Tiempo esperado:** ~40 segundos (versión optimizada)

---

## 📋 Código Ejemplo: Generar y Ejecutar 3 Algoritmos

### Versión Minimalista (15 líneas)
```python
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.runner import ExperimentRunner, ExperimentConfig
from data.loader import DatasetLoader

# 1. GENERAR 3 ALGORITMOS
grammar = Grammar(min_depth=2, max_depth=3)
generator = AlgorithmGenerator(grammar=grammar, seed=123)

algorithms = []
for i in range(3):
    ast = generator.generate_with_validation()
    if ast:
        algorithms.append({
            'name': f'Algo_{i+1}',
            'ast': ast,
            'pseudocode': ast.to_pseudocode()
        })

print(f"✅ {len(algorithms)} algoritmos generados")

# 2. CARGAR INSTANCIAS
loader = DatasetLoader("./datasets")
instances = loader.load_folder("low_dimensional")
instance_names = [inst.name for inst in instances]

print(f"📁 {len(instances)} instancias cargadas")

# 3. CONFIGURAR Y EJECUTAR
config = ExperimentConfig(
    name="quick_test",
    instances=instance_names,
    algorithms=algorithms,
    repetitions=1,
    max_time_seconds=5.0
)

runner = ExperimentRunner(config)
runner.problems = {inst.name: inst for inst in instances}
results = runner.run_all(verbose=True)

# 4. GUARDAR RESULTADOS
json_file = runner.save_results()

# 5. ESTADÍSTICAS
print("\n📊 Resultados por algoritmo:")
for alg in algorithms:
    alg_results = [r for r in results if r.algorithm_name == alg['name'] and r.success]
    gaps = [r.gap_to_optimal for r in alg_results if r.gap_to_optimal]
    avg_gap = sum(gaps) / len(gaps) if gaps else 0
    print(f"  {alg['name']}: gap promedio = {avg_gap:.2f}%")

print(f"\n💾 Resultados guardados en: {json_file}")
```

---

## 📊 Estructura de Resultados JSON

```json
{
  "config": {
    "name": "quick_test",
    "instances": ["instance_f1", "instance_f2", ...],
    "algorithms": [
      {"name": "Algo_1", "ast": {...}},
      {"name": "Algo_2", "ast": {...}},
      {"name": "Algo_3", "ast": {...}}
    ],
    "repetitions": 1,
    "max_time_seconds": 5.0
  },
  "results": [
    {
      "instance_name": "instance_f1",
      "algorithm_name": "Algo_1",
      "best_value": 255,
      "gap_to_optimal": 3.2,
      "total_time": 0.0068,
      "iterations": 12,
      "evaluations": 245,
      "success": true
    },
    ...
  ],
  "summary": {
    "total_experiments": 30,
    "successful": 30,
    "by_algorithm": {
      "Algo_1": {
        "runs": 10,
        "avg_gap": 2.85,
        "std_gap": 1.23,
        "avg_time": 0.0072
      },
      "Algo_2": {
        "runs": 10,
        "avg_gap": 1.92,
        "std_gap": 0.87,
        "avg_time": 0.0245
      },
      "Algo_3": {
        "runs": 10,
        "avg_gap": 1.54,
        "std_gap": 0.65,
        "avg_time": 0.0602
      }
    }
  }
}
```

---

## 🔬 Estructura de los 3 Algoritmos Generados

### Algoritmo Generado Automáticamente 1

```
Tipo: Simple (Construcción + Mejora)

AST:
Seq([
  GreedyConstruct('GreedyByRatio'),
  LocalSearch('FlipBestItem', 'Improving')
])

Pseudocódigo:
1. SECUENCIA:
   1. GreedyConstruct('GreedyByRatio')
      - Ordenar ítems por ratio valor/peso
      - Añadir ítems en orden decreciente hasta llenar
   2. LocalSearch('FlipBestItem', 'Improving')
      - Mientras hay mejora: flip el ítem que más mejora
```

### Algoritmo Generado Automáticamente 2

```
Tipo: Iterativo (Construcción + Bucle)

AST:
Seq([
  GreedyConstruct('GreedyByValue'),
  While(
    IterBudget(500),
    Seq([
      LocalSearch('TwoExchange', 'FirstImprovement'),
      Perturbation('RandomFlip')
    ])
  )
])

Pseudocode:
1. SECUENCIA:
   1. GreedyConstruct('GreedyByValue')
      - Ordenar ítems por valor máximo
      - Añadir ítems hasta llenar
   2. While (iteraciones < 500):
      2a. LocalSearch('TwoExchange', 'FirstImprovement')
          - Intercambiar 2 ítems si mejora (primer caso)
      2b. Perturbation('RandomFlip')
          - Flip un ítem aleatorio
```

### Algoritmo Generado Automáticamente 3

```
Tipo: Multi-start (Múltiples búsquedas locales)

AST:
For(
  5,
  Seq([
    GreedyConstruct('RandomConstruct'),
    LocalSearch('OneExchange', 'FirstImprovement')
  ])
)

Pseudocode:
1. For (i = 1; i <= 5; i++):
   1a. GreedyConstruct('RandomConstruct')
       - Construir solución aleatoria
   1b. LocalSearch('OneExchange', 'FirstImprovement')
       - Hacer 1-exchange si mejora (primer caso)
       - Mantener mejor solución de los 5 inicios
```

---

## ⚙️ Parámetros Clave

### Generación de Algoritmos
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `num_algorithms` | 3 | Cantidad de algoritmos a generar |
| `seed` | 123 | Semilla para reproducibilidad |
| `min_depth` | 2 | Profundidad mínima del AST |
| `max_depth` | 3 | Profundidad máxima del AST |

### Ejecución de Experimentos
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `instances` | 10 (low-dim) | Número de instancias de prueba |
| `algorithms` | 3 | Algoritmos a probar |
| `repetitions` | 1 | Repeticiones por combinación |
| `max_time_seconds` | 5.0 | Timeout por ejecución |
| `total_executions` | 30 | 10 × 3 × 1 |

### Metaheurística (Simulated Annealing)
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `T0` | 100.0 | Temperatura inicial |
| `alpha` | 0.95 | Factor de enfriamiento |
| `max_evaluations` | 2000 | Máximo de evaluaciones de función |
| `T_min` | 0.01 | Temperatura mínima |

---

## 📁 Archivos Generados

Después de ejecutar `demo_experimentation_both_OPTIMIZED.py`:

```
output/
├── plots_low_dimensional_{TIMESTAMP}/
│   ├── README.md
│   ├── demo_boxplot.png              # Comparación de 3 algoritmos
│   ├── demo_bars.png                 # Gap promedio por algoritmo
│   ├── demo_scatter.png              # Tiempo vs calidad
│   ├── best_algorithm_ast.png        # Árbol del mejor
│   ├── gap_evolution.png             # Evolución gap (SA)
│   ├── acceptance_rate.png           # Tasa de aceptación
│   ├── delta_e_distribution.png      # Distribución ΔE
│   ├── exploration_exploitation_*.png # Balance exploración
│   └── time_tracking.md              # Log de tiempos
│
├── plots_large_scale_{TIMESTAMP}/
│   └── [similar estructura]
│
├── low_dimensional_experiments/
│   └── experiment_*.json             # Resultados JSON
│
├── large_scale_experiments/
│   └── experiment_*.json
│
└── execution_logs/
    └── *.json                         # Logs detallados de ejecución
```

---

## 🔍 Inspeccionar Resultados

### Script para Analizar JSON de Resultados
```python
import json
from pathlib import Path

# Cargar resultados
results_file = Path("output/low_dimensional_experiments/experiment_*.json")
results_files = list(Path("output/low_dimensional_experiments").glob("*.json"))

if results_files:
    with open(results_files[-1], 'r') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("RESUMEN DE EXPERIMENTOS")
    print("=" * 60)
    print(f"\nTotal ejecuciones: {data['summary']['total_experiments']}")
    print(f"Exitosas: {data['summary']['successful']}")
    
    print("\n" + "=" * 60)
    print("RESULTADOS POR ALGORITMO")
    print("=" * 60)
    
    for alg_name, stats in data['summary']['by_algorithm'].items():
        print(f"\n{alg_name}")
        print(f"  Ejecuciones: {stats['runs']}")
        print(f"  Gap promedio: {stats['avg_gap']:.2f}% ± {stats['std_gap']:.2f}%")
        print(f"  Tiempo promedio: {stats['avg_time']:.4f}s ± {stats['std_time']:.4f}s")
    
    print("\n" + "=" * 60)
    print("RANKING (por gap promedio)")
    print("=" * 60)
    
    rankings = []
    for alg_name, stats in data['summary']['by_algorithm'].items():
        rankings.append((alg_name, stats['avg_gap']))
    
    rankings.sort(key=lambda x: x[1])
    for i, (alg_name, gap) in enumerate(rankings, 1):
        print(f"{i}. {alg_name}: {gap:.2f}%")
```

---

## 🧪 Test Rápido (2 minutos)

```python
# test_quick_3_algorithms.py
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from gaa.interpreter import ASTInterpreter
from core.problem import KnapsackProblem
from data.loader import DatasetLoader

# 1. Generar 3 algoritmos
print("🧬 Generando 3 algoritmos...")
grammar = Grammar(min_depth=2, max_depth=3)
generator = AlgorithmGenerator(grammar=grammar, seed=123)

algorithms = []
for i in range(3):
    ast = generator.generate_with_validation()
    if ast:
        algorithms.append(ast)
        print(f"✅ Algoritmo {i+1} generado")

# 2. Cargar una instancia de prueba
print("\n📁 Cargando instancia de prueba...")
loader = DatasetLoader("./datasets")
instances = loader.load_folder("low_dimensional")
test_instance = instances[0]

print(f"   Instancia: {test_instance.name} (n={test_instance.n})")

# 3. Ejecutar cada algoritmo
print("\n🚀 Ejecutando algoritmos...")
for i, ast in enumerate(algorithms, 1):
    interpreter = ASTInterpreter(test_instance, seed=42)
    solution = interpreter.execute(ast)
    report = interpreter.get_execution_report()
    
    print(f"   Algoritmo {i}:")
    print(f"     - Solución: valor={solution.value}, peso={solution.weight}")
    print(f"     - Tiempo: {report.get('time', 0):.4f}s")
    print(f"     - Evaluaciones: {report.get('evaluations', 0)}")
```

---

## 📈 Interpretación de Resultados

### Ejemplo de Salida
```
========================================
RANKING (por gap promedio)
========================================

1. Algo_3: 1.54%    ← MEJOR (gap más bajo)
2. Algo_2: 1.92%
3. Algo_1: 2.85%    ← PEOR (gap más alto)
```

**Interpretación:**
- **Algo_3** es el mejor: en promedio, está 1.54% lejos del óptimo
- **Algo_1** es el peor: en promedio, está 2.85% lejos del óptimo
- La diferencia es de 1.31 puntos porcentuales

### Ejemplo de Gráfica Boxplot
```
                  Algo_1    Algo_2    Algo_3
              ┌────┐      ┌────┐      ┌────┐
    Gap (%)   │    │      │    │      │    │
        5.0%  │ ×  │      │    │      │    │
        3.5%  ├────┤      │    │      │    │
        2.0%  │████│      ├────┤      │    │
        1.5%  │████│      │ ×× │      ├────┤
        1.0%  │    │      │████│      │████│
        0.5%  │    │      │ ×  │      │ ×  │
              └────┘      └────┘      └────┘
```

**Lectura:**
- **Altura de la caja** = rango intercuartil (50% de datos)
- **Línea en la caja** = mediana
- **× = Outliers**
- **Algo_3** tiene la caja más baja → mejor desempeño
- **Algo_1** tiene la caja más alta → peor desempeño

---

## 🐛 Troubleshooting

### Error: "No se encuentran instancias"
```
❌ Error: No hay datasets disponibles
   Por favor, coloca archivos .txt en datasets/training/
```
**Solución:** Usar las instancias incluidas:
```bash
# Verificar que existen
ls datasets/low_dimensional/*.txt
ls datasets/large_scale/*.txt
```

### Error: Timeout en ejecución
```
❌ Error: Excedido timeout de 5.0s
```
**Solución:** Aumentar timeout en config:
```python
config = ExperimentConfig(
    ...
    max_time_seconds=10.0  # Aumentar de 5.0 a 10.0
)
```

### Error: Graphviz no disponible (para visualizar AST)
```
⚠️ Graphviz no disponible. Instalar con: apt-get install graphviz
```
**Solución Windows:**
```powershell
choco install graphviz
```

---

## 📚 Referencia de Métodos

### AlgorithmGenerator
```python
generator = AlgorithmGenerator(grammar, seed=123)

ast = generator.generate()                    # Genera algoritmo aleatorio
ast = generator.generate_with_validation()   # Genera y valida
pseudocode = ast.to_pseudocode()             # Convierte a pseudocódigo legible
```

### ExperimentRunner
```python
runner = ExperimentRunner(config)

results = runner.run_all(verbose=True)       # Ejecuta todos los experimentos
json_file = runner.save_results()            # Guarda en JSON
df = runner.get_results_dataframe()          # Convierte a pandas DataFrame
```

### ASTInterpreter
```python
interpreter = ASTInterpreter(problem, seed=42)

solution = interpreter.execute(ast)          # Ejecuta AST en instancia
report = interpreter.get_execution_report()  # Obtiene stats de ejecución
```

---

## ✅ Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Datasets presentes en `datasets/low_dimensional/` y `datasets/large_scale/`
- [ ] Directorio `output/` existe (se crea automáticamente)
- [ ] Matplotlib puede usar backend 'Agg' (para Windows sin GUI)
- [ ] Ejecución sin errores en paso 1 (generación de algoritmos)
- [ ] Ejecución sin timeouts en paso 3 (experimentos)
- [ ] Resultados JSON generados correctamente
- [ ] Al menos una gráfica generada en `output/plots_*/`

---

## 🔗 Archivos Relacionados

| Ruta | Descripción | Líneas |
|------|-------------|--------|
| `gaa/generator.py` | AlgorithmGenerator | 282 |
| `gaa/grammar.py` | Gramática y validación | 324 |
| `gaa/ast_nodes.py` | Definición de nodos AST | 393 |
| `gaa/interpreter.py` | Intérprete de AST | ~200 |
| `experimentation/runner.py` | ExperimentRunner | 372 |
| `scripts/demo_experimentation_both_OPTIMIZED.py` | Demo completa | 804 |
| `config/config.yaml` | Configuración global | 162 |

---

**Versión:** 1.0  
**Última actualización:** Enero 2026
