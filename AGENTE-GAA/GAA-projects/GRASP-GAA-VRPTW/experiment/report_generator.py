"""
============================================================
Report Generator
GRASP + GAA for VRPTW Solomon
============================================================

Generates:
- summary_algorithms.csv     (per algorithm aggregated metrics)
- per_instance_results.csv   (raw results: algo x run x instance)
- family_aggregates.csv      (aggregated by family per algorithm)
- winner_report.md           (thesis-friendly text)

Assumptions:
- BKS CSV: instance_id,family,k_bks,d_bks
- AlgorithmRepository stores runs with fields:
  instance_id, vehicles, distance, gap, runtime_sec, feasible
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import statistics

from gaa.algorithm_repository import AlgorithmRepository, AlgorithmEntry, AlgorithmRunResult


# ============================================================
# BKS Loader
# ============================================================

@dataclass(frozen=True)
class BKSRecord:
    instance_id: str
    family: str
    k_bks: int
    d_bks: float


def load_bks_csv(path: str) -> Dict[str, BKSRecord]:
    """
    Load BKS file: instance_id,family,k_bks,d_bks
    Returns dict keyed by instance_id.
    """
    bks: Dict[str, BKSRecord] = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"instance_id", "family", "k_bks", "d_bks"}
        if set(reader.fieldnames or []) != required:
            # allow any ordering but require the four columns
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError(f"BKS CSV missing columns. Found={reader.fieldnames}, required={sorted(required)}")

        for row in reader:
            iid = row["instance_id"].strip()
            bks[iid] = BKSRecord(
                instance_id=iid,
                family=row["family"].strip(),
                k_bks=int(row["k_bks"]),
                d_bks=float(row["d_bks"])
            )
    return bks


# ============================================================
# Helpers
# ============================================================

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def safe_mean(xs: List[float]) -> Optional[float]:
    return statistics.mean(xs) if xs else None


def safe_stdev(xs: List[float]) -> Optional[float]:
    return statistics.stdev(xs) if len(xs) >= 2 else None


def compute_gap_percent(distance: float, bks_distance: float) -> float:
    # gap% = (D - D_bks)/D_bks * 100
    return ((distance - bks_distance) / bks_distance) * 100.0


# ============================================================
# Report Generator
# ============================================================

class ReportGenerator:
    def __init__(self, repo: AlgorithmRepository, bks_map: Dict[str, BKSRecord]):
        self.repo = repo
        self.bks = bks_map

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------

    def generate_all(self, output_dir: str) -> Dict[str, str]:
        ensure_dir(output_dir)

        paths = {
            "summary_algorithms_csv": os.path.join(output_dir, "summary_algorithms.csv"),
            "per_instance_results_csv": os.path.join(output_dir, "per_instance_results.csv"),
            "family_aggregates_csv": os.path.join(output_dir, "family_aggregates.csv"),
            "winner_report_md": os.path.join(output_dir, "winner_report.md"),
        }

        self._export_summary_algorithms(paths["summary_algorithms_csv"])
        self._export_per_instance_results(paths["per_instance_results_csv"])
        self._export_family_aggregates(paths["family_aggregates_csv"])
        self._export_winner_report(paths["winner_report_md"])

        return paths

    # --------------------------------------------------------
    # 1) Summary per algorithm
    # --------------------------------------------------------

    def _export_summary_algorithms(self, path: str) -> None:
        rows = self.repo.summary_table()
        fieldnames = [
            "algorithm_id",
            "phase",
            "runs",
            "feasibility_rate",
            "avg_vehicles",
            "avg_distance",
            "avg_gap",
            "std_gap",
            "avg_runtime_sec"
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)

    # --------------------------------------------------------
    # 2) Raw results per run per instance
    # --------------------------------------------------------

    def _export_per_instance_results(self, path: str) -> None:
        fieldnames = [
            "algorithm_id",
            "phase",
            "instance_id",
            "family",
            "vehicles",
            "distance",
            "feasible",
            "runtime_sec",
            "k_bks",
            "d_bks",
            "gap_percent",
            "gap_defined"  # True if vehicles == k_bks and feasible
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()

            for entry in self.repo.all_algorithms():
                for run in entry.stats.runs:
                    b = self.bks.get(run.instance_id, None)
                    fam = b.family if b else "UNKNOWN"
                    k_bks = b.k_bks if b else None
                    d_bks = b.d_bks if b else None

                    gap_defined = False
                    gap_percent = None

                    if b and run.feasible and run.vehicles == b.k_bks:
                        gap_defined = True
                        gap_percent = compute_gap_percent(run.distance, b.d_bks)

                    w.writerow({
                        "algorithm_id": entry.algorithm_id,
                        "phase": entry.phase,
                        "instance_id": run.instance_id,
                        "family": fam,
                        "vehicles": run.vehicles,
                        "distance": run.distance,
                        "feasible": run.feasible,
                        "runtime_sec": run.runtime_sec,
                        "k_bks": k_bks,
                        "d_bks": d_bks,
                        "gap_percent": gap_percent,
                        "gap_defined": gap_defined
                    })

    # --------------------------------------------------------
    # 3) Aggregates by family per algorithm
    # --------------------------------------------------------

    def _export_family_aggregates(self, path: str) -> None:
        fieldnames = [
            "algorithm_id",
            "phase",
            "family",
            "runs",
            "feasibility_rate",
            "avg_vehicles",
            "avg_distance",
            "avg_gap_percent_defined_only",
            "std_gap_percent_defined_only",
            "avg_runtime_sec"
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()

            for entry in self.repo.all_algorithms():
                # bucket runs by family
                buckets: Dict[str, List[AlgorithmRunResult]] = {}
                for r in entry.stats.runs:
                    fam = self.bks.get(r.instance_id).family if r.instance_id in self.bks else "UNKNOWN"
                    buckets.setdefault(fam, []).append(r)

                for fam, runs in buckets.items():
                    feas_rate = sum(1 for r in runs if r.feasible) / len(runs)
                    avg_v = statistics.mean(r.vehicles for r in runs)
                    avg_d = statistics.mean(r.distance for r in runs)
                    avg_t = statistics.mean(r.runtime_sec for r in runs)

                    # gap% only when feasible and vehicles == k_bks
                    gap_list = []
                    for r in runs:
                        b = self.bks.get(r.instance_id, None)
                        if b and r.feasible and r.vehicles == b.k_bks:
                            gap_list.append(compute_gap_percent(r.distance, b.d_bks))

                    w.writerow({
                        "algorithm_id": entry.algorithm_id,
                        "phase": entry.phase,
                        "family": fam,
                        "runs": len(runs),
                        "feasibility_rate": feas_rate,
                        "avg_vehicles": avg_v,
                        "avg_distance": avg_d,
                        "avg_gap_percent_defined_only": safe_mean(gap_list),
                        "std_gap_percent_defined_only": safe_stdev(gap_list),
                        "avg_runtime_sec": avg_t
                    })

    # --------------------------------------------------------
    # 4) Winner thesis-friendly report
    # --------------------------------------------------------

    def _export_winner_report(self, path: str) -> None:
        winner = self.repo.best_algorithm()
        stats = winner.stats

        # global gap% list defined only when V==k_bks & feasible
        gaps = []
        for r in stats.runs:
            b = self.bks.get(r.instance_id, None)
            if b and r.feasible and r.vehicles == b.k_bks:
                gaps.append(compute_gap_percent(r.distance, b.d_bks))

        text = []
        text.append("# Winner Algorithm Report (GAA + GRASP - VRPTW Solomon)\n")
        text.append(f"- algorithm_id: {winner.algorithm_id}")
        text.append(f"- phase: {winner.phase}")
        text.append(f"- runs: {len(stats.runs)}")
        text.append(f"- feasibility_rate: {stats.feasibility_rate():.3f}")
        text.append(f"- avg_vehicles: {stats.avg_vehicles():.3f}")
        text.append(f"- avg_distance: {stats.avg_distance():.3f}")
        text.append(f"- avg_runtime_sec: {stats.avg_runtime():.3f}")

        if gaps:
            text.append(f"- avg_gap_percent (defined only if feasible and V == k_BKS): {statistics.mean(gaps):.3f}%")
            if len(gaps) >= 2:
                text.append(f"- std_gap_percent (defined only if feasible and V == k_BKS): {statistics.stdev(gaps):.3f}%")
        else:
            text.append("- avg_gap_percent: N/A (no runs matched V == k_BKS while feasible)")

        text.append("\n## Notes\n")
        text.append("- Canonical Solomon criterion is lexicographic: minimize Vehicles first, then Distance.")
        text.append("- Gap% is only meaningful when the number of vehicles equals the BKS fleet size for that instance.")
        text.append("- If an algorithm uses more vehicles than BKS, it can still be feasible but is not directly comparable in distance.\n")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(text))
