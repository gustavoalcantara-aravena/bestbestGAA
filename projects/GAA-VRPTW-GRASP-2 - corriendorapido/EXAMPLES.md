# Examples and Use Cases

Practical code examples and common usage patterns.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Batch Processing](#batch-processing)
3. [Advanced Algorithms](#advanced-algorithms)
4. [Analysis Examples](#analysis-examples)
5. [Production Workflows](#production-workflows)

---

## Basic Usage

### Example 1: Simple Problem Solving

Solve a single instance and display results:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP

# Load instance
instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Create solver
grasp = GRASP(instance, seed=42, max_iterations=100)

# Solve
solution = grasp.solve()

# Display results
print(f"Instance: C101")
print(f"Number of routes: {solution.num_routes}")
print(f"Total distance: {solution.total_distance:.2f}")
print(f"Solution is feasible: {solution.is_feasible()}")
```

### Example 2: Compare Multiple Seeds

Run same instance with different seeds:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP
import pandas as pd

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

results = []
for seed in [1, 42, 100, 200, 300]:
    grasp = GRASP(instance, seed=seed, max_iterations=100)
    solution = grasp.solve()
    
    results.append({
        'seed': seed,
        'routes': solution.num_routes,
        'distance': solution.total_distance
    })

# Create comparison table
df = pd.DataFrame(results)
print(df)

# Find best seed
best_idx = df['distance'].idxmin()
print(f"\nBest seed: {df.loc[best_idx, 'seed']}")
```

### Example 3: Time-Limited Solving

Solve with time constraint instead of iteration limit:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Solve with 30-second limit
grasp = GRASP(instance, seed=42, max_runtime=30)
solution = grasp.solve()

print(f"Routes found in 30s: {solution.num_routes}")
print(f"Distance: {solution.total_distance:.2f}")
```

---

## Batch Processing

### Example 4: Process All Solomon Instances

Solve all 56 instances:

```python
from pathlib import Path
from src.core.instance import Instance
from src.core.grasp import GRASP
import pandas as pd

results = []
instance_dir = Path("datasets/benchmark")

for csv_file in sorted(instance_dir.glob("*.csv")):
    instance_name = csv_file.stem
    print(f"Solving {instance_name}...", end=" ")
    
    instance = Instance.from_solomon_csv(str(csv_file))
    grasp = GRASP(instance, seed=42, max_iterations=100)
    solution = grasp.solve()
    
    results.append({
        'instance': instance_name,
        'routes': solution.num_routes,
        'distance': solution.total_distance,
        'feasible': solution.is_feasible()
    })
    
    print(f"K={solution.num_routes}, D={solution.total_distance:.1f}")

# Create results dataframe
df = pd.DataFrame(results)
print(f"\nProcessed {len(df)} instances")
print(f"Average routes: {df['routes'].mean():.2f}")
print(f"Average distance: {df['distance'].mean():.2f}")
```

### Example 5: Family-Based Batch Processing

Process instances by family:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP
from pathlib import Path
import pandas as pd

families = ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']
instance_dir = Path("datasets/benchmark")

family_results = {}

for family in families:
    results = []
    
    # Find instances in this family
    pattern = f"{family}*.csv"
    instances = sorted(instance_dir.glob(pattern))
    
    print(f"\nFamily {family}: {len(instances)} instances")
    
    for csv_file in instances:
        instance = Instance.from_solomon_csv(str(csv_file))
        grasp = GRASP(instance, seed=42)
        solution = grasp.solve()
        
        results.append({
            'routes': solution.num_routes,
            'distance': solution.total_distance
        })
    
    df = pd.DataFrame(results)
    family_results[family] = {
        'count': len(df),
        'avg_routes': df['routes'].mean(),
        'avg_distance': df['distance'].mean()
    }

# Summary by family
for family, stats in family_results.items():
    print(f"{family}: {stats['count']} instances, "
          f"avg {stats['avg_routes']:.1f} routes, "
          f"avg {stats['avg_distance']:.1f} distance")
```

---

## Advanced Algorithms

### Example 6: Using GRASP with ILS

Solve with Iterated Local Search perturbation:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP_ILS

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# GRASP with ILS
ils = GRASP_ILS(instance, seed=42)
solution = ils.solve(
    max_iterations=100,
    perturbation_strength=0.1  # 10% perturbation
)

print(f"ILS solution - Routes: {solution.num_routes}, "
      f"Distance: {solution.total_distance:.2f}")
```

### Example 7: Custom Operators

Add custom operators to GRASP:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP
from src.core.operators import OperatorBase

class CustomLocalSearch(OperatorBase):
    """Custom local search operator."""
    
    def apply(self, solution):
        # Your custom logic
        improved = solution.copy()
        # Improve routes...
        return improved

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

grasp = GRASP(instance, seed=42)
grasp.add_operator(CustomLocalSearch())

solution = grasp.solve()
print(f"Solution with custom operator: {solution.num_routes} routes")
```

---

## Analysis Examples

### Example 8: Statistical Comparison

Compare multiple algorithm runs statistically:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP
from scripts.statistical_analysis import StatisticalTests
import numpy as np

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Run algorithm multiple times
results_algo1 = []
results_algo2 = []

for seed in range(1, 11):  # 10 runs each
    grasp1 = GRASP(instance, seed=seed, alpha=0.2)
    sol1 = grasp1.solve()
    results_algo1.append(sol1.total_distance)
    
    grasp2 = GRASP(instance, seed=seed, alpha=0.5)
    sol2 = grasp2.solve()
    results_algo2.append(sol2.total_distance)

# Statistical test
tests = StatisticalTests()
result = tests.wilcoxon_test(results_algo1, results_algo2)

print(f"Wilcoxon test p-value: {result.p_value:.4f}")
if result.significant:
    print("Results are significantly different")
else:
    print("No significant difference")

# Effect size
cohens_d = tests.cohens_d(results_algo1, results_algo2)
print(f"Cohen's d: {cohens_d:.3f}")
```

### Example 9: Convergence Analysis

Analyze convergence to optimal:

```python
from src.core.instance import Instance
from src.core.grasp import GRASP
import json

instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")

# Load best-known solution
with open('best_known_solutions.json') as f:
    bks = json.load(f)

k_bks = bks['C101']['K_BKS']
d_bks = bks['C101']['D_BKS']

# Run and track convergence
grasp = GRASP(instance, seed=42, max_iterations=100)
solution = grasp.solve()

# Calculate metrics
gap_k = solution.num_routes - k_bks
gap_d = (solution.total_distance - d_bks) / d_bks * 100

print(f"K_BKS: {k_bks}, K_found: {solution.num_routes}, delta_K: {gap_k}")
print(f"D_BKS: {d_bks:.2f}, D_found: {solution.total_distance:.2f}, gap: {gap_d:.2f}%")
```

### Example 10: Visualization

Create visualizations from results:

```python
from src.core.outputs import MatplotlibVisualizer
import pandas as pd

# Load results
results_df = pd.read_csv("output/timestamp/results/raw_results.csv")

# Create visualizer
visualizer = MatplotlibVisualizer()

# Generate plots
visualizer.plot_convergence(results_df, "Convergence Analysis")
visualizer.plot_boxplots(results_df, column='K', by='algorithm', 
                        title="Routes by Algorithm")
visualizer.plot_heatmap(results_df, title="Performance Heatmap")

# Save all
visualizer.save_all("output/plots")
print("Plots saved to output/plots/")
```

---

## Production Workflows

### Example 11: Complete Experiment Pipeline

Full workflow from configuration to analysis:

```python
from src.experiments import ExperimentConfig, ExperimentExecutor
from scripts.statistical_analysis import StatisticalAnalysisReport
from src.core.outputs import MatplotlibVisualizer
import pandas as pd

# 1. Configure experiment
config = ExperimentConfig(
    mode='FULL',
    families=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],
    seed=42
)

print("1. Running experiments...")

# 2. Execute
executor = ExperimentExecutor(config)
executor.run()

print("2. Analyzing results...")

# 3. Load and analyze
results_df = pd.read_csv(executor.results_csv)

report = StatisticalAnalysisReport()
analysis = report.run_full_analysis(results_df)

# Print summary
print("\n=== ANALYSIS SUMMARY ===")
print(f"Total experiments: {len(results_df)}")
print(f"Average K (routes): {results_df['K'].mean():.2f}")
print(f"Average D (distance): {results_df['D'].mean():.2f}")
print(f"Success rate: {results_df['reached_K_BKS'].mean():.1%}")

print("\n3. Generating visualizations...")

# 4. Visualize
visualizer = MatplotlibVisualizer()
visualizer.generate_all_plots(results_df, executor.results_dir / "plots")

print(f"\nExperiment complete! Results in {executor.results_dir}")
```

### Example 12: Benchmark Comparison Script

Compare your solver with baseline:

```python
from pathlib import Path
from src.core.instance import Instance
from src.core.grasp import GRASP
import json
import pandas as pd

instance_dir = Path("datasets/benchmark")

# Load BKS
with open('best_known_solutions.json') as f:
    bks_data = json.load(f)

results = []

# Test all instances
for csv_file in sorted(instance_dir.glob("*.csv")):
    instance_name = csv_file.stem
    
    instance = Instance.from_solomon_csv(str(csv_file))
    grasp = GRASP(instance, seed=42, max_iterations=100)
    solution = grasp.solve()
    
    bks = bks_data[instance_name]
    gap_k = solution.num_routes - bks['K_BKS']
    gap_d = (solution.total_distance - bks['D_BKS']) / bks['D_BKS'] * 100
    
    results.append({
        'instance': instance_name,
        'K': solution.num_routes,
        'K_BKS': bks['K_BKS'],
        'gap_K': gap_k,
        'D': solution.total_distance,
        'D_BKS': bks['D_BKS'],
        'gap_D%': gap_d,
        'reached_BKS': gap_k == 0
    })

# Create benchmark report
df = pd.DataFrame(results)
df.to_csv("benchmark_results.csv", index=False)

# Print summary
print(f"Benchmark results ({len(df)} instances):")
print(f"  K matches BKS: {df['reached_BKS'].sum()}/{len(df)} ({df['reached_BKS'].mean():.1%})")
print(f"  Avg gap D%: {df['gap_D%'].mean():.2f}%")
print(f"\nDetailed results saved to benchmark_results.csv")
```

---

## Tips & Tricks

### Tip 1: Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def solve_instance(csv_path):
    instance = Instance.from_solomon_csv(csv_path)
    grasp = GRASP(instance, seed=42)
    return grasp.solve()

# Solve multiple instances in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    solutions = list(executor.map(solve_instance, instance_paths))
```

### Tip 2: Caching Results

```python
# Load once, reuse multiple times
instance = Instance.from_solomon_csv("C101.csv")

solutions = []
for alpha in [0.1, 0.2, 0.5]:
    grasp = GRASP(instance, alpha=alpha)  # Reuse instance
    solutions.append(grasp.solve())
```

### Tip 3: Progress Tracking

```python
from tqdm import tqdm

instances = sorted(Path("datasets/benchmark").glob("*.csv"))

for csv_file in tqdm(instances, desc="Solving"):
    instance = Instance.from_solomon_csv(str(csv_file))
    grasp = GRASP(instance, seed=42)
    solution = grasp.solve()
```

---

**Last Updated**: January 2, 2026  
**Status**: Examples Complete ✅
