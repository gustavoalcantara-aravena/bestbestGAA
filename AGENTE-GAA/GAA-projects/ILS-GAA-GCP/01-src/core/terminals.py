import random
from copy import deepcopy
from typing import Dict, Set
from .gcp_state import GCPState


def dsatur_construct(graph: Dict[int, Set[int]], rng: random.Random):
    """
    Constructor greedy tipo DSATUR simplificado.
    """
    vertices = list(graph.keys())
    rng.shuffle(vertices)

    coloring = {}
    for v in vertices:
        used = {coloring[u] for u in graph[v] if u in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[v] = c
    return coloring


def update_penalty(state: GCPState) -> GCPState:
    new = state.copy()
    new.penalty = max(1.0, float(new.conflicts()))
    return new


def recolor_vertex(state: GCPState, rng: random.Random) -> GCPState:
    new = state.copy()

    conflicted = []
    for v in new.graph:
        cv = new.coloring.get(v, None)
        if cv is None:
            continue
        if any(new.coloring.get(u) == cv for u in new.graph[v]):
            conflicted.append(v)

    if not conflicted:
        return new

    v = rng.choice(conflicted)
    used = {new.coloring.get(u) for u in new.graph[v]}
    used.discard(None)

    c = 0
    while c in used:
        c += 1
    new.coloring[v] = c
    return new


def ruin(state: GCPState, k: int, rng: random.Random) -> GCPState:
    new = state.copy()
    keys = list(new.coloring.keys())
    if not keys:
        return new

    vs = rng.sample(keys, min(k, len(keys)))
    for v in vs:
        new.coloring.pop(v, None)
    return new


def greedy_repair(state: GCPState, rng: random.Random) -> GCPState:
    new = state.copy()
    vertices = list(new.graph.keys())
    rng.shuffle(vertices)

    for v in vertices:
        if v in new.coloring:
            continue
        used = {new.coloring.get(u) for u in new.graph[v]}
        used.discard(None)

        c = 0
        while c in used:
            c += 1
        new.coloring[v] = c
    return new
