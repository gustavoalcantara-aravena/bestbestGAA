"""
============================================================
MAIN ENTRY POINT
GRASP + GAA for VRPTW (Solomon Benchmarks)
============================================================
"""

# ------------------------------------------------------------
# Standard library imports
# ------------------------------------------------------------
import os
import sys
import time
import yaml
import random
from pathlib import Path

# ------------------------------------------------------------
# Project imports
# ------------------------------------------------------------
from data.loader_solomon import SolomonLoader
from data.bks_loader import BKSLoader

from gaa.algorithm_generator import AlgorithmGenerator
from grasp.grasp_solver import GRASPSolver

from core.solution import Solution
from core.solution_pool import SolutionPool

from experiment.experiment_runner import ExperimentRunner
from utils.logger import setup_logger
from utils.random_utils import set_global_seed


# ============================================================
# Configuration Loader
# ============================================================

def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


# ============================================================
# Main Function
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Load configuration
    # --------------------------------------------------------
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = load_config(config_path)

    # --------------------------------------------------------
    # 2. Setup reproducibility
    # --------------------------------------------------------
    seed = config["random"]["global_seed"]
    set_global_seed(seed)

    # --------------------------------------------------------
    # 3. Setup logging
    # --------------------------------------------------------
    logger = setup_logger(
        log_dir=config["logging"]["log_dir"],
        level=config["logging"]["level"]
    )

    logger.info("==========================================")
    logger.info(" GRASP + GAA for VRPTW (Solomon) STARTED ")
    logger.info("==========================================")

    # --------------------------------------------------------
    # 4. Load datasets
    # --------------------------------------------------------
    logger.info("Loading Solomon VRPTW instances...")

    solomon_loader = SolomonLoader(
        root_dir=config["dataset"]["root_dir"],
        families=config["dataset"]["families"]
    )

    instances = solomon_loader.load_instances()
    logger.info(f"Loaded {len(instances)} instances")

    # --------------------------------------------------------
    # 5. Load BKS
    # --------------------------------------------------------
    logger.info("Loading Best Known Solutions (BKS)...")

    bks_loader = BKSLoader(
        file_path=config["bks"]["file"],
        fields=config["bks"]["fields"]
    )

    bks_data = bks_loader.load()
    logger.info(f"Loaded BKS for {len(bks_data)} instances")

    # --------------------------------------------------------
    # 6. Generate Algorithms (ASTs)
    # --------------------------------------------------------
    logger.info("Generating algorithms (ASTs)...")

    algorithm_generator = AlgorithmGenerator(
        gaa_config=config["gaa"],
        random_seed=seed
    )

    algorithms = algorithm_generator.generate()
    logger.info(f"Generated {len(algorithms)} algorithms")

    # --------------------------------------------------------
    # 7. Initialize Solution Pool
    # --------------------------------------------------------
    solution_pool = SolutionPool(
        max_size=config["solution_pool"]["max_size"],
        keep_only_feasible=config["solution_pool"]["keep_only_feasible"]
    )

    # --------------------------------------------------------
    # 8. Setup Experiment Runner
    # --------------------------------------------------------
    experiment_runner = ExperimentRunner(
        algorithms=algorithms,
        instances=instances,
        bks_data=bks_data,
        config=config,
        solution_pool=solution_pool,
        logger=logger
    )

    # --------------------------------------------------------
    # 9. Run experiment
    # --------------------------------------------------------
    logger.info("Starting experiment execution...")

    start_time = time.time()

    experiment_runner.run()

    total_time = time.time() - start_time

    logger.info(f"Experiment completed in {total_time:.2f} seconds")

    # --------------------------------------------------------
    # 10. Finalize & Save Results
    # --------------------------------------------------------
    logger.info("Saving final results...")

    experiment_runner.save_results(
        output_dir=config["results"]["output_dir"]
    )

    logger.info("==========================================")
    logger.info(" EXPERIMENT FINISHED SUCCESSFULLY ")
    logger.info("==========================================")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()
