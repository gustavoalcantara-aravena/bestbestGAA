"""
Inter-Route Local Search Operators for VRPTW

Improve solutions by moving customers between different routes.
Operators: CrossExchange, TwoOptStar, SwapCustomers, RelocateInter
"""

import random
from copy import deepcopy
from typing import Optional, Tuple

from src.core import Route, Solution
from src.operators.base import LocalSearchInterOperator


class CrossExchange(LocalSearchInterOperator):
    """
    Cross-exchange operator: Swap segments between two routes.
    
    Removes segments from two routes and exchanges them.
    Complexity: O(n⁴) - expensive but very effective
    """
    
    def __init__(self):
        super().__init__("CrossExchange")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply cross-exchange between pairs of routes.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        
        # Try all pairs of routes
        for i in range(len(improved_solution.routes)):
            for j in range(i + 1, len(improved_solution.routes)):
                if self._improve_pair(improved_solution.routes[i], improved_solution.routes[j]):
                    return improved_solution
        
        return improved_solution if improved_solution != solution else solution
    
    def _improve_pair(self, route1: Route, route2: Route) -> bool:
        """Try to improve a pair of routes via cross-exchange."""
        seq1 = route1.sequence
        seq2 = route2.sequence
        
        if len(seq1) <= 3 or len(seq2) <= 3:
            return False
        
        # Try exchanging segments of different lengths
        for seg_len1 in range(1, len(seq1) - 2):
            for start1 in range(1, len(seq1) - seg_len1):
                for seg_len2 in range(1, len(seq2) - 2):
                    for start2 in range(1, len(seq2) - seg_len2):
                        # Try exchange
                        seg1 = seq1[start1:start1 + seg_len1]
                        seg2 = seq2[start2:start2 + seg_len2]
                        
                        # Create test sequences
                        test_seq1 = seq1[:start1] + seg2 + seq1[start1 + seg_len1:]
                        test_seq2 = seq2[:start2] + seg1 + seq2[start2 + seg_len2:]
                        
                        # Calculate cost change (simplified check)
                        old_cost = route1.total_distance + route2.total_distance
                        
                        # Temporarily swap
                        route1.sequence = test_seq1
                        route2.sequence = test_seq2
                        route1._distance_cache.clear()
                        route2._distance_cache.clear()
                        
                        new_cost = route1.total_distance + route2.total_distance
                        
                        if new_cost < old_cost and route1.is_feasible and route2.is_feasible:
                            return True
                        
                        # Restore
                        route1.sequence = seq1
                        route2.sequence = seq2
                        route1._distance_cache.clear()
                        route2._distance_cache.clear()
        
        return False


class TwoOptStar(LocalSearchInterOperator):
    """
    2-opt* operator: Apply 2-opt between two different routes.
    
    Connects two routes by removing one edge from each and reconnecting.
    Complexity: O(n²) × 2
    Effectiveness: Good for load balancing between vehicles
    """
    
    def __init__(self):
        super().__init__("TwoOptStar")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply 2-opt* between pairs of routes.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        # Try all pairs of routes
        for i in range(len(improved_solution.routes)):
            for j in range(i + 1, len(improved_solution.routes)):
                if self._improve_pair(improved_solution.routes[i], improved_solution.routes[j]):
                    improved = True
        
        return improved_solution if improved else solution
    
    def _improve_pair(self, route1: Route, route2: Route) -> bool:
        """Try to improve via 2-opt* between two routes."""
        seq1 = route1.sequence
        seq2 = route2.sequence
        
        if len(seq1) <= 3 or len(seq2) <= 3:
            return False
        
        best_delta = 0
        best_i = None
        best_j = None
        
        # Try removing edge from route1 and reconnecting with route2
        for i in range(1, len(seq1) - 1):
            for j in range(1, len(seq2) - 1):
                # Cost of current edges
                old_cost = (route1._distance(seq1[i-1], seq1[i]) +
                           route2._distance(seq2[j-1], seq2[j]))
                
                # Cost of new edges (reconnect route1 to route2)
                new_cost = (route1._distance(seq1[i-1], seq2[j]) +
                           route2._distance(seq1[i], seq2[j-1]))
                
                delta = old_cost - new_cost
                if delta > best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j
        
        # Apply best move if improvement found
        if best_delta > 0:
            # Reconnect: route1 gets seq1[:best_i] + reverse(seq2[best_j:])
            # route2 gets seq2[:best_j] + reverse(seq1[best_i:])
            new_seq1 = seq1[:best_i] + list(reversed(seq2[best_j:-1])) + [0]
            new_seq2 = seq2[:best_j] + list(reversed(seq1[best_i:-1])) + [0]
            
            route1.sequence = new_seq1
            route2.sequence = new_seq2
            route1._distance_cache.clear()
            route2._distance_cache.clear()
            
            if route1.is_feasible and route2.is_feasible:
                return True
            
            # Restore if infeasible
            route1.sequence = seq1
            route2.sequence = seq2
            route1._distance_cache.clear()
            route2._distance_cache.clear()
        
        return False


class SwapCustomers(LocalSearchInterOperator):
    """
    Swap customers operator: Exchange individual customers between routes.
    
    Simple but effective: moves single customer from route i to route j
    and another from j to i.
    
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("SwapCustomers")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply customer swaps between routes.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        # Try all pairs of routes
        for i in range(len(improved_solution.routes)):
            for j in range(i + 1, len(improved_solution.routes)):
                if self._swap_pair(improved_solution.routes[i], improved_solution.routes[j]):
                    improved = True
        
        return improved_solution if improved else solution
    
    def _swap_pair(self, route1: Route, route2: Route) -> bool:
        """Try to swap customers between two routes."""
        seq1 = route1.sequence
        seq2 = route2.sequence
        
        if len(seq1) <= 3 or len(seq2) <= 3:
            return False
        
        best_delta = 0
        best_cust1 = None
        best_cust2 = None
        
        # Try all customer pairs
        for pos1 in range(1, len(seq1) - 1):
            for pos2 in range(1, len(seq2) - 1):
                cust1 = seq1[pos1]
                cust2 = seq2[pos2]
                
                # Test swap
                old_cost = route1.total_distance + route2.total_distance
                
                # Temporarily swap
                route1.sequence[pos1] = cust2
                route2.sequence[pos2] = cust1
                route1._distance_cache.clear()
                route2._distance_cache.clear()
                
                new_cost = route1.total_distance + route2.total_distance
                
                if (new_cost < old_cost and 
                    route1.is_feasible and route2.is_feasible):
                    return True
                
                # Restore
                route1.sequence[pos1] = cust1
                route2.sequence[pos2] = cust2
                route1._distance_cache.clear()
                route2._distance_cache.clear()
        
        return False


class RelocateInter(LocalSearchInterOperator):
    """
    Relocate inter-route operator: Move a customer from one route to another.
    
    Generalization of single-route Relocate to work between routes.
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("RelocateInter")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply inter-route relocations.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        # Try moving customers between routes
        for source_idx in range(len(improved_solution.routes)):
            for dest_idx in range(len(improved_solution.routes)):
                if source_idx != dest_idx:
                    if self._move_customer(improved_solution.routes[source_idx],
                                          improved_solution.routes[dest_idx]):
                        improved = True
        
        return improved_solution if improved else solution
    
    def _move_customer(self, source_route: Route, dest_route: Route) -> bool:
        """Try to move a customer from source to destination route."""
        source_seq = source_route.sequence
        dest_seq = dest_route.sequence
        
        if len(source_seq) <= 3:  # Need at least one customer
            return False
        
        best_delta = 0
        best_cust = None
        best_cust_pos = None
        best_insert_pos = None
        
        # Try moving each customer from source
        for cust_pos in range(1, len(source_seq) - 1):
            cust = source_seq[cust_pos]
            
            # Cost of removing from source
            remove_cost = (source_route._distance(source_seq[cust_pos-1], source_seq[cust_pos]) +
                          source_route._distance(source_seq[cust_pos], source_seq[cust_pos+1]))
            skip_cost = source_route._distance(source_seq[cust_pos-1], source_seq[cust_pos+1])
            
            # Try inserting in destination at all positions
            for insert_pos in range(1, len(dest_seq)):
                insert_remove_cost = dest_route._distance(dest_seq[insert_pos-1], dest_seq[insert_pos])
                insert_add_cost = (dest_route._distance(dest_seq[insert_pos-1], cust) +
                                 dest_route._distance(cust, dest_seq[insert_pos]))
                
                delta = (remove_cost + insert_remove_cost) - (skip_cost + insert_add_cost)
                
                if delta > best_delta:
                    best_delta = delta
                    best_cust = cust
                    best_cust_pos = cust_pos
                    best_insert_pos = insert_pos
        
        # Apply best move
        if best_delta > 0:
            source_route.remove_customer(best_cust)
            dest_route.add_customer(best_cust, best_insert_pos)
            
            if source_route.is_feasible and dest_route.is_feasible:
                return True
            
            # Restore if infeasible
            dest_route.remove_customer(best_cust)
            source_route.sequence.insert(best_cust_pos, best_cust)
        
        return False
