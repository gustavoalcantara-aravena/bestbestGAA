#!/usr/bin/env python3
"""
Compare GAA Results Against Best Known Solutions (BKS)

This script compares the solutions found by GAA with the Best Known Solutions
from academic literature, computing optimality gaps and other metrics.

Usage:
    python compare_with_bks.py --results-dir results/ --output-file comparison.txt
    python compare_with_bks.py --family CUL --output-format json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ComparisonStatus(Enum):
    """Status of comparison between GAA and BKS"""
    OPTIMAL_FOUND = "✅ OPTIMAL"
    BEAT_BKS = "🎉 BEAT BKS"
    NEAR_BKS = "⚠️  NEAR BKS"
    GAP_ACCEPTABLE = "⚠️  GAP OK"
    GAP_LARGE = "❌ GAP LARGE"
    OPEN_INSTANCE = "❓ OPEN"


@dataclass
class ComparisonResult:
    """Result of comparing GAA solution to BKS"""
    instance_name: str
    family: str
    gaa_value: int
    bks_value: Optional[int]
    optimal: bool
    open: bool
    gap_percent: Optional[float]
    status: ComparisonStatus
    
    def to_dict(self) -> Dict:
        return {
            'instance': self.instance_name,
            'family': self.family,
            'gaa': self.gaa_value,
            'bks': self.bks_value,
            'optimal': self.optimal,
            'open': self.open,
            'gap_percent': self.gap_percent,
            'status': self.status.value
        }


class BKSComparator:
    """Compare GAA results against Best Known Solutions"""
    
    def __init__(self, bks_file: str = 'datasets/BKS.json'):
        """Initialize comparator with BKS data"""
        self.bks_file = Path(bks_file)
        self.bks_data = self._load_bks_data()
        self.results: List[ComparisonResult] = []
    
    def _load_bks_data(self) -> Dict:
        """Load BKS data from JSON file"""
        if not self.bks_file.exists():
            raise FileNotFoundError(f"BKS file not found: {self.bks_file}")
        
        with open(self.bks_file, 'r') as f:
            return json.load(f)
    
    def get_bks_info(self, family: str, instance: str) -> Optional[Dict]:
        """Get BKS information for a specific instance"""
        if family not in self.bks_data:
            return None
        
        family_data = self.bks_data[family]
        
        # Handle nested structure (SGB has subcategories)
        if 'instances' in family_data:
            instances = family_data['instances']
        elif 'subcategories' in family_data:
            # SGB case
            for subcat in family_data['subcategories'].values():
                if 'instances' in subcat and instance in subcat['instances']:
                    return subcat['instances'][instance]
            return None
        else:
            return None
        
        return instances.get(instance)
    
    def compute_gap(self, gaa_value: int, bks_value: int) -> float:
        """
        Compute optimality gap as percentage above BKS
        
        Gap = (GAA - BKS) / BKS * 100
        """
        if bks_value == 0:
            return 0.0
        return (gaa_value - bks_value) / bks_value * 100
    
    def determine_status(self, gaa_value: int, bks_value: Optional[int], 
                        gap: Optional[float], open_instance: bool) -> ComparisonStatus:
        """Determine status of solution"""
        if open_instance or bks_value is None:
            return ComparisonStatus.OPEN_INSTANCE
        
        if gap == 0:
            return ComparisonStatus.OPTIMAL_FOUND
        elif gap < 0:
            return ComparisonStatus.BEAT_BKS
        elif gap <= 1:
            return ComparisonStatus.NEAR_BKS
        elif gap <= 5:
            return ComparisonStatus.GAP_ACCEPTABLE
        else:
            return ComparisonStatus.GAP_LARGE
    
    def compare_instance(self, instance_name: str, family: str, 
                        gaa_value: int) -> ComparisonResult:
        """Compare a single instance"""
        bks_info = self.get_bks_info(family, instance_name)
        
        if bks_info is None:
            return ComparisonResult(
                instance_name=instance_name,
                family=family,
                gaa_value=gaa_value,
                bks_value=None,
                optimal=False,
                open=True,
                gap_percent=None,
                status=ComparisonStatus.OPEN_INSTANCE
            )
        
        bks_value = bks_info.get('bks')
        is_optimal = bks_info.get('optimal', False)
        is_open = bks_info.get('open', False)
        
        gap = None
        if bks_value is not None:
            gap = self.compute_gap(gaa_value, bks_value)
        
        status = self.determine_status(gaa_value, bks_value, gap, is_open)
        
        return ComparisonResult(
            instance_name=instance_name,
            family=family,
            gaa_value=gaa_value,
            bks_value=bks_value,
            optimal=is_optimal,
            open=is_open,
            gap_percent=gap,
            status=status
        )
    
    def compare_family(self, family: str, gaa_results: Dict[str, int]) -> List[ComparisonResult]:
        """Compare all instances in a family"""
        results = []
        
        for instance_name, gaa_value in gaa_results.items():
            result = self.compare_instance(instance_name, family, gaa_value)
            results.append(result)
        
        return results
    
    def analyze_results(self, results: List[ComparisonResult]) -> Dict:
        """Analyze comparison results"""
        if not results:
            return {}
        
        total = len(results)
        open_instances = sum(1 for r in results if r.open)
        closed_instances = total - open_instances
        
        # For closed instances
        optimal_found = sum(1 for r in results if not r.open and r.gap_percent == 0)
        beat_bks = sum(1 for r in results if not r.open and r.gap_percent is not None and r.gap_percent < 0)
        gaps = [r.gap_percent for r in results if r.gap_percent is not None and r.gap_percent >= 0]
        
        analysis = {
            'total_instances': total,
            'open_instances': open_instances,
            'closed_instances': closed_instances,
            'optimal_found': optimal_found,
            'optimal_percent': 100 * optimal_found / closed_instances if closed_instances > 0 else 0,
            'beat_bks': beat_bks,
            'beat_bks_percent': 100 * beat_bks / closed_instances if closed_instances > 0 else 0,
            'average_gap_percent': sum(gaps) / len(gaps) if gaps else None,
            'max_gap_percent': max(gaps) if gaps else None,
            'min_gap_percent': min(gaps) if gaps else None,
        }
        
        return analysis
    
    def print_family_comparison(self, family: str, results: List[ComparisonResult], 
                               verbose: bool = True) -> None:
        """Print comparison results for a family"""
        analysis = self.analyze_results(results)
        
        print(f"\n{'='*80}")
        print(f"COMPARISON: {family} Family vs Best Known Solutions")
        print(f"{'='*80}\n")
        
        if verbose:
            print(f"{'Instance':<20} │ {'BKS':<5} │ {'GAA':<5} │ {'Gap':<8} │ Status")
            print(f"{'-'*20}─┼─────┼─────┼────────┼─" + "─"*20)
            
            for result in sorted(results, key=lambda r: r.instance_name):
                bks_str = str(result.bks_value) if result.bks_value is not None else "?"
                gap_str = f"{result.gap_percent:+.1f}%" if result.gap_percent is not None else "-"
                
                print(f"{result.instance_name:<20} │ {bks_str:>5} │ {result.gaa_value:>5} │ "
                      f"{gap_str:>8} │ {result.status.value}")
        
        print(f"\n{'─'*80}")
        print(f"SUMMARY for {family}")
        print(f"{'─'*80}")
        print(f"  Total instances:        {analysis['total_instances']}")
        print(f"  Closed instances:       {analysis['closed_instances']} "
              f"({100*analysis['closed_instances']/analysis['total_instances']:.1f}%)")
        print(f"  Open instances:         {analysis['open_instances']} "
              f"({100*analysis['open_instances']/analysis['total_instances']:.1f}%)")
        
        if analysis['closed_instances'] > 0:
            print(f"\n  Optimality Results:")
            print(f"    Found optimal:      {analysis['optimal_found']}/{analysis['closed_instances']} "
                  f"({analysis['optimal_percent']:.1f}%)")
            print(f"    Beat BKS:           {analysis['beat_bks']}/{analysis['closed_instances']} "
                  f"({analysis['beat_bks_percent']:.1f}%)")
            
            if analysis['average_gap_percent'] is not None:
                print(f"\n  Gap Statistics:")
                print(f"    Average gap:        {analysis['average_gap_percent']:+.2f}%")
                print(f"    Max gap:            {analysis['max_gap_percent']:+.2f}%")
                print(f"    Min gap:            {analysis['min_gap_percent']:+.2f}%")
    
    def print_overall_summary(self, all_results: Dict[str, List[ComparisonResult]]) -> None:
        """Print overall summary across all families"""
        print(f"\n\n{'='*80}")
        print(f"OVERALL SUMMARY: GAA vs Literature (All Families)")
        print(f"{'='*80}\n")
        
        total_instances = 0
        total_optimal = 0
        total_beat = 0
        total_closed = 0
        all_gaps = []
        
        for family, results in sorted(all_results.items()):
            analysis = self.analyze_results(results)
            total_instances += analysis['total_instances']
            total_optimal += analysis['optimal_found']
            total_beat += analysis['beat_bks']
            total_closed += analysis['closed_instances']
            
            if analysis['average_gap_percent'] is not None:
                gaps = [r.gap_percent for r in results 
                       if r.gap_percent is not None and r.gap_percent >= 0]
                all_gaps.extend(gaps)
            
            print(f"  {family:<10} │ {analysis['total_instances']:>2} instances │ "
                  f"Optimal: {analysis['optimal_found']}/{analysis['closed_instances']} "
                  f"({analysis['optimal_percent']:>5.1f}%) │ "
                  f"Beat BKS: {analysis['beat_bks']}")
        
        print(f"\n{'─'*80}")
        print(f"  TOTALS:")
        print(f"    Total instances:      {total_instances}")
        print(f"    Closed instances:     {total_closed}")
        print(f"    Found optimal:        {total_optimal}/{total_closed} "
              f"({100*total_optimal/total_closed if total_closed > 0 else 0:.1f}%)")
        print(f"    Beat BKS:             {total_beat}/{total_closed} "
              f"({100*total_beat/total_closed if total_closed > 0 else 0:.1f}%)")
        
        if all_gaps:
            avg_gap = sum(all_gaps) / len(all_gaps)
            print(f"    Average gap:          {avg_gap:+.2f}%")
        
        print(f"\n  CONCLUSION:")
        if total_optimal / total_closed > 0.5:
            verdict = "✅ EXCELLENT - Found optimal on majority of instances"
        elif total_optimal / total_closed > 0.3:
            verdict = "⚠️  GOOD - Competitive with literature"
        else:
            verdict = "❌ NEEDS IMPROVEMENT"
        
        if total_beat > 0:
            verdict += f" + 🎉 Discovered {total_beat} new solutions"
        
        print(f"    {verdict}")


def load_gaa_results(results_dir: Path) -> Dict[str, Dict[str, int]]:
    """Load GAA results from directory structure"""
    gaa_results = {}
    
    if not results_dir.exists():
        raise FileNotFoundError(f"Results directory not found: {results_dir}")
    
    for family_dir in results_dir.iterdir():
        if not family_dir.is_dir():
            continue
        
        family = family_dir.name
        results_file = family_dir / 'results.json'
        
        if results_file.exists():
            with open(results_file, 'r') as f:
                gaa_results[family] = json.load(f)
    
    return gaa_results


def main():
    parser = argparse.ArgumentParser(
        description='Compare GAA results against Best Known Solutions (BKS)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare all families
  python compare_with_bks.py --results-dir results/
  
  # Compare specific family
  python compare_with_bks.py --results-dir results/ --family CUL
  
  # Output as JSON
  python compare_with_bks.py --results-dir results/ --output-format json
        """
    )
    
    parser.add_argument('--results-dir', default='results',
                       help='Directory containing GAA results (default: results)')
    parser.add_argument('--bks-file', default='datasets/BKS.json',
                       help='Path to BKS JSON file (default: datasets/BKS.json)')
    parser.add_argument('--family', help='Specific family to compare (optional)')
    parser.add_argument('--output-file', help='Save results to file')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output with detailed instance list')
    
    args = parser.parse_args()
    
    # Load comparator
    try:
        comparator = BKSComparator(bks_file=args.bks_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    # Load GAA results
    try:
        gaa_results = load_gaa_results(Path(args.results_dir))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    if not gaa_results:
        print(f"No results found in {args.results_dir}")
        return 1
    
    # Filter by family if specified
    if args.family:
        if args.family not in gaa_results:
            print(f"Family '{args.family}' not found in results")
            return 1
        gaa_results = {args.family: gaa_results[args.family]}
    
    # Perform comparisons
    all_results = {}
    for family, instances in gaa_results.items():
        all_results[family] = comparator.compare_family(family, instances)
    
    # Output results
    if args.output_format == 'json':
        output = {
            family: [r.to_dict() for r in results]
            for family, results in all_results.items()
        }
        
        if args.output_file:
            with open(args.output_file, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Results saved to {args.output_file}")
        else:
            print(json.dumps(output, indent=2))
    
    else:  # text format
        if len(all_results) == 1:
            family = list(all_results.keys())[0]
            comparator.print_family_comparison(family, all_results[family], 
                                              verbose=args.verbose)
        else:
            for family, results in sorted(all_results.items()):
                comparator.print_family_comparison(family, results, verbose=args.verbose)
            
            comparator.print_overall_summary(all_results)
        
        if args.output_file:
            # Redirect to file would require capturing output
            print(f"\nNote: Text output to file not implemented. Use --output-format json")
    
    return 0


if __name__ == '__main__':
    exit(main())
