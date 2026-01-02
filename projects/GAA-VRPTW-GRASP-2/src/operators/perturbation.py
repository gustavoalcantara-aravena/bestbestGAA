"""
Perturbation and Repair Operators for VRPTW

Perturbation: Destroy solutions to escape local optima (for metaheuristics)
Repair: Fix infeasible solutions by repairing constraint violations
"""

import random
from copy import deepcopy
from typing import Set, List, Optional

from src.core import Route, Solution, Instance
from src.operators.base import PerturbationOperator, RepairOperator


# ============================================================================
# PERTURBATION OPERATORS
# ============================================================================

class EjectionChain(PerturbationOperator):
    """
    Ejection chain operator: Remove customers in cascading manner.
    
    Removing one customer may force removal of others due to
    capacity or time constraints, creating a chain reaction.
    
    Complexity: Variable
    """
    
    def __init__(self, chain_length: int = 3):
        """
        Initialize ejection chain.
        
        Args:
            chain_length: Maximum number of customers to eject
        """
        super().__init__("EjectionChain")
        self.chain_length = chain_length
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply ejection chain perturbation.
        
        Args:
            solution: Current solution
            
        Returns:
            Perturbed solution
        """
        perturbed = deepcopy(solution)
        
        # Select random customer to eject
        all_customers = []
        for route in perturbed.routes:
            all_customers.extend(route.sequence[1:-1])  # Exclude depot
        
        if not all_customers:
            return solution
        
        ejected = set()
        to_process = {random.choice(all_customers)}
        
        for _ in range(self.chain_length):
            if not to_process:
                break
            
            cust = to_process.pop()
            if cust in ejected:
                continue
            
            ejected.add(cust)
            
            # Remove customer from route
            for route in perturbed.routes:
                if cust in route.sequence:
                    route.remove_customer(cust)
                    
                    # Check if other customers now violate constraints
                    # and should be ejected
                    if not route.is_feasible:
                        # Find customers causing infeasibility
                        cands = route.sequence[1:-1]
                        if cands:
                            to_process.add(random.choice(cands))
        
        # Reinsert ejected customers greedily
        for cust in ejected:
            self._reinsert_customer(perturbed, cust)
        
        return perturbed
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Greedily reinsert customer into solution."""
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                prev = route.sequence[pos - 1]
                next_cust = route.sequence[pos]
                
                old_dist = route._distance(prev, next_cust)
                new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
        
        if best_route is not None:
            best_route.add_customer(customer_id, best_pos)


class RuinRecreate(PerturbationOperator):
    """
    Ruin and Recreate operator: Destroy and rebuild portion of solution.
    
    Removes random customers (ruin) then reinserts greedily (recreate).
    Core idea of Large Neighborhood Search.
    
    Complexity: O(n²)
    """
    
    def __init__(self, destroy_ratio: float = 0.2):
        """
        Initialize ruin & recreate.
        
        Args:
            destroy_ratio: Fraction of customers to destroy (0-1)
        """
        super().__init__("RuinRecreate")
        self.destroy_ratio = destroy_ratio
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply ruin and recreate perturbation.
        
        Args:
            solution: Current solution
            
        Returns:
            Perturbed solution
        """
        perturbed = deepcopy(solution)
        
        # Collect all customers
        all_customers = []
        for route in perturbed.routes:
            all_customers.extend(route.sequence[1:-1])
        
        if not all_customers:
            return solution
        
        # Ruin: remove random customers
        num_destroy = max(1, int(len(all_customers) * self.destroy_ratio))
        to_remove = random.sample(all_customers, num_destroy)
        
        for route in perturbed.routes:
            for cust in to_remove:
                route.remove_customer(cust)
        
        # Recreate: reinsert greedily
        for cust in to_remove:
            self._reinsert_customer(perturbed, cust)
        
        return perturbed
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Greedily reinsert customer into solution."""
        instance = solution.instance
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        # Try all routes and positions
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                prev = route.sequence[pos - 1]
                next_cust = route.sequence[pos]
                
                old_dist = route._distance(prev, next_cust)
                new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
        
        # Also consider new route
        new_route_cost = 2 * solution.instance.get_distance(0, customer_id)
        if new_route_cost < best_cost:
            new_route = Route(vehicle_id=len(solution.routes), 
                            sequence=[0, customer_id, 0], 
                            instance=solution.instance)
            solution.routes.append(new_route)
        elif best_route is not None:
            best_route.add_customer(customer_id, best_pos)


class RandomRemoval(PerturbationOperator):
    """
    Random removal operator: Remove k random customers and reinsert.
    
    Similar to RuinRecreate but with fixed number of customers.
    Complexity: O(n²)
    """
    
    def __init__(self, num_remove: int = 5):
        """
        Initialize random removal.
        
        Args:
            num_remove: Number of customers to remove
        """
        super().__init__("RandomRemoval")
        self.num_remove = num_remove
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply random removal perturbation.
        
        Args:
            solution: Current solution
            
        Returns:
            Perturbed solution
        """
        perturbed = deepcopy(solution)
        
        # Collect customers
        all_customers = []
        for route in perturbed.routes:
            all_customers.extend(route.sequence[1:-1])
        
        if len(all_customers) <= self.num_remove:
            return solution
        
        # Remove random customers
        to_remove = random.sample(all_customers, self.num_remove)
        
        for route in perturbed.routes:
            for cust in to_remove:
                route.remove_customer(cust)
        
        # Reinsert greedily
        for cust in to_remove:
            self._reinsert_customer(perturbed, cust)
        
        return perturbed
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Greedy reinsertion."""
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                prev = route.sequence[pos - 1]
                next_cust = route.sequence[pos]
                
                old_dist = route._distance(prev, next_cust)
                new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
        
        if best_route is not None:
            best_route.add_customer(customer_id, best_pos)


class RouteElimination(PerturbationOperator):
    """
    Route elimination operator: Remove an entire route and redistribute customers.
    
    Useful for reducing K (number of vehicles) - the primary objective.
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("RouteElimination")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply route elimination perturbation.
        
        Args:
            solution: Current solution
            
        Returns:
            Perturbed solution with one fewer route
        """
        perturbed = deepcopy(solution)
        
        # Must have multiple routes
        if len(perturbed.routes) <= 1:
            return solution
        
        # Select route to eliminate
        eliminate_route = random.choice(perturbed.routes)
        customers_to_reinsert = eliminate_route.sequence[1:-1].copy()
        
        perturbed.routes.remove(eliminate_route)
        
        # Reinsert customers into remaining routes
        for cust in customers_to_reinsert:
            self._reinsert_customer(perturbed, cust)
        
        return perturbed
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Greedy reinsertion."""
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                prev = route.sequence[pos - 1]
                next_cust = route.sequence[pos]
                
                old_dist = route._distance(prev, next_cust)
                new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
        
        if best_route is not None:
            best_route.add_customer(customer_id, best_pos)


# ============================================================================
# REPAIR OPERATORS
# ============================================================================

class RepairCapacity(RepairOperator):
    """
    Repair capacity violations: Remove customers from overloaded routes.
    
    Find overloaded routes and remove least important customers,
    then reinsert into other routes.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("RepairCapacity")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Repair capacity constraint violations.
        
        Args:
            solution: Solution (may be infeasible)
            
        Returns:
            Feasible solution with regard to capacity
        """
        repaired = deepcopy(solution)
        
        # Find overloaded routes
        to_reinsert = []
        
        for route in repaired.routes:
            while route.total_load > repaired.instance.Q_capacity:
                # Remove least important customer (least demand? Last added?)
                cust_to_remove = route.sequence[-2]  # Last customer before depot
                to_reinsert.append(cust_to_remove)
                route.remove_customer(cust_to_remove)
        
        # Reinsert customers
        for cust in to_reinsert:
            self._reinsert_customer(repaired, cust)
        
        return repaired
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Reinsert customer respecting capacity."""
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        for route in solution.routes:
            cust_demand = solution.instance.get_customer(customer_id).demand
            
            # Check if customer fits in route
            if route.total_load + cust_demand <= solution.instance.Q_capacity:
                for pos in range(1, len(route.sequence)):
                    prev = route.sequence[pos - 1]
                    next_cust = route.sequence[pos]
                    
                    old_dist = route._distance(prev, next_cust)
                    new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                    cost = new_dist - old_dist
                    
                    if cost < best_cost:
                        best_cost = cost
                        best_route = route
                        best_pos = pos
        
        if best_route is not None:
            best_route.add_customer(customer_id, best_pos)


class RepairTimeWindows(RepairOperator):
    """
    Repair time window violations: Adjust routes to respect time constraints.
    
    Can move customers, wait at locations, or remove/relocate customers
    if time windows cannot be satisfied.
    
    Complexity: O(n²)
    CRITICAL operator for VRPTW
    """
    
    def __init__(self):
        super().__init__("RepairTimeWindows")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Repair time window constraint violations.
        
        Args:
            solution: Solution (may violate time windows)
            
        Returns:
            Feasible solution with regard to time windows
        """
        repaired = deepcopy(solution)
        to_reinsert = []
        
        # Check each route for time window violations
        for route in repaired.routes:
            # Forward pass: check time feasibility
            current_time = 0
            violated = []
            
            for i, cust_id in enumerate(route.sequence):
                cust = repaired.instance.get_customer(cust_id)
                
                if cust_id != 0:  # Not depot
                    # Arrival time after wait
                    arrival = current_time
                    
                    if arrival > cust.due_date:
                        violated.append((i, cust_id))
                    else:
                        # Wait if necessary
                        if arrival < cust.ready_time:
                            current_time = cust.ready_time
                        else:
                            current_time = arrival
                        
                        current_time += cust.service_time
                    
                    # Travel to next
                    if i < len(route.sequence) - 1:
                        next_id = route.sequence[i + 1]
                        current_time += route._distance(cust_id, next_id)
            
            # Remove violated customers and reinsert
            for _, cust_id in violated:
                route.remove_customer(cust_id)
                to_reinsert.append(cust_id)
        
        # Reinsert customers respecting time windows
        for cust in to_reinsert:
            self._reinsert_customer(repaired, cust)
        
        return repaired
    
    def _reinsert_customer(self, solution: Solution, customer_id: int):
        """Reinsert customer respecting time windows."""
        cust = solution.instance.get_customer(customer_id)
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                # Check if feasible at this position
                test_seq = route.sequence[:pos] + [customer_id] + route.sequence[pos:]
                
                # Simulate time feasibility
                time = 0
                feasible = True
                
                for i, cid in enumerate(test_seq):
                    c = solution.instance.get_customer(cid)
                    
                    if cid != 0:
                        arrival = time
                        if arrival > c.due_date:
                            feasible = False
                            break
                        
                        time = max(arrival, c.ready_time) + c.service_time
                    
                    if i < len(test_seq) - 1:
                        next_id = test_seq[i + 1]
                        time += route._distance(cid, next_id)
                
                if feasible:
                    old_dist = route._distance(route.sequence[pos-1], route.sequence[pos])
                    new_dist = route._distance(route.sequence[pos-1], customer_id) + route._distance(customer_id, route.sequence[pos])
                    cost = new_dist - old_dist
                    
                    if cost < best_cost:
                        best_cost = cost
                        best_route = route
                        best_pos = pos
        
        if best_route is not None:
            best_route.add_customer(customer_id, best_pos)


class GreedyRepair(RepairOperator):
    """
    Greedy repair: Reconstruct solution from scratch if too many violations.
    
    Used after large destruction to rebuild complete, feasible solution
    using greedy insertion.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("GreedyRepair")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Greedily repair solution.
        
        Args:
            solution: Solution to repair
            
        Returns:
            Complete, feasible solution
        """
        repaired = deepcopy(solution)
        
        # Collect all customers (visited or not)
        visited = set()
        for route in repaired.routes:
            visited.update(route.sequence[1:-1])
        
        unvisited = set(range(1, repaired.instance.n_customers + 1)) - visited
        
        # If too many unvisited, rebuild from scratch
        if len(unvisited) > len(visited):
            # Start fresh with empty routes
            repaired.routes = []
        
        # Greedily insert unvisited customers
        for cust in unvisited:
            self._insert_customer_greedy(repaired, cust)
        
        return repaired
    
    def _insert_customer_greedy(self, solution: Solution, customer_id: int):
        """Greedily insert customer at cheapest position."""
        best_route = None
        best_pos = None
        best_cost = float('inf')
        
        # Try all routes
        for route in solution.routes:
            for pos in range(1, len(route.sequence)):
                prev = route.sequence[pos - 1]
                next_cust = route.sequence[pos]
                
                old_dist = route._distance(prev, next_cust)
                new_dist = route._distance(prev, customer_id) + route._distance(customer_id, next_cust)
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
        
        # Consider new route
        new_route_cost = 2 * solution.instance.get_distance(0, customer_id)
        if new_route_cost < best_cost:
            new_route = Route(vehicle_id=len(solution.routes), 
                            sequence=[0, customer_id, 0], 
                            instance=solution.instance)
            solution.routes.append(new_route)
        elif best_route is not None:
            best_route.add_customer(customer_id, best_pos)
