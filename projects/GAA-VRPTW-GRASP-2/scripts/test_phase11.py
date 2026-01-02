"""
Phase 11 Tests: Comprehensive validation of testing and validation framework

Test coverage:
1. UnitTestsValidator: Instance, Route, Solution, Operators
2. IntegrationTestsValidator: GRASP, Algorithm generation, flows
3. FeasibilityValidator: Capacity, time windows, customer coverage
4. OutputValidator: Directory structure, CSV integrity, metrics accuracy
5. ValidationSuite: Full validation orchestration
"""

import pytest
import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

from validation import (
    ValidationResult,
    UnitTestsValidator,
    IntegrationTestsValidator,
    FeasibilityValidator,
    OutputValidator,
    ValidationSuite
)


class TestValidationResult:
    """Test ValidationResult dataclass"""
    
    def test_validation_result_passed(self):
        """Test ValidationResult with passed status"""
        result = ValidationResult(
            name="Test validation",
            passed=True,
            message="Test passed successfully",
            details={'items_checked': 5}
        )
        
        assert result.passed == True
        assert result.name == "Test validation"
    
    def test_validation_result_failed(self):
        """Test ValidationResult with failed status"""
        result = ValidationResult(
            name="Test validation",
            passed=False,
            message="Test failed",
            details={'error': 'Something went wrong'}
        )
        
        assert result.passed == False
        assert result.message == "Test failed"
    
    def test_validation_result_to_dict(self):
        """Test converting ValidationResult to dict"""
        result = ValidationResult(
            name="Test",
            passed=True,
            message="Passed",
            details={'key': 'value'}
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['test'] == "Test"
        assert result_dict['passed'] == True


class TestUnitTestsValidator:
    """Test UnitTestsValidator methods"""
    
    def test_validate_instance_class(self):
        """Test Instance class validation"""
        result = UnitTestsValidator.validate_instance_class()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Instance class parsing"
        assert result.passed == True
    
    def test_validate_route_class(self):
        """Test Route class validation"""
        result = UnitTestsValidator.validate_route_class()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Route class operations"
        assert result.passed == True
        assert 'demand_calculation' in result.details
    
    def test_validate_solution_class(self):
        """Test Solution class validation"""
        result = UnitTestsValidator.validate_solution_class()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Solution class management"
        assert result.passed == True
    
    def test_validate_operators(self):
        """Test Operators validation"""
        result = UnitTestsValidator.validate_operators()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Operator implementation"
        assert result.passed == True
        assert result.details['intra_route_operators'] > 0


class TestIntegrationTestsValidator:
    """Test IntegrationTestsValidator methods"""
    
    def test_validate_grasp_workflow(self):
        """Test GRASP workflow validation"""
        result = IntegrationTestsValidator.validate_grasp_workflow()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "GRASP complete workflow"
        assert result.passed == True
    
    def test_validate_algorithm_generation(self):
        """Test Algorithm generation validation"""
        result = IntegrationTestsValidator.validate_algorithm_generation()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Algorithm generation"
        assert result.passed == True
        assert result.details['algorithm_count'] == 3
        assert result.details['seed'] == 42
    
    def test_validate_generated_algorithm_execution(self):
        """Test Generated algorithm execution validation"""
        result = IntegrationTestsValidator.validate_generated_algorithm_execution()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Generated algorithm execution"
        assert result.passed == True
    
    def test_validate_quick_flow(self):
        """Test QUICK flow validation"""
        result = IntegrationTestsValidator.validate_quick_flow()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "QUICK experiment flow"
        assert result.passed == True
        assert result.details['experiments_count'] == 36
        assert result.details['families'] == 1
    
    def test_validate_full_flow(self):
        """Test FULL flow validation"""
        result = IntegrationTestsValidator.validate_full_flow()
        
        assert isinstance(result, ValidationResult)
        assert result.name == "FULL experiment flow"
        assert result.passed == True
        assert result.details['experiments_count'] == 168
        assert result.details['families'] == 6


class TestFeasibilityValidator:
    """Test FeasibilityValidator methods"""
    
    def test_validate_capacity_constraint(self):
        """Test capacity constraint validation"""
        solution = {'routes': []}  # Mock solution
        
        result = FeasibilityValidator.validate_capacity_constraint(solution)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Capacity constraint"
        assert result.passed == True
    
    def test_validate_time_window_constraint(self):
        """Test time window constraint validation"""
        solution = {'routes': []}
        
        result = FeasibilityValidator.validate_time_window_constraint(solution)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Time window constraint"
        assert result.passed == True
    
    def test_validate_customer_coverage(self):
        """Test customer coverage validation"""
        # Note: With empty routes, coverage is 0/99, so test should expect False
        solution = {'routes': []}
        
        result = FeasibilityValidator.validate_customer_coverage(solution, 99)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Customer coverage"
        # Empty solution has no coverage, should fail
        assert result.passed == False
        assert result.details['customers_covered'] == 0


class TestOutputValidator:
    """Test OutputValidator methods"""
    
    @pytest.fixture
    def sample_experiment_dir(self):
        """Create sample experiment directory"""
        tmpdir = tempfile.mkdtemp()
        
        # Create structure
        Path(tmpdir, 'results').mkdir()
        Path(tmpdir, 'plots').mkdir()
        Path(tmpdir, 'logs').mkdir()
        
        # Create required CSV file
        csv_path = Path(tmpdir) / 'results' / 'raw_results.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['algorithm', 'instance', 'K', 'D', 'K_BKS', 'reached_K_BKS', 'time_seconds', 'iterations', 'feasible', 'gap_percent', 'delta_K', 'seed', 'mode', 'family', 'index', 'timestamp'])
            writer.writerow(['algo1', 'C101', 10, 5, 10, True, 1.5, 100, True, 0.0, 0.0, 42, 'QUICK', 'C1', 0, '10-11-24_12-00-00'])
        
        # Create required JSON metadata file
        metadata_path = Path(tmpdir) / 'results' / 'experiment_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump({
                'experiment_id': 'test_exp_001',
                'timestamp': '10-11-24_12-00-00',
                'mode': 'QUICK',
                'families': ['C1'],
                'algorithms': ['algo1'],
                'total_experiments': 1,
                'seed': 42
            }, f)
        
        yield tmpdir
        
        # Cleanup
        shutil.rmtree(tmpdir)
    
    def test_validate_directory_structure_valid(self, sample_experiment_dir):
        """Test directory structure validation - valid case"""
        result = OutputValidator.validate_directory_structure(sample_experiment_dir)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Output directory structure"
        assert result.passed == True
    
    def test_validate_directory_structure_missing_dirs(self, tmpdir):
        """Test directory structure validation - missing directories"""
        # Don't create subdirectories
        result = OutputValidator.validate_directory_structure(str(tmpdir))
        
        assert isinstance(result, ValidationResult)
        assert result.passed == False
        assert 'missing' in result.details
    
    @pytest.fixture
    def sample_csv_file(self, sample_experiment_dir):
        """Create sample raw_results.csv"""
        data = {
            'algorithm_id': ['Algo1']*5 + ['Algo2']*5,
            'instance_id': ['R101', 'R102', 'R103', 'C101', 'C102'] * 2,
            'family': ['R1']*3 + ['C1']*2 + ['R1']*3 + ['C1']*2,
            'run_id': [1]*10,
            'random_seed': [42]*10,
            'K_final': [10, 10, 11, 9, 9, 10, 10, 11, 11, 10],
            'D_final': [1100.0]*10,
            'K_BKS': [10]*10,
            'D_BKS': [1100.0]*10,
            'delta_K': [0, 0, 1, -1, -1, 0, 0, 1, 1, 0],
            'gap_distance': [0.0]*10,
            'gap_percent': [0.0]*10,
            'total_time_sec': [5.0]*10,
            'iterations_executed': [100]*10,
            'reached_K_BKS': [True]*5 + [True]*5
        }
        
        csv_path = Path(sample_experiment_dir) / 'results' / 'raw_results.csv'
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        
        return str(csv_path)
    
    def test_validate_csv_integrity_valid(self, sample_csv_file):
        """Test CSV integrity validation - valid case"""
        result = OutputValidator.validate_csv_integrity(sample_csv_file)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "CSV integrity"
        assert result.passed == True
        assert result.details['rows'] == 10
    
    def test_validate_csv_integrity_missing_columns(self, sample_experiment_dir):
        """Test CSV integrity validation - missing columns"""
        csv_path = Path(sample_experiment_dir) / 'results' / 'bad.csv'
        csv_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Create CSV with missing columns
        df = pd.DataFrame({'col1': [1, 2, 3]})
        df.to_csv(csv_path, index=False)
        
        result = OutputValidator.validate_csv_integrity(str(csv_path))
        
        assert result.passed == False
        assert 'missing_columns' in result.details
    
    def test_validate_metrics_accuracy_valid(self, sample_csv_file):
        """Test metrics accuracy validation - valid case"""
        # Update sample CSV with correct metric columns
        df = pd.read_csv(sample_csv_file)
        
        # Add missing metric columns
        df['K_final'] = 10
        df['K_BKS'] = 10
        df['D_final'] = 1500.0
        df['D_BKS'] = 1500.0
        df['delta_K'] = 0  # K_final - K_BKS
        df['gap_percent'] = 0.0  # (D_final - D_BKS) / D_BKS * 100
        df['reached_K_BKS'] = True
        
        df.to_csv(sample_csv_file, index=False)
        
        result = OutputValidator.validate_metrics_accuracy(sample_csv_file)
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Metrics accuracy"
        assert result.passed == True
    
    @pytest.fixture
    def sample_metadata_file(self, sample_experiment_dir):
        """Create sample experiment_metadata.json"""
        metadata = {
            'experiment_id': 'vrptw_experiments_QUICK_02-01-26_10-30-45',
            'mode': 'QUICK',
            'timestamp': '2026-01-02T10:30:45.123456',
            'families': ['R1'],
            'algorithms': ['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
            'total_experiments': 36,
            'seed': 42
        }
        
        json_path = Path(sample_experiment_dir) / 'results' / 'experiment_metadata.json'
        json_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(json_path, 'w') as f:
            json.dump(metadata, f)
        
        return str(json_path)
    
    def test_validate_metadata_json_valid(self, sample_metadata_file):
        """Test metadata JSON validation - valid case"""
        result = OutputValidator.validate_metadata_json(sample_metadata_file, 'QUICK')
        
        assert isinstance(result, ValidationResult)
        assert result.name == "Metadata JSON validity"
        assert result.passed == True
        assert result.details['mode'] == 'QUICK'
    
    def test_validate_metadata_json_invalid_mode(self, sample_experiment_dir):
        """Test metadata JSON validation - invalid mode"""
        metadata = {
            'experiment_id': 'test',
            'mode': 'INVALID',
            'timestamp': '2026-01-02T10:30:45',
            'families': ['R1'],
            'algorithms': ['Algo1'],
            'total_experiments': 12,
            'seed': 42
        }
        
        json_path = Path(sample_experiment_dir) / 'results' / 'bad_metadata.json'
        json_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(json_path, 'w') as f:
            json.dump(metadata, f)
        
        result = OutputValidator.validate_metadata_json(str(json_path))
        
        assert result.passed == False


class TestValidationSuite:
    """Test ValidationSuite integration"""
    
    def test_validation_suite_initialization(self):
        """Test ValidationSuite initialization"""
        suite = ValidationSuite()
        
        assert suite.results == []
        assert suite.experiment_dir is None
    
    def test_run_unit_tests(self):
        """Test running unit tests"""
        suite = ValidationSuite()
        results = suite.run_unit_tests()
        
        assert len(results) == 4
        assert all(isinstance(r, ValidationResult) for r in results)
        assert all(r.passed for r in results)
    
    def test_run_integration_tests(self):
        """Test running integration tests"""
        suite = ValidationSuite()
        results = suite.run_integration_tests()
        
        assert len(results) == 5
        assert all(isinstance(r, ValidationResult) for r in results)
        assert all(r.passed for r in results)
    
    @pytest.fixture
    def full_experiment_dir(self):
        """Create complete experiment directory"""
        tmpdir = tempfile.mkdtemp()
        
        # Create structure
        Path(tmpdir, 'results').mkdir(parents=True)
        Path(tmpdir, 'plots').mkdir(parents=True)
        Path(tmpdir, 'logs').mkdir(parents=True)
        
        # Create CSV
        data = {
            'algorithm_id': ['Algo1']*10 + ['Algo2']*10,
            'instance_id': ['R101']*5 + ['R102']*5 + ['R101']*5 + ['R102']*5,
            'family': ['R1']*10 + ['R1']*10,
            'run_id': [1]*20,
            'random_seed': [42]*20,
            'K_final': np.random.randint(9, 12, 20),
            'D_final': np.random.uniform(1000, 1500, 20),
            'K_BKS': [10]*20,
            'D_BKS': np.random.uniform(950, 1450, 20),
            'delta_K': np.random.randint(-1, 2, 20),
            'gap_distance': np.random.uniform(0, 100, 20),
            'gap_percent': np.random.uniform(0, 10, 20),
            'total_time_sec': np.random.uniform(3, 10, 20),
            'iterations_executed': np.random.randint(50, 200, 20),
            'reached_K_BKS': np.random.choice([True, False], 20)
        }
        
        df = pd.DataFrame(data)
        df.to_csv(Path(tmpdir) / 'results' / 'raw_results.csv', index=False)
        
        # Create metadata
        metadata = {
            'experiment_id': 'test_experiment',
            'mode': 'QUICK',
            'timestamp': '2026-01-02T10:00:00',
            'families': ['R1'],
            'algorithms': ['Algo1', 'Algo2'],
            'total_experiments': 20,
            'seed': 42
        }
        
        with open(Path(tmpdir) / 'results' / 'experiment_metadata.json', 'w') as f:
            json.dump(metadata, f)
        
        yield tmpdir
        
        # Cleanup
        shutil.rmtree(tmpdir)
    
    def test_run_output_validation(self, full_experiment_dir):
        """Test output validation"""
        suite = ValidationSuite(experiment_dir=full_experiment_dir)
        results = suite.run_output_validation()
        
        assert len(results) == 4
        assert all(isinstance(r, ValidationResult) for r in results)
        # Should have some passed results
        assert any(r.passed for r in results)
    
    def test_run_full_suite(self, full_experiment_dir):
        """Test running full validation suite"""
        suite = ValidationSuite(experiment_dir=full_experiment_dir)
        results = suite.run_full_suite()
        
        assert 'unit_tests' in results
        assert 'integration_tests' in results
        assert 'output_validation' in results
        
        assert len(results['unit_tests']) == 4
        assert len(results['integration_tests']) == 5
        assert len(results['output_validation']) >= 3
    
    def test_get_summary(self, full_experiment_dir):
        """Test validation summary"""
        suite = ValidationSuite(experiment_dir=full_experiment_dir)
        suite.run_full_suite()
        summary = suite.get_summary()
        
        assert 'total_tests' in summary
        assert 'passed' in summary
        assert 'failed' in summary
        assert 'pass_rate' in summary
        assert 'all_passed' in summary
        
        assert summary['total_tests'] > 0
        assert summary['passed'] <= summary['total_tests']


class TestPhase11Integration:
    """Integration tests for Phase 11"""
    
    def test_complete_validation_workflow(self):
        """Test complete validation workflow"""
        suite = ValidationSuite()
        
        # Run all tests
        full_results = suite.run_full_suite()
        summary = suite.get_summary()
        
        # Verify structure
        assert sum(len(v) for v in full_results.values()) == summary['total_tests']
        assert summary['passed'] + summary['failed'] == summary['total_tests']
        assert 0 <= summary['pass_rate'] <= 100
    
    def test_validation_result_consistency(self):
        """Test that ValidationResult is consistent across validators"""
        validators = [
            UnitTestsValidator.validate_instance_class(),
            IntegrationTestsValidator.validate_grasp_workflow(),
            OutputValidator.validate_directory_structure('/tmp/nonexistent')
        ]
        
        for result in validators:
            # All should be ValidationResult instances
            assert isinstance(result, ValidationResult)
            # All should have these attributes
            assert hasattr(result, 'name')
            assert hasattr(result, 'passed')
            assert hasattr(result, 'message')
            assert hasattr(result, 'details')
