#!/usr/bin/env python3
"""
Test visualization scripts individually to identify errors
"""
import subprocess
import sys
from pathlib import Path

# Most recent run directory
run_dir = Path("output/Canary_RUN_2026-01-04_02-06-24")
results_file = run_dir / "canary_results.json"
vis_dir = run_dir / "visualizations"
report_file = run_dir / "report.html"

print(f"[TEST] Using run directory: {run_dir}")
print(f"[TEST] Results file: {results_file}")
print(f"[TEST] Visualizations dir: {vis_dir}\n")

# List of visualization scripts to test
scripts = [
    ("analyze_results.py", [
        "python", "analyze_results.py",
        "--results-file", str(results_file)
    ]),
    ("generate_visualizations.py", [
        "python", "generate_visualizations.py",
        "--results-file", str(results_file),
        "--output-dir", str(vis_dir),
        "--type", "canary"
    ]),
    ("generate_gap_visualizations.py", [
        "python", "generate_gap_visualizations.py",
        "--results-file", str(results_file),
        "--output-dir", str(vis_dir)
    ]),
    ("generate_algorithm_comparison.py", [
        "python", "generate_algorithm_comparison.py",
        "--results-file", str(results_file),
        "--output-dir", str(vis_dir)
    ]),
    ("generate_reports.py", [
        "python", "generate_reports.py",
        "--results-file", str(results_file),
        "--output-file", str(report_file),
        "--title", "GRASP-GAA-VRPTW Results"
    ]),
]

# Test each script
for script_name, cmd in scripts:
    print(f"\n{'='*60}")
    print(f"[TEST] Running: {script_name}")
    print(f"[TEST] Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"[TEST] Exit Code: {result.returncode}")
        
        if result.stdout:
            print(f"[STDOUT]\n{result.stdout}")
        
        if result.stderr:
            print(f"[STDERR]\n{result.stderr}")
        
        if result.returncode != 0:
            print(f"[ERROR] {script_name} failed with code {result.returncode}")
        else:
            print(f"[OK] {script_name} completed successfully")
            
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {script_name} timed out after 30 seconds")
    except Exception as e:
        print(f"[ERROR] {script_name} raised exception: {e}")

print(f"\n{'='*60}")
print("[TEST] Checking generated files...")
print(f"{'='*60}\n")

if vis_dir.exists():
    files = list(vis_dir.glob("*"))
    print(f"Files in {vis_dir}:")
    for f in files:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")
else:
    print(f"ERROR: Visualization directory not found: {vis_dir}")

if report_file.exists():
    print(f"\nreport.html exists ({report_file.stat().st_size} bytes)")
else:
    print(f"\nreport.html NOT FOUND")
