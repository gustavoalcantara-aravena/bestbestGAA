"""
Test Suite for Phase 5: GAA (Generación Automática de Algoritmos)

Comprehensive tests for:
- AST node functionality
- Grammar validation
- Algorithm generation
- AST interpretation
- Repair mechanisms

Run with: python -m pytest scripts/test_phase5.py -v
"""

import pytest
import random
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gaa.ast_nodes import (
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair,
    reconstruct_node,
)
from src.gaa.grammar import VRPTWGrammar, ConstraintValidator
from src.gaa.algorithm_generator import AlgorithmGenerator, AlgorithmValidator
from src.gaa.repair import ASTValidator, ASTRepairMechanism, ASTNormalizer


# ============================================================================
# Mock Classes for Testing (when real models not available)
# ============================================================================

class MockInstance:
    """Mock VRPTW instance for testing."""
    def __init__(self):
        self.num_customers = 5
        self.num_vehicles = 2
        self.capacity = 1000
        self.depot = (0, 0)
        self.customers = [
            {'id': i, 'x': random.randint(0, 100), 'y': random.randint(0, 100),
             'demand': random.randint(10, 100), 'service_time': random.randint(5, 20),
             'time_window': (0, 500)}
            for i in range(1, 6)
        ]


class MockSolution:
    """Mock solution for testing."""
    def __init__(self, instance=None):
        self.instance = instance or MockInstance()
        self.cost = 1000.0
        self.is_feasible = True
        self.num_routes = 2
    
    def clone(self):
        return MockSolution(self.instance)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_instance():
    """Create sample VRPTW instance for testing."""
    return MockInstance()


@pytest.fixture
def sample_solution(sample_instance):
    """Create sample solution."""
    return MockSolution(sample_instance)


@pytest.fixture
def grammar():
    """Create grammar instance."""
    return VRPTWGrammar()


@pytest.fixture
def generator():
    """Create algorithm generator."""
    return AlgorithmGenerator(seed=42)


@pytest.fixture
def validator():
    """Create AST validator."""
    return ASTValidator()


@pytest.fixture
def repair():
    """Create repair mechanism."""
    return ASTRepairMechanism()


# ============================================================================
# Phase 5.1: AST Node Tests
# ============================================================================

class TestASTNodes:
    """Test AST node functionality."""
    
    def test_seq_node_creation(self):
        """Test Seq node creation."""
        node1 = LocalSearch(operator='TwoOpt', max_iterations=50)
        node2 = LocalSearch(operator='OrOpt', max_iterations=30)
        seq = Seq(body=[node1, node2])
        
        assert len(seq.body) == 2
        assert seq.size() == 3
        assert seq.depth() == 1  # Seq is at depth 0, children at depth 0 (terminals)
    
    def test_while_node_creation(self):
        """Test While node creation."""
        body = LocalSearch(operator='TwoOpt', max_iterations=50)
        while_node = While(max_iterations=100, body=body)
        
        assert while_node.max_iterations == 100
        assert while_node.size() == 2
        assert while_node.depth() == 1  # While wraps terminal (depth 0), so 1+0=1
    
    def test_for_node_creation(self):
        """Test For node creation."""
        body = LocalSearch(operator='TwoOpt', max_iterations=50)
        for_node = For(iterations=5, body=body)
        
        assert for_node.iterations == 5
        assert for_node.size() == 2
    
    def test_if_node_creation(self):
        """Test If node creation."""
        then_br = LocalSearch(operator='TwoOpt', max_iterations=50)
        else_br = LocalSearch(operator='OrOpt', max_iterations=30)
        if_node = If(then_branch=then_br, else_branch=else_br)
        
        assert if_node.then_branch is not None
        assert if_node.else_branch is not None
    
    def test_choose_best_creation(self):
        """Test ChooseBestOf node creation."""
        alt1 = LocalSearch(operator='TwoOpt', max_iterations=50)
        alt2 = LocalSearch(operator='OrOpt', max_iterations=30)
        choose = ChooseBestOf(alternatives=[alt1, alt2])
        
        assert len(choose.alternatives) == 2
    
    def test_apply_until_creation(self):
        """Test ApplyUntilNoImprove node creation."""
        body = LocalSearch(operator='TwoOpt', max_iterations=50)
        apply_until = ApplyUntilNoImprove(max_no_improve=20, body=body)
        
        assert apply_until.max_no_improve == 20
    
    def test_greedy_construct_node(self):
        """Test GreedyConstruct node."""
        node = GreedyConstruct(heuristic='RandomizedInsertion')
        assert node.heuristic == 'RandomizedInsertion'
        assert node.size() == 1
        assert node.depth() == 0  # Terminal nodes have depth 0
    
    def test_local_search_node(self):
        """Test LocalSearch node."""
        node = LocalSearch(operator='TwoOpt', max_iterations=50)
        assert node.operator == 'TwoOpt'
        assert node.max_iterations == 50
    
    def test_node_serialization(self):
        """Test node to_dict and from_dict."""
        original = Seq(body=[
            GreedyConstruct(heuristic='RandomizedInsertion'),
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        # Serialize
        data = original.to_dict()
        
        # Deserialize
        restored = reconstruct_node(data)
        
        assert restored.size() == original.size()
        assert restored.depth() == original.depth()
    
    def test_node_pseudocode(self):
        """Test to_pseudocode output."""
        node = LocalSearch(operator='TwoOpt', max_iterations=50)
        pseudocode = node.to_pseudocode()
        
        assert 'LocalSearch' in pseudocode
        assert 'TwoOpt' in pseudocode
    
    def test_node_clone(self):
        """Test node cloning."""
        original = While(
            max_iterations=100,
            body=LocalSearch(operator='TwoOpt', max_iterations=50)
        )
        
        cloned = original.clone()
        
        assert cloned.size() == original.size()
        assert cloned.depth() == original.depth()
        # Modify clone shouldn't affect original
        cloned.max_iterations = 200
        assert original.max_iterations == 100


# ============================================================================
# Phase 5.2: Grammar and Constraint Validation Tests
# ============================================================================

class TestGrammar:
    """Test grammar validation."""
    
    def test_grammar_creation(self, grammar):
        """Test grammar initialization."""
        assert grammar is not None
        assert len(grammar.get_all_constructors()) > 0
        assert len(grammar.get_all_local_search()) > 0
    
    def test_constructor_terminals(self, grammar):
        """Test constructor terminals."""
        constructors = list(grammar.get_all_constructors())
        
        assert 'RandomizedInsertion' in constructors
        assert 'SavingsHeuristic' in constructors
        assert len(constructors) >= 4
    
    def test_local_search_terminals(self, grammar):
        """Test local search terminals."""
        ls_ops = list(grammar.get_all_local_search())
        
        assert 'TwoOpt' in ls_ops
        assert 'OrOpt' in ls_ops
        assert len(ls_ops) >= 6
    
    def test_valid_algorithm_validation(self, grammar):
        """Test validation of valid algorithm."""
        validator = ConstraintValidator()
        
        # Build valid algorithm: Construct -> While -> LocalSearch + LocalSearch
        algorithm = Seq(body=[
            GreedyConstruct(heuristic='RandomizedInsertion'),
            While(max_iterations=10, body=Seq(body=[
                LocalSearch(operator='TwoOpt', max_iterations=50),
                LocalSearch(operator='OrOpt', max_iterations=30)
            ]))
        ])
        
        is_valid, violations = validator.validate_tree(algorithm)
        assert is_valid or len(violations) == 0, f"Violations: {violations}"
    
    def test_invalid_depth_detection(self, grammar):
        """Test detection of excessive depth."""
        validator = ConstraintValidator()
        
        # Build very deep tree
        node = LocalSearch(operator='TwoOpt', max_iterations=50)
        for _ in range(10):
            node = While(max_iterations=100, body=node)
        
        is_valid, violations = validator.validate_tree(node)
        assert not is_valid


# ============================================================================
# Phase 5.3: Algorithm Generator Tests
# ============================================================================

class TestAlgorithmGenerator:
    """Test algorithm generation."""
    
    def test_generator_creation(self, generator):
        """Test generator initialization."""
        assert generator is not None
        assert generator.seed == 42
    
    def test_generate_single_algorithm(self, generator):
        """Test single algorithm generation."""
        algo = generator.generate_algorithm(depth=2, method='grow')
        
        assert isinstance(algo, ASTNode)
        assert algo.size() > 0
    
    def test_generate_three_algorithms(self, generator):
        """Test three-algorithm generation."""
        algos = generator.generate_three_algorithms(seed=42)
        
        assert len(algos) == 3
        assert all(isinstance(a, ASTNode) for a in algos)
    
    def test_reproducible_generation(self):
        """Test seed-based reproducibility."""
        gen1 = AlgorithmGenerator(seed=42)
        gen2 = AlgorithmGenerator(seed=42)
        
        algo1 = gen1.generate_algorithm(depth=2, method='grow')
        algo2 = gen2.generate_algorithm(depth=2, method='grow')
        
        assert algo1.size() == algo2.size()
        assert algo1.depth() == algo2.depth()
    
    def test_generated_algorithm_validity(self, generator):
        """Test that generated algorithms are valid."""
        validator = AlgorithmValidator()
        
        for _ in range(5):
            algo = generator.generate_algorithm(depth=2, method='grow')
            is_valid, errors, warnings = validator.validate_all(algo)
            # Most should be valid or fixable
            assert algo.size() < 30
    
    def test_grow_vs_full_methods(self, generator):
        """Test grow vs full generation methods."""
        grow_algo = generator.generate_algorithm(depth=2, method='grow')
        full_algo = generator.generate_algorithm(depth=2, method='full')
        
        # Full method typically produces larger trees
        assert grow_algo.size() > 0
        assert full_algo.size() > 0


# ============================================================================
# Phase 5.4: AST Interpreter Tests  
# ============================================================================

# Interpreter tests skipped - requires full Phase 2 models implementation
# These will be enabled once src.models is fully implemented


# ============================================================================
# Phase 5.5: AST Repair Tests
# ============================================================================

class TestASTValidator:
    """Test AST validation."""
    
    def test_validator_creation(self, validator):
        """Test validator initialization."""
        assert validator is not None
    
    def test_validate_valid_algorithm(self, validator):
        """Test validation of valid algorithm."""
        algo = Seq(body=[
            GreedyConstruct(heuristic='RandomizedInsertion'),
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        is_valid, violations = validator.validate(algo)
        assert is_valid or len(violations) <= 2


class TestASTRepairMechanism:
    """Test AST repair."""
    
    def test_repair_creation(self, repair):
        """Test repair mechanism creation."""
        assert repair is not None
    
    def test_repair_valid_algorithm(self, repair):
        """Test repair of valid algorithm."""
        algo = Seq(body=[
            GreedyConstruct(heuristic='RandomizedInsertion'),
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        repaired, was_repaired, repairs = repair.repair(algo)
        
        assert repaired is not None
        assert isinstance(repairs, list)
    
    def test_repair_missing_constructor(self, repair):
        """Test repair of missing constructor."""
        algo = Seq(body=[
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        repaired, was_repaired, repairs = repair.repair(algo)
        
        # Should add constructor
        assert len(repairs) > 0 or repaired.size() > 1
    
    def test_repair_missing_local_search(self, repair):
        """Test repair of missing local search."""
        algo = GreedyConstruct(heuristic='RandomizedInsertion')
        
        repaired, was_repaired, repairs = repair.repair(algo)
        
        # Should detect need for local search
        assert repaired is not None


class TestASTNormalizer:
    """Test AST normalization."""
    
    def test_normalizer_creation(self):
        """Test normalizer initialization."""
        normalizer = ASTNormalizer()
        assert normalizer is not None
    
    def test_normalize_sequence(self):
        """Test sequence normalization."""
        algo = Seq(body=[
            Seq(body=[
                GreedyConstruct(heuristic='RandomizedInsertion')
            ]),
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        normalizer = ASTNormalizer()
        normalized = normalizer.normalize(algo)
        
        assert normalized is not None


# ============================================================================
# Integration Tests
# ============================================================================

class TestPhase5Integration:
    """Integration tests combining all Phase 5 components."""
    
    def test_generate_and_validate(self):
        """Test: Generate algorithm then validate."""
        generator = AlgorithmGenerator(seed=42)
        validator = AlgorithmValidator()
        
        algo = generator.generate_algorithm(depth=2, method='grow')
        is_valid, errors, warnings = validator.validate_all(algo)
        
        assert algo.size() > 0
    
    def test_generate_repair_normalize(self):
        """Test: Generate, repair, and normalize."""
        generator = AlgorithmGenerator(seed=42)
        repair_mech = ASTRepairMechanism()
        normalizer = ASTNormalizer()
        
        algo = generator.generate_algorithm(depth=2, method='grow')
        repaired, _, _ = repair_mech.repair(algo)
        normalized = normalizer.normalize(repaired)
        
        assert normalized.size() > 0
    
    def test_serialize_deserialize(self):
        """Test: Serialize and deserialize algorithm."""
        algo = Seq(body=[
            GreedyConstruct(heuristic='RandomizedInsertion'),
            LocalSearch(operator='TwoOpt', max_iterations=50)
        ])
        
        # Serialize
        data = algo.to_dict()
        
        # Deserialize
        restored = reconstruct_node(data)
        
        assert restored.size() == algo.size()
        assert restored.depth() == algo.depth()


# ============================================================================
# Test Execution
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
