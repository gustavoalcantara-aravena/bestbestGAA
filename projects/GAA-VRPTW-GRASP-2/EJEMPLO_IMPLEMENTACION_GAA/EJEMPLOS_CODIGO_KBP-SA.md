# Ejemplos de Código: Generación y Ejecución de 3 Algoritmos en KBP-SA

## 📝 Tabla de Contenidos
1. [Ejemplo 1: Generador Simple](#ejemplo-1-generador-simple)
2. [Ejemplo 2: Generación Completa con Ejecución](#ejemplo-2-generación-completa-con-ejecución)
3. [Ejemplo 3: Con Análisis Estadístico](#ejemplo-3-con-análisis-estadístico)
4. [Ejemplo 4: Personalizado con Parámetros](#ejemplo-4-personalizado-con-parámetros)
5. [Ejemplo 5: Inspección Detallada de Algoritmos](#ejemplo-5-inspección-detallada-de-algoritmos)

---

## Ejemplo 1: Generador Simple

**Archivo:** `test_simple_generation.py`

```python
#!/usr/bin/env python3
"""
Ejemplo simple: Generar 3 algoritmos y mostrar su estructura
"""

import sys
from pathlib import Path

# Añadir ruta del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar


def main():
    print("=" * 70)
    print("  EJEMPLO 1: Generador Simple")
    print("=" * 70)
    print()
    
    # Crear gramática
    print("1️⃣  Creando gramática...")
    grammar = Grammar(min_depth=2, max_depth=3)
    print(f"   ✓ Profundidad: [{grammar.min_depth}, {grammar.max_depth}]")
    print(f"   ✓ Terminales disponibles: {len(grammar.ALL_TERMINALS)}")
    print(f"     - Constructivos: {grammar.CONSTRUCTIVE_TERMINALS}")
    print(f"     - Mejora: {grammar.IMPROVEMENT_TERMINALS}")
    print(f"     - Perturbación: {grammar.PERTURBATION_TERMINALS}")
    print()
    
    # Generar 3 algoritmos
    print("2️⃣  Generando 3 algoritmos...")
    generator = AlgorithmGenerator(grammar=grammar, seed=123)
    
    algorithms = []
    for i in range(3):
        print(f"\n   Algoritmo {i+1}:")
        ast = generator.generate_with_validation()
        
        if ast:
            algorithms.append(ast)
            
            # Mostrar estructura
            print(f"   ✓ Generado exitosamente")
            print(f"   ✓ Tipo de raíz: {type(ast).__name__}")
            print(f"   ✓ Representación JSON:")
            
            ast_dict = ast.to_dict()
            print(f"     {ast_dict}")
        else:
            print(f"   ✗ Error al generar (falló validación)")
    
    # Mostrar pseudocódigo
    print("\n" + "=" * 70)
    print("  PSEUDOCÓDIGO DE LOS 3 ALGORITMOS")
    print("=" * 70)
    
    for i, ast in enumerate(algorithms, 1):
        print(f"\n🔹 Algoritmo {i}:")
        pseudocode = ast.to_pseudocode(indent=1)
        print(pseudocode)
    
    print("\n" + "=" * 70)
    print(f"✅ Proceso completado: {len(algorithms)}/3 algoritmos generados")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

**Ejecución:**
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\KBP-SA
python test_simple_generation.py
```

**Salida esperada:**
```
======================================================================
  EJEMPLO 1: Generador Simple
======================================================================

1️⃣  Creando gramática...
   ✓ Profundidad: [2, 3]
   ✓ Terminales disponibles: 13
     - Constructivos: {'GreedyByValue', 'GreedyByWeight', 'GreedyByRatio', 'RandomConstruct'}
     - Mejora: {'FlipBestItem', 'FlipWorstItem', 'OneExchange', 'TwoExchange'}
     - Perturbación: {'RandomFlip', 'ShakeByRemoval', 'DestroyRepair'}

2️⃣  Generando 3 algoritmos...

   Algoritmo 1:
   ✓ Generado exitosamente
   ✓ Tipo de raíz: Seq
   ✓ Representación JSON:
     {'type': 'Seq', 'body': [{'type': 'GreedyConstruct', ...}, ...]}

   Algoritmo 2:
   ✓ Generado exitosamente
   ...

   Algoritmo 3:
   ✓ Generado exitosamente
   ...

======================================================================
  PSEUDOCÓDIGO DE LOS 3 ALGORITMOS
======================================================================

🔹 Algoritmo 1:
  SECUENCIA:
    1. GreedyConstruct('GreedyByRatio')
       Construir solución greedy ordenada por ratio
    2. LocalSearch('FlipBestItem', 'Improving')
       Aplicar búsqueda local: flip el mejor ítem

🔹 Algoritmo 2:
  SECUENCIA:
    1. GreedyConstruct('GreedyByValue')
       ...
    2. While(IterBudget(500))
       ...

🔹 Algoritmo 3:
  For (5)
    ...

======================================================================
✅ Proceso completado: 3/3 algoritmos generados
======================================================================
```

---

## Ejemplo 2: Generación Completa con Ejecución

**Archivo:** `test_complete_workflow.py`

```python
#!/usr/bin/env python3
"""
Ejemplo completo: Generar 3 algoritmos, ejecutarlos en instancias y guardar resultados
"""

import sys
import json
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.runner import ExperimentRunner, ExperimentConfig
from data.loader import DatasetLoader


def main():
    print("=" * 80)
    print("  EJEMPLO 2: Flujo Completo - Generar → Ejecutar → Guardar")
    print("=" * 80)
    print()
    
    # =========== PASO 1: GENERAR 3 ALGORITMOS ===========
    print("📝 PASO 1: Generando 3 algoritmos automáticamente...")
    print("-" * 80)
    
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=123)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algo_dict = {
                'name': f'AutoAlgorithm_{i+1}',
                'ast': ast,
                'pseudocode': ast.to_pseudocode()
            }
            algorithms.append(algo_dict)
            print(f"✅ Algoritmo {i+1} creado: {algo_dict['name']}")
    
    print(f"\n✓ Total generados: {len(algorithms)}/3")
    print()
    
    # =========== PASO 2: CARGAR INSTANCIAS ===========
    print("📝 PASO 2: Cargando instancias de prueba...")
    print("-" * 80)
    
    datasets_dir = Path(__file__).parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    
    # Cargar grupo low-dimensional
    instances = loader.load_folder("low_dimensional")
    instance_names = [inst.name for inst in instances]
    
    print(f"✅ Instancias cargadas: {len(instances)}")
    print(f"   Grupo: low-dimensional")
    print(f"   Instancias: {', '.join(instance_names[:3])}...")
    print()
    
    # =========== PASO 3: CONFIGURAR EXPERIMENTO ===========
    print("📝 PASO 3: Configurando experimento...")
    print("-" * 80)
    
    config = ExperimentConfig(
        name="complete_workflow_demo",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=5.0,
        output_dir="output/demo_results"
    )
    
    print(f"✓ Configuración:")
    print(f"  • Instancias: {len(config.instances)}")
    print(f"  • Algoritmos: {len(config.algorithms)}")
    print(f"  • Repeticiones: {config.repetitions}")
    print(f"  • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    print(f"  • Timeout: {config.max_time_seconds}s por ejecución")
    print()
    
    # =========== PASO 4: EJECUTAR EXPERIMENTOS ===========
    print("📝 PASO 4: Ejecutando experimentos...")
    print("-" * 80)
    
    runner = ExperimentRunner(config)
    runner.problems = {inst.name: inst for inst in instances}
    
    results = runner.run_all(verbose=True)
    
    print()
    successful = sum(1 for r in results if r.success)
    print(f"✓ Ejecuciones completadas: {successful}/{len(results)}")
    print()
    
    # =========== PASO 5: GUARDAR RESULTADOS ===========
    print("📝 PASO 5: Guardando resultados en JSON...")
    print("-" * 80)
    
    json_file = runner.save_results()
    print(f"✓ Archivo guardado: {json_file}")
    print()
    
    # =========== PASO 6: RESUMEN ESTADÍSTICO ===========
    print("📝 PASO 6: Análisis estadístico rápido...")
    print("-" * 80)
    
    # Cargar y mostrar resumen
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print("\n🏆 Ranking de Algoritmos (por gap promedio):\n")
    
    rankings = []
    for alg_name, stats in data['summary']['by_algorithm'].items():
        avg_gap = stats['avg_gap']
        rankings.append((alg_name, avg_gap, stats['avg_time']))
    
    rankings.sort(key=lambda x: x[1])
    
    for rank, (alg_name, avg_gap, avg_time) in enumerate(rankings, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        print(f"{medal} {rank}. {alg_name}")
        print(f"      Gap promedio: {avg_gap:.2f}%")
        print(f"      Tiempo promedio: {avg_time:.4f}s")
        print()
    
    print("=" * 80)
    print(f"✅ Ejemplo completado exitosamente")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

**Ejecución:**
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\KBP-SA
python test_complete_workflow.py
```

---

## Ejemplo 3: Con Análisis Estadístico

**Archivo:** `test_with_statistics.py`

```python
#!/usr/bin/env python3
"""
Ejemplo con análisis estadístico completo
"""

import sys
import json
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.runner import ExperimentRunner, ExperimentConfig
from experimentation.statistics import StatisticalAnalyzer
from data.loader import DatasetLoader
import numpy as np


def main():
    print("=" * 80)
    print("  EJEMPLO 3: Generación + Ejecución + Análisis Estadístico")
    print("=" * 80)
    print()
    
    # PASO 1: Generar
    print("1️⃣  Generando 3 algoritmos...")
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=123)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'Algo_{i+1}',
                'ast': ast
            })
    
    print(f"   ✓ {len(algorithms)} algoritmos generados\n")
    
    # PASO 2: Cargar instancias
    print("2️⃣  Cargando instancias...")
    datasets_dir = Path(__file__).parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    instances = loader.load_folder("low_dimensional")
    instance_names = [inst.name for inst in instances]
    print(f"   ✓ {len(instances)} instancias cargadas\n")
    
    # PASO 3: Ejecutar
    print("3️⃣  Ejecutando experimentos...")
    config = ExperimentConfig(
        name="stats_demo",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=5.0,
        output_dir="output/stats_demo"
    )
    
    runner = ExperimentRunner(config)
    runner.problems = {inst.name: inst for inst in instances}
    results = runner.run_all(verbose=False)  # Sin output verbose
    
    successful = sum(1 for r in results if r.success)
    print(f"   ✓ {successful}/{len(results)} ejecuciones exitosas\n")
    
    # PASO 4: Análisis estadístico
    print("=" * 80)
    print("  ANÁLISIS ESTADÍSTICO")
    print("=" * 80)
    print()
    
    analyzer = StatisticalAnalyzer(alpha=0.05)
    
    # Agrupar resultados por algoritmo
    algorithm_results = {}
    for alg in algorithms:
        alg_name = alg['name']
        alg_data = [r for r in results if r.algorithm_name == alg_name and r.success]
        
        if alg_data:
            gaps = [r.gap_to_optimal for r in alg_data if r.gap_to_optimal is not None]
            times = [r.total_time for r in alg_data]
            algorithm_results[alg_name] = {
                'gaps': gaps,
                'times': times
            }
    
    # Mostrar estadísticas por algoritmo
    print("📊 Estadísticas Descriptivas:\n")
    
    for alg_name in sorted(algorithm_results.keys()):
        data = algorithm_results[alg_name]
        gaps = data['gaps']
        times = data['times']
        
        gap_stats = analyzer.descriptive_statistics(gaps)
        time_stats = analyzer.descriptive_statistics(times)
        ci = analyzer.confidence_interval(gaps, confidence=0.95)
        
        print(f"📈 {alg_name}:")
        print(f"   Gap (%) - Media: {gap_stats['mean']:.2f}, Std: {gap_stats['std']:.2f}")
        print(f"           - Min: {gap_stats['min']:.2f}, Max: {gap_stats['max']:.2f}")
        print(f"           - IC 95%: [{ci[0]:.2f}, {ci[1]:.2f}]")
        print(f"   Tiempo (s) - Media: {time_stats['mean']:.4f}, Std: {time_stats['std']:.4f}")
        print()
    
    # Test de comparación (si hay 2+ algoritmos)
    if len(algorithm_results) >= 2:
        print("=" * 80)
        print("  TEST DE COMPARACIÓN")
        print("=" * 80)
        print()
        
        # Preparar datos para comparación
        algo_gaps = {name: data['gaps'] for name, data in algorithm_results.items()}
        
        # Friedman test
        print("🔬 Friedman Test (no-paramétrico para múltiples muestras):")
        comparison = analyzer.compare_multiple_algorithms(algo_gaps, test_type="friedman")
        
        print(f"   Test: {comparison['global_test'].test_name}")
        print(f"   p-value: {comparison['global_test'].p_value:.6f}")
        print(f"   Interpretación: {comparison['global_test'].interpretation}")
        print()
        
        # Rankings
        print("📊 Rankings Promedio (1 = mejor):")
        for alg_name in sorted(comparison['average_rankings'].keys()):
            rank = comparison['average_rankings'][alg_name]
            print(f"   {alg_name}: {rank:.2f}")
        print()
        
        print(f"🏆 Mejor algoritmo: {comparison['best_algorithm']}")
        print()
        
        # Test pareado si hay exactamente 2 algoritmos
        if len(algorithm_results) == 2:
            algs = list(algorithm_results.keys())
            data1 = algorithm_results[algs[0]]['gaps']
            data2 = algorithm_results[algs[1]]['gaps']
            
            # Ajustar a mismo tamaño
            min_len = min(len(data1), len(data2))
            data1 = data1[:min_len]
            data2 = data2[:min_len]
            
            print("🔬 Wilcoxon Signed-Rank Test (pareado):")
            wilcoxon = analyzer.wilcoxon_signed_rank_test(data1, data2)
            print(f"   p-value: {wilcoxon.p_value:.6f}")
            print(f"   {wilcoxon.interpretation}")
            print()
            
            cohens_d = analyzer.effect_size_cohens_d(data1, data2)
            print(f"🔬 Cohen's d (tamaño del efecto): {cohens_d:.3f}")
            if abs(cohens_d) < 0.2:
                effect = "pequeño"
            elif abs(cohens_d) < 0.5:
                effect = "mediano"
            else:
                effect = "grande"
            print(f"   Efecto: {effect}")
    
    print("\n" + "=" * 80)
    print("✅ Análisis completado")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

---

## Ejemplo 4: Personalizado con Parámetros

**Archivo:** `test_custom_parameters.py`

```python
#!/usr/bin/env python3
"""
Ejemplo personalizado con parámetros ajustables
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.runner import ExperimentRunner, ExperimentConfig
from data.loader import DatasetLoader


def run_experiment(num_algorithms=3, 
                  min_depth=2, 
                  max_depth=3,
                  group="low_dimensional",
                  max_time=5.0,
                  verbose=True):
    """
    Ejecuta experimento con parámetros personalizados
    
    Args:
        num_algorithms: Cantidad de algoritmos a generar
        min_depth: Profundidad mínima del AST
        max_depth: Profundidad máxima del AST
        group: Grupo de instancias ('low_dimensional' o 'large_scale')
        max_time: Timeout por ejecución (segundos)
        verbose: Mostrar progreso detallado
    
    Returns:
        Ruta del archivo JSON con resultados
    """
    
    if verbose:
        print("=" * 80)
        print("  EXPERIMENTO PERSONALIZADO")
        print("=" * 80)
        print(f"\nParámetros:")
        print(f"  • Algoritmos: {num_algorithms}")
        print(f"  • Profundidad AST: [{min_depth}, {max_depth}]")
        print(f"  • Grupo: {group}")
        print(f"  • Timeout: {max_time}s")
        print()
    
    # Generar algoritmos
    if verbose:
        print("1️⃣  Generando algoritmos...")
    
    grammar = Grammar(min_depth=min_depth, max_depth=max_depth)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    algorithms = []
    for i in range(num_algorithms):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'Custom_Algo_{i+1}',
                'ast': ast
            })
    
    if verbose:
        print(f"   ✓ {len(algorithms)}/{num_algorithms} generados\n")
    
    # Cargar instancias
    if verbose:
        print("2️⃣  Cargando instancias del grupo...")
    
    datasets_dir = Path(__file__).parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    instances = loader.load_folder(group)
    instance_names = [inst.name for inst in instances]
    
    if verbose:
        print(f"   ✓ {len(instances)} instancias cargadas\n")
    
    # Configurar y ejecutar
    if verbose:
        print("3️⃣  Ejecutando experimento...")
    
    config = ExperimentConfig(
        name=f"custom_{group}_{num_algorithms}_algos",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,
        max_time_seconds=max_time,
        output_dir=f"output/custom_{group}"
    )
    
    runner = ExperimentRunner(config)
    runner.problems = {inst.name: inst for inst in instances}
    results = runner.run_all(verbose=verbose)
    
    # Guardar
    json_file = runner.save_results()
    
    if verbose:
        print(f"\n✅ Experimento completado")
        print(f"   Archivo: {json_file}")
    
    return json_file


def main():
    # Ejemplo 1: Defaults
    print("\n" + "=" * 80)
    print("Ejemplo 1: Configuración por defecto")
    print("=" * 80)
    run_experiment(verbose=True)
    
    # Ejemplo 2: Más algoritmos, más profundidad
    print("\n" + "=" * 80)
    print("Ejemplo 2: 5 algoritmos con mayor profundidad")
    print("=" * 80)
    run_experiment(
        num_algorithms=5,
        max_depth=5,
        verbose=True
    )
    
    # Ejemplo 3: Large-scale
    print("\n" + "=" * 80)
    print("Ejemplo 3: Instancias large-scale")
    print("=" * 80)
    run_experiment(
        num_algorithms=3,
        group="large_scale",
        max_time=10.0,
        verbose=True
    )


if __name__ == "__main__":
    main()
```

---

## Ejemplo 5: Inspección Detallada de Algoritmos

**Archivo:** `test_inspect_algorithms.py`

```python
#!/usr/bin/env python3
"""
Ejemplo: Inspección detallada de algoritmos generados
"""

import sys
import json
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar


def analyze_ast(ast, name="Algorithm"):
    """Analiza estructura de un AST"""
    
    print(f"\n{'=' * 70}")
    print(f"  Análisis de {name}")
    print(f"{'=' * 70}\n")
    
    # 1. Tipo de raíz
    print(f"1. Estructura:")
    print(f"   • Nodo raíz: {type(ast).__name__}")
    
    # 2. Pseudocódigo
    print(f"\n2. Pseudocódigo:")
    pseudocode = ast.to_pseudocode(indent=1)
    for line in pseudocode.split('\n'):
        print(f"   {line}")
    
    # 3. Representación JSON
    print(f"\n3. Representación JSON:")
    ast_dict = ast.to_dict()
    json_str = json.dumps(ast_dict, indent=2, ensure_ascii=False)
    for line in json_str.split('\n')[:20]:  # Primeras 20 líneas
        print(f"   {line}")
    if len(json_str.split('\n')) > 20:
        print(f"   ... ({len(json_str.split('\n')) - 20} líneas más)")
    
    # 4. Estadísticas
    print(f"\n4. Estadísticas:")
    
    def count_nodes(node, type_name=None):
        """Cuenta nodos recursivamente"""
        count = {node.__class__.__name__: 1}
        
        if hasattr(node, 'body'):
            for child in node.body:
                for node_type, n in count_nodes(child).items():
                    count[node_type] = count.get(node_type, 0) + n
        
        if hasattr(node, 'then_branch') and node.then_branch:
            for node_type, n in count_nodes(node.then_branch).items():
                count[node_type] = count.get(node_type, 0) + n
        
        if hasattr(node, 'else_branch') and node.else_branch:
            for node_type, n in count_nodes(node.else_branch).items():
                count[node_type] = count.get(node_type, 0) + n
        
        if hasattr(node, 'statement'):
            for node_type, n in count_nodes(node.statement).items():
                count[node_type] = count.get(node_type, 0) + n
        
        return count
    
    node_counts = count_nodes(ast)
    total_nodes = sum(node_counts.values())
    
    print(f"   • Total nodos: {total_nodes}")
    print(f"   • Composición:")
    for node_type, count in sorted(node_counts.items()):
        percentage = (count / total_nodes) * 100
        print(f"     - {node_type}: {count} ({percentage:.1f}%)")


def main():
    print("=" * 70)
    print("  INSPECCIÓN DETALLADA DE 3 ALGORITMOS GENERADOS")
    print("=" * 70)
    
    # Generar
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=123)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append(ast)
    
    # Analizar cada uno
    for i, ast in enumerate(algorithms, 1):
        analyze_ast(ast, f"Algoritmo {i}")
    
    # Comparación
    print(f"\n\n{'=' * 70}")
    print("  COMPARACIÓN DE LOS 3 ALGORITMOS")
    print(f"{'=' * 70}\n")
    
    print("Complejidad (nodos totales):")
    for i, ast in enumerate(algorithms, 1):
        # Contar nodos
        def count_all_nodes(node):
            count = 1
            if hasattr(node, 'body'):
                count += sum(count_all_nodes(child) for child in node.body)
            if hasattr(node, 'then_branch') and node.then_branch:
                count += count_all_nodes(node.then_branch)
            if hasattr(node, 'else_branch') and node.else_branch:
                count += count_all_nodes(node.else_branch)
            if hasattr(node, 'statement'):
                count += count_all_nodes(node.statement)
            return count
        
        nodes = count_all_nodes(ast)
        print(f"  Algoritmo {i}: {nodes} nodos")
    
    print("\n✅ Inspección completada")


if __name__ == "__main__":
    main()
```

---

## 🚀 Cómo Ejecutar Estos Ejemplos

```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\KBP-SA

# Ejemplo 1: Generación simple
python test_simple_generation.py

# Ejemplo 2: Flujo completo
python test_complete_workflow.py

# Ejemplo 3: Con estadísticas
python test_with_statistics.py

# Ejemplo 4: Personalizado (editar parámetros en main())
python test_custom_parameters.py

# Ejemplo 5: Inspección detallada
python test_inspect_algorithms.py
```

---

## 📊 Estructura de Salida Esperada

Para cada ejemplo, esperar:

```
output/
├── demo_results/
│   ├── low_dimensional_experiments/
│   │   └── experiment_*.json          ← Resultados principales
│   └── large_scale_experiments/
│       └── experiment_*.json
│
├── stats_demo/
│   └── low_dimensional_experiments/
│       └── experiment_*.json
│
└── custom_low_dimensional/
    └── low_dimensional_experiments/
        └── experiment_custom_*.json
```

Cada JSON contiene:
- **config:** Parámetros del experimento
- **results:** 30-63 resultados individuales
- **summary:** Estadísticas agregadas por algoritmo

---

**Versión:** 1.0  
**Última actualización:** Enero 2026
