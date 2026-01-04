"""
============================================================
AST Nodes Implementation
GRASP + GAA for VRPTW (Solomon)
============================================================
"""

from abc import ABC, abstractmethod
import math
import random


# ============================================================
# Base AST Node
# ============================================================

class ASTNode(ABC):
    """
    Abstract base class for all AST nodes.
    """

    @abstractmethod
    def evaluate(self, state: dict):
        """
        Evaluate node given a state dictionary.
        Must be pure: no side effects.
        """
        pass


# ============================================================
# Terminal Nodes
# ============================================================

class Feature(ASTNode):
    """
    Terminal node: returns a feature value from state.
    """

    def __init__(self, name: str):
        self.name = name

    def evaluate(self, state: dict):
        if self.name not in state:
            raise KeyError(f"Feature '{self.name}' not found in state")
        return state[self.name]


class Const(ASTNode):
    """
    Constant value node.
    """

    def __init__(self, value):
        self.value = value

    def evaluate(self, state: dict):
        return self.value


# ============================================================
# Arithmetic Nodes
# ============================================================

class Add(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return self.left.evaluate(state) + self.right.evaluate(state)


class Sub(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return self.left.evaluate(state) - self.right.evaluate(state)


class Mul(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return self.left.evaluate(state) * self.right.evaluate(state)


class Div(ASTNode):
    """
    Safe division.
    """

    def __init__(self, left: ASTNode, right: ASTNode, eps: float = 1e-9):
        self.left = left
        self.right = right
        self.eps = eps

    def evaluate(self, state: dict):
        denom = self.right.evaluate(state)
        if abs(denom) < self.eps:
            return 0.0
        return self.left.evaluate(state) / denom


# ============================================================
# Aggregation Nodes
# ============================================================

class WeightedSum(ASTNode):
    """
    Weighted sum of expressions.
    """

    def __init__(self, terms: list):
        """
        terms: list of dicts
        [
            { "weight": float, "expr": ASTNode }
        ]
        """
        self.terms = terms

    def evaluate(self, state: dict):
        total = 0.0
        for term in self.terms:
            w = term["weight"]
            expr = term["expr"]
            total += w * expr.evaluate(state)
        return total


class Normalize(ASTNode):
    """
    Normalize a value to [0,1] using fixed bounds.
    """

    def __init__(self, expr: ASTNode, min_val: float = 0.0, max_val: float = 1.0):
        self.expr = expr
        self.min_val = min_val
        self.max_val = max_val

    def evaluate(self, state: dict):
        val = self.expr.evaluate(state)
        if self.max_val - self.min_val == 0:
            return 0.0
        return (val - self.min_val) / (self.max_val - self.min_val)


class Clip(ASTNode):
    """
    Clip value to [min_val, max_val].
    """

    def __init__(self, expr: ASTNode, min_val: float, max_val: float):
        self.expr = expr
        self.min_val = min_val
        self.max_val = max_val

    def evaluate(self, state: dict):
        val = self.expr.evaluate(state)
        return max(self.min_val, min(self.max_val, val))


# ============================================================
# Logical Nodes (return bool)
# ============================================================

class Less(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return self.left.evaluate(state) < self.right.evaluate(state)


class Greater(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return self.left.evaluate(state) > self.right.evaluate(state)


class And(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return bool(self.left.evaluate(state)) and bool(self.right.evaluate(state))


class Or(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def evaluate(self, state: dict):
        return bool(self.left.evaluate(state)) or bool(self.right.evaluate(state))


# ============================================================
# Control Flow Nodes
# ============================================================

class If(ASTNode):
    """
    Conditional node.
    """

    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: ASTNode):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def evaluate(self, state: dict):
        if self.condition.evaluate(state):
            return self.then_branch.evaluate(state)
        else:
            return self.else_branch.evaluate(state)


class Choose(ASTNode):
    """
    Discrete choice node.
    Returns one evaluated option.
    """

    def __init__(self, options: list, rng: random.Random):
        """
        options: list of ASTNode
        rng: controlled random generator
        """
        self.options = options
        self.rng = rng

    def evaluate(self, state: dict):
        choice = self.rng.choice(self.options)
        return choice.evaluate(state)


# ============================================================
# Utility
# ============================================================

def evaluate_ast(ast_root: ASTNode, state: dict):
    """
    Helper function to evaluate an AST.
    """
    return ast_root.evaluate(state)
