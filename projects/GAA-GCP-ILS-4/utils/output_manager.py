"""
utils/output_manager.py
Gestor centralizado de outputs del proyecto GAA-GCP-ILS-4

Responsabilidades:
- Crear estructura de directorios unificada
- Generar timestamps consistentes (DD-MM-YY_HH-MM-SS)
- Guardar archivos en ubicaciones correctas
- Integrar con PlotManager
- Gestionar logs
"""

import json
import csv
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict


@dataclass
class SessionInfo:
    """Información de una sesión de ejecución"""
    timestamp: str
    mode: str
    family: Optional[str]
    session_dir: Path
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'mode': self.mode,
            'family': self.family,
            'session_dir': str(self.session_dir)
        }


class OutputManager:
    """
    Gestor centralizado de outputs del proyecto.
    
    Estructura de directorios generada:
    
    output/
    ├── results/
    │   ├── all_datasets/{timestamp}/
    │   ├── specific_datasets/{family}/{timestamp}/
    │   └── gaa_experiments/{timestamp}/
    ├── solutions/
    └── logs/
    
    Uso:
        >>> output_mgr = OutputManager()
        >>> session_dir = output_mgr.create_session(mode="all_datasets")
        >>> output_mgr.save_summary_csv(data)
        >>> output_mgr.save_detailed_json(results)
    """
    
    # Formato de timestamp unificado
    TIMESTAMP_FORMAT = "%d-%m-%y_%H-%M-%S"
    
    def __init__(self, config_path: Optional[str] = None, base_output_dir: Optional[str] = None):
        """
        Inicializa el gestor de outputs.
        
        Args:
            config_path: Ruta al config.yaml (opcional)
            base_output_dir: Directorio base de output (sobrescribe config)
        """
        # Inicializar logger primero
        self.logger = logging.getLogger(__name__)
        
        # Cargar configuración
        self.config = self._load_config(config_path)
        
        # Directorio base unificado: output/{timestamp}/
        self.base_output_dir = Path(base_output_dir or 'output')
        
        # Sesión actual
        self.session_info: Optional[SessionInfo] = None
        self.session_dir: Optional[Path] = None
        self.results_dir: Optional[Path] = None
        self.plots_dir: Optional[Path] = None
        self.solutions_dir: Optional[Path] = None
        self.logs_dir: Optional[Path] = None
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Carga configuración desde config.yaml.
        
        Args:
            config_path: Ruta al config.yaml
        
        Returns:
            Diccionario de configuración
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
    
    def _create_base_dirs(self):
        """Crea directorios base si no existen"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def create_session(self, mode: str = "all_datasets", family: Optional[str] = None) -> Path:
        """
        Crea una sesión de ejecución con timestamp único.
        
        Estructura unificada:
        output/{timestamp}/
        ├── results/
        ├── plots/
        ├── solutions/
        └── logs/
        
        Args:
            mode: Tipo de ejecución (all_datasets, specific_dataset, gaa_experiment)
            family: Familia de dataset (requerido para specific_dataset)
        
        Returns:
            Path del directorio de sesión creado
        """
        timestamp = datetime.now().strftime(self.TIMESTAMP_FORMAT)
        
        # Crear directorio de sesión unificado: output/{timestamp}/
        self.session_dir = self.base_output_dir / timestamp
        
        # Crear subdirectorios dentro de la sesión
        self.results_dir = self.session_dir / "results"
        self.plots_dir = self.session_dir / "plots"
        self.solutions_dir = self.session_dir / "solutions"
        self.logs_dir = self.session_dir / "logs"
        self.gaa_dir = self.session_dir / "gaa"
        
        # Crear todos los directorios
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.gaa_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar información de sesión
        self.session_info = SessionInfo(
            timestamp=timestamp,
            mode=mode,
            family=family,
            session_dir=self.session_dir
        )
        
        self.logger.info(f"Session created: {self.session_dir}")
        return self.session_dir
    
    def get_session_dir(self) -> Path:
        """Retorna directorio de sesión actual"""
        if self.session_info is None:
            raise RuntimeError("No session created. Call create_session() first")
        return self.session_info.session_dir
    
    def get_timestamp(self) -> str:
        """Retorna timestamp de sesión actual"""
        if self.session_info is None:
            raise RuntimeError("No session created. Call create_session() first")
        return self.session_info.timestamp
    
    # ========================================================================
    # GUARDADO DE ARCHIVOS DE DATOS
    # ========================================================================
    
    def save_summary_csv(self, data: List[Dict[str, Any]], filename: str = "summary.csv") -> str:
        """
        Guarda tabla resumen en formato CSV.
        
        Args:
            data: Lista de diccionarios con datos
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.results_dir / filename
        
        if not data:
            self.logger.warning("Empty data for CSV")
            return str(filepath)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        self.logger.info(f"CSV saved: {filepath}")
        return str(filepath)
    
    def save_detailed_json(self, data: Dict[str, Any], filename: str = "detailed_results.json") -> str:
        """
        Guarda resultados detallados en formato JSON.
        
        Args:
            data: Diccionario con resultados completos
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.results_dir / filename
        
        # Convertir objetos no serializables
        serializable_data = self._make_serializable(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON saved: {filepath}")
        return str(filepath)
    
    def save_statistics_txt(self, content: str, filename: str = "statistics.txt") -> str:
        """
        Guarda reporte estadístico en formato texto.
        
        Args:
            content: Contenido del reporte
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"TXT saved: {filepath}")
        return str(filepath)
    
    def save_solution(self, instance_name: str, solution, problem=None) -> str:
        """
        Guarda archivo de solución en formato .sol.
        
        Formato:
            c Solution for {instance_name}
            c Colors: {num_colors}
            c Feasible: {is_feasible}
            c Conflicts: {num_conflicts}
            {vertex} {color}
            ...
        
        Args:
            instance_name: Nombre de la instancia
            solution: Objeto ColoringSolution
            problem: Objeto GraphColoringProblem (opcional)
        
        Returns:
            Ruta del archivo guardado
        """
        filename = f"{instance_name}_{self.get_timestamp()}.sol"
        filepath = self.solutions_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"c Solution for {instance_name}\n")
            f.write(f"c Timestamp: {self.get_timestamp()}\n")
            f.write(f"c Colors: {solution.num_colors}\n")
            
            if problem:
                conflicts = solution.num_conflicts(problem)
                feasible = solution.is_feasible(problem)
                f.write(f"c Conflicts: {conflicts}\n")
                f.write(f"c Feasible: {feasible}\n")
            
            f.write("c\n")
            f.write("c Format: vertex color\n")
            f.write("c\n")
            
            for vertex, color in sorted(solution.assignment.items()):
                f.write(f"{vertex} {color}\n")
        
        self.logger.info(f"Solution saved: {filepath}")
        return str(filepath)
    
    # ========================================================================
    # GUARDADO DE ARCHIVOS GAA
    # ========================================================================
    
    def save_algorithm_json(self, algorithm, filename: str = "best_algorithm.json") -> str:
        """
        Guarda algoritmo GAA en formato JSON.
        
        Args:
            algorithm: AST del algoritmo
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.gaa_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(algorithm.to_dict(), f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Algorithm JSON saved: {filepath}")
        return str(filepath)
    
    def save_algorithm_pseudocode(self, algorithm, filename: str = "algorithm_pseudocode.txt") -> str:
        """
        Guarda pseudocódigo del algoritmo GAA.
        
        Args:
            algorithm: AST del algoritmo
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.gaa_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ALGORITMO GENERADO POR GAA\n")
            f.write("="*80 + "\n\n")
            f.write(algorithm.to_pseudocode(indent=0))
            f.write("\n\n")
            f.write("="*80 + "\n")
        
        self.logger.info(f"Pseudocode saved: {filepath}")
        return str(filepath)
    
    def save_evolution_history(self, history: Dict[str, Any], filename: str = "evolution_history.json") -> str:
        """
        Guarda historial de evolución GAA.
        
        Args:
            history: Diccionario con historial de evolución
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.gaa_dir / filename
        
        serializable_history = self._make_serializable(history)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_history, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Evolution history saved: {filepath}")
        return str(filepath)
    
    def save_population_stats(self, stats: Dict[str, Any], filename: str = "population_stats.json") -> str:
        """
        Guarda estadísticas de población GAA.
        
        Args:
            stats: Diccionario con estadísticas
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.gaa_dir / filename
        
        serializable_stats = self._make_serializable(stats)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_stats, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Population stats saved: {filepath}")
        return str(filepath)
    
    def save_gaa_summary(self, content: str, filename: str = "evolution_summary.txt") -> str:
        """
        Guarda resumen de evolución GAA.
        
        Args:
            content: Contenido del resumen
            filename: Nombre del archivo
        
        Returns:
            Ruta del archivo guardado
        """
        filepath = self.gaa_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"GAA summary saved: {filepath}")
        return str(filepath)
    
    def get_gaa_algorithms_dir(self) -> Path:
        """
        Retorna directorio para guardar algoritmos individuales de GAA.
        
        Returns:
            Path del directorio gaa/algorithms/
        """
        algorithms_dir = self.gaa_dir / "algorithms"
        algorithms_dir.mkdir(parents=True, exist_ok=True)
        return algorithms_dir
    
    def save_generation_algorithms(self, generation: int, algorithms: list) -> str:
        """
        Guarda algoritmos de una generación.
        
        Args:
            generation: Número de generación
            algorithms: Lista de algoritmos
        
        Returns:
            Ruta del directorio creado
        """
        gen_dir = self.get_gaa_algorithms_dir() / f"generation_{generation}"
        gen_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, algorithm in enumerate(algorithms):
            filename = f"algorithm_{idx}.json"
            filepath = gen_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(algorithm.to_dict() if hasattr(algorithm, 'to_dict') else algorithm, 
                         f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generation {generation} algorithms saved: {gen_dir}")
        return str(gen_dir)
    
    # ========================================================================
    # GESTIÓN DE LOGS
    # ========================================================================
    
    def create_log_file(self, prefix: str = "execution") -> str:
        """
        Crea archivo de log para la sesión.
        
        Args:
            prefix: Prefijo del nombre de archivo
        
        Returns:
            Ruta del archivo de log
        """
        filename = f"{prefix}_{self.get_timestamp()}.log"
        filepath = self.logs_dir / filename
        
        self.logger.info(f"Log file created: {filepath}")
        return str(filepath)
    
    def setup_logging(self, level: int = logging.INFO, prefix: str = "execution"):
        """
        Configura logging para la sesión.
        
        Args:
            level: Nivel de logging
            prefix: Prefijo del archivo de log
        """
        log_file = self.create_log_file(prefix)
        
        # Configurar handler de archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Agregar handler al logger raíz
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().setLevel(level)
        
        self.logger.info(f"Logging configured: {log_file}")
    
    # ========================================================================
    # INTEGRACIÓN CON PLOTTER
    # ========================================================================
    
    def get_plot_dir(self) -> Path:
        """
        Retorna directorio para gráficas de la sesión actual.
        
        Las gráficas se guardan en el mismo directorio que los resultados.
        
        Returns:
            Path del directorio de sesión
        """
        return self.get_session_dir()
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _make_serializable(self, obj: Any) -> Any:
        """
        Convierte objetos a formato serializable JSON.
        
        Args:
            obj: Objeto a convertir
        
        Returns:
            Objeto serializable
        """
        import numpy as np
        
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        else:
            return obj
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Retorna información de la sesión actual.
        
        Returns:
            Diccionario con información de sesión
        """
        if self.session_info is None:
            raise RuntimeError("No session created")
        return self.session_info.to_dict()
    
    def list_sessions(self, mode: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lista sesiones existentes.
        
        Args:
            mode: Filtrar por modo (opcional)
        
        Returns:
            Lista de diccionarios con información de sesiones
        """
        sessions = []
        
        # Buscar en all_datasets
        if mode is None or mode == "all_datasets":
            all_dir = self.base_dir / "all_datasets"
            if all_dir.exists():
                for session_dir in sorted(all_dir.iterdir(), reverse=True):
                    if session_dir.is_dir():
                        sessions.append({
                            'timestamp': session_dir.name,
                            'mode': 'all_datasets',
                            'path': str(session_dir)
                        })
        
        # Buscar en specific_datasets
        if mode is None or mode == "specific_dataset":
            specific_dir = self.base_dir / "specific_datasets"
            if specific_dir.exists():
                for family_dir in specific_dir.iterdir():
                    if family_dir.is_dir():
                        for session_dir in sorted(family_dir.iterdir(), reverse=True):
                            if session_dir.is_dir():
                                sessions.append({
                                    'timestamp': session_dir.name,
                                    'mode': 'specific_dataset',
                                    'family': family_dir.name,
                                    'path': str(session_dir)
                                })
        
        # Buscar en gaa_experiments
        if mode is None or mode == "gaa_experiment":
            gaa_dir = self.base_dir / "gaa_experiments"
            if gaa_dir.exists():
                for session_dir in sorted(gaa_dir.iterdir(), reverse=True):
                    if session_dir.is_dir():
                        sessions.append({
                            'timestamp': session_dir.name,
                            'mode': 'gaa_experiment',
                            'path': str(session_dir)
                        })
        
        return sessions
    
    def __repr__(self) -> str:
        """Representación del OutputManager"""
        if self.session_info:
            return f"OutputManager(session={self.session_info.timestamp}, mode={self.session_info.mode})"
        return "OutputManager(no active session)"
