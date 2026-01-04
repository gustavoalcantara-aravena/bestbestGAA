#!/usr/bin/env python
"""
Generate HTML report from VRPTW results.
"""

import sys
import os
import json
import argparse
from pathlib import Path

os.chdir(Path(__file__).parent)

def load_results(results_file):
    """Load results from JSON"""
    with open(results_file) as f:
        return json.load(f)

def generate_html_report(results, output_file, title):
    """Generate HTML report"""
    
    feasible = [r for r in results if r.get("feasible", False)]
    
    # Calculate statistics
    total_runs = len(results)
    feasible_count = len(feasible)
    feasible_pct = (feasible_count / total_runs * 100) if total_runs > 0 else 0
    
    vehicles = [r.get("vehicles", 0) for r in feasible] if feasible else []
    distances = [r.get("distance", 0) for r in feasible] if feasible else []
    
    stats = {
        "vehicles_min": min(vehicles) if vehicles else 0,
        "vehicles_max": max(vehicles) if vehicles else 0,
        "vehicles_avg": sum(vehicles) / len(vehicles) if vehicles else 0,
        "distance_min": min(distances) if distances else 0,
        "distance_max": max(distances) if distances else 0,
        "distance_avg": sum(distances) / len(distances) if distances else 0,
    }
    
    # Find best solution
    best_solution = None
    if feasible:
        best_solution = min(feasible, key=lambda r: (r.get("vehicles", float('inf')), r.get("distance", float('inf'))))
    
    # Get top 10 solutions
    top_solutions = sorted(feasible, key=lambda r: (r.get("vehicles", float('inf')), r.get("distance", float('inf'))))[:10] if feasible else []
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            .summary {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 20px 0;
            }}
            .card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            .card.green {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            }}
            .card.blue {{
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            }}
            .card h3 {{
                margin: 0;
                font-size: 14px;
            }}
            .card .value {{
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .best-solution {{
                background-color: #d5f4e6;
                border-left: 4px solid #27ae60;
            }}
            footer {{
                text-align: center;
                color: #95a5a6;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            
            <div class="summary">
                <div class="card">
                    <h3>Total Runs</h3>
                    <div class="value">{total_runs}</div>
                </div>
                <div class="card green">
                    <h3>Feasible Runs</h3>
                    <div class="value">{feasible_count} ({feasible_pct:.1f}%)</div>
                </div>
                <div class="card blue">
                    <h3>Infeasible</h3>
                    <div class="value">{total_runs - feasible_count}</div>
                </div>
            </div>
            
            <h2>Vehicle Statistics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Minimum</td>
                    <td>{stats["vehicles_min"]}</td>
                </tr>
                <tr>
                    <td>Maximum</td>
                    <td>{stats["vehicles_max"]}</td>
                </tr>
                <tr>
                    <td>Average</td>
                    <td>{stats["vehicles_avg"]:.2f}</td>
                </tr>
            </table>
            
            <h2>Distance Statistics (km)</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Minimum</td>
                    <td>{stats["distance_min"]:.2f}</td>
                </tr>
                <tr>
                    <td>Maximum</td>
                    <td>{stats["distance_max"]:.2f}</td>
                </tr>
                <tr>
                    <td>Average</td>
                    <td>{stats["distance_avg"]:.2f}</td>
                </tr>
            </table>
    """
    
    if best_solution:
        html += f"""
            <h2>Best Solution</h2>
            <table>
                <tr class="best-solution">
                    <td><strong>Algorithm ID</strong></td>
                    <td>{best_solution.get("algorithm_id", "N/A")}</td>
                </tr>
                <tr class="best-solution">
                    <td><strong>Vehicles</strong></td>
                    <td>{best_solution.get("vehicles", "N/A")}</td>
                </tr>
                <tr class="best-solution">
                    <td><strong>Distance</strong></td>
                    <td>{best_solution.get("distance", "N/A"):.2f} km</td>
                </tr>
            </table>
        """
    
    if top_solutions:
        html += """
            <h2>Top 10 Solutions</h2>
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Algorithm</th>
                    <th>Vehicles</th>
                    <th>Distance (km)</th>
                </tr>
        """
        for idx, sol in enumerate(top_solutions, 1):
            html += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{sol.get("algorithm_id", "N/A")}</td>
                    <td>{sol.get("vehicles", "N/A")}</td>
                    <td>{sol.get("distance", "N/A"):.2f}</td>
                </tr>
            """
        html += "</table>"
    
    html += """
            <footer>
                <p>Generated by GRASP-GAA-VRPTW | 2026</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-file", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    
    print("=" * 80)
    print("GENERATING HTML REPORT")
    print("=" * 80)
    
    results_file = Path(args.results_file)
    if not results_file.exists():
        print(f"ERROR: {results_file} not found")
        sys.exit(1)
    
    results = load_results(results_file)
    print(f"Processing {len(results)} results...")
    output = generate_html_report(results, args.output_file, args.title)
    print(f"  [OK] Saved: {output.name}")
    print("[DONE]\n")
