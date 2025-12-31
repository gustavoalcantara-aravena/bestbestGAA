#!/usr/bin/env python3
"""
Regenerar análisis y reportes en todas las carpetas output que no los tienen
"""
import json
import csv
from pathlib import Path
from datetime import datetime

def regenerate_missing_reports():
    """Regenerar RESULTS.md, analysis_report.json y analysis_report.csv para carpetas que no los tienen"""
    
    output_base = Path("output")
    processed = 0
    
    for folder in sorted(output_base.iterdir()):
        if not folder.is_dir():
            continue
        
        # Archivos esperados
        results_json = folder / "results.json"
        results_md = folder / "RESULTS.md"
        analysis_json = folder / "analysis_report.json"
        analysis_csv = folder / "analysis_report.csv"
        
        # Verificar si faltan archivos
        missing = []
        if not results_md.exists():
            missing.append("RESULTS.md")
        if not analysis_json.exists():
            missing.append("analysis_report.json")
        if not analysis_csv.exists():
            missing.append("analysis_report.csv")
        
        if not missing or not results_json.exists():
            continue
        
        print(f"\n📁 {folder.name}")
        print(f"   Regenerando: {', '.join(missing)}")
        
        # Cargar results.json
        try:
            with open(results_json, 'r') as f:
                results_data = json.load(f)
        except Exception as e:
            print(f"   ❌ Error leyendo results.json: {e}")
            continue
        
        family = results_data.get('family', 'UNKNOWN')
        results = results_data.get('results', [])
        timestamp = results_data.get('timestamp', datetime.now().isoformat())
        
        # Regenerar RESULTS.md
        if "RESULTS.md" in missing:
            try:
                completed = len([r for r in results if r.get('status') in ['completed', 'simulated']])
                failed = len([r for r in results if r.get('status') in ['error', 'load_error']])
                
                total_time = sum(r.get('elapsed_time', 0) for r in results)
                avg_time = total_time / len(results) if results else 0
                
                fitnesses = [r.get('best_fitness', 0) for r in results if 'best_fitness' in r]
                avg_fitness = sum(fitnesses) / len(fitnesses) if fitnesses else 0
                
                md_lines = [
                    f"# Resultados - {family}",
                    f"",
                    f"**Fecha:** {timestamp}",
                    f"",
                    f"## Resumen Ejecutivo",
                    f"",
                    f"| Métrica | Valor |",
                    f"|---------|-------|",
                    f"| Instancias Ejecutadas | {len(results)} |",
                    f"| Completadas | {completed} ✅ |",
                    f"| Fallidas | {failed} ❌ |",
                    f"| Tasa Éxito | {100*completed//len(results) if results else 0}% |",
                    f"| Tiempo Total | {total_time:.4f}s |",
                    f"| Tiempo Promedio | {avg_time:.6f}s |",
                    f"| Fitness Promedio | {avg_fitness:.4f} |",
                    f"",
                    f"## Detalle de Instancias",
                    f"",
                    f"| # | Instancia | Vertices | Edges | Fitness | Iteraciones | Tiempo (s) | Estado |",
                    f"|---|-----------|----------|-------|---------|-------------|-----------|--------|",
                ]
                
                for i, result in enumerate(results, 1):
                    inst_name = result.get('instance', 'N/A')
                    vertices = result.get('vertices', '?')
                    edges = result.get('edges', '?')
                    fitness = result.get('best_fitness', '?')
                    iterations = result.get('iterations', '?')
                    elapsed = result.get('elapsed_time', 0)
                    status_icon = "✅" if result.get('status') == 'completed' else "⏱️"
                    
                    fitness_str = f"{fitness:.4f}" if isinstance(fitness, (int, float)) else str(fitness)
                    
                    md_lines.append(
                        f"| {i} | {inst_name} | {vertices} | {edges} | {fitness_str} | {iterations} | {elapsed:.6f} | {status_icon} |"
                    )
                
                md_lines.extend([
                    f"",
                    f"## Información Técnica",
                    f"",
                    f"- **Familia:** {family}",
                    f"- **Timestamp:** {timestamp}",
                    f"",
                    f"---",
                    f"",
                    f"*Generado automáticamente por regenerate_reports.py*",
                ])
                
                with open(results_md, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(md_lines))
                
                print(f"      ✅ RESULTS.md ({len(md_lines)} líneas)")
            except Exception as e:
                print(f"      ❌ Error generando RESULTS.md: {e}")
        
        # Regenerar analysis_report.json
        if "analysis_report.json" in missing:
            try:
                analysis_report = {
                    "timestamp": timestamp,
                    "family": family,
                    "summary": {
                        "total_instances": len(results),
                        "completed": len([r for r in results if r.get('status') in ['completed', 'simulated']]),
                        "failed": len([r for r in results if r.get('status') in ['error', 'load_error']]),
                        "avg_fitness": sum(r.get('best_fitness', 0) for r in results) / len(results) if results else 0,
                        "avg_time": sum(r.get('elapsed_time', 0) for r in results) / len(results) if results else 0,
                        "total_time": sum(r.get('elapsed_time', 0) for r in results)
                    },
                    "instances": []
                }
                
                for result in results:
                    analysis_report["instances"].append({
                        "name": result.get('instance'),
                        "vertices": result.get('vertices'),
                        "edges": result.get('edges'),
                        "fitness": result.get('best_fitness'),
                        "iterations": result.get('iterations'),
                        "time_seconds": result.get('elapsed_time'),
                        "status": result.get('status')
                    })
                
                with open(analysis_json, 'w', encoding='utf-8') as f:
                    json.dump(analysis_report, f, indent=2)
                
                print(f"      ✅ analysis_report.json ({len(results)} instancias)")
            except Exception as e:
                print(f"      ❌ Error generando analysis_report.json: {e}")
        
        # Regenerar analysis_report.csv
        if "analysis_report.csv" in missing:
            try:
                with open(analysis_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "Family", "Instance", "Vertices", "Edges", "Fitness", 
                        "Iterations", "Time_s", "Status"
                    ])
                    
                    for result in results:
                        writer.writerow([
                            family,
                            result.get('instance'),
                            result.get('vertices'),
                            result.get('edges'),
                            f"{result.get('best_fitness', 0):.4f}",
                            result.get('iterations'),
                            f"{result.get('elapsed_time', 0):.6f}",
                            result.get('status')
                        ])
                
                print(f"      ✅ analysis_report.csv ({len(results)} filas)")
            except Exception as e:
                print(f"      ❌ Error generando analysis_report.csv: {e}")
        
        processed += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Regeneración completada: {processed} carpetas procesadas")
    print(f"{'='*80}")

if __name__ == '__main__':
    regenerate_missing_reports()
