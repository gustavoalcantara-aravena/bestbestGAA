# src/evaluation/bks_metrics.py

def compute_gap_vs_bks(
    sol_k: int,
    sol_d: float,
    bks_k: int,
    bks_d: float
) -> float:
    """
    Gap porcentual canónico Solomon.

    Regla:
    - Si K_sol > K_bKS → gap = +inf (dominancia perdida)
    - Si K_sol < K_BKS → gap < 0 (mejor que BKS)
    - Si K_sol == K_BKS → gap basado en distancia
    """

    if sol_k > bks_k:
        return float("inf")

    if sol_k < bks_k:
        return -100.0 * (bks_k - sol_k) / bks_k

    # sol_k == bks_k
    return 100.0 * (sol_d - bks_d) / bks_d
