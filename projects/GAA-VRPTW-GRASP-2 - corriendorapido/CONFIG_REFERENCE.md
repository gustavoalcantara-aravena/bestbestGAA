# Configuration Reference

Complete guide to all configuration options.

## Overview

Configuration is managed via `config.yaml` file in the project root. This file controls solver behavior, dataset loading, and output generation.

## config.yaml Structure

```yaml
solver:
  name: string              # Solver type: "GRASP" or "GRASP-ILS"
  seed: integer             # Random seed (0-2^31-1)
  max_iterations: integer   # Maximum iterations
  max_runtime: integer      # Maximum runtime in seconds
  alpha: float              # Greediness parameter (0.0-1.0)

dataset:
  name: string              # Dataset type: "Solomon" or custom
  instances_dir: path       # Directory with instance CSV files
  format: string            # Format: "csv" or "json"

output:
  directory: path           # Output directory
  timestamp_format: string  # Timestamp format
  csv_schemas: integer      # Number of CSV schemas (typically 6)
  plots_enabled: bool       # Generate plots (true/false)

experiment:
  mode: string              # "QUICK" (12 instances) or "FULL" (56 instances)
  families: list            # Instance families to use
  algorithms: list          # Algorithm names
  max_experiments: integer  # Maximum experiments
```

## Solver Configuration

### solver.name

**Type**: string  
**Default**: "GRASP"  
**Valid**: "GRASP", "GRASP-ILS"

Selects the solver:
- `GRASP`: Greedy Randomized Adaptive Search Procedure
- `GRASP-ILS`: GRASP with Iterated Local Search

```yaml
solver:
  name: "GRASP"  # Basic GRASP
  # or
  name: "GRASP-ILS"  # With ILS perturbation
```

### solver.seed

**Type**: integer  
**Default**: 42  
**Range**: 0 to 2,147,483,647

Controls random number generation. Same seed produces same results:

```yaml
solver:
  seed: 42   # Reproducible results
  seed: 1    # Different but still reproducible
  seed: 100  # Another seed
```

**Impact**: All random operations (construction, local search, perturbation)

### solver.max_iterations

**Type**: integer  
**Default**: 100  
**Range**: 1 to 100,000

Maximum number of algorithm iterations:

```yaml
solver:
  max_iterations: 50     # Fast, lower quality
  max_iterations: 100    # Balanced
  max_iterations: 500    # Slow, higher quality
```

**Trade-off**: More iterations = better quality but slower

### solver.max_runtime

**Type**: integer (seconds)  
**Default**: 300  
**Range**: 1 to 3,600

Alternative termination criterion:

```yaml
solver:
  max_runtime: 60   # 1 minute
  max_runtime: 300  # 5 minutes (default)
  max_runtime: 1800 # 30 minutes
```

**Note**: Algorithm terminates when either max_iterations or max_runtime is reached, whichever comes first.

### solver.alpha

**Type**: float  
**Default**: 0.2  
**Range**: 0.0 to 1.0

Greediness parameter in GRASP construction phase:

```yaml
solver:
  alpha: 0.0   # Pure random construction
  alpha: 0.2   # 20% greedy, 80% random (balanced)
  alpha: 0.5   # 50% greedy, 50% random
  alpha: 1.0   # Pure greedy (deterministic)
```

**Effect**: Lower alpha = more randomness = more exploration

## Dataset Configuration

### dataset.name

**Type**: string  
**Default**: "Solomon"  
**Valid**: "Solomon", "Custom"

Specifies the benchmark set:

```yaml
dataset:
  name: "Solomon"  # Standard benchmark (56 instances)
  name: "Custom"   # Custom instances
```

### dataset.instances_dir

**Type**: path  
**Default**: "datasets/benchmark"

Directory containing instance CSV files:

```yaml
dataset:
  instances_dir: "datasets/benchmark"  # Standard location
  instances_dir: "/path/to/custom"     # Custom location
```

**Expected**: CSV files named `C101.csv`, `R101.csv`, etc.

### dataset.format

**Type**: string  
**Default**: "csv"  
**Valid**: "csv", "json"

Instance file format:

```yaml
dataset:
  format: "csv"   # Comma-separated values (standard)
  format: "json"  # JSON format (if supported)
```

**CSV Format** (7 columns):
```
CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
```

## Output Configuration

### output.directory

**Type**: path  
**Default**: "output"

Root directory for all output files:

```yaml
output:
  directory: "output"          # Local directory
  directory: "/tmp/vrptw"      # Absolute path
  directory: "./results/2026"  # Relative path
```

**Behavior**: Creates subdirectories with timestamp format

### output.timestamp_format

**Type**: string  
**Default**: "DD-MM-YY_HH-MM-SS"

Format for timestamped output directories:

```yaml
output:
  timestamp_format: "DD-MM-YY_HH-MM-SS"  # 01-02-26_14-30-45
  timestamp_format: "YYYY-MM-DD_HH:MM"   # 2026-01-02_14:30
  timestamp_format: "ISO"                 # 2026-01-02T14:30:45
```

**Ensures**: Different runs have different output directories

### output.csv_schemas

**Type**: integer  
**Default**: 6

Number of CSV output schemas. Standard = 6:
1. raw_results.csv - All experiment results
2. convergence_trace.csv - Per-instance convergence
3. algorithm_summary.csv - Algorithm statistics
4. family_summary.csv - Family statistics
5. metrics_summary.csv - Overall metrics
6. experiment_metadata.json - Experiment configuration

```yaml
output:
  csv_schemas: 6  # Standard (all files)
```

### output.plots_enabled

**Type**: boolean  
**Default**: true

Enable/disable plot generation:

```yaml
output:
  plots_enabled: true   # Generate plots
  plots_enabled: false  # Skip plotting (faster)
```

**Plots Generated** (if enabled):
- Convergence curves
- Boxplots (K and D)
- Heatmaps
- Time analysis
- Distribution plots

## Experiment Configuration

### experiment.mode

**Type**: string  
**Default**: "QUICK"  
**Valid**: "QUICK", "FULL"

Experiment scope:

```yaml
experiment:
  mode: "QUICK"  # 1 family, 12 instances → 36 experiments
  mode: "FULL"   # 6 families, 56 instances → 168 experiments
```

| Mode | Families | Instances | Experiments | Time |
|------|----------|-----------|-------------|------|
| QUICK | 1 | 12 | 36 | ~5 min |
| FULL | 6 | 56 | 168 | ~30 min |

### experiment.families

**Type**: list of strings  
**Default**: depends on mode

Instance families to test:

```yaml
experiment:
  families:
    - "C1"   # Clustered, small
    - "C2"   # Clustered, large
    - "R1"   # Random, small
    - "R2"   # Random, large
    - "RC1"  # Mixed, small
    - "RC2"  # Mixed, large
```

**Typical selections**:
```yaml
# QUICK: single family
mode: "QUICK"
families:
  - "R1"

# FULL: all families
mode: "FULL"
families:
  - "C1"
  - "C2"
  - "R1"
  - "R2"
  - "RC1"
  - "RC2"

# Custom: subset
families:
  - "R1"
  - "R2"
```

### experiment.algorithms

**Type**: list of strings  
**Default**: Generated algorithms

Algorithm names to test:

```yaml
experiment:
  algorithms:
    - "GAA_Algorithm_1"
    - "GAA_Algorithm_2"
    - "GAA_Algorithm_3"
```

### experiment.max_experiments

**Type**: integer  
**Default**: unlimited

Maximum experiments to run (useful for testing):

```yaml
experiment:
  max_experiments: 10   # Stop after 10 experiments
  max_experiments: null # Run all
```

## Example Configurations

### Fast Testing

```yaml
solver:
  name: "GRASP"
  seed: 42
  max_iterations: 25
  max_runtime: 60
  alpha: 0.2

dataset:
  name: "Solomon"
  instances_dir: "datasets/benchmark"
  format: "csv"

output:
  directory: "output"
  plots_enabled: false

experiment:
  mode: "QUICK"
  families:
    - "R1"
```

### Production Run

```yaml
solver:
  name: "GRASP-ILS"
  seed: 42
  max_iterations: 100
  max_runtime: 300
  alpha: 0.2

dataset:
  name: "Solomon"
  instances_dir: "datasets/benchmark"
  format: "csv"

output:
  directory: "output"
  plots_enabled: true
  csv_schemas: 6

experiment:
  mode: "FULL"
  families:
    - "C1"
    - "C2"
    - "R1"
    - "R2"
    - "RC1"
    - "RC2"
```

### High-Quality Run

```yaml
solver:
  name: "GRASP-ILS"
  seed: 42
  max_iterations: 500
  max_runtime: 900
  alpha: 0.15

dataset:
  name: "Solomon"
  instances_dir: "datasets/benchmark"
  format: "csv"

output:
  directory: "output/hq_run"
  plots_enabled: true

experiment:
  mode: "FULL"
  families:
    - "C1"
    - "C2"
    - "R1"
    - "R2"
    - "RC1"
    - "RC2"
```

## Loading Configuration in Code

```python
import yaml
from src.experiments import ExperimentConfig

# Load YAML
with open('config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)

# Create config from dict
exp_config = ExperimentConfig(**config_dict['experiment'])

# Use in experiment
executor = ExperimentExecutor(exp_config)
executor.run()
```

## Environment Variables

Configuration can be overridden via environment variables:

```bash
# Windows
set VRPTW_SEED=100
set VRPTW_MODE=FULL

# Linux/Mac
export VRPTW_SEED=100
export VRPTW_MODE=FULL
```

## Performance Tuning

### For Speed

```yaml
solver:
  max_iterations: 25      # Fewer iterations
  max_runtime: 30         # Shorter time limit
  alpha: 1.0              # Deterministic construction
```

### For Quality

```yaml
solver:
  max_iterations: 200     # More iterations
  max_runtime: 600        # Longer time limit
  alpha: 0.1              # More randomness
```

### For Memory

```yaml
experiment:
  max_experiments: 50  # Limit experiments
output:
  plots_enabled: false  # Skip plots
```

## Common Issues

### Issue: "Config file not found"

**Solution**: Ensure config.yaml is in project root:
```bash
ls config.yaml  # Should exist
```

### Issue: "Invalid YAML syntax"

**Solution**: Check indentation (YAML is whitespace-sensitive):
```yaml
solver:
  name: "GRASP"    # 2 spaces indentation
  seed: 42         # Same indentation as name
```

### Issue: "Unknown configuration option"

**Solution**: Check this reference for valid options

---

**Last Updated**: January 2, 2026  
**Status**: Complete Reference ✅
