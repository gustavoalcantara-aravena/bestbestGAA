# Output Directory Structure Documentation

## Overview

The GRASP-GAA-VRPTW project now generates organized output with timestamped directories and structured logging.

## Directory Hierarchy

```
output/
├── Canary_RUN_2026-01-04_01-49-42/
│   ├── logs/
│   │   ├── algorithm_00.json      (Construction AST for algorithm 0)
│   │   ├── algorithm_01.json      (Construction AST for algorithm 1)
│   │   ├── algorithm_02.json      (Construction AST for algorithm 2)
│   │   ├── algorithm_03.json      (Construction AST for algorithm 3)
│   │   └── algorithm_04.json      (Construction AST for algorithm 4)
│   ├── visualizations/            (For future chart outputs)
│   └── canary_results.json        (5 solutions, feasibility info)
│
├── FULL_EXPERIMENT_RUN_2026-01-04_HH-MM-SS/  (When full_experiment.py runs)
│   ├── logs/
│   │   ├── algorithm_00.json      (AST for each of 10 algorithms)
│   │   ├── algorithm_01.json
│   │   ├── ...
│   │   └── algorithm_09.json
│   ├── visualizations/            (Generated charts: gap analysis, comparisons)
│   └── experiment_results.json    (560 solutions across all instances)
│
└── canary_run/                    (Legacy: kept for backward compatibility)
```

## File Contents

### Algorithm Logs (logs/algorithm_*.json)

Each algorithm log contains the complete AST structure generated for that algorithm:

```json
{
  "algorithm_id": 0,
  "construction_ast": {
    "type": "WeightedSum",
    "terms": [
      {
        "weight": -4.799147503114012,
        "expr": { ... AST structure ... }
      }
    ]
  },
  "ls_operator_ast": {
    "type": "Choose",
    "options": [...]
  }
}
```

**Contains:**
- Algorithm ID (0-9 or 0-4 for canary)
- Complete construction phase AST (heuristic)
- Complete local search operator AST (VND operators)

### Results Files (canary_results.json / experiment_results.json)

JSON array of solution objects:

```json
[
  {
    "routes": [
      [0, 5, 3, 8, 9, 6, 4, 0],
      [0, 20, 24, 25, 27, 30, 28, 26, 23, 0],
      ...
    ],
    "total_distance": 1870.22,
    "total_vehicles": 15,
    "feasible": true,
    "instance": "C101",
    "algorithm_id": 0,
    "run": 0
  },
  ...
]
```

**Contains:**
- Complete vehicle routes
- Objective metrics (distance, vehicles)
- Feasibility status
- Instance and algorithm metadata
- Run number

## Timestamp Format

Format: `YYYY-MM-DD_HH-MM-SS`

Examples:
- `Canary_RUN_2026-01-04_01-49-42`
- `FULL_EXPERIMENT_RUN_2026-01-04_01-50-15`

## Usage

### Running Canary Test
```bash
python canary_run.py
# Output: output/Canary_RUN_{timestamp}/
```

Creates:
- 5 algorithms × 1 run = 5 solutions
- AST logs for all 5 algorithms
- Results JSON with solution details

### Running Full Experiment
```bash
python full_experiment.py
# Output: output/FULL_EXPERIMENT_RUN_{timestamp}/
```

Creates:
- 10 algorithms × 56 instances × 1 run = 560 solutions
- AST logs for all 10 algorithms
- Results JSON with all 560 solution details
- Visualizations subdirectory ready for charts

## Integration Points

### Visualization Modules

All visualization generators should read from:
- `results_file`: `{timestamp_dir}/canary_results.json` or `experiment_results.json`
- `logs_dir`: `{timestamp_dir}/logs/`
- `output_dir`: `{timestamp_dir}/visualizations/`

Example:
```python
from pathlib import Path

# Read latest results
results_dir = Path("output").glob("Canary_RUN_*")[0]
results_file = results_dir / "canary_results.json"
logs_dir = results_dir / "logs"
vis_dir = results_dir / "visualizations"
```

### AST Access

Algorithm ASTs are stored in JSON format, easily parsed:

```python
import json

alg_log = Path("output/Canary_RUN_2026-01-04_01-49-42/logs/algorithm_00.json")
with open(alg_log) as f:
    alg_data = json.load(f)
    construction_ast = alg_data["construction_ast"]
    ls_ast = alg_data["ls_operator_ast"]
```

## Benefits

1. **Traceability**: Each run has unique timestamp, impossible to overwrite
2. **Organized**: Logs, visualizations, and results separated by directory
3. **Reproducibility**: ASTs stored with results for future analysis
4. **Scalability**: Supports both quick (canary) and long (full) experiments
5. **Parallel-safe**: Multiple runs can execute simultaneously without conflicts

## Next Steps

1. Update visualization generators to read from timestamped directories
2. Generate gap analysis charts in visualizations/ subdirectory
3. Generate algorithm comparison charts
4. Run full_experiment.py for complete 560-run dataset
5. Generate comprehensive reports for thesis/publication
