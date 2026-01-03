"""Debug script to understand VND's D=654.0 problem"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.loader import SolomonLoader
from src.metaheuristic.grasp import GRASP
from src.metaheuristic.vnd import VariableNeighborhoodDescent
from src.operators import RandomizedInsertion
import json

def test_instance(instance_id='R101'):
    """Test GRASP, VND, and ILS on a single instance"""
    
    # Load instance
    loader = SolomonLoader()
    instance = loader.load_instance('datasets/R1/' + instance_id + '.csv')
    
    print(f"\n{'='*70}")
    print(f"Testing {instance_id}")
    print(f"{'='*70}")
    print(f"Instance: {instance_id}")
    print(f"  Customers: {instance.n_customers}")
    print(f"  Capacity: {instance.Q_capacity}")
    print()
    
    # Test GRASP
    print("[GRASP] Running GRASP...")
    grasp = GRASP(alpha=0.15, max_iterations=100, seed=42, verbose=True)
    grasp_solution, grasp_fitness, grasp_stats = grasp.solve(instance)
    print(f"  Result: K={grasp_fitness[0]}, D={grasp_fitness[1]:.2f}")
    print(f"  Solution has {len(grasp_solution.routes)} routes")
    for i, route in enumerate(grasp_solution.routes):
        print(f"    Route {i}: {route.sequence} (distance={route.total_distance:.2f})")
    print()
    
    # Test RandomizedInsertion (constructor)
    print("[CONSTRUCTOR] Creating initial solution with RandomizedInsertion...")
    constructor = RandomizedInsertion(alpha=0.15, seed=42)
    initial_solution = constructor.apply(instance)
    print(f"  Initial solution: K={initial_solution.num_vehicles}, D={initial_solution.total_distance:.2f}")
    print(f"  Solution has {len(initial_solution.routes)} routes")
    for i, route in enumerate(initial_solution.routes):
        print(f"    Route {i}: {route.sequence} (distance={route.total_distance:.2f})")
    print()
    
    # Test VND with constructor's initial solution
    print("[VND] Running VND on initial_solution...")
    vnd = VariableNeighborhoodDescent(verbose=True)
    vnd_solution = vnd.search(initial_solution)
    print(f"  Result: K={vnd_solution.num_vehicles}, D={vnd_solution.total_distance:.2f}")
    print(f"  Solution has {len(vnd_solution.routes)} routes")
    for i, route in enumerate(vnd_solution.routes):
        print(f"    Route {i}: {route.sequence} (distance={route.total_distance:.2f})")
    print()
    
    # Also test VND with GRASP's solution
    print("[VND-on-GRASP] Running VND on GRASP solution...")
    vnd2 = VariableNeighborhoodDescent(verbose=True)
    vnd_grasp_solution = vnd2.search(grasp_solution)
    print(f"  Result: K={vnd_grasp_solution.num_vehicles}, D={vnd_grasp_solution.total_distance:.2f}")
    print()
    
    # Comparison
    print("[COMPARISON]")
    print(f"  GRASP:          K={grasp_fitness[0]}, D={grasp_fitness[1]:.2f}")
    print(f"  VND(initial):   K={vnd_solution.num_vehicles}, D={vnd_solution.total_distance:.2f}")
    print(f"  VND(GRASP):     K={vnd_grasp_solution.num_vehicles}, D={vnd_grasp_solution.total_distance:.2f}")
    
    # Check if solution is valid
    print()
    print("[VALIDATION]")
    print(f"  Initial solution valid: {initial_solution.is_feasible}")
    print(f"  VND solution valid: {vnd_solution.is_feasible}")
    print(f"  GRASP solution valid: {grasp_solution.is_feasible}")
    print(f"  VND(GRASP) solution valid: {vnd_grasp_solution.is_feasible}")

if __name__ == "__main__":
    test_instance('R101')
    test_instance('R102')
