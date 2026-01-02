"""
Base Classes and Interfaces for VRPTW Operators

Defines abstract base classes for different operator types.
All operators inherit from BaseOperator and implement apply() method.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
from src.core import Solution, Instance


class BaseOperator(ABC):
    """
    Abstract base class for all VRPTW operators.
    
    Every operator must implement:
    - apply(): Apply the operator and return modified solution
    - can_apply(): Check if operator is applicable to this solution
    """
    
    def __init__(self, name: str, operator_type: str):
        """
        Initialize operator.
        
        Args:
            name: Operator identifier (e.g., "TwoOpt")
            operator_type: Category (constructive, local_search_intra, local_search_inter, 
                                     perturbation, repair)
        """
        self.name = name
        self.operator_type = operator_type
    
    @abstractmethod
    def apply(self, solution: Solution) -> Solution:
        """
        Apply operator to solution.
        
        Args:
            solution: Input solution
            
        Returns:
            Modified solution
        """
        pass
    
    @abstractmethod
    def can_apply(self, solution: Solution) -> bool:
        """
        Check if operator is applicable to this solution.
        
        Args:
            solution: Solution to check
            
        Returns:
            True if operator can be applied, False otherwise
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.name}({self.operator_type})"


class ConstructiveOperator(BaseOperator):
    """Base class for constructive operators (build initial solution)."""
    
    def __init__(self, name: str):
        super().__init__(name, "constructive")
    
    def can_apply(self, solution: Solution) -> bool:
        """Constructive operators can always create a new solution."""
        return True


class LocalSearchIntraOperator(BaseOperator):
    """Base class for intra-route local search operators."""
    
    def __init__(self, name: str):
        super().__init__(name, "local_search_intra")
    
    def can_apply(self, solution: Solution) -> bool:
        """Can apply if at least one route with 2+ customers exists."""
        return any(len(route.sequence) > 3 for route in solution.routes)  # [0, c1, c2, ..., 0]


class LocalSearchInterOperator(BaseOperator):
    """Base class for inter-route local search operators."""
    
    def __init__(self, name: str):
        super().__init__(name, "local_search_inter")
    
    def can_apply(self, solution: Solution) -> bool:
        """Can apply if at least two routes with customers exist."""
        non_empty_routes = sum(1 for route in solution.routes if len(route.sequence) > 2)
        return non_empty_routes >= 2


class PerturbationOperator(BaseOperator):
    """Base class for perturbation operators (escape local optima)."""
    
    def __init__(self, name: str):
        super().__init__(name, "perturbation")
    
    def can_apply(self, solution: Solution) -> bool:
        """Can apply if solution is feasible."""
        return solution.feasible


class RepairOperator(BaseOperator):
    """Base class for repair operators (fix infeasible solutions)."""
    
    def __init__(self, name: str):
        super().__init__(name, "repair")
    
    def can_apply(self, solution: Solution) -> bool:
        """Repair operators work on any solution, feasible or not."""
        return True
