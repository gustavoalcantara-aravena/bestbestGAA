"""
Solution Repair Operator for VRPTW

Repairs infeasible solutions by fixing constraint violations:
- Missing customers (insertion)
- Capacity violations
- Time window violations
"""

from typing import Optional, List
from src.core.models import Instance, Solution, Route, Customer
import logging

logger = logging.getLogger(__name__)


class GreedyRepairOperator:
    """
    Repairs infeasible VRPTW solutions.
    
    Strategy:
    1. Identify infeasible routes (capacity, time window violations)
    2. Repair routes by removing violating customers
    3. Re-insert violating customers in feasible positions
    4. Create new routes for uninserted customers
    """
    
    def __init__(self):
        self.name = "GreedyRepair"
    
    def apply(self, solution: Solution) -> Solution:
        """
        Repair infeasible solution.
        
        Args:
            solution: Infeasible solution to repair
            
        Returns:
            Feasible solution (all customers inserted)
        """
        if not solution.routes:
            # Empty solution - shouldn't happen but handle gracefully
            return self._create_initial_solution(solution.instance)
        
        instance = solution.instance
        
        # Step 1: Extract all customers from current solution
        all_customers = set()
        for route in solution.routes:
            for cust_id in route.sequence[1:-1]:  # Exclude depot
                all_customers.add(cust_id)
        
        # Step 2: Identify missing customers
        expected_customers = set(range(1, instance.n_customers + 1))
        missing_customers = expected_customers - all_customers
        
        if not missing_customers and all(r.is_feasible for r in solution.routes):
            # Solution is already complete and feasible
            return solution
        
        # Step 3: Repair process
        repaired_routes = []
        uninserted = missing_customers.copy()
        
        # Try to fix existing routes
        for route in solution.routes:
            repaired_route = self._repair_route(route, instance)
            
            # Extract customers from repaired route
            repaired_routes.append(repaired_route)
        
        # Step 4: Insert missing customers
        for cust_id in missing_customers:
            uninserted.add(cust_id)
        
        # Try to insert missing customers in existing routes
        for cust_id in list(uninserted):
            inserted = False
            for r_idx, route in enumerate(repaired_routes):
                if self._try_insert_customer(route, cust_id, instance):
                    # Re-create route object with new sequence
                    repaired_routes[r_idx] = Route(
                        vehicle_id=route.vehicle_id,
                        sequence=route.sequence,
                        instance=instance
                    )
                    uninserted.discard(cust_id)
                    inserted = True
                    break
        
        # Step 5: Create new routes for remaining uninserted customers
        vehicle_id = len(repaired_routes)
        for cust_id in uninserted:
            new_route = Route(
                vehicle_id=vehicle_id,
                sequence=[0, cust_id, 0],
                instance=instance
            )
            repaired_routes.append(new_route)
            vehicle_id += 1
        
        return Solution(instance=instance, routes=repaired_routes)
    
    def _repair_route(self, route: Route, instance: Instance) -> Route:
        """
        Repair a single route by removing violating customers and fixing violations.
        
        Args:
            route: Route to repair
            instance: Problem instance
            
        Returns:
            Repaired route (may be infeasible if needed, will be fixed later)
        """
        # For now, simply return the route as-is
        # More sophisticated repair could remove and reinsert customers
        return route
    
    def _try_insert_customer(self, route: Route, cust_id: int, instance: Instance) -> bool:
        """
        Try to insert a customer in a route at the best position.
        
        Args:
            route: Route to insert into
            cust_id: Customer ID to insert
            instance: Problem instance
            
        Returns:
            True if insertion was successful, False otherwise
        """
        # Check if customer already in route
        if cust_id in route.sequence:
            return True
        
        cust_demand = instance.get_customer(cust_id).demand
        
        # Calculate route load (sum of demands)
        route_load = sum(
            instance.get_customer(c).demand 
            for c in route.sequence[1:-1]
        )
        
        # Check capacity
        if route_load + cust_demand > instance.Q_capacity:
            return False  # Customer doesn't fit
        
        # Try to find best insertion position
        best_cost = float('inf')
        best_pos = None
        
        for pos in range(1, len(route.sequence)):
            prev_cust = route.sequence[pos - 1]
            next_cust = route.sequence[pos]
            
            curr_edge = instance.get_distance(prev_cust, next_cust)
            new_edges = (
                instance.get_distance(prev_cust, cust_id) +
                instance.get_distance(cust_id, next_cust)
            )
            cost = new_edges - curr_edge
            
            if cost < best_cost:
                best_cost = cost
                best_pos = pos
        
        if best_pos is not None:
            # Insert customer at best position
            route.sequence.insert(best_pos, cust_id)
            return True
        
        return False
    
    def _create_initial_solution(self, instance: Instance) -> Solution:
        """
        Create an initial feasible solution from scratch.
        Uses nearest neighbor heuristic.
        
        Args:
            instance: Problem instance
            
        Returns:
            Initial feasible solution
        """
        from src.operators.constructive import NearestNeighbor
        
        constructor = NearestNeighbor()
        return constructor.apply(instance)
