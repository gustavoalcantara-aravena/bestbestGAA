"""
GAA Module Initialization - GAA-GCP-ILS-4
Módulo de Generación Automática de Algoritmos
"""

from .ast_nodes import (
    ASTNode,
    Seq, If, While, For, Call,
    GreedyConstruct, LocalSearch, Perturbation,
    random_ast, mutate_ast, crossover_ast
)

from .grammar import Grammar, DEFAULT_GRAMMAR

from .generator import (
    AlgorithmGenerator,
    generate_initial_population
)

from .interpreter import (
    ExecutionContext,
    ASTInterpreter,
    execute_algorithm
)

__all__ = [
    # AST Nodes
    'ASTNode',
    'Seq', 'If', 'While', 'For', 'Call',
    'GreedyConstruct', 'LocalSearch', 'Perturbation',
    'random_ast', 'mutate_ast', 'crossover_ast',
    
    # Grammar
    'Grammar', 'DEFAULT_GRAMMAR',
    
    # Generator
    'AlgorithmGenerator', 'generate_initial_population',
    
    # Interpreter
    'ExecutionContext', 'ASTInterpreter', 'execute_algorithm'
]
