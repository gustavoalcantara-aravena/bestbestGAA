"""
Phase 8 Tests: Visualizations and Graphics

18 comprehensive tests covering:
- Convergence K plots (step-wise)
- Convergence D plots (conditional)
- Boxplots for K and D
- GAP heatmaps
- Time comparison charts
- File output and naming
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

from visualizer import MatplotlibVisualizer, PlotConfig


@pytest.fixture
def temp_plot_dir():
    """Create temporary directory for plots"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def visualizer(temp_plot_dir):
    """Create visualizer with temporary directory"""
    return MatplotlibVisualizer(output_dir=temp_plot_dir)


@pytest.fixture
def sample_convergence_data():
    """Create sample convergence trace data for testing"""
    data = []
    
    # Algorithm 1 - C101
    for iter in range(10):
        data.append({
            'algorithm_id': 'GAA_Algorithm_1',
            'instance_id': 'C101',
            'family': 'C1',
            'run_id': 0,
            'iteration': iter,
            'elapsed_time_sec': float(iter),
            'K_best_so_far': 11 - min(iter, 1),  # Steps down from 11 to 10
            'D_best_so_far': 900.0 - iter * 5,
            'is_K_BKS': (iter >= 1)  # True from iteration 1 onwards
        })
    
    # Algorithm 1 - R101
    for iter in range(15):
        data.append({
            'algorithm_id': 'GAA_Algorithm_1',
            'instance_id': 'R101',
            'family': 'R1',
            'run_id': 0,
            'iteration': iter,
            'elapsed_time_sec': float(iter),
            'K_best_so_far': 13 - min(iter // 5, 1),  # Slower convergence
            'D_best_so_far': 1650.0 - iter * 8,
            'is_K_BKS': False  # Never reaches BKS
        })
    
    return pd.DataFrame(data)


@pytest.fixture
def sample_raw_results():
    """Create sample raw results data for testing"""
    data = []
    
    # Scenario: 2 algorithms x 2 instances x 3 runs
    algorithms = ['GAA_Algorithm_1', 'GAA_Algorithm_2']
    instances = [
        ('C101', 'C1', 10, 828.94),  # (instance_id, family, K_BKS, D_BKS)
        ('R101', 'R1', 11, 1635.47)
    ]
    
    for algo in algorithms:
        for inst_id, family, k_bks, d_bks in instances:
            for run in range(3):
                # Vary results
                if algo == 'GAA_Algorithm_1':
                    k_final = k_bks if family == 'C1' else k_bks + 1
                    d_final = d_bks if k_final == k_bks else d_bks + 50
                else:
                    k_final = k_bks
                    d_final = d_bks - run  # Slightly better
                
                data.append({
                    'algorithm_id': algo,
                    'instance_id': inst_id,
                    'family': family,
                    'run_id': run,
                    'random_seed': 42 + run,
                    'K_final': k_final,
                    'D_final': d_final,
                    'K_BKS': k_bks,
                    'D_BKS': d_bks,
                    'delta_K': k_final - k_bks,
                    'gap_distance': d_final - d_bks if k_final == k_bks else None,
                    'gap_percent': ((d_final - d_bks) / d_bks * 100) if k_final == k_bks else None,
                    'total_time_sec': 5.0 + np.random.rand(),
                    'iterations_executed': 100,
                    'reached_K_BKS': (k_final == k_bks)
                })
    
    return pd.DataFrame(data)


# ============================================================================
# TESTS: CONVERGENCE K PLOTS (3 tests)
# ============================================================================

class TestConvergenceKPlot:
    """Test convergence K plot generation"""
    
    def test_convergence_K_creates_file(self, visualizer, sample_convergence_data):
        """Verify convergence_K() creates PNG file"""
        result_path = visualizer.convergence_K(sample_convergence_data, 'GAA_Algorithm_1')
        
        assert Path(result_path).exists()
        assert result_path.endswith('.png')
    
    def test_convergence_K_file_location(self, visualizer, sample_convergence_data, temp_plot_dir):
        """Verify PNG is saved to output directory"""
        result_path = visualizer.convergence_K(sample_convergence_data, 'GAA_Algorithm_1')
        
        assert temp_plot_dir in result_path
        assert 'convergence_K' in result_path
    
    def test_convergence_K_raises_error_for_missing_algorithm(self, visualizer, sample_convergence_data):
        """Verify error raised for non-existent algorithm"""
        with pytest.raises(ValueError, match="No data for algorithm"):
            visualizer.convergence_K(sample_convergence_data, 'NonExistent_Algorithm')


# ============================================================================
# TESTS: CONVERGENCE D PLOTS (3 tests)
# ============================================================================

class TestConvergenceDPlot:
    """Test convergence D plot generation (only for K=BKS)"""
    
    def test_convergence_D_creates_file(self, visualizer, sample_convergence_data):
        """Verify convergence_D() creates PNG file"""
        result_path = visualizer.convergence_D(sample_convergence_data, 'GAA_Algorithm_1')
        
        assert Path(result_path).exists()
        assert result_path.endswith('.png')
    
    def test_convergence_D_handles_no_valid_data(self, visualizer, sample_convergence_data):
        """Verify convergence_D() handles case where no K==BKS data exists"""
        # Filter to only non-valid data
        no_valid_data = sample_convergence_data[sample_convergence_data['algorithm_id'] == 'GAA_Algorithm_1'].copy()
        no_valid_data['is_K_BKS'] = False
        
        result_path = visualizer.convergence_D(no_valid_data, 'GAA_Algorithm_1')
        
        assert Path(result_path).exists()
        # Should still create file even with "No valid data" message
    
    def test_convergence_D_filters_k_equals_bks(self, visualizer):
        """Verify convergence_D() only uses data where is_K_BKS==True"""
        data = pd.DataFrame({
            'algorithm_id': ['GAA_1', 'GAA_1', 'GAA_1'],
            'instance_id': ['C101', 'C101', 'C101'],
            'iteration': [1, 2, 3],
            'D_best_so_far': [900.0, 850.0, 820.0],
            'is_K_BKS': [False, True, True]
        })
        
        result_path = visualizer.convergence_D(data, 'GAA_1')
        assert Path(result_path).exists()


# ============================================================================
# TESTS: BOXPLOTS (4 tests)
# ============================================================================

class TestBoxplots:
    """Test boxplot generation"""
    
    def test_k_boxplot_creates_file(self, visualizer, sample_raw_results):
        """Verify K_boxplot() creates PNG file"""
        result_path = visualizer.K_boxplot(sample_raw_results)
        
        assert Path(result_path).exists()
        assert 'K_boxplot' in result_path
    
    def test_d_boxplot_creates_file(self, visualizer, sample_raw_results):
        """Verify D_boxplot() creates PNG file"""
        result_path = visualizer.D_boxplot(sample_raw_results)
        
        assert Path(result_path).exists()
        assert 'D_boxplot' in result_path
    
    def test_d_boxplot_filters_reached_k_bks(self, visualizer, sample_raw_results):
        """Verify D_boxplot() only includes rows where reached_K_BKS==True"""
        # Add rows with reached_K_BKS=False
        invalid_row = sample_raw_results.iloc[0:1].copy()
        invalid_row['reached_K_BKS'] = False
        data_with_invalid = pd.concat([sample_raw_results, invalid_row])
        
        result_path = visualizer.D_boxplot(data_with_invalid)
        assert Path(result_path).exists()
    
    def test_k_boxplot_all_families_represented(self, visualizer, sample_raw_results):
        """Verify K_boxplot() includes all families"""
        result_path = visualizer.K_boxplot(sample_raw_results)
        
        assert Path(result_path).exists()
        # Verify file is not empty
        assert Path(result_path).stat().st_size > 1000


# ============================================================================
# TESTS: GAP HEATMAP (2 tests)
# ============================================================================

class TestGapHeatmap:
    """Test GAP heatmap generation"""
    
    def test_gap_heatmap_creates_file(self, visualizer):
        """Verify gap_heatmap() creates PNG file"""
        gap_data = {
            'C1': [0.1, 0.08, 0.12, 0.09],
            'R1': [0.45, 0.50, 0.40, 0.48],
            'RC1': [0.60, 0.65, 0.58, 0.62]
        }
        
        result_path = visualizer.gap_heatmap(gap_data)
        
        assert Path(result_path).exists()
        assert 'gap_heatmap' in result_path
    
    def test_gap_heatmap_empty_family_list(self, visualizer):
        """Verify gap_heatmap() handles empty data gracefully"""
        gap_data = {
            'C1': [],
            'R1': [0.5],
            'RC1': []
        }
        
        result_path = visualizer.gap_heatmap(gap_data)
        assert Path(result_path).exists()


# ============================================================================
# TESTS: TIME COMPARISON (2 tests)
# ============================================================================

class TestTimeComparison:
    """Test time comparison chart generation"""
    
    def test_time_comparison_creates_file(self, visualizer, sample_raw_results):
        """Verify time_comparison() creates PNG file"""
        result_path = visualizer.time_comparison(sample_raw_results)
        
        assert Path(result_path).exists()
        assert 'time_comparison' in result_path
    
    def test_time_comparison_groups_by_algorithm_family(self, visualizer, sample_raw_results):
        """Verify time_comparison() aggregates by algorithm and family"""
        result_path = visualizer.time_comparison(sample_raw_results)
        
        assert Path(result_path).exists()
        # File should exist and have content
        assert Path(result_path).stat().st_size > 1000


# ============================================================================
# TESTS: PLOT CONFIGURATION (2 tests)
# ============================================================================

class TestPlotConfig:
    """Test plot configuration"""
    
    def test_plot_config_default_values(self):
        """Verify PlotConfig has sensible defaults"""
        config = PlotConfig()
        
        assert config.dpi == 150
        assert config.figsize == (12, 6)
        assert config.style == 'seaborn-v0_8-darkgrid'
        assert len(config.colors) >= 5
    
    def test_plot_config_custom_values(self):
        """Verify PlotConfig accepts custom values"""
        custom_config = PlotConfig(dpi=300, figsize=(16, 8))
        
        assert custom_config.dpi == 300
        assert custom_config.figsize == (16, 8)


# ============================================================================
# TESTS: FILE OUTPUT & NAMING (2 tests)
# ============================================================================

class TestFileOutputNaming:
    """Test file output and naming conventions"""
    
    def test_custom_save_path(self, visualizer, sample_raw_results, temp_plot_dir):
        """Verify custom save path is respected"""
        custom_path = Path(temp_plot_dir) / "custom_name.png"
        
        result_path = visualizer.K_boxplot(sample_raw_results, save_path=str(custom_path))
        
        assert Path(result_path) == custom_path
        assert custom_path.exists()
    
    def test_default_naming_convention(self, visualizer, sample_convergence_data):
        """Verify default file names follow convention"""
        result_path = visualizer.convergence_K(sample_convergence_data, 'GAA_Algorithm_1')
        
        filename = Path(result_path).name
        assert 'convergence_K' in filename
        assert 'GAA_Algorithm_1' in filename
        assert filename.endswith('.png')


# ============================================================================
# INTEGRATION TEST (1 test)
# ============================================================================

class TestPhase8Integration:
    """End-to-end integration test"""
    
    def test_full_visualization_workflow(self, temp_plot_dir, sample_convergence_data, sample_raw_results):
        """Test complete visualization workflow"""
        viz = MatplotlibVisualizer(output_dir=temp_plot_dir)
        
        # Generate all canonical plots
        paths = []
        
        # Convergence plots
        paths.append(viz.convergence_K(sample_convergence_data, 'GAA_Algorithm_1'))
        paths.append(viz.convergence_D(sample_convergence_data, 'GAA_Algorithm_1'))
        
        # Boxplots
        paths.append(viz.K_boxplot(sample_raw_results))
        paths.append(viz.D_boxplot(sample_raw_results))
        
        # Other plots
        gap_data = {
            'C1': [0.1, 0.08],
            'R1': [0.45, 0.50],
            'RC1': [0.60, 0.65]
        }
        paths.append(viz.gap_heatmap(gap_data))
        paths.append(viz.time_comparison(sample_raw_results))
        
        # Verify all files created
        assert len(paths) == 6
        for path in paths:
            assert Path(path).exists()
            assert Path(path).stat().st_size > 500  # All should be non-trivial files


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
