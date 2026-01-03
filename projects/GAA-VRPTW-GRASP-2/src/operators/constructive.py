"""
Constructive Operators for VRPTW

Build initial feasible solutions from scratch using various heuristics.
Includes: Savings, NearestNeighbor, TimeOrientedNN, InsertionI1, RegretInsertion, RandomizedInsertion
"""

import random
import math
from typing import List, Set, Optional, Tuple
from copy import deepcopy

from src.core import Customer, Route, Instance, Solution
from src.operators.base import ConstructiveOperator


class SavingsHeuristic(ConstructiveOperator):
    """
    Clarke-Wright savings heuristic.
    
    Builds solution by computing savings for merging routes and greedily 
    merging routes with highest savings.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("SavingsHeuristic")
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build initial solution using savings heuristic.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution
        """
        n = instance.n_customers
        depot = instance.get_customer(0)
        
        # Start with each customer in its own route
        routes = []
        for i in range(1, n + 1):
            route = Route(vehicle_id=len(routes), sequence=[0, i, 0], instance=instance)
            routes.append(route)
        
        # Calculate savings for all pairs
        savings = {}
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                ci = instance.get_customer(i)
                cj = instance.get_customer(j)
                
                d_i_j = instance.get_distance(i, j)
                d_i_depot = instance.get_distance(i, 0)
                d_j_depot = instance.get_distance(j, 0)
                
                s_ij = d_i_depot + d_j_depot - d_i_j
                savings[(i, j)] = s_ij
        
        # Sort savings in descending order
        sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)
        
        # Merge routes based on savings
        merged = set()
        for (i, j), saving in sorted_savings:
            if i in merged or j in merged:
                continue
            
            # Find routes containing i and j
            route_i = None
            route_j = None
            for r in routes:
                if i in r.sequence:
                    route_i = r
                if j in r.sequence:
                    route_j = r
            
            if route_i is None or route_j is None or route_i == route_j:
                continue
            
            # Try to merge routes (join at i and j)
            # Remove depot from ends
            seq_i = route_i.sequence[1:-1]  # Remove 0s
            seq_j = route_j.sequence[1:-1]
            
            # Check if i is at end and j is at end
            if seq_i[-1] == i and seq_j[0] == j:
                merged_seq = [0] + seq_i + seq_j + [0]
                merged_route = Route(vehicle_id=route_i.vehicle_id, sequence=merged_seq, instance=instance)
                
                if merged_route.is_feasible:
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append(merged_route)
                    merged.add(i)
                    merged.add(j)
        
        # Renumber vehicles
        for idx, route in enumerate(routes):
            route.vehicle_id = idx
        
        return Solution(instance=instance, routes=routes)


class NearestNeighbor(ConstructiveOperator):
    """
    Nearest neighbor heuristic.
    
    Greedy: Start from depot, always go to nearest unvisited customer.
    Does NOT consider time windows.
    
    Complexity: O(n²)
    """
    
    def __init__(self, start_customer: int = 0):
        super().__init__("NearestNeighbor")
        self.start_customer = start_customer
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build solution using nearest neighbor.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution (may not be)
        """
        n = instance.n_customers
        unvisited = set(range(1, n + 1))
        routes = []  # ✅ ACCUMULATE ALL ROUTES
        route_sequence = [0]
        current = 0
        total_load = 0
        
        while unvisited:
            # Find nearest unvisited customer
            nearest = None
            min_dist = float('inf')
            
            for cand in unvisited:
                dist = instance.get_distance(current, cand)
                if dist < min_dist:
                    min_dist = dist
                    nearest = cand
            
            # Check if can visit nearest (capacity)
            demand = instance.get_customer(nearest).demand
            if total_load + demand > instance.Q_capacity:
                # Start new route - ✅ ACCUMULATE PREVIOUS ROUTE
                route_sequence.append(0)
                route = Route(vehicle_id=len(routes), sequence=route_sequence, instance=instance)
                routes.append(route)  # ✅ ADD TO ROUTES LIST
                
                total_load = 0
                current = 0
                route_sequence = [0]
            
            # Add to current route
            route_sequence.append(nearest)
            unvisited.remove(nearest)
            current = nearest
            total_load += demand
        
        # ✅ CLOSE AND ADD FINAL ROUTE
        route_sequence.append(0)
        route = Route(vehicle_id=len(routes), sequence=route_sequence, instance=instance)
        routes.append(route)  # ✅ ADD FINAL ROUTE
        
        return Solution(instance=instance, routes=routes)  # ✅ RETURN ALL ROUTES


class TimeOrientedNN(ConstructiveOperator):
    """
    Time-oriented nearest neighbor.
    
    Greedy with time window consideration: prioritize customers with
    urgent due dates.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("TimeOrientedNN")
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build solution using time-oriented nearest neighbor.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution
        """
        n = instance.n_customers
        unvisited = set(range(1, n + 1))
        routes = []
        
        while unvisited:
            route_sequence = [0]
            current = 0
            current_time = 0
            total_load = 0
            route_visited = set()
            
            while unvisited and total_load < instance.Q_capacity:
                # Find best next customer (considering time urgency)
                best_cand = None
                best_score = float('inf')
                
                for cand in unvisited - route_visited:
                    cand_obj = instance.get_customer(cand)
                    dist = instance.get_distance(current, cand)
                    arrival = current_time + dist
                    
                    # Can visit?
                    if arrival <= cand_obj.due_date:
                        wait_time = max(0, cand_obj.ready_time - arrival)
                        urgency = cand_obj.due_date / (instance.n_customers * 100 + 1)  # Normalize
                        
                        # Score: prefer urgent customers (high due date) and nearby
                        score = dist / (1 + urgency)
                        
                        if score < best_score:
                            best_score = score
                            best_cand = cand
                
                if best_cand is None:
                    break  # No more customers can be visited from here
                
                # Add to route
                best_obj = instance.get_customer(best_cand)
                route_sequence.append(best_cand)
                route_visited.add(best_cand)
                unvisited.discard(best_cand)
                
                dist = instance.get_distance(current, best_cand)
                current_time += dist + best_obj.service_time
                total_load += best_obj.demand
                current = best_cand
            
            route_sequence.append(0)
            if len(route_sequence) > 2:  # At least one customer
                route = Route(vehicle_id=len(routes), sequence=route_sequence, instance=instance)
                routes.append(route)
        
        return Solution(instance=instance, routes=routes)


class InsertionI1(ConstructiveOperator):
    """
    Sequential insertion heuristic (I1 variant).
    
    Build solution by inserting customers one by one at positions that
    minimize cost increase.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("InsertionI1")
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build solution using insertion heuristic.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution
        """
        n = instance.n_customers
        uninserted = set(range(1, n + 1))
        
        # Start with two furthest customers
        max_dist = 0
        start_pair = (1, 2)
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                d = instance.get_distance(i, j)
                if d > max_dist:
                    max_dist = d
                    start_pair = (i, j)
        
        routes = [Route(vehicle_id=0, sequence=[0, start_pair[0], start_pair[1], 0], instance=instance)]
        uninserted.discard(start_pair[0])
        uninserted.discard(start_pair[1])
        
        # Insert remaining customers
        while uninserted:
            best_customer = None
            best_route_idx = None
            best_position = None
            best_cost = float('inf')
            
            # Find cheapest insertion
            for cust in uninserted:
                for r_idx, route in enumerate(routes):
                    for pos in range(1, len(route.sequence) - 1):
                        # Calculate cost of inserting at this position
                        prev_cust = route.sequence[pos - 1]
                        next_cust = route.sequence[pos]
                        
                        curr_edge = instance.get_distance(prev_cust, next_cust)
                        new_edges = (instance.get_distance(prev_cust, cust) + 
                                    instance.get_distance(cust, next_cust))
                        cost_increase = new_edges - curr_edge
                        
                        if cost_increase < best_cost:
                            best_cost = cost_increase
                            best_customer = cust
                            best_route_idx = r_idx
                            best_position = pos
            
            # Try to insert in new route if no good position found
            if best_customer is None:
                # Create new route
                new_route = Route(vehicle_id=len(routes), sequence=[0, list(uninserted)[0], 0], instance=instance)
                routes.append(new_route)
                uninserted.pop()
            else:
                # Insert in best position
                routes[best_route_idx].add_customer(best_customer, best_position)
                uninserted.discard(best_customer)
        
        return Solution(instance=instance, routes=routes)


class RegretInsertion(ConstructiveOperator):
    """
    Regret insertion heuristic.
    
    Insert customer where the difference between best and second-best
    insertion position is greatest (highest "regret").
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("RegretInsertion")
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build solution using regret insertion.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution
        """
        n = instance.n_customers
        uninserted = set(range(1, n + 1))
        
        # Start with depot
        routes = [Route(vehicle_id=0, sequence=[0, 0], instance=instance)]
        
        while uninserted:
            best_regret = -1
            best_customer = None
            best_route = None
            best_pos = None
            
            # Calculate regret for each customer
            for cust in uninserted:
                costs = []
                
                # Find two cheapest insertion positions across all routes
                for route in routes:
                    for pos in range(1, len(route.sequence)):
                        prev_cust = route.sequence[pos - 1]
                        next_cust = route.sequence[pos]
                        
                        curr_edge = instance.get_distance(prev_cust, next_cust)
                        new_edges = (instance.get_distance(prev_cust, cust) + 
                                    instance.get_distance(cust, next_cust))
                        cost = new_edges - curr_edge
                        
                        costs.append((cost, route, pos))
                
                # Also consider new route
                cost_new_route = 2 * instance.get_distance(0, cust)
                costs.append((cost_new_route, None, None))
                
                if len(costs) < 2:
                    costs.append((float('inf'), None, None))
                
                costs.sort()
                regret = costs[1][0] - costs[0][0]
                
                if regret > best_regret:
                    best_regret = regret
                    best_customer = cust
                    best_route = costs[0][1]
                    best_pos = costs[0][2]
            
            # Insert customer
            if best_route is None:
                new_route = Route(vehicle_id=len(routes), sequence=[0, best_customer, 0], instance=instance)
                routes.append(new_route)
            else:
                best_route.add_customer(best_customer, best_pos)
            
            uninserted.discard(best_customer)
        
        return Solution(instance=instance, routes=routes)


class RandomizedInsertion(ConstructiveOperator):
    """
    Randomized insertion heuristic (GRASP-style).
    
    Build solution using insertion with random element (RCL - Restricted Candidate List).
    This is the PREFERRED constructor for GRASP phase.
    
    Complexity: O(n)
    """
    
    def __init__(self, alpha: float = 0.15, seed: Optional[int] = None):
        """
        Initialize randomized insertion.
        
        Args:
            alpha: RCL parameter (0-1). Lower = more restrictive = more random
            seed: Random seed for reproducibility
        """
        super().__init__("RandomizedInsertion")
        self.alpha = alpha
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def apply(self, instance: Instance) -> Solution:
        """
        Build solution using randomized insertion.
        
        Args:
            instance: Problem instance
            
        Returns:
            Feasible solution
        """
        n = instance.n_customers
        uninserted = set(range(1, n + 1))
        routes = [Route(vehicle_id=0, sequence=[0, 0], instance=instance)]
        
        while uninserted:
            # Find insertion costs for all customers
            candidates = []
            
            for cust in uninserted:
                cust_demand = instance.get_customer(cust).demand
                best_cost = float('inf')
                best_slot = None
                
                for r_idx, route in enumerate(routes):
                    # ✅ CHECK CAPACITY BEFORE EVALUATING INSERTION
                    route_load = sum(instance.get_customer(c).demand for c in route.sequence[1:-1])
                    if route_load + cust_demand > instance.Q_capacity:
                        continue  # Skip this route - customer doesn't fit
                    
                    for pos in range(1, len(route.sequence)):
                        prev_cust = route.sequence[pos - 1]
                        next_cust = route.sequence[pos]
                        
                        curr_edge = instance.get_distance(prev_cust, next_cust)
                        new_edges = (instance.get_distance(prev_cust, cust) + 
                                    instance.get_distance(cust, next_cust))
                        cost = new_edges - curr_edge
                        
                        if cost < best_cost:
                            best_cost = cost
                            best_slot = (r_idx, pos)
                
                # ✅ ALWAYS CONSIDER NEW ROUTE AS OPTION
                candidates.append((cust, best_cost, best_slot))
            
            # Build RCL (Restricted Candidate List)
            candidates.sort(key=lambda x: x[1])
            min_cost = candidates[0][1]
            max_cost = candidates[-1][1]
            threshold = min_cost + self.alpha * (max_cost - min_cost)
            
            rcl = [c for c in candidates if c[1] <= threshold]
            
            # ✅ HANDLE EMPTY RCL
            if not rcl:
                rcl = [candidates[0]]  # At least include the best option
            
            # Randomly select from RCL
            selected = random.choice(rcl)
            cust, cost, best_slot = selected
            
            if best_slot is None:
                # New route (customer doesn't fit in any existing route)
                new_route = Route(vehicle_id=len(routes), sequence=[0, cust, 0], instance=instance)
                routes.append(new_route)
            else:
                r_idx, pos = best_slot
                routes[r_idx].add_customer(cust, pos)
            
            uninserted.discard(cust)
        
        return Solution(instance=instance, routes=routes)
