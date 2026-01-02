"""
Phase 7: Output Manager - Gestión centralizada de outputs y métricas

Responsabilidades:
1. OutputManager: Crear estructura de directorios con timestamps únicos
2. MetricsCalculator: Calcular métricas jerárquicas según especificación canónica
3. ResultsFormatter: Preparar datos para CSV según esquema exacto
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from enum import Enum


class TimestampFormat(Enum):
    """Formato canónico de timestamp: DD-MM-YY_HH-MM-SS"""
    STANDARD = "%d-%m-%y_%H-%M-%S"


@dataclass
class ExecutionResult:
    """Resultado de una ejecución simple (algoritmo x instancia x run)"""
    algorithm_id: str
    instance_id: str
    family: str
    run_id: int
    random_seed: int
    K_final: int
    D_final: float
    K_BKS: int
    D_BKS: float
    total_time_sec: float
    iterations_executed: int
    
    # Calculados automáticamente
    delta_K: int = field(init=False)
    gap_distance: Optional[float] = field(init=False)
    gap_percent: Optional[float] = field(init=False)
    reached_K_BKS: bool = field(init=False)
    
    def __post_init__(self):
        """Calcular campos derivados"""
        self.delta_K = self.K_final - self.K_BKS
        self.reached_K_BKS = (self.K_final == self.K_BKS)
        
        # gap_distance y gap_percent solo si K_final == K_BKS
        if self.reached_K_BKS:
            self.gap_distance = self.D_final - self.D_BKS
            self.gap_percent = ((self.D_final - self.D_BKS) / self.D_BKS * 100) if self.D_BKS > 0 else 0.0
        else:
            self.gap_distance = None
            self.gap_percent = None


@dataclass
class ConvergencePoint:
    """Un punto de convergencia en una iteración"""
    algorithm_id: str
    instance_id: str
    family: str
    run_id: int
    iteration: int
    elapsed_time_sec: float
    K_best_so_far: int
    D_best_so_far: float
    is_K_BKS: bool


class OutputManager:
    """Gestor centralizado de estructura de outputs"""
    
    def __init__(self, output_root: str = "output"):
        """
        Inicializar OutputManager
        
        Args:
            output_root: Directorio raíz para outputs (default: "output")
        """
        self.output_root = Path(output_root)
        self.output_root.mkdir(exist_ok=True, parents=True)
        
        # Crear carpeta de ejecución con timestamp único
        timestamp = datetime.now().strftime(TimestampFormat.STANDARD.value)
        self.execution_dir = self.output_root / timestamp
        self.execution_dir.mkdir(exist_ok=True, parents=True)
        
        # Crear subdirectorios
        self.results_dir = self.execution_dir / "results"
        self.solutions_dir = self.execution_dir / "solutions"
        self.plots_dir = self.execution_dir / "plots"
        self.gaa_dir = self.execution_dir / "gaa"
        self.logs_dir = self.execution_dir / "logs"
        
        for d in [self.results_dir, self.solutions_dir, self.plots_dir, self.gaa_dir, self.logs_dir]:
            d.mkdir(exist_ok=True, parents=True)
        
        # Timestamp para referencias
        self.execution_timestamp = timestamp
        
        # Acumuladores de datos
        self.raw_results: List[ExecutionResult] = []
        self.convergence_trace: List[ConvergencePoint] = []
        self.execution_log_entries: List[str] = []
        self.error_log_entries: List[str] = []
        
        # Logger centralizado
        self._setup_logger()
    
    def _setup_logger(self):
        """Configurar logger centralizado"""
        self.logger = logging.getLogger("GAA-VRPTW")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para execution.log
        exec_handler = logging.FileHandler(self.logs_dir / "execution.log")
        exec_handler.setLevel(logging.DEBUG)
        exec_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        exec_handler.setFormatter(exec_formatter)
        
        # Handler para errors.log
        error_handler = logging.FileHandler(self.logs_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(exec_formatter)
        
        # Handler para console (opcional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(exec_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def add_result(self, result: ExecutionResult):
        """Registrar resultado de una ejecución"""
        self.raw_results.append(result)
        self.logger.info(
            f"Result: {result.algorithm_id} | {result.instance_id} (run {result.run_id}) | "
            f"K={result.K_final} (BKS={result.K_BKS}) | D={result.D_final:.2f} | "
            f"Time={result.total_time_sec:.2f}s"
        )
    
    def add_convergence_point(self, point: ConvergencePoint):
        """Registrar un punto de convergencia"""
        self.convergence_trace.append(point)
    
    def save_raw_results(self):
        """Guardar raw_results.csv con esquema canónico"""
        if not self.raw_results:
            self.logger.warning("No raw results to save")
            return
        
        # Convertir a lista de dicts
        data = []
        for result in self.raw_results:
            data.append({
                'algorithm_id': result.algorithm_id,
                'instance_id': result.instance_id,
                'family': result.family,
                'run_id': result.run_id,
                'random_seed': result.random_seed,
                'K_final': result.K_final,
                'D_final': result.D_final,
                'K_BKS': result.K_BKS,
                'D_BKS': result.D_BKS,
                'delta_K': result.delta_K,
                'gap_distance': result.gap_distance,
                'gap_percent': result.gap_percent,
                'total_time_sec': result.total_time_sec,
                'iterations_executed': result.iterations_executed,
                'reached_K_BKS': result.reached_K_BKS
            })
        
        df = pd.DataFrame(data)
        output_path = self.results_dir / "raw_results.csv"
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved raw_results.csv: {len(df)} rows")
    
    def save_convergence_trace(self):
        """Guardar convergence_trace.csv"""
        if not self.convergence_trace:
            self.logger.warning("No convergence trace to save")
            return
        
        data = [{
            'algorithm_id': p.algorithm_id,
            'instance_id': p.instance_id,
            'family': p.family,
            'run_id': p.run_id,
            'iteration': p.iteration,
            'elapsed_time_sec': p.elapsed_time_sec,
            'K_best_so_far': p.K_best_so_far,
            'D_best_so_far': p.D_best_so_far,
            'is_K_BKS': p.is_K_BKS
        } for p in self.convergence_trace]
        
        df = pd.DataFrame(data)
        output_path = self.results_dir / "convergence_trace.csv"
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved convergence_trace.csv: {len(df)} rows")
    
    def save_session_summary(self, summary: Dict):
        """Guardar session_summary.txt"""
        output_path = self.logs_dir / "session_summary.txt"
        
        with open(output_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("SESSION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            for key, value in summary.items():
                if isinstance(value, dict):
                    f.write(f"\n{key}:\n")
                    for k, v in value.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    f.write(f"{key}: {value}\n")
        
        self.logger.info(f"Saved session_summary.txt")


class MetricsCalculator:
    """Calculador de métricas jerárquicas según especificación canónica"""
    
    def __init__(self, raw_results: List[ExecutionResult]):
        """
        Inicializar con resultados brutos
        
        Args:
            raw_results: Lista de ExecutionResult
        """
        self.raw_results = raw_results
        self.df = self._prepare_dataframe()
    
    def _prepare_dataframe(self) -> pd.DataFrame:
        """Convertir resultados a DataFrame"""
        data = []
        for r in self.raw_results:
            data.append({
                'algorithm_id': r.algorithm_id,
                'instance_id': r.instance_id,
                'family': r.family,
                'run_id': r.run_id,
                'K_final': r.K_final,
                'D_final': r.D_final,
                'K_BKS': r.K_BKS,
                'D_BKS': r.D_BKS,
                'gap_percent': r.gap_percent,
                'total_time_sec': r.total_time_sec,
                'reached_K_BKS': r.reached_K_BKS
            })
        return pd.DataFrame(data)
    
    def calculate_k_metrics(self, algorithm_id: str, instance_id: str) -> Dict:
        """
        Calcular métricas primarias de K para algoritmo x instancia
        
        Métrica: K_best, K_mean, K_std, percent_runs_K_min
        """
        subset = self.df[(self.df['algorithm_id'] == algorithm_id) & 
                         (self.df['instance_id'] == instance_id)]
        
        if subset.empty:
            return {}
        
        K_values = subset['K_final'].values
        K_BKS = subset['K_BKS'].iloc[0]
        
        K_best = K_values.min()
        K_mean = K_values.mean()
        K_std = K_values.std()
        K_min = K_values.min()
        K_max = K_values.max()
        
        # Porcentaje de ejecuciones que alcanzan K_min
        percent_runs_K_min = (K_values == K_min).sum() / len(K_values) * 100 if len(K_values) > 0 else 0
        
        return {
            'K_best': int(K_best),
            'K_mean': float(K_mean),
            'K_std': float(K_std),
            'K_min': int(K_min),
            'K_max': int(K_max),
            'percent_runs_K_min': float(percent_runs_K_min),
            'K_BKS': int(K_BKS),
            'reached_K_BKS': (K_min == K_BKS)
        }
    
    def calculate_d_metrics(self, algorithm_id: str, instance_id: str) -> Dict:
        """
        Calcular métricas secundarias de D (solo si K == K_BKS)
        
        Métrica: D_mean_at_K_min, D_std_at_K_min, gap_percent_mean, gap_percent_std
        """
        subset = self.df[(self.df['algorithm_id'] == algorithm_id) & 
                         (self.df['instance_id'] == instance_id)]
        
        if subset.empty:
            return {}
        
        # Filtrar solo ejecuciones donde K_final == K_BKS (reached K optimally)
        reached_bks = subset[subset['reached_K_BKS']]
        
        if reached_bks.empty:
            return {'D_mean_at_K_min': None, 'D_std_at_K_min': None,
                    'gap_percent_mean': None, 'gap_percent_std': None}
        
        D_values = reached_bks['D_final'].values
        gap_values = reached_bks['gap_percent'].values
        
        return {
            'D_mean_at_K_min': float(D_values.mean()),
            'D_std_at_K_min': float(D_values.std()),
            'gap_percent_mean': float(gap_values.mean()) if len(gap_values) > 0 else None,
            'gap_percent_std': float(gap_values.std()) if len(gap_values) > 0 else None
        }
    
    def calculate_summary_by_instance(self) -> pd.DataFrame:
        """
        Crear summary_by_instance.csv
        Una fila = (Algoritmo × Instancia)
        """
        rows = []
        
        for algo_id in self.df['algorithm_id'].unique():
            for inst_id in self.df['instance_id'].unique():
                subset = self.df[(self.df['algorithm_id'] == algo_id) & 
                                (self.df['instance_id'] == inst_id)]
                
                if subset.empty:
                    continue
                
                family = subset['family'].iloc[0]
                k_metrics = self.calculate_k_metrics(algo_id, inst_id)
                d_metrics = self.calculate_d_metrics(algo_id, inst_id)
                
                row = {
                    'algorithm_id': algo_id,
                    'instance_id': inst_id,
                    'family': family,
                    'runs_total': len(subset),
                    **k_metrics,
                    **d_metrics,
                    'time_mean_sec': float(subset['total_time_sec'].mean())
                }
                rows.append(row)
        
        return pd.DataFrame(rows)
    
    def calculate_summary_by_family(self) -> pd.DataFrame:
        """
        Crear summary_by_family.csv
        Una fila = (Algoritmo × Familia)
        """
        rows = []
        
        for algo_id in self.df['algorithm_id'].unique():
            for family in self.df['family'].unique():
                subset = self.df[(self.df['algorithm_id'] == algo_id) & 
                                (self.df['family'] == family)]
                
                if subset.empty:
                    continue
                
                # Instancias únicas en la familia
                instances_count = subset['instance_id'].nunique()
                
                # K_mean: promedio de K_final en toda la familia
                K_mean = subset['K_final'].mean()
                
                # %Instancias_K_BKS: proporción de instancias que alcanzan K_BKS (en su mejor ejecución)
                instances_reaching_bks = 0
                for inst_id in subset['instance_id'].unique():
                    inst_subset = subset[subset['instance_id'] == inst_id]
                    K_min = inst_subset['K_final'].min()
                    K_BKS = inst_subset['K_BKS'].iloc[0]
                    if K_min == K_BKS:
                        instances_reaching_bks += 1
                
                percent_instances_K_BKS = (instances_reaching_bks / instances_count * 100) if instances_count > 0 else 0
                
                # gap_percent_mean: solo para ejecuciones donde K == K_BKS
                reached_bks = subset[subset['reached_K_BKS']]
                gap_percent_mean = reached_bks['gap_percent'].mean() if len(reached_bks) > 0 else None
                gap_percent_std = reached_bks['gap_percent'].std() if len(reached_bks) > 0 else None
                
                # time_mean_sec
                time_mean = subset['total_time_sec'].mean()
                
                row = {
                    'algorithm_id': algo_id,
                    'family': family,
                    'instances_count': instances_count,
                    'K_mean': float(K_mean),
                    'percent_instances_K_BKS': float(percent_instances_K_BKS),
                    'gap_percent_mean': gap_percent_mean,
                    'gap_percent_std': gap_percent_std,
                    'time_mean_sec': float(time_mean)
                }
                rows.append(row)
        
        return pd.DataFrame(rows)


# Tests pueden usar estas clases
if __name__ == "__main__":
    # Ejemplo de uso
    mgr = OutputManager()
    print(f"OutputManager initialized at: {mgr.execution_dir}")
    print(f"Directories created: {list(mgr.results_dir.parent.glob('*'))}")
