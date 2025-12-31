"""
GAA Orchestrator for GCP-ILS-GAA

Main entry point for the Generative Algorithm Architecture system.
Orchestrates:
1. Loading GCP problem instances
2. Initializing ILS-based configuration search
3. Running the optimization loop
4. Tracking evolution and best algorithms
5. Generating reports and analysis

Author: GAA Framework
Version: 1.0.0
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import yaml

from ast_nodes import AlgorithmNode, ast_statistics, validate_ast
from ast_evaluator import GCPInstance, InstanceLoader, ConfigurationEvaluator, BatchEvaluator
from ils_search import (
    Configuration, ILSConfig, ILSStatistics,
    IteratedLocalSearchOptimizer, ConfigurationFactory
)


# ============================================================================
# PROJECT CONFIGURATION
# ============================================================================

@dataclass
class ProjectConfig:
    """GAA project configuration"""
    
    project_name: str = "GCP-ILS-GAA"
    problem: str = "Graph Coloring Problem"
    metaheuristic: str = "Iterated Local Search"
    
    # Paths
    project_root: str = "."
    instances_dir: str = "datasets"
    results_dir: str = "results"
    
    # Instance sets
    training_instances: List[str] = None
    validation_instances: List[str] = None
    test_instances: List[str] = None
    
    # ILS search config
    max_iterations: int = 500
    perturbation_strength: float = 0.20
    acceptance_criterion: str = "better_or_equal"
    
    # Evaluation
    max_time_per_instance: float = 60
    num_workers: int = 1
    
    # Fitness weights
    fitness_weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.fitness_weights is None:
            self.fitness_weights = {
                'quality': 0.5,
                'time': 0.2,
                'robustness': 0.2,
                'feasibility': 0.1
            }
        
        if self.training_instances is None:
            self.training_instances = []
        if self.validation_instances is None:
            self.validation_instances = []
        if self.test_instances is None:
            self.test_instances = []
    
    @staticmethod
    def load_yaml(filepath: str) -> 'ProjectConfig':
        """Load configuration from YAML file"""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return ProjectConfig(**data)
    
    def save_yaml(self, filepath: str):
        """Save configuration to YAML file"""
        with open(filepath, 'w') as f:
            yaml.dump(asdict(self), f, default_flow_style=False)


# ============================================================================
# ORCHESTRATOR MAIN
# ============================================================================

class GAAOrchestrator:
    """
    Main orchestrator for GAA-ILS system.
    
    Workflow:
    1. Load configuration
    2. Load problem instances
    3. Initialize ILS optimizer
    4. Run configuration search
    5. Evaluate best configurations on test set
    6. Generate reports
    """
    
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.training_instances: List[GCPInstance] = []
        self.validation_instances: List[GCPInstance] = []
        self.test_instances: List[GCPInstance] = []
        
        self.ils_optimizer: Optional[IteratedLocalSearchOptimizer] = None
        self.best_configuration: Optional[Configuration] = None
        
        self.execution_log: Dict[str, Any] = {
            'start_time': None,
            'end_time': None,
            'duration_seconds': 0,
            'phases': {}
        }
    
    def _print_algorithm_components(self, config: Configuration, iteration: int, indent: int = 8):
        """Print the algorithm configuration components in a readable format"""
        indent_str = " " * indent
        try:
            ast = config.ast
            print(f"{indent_str}Algorithm Configuration (Iteration {iteration}):")
            print(f"{indent_str}├─ Initialization: {ast.initialization if hasattr(ast, 'initialization') else 'Unknown'}")
            print(f"{indent_str}├─ Local Search: {ast.local_search if hasattr(ast, 'local_search') else 'Unknown'}")
            print(f"{indent_str}├─ Perturbation: {ast.perturbation if hasattr(ast, 'perturbation') else 'Unknown'}")
            print(f"{indent_str}├─ Acceptance: {ast.acceptance if hasattr(ast, 'acceptance') else 'Unknown'}")
            print(f"{indent_str}└─ Fitness: {config.aggregated_fitness:.4f}")
        except Exception as e:
            print(f"{indent_str}(Algorithm details: {str(config.ast)[:60]}...)")
    
    def load_instances(self) -> None:
        """Load all problem instances"""
        print("\n" + "="*70)
        print("PHASE 1: LOADING PROBLEM INSTANCES")
        print("="*70)
        print("[GAA] Loading problem instances for training/validation/test...")
        print("[GAA] These instances will be used to evaluate algorithm configurations.\n")
        
        loader = InstanceLoader()
        
        # Training
        print(f"[GAA] Training instances (used for algorithm generation search):")
        print(f"      {self.config.training_instances}")
        for filepath in self.config.training_instances:
            try:
                instance = loader.load_instance(filepath)
                self.training_instances.append(instance)
                print(f"      ✓ {instance}")
            except Exception as e:
                print(f"      ✗ Failed to load {filepath}: {e}")
        
        # Validation
        print(f"\n[GAA] Validation instances (used to test discovered algorithms):")
        print(f"      {self.config.validation_instances}")
        for filepath in self.config.validation_instances:
            try:
                instance = loader.load_instance(filepath)
                self.validation_instances.append(instance)
                print(f"      ✓ {instance}")
            except Exception as e:
                print(f"      ✗ Failed to load {filepath}: {e}")
        
        # Test
        print(f"\n[GAA] Test instances (final evaluation on unseen data):")
        print(f"      {self.config.test_instances}")
        for filepath in self.config.test_instances:
            try:
                instance = loader.load_instance(filepath)
                self.test_instances.append(instance)
                print(f"      ✓ {instance}")
            except Exception as e:
                print(f"      ✗ Failed to load {filepath}: {e}")
        
        print(f"\n[GAA] Instance Summary:")
        print(f"      Training:   {len(self.training_instances)} instances")
        print(f"      Validation: {len(self.validation_instances)} instances")
        print(f"      Test:       {len(self.test_instances)} instances")
    
    def initialize_search(self) -> None:
        """Initialize ILS optimizer"""
        print("\n" + "="*70)
        print("PHASE 2: INITIALIZING ALGORITHM GENERATION SEARCH")
        print("="*70)
        print("[GAA] Setting up Iterated Local Search (ILS) for configuration space exploration...")
        print("[GAA] GAA will now GENERATE multiple algorithm configurations automatically.\n")
        
        ils_config = ILSConfig(
            seed=42,
            max_iterations=self.config.max_iterations,
            max_no_improve_iterations=50,
            enable_local_search=True,
            ls_max_moves=10,
            perturbation_strength=self.config.perturbation_strength,
            acceptance_criterion=self.config.acceptance_criterion,
            fitness_weights=self.config.fitness_weights
        )
        
        self.ils_optimizer = IteratedLocalSearchOptimizer(ils_config)
        self.ils_optimizer.initialize()
        
        print(f"[GAA] Configuration space:")
        print(f"      - Ordering strategies: 5 options")
        print(f"      - Local search operators: 6 options")
        print(f"      - Perturbation strategies: 5 options")
        print(f"      - Acceptance criteria: 3 options")
        print(f"      → Total possible configurations: 5×6×5×3 = 450 combinations")
        print(f"\n[GAA] Search strategy:")
        print(f"      - Algorithm: Iterated Local Search (ILS)")
        print(f"      - Max iterations: {self.config.max_iterations}")
        print(f"      - Each iteration: Generate new configuration → Test on training instances")
        print(f"      - Goal: Find best algorithm configuration (maximized fitness)")
        print(f"\n[GAA] Initial algorithm configuration:")
        self._print_algorithm_components(self.ils_optimizer.current_configuration, 0)
    
    def run_search(self) -> None:
        """Run ILS search for optimal configurations"""
        print("\n" + "="*70)
        print("PHASE 3: AUTOMATIC ALGORITHM GENERATION (ILS Search)")
        print("="*70)
        print("[GAA] Now generating and testing algorithm configurations...")
        print("[GAA] Each iteration:")
        print("      1. Create/modify algorithm configuration")
        print("      2. Execute this configuration on all training instances")
        print("      3. Measure fitness (quality, speed, robustness)")
        print("      4. Accept/reject and perturb for next iteration")
        print(f"[GAA] Starting {self.config.max_iterations} iterations...\n")
        
        if not self.training_instances:
            print("[ERROR] No training instances loaded!")
            return
        
        phase_start = time.time()
        
        # Create evaluator
        evaluator = ConfigurationEvaluator(
            self.training_instances,
            num_workers=self.config.num_workers
        )
        
        # Fitness function
        def fitness_function(config: Configuration) -> Dict[str, float]:
            """Evaluate configuration on training instances"""
            return evaluator.evaluate(config, self.config.max_time_per_instance)
        
        # Store previous best for comparison
        prev_best_fitness = -float('inf')
        
        # Callback for progress
        def progress_callback(stats: ILSStatistics):
            nonlocal prev_best_fitness
            
            if stats.iteration % 10 == 0:
                improvement = ""
                if stats.best_fitness > prev_best_fitness:
                    improvement = " ✓ MEJOR ALGORITMO ENCONTRADO"
                    prev_best_fitness = stats.best_fitness
                
                print(f"  [ITER {stats.iteration:03d}/{self.config.max_iterations}] "
                      f"best_fitness={stats.best_fitness:.4f}, "
                      f"current={stats.current_fitness:.4f}, "
                      f"time={stats.iteration_time:.2f}s{improvement}")
                
                # Show algorithm components every 50 iterations
                if stats.iteration % 50 == 0:
                    print(f"       → Mejor algoritmo hasta ahora (Iteración {stats.iteration}):")
                    self._print_algorithm_components(
                        self.ils_optimizer.best_configuration, 
                        stats.iteration, 
                        indent=12
                    )
        
        # Run search
        self.best_configuration = self.ils_optimizer.search(
            fitness_function,
            callback=progress_callback
        )
        
        phase_time = time.time() - phase_start
        
        self.execution_log['phases']['search'] = {
            'duration_seconds': phase_time,
            'iterations': len(self.ils_optimizer.history),
            'best_fitness': self.best_configuration.aggregated_fitness,
            'configurations_evaluated': len(self.ils_optimizer.history)
        }
        
        print(f"\n[GAA] ✓ Search complete in {phase_time:.2f}s")
        print(f"[GAA] Configurations evaluated: {len(self.ils_optimizer.history)}")
        print(f"[GAA] ✓✓✓ BEST ALGORITHM FOUND with fitness: {self.best_configuration.aggregated_fitness:.4f}")
        print(f"[GAA] Now validating this algorithm on unseen instances...\n")
    
    def evaluate_best_configuration(self) -> Dict[str, Any]:
        """Evaluate best configuration on validation+test sets"""
        print("="*70)
        print("PHASE 4: VALIDATING DISCOVERED ALGORITHM")
        print("="*70)
        print("[GAA] Testing the best algorithm on NEW instances (unseen during generation)...")
        print("[GAA] This validates that the algorithm GENERALIZES well.\n")
        
        if self.best_configuration is None:
            print("[ERROR] No best configuration found!")
            return {}
        
        all_instances = self.validation_instances + self.test_instances
        if not all_instances:
            print("[WARNING] No validation/test instances to evaluate!")
            return {}
        
        phase_start = time.time()
        
        evaluator = ConfigurationEvaluator(
            all_instances,
            num_workers=self.config.num_workers
        )
        
        validation_fitness = evaluator.evaluate(
            self.best_configuration,
            self.config.max_time_per_instance
        )
        
        phase_time = time.time() - phase_start
        
        # Statistics
        colors_list = list(validation_fitness.values())
        avg_colors = sum(colors_list) / len(colors_list)
        
        results = {
            'instance_results': validation_fitness,
            'average_colors': avg_colors,
            'best_colors': min(colors_list),
            'worst_colors': max(colors_list),
            'duration_seconds': phase_time
        }
        
        self.execution_log['phases']['validation'] = results
        
        print(f"[GAA] ✓ Validation complete in {phase_time:.2f}s")
        print(f"[GAA] Algorithm Performance on Test Set:")
        print(f"      Average colors: {avg_colors:.2f}")
        print(f"      Best result:    {min(colors_list)} colors")
        print(f"      Worst result:   {max(colors_list)} colors")
        print(f"[GAA] ✓ Algorithm successfully generalized to new instances!\n")
        
        return results
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive report"""
        print("="*70)
        print("PHASE 5: GENERATING FINAL REPORTS")
        print("="*70)
        print("[GAA] Creating comprehensive report of discovered algorithm...\n")
        
        if self.best_configuration is None:
            print("[ERROR] No configuration to report!")
            return {}
        
        # AST statistics
        ast_stats = ast_statistics(self.best_configuration.ast)
        is_valid, errors = validate_ast(self.best_configuration.ast)
        
        report = {
            'project': {
                'name': self.config.project_name,
                'problem': self.config.problem,
                'metaheuristic': self.config.metaheuristic
            },
            'best_configuration': {
                'fitness': self.best_configuration.aggregated_fitness,
                'fitness_scores': self.best_configuration.fitness_scores,
                'created_by': self.best_configuration.created_by,
                'ast_statistics': ast_stats,
                'is_valid': is_valid,
                'validation_errors': errors if not is_valid else []
            },
            'algorithm_representation': {
                'pseudocode': self.best_configuration.ast.to_pseudocode(),
                'json': json.loads(self.best_configuration.ast.to_json())
            },
            'execution_log': self.execution_log,
            'search_history': [
                {
                    'iteration': s.iteration,
                    'best_fitness': s.best_fitness,
                    'current_fitness': s.current_fitness,
                    'elapsed_time': s.elapsed_time,
                    'iteration_time': s.iteration_time
                }
                for s in self.ils_optimizer.history[:min(50, len(self.ils_optimizer.history))]
            ]
        }
        
        return report
    
    def save_report(self, output_dir: str = None) -> str:
        """Save report to file"""
        if output_dir is None:
            output_dir = self.config.results_dir
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        
        # Save as JSON
        report_path = Path(output_dir) / "gaa_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save best configuration
        config_path = Path(output_dir) / "best_configuration.json"
        with open(config_path, 'w') as f:
            json.dump({
                'ast': self.best_configuration.ast.to_dict(),
                'fitness': self.best_configuration.aggregated_fitness,
                'fitness_scores': self.best_configuration.fitness_scores
            }, f, indent=2)
        
        # Save pseudocode
        pseudo_path = Path(output_dir) / "best_algorithm.txt"
        with open(pseudo_path, 'w') as f:
            f.write(self.best_configuration.ast.to_pseudocode())
        
        print(f"[GAA] ✓ Reports saved to: {output_dir}/")
        print(f"      - gaa_report.json (complete report)")
        print(f"      - best_configuration.json (algorithm in JSON format)")
        print(f"      - best_algorithm.txt (algorithm pseudocode)\n")
        
        return str(output_dir)
    
    def run_complete_workflow(self) -> Dict[str, Any]:
        """
        Execute complete GAA workflow:
        1. Load instances
        2. Initialize search
        3. Run search
        4. Evaluate on test set
        5. Generate reports
        """
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " GAA - GENERATIVE ALGORITHM ARCHITECTURE ".center(68) + "█")
        print("█" + f" {self.config.project_name} ".center(68) + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        print("\n[GAA] WELCOME TO AUTOMATIC ALGORITHM GENERATION!")
        print("[GAA] This system automatically generates and optimizes algorithms.")
        print("[GAA] It searches a configuration space to find the best algorithm for your problem.\n")
        
        self.execution_log['start_time'] = time.time()
        
        try:
            # Phase 1: Load instances
            self.load_instances()
            
            # Phase 2: Initialize
            self.initialize_search()
            
            # Phase 3: Search
            self.run_search()
            
            # Phase 4: Validate
            validation_results = self.evaluate_best_configuration()
            
            # Phase 5: Report
            report = self.generate_report()
            
            self.execution_log['end_time'] = time.time()
            self.execution_log['duration_seconds'] = (
                self.execution_log['end_time'] - self.execution_log['start_time']
            )
            
            # Save reports
            self.save_report()
            
            print("█"*70)
            print("█" + " AUTOMATIC ALGORITHM GENERATION COMPLETE ".center(68) + "█")
            print("█"*70)
            print(f"\n[GAA] ✓✓✓ SUCCESS!")
            print(f"[GAA] Generated optimal algorithm in {self.execution_log['duration_seconds']:.1f} seconds")
            print(f"[GAA] Best algorithm fitness: {self.best_configuration.aggregated_fitness:.4f}")
            print(f"[GAA] See 'results/' directory for complete reports and pseudocode.\n")
            
            return report
        
        except Exception as e:
            print(f"[ERROR] Workflow failed: {e}")
            import traceback
            traceback.print_exc()
            return {}


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GAA Orchestrator for GCP-ILS-GAA")
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--results-dir', type=str, default='results',
                       help='Output directory for results')
    parser.add_argument('--quick-test', action='store_true',
                       help='Run quick test with dummy data')
    
    args = parser.parse_args()
    
    if args.quick_test:
        # Quick test with synthetic data
        print("[TEST MODE] Running quick test with synthetic data...")
        
        config = ProjectConfig(
            project_name="GCP-ILS-GAA (TEST)",
            training_instances=[],
            validation_instances=[],
            test_instances=[],
            max_iterations=5  # Minimal
        )
        
        orchestrator = GAAOrchestrator(config)
        
        # Create synthetic instances for testing
        from ast_evaluator import GCPInstance
        
        test_instance = GCPInstance(
            name="synthetic_test",
            num_vertices=10,
            num_edges=20,
            edges=[(i, (i+1) % 10) for i in range(10)]
        )
        
        orchestrator.training_instances = [test_instance]
        orchestrator.validation_instances = [test_instance]
        orchestrator.test_instances = [test_instance]
    
    else:
        # Load from configuration file
        if not os.path.exists(args.config):
            print(f"[ERROR] Config file not found: {args.config}")
            sys.exit(1)
        
        config = ProjectConfig.load_yaml(args.config)
        config.results_dir = args.results_dir
        orchestrator = GAAOrchestrator(config)
    
    # Run workflow
    report = orchestrator.run_complete_workflow()
    
    return report


if __name__ == "__main__":
    main()
