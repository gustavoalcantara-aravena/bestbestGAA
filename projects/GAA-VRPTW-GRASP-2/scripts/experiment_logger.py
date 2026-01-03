"""
Logging System for Experiments
================================

Captures detailed information about:
- Characteristics of automatically generated algorithms
- Execution of each test
- Timing of each process
- Performance analysis and best algorithm selection
"""

import os
import json
import csv
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
import statistics


@dataclass
class AlgorithmMetadata:
    """Information about an automatically generated algorithm"""
    name: str
    pattern: str
    depth: int
    size: int
    components: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimingInfo:
    """Information about execution timing"""
    algorithm: str
    instance_id: str
    construction_time: float = 0.0
    local_search_time: float = 0.0
    total_time: float = 0.0
    algorithm_generation_time: float = 0.0


@dataclass
class ExecutionResult:
    """Result of a single execution"""
    algorithm: str
    instance_id: str
    family: str
    k_final: float
    d_final: float
    time_sec: float
    status: str = "success"
    error: Optional[str] = None
    gaa_rank: Optional[int] = None  # Rank si es GAA


class ExperimentLogger:
    """Sistema integral de logging para experimentos"""
    
    def __init__(self, output_base_dir: str = "output"):
        """
        Inicializar logger
        
        Args:
            output_base_dir: Directorio base para outputs
        """
        self.output_base = Path(output_base_dir)
        self.logs_dir = self.output_base / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos de log
        self.execution_log = self.logs_dir / "execution_log.txt"
        self.algorithm_specs = self.logs_dir / "algorithm_specifications.json"
        self.timing_report = self.logs_dir / "timing_report.csv"
        self.timing_log = self.logs_dir / "timing_log.txt"  # New: detailed timing
        self.algorithm_log = self.logs_dir / "algorithm_generation_log.txt"  # New: algorithms
        self.performance_summary = self.logs_dir / "performance_summary.txt"
        self.best_algorithm_report = self.logs_dir / "best_algorithm_report.txt"
        
        # In-memory storage
        self.algorithms: List[AlgorithmMetadata] = []
        self.execution_results: List[ExecutionResult] = []
        self.timings: List[TimingInfo] = []
        
        # Setup Python logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configurar Python logging con handlers para archivo y consola"""
        # Formatter con timestamps
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler para execution_log.txt
        file_handler = logging.FileHandler(self.execution_log, mode='w')
        file_handler.setFormatter(formatter)
        
        # Console handler para imprimir en terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Crear logger y configurarlo
        self.logger = logging.getLogger('ExperimentLogger')
        # Limpiar handlers previos si existen
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.propagate = False  # No propagar a loggers padres
    
    def log_algorithm_generated(self, algo: AlgorithmMetadata):
        """Log automatically generated algorithm details"""
        self.algorithms.append(algo)
        
        # Log to console and main log file
        algo_info = (
            f"[GAA-ALGO] Name: {algo.name} | "
            f"Pattern: {algo.pattern} | "
            f"Depth: {algo.depth}, Size: {algo.size}"
        )
        self.logger.info(algo_info)
        
        # Detailed log in algorithm generation log file
        with open(self.algorithm_log, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"ALGORITHM GENERATED: {algo.name}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"AST Pattern: {algo.pattern}\n")
            f.write(f"Depth: {algo.depth}\n")
            f.write(f"Size: {algo.size}\n")
            if algo.components:
                f.write(f"Components: {algo.components}\n")
            if algo.parameters:
                f.write(f"Parameters: {algo.parameters}\n")
    
    def log_execution_start(self, mode: str, total_experiments: int, 
                            num_algorithms: int = None, num_instances: int = None, 
                            repetitions: int = 1):
        """Log experiment execution start with breakdown details"""
        self.start_time = time.time()
        self.logger.info("=" * 80)
        self.logger.info(f"STARTING EXPERIMENTS - MODE: {mode}")
        
        # Build breakdown message
        if num_algorithms is not None and num_instances is not None:
            breakdown = f"Total exp: {total_experiments} ({num_algorithms} GAA algorithms × {num_instances} instances × {repetitions} repetition{'s' if repetitions > 1 else ''})"
        else:
            breakdown = f"Total exp: {total_experiments}"
        
        self.logger.info(breakdown)
        self.logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.logger.info("=" * 80)
        
        # Log execution start in timing_log.txt
        with open(self.timing_log, 'w') as f:
            f.write(f"{'='*80}\n")
            f.write(f"TIMING REPORT\n")
            f.write(f"{'='*80}\n")
            f.write(f"Mode: {mode}\n")
            f.write(f"Start: {datetime.now().isoformat()}\n")
            f.write(f"Total Experiments: {total_experiments}\n")
            if num_algorithms is not None:
                f.write(f"  - Algorithms: {num_algorithms}\n")
                f.write(f"  - Instances: {num_instances}\n")
                f.write(f"  - Repetitions: {repetitions}\n")
            f.write(f"{'='*80}\n\n")
    
    def log_algorithm_execution(self, 
                               algorithm: str,
                               instance_id: str,
                               family: str,
                               k_final: float,
                               d_final: float,
                               elapsed_time: float,
                               status: str = "success",
                               error: Optional[str] = None):
        """Log algorithm execution results"""
        result = ExecutionResult(
            algorithm=algorithm,
            instance_id=instance_id,
            family=family,
            k_final=k_final,
            d_final=d_final,
            time_sec=elapsed_time,
            status=status,
            error=error
        )
        self.execution_results.append(result)
        
        if status == "success":
            msg = (
                f"[OK] {algorithm:8} | {instance_id:7} ({family}) | "
                f"K={k_final:2.0f}, D={d_final:8.1f}, t={elapsed_time:6.2f}s"
            )
            self.logger.info(msg)
            
            # Log to timing_log.txt
            with open(self.timing_log, 'a') as f:
                f.write(f"{msg}\n")
        else:
            msg = (
                f"[ERROR] {algorithm:8} | {instance_id:7} ({family}) | "
                f"Error: {error}"
            )
            self.logger.error(msg)
            
            # Log to timing_log.txt
            with open(self.timing_log, 'a') as f:
                f.write(f"{msg}\n")
    
    def log_execution_end(self):
        """Log experiment completion with timing summary"""
        total_time = time.time() - self.start_time
        successful = len([r for r in self.execution_results if r.status == "success"])
        total = len(self.execution_results)
        
        # Calculate timing statistics
        times = [r.time_sec for r in self.execution_results if r.status == "success"]
        avg_time = statistics.mean(times) if times else 0
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        
        self.logger.info("=" * 80)
        self.logger.info(f"EXECUTION COMPLETED")
        self.logger.info(f"Experiments completed: {successful}/{total}")
        self.logger.info(f"Total time: {total_time:8.2f}s ({total_time/60:.2f} minutes)")
        self.logger.info("=" * 80)
        
        # Save summary to timing_log.txt
        with open(self.timing_log, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"TIMING SUMMARY\n")
            f.write(f"{'='*80}\n")
            f.write(f"End: {datetime.now().isoformat()}\n")
            f.write(f"Experiments completed: {successful}/{total}\n")
            f.write(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)\n")
            f.write(f"\nPer-experiment statistics:\n")
            f.write(f"  - Average time: {avg_time:.2f}s\n")
            f.write(f"  - Minimum time: {min_time:.2f}s\n")
            f.write(f"  - Maximum time: {max_time:.2f}s\n")
            if total > 0:
                f.write(f"  - Average time per experiment: {total_time/total:.2f}s/exp\n")
            f.write(f"{'='*80}\n")
    
    def save_algorithm_specifications(self):
        """Save specifications of generated algorithms"""
        algo_data = [asdict(algo) for algo in self.algorithms]
        
        with open(self.algorithm_specs, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_algorithms': len(self.algorithms),
                'algorithms': algo_data
            }, f, indent=2)
        
        self.logger.info(f"Algorithm specifications saved: {self.algorithm_specs}")
    
    def save_timing_report(self):
        """Save timing report"""
        with open(self.timing_report, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['algorithm', 'instance_id', 'total_time_sec', 
                           'construction_time', 'local_search_time']
            )
            writer.writeheader()
            
            for timing in self.timings:
                writer.writerow(asdict(timing))
        
        self.logger.info(f"Timing report saved: {self.timing_report}")
    
    def save_execution_results_csv(self, csv_file: Optional[Path] = None):
        """Save execution results to CSV"""
        if csv_file is None:
            csv_file = self.logs_dir / "execution_results.csv"
        
        with open(csv_file, 'w', newline='') as f:
            fieldnames = ['algorithm', 'instance_id', 'family', 'k_final', 
                         'd_final', 'time_sec', 'hit', 'status', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
            writer.writeheader()
            
            for result in self.execution_results:
                row = {
                    'algorithm': result.algorithm,
                    'instance_id': result.instance_id,
                    'family': result.family,
                    'k_final': result.k_final,
                    'd_final': result.d_final,
                    'time_sec': result.time_sec,
                    'hit': result.__dict__.get('hit', 'N/A'),
                    'status': result.status,
                    'error': result.error if hasattr(result, 'error') else ''
                }
                writer.writerow(row)
        
        self.logger.info(f"Results saved: {csv_file}")
    
    def generate_performance_summary(self):
        """Generate performance summary with comparative analysis"""
        summary_lines = []
        summary_lines.append("=" * 80)
        summary_lines.append("PERFORMANCE SUMMARY - COMPARATIVE ANALYSIS")
        summary_lines.append("=" * 80)
        summary_lines.append(f"\nTimestamp: {datetime.now().isoformat()}")
        summary_lines.append(f"Total executions: {len(self.execution_results)}")
        
        # Successful results
        successful = [r for r in self.execution_results if r.status == "success"]
        summary_lines.append(f"Successful executions: {len(successful)}")
        
        if not successful:
            summary_lines.append("\n[WARNING] No successful results available for analysis")
            return "\n".join(summary_lines)
        
        # Analysis per algorithm
        summary_lines.append("\n" + "-" * 80)
        summary_lines.append("PERFORMANCE BY ALGORITHM")
        summary_lines.append("-" * 80)
        
        algorithms = set(r.algorithm for r in successful)
        algo_stats = {}
        
        for algo in sorted(algorithms):
            results = [r for r in successful if r.algorithm == algo]
            k_values = [r.k_final for r in results]
            d_values = [r.d_final for r in results]
            times = [r.time_sec for r in results]
            
            # Count HITs (within 5% of BKS with matching K)
            hits = sum(1 for r in results if hasattr(r, 'hit') and r.hit)
            hit_rate = (hits / len(results) * 100) if results else 0
            
            algo_stats[algo] = {
                'count': len(results),
                'k_avg': statistics.mean(k_values),
                'k_min': min(k_values),
                'k_max': max(k_values),
                'd_avg': statistics.mean(d_values),
                'd_min': min(d_values),
                'd_max': max(d_values),
                'time_avg': statistics.mean(times),
                'time_total': sum(times),
                'hits': hits,
                'hit_rate': hit_rate
            }
            
            stats = algo_stats[algo]
            summary_lines.append(f"\n{algo}")
            summary_lines.append(f"  Executions:      {stats['count']}")
            summary_lines.append(f"  K (vehicles):    avg={stats['k_avg']:.2f}, "
                               f"min={stats['k_min']:.0f}, max={stats['k_max']:.0f}")
            summary_lines.append(f"  D (distance):    avg={stats['d_avg']:.2f}, "
                               f"min={stats['d_min']:.2f}, max={stats['d_max']:.2f}")
            summary_lines.append(f"  Time:            avg={stats['time_avg']:.3f}s, "
                               f"total={stats['time_total']:.1f}s")
            summary_lines.append(f"  HIT Rate (within 5% gap): {stats['hits']}/{stats['count']} ({stats['hit_rate']:.1f}%)")
        
        # Analysis per family
        summary_lines.append("\n" + "-" * 80)
        summary_lines.append("PERFORMANCE BY FAMILY")
        summary_lines.append("-" * 80)
        
        families = set(r.family for r in successful)
        
        for family in sorted(families):
            results = [r for r in successful if r.family == family]
            k_values = [r.k_final for r in results]
            d_values = [r.d_final for r in results]
            
            summary_lines.append(f"\n{family}")
            summary_lines.append(f"  Instances:       {len(results)}")
            summary_lines.append(f"  Avg K:           {statistics.mean(k_values):.2f}")
            summary_lines.append(f"  Avg D:           {statistics.mean(d_values):.2f}")
        
        # Best solutions
        summary_lines.append("\n" + "-" * 80)
        summary_lines.append("BEST SOLUTIONS")
        summary_lines.append("-" * 80)
        
        # HIT Summary
        total_hits = sum(1 for r in successful if hasattr(r, 'hit') and r.hit)
        total_rate = (total_hits / len(successful) * 100) if successful else 0
        summary_lines.append(f"\nHIT RATE (within 5% gap from BKS with K match):")
        summary_lines.append(f"  Total: {total_hits}/{len(successful)} ({total_rate:.1f}%)")
        
        # Best K
        best_k = min(successful, key=lambda r: r.k_final)
        summary_lines.append(f"\nBest K (fewest vehicles):")
        summary_lines.append(f"  Algorithm:  {best_k.algorithm}")
        summary_lines.append(f"  Instance:   {best_k.instance_id} ({best_k.family})")
        summary_lines.append(f"  K:          {best_k.k_final:.0f}")
        summary_lines.append(f"  D:          {best_k.d_final:.2f}")
        summary_lines.append(f"  Time:       {best_k.time_sec:.3f}s")
        
        # Best D (with K equal to best K)
        same_k = [r for r in successful if r.k_final == best_k.k_final]
        if same_k:
            best_d = min(same_k, key=lambda r: r.d_final)
            summary_lines.append(f"\nBest D (with K = {best_k.k_final:.0f}):")
            summary_lines.append(f"  Algorithm:  {best_d.algorithm}")
            summary_lines.append(f"  Instance:   {best_d.instance_id} ({best_d.family})")
            summary_lines.append(f"  K:          {best_d.k_final:.0f}")
            summary_lines.append(f"  D:          {best_d.d_final:.2f}")
            summary_lines.append(f"  Time:       {best_d.time_sec:.3f}s")
        
        # Most efficient (best K/time ratio)
        efficiency = [(r, r.k_final / r.time_sec if r.time_sec > 0 else float('inf')) 
                     for r in successful]
        if efficiency:
            best_eff = min(efficiency, key=lambda x: x[1])
            summary_lines.append(f"\nMost efficient (best K/time ratio):")
            summary_lines.append(f"  Algorithm:  {best_eff[0].algorithm}")
            summary_lines.append(f"  Instance:   {best_eff[0].instance_id} ({best_eff[0].family})")
            summary_lines.append(f"  K/time:     {best_eff[1]:.2f}")
        
        summary_lines.append("\n" + "=" * 80)
        
        return "\n".join(summary_lines)
    
    def generate_best_algorithm_report(self) -> str:
        """Generate report identifying the best algorithm"""
        if not self.execution_results:
            return "No results available for analysis"
        
        successful = [r for r in self.execution_results if r.status == "success"]
        if not successful:
            return "No successful executions"
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("BEST ALGORITHM SELECTION")
        report_lines.append("=" * 80)
        report_lines.append(f"\nTimestamp: {datetime.now().isoformat()}")
        
        # Scoring by multiple criteria
        algorithms = set(r.algorithm for r in successful)
        scores = {}
        
        for algo in algorithms:
            results = [r for r in successful if r.algorithm == algo]
            
            # Criterion 1: Minimize K (primary)
            k_avg = statistics.mean(r.k_final for r in results)
            
            # Criterion 2: Minimize D (secondary)
            d_avg = statistics.mean(r.d_final for r in results)
            
            # Criterion 3: Minimize time
            time_avg = statistics.mean(r.time_sec for r in results)
            
            # Criterion 4: Consistency (variance in K)
            k_values = [r.k_final for r in results]
            k_std = statistics.stdev(k_values) if len(k_values) > 1 else 0
            
            # Lexicographic score
            scores[algo] = {
                'k_avg': k_avg,
                'd_avg': d_avg,
                'time_avg': time_avg,
                'k_std': k_std,
                'count': len(results)
            }
        
        # Display scores
        report_lines.append("\nSCORES BY ALGORITHM:")
        report_lines.append("-" * 80)
        
        sorted_by_k = sorted(scores.items(), key=lambda x: x[1]['k_avg'])
        for i, (algo, score) in enumerate(sorted_by_k, 1):
            report_lines.append(f"\n{i}. {algo}")
            report_lines.append(f"   Instances tested:     {score['count']}")
            report_lines.append(f"   Avg K:                {score['k_avg']:.2f} ± {score['k_std']:.2f}")
            report_lines.append(f"   Avg D:                {score['d_avg']:.2f}")
            report_lines.append(f"   Avg time:             {score['time_avg']:.3f}s")
        
        # Best algorithm
        best_algo = sorted_by_k[0][0]
        best_score = sorted_by_k[0][1]
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append(f"SELECTED ALGORITHM: {best_algo}")
        report_lines.append("=" * 80)
        report_lines.append(f"\nJustification:")
        report_lines.append(f"  • Lowest avg K: {best_score['k_avg']:.2f} vehicles")
        report_lines.append(f"  • K variance: {best_score['k_std']:.2f} (consistency)")
        report_lines.append(f"  • Avg D: {best_score['d_avg']:.2f}")
        report_lines.append(f"  • Avg time: {best_score['time_avg']:.3f}s")
        
        report_lines.append("\n" + "=" * 80)
        
        return "\n".join(report_lines)
    
    def save_all_reports(self):
        """Save all generated reports to files"""
        # Performance Summary
        summary = self.generate_performance_summary()
        with open(self.performance_summary, 'w') as f:
            f.write(summary)
        self.logger.info(f"Performance summary saved: {self.performance_summary}")
        
        # Best Algorithm Report
        best_algo_report = self.generate_best_algorithm_report()
        with open(self.best_algorithm_report, 'w') as f:
            f.write(best_algo_report)
        self.logger.info(f"Best algorithm report saved: {self.best_algorithm_report}")
    
    def print_summary(self):
        """Print summary to console"""
        print("\n" + self.generate_performance_summary())
        print("\n" + self.generate_best_algorithm_report())


# Example usage
if __name__ == "__main__":
    logger = ExperimentLogger()
    
    # Simulate algorithm generation
    logger.log_algorithm_generated(AlgorithmMetadata(
        name="GAA_Algorithm_1",
        pattern="Pattern_A",
        depth=3,
        size=15,
        components={'construction': 'Type_1'},
        parameters={'alpha': 0.5, 'beta': 0.7}
    ))
    
    logger.log_execution_start(mode="QUICK", total_experiments=36)
    
    # Simulate executions
    for i in range(5):
        logger.log_algorithm_execution(
            algorithm="GRASP",
            instance_id=f"R101",
            family="R1",
            k_final=21,
            d_final=1719.75,
            elapsed_time=0.45
        )
    
    logger.log_execution_end()
    logger.save_all_reports()
    logger.print_summary()
