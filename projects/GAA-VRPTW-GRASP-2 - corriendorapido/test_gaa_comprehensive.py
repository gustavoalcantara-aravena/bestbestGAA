#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit Tests for GAA Module
Comprehensive testing of Grammar, AST Nodes, and Algorithm Generator
"""

import unittest
import sys
import json
from pathlib import Path
from gaa import Grammar, AlgorithmGenerator
from gaa.ast_nodes import (
    ASTNode, Seq, If, While, For,
    GreedyConstruct, LocalSearch, Perturbation
)


class TestGrammar(unittest.TestCase):
    """Test Grammar class and operator definitions"""
    
    def setUp(self):
        self.grammar = Grammar()
    
    def test_01_constructive_operators(self):
        """Test: 6 constructive operators defined"""
        self.assertEqual(len(self.grammar.CONSTRUCTIVE_TERMINALS), 6)
    
    def test_02_improvement_operators(self):
        """Test: 8 improvement operators defined"""
        self.assertEqual(len(self.grammar.IMPROVEMENT_TERMINALS), 8)
    
    def test_03_perturbation_operators(self):
        """Test: 4 perturbation operators defined"""
        self.assertEqual(len(self.grammar.PERTURBATION_TERMINALS), 4)
    
    def test_04_total_operators(self):
        """Test: Total of 18 operators"""
        total = (len(self.grammar.CONSTRUCTIVE_TERMINALS) +
                len(self.grammar.IMPROVEMENT_TERMINALS) +
                len(self.grammar.PERTURBATION_TERMINALS))
        self.assertEqual(total, 18)
    
    def test_05_depth_limits(self):
        """Test: Grammar has proper depth limits"""
        self.assertEqual(self.grammar.min_depth, 2)
        self.assertEqual(self.grammar.max_depth, 5)
    
    def test_06_validate_valid_ast(self):
        """Test: Validation passes for valid AST"""
        ast = Seq(body=[
            GreedyConstruct(heuristic="Savings"),
            LocalSearch(operator="TwoOpt")
        ])
        errors = self.grammar.validate_ast(ast)
        self.assertEqual(len(errors), 0)
    
    def test_07_validate_invalid_ast(self):
        """Test: Validation fails for non-ASTNode"""
        errors = self.grammar.validate_ast("not an ast")
        self.assertGreater(len(errors), 0)
    
    def test_08_statistics(self):
        """Test: Statistics collection works"""
        ast = Seq(body=[GreedyConstruct(), LocalSearch()])
        stats = self.grammar.get_statistics(ast)
        
        self.assertIn('depth', stats)
        self.assertIn('size', stats)
        self.assertIn('num_constructive', stats)
        self.assertIn('num_improvement', stats)


class TestASTNodes(unittest.TestCase):
    """Test AST Node classes"""
    
    def test_01_greedy_construct(self):
        """Test: GreedyConstruct node works"""
        node = GreedyConstruct(heuristic="Savings", alpha=0.25)
        self.assertEqual(node.heuristic, "Savings")
        self.assertEqual(node.alpha, 0.25)
        self.assertEqual(node.depth(), 1)
        self.assertEqual(node.size(), 1)
    
    def test_02_local_search(self):
        """Test: LocalSearch node works"""
        node = LocalSearch(operator="TwoOpt", max_iterations=100)
        self.assertEqual(node.operator, "TwoOpt")
        self.assertEqual(node.max_iterations, 100)
        self.assertEqual(node.depth(), 1)
        self.assertEqual(node.size(), 1)
    
    def test_03_perturbation(self):
        """Test: Perturbation node works"""
        node = Perturbation(operator="RandomRouteRemoval", strength=2)
        self.assertEqual(node.operator, "RandomRouteRemoval")
        self.assertEqual(node.strength, 2)
    
    def test_04_seq_depth(self):
        """Test: Seq node computes correct depth"""
        seq = Seq(body=[GreedyConstruct(), LocalSearch()])
        self.assertEqual(seq.depth(), 2)
        self.assertEqual(seq.size(), 3)
    
    def test_05_while_node(self):
        """Test: While node structure"""
        loop = While(condition="IterBudget", max_iterations=100, 
                    body=LocalSearch(operator="TwoOpt"))
        self.assertEqual(loop.depth(), 2)
        self.assertEqual(loop.size(), 2)
    
    def test_06_for_node(self):
        """Test: For node structure"""
        body = Seq(body=[GreedyConstruct(), LocalSearch()])
        for_loop = For(iterations=5, body=body)
        self.assertEqual(for_loop.depth(), 3)
        self.assertEqual(for_loop.size(), 4)
    
    def test_07_if_node(self):
        """Test: If node structure"""
        if_node = If(condition="Improves", then_branch=LocalSearch(),
                    else_branch=Perturbation())
        self.assertEqual(if_node.depth(), 2)
        self.assertEqual(if_node.size(), 3)
    
    def test_08_to_pseudocode(self):
        """Test: Pseudocode generation"""
        node = GreedyConstruct(heuristic="Savings", alpha=0.25)
        pseudocode = node.to_pseudocode()
        self.assertIn("Savings", pseudocode)
        self.assertIn("0.25", pseudocode)
    
    def test_09_to_dict(self):
        """Test: Node serialization to dict"""
        node = GreedyConstruct(heuristic="Savings", alpha=0.25)
        node_dict = node.to_dict()
        self.assertEqual(node_dict['type'], 'GreedyConstruct')
        self.assertEqual(node_dict['heuristic'], 'Savings')
    
    def test_10_seq_serialization(self):
        """Test: Seq serialization"""
        seq = Seq(body=[GreedyConstruct(heuristic="Savings"), 
                       LocalSearch(operator="TwoOpt")])
        seq_dict = seq.to_dict()
        self.assertEqual(seq_dict['type'], 'Seq')
        self.assertEqual(len(seq_dict['body']), 2)
    
    def test_11_get_all_nodes(self):
        """Test: Get all nodes from tree"""
        seq = Seq(body=[GreedyConstruct(), LocalSearch(), Perturbation()])
        all_nodes = seq.get_all_nodes()
        self.assertEqual(len(all_nodes), 4)  # Seq + 3 children
    
    def test_12_complex_tree_depth(self):
        """Test: Depth calculation in complex tree"""
        complex_ast = Seq(body=[
            GreedyConstruct(),
            While(max_iterations=100, body=Seq(body=[
                LocalSearch(), Perturbation()
            ]))
        ])
        self.assertEqual(complex_ast.depth(), 4)
    
    def test_13_complex_tree_size(self):
        """Test: Size calculation in complex tree"""
        complex_ast = Seq(body=[
            GreedyConstruct(),
            While(max_iterations=100, body=Seq(body=[
                LocalSearch(), Perturbation()
            ]))
        ])
        self.assertEqual(complex_ast.size(), 6)


class TestAlgorithmGenerator(unittest.TestCase):
    """Test AlgorithmGenerator class"""
    
    def setUp(self):
        self.generator = AlgorithmGenerator(seed=42)
    
    def test_01_initialization(self):
        """Test: Generator initializes properly"""
        self.assertEqual(self.generator.seed, 42)
        self.assertIsNotNone(self.generator.grammar)
    
    def test_02_generate_simple(self):
        """Test: Simple pattern generation"""
        ast = self.generator._generate_simple()
        self.assertIsInstance(ast, Seq)
        self.assertEqual(len(ast.body), 2)
        self.assertIsInstance(ast.body[0], GreedyConstruct)
        self.assertIsInstance(ast.body[1], LocalSearch)
    
    def test_03_generate_iterative(self):
        """Test: Iterative pattern generation"""
        ast = self.generator._generate_iterative()
        self.assertIsInstance(ast, Seq)
        self.assertIsInstance(ast.body[1], While)
    
    def test_04_generate_multistart(self):
        """Test: Multi-start pattern generation"""
        ast = self.generator._generate_multistart()
        self.assertIsInstance(ast, For)
    
    def test_05_generate_complex(self):
        """Test: Complex pattern generation"""
        ast = self.generator._generate_complex()
        self.assertIsInstance(ast, Seq)
    
    def test_06_generate_with_validation(self):
        """Test: Generation with validation"""
        ast = self.generator.generate_with_validation(max_attempts=50)
        self.assertIsNotNone(ast)
        errors = self.generator.grammar.validate_ast(ast)
        self.assertEqual(len(errors), 0)
    
    def test_07_generate_three(self):
        """Test: Generate three algorithms"""
        algorithms = self.generator.generate_three_algorithms()
        self.assertEqual(len(algorithms), 3)
        
        for i, algo in enumerate(algorithms):
            self.assertEqual(algo['id'], i + 1)
            self.assertIn('name', algo)
            self.assertIn('ast', algo)
            self.assertIn('pattern', algo)
            self.assertIn('stats', algo)
    
    def test_08_reproducibility(self):
        """Test: Reproducibility with same seed"""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=42)
        
        algos1 = gen1.generate_three_algorithms()
        algos2 = gen2.generate_three_algorithms()
        
        patterns1 = [a['pattern'] for a in algos1]
        patterns2 = [a['pattern'] for a in algos2]
        
        self.assertEqual(patterns1, patterns2)
    
    def test_09_different_seed(self):
        """Test: Different seeds work correctly"""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=123)
        
        algos1 = gen1.generate_three_algorithms()
        algos2 = gen2.generate_three_algorithms()
        
        self.assertEqual(len(algos1), 3)
        self.assertEqual(len(algos2), 3)
    
    def test_10_metadata_present(self):
        """Test: Generated algorithms have all metadata"""
        algorithms = self.generator.generate_three_algorithms()
        
        for algo in algorithms:
            self.assertIn('id', algo)
            self.assertIn('name', algo)
            self.assertIn('ast', algo)
            self.assertIn('pattern', algo)
            self.assertIn('seed', algo)
            self.assertIn('timestamp', algo)
            self.assertIn('stats', algo)
    
    def test_11_statistics_present(self):
        """Test: Generated algorithms have statistics"""
        algorithms = self.generator.generate_three_algorithms()
        
        for algo in algorithms:
            stats = algo['stats']
            self.assertIn('depth', stats)
            self.assertIn('size', stats)
            self.assertIn('num_constructive', stats)
            self.assertIn('num_improvement', stats)
            self.assertIn('num_perturbation', stats)
    
    def test_12_depth_in_range(self):
        """Test: Algorithm depths in valid range"""
        for _ in range(5):
            algorithms = self.generator.generate_three_algorithms()
            for algo in algorithms:
                depth = algo['stats']['depth']
                self.assertGreaterEqual(depth, 2)
                self.assertLessEqual(depth, 5)
    
    def test_13_size_in_range(self):
        """Test: Algorithm sizes in valid range"""
        for _ in range(5):
            algorithms = self.generator.generate_three_algorithms()
            for algo in algorithms:
                size = algo['stats']['size']
                self.assertGreaterEqual(size, 3)
                self.assertLessEqual(size, 100)
    
    def test_14_alpha_in_range(self):
        """Test: Alpha parameter in [0.1, 0.5]"""
        for _ in range(5):
            ast = self.generator.generate()
            nodes = ast.get_all_nodes()
            
            for node in nodes:
                if isinstance(node, GreedyConstruct):
                    self.assertGreaterEqual(node.alpha, 0.1)
                    self.assertLessEqual(node.alpha, 0.5)
    
    def test_15_max_iterations_valid(self):
        """Test: Max iterations in valid range"""
        for _ in range(5):
            ast = self.generator.generate()
            nodes = ast.get_all_nodes()
            
            for node in nodes:
                if isinstance(node, LocalSearch):
                    self.assertGreater(node.max_iterations, 0)
                    self.assertLessEqual(node.max_iterations, 500)
    
    def test_16_save_algorithms(self):
        """Test: Saving algorithms to files"""
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            algorithms = self.generator.generate_three_algorithms()
            self.generator.save_algorithms(algorithms, temp_dir)
            
            temp_path = Path(temp_dir)
            algorithm_files = list(temp_path.glob('GAA_Algorithm_*.json'))
            index_file = temp_path / '_algorithms.json'
            
            self.assertEqual(len(algorithm_files), 3)
            self.assertTrue(index_file.exists())
            
            with open(index_file) as f:
                index_data = json.load(f)
                self.assertEqual(index_data['total_algorithms'], 3)
        
        finally:
            shutil.rmtree(temp_dir)


class TestIntegration(unittest.TestCase):
    """Integration tests for GAA system"""
    
    def test_01_full_workflow(self):
        """Test: Complete GAA workflow"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        grammar = Grammar()
        for algo in algorithms:
            ast_dict = algo['ast']
            self.assertEqual(ast_dict['type'], 'Seq')
            self.assertIn('body', ast_dict)
            
            stats = algo['stats']
            self.assertGreaterEqual(stats['size'], 3)
    
    def test_02_json_serializable(self):
        """Test: Generated AST can be JSON serialized"""
        gen = AlgorithmGenerator(seed=42)
        algorithms = gen.generate_three_algorithms()
        
        for algo in algorithms:
            json_str = json.dumps(algo['ast'])
            deserialized = json.loads(json_str)
            self.assertEqual(deserialized['type'], algo['ast']['type'])


def run_tests():
    """Run all tests"""
    
    print("\n" + "=" * 70)
    print("[TEST] GAA MODULE - COMPREHENSIVE UNIT TESTS")
    print("=" * 70 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestGrammar))
    suite.addTests(loader.loadTestsFromTestCase(TestASTNodes))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("Tests run:    {}".format(result.testsRun))
    print("Passed:       {}".format(result.testsRun - len(result.failures) - len(result.errors)))
    print("Failed:       {}".format(len(result.failures)))
    print("Errors:       {}".format(len(result.errors)))
    
    if result.wasSuccessful():
        print("\n[OK] ALL TESTS PASSED - GAA module verified!")
    else:
        print("\n[FAILED] Some tests failed")
    
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
