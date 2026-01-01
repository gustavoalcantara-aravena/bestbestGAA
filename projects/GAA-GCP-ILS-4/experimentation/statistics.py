"""
experimentation/statistics.py
Análisis estadístico avanzado para comparación de algoritmos GAA

Responsabilidades:
- Estadísticas descriptivas por algoritmo
- Test de Friedman (comparación global)
- Test de Wilcoxon pareado
- Cohen's d (tamaño de efecto)
- Ranking de algoritmos
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Análisis estadístico avanzado para algoritmos GAA"""
    
    def __init__(self, alpha: float = 0.05):
        """
        Inicializa analizador estadístico
        
        Args:
            alpha: Nivel de significancia (default 0.05)
        """
        self.alpha = alpha
        self.logger = logger
    
    # ========================================================================
    # ESTADÍSTICAS DESCRIPTIVAS
    # ========================================================================
    
    def descriptive_statistics(self, data: List[float]) -> Dict[str, float]:
        """
        Calcula estadísticas descriptivas
        
        Args:
            data: Lista de valores
        
        Returns:
            Diccionario con media, std, min, max, mediana, Q1, Q3
        """
        data = np.array(data)
        
        return {
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'median': float(np.median(data)),
            'q1': float(np.percentile(data, 25)),
            'q3': float(np.percentile(data, 75)),
            'iqr': float(np.percentile(data, 75) - np.percentile(data, 25)),
            'count': len(data)
        }
    
    def confidence_interval(self, data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calcula intervalo de confianza
        
        Args:
            data: Lista de valores
            confidence: Nivel de confianza (default 0.95)
        
        Returns:
            Tupla (lower_bound, upper_bound)
        """
        data = np.array(data)
        n = len(data)
        mean = np.mean(data)
        std_err = stats.sem(data)
        
        # t-value para el nivel de confianza
        t_val = stats.t.ppf((1 + confidence) / 2, n - 1)
        margin = t_val * std_err
        
        return (float(mean - margin), float(mean + margin))
    
    # ========================================================================
    # COMPARACIÓN GLOBAL: TEST DE FRIEDMAN
    # ========================================================================
    
    def friedman_test(self, algorithm_results: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Test de Friedman para comparación global de múltiples algoritmos
        
        Args:
            algorithm_results: Dict con {nombre_algoritmo: [valores]}
        
        Returns:
            Diccionario con resultados del test
        """
        # Preparar datos: cada fila es una instancia, cada columna es un algoritmo
        algorithms = list(algorithm_results.keys())
        data_arrays = [np.array(algorithm_results[alg]) for alg in algorithms]
        
        # Asegurar que todos tienen la misma longitud
        min_len = min(len(arr) for arr in data_arrays)
        data_arrays = [arr[:min_len] for arr in data_arrays]
        
        # Realizar test de Friedman
        statistic, p_value = stats.friedmanchisquare(*data_arrays)
        
        # Calcular rankings promedio
        rankings = {}
        for i, alg in enumerate(algorithms):
            # Ranking de cada valor (1 = mejor, n = peor)
            ranks = stats.rankdata(data_arrays[i])
            rankings[alg] = float(np.mean(ranks))
        
        # Ordenar por ranking
        sorted_rankings = sorted(rankings.items(), key=lambda x: x[1])
        
        return {
            'test_name': 'Friedman',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_friedman(p_value),
            'average_rankings': rankings,
            'ranking_order': [alg for alg, _ in sorted_rankings],
            'best_algorithm': sorted_rankings[0][0] if sorted_rankings else None
        }
    
    def _interpret_friedman(self, p_value: float) -> str:
        """Interpreta resultado del test de Friedman"""
        if p_value < self.alpha:
            return f"Hay diferencias significativas entre algoritmos (p={p_value:.4f} < {self.alpha})"
        else:
            return f"No hay diferencias significativas entre algoritmos (p={p_value:.4f} >= {self.alpha})"
    
    # ========================================================================
    # COMPARACIÓN PAREADA: TEST DE WILCOXON
    # ========================================================================
    
    def wilcoxon_signed_rank_test(self, data1: List[float], data2: List[float]) -> Dict[str, Any]:
        """
        Test de Wilcoxon de rangos signados para comparación pareada
        
        Args:
            data1: Valores del algoritmo 1
            data2: Valores del algoritmo 2
        
        Returns:
            Diccionario con resultados del test
        """
        # Asegurar misma longitud
        min_len = min(len(data1), len(data2))
        data1 = np.array(data1[:min_len])
        data2 = np.array(data2[:min_len])
        
        # Test de Wilcoxon
        statistic, p_value = stats.wilcoxon(data1, data2)
        
        # Calcular diferencias
        differences = data1 - data2
        mean_diff = float(np.mean(differences))
        
        return {
            'test_name': 'Wilcoxon Signed-Rank',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_wilcoxon(p_value, mean_diff),
            'mean_difference': mean_diff,
            'median_difference': float(np.median(differences))
        }
    
    def _interpret_wilcoxon(self, p_value: float, mean_diff: float) -> str:
        """Interpreta resultado del test de Wilcoxon"""
        if p_value < self.alpha:
            if mean_diff < 0:
                return f"Algoritmo 1 es significativamente mejor (p={p_value:.4f} < {self.alpha})"
            else:
                return f"Algoritmo 2 es significativamente mejor (p={p_value:.4f} < {self.alpha})"
        else:
            return f"No hay diferencia significativa (p={p_value:.4f} >= {self.alpha})"
    
    # ========================================================================
    # TAMAÑO DE EFECTO: COHEN'S D
    # ========================================================================
    
    def effect_size_cohens_d(self, data1: List[float], data2: List[float]) -> float:
        """
        Calcula Cohen's d (tamaño de efecto)
        
        Args:
            data1: Valores del algoritmo 1
            data2: Valores del algoritmo 2
        
        Returns:
            Valor de Cohen's d
        """
        data1 = np.array(data1)
        data2 = np.array(data2)
        
        n1, n2 = len(data1), len(data2)
        var1, var2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        # Cohen's d
        cohens_d = (np.mean(data1) - np.mean(data2)) / pooled_std
        
        return float(cohens_d)
    
    def interpret_cohens_d(self, cohens_d: float) -> str:
        """Interpreta magnitud de Cohen's d"""
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "efecto pequeño"
        elif abs_d < 0.5:
            return "efecto mediano"
        elif abs_d < 0.8:
            return "efecto grande"
        else:
            return "efecto muy grande"
    
    # ========================================================================
    # COMPARACIÓN MÚLTIPLE DE ALGORITMOS
    # ========================================================================
    
    def compare_multiple_algorithms(self, 
                                   algorithm_results: Dict[str, List[float]], 
                                   test_type: str = "friedman") -> Dict[str, Any]:
        """
        Comparación completa de múltiples algoritmos
        
        Args:
            algorithm_results: Dict con {nombre_algoritmo: [valores]}
            test_type: Tipo de test ("friedman" o "kruskal")
        
        Returns:
            Diccionario con resultados completos
        """
        # Estadísticas descriptivas por algoritmo
        descriptive_stats = {}
        for alg_name, values in algorithm_results.items():
            descriptive_stats[alg_name] = self.descriptive_statistics(values)
        
        # Test global
        if test_type == "friedman":
            global_test = self.friedman_test(algorithm_results)
        else:
            global_test = self.kruskal_wallis_test(algorithm_results)
        
        # Comparaciones pareadas
        algorithms = list(algorithm_results.keys())
        pairwise_comparisons = {}
        
        for i in range(len(algorithms)):
            for j in range(i + 1, len(algorithms)):
                alg1, alg2 = algorithms[i], algorithms[j]
                key = f"{alg1}_vs_{alg2}"
                
                wilcoxon_result = self.wilcoxon_signed_rank_test(
                    algorithm_results[alg1],
                    algorithm_results[alg2]
                )
                cohens_d = self.effect_size_cohens_d(
                    algorithm_results[alg1],
                    algorithm_results[alg2]
                )
                
                pairwise_comparisons[key] = {
                    'wilcoxon': wilcoxon_result,
                    'cohens_d': cohens_d,
                    'cohens_d_interpretation': self.interpret_cohens_d(cohens_d)
                }
        
        return {
            'descriptive_statistics': descriptive_stats,
            'global_test': global_test,
            'pairwise_comparisons': pairwise_comparisons,
            'best_algorithm': global_test['best_algorithm'],
            'average_rankings': global_test['average_rankings']
        }
    
    # ========================================================================
    # TEST DE KRUSKAL-WALLIS (alternativa a Friedman)
    # ========================================================================
    
    def kruskal_wallis_test(self, algorithm_results: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Test de Kruskal-Wallis para comparación global (alternativa a Friedman)
        
        Args:
            algorithm_results: Dict con {nombre_algoritmo: [valores]}
        
        Returns:
            Diccionario con resultados del test
        """
        algorithms = list(algorithm_results.keys())
        data_arrays = [np.array(algorithm_results[alg]) for alg in algorithms]
        
        # Test de Kruskal-Wallis
        statistic, p_value = stats.kruskal(*data_arrays)
        
        # Calcular rankings promedio
        rankings = {}
        for i, alg in enumerate(algorithms):
            ranks = stats.rankdata(data_arrays[i])
            rankings[alg] = float(np.mean(ranks))
        
        sorted_rankings = sorted(rankings.items(), key=lambda x: x[1])
        
        return {
            'test_name': 'Kruskal-Wallis',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant': p_value < self.alpha,
            'interpretation': self._interpret_kruskal_wallis(p_value),
            'average_rankings': rankings,
            'ranking_order': [alg for alg, _ in sorted_rankings],
            'best_algorithm': sorted_rankings[0][0] if sorted_rankings else None
        }
    
    def _interpret_kruskal_wallis(self, p_value: float) -> str:
        """Interpreta resultado del test de Kruskal-Wallis"""
        if p_value < self.alpha:
            return f"Hay diferencias significativas entre algoritmos (p={p_value:.4f} < {self.alpha})"
        else:
            return f"No hay diferencias significativas entre algoritmos (p={p_value:.4f} >= {self.alpha})"
    
    # ========================================================================
    # GENERACIÓN DE REPORTE
    # ========================================================================
    
    def generate_comparison_report(self, 
                                  comparison_results: Dict[str, Any],
                                  algorithm_names: List[str] = None) -> str:
        """
        Genera reporte textual de comparación
        
        Args:
            comparison_results: Resultados de compare_multiple_algorithms
            algorithm_names: Nombres de algoritmos (opcional)
        
        Returns:
            String con reporte formateado
        """
        report = []
        report.append("=" * 80)
        report.append("REPORTE DE COMPARACIÓN ESTADÍSTICA DE ALGORITMOS GAA")
        report.append("=" * 80)
        report.append("")
        
        # Estadísticas descriptivas
        report.append("ESTADÍSTICAS DESCRIPTIVAS")
        report.append("-" * 80)
        for alg_name, stats_dict in comparison_results['descriptive_statistics'].items():
            report.append(f"\n{alg_name}:")
            report.append(f"  Media: {stats_dict['mean']:.4f} ± {stats_dict['std']:.4f}")
            report.append(f"  Rango: [{stats_dict['min']:.4f}, {stats_dict['max']:.4f}]")
            report.append(f"  Mediana: {stats_dict['median']:.4f}")
            report.append(f"  IQR: {stats_dict['iqr']:.4f}")
        
        report.append("\n" + "=" * 80)
        report.append("TEST GLOBAL (Friedman/Kruskal-Wallis)")
        report.append("=" * 80)
        
        global_test = comparison_results['global_test']
        report.append(f"Test: {global_test['test_name']}")
        report.append(f"Estadístico: {global_test['statistic']:.4f}")
        report.append(f"p-value: {global_test['p_value']:.4f}")
        report.append(f"Significativo: {global_test['significant']}")
        report.append(f"Interpretación: {global_test['interpretation']}")
        
        report.append("\nRankings Promedio (menor = mejor):")
        for alg, rank in sorted(global_test['average_rankings'].items(), key=lambda x: x[1]):
            report.append(f"  {rank:.2f}  {alg}")
        
        report.append(f"\n🏆 Mejor algoritmo: {global_test['best_algorithm']}")
        
        report.append("\n" + "=" * 80)
        report.append("COMPARACIONES PAREADAS (Wilcoxon + Cohen's d)")
        report.append("=" * 80)
        
        for comparison_key, comparison_data in comparison_results['pairwise_comparisons'].items():
            report.append(f"\n{comparison_key}:")
            wilcoxon = comparison_data['wilcoxon']
            report.append(f"  Wilcoxon p-value: {wilcoxon['p_value']:.4f}")
            report.append(f"  Significativo: {wilcoxon['significant']}")
            report.append(f"  Interpretación: {wilcoxon['interpretation']}")
            report.append(f"  Cohen's d: {comparison_data['cohens_d']:.3f} ({comparison_data['cohens_d_interpretation']})")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
