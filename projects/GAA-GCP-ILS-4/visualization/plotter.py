"""
visualization/plotter.py
Gestor central de visualizaciones

Orquesta la generación de todos los tipos de gráficas.
Integrado con la estructura de output del proyecto.
"""

import json
import yaml
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

from .convergence import (
    plot_convergence_single,
    plot_convergence_multiple,
    plot_convergence_by_family
)
from .robustness import plot_robustness, plot_multi_robustness
from .scalability import plot_scalability_time, plot_scalability_iterations, plot_complexity_analysis
from .heatmap import plot_conflict_heatmap, plot_conflict_distribution, plot_conflict_statistics
from .time_quality import plot_time_quality_tradeoff, plot_multiple_algorithms_tradeoff, plot_convergence_speed


# Configurar logging
logger = logging.getLogger(__name__)


class PlotManager:
    """Gestor centralizado de visualizaciones con integración a config.yaml."""
    
    def __init__(self, output_dir: Optional[str] = None, config_path: Optional[str] = None):
        """
        Inicializa el gestor de visualizaciones.
        
        Parámetros:
            output_dir: Directorio base para guardar resultados
                       Si None, carga de config.yaml
            config_path: Ruta al config.yaml (si None, busca automáticamente)
        """
        # Cargar configuración
        self.config = self._load_config(config_path)
        
        # Determinar directorio de output
        if output_dir is None:
            output_dir = self.config.get('output', {}).get('plots_dir', 'output/plots')
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir = None
        self.logger = logger
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Carga la configuración desde config.yaml.
        
        Parámetros:
            config_path: Ruta al config.yaml
        
        Retorna:
            dict: Configuración cargada
        """
        if config_path is None:
            # Buscar config.yaml en ubicaciones estándar
            possible_paths = [
                Path(__file__).parent.parent / "config" / "config.yaml",
                Path("config") / "config.yaml",
                Path(".") / "config.yaml"
            ]
            
            for path in possible_paths:
                if path.exists():
                    config_path = path
                    break
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                self.logger.warning(f"Error cargando config: {e}")
                return {}
        
        return {}
    
    def create_session_dir(self, mode: str = "all_datasets") -> Path:
        """
        Crea un directorio de sesión con timestamp.
        
        RESPETA LA ESTRUCTURA DE OUTPUT DEL PROYECTO:
        - output/results/all_datasets/{timestamp}/
        - output/results/specific_datasets/{family}/{timestamp}/
        
        Parámetros:
            mode: "all_datasets" o "specific_datasets/{family}"
        
        Retorna:
            Path: Ruta del directorio de sesión
        """
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        
        # Construir ruta según estructura de proyecto
        if mode.startswith("specific_datasets/"):
            # Modo específico: output/results/specific_datasets/FAMILY/timestamp/
            family = mode.split("/")[1]
            session_dir = self.output_dir / "specific_datasets" / family / timestamp
        else:
            # Modo todos: output/results/all_datasets/timestamp/
            session_dir = self.output_dir / "all_datasets" / timestamp
        
        session_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir = session_dir
        self.logger.info(f"Session directory created: {session_dir}")
        return session_dir
    
    def plot_convergence(
        self,
        fitness_history: List[float],
        times: Optional[List[float]] = None,
        instance_name: str = "Instance",
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera gráfica de convergencia de una ejecución.
        
        Parámetros:
            fitness_history: Historial de fitness
            times: Tiempos opcionales
            instance_name: Nombre de la instancia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "convergence_plot.png"
        return plot_convergence_single(
            fitness_history,
            times=times,
            output_path=str(output_path),
            instance_name=instance_name,
            title="Convergencia de ILS"
        )
    
    def plot_convergence_ensemble(
        self,
        fitness_histories: List[List[float]],
        instance_name: str = "Instance",
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera gráfica de convergencia promediada de múltiples ejecuciones.
        
        Parámetros:
            fitness_histories: Lista de historiales de fitness
            instance_name: Nombre de la instancia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "convergence_ensemble_plot.png"
        return plot_convergence_multiple(
            fitness_histories,
            instance_name=instance_name,
            output_path=str(output_path),
            title="Convergencia Promediada"
        )
    
    def plot_robustness(
        self,
        results: List[float],
        bks: Optional[float] = None,
        instance_name: str = "Instance",
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera boxplot de robustez.
        
        Parámetros:
            results: Lista de resultados finales (múltiples ejecuciones)
            bks: Best Known Solution
            instance_name: Nombre de la instancia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "boxplot_robustness.png"
        return plot_robustness(
            results,
            bks=bks,
            output_path=str(output_path),
            instance_name=instance_name
        )
    
    def plot_scalability(
        self,
        vertices: List[int],
        times: List[float],
        family_labels: Optional[List[str]] = None,
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera gráfica de escalabilidad (tiempo vs tamaño).
        
        Parámetros:
            vertices: Tamaños de instancia
            times: Tiempos de ejecución
            family_labels: Etiquetas de familia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "scalability_plot.png"
        return plot_scalability_time(
            vertices,
            times,
            family_labels=family_labels,
            output_path=str(output_path)
        )
    
    def plot_conflict_heatmap(
        self,
        conflict_matrix: np.ndarray,
        instance_name: str = "Instance",
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera heatmap de conflictos.
        
        Parámetros:
            conflict_matrix: Matriz de conflictos n×n
            instance_name: Nombre de la instancia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "conflict_heatmap.png"
        return plot_conflict_heatmap(
            conflict_matrix,
            instance_name=instance_name,
            output_path=str(output_path)
        )
    
    def plot_time_quality(
        self,
        times: List[float],
        fitness_values: List[float],
        instance_name: str = "Instance",
        output_dir: Optional[Path] = None
    ) -> Optional[str]:
        """
        Genera gráfica tiempo-calidad.
        
        Parámetros:
            times: Tiempos de computación
            fitness_values: Valores de fitness
            instance_name: Nombre de la instancia
            output_dir: Directorio para guardar
        
        Retorna:
            str: Ruta del archivo generado
        """
        if output_dir is None:
            output_dir = self.session_dir or self.output_dir
        
        output_path = output_dir / "time_quality_tradeoff.png"
        return plot_time_quality_tradeoff(
            times,
            fitness_values,
            instance_name=instance_name,
            output_path=str(output_path)
        )
    
    def plot_all(
        self,
        experiment_data: Dict[str, Any],
        mode: str = "all_datasets",
        create_session: bool = True
    ) -> Dict[str, str]:
        """
        Genera todas las gráficas disponibles.
        
        Las gráficas se guardan automáticamente en la estructura:
        - output/results/all_datasets/{timestamp}/ (modo all)
        - output/results/specific_datasets/{family}/{timestamp}/ (modo specific)
        
        Parámetros:
            experiment_data: Diccionario con datos del experimento
                Esperado: {
                    'instance_name': str,
                    'convergence': [list of fitness values],
                    'convergence_histories': [list of lists],
                    'robustness': [list of final fitness values],
                    'bks': float,
                    'vertices': [list of sizes],
                    'times': [list of times],
                    'conflict_matrix': np.ndarray,
                    'time_fitness_pairs': [(time, fitness), ...]
                }
            mode: "all_datasets" o "specific_datasets/FAMILY"
            create_session: Si True, crea nuevo directorio de sesión
        
        Retorna:
            Dict[str, str]: Diccionario con rutas de archivos generados
        """
        # Crear sesión si es necesario
        if create_session:
            self.create_session_dir(mode)
        
        if self.session_dir is None:
            raise ValueError("No session directory created. Call create_session_dir() first")
        
        results = {}
        
        try:
            instance_name = experiment_data.get('instance_name', 'Instance')
            
            # Convergencia simple
            if 'convergence' in experiment_data:
                try:
                    path = self.plot_convergence(
                        experiment_data['convergence'],
                        instance_name=instance_name,
                        times=experiment_data.get('times')
                    )
                    results['convergence'] = path
                    self.logger.info(f"✓ Convergence plot generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate convergence plot: {e}")
            
            # Convergencia promediada
            if 'convergence_histories' in experiment_data:
                try:
                    path = self.plot_convergence_ensemble(
                        experiment_data['convergence_histories'],
                        instance_name=instance_name
                    )
                    results['convergence_ensemble'] = path
                    self.logger.info(f"✓ Convergence ensemble plot generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate convergence ensemble: {e}")
            
            # Robustez
            if 'robustness' in experiment_data:
                try:
                    path = self.plot_robustness(
                        experiment_data['robustness'],
                        bks=experiment_data.get('bks'),
                        instance_name=instance_name
                    )
                    results['robustness'] = path
                    self.logger.info(f"✓ Robustness plot generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate robustness plot: {e}")
            
            # Escalabilidad
            if 'vertices' in experiment_data and 'times' in experiment_data:
                try:
                    path = self.plot_scalability(
                        experiment_data['vertices'],
                        experiment_data['times'],
                        family_labels=experiment_data.get('family_labels')
                    )
                    results['scalability'] = path
                    self.logger.info(f"✓ Scalability plot generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate scalability plot: {e}")
            
            # Heatmap de conflictos
            if 'conflict_matrix' in experiment_data:
                try:
                    path = self.plot_conflict_heatmap(
                        experiment_data['conflict_matrix'],
                        instance_name=instance_name
                    )
                    results['conflict_heatmap'] = path
                    self.logger.info(f"✓ Conflict heatmap generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate conflict heatmap: {e}")
            
            # Tiempo-Calidad
            if 'time_fitness_pairs' in experiment_data:
                try:
                    times = [t for t, _ in experiment_data['time_fitness_pairs']]
                    fitness = [f for _, f in experiment_data['time_fitness_pairs']]
                    path = self.plot_time_quality(
                        times,
                        fitness,
                        instance_name=instance_name
                    )
                    results['time_quality'] = path
                    self.logger.info(f"✓ Time-quality plot generated: {path}")
                except Exception as e:
                    self.logger.warning(f"✗ Failed to generate time-quality plot: {e}")
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error in plot_all: {e}")
            return results
    
    def save_summary(self, data: Dict[str, Any]) -> str:
        """
        Guarda un resumen de los resultados en JSON.
        
        Parámetros:
            data: Datos a guardar
        
        Retorna:
            str: Ruta del archivo guardado
        """
        summary_path = self.session_dir / "summary.json"
        
        # Convertir arrays numpy a listas
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            return obj
        
        serializable_data = convert_to_serializable(data)
        
        with open(summary_path, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        self.logger.info(f"Summary saved: {summary_path}")
        return str(summary_path)
