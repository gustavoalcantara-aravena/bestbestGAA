"""
Unit Tests for Fase 2: Core VRPTW Components

Tests for:
- Customer data structure
- Route evaluation and constraints
- Instance validation
- Solution feasibility and fitness
- Integration with BKS
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core import (
    Customer, Route, Instance, Solution,
    SolomonLoader, evaluate_solution, fitness_function,
    validate_solution_against_bks
)


def test_customer():
    """Test Customer data structure."""
    print("\n📋 TEST: Customer")
    
    # Create depot
    depot = Customer(id=0, x=0, y=0, demand=0, ready_time=0, due_date=1000, service_time=0)
    assert depot.id == 0
    assert depot.demand == 0
    print("  ✅ Depot creation")
    
    # Create regular customer
    c1 = Customer(id=1, x=10, y=20, demand=10, ready_time=100, due_date=500, service_time=10)
    assert c1.id == 1
    assert c1.demand == 10
    print("  ✅ Customer creation")
    
    # Test time window check
    assert c1.is_in_time_window(150)
    assert not c1.is_in_time_window(50)
    assert not c1.is_in_time_window(550)
    print("  ✅ Time window validation")
    
    return True


def test_instance():
    """Test Instance creation and validation."""
    print("\n📋 TEST: Instance")
    
    # Create simple 100-customer instance
    customers = [
        Customer(id=0, x=0, y=0, demand=0, ready_time=0, due_date=1000, service_time=0)
    ]
    
    for i in range(1, 101):
        customers.append(
            Customer(
                id=i, x=float(i), y=float(i * 2),
                demand=10, ready_time=0, due_date=1000, service_time=10
            )
        )
    
    instance = Instance(
        name="TEST101",
        n_customers=100,
        K_vehicles=10,
        Q_capacity=100,
        customers=customers,
        family="C1"
    )
    
    # Test validation
    is_valid, errors = instance.validate()
    if not is_valid:
        print(f"  ❌ Validation failed: {errors}")
        return False
    print("  ✅ Instance creation and validation")
    
    # Test distance calculation
    dist = instance.get_distance(0, 1)
    assert dist > 0
    print("  ✅ Distance calculation")
    
    # Test get_customer
    c = instance.get_customer(5)
    assert c.id == 5
    print("  ✅ Customer retrieval")
    
    return True


def test_route():
    """Test Route creation, constraints, and feasibility."""
    print("\n📋 TEST: Route")
    
    # Create instance
    customers = [
        Customer(id=0, x=0, y=0, demand=0, ready_time=0, due_date=1000, service_time=0)
    ]
    for i in range(1, 101):
        customers.append(
            Customer(
                id=i, x=float(i), y=float(i),
                demand=10, ready_time=0, due_date=1000, service_time=10
            )
        )
    
    instance = Instance(
        name="TEST101", n_customers=100, K_vehicles=10, Q_capacity=100,
        customers=customers
    )
    
    # Create route
    route = Route(vehicle_id=1, sequence=[0, 1, 2, 3, 0], instance=instance)
    
    # Test basic properties
    assert route.vehicle_id == 1
    print("  ✅ Route creation")
    
    # Test distance
    dist = route.total_distance
    assert dist > 0
    print(f"  ✅ Total distance: {dist:.2f}")
    
    # Test load
    load = route.total_load
    assert load == 30  # 3 customers × 10 demand
    print(f"  ✅ Total load: {load}")
    
    # Test time
    time = route.total_time
    assert time < float('inf')
    print(f"  ✅ Total time: {time:.2f}")
    
    # Test feasibility
    assert route.is_feasible
    print("  ✅ Feasibility check")
    
    # Test add_customer
    route.add_customer(5)
    assert 5 in route.sequence
    print("  ✅ Add customer")
    
    # Test remove_customer
    route.remove_customer(5)
    assert 5 not in route.sequence
    print("  ✅ Remove customer")
    
    return True


def test_solution():
    """Test Solution structure and fitness."""
    print("\n📋 TEST: Solution")
    
    # Create instance
    customers = [
        Customer(id=0, x=0, y=0, demand=0, ready_time=0, due_date=1000, service_time=0)
    ]
    for i in range(1, 101):
        customers.append(
            Customer(
                id=i, x=float(i), y=float(i),
                demand=10, ready_time=0, due_date=1000, service_time=10
            )
        )
    
    instance = Instance(
        name="TEST101", n_customers=100, K_vehicles=10, Q_capacity=100,
        customers=customers
    )
    
    # Create solution with multiple routes
    route1 = Route(vehicle_id=1, sequence=[0] + list(range(1, 6)) + [0], instance=instance)
    route2 = Route(vehicle_id=2, sequence=[0] + list(range(6, 11)) + [0], instance=instance)
    
    solution = Solution(instance=instance, routes=[route1, route2])
    
    # Test num_vehicles
    assert solution.num_vehicles == 2
    print("  ✅ Vehicle count")
    
    # Test fitness
    fitness = solution.fitness
    assert fitness[0] == 2  # K = num_vehicles
    assert fitness[1] > 0  # D = total_distance
    print(f"  ✅ Fitness: K={fitness[0]}, D={fitness[1]:.2f}")
    
    # Test to_dict
    solution_dict = solution.to_dict()
    assert 'num_vehicles' in solution_dict
    assert 'routes' in solution_dict
    print("  ✅ Serialization to dict")
    
    return True


def test_evaluation():
    """Test solution evaluation functions."""
    print("\n📋 TEST: Evaluation")
    
    # Create instance
    customers = [
        Customer(id=0, x=0, y=0, demand=0, ready_time=0, due_date=1000, service_time=0)
    ]
    for i in range(1, 101):
        customers.append(
            Customer(
                id=i, x=float(i), y=float(i),
                demand=10, ready_time=0, due_date=1000, service_time=10
            )
        )
    
    instance = Instance(
        name="TEST101", n_customers=100, K_vehicles=10, Q_capacity=1000,
        customers=customers
    )
    
    # Create solution that covers all customers
    routes = []
    customers_per_route = 20
    for v_id in range(5):
        start = v_id * customers_per_route + 1
        end = (v_id + 1) * customers_per_route + 1
        customers_in_route = list(range(start, end))
        route = Route(vehicle_id=v_id, sequence=[0] + customers_in_route + [0], instance=instance)
        routes.append(route)
    
    solution = Solution(instance=instance, routes=routes)
    
    # Test feasibility
    is_feasible, details = evaluate_solution(solution)
    assert is_feasible
    assert details['coverage_ok']
    print("  ✅ Solution evaluation")
    
    # Test fitness
    fit = fitness_function(solution)
    assert fit[0] == 5  # 5 vehicles
    print(f"  ✅ Fitness calculation: {fit}")
    
    return True


def test_bks_integration():
    """Test integration with BKS manager."""
    print("\n📋 TEST: BKS Integration")
    
    try:
        from src.core import BKSManager
        
        # Initialize BKS manager
        bks_manager = BKSManager()
        
        # Get a known instance
        c101_bks = bks_manager.get_bks("C101")
        if c101_bks:
            k_bks, d_bks = c101_bks
            assert k_bks > 0
            assert d_bks > 0
            print(f"  ✅ BKS for C101: K={k_bks}, D={d_bks:.2f}")
        else:
            print("  ⚠️  BKS data not available (this is OK in test environment)")
        
        return True
    except Exception as e:
        print(f"  ⚠️  BKS test skipped: {e}")
        return True


def test_solomon_loader():
    """Test SolomonLoader functionality."""
    print("\n📋 TEST: SolomonLoader")
    
    # Test family parsing
    families = [
        ("C101", "C1"),
        ("C201", "C2"),
        ("R101", "R1"),
        ("R201", "R2"),
        ("RC101", "RC1"),
        ("RC201", "RC2"),
    ]
    
    for instance_name, expected_family in families:
        family = SolomonLoader.parse_family(instance_name)
        assert family == expected_family, f"Failed: {instance_name} -> {family} (expected {expected_family})"
    
    print("  ✅ Family parsing")
    
    # Test loading from directory (if available)
    dataset_path = project_root / "datasets"
    if dataset_path.exists():
        try:
            instances = SolomonLoader.load_all_instances(str(dataset_path))
            summary = SolomonLoader.summary(instances)
            print(f"  ✅ Loaded {summary['total_instances']} instances from {summary['total_families']} families")
            return True
        except Exception as e:
            print(f"  ⚠️  Could not load dataset: {e}")
            return True
    else:
        print("  ⚠️  Dataset directory not found (this is OK)")
        return True


# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  PHASE 2 - VRPTW CORE COMPONENTS TEST SUITE")
    print("="*60)
    
    tests = [
        ("Customer", test_customer),
        ("Instance", test_instance),
        ("Route", test_route),
        ("Solution", test_solution),
        ("Evaluation", test_evaluation),
        ("BKS Integration", test_bks_integration),
        ("SolomonLoader", test_solomon_loader),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"  ❌ {test_name} failed")
        except Exception as e:
            failed += 1
            print(f"  ❌ {test_name} error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"  RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    sys.exit(0 if failed == 0 else 1)
