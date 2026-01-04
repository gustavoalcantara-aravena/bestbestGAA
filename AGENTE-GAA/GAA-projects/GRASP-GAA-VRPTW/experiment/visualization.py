"""
============================================================
Visualization Module
GRASP + GAA for VRPTW Solomon
============================================================

Generates publication-quality plots:
1. Boxplots of GAP% vs BKS (defined only when V == k_BKS)
2. Bar charts of average vehicles per family
3. Algorithm ranking plots (vehicles, distance, gap)

Input:
- summary_algorithms.csv
- per_instance_results.csv
- family_aggregates.csv

IMPORTANT:
- GAP% is only plotted when feasible and V == k_BKS
- Matplotlib only (no seaborn)
"""

import csv
import os
from typing import Dict, List, Any
import statistics
import matplotlib.pyplot as plt


# ============================================================
# Helpers
# ============================================================

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def load_csv(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(x):
    if x is None or x == "" or x == "None":
        return None
    return float(x)


def to_int(x):
    if x is None or x == "" or x == "None":
        return None
    return int(x)


# ============================================================
# Visualization Class
# ============================================================

class Visualization:
    def __init__(self, reports_dir: str, output_dir: str):
        self.reports_dir = reports_dir
        self.output_dir = output_dir
        ensure_dir(output_dir)

        self.summary = load_csv(os.path.join(reports_dir, "summary_algorithms.csv"))
        self.per_instance = load_csv(os.path.join(reports_dir, "per_instance_results.csv"))
        self.family = load_csv(os.path.join(reports_dir, "family_aggregates.csv"))

    # =========================================================
    # 1. GAP% Boxplots (per algorithm)
    # =========================================================

    def plot_gap_boxplots(self):
        """
        Boxplots of GAP% relative to BKS.
        Only includes runs where:
        - feasible == True
        - gap_defined == True (i.e., vehicles == k_BKS)
        """
        gaps_by_algo: Dict[str, List[float]] = {}

        for row in self.per_instance:
            if row["gap_defined"] == "True":
                algo = row["algorithm_id"]
                gap = to_float(row["gap_percent"])
                if gap is not None:
                    gaps_by_algo.setdefault(algo, []).append(gap)

        if not gaps_by_algo:
            print("[WARN] No GAP% data available for boxplots.")
            return

        labels = list(gaps_by_algo.keys())
        data = [gaps_by_algo[a] for a in labels]

        plt.figure()
        plt.boxplot(data, labels=labels, showfliers=True)
        plt.axhline(0.0, linestyle="--")
        plt.ylabel("GAP% vs BKS")
        plt.title("GAP% Distribution (Only Feasible Solutions with V = k_BKS)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        path = os.path.join(self.output_dir, "gap_boxplots.png")
        plt.savefig(path)
        plt.close()

    # =========================================================
    # 2. Average Vehicles per Family (Bar Chart)
    # =========================================================

    def plot_avg_vehicles_by_family(self):
        """
        Bar chart: average number of vehicles per family, per algorithm.
        """
        families = sorted(set(r["family"] for r in self.family))
        algos = sorted(set(r["algorithm_id"] for r in self.family))

        # Build structure: family -> algo -> avg_vehicles
        values: Dict[str, Dict[str, float]] = {f: {} for f in families}

        for row in self.family:
            fam = row["family"]
            algo = row["algorithm_id"]
            values[fam][algo] = to_float(row["avg_vehicles"])

        width = 0.8 / len(algos)
        x = list(range(len(families)))

        plt.figure()

        for i, algo in enumerate(algos):
            y = [values[f].get(algo, None) for f in families]
            xpos = [xi + i * width for xi in x]
            plt.bar(xpos, y, width=width, label=algo)

        plt.xticks([xi + width * (len(algos) - 1) / 2 for xi in x], families)
        plt.ylabel("Average Vehicles")
        plt.title("Average Fleet Size per Family")
        plt.legend()
        plt.tight_layout()

        path = os.path.join(self.output_dir, "avg_vehicles_by_family.png")
        plt.savefig(path)
        plt.close()

    # =========================================================
    # 3. Algorithm Ranking Plot (Vehicles & Distance)
    # =========================================================

    def plot_algorithm_ranking(self):
        """
        Ranking plot using:
        - avg_vehicles (primary)
        - avg_distance (secondary)
        """
        algos = []
        avg_vehicles = []
        avg_distance = []

        for row in self.summary:
            algos.append(row["algorithm_id"])
            avg_vehicles.append(to_float(row["avg_vehicles"]))
            avg_distance.append(to_float(row["avg_distance"]))

        # Sort by lexicographic VRPTW criterion
        order = sorted(
            range(len(algos)),
            key=lambda i: (avg_vehicles[i], avg_distance[i])
        )

        algos = [algos[i] for i in order]
        avg_vehicles = [avg_vehicles[i] for i in order]
        avg_distance = [avg_distance[i] for i in order]

        fig, ax1 = plt.subplots()

        ax1.bar(algos, avg_vehicles)
        ax1.set_ylabel("Average Vehicles")
        ax1.set_xlabel("Algorithm")

        ax2 = ax1.twinx()
        ax2.plot(algos, avg_distance, marker="o")
        ax2.set_ylabel("Average Distance")

        plt.title("Algorithm Ranking (Lexicographic: Vehicles → Distance)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        path = os.path.join(self.output_dir, "algorithm_ranking.png")
        plt.savefig(path)
        plt.close()

    # =========================================================
    # Run All
    # =========================================================

    def generate_all(self):
        self.plot_gap_boxplots()
        self.plot_avg_vehicles_by_family()
        self.plot_algorithm_ranking()
