"""
AST Interpreter for VRPTW

Executes Abstract Syntax Trees (algorithms) on problem instances.
Handles all node types and provides exception handling.
"""

from typing import Optional, Tuple
import logging

# Try importing models, but make them optional
try:
    from src.core.loader import SolomonLoader
    from src.core.models import Instance, Solution
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
        NearestNeighbor, RandomizedInsertion, SavingsHeuristic,
        TimeOrientedNN, InsertionI1, RegretInsertion
    )
    from src.operators.local_search_intra import (
        TwoOpt, OrOpt, Relocate, ThreeOpt
    )
    from src.operators.local_search_inter import (
        CrossExchange, TwoOptStar, SwapCustomers, RelocateInter
    )
    from src.operators.perturbation import (
        EjectionChain, RuinRecreate, RandomRemoval, RouteElimination
    )
    from src.operators.perturbation import (
        RepairCapacity, RepairTimeWindows, GreedyRepair
    )
    OPERATORS_AVAILABLE = True
except ImportError as e:
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
            'NearestNeighbor': NearestNeighbor(),
            'RandomizedInsertion': RandomizedInsertion(),
            'SavingsHeuristic': SavingsHeuristic(),
            'TimeOrientedNN': TimeOrientedNN(),
            'InsertionI1': InsertionI1(),
            'RegretInsertion': RegretInsertion(),
        }
        
        # Local search operators (intra-route)
        self.local_search = {
            # Intra-route
            'TwoOpt': TwoOpt(),
            'OrOpt': OrOpt(),
            'Relocate': Relocate(),
            'ThreeOpt': ThreeOpt(),
            # Inter-route
            'CrossExchange': CrossExchange(),
            'TwoOptStar': TwoOptStar(),
            'SwapCustomers': SwapCustomers(),
            'RelocateInter': RelocateInter(),
        }
        
        # Perturbation operators
        self.perturbation = {
            'EjectionChain': EjectionChain(),
            'RuinRecreate': RuinRecreate(),
            'RandomRemoval': RandomRemoval(),
            'RouteElimination': RouteElimination(),
        }
        
        # Repair operators
        self.repair = {
            'RepairCapacity': RepairCapacity(),
            'RepairTimeWindows': RepairTimeWindows(),
            'GreedyRepair': GreedyRepair(),
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
            prev_distance = solution.total_distance
            solution = self._execute_node(node.body, instance, solution)
            
            # Check for improvement
            if solution.total_distance < prev_distance:
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
            if current.total_distance < best_solution.total_distance:
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
            
            if current.total_distance < best.total_distance:
                best = current.clone()
        
        return best
    
    def _execute_apply_until(self, node: ApplyUntilNoImprove,
                            instance: Instance, solution: Solution) -> Solution:
        """Execute until no improvement for K iterations."""
        no_improve_count = 0
        
        while no_improve_count < node.max_no_improve:
            prev_distance = solution.total_distance
            solution = self._execute_node(node.body, instance, solution)
            
            if solution.total_distance < prev_distance:
                no_improve_count = 0
            else:
                no_improve_count += 1
        
        return solution
    
    def _execute_construct(self, node: GreedyConstruct, instance: Instance,
                          solution: Solution) -> Solution:
        """Execute constructive heuristic."""
        self.stats['operator_calls'] += 1
        
        # Create constructor with parameters from AST node
        if node.heuristic == 'RandomizedInsertion':
            constructor = RandomizedInsertion(alpha=node.alpha)
        elif node.heuristic == 'NearestNeighbor':
            constructor = NearestNeighbor()
        elif node.heuristic == 'SavingsHeuristic':
            constructor = SavingsHeuristic()
        elif node.heuristic == 'TimeOrientedNN':
            constructor = TimeOrientedNN()
        elif node.heuristic == 'InsertionI1':
            constructor = InsertionI1()
        elif node.heuristic == 'RegretInsertion':
            constructor = RegretInsertion()
        else:
            raise ValueError(f"Unknown constructor: {node.heuristic}")
        
        new_solution = constructor.apply(instance)
        
        # Always use the constructed solution (overwrites initial empty solution)
        # Then repair if needed to ensure feasibility
        repaired_solution = self._repair_solution_if_needed(new_solution, instance)
        
        return repaired_solution
    
    def _repair_solution_if_needed(self, solution: Solution, instance: Instance) -> Solution:
        """
        Repair solution if it's incomplete or infeasible.
        
        Args:
            solution: Solution to check and potentially repair
            instance: Problem instance
            
        Returns:
            Repaired solution (feasible or at least complete)
        """
        # Check if solution has all customers inserted
        inserted_customers = set()
        for route in solution.routes:
            for cust_id in route.sequence[1:-1]:  # Exclude depot
                inserted_customers.add(cust_id)
        
        expected_customers = set(range(1, instance.n_customers + 1))
        missing_customers = expected_customers - inserted_customers
        
        # If solution is incomplete, use repair operator
        if missing_customers or not all(r.is_feasible for r in solution.routes):
            try:
                from src.operators.repair_solution import GreedyRepairOperator
                repair_op = GreedyRepairOperator()
                solution = repair_op.apply(solution)
            except ImportError:
                logger.warning("Repair operator not available, returning as-is")
        
        return solution
    
    def _execute_local_search(self, node: LocalSearch, instance: Instance,
                             solution: Solution) -> Solution:
        """Execute local search operator."""
        self.stats['operator_calls'] += 1
        
        operator = self.registry.get_local_search(node.operator)
        
        for _ in range(node.max_iterations):
            prev_distance = solution.total_distance
            solution = operator.apply(solution)
            
            if solution.total_distance >= prev_distance:
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
        if not solution.feasible:
            return False
        
        # Check cost relative to instance
        # (can be customized based on instance characteristics)
        return solution.total_distance < float('inf')
    
    def _generate_start_solution(self, instance: Instance) -> Solution:
        """Generate a random starting solution."""
        # Use randomized nearest neighbor
        constructor = self.registry.get_constructor('RandomizedInsertion')
        return constructor.apply(instance)
    
    def _verify_solution(self, solution: Solution, instance: Instance) -> None:
        """Verify solution is valid."""
        if not solution.feasible:
            # Try repair
            repairer = self.registry.get_repair('GreedyRepair')
            solution = repairer.apply(solution)
        
        if solution.feasible:
            self.stats['feasible_solutions'] += 1
        else:
            logger.warning("Solution is infeasible after execution")
    
    def get_stats(self) -> dict:
        """Get execution statistics."""
        return self.stats.copy()
