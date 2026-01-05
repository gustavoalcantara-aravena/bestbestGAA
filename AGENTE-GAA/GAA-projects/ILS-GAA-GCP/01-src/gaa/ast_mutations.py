import random
from copy import deepcopy
from typing import List, Tuple, Optional

from ..core.ast_nodes import Seq, Call, While, If, DestroyRepair, ASTNode, Budget, Condition


TERMINALS = ["DSATUR", "UpdatePenalty", "RecolorVertex", "GreedyRepair"]
# Ruin se maneja aparte porque requiere args={"k":...}


def _collect_calls(node: ASTNode, path=()) -> List[Tuple[Tuple[int, ...], Call]]:
    """
    Retorna lista de (path, CallNode). El path codifica cómo llegar.
    """
    out = []
    if isinstance(node, Call):
        out.append((path, node))

    kids = []
    if isinstance(node, Seq):
        kids = list(enumerate(node.body))
        for i, child in kids:
            out.extend(_collect_calls(child, path + (("Seq", i),)))
    elif isinstance(node, While):
        out.extend(_collect_calls(node.body, path + (("While", 0),)))
    elif isinstance(node, If):
        out.extend(_collect_calls(node.then_branch, path + (("IfThen", 0),)))
        out.extend(_collect_calls(node.else_branch, path + (("IfElse", 0),)))
    elif isinstance(node, DestroyRepair):
        out.extend(_collect_calls(node.destroy, path + (("DRDestroy", 0),)))
        out.extend(_collect_calls(node.repair, path + (("DRRepair", 0),)))

    return out


def _get_ref(root: ASTNode, path: Tuple[Tuple[str, int], ...]):
    """
    Devuelve (parent, key) para poder reemplazar el hijo indicado por path.
    """
    node = root
    parent = None
    key = None
    for tag, idx in path:
        parent = node
        key = (tag, idx)
        if tag == "Seq":
            node = node.body[idx]
        elif tag == "While":
            node = node.body
        elif tag == "IfThen":
            node = node.then_branch
        elif tag == "IfElse":
            node = node.else_branch
        elif tag == "DRDestroy":
            node = node.destroy
        elif tag == "DRRepair":
            node = node.repair
        else:
            raise ValueError(f"Tag path no soportado: {tag}")
    return parent, key


def _replace_child(parent: ASTNode, key, new_child: ASTNode):
    tag, idx = key
    if tag == "Seq":
        parent.body[idx] = new_child
    elif tag == "While":
        parent.body = new_child
    elif tag == "IfThen":
        parent.then_branch = new_child
    elif tag == "IfElse":
        parent.else_branch = new_child
    elif tag == "DRDestroy":
        parent.destroy = new_child
    elif tag == "DRRepair":
        parent.repair = new_child
    else:
        raise ValueError(f"Tag replace no soportado: {tag}")


def mutate_replace_terminal(ast: ASTNode, rng: random.Random) -> ASTNode:
    """
    Reemplaza un Call(name=...) por otro terminal seguro.
    Evitamos romper semántica: DSATUR solo debería estar al inicio, así que lo protegemos.
    """
    new_ast = deepcopy(ast)
    calls = _collect_calls(new_ast)
    if not calls:
        return new_ast

    (path, callnode) = rng.choice(calls)

    # Evitar reemplazar el primer constructor DSATUR (asumimos que es el primer Call del Seq raíz)
    # Si lo cambias, puedes quedar con solución vacía.
    if callnode.name == "DSATUR":
        return new_ast

    # Reemplazo seguro
    options = [t for t in TERMINALS if t != callnode.name and t != "DSATUR"]
    if not options:
        return new_ast

    callnode.name = rng.choice(options)
    callnode.args = None
    return new_ast


def mutate_change_ruin_k(ast: ASTNode, rng: random.Random) -> ASTNode:
    """
    Busca un Call 'Ruin' y cambia su k.
    """
    new_ast = deepcopy(ast)
    calls = _collect_calls(new_ast)
    ruins = [(p, c) for (p, c) in calls if c.name == "Ruin"]
    if not ruins:
        return new_ast

    _, ruin_call = rng.choice(ruins)
    if ruin_call.args is None:
        ruin_call.args = {"k": 5}
    current = int(ruin_call.args.get("k", 5))
    candidates = [3, 5, 8, 12, 20]
    candidates = [x for x in candidates if x != current]
    ruin_call.args["k"] = rng.choice(candidates)
    return new_ast


def mutate_replace_destroyrepair(ast: ASTNode, rng: random.Random) -> ASTNode:
    """
    Reemplaza el bloque DestroyRepair por otro DestroyRepair con parámetros diferentes.
    Esto es una perturbación estructural ligera pero robusta.
    """
    new_ast = deepcopy(ast)

    # Buscar nodos DestroyRepair
    dr_paths = []

    def walk(node: ASTNode, path=()):
        if isinstance(node, DestroyRepair):
            dr_paths.append(path)
        if isinstance(node, Seq):
            for i, ch in enumerate(node.body):
                walk(ch, path + (("Seq", i),))
        elif isinstance(node, While):
            walk(node.body, path + (("While", 0),))
        elif isinstance(node, If):
            walk(node.then_branch, path + (("IfThen", 0),))
            walk(node.else_branch, path + (("IfElse", 0),))
        elif isinstance(node, DestroyRepair):
            walk(node.destroy, path + (("DRDestroy", 0),))
            walk(node.repair, path + (("DRRepair", 0),))

    walk(new_ast)
    if not dr_paths:
        return new_ast

    path = rng.choice(dr_paths)
    parent, key = _get_ref(new_ast, path)

    k_ruin = rng.choice([3, 5, 8, 12, 20])
    replacement = DestroyRepair(
        type="DestroyRepair",
        destroy=Call(type="Call", name="Ruin", args={"k": k_ruin}),
        repair=Call(type="Call", name="GreedyRepair"),
    )

    if parent is None:
        return replacement
    _replace_child(parent, key, replacement)
    return new_ast


def mutate(ast: ASTNode, rng: random.Random) -> ASTNode:
    """
    Mutación aleatoria del vecindario: elige un operador.
    """
    ops = [mutate_replace_terminal, mutate_change_ruin_k, mutate_replace_destroyrepair]
    op = rng.choice(ops)
    return op(ast, rng)
