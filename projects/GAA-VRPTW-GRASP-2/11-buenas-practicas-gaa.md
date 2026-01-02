# 11️⃣ Buenas Prácticas: Generación de 3 Algoritmos VRPTW

**Basado en:** Implementación KBP-SA (generación automática de algoritmos)  
**Adaptado para:** VRPTW-GRASP (22 operadores, 56 instancias Solomon)  
**Objetivo:** Generar 3 algoritmos automáticamente y ejecutar 3 baterías de pruebas

---

## 📋 Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Los 3 Algoritmos VRPTW](#los-3-algoritmos-vrptw)
3. [Generación Automática (Código)](#generación-automática-código)
4. [Ejecución de Pruebas](#ejecución-de-pruebas)
5. [Registro de Resultados](#registro-de-resultados)
6. [Análisis Estadístico](#análisis-estadístico)
7. [Script Completo: Inicio a Fin](#script-completo-inicio-a-fin)

---

## 🏗️ Arquitectura General

### Estructura de Directorios

```
GAA-VRPTW-GRASP-2/
├── gaa/                              # Módulo GAA
│   ├── __init__.py
│   ├── ast_nodes.py                  # 7 nodos: Seq, While, For, If, etc
│   ├── grammar.py                    # Gramática BNF para VRPTW
│   ├── generator.py                  # AlgorithmGenerator (4 patrones)
│   ├── interpreter.py                # ASTInterpreter (ejecuta AST)
│   └── operators_map.py              # Mapeo: nombre → clase operador
│
├── operators/                        # 22 operadores VRPTW
│   ├── constructive.py               # 6: NearestNeighbor, Savings, Sweep, etc
│   ├── local_search.py               # 8: TwoOpt, OrOpt, ThreeOpt, etc
│   ├── perturbation.py               # 4: EjectionChain, RuinRecreate, etc
│   └── repair.py                     # 3: RepairCapacity, RepairTimeWindows, etc
│
├── evaluation/                       # Evaluación
│   ├── evaluator.py                  # GAEvaluator (evalúa algoritmo en instancias)
│   ├── fitness.py                    # Función fitness (K, D) jerárquica
│   ├── metrics.py                    # QualityMetrics, PerformanceMetrics
│   └── statistics.py                 # Análisis estadístico
│
├── experimentation/                  # Experimentos
│   ├── runner.py                     # ExperimentRunner (orquesta ejecuciones)
│   ├── config.py                     # ExperimentConfig (configuración)
│   ├── smart_algorithm_selector.py   # Generador inteligente de 3 algoritmos
│   └── execution_logger.py           # Registro de ejecuciones
│
├── datasets/                         # 56 instancias Solomon
│   ├── C1/ C2/                       # Familias C: 9+8 instancias
│   ├── R1/ R2/                       # Familias R: 12+11 instancias
│   └── RC1/ RC2/                     # Familias RC: 8+8 instancias
│
├── scripts/
│   ├── 01_generate_algorithms.py     # Genera 3 algoritmos
│   ├── 02_run_quick_tests.py         # Pruebas QUICK (validación)
│   ├── 03_run_full_tests.py          # Pruebas FULL (evaluación exhaustiva)
│   └── run_complete_pipeline.py      # Pipeline completo (inicio a fin)
│
└── output/                           # Resultados
    ├── algorithms/                   # ASTs en JSON
    ├── results/                      # CSVs con resultados
    ├── logs/                         # Archivos de log
    └── plots/                        # Gráficas de análisis
```

---

## 🤖 Los 3 Algoritmos VRPTW

### Patrón 1: **SIMPLE** (Construcción + Mejora Única)

**Estructura:**
```
Secuencia(
  1. Construcción greedy inicial
  2. Búsqueda local iterativa (máx 100 iteraciones)
)
```

**Ejemplo:**
```python
Seq(body=[
    GreedyConstruct(heuristic="NearestNeighbor"),
    LocalSearch(operator="TwoOpt", max_iterations=100)
])
```

**Pseudocódigo:**
```
1. Construir solución inicial con NearestNeighbor
2. Aplicar TwoOpt (máx 100 iteraciones)
   - Mientras hay mejora: intercambiar aristas
3. Retornar mejor solución encontrada
```

**Complejidad:** ⭐ Baja  
**Tiempo esperado:** ~0.5-1.0 segundos por instancia  
**Mejor para:** Instancias pequeñas (n≤100)

---

### Patrón 2: **ITERATIVO** (Construcción + Bucle de Mejora + Perturbación)

**Estructura:**
```
Secuencia(
  1. Construcción greedy
  2. Mientras iteraciones < 200:
     a. Búsqueda local (mejora)
     b. Perturbación (escapar óptimos locales)
)
```

**Ejemplo:**
```python
Seq(body=[
    GreedyConstruct(heuristic="Savings"),
    While(max_iterations=200, body=
        Seq(body=[
            LocalSearch(operator="OrOpt", max_iterations=50),
            Perturbation(operator="EjectionChain", strength=2)
        ])
    )
])
```

**Pseudocódigo:**
```
1. Construir solución inicial con Savings
2. Para i = 1 hasta 200:
   2a. Aplicar OrOpt (máx 50 iteraciones)
   2b. Aplicar EjectionChain para diversificar
   2c. Si nueva solución es mejor: mantener
3. Retornar mejor solución encontrada
```

**Complejidad:** ⭐⭐ Media  
**Tiempo esperado:** ~2-5 segundos por instancia  
**Mejor para:** Instancias medianas (n=100-200)

---

### Patrón 3: **MULTI-START** (Múltiples Construcciones + Búsqueda Local)

**Estructura:**
```
Para N iteraciones:
  1. Construir solución (con diferentes heurísticas)
  2. Aplicar búsqueda local
  3. Mantener mejor global
```

**Ejemplo:**
```python
For(iterations=5, body=
    Seq(body=[
        GreedyConstruct(heuristic="TimeOrientedNN"),
        LocalSearch(operator="ThreeOpt", max_iterations=200)
    ])
)
```

**Pseudocódigo:**
```
1. best_global = ∅
2. Para i = 1 hasta 5:
   2a. Construir solución con TimeOrientedNN
   2b. Aplicar ThreeOpt (máx 200 iteraciones)
   2c. Si solución es mejor que best_global:
       best_global = solución
3. Retornar best_global
```

**Complejidad:** ⭐⭐⭐ Alta  
**Tiempo esperado:** ~5-15 segundos por instancia  
**Mejor para:** Instancias grandes (n>200)

---

## 📝 Generación Automática (Código)

### Paso 1: Generador de Algoritmos

**Archivo:** `gaa/generator.py`

```python
from gaa.grammar import Grammar
from gaa.ast_nodes import Seq, While, For, GreedyConstruct, LocalSearch, Perturbation

class AlgorithmGenerator:
    """Genera algoritmos VRPTW válidos como AST"""
    
    def __init__(self, grammar: Grammar = None, seed: int = None):
        self.grammar = grammar or Grammar()
        self.rng = np.random.Generator(np.random.PCG64(seed))
    
    def generate(self) -> ASTNode:
        """Elige patrón aleatorio y genera"""
        pattern = self.rng.choice([
            'simple', 'iterative', 'multistart', 'complex'
        ])
        
        if pattern == 'simple':
            return self._generate_simple()
        elif pattern == 'iterative':
            return self._generate_iterative()
        elif pattern == 'multistart':
            return self._generate_multistart()
        else:
            return self._generate_complex()
    
    def _generate_simple(self) -> ASTNode:
        """Patrón simple: Construcción + Mejora"""
        construction = GreedyConstruct(
            heuristic=self.rng.choice(CONSTRUCTIVE_OPS)
        )
        improvement = LocalSearch(
            operator=self.rng.choice(LOCAL_SEARCH_OPS),
            max_iterations=self.rng.choice([50, 100, 200])
        )
        return Seq(body=[construction, improvement])
    
    def _generate_iterative(self) -> ASTNode:
        """Patrón iterativo: Construcción + While + Mejora + Perturbación"""
        construction = GreedyConstruct(
            heuristic=self.rng.choice(CONSTRUCTIVE_OPS)
        )
        improvement = LocalSearch(
            operator=self.rng.choice(LOCAL_SEARCH_OPS),
            max_iterations=self.rng.choice([50, 100])
        )
        perturbation = Perturbation(
            operator=self.rng.choice(PERTURBATION_OPS),
            strength=self.rng.choice([1, 2, 3])
        )
        loop_body = Seq(body=[improvement, perturbation])
        loop = While(
            max_iterations=self.rng.choice([100, 200, 300]),
            body=loop_body
        )
        return Seq(body=[construction, loop])
    
    def _generate_multistart(self) -> ASTNode:
        """Patrón multi-start: For + Construcción + Mejora"""
        construction = GreedyConstruct(
            heuristic=self.rng.choice(CONSTRUCTIVE_OPS)
        )
        improvement = LocalSearch(
            operator=self.rng.choice(LOCAL_SEARCH_OPS),
            max_iterations=self.rng.choice([100, 200])
        )
        body = Seq(body=[construction, improvement])
        return For(
            iterations=self.rng.choice([3, 5, 10]),
            body=body
        )
    
    def _generate_complex(self) -> ASTNode:
        """Patrón complejo: Construcción + If(Mejora, Perturbación)"""
        construction = GreedyConstruct(
            heuristic=self.rng.choice(CONSTRUCTIVE_OPS)
        )
        improvement = LocalSearch(
            operator=self.rng.choice(LOCAL_SEARCH_OPS),
            max_iterations=self.rng.choice([100, 200])
        )
        perturbation = Perturbation(
            operator=self.rng.choice(PERTURBATION_OPS),
            strength=self.rng.choice([1, 2, 3])
        )
        conditional = If(
            then_branch=improvement,
            else_branch=perturbation
        )
        return Seq(body=[construction, conditional])
    
    def generate_with_validation(self) -> Optional[ASTNode]:
        """Genera algoritmo con validación de estructura"""
        for attempt in range(10):
            ast = self.generate()
            if self.grammar.validate_ast(ast):
                return ast
        return None
```

### Paso 2: Selector Inteligente de 3 Algoritmos

**Archivo:** `experimentation/smart_algorithm_selector.py`

```python
from typing import List, Tuple

def generate_three_algorithms(
    seed: int = 42,
    verbose: bool = True
) -> List[dict]:
    """
    Genera automáticamente 3 algoritmos diversos
    
    Args:
        seed: Semilla para reproducibilidad (DEFAULT: 42)
        verbose: Mostrar detalles de generación
    
    Returns:
        Lista de 3 dicts con estructura:
        [
            {'name': 'Algorithm_1', 'ast': <AST>, 'pattern': 'simple', ...},
            {'name': 'Algorithm_2', 'ast': <AST>, 'pattern': 'iterative', ...},
            {'name': 'Algorithm_3', 'ast': <AST>, 'pattern': 'multistart', ...}
        ]
    """
    
    grammar = Grammar()
    generator = AlgorithmGenerator(grammar=grammar, seed=seed)
    
    algorithms = []
    patterns_used = set()
    
    if verbose:
        print("\n🧬 GENERACIÓN AUTOMÁTICA DE 3 ALGORITMOS VRPTW")
        print("=" * 70)
    
    for algo_idx in range(3):
        attempt = 0
        max_attempts = 20
        
        while attempt < max_attempts:
            # Generar
            ast = generator.generate_with_validation()
            
            if ast is None:
                attempt += 1
                continue
            
            # Detectar patrón
            pattern = detect_pattern(ast)
            
            # Verificar diversidad (cada algoritmo debe tener patrón diferente)
            if pattern not in patterns_used:
                patterns_used.add(pattern)
                
                # Guardar
                algo_dict = {
                    'name': f'VRPTW_Algorithm_{algo_idx + 1}',
                    'ast': ast,
                    'pattern': pattern,
                    'seed': seed,
                    'pseudocode': ast.to_pseudocode()
                }
                algorithms.append(algo_dict)
                
                if verbose:
                    print(f"\n✅ Algoritmo {algo_idx + 1} generado ({pattern}):")
                    print(f"   Nombre: {algo_dict['name']}")
                    print(f"   Patrón: {pattern.upper()}")
                    print(f"   Pseudocódigo:")
                    for line in ast.to_pseudocode().split('\n'):
                        print(f"      {line}")
                
                break
            
            attempt += 1
        
        if attempt >= max_attempts:
            raise RuntimeError(f"No se pudo generar algoritmo diverso {algo_idx + 1}")
    
    if verbose:
        print("\n" + "=" * 70)
        print(f"✅ GENERACIÓN COMPLETADA: {len(algorithms)}/3 algoritmos")
        print("=" * 70)
        print(f"\n📊 Resumen:")
        for algo in algorithms:
            print(f"   • {algo['name']}: {algo['pattern']}")
    
    return algorithms


def detect_pattern(ast: ASTNode) -> str:
    """Detecta el patrón del algoritmo generado"""
    
    if isinstance(ast, Seq):
        if len(ast.body) == 2:
            if isinstance(ast.body[1], While):
                return 'iterative'
            elif isinstance(ast.body[1], LocalSearch):
                return 'simple'
        elif isinstance(ast.body[1], If):
            return 'complex'
    
    elif isinstance(ast, For):
        return 'multistart'
    
    return 'unknown'
```

---

## 🏃 Ejecución de Pruebas

### Paso 1: Cargar Datasets

**Archivo:** `scripts/01_generate_algorithms.py` (parcial)

```python
from datasets import load_solomon_instances

def load_datasets(family: str = None) -> dict:
    """
    Carga instancias Solomon
    
    Args:
        family: 'C1', 'C2', 'R1', 'R2', 'RC1', 'RC2' o None (todas)
    
    Returns:
        Dict con instancias agrupadas por familia
    """
    
    if family:
        instances = load_solomon_instances([family])
        return {family: instances}
    else:
        # Cargar todas las 56 instancias
        all_instances = {}
        for fam in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
            all_instances[fam] = load_solomon_instances([fam])
        return all_instances

# Ejemplo de uso
datasets = load_datasets()
print(f"✅ {sum(len(v) for v in datasets.values())} instancias cargadas")
# Output: ✅ 56 instancias cargadas
```

### Paso 2: Ejecutar Batería QUICK

**Archivo:** `scripts/02_run_quick_tests.py`

```python
from experimentation import ExperimentRunner, ExperimentConfig
from experimentation.smart_algorithm_selector import generate_three_algorithms

def run_quick_tests():
    """
    Pruebas QUICK: Validación rápida en 1 familia
    
    Configuración:
    • 1 familia (ej: C1)
    • 9 instancias
    • 3 algoritmos
    • 1 repetición por combinación
    • Total: 9 × 3 × 1 = 27 ejecuciones
    • Tiempo estimado: ~2-3 minutos
    """
    
    print("\n" + "=" * 70)
    print("🚀 PRUEBAS QUICK: VALIDACIÓN RÁPIDA")
    print("=" * 70)
    
    # PASO 1: Generar 3 algoritmos
    algorithms = generate_three_algorithms(seed=42, verbose=True)
    
    # PASO 2: Cargar instancias (solo C1 para validación rápida)
    instances = load_solomon_instances(['C1'])
    instance_names = [inst.name for inst in instances]
    
    print(f"\n📁 Instancias QUICK: {len(instances)} (familia C1)")
    
    # PASO 3: Configurar experimento
    config = ExperimentConfig(
        name="VRPTW_QUICK",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=60.0,
        output_dir="output/quick"
    )
    
    print(f"\n⚙️  Configuración:")
    print(f"   • Instancias: {len(config.instances)}")
    print(f"   • Algoritmos: {len(config.algorithms)}")
    print(f"   • Repeticiones: {config.repetitions}")
    print(f"   • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    
    # PASO 4: Ejecutar
    runner = ExperimentRunner(config)
    runner.problems = {inst.name: inst for inst in instances}
    
    print(f"\n🏃 Ejecutando {len(config.instances) * len(config.algorithms)} combinaciones...\n")
    results = runner.run_all(verbose=True)
    
    # PASO 5: Guardar y resumir
    json_file = runner.save_results()
    
    print(f"\n✅ QUICK TESTS COMPLETADAS")
    print(f"💾 Resultados guardados: {json_file}")
    
    return results, json_file


if __name__ == "__main__":
    results, json_file = run_quick_tests()
```

### Paso 3: Ejecutar Batería FULL

**Archivo:** `scripts/03_run_full_tests.py`

```python
def run_full_tests():
    """
    Pruebas FULL: Evaluación exhaustiva en todas las familias
    
    Configuración:
    • 6 familias (C1, C2, R1, R2, RC1, RC2)
    • 56 instancias totales
    • 3 algoritmos
    • 1 repetición por combinación
    • Total: 56 × 3 × 1 = 168 ejecuciones
    • Tiempo estimado: ~40-60 minutos
    """
    
    print("\n" + "=" * 70)
    print("🚀 PRUEBAS FULL: EVALUACIÓN EXHAUSTIVA")
    print("=" * 70)
    
    # PASO 1: Generar 3 algoritmos (mismos del QUICK)
    algorithms = generate_three_algorithms(seed=42, verbose=True)
    
    # PASO 2: Cargar todas las instancias
    all_instances = load_solomon_instances(['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'])
    instance_names = [inst.name for inst in all_instances]
    
    print(f"\n📁 Instancias FULL: {len(all_instances)} (todas las familias)")
    
    # PASO 3: Configurar experimento
    config = ExperimentConfig(
        name="VRPTW_FULL",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=120.0,
        output_dir="output/full"
    )
    
    print(f"\n⚙️  Configuración:")
    print(f"   • Instancias: {len(config.instances)}")
    print(f"   • Algoritmos: {len(config.algorithms)}")
    print(f"   • Repeticiones: {config.repetitions}")
    print(f"   • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    
    # PASO 4: Ejecutar
    runner = ExperimentRunner(config)
    runner.problems = {inst.name: inst for inst in all_instances}
    
    print(f"\n🏃 Ejecutando {len(config.instances) * len(config.algorithms)} combinaciones...\n")
    results = runner.run_all(verbose=True)
    
    # PASO 5: Guardar y resumir
    json_file = runner.save_results()
    
    print(f"\n✅ FULL TESTS COMPLETADAS")
    print(f"💾 Resultados guardados: {json_file}")
    
    return results, json_file


if __name__ == "__main__":
    results, json_file = run_full_tests()
```

---

## 📊 Registro de Resultados

### Estructura JSON de Resultados

**Archivo:** `output/results_VRPTW_FULL_20260101_231500.json`

```json
{
  "metadata": {
    "timestamp": "2026-01-01T23:15:00",
    "mode": "FULL",
    "total_instances": 56,
    "total_algorithms": 3,
    "total_repetitions": 1
  },
  
  "algorithms": [
    {
      "name": "VRPTW_Algorithm_1",
      "pattern": "simple",
      "seed": 42,
      "pseudocode": "...",
      "ast_json": {...}
    },
    {
      "name": "VRPTW_Algorithm_2",
      "pattern": "iterative",
      "seed": 42,
      "pseudocode": "...",
      "ast_json": {...}
    },
    {
      "name": "VRPTW_Algorithm_3",
      "pattern": "multistart",
      "seed": 42,
      "pseudocode": "...",
      "ast_json": {...}
    }
  ],
  
  "results": [
    {
      "instance_name": "C101",
      "algorithm_name": "VRPTW_Algorithm_1",
      "seed": 42,
      "vehicles": 10,
      "distance": 1050.5,
      "fitness": "(10, 1050.5)",
      "gap_to_bks": 5.2,
      "total_time": 0.85,
      "iterations": 150,
      "evaluations": 2500,
      "success": true,
      "feasible": true
    },
    {
      "instance_name": "C101",
      "algorithm_name": "VRPTW_Algorithm_2",
      "seed": 42,
      "vehicles": 10,
      "distance": 1025.3,
      "fitness": "(10, 1025.3)",
      "gap_to_bks": 3.1,
      "total_time": 2.45,
      "iterations": 450,
      "evaluations": 7200,
      "success": true,
      "feasible": true
    },
    ...
    (168 resultados totales)
  ],
  
  "summary": {
    "total_experiments": 168,
    "successful": 168,
    "by_algorithm": {
      "VRPTW_Algorithm_1": {
        "runs": 56,
        "avg_vehicles": 10.3,
        "avg_distance": 1045.2,
        "avg_gap_to_bks": 4.8,
        "std_vehicles": 1.2,
        "std_distance": 120.3,
        "std_gap": 2.1,
        "avg_time": 0.9
      },
      "VRPTW_Algorithm_2": {
        "runs": 56,
        "avg_vehicles": 10.1,
        "avg_distance": 985.5,
        "avg_gap_to_bks": 2.3,
        "std_vehicles": 0.8,
        "std_distance": 95.1,
        "std_gap": 1.5,
        "avg_time": 2.8
      },
      "VRPTW_Algorithm_3": {
        "runs": 56,
        "avg_vehicles": 10.0,
        "avg_distance": 950.2,
        "avg_gap_to_bks": 1.1,
        "std_vehicles": 0.5,
        "std_distance": 78.4,
        "std_gap": 0.9,
        "avg_time": 5.5
      }
    },
    "by_family": {
      "C1": {...},
      "C2": {...},
      "R1": {...},
      "R2": {...},
      "RC1": {...},
      "RC2": {...}
    }
  }
}
```

### CSV de Resultados

**Archivo:** `output/results_VRPTW_FULL_20260101_231500.csv`

```csv
instance_name,algorithm_name,vehicles,distance,fitness,gap_to_bks,total_time,iterations,evaluations,success,feasible
C101,VRPTW_Algorithm_1,10,1050.5,"(10, 1050.5)",5.2,0.85,150,2500,true,true
C101,VRPTW_Algorithm_2,10,1025.3,"(10, 1025.3)",3.1,2.45,450,7200,true,true
C101,VRPTW_Algorithm_3,10,975.2,"(10, 975.2)",1.0,5.12,850,12000,true,true
C102,VRPTW_Algorithm_1,9,980.3,"(9, 980.3)",4.8,0.92,160,2700,true,true
C102,VRPTW_Algorithm_2,9,950.1,"(9, 950.1)",2.1,2.38,440,7100,true,true
C102,VRPTW_Algorithm_3,9,920.5,"(9, 920.5)",0.6,5.08,820,11800,true,true
...
```

---

## 📈 Análisis Estadístico

### Script de Análisis

**Archivo:** `evaluation/statistics.py`

```python
import pandas as pd
import json

def analyze_results(json_file: str) -> dict:
    """
    Análisis estadístico completo de los resultados
    
    Returns:
        Dict con análisis por algoritmo, familia e instancia
    """
    
    with open(json_file) as f:
        data = json.load(f)
    
    results_df = pd.DataFrame(data['results'])
    
    analysis = {
        'by_algorithm': {},
        'by_family': {},
        'rankings': {}
    }
    
    # ANÁLISIS POR ALGORITMO
    for algo_name in results_df['algorithm_name'].unique():
        algo_results = results_df[results_df['algorithm_name'] == algo_name]
        
        analysis['by_algorithm'][algo_name] = {
            'avg_vehicles': algo_results['vehicles'].mean(),
            'std_vehicles': algo_results['vehicles'].std(),
            'avg_gap_to_bks': algo_results['gap_to_bks'].mean(),
            'std_gap': algo_results['gap_to_bks'].std(),
            'avg_time': algo_results['total_time'].mean(),
            'instances_optimized': (algo_results['gap_to_bks'] == 0).sum(),
            'total_runs': len(algo_results)
        }
    
    # ANÁLISIS POR FAMILIA
    for family in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
        family_results = results_df[results_df['instance_name'].str.contains(family)]
        
        analysis['by_family'][family] = {
            'instances': len(family_results['instance_name'].unique()),
            'by_algorithm': {}
        }
        
        for algo in family_results['algorithm_name'].unique():
            algo_fam_results = family_results[family_results['algorithm_name'] == algo]
            analysis['by_family'][family]['by_algorithm'][algo] = {
                'avg_gap': algo_fam_results['gap_to_bks'].mean(),
                'std_gap': algo_fam_results['gap_to_bks'].std()
            }
    
    # RANKING GENERAL
    for algo_name in results_df['algorithm_name'].unique():
        algo_results = results_df[results_df['algorithm_name'] == algo_name]
        analysis['rankings'][algo_name] = algo_results['gap_to_bks'].mean()
    
    # Ordenar por desempeño
    analysis['ranking_sorted'] = sorted(
        analysis['rankings'].items(),
        key=lambda x: x[1]
    )
    
    return analysis


def print_analysis(analysis: dict):
    """Imprime análisis en formato legible"""
    
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS ESTADÍSTICO COMPLETO")
    print("=" * 70)
    
    # Ranking general
    print("\n🏆 RANKING GENERAL (por gap promedio a BKS):")
    print("-" * 70)
    for rank, (algo_name, avg_gap) in enumerate(analysis['ranking_sorted'], 1):
        stats = analysis['by_algorithm'][algo_name]
        print(f"{rank}. {algo_name}")
        print(f"   Gap promedio: {avg_gap:.2f}%")
        print(f"   Vehículos promedio: {stats['avg_vehicles']:.1f}")
        print(f"   Tiempo promedio: {stats['avg_time']:.2f}s")
        print(f"   Instancias optimales: {stats['instances_optimized']}/{stats['total_runs']}")
        print()
```

---

## 🚀 Script Completo: Inicio a Fin

### Pipeline Completo

**Archivo:** `scripts/run_complete_pipeline.py`

```python
#!/usr/bin/env python3
"""
Pipeline completo: Generar 3 algoritmos y ejecutar pruebas QUICK + FULL

Ejecución:
    python scripts/run_complete_pipeline.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Importar módulos
from gaa import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation import ExperimentRunner, ExperimentConfig
from experimentation.smart_algorithm_selector import generate_three_algorithms
from datasets import load_solomon_instances
from evaluation.statistics import analyze_results, print_analysis


def main():
    print("\n" + "=" * 80)
    print("🚀 PIPELINE COMPLETO: VRPTW-GRASP CON 3 ALGORITMOS GENERADOS")
    print("=" * 80)
    
    # PASO 1: GENERAR 3 ALGORITMOS
    print("\n" + "─" * 80)
    print("PASO 1: GENERACIÓN AUTOMÁTICA DE 3 ALGORITMOS")
    print("─" * 80)
    
    algorithms = generate_three_algorithms(seed=42, verbose=True)
    
    print(f"\n✅ {len(algorithms)} algoritmos generados exitosamente")
    
    # Guardar ASTs en JSON
    output_dir = Path("output/algorithms")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for algo in algorithms:
        algo_file = output_dir / f"{algo['name']}.json"
        with open(algo_file, 'w') as f:
            json.dump({
                'name': algo['name'],
                'pattern': algo['pattern'],
                'seed': algo['seed'],
                'pseudocode': algo['pseudocode'],
                'ast': algo['ast'].to_dict()
            }, f, indent=2)
        print(f"   Guardado: {algo_file}")
    
    # PASO 2: EJECUTAR PRUEBAS QUICK
    print("\n" + "─" * 80)
    print("PASO 2: PRUEBAS QUICK (Validación rápida)")
    print("─" * 80)
    
    quick_instances = load_solomon_instances(['C1'])
    quick_instance_names = [inst.name for inst in quick_instances]
    
    quick_config = ExperimentConfig(
        name="VRPTW_QUICK",
        instances=quick_instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=60.0,
        output_dir="output/quick"
    )
    
    quick_runner = ExperimentRunner(quick_config)
    quick_runner.problems = {inst.name: inst for inst in quick_instances}
    
    print(f"\n🏃 Ejecutando {len(quick_config.instances) * len(quick_config.algorithms)} combinaciones...")
    quick_results = quick_runner.run_all(verbose=True)
    
    quick_json = quick_runner.save_results()
    print(f"\n✅ QUICK tests completados")
    print(f"💾 Guardado: {quick_json}")
    
    # PASO 3: EJECUTAR PRUEBAS FULL
    print("\n" + "─" * 80)
    print("PASO 3: PRUEBAS FULL (Evaluación exhaustiva)")
    print("─" * 80)
    
    full_instances = load_solomon_instances(['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'])
    full_instance_names = [inst.name for inst in full_instances]
    
    full_config = ExperimentConfig(
        name="VRPTW_FULL",
        instances=full_instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=120.0,
        output_dir="output/full"
    )
    
    full_runner = ExperimentRunner(full_config)
    full_runner.problems = {inst.name: inst for inst in full_instances}
    
    print(f"\n🏃 Ejecutando {len(full_config.instances) * len(full_config.algorithms)} combinaciones...")
    print(f"   (Esto puede tomar 40-60 minutos)\n")
    full_results = full_runner.run_all(verbose=True)
    
    full_json = full_runner.save_results()
    print(f"\n✅ FULL tests completados")
    print(f"💾 Guardado: {full_json}")
    
    # PASO 4: ANÁLISIS ESTADÍSTICO
    print("\n" + "─" * 80)
    print("PASO 4: ANÁLISIS ESTADÍSTICO")
    print("─" * 80)
    
    analysis = analyze_results(str(full_json))
    print_analysis(analysis)
    
    # PASO 5: RESUMEN FINAL
    print("\n" + "=" * 80)
    print("✅ PIPELINE COMPLETADO")
    print("=" * 80)
    print(f"""
📊 RESUMEN:
   • Algoritmos generados: {len(algorithms)}
   • Pruebas QUICK: {len(quick_results)} ejecuciones
   • Pruebas FULL: {len(full_results)} ejecuciones
   • Total: {len(quick_results) + len(full_results)} ejecuciones

📁 RESULTADOS:
   • Algoritmos: {output_dir}
   • QUICK results: {quick_json}
   • FULL results: {full_json}

🏆 MEJOR ALGORITMO:
   {analysis['ranking_sorted'][0][0]} (gap = {analysis['ranking_sorted'][0][1]:.2f}%)
""")


if __name__ == "__main__":
    main()
```

### Ejecución

```bash
# Ir al directorio del proyecto
cd C:\Users\gustavo_windows\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2

# Ejecutar pipeline completo
python scripts/run_complete_pipeline.py
```

**Salida esperada:**
```
════════════════════════════════════════════════════════════════════════════════
🚀 PIPELINE COMPLETO: VRPTW-GRASP CON 3 ALGORITMOS GENERADOS
════════════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────────────
PASO 1: GENERACIÓN AUTOMÁTICA DE 3 ALGORITMOS
────────────────────────────────────────────────────────────────────────────────

🧬 GENERACIÓN AUTOMÁTICA DE 3 ALGORITMOS VRPTW
======================================================================

✅ Algoritmo 1 generado (simple):
   Nombre: VRPTW_Algorithm_1
   Patrón: SIMPLE
   Pseudocódigo:
      SECUENCIA:
      1. GreedyConstruct('NearestNeighbor')
      2. LocalSearch('TwoOpt', 100 iteraciones)

✅ Algoritmo 2 generado (iterative):
   Nombre: VRPTW_Algorithm_2
   Patrón: ITERATIVE
   Pseudocódigo:
      SECUENCIA:
      1. GreedyConstruct('Savings')
      2. MIENTRAS (iteraciones < 200):
         2a. LocalSearch('OrOpt', 50 iteraciones)
         2b. Perturbation('EjectionChain', strength=2)

✅ Algoritmo 3 generado (multistart):
   Nombre: VRPTW_Algorithm_3
   Patrón: MULTISTART
   Pseudocódigo:
      PARA i = 1 hasta 5:
      1. GreedyConstruct('TimeOrientedNN')
      2. LocalSearch('ThreeOpt', 200 iteraciones)
      
✅ GENERACIÓN COMPLETADA: 3/3 algoritmos

────────────────────────────────────────────────────────────────────────────────
PASO 2: PRUEBAS QUICK (Validación rápida)
────────────────────────────────────────────────────────────────────────────────

🏃 Ejecutando 27 combinaciones...
[1/27] C101 × VRPTW_Algorithm_1 ... ✅ K=10, D=1050.5, gap=5.2%, t=0.85s
[2/27] C101 × VRPTW_Algorithm_2 ... ✅ K=10, D=1025.3, gap=3.1%, t=2.45s
...
[27/27] C109 × VRPTW_Algorithm_3 ... ✅ K=11, D=920.1, gap=1.8%, t=5.32s

✅ QUICK tests completados
💾 Guardado: output/quick/experiment_VRPTW_QUICK_20260101_231530.json

────────────────────────────────────────────────────────────────────────────────
PASO 3: PRUEBAS FULL (Evaluación exhaustiva)
────────────────────────────────────────────────────────────────────────────────

🏃 Ejecutando 168 combinaciones...
   (Esto puede tomar 40-60 minutos)

[1/168] C101 × VRPTW_Algorithm_1 ... ✅
[2/168] C101 × VRPTW_Algorithm_2 ... ✅
...
[168/168] RC208 × VRPTW_Algorithm_3 ... ✅

✅ FULL tests completados
💾 Guardado: output/full/experiment_VRPTW_FULL_20260101_234530.json

────────────────────────────────────────────────────────────────────────────────
PASO 4: ANÁLISIS ESTADÍSTICO
────────────────────────────────────────────────────────────────────────────────

======================================================================
📊 ANÁLISIS ESTADÍSTICO COMPLETO
======================================================================

🏆 RANKING GENERAL (por gap promedio a BKS):
──────────────────────────────────────────────────────────────────

1. VRPTW_Algorithm_3
   Gap promedio: 1.12%
   Vehículos promedio: 10.05
   Tiempo promedio: 5.45s
   Instancias optimales: 8/56

2. VRPTW_Algorithm_2
   Gap promedio: 2.34%
   Vehículos promedio: 10.18
   Tiempo promedio: 2.82s
   Instancias optimales: 3/56

3. VRPTW_Algorithm_1
   Gap promedio: 4.78%
   Vehículos promedio: 10.32
   Tiempo promedio: 0.92s
   Instancias optimales: 1/56

════════════════════════════════════════════════════════════════════════════════
✅ PIPELINE COMPLETADO
════════════════════════════════════════════════════════════════════════════════

📊 RESUMEN:
   • Algoritmos generados: 3
   • Pruebas QUICK: 27 ejecuciones
   • Pruebas FULL: 168 ejecuciones
   • Total: 195 ejecuciones

📁 RESULTADOS:
   • Algoritmos: output/algorithms
   • QUICK results: output/quick/experiment_VRPTW_QUICK_20260101_231530.json
   • FULL results: output/full/experiment_VRPTW_FULL_20260101_234530.json

🏆 MEJOR ALGORITMO:
   VRPTW_Algorithm_3 (gap = 1.12%)
```

---

## 📌 Checklist de Implementación

- [ ] Crear módulo `gaa/` con generador
- [ ] Implementar 7 tipos de nodos AST
- [ ] Implementar gramática BNF
- [ ] Implementar intérprete de AST
- [ ] Implementar función `generate_three_algorithms()`
- [ ] Crear `ExperimentRunner` y `ExperimentConfig`
- [ ] Implementar carga de datasets Solomon (56 instancias)
- [ ] Crear script `run_complete_pipeline.py`
- [ ] Implementar análisis estadístico
- [ ] Generar visualizaciones (gráficas)
- [ ] Documentar resultados

---

## 🔗 Referencias

- [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md) — Documentación GAA completa
- [03-operadores-dominio.md](03-operadores-dominio.md) — 22 operadores VRPTW
- [06-experimentos-plan.md](06-experimentos-plan.md) — Plan experimental
- [development_checklist.md](development_checklist.md) — Checklist de desarrollo

---

**Última actualización:** 2026-01-01  
**Versión:** 1.0.0  
**Base:** KBP-SA implementation
