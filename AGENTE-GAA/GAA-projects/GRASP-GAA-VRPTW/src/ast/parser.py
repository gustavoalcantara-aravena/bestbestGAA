# src/ast/parser.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import random


class ASTRuntimeError(RuntimeError):
    pass


class Node:
    """Base class for AST nodes that can be evaluated."""
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> Any:
        """
        Evaluate this node with given state.
        
        Args:
            state: Dictionary of features and values
            rng: Optional RNG for stochastic operators (Choose)
        
        Returns:
            float (for numeric nodes) or str (for operator selectors)
        """
        raise NotImplementedError


class ASTParser:
    """
    Parses JSON AST dicts into executable Node objects.
    Does NOT validate structure: assumes AST is already validated.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        """
        Args:
            rng: RNG for stochastic choices (Choose nodes)
        """
        self.rng = rng or random.Random()

    # =====================================================
    # Public API
    # =====================================================

    def parse(self, ast: Dict[str, Any]) -> Node:
        """
        Parse JSON AST into executable Node.
        
        Args:
            ast: JSON dict representing AST
        
        Returns:
            Node object with evaluate() method
        """
        return self._parse_node(ast)

    def evaluate(self, ast: Dict[str, Any], state: Dict[str, Any], rng: Optional[random.Random] = None) -> Any:
        """
        Legacy method: evaluate JSON AST directly (old API).
        
        Args:
            ast: JSON dict
            state: Feature state dict
            rng: Optional RNG for Choose nodes
        
        Returns:
            float or str
        """
        if rng is None:
            rng = self.rng
            
        if not isinstance(ast, dict):
            raise ASTRuntimeError("AST node must be dict")

        t = ast.get("type")
        if t is None:
            raise ASTRuntimeError("AST node missing 'type'")

        # -----------------------
        # Terminals
        # -----------------------

        if t == "Feature":
            name = ast.get("name")
            if name not in state:
                raise ASTRuntimeError(f"Feature '{name}' missing in state")
            return state[name]

        if t == "Const":
            return ast.get("value")

        # -----------------------
        # Arithmetic
        # -----------------------

        if t == "Add":
            return self._num(ast, "left", state, rng) + self._num(ast, "right", state, rng)

        if t == "Sub":
            return self._num(ast, "left", state, rng) - self._num(ast, "right", state, rng)

        if t == "Mul":
            return self._num(ast, "left", state, rng) * self._num(ast, "right", state, rng)

        if t == "Div":
            denom = self._num(ast, "right", state, rng)
            return 0.0 if abs(denom) < 1e-12 else self._num(ast, "left", state, rng) / denom

        # -----------------------
        # Aggregation
        # -----------------------

        if t == "WeightedSum":
            total = 0.0
            for term in ast.get("terms", []):
                w = float(term["weight"])
                x = float(self.evaluate(term["expr"], state, rng))
                total += w * x
            return total

        if t == "Normalize":
            x = self._num(ast, "expr", state, rng)
            lo = ast.get("min", 0.0)
            hi = ast.get("max", 1.0)
            if hi <= lo:
                return 0.0
            return max(0.0, min(1.0, (x - lo) / (hi - lo)))

        if t == "Clip":
            x = self._num(ast, "expr", state, rng)
            return max(ast["min"], min(ast["max"], x))

        # -----------------------
        # Logic / comparisons
        # -----------------------

        if t == "Less":
            return self._num(ast, "left", state, rng) < self._num(ast, "right", state, rng)

        if t == "Greater":
            return self._num(ast, "left", state, rng) > self._num(ast, "right", state, rng)

        if t == "And":
            return bool(self.evaluate(ast["left"], state, rng)) and bool(self.evaluate(ast["right"], state, rng))

        if t == "Or":
            return bool(self.evaluate(ast["left"], state, rng)) or bool(self.evaluate(ast["right"], state, rng))

        # -----------------------
        # Control
        # -----------------------

        if t == "If":
            cond = bool(self.evaluate(ast["condition"], state, rng))
            return self.evaluate(ast["then"], state, rng) if cond else self.evaluate(ast["else"], state, rng)

        if t == "Choose":
            options = ast.get("options", [])
            if not options:
                raise ASTRuntimeError("Choose node with empty options")
            
            # Weighted selection based on option weights
            weights = [opt.get("weight", 1.0) for opt in options]
            values = [opt.get("value") for opt in options]
            
            # Use rng.choices for weighted sampling
            selected = rng.choices(values, weights=weights, k=1)[0]
            return selected

        raise ASTRuntimeError(f"Unsupported AST node type at runtime: {t}")

    # =====================================================
    # Helpers
    # =====================================================

    def _num(self, node: Dict[str, Any], key: str, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        """Extract and evaluate numeric subexpression."""
        if rng is None:
            rng = self.rng
            
        if key not in node:
            raise ASTRuntimeError(f"Missing '{key}' in node {node['type']}")
        return float(self.evaluate(node[key], state, rng))

    def _parse_node(self, ast: Dict[str, Any]) -> Node:
        """
        Parse a JSON AST node into corresponding Node class.
        
        This method creates concrete Node subclasses from JSON.
        Each subclass implements evaluate(state) -> value
        """
        if not isinstance(ast, dict) or "type" not in ast:
            raise ASTRuntimeError("Invalid node: must be dict with 'type' field")
        
        node_type = ast["type"]
        
        # Terminals
        if node_type == "Const":
            return ConstNode(ast.get("value"))
        
        if node_type == "Feature":
            return FeatureNode(ast.get("name"))
        
        # Arithmetic
        if node_type == "Add":
            return AddNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "Sub":
            return SubNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "Mul":
            return MulNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "Div":
            return DivNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        # Aggregation
        if node_type == "WeightedSum":
            terms = [(t["weight"], self._parse_node(t["expr"])) for t in ast.get("terms", [])]
            return WeightedSumNode(terms)
        
        if node_type == "Normalize":
            return NormalizeNode(
                self._parse_node(ast["expr"]),
                ast.get("min", 0.0),
                ast.get("max", 1.0)
            )
        
        if node_type == "Clip":
            return ClipNode(
                self._parse_node(ast["expr"]),
                ast.get("min", 0.0),
                ast.get("max", 1.0)
            )
        
        # Logic
        if node_type == "Less":
            return LessNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "Greater":
            return GreaterNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "And":
            return AndNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        if node_type == "Or":
            return OrNode(self._parse_node(ast["left"]), self._parse_node(ast["right"]))
        
        # Control
        if node_type == "If":
            return IfNode(
                self._parse_node(ast["condition"]),
                self._parse_node(ast["then"]),
                self._parse_node(ast["else"])
            )
        
        if node_type == "Choose":
            options = ast.get("options", [])
            parsed_options = [
                (opt.get("weight", 1.0), opt.get("value"))
                for opt in options
            ]
            return ChooseNode(parsed_options, self.rng)
        
        raise ASTRuntimeError(f"Unknown node type: {node_type}")


# ============================================================
# Node Classes (One per AST type)
# ============================================================

class ConstNode(Node):
    def __init__(self, value):
        self.value = float(value) if value is not None else 0.0
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        return self.value


class FeatureNode(Node):
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        if self.name not in state:
            raise ASTRuntimeError(f"Feature '{self.name}' not in state")
        return float(state[self.name])


class AddNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        return self.left.evaluate(state, rng) + self.right.evaluate(state, rng)


class SubNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        return self.left.evaluate(state, rng) - self.right.evaluate(state, rng)


class MulNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        return self.left.evaluate(state, rng) * self.right.evaluate(state, rng)


class DivNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        denom = self.right.evaluate(state, rng)
        return 0.0 if abs(denom) < 1e-12 else self.left.evaluate(state, rng) / denom


class WeightedSumNode(Node):
    def __init__(self, terms: List[tuple]):
        """terms: list of (weight, Node) tuples"""
        self.terms = terms
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        total = 0.0
        for weight, node in self.terms:
            val = node.evaluate(state, rng)
            total += weight * val
        return total


class NormalizeNode(Node):
    def __init__(self, expr: Node, min_val: float, max_val: float):
        self.expr = expr
        self.min_val = min_val
        self.max_val = max_val
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        x = self.expr.evaluate(state, rng)
        if self.max_val <= self.min_val:
            return 0.0
        return max(0.0, min(1.0, (x - self.min_val) / (self.max_val - self.min_val)))


class ClipNode(Node):
    def __init__(self, expr: Node, min_val: float, max_val: float):
        self.expr = expr
        self.min_val = min_val
        self.max_val = max_val
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> float:
        x = self.expr.evaluate(state, rng)
        return max(self.min_val, min(self.max_val, x))


class LessNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> bool:
        return self.left.evaluate(state, rng) < self.right.evaluate(state, rng)


class GreaterNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> bool:
        return self.left.evaluate(state, rng) > self.right.evaluate(state, rng)


class AndNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> bool:
        return bool(self.left.evaluate(state, rng)) and bool(self.right.evaluate(state, rng))


class OrNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> bool:
        return bool(self.left.evaluate(state, rng)) or bool(self.right.evaluate(state, rng))


class IfNode(Node):
    def __init__(self, condition: Node, then_node: Node, else_node: Node):
        self.condition = condition
        self.then_node = then_node
        self.else_node = else_node
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> Any:
        cond = bool(self.condition.evaluate(state, rng))
        if cond:
            return self.then_node.evaluate(state, rng)
        else:
            return self.else_node.evaluate(state, rng)


class ChooseNode(Node):
    def __init__(self, options: List[tuple], rng: Optional[random.Random] = None):
        """
        options: list of (weight, value) tuples
        rng: RNG for weighted selection
        """
        self.options = options
        self.rng = rng or random.Random()
    
    def evaluate(self, state: Dict[str, Any], rng: Optional[random.Random] = None) -> str:
        if not self.options:
            raise ASTRuntimeError("Choose node with no options")
        
        if rng is None:
            rng = self.rng
        
        weights = [opt[0] for opt in self.options]
        values = [opt[1] for opt in self.options]
        
        selected = rng.choices(values, weights=weights, k=1)[0]
        return str(selected)
