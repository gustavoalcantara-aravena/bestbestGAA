# Usage Guide

Complete guide on how to use VRPTW-GRASP with GAA Integration framework.

## Table of Contents

1. [Basic Workflow](#basic-workflow)
2. [Loading Instances](#loading-instances)
3. [Creating Solvers](#creating-solvers)
4. [Running Experiments](#running-experiments)
5. [Analyzing Results](#analyzing-results)
6. [Visualization](#visualization)
7. [Advanced Topics](#advanced-topics)

---

## Basic Workflow

### Step 1: Load an Instance

```python
from src.core.instance import Instance

# Load from Solomon CSV
instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Check instance properties
print(f"Number of customers: {instance.num_customers}")
print(f"Vehicle capacity: {instance.vehicle_capacity}")
print(f"Depot: {instance.depot}")
```

### Step 2: Create a Solver

```python
from src.core.grasp import GRASP

# Create GRASP solver with reproducible seed
grasp = GRASP(instance, seed=42)
```

### Step 3: Solve the Instance

```python
# Solve with 100 iterations
solution = grasp.solve(max_iterations=100)

# Check solution properties
print(f"Number of routes: {solution.num_routes}")
print(f"Total distance: {solution.total_distance:.2f}")
print(f"Is feasible: {solution.is_feasible()}")
```

---

## Loading Instances

### From Solomon CSV

```python
from src.core.instance import Instance

# Single instance
instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Multiple instances
instances = []
for family in ['C1', 'R1', 'RC1']:
    instance = Instance.from_solomon_csv(f"datasets/benchmark/{family}01.csv")
    instances.append(instance)
```

### Validating Instances

```python
# Check if instance is valid
if instance.is_valid():
    print("Instance is valid")
else:
    print("Instance has issues")

# Get instance info
print(f"Customers: {instance.num_customers}")
print(f"Depot coordinates: ({instance.depot.x}, {instance.depot.y})")
```

### Available Solomon Instances

```
56 instances in 6 families:
- C1 (9 instances):  C101-C109     (clustered, small)
- C2 (8 instances):  C201-C208     (clustered, large)
- R1 (12 instances): R101-R112     (random, small)
- R2 (11 instances): R201-R211     (random, large)
- RC1 (8 instances): RC101-RC108   (mixed, small)
- RC2 (8 instances): RC201-RC208   (mixed, large)
```

---

## Creating Solvers

### GRASP Solver

```python
from src.core.grasp import GRASP

# Basic GRASP
grasp = GRASP(instance, seed=42)

# GRASP with custom parameters
grasp = GRASP(
    instance,
    seed=42,
    alpha=0.2,  # Greediness parameter
    max_iterations=100,
    max_runtime=300  # seconds
)

# Run solver
solution = grasp.solve()
```

### GRASP with ILS (Iterated Local Search)

```python
from src.core.grasp import GRASP_ILS

# GRASP + ILS hybrid
ils = GRASP_ILS(instance, seed=42)

# Run with ILS
solution = ils.solve(
    max_iterations=100,
    perturbation_strength=0.1
)
```

### Custom Solver Configuration

```python
config = {
    'seed': 42,
    'max_iterations': 100,
    'max_runtime': 300,
    'construction_method': 'savings',  # or 'nearest_neighbor'
    'local_search_method': 'vnd',      # or 'ils'
}

grasp = GRASP(instance, **config)
solution = grasp.solve()
```

---

## Running Experiments

### Quick Experiment (1 Family, 12 Instances)

```python
from src.experiments import ExperimentConfig, ExperimentExecutor

# Configure QUICK experiment
config = ExperimentConfig(
    mode='QUICK',
    families=['R1'],  # Only R1 family
    seed=42
)

# Execute
executor = ExperimentExecutor(config)
executor.run()

# Results saved to: output/timestamp/
# - results/raw_results.csv
# - results/experiment_metadata.json
# - plots/
# - logs/
```

### Full Experiment (6 Families, 56 Instances)

```python
# Configure FULL experiment
config = ExperimentConfig(
    mode='FULL',
    families=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],
    seed=42
)

# Execute - runs 56 instances
executor = ExperimentExecutor(config)
executor.run()

# Generates 168 experiments (56 instances × 3 algorithms)
```

### Custom Experiment Configuration

```python
config = ExperimentConfig(
    mode='FULL',
    families=['R1', 'R2'],  # Only R families
    algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2'],  # 2 algorithms
    seed=42
)

executor = ExperimentExecutor(config)
executor.run()
```

### Monitoring Experiment Progress

```python
# Run and get intermediate results
executor = ExperimentExecutor(config)

# Get progress
total = executor.total_experiments
for i, result in enumerate(executor.run_with_progress()):
    print(f"Progress: {i+1}/{total}")
    print(f"  Algorithm: {result.algorithm}")
    print(f"  Instance: {result.instance}")
    print(f"  K (routes): {result.K}")
    print(f"  D (distance): {result.D:.2f}")
```

---

## Analyzing Results

### Loading Results

```python
import pandas as pd

# Load raw results CSV
results_df = pd.read_csv("output/timestamp/results/raw_results.csv")

print(results_df.head())
print(results_df.describe())
```

### Statistical Analysis

```python
from scripts.statistical_analysis import StatisticalAnalysisReport

# Create report
report = StatisticalAnalysisReport()

# Run full analysis
analysis = report.run_full_analysis(results_df)

# Access different analyses
print("Descriptive stats:", analysis['descriptive_stats'])
print("Kruskal-Wallis test:", analysis['kruskal_wallis'])
print("Effect sizes:", analysis['effect_sizes'])
```

### Algorithm Comparison

```python
# Compare algorithms
algo_stats = analysis['algorithm_analysis']

for algo, stats in algo_stats.items():
    print(f"{algo}:")
    print(f"  Avg K: {stats.mean_K:.2f}")
    print(f"  Std K: {stats.std_K:.2f}")
    print(f"  Avg D: {stats.mean_D:.2f}")
    print(f"  Success rate: {stats.success_rate:.1%}")
```

### Family Performance

```python
# Analyze by family
family_stats = analysis['family_analysis']

for family, stats in family_stats.items():
    print(f"{family}:")
    print(f"  Avg gap: {stats.gap_percent:.2f}%")
    print(f"  K_BKS match: {stats.k_bks_match_rate:.1%}")
```

### Convergence Analysis

```python
from scripts.statistical_analysis import ConvergenceAnalysis

conv = ConvergenceAnalysis()

# Time to K_BKS
time_analysis = conv.time_to_k_bks(results_df)
print(f"Avg time to K_BKS: {time_analysis['mean_time']:.2f} seconds")

# Iterations to K_BKS
iter_analysis = conv.iterations_to_k_bks(results_df)
print(f"Avg iterations to K_BKS: {iter_analysis['mean_iterations']:.0f}")
```

---

## Visualization

### Convergence Plots

```python
from src.core.outputs import MatplotlibVisualizer

visualizer = MatplotlibVisualizer()

# Plot convergence by algorithm
visualizer.plot_convergence(
    results_df,
    title="Algorithm Convergence",
    save_path="output/convergence.png"
)
```

### Boxplots

```python
# Compare algorithms using boxplots
visualizer.plot_boxplots(
    results_df,
    column='K',  # Number of routes
    by='algorithm',
    title="Route Count Comparison",
    save_path="output/boxplot_K.png"
)

# Compare by family
visualizer.plot_boxplots(
    results_df,
    column='D',  # Total distance
    by='family',
    title="Distance by Family",
    save_path="output/boxplot_D.png"
)
```

### Heatmap

```python
# Algorithm vs Family performance heatmap
visualizer.plot_heatmap(
    results_df,
    title="Algorithm × Family Performance",
    save_path="output/heatmap.png"
)
```

### Time Analysis

```python
# Time spent vs performance
visualizer.plot_time_vs_performance(
    results_df,
    title="Time vs Solution Quality",
    save_path="output/time_analysis.png"
)
```

### Save All Plots

```python
# Generate and save all standard plots
visualizer.generate_all_plots(
    results_df,
    output_dir="output/plots"
)

# Generates: convergence, boxplots, heatmap, time analysis, etc.
```

---

## Advanced Topics

### Custom Operators

```python
from src.core.operators import OperatorBase

class CustomOperator(OperatorBase):
    def apply(self, solution):
        # Implement custom logic
        return modified_solution

# Use in GRASP
grasp = GRASP(instance, seed=42)
grasp.add_operator(CustomOperator())
solution = grasp.solve()
```

### Algorithm Generation

```python
from src.gaa.generator import AlgorithmGenerator

# Generate algorithms
generator = AlgorithmGenerator(seed=42)
algorithms = generator.generate(count=3)

# Each algorithm is a JSON AST
for algo in algorithms:
    print(f"Algorithm structure: {algo}")
```

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def solve_instance(instance_path):
    instance = Instance.from_solomon_csv(instance_path)
    grasp = GRASP(instance, seed=42)
    return grasp.solve()

# Parallel processing
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(solve_instance, instance_paths))
```

### Custom Configuration

```python
import yaml

# Load custom config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use in experiments
experiment_config = ExperimentConfig(**config['experiment'])
executor = ExperimentExecutor(experiment_config)
executor.run()
```

### Reproducibility

```python
# All operations with same seed produce same results
seed = 42

# Experiment 1
config1 = ExperimentConfig(mode='QUICK', seed=seed)
executor1 = ExperimentExecutor(config1)
results1 = executor1.run()

# Experiment 2 (same seed)
config2 = ExperimentConfig(mode='QUICK', seed=seed)
executor2 = ExperimentExecutor(config2)
results2 = executor2.run()

# results1 == results2 (same K, D, routes, etc.)
assert results1['K'] == results2['K']
```

---

## Common Workflows

### Workflow 1: Quick Algorithm Testing

```python
from src.core.instance import Instance
from src.core.grasp import GRASP

# Load instance
instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Test algorithm
grasp = GRASP(instance, seed=42)
solution = grasp.solve(max_iterations=50)

# Report
print(f"Routes: {solution.num_routes}")
print(f"Distance: {solution.total_distance:.2f}")
print(f"Time: {solution.total_time:.2f}s")
```

### Workflow 2: Full Benchmark Comparison

```python
# Run FULL experiment
config = ExperimentConfig(mode='FULL', seed=42)
executor = ExperimentExecutor(config)
executor.run()

# Analyze
report = StatisticalAnalysisReport()
analysis = report.run_full_analysis(executor.results_df)

# Visualize
visualizer = MatplotlibVisualizer()
visualizer.generate_all_plots(executor.results_df, "output/plots")
```

### Workflow 3: Algorithm Development

```python
# Test custom algorithm
algo = MyCustomAlgorithm(instance)
solution = algo.solve()

# Validate
if solution.is_feasible():
    print(f"Routes: {solution.num_routes}")
    print(f"Distance: {solution.total_distance}")
else:
    print("Solution is infeasible!")
```

---

## Performance Tips

1. **Use appropriate max_iterations**: More iterations = better quality but slower
2. **Set max_runtime**: Limit execution time instead of iterations
3. **Use QUICK mode for testing**: Before running FULL mode
4. **Enable parallel processing**: For batch experiments
5. **Cache instance loading**: Load once, reuse multiple times

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

---

**Last Updated**: January 2, 2026
