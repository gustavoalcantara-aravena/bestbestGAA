"""
Solution Evaluation Functions for VRPTW

Calculates route feasibility, distances, time windows, and fitness scores.
All evaluations follow Solomon benchmark constraints.
"""

from typing import Tuple
from .models import Route, Solution, Instance


def calculate_route_distance(route: Route) -> float:
    """
    Calculate total distance traveled by a route.
    
    Args:
        route: Route object with sequence of customers
        
    Returns:
        Total euclidean distance
    """
    return route.total_distance


def calculate_route_time(route: Route) -> float:
    """
    Calculate total elapsed time for a route including travel and service.
    
    Args:
        route: Route object
        
    Returns:
        Total time (or infinity if infeasible due to time windows)
    """
    return route.total_time


def check_capacity_constraint(route: Route, instance: Instance) -> bool:
    """
    Check if route respects vehicle capacity constraint.
    
    Args:
        route: Route to evaluate
        instance: Problem instance with Q_capacity
        
    Returns:
        True if total load <= Q, False otherwise
    """
    return route.total_load <= instance.Q_capacity


def check_time_window_constraint(route: Route, instance: Instance) -> bool:
    """
    Check if all customers in route can be served within their time windows.
    
    Args:
        route: Route to evaluate
        instance: Problem instance
        
    Returns:
        True if all customers can be served in time, False if any violation
    """
    return route.total_time != float('inf')


def check_max_route_time_constraint(route: Route, instance: Instance) -> bool:
    """
    Check if route respects maximum allowed route duration.
    
    Args:
        route: Route to evaluate
        instance: Problem instance with optional max_route_time
        
    Returns:
        True if route time <= max_route_time (or max_route_time is None)
    """
    if instance.max_route_time is None:
        return True
    return route.total_time <= instance.max_route_time


def evaluate_route(route: Route, instance: Instance) -> Tuple[bool, dict]:
    """
    Comprehensive evaluation of a single route.
    
    Args:
        route: Route to evaluate
        instance: Problem instance
        
    Returns:
        Tuple of (is_feasible, details_dict)
        where details_dict contains:
        - distance: Total distance
        - time: Total time
        - load: Total load
        - capacity_ok: Whether capacity respected
        - time_windows_ok: Whether all time windows respected
        - max_time_ok: Whether max route time respected
        - is_feasible: Overall feasibility
    """
    details = {
        'distance': calculate_route_distance(route),
        'time': calculate_route_time(route),
        'load': route.total_load,
        'capacity_ok': check_capacity_constraint(route, instance),
        'time_windows_ok': check_time_window_constraint(route, instance),
        'max_time_ok': check_max_route_time_constraint(route, instance),
    }
    
    is_feasible = (
        details['capacity_ok'] and
        details['time_windows_ok'] and
        details['max_time_ok']
    )
    details['is_feasible'] = is_feasible
    
    return is_feasible, details


def evaluate_solution(solution: Solution) -> Tuple[bool, dict]:
    """
    Comprehensive evaluation of a complete solution.
    
    Checks:
    1. All routes are feasible
    2. All customers visited exactly once
    3. No customer visited twice
    4. All customers in range [1, n_customers]
    
    Args:
        solution: Solution to evaluate
        
    Returns:
        Tuple of (is_feasible, details_dict)
        where details_dict contains:
        - num_vehicles: Number of non-empty routes
        - total_distance: K objective value
        - total_time: Maximum route time
        - fitness: (K, D) tuple
        - feasible: Overall feasibility
        - route_details: List of individual route evaluations
        - coverage_ok: All customers visited exactly once
        - constraint_violations: List of any violations
    """
    details = {
        'num_vehicles': solution.num_vehicles,
        'total_distance': solution.total_distance,
        'total_time': solution.total_time,
        'fitness': solution.fitness,
    }
    
    # Check all routes individually
    route_details = []
    all_routes_feasible = True
    
    for route in solution.routes:
        route_feasible, route_eval = evaluate_route(route, solution.instance)
        route_details.append(route_eval)
        if not route_feasible:
            all_routes_feasible = False
    
    details['route_details'] = route_details
    
    # Check customer coverage
    visited = set()
    coverage_violations = []
    
    for route in solution.routes:
        for customer_id in route.sequence:
            if customer_id == 0:  # Depot
                continue
            if customer_id in visited:
                coverage_violations.append(f"Customer {customer_id} visited multiple times")
            visited.add(customer_id)
    
    expected = set(range(1, solution.instance.n_customers + 1))
    missing = expected - visited
    extra = visited - expected
    
    if missing:
        coverage_violations.append(f"Missing customers: {sorted(missing)}")
    if extra:
        coverage_violations.append(f"Extra/invalid customers: {sorted(extra)}")
    
    coverage_ok = len(coverage_violations) == 0
    details['coverage_ok'] = coverage_ok
    details['constraint_violations'] = coverage_violations
    
    # Overall feasibility
    is_feasible = all_routes_feasible and coverage_ok
    details['feasible'] = is_feasible
    
    return is_feasible, details


def fitness_function(solution: Solution) -> Tuple[int, float]:
    """
    Calculate hierarchical fitness of a solution.
    
    Lexicographic ordering:
    1. Minimize K (number of vehicles) — primary objective
    2. Minimize D (total distance) — secondary objective
    
    Args:
        solution: Solution to evaluate
        
    Returns:
        Tuple (K, D)
    """
    return (solution.num_vehicles, solution.total_distance)


def compare_solutions(sol1: Solution, sol2: Solution, strict: bool = False) -> int:
    """
    Compare two solutions using hierarchical fitness.
    
    Args:
        sol1: First solution
        sol2: Second solution
        strict: If False, use lexicographic ordering (K first, then D)
                If True, use Pareto ordering
        
    Returns:
        -1 if sol1 is better, 0 if equal, 1 if sol2 is better
    """
    if strict:
        # Pareto dominance
        k1, d1 = sol1.fitness
        k2, d2 = sol2.fitness
        
        k1_better = k1 <= k2
        d1_better = d1 <= d2
        k1_strictly = k1 < k2
        d1_strictly = d1 < d2
        
        sol1_pareto_better = k1_better and d1_better and (k1_strictly or d1_strictly)
        sol2_pareto_better = k2 <= k1 and d2 <= d1 and (k2 < k1 or d2 < d1)
        
        if sol1_pareto_better:
            return -1
        elif sol2_pareto_better:
            return 1
        else:
            return 0
    else:
        # Lexicographic
        k1, d1 = sol1.fitness
        k2, d2 = sol2.fitness
        
        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        elif d1 < d2:
            return -1
        elif d1 > d2:
            return 1
        else:
            return 0


def validate_solution_against_bks(
    solution: Solution,
    bks_k: int,
    bks_d: float
) -> dict:
    """
    Validate solution against Best Known Solution (BKS) benchmarks.
    
    Args:
        solution: Solution to validate
        bks_k: Best known number of vehicles
        bks_d: Best known total distance
        
    Returns:
        Dictionary with validation results
    """
    k_gap = 100.0 * (solution.num_vehicles - bks_k) / bks_k if bks_k > 0 else float('inf')
    d_gap = 100.0 * (solution.total_distance - bks_d) / bks_d if bks_d > 0 else float('inf')
    
    return {
        'num_vehicles': solution.num_vehicles,
        'total_distance': solution.total_distance,
        'bks_vehicles': bks_k,
        'bks_distance': bks_d,
        'k_gap_percent': k_gap,
        'd_gap_percent': d_gap,
        'vehicles_match_bks': solution.num_vehicles == bks_k,
        'distance_match_bks': abs(solution.total_distance - bks_d) < 0.01,
    }
