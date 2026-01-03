"""
Phase 9: Experimentation Scripts - QUICK and FULL modes for GAA-VRPTW evaluation

Responsabilidades:
1. Execute GRASP/VND/ILS on REAL Solomon datasets
2. QUICK: R1 family (12 instances) - ~10 minutes
3. FULL: All 6 families (56 instances) - ~45 minutes
4. Comprehensive result collection and output generation
"""

import os
import json
import csv
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.loader import SolomonLoader
from src.metaheuristic.grasp import GRASP
from src.metaheuristic.vnd import VariableNeighborhoodDescent
from src.metaheuristic.ils import IteratedLocalSearch
from src.gaa.interpreter import ASTInterpreter
from src.gaa.ast_nodes import (
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair
)

# Handle both relative and absolute imports
try:
    from .visualization import generate_visualizations
    from .analysis import generate_summary_report
    from .route_visualization import generate_route_visualizations
    from .experiment_logger import ExperimentLogger, AlgorithmMetadata
except ImportError:
    from visualization import generate_visualizations
    from analysis import generate_summary_report
    from route_visualization import generate_route_visualizations
    from experiment_logger import ExperimentLogger, AlgorithmMetadata

try:
    from gaa import AlgorithmGenerator
except ImportError:
    # Fallback if gaa is not available
    print("[WARNING] gaa module not found, using legacy algorithm generator")
    AlgorithmGenerator = None


def dict_to_ast(ast_dict: Dict[str, Any]) -> ASTNode:
    """
    Converts AST dict representation to ASTNode object for execution.
    
    The AST generator creates ASTNode objects and serializes them to dicts via to_dict().
    This function reconstructs the ASTNode hierarchy from the dict representation.
    
    Args:
        ast_dict: Dictionary representation of AST (from algo['ast'])
    
    Returns:
        ASTNode object that can be executed by ASTInterpreter
    
    Raises:
        ValueError: If ast_dict has unknown node type
    """
    # If already an ASTNode, return as-is
    if isinstance(ast_dict, ASTNode):
        return ast_dict
    
    if not isinstance(ast_dict, dict):
        raise ValueError(f"Expected dict or ASTNode, got {type(ast_dict)}")
    
    node_type = ast_dict.get('type')
    
    if node_type == 'Seq':
        body = [dict_to_ast(item) for item in ast_dict.get('body', [])]
        return Seq(body=body)
    
    elif node_type == 'While':
        body = dict_to_ast(ast_dict.get('body'))
        max_iterations = ast_dict.get('max_iterations', 100)
        return While(max_iterations=max_iterations, body=body)
    
    elif node_type == 'For':
        iterations = ast_dict.get('iterations')
        body = dict_to_ast(ast_dict.get('body'))
        return For(iterations=iterations, body=body)
    
    elif node_type == 'If':
        condition = ast_dict.get('condition')
        then_branch = dict_to_ast(ast_dict.get('then_branch'))
        else_branch = dict_to_ast(ast_dict.get('else_branch')) if ast_dict.get('else_branch') else None
        return If(condition=condition, then_branch=then_branch, else_branch=else_branch)
    
    elif node_type == 'ChooseBestOf':
        branches = [dict_to_ast(b) for b in ast_dict.get('branches', [])]
        return ChooseBestOf(branches=branches)
    
    elif node_type == 'ApplyUntilNoImprove':
        max_no_improve = ast_dict.get('max_no_improve')
        body = dict_to_ast(ast_dict.get('body'))
        return ApplyUntilNoImprove(max_no_improve=max_no_improve, body=body)
    
    elif node_type == 'GreedyConstruct':
        heuristic = ast_dict.get('heuristic')
        alpha = ast_dict.get('alpha')
        return GreedyConstruct(heuristic=heuristic, alpha=alpha)
    
    elif node_type == 'LocalSearch':
        operator = ast_dict.get('operator')
        max_iterations = ast_dict.get('max_iterations')
        return LocalSearch(operator=operator, max_iterations=max_iterations)
    
    elif node_type == 'Perturbation':
        operator = ast_dict.get('operator')
        return Perturbation(operator=operator)
    
    elif node_type == 'Repair':
        operator = ast_dict.get('operator')
        return Repair(operator=operator)
    
    else:
        raise ValueError(f"Unknown AST node type: {node_type}")


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


class AlgorithmGeneratorLegacy:
    """Generates GAA algorithms (once per session, seed=42) - LEGACY VERSION FOR METADATA ONLY"""
    
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
        
        print(f"\n[INFO] Generando {num_algorithms} algoritmos GAA con seed={self.seed}...")
        print("=" * 70)
        
        for i in range(1, num_algorithms + 1):
            algo_id = f"GAA_Algorithm_{i}"
            
            # Generate algorithm metadata
            alpha = round(random.uniform(0.1, 0.9), 2)
            beta = round(random.uniform(0.1, 0.9), 2)
            max_iter = 100 + i * 50
            
            algo_data = {
                'algorithm_id': algo_id,
                'seed': self.seed,
                'version': '1.0',
                'components': {
                    'construction': f'ConstructionHeuristic_{i}',
                    'local_search': f'LocalSearch_{i}',
                    'parameters': {
                        'alpha': alpha,
                        'beta': beta,
                        'max_iterations': max_iter
                    }
                },
                'description': f'Auto-generated GAA algorithm #{i} with seed={self.seed}'
            }
            
            # Save to JSON
            algo_file = self.output_dir / f"{algo_id}.json"
            with open(algo_file, 'w') as f:
                json.dump(algo_data, f, indent=2)
            
            # Print algorithm details
            print(f"  [{i}/{num_algorithms}] {algo_id}")
            print(f"        alpha={alpha}, beta={beta}, max_iter={max_iter}")
            print(f"        Construction: {algo_data['components']['construction']}")
            print(f"        LocalSearch:  {algo_data['components']['local_search']}")
            
            algorithm_ids.append(algo_id)
        
        print("=" * 70)
        return algorithm_ids


class ExperimentExecutor:
    """Manages experiment execution with REAL Solomon datasets"""
    
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
        
        # Load REAL datasets
        print("[INFO] Cargando datasets REALES de Solomon...")
        self.loader = SolomonLoader()
        self.all_instances = self.loader.load_all_instances('datasets')
        total_loaded = sum(len(v) for v in self.all_instances.values())
        print(f"[OK] {total_loaded}/56 instancias cargadas")
        
        # Load BKS
        self.bks_data = self._load_bks()
        
        # Data accumulation
        self.raw_results = []
    
    def _load_bks(self) -> Dict:
        """Load Best Known Solutions from JSON"""
        bks_file = Path('datasets') / 'bks.json'
        if bks_file.exists():
            with open(bks_file) as f:
                return json.load(f)
        return {}
    
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
            'RC1': [f'RC1{i:02d}' for i in range(1, 9)],  # RC101-RC108
            'RC2': [f'RC2{i:02d}' for i in range(1, 9)],  # RC201-RC208
        }
        
        result = {}
        for family in families:
            if family in solomon_map:
                result[family] = solomon_map[family]
            else:
                raise ValueError(f"Unknown Solomon family: {family}")
        
        return result
    
    def add_result(self, algorithm_id: str = None, instance_id: str = None, family: str = None,
                   run_id: int = None, k_final: int = None, k_bks: int = None, d_final: float = None,
                   d_bks: float = None, total_time_sec: float = None, iterations: int = None, 
                   metric_dict: Dict = None):
        """
        Add experiment result - supports both signature styles
        
        Args (dict style - for new experiments):
            metric_dict: Dictionary with metrics
            
        Args (param style - for GAA):
            algorithm_id, instance_id, family, run_id, k_final, k_bks, d_final, d_bks, total_time_sec, iterations
        """
        # Support dict-based calls (for real datasets experiments)
        if metric_dict is not None:
            # This is the new dict-based approach
            result = metric_dict.copy()
            
            instance_id = result.get('instance_id')
            family = result.get('family')
            
            # Get BKS if available
            if instance_id and family:
                bks_key = f"{family}/{instance_id}"
                if bks_key in self.bks_data:
                    bks = self.bks_data[bks_key]
                    result['k_bks'] = bks.get('K')
                    result['d_bks'] = bks.get('D')
                    
                    # Calculate GAP metrics
                    k_final = result.get('k_final')
                    d_final = result.get('d_final')
                    k_bks = result.get('k_bks')
                    d_bks = result.get('d_bks')
                    
                    # delta_K: difference in vehicles
                    if k_final is not None and k_bks is not None:
                        result['delta_K'] = int(k_final) - int(k_bks)
                        result['reached_K_BKS'] = (int(k_final) == int(k_bks))
                    
                    # gap_distance and gap_percent: only if K matches
                    if (k_final is not None and k_bks is not None and 
                        int(k_final) == int(k_bks) and d_final is not None and d_bks is not None):
                        result['gap_distance'] = float(d_final) - float(d_bks)
                        result['gap_percent'] = ((float(d_final) - float(d_bks)) / float(d_bks)) * 100
                        
                        # HIT: within 5% of BKS when K matches
                        result['hit'] = (result['gap_percent'] <= 5.0)
                    else:
                        result['hit'] = False
            
            self.raw_results.append(result)
        
        # Support original parameter-based calls (for GAA)
        else:
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
                'delta_K': k_final - k_bks if (k_final is not None and k_bks is not None) else None,
                'gap_distance': d_final - d_bks if (k_final == k_bks and d_final is not None and d_bks is not None) else None,
                'gap_percent': ((d_final - d_bks) / d_bks * 100) if (k_final == k_bks and d_final is not None and d_bks is not None) else None,
                'total_time_sec': total_time_sec,
                'iterations_executed': iterations,
                'reached_K_BKS': (k_final == k_bks) if (k_final is not None and k_bks is not None) else None
            }
            
            # HIT for parameter-based calls
            if result['gap_percent'] is not None and result['gap_percent'] <= 5.0:
                result['hit'] = True
            else:
                result['hit'] = False
                
            self.raw_results.append(result)
    
    def save_raw_results(self):
        """Save raw_results.csv"""
        output_path = self.results_dir / "raw_results.csv"
        
        if not self.raw_results:
            return
        
        # Collect all possible fieldnames from all results
        all_fieldnames = set()
        for result in self.raw_results:
            all_fieldnames.update(result.keys())
        
        # Sort fieldnames for consistent order
        fieldnames = sorted(list(all_fieldnames))
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
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
        """Execute QUICK experiment with REAL Solomon datasets"""
        config = QuickExperiment.get_config()
        
        # Initialize executor FIRST to get the correct output directory
        executor = ExperimentExecutor(config)
        
        # Initialize logger with the correct output directory
        logger = ExperimentLogger(output_base_dir=str(executor.output_dir))
        
        # Generate algorithms using proper GAA framework
        print("\n" + "="*70)
        print(f"[GAA] Generando 3 algoritmos - ITER-3 (CONTROL)")
        print("="*70)
        
        gaa_generator = AlgorithmGenerator(seed=config.seed)
        gaa_algorithms = gaa_generator.generate_three_algorithms()
        gaa_generator.save_algorithms(gaa_algorithms)
        
        print(f"[OK] {len(gaa_algorithms)} algoritmos GAA generados")
        
        # Registrar algoritmos generados en el logger
        for algo in gaa_algorithms:
            logger.log_algorithm_generated(AlgorithmMetadata(
                name=algo['name'],
                pattern=algo['pattern'],
                depth=algo['stats']['depth'],
                size=algo['stats']['size'],
                components={'structure': 'AST'},
                parameters={'seed': config.seed}
            ))
            print(f"  - {algo['name']}: patrón={algo['pattern']}, depth={algo['stats']['depth']}, size={algo['stats']['size']}")
        
        # Get instances
        solomon_data = executor.get_solomon_instances(config.families)
        
        # Use generated GAA algorithms instead of hardcoded GRASP/VND/ILS
        algorithms_to_test = gaa_algorithms
        total_instances = sum(len(instances) for instances in solomon_data.values())
        total_experiments = len(algorithms_to_test) * total_instances  # 3 * 12 = 36 for QUICK
        completed = 0
        best_solutions_by_instance = {}
        
        # Log execution start with breakdown
        logger.log_execution_start(mode=config.mode, total_experiments=total_experiments,
                                  num_algorithms=len(algorithms_to_test), 
                                  num_instances=total_instances,
                                  repetitions=config.repetitions)
        
        # Create progress bar for all experiments
        pbar = tqdm(total=total_experiments, desc="Experiments", unit="exp", ncols=80)
        
        # Initialize ASTInterpreter for executing GAA algorithms
        interpreter = ASTInterpreter()
        
        for family in config.families:
            for instance_id in solomon_data[family]:
                instance = executor.all_instances[family][instance_id]
                
                # Execute each GAA algorithm (3 algorithms total)
                for algo_dict in algorithms_to_test:
                    algo_name = algo_dict['name']  # 'GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'
                    start_time = time.time()
                    
                    try:
                        # Reconstruct AST from dict representation
                        ast_dict = algo_dict['ast']
                        ast_node = dict_to_ast(ast_dict)
                        
                        # Execute algorithm using ASTInterpreter
                        solution = interpreter.execute(ast_node, instance)
                        
                        # Extract results
                        k_final = solution.num_vehicles
                        d_final = solution.total_distance
                        elapsed = time.time() - start_time
                        
                        # VALIDATE FEASIBILITY
                        feasible = solution.feasible
                        if not feasible:
                            print(f"[WARNING] INFEASIBLE solution for {algo_name} on {instance_id}: K={k_final}, D={d_final}")
                        
                        metrics = {
                            'algorithm': algo_name,
                            'instance_id': instance_id,
                            'family': family,
                            'k_final': k_final,
                            'd_final': d_final,
                            'time_sec': elapsed,
                            'feasible': feasible,
                            'status': 'success'
                        }
                        executor.add_result(metric_dict=metrics)
                        
                        # Log execution
                        logger.log_algorithm_execution(
                            algorithm=algo_name,
                            instance_id=instance_id,
                            family=family,
                            k_final=k_final,
                            d_final=d_final,
                            elapsed_time=elapsed,
                            status='success'
                        )
                        
                        status = "[OK]"
                        
                    except Exception as e:
                        elapsed = time.time() - start_time
                        error_msg = str(e)
                        metrics = {
                            'algorithm': algo_name,
                            'instance_id': instance_id,
                            'family': family,
                            'status': 'failed',
                            'error': error_msg,
                            'time_sec': elapsed
                        }
                        executor.add_result(metric_dict=metrics)
                        
                        # Log error
                        logger.log_algorithm_execution(
                            algorithm=algo_name,
                            instance_id=instance_id,
                            family=family,
                            k_final=0,
                            d_final=0,
                            elapsed_time=elapsed,
                            status='failed',
                            error=error_msg
                        )
                        
                        status = "[ERROR]"
                    
                    completed += 1
                    pbar.update(1)
                    k = metrics.get('k_final', '?')
                    d = metrics.get('d_final', '?')
                    t = metrics.get('time_sec', '?')
                    
                    # Format output - handle both numeric and error cases
                    if isinstance(d, (int, float)) and isinstance(t, (int, float)):
                        print(f"  {status} {algo_name:18} {instance_id:7} - K={k:2}, D={d:8.1f}, t={t:5.2f}s  [{completed}/{total_experiments}]")
                    else:
                        print(f"  {status} {algo_name:18} {instance_id:7} - K={k}, D={d}, t={t}s  [{completed}/{total_experiments}]")
        
        pbar.close()
        
        # Log execution end
        logger.log_execution_end()
        
        # Save results
        print("\n[INFO] Guardando resultados...")
        executor.save_raw_results()
        executor.save_experiment_metadata()
        
        # Save logger reports
        logger.save_algorithm_specifications()
        logger.save_execution_results_csv(executor.results_dir / "raw_results_detailed.csv")
        logger.save_all_reports()
        
        # Print summaries
        logger.print_summary()
        
        # Generate visualizations
        print("[INFO] Generando visualizaciones...")
        try:
            generate_visualizations(
                str(executor.results_dir / "raw_results.csv"),
                str(executor.plots_dir)
            )
            print(f"[INFO] Gráficos guardados en: {executor.plots_dir}")
        except Exception as e:
            print(f"[WARNING] Error generando gráficos: {e}")
        
        # Generate summary report
        print("[INFO] Generando resumen de resultados...")
        try:
            generate_summary_report(
                str(executor.results_dir / "raw_results.csv"),
                str(executor.results_dir / "summary_report.txt")
            )
        except Exception as e:
            print(f"[WARNING] Error generando reporte: {e}")
        
        # Generate GAP data JSON
        print("[INFO] Generando datos de GAP en JSON...")
        try:
            from gap_data_generator import generate_gap_data_json
            json_output = executor.results_dir / "gap_data.json"
            generate_gap_data_json(
                str(executor.results_dir / "raw_results.csv"),
                str(json_output)
            )
        except Exception as e:
            print(f"[WARNING] Error generando JSON de GAP: {e}")
        
        # Generate GAP comparison visualizations automatically
        print("\n[INFO] Generando gráficas de comparación GAP...")
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "plot_gap_comparison.py"],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                # Print the output from plot_gap_comparison.py
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"[WARNING] Error generando gráficas GAP: {result.stderr}")
        except Exception as e:
            print(f"[WARNING] Error en generación automática de gráficas: {e}")
        
        print(f"\n[SUMMARY] {completed}/{total_experiments} completados")
        print(f"[RESULTS] {executor.results_dir}\n")
        
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
        """Execute FULL experiment with REAL Solomon datasets"""
        config = FullExperiment.get_config()
        
        # Initialize executor FIRST
        executor = ExperimentExecutor(config)
        
        # Initialize logger with the correct output directory
        logger = ExperimentLogger(output_base_dir=str(executor.output_dir))
        
        # Generate algorithms using proper GAA framework
        print("\n" + "="*70)
        print(f"[GAA] Generando 3 algoritmos - ITER-3 (CONTROL)")
        print("="*70)
        
        gaa_generator = AlgorithmGenerator(seed=config.seed)
        gaa_algorithms = gaa_generator.generate_three_algorithms()
        gaa_generator.save_algorithms(gaa_algorithms)
        
        print(f"[OK] {len(gaa_algorithms)} algoritmos GAA generados")
        
        # Registrar algoritmos generados en el logger
        for algo in gaa_algorithms:
            logger.log_algorithm_generated(AlgorithmMetadata(
                name=algo['name'],
                pattern=algo['pattern'],
                depth=algo['stats']['depth'],
                size=algo['stats']['size'],
                components={'structure': 'AST'},
                parameters={'seed': config.seed}
            ))
            print(f"  - {algo['name']}: patrón={algo['pattern']}, depth={algo['stats']['depth']}, size={algo['stats']['size']}")
        
        # Get instances
        solomon_data = executor.get_solomon_instances(config.families)
        
        # Calculate total experiments: 3 algorithms × 56 instances (all families)
        algorithms_to_test = ['GRASP', 'VND', 'ILS']
        total_instances = sum(len(instances) for instances in solomon_data.values())
        total_experiments = len(gaa_algorithms) * total_instances  # 3 * 56 = 168 for FULL
        completed = 0
        best_solutions_by_instance = {}
        
        # Log execution start with breakdown
        logger.log_execution_start(mode=config.mode, total_experiments=total_experiments,
                                  num_algorithms=len(gaa_algorithms), 
                                  num_instances=total_instances,
                                  repetitions=config.repetitions)
        
        # Create progress bar for all experiments
        pbar = tqdm(total=total_experiments, desc="Experiments", unit="exp", ncols=80)
        
        # Initialize ASTInterpreter for executing GAA algorithms
        interpreter = ASTInterpreter()
        
        for family in config.families:
            for instance_id in solomon_data[family]:
                instance = executor.all_instances[family][instance_id]
                
                # Execute each GAA algorithm (3 algorithms total)
                for algo_dict in gaa_algorithms:
                    algo_name = algo_dict['name']  # 'GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'
                    start_time = time.time()
                    
                    try:
                        # Reconstruct AST from dict representation
                        ast_dict = algo_dict['ast']
                        ast_node = dict_to_ast(ast_dict)
                        
                        # Execute algorithm using ASTInterpreter
                        solution = interpreter.execute(ast_node, instance)
                        
                        # Extract results
                        k_final = solution.num_vehicles
                        d_final = solution.total_distance
                        elapsed = time.time() - start_time
                        
                        # VALIDATE FEASIBILITY
                        feasible = solution.feasible
                        if not feasible:
                            print(f"[WARNING] INFEASIBLE solution for {algo_name} on {instance_id}: K={k_final}, D={d_final}")
                        
                        metrics = {
                            'algorithm': algo_name,
                            'instance_id': instance_id,
                            'family': family,
                            'k_final': k_final,
                            'd_final': d_final,
                            'time_sec': elapsed,
                            'feasible': feasible,
                            'status': 'success'
                        }
                        executor.add_result(metric_dict=metrics)
                        
                        # Log execution
                        logger.log_algorithm_execution(
                            algorithm=algo_name,
                            instance_id=instance_id,
                            family=family,
                            k_final=k_final,
                            d_final=d_final,
                            elapsed_time=elapsed,
                            status='success'
                        )
                        
                        status = "[OK]"
                        
                    except Exception as e:
                        elapsed = time.time() - start_time
                        error_msg = str(e)
                        metrics = {
                            'algorithm': algo_name,
                            'instance_id': instance_id,
                            'family': family,
                            'status': 'failed',
                            'error': error_msg,
                            'time_sec': elapsed
                        }
                        executor.add_result(metric_dict=metrics)
                        
                        # Log error
                        logger.log_algorithm_execution(
                            algorithm=algo_name,
                            instance_id=instance_id,
                            family=family,
                            k_final=0,
                            d_final=0,
                            elapsed_time=elapsed,
                            status='failed',
                            error=error_msg
                        )
                        
                        status = "[ERROR]"
                    
                    completed += 1
                    pbar.update(1)
                    k = metrics.get('k_final', '?')
                    d = metrics.get('d_final', '?')
                    t = metrics.get('time_sec', '?')
                    
                    # Format output - handle both numeric and error cases
                    if isinstance(d, (int, float)) and isinstance(t, (int, float)):
                        print(f"  {status} {algo_name:18} {instance_id:7} - K={k:2}, D={d:8.1f}, t={t:5.2f}s  [{completed}/{total_experiments}]")
                    else:
                        print(f"  {status} {algo_name:18} {instance_id:7} - K={k}, D={d}, t={t}s  [{completed}/{total_experiments}]")
        
        pbar.close()
        
        # Log execution end
        logger.log_execution_end()
        
        # Save results
        print("\n[INFO] Guardando resultados...")
        executor.save_raw_results()
        executor.save_experiment_metadata()
        
        # Save logger reports
        logger.save_algorithm_specifications()
        logger.save_execution_results_csv(executor.results_dir / "raw_results_detailed.csv")
        logger.save_all_reports()
        
        # Print summaries
        logger.print_summary()
        
        # Generate visualizations
        print("[INFO] Generando visualizaciones...")
        try:
            generate_visualizations(
                str(executor.results_dir / "raw_results.csv"),
                str(executor.plots_dir)
            )
            print(f"[INFO] Gráficos guardados en: {executor.plots_dir}")
        except Exception as e:
            print(f"[WARNING] Error generando gráficos: {e}")
        
        # Generate summary report
        print("[INFO] Generando resumen de resultados...")
        try:
            generate_summary_report(
                str(executor.results_dir / "raw_results.csv"),
                str(executor.results_dir / "summary_report.txt")
            )
        except Exception as e:
            print(f"[WARNING] Error generando reporte: {e}")
        
        # Generate GAP data JSON
        print("[INFO] Generando datos de GAP en JSON...")
        try:
            from gap_data_generator import generate_gap_data_json
            json_output = executor.results_dir / "gap_data.json"
            generate_gap_data_json(
                str(executor.results_dir / "raw_results.csv"),
                str(json_output)
            )
        except Exception as e:
            print(f"[WARNING] Error generando JSON de GAP: {e}")
        
        # Generate GAP comparison visualizations automatically
        print("\n[INFO] Generando gráficas de comparación GAP...")
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "plot_gap_comparison.py"],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                # Print the output from plot_gap_comparison.py
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"[WARNING] Error generando gráficas GAP: {result.stderr}")
        except Exception as e:
            print(f"[WARNING] Error en generación automática de gráficas: {e}")
        
        print(f"\n[SUMMARY] {completed}/{total_experiments} completados")
        print(f"[RESULTS] {executor.results_dir}\n")
        
        return executor


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run QUICK or FULL experiments')
    parser.add_argument('--mode', choices=['QUICK', 'FULL'], default='QUICK',
                       help='QUICK: R1 family (12 instances), FULL: all families (56 instances)')
    
    args = parser.parse_args()
    
    if args.mode == 'QUICK':
        print("\n" + "="*70)
        print("  QUICK EXPERIMENT: R1 family (12 instances)")
        print("  Algoritmo 2: CONTROL (ITER-3)")
        print("  Algoritmos: GAA con DATASETS REALES")
        print("="*70)
        QuickExperiment.run()
    else:
        print("\n" + "="*70)
        print("  FULL EXPERIMENT: All 6 families (56 instances)")
        print("  Algoritmo 2: CONTROL (ITER-3)")
        print("  Algoritmos: GAA con DATASETS REALES")
        print("="*70)
        FullExperiment.run()

