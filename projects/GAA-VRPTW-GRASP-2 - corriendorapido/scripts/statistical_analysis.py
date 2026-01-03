"""
Phase 10: Statistical Analysis Framework for VRPTW Algorithm Evaluation

Responsabilidades:
1. Estadísticas descriptivas por algoritmo (K, D, %GAP)
2. Tests estadísticos (Kruskal-Wallis, Wilcoxon)
3. Tamaño del efecto (Cohen's d)
4. Análisis por familia Solomon (C, R, RC)
5. Análisis de convergencia (tiempo a K_BKS)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from scipy import stats


@dataclass
class DescriptiveStats:
    """Estadísticas descriptivas para una métrica"""
    mean: float
    std: float
    min: float
    max: float
    median: float
    q25: float
    q75: float
    count: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'mean': round(self.mean, 4),
            'std': round(self.std, 4),
            'min': round(self.min, 4),
            'max': round(self.max, 4),
            'median': round(self.median, 4),
            'q25': round(self.q25, 4),
            'q75': round(self.q75, 4),
            'count': self.count
        }


@dataclass
class StatisticalTestResult:
    """Resultado de un test estadístico"""
    test_name: str
    statistic: float
    p_value: float
    significant: bool  # p_value < 0.05
    alpha: float = 0.05
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'test': self.test_name,
            'statistic': round(self.statistic, 4),
            'p_value': round(self.p_value, 6),
            'significant': self.significant,
            'alpha': self.alpha
        }


class DescriptiveAnalysis:
    """Análisis descriptivo de resultados experimentales"""
    
    @staticmethod
    def calculate_stats(data: np.ndarray) -> DescriptiveStats:
        """
        Calcula estadísticas descriptivas de un array
        
        Args:
            data: numpy array con valores
            
        Returns:
            DescriptiveStats dataclass
        """
        data_clean = data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            raise ValueError("No valid data to analyze")
        
        return DescriptiveStats(
            mean=float(np.mean(data_clean)),
            std=float(np.std(data_clean, ddof=1) if len(data_clean) > 1 else 0),
            min=float(np.min(data_clean)),
            max=float(np.max(data_clean)),
            median=float(np.median(data_clean)),
            q25=float(np.percentile(data_clean, 25)),
            q75=float(np.percentile(data_clean, 75)),
            count=len(data_clean)
        )
    
    @staticmethod
    def analyze_by_algorithm(results_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analiza resultados agrupados por algoritmo
        
        Args:
            results_df: DataFrame con columnas algorithm_id, K_final, D_final, gap_percent
            
        Returns:
            Dict con estadísticas por algoritmo
        """
        analysis = {}
        
        for algo in results_df['algorithm_id'].unique():
            algo_data = results_df[results_df['algorithm_id'] == algo]
            
            analysis[algo] = {
                'K_stats': DescriptiveAnalysis.calculate_stats(
                    algo_data['K_final'].values
                ),
                'D_stats': DescriptiveAnalysis.calculate_stats(
                    algo_data['D_final'].values
                ),
                'gap_stats': DescriptiveAnalysis.calculate_stats(
                    algo_data['gap_percent'].values
                ),
                'K_BKS_reached': int((algo_data['reached_K_BKS'] == True).sum()),
                'total_runs': len(algo_data)
            }
        
        return analysis
    
    @staticmethod
    def analyze_by_family(results_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analiza resultados agrupados por familia Solomon
        
        Args:
            results_df: DataFrame con columna 'family'
            
        Returns:
            Dict con estadísticas por familia
        """
        analysis = {}
        
        for family in sorted(results_df['family'].unique()):
            family_data = results_df[results_df['family'] == family]
            
            analysis[family] = {
                'K_stats': DescriptiveAnalysis.calculate_stats(
                    family_data['K_final'].values
                ),
                'D_stats': DescriptiveAnalysis.calculate_stats(
                    family_data['D_final'].values
                ),
                'gap_stats': DescriptiveAnalysis.calculate_stats(
                    family_data['gap_percent'].values
                ),
                'instance_count': family_data['instance_id'].nunique(),
                'total_runs': len(family_data)
            }
        
        return analysis
    
    @staticmethod
    def analyze_by_algorithm_and_family(results_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analiza resultados por combinación algoritmo-familia
        
        Args:
            results_df: DataFrame con algoritmo y familia
            
        Returns:
            Dict[algorithm][family] = estadísticas
        """
        analysis = {}
        
        for algo in results_df['algorithm_id'].unique():
            analysis[algo] = {}
            algo_data = results_df[results_df['algorithm_id'] == algo]
            
            for family in sorted(algo_data['family'].unique()):
                family_algo_data = algo_data[algo_data['family'] == family]
                
                analysis[algo][family] = {
                    'K_stats': DescriptiveAnalysis.calculate_stats(
                        family_algo_data['K_final'].values
                    ),
                    'D_stats': DescriptiveAnalysis.calculate_stats(
                        family_algo_data['D_final'].values
                    ),
                    'gap_stats': DescriptiveAnalysis.calculate_stats(
                        family_algo_data['gap_percent'].values
                    ),
                    'runs': len(family_algo_data)
                }
        
        return analysis


class StatisticalTests:
    """Tests estadísticos para comparación de algoritmos"""
    
    @staticmethod
    def kruskal_wallis(results_df: pd.DataFrame, metric: str = 'K_final') -> StatisticalTestResult:
        """
        Test Kruskal-Wallis (comparación múltiple no paramétrica)
        
        H0: Los algoritmos tienen la misma distribución
        
        Args:
            results_df: DataFrame con resultados
            metric: Métrica a comparar ('K_final', 'D_final', 'gap_percent')
            
        Returns:
            StatisticalTestResult
        """
        groups = [group[metric].dropna().values 
                 for algo, group in results_df.groupby('algorithm_id')]
        
        stat, p_value = stats.kruskal(*groups)
        
        return StatisticalTestResult(
            test_name='Kruskal-Wallis',
            statistic=float(stat),
            p_value=float(p_value),
            significant=float(p_value) < 0.05
        )
    
    @staticmethod
    def wilcoxon_pairwise(results_df: pd.DataFrame, metric: str = 'K_final') -> Dict:
        """
        Test Wilcoxon pareado (comparación entre pares de algoritmos)
        
        Args:
            results_df: DataFrame con resultados
            metric: Métrica a comparar
            
        Returns:
            Dict[algo1_vs_algo2] = StatisticalTestResult
        """
        algorithms = sorted(results_df['algorithm_id'].unique())
        results = {}
        
        for i, algo1 in enumerate(algorithms):
            for algo2 in algorithms[i+1:]:
                data1 = results_df[results_df['algorithm_id'] == algo1][metric].dropna().values
                data2 = results_df[results_df['algorithm_id'] == algo2][metric].dropna().values
                
                # Emparejar por instancia si es posible
                if len(data1) == len(data2):
                    stat, p_value = stats.wilcoxon(data1, data2)
                else:
                    # Si no son pareados, usar Mann-Whitney U como alternativa
                    stat, p_value = stats.mannwhitneyu(data1, data2)
                
                key = f"{algo1} vs {algo2}"
                results[key] = StatisticalTestResult(
                    test_name='Wilcoxon/Mann-Whitney U',
                    statistic=float(stat),
                    p_value=float(p_value),
                    significant=float(p_value) < 0.05
                )
        
        return results
    
    @staticmethod
    def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
        """
        Calcula Cohen's d (tamaño del efecto)
        
        Interpretación:
        - d < 0.2: efecto negligible
        - 0.2 <= d < 0.5: efecto pequeño
        - 0.5 <= d < 0.8: efecto medio
        - d >= 0.8: efecto grande
        
        Args:
            group1: array con valores grupo 1
            group2: array con valores grupo 2
            
        Returns:
            float: Cohen's d
        """
        group1_clean = group1[~np.isnan(group1)]
        group2_clean = group2[~np.isnan(group2)]
        
        if len(group1_clean) == 0 or len(group2_clean) == 0:
            return np.nan
        
        mean1 = np.mean(group1_clean)
        mean2 = np.mean(group2_clean)
        std1 = np.std(group1_clean, ddof=1)
        std2 = np.std(group2_clean, ddof=1)
        
        # Pooled standard deviation
        n1, n2 = len(group1_clean), len(group2_clean)
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        d = (mean1 - mean2) / pooled_std
        return float(d)
    
    @staticmethod
    def pairwise_effect_sizes(results_df: pd.DataFrame, metric: str = 'K_final') -> Dict:
        """
        Calcula Cohen's d para todos los pares de algoritmos
        
        Args:
            results_df: DataFrame con resultados
            metric: Métrica a comparar
            
        Returns:
            Dict[algo1_vs_algo2] = Cohen's d
        """
        algorithms = sorted(results_df['algorithm_id'].unique())
        effect_sizes = {}
        
        for i, algo1 in enumerate(algorithms):
            for algo2 in algorithms[i+1:]:
                data1 = results_df[results_df['algorithm_id'] == algo1][metric].values
                data2 = results_df[results_df['algorithm_id'] == algo2][metric].values
                
                d = StatisticalTests.cohens_d(data1, data2)
                key = f"{algo1} vs {algo2}"
                effect_sizes[key] = {
                    'cohens_d': round(d, 4),
                    'interpretation': StatisticalTests._interpret_cohens_d(d)
                }
        
        return effect_sizes
    
    @staticmethod
    def _interpret_cohens_d(d: float) -> str:
        """Interpreta tamaño del efecto Cohen's d"""
        d_abs = abs(d)
        if d_abs < 0.2:
            return "negligible"
        elif d_abs < 0.5:
            return "small"
        elif d_abs < 0.8:
            return "medium"
        else:
            return "large"


class ConvergenceAnalysis:
    """Análisis de convergencia hacia K_BKS"""
    
    @staticmethod
    def time_to_k_bks(results_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Tiempo promedio (segundos) para alcanzar K_BKS por algoritmo
        
        Args:
            results_df: DataFrame con columnas algorithm_id, K_final, K_BKS, total_time_sec
            
        Returns:
            Dict[algorithm] = {'mean_time': float, 'success_rate': float}
        """
        analysis = {}
        
        for algo in results_df['algorithm_id'].unique():
            algo_data = results_df[results_df['algorithm_id'] == algo]
            
            # Instancias donde K_final == K_BKS
            successful = algo_data[algo_data['K_final'] == algo_data['K_BKS']]
            
            if len(successful) > 0:
                mean_time = successful['total_time_sec'].mean()
                success_rate = len(successful) / len(algo_data)
            else:
                mean_time = np.nan
                success_rate = 0.0
            
            analysis[algo] = {
                'mean_time_sec': round(float(mean_time), 4),
                'success_rate': round(float(success_rate), 4),
                'successful_runs': len(successful),
                'total_runs': len(algo_data)
            }
        
        return analysis
    
    @staticmethod
    def iterations_to_k_bks(results_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Iteraciones promedio para alcanzar K_BKS por algoritmo
        
        Args:
            results_df: DataFrame con columnas algorithm_id, K_final, K_BKS, iterations_executed
            
        Returns:
            Dict[algorithm] = {'mean_iterations': float, 'success_rate': float}
        """
        analysis = {}
        
        for algo in results_df['algorithm_id'].unique():
            algo_data = results_df[results_df['algorithm_id'] == algo]
            
            # Instancias donde K_final == K_BKS
            successful = algo_data[algo_data['K_final'] == algo_data['K_BKS']]
            
            if len(successful) > 0:
                mean_iter = successful['iterations_executed'].mean()
                success_rate = len(successful) / len(algo_data)
            else:
                mean_iter = np.nan
                success_rate = 0.0
            
            analysis[algo] = {
                'mean_iterations': round(float(mean_iter), 2),
                'success_rate': round(float(success_rate), 4),
                'successful_runs': len(successful),
                'total_runs': len(algo_data)
            }
        
        return analysis


class StatisticalAnalysisReport:
    """Genera reportes completos de análisis estadístico"""
    
    def __init__(self, results_csv_path: str):
        """
        Inicializa el reporte con resultados experimentales
        
        Args:
            results_csv_path: Ruta a raw_results.csv
        """
        self.results_df = pd.read_csv(results_csv_path)
        self.analysis_results = {}
    
    def run_full_analysis(self) -> Dict:
        """
        Ejecuta análisis estadístico completo
        
        Returns:
            Dict con todos los resultados
        """
        self.analysis_results = {
            'descriptive_by_algorithm': DescriptiveAnalysis.analyze_by_algorithm(
                self.results_df
            ),
            'descriptive_by_family': DescriptiveAnalysis.analyze_by_family(
                self.results_df
            ),
            'descriptive_by_algorithm_family': DescriptiveAnalysis.analyze_by_algorithm_and_family(
                self.results_df
            ),
            'kruskal_wallis_K': StatisticalTests.kruskal_wallis(
                self.results_df, 'K_final'
            ),
            'kruskal_wallis_gap': StatisticalTests.kruskal_wallis(
                self.results_df, 'gap_percent'
            ),
            'wilcoxon_pairwise_K': StatisticalTests.wilcoxon_pairwise(
                self.results_df, 'K_final'
            ),
            'wilcoxon_pairwise_gap': StatisticalTests.wilcoxon_pairwise(
                self.results_df, 'gap_percent'
            ),
            'effect_sizes_K': StatisticalTests.pairwise_effect_sizes(
                self.results_df, 'K_final'
            ),
            'effect_sizes_gap': StatisticalTests.pairwise_effect_sizes(
                self.results_df, 'gap_percent'
            ),
            'convergence_time': ConvergenceAnalysis.time_to_k_bks(
                self.results_df
            ),
            'convergence_iterations': ConvergenceAnalysis.iterations_to_k_bks(
                self.results_df
            )
        }
        
        return self.analysis_results
    
    def get_summary(self) -> Dict:
        """
        Retorna resumen ejecutivo
        
        Returns:
            Dict con métricas clave
        """
        if not self.analysis_results:
            self.run_full_analysis()
        
        # Mejores algoritmos
        by_algo = self.analysis_results['descriptive_by_algorithm']
        best_K_algo = min(
            by_algo.items(),
            key=lambda x: x[1]['K_stats'].mean
        )[0]
        best_gap_algo = min(
            (x for x in by_algo.items() if not np.isnan(x[1]['gap_stats'].mean)),
            key=lambda x: x[1]['gap_stats'].mean,
            default=(None, None)
        )[0]
        
        return {
            'total_experiments': len(self.results_df),
            'algorithms': self.results_df['algorithm_id'].nunique(),
            'families': self.results_df['family'].nunique(),
            'instances': self.results_df['instance_id'].nunique(),
            'best_by_K': best_K_algo,
            'best_by_gap': best_gap_algo,
            'kruskal_wallis_K_significant': self.analysis_results['kruskal_wallis_K'].significant,
            'kruskal_wallis_gap_significant': self.analysis_results['kruskal_wallis_gap'].significant
        }


if __name__ == "__main__":
    print("Phase 10 Statistical Analysis Framework initialized")
