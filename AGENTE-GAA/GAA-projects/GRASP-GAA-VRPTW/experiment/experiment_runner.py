"""
============================================================
ExperimentRunner
GRASP + GAA for VRPTW Solomon
============================================================

Responsabilidades:
- Cargar configuración experimental
- Cargar instancias Solomon
- Cargar BKS
- Ejecutar N algoritmos (ASTs)
- Ejecutar múltiples runs por algoritmo
- Almacenar resultados por solución
- Generar reportes y visualizaciones

Este módulo NO implementa lógica VRPTW ni GRASP.
Orquesta el experimento completo.
"""

import os
import json
import time
import random
from typing import Dict, List

from gaa.algorithm_generator import AlgorithmGenerator
from gaa.algorithm_repository import AlgorithmRepository
from solver.grasp_solver import GRASPSolver
from solution.solution_container import Solution
from solution.solution_pool import SolutionPool
from experiment.report_generator import ReportGenerator
from experiment.visualization import Visualization
from utils.dataset_loader import load_solomon_instance
from utils.bks_loader import load_bks_table
from typing import List
from data.dataset_loader import DatasetLoader
from data.bks_loader import BKSLoader
from grasp.grasp_solver import GRASPSolver
from experiment.logging import ExperimentLogger


# ============================================================
# ExperimentRunner
# ============================================================

class ExperimentRunner:

    def __init__(self, config: Dict):
        self.config = config

        # Paths
        self.dataset_dir = config["paths"]["dataset_dir"]
        self.bks_path = config["paths"]["bks_file"]
        self.reports_dir = config["paths"]["reports_dir"]
        self.figures_dir = os.path.join(self.reports_dir, "figures")

        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.figures_dir, exist_ok=True)

        # Experiment parameters
        self.seed = config["experiment"]["seed"]
        self.num_algorithms = config["experiment"]["num_algorithms"]
        self.num_runs = config["experiment"]["num_runs"]

        # Load BKS table
        self.bks_table = load_bks_table(self.bks_path)

        # Algorithm infra
        self.algorithm_generator = AlgorithmGenerator(config)
        self.algorithm_repository = AlgorithmRepository()

        # Global solution pool
        self.solution_pool = SolutionPool()

    # =========================================================
    # Main Entry Point
    # =========================================================

    def run(self):
        self._set_seed()

        print("=== GAA + GRASP VRPTW Experiment Started ===")

        algorithms = self._generate_algorithms()
        instances = self._load_instances()

        for algo in algorithms:
            print(f"\n[ALGORITHM] {algo.algorithm_id}")

            for instance_id, instance in instances.items():
                print(f"  [INSTANCE] {instance_id}")

                bks = self.bks_table[instance_id]

                for run_id in range(self.num_runs):
                    solution = self._run_single(
                        algo,
                        instance_id,
                        instance,
                        bks,
                        run_id
                    )
                    self.solution_pool.add(solution)

        self._finalize()

    # =========================================================
    # Single Run
    # =========================================================

    def _run_single(
        self,
        algorithm,
        instance_id: str,
        instance: Dict,
        bks: Dict,
        run_id: int
    ) -> Solution:

        solver = GRASPSolver(
            algorithm=algorithm,
            instance=instance,
            bks=bks,
            config=self.config
        )

        start_time = time.time()
        solution_data = solver.solve()
        elapsed = time.time() - start_time

        solution = Solution(
            algorithm_id=algorithm.algorithm_id,
            instance_id=instance_id,
            family=instance["family"],
            run_id=run_id,
            seed=self.seed,
            vehicles=solution_data["vehicles"],
            distance=solution_data["distance"],
            feasible=solution_data["feasible"],
            capacity_violation=solution_data["capacity_violation"],
            time_violation=solution_data["time_violation"],
            elapsed_time=elapsed,
            bks=bks,
            ast_metadata=algorithm.metadata
        )

        return solution

    # =========================================================
    # Algorithm Generation
    # =========================================================

    def _generate_algorithms(self):
        algorithms = []

        print("[INFO] Generating algorithms...")

        while len(algorithms) < self.num_algorithms:
            algo = self.algorithm_generator.generate()

            if self.algorithm_repository.register(algo):
                algorithms.append(algo)
                print(f"  - Generated {algo.algorithm_id}")

        return algorithms

    # =========================================================
    # Instance Loading
    # =========================================================

    def _load_instances(self) -> Dict[str, Dict]:
        instances = {}

        families = self.config["experiment"]["families"]

        print("[INFO] Loading Solomon instances...")

        for fam in families:
            fam_dir = os.path.join(self.dataset_dir, fam)

            for file in os.listdir(fam_dir):
                if not file.endswith(".txt"):
                    continue

                instance_id = file.replace(".txt", "")
                path = os.path.join(fam_dir, file)

                instances[instance_id] = load_solomon_instance(path, fam)

        print(f"[INFO] Loaded {len(instances)} instances.")
        return instances

    # =========================================================
    # Finalization
    # =========================================================

    def _finalize(self):
        print("\n[INFO] Generating reports...")

        report = ReportGenerator(
            solution_pool=self.solution_pool,
            output_dir=self.reports_dir
        )
        report.generate_all()

        print("[INFO] Generating visualizations...")

        viz = Visualization(
            reports_dir=self.reports_dir,
            output_dir=self.figures_dir
        )
        viz.generate_all()

        print("\n=== Experiment Finished ===")

    # =========================================================
    # Utilities
    # =========================================================

    def _set_seed(self):
        random.seed(self.seed)




        # Initialize logging
        self.logger = ExperimentLogger(self.config)
        self.logger.log_experiment_start()

        