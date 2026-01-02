# API Reference

Complete API documentation for VRPTW-GRASP framework classes and methods.

## Core Classes

### Instance

Represents a VRPTW problem instance.

```python
class Instance:
    """Vehicle Routing Problem with Time Windows instance."""
    
    # Constructor
    def __init__(self, customers: List[Customer], depot: Customer)
    
    # Class Methods
    @classmethod
    def from_solomon_csv(cls, filepath: str) -> 'Instance'
        """Load instance from Solomon CSV format."""
    
    # Properties
    @property
    def num_customers(self) -> int
        """Number of customers (excluding depot)."""
    
    @property
    def vehicle_capacity(self) -> float
        """Vehicle carrying capacity."""
    
    @property
    def customers(self) -> List[Customer]
        """List of all customers."""
    
    @property
    def depot(self) -> Customer
        """Depot customer."""
    
    # Methods
    def is_valid(self) -> bool
        """Check if instance is valid."""
    
    def get_distance(self, i: int, j: int) -> float
        """Euclidean distance between customers i and j."""
    
    def get_time_window(self, customer_id: int) -> Tuple[float, float]
        """Get time window (ready_time, due_time) for customer."""
```

### Customer

Represents a customer in the problem.

```python
class Customer:
    """Customer with location, demand, and time window."""
    
    def __init__(self,
                 customer_id: int,
                 x: float,
                 y: float,
                 demand: float,
                 ready_time: float,
                 due_time: float,
                 service_time: float)
    
    # Properties
    x: float                # X coordinate
    y: float                # Y coordinate
    demand: float           # Demand quantity
    ready_time: float       # Ready time (earliest arrival)
    due_time: float         # Due time (latest arrival)
    service_time: float     # Service duration
```

### Route

Represents a single vehicle route.

```python
class Route:
    """Single route (vehicle) serving customers."""
    
    def __init__(self, depot: Customer, capacity: float)
    
    # Methods
    def add_customer(self, customer: Customer) -> bool
        """Add customer to end of route. Returns True if successful."""
    
    def insert_customer(self, customer: Customer, position: int) -> bool
        """Insert customer at specific position."""
    
    def remove_customer(self, position: int) -> Customer
        """Remove and return customer at position."""
    
    def is_feasible(self) -> bool
        """Check capacity and time window constraints."""
    
    def calculate_distance(self) -> float
        """Total distance of route."""
    
    def calculate_time(self) -> float
        """Total time of route."""
    
    # Properties
    @property
    def customers(self) -> List[Customer]
        """Customers in route (excluding depot)."""
    
    @property
    def load(self) -> float
        """Total load on route."""
    
    @property
    def distance(self) -> float
        """Total distance of route."""
    
    @property
    def time(self) -> float
        """Total time of route."""
```

### Solution

Represents a complete solution (all routes).

```python
class Solution:
    """Complete solution with multiple routes."""
    
    def __init__(self, instance: Instance)
    
    # Methods
    def add_route(self, route: Route) -> None
        """Add route to solution."""
    
    def is_feasible(self) -> bool
        """Check if all constraints are satisfied."""
    
    def calculate_metrics(self) -> Dict
        """Calculate K, D, time, etc."""
    
    def copy(self) -> 'Solution'
        """Create deep copy of solution."""
    
    def to_dict(self) -> Dict
        """Convert to dictionary."""
    
    # Properties
    @property
    def routes(self) -> List[Route]
        """List of all routes."""
    
    @property
    def num_routes(self) -> int
        """Number of routes (K)."""
    
    @property
    def total_distance(self) -> float
        """Total distance (D)."""
    
    @property
    def total_time(self) -> float
        """Total time."""
    
    @property
    def visited_customers(self) -> Set[int]
        """Set of visited customer IDs."""
    
    @property
    def unvisited_customers(self) -> Set[int]
        """Set of unvisited customer IDs."""
```

## Solver Classes

### GRASP

Greedy Randomized Adaptive Search Procedure.

```python
class GRASP:
    """GRASP metaheuristic solver."""
    
    def __init__(self,
                 instance: Instance,
                 seed: int = 42,
                 alpha: float = 0.2,
                 max_iterations: int = 100,
                 max_runtime: int = 300):
        """
        Args:
            instance: VRPTW instance
            seed: Random seed for reproducibility
            alpha: Greediness parameter (0-1)
            max_iterations: Maximum iterations
            max_runtime: Maximum runtime in seconds
        """
    
    # Methods
    def solve(self) -> Solution
        """Solve instance using GRASP."""
    
    def add_operator(self, operator: 'Operator') -> None
        """Add custom operator."""
    
    # Properties
    @property
    def best_solution(self) -> Solution
        """Best solution found."""
    
    @property
    def best_distance(self) -> float
        """Distance of best solution."""
    
    @property
    def num_iterations(self) -> int
        """Number of iterations completed."""
```

### VND

Variable Neighborhood Descent.

```python
class VariableNeighborhoodDescent:
    """VND local search."""
    
    def __init__(self, instance: Instance)
    
    # Methods
    def search(self, solution: Solution) -> Solution
        """Improve solution using VND."""
```

### ILS

Iterated Local Search.

```python
class IteratedLocalSearch:
    """ILS perturbation framework."""
    
    def __init__(self, instance: Instance, base_search: 'LocalSearch')
    
    # Methods
    def search(self, solution: Solution) -> Solution
        """Improve solution using ILS."""
```

## Experiment Classes

### ExperimentConfig

Configuration for experiments.

```python
@dataclass
class ExperimentConfig:
    """Experiment configuration."""
    
    mode: str                    # 'QUICK' or 'FULL'
    families: List[str]          # Families to test
    algorithms: List[str]        # Algorithm names
    seed: int = 42               # Random seed
    
    # Methods
    def validate(self) -> bool
        """Validate configuration."""
```

### ExperimentExecutor

Execute experiments.

```python
class ExperimentExecutor:
    """Execute experiments systematically."""
    
    def __init__(self, config: ExperimentConfig)
    
    # Methods
    def run(self) -> None
        """Execute all experiments."""
    
    def add_result(self, result: 'ExecutionResult') -> None
        """Add experiment result."""
    
    def save_raw_results(self) -> str
        """Save results to CSV. Returns path."""
    
    def save_experiment_metadata(self) -> str
        """Save metadata JSON. Returns path."""
    
    # Properties
    @property
    def results_dir(self) -> Path
        """Output directory for this experiment."""
    
    @property
    def results_csv(self) -> str
        """Path to raw results CSV."""
    
    @property
    def total_experiments(self) -> int
        """Total number of experiments to run."""
    
    @property
    def completed_experiments(self) -> int
        """Number of experiments completed."""
```

## Output Classes

### ExecutionResult

Results from a single experiment.

```python
@dataclass
class ExecutionResult:
    """Results from single algorithm execution."""
    
    algorithm: str
    instance: str
    K: int                       # Number of routes
    D: float                     # Total distance
    K_BKS: int                  # Best-known K
    D_BKS: float                # Best-known D
    time_seconds: float
    iterations: int
    feasible: bool
    timestamp: str
    family: str
    index: int
    
    # Methods
    def calculate_metrics(self) -> Dict
        """Calculate gap, delta_K, etc."""
```

### MetricsCalculator

Calculate and aggregate metrics.

```python
class MetricsCalculator:
    """Calculate metrics from solutions."""
    
    @staticmethod
    def calculate_metrics(solution: Solution,
                         k_bks: int,
                         d_bks: float) -> Dict
        """Calculate all metrics."""
```

## Analysis Classes

### StatisticalAnalysisReport

Perform statistical analysis.

```python
class StatisticalAnalysisReport:
    """Statistical analysis of results."""
    
    def __init__(self)
    
    # Methods
    def run_full_analysis(self, results_df: pd.DataFrame) -> Dict
        """Run complete analysis suite."""
    
    def analyze_by_algorithm(self, results_df: pd.DataFrame) -> Dict
        """Analyze grouped by algorithm."""
    
    def analyze_by_family(self, results_df: pd.DataFrame) -> Dict
        """Analyze grouped by family."""
    
    def analyze_by_algorithm_and_family(self, results_df: pd.DataFrame) -> Dict
        """Analyze by algorithm and family."""
    
    def kruskal_wallis(self, results_df: pd.DataFrame,
                      column: str) -> Dict
        """Perform Kruskal-Wallis test."""
    
    def wilcoxon_pairwise(self, results_df: pd.DataFrame,
                         column: str) -> Dict
        """Perform pairwise Wilcoxon tests."""
    
    def cohens_d(self, group1: List[float],
                group2: List[float]) -> float
        """Calculate Cohen's d effect size."""
```

### MatplotlibVisualizer

Generate plots.

```python
class MatplotlibVisualizer:
    """Matplotlib-based visualization."""
    
    def __init__(self)
    
    # Methods
    def plot_convergence(self, results_df: pd.DataFrame,
                        title: str = None,
                        save_path: str = None) -> None
        """Plot convergence curves."""
    
    def plot_boxplots(self, results_df: pd.DataFrame,
                     column: str,
                     by: str,
                     title: str = None,
                     save_path: str = None) -> None
        """Create boxplots."""
    
    def plot_heatmap(self, results_df: pd.DataFrame,
                    title: str = None,
                    save_path: str = None) -> None
        """Create heatmap."""
    
    def plot_time_vs_performance(self, results_df: pd.DataFrame,
                                title: str = None,
                                save_path: str = None) -> None
        """Plot time vs solution quality."""
    
    def generate_all_plots(self, results_df: pd.DataFrame,
                          output_dir: str) -> None
        """Generate all standard plots."""
    
    def save_all(self, output_dir: str) -> None
        """Save all generated plots."""
```

## Validation Classes

### ValidationSuite

Validation framework.

```python
class ValidationSuite:
    """Complete validation framework."""
    
    def __init__(self)
    
    # Methods
    def run_unit_tests(self) -> List['ValidationResult']
        """Run unit tests."""
    
    def run_integration_tests(self) -> List['ValidationResult']
        """Run integration tests."""
    
    def run_output_validation(self) -> List['ValidationResult']
        """Validate outputs."""
    
    def run_feasibility_validation(self) -> List['ValidationResult']
        """Validate feasibility."""
    
    def run_full_suite(self) -> Dict[str, List['ValidationResult']]
        """Run all validations."""
    
    def get_summary(self) -> Dict
        """Get validation summary."""
```

---

**Last Updated**: January 2, 2026  
**Status**: Complete Reference ✅
