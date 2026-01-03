#!/usr/bin/env python3
"""
Test script for BKS Manager

Demonstrates usage of best_known_solutions module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.bks import BKSManager


def main():
    """Run BKS manager tests."""
    print("\n" + "="*70)
    print("BEST KNOWN SOLUTIONS (BKS) MANAGER - TEST SUITE")
    print("="*70 + "\n")
    
    # Initialize manager
    print("1. Loading BKS data...")
    bks = BKSManager()
    print("   ✓ BKS loaded successfully\n")
    
    # Test individual instance lookup
    print("2. Testing individual instance lookup:")
    instance_id = "C101"
    bks_data = bks.get_instance(instance_id)
    print(f"   Instance {instance_id}: K={bks_data['k_bks']}, D={bks_data['d_bks']:.5f}\n")
    
    # Test family lookup
    print("3. Testing family lookup:")
    for family in ['C1', 'R1', 'RC2']:
        family_data = bks.get_family(family)
        print(f"   {family}: {family_data['name']} ({family_data['num_instances']} instances)")
    print()
    
    # Test gap calculation
    print("4. Testing gap calculations:")
    test_cases = [
        ("C101", 10, 828.93664),  # Perfect match
        ("C101", 11, 900.0),      # Worse K
        ("R101", 19, 1700.0),     # Same K, worse D
    ]
    
    for inst_id, algo_k, algo_d in test_cases:
        validation = bks.validate_solution(inst_id, algo_k, algo_d)
        print(f"   {inst_id}: algo=(K={algo_k}, D={algo_d:.2f})")
        print(f"      → {validation['comparison']['reason']}")
    print()
    
    # Test statistics
    print("5. Testing statistics:")
    print("   Overall summary:")
    summary = bks.get_summary()
    print(f"      Total instances: {summary['total_instances']}")
    print(f"      Avg vehicles: {summary['avg_vehicles']:.2f}")
    print(f"      Avg distance: {summary['avg_distance']:.2f}\n")
    
    print("   Family summary (C1):")
    summary_c1 = bks.get_summary('C1')
    print(f"      Avg vehicles: {summary_c1['avg_k']}")
    print(f"      Avg distance: {summary_c1['avg_distance']:.2f}\n")
    
    # Test all families and instances
    print("6. All Solomon families and instances:")
    all_families = bks.get_all_families()
    print(f"   Families: {', '.join(all_families)}")
    print(f"   Total instances: {len(bks.get_all_instances())}\n")
    
    # Summary by family
    print("7. Summary by family:")
    print("   Family  | Instances | Avg K  | Avg Distance")
    print("   " + "-"*48)
    for fam_id in all_families:
        family = bks.get_family(fam_id)
        summary = bks.get_summary(fam_id)
        print(
            f"   {fam_id:6s} | {family['num_instances']:9d} | "
            f"{summary['avg_k']:6.2f} | {summary['avg_distance']:11.2f}"
        )
    print()
    
    print("="*70)
    print("✓ All tests completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
