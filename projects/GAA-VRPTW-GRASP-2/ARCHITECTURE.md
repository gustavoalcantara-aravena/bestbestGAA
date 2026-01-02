# Architecture and Design

High-level overview of VRPTW-GRASP framework architecture, design patterns, and component interactions.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VRPTW-GRASP Framework                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Data Layer     │  │  Solver Layer    │  │  Analysis Layer  │  │
│  ├─────────────────┤  ├──────────────────┤  ├──────────────────┤  │
│  │ Instance        │  │ GRASP            │  │ OutputManager    │  │
│  │ Customer        │  │ VND              │  │ Statistics       │  │
│  │ Route           │  │ ILS              │  │ Visualization    │  │
│  │ Solution        │  │ Operators        │  │ Metrics          │  │
│  │ BKS Manager     │  │ Evaluator        │  │ Validation       │  │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Framework      │  │  Experiment      │  │  Algorithm Gen   │  │
│  ├─────────────────┤  ├──────────────────┤  ├──────────────────┤  │
│  │ Config          │  │ ExperimentConfig │  │ AST              │  │
│  │ Loader          │  │ ExperimentExec   │  │ Grammar          │  │
│  │ Helpers         │  │ QUICK/FULL modes │  │ Generator        │  │
│  │ Validators      │  │ CSV Export       │  │ JSON AST         │  │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Data Layer

**Purpose**: Represent and manage VRPTW problem data

**Classes**:
- `Customer`: Individual customer with location, demand, time window
- `Instance`: Full problem instance with 1 depot + N customers
- `Route`: Ordered sequence of customers served by single vehicle
- `Solution`: Collection of routes forming complete solution
- `Evaluator`: Calculates fitness (routes, distance, feasibility)

**Responsibilities**:
- Parse Solomon CSV format
- Validate constraints (capacity, time windows)
- Calculate metrics (distance, time, load)
- Check feasibility

**Dependencies**: numpy, pandas

### 2. Solver Layer

**Purpose**: Solve VRPTW using metaheuristic algorithms

**Classes**:
- `GRASP`: Greedy Randomized Adaptive Search Procedure
  - Construction phase (greedy + randomized)
  - Local search phase (improvement)
  - Iteration control

- `VariableNeighborhoodDescent (VND)`: Local search
  - Sequential neighborhood exploration
  - First-improvement strategy

- `IteratedLocalSearch (ILS)`: Perturbation + reoptimization
  - Escape local optima
  - Perturbation strength control

**Operators** (22 total):
- **Construction (6)**: Savings, NN, Christofides, etc.
- **Intra-route (4)**: 2-opt, 3-opt, OrOpt, etc.
- **Inter-route (4)**: CrossExchange, SwapRoutes, etc.
- **Perturbation (4)**: EjectionChain, DoubleMove, etc.
- **Repair (4)**: TimeWindowRepair, CapacityRepair, etc.

**Responsibilities**:
- Generate initial solutions
- Improve solutions via local search
- Manage iteration counter
- Track best solution
- Report statistics

**Dependencies**: numpy, custom operators

### 3. Analysis Layer

**Purpose**: Generate outputs, analyze results, and create visualizations

**Classes**:
- `OutputManager`: Manages directory structure, CSV export
  - Creates timestamped directories
  - Defines 6 CSV schemas
  - Handles experiment metadata

- `StatisticalAnalysisReport`: Statistical tests and analysis
  - Descriptive statistics (mean, std, median)
  - Non-parametric tests (Kruskal-Wallis, Wilcoxon)
  - Effect size (Cohen's d)
  - Convergence analysis

- `MatplotlibVisualizer`: Plot generation
  - Convergence curves
  - Boxplots
  - Heatmaps
  - Time analysis

- `ValidationSuite`: Framework validation
  - Unit tests
  - Integration tests
  - Feasibility validation
  - Output validation

**Responsibilities**:
- Organize results
- Calculate metrics
- Generate plots
- Perform statistical tests
- Validate framework

**Dependencies**: pandas, matplotlib, scipy, numpy

### 4. Framework Layer

**Purpose**: Configuration and utilities

**Classes**:
- `Config`: YAML-based configuration
- `InstanceLoader`: Load Solomon instances
- `BKSManager`: Best-known solutions management
- `Helpers`: Utility functions

**Responsibilities**:
- Read/write configuration
- Load instances from CSV
- Manage BKS comparison
- Provide helper functions

**Dependencies**: yaml, pandas, pathlib

### 5. Experiment Layer

**Purpose**: Execute and manage large-scale experiments

**Classes**:
- `ExperimentConfig`: Validate experiment configuration
  - Mode: QUICK (1 family, 12 instances) or FULL (6 families, 56 instances)
  - Families: C1, C2, R1, R2, RC1, RC2
  - Algorithms: User-defined or generated
  - Seed: Reproducibility control

- `ExperimentExecutor`: Execute experiments
  - Iterate over instances and algorithms
  - Collect results
  - Export to CSV
  - Manage directories

- `QuickExperiment` / `FullExperiment`: Static convenience classes

**Responsibilities**:
- Run experiments systematically
- Collect metrics
- Export results
- Track progress
- Ensure reproducibility

**Dependencies**: ExperimentConfig, Instance, GRASP, OutputManager

### 6. Algorithm Generation Layer

**Purpose**: Generate algorithms via GAA framework

**Classes**:
- `AST`: Abstract Syntax Tree representation
  - Nodes for operations
  - Connections for flow
  - Parameters for configuration

- `Grammar`: Grammar specification
  - Production rules
  - Valid sequences
  - Constraints

- `AlgorithmGenerator`: Generate algorithms
  - Parse grammar
  - Create valid AST
  - Serialize to JSON
  - Seed-based reproducibility

**Responsibilities**:
- Define algorithm structure
- Generate valid algorithms
- Serialize to JSON
- Support algorithm deserialization

**Dependencies**: json, random, dataclasses

## Design Patterns

### 1. Strategy Pattern

**Solvers** (GRASP, VND, ILS) implement different solving strategies

```python
class MetaheuristicBase:
    def solve(self, instance):
        raise NotImplementedError

class GRASP(MetaheuristicBase):
    def solve(self, instance):
        # GRASP implementation
        ...
```

### 2. Factory Pattern

**InstanceLoader** creates instances from various formats

```python
class InstanceLoader:
    @staticmethod
    def from_solomon_csv(path):
        # Parse and create Instance
        return Instance(...)
```

### 3. Builder Pattern

**ExperimentConfig** builds configurations step-by-step

```python
config = ExperimentConfig(
    mode='FULL',
    families=['R1', 'R2'],
    seed=42
)
```

### 4. Command Pattern

**Operators** encapsulate solution modifications

```python
class OperatorBase:
    def apply(self, solution):
        # Modify and return solution
        return modified_solution
```

### 5. Observer Pattern

**ExperimentExecutor** notifies progress updates

```python
for result in executor.run_with_progress():
    print(f"Progress: {result.instance}")
```

### 6. Decorator Pattern

**Validation** wraps core functionality

```python
def validate_solution(func):
    def wrapper(solution):
        result = func(solution)
        assert result.is_feasible()
        return result
    return wrapper
```

## Data Flow

### Experiment Execution Flow

```
Load Config
    ↓
Iterate Families
    ↓
Iterate Instances
    ↓
For Each Instance:
  - Load Instance
  - For Each Algorithm:
    - Create Solver
    - Run Solver
    - Collect Metrics
    - Save Result
    ↓
Export Results
    ↓
Statistical Analysis
    ↓
Generate Visualization
```

### Result Collection Flow

```
Experiment Runs
    ↓
ExecutionResult Objects (one per run)
    ↓
Raw Results List
    ↓
CSV Export (raw_results.csv)
    ↓
Metadata Export (experiment_metadata.json)
    ↓
Analysis
    ↓
Visualization
```

## Integration Points

### Phase Integration

| Phase | Component | Integration |
|-------|-----------|-------------|
| 2-4 | Core + GRASP | Solver layer |
| 5 | GAA | Algorithm generation |
| 6 | Dataset | Data layer (Instance) |
| 7 | Output | Analysis layer |
| 8 | Visualization | Analysis layer |
| 9 | Experiments | Experiment layer |
| 10 | Statistics | Analysis layer |
| 11 | Validation | All layers |

### External Dependencies

```
Core: numpy, pandas
Solver: (none - pure Python)
Analysis: matplotlib, scipy
Experiments: (core + solver)
Stats: scipy.stats, numpy
Validation: pytest
```

## Performance Considerations

### Optimization Strategies

1. **Caching**: Load instances once, reuse
2. **Parallel Processing**: Distribute experiments across cores
3. **Batch Operations**: Process multiple solutions together
4. **Vectorization**: Use numpy for calculations

### Memory Management

- Instances: ~1MB each (loaded on demand)
- Solutions: ~10KB each (kept in memory during search)
- Results: CSV with ~50KB per 100 experiments

### Execution Time

- Single instance solve: 1-5 seconds
- QUICK experiment: ~5-10 minutes
- FULL experiment: ~25-45 minutes

## Extension Points

### Adding New Operator

```python
from src.core.operators import OperatorBase

class MyOperator(OperatorBase):
    def apply(self, solution):
        # Implementation
        return modified_solution

# Register in GRASP
grasp.add_operator(MyOperator())
```

### Adding New Analyzer

```python
from scripts.statistical_analysis import AnalysisBase

class MyAnalysis(AnalysisBase):
    def analyze(self, results_df):
        # Implementation
        return analysis_results
```

### Adding New Visualizer

```python
class MyVisualizer:
    def plot(self, results_df):
        # Implementation
        plt.show()
```

## Quality Assurance

### Testing Strategy

- **Unit Tests**: Individual classes (Phase 2-5)
- **Integration Tests**: Component interactions (Phase 9-11)
- **Feasibility Tests**: Constraint validation (Phase 11)
- **Output Tests**: File integrity (Phase 11)

### Test Coverage

- **253 tests total**
- **100% pass rate**
- **Phases 1-11 complete**

---

**Last Updated**: January 2, 2026  
**Status**: Production Ready ✅
