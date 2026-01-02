# Contributing Guide

Guidelines for contributing to VRPTW-GRASP framework.

## Code of Conduct

- Be respectful to all contributors
- Focus on constructive feedback
- Welcome newcomers and diverse perspectives
- Report issues professionally

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/GAA-VRPTW-GRASP-2.git
cd GAA-VRPTW-GRASP-2
```

### 2. Create Feature Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-bugfix
```

### 3. Set Up Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate    # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

### 4. Make Changes

Follow the guidelines below.

### 5. Test Your Changes

```bash
pytest -v
pytest --cov=src  # Check coverage
```

### 6. Commit and Push

```bash
git add .
git commit -m "Descriptive commit message"
git push origin feature/my-feature
```

### 7. Create Pull Request

Open PR with description of changes.

## Development Workflow

### Coding Standards

#### Python Style (PEP 8)

```python
# ✅ Good
class MyClass:
    """Brief description."""
    
    def my_method(self, param1: int, param2: str) -> bool:
        """
        Detailed description.
        
        Args:
            param1: Description
            param2: Description
        
        Returns:
            Description of return value
        """
        result = param1 + len(param2)
        return result > 0

# ❌ Avoid
def myFunction(p1,p2):  # Wrong: camelCase, no types
    x=p1+len(p2)  # Wrong: no spaces
    return x>0
```

#### Type Hints

```python
# ✅ Always use type hints
def solve(instance: Instance, 
          max_iter: int = 100) -> Solution:
    ...

# ✅ For complex types
from typing import List, Dict, Tuple, Optional

def analyze(results: List[Dict[str, float]]) -> Tuple[float, float]:
    ...

# ✅ For custom classes
from src.core.instance import Instance
from src.core.grasp import Solution
```

#### Docstrings

```python
# ✅ Google-style docstrings
def calculate_metrics(solution: Solution) -> Dict[str, float]:
    """
    Calculate performance metrics for solution.
    
    This function computes K (routes), D (distance),
    and other relevant metrics.
    
    Args:
        solution: Solution object to analyze
    
    Returns:
        Dictionary with:
            - 'K': Number of routes
            - 'D': Total distance
            - 'time': Total time
            - 'feasible': Feasibility flag
    
    Raises:
        ValueError: If solution is invalid
    
    Examples:
        >>> solution = grasp.solve()
        >>> metrics = calculate_metrics(solution)
        >>> print(metrics['K'])
    """
```

#### Naming Conventions

```python
# Classes: PascalCase
class GRASP:
    pass

class ExperimentConfig:
    pass

# Functions/Methods: snake_case
def solve_instance(instance):
    pass

def add_customer(self, customer):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ITERATIONS = 100
VEHICLE_CAPACITY = 1000

# Private: Leading underscore
def _helper_function():
    pass

self._internal_state = None
```

## Testing

### Running Tests

```bash
# All tests
pytest -v

# Single file
pytest scripts/test_phase11.py -v

# Single test
pytest scripts/test_phase11.py::TestValidationResult::test_validation_result_passed -v

# With coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

```python
import pytest
from src.core.instance import Instance
from src.core.grasp import GRASP

class TestGRASP:
    """Tests for GRASP solver."""
    
    @pytest.fixture
    def instance(self):
        """Load test instance."""
        return Instance.from_solomon_csv("datasets/test/C101.csv")
    
    def test_solve_returns_solution(self, instance):
        """Test that solve returns a Solution object."""
        grasp = GRASP(instance, seed=42)
        solution = grasp.solve()
        assert solution is not None
        assert solution.num_routes > 0
    
    def test_reproducibility(self, instance):
        """Test that same seed produces same result."""
        grasp1 = GRASP(instance, seed=42)
        sol1 = grasp1.solve()
        
        grasp2 = GRASP(instance, seed=42)
        sol2 = grasp2.solve()
        
        assert sol1.num_routes == sol2.num_routes
        assert sol1.total_distance == sol2.total_distance
    
    def test_feasibility(self, instance):
        """Test that solution is feasible."""
        grasp = GRASP(instance, seed=42)
        solution = grasp.solve()
        assert solution.is_feasible()
```

### Test Coverage Requirements

- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- **Critical paths**: 100% coverage

```bash
# Check coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html
```

## Documentation

### Updating Documentation

1. **Code Comments**: Explain complex logic
2. **Docstrings**: Document all public classes/methods
3. **README**: Update if adding features
4. **CHANGELOG**: Record your changes

### Documentation Style

```python
# ✅ Good: Clear and concise
# Check feasibility by validating constraints
if not solution.is_feasible():
    return False

# ❌ Avoid: Obvious comments
# Increment counter
counter += 1

# ❌ Avoid: Outdated comments
# TODO: Fix this bug (3 years old)
```

## Git Workflow

### Commit Messages

```
# ✅ Good
commit: Add 2-opt operator for local search
commit: Fix memory leak in result aggregation
commit: Update documentation for API

# ❌ Avoid
commit: changes
commit: fixed stuff
commit: asdf
```

### Commit Frequency

```bash
# Good: Logical, meaningful commits
git commit -m "Add validation for instance constraints"
git commit -m "Fix edge case in capacity check"

# Avoid: Huge, monolithic commits
git commit -m "Update everything"
```

## Pull Request Process

### 1. Before Creating PR

- [ ] All tests pass: `pytest -v`
- [ ] Coverage maintained: `pytest --cov=src`
- [ ] Code follows PEP 8: `flake8 src/`
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

### 2. PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation
- [ ] Refactoring

## Changes Made
- Point 1
- Point 2
- Point 3

## Testing
- [ ] Added tests
- [ ] All tests pass
- [ ] Coverage maintained

## Related Issues
Closes #123

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

### 3. Review Process

- Maintainers review code
- Provide feedback
- Update code as needed
- Approve and merge

## Adding New Features

### Example: Adding a New Operator

1. **Create the operator class**:

```python
# src/core/operators.py

class MyNewOperator(OperatorBase):
    """Description of operator."""
    
    def apply(self, solution: Solution) -> Solution:
        """Apply operator to solution."""
        # Implementation
        return modified_solution
```

2. **Write tests**:

```python
# scripts/test_my_operator.py

def test_my_new_operator():
    """Test new operator."""
    solution = create_test_solution()
    operator = MyNewOperator()
    result = operator.apply(solution)
    assert result.is_feasible()
    assert result.num_routes <= solution.num_routes
```

3. **Update documentation**:

```python
# Update ARCHITECTURE.md
# Add to operator list: MyNewOperator
```

4. **Test integration**:

```python
# Ensure operator works with GRASP
grasp = GRASP(instance)
grasp.add_operator(MyNewOperator())
solution = grasp.solve()
```

## Release Process

### Version Numbering

Follow Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Steps

1. Update version number in setup.py
2. Update CHANGELOG.md
3. Create release notes
4. Tag commit: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`

## Project Structure

```
src/
├── core/              # Core VRPTW classes
│   ├── __init__.py
│   ├── instance.py   # Instance, Customer, Route, Solution
│   ├── grasp.py      # GRASP solver
│   ├── operators.py  # All domain operators
│   ├── evaluator.py  # Fitness evaluation
│   └── bks.py        # Best-known solutions
├── gaa/              # Algorithm generation
│   ├── __init__.py
│   ├── ast.py        # AST implementation
│   ├── grammar.py    # Grammar rules
│   └── generator.py  # Algorithm generator
└── utils/            # Utilities
    ├── __init__.py
    ├── loader.py     # Instance loader
    └── helpers.py    # Helper functions
```

## Common Development Tasks

### Adding a Configuration Option

1. Update `config.yaml`:
```yaml
new_option:
  value: default
```

2. Update Config class:
```python
class Config:
    new_option: str = "default"
```

3. Document in CONFIG_REFERENCE.md

### Adding a Metric

1. Implement in Evaluator:
```python
def calculate_new_metric(solution):
    # Calculate
    return value
```

2. Add to ExecutionResult:
```python
@dataclass
class ExecutionResult:
    new_metric: float
```

3. Test and document

### Adding a Visualization

1. Implement in MatplotlibVisualizer:
```python
def plot_new_visualization(self, data):
    # Create plot
    plt.show()
```

2. Test visualization
3. Add to `generate_all_plots()`

## Resources

- **Python Style**: [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Testing**: [Pytest Documentation](https://docs.pytest.org/)
- **Git**: [Git Documentation](https://git-scm.com/doc)

## Getting Help

- Check existing issues
- Ask in pull requests
- Review similar code
- Consult ARCHITECTURE.md

---

**Last Updated**: January 2, 2026  
**Status**: Development Ready ✅
