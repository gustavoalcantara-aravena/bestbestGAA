from typing import Dict, Set, Optional

class GCPState:
    """
    Estado de una solución para Graph Coloring Problem.
    """
    def __init__(
        self,
        graph: Dict[int, Set[int]],
        coloring: Optional[Dict[int, int]] = None,
        penalty: float = 1.0,
    ):
        self.graph = graph
        self.n = len(graph)
        self.coloring = coloring or {}
        self.penalty = penalty

    def num_colors(self) -> int:
        if not self.coloring:
            return 0
        return len(set(self.coloring.values()))

    def conflicts(self) -> int:
        c = 0
        for u, nbrs in self.graph.items():
            cu = self.coloring.get(u, None)
            if cu is None:
                continue
            for v in nbrs:
                if u < v:
                    cv = self.coloring.get(v, None)
                    if cv is not None and cu == cv:
                        c += 1
        return c

    def feasible(self) -> bool:
        return self.conflicts() == 0 and len(self.coloring) == self.n

    def objective(self) -> float:
        """
        Función objetivo penalizada.
        """
        return self.num_colors() + self.penalty * self.conflicts()

    def copy(self):
        return GCPState(
            self.graph,
            coloring=dict(self.coloring),
            penalty=self.penalty,
        )
