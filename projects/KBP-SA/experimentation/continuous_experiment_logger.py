"""
Continuous Experiment Logger - 3 Day Protocol
Sistema completo para logging exhaustivo según protocolo experimental
"""

import json
import csv
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid


class ContinuousExperimentLogger:
    """
    Logger para experimentación continua de 3 días
    Captura TODAS las métricas del protocolo experimental
    """

    def __init__(self, output_dir: str, experiment_name: str = "3day_protocol"):
        """
        Inicializa el logger

        Args:
            output_dir: Directorio de salida
            experiment_name: Nombre del experimento
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.experiment_name = experiment_name
        self.experiment_id = f"{experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Archivos de salida
        self.json_file = self.output_dir / f"{self.experiment_id}.json"
        self.csv_file = self.output_dir / f"{self.experiment_id}.csv"
        self.features_file = self.output_dir / f"{self.experiment_id}_features.json"

        # Datos acumulados
        self.runs_data = []
        self.features_data = []

        # Inicializar CSV
        self._init_csv()

    def _init_csv(self):
        """Inicializa el archivo CSV con headers"""
        headers = [
            'run_id',
            'timestamp',
            'algorithm_id',
            'execution_status',
            'time_generation',
            'time_initialization',
            'time_search',
            'time_evaluation',
            'time_postprocessing',
            'time_total',
            'objective_value',
            'optimal_value',
            'absolute_error',
            'relative_error',
            'gap_percent',
            'hit',
            # Features del algoritmo
            'constructor_type',
            'num_operators',
            'operator_types',
            'has_loop',
            'loop_budget',
            'acceptance_criterion',
            'num_evaluations',
            'tree_depth',
            'complexity_score'
        ]

        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

    def log_run(
        self,
        algorithm_pseudocode: str,
        algorithm_features: Dict,
        execution_status: str,
        time_breakdown: Dict[str, float],
        objective_value: Optional[float] = None,
        optimal_value: Optional[float] = None
    ) -> str:
        """
        Registra una corrida completa

        Args:
            algorithm_pseudocode: Pseudocódigo del algoritmo
            algorithm_features: Características extraídas del algoritmo
            execution_status: 'success', 'timeout', o 'error'
            time_breakdown: Dict con tiempos de cada etapa
            objective_value: Valor objetivo obtenido
            optimal_value: Valor óptimo conocido

        Returns:
            run_id generado
        """
        run_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        algorithm_id = f"algo_{hash(algorithm_pseudocode) % 1000000}"

        # Calcular métricas de calidad
        absolute_error = None
        relative_error = None
        gap_percent = None
        hit = False

        if objective_value is not None and optimal_value is not None and optimal_value > 0:
            absolute_error = abs(optimal_value - objective_value)
            relative_error = absolute_error / optimal_value
            gap_percent = (absolute_error / optimal_value) * 100
            hit = gap_percent <= 5.0  # HIT si gap ≤ 5%

        # Registro completo
        run_record = {
            'run_id': run_id,
            'timestamp': timestamp,
            'algorithm_id': algorithm_id,
            'algorithm_pseudocode': algorithm_pseudocode,
            'execution_status': execution_status,
            'time_generation': time_breakdown.get('generation', 0.0),
            'time_initialization': time_breakdown.get('initialization', 0.0),
            'time_search': time_breakdown.get('search', 0.0),
            'time_evaluation': time_breakdown.get('evaluation', 0.0),
            'time_postprocessing': time_breakdown.get('postprocessing', 0.0),
            'time_total': time_breakdown.get('total', 0.0),
            'objective_value': objective_value,
            'optimal_value': optimal_value,
            'absolute_error': absolute_error,
            'relative_error': relative_error,
            'gap_percent': gap_percent,
            'hit': hit,
            'features': algorithm_features
        }

        # Guardar en memoria
        self.runs_data.append(run_record)

        # Escribir a CSV (append)
        csv_record = {
            'run_id': run_id,
            'timestamp': timestamp,
            'algorithm_id': algorithm_id,
            'execution_status': execution_status,
            'time_generation': time_breakdown.get('generation', 0.0),
            'time_initialization': time_breakdown.get('initialization', 0.0),
            'time_search': time_breakdown.get('search', 0.0),
            'time_evaluation': time_breakdown.get('evaluation', 0.0),
            'time_postprocessing': time_breakdown.get('postprocessing', 0.0),
            'time_total': time_breakdown.get('total', 0.0),
            'objective_value': objective_value or '',
            'optimal_value': optimal_value or '',
            'absolute_error': absolute_error or '',
            'relative_error': relative_error or '',
            'gap_percent': gap_percent or '',
            'hit': hit,
            # Features
            'constructor_type': algorithm_features.get('constructor', ''),
            'num_operators': algorithm_features.get('num_operators', 0),
            'operator_types': ','.join(algorithm_features.get('operators', [])),
            'has_loop': algorithm_features.get('has_loop', False),
            'loop_budget': algorithm_features.get('loop_budget', ''),
            'acceptance_criterion': algorithm_features.get('acceptance_criteria', ''),
            'num_evaluations': algorithm_features.get('num_evaluations', ''),
            'tree_depth': algorithm_features.get('tree_depth', ''),
            'complexity_score': algorithm_features.get('complexity_score', '')
        }

        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_record.keys())
            writer.writerow(csv_record)

        # Escribir JSON (sobrescribir todo)
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'experiment_id': self.experiment_id,
                'experiment_name': self.experiment_name,
                'runs': self.runs_data
            }, f, indent=2)

        return run_id

    def get_statistics(self) -> Dict:
        """Retorna estadísticas acumuladas"""
        if not self.runs_data:
            return {'total_runs': 0}

        successful = [r for r in self.runs_data if r['execution_status'] == 'success']
        timeouts = [r for r in self.runs_data if r['execution_status'] == 'timeout']
        errors = [r for r in self.runs_data if r['execution_status'] == 'error']

        hits = [r for r in successful if r['hit']]

        stats = {
            'total_runs': len(self.runs_data),
            'successful_runs': len(successful),
            'timeout_runs': len(timeouts),
            'error_runs': len(errors),
            'hit_runs': len(hits),
            'hit_rate': len(hits) / len(successful) * 100 if successful else 0,
        }

        if successful:
            times = [r['time_total'] for r in successful]
            import numpy as np
            stats.update({
                'avg_time': np.mean(times),
                'min_time': np.min(times),
                'max_time': np.max(times),
                'median_time': np.median(times),
                'std_time': np.std(times)
            })

            gaps = [r['gap_percent'] for r in successful if r['gap_percent'] is not None]
            if gaps:
                stats.update({
                    'avg_gap': np.mean(gaps),
                    'min_gap': np.min(gaps),
                    'max_gap': np.max(gaps)
                })

        return stats

    def print_progress(self):
        """Imprime progreso actual"""
        stats = self.get_statistics()

        print(f"\n{'=' * 80}")
        print(f"PROGRESO EXPERIMENTAL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}")
        print(f"Total corridas: {stats['total_runs']}")
        print(f"  ✅ Exitosas: {stats['successful_runs']} ({stats['successful_runs']/stats['total_runs']*100:.1f}%)")
        print(f"  ⚠️  Timeouts: {stats['timeout_runs']} ({stats['timeout_runs']/stats['total_runs']*100:.1f}%)")
        if stats['error_runs'] > 0:
            print(f"  ❌ Errores: {stats['error_runs']}")

        if stats['successful_runs'] > 0:
            print(f"\nTiempos de ejecución:")
            print(f"  • Promedio: {stats['avg_time']:.1f}s")
            print(f"  • Mínimo: {stats['min_time']:.1f}s ⚡")
            print(f"  • Máximo: {stats['max_time']:.1f}s")
            print(f"  • Mediana: {stats['median_time']:.1f}s")

            print(f"\nCalidad de soluciones:")
            print(f"  • HITs: {stats['hit_runs']} ({stats['hit_rate']:.1f}%)")
            if 'avg_gap' in stats:
                print(f"  • GAP promedio: {stats['avg_gap']:.2f}%")

        print(f"{'=' * 80}\n")
