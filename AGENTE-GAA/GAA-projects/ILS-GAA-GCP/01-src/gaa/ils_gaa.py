import time
import random
from dataclasses import dataclass
from typing import Optional, Tuple

from .ast_generator import random_valid_ast
from .ast_mutations import mutate
from .fitness import FitnessEvaluator, FitnessConfig
from ..core.ast_utils import ast_to_ascii, ast_to_pseudocode


@dataclass
class ILSGAAConfig:
    seed: int = 1
    max_evals: int = 200
    no_improve_limit: int = 50
    # Intensidad perturbación: cuántas mutaciones aplicar si no mejora
    perturb_strength: int = 3


def ils_gaa_run(fit: FitnessEvaluator, cfg: ILSGAAConfig):
    rng = random.Random(cfg.seed)

    # Solución inicial (algoritmo inicial)
    A = random_valid_ast(rng)
    A_seed = rng.randint(1, 10_000_000)
    fA = fit.evaluate(A, A_seed)

    bestA = A
    bestSeed = A_seed
    bestF = fA

    evals = 1
    noimp = 0

    while evals < cfg.max_evals and noimp < cfg.no_improve_limit:
        # Búsqueda local: un vecino por iteración (simple y estable)
        A2 = mutate(A, rng)
        A2_seed = rng.randint(1, 10_000_000)
        fA2 = fit.evaluate(A2, A2_seed)
        evals += 1

        if fA2 < fA:
            A, A_seed, fA = A2, A2_seed, fA2
            noimp = 0
            if fA < bestF:
                bestA, bestSeed, bestF = A, A_seed, fA
        else:
            noimp += 1
            # Perturbación (sacudir el algoritmo actual)
            A_pert = A
            for _ in range(cfg.perturb_strength):
                A_pert = mutate(A_pert, rng)
            A, A_seed = A_pert, rng.randint(1, 10_000_000)
            fA = fit.evaluate(A, A_seed)
            evals += 1
            if fA < bestF:
                bestA, bestSeed, bestF = A, A_seed, fA

    report = {
        "best_fitness": bestF,
        "best_seed": bestSeed,
        "evals": evals,
        "ast_ascii": ast_to_ascii(bestA).rstrip(),
        "pseudocode": ast_to_pseudocode(seed=cfg.seed),
    }
    return bestA, report
