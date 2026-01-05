import random
from . import ast_mutations
from ..core.ast_nodes import Seq, Call, While, If, DestroyRepair, Budget, Condition

def random_valid_ast(rng: random.Random):
    """
    Genera un AST válido (semánticamente seguro) usando una plantilla
    y randomizando parámetros.
    """
    iter_budget = rng.choice([20, 40])
    k_ruin = rng.choice([3, 5, 8, 12])

    ast = Seq(
        type="Seq",
        body=[
            Call(type="Call", name="DSATUR"),
            Call(type="Call", name="UpdatePenalty"),
            While(
                type="While",
                budget=Budget(kind="IterBudget", value=iter_budget),
                body=Seq(
                    type="Seq",
                    body=[
                        Call(type="Call", name="RecolorVertex"),
                        If(
                            type="If",
                            cond=Condition(type="Improves"),
                            then_branch=Call(type="Call", name="UpdatePenalty"),
                            else_branch=DestroyRepair(
                                type="DestroyRepair",
                                destroy=Call(type="Call", name="Ruin", args={"k": k_ruin}),
                                repair=Call(type="Call", name="GreedyRepair"),
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    return ast
