"""
Phase 9: Experimentation Scripts - QUICK and FULL modes for GAA-VRPTW evaluation

Responsabilidades:
1. Demo scripts for algorithm evaluation (QUICK: 1 family, FULL: 6 families)
2. Algorithm generation once (seed=42) - reused in both modes
3. Comprehensive result collection and output generation
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random


@dataclass
class ExperimentConfig:
    """Configuration for experiment execution"""
    mode: str  # 'QUICK' or 'FULL'
    families: List[str]  # Solomon families to evaluate
    algorithms: List[str]  # Algorithm IDs to use
    repetitions: int = 1
    seed: int = 42
    timeout_sec: int = 600
    
    def __post_init__(self):
        assert self.mode in ['QUICK', 'FULL'], "Mode must be 'QUICK' or 'FULL'"
        assert self.repetitions >= 1, "Repetitions must be >= 1"


class AlgorithmGenerator:
    """Generates GAA algorithms (once per session, seed=42)"""
    
    def __init__(self, seed: int = 42, output_dir: str = "algorithms"):
        """
        Initialize algorithm generator
        
        Args:
            seed: Random seed for reproducibility
            output_dir: Directory to save generated algorithms
        """
        self.seed = seed
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        random.seed(self.seed)
    
    def generate_algorithms(self, num_algorithms: int = 3) -> List[str]:
        """
        Generate num_algorithms GAA algorithms with seed=42
        
        Returns:
            List of algorithm IDs (e.g., ['GAA_Algorithm_1', 'GAA_Algorithm_2', ...])
        """
        algorithm_ids = []
        
        for i in range(1, num_algorithms + 1):
            algo_id = f"GAA_Algorithm_{i}"
            
            # Generate algorithm metadata
            algo_data = {
                'algorithm_id': algo_id,
                'seed': self.seed,
                'version': '1.0',
                'components': {
                    'construction': f'ConstructionHeuristic_{i}',
                    'local_search': f'LocalSearch_{i}',
                    'parameters': {
                        'alpha': round(random.uniform(0.1, 0.9), 2),
                        'beta': round(random.uniform(0.1, 0.9), 2),
                        'max_iterations': 100 + i * 50
                    }
                },
                'description': f'Auto-generated GAA algorithm #{i} with seed={self.seed}'
            }
            
            # Save to JSON
            algo_file = self.output_dir / f"{algo_id}.json"
            with open(algo_file, 'w') as f:
                json.dump(algo_data, f, indent=2)
            
            algorithm_ids.append(algo_id)
        
        return algorithm_ids


class ExperimentExecutor:
    """Manages experiment execution and data collection"""
    
    def __init__(self, config: ExperimentConfig):
        """
        Initialize experiment executor
        
        Args:
            config: ExperimentConfig instance
        """
        self.config = config
        
        # Create output structure
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        self.experiment_id = f"vrptw_experiments_{config.mode}_{timestamp}"
        self.output_dir = Path("output") / self.experiment_id
        self.results_dir = self.output_dir / "results"
        self.plots_dir = self.output_dir / "plots"
        self.logs_dir = self.output_dir / "logs"
        
        for d in [self.results_dir, self.plots_dir, self.logs_dir]:
            d.mkdir(exist_ok=True, parents=True)
        
        # Data accumulation
        self.raw_results = []
    
    def get_solomon_instances(self, families: List[str]) -> Dict[str, List[str]]:
        """
        Get Solomon instances for given families
        
        Args:
            families: List of family names (e.g., ['C1', 'R1', 'RC1'])
            
        Returns:
            Dict mapping family -> list of instance IDs
        """
        # Solomon benchmark definition
        solomon_map = {
            'C1': [f'C1{i:02d}' for i in range(1, 10)],  # C101-C109
            'C2': [f'C2{i:02d}' for i in range(1, 9)],   # C201-C208
            'R1': [f'R1{i:02d}' for i in range(1, 13)],  # R101-R112
            'R2': [f'R2{i:02d}' for i in range(1, 12)],  # R201-R211
            'RC1': [f'RC1{i:1d}' for i in range(1, 9)],  # RC101-RC108
            'RC2': [f'RC2{i:1d}' for i in range(1, 9)],  # RC201-RC208
        }
        
        result = {}
        for family in families:
            if family in solomon_map:
                result[family] = solomon_map[family]
            else:
                raise ValueError(f"Unknown Solomon family: {family}")
        
        return result
    
    def add_result(self, algorithm_id: str, instance_id: str, family: str,
                   run_id: int, k_final: int, k_bks: int, d_final: float,
                   d_bks: float, total_time_sec: float, iterations: int):
        """
        Add a single experiment result
        
        Args:
            All parameters for ExecutionResult
        """
        result = {
            'algorithm_id': algorithm_id,
            'instance_id': instance_id,
            'family': family,
            'run_id': run_id,
            'random_seed': self.config.seed,
            'K_final': k_final,
            'D_final': d_final,
            'K_BKS': k_bks,
            'D_BKS': d_bks,
            'delta_K': k_final - k_bks,
            'gap_distance': d_final - d_bks if k_final == k_bks else None,
            'gap_percent': ((d_final - d_bks) / d_bks * 100) if k_final == k_bks else None,
            'total_time_sec': total_time_sec,
            'iterations_executed': iterations,
            'reached_K_BKS': (k_final == k_bks)
        }
        self.raw_results.append(result)
    
    def save_raw_results(self):
        """Save raw_results.csv"""
        output_path = self.results_dir / "raw_results.csv"
        
        if not self.raw_results:
            return
        
        fieldnames = [
            'algorithm_id', 'instance_id', 'family', 'run_id', 'random_seed',
            'K_final', 'D_final', 'K_BKS', 'D_BKS', 'delta_K',
            'gap_distance', 'gap_percent', 'total_time_sec', 'iterations_executed',
            'reached_K_BKS'
        ]
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.raw_results)
    
    def save_experiment_metadata(self):
        """Save experiment_metadata.json"""
        metadata = {
            'experiment_id': self.experiment_id,
            'mode': self.config.mode,
            'timestamp': datetime.now().isoformat(),
            'families': self.config.families,
            'algorithms': self.config.algorithms,
            'total_experiments': len(self.raw_results),
            'results_location': str(self.results_dir),
            'seed': self.config.seed
        }
        
        output_path = self.results_dir / "experiment_metadata.json"
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)


class QuickExperiment:
    """QUICK mode: 1 family (R1), 3 algorithms, 1 repetition"""
    
    @staticmethod
    def get_config() -> ExperimentConfig:
        """Get QUICK mode configuration"""
        return ExperimentConfig(
            mode='QUICK',
            families=['R1'],
            algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        """Execute QUICK experiment"""
        config = QuickExperiment.get_config()
        executor = ExperimentExecutor(config)
        
        # Get instances
        solomon_data = executor.get_solomon_instances(config.families)
        
        # Simulate experiments
        total_experiments = 0
        for family, instances in solomon_data.items():
            for instance_id in instances:
                for algo_id in config.algorithms:
                    for run in range(config.repetitions):
                        # Simulate algorithm execution (mock data)
                        k_bks = random.randint(9, 12)
                        k_final = k_bks if random.random() > 0.3 else k_bks + 1
                        d_bks = random.uniform(800, 2000)
                        d_final = d_bks + random.uniform(-100, 200) if k_final == k_bks else d_bks + 100
                        
                        executor.add_result(
                            algorithm_id=algo_id,
                            instance_id=instance_id,
                            family=family,
                            run_id=run,
                            k_final=k_final,
                            k_bks=k_bks,
                            d_final=d_final,
                            d_bks=d_bks,
                            total_time_sec=random.uniform(3.0, 8.0),
                            iterations=random.randint(80, 200)
                        )
                        total_experiments += 1
        
        # Save results
        executor.save_raw_results()
        executor.save_experiment_metadata()
        
        return executor


class FullExperiment:
    """FULL mode: 6 families, 3 algorithms, 1 repetition"""
    
    @staticmethod
    def get_config() -> ExperimentConfig:
        """Get FULL mode configuration"""
        return ExperimentConfig(
            mode='FULL',
            families=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],
            algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        """Execute FULL experiment"""
        config = FullExperiment.get_config()
        executor = ExperimentExecutor(config)
        
        # Get instances
        solomon_data = executor.get_solomon_instances(config.families)
        
        # Simulate experiments
        total_experiments = 0
        for family, instances in solomon_data.items():
            for instance_id in instances:
                for algo_id in config.algorithms:
                    for run in range(config.repetitions):
                        # Simulate algorithm execution with family-dependent difficulty
                        family_base_k = {'C1': 10, 'C2': 11, 'R1': 11, 'R2': 13, 'RC1': 12, 'RC2': 14}
                        k_bks = family_base_k.get(family, 11) + random.randint(-1, 2)
                        k_final = k_bks if random.random() > (0.5 if family.startswith('C') else 0.3) else k_bks + 1
                        d_bks = random.uniform(800, 2000)
                        d_final = d_bks + random.uniform(-100, 200) if k_final == k_bks else d_bks + 100
                        
                        executor.add_result(
                            algorithm_id=algo_id,
                            instance_id=instance_id,
                            family=family,
                            run_id=run,
                            k_final=k_final,
                            k_bks=k_bks,
                            d_final=d_final,
                            d_bks=d_bks,
                            total_time_sec=random.uniform(3.0, 15.0),
                            iterations=random.randint(80, 300)
                        )
                        total_experiments += 1
        
        # Save results
        executor.save_raw_results()
        executor.save_experiment_metadata()
        
        return executor


if __name__ == "__main__":
    print("Phase 9 Experimentation Framework initialized")
    
    # Example: Generate algorithms
    gen = AlgorithmGenerator(seed=42)
    algos = gen.generate_algorithms(3)
    print(f"Generated algorithms: {algos}")
