"""
Family Comparison Analysis Script

Analiza y compara resultados de experimentos entre familias.

Usa después de ejecutar: python gaa_family_experiments.py

Genera:
  - Tabla comparativa
  - Gráficos de comparación
  - Análisis estadístico
  - Reporte de hallazgos
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import statistics


@dataclass
class FamilyStats:
    """Statistics for a family"""
    family: str
    best_fitness: float
    mean_colors: float
    std_colors: float
    success_rate: float
    mean_time_ms: float
    num_instances: int
    
    def __str__(self) -> str:
        return (f"{self.family:10} | "
               f"Fitness: {self.best_fitness:.4f} | "
               f"Colors: {self.mean_colors:6.2f}±{self.std_colors:5.2f} | "
               f"Success: {self.success_rate*100:6.1f}% | "
               f"Time: {self.mean_time_ms:7.1f}ms | "
               f"Instances: {self.num_instances}")


class FamilyComparator:
    """Compare results across families"""
    
    def __init__(self, results_root: str = "results"):
        self.results_root = Path(results_root)
        self.families: Dict[str, FamilyStats] = {}
    
    def load_family_results(self) -> bool:
        """Load results from all families"""
        print("[INFO] Loading family results...\n")
        
        families = ['CUL', 'DSJ', 'LEI', 'MYC', 'REG', 'SCH', 'SGB']
        loaded = 0
        failed = 0
        
        for family in families:
            family_dir = self.results_root / family
            results_file = family_dir / "results.json"
            
            if not results_file.exists():
                print(f"[SKIP] {family}: No results found at {results_file}")
                failed += 1
                continue
            
            try:
                with open(results_file, 'r') as f:
                    results = json.load(f)
                
                # Extract top configuration
                top_config = results['top_configurations'][0]
                stats = FamilyStats(
                    family=family,
                    best_fitness=top_config['fitness'],
                    mean_colors=top_config['statistics']['mean_colors'],
                    std_colors=top_config['statistics']['std_colors'],
                    success_rate=top_config['statistics']['success_rate'],
                    mean_time_ms=top_config['statistics']['mean_time_ms'],
                    num_instances=len([f for f in 
                                     results['top_configurations'][0]
                                     .get('dataset_breakdown', {}).values()])
                )
                
                self.families[family] = stats
                print(f"[LOAD] {family}: ✓")
                loaded += 1
                
            except Exception as e:
                print(f"[ERROR] {family}: {e}")
                failed += 1
        
        print(f"\n[SUMMARY] Loaded: {loaded}, Failed: {failed}\n")
        return loaded > 0
    
    def print_comparison_table(self) -> None:
        """Print comparison table"""
        
        if not self.families:
            print("[ERROR] No families loaded")
            return
        
        print("=" * 100)
        print("FAMILY COMPARISON TABLE")
        print("=" * 100)
        print()
        print(f"{'Family':<10} | "
              f"{'Fitness':<15} | "
              f"{'Colors (mean±std)':<21} | "
              f"{'Success Rate':<15} | "
              f"{'Time (ms)':<12} | "
              f"{'Instances':<10}")
        print("-" * 100)
        
        # Sort by fitness (descending)
        sorted_families = sorted(self.families.values(), 
                                key=lambda x: x.best_fitness, 
                                reverse=True)
        
        for i, stats in enumerate(sorted_families, 1):
            fitness_str = f"{stats.best_fitness:.4f}"
            colors_str = f"{stats.mean_colors:.1f}±{stats.std_colors:.1f}"
            success_str = f"{stats.success_rate*100:.1f}%"
            time_str = f"{stats.mean_time_ms:.0f}"
            
            print(f"{i}. {stats.family:<8} | "
                  f"{fitness_str:<15} | "
                  f"{colors_str:<21} | "
                  f"{success_str:<15} | "
                  f"{time_str:<12} | "
                  f"{stats.num_instances:<10}")
        
        print("=" * 100)
        print()
    
    def print_rankings(self) -> None:
        """Print rankings by different metrics"""
        
        print("=" * 80)
        print("FAMILY RANKINGS")
        print("=" * 80)
        
        # Ranking by Fitness
        print("\n1. BY FITNESS (Higher is Better)")
        print("-" * 80)
        sorted_by_fitness = sorted(self.families.values(), 
                                   key=lambda x: x.best_fitness, 
                                   reverse=True)
        for i, stats in enumerate(sorted_by_fitness, 1):
            print(f"   {i}. {stats.family:<10} {stats.best_fitness:.4f}")
        
        # Ranking by Quality (Colors - lower is better)
        print("\n2. BY SOLUTION QUALITY (Lower colors is Better)")
        print("-" * 80)
        sorted_by_colors = sorted(self.families.values(), 
                                  key=lambda x: x.mean_colors)
        for i, stats in enumerate(sorted_by_colors, 1):
            print(f"   {i}. {stats.family:<10} {stats.mean_colors:.1f}±{stats.std_colors:.1f} colors")
        
        # Ranking by Consistency (lower std is better)
        print("\n3. BY CONSISTENCY (Lower std is Better)")
        print("-" * 80)
        sorted_by_consistency = sorted(self.families.values(), 
                                       key=lambda x: x.std_colors)
        for i, stats in enumerate(sorted_by_consistency, 1):
            print(f"   {i}. {stats.family:<10} σ = {stats.std_colors:.2f}")
        
        # Ranking by Speed (lower time is better)
        print("\n4. BY SPEED (Faster is Better)")
        print("-" * 80)
        sorted_by_speed = sorted(self.families.values(), 
                                key=lambda x: x.mean_time_ms)
        for i, stats in enumerate(sorted_by_speed, 1):
            print(f"   {i}. {stats.family:<10} {stats.mean_time_ms:.1f} ms")
        
        # Ranking by Robustness
        print("\n5. BY ROBUSTNESS (Higher success is Better)")
        print("-" * 80)
        sorted_by_robustness = sorted(self.families.values(), 
                                      key=lambda x: x.success_rate, 
                                      reverse=True)
        for i, stats in enumerate(sorted_by_robustness, 1):
            print(f"   {i}. {stats.family:<10} {stats.success_rate*100:.1f}%")
        
        print("=" * 80)
        print()
    
    def print_insights(self) -> None:
        """Print insights and findings"""
        
        if not self.families:
            return
        
        stats_list = list(self.families.values())
        
        print("=" * 80)
        print("INSIGHTS AND FINDINGS")
        print("=" * 80)
        print()
        
        # Best overall
        best_overall = max(stats_list, key=lambda x: x.best_fitness)
        print(f"🏆 BEST OVERALL: {best_overall.family}")
        print(f"   Fitness: {best_overall.best_fitness:.4f}")
        print()
        
        # Easiest (highest fitness)
        easiest = max(stats_list, key=lambda x: x.best_fitness)
        print(f"✓ EASIEST FOR GAA: {easiest.family}")
        print(f"   Reason: Highest fitness ({easiest.best_fitness:.4f})")
        print()
        
        # Hardest (lowest fitness)
        hardest = min(stats_list, key=lambda x: x.best_fitness)
        print(f"✗ HARDEST FOR GAA: {hardest.family}")
        print(f"   Reason: Lowest fitness ({hardest.best_fitness:.4f})")
        print()
        
        # Best quality (lowest colors)
        best_quality = min(stats_list, key=lambda x: x.mean_colors)
        print(f"📊 BEST SOLUTION QUALITY: {best_quality.family}")
        print(f"   Average colors: {best_quality.mean_colors:.1f}")
        print()
        
        # Most consistent
        most_consistent = min(stats_list, key=lambda x: x.std_colors)
        print(f"🔄 MOST CONSISTENT: {most_consistent.family}")
        print(f"   Std dev: {most_consistent.std_colors:.2f}")
        print()
        
        # Fastest
        fastest = min(stats_list, key=lambda x: x.mean_time_ms)
        print(f"⚡ FASTEST: {fastest.family}")
        print(f"   Time: {fastest.mean_time_ms:.1f} ms")
        print()
        
        # Most robust
        most_robust = max(stats_list, key=lambda x: x.success_rate)
        print(f"✅ MOST ROBUST: {most_robust.family}")
        print(f"   Success rate: {most_robust.success_rate*100:.1f}%")
        print()
        
        # Fitness range
        fitness_values = [s.best_fitness for s in stats_list]
        fitness_range = max(fitness_values) - min(fitness_values)
        fitness_std = statistics.stdev(fitness_values) if len(fitness_values) > 1 else 0
        print(f"📈 FITNESS VARIATION")
        print(f"   Range: {fitness_range:.4f}")
        print(f"   Std Dev: {fitness_std:.4f}")
        print()
        
        # Difficulty analysis
        avg_fitness = sum(fitness_values) / len(fitness_values)
        print(f"📍 OVERALL DIFFICULTY ANALYSIS")
        print(f"   Average fitness across families: {avg_fitness:.4f}")
        print(f"   Difficulty classes:")
        for stats in sorted(stats_list, key=lambda x: x.best_fitness, reverse=True):
            if stats.best_fitness >= avg_fitness + fitness_std:
                difficulty = "EASY ⚪"
            elif stats.best_fitness >= avg_fitness:
                difficulty = "MEDIUM 🟡"
            else:
                difficulty = "HARD 🔴"
            print(f"   - {stats.family:<10} {difficulty:<20} (fitness: {stats.best_fitness:.4f})")
        
        print("=" * 80)
        print()
    
    def generate_comparison_csv(self, output_file: str = "family_comparison.csv") -> bool:
        """Generate CSV comparison file"""
        
        try:
            with open(output_file, 'w') as f:
                # Header
                f.write("Family,Fitness,MeanColors,StdColors,SuccessRate,MeanTime_ms,Instances\n")
                
                # Data (sorted by fitness)
                sorted_families = sorted(self.families.values(), 
                                       key=lambda x: x.best_fitness, 
                                       reverse=True)
                
                for stats in sorted_families:
                    f.write(f"{stats.family},"
                           f"{stats.best_fitness:.4f},"
                           f"{stats.mean_colors:.2f},"
                           f"{stats.std_colors:.2f},"
                           f"{stats.success_rate:.4f},"
                           f"{stats.mean_time_ms:.1f},"
                           f"{stats.num_instances}\n")
            
            print(f"[SAVE] Comparison CSV saved to {output_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save CSV: {e}")
            return False
    
    def run_analysis(self) -> bool:
        """Run complete analysis"""
        
        print("\n" + "=" * 80)
        print("FAMILY COMPARISON ANALYSIS")
        print("=" * 80 + "\n")
        
        if not self.load_family_results():
            print("[ERROR] No families loaded, exiting")
            return False
        
        self.print_comparison_table()
        self.print_rankings()
        self.print_insights()
        self.generate_comparison_csv()
        
        print("[INFO] Analysis complete!")
        return True


def main():
    """Main entry point"""
    
    comparator = FamilyComparator(results_root="results")
    success = comparator.run_analysis()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
