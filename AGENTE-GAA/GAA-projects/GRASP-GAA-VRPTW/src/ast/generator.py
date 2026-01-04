"""
============================================================
Random AST Generator (JSON + Executable AST)
GRASP + GAA for VRPTW (Solomon)
============================================================
Generates:
- Construction AST: numeric expression for insertion scoring
- Local Search Operator AST: categorical decision among operators
With constraints:
- max_depth
- max_function_nodes (internal nodes)
- type correctness (numeric/bool/categorical)

This module outputs JSON dictionaries (serializable) and can
also parse them into executable nodes via ASTParser.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple, Optional
import json
import hashlib
import random

from .parser import ASTParser
from .generator_config import (
    CONSTRUCTION_FEATURES,
    LOCAL_SEARCH_FEATURES,
    LOCAL_SEARCH_OPERATORS,
    GenLimits as ConfigGenLimits,
)


# ============================================================
# Utilities
# ============================================================

def stable_signature(obj: Dict[str, Any]) -> str:
    """
    Stable hash of a JSON-serializable dict (sorted keys).
    """
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


@dataclass
class GenLimits:
    max_depth: int
    max_function_nodes: int


@dataclass
class GenContext:
    rng: random.Random
    limits: GenLimits

    # counters
    function_nodes_used: int = 0

    def can_add_function_node(self) -> bool:
        return self.function_nodes_used < self.limits.max_function_nodes

    def add_function_node(self) -> None:
        self.function_nodes_used += 1


# ============================================================
# Generator
# ============================================================

class RandomASTGenerator:
    """
    Generates AST JSON dicts with type correctness and constraints.
    
    Simple constructor:
        gen = RandomASTGenerator(seed=42)
    
    Usage:
        ast = gen.generate(phase="construction", seed=42)
    """

    # Node type pools (by return type)
    NUM_BINOPS = ["Add", "Sub", "Mul", "Div"]
    BOOL_BINOPS = ["And", "Or"]
    BOOL_CMPOPS = ["Less", "Greater"]

    def __init__(
        self,
        seed: int = 42,
        construction_features: Optional[List[str]] = None,
        ls_features: Optional[List[str]] = None,
        ls_operators: Optional[List[str]] = None,
        max_depth: int = 10,
        max_function_nodes: int = 50,
    ):
        """
        Simple constructor with sensible defaults.
        
        Args:
            seed: Random seed for reproducibility
            construction_features: Features for construction phase (default: CONSTRUCTION_FEATURES)
            ls_features: Features for local search phase (default: LOCAL_SEARCH_FEATURES)
            ls_operators: Operators for local search (default: LOCAL_SEARCH_OPERATORS)
            max_depth: Maximum AST depth
            max_function_nodes: Maximum internal (functional) nodes
        """
        self.seed = seed
        self.rng = random.Random(seed)
        self.construction_features = construction_features or CONSTRUCTION_FEATURES
        self.ls_features = ls_features or LOCAL_SEARCH_FEATURES
        self.ls_operators = ls_operators or LOCAL_SEARCH_OPERATORS
        
        self.limits = GenLimits(
            max_depth=max_depth,
            max_function_nodes=max_function_nodes
        )
        self.const_float_range = (-5.0, 5.0)

    # ========================================================
    # Public API
    # ========================================================

    def generate_algorithm_json(self, algorithm_id: str, seed: int) -> Dict[str, Any]:
        """
        Returns a full algorithm package with two ASTs:
        - construction_ast: numeric scoring expression
        - ls_operator_ast: operator selection decision
        plus metadata and signatures.
        """
        ctx1 = GenContext(rng=self._spawn_rng(seed, salt="construction"), limits=self.limits)
        construction_ast = self._gen_numeric_expr(ctx1, depth=0, feature_pool=self.construction_features)

        ctx2 = GenContext(rng=self._spawn_rng(seed, salt="ls_operator"), limits=self.limits)
        ls_operator_ast = self._gen_operator_selector(ctx2, depth=0)

        algo = {
            "algorithm_id": algorithm_id,
            "seed": seed,
            "max_depth": self.limits.max_depth,
            "max_function_nodes": self.limits.max_function_nodes,
            "construction_ast": construction_ast,
            "ls_operator_ast": ls_operator_ast,
        }

        algo["construction_signature"] = stable_signature(construction_ast)
        algo["ls_operator_signature"] = stable_signature(ls_operator_ast)
        algo["ast_signature"] = stable_signature({
            "construction": construction_ast,
            "ls_operator": ls_operator_ast
        })

        # Helpful debug metadata
        algo["meta"] = {
            "construction_function_nodes_used": ctx1.function_nodes_used,
            "ls_function_nodes_used": ctx2.function_nodes_used,
            "ls_operator_set": self.ls_operators
        }

        return algo

    def build_executable(self, algorithm_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses JSON ASTs into executable objects using ASTParser.
        Returns dict with 'construction_root' and 'ls_operator_root'.
        """
        parser = ASTParser(rng=self.rng)  # controlled rng for Choose in execution
        return {
            "construction_root": parser.parse(algorithm_json["construction_ast"]),
            "ls_operator_root": parser.parse(algorithm_json["ls_operator_ast"]),
        }

    # ========================================================
    # RNG helpers
    # ========================================================

    def _spawn_rng(self, seed: int, salt: str) -> random.Random:
        """
        Derive a deterministic RNG from (seed, salt) without affecting global rng.
        """
        mix = f"{seed}:{salt}".encode("utf-8")
        derived = int(hashlib.sha256(mix).hexdigest()[:8], 16)
        return random.Random(derived)

    # ========================================================
    # Generation: Numeric Expression (Construction score)
    # ========================================================

    def _gen_numeric_expr(self, ctx: GenContext, depth: int, feature_pool: List[str]) -> Dict[str, Any]:
        """
        Generates a numeric expression AST.
        Ensures type correctness: returns float.
        """
        # Forced leaf if depth limit reached or no internal nodes remaining
        if depth >= ctx.limits.max_depth or not ctx.can_add_function_node():
            return self._gen_numeric_leaf(ctx, feature_pool)

        # Decide node type: WeightedSum, If (numeric), or binary op
        choices = ["WeightedSum", "If", "BinOp", "Leaf"]
        # Bias towards leaves at deeper levels
        if depth >= ctx.limits.max_depth - 1:
            weights = [0.25, 0.15, 0.20, 0.40]
        else:
            weights = [0.35, 0.20, 0.25, 0.20]

        pick = self._weighted_choice(ctx.rng, choices, weights)

        if pick == "Leaf":
            return self._gen_numeric_leaf(ctx, feature_pool)

        if pick == "WeightedSum":
            ctx.add_function_node()
            return self._gen_weighted_sum(ctx, depth, feature_pool)

        if pick == "If":
            ctx.add_function_node()
            cond = self._gen_bool_expr(ctx, depth + 1, feature_pool=self._bool_feature_pool(depth, phase="construction"))
            then_expr = self._gen_numeric_expr(ctx, depth + 1, feature_pool)
            else_expr = self._gen_numeric_expr(ctx, depth + 1, feature_pool)
            return {
                "type": "If",
                "condition": cond,
                "then": then_expr,
                "else": else_expr
            }

        # BinOp
        ctx.add_function_node()
        op = ctx.rng.choice(self.NUM_BINOPS)
        left = self._gen_numeric_expr(ctx, depth + 1, feature_pool)
        right = self._gen_numeric_expr(ctx, depth + 1, feature_pool)
        return {
            "type": op,
            "left": left,
            "right": right
        }

    def _gen_numeric_leaf(self, ctx: GenContext, feature_pool: List[str]) -> Dict[str, Any]:
        """
        Numeric leaf: either Feature or Const(float)
        """
        if feature_pool and ctx.rng.random() < 0.70:
            return {"type": "Feature", "name": ctx.rng.choice(feature_pool)}
        # constant
        lo, hi = self.const_float_range
        val = ctx.rng.uniform(lo, hi)
        return {"type": "Const", "value": float(val)}

    def _gen_weighted_sum(self, ctx: GenContext, depth: int, feature_pool: List[str]) -> Dict[str, Any]:
        """
        WeightedSum with 2..4 terms.
        """
        num_terms = ctx.rng.randint(2, 4)
        terms = []
        for _ in range(num_terms):
            w = ctx.rng.uniform(-5.0, 5.0)
            expr = self._gen_numeric_expr(ctx, depth + 1, feature_pool)
            terms.append({"weight": float(w), "expr": expr})
        return {"type": "WeightedSum", "terms": terms}

    # ========================================================
    # Generation: Boolean Expressions (Conditions)
    # ========================================================

    def _gen_bool_expr(self, ctx: GenContext, depth: int, feature_pool: List[str]) -> Dict[str, Any]:
        """
        Generates a boolean expression AST.
        """
        if depth >= ctx.limits.max_depth or not ctx.can_add_function_node():
            return self._gen_bool_leaf(ctx, feature_pool)

        choices = ["Cmp", "Logic", "Leaf"]
        weights = [0.50, 0.25, 0.25] if depth < ctx.limits.max_depth - 1 else [0.60, 0.15, 0.25]
        pick = self._weighted_choice(ctx.rng, choices, weights)

        if pick == "Leaf":
            return self._gen_bool_leaf(ctx, feature_pool)

        if pick == "Logic":
            ctx.add_function_node()
            op = ctx.rng.choice(self.BOOL_BINOPS)
            left = self._gen_bool_expr(ctx, depth + 1, feature_pool)
            right = self._gen_bool_expr(ctx, depth + 1, feature_pool)
            return {"type": op, "left": left, "right": right}

        # Cmp
        ctx.add_function_node()
        op = ctx.rng.choice(self.BOOL_CMPOPS)
        # Compare numeric subexpressions
        left = self._gen_numeric_expr(ctx, depth + 1, feature_pool=self._numeric_feature_pool_for_cmp(feature_pool))
        right = self._gen_numeric_expr(ctx, depth + 1, feature_pool=self._numeric_feature_pool_for_cmp(feature_pool))
        return {"type": op, "left": left, "right": right}

    def _gen_bool_leaf(self, ctx: GenContext, feature_pool: List[str]) -> Dict[str, Any]:
        """
        Boolean leaf. We avoid raw boolean features unless you explicitly include them.
        Default: compare a feature against a constant.
        """
        # Compare Feature(name) > Const(threshold)
        if feature_pool:
            f = ctx.rng.choice(feature_pool)
        else:
            f = "iterations_no_improve"  # safe fallback if present in LS state

        threshold = ctx.rng.uniform(0.0, 20.0)
        cmp_type = ctx.rng.choice(["Greater", "Less"])
        return {
            "type": cmp_type,
            "left": {"type": "Feature", "name": f},
            "right": {"type": "Const", "value": float(threshold)}
        }

    # Pools for conditions (phase-aware)
    def _bool_feature_pool(self, depth: int, phase: str) -> List[str]:
        """
        Feature pool to build boolean comparisons.
        We choose a subset that tends to be meaningful and stable.
        """
        if phase == "construction":
            # features that exist in InsertionState and are numeric
            return [
                "route_length",
                "route_load",
                "route_capacity_remaining",
                "route_current_time",
                "route_total_waiting",
                "route_slack_forward",
                "cust_demand",
                "cust_ready_time",
                "cust_due_time",
                "cust_service_time",
                "delta_distance",
                "delta_time",
                "delta_waiting",
                "capacity_violation",
                "time_violation",
                "urgency",
                "relative_slack",
                "load_ratio",
                "num_customers_remaining",
                "num_routes_current"
            ]
        # local_search
        return [
            "num_routes",
            "total_distance",
            "penalty_value",
            "avg_route_length",
            "min_route_length",
            "max_route_length",
            "avg_route_load_ratio",
            "min_route_slack",
            "num_time_violations",
            "num_capacity_violations",
            "ls_iteration",
            "iterations_no_improve",
            "last_improvement_delta"
        ]

    def _numeric_feature_pool_for_cmp(self, feature_pool: List[str]) -> List[str]:
        # For comparisons we can reuse same pool; keep it bounded
        if not feature_pool:
            return []
        # sample a subset to reduce overfitting/bloat
        return feature_pool[: min(len(feature_pool), 10)]

    # ========================================================
    # Generation: Local Search Operator Selector (Categorical)
    # ========================================================

    def _gen_operator_selector(self, ctx: GenContext, depth: int) -> Dict[str, Any]:
        """
        Returns an AST that evaluates to a string operator name.
        Uses If + Choose + Const("operator").
        """
        # If at depth limit or no internal nodes left -> simple Choose
        if depth >= ctx.limits.max_depth or not ctx.can_add_function_node():
            return self._gen_choose_operator(ctx)

        # Decide between If or Choose
        if ctx.rng.random() < 0.60:
            ctx.add_function_node()
            cond = self._gen_bool_expr(ctx, depth + 1, feature_pool=self._bool_feature_pool(depth, phase="local_search"))
            then_branch = self._gen_operator_selector(ctx, depth + 1)
            else_branch = self._gen_operator_selector(ctx, depth + 1)
            return {
                "type": "If",
                "condition": cond,
                "then": then_branch,
                "else": else_branch
            }

        # Choose
        ctx.add_function_node()
        return self._gen_choose_operator(ctx)

    def _gen_choose_operator(self, ctx: GenContext) -> Dict[str, Any]:
        """
        Choose among enabled operators with weighted selection.
        
        Returns: 
        {
            "type": "Choose",
            "options": [
                {"weight": 0.3, "value": "TwoOpt"},
                {"weight": 0.5, "value": "Relocate"},
                ...
            ]
        }
        """
        ops = list(self.ls_operators)
        if not ops:
            ops = ["relocate"]  # safe fallback

        # Choose 2..min(4, len(ops)) operators
        k = ctx.rng.randint(2, min(4, len(ops)))
        chosen_ops = ctx.rng.sample(ops, k)
        
        # Assign random weights and normalize
        weights = [ctx.rng.uniform(0.1, 5.0) for _ in chosen_ops]
        weight_sum = sum(weights)
        normalized_weights = [w / weight_sum for w in weights]
        
        # Build options list with weights
        options = [
            {"weight": float(w), "value": str(op)}
            for op, w in zip(chosen_ops, normalized_weights)
        ]

        return {
            "type": "Choose",
            "options": options
        }

    # ========================================================
    # Weighted choice
    # ========================================================

    @staticmethod
    def _weighted_choice(rng: random.Random, items: List[str], weights: List[float]) -> str:
        """
        rng-based weighted choice (no numpy).
        """
        assert len(items) == len(weights)
        total = sum(weights)
        r = rng.uniform(0, total)
        acc = 0.0
        for item, w in zip(items, weights):
            acc += w
            if r <= acc:
                return item
        return items[-1]

    # ========================================================
    # Public wrapper: generate() for phase-based generation
    # ========================================================

    def generate(self, phase: str, seed: int) -> Dict[str, Any]:
        """
        Wrapper method to generate AST for a specific phase.
        
        Args:
            phase: "construction" for numeric scoring AST, 
                   "local_search" for operator selector AST
            seed: Random seed for deterministic generation
        
        Returns:
            JSON-serializable AST dict
        """
        ctx = GenContext(rng=self._spawn_rng(seed, salt=phase), limits=self.limits)
        
        if phase == "construction":
            return self._gen_numeric_expr(ctx, depth=0, feature_pool=self.construction_features)
        
        if phase == "local_search":
            return self._gen_operator_selector(ctx, depth=0)
        
        raise ValueError(f"Invalid phase: {phase}. Use 'construction' or 'local_search'.")