"""
============================================================
AST Printer
GRASP + GAA for VRPTW (Solomon)
============================================================

Responsibilities:
- Pretty-print AST structure (ASCII tree)
- Generate human-readable pseudocode
- Deterministic output (no randomness)
- Debugging & thesis-ready representation
"""

from typing import Dict, Any, List


# ============================================================
# Public API
# ============================================================

def print_ast_tree(ast_json: Dict[str, Any]) -> str:
    """
    Returns an ASCII tree representation of the AST.
    """
    lines: List[str] = []
    _print_tree_rec(ast_json, prefix="", is_last=True, out=lines)
    return "\n".join(lines)


def print_ast_pseudocode(ast_json: Dict[str, Any], indent: int = 0) -> str:
    """
    Returns readable pseudocode representation of the AST.
    """
    return _print_pseudocode_rec(ast_json, indent)


# ============================================================
# Tree Printer (ASCII)
# ============================================================

def _print_tree_rec(node: Dict[str, Any], prefix: str, is_last: bool, out: List[str]):
    connector = "└── " if is_last else "├── "
    node_label = _node_label(node)
    out.append(prefix + connector + node_label)

    children = _children(node)
    if not children:
        return

    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(children):
        _print_tree_rec(
            child,
            prefix=new_prefix,
            is_last=(i == len(children) - 1),
            out=out
        )


def _node_label(node: Dict[str, Any]) -> str:
    t = node.get("type", "UNKNOWN")

    if t == "Feature":
        return f"Feature({node['name']})"

    if t == "Const":
        return f"Const({node['value']})"

    if t == "WeightedSum":
        return f"WeightedSum[{len(node['terms'])}]"

    if t == "Normalize":
        return f"Normalize(min={node.get('min','-')}, max={node.get('max','-')})"

    if t == "Clip":
        return f"Clip(min={node['min']}, max={node['max']})"

    if t == "Choose":
        return f"Choose[{len(node['options'])}]"

    return t


def _children(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    t = node["type"]

    if t in {"Add", "Sub", "Mul", "Div", "Less", "Greater", "And", "Or"}:
        return [node["left"], node["right"]]

    if t == "If":
        return [node["condition"], node["then"], node["else"]]

    if t == "WeightedSum":
        return [term["expr"] for term in node["terms"]]

    if t in {"Normalize", "Clip"}:
        return [node["expr"]]

    if t == "Choose":
        return node["options"]

    return []


# ============================================================
# Pseudocode Printer
# ============================================================

def _print_pseudocode_rec(node: Dict[str, Any], indent: int) -> str:
    pad = "    " * indent
    t = node["type"]

    # ----- Terminals -----
    if t == "Feature":
        return pad + node["name"]

    if t == "Const":
        return pad + repr(node["value"])

    # ----- Arithmetic -----
    if t == "Add":
        return pad + f"({_pc(node['left'])} + {_pc(node['right'])})"

    if t == "Sub":
        return pad + f"({_pc(node['left'])} - {_pc(node['right'])})"

    if t == "Mul":
        return pad + f"({_pc(node['left'])} * {_pc(node['right'])})"

    if t == "Div":
        return pad + f"({_pc(node['left'])} / {_pc(node['right'])})"

    # ----- Aggregation -----
    if t == "WeightedSum":
        terms = []
        for term in node["terms"]:
            w = term["weight"]
            expr = _pc(term["expr"])
            terms.append(f"{w} * {expr}")
        return pad + "(" + " + ".join(terms) + ")"

    if t == "Normalize":
        expr = _pc(node["expr"])
        mn = node.get("min", 0.0)
        mx = node.get("max", 1.0)
        return pad + f"normalize({expr}, min={mn}, max={mx})"

    if t == "Clip":
        expr = _pc(node["expr"])
        return pad + f"clip({expr}, min={node['min']}, max={node['max']})"

    # ----- Logic -----
    if t == "Less":
        return pad + f"({_pc(node['left'])} < {_pc(node['right'])})"

    if t == "Greater":
        return pad + f"({_pc(node['left'])} > {_pc(node['right'])})"

    if t == "And":
        return pad + f"({_pc(node['left'])} AND {_pc(node['right'])})"

    if t == "Or":
        return pad + f"({_pc(node['left'])} OR {_pc(node['right'])})"

    # ----- Control -----
    if t == "If":
        cond = _pc(node["condition"])
        then = _print_pseudocode_rec(node["then"], indent + 1)
        els = _print_pseudocode_rec(node["else"], indent + 1)
        return (
            pad + f"IF {cond}:\n"
            f"{then}\n"
            f"{pad}ELSE:\n"
            f"{els}"
        )

    if t == "Choose":
        opts = ", ".join(_pc(o) for o in node["options"])
        return pad + f"CHOOSE({opts})"

    return pad + f"<UNKNOWN {t}>"


def _pc(node: Dict[str, Any]) -> str:
    """
    Inline pseudocode (no indentation).
    """
    return _print_pseudocode_rec(node, indent=0).strip()
