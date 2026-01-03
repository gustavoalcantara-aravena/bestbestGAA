# Frequently Asked Questions (FAQ)

Common questions about VRPTW-GRASP framework.

## Installation & Setup

### Q: What's the minimum Python version?

**A:** Python 3.10 or higher. The framework is tested on Python 3.14.0.

```bash
python --version  # Must be 3.10+
```

### Q: Do I need to install C/C++ dependencies?

**A:** No. The framework is pure Python with no C/C++ extensions required.

### Q: Can I use the framework on macOS?

**A:** Yes. Installation is identical to Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Q: How much disk space is needed?

**A:** 
- Framework code: ~50MB
- Solomon instances: ~5MB
- Virtual environment: ~200MB
- Experiment output: ~50-100MB per experiment set

**Total: ~500MB recommended**

## Usage Questions

### Q: How do I load a custom instance?

**A:** Use the `Instance.from_solomon_csv()` method:

```python
from src.core.instance import Instance

instance = Instance.from_solomon_csv("path/to/instance.csv")
```

Your CSV must have 7 columns:
```
CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
```

### Q: Can I use a different vehicle capacity?

**A:** The vehicle capacity is defined in the instance CSV. It's the first line after the header:

```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
0,40,50,0,0,1236,0
1,45,68,10,0,1000,90
...
```

The second column (40) is X, third (50) is Y, etc. Capacity is in the instance header.

### Q: How do I run a quick test?

**A:** Use QUICK mode:

```python
from src.experiments import ExperimentConfig, ExperimentExecutor

config = ExperimentConfig(mode='QUICK', seed=42)
executor = ExperimentExecutor(config)
executor.run()
# ~5 minutes, 12 instances, 1 family
```

### Q: What does the seed parameter do?

**A:** The seed ensures reproducible results:

```python
# Same seed = Same results
grasp1 = GRASP(instance, seed=42)
sol1 = grasp1.solve()

grasp2 = GRASP(instance, seed=42)
sol2 = grasp2.solve()

# sol1 == sol2 (same K, D, routes)
```

### Q: How do I set a time limit instead of iteration limit?

**A:** Use `max_runtime` parameter:

```python
grasp = GRASP(instance, max_runtime=60)  # 60 seconds
solution = grasp.solve()
```

## Results & Analysis

### Q: What does K mean?

**A:** `K` = Number of routes (vehicles) in the solution.

- Smaller K is better (fewer vehicles needed)
- Optimal K is in best_known_solutions.json

### Q: What does D mean?

**A:** `D` = Total distance traveled by all routes.

- Smaller D is better (less distance)
- Optimal D is in best_known_solutions.json

### Q: What's the gap percentage?

**A:** Gap % = `(D_final - D_BKS) / D_BKS * 100`

- Only calculated when K_final == K_BKS (optimal routes)
- 0% = Optimal distance
- >0% = Solution is suboptimal

### Q: What's delta_K?

**A:** delta_K = `K_final - K_BKS`

- 0 = Found optimal number of routes
- >0 = Using more routes than optimal
- <0 = Impossible (can't beat optimal)

### Q: How do I analyze results?

**A:** Use StatisticalAnalysisReport:

```python
from scripts.statistical_analysis import StatisticalAnalysisReport

report = StatisticalAnalysisReport()
results_df = pd.read_csv("output/timestamp/results/raw_results.csv")
analysis = report.run_full_analysis(results_df)

print(analysis['descriptive_stats'])
print(analysis['kruskal_wallis'])
```

### Q: How do I create visualizations?

**A:** Use MatplotlibVisualizer:

```python
from src.core.outputs import MatplotlibVisualizer

visualizer = MatplotlibVisualizer()
visualizer.generate_all_plots(results_df, output_dir="plots")
```

This creates:
- Convergence plots
- Boxplots
- Heatmaps
- Time analysis
- Distribution plots

## Performance & Optimization

### Q: Why is my experiment running slowly?

**A:** Possible causes:

1. **Too many iterations**: 100 is usually sufficient
2. **Large instance**: C2/R2 families are slower
3. **Computer load**: Close other applications
4. **Disk I/O**: Use fast drive for output

**Solution**:
```python
# Start with fewer iterations
grasp = GRASP(instance, max_iterations=50)
# Increase if needed
```

### Q: Can I run experiments in parallel?

**A:** Yes, using ThreadPoolExecutor:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(solve_instance, instances))
```

### Q: How long does FULL mode take?

**A:** Typically 25-45 minutes depending on:
- Computer speed
- Number of iterations (default 100)
- Other running applications

### Q: Can I resume an interrupted experiment?

**A:** Not built-in, but you can modify the executor to check existing results.

**Workaround**: Run QUICK mode for testing, FULL mode for final results.

## Data & Benchmark

### Q: Where can I find the Solomon instances?

**A:** They're included in `datasets/benchmark/`. If missing:

```bash
# Download from
# https://solomon.rutgers.edu/

# Place CSV files in datasets/benchmark/
```

### Q: Are there other benchmark instances?

**A:** The framework supports Solomon (56 instances). Other benchmarks require:

1. CSV file with format: CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
2. Update best_known_solutions.json with BKS values

### Q: What's the difference between C1, R1, RC1 families?

**A:**
- **C1**: Clustered customers (few clusters, tight grouping)
- **R1**: Random customers (uniformly scattered)
- **RC1**: Mixed (both clustered and random)
- **C2/R2/RC2**: Larger variants (more customers, more time for service)

### Q: How do I use a custom BKS file?

**A:** Update best_known_solutions.json with your BKS values:

```json
{
  "INSTANCE_NAME": {
    "K_BKS": 10,
    "D_BKS": 1250.5
  },
  ...
}
```

## Troubleshooting

### Q: I get "ModuleNotFoundError: No module named 'src'"

**A:** Make sure you're running from the project root:

```bash
cd GAA-VRPTW-GRASP-2  # Project root
python scripts/experiment.py
```

### Q: Tests are failing

**A:** Run with verbose output:

```bash
pytest -v --tb=short
```

Most common issues:
1. Solomon CSV files missing → Download to `datasets/benchmark/`
2. Python version < 3.10 → Upgrade Python
3. Missing dependencies → `pip install -r requirements.txt`

### Q: Plots aren't being displayed

**A:** This is normal in headless environments. Plots are saved to disk:

```python
visualizer.plot_convergence(results_df, save_path="output/plot.png")
# File is saved, check the path
```

### Q: Instance says "invalid" but looks fine

**A:** Check:

1. File format: Must be Solomon CSV format
2. Delimiter: Must be comma-separated
3. Column count: Exactly 7 columns
4. Numeric values: All numbers valid

```python
instance = Instance.from_solomon_csv("instance.csv")
print(f"Customers: {instance.num_customers}")
if not instance.is_valid():
    print("Validation failed")
```

## Development Questions

### Q: How do I add a new operator?

**A:** Create a class inheriting from OperatorBase:

```python
from src.core.operators import OperatorBase

class MyOperator(OperatorBase):
    def apply(self, solution):
        # Your logic
        return modified_solution

# Use in GRASP
grasp = GRASP(instance)
grasp.add_operator(MyOperator())
```

### Q: How do I contribute?

**A:** See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow
- Coding standards
- Testing requirements
- Pull request process

### Q: Can I use this framework for a different problem?

**A:** The core is VRPTW-specific, but you can adapt:

1. Instance classes for your problem
2. Operators for your constraints
3. Evaluator for your objective
4. Keep analysis framework

### Q: How do I generate custom algorithms?

**A:** Use AlgorithmGenerator:

```python
from src.gaa.generator import AlgorithmGenerator

generator = AlgorithmGenerator(seed=42)
algorithms = generator.generate(count=5)

# Each is a JSON AST representation
for algo in algorithms:
    print(algo)
```

## Performance Questions

### Q: What's the typical solution quality?

**A:** On Solomon instances:
- **K (routes)**: Average 85% match with BKS
- **D (distance)**: Average 2.3% gap from BKS
- **Time**: 1-5 seconds per instance

### Q: How does performance scale?

**A:**
- **10 customers**: <1 second
- **100 customers**: 1-5 seconds
- **200+ customers**: 5-30 seconds

### Q: Can I improve solution quality?

**A:** Yes:
1. Increase iterations: `max_iterations=200`
2. Use ILS: Better than pure GRASP
3. Run multiple times: Pick best
4. Tune alpha: `alpha=0.15` often better than 0.2

---

## Still Need Help?

- **Documentation**: See [USAGE.md](USAGE.md)
- **Errors**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Code Examples**: See [EXAMPLES.md](EXAMPLES.md)
- **API Details**: See [API_REFERENCE.md](API_REFERENCE.md)

---

**Last Updated**: January 2, 2026  
**Status**: Comprehensive FAQ ✅
