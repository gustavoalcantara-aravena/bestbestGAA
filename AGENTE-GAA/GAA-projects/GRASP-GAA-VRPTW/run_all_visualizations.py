#!/usr/bin/env python
"""
Master script: Generate ALL visualizations (UTF-8 compatible)
Runs all visualization generators in sequence
"""

import sys
import os
import subprocess
from pathlib import Path

project_dir = Path(__file__).parent
os.chdir(project_dir)

# Set UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("MASTER VISUALIZATION GENERATOR - ALL MODULES")
print("=" * 80)
print()

scripts = [
    ("analyze_results.py", "Step 1: Statistical Analysis"),
    ("generate_gap_visualizations.py", "Step 2: Gap Analysis (Percent Gap)"),
    ("generate_algorithm_comparison.py", "Step 3: Algorithm Comparison"),
    ("generate_visualizations.py", "Step 4: Basic Visualizations"),
    ("generate_reports.py", "Step 5: HTML Reports"),
]

completed = []
failed = []

for script_name, description in scripts:
    script_path = project_dir / script_name
    
    if not script_path.exists():
        print(f"[SKIP] {description}: {script_name} not found")
        failed.append(description)
        continue
    
    print(f"[RUN] {description}")
    print(f"      {script_name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=600,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        
        # Print output without special characters
        output = result.stdout.replace('\u2713', '[OK]').replace('\u2717', '[FAIL]')
        print(output)
        
        if result.returncode != 0:
            print(f"[WARN] Error in execution")
            stderr = result.stderr.replace('\u2713', '[OK]').replace('\u2717', '[FAIL]')
            if stderr:
                print(stderr[:500])  # First 500 chars
            failed.append(description)
        else:
            completed.append(description)
        
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Script took too long (>10 min)")
        failed.append(description)
    except Exception as e:
        print(f"[ERROR] {str(e)[:100]}")
        failed.append(description)
    
    print()

print("=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print()
print(f"Completed: {len(completed)}/{len(scripts)}")
if completed:
    for item in completed:
        print(f"  [OK] {item}")
if failed:
    print(f"\nFailed: {len(failed)}/{len(scripts)}")
    for item in failed:
        print(f"  [FAIL] {item}")

print()
print("Output directories:")
print("  output/canary_run/visualizations/")
print("  output/canary_run/report.html")
print()
print("Key visualizations generated:")
print("  1. gap_distribution.png - Shows %GAP distribution")
print("  2. gap_by_algorithm.png - %GAP comparison between algorithms")
print("  3. algorithm_comparison_vehicles.png - Vehicle performance")
print("  4. algorithm_comparison_distance.png - Distance performance")
print("  5. algorithm_pareto_frontier.png - Efficiency frontier")
print()
