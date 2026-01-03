#!/usr/bin/env python
"""Debug test for GAA algorithm execution"""

from gaa import AlgorithmGenerator
from src.core.loader import SolomonLoader
from src.gaa.interpreter import ASTInterpreter
from scripts.experiments import dict_to_ast

# Generate algorithm
gen = AlgorithmGenerator(seed=42)
algos = gen.generate_three_algorithms()
algo = algos[0]

# Load instance
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')

# Try to execute
interpreter = ASTInterpreter()
ast_dict = algo['ast']
print(f'AST dict type: {type(ast_dict)}')

try:
    ast_node = dict_to_ast(ast_dict)
    print(f'AST node type: {type(ast_node)}')
    print(f'AST node: {ast_node}')
    
    solution = interpreter.execute(ast_node, instance)
    print(f'Solution: K={solution.num_vehicles}, D={solution.total_distance}')
except Exception as e:
    import traceback
    print(f'ERROR: {e}')
    traceback.print_exc()
