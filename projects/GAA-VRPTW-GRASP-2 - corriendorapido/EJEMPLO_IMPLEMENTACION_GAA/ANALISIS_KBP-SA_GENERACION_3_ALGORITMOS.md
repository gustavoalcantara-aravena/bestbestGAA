# Análisis Completo: KBP-SA - Generación y Ejecución de 3 Algoritmos

**Proyecto:** KBP-SA (Knapsack Problem con Simulated Annealing)  
**Framework:** GAA (Generación Automática de Algoritmos)  
**Objeto de estudio:** Cómo se generan automáticamente 3 algoritmos y se ejecutan pruebas  
**Fecha:** Enero 2026

---

## 📋 Tabla de Contenidos

1. [Estructura de Directorios](#estructura-de-directorios)
2. [Archivos Clave Identificados](#archivos-clave-identificados)
3. [Flujo Completo: Generar → Ejecutar → Registrar](#flujo-completo)
4. [Parámetros Clave](#parámetros-clave)
5. [Ejemplo Concreto: Los 3 Algoritmos](#ejemplo-concreto)
6. [Estructura de Outputs/Resultados](#estructura-de-outputsresultados)

---

## 📁 Estructura de Directorios

```
KBP-SA/
├── gaa/                           # Sistema de Generación de Algoritmos
│   ├── generator.py              # AlgorithmGenerator: crea AST aleatorios
│   ├── grammar.py                # Gramática BNF y validación
│   ├── ast_nodes.py              # Nodos del árbol sintáctico
│   └── interpreter.py            # Intérprete que ejecuta AST
│
├── experimentation/              # Framework Experimental
│   ├── runner.py                 # ExperimentRunner: orquesta ejecuciones
│   ├── smart_algorithm_selector.py # Genera N algoritmos automáticamente
│   ├── metrics.py                # QualityMetrics, PerformanceMetrics
│   ├── statistics.py             # Análisis estadístico
│   ├── visualization.py          # Generación de gráficas
│   ├── ast_visualization.py      # Visualización de árboles sintácticos
│   ├── execution_logger.py       # Registro de ejecuciones
│   └── time_tracker.py           # Tracking de tiempos
│
├── scripts/                       # Scripts ejecutables
│   ├── run.py                    # Punto de entrada principal
│   ├── demo_experimentation_both.py         # Demo multi-grupo
│   └── demo_experimentation_both_OPTIMIZED.py  # Versión optimizada
│
├── config/                        # Configuración
│   └── config.yaml               # Parámetros del proyecto
│
├── datasets/                      # 31 instancias benchmark
│   ├── low_dimensional/          # 10 instancias pequeñas (n=4-23)
│   └── large_scale/              # 21 instancias grandes (n=100-10000)
│
└── output/                        # Resultados generados
    ├── plots_low_dimensional_*   # Visualizaciones grupo bajo-dimensional
    ├── plots_large_scale_*       # Visualizaciones grupo largo-escala
    └── experiments/              # Datos JSON de ejecuciones
```

---

## 🔍 Archivos Clave Identificados

### 1. Generador de Algoritmos
**Ruta:** `gaa/generator.py`

```python
class AlgorithmGenerator:
    """Generador de algoritmos aleatorios para KBP"""
    
    def __init__(self, 
                 grammar: Optional[Grammar] = None,
                 seed: Optional[int] = None)
    
    def generate(self, max_depth: Optional[int] = None) -> ASTNode:
        """Genera algoritmo aleatorio completo"""
        # Elige entre 4 estructuras:
        # - simple: Construcción + mejora
        # - iterative: Construcción + bucle con mejora
        # - multistart: Múltiples construcciones
        # - complex: Estructura completa con perturbación
```

**Métodos principales:**
- `generate()` → AST raíz
- `generate_with_validation()` → AST validado
- `_generate_simple_algorithm()` → Seq(construcción, mejora)
- `_generate_iterative_algorithm()` → Seq(construcción, While(mejora))
- `_generate_multistart_algorithm()` → For(multi-construcciones)
- `_generate_complex_algorithm()` → Estructura completa

---

### 2. Selector Inteligente de Algoritmos
**Ruta:** `experimentation/smart_algorithm_selector.py`

```python
def generate_diverse_algorithms(
    num_algorithms: int = 3,
    seed: int = 42,
    verbose: bool = True
) -> List[Tuple[str, ASTNode, float, str]]:
    """
    Genera N algoritmos diversos automáticamente
    
    Args:
        num_algorithms: Cantidad a generar (DEFAULT: 3)
        seed: Semilla para reproducibilidad
        verbose: Mostrar detalles
    
    Returns:
        Lista de (nombre, AST, score_complejidad, categoría)
    """
```

**Características:**
- Genera candidatos automáticamente
- Valida estructura y complejidad
- Filtra por complejidad máxima
- Selecciona TOP N más diversos

---

### 3. Ejecutor de Experimentos
**Ruta:** `experimentation/runner.py`

```python
@dataclass
class ExperimentConfig:
    name: str
    instances: List[str]              # Nombres de instancias
    algorithms: List[Dict[str, Any]]  # Algoritmos a probar
    repetitions: int = 30             # Repeticiones por combinación
    seeds: Optional[List[int]] = None # Seeds específicas
    max_time_seconds: float = 300.0   # Timeout por ejecución

class ExperimentRunner:
    """Ejecutor de experimentos en batch"""
    
    def run_all(self, verbose: bool = True) -> List[ExperimentResult]:
        """Ejecuta todos los experimentos configurados"""
        # Total ejecuciones = instancias × algoritmos × repeticiones
```

---

### 4. Script de Demostración Principal
**Ruta:** `scripts/demo_experimentation_both_OPTIMIZED.py`

Este es el script que **demuestra el flujo completo** con generación de 3 algoritmos.

---

## 🔄 Flujo Completo: Generar → Ejecutar → Registrar

### PASO 1: Generar 3 Algoritmos
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:680-700`

```python
# PASO 1: Generar algoritmos (UNA SOLA VEZ)
with global_tracker.track("Paso 1: Generando algoritmos GAA", num_algorithms=3):
    print("🧬 Paso 1: Generando algoritmos GAA...\n")
    
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=123)
    
    algorithms = []
    for i in range(3):  # ← GENERA 3 ALGORITMOS
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'GAA_Algorithm_{i+1}',
                'ast': ast
            })
            
            # Generar pseudocódigo
            pseudocode = ast.to_pseudocode(indent=2)
            print(f"✅ Algoritmo {i+1} generado")
            print(f"   Pseudocódigo:")
            for line in pseudocode.split('\n'):
                print(f"   {line}")
```

**Resultado:** Lista `algorithms` con 3 diccionarios:
```python
[
    {'name': 'GAA_Algorithm_1', 'ast': <AST node>},
    {'name': 'GAA_Algorithm_2', 'ast': <AST node>},
    {'name': 'GAA_Algorithm_3', 'ast': <AST node>}
]
```

---

### PASO 2: Configurar Experimento
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:730-765`

```python
config = ExperimentConfig(
    name=f"{folder_name}_experiment",
    instances=instance_names,          # Lista de nombres de instancias
    algorithms=algorithms,              # Los 3 algoritmos generados
    repetitions=1,                      # Repeticiones por combinación
    max_time_seconds=5.0,              # Timeout por ejecución
    output_dir=f"output/{folder_name}_experiments"
)

print(f"⚙️  Configuración:")
print(f"  • Instancias: {len(config.instances)}")
print(f"  • Algoritmos: {len(config.algorithms)}")  # = 3
print(f"  • Repeticiones: {config.repetitions}")     # = 1
print(f"  • Total ejecuciones: {len(config.instances) × 3 × 1}")
```

**Ejemplo:**
- Instancias low_dimensional: 10
- Algoritmos: 3
- Repeticiones: 1
- **Total ejecuciones: 10 × 3 × 1 = 30**

---

### PASO 3: Ejecutar Experimentos
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:770-790`

```python
runner = ExperimentRunner(config)
runner.problems = {inst.name: inst for inst in all_instances}

results = runner.run_all(verbose=True)
```

**Proceso interno (runner.py:260-310):**

```python
def run_single(self, problem, algorithm, seed, repetition) -> ExperimentResult:
    """Ejecuta una combinación: algoritmo × instancia × seed"""
    
    start_time = time.time()
    
    try:
        # Ejecutar algoritmo GAA
        ast_node = algorithm['ast']
        interpreter = ASTInterpreter(problem, seed=seed)
        best_solution = interpreter.execute(ast_node)
        report = interpreter.get_execution_report()
        
        elapsed_time = time.time() - start_time
        
        # Calcular métricas
        gap = evaluator.gap_to_optimal(best_solution)
        
        return ExperimentResult(
            instance_name=problem.name,
            algorithm_name=algorithm['name'],  # ej: "GAA_Algorithm_1"
            seed=seed,
            repetition=repetition,
            best_value=best_solution.value,
            gap_to_optimal=gap,
            total_time=elapsed_time,
            iterations=report.get('iterations', 0),
            evaluations=report.get('evaluations', 0),
            success=True
        )
```

**Ejemplo de ejecución (10 instancias):**
```
[1/30] instance_f1 × GAA_Algorithm_1 (rep 1) ... ✅ valor=X, gap=Y%, tiempo=T
[2/30] instance_f1 × GAA_Algorithm_2 (rep 1) ... ✅ valor=X, gap=Y%, tiempo=T
[3/30] instance_f1 × GAA_Algorithm_3 (rep 1) ... ✅ valor=X, gap=Y%, tiempo=T
[4/30] instance_f2 × GAA_Algorithm_1 (rep 1) ... ✅ valor=X, gap=Y%, tiempo=T
...
[30/30] instance_f10 × GAA_Algorithm_3 (rep 1) ... ✅ valor=X, gap=Y%, tiempo=T
```

---

### PASO 4: Guardar Resultados
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:795-805`

```python
json_file = runner.save_results()
```

**Proceso (runner.py:330-360):**

```python
def save_results(self, filename: Optional[str] = None) -> Path:
    """Guarda resultados en JSON"""
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{self.config.name}_{timestamp}.json"
    
    filepath = self.output_path / filename
    
    data = {
        'config': {
            'name': '...',
            'instances': [...],
            'algorithms': [...],
            'repetitions': 1,
            'max_time_seconds': 5.0
        },
        'results': [
            {
                'instance_name': 'instance_f1',
                'algorithm_name': 'GAA_Algorithm_1',
                'best_value': X,
                'gap_to_optimal': Y,
                'total_time': T,
                'iterations': N,
                'success': True
            },
            ...
        ],
        'summary': {
            'total_experiments': 30,
            'successful': 30,
            'by_algorithm': {
                'GAA_Algorithm_1': {
                    'runs': 10,
                    'avg_gap': Y1,
                    'avg_time': T1
                },
                'GAA_Algorithm_2': {
                    'runs': 10,
                    'avg_gap': Y2,
                    'avg_time': T2
                },
                'GAA_Algorithm_3': {
                    'runs': 10,
                    'avg_gap': Y3,
                    'avg_time': T3
                }
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath
```

---

### PASO 5: Análisis Estadístico
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:810-850`

```python
analyzer = StatisticalAnalyzer(alpha=0.05)

algorithm_results = {}
for alg in algorithms:
    alg_name = alg['name']
    alg_data = [r for r in results if r.algorithm_name == alg_name and r.success]
    
    if alg_data:
        gaps = [r.gap_to_optimal for r in alg_data]
        algorithm_results[alg_name] = gaps
        
        # Estadísticas descriptivas
        stats = analyzer.descriptive_statistics(gaps)
        print(f"Algoritmo: {alg_name}")
        print(f"  Gap (%): media={stats['mean']:.2f} ± {stats['std']:.2f}")
        print(f"  IC 95%: [{ci[0]:.2f}, {ci[1]:.2f}]")
```

---

### PASO 6: Comparación entre Algoritmos
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:860-900`

```python
if len(algorithm_results) >= 2:
    comparison = analyzer.compare_multiple_algorithms(
        algorithm_results,
        test_type="friedman"
    )
    
    print(f"Test: {comparison['global_test'].test_name}")
    print(f"  p-value: {comparison['global_test'].p_value:.4f}")
    print("Rankings promedio (menor = mejor):")
    for alg, rank in sorted(comparison['average_rankings'].items(), key=lambda x: x[1]):
        print(f"  {rank:.2f}  {alg}")
    print(f"🏆 Mejor algoritmo: {comparison['best_algorithm']}")
```

---

### PASO 7: Visualización
**Líneas:** `demo_experimentation_both_OPTIMIZED.py:910-980`

Se generan múltiples gráficas:
1. **Boxplot** comparativo entre los 3 algoritmos
2. **Barras** con gap promedio por algoritmo
3. **Scatter** tiempo vs calidad
4. **AST visualization** del mejor algoritmo
5. **SA visualization** (gap evolution, acceptance rate, ΔE distribution)

---

## ⚙️ Parámetros Clave

### Configuración Global
**Archivo:** `config/config.yaml`

```yaml
gaa:
  max_depth: 5              # Profundidad máxima del AST
  min_depth: 2              # Profundidad mínima del AST
  population_size: 50       # Tamaño de población (si usa GA)
  n_generations: 100        # Generaciones (si usa GA)
  crossover_rate: 0.8
  mutation_rate: 0.2

metaheuristic:
  parameters:
    T0: 100.0               # Temperatura inicial
    alpha: 0.95             # Factor de enfriamiento
    iterations_per_temp: 100
    T_min: 0.01
    max_evaluations: 10000  # Máximo de evaluaciones de función
```

### Parámetros de Ejecución
**Script:** `demo_experimentation_both_OPTIMIZED.py:673-690`

```python
execution_logger.log_parameters(
    seed=123,                           # Semilla para reproducibilidad
    grammar_min_depth=2,                # Profundidad mínima AST
    grammar_max_depth=3,                # Profundidad máxima AST
    max_time_per_experiment_seconds=5.0,  # Timeout por ejecución
    max_evaluations_sa=2000,            # Evaluaciones (OPTIMIZADO: era 5000)
    repetitions_per_instance=1,         # Repeticiones (en este caso: 1)
    num_algorithms=3,                   # ← CANTIDAD DE ALGORITMOS
    matplotlib_backend='Agg',           # Backend sin GUI
    optimization_version='v2_with_timeout_5s'
)
```

### Parámetros de Instancias
**Configuración:** `datasets/`

**Grupo Low-Dimensional:**
- 10 instancias
- Tamaños: n = 4, 5, 7, 10, 15, 20, 23
- Ejemplos: `instance_f1`, `instance_f2`, ...

**Grupo Large-Scale:**
- 21 instancias
- Tamaños: n = 100, 200, 500, 1000, 2000, 5000, 10000
- Tipos: Pisinger Type 1, 2, 3

---

## 🔬 Ejemplo Concreto: Los 3 Algoritmos

Supongamos que se generan estos 3 algoritmos:

### Algoritmo 1: Simple
```
Estructura: Seq([
    GreedyConstruct("GreedyByRatio"),
    LocalSearch("FlipBestItem", "Improving")
])

Pseudocódigo:
1. Construir solución greedy ordenada por ratio valor/peso
2. Aplicar búsqueda local: flip el mejor ítem si mejora
```

### Algoritmo 2: Iterativo
```
Estructura: Seq([
    GreedyConstruct("GreedyByValue"),
    While(IterBudget(500), Seq([
        LocalSearch("TwoExchange", "Improving"),
        Perturbation("RandomFlip")
    ]))
])

Pseudocódigo:
1. Construir solución greedy por valor máximo
2. Mientras presupuesto < 500 iteraciones:
   2a. Aplicar búsqueda local con 2-exchange
   2b. Perturbar aleatoriamente 1 ítem
```

### Algoritmo 3: Multi-start
```
Estructura: For(5, Seq([
    GreedyConstruct("RandomConstruct"),
    LocalSearch("OneExchange", "FirstImprovement"),
    If(Improves(), Seq([...]), Seq([...]))
]))

Pseudocódigo:
1. Para i = 1 hasta 5:
   1a. Construir solución aleatoria
   1b. Aplicar búsqueda local con 1-exchange
   1c. Si mejora: [hacer X] si no: [hacer Y]
```

### Ejecución en Instancia f1
```
Instancia: f1 (n=10, capacidad=269, 10 ítems)

GAA_Algorithm_1:
  • Construcción: 2.3ms → solución inicial valor=245, peso=269
  • Búsqueda local: 4.5ms → mejora a valor=255
  • Total: 6.8ms, gap=3.2%

GAA_Algorithm_2:
  • Construcción: 1.9ms → solución inicial valor=242
  • Iteración 1: LS + Perturbación: 8.2ms → valor=260
  • Iteración 2: LS + Perturbación: 7.9ms → valor=262
  • Iteración 3-5: sin mejora significativa
  • Total: 25.3ms, gap=1.8%

GAA_Algorithm_3:
  • Start 1: Construcción aleatoria + LS: 12.4ms → valor=250
  • Start 2: Construcción aleatoria + LS: 11.8ms → valor=258
  • Start 3: Construcción aleatoria + LS: 12.1ms → valor=259
  • Start 4: Construcción aleatoria + LS: 11.9ms → valor=260
  • Start 5: Construcción aleatoria + LS: 12.0ms → valor=261
  • Total: 60.2ms, gap=1.5%
```

---

## 📊 Estructura de Outputs/Resultados

### 1. JSON Principal de Resultados
**Ruta:** `output/{folder_name}_experiments/experiment_{name}_{timestamp}.json`

```json
{
  "config": {
    "name": "low_dimensional_experiment",
    "instances": ["instance_f1", "instance_f2", ...],
    "algorithms": [
      {
        "name": "GAA_Algorithm_1",
        "ast": {...}
      },
      {
        "name": "GAA_Algorithm_2",
        "ast": {...}
      },
      {
        "name": "GAA_Algorithm_3",
        "ast": {...}
      }
    ],
    "repetitions": 1,
    "max_time_seconds": 5.0
  },
  
  "results": [
    {
      "instance_name": "instance_f1",
      "algorithm_name": "GAA_Algorithm_1",
      "seed": 42,
      "repetition": 0,
      "best_value": 255,
      "best_weight": 269,
      "is_feasible": true,
      "gap_to_optimal": 3.2,
      "total_time": 0.0068,
      "iterations": 12,
      "evaluations": 245,
      "initial_value": 245,
      "improvement": 10,
      "improvement_ratio": 0.041,
      "timestamp": "2026-01-01T10:30:45.123456",
      "success": true
    },
    {...},
    {...}
  ],
  
  "summary": {
    "total_experiments": 30,
    "successful": 30,
    "by_algorithm": {
      "GAA_Algorithm_1": {
        "runs": 10,
        "avg_gap": 2.85,
        "std_gap": 1.23,
        "avg_time": 0.0072,
        "std_time": 0.0015
      },
      "GAA_Algorithm_2": {
        "runs": 10,
        "avg_gap": 1.92,
        "std_gap": 0.87,
        "avg_time": 0.0245,
        "std_time": 0.0032
      },
      "GAA_Algorithm_3": {
        "runs": 10,
        "avg_gap": 1.54,
        "std_gap": 0.65,
        "avg_time": 0.0602,
        "std_time": 0.0048
      }
    },
    "by_instance": {
      "instance_f1": {
        "runs": 3,
        "avg_gap": 2.10,
        "best_gap": 1.54,
        "worst_gap": 3.20
      },
      {...}
    }
  }
}
```

### 2. Plots Generados
**Ruta:** `output/plots_low_dimensional_{timestamp}/`

```
├── README.md                              # Documentación del experimento
├── demo_boxplot.png                       # Boxplot comparativo (3 algoritmos)
├── demo_bars.png                          # Barras con gap promedio
├── demo_scatter.png                       # Scatter tiempo vs calidad
├── best_algorithm_ast.png                 # Árbol sintáctico del mejor
├── gap_evolution.png                      # Evolución del gap (SA)
├── acceptance_rate.png                    # Tasa de aceptación (SA)
├── delta_e_distribution.png               # Distribución ΔE (SA)
├── exploration_exploitation_inst1.png     # Balance E-E instancia 1
├── exploration_exploitation_inst2.png     # Balance E-E instancia 2
└── time_tracking.md                       # Log de tiempos
```

### 3. Archivo de Tracking de Tiempos
**Ruta:** `output/time_tracker_global/time_tracking_global_{timestamp}.md`

```markdown
# Time Tracking Report

## Ejecución completa de experimentos multi-grupo

### Paso 1: Generando algoritmos GAA
- Start: 2026-01-01 10:30:00
- End: 2026-01-01 10:30:03
- Duration: 3.2s
- num_algorithms: 3

### Paso 2: Configurando experimento
- Start: 2026-01-01 10:30:03
- End: 2026-01-01 10:30:05
- Duration: 2.1s
- instances: 10

### Paso 3: Ejecutando experimentos
- Start: 2026-01-01 10:30:05
- End: 2026-01-01 10:30:35
- Duration: 30.4s
- total_ejecuciones: 30
- successful: 30

### Paso 4: Guardando resultados
- Start: 2026-01-01 10:30:35
- End: 2026-01-01 10:30:36
- Duration: 1.2s
- output_file: output/experiment_low_dimensional_experiment_20260101_103036.json

...más pasos...
```

### 4. Logs de Ejecución
**Ruta:** `output/execution_logs/`

```json
{
  "experiment_name": "Multi-Group_Experimentation_OPTIMIZED",
  "timestamp": "2026-01-01T10:30:00",
  "parameters": {
    "seed": 123,
    "grammar_min_depth": 2,
    "grammar_max_depth": 3,
    "max_time_per_experiment_seconds": 5.0,
    "max_evaluations_sa": 2000,
    "repetitions_per_instance": 1,
    "num_algorithms": 3
  },
  "steps": [
    {
      "name": "Generating GAA Algorithms",
      "timestamp": "2026-01-01T10:30:00",
      "details": {
        "num_algorithms": 3,
        "seed": 123,
        "min_depth": 2,
        "max_depth": 3
      },
      "status": "completed"
    },
    {
      "name": "Processing Low-Dimensional Group",
      "timestamp": "2026-01-01T10:30:03",
      "details": {
        "instances": 10,
        "algorithms": 3,
        "total_runs": 30
      },
      "status": "completed"
    },
    {...}
  ],
  "algorithms": [
    {
      "name": "GAA_Algorithm_1",
      "pseudocode": "...",
      "ast_depth": 3,
      "terminals_used": ["GreedyByRatio", "FlipBestItem"]
    },
    {...}
  ],
  "results": [
    {
      "group": "Low-Dimensional",
      "best_algorithm": "GAA_Algorithm_2",
      "experiments_completed": 30,
      "json_file": "output/experiment_low_dimensional_experiment_20260101_103036.json"
    },
    {...}
  ]
}
```

---

## 📝 Pseudocódigo del Flujo Completo

```pseudocódigo
FUNCIÓN main():
    
    # PASO 1: Generar 3 algoritmos
    grammar ← Grammar(min_depth=2, max_depth=3)
    generator ← AlgorithmGenerator(grammar, seed=123)
    algorithms ← []
    
    PARA i ← 1 HASTA 3:
        ast ← generator.generate_with_validation()
        SI ast ≠ NULL ENTONCES:
            algorithms.add({
                'name': f'GAA_Algorithm_{i}',
                'ast': ast
            })
        FIN SI
    FIN PARA
    
    # PASO 2: Procesar grupos de datasets
    grupos ← ['low_dimensional', 'large_scale']
    
    PARA cada grupo EN grupos:
        # 2a: Cargar instancias del grupo
        instances ← load_dataset(grupo)
        config ← ExperimentConfig(
            instances=instances,
            algorithms=algorithms,
            repetitions=1,
            max_time_seconds=5.0
        )
        
        # 2b: Ejecutar experimentos
        runner ← ExperimentRunner(config)
        results ← []
        
        PARA cada instancia EN instances:
            PARA cada algoritmo EN algorithms:
                PARA rep ← 1 HASTA 1:
                    
                    # Ejecutar algoritmo en instancia con seed
                    interpreter ← ASTInterpreter(instancia, seed)
                    solucion ← interpreter.execute(algoritmo.ast)
                    
                    # Calcular métricas
                    gap ← evaluator.gap_to_optimal(solucion)
                    tiempo ← elapsed_time
                    
                    # Guardar resultado
                    results.add(ExperimentResult(
                        instance_name=instancia.name,
                        algorithm_name=algoritmo.name,
                        best_value=solucion.value,
                        gap_to_optimal=gap,
                        total_time=tiempo
                    ))
                FIN PARA
            FIN PARA
        FIN PARA
        
        # 2c: Guardar resultados en JSON
        json_file ← save_results(results, grupo)
        
        # 2d: Análisis estadístico
        PARA cada algoritmo EN algorithms:
            gaps ← [r.gap PARA r EN results SI r.algorithm = algoritmo]
            stats ← descriptive_statistics(gaps)
            print(f"{algoritmo}: media={stats.mean} ± {stats.std}")
        FIN PARA
        
        # 2e: Test comparación (Friedman)
        comparison ← compare_algorithms(results, test='friedman')
        mejor_algoritmo ← comparison.best_algorithm
        
        # 2f: Generar visualizaciones
        generate_plots(results, mejor_algoritmo, grupo)
    FIN PARA
    
FIN FUNCIÓN
```

---

## 🎯 Resumen Ejecutivo

| Aspecto | Valor |
|--------|-------|
| **Cantidad de algoritmos generados** | 3 |
| **Método de generación** | AlgorithmGenerator + Grammar |
| **Validación** | Mediante grammar.validate() |
| **Representación** | AST (Árbol Sintáctico Abstracto) |
| **Instancias de prueba (low-dim)** | 10 |
| **Instancias de prueba (large-scale)** | 21 |
| **Repeticiones por combinación** | 1 |
| **Total ejecuciones (low-dim)** | 10 × 3 × 1 = 30 |
| **Total ejecuciones (large-scale)** | 21 × 3 × 1 = 63 |
| **Timeout por ejecución** | 5.0 segundos |
| **Máximo de evaluaciones (SA)** | 2000 (optimizado de 5000) |
| **Seeds para reproducibilidad** | seed=123 para generación, seed=42+ para ejecuciones |
| **Formato de salida resultados** | JSON con config, resultados individuales, resumen |
| **Visualizaciones generadas** | Boxplot, barras, scatter, AST, SA analysis |
| **Test estadístico** | Friedman (si n ≥ 2 algoritmos) |
| **Lenguaje de especificación** | Pseudocódigo en texto (to_pseudocode()) |

---

## 🔗 Referencias Cruzadas

- **AlgorithmGenerator:** `gaa/generator.py` (282 líneas)
- **Grammar:** `gaa/grammar.py` (324 líneas)
- **ASTNodes:** `gaa/ast_nodes.py` (393 líneas)
- **ExperimentRunner:** `experimentation/runner.py` (372 líneas)
- **SmartAlgorithmSelector:** `experimentation/smart_algorithm_selector.py` (272 líneas)
- **Demo Script:** `scripts/demo_experimentation_both_OPTIMIZED.py` (804 líneas)
- **Configuración:** `config/config.yaml` (162 líneas)
- **README:** `README.md` (488 líneas)

**Total de código analizado:** ~2,600+ líneas de Python + configuración YAML

---

**Fecha de análisis:** Enero 2026  
**Versión del proyecto:** KBP-SA v1.0.0
