"""Debug script to test constructor operators directly"""

from src.core.loader import SolomonLoader
from src.operators.constructive import (
    NearestNeighbor, RandomizedInsertion, SavingsHeuristic,
    TimeOrientedNN, InsertionI1, RegretInsertion
)
from src.core.models import Solution

"""Debug script to test constructor operators directly"""

from src.core.loader import SolomonLoader
from src.operators.constructive import (
    NearestNeighbor, RandomizedInsertion, SavingsHeuristic,
    TimeOrientedNN, InsertionI1, RegretInsertion
)
from src.core.models import Solution

# Load instance
loader = SolomonLoader()
all_instances = loader.load_all_instances('datasets')
instance = list(all_instances['R1'].values())[0]  # Get first instance from R1 family
print(f"Instance loaded: {instance.name}, n_customers={instance.n_customers}")

# Test each constructor
constructors = [
    NearestNeighbor(),
    RandomizedInsertion(alpha=0.25),
    SavingsHeuristic(),
    TimeOrientedNN(),
    InsertionI1(),
    RegretInsertion()
]

for constructor in constructors:
    print(f"\n{'='*60}")
    print(f"Testing: {constructor.name}")
    print('='*60)
    
    try:
        solution = constructor.apply(instance)
        print(f"✓ Constructor returned solution")
        print(f"  - Type: {type(solution)}")
        print(f"  - K (vehicles): {solution.num_vehicles}")
        print(f"  - D (distance): {solution.total_distance:.2f}")
        print(f"  - Feasible: {solution.feasible}")
        print(f"  - Routes: {len(solution.routes)}")
        if len(solution.routes) > 0:
            print(f"  - First route: {solution.routes[0].sequence[:5]}...")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
