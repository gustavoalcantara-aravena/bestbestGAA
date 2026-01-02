"""
GAA: Generación Automática de Algoritmos (Automatic Algorithm Generation)

Core AST Node implementations for representing VRPTW algorithms as Abstract Syntax Trees.

AST (Abstract Syntax Tree) allows:
- Representing algorithms as tree structures
- Generating new algorithms automatically
- Evolving algorithms through genetic operators
- Executing generated algorithms

Node Types:
1. ASTNode (base class) - All nodes inherit from this
2. ControlFlow nodes - Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove
3. TerminalNodes - GreedyConstruct, LocalSearch, Perturbation, Repair
4. ParameterNodes - Alpha, K, MaxIterations, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from copy import deepcopy
import json


# ============================================================================
# BASE CLASS: ASTNode
# ============================================================================

class ASTNode(ABC):
    """
    Abstract base class for all AST nodes.
    
    Every node can:
    - Execute itself on a problem instance
    - Convert to/from dictionary representation
    - Generate pseudocode
    - Report tree metrics (size, depth)
    """
    
    @abstractmethod
    def execute(self, instance, solution):
        """
        Execute this node on the given problem instance and solution.
        
        Args:
            instance: VRPTW problem instance
            solution: Current solution
            
        Returns:
            Modified solution after execution
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ASTNode':
        """Reconstruct node from dictionary representation."""
        pass
    
    @abstractmethod
    def to_pseudocode(self, indent: int = 0) -> str:
        """Generate human-readable pseudocode."""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Total number of nodes in subtree (including self)."""
        pass
    
    @abstractmethod
    def depth(self) -> int:
        """Maximum depth from this node to any leaf."""
        pass
    
    @abstractmethod
    def clone(self) -> 'ASTNode':
        """Create deep copy of this subtree."""
        pass


# ============================================================================
# CONTROL FLOW NODES
# ============================================================================

@dataclass
class Seq(ASTNode):
    """
    Sequence node: Execute multiple statements in order.
    
    Pseudocode:
        body[0]
        body[1]
        ...
        body[n]
    
    Example:
        Seq(body=[
            GreedyConstruct(heuristic="RandomizedInsertion"),
            LocalSearch(operator="TwoOpt", max_iterations=50)
        ])
    """
    body: List[ASTNode]
    
    def execute(self, instance, solution):
        """Execute each statement in sequence."""
        for statement in self.body:
            solution = statement.execute(instance, solution)
        return solution
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Seq',
            'body': [node.to_dict() for node in self.body]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Seq':
        body = [reconstruct_node(node_dict) for node_dict in data['body']]
        return cls(body=body)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}SEQ {{"]
        for stmt in self.body:
            lines.append(stmt.to_pseudocode(indent + 1))
        lines.append(f"{ind}}}")
        return "\n".join(lines)
    
    def size(self) -> int:
        return 1 + sum(node.size() for node in self.body)
    
    def depth(self) -> int:
        if not self.body:
            return 1
        return 1 + max(node.depth() for node in self.body)
    
    def clone(self) -> 'Seq':
        return Seq(body=[node.clone() for node in self.body])


@dataclass
class While(ASTNode):
    """
    While loop: Repeatedly execute body up to max_iterations.
    
    Pseudocode:
        WHILE iterations < max_iterations:
            body
    
    Example:
        While(max_iterations=100, body=
            LocalSearch(operator="TwoOpt", max_iterations=20)
        )
    """
    max_iterations: int
    body: ASTNode
    
    def execute(self, instance, solution):
        """Execute body up to max_iterations times."""
        best = solution
        for iteration in range(self.max_iterations):
            solution = self.body.execute(instance, solution)
            # Track best improvement
            if solution.fitness < best.fitness:
                best = solution
        return best
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'While',
            'max_iterations': self.max_iterations,
            'body': self.body.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'While':
        body = reconstruct_node(data['body'])
        return cls(max_iterations=data['max_iterations'], body=body)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return (f"{ind}WHILE iterations < {self.max_iterations}:\n" +
                self.body.to_pseudocode(indent + 1))
    
    def size(self) -> int:
        return 1 + self.body.size()
    
    def depth(self) -> int:
        return 1 + self.body.depth()
    
    def clone(self) -> 'While':
        return While(max_iterations=self.max_iterations, body=self.body.clone())


@dataclass
class For(ASTNode):
    """
    For loop: Execute body N times (multi-start), keep best.
    
    Pseudocode:
        best = current
        FOR i = 1 TO iterations:
            solution = body
            IF solution better than best:
                best = solution
        RETURN best
    
    Example:
        For(iterations=5, body=
            Seq(body=[
                GreedyConstruct(heuristic="SavingsHeuristic"),
                LocalSearch(operator="TwoOpt", max_iterations=30)
            ])
        )
    """
    iterations: int
    body: ASTNode
    
    def execute(self, instance, solution):
        """Execute body N times, keep best solution."""
        best = solution
        for _ in range(self.iterations):
            current = self.body.execute(instance, deepcopy(solution))
            if current.fitness < best.fitness:
                best = current
        return best
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'For',
            'iterations': self.iterations,
            'body': self.body.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'For':
        body = reconstruct_node(data['body'])
        return cls(iterations=data['iterations'], body=body)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return (f"{ind}FOR i = 1 TO {self.iterations}:\n" +
                f"{self.body.to_pseudocode(indent + 1)}\n" +
                f"{ind}KEEP BEST")
    
    def size(self) -> int:
        return 1 + self.body.size()
    
    def depth(self) -> int:
        return 1 + self.body.depth()
    
    def clone(self) -> 'For':
        return For(iterations=self.iterations, body=self.body.clone())


@dataclass
class If(ASTNode):
    """
    Conditional: Execute then_branch or else_branch based on improvement.
    
    Pseudocode:
        improved = then_branch(solution)
        IF improved better than current:
            RETURN improved
        ELSE IF else_branch exists:
            RETURN else_branch(solution)
        ELSE:
            RETURN solution
    
    Example:
        If(then_branch=LocalSearch(operator="ThreeOpt"),
           else_branch=Perturbation(operator="RuinRecreate"))
    """
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None
    
    def execute(self, instance, solution):
        """Execute then_branch; if improves, return it; else try else_branch."""
        improved = self.then_branch.execute(instance, deepcopy(solution))
        if improved.fitness < solution.fitness:
            return improved
        elif self.else_branch is not None:
            return self.else_branch.execute(instance, solution)
        else:
            return solution
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'If',
            'then_branch': self.then_branch.to_dict(),
            'else_branch': self.else_branch.to_dict() if self.else_branch else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'If':
        then_branch = reconstruct_node(data['then_branch'])
        else_branch = reconstruct_node(data['else_branch']) if data['else_branch'] else None
        return cls(then_branch=then_branch, else_branch=else_branch)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}IF improved:"]
        lines.append(self.then_branch.to_pseudocode(indent + 1))
        if self.else_branch:
            lines.append(f"{ind}ELSE:")
            lines.append(self.else_branch.to_pseudocode(indent + 1))
        return "\n".join(lines)
    
    def size(self) -> int:
        size = 1 + self.then_branch.size()
        if self.else_branch:
            size += self.else_branch.size()
        return size
    
    def depth(self) -> int:
        max_depth = self.then_branch.depth()
        if self.else_branch:
            max_depth = max(max_depth, self.else_branch.depth())
        return 1 + max_depth
    
    def clone(self) -> 'If':
        else_branch = self.else_branch.clone() if self.else_branch else None
        return If(then_branch=self.then_branch.clone(), else_branch=else_branch)


@dataclass
class ChooseBestOf(ASTNode):
    """
    Execute multiple alternatives and return the best solution.
    
    Pseudocode:
        best = alternatives[0]
        FOR each alt in alternatives[1:]:
            current = alt
            IF current better than best:
                best = current
        RETURN best
    
    Example:
        ChooseBestOf(alternatives=[
            LocalSearch(operator="TwoOpt"),
            LocalSearch(operator="OrOpt"),
            LocalSearch(operator="ThreeOpt")
        ])
    """
    alternatives: List[ASTNode]
    
    def execute(self, instance, solution):
        """Execute each alternative, return best."""
        best = solution
        for alt in self.alternatives:
            current = alt.execute(instance, deepcopy(solution))
            if current.fitness < best.fitness:
                best = current
        return best
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'ChooseBestOf',
            'alternatives': [node.to_dict() for node in self.alternatives]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChooseBestOf':
        alternatives = [reconstruct_node(node_dict) for node_dict in data['alternatives']]
        return cls(alternatives=alternatives)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}CHOOSE BEST OF {{"]
        for i, alt in enumerate(self.alternatives):
            lines.append(f"{ind}  Option {i+1}:")
            lines.append(alt.to_pseudocode(indent + 2))
        lines.append(f"{ind}}}")
        return "\n".join(lines)
    
    def size(self) -> int:
        return 1 + sum(node.size() for node in self.alternatives)
    
    def depth(self) -> int:
        if not self.alternatives:
            return 1
        return 1 + max(node.depth() for node in self.alternatives)
    
    def clone(self) -> 'ChooseBestOf':
        return ChooseBestOf(alternatives=[node.clone() for node in self.alternatives])


@dataclass
class ApplyUntilNoImprove(ASTNode):
    """
    Apply body repeatedly until no improvement for max_no_improve iterations.
    
    Pseudocode:
        best = solution
        no_improve_count = 0
        WHILE no_improve_count < max_no_improve:
            current = body
            IF current better than best:
                best = current
                no_improve_count = 0
            ELSE:
                no_improve_count += 1
        RETURN best
    
    Example:
        ApplyUntilNoImprove(max_no_improve=20, body=
            LocalSearch(operator="TwoOpt")
        )
    """
    max_no_improve: int
    body: ASTNode
    
    def execute(self, instance, solution):
        """Apply body until no improvement for max_no_improve iterations."""
        best = solution
        no_improve_count = 0
        
        while no_improve_count < self.max_no_improve:
            current = self.body.execute(instance, deepcopy(best))
            if current.fitness < best.fitness:
                best = current
                no_improve_count = 0
            else:
                no_improve_count += 1
        
        return best
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'ApplyUntilNoImprove',
            'max_no_improve': self.max_no_improve,
            'body': self.body.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApplyUntilNoImprove':
        body = reconstruct_node(data['body'])
        return cls(max_no_improve=data['max_no_improve'], body=body)
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return (f"{ind}APPLY UNTIL NO IMPROVE FOR {self.max_no_improve}:\n" +
                self.body.to_pseudocode(indent + 1))
    
    def size(self) -> int:
        return 1 + self.body.size()
    
    def depth(self) -> int:
        return 1 + self.body.depth()
    
    def clone(self) -> 'ApplyUntilNoImprove':
        return ApplyUntilNoImprove(max_no_improve=self.max_no_improve, 
                                   body=self.body.clone())


# ============================================================================
# TERMINAL NODES (Operators)
# ============================================================================

@dataclass
class GreedyConstruct(ASTNode):
    """
    Terminal: Apply greedy constructive heuristic.
    
    Valid heuristics:
    - "NearestNeighbor"
    - "SavingsHeuristic"
    - "TimeOrientedNN"
    - "InsertionI1"
    - "RegretInsertion"
    - "RandomizedInsertion"
    """
    heuristic: str  # Constructive operator name
    
    def execute(self, instance, solution):
        """Execute constructive heuristic."""
        from src.operators import CONSTRUCTIVE_OPERATORS
        
        if self.heuristic not in CONSTRUCTIVE_OPERATORS:
            raise ValueError(f"Unknown heuristic: {self.heuristic}")
        
        constructor = CONSTRUCTIVE_OPERATORS[self.heuristic]()
        return constructor.apply(instance)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'GreedyConstruct',
            'heuristic': self.heuristic
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GreedyConstruct':
        return cls(heuristic=data['heuristic'])
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}Construct({self.heuristic})"
    
    def size(self) -> int:
        return 1
    
    def depth(self) -> int:
        return 0
    
    def clone(self) -> 'GreedyConstruct':
        return GreedyConstruct(heuristic=self.heuristic)


@dataclass
class LocalSearch(ASTNode):
    """
    Terminal: Apply local search operator with iteration limit.
    
    Valid operators:
    Intra-route: "TwoOpt", "OrOpt", "Relocate", "ThreeOpt"
    Inter-route: "CrossExchange", "TwoOptStar", "SwapCustomers", "RelocateInter"
    """
    operator: str  # Local search operator name
    max_iterations: int = 50  # Limit on iterations
    
    def execute(self, instance, solution):
        """Execute local search."""
        from src.operators import LOCAL_SEARCH_INTRA, LOCAL_SEARCH_INTER
        
        all_ops = {**LOCAL_SEARCH_INTRA, **LOCAL_SEARCH_INTER}
        
        if self.operator not in all_ops:
            raise ValueError(f"Unknown operator: {self.operator}")
        
        searcher = all_ops[self.operator]()
        return searcher.apply(solution, max_iterations=self.max_iterations)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'LocalSearch',
            'operator': self.operator,
            'max_iterations': self.max_iterations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LocalSearch':
        return cls(operator=data['operator'], 
                   max_iterations=data.get('max_iterations', 50))
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}LocalSearch({self.operator}, {self.max_iterations})"
    
    def size(self) -> int:
        return 1
    
    def depth(self) -> int:
        return 0
    
    def clone(self) -> 'LocalSearch':
        return LocalSearch(operator=self.operator, max_iterations=self.max_iterations)


@dataclass
class Perturbation(ASTNode):
    """
    Terminal: Apply perturbation operator to escape local optima.
    
    Valid operators:
    - "EjectionChain"
    - "RuinRecreate"
    - "RandomRemoval"
    - "RouteElimination"
    """
    operator: str
    strength: int = 3  # Perturbation strength (1-5)
    
    def execute(self, instance, solution):
        """Execute perturbation."""
        from src.operators import PERTURBATION_OPERATORS
        
        if self.operator not in PERTURBATION_OPERATORS:
            raise ValueError(f"Unknown perturbation: {self.operator}")
        
        perturber = PERTURBATION_OPERATORS[self.operator]()
        return perturber.apply(solution)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Perturbation',
            'operator': self.operator,
            'strength': self.strength
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Perturbation':
        return cls(operator=data['operator'], strength=data.get('strength', 3))
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}Perturb({self.operator}, strength={self.strength})"
    
    def size(self) -> int:
        return 1
    
    def depth(self) -> int:
        return 0
    
    def clone(self) -> 'Perturbation':
        return Perturbation(operator=self.operator, strength=self.strength)


@dataclass
class Repair(ASTNode):
    """
    Terminal: Apply repair operator to fix constraint violations.
    
    Valid operators:
    - "RepairCapacity"
    - "RepairTimeWindows"
    - "GreedyRepair"
    """
    operator: str
    
    def execute(self, instance, solution):
        """Execute repair."""
        from src.operators import REPAIR_OPERATORS
        
        if self.operator not in REPAIR_OPERATORS:
            raise ValueError(f"Unknown repair: {self.operator}")
        
        repairer = REPAIR_OPERATORS[self.operator]()
        return repairer.apply(solution)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Repair',
            'operator': self.operator
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Repair':
        return cls(operator=data['operator'])
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}Repair({self.operator})"
    
    def size(self) -> int:
        return 1
    
    def depth(self) -> int:
        return 0
    
    def clone(self) -> 'Repair':
        return Repair(operator=self.operator)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def reconstruct_node(data: Dict[str, Any]) -> ASTNode:
    """Reconstruct AST node from dictionary."""
    node_type = data['type']
    
    node_classes = {
        'Seq': Seq,
        'While': While,
        'For': For,
        'If': If,
        'ChooseBestOf': ChooseBestOf,
        'ApplyUntilNoImprove': ApplyUntilNoImprove,
        'GreedyConstruct': GreedyConstruct,
        'LocalSearch': LocalSearch,
        'Perturbation': Perturbation,
        'Repair': Repair,
    }
    
    if node_type not in node_classes:
        raise ValueError(f"Unknown node type: {node_type}")
    
    return node_classes[node_type].from_dict(data)
