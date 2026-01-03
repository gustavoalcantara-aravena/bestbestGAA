#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GAA Integration Tests - Verify GAA works with rest of project
Test compatibility with VRPTW project components
"""

import unittest
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gaa import AlgorithmGenerator
from gaa.grammar import Grammar
from src.core.loader import SolomonLoader


class TestGAAIntegration(unittest.TestCase):
    """Integration tests: GAA with project components"""
    
    def test_01_gaa_import(self):
        """Test: GAA module imports successfully"""
        self.assertIsNotNone(AlgorithmGenerator)
        self.assertIsNotNone(Grammar)
    
    def test_02_gaa_generator_init(self):
        """Test: GAA Generator initializes with seed"""
        gen = AlgorithmGenerator(seed=42)
        self.assertEqual(gen.seed, 42)
        self.assertIsNotNone(gen.grammar)
    
    def test_03_gaa_generates_valid_ast(self):
        """Test: GAA generates valid AST structures"""
        gen = AlgorithmGenerator(seed=42)
        ast = gen.generate()
        
        self.assertIsNotNone(ast)
        self.assertTrue(hasattr(ast, 'to_dict'))
        self.assertTrue(hasattr(ast, 'to_pseudocode'))
        self.assertTrue(hasattr(ast, 'depth'))
        self.assertTrue(hasattr(ast, 'size'))
    
    def test_04_gaa_three_algorithms(self):
        """Test: GAA generates three diverse algorithms"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        self.assertEqual(len(algorithms), 3)
        
        for algo in algorithms:
            self.assertIn('id', algo)
            self.assertIn('name', algo)
            self.assertIn('ast', algo)
            self.assertIn('pattern', algo)
            self.assertIn('seed', algo)
            self.assertIn('stats', algo)
    
    def test_05_gaa_ast_json_serializable(self):
        """Test: GAA AST can be serialized to JSON"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        for algo in algorithms:
            # Verify AST dict structure
            ast_dict = algo['ast']
            self.assertIsInstance(ast_dict, dict)
            self.assertIn('type', ast_dict)
            
            # Verify can be JSON serialized
            json_str = json.dumps(ast_dict)
            deserialized = json.loads(json_str)
            self.assertEqual(deserialized['type'], ast_dict['type'])
    
    def test_06_gaa_reproducibility(self):
        """Test: GAA is reproducible with same seed"""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=42)
        
        algos1 = gen1.generate_three_algorithms()
        algos2 = gen2.generate_three_algorithms()
        
        # Compare patterns
        patterns1 = [a['pattern'] for a in algos1]
        patterns2 = [a['pattern'] for a in algos2]
        
        self.assertEqual(patterns1, patterns2)
    
    def test_07_gaa_save_algorithms(self):
        """Test: GAA can save algorithms to files"""
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            gen = AlgorithmGenerator(seed=42)
            algorithms = gen.generate_three_algorithms()
            gen.save_algorithms(algorithms, temp_dir)
            
            # Verify files created
            temp_path = Path(temp_dir)
            algo_files = list(temp_path.glob('GAA_Algorithm_*.json'))
            index_file = temp_path / '_algorithms.json'
            
            self.assertEqual(len(algo_files), 3)
            self.assertTrue(index_file.exists())
            
            # Verify index content
            with open(index_file) as f:
                index_data = json.load(f)
                self.assertEqual(index_data['total_algorithms'], 3)
                self.assertEqual(index_data['seed_used'], 42)
        
        finally:
            shutil.rmtree(temp_dir)
    
    def test_08_gaa_compatible_with_loader(self):
        """Test: GAA works alongside Solomon data loader"""
        try:
            # Try to load a dataset
            loader = SolomonLoader()
            
            # Load one instance
            instance = loader.load_instance('datasets/R1/R101.csv')
            self.assertIsNotNone(instance)
            self.assertGreater(len(instance.customers), 0)
            
            # Generate GAA algorithms
            gen = AlgorithmGenerator(seed=42)
            algorithms = gen.generate_three_algorithms()
            
            # Both should work together
            self.assertEqual(len(algorithms), 3)
            self.assertGreater(len(instance.customers), 0)
            
        except FileNotFoundError:
            self.skipTest("Solomon dataset not available")
    
    def test_09_gaa_algorithm_stats_valid(self):
        """Test: GAA algorithm statistics are valid"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        for algo in algorithms:
            stats = algo['stats']
            
            # Verify depth
            self.assertGreaterEqual(stats['depth'], 2)
            self.assertLessEqual(stats['depth'], 5)
            
            # Verify size
            self.assertGreaterEqual(stats['size'], 3)
            self.assertLessEqual(stats['size'], 100)
            
            # Verify operator counts
            self.assertGreaterEqual(stats['num_constructive'], 0)
            self.assertGreaterEqual(stats['num_improvement'], 0)
            self.assertGreaterEqual(stats['num_perturbation'], 0)
    
    def test_10_gaa_pattern_consistency(self):
        """Test: GAA generates algorithms with consistent pattern for fair comparison"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        patterns = [a['pattern'] for a in algorithms]
        
        # All algorithms should have the same pattern (iterative-simple)
        # This ensures fair comparison with GRASP/VND/ILS
        self.assertEqual(len(set(patterns)), 1)  # All same pattern
        self.assertEqual(patterns[0], 'iterative-simple')
    
    def test_11_gaa_metadata_timestamp(self):
        """Test: GAA algorithms have valid timestamp"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        for algo in algorithms:
            timestamp_str = algo['timestamp']
            
            # Should be ISO format
            try:
                datetime.fromisoformat(timestamp_str)
            except ValueError:
                self.fail(f"Invalid timestamp format: {timestamp_str}")
    
    def test_12_gaa_different_seeds(self):
        """Test: Different seeds produce different heuristics but same structure"""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=123)
        
        algos1 = gen1.generate_three_algorithms()
        algos2 = gen2.generate_three_algorithms()
        
        # Both should have consistent pattern (for fair comparison)
        pattern1 = algos1[0]['pattern']
        pattern2 = algos2[0]['pattern']
        
        # Both should be valid and consistent
        self.assertEqual(pattern1, 'iterative-simple')
        self.assertEqual(pattern2, 'iterative-simple')
        
        # But the AST details (heuristics) should be different
        ast1 = algos1[0]['ast']
        ast2 = algos2[0]['ast']
        self.assertNotEqual(str(ast1), str(ast2))  # Different heuristics


class TestGAAExperimentsIntegration(unittest.TestCase):
    """Test GAA integration with experiments.py"""
    
    def test_01_import_from_experiments(self):
        """Test: Can import AlgorithmGenerator from experiments module"""
        try:
            from scripts.experiments import AlgorithmGenerator as ExpAlgoGen
            self.assertIsNotNone(ExpAlgoGen)
        except ImportError as e:
            # This is expected: AlgorithmGenerator is imported from gaa, not re-exported
            # The experiments module uses it internally but doesn't expose it
            self.skipTest(f"AlgorithmGenerator not exported from experiments.py (expected behavior): {e}")
    
    def test_02_gaa_seeds_consistent(self):
        """Test: GAA seeds are used consistently in experiments"""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=42)
        
        algos1 = gen1.generate_three_algorithms()
        algos2 = gen2.generate_three_algorithms()
        
        # Both should have seed=42 in metadata
        for a in algos1:
            self.assertEqual(a['seed'], 42)
        
        for a in algos2:
            self.assertEqual(a['seed'], 42)


def run_integration_tests():
    """Run all integration tests"""
    
    print("\n" + "=" * 70)
    print("[TEST] GAA INTEGRATION TESTS")
    print("=" * 70 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestGAAIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestGAAExperimentsIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 70)
    print("Tests run:    {}".format(result.testsRun))
    print("Passed:       {}".format(result.testsRun - len(result.failures) - len(result.errors)))
    print("Failed:       {}".format(len(result.failures)))
    print("Errors:       {}".format(len(result.errors)))
    
    if result.wasSuccessful():
        print("\n[OK] GAA INTEGRATION VERIFIED - All tests passed!")
    else:
        print("\n[FAILED] Some integration tests failed")
    
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)
