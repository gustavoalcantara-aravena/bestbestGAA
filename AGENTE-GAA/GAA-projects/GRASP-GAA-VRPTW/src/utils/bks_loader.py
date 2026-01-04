"""
============================================================
BKS Loader
Solomon VRPTW
============================================================

Responsabilidades:
- Cargar Best Known Solutions (BKS) desde CSV
- Proveer acceso rápido por instance_id
- Calcular gap porcentual respecto a BKS
- Comparaciones lexicográficas (V, D)
"""

from typing import Dict, Tuple
import csv


# ============================================================
# Public API
# ============================================================

def load_bks(csv_path: str) -> Dict[str, Dict]:
    """
    Load BKS table from CSV.

    CSV format:
    instance_id,family,k_bks,d_bks

    Returns:
    {
        "C101": {
            "family": "C1",
            "k_bks": 10,
            "d_bks": 828.93664
        },
        ...
    }
    """
    bks: Dict[str, Dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            instance_id = row["instance_id"]

            bks[instance_id] = {
                "family": row["family"],
                "k_bks": int(row["k_bks"]),
                "d_bks": float(row["d_bks"])
            }

    return bks


# ============================================================
# Evaluation Utilities
# ============================================================

def lexicographic_compare(
    v1: int, d1: float,
    v2: int, d2: float
) -> int:
    """
    Lexicographic comparison for VRPTW solutions.

    Returns:
    -1 if (v1, d1) is better
     0 if equal
     1 if worse
    """
    if v1 < v2:
        return -1
    if v1 > v2:
        return 1

    # Same number of vehicles
    if d1 < d2:
        return -1
    if d1 > d2:
        return 1

    return 0


def compute_gap(
    v_sol: int,
    d_sol: float,
    bks_entry: Dict
) -> float:
    """
    Compute gap (%) with respect to BKS.

    Rules:
    - If vehicles > BKS vehicles → infinite gap
    - If vehicles == BKS vehicles → distance gap
    - If vehicles < BKS vehicles → negative gap (improvement)
    """
    k_bks = bks_entry["k_bks"]
    d_bks = bks_entry["d_bks"]

    if v_sol > k_bks:
        return float("inf")

    if v_sol < k_bks:
        return -100.0  # strong improvement signal

    return 100.0 * (d_sol - d_bks) / d_bks


def is_bks_improved(
    v_sol: int,
    d_sol: float,
    bks_entry: Dict
) -> bool:
    """
    Check if solution improves BKS.
    """
    return lexicographic_compare(
        v_sol, d_sol,
        bks_entry["k_bks"], bks_entry["d_bks"]
    ) == -1


# ============================================================
# Convenience accessor
# ============================================================

class BKSTable:
    """
    Thin wrapper for BKS lookup and evaluation.
    """

    def __init__(self, csv_path: str):
        self.bks = load_bks(csv_path)

    def get(self, instance_id: str) -> Dict:
        return self.bks[instance_id]

    def gap(self, instance_id: str, v: int, d: float) -> float:
        return compute_gap(v, d, self.bks[instance_id])

    def improved(self, instance_id: str, v: int, d: float) -> bool:
        return is_bks_improved(v, d, self.bks[instance_id])
