import time
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional

from ..core.ast_interpreter import ASTInterpreter
from ..core.dimacs_loader import load_dimacs_col


@dataclass
class FitnessConfig:
    instance_paths: List[str]
    seeds: List[int]
    # penalización grande para infeasibilidad / incompletitud
    infeasible_penalty: float = 10_000.0


class FitnessEvaluator:
    def __init__(self, cfg: FitnessConfig):
        self.cfg = cfg
        self._cache: Dict[str, Tuple[Dict[int, Set[int]], int, int]] = {}

    def _get_graph(self, path: str):
        if path not in self._cache:
            self._cache[path] = load_dimacs_col(path)
        return self._cache[path]

    def evaluate(self, ast, algo_seed: int) -> float:
        """
        Fitness escalar (menor es mejor).
        Promedio sobre instancias y semillas.
        """
        total = 0.0
        count = 0

        for inst_path in self.cfg.instance_paths:
            graph, _, _ = self._get_graph(inst_path)
            for s in self.cfg.seeds:
                interp = ASTInterpreter(graph, seed=(algo_seed * 10_000 + s))
                best = interp.run(ast)

                k = best.num_colors()
                conf = best.conflicts()
                complete = (len(best.coloring) == len(graph))

                score = float(k)
                if conf > 0 or not complete:
                    score += self.cfg.infeasible_penalty + 100.0 * conf
                total += score
                count += 1

        return total / max(1, count)
