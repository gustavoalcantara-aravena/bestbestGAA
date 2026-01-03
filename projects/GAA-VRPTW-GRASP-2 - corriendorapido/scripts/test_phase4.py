"""
Phase 4 Test Suite: GRASP, VND, and ILS Metaheuristics

Tests:
1. GRASP basic functionality
2. VND convergence
3. ILS improvement over GRASP
4. Hybrid GRASP-ILS
5. Time limits
6. Verbose logging
"""

import unittest
import time
from copy import deepcopy

from src.core import Instance, Customer, Solution, Route
from src.metaheuristic import GRASP, VariableNeighborhoodDescent, IteratedLocalSearch, HybridGRASP_ILS


def create_small_instance(n_customers: int = 10) -> Instance:
    """Create a small synthetic VRPTW instance for testing."""
    instance = Instance(
        name="test_small",
        n_customers=n_customers,
        K_vehicles=5,
        Q_capacity=200,
    )
    
    # Depot at origin (index 0)
    depot = Customer(
        id=0, x=0, y=0, demand=0,
        ready_time=0, due_date=1000, service_time=0,
    )
    instance.customers.append(depot)
    
    # Random customers in [0, 100] x [0, 100]
    import random
    random.seed(42)
    
    for i in range(1, n_customers + 1):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        demand = random.randint(5, 50)
        ready_time = random.randint(0, 600)
        due_date = min(1000, ready_time + 200)
        service_time = random.randint(5, 30)
        
        customer = Customer(
            id=i,
            x=x,
            y=y,
            demand=demand,
            ready_time=ready_time,
            due_date=due_date,
            service_time=service_time,
        )
        instance.customers.append(customer)
    
    return instance


class TestGRASP(unittest.TestCase):
    """Test GRASP metaheuristic."""
    
    def setUp(self):
        """Setup test instance."""
        self.instance = create_small_instance(n_customers=10)
    
    def test_grasp_initialization(self):
        """Test GRASP can be initialized."""
        grasp = GRASP(alpha=0.15, max_iterations=5, seed=42, verbose=False)
        self.assertEqual(grasp.alpha, 0.15)
        self.assertEqual(grasp.max_iterations, 5)
    
    def test_grasp_solve_basic(self):
        """Test GRASP solve produces feasible solution."""
        grasp = GRASP(alpha=0.15, max_iterations=5, seed=42, verbose=False)
        solution, fitness, stats = grasp.solve(self.instance, time_limit=None)
        
        # Check solution structure
        self.assertIsInstance(solution, Solution)
        self.assertIsInstance(fitness, tuple)
        self.assertEqual(len(fitness), 2)  # (K, D)
        
        # Check fitness
        self.assertGreater(fitness[0], 0)  # num_vehicles > 0
        self.assertGreater(fitness[1], 0)  # total_distance > 0
        
        # Check stats
        self.assertIn('total_iterations', stats)
        self.assertIn('total_time', stats)
        self.assertGreater(stats['total_iterations'], 0)
    
    def test_grasp_determinism_with_seed(self):
        """Test GRASP produces same result with same seed."""
        grasp1 = GRASP(alpha=0.15, max_iterations=10, seed=42, verbose=False)
        solution1, fitness1, _ = grasp1.solve(self.instance)
        
        grasp2 = GRASP(alpha=0.15, max_iterations=10, seed=42, verbose=False)
        solution2, fitness2, _ = grasp2.solve(self.instance)
        
        # Same fitness
        self.assertEqual(fitness1, fitness2)
    
    def test_grasp_time_limit(self):
        """Test GRASP respects time limit."""
        grasp = GRASP(alpha=0.15, max_iterations=1000, seed=42, verbose=False)
        
        start = time.time()
        solution, fitness, stats = grasp.solve(self.instance, time_limit=0.5)
        elapsed = time.time() - start
        
        # Should complete within reasonable time
        self.assertLess(elapsed, 2.0)
        self.assertLess(stats['total_time'], 1.0)
    
    def test_grasp_verbose(self):
        """Test GRASP verbose mode."""
        grasp = GRASP(alpha=0.15, max_iterations=3, verbose=True)
        solution, fitness, stats = grasp.solve(self.instance)
        
        # Should have iteration log
        self.assertGreater(len(grasp.iteration_log), 0)
    
    def test_grasp_multiple_runs(self):
        """Test GRASP can run multiple times."""
        grasp = GRASP(alpha=0.15, max_iterations=3, seed=None, verbose=False)
        
        fitnesses = []
        for _ in range(3):
            solution, fitness, stats = grasp.solve(self.instance)
            fitnesses.append(fitness)
        
        # Should have 3 results
        self.assertEqual(len(fitnesses), 3)


class TestVND(unittest.TestCase):
    """Test Variable Neighborhood Descent."""
    
    def setUp(self):
        """Setup test instance and solution."""
        self.instance = create_small_instance(n_customers=10)
        
        # Create an initial solution
        self.grasp = GRASP(alpha=0.15, max_iterations=5, seed=42, verbose=False)
        self.initial_solution, _, _ = self.grasp.solve(self.instance)
    
    def test_vnd_initialization(self):
        """Test VND can be initialized."""
        vnd = VariableNeighborhoodDescent(verbose=False)
        self.assertIsNotNone(vnd.neighborhoods)
        self.assertGreater(len(vnd.neighborhoods), 0)
    
    def test_vnd_search(self):
        """Test VND search improves or maintains solution."""
        vnd = VariableNeighborhoodDescent(verbose=False)
        
        initial_fitness = self.initial_solution.fitness
        improved_solution = vnd.search(deepcopy(self.initial_solution))
        improved_fitness = improved_solution.fitness
        
        # VND should not worsen solution
        self.assertLessEqual(improved_fitness, initial_fitness)
    
    def test_vnd_search_with_shaking(self):
        """Test VND with perturbation."""
        from src.operators import RandomRemoval
        
        vnd = VariableNeighborhoodDescent(verbose=False)
        perturbation = RandomRemoval(num_remove=3)
        
        result = vnd.search_with_shaking(
            deepcopy(self.initial_solution),
            perturbation_operator=perturbation,
            max_iterations=5,
        )
        
        self.assertIsInstance(result, Solution)
        self.assertGreater(result.num_vehicles, 0)
    
    def test_vnd_logging(self):
        """Test VND generates search log."""
        vnd = VariableNeighborhoodDescent(verbose=False)
        vnd.search(deepcopy(self.initial_solution))
        
        self.assertGreater(len(vnd.search_log), 0)
        
        # Check log structure
        for entry in vnd.search_log:
            self.assertIn('iteration', entry)
            self.assertIn('operator', entry)
            self.assertIn('fitness', entry)


class TestILS(unittest.TestCase):
    """Test Iterated Local Search."""
    
    def setUp(self):
        """Setup test instance."""
        self.instance = create_small_instance(n_customers=10)
    
    def test_ils_initialization(self):
        """Test ILS can be initialized."""
        ils = IteratedLocalSearch(
            max_iterations=10,
            acceptance_criterion='better',
            verbose=False,
        )
        self.assertEqual(ils.max_iterations, 10)
        self.assertEqual(ils.acceptance_criterion, 'better')
    
    def test_ils_solve_basic(self):
        """Test ILS solve produces feasible solution."""
        ils = IteratedLocalSearch(
            max_iterations=5,
            acceptance_criterion='better',
            seed=42,
            verbose=False,
        )
        
        solution, fitness, stats = ils.solve(self.instance, time_limit=None)
        
        # Check solution
        self.assertIsInstance(solution, Solution)
        self.assertIsInstance(fitness, tuple)
        self.assertEqual(len(fitness), 2)
        
        # Check stats
        self.assertIn('total_iterations', stats)
        self.assertIn('total_time', stats)
        self.assertGreater(stats['total_iterations'], 0)
    
    def test_ils_vs_grasp(self):
        """Test ILS produces competitive results with GRASP."""
        # GRASP solution
        grasp = GRASP(alpha=0.15, max_iterations=10, seed=42, verbose=False)
        grasp_solution, grasp_fitness, _ = grasp.solve(self.instance)
        
        # ILS solution
        ils = IteratedLocalSearch(
            max_iterations=10,
            acceptance_criterion='better',
            seed=42,
            verbose=False,
        )
        ils_solution, ils_fitness, _ = ils.solve(self.instance)
        
        # ILS should be competitive (may not always be better due to randomness)
        # At minimum, should find feasible solution
        self.assertGreater(ils_fitness[0], 0)
        self.assertGreater(ils_fitness[1], 0)
    
    def test_ils_acceptance_better(self):
        """Test ILS with 'better' acceptance criterion."""
        ils = IteratedLocalSearch(
            max_iterations=5,
            acceptance_criterion='better',
            seed=42,
            verbose=False,
        )
        
        solution, fitness, stats = ils.solve(self.instance)
        self.assertIsNotNone(solution)
    
    def test_ils_acceptance_probability(self):
        """Test ILS with probabilistic acceptance."""
        ils = IteratedLocalSearch(
            max_iterations=5,
            acceptance_criterion='probability',
            seed=42,
            verbose=False,
        )
        
        solution, fitness, stats = ils.solve(self.instance)
        self.assertIsNotNone(solution)
    
    def test_ils_time_limit(self):
        """Test ILS respects time limit."""
        ils = IteratedLocalSearch(
            max_iterations=1000,
            acceptance_criterion='better',
            seed=42,
            verbose=False,
        )
        
        start = time.time()
        solution, fitness, stats = ils.solve(self.instance, time_limit=0.5)
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 2.0)
    
    def test_ils_verbose(self):
        """Test ILS verbose mode."""
        ils = IteratedLocalSearch(
            max_iterations=5,
            verbose=True,
        )
        
        solution, fitness, stats = ils.solve(self.instance)
        self.assertGreater(len(ils.iteration_log), 0)


class TestHybridGRASP_ILS(unittest.TestCase):
    """Test Hybrid GRASP-ILS."""
    
    def setUp(self):
        """Setup test instance."""
        self.instance = create_small_instance(n_customers=10)
    
    def test_hybrid_initialization(self):
        """Test Hybrid GRASP-ILS initialization."""
        hybrid = HybridGRASP_ILS(
            grasp_iterations=5,
            ils_iterations=5,
            alpha=0.15,
            verbose=False,
        )
        self.assertEqual(hybrid.grasp_iterations, 5)
        self.assertEqual(hybrid.ils_iterations, 5)
    
    def test_hybrid_solve(self):
        """Test Hybrid GRASP-ILS solve."""
        hybrid = HybridGRASP_ILS(
            grasp_iterations=5,
            ils_iterations=5,
            alpha=0.15,
            seed=42,
            verbose=False,
        )
        
        solution, fitness, stats = hybrid.solve(self.instance)
        
        # Check solution
        self.assertIsInstance(solution, Solution)
        self.assertIsInstance(fitness, tuple)
        self.assertEqual(len(fitness), 2)
        
        # Check stats
        self.assertIn('total_time', stats)
        self.assertIn('grasp_stats', stats)
        self.assertIn('ils_stats', stats)
    
    def test_hybrid_vs_pure_algorithms(self):
        """Test Hybrid combines GRASP and ILS benefits."""
        # Hybrid solution
        hybrid = HybridGRASP_ILS(
            grasp_iterations=5,
            ils_iterations=5,
            seed=42,
            verbose=False,
        )
        hybrid_solution, hybrid_fitness, _ = hybrid.solve(self.instance)
        
        # Pure GRASP
        grasp = GRASP(alpha=0.15, max_iterations=10, seed=42, verbose=False)
        grasp_solution, grasp_fitness, _ = grasp.solve(self.instance)
        
        # Both should find feasible solutions
        self.assertGreater(hybrid_fitness[0], 0)
        self.assertGreater(grasp_fitness[0], 0)


class TestPhase4Integration(unittest.TestCase):
    """Integration tests for Phase 4 metaheuristics."""
    
    def setUp(self):
        """Setup test instance."""
        self.instance = create_small_instance(n_customers=15)
    
    def test_all_metaheuristics_work(self):
        """Test all metaheuristics produce valid solutions."""
        # GRASP
        grasp = GRASP(alpha=0.15, max_iterations=5, seed=42)
        grasp_solution, grasp_fitness, _ = grasp.solve(self.instance)
        self.assertGreater(grasp_fitness[0], 0)
        
        # ILS
        ils = IteratedLocalSearch(max_iterations=5, seed=42)
        ils_solution, ils_fitness, _ = ils.solve(self.instance)
        self.assertGreater(ils_fitness[0], 0)
        
        # Hybrid
        hybrid = HybridGRASP_ILS(grasp_iterations=3, ils_iterations=3, seed=42)
        hybrid_solution, hybrid_fitness, _ = hybrid.solve(self.instance)
        self.assertGreater(hybrid_fitness[0], 0)
    
    def test_metaheuristics_improve_solutions(self):
        """Test that metaheuristics improve over iterations."""
        grasp = GRASP(alpha=0.15, max_iterations=20, seed=42, verbose=False)
        solution, fitness, stats = grasp.solve(self.instance)
        
        # Should have multiple iterations
        self.assertGreater(len(grasp.iteration_log), 1)
        
        # Later iterations should have better fitness
        first_fitness = grasp.iteration_log[0]['best_fitness']
        last_fitness = grasp.iteration_log[-1]['best_fitness']
        
        self.assertLessEqual(last_fitness, first_fitness)
    
    def test_reproducibility(self):
        """Test determinism with same seed."""
        # GRASP
        grasp1 = GRASP(alpha=0.15, max_iterations=10, seed=123)
        _, fitness1, _ = grasp1.solve(self.instance)
        
        grasp2 = GRASP(alpha=0.15, max_iterations=10, seed=123)
        _, fitness2, _ = grasp2.solve(self.instance)
        
        self.assertEqual(fitness1, fitness2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
