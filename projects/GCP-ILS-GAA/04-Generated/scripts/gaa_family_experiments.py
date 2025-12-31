"""
GAA Family-Based Experimentation Script

Ejecuta experimentos GAA para cada familia de instancias de datasets.

Familias disponibles:
  - CUL: Culberson instances
  - DSJ: DIMACS-Sparse-Johnson instances  
  - LEI: Leighton instances
  - MYC: Mycielski instances
  - REG: Regular instances
  - SCH: SchURe instances
  - SGB: Stanford GraphBase instances

Uso:
  python gaa_family_experiments.py              # Todas las familias
  python gaa_family_experiments.py --family DSJ # Solo DSJ
  python gaa_family_experiments.py --family CUL --iterations 1000
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import shutil

# Try importing GAA modules
try:
    from gaa_orchestrator import GAAOrchestrator, ProjectConfig
    from ils_search import ILSConfig
except ImportError as e:
    print(f"[ERROR] Could not import GAA modules: {e}")
    print("Make sure you're running from the scripts directory")
    sys.exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

FAMILIES = {
    'CUL': 'Culberson instances - Flat graph coloring',
    'DSJ': 'DIMACS-Sparse-Johnson instances - Sparse random graphs',
    'LEI': 'Leighton instances - Structured graphs',
    'MYC': 'Mycielski instances - Mycielski construction',
    'REG': 'Regular instances - Regular degree graphs',
    'SCH': 'Schure instances - Carefully structured',
    'SGB': 'Stanford GraphBase instances - Various patterns',
}

@dataclass
class FamilyExperimentConfig:
    """Configuration for family-based experiments"""
    
    family: str                      # Family name (CUL, DSJ, etc)
    dataset_root: str = "datasets"   # Root datasets folder
    results_root: str = "results"    # Root results folder
    
    # ILS Configuration
    max_iterations: int = 500
    perturbation_strength: float = 0.20
    seed: int = 42
    
    # Reporting
    verbose: bool = True
    save_configs: bool = True
    generate_comparison: bool = True


# ============================================================================
# FAMILY EXPERIMENTER
# ============================================================================

class FamilyExperimenter:
    """Executes GAA experiments for each instance family"""
    
    def __init__(self, config: FamilyExperimentConfig):
        self.config = config
        self.family_dir = Path(config.dataset_root) / config.family
        self.results_dir = Path(config.results_root) / config.family
        self.instances: List[Path] = []
        self.family_results: Dict[str, Any] = {
            'family': config.family,
            'timestamp': datetime.now().isoformat(),
            'instances_tested': [],
            'summary': {}
        }
    
    def log(self, msg: str, level: str = "INFO"):
        """Print log message"""
        if self.config.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {msg}")
    
    def load_instances(self) -> bool:
        """Load all instances from family folder"""
        self.log(f"Loading instances from family: {self.config.family}")
        
        if not self.family_dir.exists():
            self.log(f"Family directory not found: {self.family_dir}", "ERROR")
            return False
        
        # Find all .col files
        col_files = sorted(list(self.family_dir.glob("*.col")))
        
        if not col_files:
            self.log(f"No .col files found in {self.family_dir}", "WARNING")
            return False
        
        self.instances = col_files
        self.log(f"Found {len(self.instances)} instances in {self.config.family} family")
        
        for i, instance in enumerate(self.instances, 1):
            self.log(f"  {i}. {instance.name}")
        
        return True
    
    def prepare_results_dir(self) -> bool:
        """Create and prepare results directory"""
        self.log(f"Preparing results directory: {self.results_dir}")
        
        try:
            self.results_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"Results directory ready: {self.results_dir}")
            return True
        except Exception as e:
            self.log(f"Failed to create results directory: {e}", "ERROR")
            return False
    
    def run_experiment_for_instances(self) -> bool:
        """Run GAA experiment for this family's instances"""
        
        self.log("=" * 70)
        self.log(f"RUNNING EXPERIMENT FOR FAMILY: {self.config.family}", "INFO")
        self.log("=" * 70)
        
        if not self.load_instances():
            return False
        
        if not self.prepare_results_dir():
            return False
        
        # Convert .col paths to strings for gaa_orchestrator
        training_instances = [str(p) for p in self.instances]
        
        # Create project config
        project_config = ProjectConfig(
            project_name=f"GCP-ILS-GAA-{self.config.family}",
            problem="Graph Coloring Problem",
            metaheuristic="Iterated Local Search",
            project_root=".",
            instances_dir=str(self.family_dir.parent),
            results_dir=str(self.results_dir),
            training_instances=training_instances,
            validation_instances=[],  # No separate validation for family experiments
            test_instances=[],         # No separate test set
            max_iterations=self.config.max_iterations,
            perturbation_strength=self.config.perturbation_strength,
        )
        
        # Create orchestrator
        orchestrator = GAAOrchestrator(project_config)
        
        # Run experiment
        experiment_start = time.time()
        
        try:
            self.log(f"Initializing orchestrator...")
            orchestrator.load_instances()
            orchestrator.initialize_search()
            
            self.log(f"Starting ILS search for {len(self.instances)} instances...")
            orchestrator.run_search()
            
            self.log(f"Generating reports...")
            orchestrator.generate_reports()
            
            experiment_duration = time.time() - experiment_start
            
            # Record results
            self.family_results['experiment_duration_seconds'] = experiment_duration
            self.family_results['instances_count'] = len(self.instances)
            self.family_results['max_iterations'] = self.config.max_iterations
            
            self.log(f"Experiment completed successfully in {experiment_duration:.1f} seconds")
            return True
            
        except Exception as e:
            self.log(f"Experiment failed: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False
    
    def save_family_results(self) -> bool:
        """Save family results summary"""
        try:
            results_file = self.results_dir / "family_results.json"
            with open(results_file, 'w') as f:
                json.dump(self.family_results, f, indent=2)
            self.log(f"Family results saved to {results_file}")
            return True
        except Exception as e:
            self.log(f"Failed to save family results: {e}", "ERROR")
            return False


# ============================================================================
# MULTI-FAMILY COORDINATOR
# ============================================================================

class MultiFamilyExperimenter:
    """Coordinates experiments across multiple families"""
    
    def __init__(self, families: List[str], iterations: int = 500, verbose: bool = True):
        self.families = families
        self.iterations = iterations
        self.verbose = verbose
        self.results: Dict[str, Any] = {
            'timestamp': datetime.now().isoformat(),
            'families': {},
            'summary': {}
        }
    
    def log(self, msg: str, level: str = "INFO"):
        """Print log message"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {msg}")
    
    def run_all_families(self) -> bool:
        """Run experiments for all specified families"""
        
        self.log("=" * 70, "INFO")
        self.log("STARTING MULTI-FAMILY EXPERIMENTATION", "INFO")
        self.log("=" * 70, "INFO")
        self.log(f"Families to process: {', '.join(self.families)}", "INFO")
        self.log(f"Max iterations per family: {self.iterations}", "INFO")
        self.log("=" * 70, "INFO")
        
        overall_start = time.time()
        successful_families = []
        failed_families = []
        
        for i, family in enumerate(self.families, 1):
            self.log(f"\n{'=' * 70}")
            self.log(f"FAMILY {i}/{len(self.families)}: {family}")
            self.log(f"Description: {FAMILIES.get(family, 'Unknown')}")
            self.log(f"{'=' * 70}\n")
            
            family_config = FamilyExperimentConfig(
                family=family,
                max_iterations=self.iterations,
                verbose=self.verbose
            )
            
            experimenter = FamilyExperimenter(family_config)
            
            family_start = time.time()
            success = experimenter.run_experiment_for_instances()
            family_duration = time.time() - family_start
            
            if success:
                experimenter.save_family_results()
                successful_families.append(family)
                self.results['families'][family] = {
                    'status': 'completed',
                    'duration_seconds': family_duration
                }
                self.log(f"\n✓ {family} completed successfully in {family_duration:.1f}s\n")
            else:
                failed_families.append(family)
                self.results['families'][family] = {
                    'status': 'failed',
                    'duration_seconds': family_duration
                }
                self.log(f"\n✗ {family} FAILED\n", "ERROR")
        
        overall_duration = time.time() - overall_start
        
        # Print summary
        self.log("\n" + "=" * 70)
        self.log("MULTI-FAMILY EXPERIMENTATION SUMMARY", "INFO")
        self.log("=" * 70)
        self.log(f"Total families: {len(self.families)}")
        self.log(f"Completed: {len(successful_families)} ✓")
        self.log(f"Failed: {len(failed_families)} ✗")
        self.log(f"Total time: {overall_duration:.1f} seconds ({overall_duration/60:.1f} minutes)")
        
        if successful_families:
            self.log(f"\nSuccessful families:")
            for family in successful_families:
                self.log(f"  ✓ {family}")
        
        if failed_families:
            self.log(f"\nFailed families:", "WARNING")
            for family in failed_families:
                self.log(f"  ✗ {family}", "WARNING")
        
        self.log("=" * 70 + "\n")
        
        # Save overall results
        self.results['summary'] = {
            'total_families': len(self.families),
            'successful': len(successful_families),
            'failed': len(failed_families),
            'total_duration_seconds': overall_duration,
            'successful_families': successful_families,
            'failed_families': failed_families
        }
        
        self.save_overall_results()
        
        return len(failed_families) == 0
    
    def save_overall_results(self) -> bool:
        """Save overall multi-family results"""
        try:
            results_file = Path("results") / "multi_family_summary.json"
            results_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            self.log(f"Overall results saved to {results_file}")
            return True
        except Exception as e:
            self.log(f"Failed to save overall results: {e}", "ERROR")
            return False
    
    def generate_comparison_report(self) -> bool:
        """Generate comparison report across families"""
        
        try:
            report = Path("results") / "family_comparison_report.txt"
            
            with open(report, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("MULTI-FAMILY EXPERIMENTATION COMPARISON REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Total families tested: {len(self.families)}\n")
                f.write(f"Iterations per family: {self.iterations}\n\n")
                
                f.write("FAMILY RESULTS\n")
                f.write("-" * 80 + "\n")
                f.write(f"{'Family':<15} {'Status':<12} {'Time (s)':<12} {'Description':<40}\n")
                f.write("-" * 80 + "\n")
                
                for family in sorted(self.families):
                    if family in self.results['families']:
                        status = self.results['families'][family]['status']
                        duration = self.results['families'][family]['duration_seconds']
                        description = FAMILIES.get(family, 'Unknown')[:40]
                        status_str = "✓ Completed" if status == "completed" else "✗ Failed"
                        f.write(f"{family:<15} {status_str:<12} {duration:<12.1f} {description:<40}\n")
                
                f.write("-" * 80 + "\n")
                f.write(f"{'TOTAL':<15} {self.results['summary']['total_families']:<12} "
                       f"{self.results['summary']['total_duration_seconds']:<12.1f}\n")
            
            self.log(f"Comparison report saved to {report}")
            return True
        except Exception as e:
            self.log(f"Failed to generate comparison report: {e}", "ERROR")
            return False


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='Run GAA experiments for instance families',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all families
  python gaa_family_experiments.py
  
  # Run single family
  python gaa_family_experiments.py --family DSJ
  
  # Run multiple families with custom iterations
  python gaa_family_experiments.py --families CUL DSJ LEI --iterations 1000
  
  # Run all families, quiet mode
  python gaa_family_experiments.py --quiet
        """
    )
    
    parser.add_argument(
        '--families',
        nargs='+',
        default=list(FAMILIES.keys()),
        help='Families to test (default: all)'
    )
    
    parser.add_argument(
        '--family',
        help='Single family to test (alternative to --families)'
    )
    
    parser.add_argument(
        '--iterations',
        type=int,
        default=500,
        help='Max iterations for ILS search (default: 500)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Handle single family argument
    families = [args.family] if args.family else args.families
    
    # Validate families
    invalid_families = [f for f in families if f not in FAMILIES]
    if invalid_families:
        print(f"[ERROR] Invalid families: {invalid_families}")
        print(f"Valid families: {list(FAMILIES.keys())}")
        return 1
    
    # Run experiments
    coordinator = MultiFamilyExperimenter(
        families=families,
        iterations=args.iterations,
        verbose=not args.quiet
    )
    
    success = coordinator.run_all_families()
    coordinator.generate_comparison_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
