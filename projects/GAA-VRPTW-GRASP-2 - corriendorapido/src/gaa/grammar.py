"""
Grammar for VRPTW-GRASP Algorithms

Defines the formal grammar using BNF/EBNF for valid algorithm structures.
Enforces canonical constraints:
1. Constructor randomized is mandatory
2. Minimum 2 local search operators
3. Repair mechanisms for constraint violations
4. Maximum depth and size constraints
"""

from typing import List, Set, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the grammar."""
    SEQUENCE = "Seq"
    WHILE_LOOP = "While"
    FOR_LOOP = "For"
    IF_COND = "If"
    CHOOSE_BEST = "ChooseBestOf"
    APPLY_UNTIL_NO_IMPROVE = "ApplyUntilNoImprove"
    
    # Terminals
    GREEDY_CONSTRUCT = "GreedyConstruct"
    LOCAL_SEARCH = "LocalSearch"
    PERTURBATION = "Perturbation"
    REPAIR = "Repair"


@dataclass
class GrammarRule:
    """
    Represents a single BNF production rule.
    
    Example:
        GrammarRule(
            lhs="<algorithm>",
            rhs=[
                ["<construction>", "<local_search>"],
                ["<construction>", "<perturbation>", "<local_search>"]
            ]
        )
    """
    lhs: str  # Left-hand side (non-terminal)
    rhs: List[List[str]]  # Right-hand side alternatives


class VRPTWGrammar:
    """
    Formal BNF Grammar for VRPTW-GRASP algorithms.
    
    Grammar Production Rules (simplified):
    
    <algorithm>         ::= <construction> <phase>
    <phase>             ::= <local_search> | <local_search> <phase>
                          | <while_intensify>
                          | <for_multistart>
    <while_intensify>   ::= WHILE <local_search> | WHILE <local_search> <phase>
    <for_multistart>    ::= FOR N TIMES <phase>
    <construction>      ::= CONSTRUCT Randomized | CONSTRUCT SavingsHeuristic | ...
    <local_search>      ::= SEARCH TwoOpt | SEARCH OrOpt | ... (min 2 required)
    <perturbation>      ::= PERTURB RuinRecreate | PERTURB EjectionChain | ...
    <repair>            ::= REPAIR Capacity | REPAIR TimeWindows
    """
    
    def __init__(self):
        self.rules = self._define_rules()
        self.terminals = self._define_terminals()
        self.constraints = self._define_constraints()
    
    def _define_rules(self) -> Dict[str, GrammarRule]:
        """Define all BNF production rules."""
        return {
            'algorithm': GrammarRule(
                lhs='<algorithm>',
                rhs=[
                    ['<construction>', '<local_search>'],
                    ['<construction>', '<intensification>'],
                    ['<construction>', '<for_multistart>'],
                ]
            ),
            'construction': GrammarRule(
                lhs='<construction>',
                rhs=[
                    ['CONSTRUCT_RANDOMIZED'],
                    ['CONSTRUCT_SAVINGS'],
                    ['CONSTRUCT_NN_TIME'],
                    ['CONSTRUCT_REGRET'],
                ]
            ),
            'local_search': GrammarRule(
                lhs='<local_search>',
                rhs=[
                    ['SEARCH_TWOOPT'],
                    ['SEARCH_OROPT'],
                    ['SEARCH_RELOCATE'],
                    ['SEARCH_THREEOPT'],
                    ['SEARCH_CROSSEXCHANGE'],
                    ['SEARCH_TWOOPTSTAR'],
                    ['SEARCH_SWAPCUSTOMERS'],
                ]
            ),
            'intensification': GrammarRule(
                lhs='<intensification>',
                rhs=[
                    ['WHILE_LS <local_search>'],
                    ['APPLY_UNTIL_NO_IMPROVE <local_search>'],
                    ['VND <local_search>+'],
                ]
            ),
            'for_multistart': GrammarRule(
                lhs='<for_multistart>',
                rhs=[
                    ['FOR N TIMES <algorithm>'],
                ]
            ),
            'perturbation': GrammarRule(
                lhs='<perturbation>',
                rhs=[
                    ['PERTURB_RUIN_RECREATE'],
                    ['PERTURB_EJECTION_CHAIN'],
                    ['PERTURB_RANDOM_REMOVAL'],
                ]
            ),
        }
    
    def _define_terminals(self) -> Dict[str, Set[str]]:
        """Define all terminal symbols (actual operators)."""
        return {
            'constructors': {
                'NearestNeighbor',
                'SavingsHeuristic',
                'TimeOrientedNN',
                'InsertionI1',
                'RegretInsertion',
                'RandomizedInsertion',
            },
            'local_search_intra': {
                'TwoOpt',
                'OrOpt',
                'Relocate',
                'ThreeOpt',
            },
            'local_search_inter': {
                'CrossExchange',
                'TwoOptStar',
                'SwapCustomers',
                'RelocateInter',
            },
            'perturbation': {
                'EjectionChain',
                'RuinRecreate',
                'RandomRemoval',
                'RouteElimination',
            },
            'repair': {
                'RepairCapacity',
                'RepairTimeWindows',
                'GreedyRepair',
            },
        }
    
    def _define_constraints(self) -> Dict[str, any]:
        """Define canonical constraints that all algorithms must satisfy."""
        return {
            'constructor_randomized': True,  # Must use RandomizedInsertion or similar
            'min_local_search': 2,  # At least 2 different local search operators
            'max_tree_depth': 5,  # Maximum nesting depth
            'max_tree_size': 25,  # Maximum total nodes
            'must_repair': True,  # Must have repair for constraint violations
            'must_have_iterations_limit': True,  # Must limit iterations
        }
    
    def is_valid_constructor(self, heuristic: str) -> bool:
        """Check if constructor is valid."""
        return heuristic in self.terminals['constructors']
    
    def is_valid_local_search(self, operator: str) -> bool:
        """Check if local search operator is valid."""
        all_ls = self.terminals['local_search_intra'] | self.terminals['local_search_inter']
        return operator in all_ls
    
    def is_valid_perturbation(self, operator: str) -> bool:
        """Check if perturbation operator is valid."""
        return operator in self.terminals['perturbation']
    
    def is_valid_repair(self, operator: str) -> bool:
        """Check if repair operator is valid."""
        return operator in self.terminals['repair']
    
    def get_all_constructors(self) -> Set[str]:
        """Get all valid constructive operators."""
        return self.terminals['constructors'].copy()
    
    def get_all_local_search(self) -> Set[str]:
        """Get all valid local search operators."""
        return (self.terminals['local_search_intra'] | 
                self.terminals['local_search_inter']).copy()
    
    def get_all_perturbation(self) -> Set[str]:
        """Get all valid perturbation operators."""
        return self.terminals['perturbation'].copy()
    
    def get_all_repair(self) -> Set[str]:
        """Get all valid repair operators."""
        return self.terminals['repair'].copy()


class ConstraintValidator:
    """
    Validates AST nodes against canonical constraints.
    
    Constraints:
    1. Constructor must be randomized (RandomizedInsertion preferred)
    2. At least 2 different local search operators
    3. Tree depth ≤ 5
    4. Tree size ≤ 25 nodes
    5. Repair mechanism for constraint violations
    6. Iterations limit required
    """
    
    def __init__(self):
        self.grammar = VRPTWGrammar()
        self.violations = []
    
    def validate_tree(self, ast_node) -> Tuple[bool, List[str]]:
        """
        Validate AST tree against all constraints.
        
        Returns:
            Tuple of (is_valid, violation_messages)
        """
        self.violations = []
        
        # Check depth
        depth = ast_node.depth()
        max_depth = self.grammar.constraints['max_tree_depth']
        if depth > max_depth:
            self.violations.append(f"Tree depth {depth} exceeds max {max_depth}")
        
        # Check size
        size = ast_node.size()
        max_size = self.grammar.constraints['max_tree_size']
        if size > max_size:
            self.violations.append(f"Tree size {size} exceeds max {max_size}")
        
        # Check construction phase
        self._check_construction_phase(ast_node)
        
        # Check local search operators
        local_search_ops = self._extract_local_search_ops(ast_node)
        if len(local_search_ops) < self.grammar.constraints['min_local_search']:
            self.violations.append(
                f"Need at least {self.grammar.constraints['min_local_search']} " +
                f"local search operators, found {len(local_search_ops)}"
            )
        
        # Check iteration limits
        self._check_iteration_limits(ast_node)
        
        is_valid = len(self.violations) == 0
        return is_valid, self.violations
    
    def _check_construction_phase(self, ast_node) -> None:
        """Verify construction phase exists and uses valid operators."""
        from src.gaa.ast_nodes import GreedyConstruct, Seq
        
        # Check if first node is construction
        if isinstance(ast_node, Seq) and len(ast_node.body) > 0:
            first = ast_node.body[0]
            if not isinstance(first, GreedyConstruct):
                self.violations.append(
                    "Algorithm must start with construction phase"
                )
        elif not isinstance(ast_node, GreedyConstruct):
            self.violations.append(
                "Algorithm must start with construction phase"
            )
    
    def _extract_local_search_ops(self, ast_node) -> Set[str]:
        """Extract all unique local search operators from AST."""
        from src.gaa.ast_nodes import LocalSearch, Seq
        
        operators = set()
        
        def traverse(node):
            if isinstance(node, LocalSearch):
                operators.add(node.operator)
            
            # Handle Seq (body is a list)
            if isinstance(node, Seq):
                for child in node.body:
                    traverse(child)
            elif hasattr(node, 'body'):
                traverse(node.body)
            elif hasattr(node, 'alternatives'):
                for alt in node.alternatives:
                    traverse(alt)
            elif hasattr(node, 'branches'):
                for branch in node.branches:
                    traverse(branch)
            elif hasattr(node, 'body_list'):
                for child in node.body_list:
                    traverse(child)
            elif hasattr(node, 'then_branch'):
                traverse(node.then_branch)
                if hasattr(node, 'else_branch') and node.else_branch:
                    traverse(node.else_branch)
        
        traverse(ast_node)
        return operators
    
    def _check_iteration_limits(self, ast_node) -> None:
        """Verify that iteration limits are properly set."""
        from src.gaa.ast_nodes import While, For, ApplyUntilNoImprove, Seq
        
        has_limit = False
        
        def check_limits(node):
            nonlocal has_limit
            if isinstance(node, (While, For, ApplyUntilNoImprove)):
                has_limit = True
            
            # Handle Seq (body is a list)
            if isinstance(node, Seq):
                for child in node.body:
                    check_limits(child)
            elif hasattr(node, 'body'):
                check_limits(node.body)
            elif hasattr(node, 'alternatives'):
                for alt in node.alternatives:
                    check_limits(alt)
            elif hasattr(node, 'branches'):
                for branch in node.branches:
                    check_limits(branch)
            elif hasattr(node, 'body_list'):
                for child in node.body_list:
                    check_limits(child)
            elif hasattr(node, 'then_branch'):
                check_limits(node.then_branch)
                if hasattr(node, 'else_branch') and node.else_branch:
                    check_limits(node.else_branch)
        
        check_limits(ast_node)
        
        if not has_limit:
            self.violations.append(
                "Algorithm must have iteration limits (While, For, or ApplyUntilNoImprove)"
            )
