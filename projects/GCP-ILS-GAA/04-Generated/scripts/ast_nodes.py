"""
AST Node Implementation for GCP-ILS-GAA

Implements the Abstract Syntax Tree nodes defined in 01-System/AST-Nodes.md.
These nodes represent algorithms as tree structures that can be:
  - Executed on problems
  - Mutated/recombined by genetic algorithm
  - Serialized for storage/transmission

Author: GAA Framework
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from copy import deepcopy
import json
from enum import Enum
import random


# ============================================================================
# ENUMS and TYPE DEFINITIONS
# ============================================================================

class NodeType(Enum):
    """Enumeration of all valid AST node types"""
    ALGORITHM = "Algorithm"
    INIT_PHASE = "InitPhase"
    SEARCH_PHASE = "SearchPhase"
    LOCAL_SEARCH_PHASE = "LocalSearchPhase"
    PERTURBATION_PHASE = "PerturbationPhase"
    TERMINATION = "Termination"
    ACCEPTANCE = "Acceptance"
    
    # Constructive operators
    DSATUR = "DSATUR"
    LARGEST_FIRST = "LargestFirst"
    SMALLEST_LAST = "SmallestLast"
    RANDOM_SEQUENTIAL = "RandomSequential"
    RLF = "RLF"
    
    # Local search operators
    KEMPE_CHAIN = "KempeChain"
    SINGLE_VERTEX_MOVE = "SingleVertexMove"
    COLOR_CLASS_MERGE = "ColorClassMerge"
    TABU_SEARCH = "TabuSearch"
    SWAP_COLORS = "SwapColors"
    
    # Perturbation operators
    RANDOM_RECOLOR = "RandomRecolor"
    PARTIAL_DESTROY = "PartialDestroy"
    SHAKE_COLORS = "ShakeColors"
    
    # Termination
    MAX_ITER = "MaxIter"
    TIME_LIMIT = "TimeLimit"
    NO_IMPROVEMENT = "NoImprovement"
    OPTIMAL_REACHED = "OptimalReached"
    
    # Acceptance
    BETTER_OR_EQUAL = "BetterOrEqual"
    METROPOLIS = "Metropolis"
    FIRST_IMPROVEMENT = "FirstImprovement"


# ============================================================================
# BASE CLASSES
# ============================================================================

class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    def __init__(self, node_type: NodeType):
        self.node_type = node_type
        self.parent: Optional['ASTNode'] = None
        self.children: List['ASTNode'] = []
    
    @abstractmethod
    def __repr__(self) -> str:
        """String representation of node"""
        pass
    
    @abstractmethod
    def to_pseudocode(self, indent: int = 0) -> str:
        """Convert to readable pseudocode"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        pass
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def copy(self) -> 'ASTNode':
        """Create deep copy of node and subtree"""
        return deepcopy(self)
    
    def depth(self) -> int:
        """Depth of subtree rooted at this node"""
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)
    
    def size(self) -> int:
        """Number of nodes in subtree"""
        return 1 + sum(child.size() for child in self.children)
    
    def all_nodes(self) -> List['ASTNode']:
        """Get all nodes in subtree (DFS)"""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.all_nodes())
        return nodes
    
    def add_child(self, child: 'ASTNode') -> None:
        """Add child node"""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'ASTNode') -> None:
        """Remove child node"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None


# ============================================================================
# OPERATOR BASE CLASSES
# ============================================================================

class OperatorNode(ASTNode):
    """Base class for operators (constructive, LS, perturbation)"""
    
    def __init__(self, node_type: NodeType, **params):
        super().__init__(node_type)
        self.parameters = params
    
    @abstractmethod
    def execute(self, problem, coloring: Dict, **kwargs):
        """Execute operator on problem/coloring"""
        pass
    
    def __repr__(self) -> str:
        param_str = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        if param_str:
            return f"{self.node_type.value}({param_str})"
        return self.node_type.value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "parameters": self.parameters
        }


# ============================================================================
# CONSTRUCTIVE OPERATORS
# ============================================================================

class DSATURNode(OperatorNode):
    """Degree of Saturation constructive heuristic"""
    
    def __init__(self):
        super().__init__(NodeType.DSATUR)
    
    def execute(self, problem, coloring=None, **kwargs):
        # Returns initial feasible coloring via DSATUR
        # Implementation in gaa_components.py
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "INIT: DSATUR"


class LargestFirstNode(OperatorNode):
    """Construct coloring by decreasing vertex degree"""
    
    def __init__(self):
        super().__init__(NodeType.LARGEST_FIRST)
    
    def execute(self, problem, coloring=None, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "INIT: LargestFirst"


class SmallestLastNode(OperatorNode):
    """Construct coloring by increasing vertex degree"""
    
    def __init__(self):
        super().__init__(NodeType.SMALLEST_LAST)
    
    def execute(self, problem, coloring=None, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "INIT: SmallestLast"


class RandomSequentialNode(OperatorNode):
    """Random sequential coloring construction"""
    
    def __init__(self):
        super().__init__(NodeType.RANDOM_SEQUENTIAL)
    
    def execute(self, problem, coloring=None, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "INIT: RandomSequential"


class RLFNode(OperatorNode):
    """Recursive Largest First construction"""
    
    def __init__(self):
        super().__init__(NodeType.RLF)
    
    def execute(self, problem, coloring=None, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "INIT: RLF"


# ============================================================================
# LOCAL SEARCH OPERATORS
# ============================================================================

class KempeChainNode(OperatorNode):
    """Color exchange via Kempe chains"""
    
    def __init__(self, max_iterations: int = 100):
        super().__init__(NodeType.KEMPE_CHAIN, max_iterations=max_iterations)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"LS: KempeChain(iter={self.parameters['max_iterations']})"


class SingleVertexMoveNode(OperatorNode):
    """Recolor one vertex at a time"""
    
    def __init__(self, max_iterations: int = 100):
        super().__init__(NodeType.SINGLE_VERTEX_MOVE, max_iterations=max_iterations)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"LS: SingleVertexMove(iter={self.parameters['max_iterations']})"


class ColorClassMergeNode(OperatorNode):
    """Merge two color classes"""
    
    def __init__(self, max_iterations: int = 100):
        super().__init__(NodeType.COLOR_CLASS_MERGE, max_iterations=max_iterations)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"LS: ColorClassMerge(iter={self.parameters['max_iterations']})"


class TabuSearchNode(OperatorNode):
    """Local search with tabu memory"""
    
    def __init__(self, max_iterations: int = 100, tabu_tenure: int = 10):
        super().__init__(NodeType.TABU_SEARCH, 
                        max_iterations=max_iterations, 
                        tabu_tenure=tabu_tenure)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"LS: TabuSearch(iter={self.parameters['max_iterations']})"


class SwapColorsNode(OperatorNode):
    """Swap two colors directly"""
    
    def __init__(self, max_iterations: int = 100):
        super().__init__(NodeType.SWAP_COLORS, max_iterations=max_iterations)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"LS: SwapColors(iter={self.parameters['max_iterations']})"


# ============================================================================
# PERTURBATION OPERATORS
# ============================================================================

class RandomRecolorNode(OperatorNode):
    """Recolor p% of vertices randomly"""
    
    def __init__(self, strength: float = 0.2):
        super().__init__(NodeType.RANDOM_RECOLOR, strength=strength)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"PERT: RandomRecolor(strength={self.parameters['strength']})"


class PartialDestroyNode(OperatorNode):
    """Destroy and rebuild subgraph"""
    
    def __init__(self, strength: float = 0.2):
        super().__init__(NodeType.PARTIAL_DESTROY, strength=strength)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"PERT: PartialDestroy(strength={self.parameters['strength']})"


class ShakeColorsNode(OperatorNode):
    """Random permutation of color assignments"""
    
    def __init__(self, strength: float = 0.2):
        super().__init__(NodeType.SHAKE_COLORS, strength=strength)
    
    def execute(self, problem, coloring, **kwargs):
        pass
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"PERT: ShakeColors(strength={self.parameters['strength']})"


# ============================================================================
# PHASE NODES
# ============================================================================

class InitPhaseNode(ASTNode):
    """Initialization phase with constructive heuristic"""
    
    def __init__(self, constructive: OperatorNode):
        super().__init__(NodeType.INIT_PHASE)
        self.constructive = constructive
        self.add_child(constructive)
    
    def execute(self, problem, **kwargs):
        """Execute constructive and return initial coloring"""
        return self.constructive.execute(problem, **kwargs)
    
    def __repr__(self) -> str:
        return f"InitPhase({self.constructive})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return self.constructive.to_pseudocode(indent)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "InitPhase",
            "constructive": self.constructive.to_dict()
        }


class LocalSearchPhaseNode(ASTNode):
    """Local search phase with 1+ operators applied sequentially"""
    
    def __init__(self, operators: List[OperatorNode], 
                 max_iterations: int = 100,
                 first_improvement: bool = True):
        super().__init__(NodeType.LOCAL_SEARCH_PHASE)
        self.operators = operators
        self.max_iterations = max_iterations
        self.first_improvement = first_improvement
        
        for op in operators:
            self.add_child(op)
    
    def execute(self, problem, coloring, context=None, **kwargs):
        """Apply all operators sequentially"""
        result = coloring.copy()
        for operator in self.operators:
            result = operator.execute(problem, result, **kwargs)
        return result
    
    def __repr__(self) -> str:
        ops_str = ", ".join(str(op) for op in self.operators)
        return f"LocalSearchPhase([{ops_str}])"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        lines = [" " * indent + "SEARCH:"]
        for op in self.operators:
            lines.append(op.to_pseudocode(indent + 2))
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LocalSearchPhase",
            "operators": [op.to_dict() for op in self.operators],
            "max_iterations": self.max_iterations,
            "first_improvement": self.first_improvement
        }


class PerturbationPhaseNode(ASTNode):
    """Perturbation phase with single operator"""
    
    def __init__(self, operator: OperatorNode, strength: float = 0.2):
        super().__init__(NodeType.PERTURBATION_PHASE)
        self.operator = operator
        self.strength = strength
        self.add_child(operator)
    
    def execute(self, problem, coloring, context=None, **kwargs):
        """Apply perturbation"""
        return self.operator.execute(problem, coloring, **kwargs)
    
    def __repr__(self) -> str:
        return f"PerturbationPhase({self.operator})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return self.operator.to_pseudocode(indent)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "PerturbationPhase",
            "operator": self.operator.to_dict(),
            "strength": self.strength
        }


# ============================================================================
# TERMINATION CONDITIONS
# ============================================================================

class TerminationNode(ASTNode):
    """Base class for termination conditions"""
    
    @abstractmethod
    def should_terminate(self, context: Dict) -> bool:
        """Check if termination condition is met"""
        pass


class MaxIterNode(TerminationNode):
    """Terminate after N iterations"""
    
    def __init__(self, max_iterations: int = 500):
        super().__init__(NodeType.MAX_ITER)
        self.max_iterations = max_iterations
    
    def should_terminate(self, context: Dict) -> bool:
        return context.get('iteration', 0) >= self.max_iterations
    
    def __repr__(self) -> str:
        return f"MaxIter({self.max_iterations})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"TERM: MAX_ITER({self.max_iterations})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "MaxIter", "value": self.max_iterations}


class TimeLimitNode(TerminationNode):
    """Terminate after T seconds"""
    
    def __init__(self, time_limit_seconds: float = 60):
        super().__init__(NodeType.TIME_LIMIT)
        self.time_limit = time_limit_seconds
    
    def should_terminate(self, context: Dict) -> bool:
        elapsed = context.get('elapsed_time', 0)
        return elapsed >= self.time_limit
    
    def __repr__(self) -> str:
        return f"TimeLimit({self.time_limit}s)"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"TERM: TIME_LIMIT({self.time_limit}s)"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "TimeLimit", "seconds": self.time_limit}


class NoImprovementNode(TerminationNode):
    """Terminate if no improvement for N iterations"""
    
    def __init__(self, patience: int = 50):
        super().__init__(NodeType.NO_IMPROVEMENT)
        self.patience = patience
    
    def should_terminate(self, context: Dict) -> bool:
        no_improve_count = context.get('no_improve_count', 0)
        return no_improve_count >= self.patience
    
    def __repr__(self) -> str:
        return f"NoImprovement({self.patience})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"TERM: NO_IMPROVE({self.patience})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "NoImprovement", "patience": self.patience}


class OptimalReachedNode(TerminationNode):
    """Terminate if known optimal is reached"""
    
    def __init__(self, known_optimal: int):
        super().__init__(NodeType.OPTIMAL_REACHED)
        self.known_optimal = known_optimal
    
    def should_terminate(self, context: Dict) -> bool:
        best_fitness = context.get('best_fitness', float('inf'))
        return best_fitness <= self.known_optimal
    
    def __repr__(self) -> str:
        return f"OptimalReached({self.known_optimal})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"TERM: OPTIMAL({self.known_optimal})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "OptimalReached", "value": self.known_optimal}


# ============================================================================
# ACCEPTANCE CRITERIA
# ============================================================================

class AcceptanceNode(ASTNode):
    """Base class for acceptance criteria"""
    
    @abstractmethod
    def should_accept(self, f_current: float, f_candidate: float, context: Dict) -> bool:
        """Determine if candidate solution should be accepted"""
        pass


class BetterOrEqualNode(AcceptanceNode):
    """Accept if candidate is better or equal"""
    
    def __init__(self):
        super().__init__(NodeType.BETTER_OR_EQUAL)
    
    def should_accept(self, f_current: float, f_candidate: float, context: Dict) -> bool:
        return f_candidate <= f_current
    
    def __repr__(self) -> str:
        return "BetterOrEqual"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "ACCEPT: BETTER_OR_EQUAL"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "BetterOrEqual"}


class MetropolisNode(AcceptanceNode):
    """Probabilistic acceptance (Metropolis criterion)"""
    
    def __init__(self, temperature: float = 0.1):
        super().__init__(NodeType.METROPOLIS)
        self.temperature = temperature
    
    def should_accept(self, f_current: float, f_candidate: float, context: Dict) -> bool:
        if f_candidate <= f_current:
            return True
        delta = f_candidate - f_current
        prob = min(1.0, exp(-delta / self.temperature))
        return random.random() < prob
    
    def __repr__(self) -> str:
        return f"Metropolis(T={self.temperature})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + f"ACCEPT: METROPOLIS(T={self.temperature})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "Metropolis", "temperature": self.temperature}


class FirstImprovementNode(AcceptanceNode):
    """Accept first improving move"""
    
    def __init__(self):
        super().__init__(NodeType.FIRST_IMPROVEMENT)
    
    def should_accept(self, f_current: float, f_candidate: float, context: Dict) -> bool:
        return f_candidate < f_current
    
    def __repr__(self) -> str:
        return "FirstImprovement"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        return " " * indent + "ACCEPT: FIRST_IMPROVEMENT"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "FirstImprovement"}


# ============================================================================
# MAIN ALGORITHM NODE
# ============================================================================

class AlgorithmNode(ASTNode):
    """Root node representing a complete algorithm"""
    
    def __init__(self, init_phase: InitPhaseNode,
                 search_phases: List[ASTNode],
                 termination: TerminationNode,
                 acceptance: AcceptanceNode):
        super().__init__(NodeType.ALGORITHM)
        
        self.init_phase = init_phase
        self.search_phases = search_phases
        self.termination = termination
        self.acceptance = acceptance
        
        # Add as children for tree structure
        self.add_child(init_phase)
        for phase in search_phases:
            self.add_child(phase)
        self.add_child(termination)
        self.add_child(acceptance)
    
    def execute(self, problem, max_time: float = 60, seed: Optional[int] = None):
        """
        Execute algorithm on problem.
        
        Returns:
            {
                'best_coloring': dict,
                'best_fitness': int,
                'iterations': int,
                'elapsed_time': float,
                'log': [...]
            }
        """
        if seed is not None:
            random.seed(seed)
        
        import time
        start_time = time.time()
        
        # Initialize
        coloring = self.init_phase.execute(problem)
        best_coloring = coloring.copy()
        best_fitness = problem.evaluate(coloring)
        
        # Search
        context = {
            'iteration': 0,
            'best_fitness': best_fitness,
            'no_improve_count': 0,
            'elapsed_time': 0
        }
        
        log = []
        
        while not self.termination.should_terminate(context):
            context['iteration'] += 1
            current_fitness = problem.evaluate(coloring)
            
            # Apply search phases
            for phase in self.search_phases:
                coloring = phase.execute(problem, coloring, context)
            
            candidate_fitness = problem.evaluate(coloring)
            
            # Check acceptance
            if self.acceptance.should_accept(current_fitness, candidate_fitness, context):
                pass  # Accept current coloring
            else:
                coloring = best_coloring.copy()  # Reject
            
            # Update best
            if candidate_fitness < best_fitness:
                best_coloring = coloring.copy()
                best_fitness = candidate_fitness
                context['no_improve_count'] = 0
            else:
                context['no_improve_count'] += 1
            
            context['best_fitness'] = best_fitness
            context['elapsed_time'] = time.time() - start_time
            
            log.append({
                'iteration': context['iteration'],
                'fitness': candidate_fitness,
                'best': best_fitness,
                'time': context['elapsed_time']
            })
            
            if context['elapsed_time'] > max_time:
                break
        
        return {
            'best_coloring': best_coloring,
            'best_fitness': best_fitness,
            'iterations': context['iteration'],
            'elapsed_time': context['elapsed_time'],
            'log': log
        }
    
    def is_valid(self) -> Tuple[bool, List[str]]:
        """Validate algorithm against grammar rules"""
        errors = []
        
        # R1: Minimal structure
        if not self.init_phase:
            errors.append("R1: Missing InitPhase")
        if not self.search_phases:
            errors.append("R1: Missing SearchPhase")
        if not self.termination:
            errors.append("R1: Missing Termination")
        
        # R2: LocalSearch validity
        for phase in self.search_phases:
            if isinstance(phase, LocalSearchPhaseNode):
                if len(phase.operators) > 3:
                    errors.append(f"R2: LocalSearch phase has {len(phase.operators)} > 3 operators")
        
        # R3: Perturbation validity
        pert_count = sum(1 for p in self.search_phases if isinstance(p, PerturbationPhaseNode))
        if pert_count > 2:
            errors.append(f"R3: Algorithm has {pert_count} > 2 perturbations")
        
        return len(errors) == 0, errors
    
    def __repr__(self) -> str:
        return f"Algorithm(init={self.init_phase}, " \
               f"search={len(self.search_phases)} phases, " \
               f"term={self.termination}, " \
               f"accept={self.acceptance})"
    
    def to_pseudocode(self, indent: int = 0) -> str:
        lines = [" " * indent + "ALGORITHM:"]
        lines.append(self.init_phase.to_pseudocode(indent + 2))
        for phase in self.search_phases:
            lines.append(phase.to_pseudocode(indent + 2))
        lines.append(self.termination.to_pseudocode(indent + 2))
        lines.append(self.acceptance.to_pseudocode(indent + 2))
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Algorithm",
            "init_phase": self.init_phase.to_dict(),
            "search_phases": [p.to_dict() for p in self.search_phases],
            "termination": self.termination.to_dict(),
            "acceptance": self.acceptance.to_dict()
        }


# ============================================================================
# GENETIC OPERATORS ON ASTs
# ============================================================================

def mutate_ast(ast: AlgorithmNode, mutation_rate: float = 0.1) -> AlgorithmNode:
    """
    Mutate AST by randomly changing nodes.
    
    Mutation operations:
    1. Change constructive heuristic
    2. Change LS operator
    3. Change perturbation operator
    4. Change parameter value
    """
    mutated = ast.copy()
    
    if random.random() < mutation_rate:
        # Mutation 1: Change constructive
        constructives = [DSATURNode(), LargestFirstNode(), SmallestLastNode(),
                        RandomSequentialNode(), RLFNode()]
        new_constructive = random.choice(constructives)
        mutated.init_phase.constructive = new_constructive
    
    if random.random() < mutation_rate:
        # Mutation 2: Change LS operator
        ls_ops = [KempeChainNode(), SingleVertexMoveNode(), 
                 ColorClassMergeNode(), SwapColorsNode()]
        for phase in mutated.search_phases:
            if isinstance(phase, LocalSearchPhaseNode) and phase.operators:
                phase.operators[0] = random.choice(ls_ops)
    
    if random.random() < mutation_rate:
        # Mutation 3: Change termination
        terminations = [MaxIterNode(500), MaxIterNode(1000), TimeLimitNode(60)]
        mutated.termination = random.choice(terminations)
    
    return mutated


def crossover_ast(parent1: AlgorithmNode, parent2: AlgorithmNode) -> Tuple[AlgorithmNode, AlgorithmNode]:
    """
    Crossover: exchange search phases between parents.
    """
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    # Single-point crossover on search phases
    if len(parent1.search_phases) > 1 and len(parent2.search_phases) > 1:
        point = random.randint(1, min(len(parent1.search_phases), 
                                     len(parent2.search_phases)) - 1)
        
        child1.search_phases = parent1.search_phases[:point] + parent2.search_phases[point:]
        child2.search_phases = parent2.search_phases[:point] + parent1.search_phases[point:]
    
    return child1, child2


def insert_phase(ast: AlgorithmNode, phase: ASTNode, position: int) -> AlgorithmNode:
    """Insert new search phase at position"""
    mutated = ast.copy()
    mutated.search_phases.insert(position, phase)
    return mutated


def remove_phase(ast: AlgorithmNode, position: int) -> AlgorithmNode:
    """Remove search phase at position"""
    mutated = ast.copy()
    if 0 <= position < len(mutated.search_phases):
        mutated.search_phases.pop(position)
    return mutated


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def ast_statistics(ast: AlgorithmNode) -> Dict[str, Any]:
    """Calculate statistics about AST structure"""
    nodes = ast.all_nodes()
    
    constructive_count = sum(1 for n in nodes if isinstance(n, OperatorNode) 
                            and n.node_type in [NodeType.DSATUR, NodeType.LARGEST_FIRST])
    ls_count = sum(1 for n in nodes if isinstance(n, (KempeChainNode, SingleVertexMoveNode)))
    pert_count = sum(1 for n in nodes if isinstance(n, (RandomRecolorNode, PartialDestroyNode)))
    
    return {
        'num_nodes': ast.size(),
        'depth': ast.depth(),
        'num_constructives': constructive_count,
        'num_local_search': ls_count,
        'num_perturbations': pert_count,
        'num_phases': len(ast.search_phases),
    }


def validate_ast(ast: AlgorithmNode) -> Tuple[bool, List[str]]:
    """Validate AST against grammar rules"""
    return ast.is_valid()


if __name__ == "__main__":
    # Example: Create a simple ILS algorithm AST
    init = InitPhaseNode(DSATURNode())
    search = [
        LocalSearchPhaseNode([KempeChainNode(max_iterations=100)]),
        PerturbationPhaseNode(RandomRecolorNode(strength=0.2)),
        LocalSearchPhaseNode([KempeChainNode(max_iterations=100)])
    ]
    term = MaxIterNode(max_iterations=500)
    accept = BetterOrEqualNode()
    
    algorithm = AlgorithmNode(init, search, term, accept)
    
    print("Algorithm AST:")
    print(algorithm)
    print("\nPseudocode:")
    print(algorithm.to_pseudocode())
    print("\nJSON:")
    print(algorithm.to_json())
    print("\nStatistics:")
    print(ast_statistics(algorithm))
    
    is_valid, errors = validate_ast(algorithm)
    print(f"\nValid: {is_valid}")
    if errors:
        print("Errors:", errors)
