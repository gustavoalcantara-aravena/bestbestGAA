import time
import random
from typing import Dict, Set

from .gcp_state import GCPState
from . import terminals
from .ast_nodes import *


class ASTInterpreter:
    def __init__(self, graph: Dict[int, Set[int]], seed: int = 0):
        self.graph = graph
        self.rng = random.Random(seed)
        self.start_time = None
        self.best_state: GCPState = None

    # -------------------------
    # Ejecución principal
    # -------------------------

    def run(self, ast: ASTNode) -> GCPState:
        self.start_time = time.perf_counter()
        state = GCPState(self.graph)

        state = self._eval(ast, state)
        return self.best_state or state

    # -------------------------
    # Evaluador recursivo
    # -------------------------

    def _eval(self, node: ASTNode, state: GCPState) -> GCPState:
        if isinstance(node, Seq):
            for stmt in node.body:
                state = self._eval(stmt, state)
            return state

        if isinstance(node, Call):
            return self._call_terminal(node, state)

        if isinstance(node, If):
            cond = self._eval_condition(node.cond, state)
            branch = node.then_branch if cond else node.else_branch
            return self._eval(branch, state)

        if isinstance(node, While):
            return self._eval_while(node, state)

        if isinstance(node, DestroyRepair):
            s1 = self._eval(node.destroy, state)
            s2 = self._eval(node.repair, s1)
            return s2

        raise ValueError(f"Nodo AST no soportado: {node}")

    # -------------------------
    # Terminales
    # -------------------------

    def _call_terminal(self, node: Call, state: GCPState) -> GCPState:
        name = node.name
        args = node.args or {}

        if name == "DSATUR":
            coloring = terminals.dsatur_construct(self.graph, self.rng)
            new = GCPState(self.graph, coloring)
            self._update_best(new)
            return new

        if name == "UpdatePenalty":
            new = terminals.update_penalty(state)
            self._update_best(new)
            return new

        if name == "RecolorVertex":
            new = terminals.recolor_vertex(state, self.rng)
            self._update_best(new)
            return new

        if name == "Ruin":
            k = args.get("k", 3)
            new = terminals.ruin(state, k, self.rng)
            return new

        if name == "GreedyRepair":
            new = terminals.greedy_repair(state, self.rng)
            self._update_best(new)
            return new

        raise ValueError(f"Terminal no soportado: {name}")

    # -------------------------
    # Condiciones
    # -------------------------

    def _eval_condition(self, cond: Condition, state: GCPState) -> bool:
        if cond.type == "Improves":
            if self.best_state is None:
                return True
            return state.objective() < self.best_state.objective()

        if cond.type == "Prob":
            p = cond.params.get("p", 0.1)
            return self.rng.random() < p

        raise ValueError(f"Condición no soportada: {cond.type}")

    # -------------------------
    # While
    # -------------------------

    def _eval_while(self, node: While, state: GCPState) -> GCPState:
        if node.budget.kind == "IterBudget":
            for _ in range(int(node.budget.value)):
                state = self._eval(node.body, state)
        else:
            raise ValueError(f"Budget no soportado: {node.budget.kind}")
        return state

    # -------------------------
    # Mejor solución
    # -------------------------

    def _update_best(self, state: GCPState):
        if self.best_state is None:
            self.best_state = state.copy()
        else:
            if state.objective() < self.best_state.objective():
                self.best_state = state.copy()
