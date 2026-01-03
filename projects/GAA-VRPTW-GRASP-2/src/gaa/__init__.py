"""
GAA (Generación Automática de Algoritmos) Package

Automatic Algorithm Generation for VRPTW using Abstract Syntax Trees.
Provides framework for representing, generating, executing, and repairing algorithms.

Module Structure:
- ast_nodes: Abstract Syntax Tree node definitions
- grammar: Formal grammar and constraint validation
- algorithm_generator: Random algorithm generation (Ramped Half-and-Half)
- interpreter: AST execution on problem instances
- repair: AST validation and automatic repair
"""

from .ast_nodes import (
    ASTNode,
    Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair,
    reconstruct_node,
)

from .grammar import (
    VRPTWGrammar,
    GrammarRule,
    ConstraintValidator,
)

from .algorithm_generator import (
    AlgorithmGenerator,
)

from .interpreter import (
    ASTInterpreter,
    OperatorRegistry,
    ASTProgramException,
)

from .repair import (
    ASTValidator,
    ASTRepairMechanism,
    ASTNormalizer,
    ASTStatistics,
    ASTRepairError,
)


__all__ = [
    # AST Nodes
    'ASTNode',
    'Seq', 'While', 'For', 'If', 'ChooseBestOf', 'ApplyUntilNoImprove',
    'GreedyConstruct', 'LocalSearch', 'Perturbation', 'Repair',
    'reconstruct_node',
    
    # Grammar
    'VRPTWGrammar',
    'GrammarRule',
    'ConstraintValidator',
    
    # Generator
    'AlgorithmGenerator',
    
    # Interpreter
    'ASTInterpreter',
    'OperatorRegistry',
    'ASTProgramException',
    
    # Repair
    'ASTValidator',
    'ASTRepairMechanism',
    'ASTNormalizer',
    'ASTStatistics',
    'ASTRepairError',
]
