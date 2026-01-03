---
title: "Phase 4 Quick Reference Guide"
type: "Developer Guide"
---

# Phase 4 Quick Reference: GRASP, VND, ILS

## 🚀 Quick Start

### Using GRASP (Simplest Algorithm)
```python
from src.metaheuristic import GRASP
from src.core import SolomonLoader

# Load instance
loader = SolomonLoader(family='C1')
instance = loader.load_instance('C101')

# Run GRASP
grasp = GRASP(alpha=0.15, max_iterations=100, seed=42, verbose=True)
solution, fitness, stats = grasp.solve(instance, time_limit=30)

# Results
print(f"Best solution: K={fitness[0]} vehicles, D={fitness[1]:.2f} distance")
print(f"Time: {stats['total_time']:.2f}s")
```

### Using ILS (Better Quality, Longer Time)
```python
from src.metaheuristic import IteratedLocalSearch

ils = IteratedLocalSearch(
    max_iterations=100,
    acceptance_criterion='better',
    seed=42,
    verbose=True
)
solution, fitness, stats = ils.solve(instance, time_limit=60)
```

### Using Hybrid (Balanced Approach)
```python
from src.metaheuristic import HybridGRASP_ILS

hybrid = HybridGRASP_ILS(
    grasp_iterations=20,
    ils_iterations=50,
    alpha=0.15,
    seed=42,
    verbose=True
)
solution, fitness, stats = hybrid.solve(instance)
```

---

## 📊 Algorithm Comparison

| Aspect | GRASP | ILS | Hybrid |
|--------|-------|-----|--------|
| **Speed** | Fast | Slow | Medium |
| **Quality** | Good | Better | Balanced |
| **Time** | 10-30s | 30-60s | 20-40s |
| **Exploration** | High | Medium | High |
| **Exploitation** | Medium | High | Medium |
| **Use Case** | Quick baseline | Best quality | Default |

---

## 🔧 Configuration

### GRASP Parameters
```python
GRASP(
    alpha=0.15,                    # RCL width (0-1)
    max_iterations=100,            # Max GRASP iterations
    max_iterations_no_improvement=20,  # Early stopping
    constructor=RandomizedInsertion(),  # Construction operator
    local_search_ops=[TwoOpt, OrOpt, Relocate, SwapCustomers],  # VND neighborhoods
    seed=None,                     # Random seed (None = random)
    verbose=False                  # Print iteration details
)
```

### ILS Parameters
```python
IteratedLocalSearch(
    grasp=GRASP(...),              # GRASP for initial solution
    perturbation_operator=RuinRecreate(),  # How to perturb
    vnd=VariableNeighborhoodDescent(),     # Local search
    acceptance_criterion='better',  # 'better' or 'probability'
    perturbation_strength=5,       # Destruction level (0-10)
    max_iterations=100,            # Max ILS iterations
    max_perturbations_no_improvement=20,   # Early stopping
    seed=None,
    verbose=False
)
```

### Hybrid Parameters
```python
HybridGRASP_ILS(
    grasp_iterations=20,           # Phase 1: GRASP iterations
    ils_iterations=50,             # Phase 2: ILS iterations
    alpha=0.15,                    # GRASP alpha
    seed=None,
    verbose=False
)
```

---

## 📈 Monitoring Execution

### Verbose Output
All algorithms support `verbose=True` for real-time progress:

```python
grasp = GRASP(verbose=True)
solution, fitness, stats = grasp.solve(instance)

# Output:
# ============================================================
#   Greedy Randomized Adaptive Search Procedure for C101
#   Alpha: 0.15, Iterations: 100, No-improvement limit: 20
# ============================================================
#   [  1] K=10, D=828.94  Best: K=10, D=828.94  Time: 0.05s
#   [  2] K=10, D=825.12  Best: K=10, D=825.12  Time: 0.09s
#   [  3] K=10, D=823.45  Best: K=10, D=823.45  Time: 0.14s
#   ...
# ============================================================
```

### Statistics Dictionary
```python
stats = {
    'total_iterations': int,           # Number of iterations run
    'total_time': float,               # Total execution time (seconds)
    'best_fitness': Tuple[int, float], # (K, D)
    'num_vehicles': int,               # K from solution
    'total_distance': float            # D from solution
}
```

### Access Iteration Log
```python
grasp = GRASP(...)
solution, fitness, stats = grasp.solve(instance)

# Each entry in grasp.iteration_log:
for entry in grasp.iteration_log:
    print(f"Iter {entry['iteration']}: "
          f"fitness={entry['fitness']}, "
          f"best={entry['best_fitness']}, "
          f"time={entry['time']:.2f}s")
```

---

## 🧪 Testing

### Run All Phase 4 Tests
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python -c "import sys; sys.path.insert(0, '.'); exec(open('scripts/test_phase4.py').read())"
```

### Run Specific Test Category
```python
import unittest
loader = unittest.TestLoader()

# GRASP tests only
suite = loader.loadTestsFromTestCase(TestGRASP)
unittest.TextTestRunner(verbosity=2).run(suite)

# ILS tests only
suite = loader.loadTestsFromTestCase(TestILS)
unittest.TextTestRunner(verbosity=2).run(suite)
```

### Run Single Test
```python
import sys
sys.path.insert(0, '.')
import unittest
loader = unittest.TestLoader()
suite = loader.loadTestsFromName('scripts.test_phase4.TestGRASP.test_grasp_solve_basic')
unittest.TextTestRunner(verbosity=2).run(suite)
```

---

## 🎯 Common Workflows

### 1. Quick Optimization (30 seconds)
```python
from src.metaheuristic import GRASP
from src.core import SolomonLoader

loader = SolomonLoader(family='C1')
instance = loader.load_instance('C101')

grasp = GRASP(alpha=0.15, max_iterations=50)
solution, fitness, stats = grasp.solve(instance, time_limit=30)
print(f"Solution: K={fitness[0]}, D={fitness[1]:.2f}")
```

### 2. Deep Optimization (2 minutes)
```python
from src.metaheuristic import IteratedLocalSearch

ils = IteratedLocalSearch(max_iterations=100, seed=42)
solution, fitness, stats = ils.solve(instance, time_limit=120)
print(f"Solution: K={fitness[0]}, D={fitness[1]:.2f}")
```

### 3. Deterministic Reproducibility
```python
# Run 1
grasp1 = GRASP(alpha=0.15, max_iterations=100, seed=123)
_, fit1, _ = grasp1.solve(instance)

# Run 2 (with same seed)
grasp2 = GRASP(alpha=0.15, max_iterations=100, seed=123)
_, fit2, _ = grasp2.solve(instance)

# fit1 == fit2 (same result)
assert fit1 == fit2
```

### 4. Parameter Sensitivity Analysis
```python
alphas = [0.05, 0.10, 0.15, 0.20, 0.25]
for alpha in alphas:
    grasp = GRASP(alpha=alpha, max_iterations=100)
    _, fitness, _ = grasp.solve(instance)
    print(f"Alpha={alpha}: K={fitness[0]}, D={fitness[1]:.2f}")
```

### 5. Benchmark Across All Solomon Instances
```python
from src.core import SolomonLoader, BKSManager

loader = SolomonLoader()
bks = BKSManager()

results = {}
for family in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
    results[family] = []
    instances = loader.load_all_instances(family)
    for instance in instances:
        grasp = GRASP(alpha=0.15, max_iterations=100)
        solution, fitness, _ = grasp.solve(instance)
        
        gap = solution.get_fitness_gap(bks.get_instance(instance.name))
        results[family].append({
            'instance': instance.name,
            'K': fitness[0],
            'D': fitness[1],
            'gap': gap
        })
```

---

## 🔍 Troubleshooting

### Problem: Slow Execution
**Solution**: Reduce iterations or use time limit:
```python
# Option 1: Fewer iterations
grasp = GRASP(max_iterations=20)

# Option 2: Time limit
_, fitness, _ = grasp.solve(instance, time_limit=10)

# Option 3: First improvement (faster VND)
from src.metaheuristic.vnd import FirstImprovementVND
vnd = FirstImprovementVND()
grasp = GRASP()
grasp.solve(instance)
```

### Problem: Not Improving After Few Iterations
**Solution**: Increase early stopping threshold:
```python
# Increase patience
grasp = GRASP(max_iterations_no_improvement=50)
```

### Problem: Different Results Every Run
**Solution**: Set a seed for reproducibility:
```python
grasp = GRASP(seed=42)  # Now deterministic
```

### Problem: Memory Issues on Large Problems
**Solution**: Use streaming or reduce VND neighborhoods:
```python
from src.metaheuristic.vnd import FirstImprovementVND

vnd = FirstImprovementVND()  # Faster, less memory
grasp = GRASP()
```

---

## 📚 Key References

### VND (Variable Neighborhood Descent)
- Default neighborhoods: TwoOpt → OrOpt → Relocate → SwapCustomers
- Each neighborhood applied in sequence
- Resets to first when improvement found
- Better than single neighborhood for escaping local optima

### ILS (Iterated Local Search)
- Perturbation breaks out of local optima
- Acceptance can be deterministic or probabilistic
- Works well with VND as local search
- Often better than pure GRASP for longer times

### GRASP (Greedy Randomized Adaptive Search)
- RCL (Restricted Candidate List) balances quality vs randomness
- Alpha parameter controls RCL width
- 0.15 recommended for VRPTW
- Simpler than ILS but good baseline

---

## 🔗 File Locations

| Component | File | Lines |
|-----------|------|-------|
| GRASP | `src/metaheuristic/grasp.py` | 250 |
| VND | `src/metaheuristic/vnd.py` | 150 |
| ILS | `src/metaheuristic/ils.py` | 380 |
| Tests | `scripts/test_phase4.py` | 650 |
| Module | `src/metaheuristic/__init__.py` | 40 |

---

## ✅ Checklist

Before running optimization:
- [ ] Python 3.9+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Solomon instance available (or use synthetic from tests)
- [ ] SolomonLoader path configured
- [ ] Seed set if reproducibility needed
- [ ] Time limit reasonable for problem size

---

## 📞 Support

For issues:
1. Check test suite: `scripts/test_phase4.py`
2. Review this guide for common workflows
3. Check phase completion summary: `PHASE_4_COMPLETION.md`
4. Check project status: `PROJECT_STATUS_COMPREHENSIVE.md`

---

**Version**: 1.0  
**Phase**: 4 Complete  
**Status**: Production Ready
