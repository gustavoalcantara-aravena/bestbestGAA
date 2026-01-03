# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### Issue: "ModuleNotFoundError: No module named 'pip'"

**Solution**: Upgrade pip:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Virtual environment not activating (Windows)

**Solution**: Check execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### Issue: "Permission denied" on Linux/Mac

**Solution**: Ensure script is executable:
```bash
chmod +x .venv/bin/activate
source .venv/bin/activate
```

## Import Errors

### Issue: "ModuleNotFoundError: No module named 'src'"

**Causes**:
1. Not running from project root
2. PYTHONPATH not set correctly
3. src/ directory missing

**Solutions**:
```bash
# Verify you're in the project root
ls src/  # Should list core/, gaa/, utils/

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/GAA-VRPTW-GRASP-2"
```

### Issue: "ImportError: cannot import name 'GRASP'"

**Causes**:
1. GRASP class not found
2. Typo in import
3. src/core/grasp.py missing

**Solutions**:
```python
# ✅ Correct
from src.core.grasp import GRASP

# ❌ Wrong
from grasp import GRASP
from core.grasp import GRASP
```

## Data Loading Issues

### Issue: "FileNotFoundError: datasets/benchmark/C101.csv not found"

**Causes**:
1. CSV files not downloaded
2. Wrong path
3. Wrong working directory

**Solutions**:
```bash
# Check if files exist
ls datasets/benchmark/ | head

# Download from https://solomon.rutgers.edu/
# Place in datasets/benchmark/

# Or download programmatically (if available)
```

### Issue: "ValueError: Instance invalid"

**Causes**:
1. Wrong CSV format
2. Missing columns
3. Invalid numeric values

**Solutions**:
```python
# Check CSV format
import pandas as pd
df = pd.read_csv("instance.csv")
print(df.head())
print(df.columns)  # Should have 7 columns

# Expected columns:
# CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
```

### Issue: "pandas.errors.ParserError: Error tokenizing data"

**Causes**:
1. Wrong delimiter (not comma)
2. Extra spaces in data
3. Mixed line endings

**Solutions**:
```python
# Try different delimiter
df = pd.read_csv("instance.csv", delim_whitespace=True)

# Or clean the file first
df = pd.read_csv("instance.csv", skipinitialspace=True)
```

## Solver Issues

### Issue: "ValueError: Solution is infeasible"

**Causes**:
1. Demand exceeds capacity
2. Time window violated
3. Algorithm bug

**Solutions**:
```python
# Check solution feasibility
if solution.is_feasible():
    print("OK")
else:
    # Diagnose
    for route in solution.routes:
        print(f"Load: {route.load}")
        print(f"Capacity: {route.capacity}")
```

### Issue: GRASP is too slow

**Causes**:
1. Too many iterations
2. Large instance (C2, R2)
3. Computer load

**Solutions**:
```python
# Reduce iterations
grasp = GRASP(instance, max_iterations=50)
solution = grasp.solve()

# Or use time limit
grasp = GRASP(instance, max_runtime=30)  # 30 seconds
solution = grasp.solve()
```

### Issue: Solution quality is poor

**Causes**:
1. Too few iterations
2. Unlucky random seed
3. Weak initial solution

**Solutions**:
```python
# Increase iterations
grasp = GRASP(instance, max_iterations=200)

# Try different seed
for seed in [1, 42, 100]:
    grasp = GRASP(instance, seed=seed)
    solution = grasp.solve()
    # Pick best

# Use ILS
ils = GRASP_ILS(instance)
solution = ils.solve()  # Usually better
```

## Experiment Issues

### Issue: "KeyError: 'C101'" in experiment

**Causes**:
1. Instance file missing
2. Instance name not in mapping
3. BKS file missing

**Solutions**:
```python
# Check available instances
from src.utils.loader import get_solomon_instances
instances = get_solomon_instances()
print(instances.keys())

# Verify BKS file
import json
with open('best_known_solutions.json') as f:
    bks = json.load(f)
    if 'C101' not in bks:
        print("C101 missing from BKS")
```

### Issue: Experiment takes too long

**Causes**:
1. FULL mode (168 experiments)
2. Too many iterations
3. Large instances

**Solutions**:
```python
# Use QUICK mode first
config = ExperimentConfig(mode='QUICK', families=['R1'])
executor = ExperimentExecutor(config)
executor.run()  # 12 instances instead of 56

# Reduce iterations
config = ExperimentConfig(mode='FULL', max_iterations=50)
```

### Issue: "MemoryError" during experiment

**Causes**:
1. Too many results in memory
2. Large CSV file
3. Memory leak

**Solutions**:
```python
# Use smaller experiment
config = ExperimentConfig(mode='QUICK')

# Or process results in batches
for batch in executor.run_batch(batch_size=5):
    process_batch(batch)
    # Clear memory
```

## Output Issues

### Issue: CSV file is empty

**Causes**:
1. No results saved
2. Wrong file path
3. Experiment didn't complete

**Solutions**:
```python
# Check if results exist
import os
results_path = executor.results_csv
if os.path.exists(results_path):
    df = pd.read_csv(results_path)
    print(f"Rows: {len(df)}")
else:
    print("Results file not found")
```

### Issue: Plots are not generated

**Causes**:
1. Missing matplotlib
2. No X display (headless)
3. Wrong save path

**Solutions**:
```bash
# Ensure matplotlib installed
pip install matplotlib

# Force headless mode
# Already done in framework (Agg backend)

# Check save path
import os
os.makedirs("output/plots", exist_ok=True)
visualizer.save_all("output/plots")
```

### Issue: "No such file or directory" when saving

**Causes**:
1. Directory doesn't exist
2. No write permissions
3. Path too long

**Solutions**:
```python
from pathlib import Path

# Create directory if needed
output_dir = Path("output/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# Use Path for safe operations
save_path = output_dir / "convergence.png"
visualizer.save(save_path)
```

## Analysis Issues

### Issue: "ValueError" in statistical analysis

**Causes**:
1. Insufficient data
2. All values identical
3. NaN or infinite values

**Solutions**:
```python
# Check data quality
results_df = pd.read_csv(csv_path)
print(results_df.describe())
print(results_df.isnull().sum())

# Remove problematic rows
results_df = results_df.dropna()
```

### Issue: "ZeroDivisionError" in metrics

**Causes**:
1. D_BKS is zero
2. All solutions have same distance
3. Division by standard deviation

**Solutions**:
```python
# Check BKS values
with open('best_known_solutions.json') as f:
    bks = json.load(f)
    for k, v in bks.items():
        if v['D_BKS'] == 0:
            print(f"{k}: D_BKS is zero!")
```

## Performance Issues

### Issue: Tests are failing

**Solution**:
```bash
# Run tests with verbose output
pytest -v --tb=short

# Run specific test
pytest scripts/test_phase11.py::TestValidationResult -v

# See full error
pytest -v --tb=long
```

### Issue: Code is running out of memory

**Solutions**:
1. Use smaller experiments
2. Process in batches
3. Clear temporary data

```python
# Monitor memory usage
import psutil
memory = psutil.virtual_memory()
print(f"Available: {memory.available / 1e9:.2f} GB")
```

## System-Specific Issues

### Windows PowerShell

**Issue**: Execution policy blocks scripts

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux

**Issue**: Permission denied

**Solution**:
```bash
chmod +x scripts/*.py
```

### macOS

**Issue**: "Python not found"

**Solution**:
```bash
# Use python3 explicitly
python3 -m venv .venv
source .venv/bin/activate
```

## Getting More Help

### 1. Check Error Message Carefully

Look at the full error traceback:
```
Traceback (most recent call last):
  File "...", line X, in function()
    problematic_code()
  ...
ErrorType: error message
```

The last line shows the actual error.

### 2. Search Documentation

- [USAGE.md](USAGE.md) - How to use framework
- [API_REFERENCE.md](API_REFERENCE.md) - Class documentation
- [FAQ.md](FAQ.md) - Common questions
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - Design guidelines

### 3. Run Minimal Example

```python
from src.core.instance import Instance
from src.core.grasp import GRASP

# Minimal test
instance = Instance.from_solomon_csv("datasets/benchmark/C101.csv")
grasp = GRASP(instance, seed=42)
solution = grasp.solve()
print(f"Routes: {solution.num_routes}")
```

### 4. Enable Debug Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now operations print debug information
```

---

**Last Updated**: January 2, 2026  
**Status**: Comprehensive Guide ✅
