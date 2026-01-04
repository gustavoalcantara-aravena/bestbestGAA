#!/usr/bin/env python
"""
Master script: Generate ALL visualizations
Runs all visualization generators in sequence
"""

import sys
import os
import subprocess
from pathlib import Path

project_dir = Path(__file__).parent
os.chdir(project_dir)

print("=" * 80)
print("MASTER VISUALIZATION GENERATOR")
print("=" * 80)
print()

scripts = [
    ("analyze_results.py", "Statistical Analysis"),
    ("generate_visualizations.py", "Basic Visualizations"),
    ("generate_gap_visualizations.py", "Gap Analysis (%GAP)"),
    ("generate_algorithm_comparison.py", "Algorithm Comparison"),
    ("generate_reports.py", "HTML Reports"),
]

for script_name, description in scripts:
    script_path = project_dir / script_name
    
    if not script_path.exists():
        print(f"⚠️  {description}: {script_name} not found")
        continue
    
    print(f"[*] Running: {description}")
    print(f"    Script: {script_name}")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"⚠️  Error output:")
            print(result.stderr)
        
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timeout: Script took too long")
    except Exception as e:
        print(f"⚠️  Error: {e}")
    
    print()

print("=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print()
print("Generated files:")
print("  - output/canary_run/visualizations/")
print("    ├── canary_visualizations.png")
print("    ├── gap_distribution.png")
print("    ├── gap_by_algorithm.png")
print("    ├── gap_scatter.png")
print("    ├── gap_cumulative.png")
print("    ├── algorithm_comparison_heatmap.png")
print("    ├── algorithm_comparison_vehicles.png")
print("    ├── algorithm_comparison_distance.png")
print("    ├── algorithm_pareto_frontier.png")
print("    └── algorithm_radar_profiles.png")
print()
print("  - output/canary_run/")
print("    ├── report.html")
print("    └── canary_results.json")
print()
print("View results:")
print("  1. Open output/canary_run/report.html in browser")
print("  2. View PNG files in output/canary_run/visualizations/")
print()
