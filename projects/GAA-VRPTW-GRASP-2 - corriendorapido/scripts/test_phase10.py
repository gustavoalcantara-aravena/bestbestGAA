"""
Phase 10 Tests: Comprehensive validation of statistical analysis framework

Test coverage:
1. DescriptiveStats: Cálculo de media, std, min, max, quartiles
2. DescriptiveAnalysis: Análisis por algoritmo, familia, combinación
3. StatisticalTests: Kruskal-Wallis, Wilcoxon, Cohen's d
4. ConvergenceAnalysis: Tiempo e iteraciones a K_BKS
5. StatisticalAnalysisReport: Análisis completo e integración
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

from statistical_analysis import (
    DescriptiveStats,
    StatisticalTestResult,
    DescriptiveAnalysis,
    StatisticalTests,
    ConvergenceAnalysis,
    StatisticalAnalysisReport
)


class TestDescriptiveStats:
    """Test DescriptiveStats dataclass"""
    
    def test_descriptive_stats_creation(self):
        """Test creating DescriptiveStats"""
        stats = DescriptiveStats(
            mean=10.5,
            std=2.3,
            min=5.0,
            max=15.0,
            median=10.0,
            q25=8.0,
            q75=12.0,
            count=100
        )
        
        assert stats.mean == 10.5
        assert stats.count == 100
    
    def test_descriptive_stats_to_dict(self):
        """Test converting DescriptiveStats to dict"""
        stats = DescriptiveStats(
            mean=10.5,
            std=2.3,
            min=5.0,
            max=15.0,
            median=10.0,
            q25=8.0,
            q75=12.0,
            count=100
        )
        
        result = stats.to_dict()
        assert isinstance(result, dict)
        assert result['mean'] == 10.5
        assert result['count'] == 100


class TestStatisticalTestResult:
    """Test StatisticalTestResult dataclass"""
    
    def test_test_result_significant(self):
        """Test significant result (p < 0.05)"""
        result = StatisticalTestResult(
            test_name='Kruskal-Wallis',
            statistic=12.34,
            p_value=0.03,
            significant=True
        )
        
        assert result.significant == True
        assert result.p_value == 0.03
    
    def test_test_result_not_significant(self):
        """Test non-significant result (p >= 0.05)"""
        result = StatisticalTestResult(
            test_name='Kruskal-Wallis',
            statistic=5.6,
            p_value=0.15,
            significant=False
        )
        
        assert result.significant == False


class TestDescriptiveAnalysisCalculateStats:
    """Test DescriptiveAnalysis.calculate_stats()"""
    
    def test_calculate_stats_basic(self):
        """Test basic statistics calculation"""
        data = np.array([1, 2, 3, 4, 5])
        
        stats = DescriptiveAnalysis.calculate_stats(data)
        
        assert stats.mean == 3.0
        assert stats.min == 1.0
        assert stats.max == 5.0
        assert stats.median == 3.0
        assert stats.count == 5
    
    def test_calculate_stats_with_nan(self):
        """Test statistics calculation with NaN values"""
        data = np.array([1, 2, np.nan, 4, 5])
        
        stats = DescriptiveAnalysis.calculate_stats(data)
        
        assert stats.count == 4  # NaN excluded
        assert stats.mean == 3.0  # (1+2+4+5)/4
    
    def test_calculate_stats_all_nan(self):
        """Test error when all values are NaN"""
        data = np.array([np.nan, np.nan, np.nan])
        
        with pytest.raises(ValueError, match="No valid data"):
            DescriptiveAnalysis.calculate_stats(data)
    
    def test_calculate_stats_quartiles(self):
        """Test quartile calculation"""
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        stats = DescriptiveAnalysis.calculate_stats(data)
        
        assert 2.0 <= stats.q25 <= 3.5  # Q1 approximately
        assert 7.0 <= stats.q75 <= 8.5  # Q3 approximately


class TestDescriptiveAnalysisByAlgorithm:
    """Test DescriptiveAnalysis.analyze_by_algorithm()"""
    
    @pytest.fixture
    def sample_results(self):
        """Create sample results DataFrame"""
        data = {
            'algorithm_id': ['Algo1']*5 + ['Algo2']*5,
            'K_final': [10, 10, 11, 10, 10, 10, 10, 11, 11, 10],
            'D_final': [1100, 1150, 1200, 1100, 1100, 1050, 1100, 1250, 1300, 1100],
            'gap_percent': [0.5, 1.0, np.nan, 0.3, 0.2, 0.0, 0.5, np.nan, np.nan, 0.3],
            'reached_K_BKS': [True, True, False, True, True, True, True, False, False, True]
        }
        return pd.DataFrame(data)
    
    def test_analyze_by_algorithm(self, sample_results):
        """Test algorithm-level analysis"""
        analysis = DescriptiveAnalysis.analyze_by_algorithm(sample_results)
        
        assert 'Algo1' in analysis
        assert 'Algo2' in analysis
        assert 'K_stats' in analysis['Algo1']
        assert 'gap_stats' in analysis['Algo1']
    
    def test_k_bks_reached_counting(self, sample_results):
        """Test K_BKS reached counting"""
        analysis = DescriptiveAnalysis.analyze_by_algorithm(sample_results)
        
        # Algo1: 4/5 reached K_BKS
        assert analysis['Algo1']['K_BKS_reached'] == 4
        # Algo2: 3/5 reached K_BKS (only first two and last one)
        assert analysis['Algo2']['K_BKS_reached'] == 3


class TestDescriptiveAnalysisByFamily:
    """Test DescriptiveAnalysis.analyze_by_family()"""
    
    @pytest.fixture
    def sample_results_family(self):
        """Create sample results with families"""
        data = {
            'family': ['R1']*3 + ['C1']*3,
            'K_final': [10, 10, 11, 9, 9, 10],
            'D_final': [1100, 1150, 1200, 950, 1000, 1050],
            'gap_percent': [0.5, 1.0, np.nan, 0.2, 0.3, 0.1],
            'instance_id': ['R101', 'R102', 'R103', 'C101', 'C102', 'C103']
        }
        return pd.DataFrame(data)
    
    def test_analyze_by_family(self, sample_results_family):
        """Test family-level analysis"""
        analysis = DescriptiveAnalysis.analyze_by_family(sample_results_family)
        
        assert 'R1' in analysis
        assert 'C1' in analysis
        assert analysis['R1']['instance_count'] == 3
        assert analysis['C1']['instance_count'] == 3
    
    def test_family_instance_count(self, sample_results_family):
        """Test instance count per family"""
        analysis = DescriptiveAnalysis.analyze_by_family(sample_results_family)
        
        assert analysis['R1']['instance_count'] == 3
        assert analysis['C1']['instance_count'] == 3


class TestKruskalWallis:
    """Test Kruskal-Wallis test implementation"""
    
    @pytest.fixture
    def sample_results_kw(self):
        """Create sample results for Kruskal-Wallis"""
        np.random.seed(42)
        data = {
            'algorithm_id': ['Algo1']*20 + ['Algo2']*20 + ['Algo3']*20,
            'K_final': np.concatenate([
                np.random.normal(10, 1, 20),
                np.random.normal(11, 1, 20),
                np.random.normal(10.5, 1, 20)
            ])
        }
        return pd.DataFrame(data)
    
    def test_kruskal_wallis_returns_result(self, sample_results_kw):
        """Test Kruskal-Wallis returns StatisticalTestResult"""
        result = StatisticalTests.kruskal_wallis(sample_results_kw, 'K_final')
        
        assert isinstance(result, StatisticalTestResult)
        assert result.test_name == 'Kruskal-Wallis'
        assert result.p_value >= 0
        assert result.p_value <= 1
    
    def test_kruskal_wallis_alpha(self, sample_results_kw):
        """Test Kruskal-Wallis alpha=0.05"""
        result = StatisticalTests.kruskal_wallis(sample_results_kw, 'K_final')
        
        assert result.alpha == 0.05
        assert isinstance(result.significant, bool)


class TestWilcoxonPairwise:
    """Test Wilcoxon pairwise test"""
    
    @pytest.fixture
    def sample_results_wilcoxon(self):
        """Create sample results for Wilcoxon"""
        np.random.seed(42)
        data = {
            'algorithm_id': ['Algo1']*15 + ['Algo2']*15 + ['Algo3']*15,
            'K_final': np.concatenate([
                np.random.normal(10, 0.5, 15),
                np.random.normal(10.2, 0.5, 15),
                np.random.normal(9.8, 0.5, 15)
            ])
        }
        return pd.DataFrame(data)
    
    def test_wilcoxon_pairwise_returns_dict(self, sample_results_wilcoxon):
        """Test Wilcoxon returns dict of comparisons"""
        result = StatisticalTests.wilcoxon_pairwise(sample_results_wilcoxon, 'K_final')
        
        assert isinstance(result, dict)
        assert len(result) == 3  # 3 combinations: Algo1 vs 2,3 and Algo2 vs 3
        
        # Check all keys are pairs
        for key in result.keys():
            assert 'vs' in key


class TestCohensD:
    """Test Cohen's d effect size calculation"""
    
    def test_cohens_d_no_difference(self):
        """Test Cohen's d when groups are identical"""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([1, 2, 3, 4, 5])
        
        d = StatisticalTests.cohens_d(group1, group2)
        
        assert d == 0.0
    
    def test_cohens_d_small_difference(self):
        """Test Cohen's d with small difference"""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([2, 3, 4, 5, 6])  # Shifted by 1
        
        d = StatisticalTests.cohens_d(group1, group2)
        
        # Should be small effect
        assert 0.2 <= abs(d) < 0.8
    
    def test_cohens_d_with_nan(self):
        """Test Cohen's d handles NaN values"""
        group1 = np.array([1, 2, np.nan, 4, 5])
        group2 = np.array([2, 3, 4, 5, 6])
        
        d = StatisticalTests.cohens_d(group1, group2)
        
        assert not np.isnan(d)
    
    def test_cohens_d_interpretation(self):
        """Test Cohen's d interpretation"""
        # Negligible
        assert StatisticalTests._interpret_cohens_d(0.1) == "negligible"
        # Small
        assert StatisticalTests._interpret_cohens_d(0.3) == "small"
        # Medium
        assert StatisticalTests._interpret_cohens_d(0.6) == "medium"
        # Large
        assert StatisticalTests._interpret_cohens_d(0.9) == "large"


class TestPairwiseEffectSizes:
    """Test pairwise Cohen's d calculations"""
    
    @pytest.fixture
    def sample_results_effect(self):
        """Create sample results for effect sizes"""
        np.random.seed(42)
        data = {
            'algorithm_id': ['Algo1']*10 + ['Algo2']*10,
            'K_final': np.concatenate([
                np.random.normal(10, 1, 10),
                np.random.normal(10.5, 1, 10)
            ])
        }
        return pd.DataFrame(data)
    
    def test_pairwise_effect_sizes(self, sample_results_effect):
        """Test pairwise effect sizes calculation"""
        effect_sizes = StatisticalTests.pairwise_effect_sizes(
            sample_results_effect, 'K_final'
        )
        
        assert isinstance(effect_sizes, dict)
        assert len(effect_sizes) >= 1
        
        for key, value in effect_sizes.items():
            assert 'cohens_d' in value
            assert 'interpretation' in value
            assert value['interpretation'] in ['negligible', 'small', 'medium', 'large']


class TestConvergenceTime:
    """Test ConvergenceAnalysis.time_to_k_bks()"""
    
    @pytest.fixture
    def sample_convergence_data(self):
        """Create sample convergence data"""
        data = {
            'algorithm_id': ['Algo1']*6 + ['Algo2']*6,
            'K_final': [10, 10, 11, 10, 10, 10, 10, 10, 11, 11, 10, 10],
            'K_BKS': [10]*12,
            'total_time_sec': [5.2, 5.1, 6.3, 5.0, 5.3, 5.1, 5.8, 5.9, 7.0, 7.2, 5.5, 5.4]
        }
        return pd.DataFrame(data)
    
    def test_time_to_k_bks(self, sample_convergence_data):
        """Test time to K_BKS calculation"""
        analysis = ConvergenceAnalysis.time_to_k_bks(sample_convergence_data)
        
        assert 'Algo1' in analysis
        assert 'Algo2' in analysis
        assert 'mean_time_sec' in analysis['Algo1']
        assert 'success_rate' in analysis['Algo1']
    
    def test_success_rate_calculation(self, sample_convergence_data):
        """Test success rate calculation"""
        analysis = ConvergenceAnalysis.time_to_k_bks(sample_convergence_data)
        
        # Algo1: 5/6 reached K_BKS
        assert analysis['Algo1']['success_rate'] == pytest.approx(5/6, rel=0.01)
        # Algo2: 4/6 reached K_BKS
        assert analysis['Algo2']['success_rate'] == pytest.approx(4/6, rel=0.01)


class TestConvergenceIterations:
    """Test ConvergenceAnalysis.iterations_to_k_bks()"""
    
    @pytest.fixture
    def sample_iterations_data(self):
        """Create sample iterations data"""
        data = {
            'algorithm_id': ['Algo1']*6 + ['Algo2']*6,
            'K_final': [10, 10, 11, 10, 10, 10, 10, 10, 11, 11, 10, 10],
            'K_BKS': [10]*12,
            'iterations_executed': [95, 98, 100, 92, 100, 96, 100, 100, 100, 100, 95, 98]
        }
        return pd.DataFrame(data)
    
    def test_iterations_to_k_bks(self, sample_iterations_data):
        """Test iterations to K_BKS calculation"""
        analysis = ConvergenceAnalysis.iterations_to_k_bks(sample_iterations_data)
        
        assert 'Algo1' in analysis
        assert 'mean_iterations' in analysis['Algo1']
        assert analysis['Algo1']['mean_iterations'] > 0


class TestStatisticalAnalysisReport:
    """Test StatisticalAnalysisReport integration"""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create sample CSV results file"""
        data = {
            'algorithm_id': ['Algo1']*10 + ['Algo2']*10 + ['Algo3']*10,
            'instance_id': ['R101', 'R102', 'R103', 'C101', 'C102', 'R104', 'R105', 'R106', 'R107', 'R108'] * 3,
            'family': ['R1', 'R1', 'R1', 'C1', 'C1', 'R1', 'R1', 'R1', 'R1', 'R1'] * 3,
            'K_final': np.random.randint(9, 12, 30),
            'D_final': np.random.uniform(1000, 1500, 30),
            'K_BKS': [10]*30,
            'D_BKS': np.random.uniform(950, 1450, 30),
            'gap_percent': np.random.uniform(0, 5, 30),
            'total_time_sec': np.random.uniform(3, 10, 30),
            'iterations_executed': np.random.randint(50, 200, 30),
            'reached_K_BKS': np.random.choice([True, False], 30)
        }
        df = pd.DataFrame(data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_path = f.name
        
        yield csv_path
        
        # Cleanup
        Path(csv_path).unlink()
    
    def test_report_initialization(self, sample_csv_file):
        """Test report initialization"""
        report = StatisticalAnalysisReport(sample_csv_file)
        
        assert report.results_df is not None
        assert len(report.results_df) == 30
    
    def test_run_full_analysis(self, sample_csv_file):
        """Test running full analysis"""
        report = StatisticalAnalysisReport(sample_csv_file)
        results = report.run_full_analysis()
        
        assert 'descriptive_by_algorithm' in results
        assert 'kruskal_wallis_K' in results
        assert 'effect_sizes_K' in results
        assert 'convergence_time' in results
    
    def test_get_summary(self, sample_csv_file):
        """Test summary generation"""
        report = StatisticalAnalysisReport(sample_csv_file)
        summary = report.get_summary()
        
        assert summary['total_experiments'] == 30
        assert summary['algorithms'] == 3
        assert summary['families'] >= 1
        assert 'best_by_K' in summary
        assert 'kruskal_wallis_K_significant' in summary


class TestPhase10Integration:
    """Integration tests for Phase 10"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        # Create sample data
        np.random.seed(42)
        data = {
            'algorithm_id': ['Algo1']*15 + ['Algo2']*15,
            'instance_id': list(range(1, 16)) * 2,
            'family': (['R1']*5 + ['C1']*5 + ['RC1']*5) * 2,
            'K_final': np.concatenate([
                np.random.randint(9, 11, 15),
                np.random.randint(9, 12, 15)
            ]),
            'D_final': np.random.uniform(1000, 1500, 30),
            'K_BKS': [10]*30,
            'D_BKS': np.random.uniform(950, 1450, 30),
            'gap_percent': np.random.uniform(0, 5, 30),
            'total_time_sec': np.random.uniform(3, 10, 30),
            'iterations_executed': np.random.randint(50, 200, 30),
            'reached_K_BKS': np.random.choice([True, False], 30)
        }
        df = pd.DataFrame(data)
        
        # Save to temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_path = f.name
        
        try:
            # Run analysis
            report = StatisticalAnalysisReport(csv_path)
            results = report.run_full_analysis()
            summary = report.get_summary()
            
            # Verify completeness
            assert len(results) > 0
            assert summary['algorithms'] == 2
            assert summary['total_experiments'] == 30
        finally:
            Path(csv_path).unlink()
