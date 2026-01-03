#!/usr/bin/env python3
"""Quick test of one instance to verify constructors work"""

from src.core.loader import SolomonLoader
from src.gaa.algorithm_generator import AlgorithmGenerator
from src.gaa.interpreter import ASTInterpreter
from scripts.experiments import dict_to_ast

# Load one instance
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')
print(f'Instance R101, Customers: {instance.n_customers}')

# Generate one algorithm
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()
algo_dict = algos[0]
print(f'Algorithm: {algo_dict["name"]}')

# Execute
interpreter = ASTInterpreter()
ast_node = dict_to_ast(algo_dict['ast'])
solution = interpreter.execute(ast_node, instance)

print(f'Result: K={solution.num_vehicles}, D={solution.total_distance:.2f}')
print(f'Feasible: {solution.feasible}')
print(f'Routes: {len(solution.routes)}')
for i, route in enumerate(solution.routes):
    print(f'  Route {i}: {len(route.sequence)} stops, load={sum(instance.get_customer(c).demand for c in route.sequence[1:-1])}/{instance.Q_capacity}')
