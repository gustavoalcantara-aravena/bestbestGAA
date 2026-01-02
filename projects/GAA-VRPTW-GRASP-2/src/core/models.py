"""
VRPTW Core Data Models

Defines the fundamental data structures for the Vehicle Routing Problem with Time Windows:
- Customer: Individual customer with location, demand, and time window
- Route: Vehicle route with sequence of customers
- Instance: Problem instance with all customers and parameters
- Solution: Complete solution with multiple routes and fitness evaluation

All constraints are validated according to Solomon benchmark format (100 customers, euclideandistance, time windows).
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import math


@dataclass
class Customer:
    """
    Represents a single customer in the VRPTW problem.
    
    Attributes:
        id: Customer identifier (0=depot, 1-100=customers)
        x: X coordinate (cartesian)
        y: Y coordinate (cartesian)
        demand: Quantity demanded (0 for depot)
        ready_time: Earliest service start time (a_i)
        due_date: Latest service end time (b_i)
        service_time: Duration of service at this customer (s_i)
    """
    id: int
    x: float
    y: float
    demand: float
    ready_time: float
    due_date: float
    service_time: float
    
    def is_in_time_window(self, arrival_time: float) -> bool:
        """
        Check if arrival time is within the customer's time window.
        
        Args:
            arrival_time: Time when vehicle arrives at this customer
            
        Returns:
            True if ready_time <= arrival_time <= due_date, False otherwise
        """
        return self.ready_time <= arrival_time <= self.due_date
    
    def __repr__(self) -> str:
        return f"C{self.id}({self.x:.1f},{self.y:.1f})"


@dataclass
class Route:
    """
    Represents a single vehicle route in a solution.
    
    Attributes:
        vehicle_id: Unique identifier for the vehicle
        sequence: Ordered list of customer IDs in this route (includes 0 for depot at start/end)
        instance: Reference to the problem instance (for distance/time calculations)
        
    Computed Properties:
        total_distance: Sum of distances between consecutive customers
        total_load: Sum of customer demands in the route
        total_time: Total time including travel and service times
        is_feasible: Whether route satisfies capacity and time window constraints
    """
    vehicle_id: int
    sequence: List[int] = field(default_factory=list)
    instance: Optional['Instance'] = None
    _distance_cache: Dict[Tuple[int, int], float] = field(default_factory=dict, init=False, repr=False)
    
    def add_customer(self, customer_id: int, position: Optional[int] = None) -> None:
        """
        Add a customer to the route at the specified position.
        
        Args:
            customer_id: ID of customer to add
            position: Position in sequence (default: append at end before returning to depot)
        """
        if position is None:
            # Insert before the return to depot (last position is always 0)
            if self.sequence and self.sequence[-1] == 0:
                self.sequence.insert(-1, customer_id)
            else:
                self.sequence.append(customer_id)
        else:
            self.sequence.insert(position, customer_id)
    
    def remove_customer(self, customer_id: int) -> bool:
        """
        Remove a customer from the route.
        
        Args:
            customer_id: ID of customer to remove
            
        Returns:
            True if customer was found and removed, False otherwise
        """
        try:
            self.sequence.remove(customer_id)
            self._distance_cache.clear()
            return True
        except ValueError:
            return False
    
    def _distance(self, i: int, j: int) -> float:
        """Calculate euclidean distance between two customers."""
        ci = self.instance.get_customer(i)
        cj = self.instance.get_customer(j)
        return math.sqrt((ci.x - cj.x) ** 2 + (ci.y - cj.y) ** 2)
    
    @property
    def total_distance(self) -> float:
        """Calculate total distance traveled in this route."""
        if not self.sequence or len(self.sequence) < 2:
            return 0.0
        
        distance = 0.0
        for i in range(len(self.sequence) - 1):
            key = (self.sequence[i], self.sequence[i + 1])
            if key not in self._distance_cache:
                self._distance_cache[key] = self._distance(self.sequence[i], self.sequence[i + 1])
            distance += self._distance_cache[key]
        
        return distance
    
    @property
    def total_load(self) -> float:
        """Calculate total load (sum of demands) in this route."""
        return sum(self.instance.get_customer(cid).demand for cid in self.sequence if cid != 0)
    
    @property
    def total_time(self) -> float:
        """
        Calculate total time for this route including travel and service times.
        
        Returns:
            Total elapsed time from depot to depot (or inf if infeasible)
        """
        if not self.sequence or len(self.sequence) < 2:
            return 0.0
        
        current_time = 0.0
        for i, customer_id in enumerate(self.sequence):
            customer = self.instance.get_customer(customer_id)
            
            # Wait until time window opens
            if current_time < customer.ready_time:
                current_time = customer.ready_time
            
            # Check time window violation
            if current_time > customer.due_date:
                return float('inf')
            
            # Add service time
            current_time += customer.service_time
            
            # Add travel time to next customer (if not last)
            if i < len(self.sequence) - 1:
                next_id = self.sequence[i + 1]
                current_time += self._distance(customer_id, next_id)
        
        return current_time
    
    @property
    def is_feasible(self) -> bool:
        """
        Check if route satisfies all constraints:
        - Capacity: total load <= Q
        - Time windows: all customers served within time windows
        
        Returns:
            True if feasible, False otherwise
        """
        # Check capacity constraint
        if self.total_load > self.instance.Q_capacity:
            return False
        
        # Check time window constraint
        if self.total_time == float('inf'):
            return False
        
        # Check vehicle max route time if applicable
        if self.instance.max_route_time is not None and self.total_time > self.instance.max_route_time:
            return False
        
        return True
    
    def __repr__(self) -> str:
        route_str = "->".join(str(cid) for cid in self.sequence)
        return f"V{self.vehicle_id}:[{route_str}]"


@dataclass
class Instance:
    """
    Represents a complete VRPTW problem instance (Solomon benchmark format).
    
    Attributes:
        name: Instance identifier (e.g., "C101", "R103", "RC201")
        n_customers: Number of customers (typically 100 for Solomon)
        K_vehicles: Number of vehicles available
        Q_capacity: Vehicle carrying capacity
        customers: List of Customer objects (index 0 = depot)
        max_route_time: Optional maximum duration per route
        family: Solomon family classification (C1, C2, R1, R2, RC1, RC2)
    """
    name: str
    n_customers: int
    K_vehicles: int
    Q_capacity: float
    customers: List[Customer] = field(default_factory=list)
    max_route_time: Optional[float] = None
    family: Optional[str] = None
    
    def get_customer(self, customer_id: int) -> Customer:
        """
        Get customer by ID.
        
        Args:
            customer_id: Customer ID (0=depot, 1-100=customers)
            
        Returns:
            Customer object
            
        Raises:
            IndexError if customer_id is out of range
        """
        return self.customers[customer_id]
    
    def get_distance(self, i: int, j: int) -> float:
        """
        Calculate euclidean distance between two customers.
        
        Args:
            i: First customer ID
            j: Second customer ID
            
        Returns:
            Euclidean distance
        """
        ci = self.get_customer(i)
        cj = self.get_customer(j)
        return math.sqrt((ci.x - cj.x) ** 2 + (ci.y - cj.y) ** 2)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate instance integrity against Solomon constraints.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check customer count (Solomon = 100 + 1 depot)
        if self.n_customers != 100:
            errors.append(f"Expected 100 customers, got {self.n_customers}")
        
        if len(self.customers) != self.n_customers + 1:
            errors.append(f"Expected {self.n_customers + 1} customer objects (including depot), got {len(self.customers)}")
        
        # Check depot (customer 0)
        if self.customers[0].id != 0:
            errors.append("Customer 0 (depot) has incorrect ID")
        if self.customers[0].demand != 0:
            errors.append("Depot should have zero demand")
        
        # Check customer IDs are sequential
        for i, customer in enumerate(self.customers):
            if customer.id != i:
                errors.append(f"Customer at index {i} has ID {customer.id}, expected {i}")
        
        # Check parameters are non-negative
        if self.Q_capacity <= 0:
            errors.append(f"Q_capacity must be positive, got {self.Q_capacity}")
        
        for i, customer in enumerate(self.customers):
            if i == 0:  # Skip depot
                continue
            if customer.demand < 0:
                errors.append(f"Customer {customer.id} has negative demand")
            if customer.service_time < 0:
                errors.append(f"Customer {customer.id} has negative service time")
            if customer.ready_time < 0 or customer.due_date < 0:
                errors.append(f"Customer {customer.id} has invalid time window")
            if customer.ready_time > customer.due_date:
                errors.append(f"Customer {customer.id} has ready_time > due_date")
        
        return len(errors) == 0, errors
    
    def __repr__(self) -> str:
        return f"Instance({self.name}, n={self.n_customers}, K={self.K_vehicles}, Q={self.Q_capacity})"


@dataclass
class Solution:
    """
    Represents a complete solution to a VRPTW instance.
    
    Attributes:
        instance: Reference to the problem instance
        routes: List of Route objects
        
    Computed Properties:
        num_vehicles: Number of non-empty routes
        total_distance: Sum of distances across all routes (K primary)
        feasible: Whether all routes are feasible
        fitness: Tuple (K, D) for hierarchical comparison
    """
    instance: Instance
    routes: List[Route] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize routes with instance references."""
        for route in self.routes:
            if route.instance is None:
                route.instance = self.instance
    
    @property
    def num_vehicles(self) -> int:
        """Count vehicles with at least one customer."""
        return sum(1 for route in self.routes if len(route.sequence) > 2)  # sequence = [0, ..., 0]
    
    @property
    def total_distance(self) -> float:
        """Sum of distances across all routes (Primary objective K)."""
        return sum(route.total_distance for route in self.routes)
    
    @property
    def total_time(self) -> float:
        """Maximum time spent by any vehicle."""
        return max((route.total_time for route in self.routes), default=0.0)
    
    @property
    def feasible(self) -> bool:
        """Check if all routes are feasible."""
        if not all(route.is_feasible for route in self.routes):
            return False
        
        # Check that all customers are visited exactly once
        visited = set()
        for route in self.routes:
            for customer_id in route.sequence:
                if customer_id == 0:  # Depot
                    continue
                if customer_id in visited:
                    return False
                visited.add(customer_id)
        
        # Check all customers are visited
        expected_customers = set(range(1, self.instance.n_customers + 1))
        if visited != expected_customers:
            return False
        
        return True
    
    @property
    def fitness(self) -> Tuple[float, float]:
        """
        Calculate hierarchical fitness (K, D) for solution comparison.
        
        Returns:
            Tuple (K, D) where:
            - K: Number of vehicles (primary objective - minimize)
            - D: Total distance (secondary objective - minimize)
        """
        return (float(self.num_vehicles), self.total_distance)
    
    def get_fitness_gap(self, bks: Tuple[int, float]) -> Tuple[float, float]:
        """
        Calculate gap from Best Known Solution (BKS).
        
        Args:
            bks: Tuple (K_bks, D_bks) from best_known_solutions.json
            
        Returns:
            Tuple (K_gap%, D_gap%) - percentage above BKS
        """
        k_gap = 100.0 * (self.num_vehicles - bks[0]) / bks[0] if bks[0] > 0 else float('inf')
        d_gap = 100.0 * (self.total_distance - bks[1]) / bks[1] if bks[1] > 0 else float('inf')
        return (k_gap, d_gap)
    
    def is_better_than(self, other: 'Solution', strict: bool = False) -> bool:
        """
        Compare two solutions hierarchically.
        
        Args:
            other: Solution to compare with
            strict: If False, uses hierarchical (K first, then D)
                   If True, requires Pareto improvement
            
        Returns:
            True if self is better than other
        """
        if strict:
            # Pareto comparison: better or equal in all objectives, strictly better in at least one
            k_better = self.num_vehicles <= other.num_vehicles
            d_better = self.total_distance <= other.total_distance
            k_strictly = self.num_vehicles < other.num_vehicles
            d_strictly = self.total_distance < other.total_distance
            return k_better and d_better and (k_strictly or d_strictly)
        else:
            # Lexicographic: K first, then D
            if self.num_vehicles != other.num_vehicles:
                return self.num_vehicles < other.num_vehicles
            return self.total_distance < other.total_distance
    
    def to_dict(self) -> Dict:
        """
        Serialize solution to dictionary format.
        
        Returns:
            Dictionary with solution structure
        """
        return {
            "instance": self.instance.name,
            "num_vehicles": self.num_vehicles,
            "total_distance": self.total_distance,
            "total_time": self.total_time,
            "feasible": self.feasible,
            "fitness": {"K": self.num_vehicles, "D": self.total_distance},
            "routes": [
                {
                    "vehicle_id": route.vehicle_id,
                    "sequence": route.sequence,
                    "distance": route.total_distance,
                    "load": route.total_load,
                    "time": route.total_time,
                    "feasible": route.is_feasible
                }
                for route in self.routes
            ]
        }
    
    def __repr__(self) -> str:
        return f"Solution(K={self.num_vehicles}, D={self.total_distance:.2f}, feasible={self.feasible})"
