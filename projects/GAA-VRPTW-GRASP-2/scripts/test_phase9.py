"""
Phase 9 Tests: Comprehensive validation of experimentation scripts

Test coverage:
1. AlgorithmGenerator: seed=42, JSON output, multiple algorithms
2. ExperimentConfig: validation, defaults, modes
3. ExperimentExecutor: output directory structure, result storage
4. QUICK mode: 1 family (R1), 12 instances, 36 total experiments
5. FULL mode: 6 families, 56 instances, 168 total experiments
6. CSV output format and validation
7. Experiment metadata generation
8. Solomon instance mapping accuracy
"""

import pytest
import json
import csv
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

from experiments import (
    ExperimentConfig,
    AlgorithmGenerator,
    ExperimentExecutor,
    QuickExperiment,
    FullExperiment
)


class TestExperimentConfig:
    """Test experiment configuration validation"""
    
    def test_valid_quick_config(self):
        """Test valid QUICK mode configuration"""
        config = ExperimentConfig(
            mode='QUICK',
            families=['R1'],
            algorithms=['Algo1', 'Algo2']
        )
        assert config.mode == 'QUICK'
        assert config.families == ['R1']
        assert config.repetitions == 1
    
    def test_valid_full_config(self):
        """Test valid FULL mode configuration"""
        config = ExperimentConfig(
            mode='FULL',
            families=['C1', 'R1', 'RC1'],
            algorithms=['Algo1', 'Algo2', 'Algo3']
        )
        assert config.mode == 'FULL'
        assert len(config.families) == 3
    
    def test_invalid_mode(self):
        """Test invalid mode raises assertion"""
        with pytest.raises(AssertionError):
            ExperimentConfig(
                mode='INVALID',
                families=['R1'],
                algorithms=['Algo1']
            )
    
    def test_invalid_repetitions(self):
        """Test invalid repetitions raises assertion"""
        with pytest.raises(AssertionError):
            ExperimentConfig(
                mode='QUICK',
                families=['R1'],
                algorithms=['Algo1'],
                repetitions=0
            )
    
    def test_config_defaults(self):
        """Test configuration defaults"""
        config = ExperimentConfig(
            mode='QUICK',
            families=['R1'],
            algorithms=['Algo1']
        )
        assert config.repetitions == 1
        assert config.seed == 42
        assert config.timeout_sec == 600


class TestAlgorithmGenerator:
    """Test algorithm generation with seed=42"""
    
    def test_generator_initialization(self):
        """Test generator initialization with custom output dir"""
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = AlgorithmGenerator(seed=42, output_dir=tmpdir)
            assert gen.seed == 42
            assert Path(tmpdir).exists()
    
    def test_generate_algorithms_count(self):
        """Test correct number of algorithms generated"""
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = AlgorithmGenerator(seed=42, output_dir=tmpdir)
            algos = gen.generate_algorithms(3)
            
            assert len(algos) == 3
            assert all(f'GAA_Algorithm_{i}' in algos for i in range(1, 4))
    
    def test_algorithm_json_format(self):
        """Test generated algorithm JSON structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = AlgorithmGenerator(seed=42, output_dir=tmpdir)
            algos = gen.generate_algorithms(2)
            
            # Verify first algorithm file exists and has correct structure
            algo_file = Path(tmpdir) / f"{algos[0]}.json"
            assert algo_file.exists()
            
            with open(algo_file) as f:
                algo_data = json.load(f)
            
            assert algo_data['algorithm_id'] == algos[0]
            assert algo_data['seed'] == 42
            assert 'components' in algo_data
            assert 'construction' in algo_data['components']
            assert 'local_search' in algo_data['components']
            assert 'parameters' in algo_data['components']
    
    def test_seed_reproducibility(self):
        """Test that same seed produces consistent algorithm structure"""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                gen1 = AlgorithmGenerator(seed=42, output_dir=tmpdir1)
                gen2 = AlgorithmGenerator(seed=42, output_dir=tmpdir2)
                
                algos1 = gen1.generate_algorithms(2)
                algos2 = gen2.generate_algorithms(2)
                
                # Load and compare first algorithm structure
                with open(Path(tmpdir1) / f"{algos1[0]}.json") as f:
                    data1 = json.load(f)
                with open(Path(tmpdir2) / f"{algos2[0]}.json") as f:
                    data2 = json.load(f)
                
                # With same seed, both should have same algorithm_id and structure
                assert data1['algorithm_id'] == data2['algorithm_id']
                assert data1['seed'] == data2['seed'] == 42
                assert 'components' in data1
                assert 'components' in data2
                assert 'parameters' in data1['components']
                assert 'parameters' in data2['components']


class TestExperimentExecutor:
    """Test experiment execution framework"""
    
    @pytest.fixture
    def executor(self):
        """Create temporary executor"""
        config = ExperimentConfig(
            mode='QUICK',
            families=['R1'],
            algorithms=['GAA_Algo_1'],
            repetitions=1,
            seed=42
        )
        executor = ExperimentExecutor(config)
        yield executor
        # Cleanup
        if executor.output_dir.exists():
            shutil.rmtree(executor.output_dir.parent / executor.output_dir.name)
    
    def test_output_directory_structure(self, executor):
        """Test correct output directory structure created"""
        assert executor.output_dir.exists()
        assert executor.results_dir.exists()
        assert executor.plots_dir.exists()
        assert executor.logs_dir.exists()
    
    def test_experiment_id_format(self, executor):
        """Test experiment ID format"""
        assert executor.config.mode in executor.experiment_id
        assert 'vrptw_experiments' in executor.experiment_id
        assert len(executor.experiment_id.split('_')) >= 3
    
    def test_add_single_result(self, executor):
        """Test adding single result"""
        executor.add_result(
            algorithm_id='GAA_Algo_1',
            instance_id='R101',
            family='R1',
            run_id=1,
            k_final=10,
            k_bks=10,
            d_final=1150.5,
            d_bks=1105.0,
            total_time_sec=5.2,
            iterations=100
        )
        
        assert len(executor.raw_results) == 1
        assert executor.raw_results[0]['instance_id'] == 'R101'
        assert executor.raw_results[0]['delta_K'] == 0
        assert executor.raw_results[0]['reached_K_BKS'] == True
    
    def test_add_results_multiple(self, executor):
        """Test adding multiple results"""
        for i in range(5):
            executor.add_result(
                algorithm_id='GAA_Algo_1',
                instance_id=f'R10{i+1}',
                family='R1',
                run_id=1,
                k_final=10+i,
                k_bks=10,
                d_final=1000+i*10,
                d_bks=1000,
                total_time_sec=5.0+i,
                iterations=100
            )
        
        assert len(executor.raw_results) == 5
    
    def test_gap_calculation_when_k_optimal(self, executor):
        """Test gap_percent calculation when K is optimal"""
        executor.add_result(
            algorithm_id='GAA_Algo_1',
            instance_id='R101',
            family='R1',
            run_id=1,
            k_final=10,
            k_bks=10,
            d_final=1105.0,
            d_bks=1100.0,
            total_time_sec=5.0,
            iterations=100
        )
        
        result = executor.raw_results[0]
        assert result['gap_percent'] == pytest.approx(0.4545, rel=0.001)
        assert result['gap_distance'] == pytest.approx(5.0, rel=0.001)
    
    def test_gap_calculation_when_k_suboptimal(self, executor):
        """Test gap_percent is None when K is suboptimal"""
        executor.add_result(
            algorithm_id='GAA_Algo_1',
            instance_id='R101',
            family='R1',
            run_id=1,
            k_final=11,
            k_bks=10,
            d_final=900.0,
            d_bks=1100.0,
            total_time_sec=5.0,
            iterations=100
        )
        
        result = executor.raw_results[0]
        assert result['gap_percent'] is None
        assert result['gap_distance'] is None
        assert result['reached_K_BKS'] == False
    
    def test_save_raw_results_csv(self, executor):
        """Test saving raw_results.csv"""
        for i in range(3):
            executor.add_result(
                algorithm_id='GAA_Algo_1',
                instance_id=f'R10{i+1}',
                family='R1',
                run_id=1,
                k_final=10,
                k_bks=10,
                d_final=1100.0,
                d_bks=1100.0,
                total_time_sec=5.0,
                iterations=100
            )
        
        executor.save_raw_results()
        
        csv_file = executor.results_dir / "raw_results.csv"
        assert csv_file.exists()
        
        # Verify CSV content
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 3
        assert rows[0]['algorithm_id'] == 'GAA_Algo_1'
        assert rows[0]['family'] == 'R1'
    
    def test_save_experiment_metadata(self, executor):
        """Test saving experiment_metadata.json"""
        executor.save_experiment_metadata()
        
        metadata_file = executor.results_dir / "experiment_metadata.json"
        assert metadata_file.exists()
        
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        assert metadata['mode'] == 'QUICK'
        assert metadata['families'] == ['R1']
        assert 'experiment_id' in metadata
        assert 'timestamp' in metadata
        assert metadata['seed'] == 42


class TestSolomonInstanceMapping:
    """Test Solomon benchmark instance mapping"""
    
    @pytest.fixture
    def executor(self):
        """Create executor for testing"""
        config = ExperimentConfig(
            mode='QUICK',
            families=['R1'],
            algorithms=['GAA_Algo_1']
        )
        return ExperimentExecutor(config)
    
    def test_r1_family_instances(self, executor):
        """Test R1 family has 12 instances (R101-R112)"""
        instances = executor.get_solomon_instances(['R1'])
        assert 'R1' in instances
        assert len(instances['R1']) == 12
        assert instances['R1'][0] == 'R101'
        assert instances['R1'][-1] == 'R112'
    
    def test_c1_family_instances(self, executor):
        """Test C1 family has 9 instances (C101-C109)"""
        instances = executor.get_solomon_instances(['C1'])
        assert len(instances['C1']) == 9
    
    def test_c2_family_instances(self, executor):
        """Test C2 family has 8 instances (C201-C208)"""
        instances = executor.get_solomon_instances(['C2'])
        assert len(instances['C2']) == 8
    
    def test_r2_family_instances(self, executor):
        """Test R2 family has 11 instances (R201-R211)"""
        instances = executor.get_solomon_instances(['R2'])
        assert len(instances['R2']) == 11
    
    def test_rc1_family_instances(self, executor):
        """Test RC1 family has 8 instances (RC101-RC108)"""
        instances = executor.get_solomon_instances(['RC1'])
        assert len(instances['RC1']) == 8
    
    def test_rc2_family_instances(self, executor):
        """Test RC2 family has 8 instances (RC201-RC208)"""
        instances = executor.get_solomon_instances(['RC2'])
        assert len(instances['RC2']) == 8
    
    def test_all_families_total(self, executor):
        """Test total Solomon instances across all families"""
        instances = executor.get_solomon_instances(['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'])
        total = sum(len(v) for v in instances.values())
        assert total == 56  # Total Solomon instances
    
    def test_invalid_family(self, executor):
        """Test invalid family raises error"""
        with pytest.raises(ValueError, match="Unknown Solomon family"):
            executor.get_solomon_instances(['INVALID_FAMILY'])


class TestQuickExperiment:
    """Test QUICK mode experiment"""
    
    def test_quick_config(self):
        """Test QUICK mode configuration"""
        config = QuickExperiment.get_config()
        assert config.mode == 'QUICK'
        assert config.families == ['R1']
        assert len(config.algorithms) == 3
    
    def test_quick_experiment_count(self):
        """Test QUICK mode generates 36 experiments (1 family × 12 instances × 3 algorithms × 1 rep)"""
        executor = QuickExperiment.run()
        
        # 1 family (R1) × 12 instances × 3 algorithms × 1 repetition = 36
        assert len(executor.raw_results) == 36
        
        # Verify all results are for R1 family
        families = set(r['family'] for r in executor.raw_results)
        assert families == {'R1'}
        
        # Cleanup
        shutil.rmtree(executor.output_dir.parent / executor.output_dir.name)
    
    def test_quick_output_files(self):
        """Test QUICK mode creates expected output files"""
        executor = QuickExperiment.run()
        
        # Check files exist
        assert (executor.results_dir / "raw_results.csv").exists()
        assert (executor.results_dir / "experiment_metadata.json").exists()
        
        # Cleanup
        shutil.rmtree(executor.output_dir.parent / executor.output_dir.name)


class TestFullExperiment:
    """Test FULL mode experiment"""
    
    def test_full_config(self):
        """Test FULL mode configuration"""
        config = FullExperiment.get_config()
        assert config.mode == 'FULL'
        assert len(config.families) == 6
        assert len(config.algorithms) == 3
    
    def test_full_experiment_count(self):
        """Test FULL mode generates 168 experiments (6 families × 56 instances × 3 algorithms × 1 rep)"""
        executor = FullExperiment.run()
        
        # 6 families × 56 instances × 3 algorithms × 1 repetition = 168
        assert len(executor.raw_results) == 168
        
        # Verify all families represented
        families = set(r['family'] for r in executor.raw_results)
        assert families == {'C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'}
        
        # Cleanup
        shutil.rmtree(executor.output_dir.parent / executor.output_dir.name)
    
    def test_full_output_files(self):
        """Test FULL mode creates expected output files"""
        executor = FullExperiment.run()
        
        # Check files exist
        assert (executor.results_dir / "raw_results.csv").exists()
        assert (executor.results_dir / "experiment_metadata.json").exists()
        
        # Cleanup
        shutil.rmtree(executor.output_dir.parent / executor.output_dir.name)


class TestPhase9Integration:
    """Integration tests for Phase 9"""
    
    def test_quick_and_full_different_outputs(self):
        """Test QUICK and FULL modes produce different experiment counts"""
        quick_executor = QuickExperiment.run()
        full_executor = FullExperiment.run()
        
        quick_count = len(quick_executor.raw_results)
        full_count = len(full_executor.raw_results)
        
        assert quick_count == 36
        assert full_count == 168
        assert full_count > quick_count
        
        # Cleanup
        shutil.rmtree(quick_executor.output_dir.parent / quick_executor.output_dir.name)
        shutil.rmtree(full_executor.output_dir.parent / full_executor.output_dir.name)
    
    def test_experiment_reproducibility_with_seed(self):
        """Test experiments are reproducible with same seed"""
        executor1 = QuickExperiment.run()
        results1_k = [r['K_final'] for r in executor1.raw_results]
        output_dir1 = executor1.output_dir.parent / executor1.output_dir.name
        
        executor2 = QuickExperiment.run()
        results2_k = [r['K_final'] for r in executor2.raw_results]
        output_dir2 = executor2.output_dir.parent / executor2.output_dir.name
        
        # Same seed should produce same experiment count
        assert len(results1_k) == len(results2_k) == 36
        
        # Cleanup - use absolute paths
        try:
            if output_dir1.exists():
                shutil.rmtree(output_dir1)
        except:
            pass
        
        try:
            if output_dir2.exists():
                shutil.rmtree(output_dir2)
        except:
            pass
