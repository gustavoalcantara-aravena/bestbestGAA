#!/usr/bin/env python
"""Detailed debug for GAA algorithm execution with step-by-step inspection"""

from gaa import AlgorithmGenerator
from src.core.loader import SolomonLoader
from src.gaa.interpreter import ASTInterpreter
from src.core.models import Solution
from scripts.experiments import dict_to_ast
import traceback

# Generate algorithm
print("=" * 80)
print("STEP 1: Generate GAA Algorithm")
print("=" * 80)
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()
algo = algos[0]
print(f"Algorithm name: {algo['name']}")
print(f"Algorithm pattern: {algo['pattern']}")
print(f"Algorithm AST (dict): {algo['ast']}")

# Load instance
print("\n" + "=" * 80)
print("STEP 2: Load VRPTW Instance")
print("=" * 80)
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')
print(f"Instance: R101")
print(f"  - Customers: {len(instance.customers)}")
print(f"  - Vehicle capacity: {instance.vehicle_capacity if hasattr(instance, 'vehicle_capacity') else 'N/A'}")

# Create initial solution
print("\n" + "=" * 80)
print("STEP 3: Create Initial Empty Solution")
print("=" * 80)
initial = Solution(instance)
print(f"Initial solution created:")
print(f"  - Routes: {len(initial.routes)}")
print(f"  - Vehicles: {initial.num_vehicles}")
print(f"  - Distance: {initial.total_distance}")
print(f"  - Feasible: {initial.feasible}")

# Reconstruct AST
print("\n" + "=" * 80)
print("STEP 4: Reconstruct AST from Dict")
print("=" * 80)
ast_dict = algo['ast']
try:
    ast_node = dict_to_ast(ast_dict)
    print(f"AST reconstructed successfully")
    print(f"  - Type: {type(ast_node).__name__}")
    print(f"  - AST: {ast_node}")
except Exception as e:
    print(f"ERROR reconstructing AST: {e}")
    traceback.print_exc()
    exit(1)

# Try to execute
print("\n" + "=" * 80)
print("STEP 5: Execute Algorithm with ASTInterpreter")
print("=" * 80)
interpreter = ASTInterpreter()
try:
    print(f"Calling interpreter.execute(ast_node, instance)...")
    solution = interpreter.execute(ast_node, instance)
    print(f"Execution completed successfully")
    print(f"  - Result type: {type(solution).__name__}")
    print(f"  - Routes: {len(solution.routes)}")
    print(f"  - Vehicles: {solution.num_vehicles}")
    print(f"  - Distance: {solution.total_distance}")
    print(f"  - Feasible: {solution.feasible}")
    
    if solution.num_vehicles == 0:
        print("\n[WARNING] Solution is empty (K=0)!")
        print("Routes content:", solution.routes)
        
except Exception as e:
    print(f"ERROR executing algorithm: {e}")
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)
