from .dimacs_loader import load_dimacs_col
from .gcp_state import GCPState
from .terminals import dsatur_construct

import random

graph, n, m = load_dimacs_col(
    "03-data/DIMACS-GPC-Dataset/CUL/flat300_20_0.col"
)

rng = random.Random(123)
coloring = dsatur_construct(graph, rng)
state = GCPState(graph, coloring)

print("n =", n, "m =", m)
print("colors =", state.num_colors())
print("conflicts =", state.conflicts())
