"""
Intra-Route Local Search Operators for VRPTW

Improve single routes by modifying their structure.
Operators: TwoOpt, OrOpt, Relocate, ThreeOpt

These are the most effective local search operators for VRPTW.
"""

import random
from copy import deepcopy
from typing import Optional, Tuple

from src.core import Route, Solution, Instance
from src.operators.base import LocalSearchIntraOperator


class TwoOpt(LocalSearchIntraOperator):
    """
    2-opt local search operator (most fundamental).
    
    Remove two edges and reverse the segment between them.
    Complexity: O(n²) per route
    Effectiveness: Very high for VRPTW
    """
    
    def __init__(self, first_improvement: bool = False):
        """
        Initialize 2-opt.
        
        Args:
            first_improvement: If True, return first improving move (faster).
                               If False, find best improving move (better quality).
        """
        super().__init__("TwoOpt")
        self.first_improvement = first_improvement
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply 2-opt to all routes in solution.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution (or original if no improvement found)
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        for route in improved_solution.routes:
            if self._improve_route(route):
                improved = True
        
        return improved_solution if improved else solution
    
    def _improve_route(self, route: Route) -> bool:
        """
        Apply 2-opt to a single route.
        
        Args:
            route: Route to improve
            
        Returns:
            True if route was improved, False otherwise
        """
        seq = route.sequence
        n = len(seq)
        
        if n <= 4:  # Need at least [0, c1, c2, 0]
            return False
        
        best_delta = 0
        best_i = None
        best_j = None
        
        # Try all possible 2-opt moves
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                # Current edges: (seq[i-1], seq[i]) and (seq[j], seq[j+1])
                # New edges: (seq[i-1], seq[j]) and (seq[i], seq[j+1])
                
                old_dist = (route._distance(seq[i-1], seq[i]) + 
                           route._distance(seq[j], seq[j+1]))
                new_dist = (route._distance(seq[i-1], seq[j]) + 
                           route._distance(seq[i], seq[j+1]))
                
                delta = old_dist - new_dist
                
                if delta > best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j
                    
                    if self.first_improvement:
                        break
            
            if self.first_improvement and best_delta > 0:
                break
        
        # Apply best move if any improvement found
        if best_delta > 0:
            # Reverse segment [best_i:best_j+1]
            route.sequence[best_i:best_j+1] = reversed(route.sequence[best_i:best_j+1])
            route._distance_cache.clear()
            return True
        
        return False


class OrOpt(LocalSearchIntraOperator):
    """
    Or-opt operator: Relocate sequences of 1-3 customers.
    
    More flexible than 2-opt, can move customer sequences to other positions.
    Complexity: O(n³)
    """
    
    def __init__(self, max_sequence_length: int = 3):
        """
        Initialize Or-opt.
        
        Args:
            max_sequence_length: Maximum customers to move together (1-3)
        """
        super().__init__("OrOpt")
        self.max_sequence_length = min(max_sequence_length, 3)
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply Or-opt to all routes.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        for route in improved_solution.routes:
            if self._improve_route(route):
                improved = True
        
        return improved_solution if improved else solution
    
    def _improve_route(self, route: Route) -> bool:
        """
        Apply Or-opt to a single route.
        
        Args:
            route: Route to improve
            
        Returns:
            True if improved, False otherwise
        """
        seq = route.sequence
        n = len(seq)
        
        if n <= 4:
            return False
        
        best_delta = 0
        best_seq_len = None
        best_start = None
        best_insert_pos = None
        
        # Try sequences of length 1, 2, 3
        for seq_len in range(1, min(self.max_sequence_length + 1, n - 2)):
            # Try all starting positions for the sequence
            for start in range(1, n - seq_len - 1):
                # Try all insertion positions
                for insert_pos in range(1, n - 1):
                    if insert_pos >= start and insert_pos <= start + seq_len:
                        continue  # Skip if overlapping
                    
                    # Calculate cost change
                    # Remove edges around sequence
                    remove_cost = (route._distance(seq[start-1], seq[start]) +
                                 route._distance(seq[start+seq_len-1], seq[start+seq_len]))
                    
                    # Add edge to skip sequence
                    skip_cost = route._distance(seq[start-1], seq[start+seq_len])
                    
                    # Remove edge at insert position
                    insert_remove_cost = route._distance(seq[insert_pos-1], seq[insert_pos])
                    
                    # Add edges for insertion
                    insert_add_cost = (route._distance(seq[insert_pos-1], seq[start]) +
                                      route._distance(seq[start+seq_len-1], seq[insert_pos]))
                    
                    delta = (remove_cost + insert_remove_cost) - (skip_cost + insert_add_cost)
                    
                    if delta > best_delta:
                        best_delta = delta
                        best_seq_len = seq_len
                        best_start = start
                        best_insert_pos = insert_pos
        
        # Apply best move
        if best_delta > 0:
            extracted = seq[best_start:best_start + best_seq_len]
            del seq[best_start:best_start + best_seq_len]
            
            # Adjust insert position if needed
            insert_pos = best_insert_pos
            if best_insert_pos > best_start:
                insert_pos -= best_seq_len
            
            seq[insert_pos:insert_pos] = extracted
            route._distance_cache.clear()
            return True
        
        return False


class Relocate(LocalSearchIntraOperator):
    """
    Relocate operator: Move a single customer to another position in the SAME route.
    
    Simpler version of Or-opt with sequence length = 1.
    Complexity: O(n²)
    """
    
    def __init__(self):
        super().__init__("Relocate")
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply Relocate to all routes.
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        for route in improved_solution.routes:
            if self._improve_route(route):
                improved = True
        
        return improved_solution if improved else solution
    
    def _improve_route(self, route: Route) -> bool:
        """
        Apply Relocate to a single route.
        
        Args:
            route: Route to improve
            
        Returns:
            True if improved, False otherwise
        """
        seq = route.sequence
        n = len(seq)
        
        if n <= 4:
            return False
        
        best_delta = 0
        best_cust = None
        best_pos = None
        
        # Try relocating each customer
        for cust_pos in range(1, n - 1):
            cust = seq[cust_pos]
            
            # Cost of removing customer
            remove_cost = (route._distance(seq[cust_pos-1], seq[cust_pos]) +
                          route._distance(seq[cust_pos], seq[cust_pos+1]))
            skip_cost = route._distance(seq[cust_pos-1], seq[cust_pos+1])
            
            # Try inserting at other positions
            for insert_pos in range(1, n - 1):
                if abs(insert_pos - cust_pos) <= 1:
                    continue  # Skip adjacent positions (no improvement)
                
                # Cost of insertion
                insert_remove_cost = route._distance(seq[insert_pos-1], seq[insert_pos])
                insert_add_cost = (route._distance(seq[insert_pos-1], cust) +
                                 route._distance(cust, seq[insert_pos]))
                
                delta = (remove_cost + insert_remove_cost) - (skip_cost + insert_add_cost)
                
                if delta > best_delta:
                    best_delta = delta
                    best_cust = cust_pos
                    best_pos = insert_pos
        
        # Apply best move
        if best_delta > 0:
            cust = seq.pop(best_cust)
            insert_pos = best_pos
            if best_pos > best_cust:
                insert_pos -= 1
            seq.insert(insert_pos, cust)
            route._distance_cache.clear()
            return True
        
        return False


class ThreeOpt(LocalSearchIntraOperator):
    """
    3-opt operator: Remove three edges and reconnect (more powerful than 2-opt).
    
    Can create more complex rearrangements than 2-opt.
    Complexity: O(n⁴) - expensive but very effective
    Use only when 2-opt no longer improves.
    """
    
    def __init__(self, max_iterations: int = 50):
        """
        Initialize 3-opt.
        
        Args:
            max_iterations: Limit iterations due to high complexity
        """
        super().__init__("ThreeOpt")
        self.max_iterations = max_iterations
    
    def apply(self, solution: Solution) -> Solution:
        """
        Apply 3-opt to all routes (limited iterations).
        
        Args:
            solution: Current solution
            
        Returns:
            Improved solution
        """
        improved_solution = deepcopy(solution)
        improved = False
        
        for route in improved_solution.routes:
            if self._improve_route(route):
                improved = True
        
        return improved_solution if improved else solution
    
    def _improve_route(self, route: Route) -> bool:
        """
        Apply 3-opt to a single route.
        
        Args:
            route: Route to improve
            
        Returns:
            True if improved, False otherwise
        """
        seq = route.sequence
        n = len(seq)
        
        if n <= 6:  # Need at least [0, c1, c2, c3, c4, 0]
            return False
        
        iterations = 0
        
        # Try all 3-opt moves (simplified version)
        for i in range(1, n - 4):
            for j in range(i + 2, n - 2):
                for k in range(j + 2, n - 1):
                    iterations += 1
                    if iterations > self.max_iterations:
                        return False
                    
                    # Current cost
                    old_cost = (route._distance(seq[i-1], seq[i]) +
                               route._distance(seq[j], seq[j+1]) +
                               route._distance(seq[k], seq[k+1]))
                    
                    # Try different reconnections (there are 7 possible ways to reconnect)
                    # This is the simplified 2-exchange between segments
                    new_cost = (route._distance(seq[i-1], seq[j]) +
                               route._distance(seq[i], seq[j+1]) +
                               route._distance(seq[k], seq[k+1]))
                    
                    if new_cost < old_cost:
                        # Apply move: reverse segment [i:j+1]
                        seq[i:j+1] = reversed(seq[i:j+1])
                        route._distance_cache.clear()
                        return True
        
        return False
