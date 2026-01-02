"""
AST Interpreter for VRPTW

Executes Abstract Syntax Trees (algorithms) on problem instances.
Handles all node types and provides exception handling.
"""

from typing import Optional, Tuple
import logging

# Try importing models, but make them optional
try:
    from src.models.instance import Instance
    from src.models.solution import Solution
except ImportError:
    Instance = None
    Solution = None

from src.gaa.ast_nodes import (
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair
)

# Try importing operators, but make them optional
try:
    from src.operators.constructive import (
        GreedyConstructor, RandomInsertionHeuristic, SavingsHeuristic,
        TimeOrientedNearestNeighbor, InsertionI1, RegretInsertion
    )
    from src.operators.local_search import (
        TwoOptOperator, OrOptOperator, RelocateOperator, ThreeOptOperator,
        CrossExchangeOperator, TwoOptStarOperator, SwapCustomersOperator,
        RelocateInterOperator
    )
    from src.operators.perturbation import (
        EjectionChainOperator, RuinRecreateOperator, RandomRemovalOperator,
        RouteEliminationOperator
    )
    from src.operators.repair import (
        CapacityRepairOperator, TimeWindowRepairOperator, GreedyRepairOperator
    )
    OPERATORS_AVAILABLE = True
except ImportError:
    OPERATORS_AVAILABLE = False


logger = logging.getLogger(__name__)


class ASTProgramException(Exception):
    """Exception raised during AST execution."""
    pass


class OperatorRegistry:
    """
    Registry of all available VRPTW operators.
    Maps operator names to their implementations.
    """
    
    def __init__(self):
        # Constructive operators
        self.constructors = {
            'NearestNeighbor': GreedyConstructor(),
            'RandomizedInsertion': RandomInsertionHeuristic(),
            'SavingsHeuristic': SavingsHeuristic(),
            'TimeOrientedNN': TimeOrientedNearestNeighbor(),
            'InsertionI1': InsertionI1(),
            'RegretInsertion': RegretInsertion(),
        }
        
        # Local search operators
        self.local_search = {
            # Intra-route
            'TwoOpt': TwoOptOperator(),
            'OrOpt': OrOptOperator(),
            'Relocate': RelocateOperator(),
            'ThreeOpt': ThreeOptOperator(),
            # Inter-route
            'CrossExchange': CrossExchangeOperator(),
            'TwoOptStar': TwoOptStarOperator(),
            'SwapCustomers': SwapCustomersOperator(),
            'RelocateInter': RelocateInterOperator(),
        }
        
        # Perturbation operators
        self.perturbation = {
            'EjectionChain': EjectionChainOperator(),
            'RuinRecreate': RuinRecreateOperator(),
            'RandomRemoval': RandomRemovalOperator(),
            'RouteElimination': RouteEliminationOperator(),
        }
        
        # Repair operators
        self.repair = {
            'RepairCapacity': CapacityRepairOperator(),
            'RepairTimeWindows': TimeWindowRepairOperator(),
            'GreedyRepair': GreedyRepairOperator(),
        }
    
    def get_constructor(self, name: str):
        """Get constructor by name."""
        if name not in self.constructors:
            raise KeyError(f"Unknown constructor: {name}")
        return self.constructors[name]
    
    def get_local_search(self, name: str):
        """Get local search operator by name."""
        if name not in self.local_search:
            raise KeyError(f"Unknown local search operator: {name}")
        return self.local_search[name]
    
    def get_perturbation(self, name: str):
        """Get perturbation operator by name."""
        if name not in self.perturbation:
            raise KeyError(f"Unknown perturbation: {name}")
        return self.perturbation[name]
    
    def get_repair(self, name: str):
        """Get repair operator by name."""
        if name not in self.repair:
            raise KeyError(f"Unknown repair: {name}")
        return self.repair[name]


class ASTInterpreter:
    """
    Interprets and executes AST algorithms on VRPTW instances.
    
    Features:
    - All node type support (control flow + terminals)
    - Exception handling and logging
    - Solution improvement tracking
    - Feasibility verification
    """
    
    def __init__(self):
        self.registry = OperatorRegistry()
        self.stats = {
            'nodes_executed': 0,
            'operator_calls': 0,
            'feasible_solutions': 0,
            'improvements': 0,
        }
    
    def execute(self, algorithm: ASTNode, instance: Instance,
                initial_solution: Optional[Solution] = None) -> Solution:
        """
        Execute algorithm on instance.
        
        Args:
            algorithm: AST representing algorithm
            instance: VRPTW instance
            initial_solution: Starting solution (if None, create empty)
        
        Returns:
            Final solution
        """
        # Initialize solution
        if initial_solution is None:
            initial_solution = Solution(instance)
        
        # Reset stats
        self.stats = {
            'nodes_executed': 0,
            'operator_calls': 0,
            'feasible_solutions': 0,
            'improvements': 0,
        }
        
        # Execute
        try:
            solution = self._execute_node(algorithm, instance, initial_solution)
            self._verify_solution(solution, instance)
            return solution
        except Exception as e:
            logger.error(f"Error executing algorithm: {e}")
            raise ASTProgramException(f"Algorithm execution failed: {e}")
    
    def _execute_node(self, node: ASTNode, instance: Instance,
                     solution: Solution) -> Solution:
        """Execute a single AST node."""
        self.stats['nodes_executed'] += 1
        
        if isinstance(node, Seq):
            return self._execute_seq(node, instance, solution)
        elif isinstance(node, While):
            return self._execute_while(node, instance, solution)
        elif isinstance(node, For):
            return self._execute_for(node, instance, solution)
        elif isinstance(node, If):
            return self._execute_if(node, instance, solution)
        elif isinstance(node, ChooseBestOf):
            return self._execute_choose_best(node, instance, solution)
        elif isinstance(node, ApplyUntilNoImprove):
            return self._execute_apply_until(node, instance, solution)
        elif isinstance(node, GreedyConstruct):
            return self._execute_construct(node, instance, solution)
        elif isinstance(node, LocalSearch):
            return self._execute_local_search(node, instance, solution)
        elif isinstance(node, Perturbation):
            return self._execute_perturbation(node, instance, solution)
        elif isinstance(node, Repair):
            return self._execute_repair(node, instance, solution)
        else:
            raise ASTProgramException(f"Unknown node type: {type(node)}")
    
    def _execute_seq(self, node: Seq, instance: Instance,
                    solution: Solution) -> Solution:
        """Execute sequence of statements."""
        for stmt in node.body:
            solution = self._execute_node(stmt, instance, solution)
        return solution
    
    def _execute_while(self, node: While, instance: Instance,
                      solution: Solution) -> Solution:
        """Execute while loop."""
        iteration = 0
        while iteration < node.max_iterations:
            prev_cost = solution.cost
            solution = self._execute_node(node.body, instance, solution)
            
            # Check for improvement
            if solution.cost < prev_cost:
                iteration = 0  # Reset counter
            else:
                iteration += 1
        
        return solution
    
    def _execute_for(self, node: For, instance: Instance,
                    solution: Solution) -> Solution:
        """Execute for loop (multi-start)."""
        best_solution = solution.clone()
        
        for i in range(node.iterations):
            # Generate new starting point
            if i > 0:
                current = self._generate_start_solution(instance)
            else:
                current = solution.clone()
            
            # Execute body
            current = self._execute_node(node.body, instance, current)
            
            # Keep best
            if current.cost < best_solution.cost:
                best_solution = current.clone()
        
        return best_solution
    
    def _execute_if(self, node: If, instance: Instance,
                   solution: Solution) -> Solution:
        """Execute conditional (quality-based selection)."""
        # Condition: solution quality (feasible and cost)
        condition_met = self._evaluate_condition(solution, instance)
        
        if condition_met and node.then_branch:
            return self._execute_node(node.then_branch, instance, solution)
        elif not condition_met and node.else_branch:
            return self._execute_node(node.else_branch, instance, solution)
        else:
            return solution
    
    def _execute_choose_best(self, node: ChooseBestOf, instance: Instance,
                            solution: Solution) -> Solution:
        """Execute all alternatives, return best."""
        best = solution.clone()
        
        for alt in node.alternatives:
            current = solution.clone()
            current = self._execute_node(alt, instance, current)
            
            if current.cost < best.cost:
                best = current.clone()
        
        return best
    
    def _execute_apply_until(self, node: ApplyUntilNoImprove,
                            instance: Instance, solution: Solution) -> Solution:
        """Execute until no improvement for K iterations."""
        no_improve_count = 0
        
        while no_improve_count < node.max_no_improve:
            prev_cost = solution.cost
            solution = self._execute_node(node.body, instance, solution)
            
            if solution.cost < prev_cost:
                no_improve_count = 0
            else:
                no_improve_count += 1
        
        return solution
    
    def _execute_construct(self, node: GreedyConstruct, instance: Instance,
                          solution: Solution) -> Solution:
        """Execute constructive heuristic."""
        self.stats['operator_calls'] += 1
        
        constructor = self.registry.get_constructor(node.heuristic)
        new_solution = constructor.construct(instance)
        
        if new_solution.cost < solution.cost:
            self.stats['improvements'] += 1
            return new_solution
        return solution
    
    def _execute_local_search(self, node: LocalSearch, instance: Instance,
                             solution: Solution) -> Solution:
        """Execute local search operator."""
        self.stats['operator_calls'] += 1
        
        operator = self.registry.get_local_search(node.operator)
        
        for _ in range(node.max_iterations):
            prev_cost = solution.cost
            solution = operator.apply(solution, instance)
            
            if solution.cost >= prev_cost:
                break  # No improvement, stop
        
        return solution
    
    def _execute_perturbation(self, node: Perturbation, instance: Instance,
                             solution: Solution) -> Solution:
        """Execute perturbation operator."""
        self.stats['operator_calls'] += 1
        
        perturbator = self.registry.get_perturbation(node.operator)
        solution = perturbator.perturb(solution, instance, strength=node.strength)
        
        return solution
    
    def _execute_repair(self, node: Repair, instance: Instance,
                       solution: Solution) -> Solution:
        """Execute repair operator."""
        self.stats['operator_calls'] += 1
        
        repairer = self.registry.get_repair(node.operator)
        solution = repairer.repair(solution, instance)
        
        return solution
    
    def _evaluate_condition(self, solution: Solution, instance: Instance) -> bool:
        """
        Evaluate condition for If node.
        Returns True if solution is good (feasible and reasonable cost).
        """
        # Check feasibility
        if not solution.is_feasible:
            return False
        
        # Check cost relative to instance
        # (can be customized based on instance characteristics)
        return solution.cost < float('inf')
    
    def _generate_start_solution(self, instance: Instance) -> Solution:
        """Generate a random starting solution."""
        # Use randomized nearest neighbor
        constructor = self.registry.get_constructor('RandomizedInsertion')
        return constructor.construct(instance)
    
    def _verify_solution(self, solution: Solution, instance: Instance) -> None:
        """Verify solution is valid."""
        if not solution.is_feasible:
            # Try repair
            repairer = self.registry.get_repair('GreedyRepair')
            solution = repairer.repair(solution, instance)
        
        if solution.is_feasible:
            self.stats['feasible_solutions'] += 1
        else:
            logger.warning("Solution is infeasible after execution")
    
    def get_stats(self) -> dict:
        """Get execution statistics."""
        return self.stats.copy()
