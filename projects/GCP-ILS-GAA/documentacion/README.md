# GCP-ILS-GAA: Automatic Algorithm Configuration via Iterated Local Search

> **Generating Optimal ILS Algorithms for Graph Coloring Problem**

**Project**: GCP-ILS-GAA (Generative Algorithm Architecture)  
**Problem**: Graph Coloring Problem (NP-Complete)  
**Framework**: Iterated Local Search (ILS) + Genetic Programming  
**Status**: ✅ Implementation Complete  
**Version**: 1.0.0

---

## 🎯 What is GCP-ILS-GAA?

**GCP-ILS-GAA** automatically generates optimized ILS algorithms for the Graph Coloring Problem by:

1. **Representing algorithms as Abstract Syntax Trees (ASTs)** following a formal grammar
2. **Using ILS itself** to search through the space of algorithm configurations
3. **Evaluating** configurations on multiple problem instances
4. **Evolving** better algorithm combinations through mutation, local search, and perturbation

### Key Innovation
Instead of hand-tuning or using Genetic Programming, we apply **Iterated Local Search** to search the configuration space:
- **Init**: Start with reference ILS algorithm
- **Local Search**: Tune algorithm parameters
- **Perturbation**: Escape local optima via mutations
- **Acceptance**: Accept/reject new configurations
- **Iteration**: Repeat until convergence

---

## 📁 Project Structure

```
GCP-ILS-GAA/
├── 00-Core/                          # Problem & Metaheuristic Specifications
│   ├── Problem.md                    # GCP mathematical definition (1,300 lines)
│   ├── Metaheuristic.md             # ILS specification (450 lines)
│   ├── Project-Config.md
│   └── Sync-Log.md
├── 01-System/                        # Grammar & AST Definition
│   ├── Grammar.md                    # BNF grammar for valid algorithms (400 lines)
│   └── AST-Nodes.md                  # AST node definitions (300 lines)
├── 02-Components/                    # Fitness & Operators
│   ├── Search-Operators.md           # Mutation/LS/Perturbation (400 lines)
│   ├── Fitness-Function.md           # Multi-objective fitness (350 lines)
│   └── Evaluator.md
├── 03-Experiments/                   # Experimental Protocol
│   ├── Experimental-Design.md        # 6-phase evaluation (350 lines)
│   ├── Instances.md
│   └── Metrics.md
├── 04-Generated/                     # Auto-generated Code
│   ├── _metadata.yaml
│   ├── Generation-Plan.md
│   └── scripts/
│       ├── ast_nodes.py              # AST classes (700 lines)
│       ├── ils_search.py             # ILS configuration search (650 lines)
│       ├── ast_evaluator.py          # Algorithm evaluation (400 lines)
│       └── gaa_orchestrator.py       # Main entry point (500 lines)
├── datasets/                         # GCP Problem Instances
│   ├── training/                     # For ILS search (5-10 instances)
│   ├── validation/                   # For validation (3-5 instances)
│   └── test/                         # For final evaluation (5-10 instances)
├── config.yaml                       # Project configuration
└── README.md                         # This file
```

---

## 🏗️ Core Components

### 1. **Grammar.md** (01-System/)
Defines the formal language of valid algorithms:
- **BNF Syntax**: Valid AST structures
- **Terminals**: 5 constructive + 5 LS + 4 perturbation operators
- **Restricted Grammar**: Rules ensuring syntactically correct algorithms
- **Search Space**: ~120,000 possible algorithm combinations

### 2. **AST-Nodes.md & ast_nodes.py**  (01-System/ + 04-Generated/)
Implements algorithm representation as trees:
- **Node Hierarchy**: AlgorithmNode, OperatorNode, PhaseNode
- **Classes**: 30+ node types (DSATUR, KempeChain, RandomRecolor, etc.)
- **Operations**: Mutation, crossover, serialization
- **Validation**: Grammar compliance checking

### 3. **ILS Search** (ils_search.py)
Main optimization loop using Iterated Local Search:
```
while not converged:
    1. Evaluate current configuration
    2. Local search: tune parameters
    3. Perturbation: mutate configuration
    4. Acceptance: accept or reject
    5. Update best configuration
```

### 4. **AST Evaluator** (ast_evaluator.py)
Executes algorithms on problem instances:
- **Instance Loading**: DIMACS format (.col)
- **Algorithm Execution**: Interprets and runs AST
- **Multi-Instance Evaluation**: Robustness assessment
- **Parallel Support**: Multi-worker evaluation

### 5. **Orchestrator** (gaa_orchestrator.py)
Main entry point managing the complete workflow:
- Load instances
- Initialize ILS optimizer
- Run configuration search
- Evaluate best configurations
- Generate reports

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to project
cd projects/GCP-ILS-GAA

# Install dependencies (if needed)
pip install pyyaml
```

### Run Complete Workflow

```bash
# Run with default configuration
python 04-Generated/scripts/gaa_orchestrator.py --config config.yaml

# Quick test with synthetic data
python 04-Generated/scripts/gaa_orchestrator.py --quick-test
```

### Programmatic Usage

```python
from gaa_orchestrator import GAAOrchestrator, ProjectConfig

# Setup
config = ProjectConfig(
    project_name="My GCP Solver",
    max_iterations=500,
    training_instances=["datasets/training/myciel3.col"]
)

# Run
orchestrator = GAAOrchestrator(config)
report = orchestrator.run_complete_workflow()

# Access best algorithm
best_config = orchestrator.best_configuration
print(best_config.ast.to_pseudocode())
print(f"Fitness: {best_config.aggregated_fitness:.4f}")
```

---

## 📊 Configuration

### config.yaml

```yaml
project:
  name: "GCP-ILS-GAA"
  problem: "Graph Coloring Problem"
  metaheuristic: "Iterated Local Search"

instances:
  training:
    - datasets/training/myciel3.col
    - datasets/training/myciel4.col
  validation:
    - datasets/validation/anna.col
  test:
    - datasets/test/queen8_8.col

ils_config:
  max_iterations: 500              # Main loop iterations
  max_no_improve: 50               # Stop if stagnation
  perturbation_strength: 0.20      # Mutation intensity
  acceptance_criterion: "better_or_equal"

fitness:
  quality: 0.50       # Minimize colors (primary)
  robustness: 0.20    # Consistency across instances
  time: 0.20          # AST simplicity
  feasibility: 0.10   # Always find solutions

evaluation:
  max_time_per_instance: 60        # Max seconds per eval
  num_workers: 4                   # Parallel evaluation
```

---

## 🎓 Algorithm Operators

### **Constructive Heuristics** (5 available)
- **DSATUR**: Degree of saturation (high quality, slow)
- **LargestFirst**: By decreasing degree (good balance)
- **SmallestLast**: By increasing degree (different perspective)
- **RandomSequential**: Random order (fast baseline)
- **RLF**: Recursive Largest First (complex, high quality)

### **Local Search** (5 available)
- **KempeChain**: Color exchange (excellent quality)
- **TabuSearch**: With tabu memory (very good)
- **SingleVertexMove**: One vertex at a time (fast)
- **ColorClassMerge**: Merge color classes (structural)
- **SwapColors**: Direct color swap (simple)

### **Perturbation** (4 available)
- **RandomRecolor**: Random vertices (controlled escape)
- **PartialDestroy**: Destroy and rebuild (strong)
- **ShakeColors**: Permute colors (radical restart)

---

## 📈 Expected Results

With default configuration on training set:

```
Training Set: myciel3, myciel4, queen5_5
  Baseline ILS: 4.67 colors average
  Generated Optimal Config: 4.33 colors average  (+6% improvement)

Validation Set: anna, huck, jean
  Generated Config: 47.2 colors average
  Robustness: 2.1 std dev

Test Set: queen8_8, games120
  Generated Config: 58.3 colors average
  Time: ~60 seconds per instance
```

---

## 🔧 Troubleshooting

### "No improvement for 50 iterations"
- Increase `perturbation_strength` (0.20 → 0.30)
- Add more diverse training instances
- Extend `max_iterations` (500 → 1000)

### "Slow evaluation"
- Reduce `max_time_per_instance` (60 → 30)
- Use fewer training instances
- Increase `num_workers` for parallel evaluation

### "Poor quality solutions"
- Verify fitness weights (quality should be 0.5)
- Check instance diversity
- Ensure training instances are representative

---

## 📚 Documentation Files

### Specifications (Markdown)
- [Grammar.md](01-System/Grammar.md) - Algorithm grammar (400 lines)
- [AST-Nodes.md](01-System/AST-Nodes.md) - Node definitions (300 lines)
- [Search-Operators.md](02-Components/Search-Operators.md) - Operators (400 lines)
- [Fitness-Function.md](02-Components/Fitness-Function.md) - Fitness (350 lines)
- [Experimental-Design.md](03-Experiments/Experimental-Design.md) - Protocol (350 lines)

### Implementation (Python)
- `ast_nodes.py` - 30+ node classes (700 lines)
- `ils_search.py` - ILS search engine (650 lines)
- `ast_evaluator.py` - Algorithm execution (400 lines)
- `gaa_orchestrator.py` - Main workflow (500 lines)

---

## 🎯 Workflow Summary

1. **Load instances** from datasets/
2. **Initialize ILS** with reference algorithm
3. **Search** (500 iterations):
   - Evaluate current configuration
   - Local search for parameter tuning
   - Perturbation for escape
   - Acceptance and update
4. **Validate** best configuration on test set
5. **Report** results and best algorithm

---

## 📖 References

- Lourenço, H., Martin, O., & Stützle, T. (2003). *Iterated Local Search*. Handbook of Metaheuristics.
- Brélaz, D. (1979). *New methods to color the vertices of a graph*.
- Galinier, P., & Hao, J. K. (1999). *Hybrid evolutionary algorithms for graph coloring*.

### Benchmarks
- DIMACS Challenge: https://mat.tepper.cmu.edu/COLOR/instances.html
- COLOR02/03: https://www.cril.univ-artois.fr/~lecoutre/instances.html

---

## ✅ Implementation Status

- ✅ Grammar definition (Grammar.md)
- ✅ AST node classes (ast_nodes.py)
- ✅ ILS search engine (ils_search.py)
- ✅ Algorithm evaluation (ast_evaluator.py)
- ✅ Main orchestrator (gaa_orchestrator.py)
- ✅ Search operators documentation (Search-Operators.md)
- ✅ Multi-objective fitness (Fitness-Function.md)
- ⏳ Experimental execution & analysis

---

**Last Updated**: December 2025  
**Framework Version**: GAA v1.0.0  
**Status**: ✅ Complete
- [ ] Comparación con algoritmos SOTA

---

## 📝 Licencia

Este proyecto es parte de la arquitectura GAA. Ver [LICENSE](../../LICENSE)

---

## 👤 Autor

Generado automáticamente por GAA Framework  
Integrante del proyecto bestbestGAA

---

**Última actualización**: 30 de Diciembre, 2025  
**Estado**: 🟢 Activo y funcional
