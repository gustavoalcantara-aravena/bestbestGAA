"""
Execution Logger - KBP-SA
Sistema completo de logging para reproducibilidad científica
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess


class ExecutionLogger:
    """
    Logger completo para documentar toda la ejecución

    Guarda:
    - Configuración completa (seeds, parámetros, etc.)
    - Algoritmos generados (pseudocódigo completo)
    - Versión del código (git hash)
    - Entorno de ejecución (Python, numpy, etc.)
    - Timestamps de cada paso
    - Resultados finales
    """

    def __init__(self, output_dir: str, experiment_name: str):
        """
        Inicializa logger

        Args:
            output_dir: Directorio donde guardar logs
            experiment_name: Nombre del experimento
        """
        self.output_dir = Path(output_dir)
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Crear directorio si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Archivo de configuración
        self.config_file = self.output_dir / f"execution_config_{self.timestamp}.json"

        # Archivo de log completo
        self.log_file = self.output_dir / f"execution_log_{self.timestamp}.md"

        # Datos a guardar
        self.config = {
            'experiment_name': experiment_name,
            'timestamp': self.timestamp,
            'start_time': datetime.now().isoformat(),
            'environment': self._get_environment_info(),
            'git_info': self._get_git_info(),
            'algorithms': [],
            'parameters': {},
            'execution_steps': [],
            'results_summary': {}
        }

        # Iniciar log markdown
        self._init_log_file()

    def _get_environment_info(self) -> Dict[str, str]:
        """Obtiene información del entorno de ejecución"""
        import platform
        import numpy as np

        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'platform_system': platform.system(),
            'platform_release': platform.release(),
            'numpy_version': np.__version__,
            'working_directory': os.getcwd()
        }

    def _get_git_info(self) -> Dict[str, str]:
        """Obtiene información de Git para reproducibilidad"""
        try:
            # Git hash
            git_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Branch
            git_branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Check if there are uncommitted changes
            git_status = subprocess.check_output(
                ['git', 'status', '--porcelain'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            has_changes = len(git_status) > 0

            return {
                'git_hash': git_hash,
                'git_branch': git_branch,
                'has_uncommitted_changes': has_changes,
                'git_status': git_status if has_changes else 'clean'
            }
        except Exception as e:
            return {
                'git_hash': 'unknown',
                'error': str(e)
            }

    def _init_log_file(self):
        """Inicializa archivo de log markdown"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"# Execution Log: {self.experiment_name}\n\n")
            f.write(f"**Timestamp**: {self.timestamp}\n")
            f.write(f"**Start Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## Environment Information\n\n")
            f.write(f"- **Python**: {self.config['environment']['python_version'].split()[0]}\n")
            f.write(f"- **Platform**: {self.config['environment']['platform']}\n")
            f.write(f"- **NumPy**: {self.config['environment']['numpy_version']}\n")
            f.write(f"- **Working Directory**: {self.config['environment']['working_directory']}\n\n")

            f.write("## Git Information\n\n")
            git_info = self.config['git_info']
            f.write(f"- **Git Hash**: `{git_info.get('git_hash', 'unknown')}`\n")
            f.write(f"- **Branch**: `{git_info.get('git_branch', 'unknown')}`\n")
            f.write(f"- **Uncommitted Changes**: {git_info.get('has_uncommitted_changes', 'unknown')}\n\n")

            if git_info.get('has_uncommitted_changes'):
                f.write("```\n")
                f.write(git_info.get('git_status', ''))
                f.write("\n```\n\n")

            f.write("---\n\n")

    def log_parameters(self, **params):
        """
        Registra parámetros de configuración

        Args:
            **params: Parámetros clave-valor
        """
        self.config['parameters'].update(params)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("## Configuration Parameters\n\n")
            f.write("```json\n")
            f.write(json.dumps(params, indent=2))
            f.write("\n```\n\n")
            f.write("---\n\n")

    def log_algorithm(self, name: str, pseudocode: str, ast_dict: Optional[Dict] = None):
        """
        Registra un algoritmo generado

        Args:
            name: Nombre del algoritmo
            pseudocode: Pseudocódigo completo
            ast_dict: Representación del AST (opcional)
        """
        algorithm_info = {
            'name': name,
            'pseudocode': pseudocode,
            'timestamp': datetime.now().isoformat()
        }

        if ast_dict:
            algorithm_info['ast'] = ast_dict

        self.config['algorithms'].append(algorithm_info)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"## Algorithm: {name}\n\n")
            f.write("**Pseudocode:**\n\n")
            f.write("```\n")
            f.write(pseudocode)
            f.write("\n```\n\n")

            if ast_dict:
                f.write("**AST Representation:**\n\n")
                f.write("```json\n")
                f.write(json.dumps(ast_dict, indent=2))
                f.write("\n```\n\n")

            f.write("---\n\n")

    def log_step(self, step_name: str, details: Optional[Dict] = None):
        """
        Registra un paso de ejecución

        Args:
            step_name: Nombre del paso
            details: Detalles adicionales (opcional)
        """
        step_info = {
            'step_name': step_name,
            'timestamp': datetime.now().isoformat(),
        }

        if details:
            step_info['details'] = details

        self.config['execution_steps'].append(step_info)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"### Step: {step_name}\n\n")
            f.write(f"**Time**: {datetime.now().strftime('%H:%M:%S')}\n\n")

            if details:
                f.write("**Details:**\n\n")
                f.write("```json\n")
                f.write(json.dumps(details, indent=2))
                f.write("\n```\n\n")

    def log_result(self, result_name: str, result_data: Any):
        """
        Registra un resultado

        Args:
            result_name: Nombre del resultado
            result_data: Datos del resultado
        """
        self.config['results_summary'][result_name] = result_data

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"### Result: {result_name}\n\n")
            f.write("```json\n")
            f.write(json.dumps(result_data, indent=2, default=str))
            f.write("\n```\n\n")

    def finalize(self, total_time: Optional[float] = None, success: bool = True):
        """
        Finaliza el logging y guarda archivos

        Args:
            total_time: Tiempo total de ejecución (opcional)
            success: Si la ejecución fue exitosa
        """
        self.config['end_time'] = datetime.now().isoformat()
        self.config['success'] = success

        if total_time:
            self.config['total_execution_time_seconds'] = total_time

        # Guardar configuración completa en JSON
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, default=str)

        # Finalizar log markdown
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("---\n\n")
            f.write("## Execution Summary\n\n")
            f.write(f"- **Status**: {'✅ Success' if success else '❌ Failed'}\n")
            f.write(f"- **End Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            if total_time:
                f.write(f"- **Total Time**: {total_time:.2f}s\n")

            f.write(f"\n**Configuration saved to**: `{self.config_file.name}`\n\n")

            f.write("### Algorithms Generated\n\n")
            for alg in self.config['algorithms']:
                f.write(f"- **{alg['name']}**\n")

            f.write("\n### Results Summary\n\n")
            f.write("```json\n")
            f.write(json.dumps(self.config['results_summary'], indent=2, default=str))
            f.write("\n```\n\n")

            f.write("---\n\n")
            f.write(f"**Log completed at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        return {
            'config_file': str(self.config_file),
            'log_file': str(self.log_file)
        }

    def get_summary(self) -> Dict:
        """Retorna resumen de la ejecución"""
        return {
            'timestamp': self.timestamp,
            'config_file': str(self.config_file),
            'log_file': str(self.log_file),
            'algorithms_count': len(self.config['algorithms']),
            'steps_count': len(self.config['execution_steps'])
        }
