"""
Generate statistical summary and report from experiment results.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List
import statistics


class ResultsAnalyzer:
    """Analyze and summarize experiment results"""
    
    def __init__(self, results_csv_path: str):
        """
        Initialize analyzer.
        
        Args:
            results_csv_path: Path to raw_results.csv
        """
        self.results_path = Path(results_csv_path)
        self.data = self._load_results()
    
    def _load_results(self) -> List[Dict]:
        """Load results from CSV"""
        results = []
        
        if not self.results_path.exists():
            return results
        
        with open(self.results_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key in ['k_final', 'd_final', 'k_bks', 'd_bks', 'time_sec']:
                    if key in row and row[key]:
                        try:
                            row[key] = float(row[key])
                        except (ValueError, TypeError):
                            pass
                
                results.append(row)
        
        return results
    
    def generate_summary(self, output_path: str):
        """
        Generate comprehensive summary report.
        
        Args:
            output_path: Path to save summary file
        """
        if not self.data:
            return
        
        summary = []
        summary.append("=" * 80)
        summary.append("EXPERIMENT RESULTS SUMMARY")
        summary.append("=" * 80)
        summary.append("")
        
        # Overall statistics
        summary.append("[GENERAL STATISTICS]")
        summary.append(f"  Total experiments: {len(self.data)}")
        
        algorithms = set(row.get('algorithm', 'Unknown') for row in self.data)
        summary.append(f"  Algorithms: {', '.join(sorted(algorithms))}")
        
        families = set(row.get('family', 'Unknown') for row in self.data)
        summary.append(f"  Families: {', '.join(sorted(families))}")
        
        summary.append("")
        
        # Algorithm-wise statistics
        summary.append("[ALGORITHM PERFORMANCE]")
        summary.append("")
        
        for algo in sorted(algorithms):
            algo_data = [row for row in self.data if row.get('algorithm') == algo]
            
            distances = []
            times = []
            for row in algo_data:
                try:
                    distances.append(float(row.get('d_final', 0)))
                    times.append(float(row.get('time_sec', 0)))
                except (ValueError, TypeError):
                    pass
            
            if distances:
                summary.append(f"  {algo}:")
                summary.append(f"    Instances: {len(algo_data)}")
                summary.append(f"    Avg Distance: {statistics.mean(distances):.2f}")
                summary.append(f"    Min Distance: {min(distances):.2f}")
                summary.append(f"    Max Distance: {max(distances):.2f}")
                if len(distances) > 1:
                    summary.append(f"    Std Dev:      {statistics.stdev(distances):.2f}")
                summary.append(f"    Avg Time:     {statistics.mean(times):.2f}s")
                summary.append("")
        
        # Family-wise statistics
        summary.append("[FAMILY PERFORMANCE]")
        summary.append("")
        
        for family in sorted(families):
            family_data = [row for row in self.data if row.get('family') == family]
            
            distances = []
            for row in family_data:
                try:
                    distances.append(float(row.get('d_final', 0)))
                except (ValueError, TypeError):
                    pass
            
            if distances:
                summary.append(f"  {family}:")
                summary.append(f"    Instances: {len(family_data)}")
                summary.append(f"    Avg Distance: {statistics.mean(distances):.2f}")
                summary.append(f"    Min Distance: {min(distances):.2f}")
                summary.append(f"    Max Distance: {max(distances):.2f}")
                if len(distances) > 1:
                    summary.append(f"    Std Dev:      {statistics.stdev(distances):.2f}")
                summary.append("")
        
        # Best and worst results
        summary.append("[BEST & WORST RESULTS]")
        summary.append("")
        
        sorted_by_distance = sorted(
            [(row.get('algorithm'), row.get('instance_id'), float(row.get('d_final', 0)))
             for row in self.data if row.get('d_final')],
            key=lambda x: x[2]
        )
        
        if sorted_by_distance:
            summary.append("  Best 5 Solutions:")
            for algo, instance, distance in sorted_by_distance[:5]:
                summary.append(f"    {algo:20} {instance:10} Distance: {distance:8.2f}")
            
            summary.append("")
            summary.append("  Worst 5 Solutions:")
            for algo, instance, distance in sorted_by_distance[-5:]:
                summary.append(f"    {algo:20} {instance:10} Distance: {distance:8.2f}")
        
        summary.append("")
        summary.append("=" * 80)
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(summary))
        
        # Also print to console
        print('\n'.join(summary))


def generate_summary_report(results_csv_path: str, output_path: str):
    """
    Generate summary report from results CSV.
    
    Args:
        results_csv_path: Path to raw_results.csv
        output_path: Path to save summary file
    """
    analyzer = ResultsAnalyzer(results_csv_path)
    analyzer.generate_summary(output_path)
