#!/usr/bin/env python
"""
Wrapper to generate all visualizations for a run directory.
"""

import sys
import os
import subprocess
from pathlib import Path

project_dir = Path(__file__).parent
os.chdir(project_dir)

def generate_visualizations_for_run(run_dir):
    """Generate all visualizations for a specific run directory."""
    
    run_dir = Path(run_dir)
    if not run_dir.exists():
        print(f"Error: Run directory not found: {run_dir}")
        return False
    
    # Determine run type and files
    if "Canary" in str(run_dir):
        results_file = run_dir / "canary_results.json"
    else:
        results_file = run_dir / "experiment_results.json"
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        return False
    
    # Create visualizations directory
    vis_dir = run_dir / "visualizations"
    vis_dir.mkdir(parents=True, exist_ok=True)
    report_file = run_dir / "report.html"
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    print()
    
    scripts = [
        ("analyze_results.py", ["--results-file", str(results_file)]),
        ("generate_visualizations.py", ["--results-file", str(results_file), "--output-dir", str(vis_dir), "--type", "canary"]),
        ("generate_gap_visualizations.py", ["--results-file", str(results_file), "--output-dir", str(vis_dir)]),
        ("generate_algorithm_comparison.py", ["--results-file", str(results_file), "--output-dir", str(vis_dir)]),
        ("generate_reports.py", ["--results-file", str(results_file), "--output-file", str(report_file), "--title", "Canary Run Results"]),
        ("generate_extra_visualizations.py", [str(run_dir)]),
        ("generate_extra_visualizations_set2.py", [str(run_dir)]),
    ]
    
    for script_name, args in scripts:
        script_path = project_dir / script_name
        
        if not script_path.exists():
            print(f"[!] {script_name} not found, skipping")
            continue
        
        print(f"[*] {script_name}")
        
        try:
            cmd = [sys.executable, str(script_path)] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"    [OK]")
            else:
                print(f"    [ERROR]")
                if result.stderr:
                    # Print first 200 chars of error
                    print(f"    {result.stderr[:200]}")
            
        except subprocess.TimeoutExpired:
            print(f"    [TIMEOUT]")
        except Exception as e:
            print(f"    [ERROR] {str(e)[:100]}")
        
        print()
    
    print("=" * 80)
    print("VISUALIZATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_visualizations_for_run.py <run_directory>")
        sys.exit(1)
    
    run_dir = sys.argv[1]
    success = generate_visualizations_for_run(run_dir)
    sys.exit(0 if success else 1)
