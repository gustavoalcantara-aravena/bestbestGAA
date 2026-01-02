"""
AST Repair System for VRPTW

Validates and fixes invalid ASTs.
Implements automatic repair mechanisms for constraint violations.
"""

from typing import List, Tuple, Optional
import logging

from src.gaa.ast_nodes import (
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair
)
from src.gaa.grammar import VRPTWGrammar, ConstraintValidator


logger = logging.getLogger(__name__)


class ASTRepairError(Exception):
    """Exception raised during AST repair."""
    pass


class ASTValidator:
    """
    Validates AST against all constraints.
    Identifies specific violations.
    """
    
    def __init__(self):
        self.grammar = VRPTWGrammar()
        self.constraint_validator = ConstraintValidator()
    
    def validate(self, ast: ASTNode) -> Tuple[bool, List[str]]:
        """
        Validate AST comprehensively.
        
        Returns:
            (is_valid, list of violation descriptions)
        """
        violations = []
        
        # Check canonical constraints
        is_valid, constraint_violations = self.constraint_validator.validate_tree(ast)
        if not is_valid:
            violations.extend(constraint_violations)
        
        # Check structure constraints
        structure_issues = self._check_structure(ast)
        violations.extend(structure_issues)
        
        return len(violations) == 0, violations
    
    def _check_structure(self, ast: ASTNode) -> List[str]:
        """Check structural constraints."""
        issues = []
        
        # Every algorithm must have at least construction + local search
        if isinstance(ast, Seq):
            has_constructor = any(
                isinstance(n, GreedyConstruct)
                for n in self._flatten_body(ast)
            )
            has_local_search = any(
                isinstance(n, LocalSearch)
                for n in self._flatten_body(ast)
            )
            
            if not has_constructor:
                issues.append("Algorithm must have at least one constructor")
            if not has_local_search:
                issues.append("Algorithm must have at least one local search operator")
        
        return issues
    
    def _flatten_body(self, ast: ASTNode) -> List[ASTNode]:
        """Flatten AST to list of all nodes."""
        nodes = [ast]
        
        if isinstance(ast, Seq):
            for child in ast.body:
                nodes.extend(self._flatten_body(child))
        elif isinstance(ast, (While, For, ApplyUntilNoImprove)):
            if isinstance(ast, For):
                nodes.extend(self._flatten_body(ast.body))
            else:
                nodes.extend(self._flatten_body(ast.body))
        elif isinstance(ast, If):
            if ast.then_branch:
                nodes.extend(self._flatten_body(ast.then_branch))
            if ast.else_branch:
                nodes.extend(self._flatten_body(ast.else_branch))
        elif isinstance(ast, ChooseBestOf):
            for alt in ast.alternatives:
                nodes.extend(self._flatten_body(alt))
        
        return nodes


class ASTRepairMechanism:
    """
    Repairs invalid ASTs automatically.
    Implements multiple repair strategies.
    """
    
    def __init__(self):
        self.validator = ASTValidator()
        self.grammar = VRPTWGrammar()
    
    def repair(self, ast: ASTNode) -> Tuple[ASTNode, bool, List[str]]:
        """
        Attempt to repair invalid AST.
        
        Args:
            ast: Potentially invalid AST
        
        Returns:
            (repaired_ast, was_repaired, repairs_applied)
        """
        is_valid, violations = self.validator.validate(ast)
        if is_valid:
            return ast, False, []
        
        repairs_applied = []
        
        # Try to fix violations
        for violation in violations:
            if "max tree depth" in violation.lower():
                ast, fixed = self._fix_depth_violation(ast)
                if fixed:
                    repairs_applied.append("Fixed tree depth")
            
            elif "max tree size" in violation.lower():
                ast, fixed = self._fix_size_violation(ast)
                if fixed:
                    repairs_applied.append("Fixed tree size")
            
            elif "constructor" in violation.lower():
                ast, fixed = self._fix_constructor_violation(ast)
                if fixed:
                    repairs_applied.append("Added constructor")
            
            elif "local search" in violation.lower():
                ast, fixed = self._fix_local_search_violation(ast)
                if fixed:
                    repairs_applied.append("Added local search")
            
            elif "iteration" in violation.lower():
                ast, fixed = self._fix_iteration_violation(ast)
                if fixed:
                    repairs_applied.append("Added iteration limits")
        
        # Validate after repairs
        is_valid, _ = self.validator.validate(ast)
        return ast, is_valid or len(repairs_applied) > 0, repairs_applied
    
    def _fix_depth_violation(self, ast: ASTNode) -> Tuple[ASTNode, bool]:
        """Fix tree depth violation by pruning deep branches."""
        if not isinstance(ast, Seq):
            return ast, False
        
        # Prune very deep non-terminal nodes
        new_body = []
        for node in ast.body:
            if node.depth() > 3:
                # Replace with local search (terminal)
                new_body.append(LocalSearch(
                    operator='TwoOpt',
                    max_iterations=50
                ))
            else:
                new_body.append(node)
        
        return Seq(body=new_body), True
    
    def _fix_size_violation(self, ast: ASTNode) -> Tuple[ASTNode, bool]:
        """Fix tree size violation by removing redundant nodes."""
        if not isinstance(ast, Seq):
            return ast, False
        
        # Keep only first K nodes
        max_nodes = 20
        new_body = ast.body[:min(len(ast.body), max_nodes // 3)]
        
        return Seq(body=new_body), len(new_body) < len(ast.body)
    
    def _fix_constructor_violation(self, ast: ASTNode) -> Tuple[ASTNode, bool]:
        """Add constructor if missing."""
        if isinstance(ast, Seq):
            # Check if constructor exists
            has_constructor = any(
                isinstance(n, GreedyConstruct)
                for n in ast.body
            )
            
            if not has_constructor:
                # Add at beginning
                constructor = GreedyConstruct(heuristic='RandomizedInsertion')
                ast.body.insert(0, constructor)
                return ast, True
        
        return ast, False
    
    def _fix_local_search_violation(self, ast: ASTNode) -> Tuple[ASTNode, bool]:
        """Add local search if missing or insufficient."""
        if not isinstance(ast, Seq):
            return ast, False
        
        # Count unique local search operators
        ls_ops = set()
        for node in ast.body:
            if isinstance(node, LocalSearch):
                ls_ops.add(node.operator)
        
        # Need at least 2 different
        if len(ls_ops) < 2:
            # Add another local search
            available = list(self.grammar.get_all_local_search())
            for op in available:
                if op not in ls_ops:
                    ast.body.append(LocalSearch(
                        operator=op,
                        max_iterations=30
                    ))
                    break
            
            return ast, True
        
        return ast, False
    
    def _fix_iteration_violation(self, ast: ASTNode) -> Tuple[ASTNode, bool]:
        """Add iteration limits to control flow nodes."""
        fixed = False
        
        def add_limits(node: ASTNode) -> ASTNode:
            nonlocal fixed
            
            if isinstance(node, While):
                if node.max_iterations is None or node.max_iterations == 0:
                    node.max_iterations = 100
                    fixed = True
            elif isinstance(node, For):
                if node.iterations is None or node.iterations == 0:
                    node.iterations = 5
                    fixed = True
            elif isinstance(node, ApplyUntilNoImprove):
                if node.max_no_improve is None or node.max_no_improve == 0:
                    node.max_no_improve = 20
                    fixed = True
            elif isinstance(node, Seq):
                for child in node.body:
                    add_limits(child)
            
            return node
        
        ast = add_limits(ast)
        return ast, fixed


class ASTNormalizer:
    """
    Normalizes valid ASTs to standard forms.
    Improves readability and potential performance.
    """
    
    def normalize(self, ast: ASTNode) -> ASTNode:
        """
        Apply normalization rules to AST.
        
        Rules:
        - Collapse single-node sequences
        - Reorder nodes (construction first, then local search)
        - Simplify if/else branches
        """
        ast = self._collapse_sequences(ast)
        ast = self._reorder_phases(ast)
        ast = self._simplify_control_flow(ast)
        
        return ast
    
    def _collapse_sequences(self, ast: ASTNode) -> ASTNode:
        """Flatten nested sequences."""
        if not isinstance(ast, Seq):
            return ast
        
        # Check if body has single Seq that can be collapsed
        if len(ast.body) == 1 and isinstance(ast.body[0], Seq):
            return self._collapse_sequences(ast.body[0])
        
        # Recursively process children
        new_body = [self._collapse_sequences(node) for node in ast.body]
        return Seq(body=new_body)
    
    def _reorder_phases(self, ast: ASTNode) -> ASTNode:
        """Ensure construction phase comes first."""
        if not isinstance(ast, Seq):
            return ast
        
        constructors = []
        others = []
        
        for node in ast.body:
            if isinstance(node, GreedyConstruct):
                constructors.append(node)
            else:
                others.append(node)
        
        if constructors:
            # Reorder: constructors first, then others
            new_body = constructors + others
            return Seq(body=new_body)
        
        return ast
    
    def _simplify_control_flow(self, ast: ASTNode) -> ASTNode:
        """Simplify overly nested control structures."""
        if isinstance(ast, If):
            # Remove unnecessary If nodes
            if ast.then_branch is None and ast.else_branch is None:
                return LocalSearch(operator='TwoOpt', max_iterations=50)
        
        elif isinstance(ast, ChooseBestOf):
            # If only one alternative, unwrap
            if len(ast.alternatives) == 1:
                return ast.alternatives[0]
        
        return ast


class ASTStatistics:
    """
    Analyzes AST characteristics and statistics.
    """
    
    @staticmethod
    def analyze(ast: ASTNode) -> dict:
        """
        Analyze AST structure.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'depth': ast.depth(),
            'size': ast.size(),
            'structure': ast.to_pseudocode(),
            'node_type': type(ast).__name__,
        }
