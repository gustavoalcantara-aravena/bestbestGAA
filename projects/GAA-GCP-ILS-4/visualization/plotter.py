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
    
    def __init__(self, session_dir: Optional[str] = None, config_path: Optional[str] = None):
        """
        Inicializa el gestor de visualizaciones.
        
        Parámetros:
            session_dir: Directorio de sesión (output/{timestamp}/)
                        Las gráficas se guardarán en {session_dir}/plots/
            config_path: Ruta al config.yaml (si None, busca automáticamente)
        """
        # Inicializar logger primero
        self.logger = logger
        
        # Cargar configuración
        self.config = self._load_config(config_path)
        
        # Determinar directorio de output
        # Las gráficas van en {session_dir}/plots/
        if session_dir:
            self.output_dir = Path(session_dir) / "plots"
        else:
            self.output_dir = Path(self.config.get('output', {}).get('plots_dir', 'output/plots'))
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir = self.output_dir
        self.logger.info(f"PlotManager inicializado con directorio: {self.output_dir}")
    
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
        - output/plots/all_datasets/{timestamp}/
        - output/plots/specific_datasets/{family}/{timestamp}/
        
        Parámetros:
            mode: "all_datasets" o "specific_datasets/{family}"
        
        Retorna:
            Path: Ruta del directorio de sesión
        """
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        
        # Construir ruta según estructura de proyecto
        # Las gráficas van en output/plots/ (no en output/results/)
        if mode.startswith("specific_datasets/"):
            # Modo específico: output/plots/specific_datasets/FAMILY/timestamp/
            family = mode.split("/")[1]
            session_dir = self.output_dir / "specific_datasets" / family / timestamp
        else:
            # Modo todos: output/plots/all_datasets/timestamp/
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
    
    # ========================================================================
    # GRÁFICAS AGREGADAS (PATRÓN BOTH) PARA COMPARACIÓN DE ALGORITMOS GAA
    # ========================================================================
    
    def plot_algorithm_comparison_boxplot(self, 
                                         algorithm_results: Dict[str, List[float]],
                                         title: str = "Comparación de Algoritmos GAA",
                                         filename: str = "algorithm_comparison_boxplot.png") -> str:
        """
        Genera boxplot comparativo de algoritmos GAA
        
        Args:
            algorithm_results: Dict con {nombre_algoritmo: [valores]}
            title: Título de la gráfica
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        import matplotlib.pyplot as plt
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Preparar datos
            algorithms = list(algorithm_results.keys())
            data = [algorithm_results[alg] for alg in algorithms]
            
            # Crear boxplot
            bp = ax.boxplot(data, labels=algorithms, patch_artist=True)
            
            # Colorear boxes
            colors = ['lightblue', 'lightgreen', 'lightcoral']
            for patch, color in zip(bp['boxes'], colors[:len(algorithms)]):
                patch.set_facecolor(color)
            
            ax.set_ylabel('Valor (Gap o Colores)', fontsize=12)
            ax.set_xlabel('Algoritmo', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Guardar
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Algorithm comparison boxplot saved: {filepath}")
            return str(filepath)
        
        except Exception as e:
            self.logger.error(f"Error generating algorithm comparison boxplot: {e}")
            return ""
    
    def plot_algorithm_ranking_bars(self,
                                   rankings: Dict[str, float],
                                   title: str = "Ranking Promedio de Algoritmos GAA",
                                   filename: str = "algorithm_ranking_bars.png") -> str:
        """
        Genera gráfica de barras con ranking de algoritmos
        
        Args:
            rankings: Dict con {nombre_algoritmo: ranking_promedio}
            title: Título de la gráfica
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        import matplotlib.pyplot as plt
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Ordenar por ranking
            sorted_rankings = sorted(rankings.items(), key=lambda x: x[1])
            algorithms = [alg for alg, _ in sorted_rankings]
            ranks = [rank for _, rank in sorted_rankings]
            
            # Crear barras
            colors = ['gold' if i == 0 else 'silver' if i == 1 else 'chocolate' 
                     for i in range(len(algorithms))]
            bars = ax.barh(algorithms, ranks, color=colors)
            
            # Agregar valores en las barras
            for i, (bar, rank) in enumerate(zip(bars, ranks)):
                ax.text(rank + 0.05, i, f'{rank:.2f}', va='center', fontsize=10)
            
            ax.set_xlabel('Ranking Promedio (menor = mejor)', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x')
            
            plt.tight_layout()
            
            # Guardar
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Algorithm ranking bars saved: {filepath}")
            return str(filepath)
        
        except Exception as e:
            self.logger.error(f"Error generating algorithm ranking bars: {e}")
            return ""
    
    def plot_algorithm_performance_scatter(self,
                                          algorithm_results: Dict[str, List[float]],
                                          instance_names: List[str] = None,
                                          title: str = "Desempeño de Algoritmos por Instancia",
                                          filename: str = "algorithm_performance_scatter.png") -> str:
        """
        Genera scatter plot del desempeño de algoritmos por instancia
        
        Args:
            algorithm_results: Dict con {nombre_algoritmo: [valores]}
            instance_names: Nombres de instancias (opcional)
            title: Título de la gráfica
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        import matplotlib.pyplot as plt
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            algorithms = list(algorithm_results.keys())
            colors = ['blue', 'green', 'red', 'orange', 'purple']
            
            # Plotear cada algoritmo
            for idx, (alg, values) in enumerate(algorithm_results.items()):
                x_pos = np.arange(len(values))
                ax.scatter(x_pos, values, label=alg, alpha=0.6, s=100, 
                          color=colors[idx % len(colors)])
            
            ax.set_xlabel('Instancia', fontsize=12)
            ax.set_ylabel('Valor (Gap o Colores)', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Guardar
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Algorithm performance scatter saved: {filepath}")
            return str(filepath)
        
        except Exception as e:
            self.logger.error(f"Error generating algorithm performance scatter: {e}")
            return ""
    
    def plot_group_comparison(self,
                             group1_results: Dict[str, List[float]],
                             group2_results: Dict[str, List[float]],
                             group1_name: str = "Grupo 1",
                             group2_name: str = "Grupo 2",
                             title: str = "Comparación entre Grupos",
                             filename: str = "group_comparison.png") -> str:
        """
        Genera gráfica comparativa entre dos grupos (BOTH pattern)
        
        Args:
            group1_results: Resultados del grupo 1
            group2_results: Resultados del grupo 2
            group1_name: Nombre del grupo 1
            group2_name: Nombre del grupo 2
            title: Título de la gráfica
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        import matplotlib.pyplot as plt
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Grupo 1
            algorithms1 = list(group1_results.keys())
            data1 = [group1_results[alg] for alg in algorithms1]
            bp1 = ax1.boxplot(data1, labels=algorithms1, patch_artist=True)
            for patch in bp1['boxes']:
                patch.set_facecolor('lightblue')
            ax1.set_title(f"{group1_name}", fontsize=12, fontweight='bold')
            ax1.set_ylabel('Valor', fontsize=11)
            ax1.grid(True, alpha=0.3)
            
            # Grupo 2
            algorithms2 = list(group2_results.keys())
            data2 = [group2_results[alg] for alg in algorithms2]
            bp2 = ax2.boxplot(data2, labels=algorithms2, patch_artist=True)
            for patch in bp2['boxes']:
                patch.set_facecolor('lightcoral')
            ax2.set_title(f"{group2_name}", fontsize=12, fontweight='bold')
            ax2.set_ylabel('Valor', fontsize=11)
            ax2.grid(True, alpha=0.3)
            
            fig.suptitle(title, fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Guardar
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Group comparison plot saved: {filepath}")
            return str(filepath)
        
        except Exception as e:
            self.logger.error(f"Error generating group comparison plot: {e}")
            return ""
