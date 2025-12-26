#!/usr/bin/env python3
"""
3-Day Continuous Experimental Protocol
Ejecuta corridas continuas con timeout de 60s y logging exhaustivo
"""

import sys
import subprocess
import time
import re
import signal
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.continuous_experiment_logger import ContinuousExperimentLogger
from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


class ThreeDayProtocolRunner:
    """Runner para protocolo experimental de 3 días"""

    def __init__(self, timeout_seconds: int = 60, duration_days: float = 3.0):
        """
        Args:
            timeout_seconds: Timeout por corrida (60s por protocolo)
            duration_days: Duración total del experimento en días
        """
        self.timeout = timeout_seconds
        self.duration = timedelta(days=duration_days)

        # Crear logger
        output_dir = project_root / 'output' / '3day_protocol'
        self.logger = ContinuousExperimentLogger(str(output_dir))

        # Analyzer para extraer features
        self.analyzer = AlgorithmPatternAnalyzer()

        # Control de tiempo
        self.start_time = None
        self.end_time = None
        self.run_number = 0

        # Frecuencia de reportes
        self.report_every = 10  # Cada 10 corridas

    def parse_output(self, output: str) -> dict:
        """Parsea la salida de una ejecución"""
        # Extraer algoritmos
        algorithms = {}
        pattern = r'✅ Algoritmo (\d+) generado\s+Pseudocódigo:\s+((?:.*\n?)+?)(?=✅|\n\n|  ✅)'
        matches = re.finditer(pattern, output, re.MULTILINE)

        for match in matches:
            algo_num = match.group(1)
            pseudocode = match.group(2).strip()
            algorithms[f'Algorithm_{algo_num}'] = pseudocode

        # Extraer tiempos individuales
        time_pattern = r'× GAA_Algorithm_(\d+) \(rep \d+\).*?tiempo=([\d.]+)s'
        time_matches = re.findall(time_pattern, output)

        times_by_algorithm = {f'Algorithm_{i}': [] for i in range(1, 10)}
        for algo_num, time_str in time_matches:
            times_by_algorithm[f'Algorithm_{algo_num}'].append(float(time_str))

        return {
            'algorithms': algorithms,
            'times': times_by_algorithm
        }

    def extract_algorithm_features(self, pseudocode: str) -> dict:
        """Extrae features del algoritmo según protocolo"""
        features = self.analyzer.extract_features(pseudocode)

        return {
            'constructor': features.constructor,
            'operators': features.operators,
            'num_operators': len(features.operators),
            'acceptance_criteria': features.acceptance_criteria,
            'has_loop': features.has_loop,
            'loop_budget': features.loop_budget,
            'stagnation_limit': features.stagnation_limit,
            'complexity_score': features.complexity_score,
            # Estimaciones (en ausencia de instrumentación interna)
            'tree_depth': 3 if features.has_loop else 2,  # Estimado
            'num_evaluations': None,  # Requiere instrumentación
        }

    def run_single_experiment(self) -> bool:
        """
        Ejecuta un experimento individual

        Returns:
            True si debe continuar, False si debe detenerse
        """
        self.run_number += 1

        # Verificar si se acabó el tiempo
        if datetime.now() >= self.end_time:
            print(f"\n⏰ Tiempo de experimentación completado ({self.duration.days} días)")
            return False

        # Calcular tiempo restante
        remaining = self.end_time - datetime.now()
        hours_remaining = remaining.total_seconds() / 3600

        print(f"\n[{self.run_number}] ⏱️  Iniciando - {datetime.now().strftime('%H:%M:%S')} (quedan {hours_remaining:.1f}h)", end=" ", flush=True)

        start_time = time.time()

        try:
            # Ejecutar demo_experimentation_both.py
            result = subprocess.run(
                ['python3', str(project_root / 'scripts' / 'demo_experimentation_both.py')],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            execution_time = time.time() - start_time

            # Parsear resultados
            parsed = self.parse_output(result.stdout)

            if not parsed['algorithms']:
                print(f"⚠️  Sin algoritmos - {execution_time:.1f}s")
                # Registrar como error
                self.logger.log_run(
                    algorithm_pseudocode="ERROR: No algorithms generated",
                    algorithm_features={},
                    execution_status='error',
                    time_breakdown={'total': execution_time}
                )
                return True

            # Procesar cada algoritmo
            for algo_name, pseudocode in parsed['algorithms'].items():
                # Extraer features
                features = self.extract_algorithm_features(pseudocode)

                # Tiempos individuales
                algo_times = parsed['times'].get(algo_name, [])

                # Desglose temporal (simplificado - requiere instrumentación completa)
                time_breakdown = {
                    'generation': execution_time * 0.01,  # ~1% estimado
                    'initialization': execution_time * 0.02,  # ~2% estimado
                    'search': execution_time * 0.95,  # ~95% estimado
                    'evaluation': execution_time * 0.90,  # Dentro de search
                    'postprocessing': execution_time * 0.02,  # ~2% estimado
                    'total': execution_time
                }

                # Log completo
                self.logger.log_run(
                    algorithm_pseudocode=pseudocode,
                    algorithm_features=features,
                    execution_status='success',
                    time_breakdown=time_breakdown,
                    objective_value=None,  # Requiere parseo adicional
                    optimal_value=None
                )

            print(f"✅ {execution_time:.1f}s - {len(parsed['algorithms'])} algoritmos")

            # Reportar progreso periódicamente
            if self.run_number % self.report_every == 0:
                self.logger.print_progress()

            return True

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"⚠️  TIMEOUT ({self.timeout}s)")

            # Registrar timeout
            self.logger.log_run(
                algorithm_pseudocode="TIMEOUT: Execution exceeded limit",
                algorithm_features={},
                execution_status='timeout',
                time_breakdown={'total': execution_time}
            )

            return True

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ ERROR: {e}")

            # Registrar error
            self.logger.log_run(
                algorithm_pseudocode=f"ERROR: {str(e)}",
                algorithm_features={},
                execution_status='error',
                time_breakdown={'total': execution_time}
            )

            return True

    def run(self):
        """Ejecuta el protocolo completo"""
        print("=" * 80)
        print("PROTOCOLO EXPERIMENTAL DE 3 DÍAS")
        print("=" * 80)
        print()
        print(f"⚙️  Configuración:")
        print(f"   • Timeout por corrida: {self.timeout}s")
        print(f"   • Duración total: {self.duration.days} días")
        print(f"   • Output: {self.logger.output_dir}")
        print()

        self.start_time = datetime.now()
        self.end_time = self.start_time + self.duration

        print(f"🚀 Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🏁 Fin estimado: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Iniciando experimentación continua...")
        print()

        # Loop principal
        try:
            while True:
                should_continue = self.run_single_experiment()

                if not should_continue:
                    break

                # Pequeña pausa entre corridas
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⚠️  Experimentación interrumpida por el usuario")

        finally:
            # Reporte final
            print("\n" + "=" * 80)
            print("EXPERIMENTACIÓN FINALIZADA")
            print("=" * 80)

            actual_duration = datetime.now() - self.start_time
            print(f"\n⏱️  Duración real: {actual_duration}")
            print()

            self.logger.print_progress()

            print(f"\n📁 Archivos generados:")
            print(f"   • CSV: {self.logger.csv_file}")
            print(f"   • JSON: {self.logger.json_file}")
            print()


def main():
    """Función principal"""

    # Configuración por defecto del protocolo
    timeout = 60  # 60 segundos según protocolo
    duration_days = 3.0  # 3 días completos

    # Permitir override vía argumentos (para testing)
    if len(sys.argv) > 1:
        timeout = int(sys.argv[1])
    if len(sys.argv) > 2:
        duration_days = float(sys.argv[2])

    runner = ThreeDayProtocolRunner(
        timeout_seconds=timeout,
        duration_days=duration_days
    )

    runner.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
