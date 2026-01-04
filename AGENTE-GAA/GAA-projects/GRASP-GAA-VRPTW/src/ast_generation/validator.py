"""
============================================================
AST Validator
GRASP + GAA for VRPTW (Solomon)
============================================================
Validates JSON ASTs BEFORE parsing/execution.

Checks:
- max depth (real)
- max functional/internal nodes (real)
- allowed node types only
- features existence (phase-aware)
- return type compatibility (numeric vs operator string)
- total node count (optional bloat safeguard)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Set, Tuple, Optional, Union


# ============================================================
# Validation Result
# ============================================================

@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    stats: Dict[str, Any]


# ============================================================
# Validator Config
# ============================================================

@dataclass
class ASTValidationConfig:
    max_depth: int
    max_function_nodes: int
    max_total_nodes: int = 64  # safety cap
    allowed_node_types: Optional[Set[str]] = None


# ============================================================
# Node Type Sets (default whitelist)
# ============================================================

DEFAULT_ALLOWED_NODE_TYPES: Set[str] = {
    # terminals
    "Feature",
    "Const",

    # arithmetic
    "Add",
    "Sub",
    "Mul",
    "Div",

    # aggregation
    "WeightedSum",
    "Normalize",
    "Clip",

    # logic
    "Less",
    "Greater",
    "And",
    "Or",

    # control
    "If",
    "Choose",
}


# "Functional" nodes = internal nodes that contribute to structure (bloat control)
DEFAULT_FUNCTIONAL_NODE_TYPES: Set[str] = {
    "Add", "Sub", "Mul", "Div",
    "WeightedSum", "Normalize", "Clip",
    "Less", "Greater", "And", "Or",
    "If", "Choose"
}


# ============================================================
# Type System (very light)
# ============================================================

# In this project we only need three return kinds:
RET_NUM = "num"          # float/int
RET_BOOL = "bool"        # True/False
RET_STR = "str"          # operator names for LS


# ============================================================
# Validator
# ============================================================

class ASTValidator:
    """
    Validates JSON AST nodes against constraints and phase expectations.
    """

    def __init__(
        self,
        config: ASTValidationConfig,
        construction_feature_names: Set[str],
        local_search_feature_names: Set[str],
        allowed_operator_values: Set[str]
    ):
        self.cfg = config
        self.allowed_node_types = config.allowed_node_types or DEFAULT_ALLOWED_NODE_TYPES
        self.functional_types = DEFAULT_FUNCTIONAL_NODE_TYPES

        self.construction_features = construction_feature_names
        self.ls_features = local_search_feature_names
        self.allowed_ops = allowed_operator_values

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def validate_construction_ast(self, ast_json: Dict[str, Any]) -> ValidationResult:
        """
        Construction AST must evaluate to numeric.
        """
        return self._validate(
            ast_json=ast_json,
            phase="construction",
            expected_return=RET_NUM
        )

    def validate_ls_operator_ast(self, ast_json: Dict[str, Any]) -> ValidationResult:
        """
        Local Search operator AST must evaluate to string in allowed operators.
        """
        return self._validate(
            ast_json=ast_json,
            phase="local_search",
            expected_return=RET_STR
        )

    # --------------------------------------------------------
    # Core validation
    # --------------------------------------------------------

    def _validate(self, ast_json: Dict[str, Any], phase: str, expected_return: str) -> ValidationResult:
        errors: List[str] = []

        # basic structural checks
        if not isinstance(ast_json, dict):
            return ValidationResult(False, ["AST root must be a dict"], stats={})

        # walk tree and compute stats + validate node types + features
        stats = {
            "total_nodes": 0,
            "functional_nodes": 0,
            "max_depth_real": 0,
            "feature_count": 0,
            "features_used": set(),
            "const_count": 0,
            "node_type_counts": {},
        }

        # recursion: returns inferred return type
        inferred = self._walk(
            node=ast_json,
            phase=phase,
            depth=1,
            errors=errors,
            stats=stats
        )

        # constraints
        if stats["max_depth_real"] > self.cfg.max_depth:
            errors.append(
                f"Depth violation: max_depth_real={stats['max_depth_real']} > max_depth={self.cfg.max_depth}"
            )

        if stats["functional_nodes"] > self.cfg.max_function_nodes:
            errors.append(
                f"Functional nodes violation: functional_nodes={stats['functional_nodes']} > max_function_nodes={self.cfg.max_function_nodes}"
            )

        if stats["total_nodes"] > self.cfg.max_total_nodes:
            errors.append(
                f"Total nodes (bloat) violation: total_nodes={stats['total_nodes']} > max_total_nodes={self.cfg.max_total_nodes}"
            )

        # return type check
        if inferred != expected_return:
            errors.append(
                f"Return type mismatch: inferred={inferred} expected={expected_return} (phase={phase})"
            )

        # if expected is operator string, ensure Const values are valid ops where possible
        if expected_return == RET_STR:
            # We'll check that any Const that appears under Choose or directly is allowed op
            # (strict mode: forbid arbitrary strings)
            bad_ops = self._collect_invalid_operator_consts(ast_json)
            if bad_ops:
                errors.append(f"Invalid operator Const values found: {sorted(bad_ops)}; allowed={sorted(self.allowed_ops)}")

        # convert sets to lists in stats for JSON friendliness
        stats["features_used"] = sorted(list(stats["features_used"]))

        ok = len(errors) == 0
        return ValidationResult(ok, errors, stats)

    # --------------------------------------------------------
    # Walk + infer type
    # --------------------------------------------------------

    def _walk(
        self,
        node: Dict[str, Any],
        phase: str,
        depth: int,
        errors: List[str],
        stats: Dict[str, Any]
    ) -> str:
        """
        Recursively validates node and infers return type.
        """
        stats["total_nodes"] += 1
        stats["max_depth_real"] = max(stats["max_depth_real"], depth)

        if "type" not in node:
            errors.append("Node missing 'type'")
            return "unknown"

        t = node["type"]

        stats["node_type_counts"][t] = stats["node_type_counts"].get(t, 0) + 1

        if t not in self.allowed_node_types:
            errors.append(f"Disallowed node type: {t}")
            return "unknown"

        if t in self.functional_types:
            stats["functional_nodes"] += 1

        # ----- Terminals -----
        if t == "Feature":
            name = node.get("name", None)
            if not isinstance(name, str):
                errors.append("Feature node requires string 'name'")
                return "unknown"

            stats["feature_count"] += 1
            stats["features_used"].add(name)

            if phase == "construction":
                if name not in self.construction_features:
                    errors.append(f"Unknown construction feature: {name}")
            else:
                if name not in self.ls_features:
                    errors.append(f"Unknown local_search feature: {name}")

            # Features are always numeric in our minimal system (bool is built via comparisons)
            return RET_NUM

        if t == "Const":
            stats["const_count"] += 1
            v = node.get("value", None)
            # const can be float/int/bool/str depending on usage
            if isinstance(v, bool):
                return RET_BOOL
            if isinstance(v, (int, float)):
                return RET_NUM
            if isinstance(v, str):
                return RET_STR
            errors.append(f"Const value has unsupported type: {type(v)}")
            return "unknown"

        # ----- Arithmetic -----
        if t in {"Add", "Sub", "Mul", "Div"}:
            left = node.get("left")
            right = node.get("right")
            if left is None or right is None:
                errors.append(f"{t} requires 'left' and 'right' fields")
                return RET_NUM
            lt = self._walk(left, phase, depth + 1, errors, stats)
            rt = self._walk(right, phase, depth + 1, errors, stats)
            if lt != RET_NUM or rt != RET_NUM:
                errors.append(f"{t} requires numeric children; got left={lt}, right={rt}")
            return RET_NUM

        # ----- Aggregation -----
        if t == "WeightedSum":
            terms = node.get("terms", None)
            if not isinstance(terms, list) or len(terms) == 0:
                errors.append("WeightedSum requires non-empty 'terms' list")
                return RET_NUM

            for term in terms:
                w = term.get("weight")
                expr = term.get("expr")
                if w is None or expr is None:
                    errors.append("WeightedSum term requires 'weight' and 'expr'")
                    continue
                if not isinstance(w, (int, float)):
                    errors.append(f"WeightedSum term weight must be numeric; got {type(w)}")
                et = self._walk(expr, phase, depth + 1, errors, stats)
                if et != RET_NUM:
                    errors.append(f"WeightedSum term expr must be numeric; got {et}")
            return RET_NUM

        if t == "Normalize":
            expr = node.get("expr")
            if expr is None:
                errors.append("Normalize requires 'expr' field")
                return RET_NUM
            et = self._walk(expr, phase, depth + 1, errors, stats)
            if et != RET_NUM:
                errors.append(f"Normalize requires numeric expr; got {et}")
            # min/max are optional; if present should be numeric
            if "min" in node and not isinstance(node["min"], (int, float)):
                errors.append("Normalize 'min' must be numeric")
            if "max" in node and not isinstance(node["max"], (int, float)):
                errors.append("Normalize 'max' must be numeric")
            return RET_NUM

        if t == "Clip":
            expr = node.get("expr")
            if expr is None:
                errors.append("Clip requires 'expr' field")
                return RET_NUM
            et = self._walk(expr, phase, depth + 1, errors, stats)
            if et != RET_NUM:
                errors.append(f"Clip requires numeric expr; got {et}")
            if not isinstance(node.get("min", None), (int, float)):
                errors.append("Clip requires numeric 'min'")
            if not isinstance(node.get("max", None), (int, float)):
                errors.append("Clip requires numeric 'max'")
            return RET_NUM

        # ----- Logic / comparisons -----
        if t in {"Less", "Greater"}:
            left = node.get("left")
            right = node.get("right")
            if left is None or right is None:
                errors.append(f"{t} requires 'left' and 'right' fields")
                return RET_BOOL
            lt = self._walk(left, phase, depth + 1, errors, stats)
            rt = self._walk(right, phase, depth + 1, errors, stats)
            if lt != RET_NUM or rt != RET_NUM:
                errors.append(f"{t} requires numeric children; got left={lt}, right={rt}")
            return RET_BOOL

        if t in {"And", "Or"}:
            left = node.get("left")
            right = node.get("right")
            if left is None or right is None:
                errors.append(f"{t} requires 'left' and 'right' fields")
                return RET_BOOL
            lt = self._walk(left, phase, depth + 1, errors, stats)
            rt = self._walk(right, phase, depth + 1, errors, stats)
            if lt != RET_BOOL or rt != RET_BOOL:
                errors.append(f"{t} requires boolean children; got left={lt}, right={rt}")
            return RET_BOOL

        # ----- Control -----
        if t == "If":
            cond = node.get("condition")
            then_br = node.get("then")
            else_br = node.get("else")
            
            if cond is None or then_br is None or else_br is None:
                errors.append("If requires 'condition', 'then', and 'else' fields")
                return "unknown"
            
            ct = self._walk(cond, phase, depth + 1, errors, stats)
            tt = self._walk(then_br, phase, depth + 1, errors, stats)
            et = self._walk(else_br, phase, depth + 1, errors, stats)

            if ct != RET_BOOL:
                errors.append(f"If condition must be boolean; got {ct}")

            # then/else must have same return kind
            if tt != et:
                errors.append(f"If branches must return same type; then={tt}, else={et}")
                return "unknown"
            return tt

        if t == "Choose":
            options = node.get("options", None)
            if not isinstance(options, list) or len(options) == 0:
                errors.append("Choose requires non-empty 'options' list")
                return "unknown"

            opt_types = []
            for opt in options:
                if not isinstance(opt, dict):
                    errors.append(f"Choose option must be a dict; got {type(opt)}")
                    continue
                opt_types.append(self._walk(opt, phase, depth + 1, errors, stats))

            # all options must have same type
            if len(opt_types) == 0:
                return "unknown"
            first = opt_types[0]
            if any(ot != first for ot in opt_types):
                errors.append(f"Choose options must have same type; got {opt_types}")
                return "unknown"
            return first

        # Should never reach here (whitelist exhausts)
        errors.append(f"Unhandled node type: {t}")
        return "unknown"

    # --------------------------------------------------------
    # Operator Const validity check
    # --------------------------------------------------------

    def _collect_invalid_operator_consts(self, ast_json: Dict[str, Any]) -> Set[str]:
        """
        Collect string Const values that are not allowed operators.
        Strict: any Const(str) is assumed to be an operator name and must be allowed.
        If you later allow other strings, relax this logic.
        """
        bad: Set[str] = set()

        def rec(n: Any):
            if isinstance(n, dict):
                t = n.get("type")
                if t == "Const" and isinstance(n.get("value"), str):
                    v = n["value"]
                    if v not in self.allowed_ops:
                        bad.add(v)
                # walk all dict children
                for k, v in n.items():
                    if k == "type":
                        continue
                    rec(v)
            elif isinstance(n, list):
                for x in n:
                    rec(x)

        rec(ast_json)
        return bad
