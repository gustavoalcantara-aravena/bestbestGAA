from typing import Any
from .ast_nodes import Seq, Call, While, If, DestroyRepair, ASTNode, Budget, Condition

def ast_to_ascii(node: ASTNode, prefix: str = "", is_last: bool = True) -> str:
    head = getattr(node, "type", node.__class__.__name__)
    extra = ""

    if isinstance(node, Call):
        extra = f":{node.name}"
        if node.args:
            extra += f"{node.args}"
    elif isinstance(node, While):
        extra = f"({node.budget.kind}={node.budget.value})"
    elif isinstance(node, If):
        extra = f"(cond={node.cond.type})"

    branch = "└── " if is_last else "├── "
    s = f"{prefix}{branch}{head}{extra}\n"

    kids = []
    if isinstance(node, Seq):
        kids = node.body
    elif isinstance(node, While):
        kids = [node.body]
    elif isinstance(node, If):
        kids = [node.then_branch, node.else_branch]
    elif isinstance(node, DestroyRepair):
        kids = [node.destroy, node.repair]

    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, k in enumerate(kids):
        s += ast_to_ascii(k, new_prefix, i == len(kids) - 1)
    return s


def ast_to_pseudocode(seed: int = 0) -> str:
    # Por ahora devolvemos una plantilla estándar (suficiente para reportes).
    # Luego, si quieres, lo hacemos "AST->pseudocódigo" completo.
    return f"""Algoritmo ILS-GAA-GCP (seed={seed})

1: S ← DSATUR(G)
2: λ ← UpdatePenalty(S)
3: repetir por un presupuesto:
4:     aplicar RecolorVertex / búsqueda local
5:     si mejora: actualizar mejor
6:     si no: DestroyRepair(Ruin(k), GreedyRepair)
7: fin repetir
8: retornar mejor solución
"""
