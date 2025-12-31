#!/usr/bin/env python3
"""
robustness_analyzer.py - Análisis de robustez para múltiples ejecuciones
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from statistics import mean, stdev


class RobustnessAnalyzer:
    """Analiza robustez de múltiples ejecuciones del mismo experimento"""
    
    @staticmethod
    def analyze_multiple_runs(all_results: List[Dict]) -> Dict[str, Any]:
        """
        Analizar múltiples ejecuciones
        
        Args:
            all_results: Lista de resultados (cada uno es una ejecución)
        
        Returns:
            Análisis de robustez con estadísticas
        """
        
        if not all_results:
            return {}
        
        # Agrupar por instancia
        instances_data = {}
        
        for result in all_results:
            inst_name = result.get('instance')
            if inst_name not in instances_data:
                instances_data[inst_name] = {
                    'fitness_values': [],
                    'iteration_values': [],
                    'time_values': [],
                    'runs': []
                }
            
            instances_data[inst_name]['fitness_values'].append(result.get('best_fitness', 0))
            instances_data[inst_name]['iteration_values'].append(result.get('iterations', 0))
            instances_data[inst_name]['time_values'].append(result.get('elapsed_time', 0))
            instances_data[inst_name]['runs'].append(result)
        
        # Calcular estadísticas por instancia
        robustness_data = {
            "num_runs": len(all_results),
            "instances": {}
        }
        
        for inst_name, data in instances_data.items():
            fitness_vals = data['fitness_values']
            iter_vals = data['iteration_values']
            time_vals = data['time_values']
            
            robustness_data["instances"][inst_name] = {
                "fitness": {
                    "mean": mean(fitness_vals),
                    "min": min(fitness_vals),
                    "max": max(fitness_vals),
                    "stdev": stdev(fitness_vals) if len(fitness_vals) > 1 else 0,
                    "all_values": fitness_vals
                },
                "iterations": {
                    "mean": mean(iter_vals),
                    "min": min(iter_vals),
                    "max": max(iter_vals),
                    "all_values": iter_vals
                },
                "time": {
                    "mean": mean(time_vals),
                    "min": min(time_vals),
                    "max": max(time_vals),
                    "all_values": time_vals
                }
            }
        
        return robustness_data
    
    @staticmethod
    def generate_robustness_markdown(robustness_data: Dict) -> str:
        """Generar reporte de robustez en Markdown"""
        
        if not robustness_data.get("instances"):
            return ""
        
        lines = [
            "# 📊 Análisis de Robustez",
            "",
            f"**Número de ejecuciones:** {robustness_data.get('num_runs', 1)}",
            "",
            "## Estadísticas por Instancia",
            "",
        ]
        
        for inst_name, stats in robustness_data.get("instances", {}).items():
            lines.extend([
                f"### {inst_name}",
                "",
                "**Fitness:**",
                f"- Media: {stats['fitness']['mean']:.4f}",
                f"- Min: {stats['fitness']['min']:.4f}",
                f"- Max: {stats['fitness']['max']:.4f}",
                f"- Desv. Est.: {stats['fitness']['stdev']:.4f}",
                "",
                "**Iteraciones:**",
                f"- Media: {stats['iterations']['mean']:.0f}",
                f"- Min: {stats['iterations']['min']:.0f}",
                f"- Max: {stats['iterations']['max']:.0f}",
                "",
                "**Tiempo (segundos):**",
                f"- Media: {stats['time']['mean']:.6f}",
                f"- Min: {stats['time']['min']:.6f}",
                f"- Max: {stats['time']['max']:.6f}",
                "",
            ])
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_robustness_csv(robustness_data: Dict, output_path: Path):
        """Generar reporte de robustez en CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Instance", "Fitness_Mean", "Fitness_Min", "Fitness_Max", "Fitness_StDev",
                "Iterations_Mean", "Iterations_Min", "Iterations_Max",
                "Time_Mean", "Time_Min", "Time_Max"
            ])
            
            for inst_name, stats in robustness_data.get("instances", {}).items():
                writer.writerow([
                    inst_name,
                    f"{stats['fitness']['mean']:.4f}",
                    f"{stats['fitness']['min']:.4f}",
                    f"{stats['fitness']['max']:.4f}",
                    f"{stats['fitness']['stdev']:.4f}",
                    f"{stats['iterations']['mean']:.0f}",
                    f"{stats['iterations']['min']:.0f}",
                    f"{stats['iterations']['max']:.0f}",
                    f"{stats['time']['mean']:.6f}",
                    f"{stats['time']['min']:.6f}",
                    f"{stats['time']['max']:.6f}",
                ])
