import os
from ..core.dimacs_loader import scan_dimacs_families
from .fitness import FitnessConfig, FitnessEvaluator
from .ils_gaa import ILSGAAConfig, ils_gaa_run

DATASET_ROOT = "03-data/DIMACS-GPC-Dataset"

# Selecciona poquitas instancias para partir (rápido)
families = scan_dimacs_families(DATASET_ROOT)

# Ejemplo: 2 instancias de CUL (ajusta si quieres)
cul_files = families["CUL"][:2]

fit_cfg = FitnessConfig(
    instance_paths=cul_files,
    seeds=[101, 202, 303],
    infeasible_penalty=10_000.0
)
fit = FitnessEvaluator(fit_cfg)

ils_cfg = ILSGAAConfig(
    seed=7,
    max_evals=60,
    no_improve_limit=20,
    perturb_strength=2
)

best_ast, report = ils_gaa_run(fit, ils_cfg)

print("=== BEST FITNESS ===")
print(report["best_fitness"])
print("\n=== AST (ASCII) ===")
print(report["ast_ascii"])
print("\n=== PSEUDOCÓDIGO (plantilla) ===")
print(report["pseudocode"])
