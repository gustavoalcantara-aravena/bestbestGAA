# Best Practices Guide

Guidelines, patterns, and best practices for using and extending VRPTW-GRASP framework.

## Code Organization

### File Structure

```
project/
├── src/
│   ├── core/          # Core classes (Instance, Route, Solution)
│   ├── gaa/           # Algorithm generation framework
│   └── utils/         # Helper functions and loaders
├── scripts/
│   ├── experiments.py           # Experiment framework
│   ├── statistical_analysis.py # Statistical tests
│   └── validation.py            # Validation framework
├── datasets/          # Benchmark instances
├── output/            # Experiment results
└── tests/             # Test files
```

### Naming Conventions

- **Classes**: PascalCase (`GRASP`, `Instance`, `ExperimentConfig`)
- **Functions**: snake_case (`solve_instance`, `load_csv`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_ITERATIONS`, `VEHICLE_CAPACITY`)
- **Private**: Leading underscore (`_helper_method`)

## Writing Solutions

### 1. Validation Before Use

```python
# ✅ Good
instance = Instance.from_solomon_csv(path)
if instance.is_valid():
    grasp = GRASP(instance)
    solution = grasp.solve()

# ❌ Avoid
solution = GRASP(instance).solve()  # No validation
```

### 2. Use Seed for Reproducibility

```python
# ✅ Good - Reproducible
grasp = GRASP(instance, seed=42)
solution = grasp.solve()

# ❌ Avoid - Random every time
grasp = GRASP(instance)  # No seed
solution = grasp.solve()
```

### 3. Check Feasibility

```python
# ✅ Good
solution = grasp.solve()
if solution.is_feasible():
    print(f"Routes: {solution.num_routes}")
else:
    print("Solution is infeasible!")

# ❌ Avoid
solution = grasp.solve()
print(solution.num_routes)  # Might be infeasible
```

### 4. Use Meaningful Variable Names

```python
# ✅ Good
best_solution = grasp.solve()
best_distance = best_solution.total_distance
improvement = baseline_distance - best_distance

# ❌ Avoid
sol = grasp.solve()
d = sol.total_distance
imp = base_d - d
```

## Performance Optimization

### 1. Reuse Instances

```python
# ✅ Good - Load once
instance = Instance.from_solomon_csv(path)
solver1 = GRASP(instance, seed=1)
solver2 = GRASP(instance, seed=2)
solution1 = solver1.solve()
solution2 = solver2.solve()

# ❌ Avoid - Load multiple times
solution1 = GRASP(Instance.from_solomon_csv(path), seed=1).solve()
solution2 = GRASP(Instance.from_solomon_csv(path), seed=2).solve()
```

### 2. Set Appropriate Limits

```python
# ✅ Good - Balanced
grasp = GRASP(instance, max_iterations=100, max_runtime=60)

# ❌ Too many iterations
grasp = GRASP(instance, max_iterations=10000)  # Very slow

# ❌ Too few iterations
grasp = GRASP(instance, max_iterations=5)  # Low quality
```

### 3. Use Batch Processing

```python
# ✅ Good - Batch experiments
config = ExperimentConfig(mode='FULL')
executor = ExperimentExecutor(config)
executor.run()  # Process all at once

# ❌ Avoid - Individual runs
for instance_path in all_paths:
    solution = GRASP(load(instance_path)).solve()
```

### 4. Cache Analysis Results

```python
# ✅ Good
results_df = pd.read_csv(csv_path)
analysis = run_analysis(results_df)
# Reuse analysis for multiple visualizations

# ❌ Avoid
# Recalculating analysis each time
for plot in all_plots:
    analysis = run_analysis(results_df)
    create_plot(analysis)
```

## Experiment Management

### 1. Use Consistent Configuration

```python
# ✅ Good - Centralized config
config = ExperimentConfig(
    mode='FULL',
    families=['R1', 'R2'],
    seed=42
)
executor = ExperimentExecutor(config)
executor.run()

# Save and reuse configuration
with open('config.yaml', 'w') as f:
    yaml.dump(config, f)
```

### 2. Document Experiment Runs

```python
# ✅ Good - Clear naming and docs
experiment_dir = "output/2026-01-02_FULL_seed42"
# Contains:
# - raw_results.csv
# - experiment_metadata.json
# - plots/
# - logs/

# README documenting purpose
```

### 3. Version Your Results

```python
# ✅ Good - Track versions
output/
  └── FULL_v1/         # Baseline
  └── FULL_v2/         # With optimization A
  └── FULL_v3/         # With optimization B
```

## Testing

### 1. Test Before Production

```python
# ✅ Good - Test first
pytest -v              # All tests
pytest --cov=src      # With coverage
# Only use after tests pass

# ❌ Avoid
# Using code without testing
```

### 2. Write Reproducible Tests

```python
# ✅ Good
def test_vrptw_solution():
    instance = Instance.from_solomon_csv("test.csv")
    grasp = GRASP(instance, seed=42)
    solution = grasp.solve()
    assert solution.is_feasible()
    assert solution.num_routes <= EXPECTED_ROUTES

# ❌ Avoid
def test_vrptw_solution():
    solution = GRASP(instance).solve()  # Non-deterministic
    assert solution.distance < 1000  # Arbitrary threshold
```

### 3. Test Edge Cases

```python
# ✅ Good
def test_single_customer():
    # Instance with 1 customer
    assert solution.num_routes == 1

def test_tight_time_windows():
    # Instance with very tight time windows
    assert solution.is_feasible()

def test_high_demand():
    # Instance with high demands
    assert solution.is_feasible()
```

## Statistical Analysis

### 1. Use Non-Parametric Tests

```python
# ✅ Good - Appropriate for this data
from scipy.stats import kruskal

stat, pvalue = kruskal(group1, group2, group3)
if pvalue < 0.05:
    print("Significant difference")

# ❌ Avoid - Assumes normal distribution
from scipy.stats import f_oneway
stat, pvalue = f_oneway(group1, group2, group3)
```

### 2. Report Effect Sizes

```python
# ✅ Good
cohens_d = (mean1 - mean2) / pooled_std
print(f"Effect size: {cohens_d:.2f}")
if cohens_d > 0.8:
    print("Large effect")

# ❌ Avoid
print(f"Mean diff: {mean1 - mean2}")  # Without context
```

### 3. Multiple Comparisons Correction

```python
# ✅ Good - Account for multiple tests
from scipy.stats import bonferroni
corrected_alpha = bonferroni(alpha, num_comparisons)

# ❌ Avoid
# Using uncorrected p-values with multiple comparisons
```

## Documentation

### 1. Document Complex Logic

```python
# ✅ Good
def calculate_gap_percent(d_final, d_bks):
    """
    Calculate gap percentage.
    
    Gap% = (D_final - D_BKS) / D_BKS * 100
    
    Only meaningful when K_final == K_BKS (optimal routes).
    
    Args:
        d_final: Final solution distance
        d_bks: Best-known solution distance
    
    Returns:
        Gap percentage (0 = optimal, >0 = suboptimal)
    """
    return (d_final - d_bks) / d_bks * 100

# ❌ Avoid
def calc_gap(df, db):
    return (df - db) / db * 100
```

### 2. Use Type Hints

```python
# ✅ Good
def solve_instance(instance: Instance,
                   max_iter: int = 100) -> Solution:
    """Solve instance using GRASP."""
    ...

# ❌ Avoid
def solve_instance(instance, max_iter=100):
    """Solve instance."""
    ...
```

### 3. Document Return Values

```python
# ✅ Good
def get_summary() -> Dict[str, Union[int, float, str]]:
    """
    Get validation summary.
    
    Returns:
        {
            'total_tests': int,
            'passed': int,
            'failed': int,
            'pass_rate': float,
            'status': str
        }
    """
    ...

# ❌ Avoid
def get_summary():
    """Get summary."""
    return summary_dict  # What's in it?
```

## Configuration Management

### 1. Use YAML for Configuration

```yaml
# ✅ Good - config.yaml
solver:
  name: "GRASP-ILS"
  seed: 42
  max_iterations: 100

dataset:
  dir: "datasets/benchmark"
  format: "csv"

output:
  dir: "output"
```

### 2. Validate Configuration

```python
# ✅ Good
config = ExperimentConfig(mode='FULL', seed=42)
assert config.validate()  # Verify before use

# ❌ Avoid
config = ExperimentConfig(mode='INVALID', seed=-1)
executor = ExperimentExecutor(config)  # Fails later
```

## Error Handling

### 1. Provide Meaningful Error Messages

```python
# ✅ Good
if not instance.is_valid():
    raise ValueError(
        f"Instance {path} is invalid: "
        f"has {instance.num_customers} customers "
        f"but {len(visited)} visited"
    )

# ❌ Avoid
if not instance.is_valid():
    raise ValueError("Instance invalid")
```

### 2. Use Try-Except Appropriately

```python
# ✅ Good
try:
    instance = Instance.from_solomon_csv(path)
except FileNotFoundError:
    print(f"File not found: {path}")
except ValueError as e:
    print(f"Invalid instance: {e}")

# ❌ Avoid
try:
    instance = Instance.from_solomon_csv(path)
except:
    pass  # Silently ignore error
```

## Algorithm Development

### 1. Modular Operator Design

```python
# ✅ Good
class TwoOptOperator(OperatorBase):
    """2-opt local search improvement."""
    def apply(self, solution: Solution) -> Solution:
        # Implementation
        return improved_solution

# Register as needed
operators = [TwoOptOperator(), ThreeOptOperator()]

# ❌ Avoid
# Monolithic code with all operators mixed
```

### 2. Parameter Documentation

```python
# ✅ Good
class GRASP:
    def __init__(self, instance, seed=42, alpha=0.2):
        """
        Args:
            instance: VRPTW problem instance
            seed: Random seed for reproducibility (default 42)
            alpha: Greediness parameter (0-1, default 0.2)
                   0 = fully random
                   1 = purely greedy
        """
```

## Summary

**Key Principles**:
1. ✅ Always validate data before use
2. ✅ Use seeds for reproducibility
3. ✅ Optimize for performance
4. ✅ Test thoroughly
5. ✅ Document clearly
6. ✅ Handle errors gracefully
7. ✅ Organize code modularly
8. ✅ Version your results

---

**Last Updated**: January 2, 2026  
**Status**: Best Practices Documented ✅
