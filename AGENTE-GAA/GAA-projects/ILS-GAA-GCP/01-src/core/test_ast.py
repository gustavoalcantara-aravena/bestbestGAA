from .dimacs_loader import load_dimacs_col
from .ast_nodes import *
from .ast_interpreter import ASTInterpreter

ast = Seq(
    type="Seq",
    body=[
        Call(type="Call", name="DSATUR"),
        Call(type="Call", name="UpdatePenalty"),
        While(
            type="While",
            budget=Budget(kind="IterBudget", value=200),
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
                            destroy=Call(
                                type="Call",
                                name="Ruin",
                                args={"k": 5}
                            ),
                            repair=Call(
                                type="Call",
                                name="GreedyRepair"
                            )
                        )
                    )
                ]
            )
        )
    ]
)

graph, _, _ = load_dimacs_col(
    "03-data/DIMACS-GPC-Dataset/CUL/flat300_20_0.col"
)

interp = ASTInterpreter(graph, seed=42)
best = interp.run(ast)

print("Colores:", best.num_colors())
print("Conflictos:", best.conflicts())
