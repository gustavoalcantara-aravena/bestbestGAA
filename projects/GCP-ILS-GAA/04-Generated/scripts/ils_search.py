"""
ILS-based Search for Optimal ILS Algorithm Configurations in GCP-ILS-GAA

Instead of Genetic Algorithm, this module uses Iterated Local Search to explore
the space of ILS algorithm configurations (AST variations).

The key insight:
- ILS metaheuristic searches through configuration space
- Each configuration is an ILS algorithm (AST) for solving GCP
- Mutations modify operators, parameters, structure
- Local search improves configurations by tuning parameters
- Perturbation escapes local optima in configuration space

Author: GAA Framework
Version: 1.0.0
Based on: problema_metaheuristica.md (ILS-based GAA)
"""

import random
import time
from typing import List, Tuple, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum

# Import AST nodes
from ast_nodes import (
    AlgorithmNode, InitPhaseNode, ASTNode,
    LocalSearchPhaseNode, PerturbationPhaseNode,
    DSATURNode, LargestFirstNode, SmallestLastNode, RandomSequentialNode, RLFNode,
    KempeChainNode, SingleVertexMoveNode, ColorClassMergeNode, TabuSearchNode, SwapColorsNode,
    RandomRecolorNode, PartialDestroyNode, ShakeColorsNode,
    MaxIterNode, TimeLimitNode, NoImprovementNode, OptimalReachedNode,
    BetterOrEqualNode, MetropolisNode, FirstImprovementNode,
    ast_statistics, validate_ast
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Configuration:
    """
    Represents one ILS algorithm configuration (an AST solution in the search space).
    
    The configuration is an AST that represents a complete ILS algorithm for GCP.
    We search through different AST configurations to find optimal ones.
    """
    
    ast: AlgorithmNode
    fitness_scores: Dict[str, float] = field(default_factory=dict)  # per-instance
    aggregated_fitness: float = float('inf')  # Combined fitness value
    
    # Metadata
    iteration_created: int = 0
    parent_config: Optional['Configuration'] = None
    created_by: str = "initialization"  # "mutation", "local_search", "perturbation", "initialization"
    
    # Local search history
    ls_improvements: int = 0
    ls_moves_tried: int = 0
    
    def __hash__(self):
        return id(self)
    
    def __lt__(self, other):
        """For comparisons (better fitness = lower value)"""
        return self.aggregated_fitness < other.aggregated_fitness
    
    def __repr__(self):
        return f"Cfg(fit={self.aggregated_fitness:.4f}, ast_size={self.ast.size()}, ls_imp={self.ls_improvements})"
    
    def copy(self) -> 'Configuration':
        """Create deep copy"""
        return Configuration(
            ast=self.ast.copy(),
            fitness_scores=self.fitness_scores.copy(),
            aggregated_fitness=self.aggregated_fitness,
            iteration_created=self.iteration_created,
            created_by=self.created_by,
            ls_improvements=self.ls_improvements,
            ls_moves_tried=self.ls_moves_tried
        )


@dataclass
class ILSConfig:
    """ILS-based search configuration for finding optimal algorithm configurations"""
    
    # Problem/instance settings
    seed: Optional[int] = None
    
    # ILS search parameters
    max_iterations: int = 500  # Main loop iterations
    max_no_improve_iterations: int = 50  # Stop if no improvement
    
    # Local search settings (tuning phase)
    enable_local_search: bool = True
    ls_max_moves: int = 10  # Maximum moves tried in LS phase
    ls_max_no_improve: int = 3  # Stop LS if no improvement
    
    # Perturbation settings (escape phase)
    perturbation_strength: float = 0.20  # Fraction of AST to modify
    perturbation_type: str = "mutation"  # "mutation", "operator_swap", "parameter_change"
    
    # Acceptance criteria
    acceptance_criterion: str = "better_or_equal"  # "better", "better_or_equal", "always"
    
    # Fitness aggregation
    fitness_weights: Dict[str, float] = field(default_factory=lambda: {
        'quality': 0.5,      # Minimize num_colors
        'time': 0.2,         # Minimize computation time
        'robustness': 0.2,   # Consistency across instances
        'feasibility': 0.1,  # Always find feasible solution
    })
    
    # Termination
    max_time_seconds: float = 3600  # 1 hour
    target_fitness: Optional[float] = None  # Stop if reached


@dataclass
class ILSStatistics:
    """Statistics collected during ILS search"""
    
    iteration: int = 0
    best_fitness: float = float('inf')
    current_fitness: float = float('inf')
    
    best_configuration: Optional[Configuration] = None
    current_configuration: Optional[Configuration] = None
    
    # Evolutionary events
    improvements_found: int = 0
    acceptances: int = 0
    mutations_applied: int = 0
    ls_moves_applied: int = 0
    perturbations_applied: int = 0
    
    # Timing
    elapsed_time: float = 0.0
    iteration_time: float = 0.0
    total_evaluations: int = 0
    
    def __repr__(self):
        return (f"ILS[iter={self.iteration}, best={self.best_fitness:.4f}, "
                f"current={self.current_fitness:.4f}, imp={self.improvements_found}]")


# ============================================================================
# CONFIGURATION FACTORY
# ============================================================================

class ConfigurationFactory:
    """Factory for creating initial ILS algorithm configurations"""
    
    CONSTRUCTIVES = [DSATURNode(), LargestFirstNode(), SmallestLastNode(),
                    RandomSequentialNode(), RLFNode()]
    
    LS_OPERATORS = [KempeChainNode(), SingleVertexMoveNode(),
                   ColorClassMergeNode(), TabuSearchNode(), SwapColorsNode()]
    
    PERTURBATIONS = [RandomRecolorNode(), PartialDestroyNode(),
                    ShakeColorsNode()]
    
    TERMINATIONS = [MaxIterNode(500), MaxIterNode(1000), TimeLimitNode(60)]
    
    ACCEPTANCES = [BetterOrEqualNode(), FirstImprovementNode()]
    
    @staticmethod
    def create_random_configuration() -> Configuration:
        """Create random valid ILS algorithm configuration"""
        init = InitPhaseNode(random.choice(ConfigurationFactory.CONSTRUCTIVES).copy())
        
        # Search phases (1-3 phases)
        num_phases = random.randint(1, 3)
        search_phases = []
        
        for _ in range(num_phases):
            if random.random() < 0.7:
                # Local search phase
                num_ops = random.randint(1, 2)
                ops = [random.choice(ConfigurationFactory.LS_OPERATORS).copy() 
                       for _ in range(num_ops)]
                search_phases.append(LocalSearchPhaseNode(ops, max_iterations=100))
            else:
                # Perturbation phase
                search_phases.append(PerturbationPhaseNode(
                    random.choice(ConfigurationFactory.PERTURBATIONS).copy(),
                    strength=random.uniform(0.1, 0.4)
                ))
        
        termination = random.choice(ConfigurationFactory.TERMINATIONS).copy()
        acceptance = random.choice(ConfigurationFactory.ACCEPTANCES).copy()
        
        ast = AlgorithmNode(init, search_phases, termination, acceptance)
        
        return Configuration(
            ast=ast,
            iteration_created=0,
            created_by="initialization"
        )
    
    @staticmethod
    def create_ils_classic() -> Configuration:
        """Create classic ILS algorithm (reference)"""
        init = InitPhaseNode(DSATURNode())
        search = [
            LocalSearchPhaseNode([KempeChainNode(max_iterations=100)]),
            PerturbationPhaseNode(RandomRecolorNode(strength=0.2)),
            LocalSearchPhaseNode([KempeChainNode(max_iterations=100)])
        ]
        term = MaxIterNode(max_iterations=500)
        accept = BetterOrEqualNode()
        ast = AlgorithmNode(init, search, term, accept)
        
        return Configuration(
            ast=ast,
            iteration_created=0,
            created_by="initialization"
        )
    
    @staticmethod
    def create_intensive_local_search() -> Configuration:
        """Create configuration emphasizing local search"""
        init = InitPhaseNode(DSATURNode())
        search = [
            LocalSearchPhaseNode([KempeChainNode(100), TabuSearchNode(100)])
        ]
        term = MaxIterNode(max_iterations=1000)
        accept = FirstImprovementNode()
        ast = AlgorithmNode(init, search, term, accept)
        
        return Configuration(
            ast=ast,
            iteration_created=0,
            created_by="initialization"
        )


# ============================================================================
# OPERATORS: MUTATION, LOCAL SEARCH, PERTURBATION
# ============================================================================

class MutationOperator:
    """Mutation operators for changing configurations"""
    
    @staticmethod
    def mutate_constructive(config: Configuration) -> Configuration:
        """Change constructive heuristic"""
        mutated = config.copy()
        new_constructive = random.choice(ConfigurationFactory.CONSTRUCTIVES).copy()
        mutated.ast.init_phase.constructive = new_constructive
        return mutated
    
    @staticmethod
    def mutate_ls_operator(config: Configuration) -> Configuration:
        """Change local search operator"""
        mutated = config.copy()
        for phase in mutated.ast.search_phases:
            if isinstance(phase, LocalSearchPhaseNode) and phase.operators:
                idx = random.randint(0, len(phase.operators) - 1)
                phase.operators[idx] = random.choice(ConfigurationFactory.LS_OPERATORS).copy()
        return mutated
    
    @staticmethod
    def mutate_perturbation(config: Configuration) -> Configuration:
        """Change perturbation operator"""
        mutated = config.copy()
        for phase in mutated.ast.search_phases:
            if isinstance(phase, PerturbationPhaseNode):
                phase.operator = random.choice(ConfigurationFactory.PERTURBATIONS).copy()
        return mutated
    
    @staticmethod
    def mutate_parameter(config: Configuration) -> Configuration:
        """Change parameter values"""
        mutated = config.copy()
        for node in mutated.ast.all_nodes():
            if hasattr(node, 'parameters'):
                for param_name in list(node.parameters.keys()):
                    if param_name == 'max_iterations':
                        node.parameters[param_name] = random.choice([50, 100, 200, 500])
                    elif param_name == 'strength':
                        node.parameters[param_name] = random.uniform(0.1, 0.5)
                    elif param_name == 'tabu_tenure':
                        node.parameters[param_name] = random.choice([5, 10, 20])
        return mutated
    
    @staticmethod
    def mutate_structure(config: Configuration) -> Configuration:
        """Add or remove search phase"""
        mutated = config.copy()
        
        if random.random() < 0.5 and len(mutated.ast.search_phases) < 5:
            # Insert phase
            new_phase = random.choice([
                LocalSearchPhaseNode([random.choice(ConfigurationFactory.LS_OPERATORS)]),
                PerturbationPhaseNode(random.choice(ConfigurationFactory.PERTURBATIONS))
            ])
            position = random.randint(0, len(mutated.ast.search_phases))
            mutated.ast.search_phases.insert(position, new_phase)
        
        elif random.random() < 0.5 and len(mutated.ast.search_phases) > 1:
            # Remove phase
            position = random.randint(0, len(mutated.ast.search_phases) - 1)
            mutated.ast.search_phases.pop(position)
        
        return mutated
    
    @staticmethod
    def apply_random_mutation(config: Configuration, strength: float = 0.20) -> Configuration:
        """
        Apply random mutation with given strength.
        
        strength: fraction of mutation types to apply
        """
        mutation_ops = [
            MutationOperator.mutate_constructive,
            MutationOperator.mutate_ls_operator,
            MutationOperator.mutate_perturbation,
            MutationOperator.mutate_parameter,
            MutationOperator.mutate_structure
        ]
        
        mutated = config.copy()
        num_mutations = max(1, int(len(mutation_ops) * strength))
        
        selected_ops = random.sample(mutation_ops, num_mutations)
        for op in selected_ops:
            mutated = op(mutated)
        
        mutated.created_by = "perturbation"
        return mutated


class LocalSearchPhase:
    """Local search over configuration space (parameter tuning)"""
    
    @staticmethod
    def parameter_tuning(config: Configuration,
                        max_moves: int = 10,
                        max_no_improve: int = 3) -> Tuple[Configuration, int]:
        """
        Local search: tune parameters of current configuration.
        
        Returns:
            (improved_config, num_improvements)
        """
        current = config.copy()
        improvements = 0
        no_improve_count = 0
        moves_tried = 0
        
        for _ in range(max_moves):
            if no_improve_count >= max_no_improve:
                break
            
            moves_tried += 1
            
            # Generate neighbor by small parameter change
            neighbor = LocalSearchPhase._generate_neighbor(current)
            
            # Check if neighbor is better (will be evaluated externally)
            # For now, just return candidate
            # Actual comparison happens in ILS main loop
            
            current = neighbor
        
        return current, improvements
    
    @staticmethod
    def _generate_neighbor(config: Configuration) -> Configuration:
        """Generate neighbor by small change"""
        neighbor = config.copy()
        
        # Small parameter change
        for node in neighbor.ast.all_nodes():
            if hasattr(node, 'parameters') and random.random() < 0.3:
                for param_name in list(node.parameters.keys()):
                    if param_name == 'max_iterations':
                        # Small change: ±10%
                        old_val = node.parameters[param_name]
                        node.parameters[param_name] = max(10, int(old_val * random.uniform(0.9, 1.1)))
                    elif param_name == 'strength':
                        old_val = node.parameters[param_name]
                        node.parameters[param_name] = max(0.05, min(0.9, old_val + random.uniform(-0.05, 0.05)))
        
        neighbor.created_by = "local_search"
        return neighbor


# ============================================================================
# FITNESS AGGREGATION
# ============================================================================

class FitnessAggregator:
    """Aggregate fitness scores across instances and objectives"""
    
    @staticmethod
    def aggregate_fitness(config: Configuration, weights: Dict[str, float]) -> float:
        """
        Compute aggregated fitness from:
        1. Per-instance quality scores
        2. Time efficiency
        3. Robustness (consistency)
        4. Feasibility
        
        Returns: Single fitness value (lower is better)
        """
        
        if not config.fitness_scores:
            return float('inf')
        
        # Quality: average colors used across instances
        quality_scores = list(config.fitness_scores.values())
        mean_quality = sum(quality_scores) / len(quality_scores) if quality_scores else float('inf')
        
        # Robustness: std dev of colors (lower = more consistent)
        if len(quality_scores) > 1:
            mean = sum(quality_scores) / len(quality_scores)
            variance = sum((x - mean) ** 2 for x in quality_scores) / len(quality_scores)
            robustness = variance ** 0.5
        else:
            robustness = 0
        
        # Time: approximated by AST complexity
        ast_stats = ast_statistics(config.ast)
        time_penalty = ast_stats['num_nodes'] * 0.01
        
        # Feasibility
        feasibility = 1.0 if all(s < float('inf') for s in quality_scores) else 100.0
        
        # Weighted combination
        components = {
            'quality': mean_quality,
            'time': time_penalty,
            'robustness': robustness,
            'feasibility': feasibility
        }
        
        weighted_fitness = sum(
            components[key] * weights.get(key, 0.0)
            for key in components
        )
        
        return weighted_fitness


# ============================================================================
# ITERATED LOCAL SEARCH MAIN
# ============================================================================

class IteratedLocalSearchOptimizer:
    """
    ILS-based search for optimal ILS algorithm configurations.
    
    The ILS structure mirrors the original ILS for GCP:
    1. Initialization: Create random configuration
    2. Local Search: Tune parameters of current configuration
    3. Perturbation: Escape local optimum via mutation
    4. Acceptance: Decide if accept perturbed solution
    5. Iteration: Repeat until convergence
    """
    
    def __init__(self, config: ILSConfig):
        self.config = config
        self.best_configuration: Optional[Configuration] = None
        self.current_configuration: Optional[Configuration] = None
        self.history: List[ILSStatistics] = []
        
        if config.seed is not None:
            random.seed(config.seed)
    
    def initialize(self) -> None:
        """Initialize with reference + random configurations"""
        
        # Start with one of the reference configurations
        self.current_configuration = ConfigurationFactory.create_ils_classic()
        self.best_configuration = self.current_configuration.copy()
    
    def search(self, 
               fitness_function: Callable[[Configuration], Dict[str, float]],
               callback: Optional[Callable[[ILSStatistics], None]] = None) -> Configuration:
        """
        Main ILS search loop for finding optimal configurations.
        
        Args:
            fitness_function: Evaluates Configuration and sets fitness_scores
            callback: Called after each iteration with statistics
        
        Returns:
            Best configuration found
        """
        
        start_time = time.time()
        no_improve_count = 0
        
        print(f"[ILS] Starting configuration search...")
        print(f"[ILS] Max iterations: {self.config.max_iterations}")
        print(f"[ILS] Perturbation strength: {self.config.perturbation_strength}")
        
        for iteration in range(self.config.max_iterations):
            iter_start = time.time()
            
            # 1. EVALUATE current configuration (if not evaluated)
            if self.current_configuration.aggregated_fitness == float('inf'):
                self.current_configuration.fitness_scores = fitness_function(self.current_configuration)
                self.current_configuration.aggregated_fitness = FitnessAggregator.aggregate_fitness(
                    self.current_configuration, 
                    self.config.fitness_weights
                )
            
            # 2. LOCAL SEARCH: Tune parameters (improvement phase)
            if self.config.enable_local_search:
                ls_config, ls_improvements = LocalSearchPhase.parameter_tuning(
                    self.current_configuration,
                    max_moves=self.config.ls_max_moves,
                    max_no_improve=self.config.ls_max_no_improve
                )
                ls_config.fitness_scores = fitness_function(ls_config)
                ls_config.aggregated_fitness = FitnessAggregator.aggregate_fitness(
                    ls_config,
                    self.config.fitness_weights
                )
                
                if ls_config.aggregated_fitness < self.current_configuration.aggregated_fitness:
                    self.current_configuration = ls_config
            
            # 3. Update best if improved
            if self.current_configuration.aggregated_fitness < self.best_configuration.aggregated_fitness:
                self.best_configuration = self.current_configuration.copy()
                no_improve_count = 0
            else:
                no_improve_count += 1
            
            # 4. PERTURBATION: Escape local optimum
            perturbed = MutationOperator.apply_random_mutation(
                self.current_configuration,
                strength=self.config.perturbation_strength
            )
            perturbed.fitness_scores = fitness_function(perturbed)
            perturbed.aggregated_fitness = FitnessAggregator.aggregate_fitness(
                perturbed,
                self.config.fitness_weights
            )
            
            # 5. ACCEPTANCE CRITERION
            should_accept = self._acceptance_criterion(
                self.current_configuration.aggregated_fitness,
                perturbed.aggregated_fitness
            )
            
            if should_accept:
                self.current_configuration = perturbed
            
            # 6. STATISTICS
            stats = ILSStatistics(
                iteration=iteration,
                best_fitness=self.best_configuration.aggregated_fitness,
                current_fitness=self.current_configuration.aggregated_fitness,
                best_configuration=self.best_configuration,
                current_configuration=self.current_configuration,
                improvements_found=sum(1 for s in self.history if s.best_fitness < s.current_fitness),
                acceptances=sum(1 for s in self.history if s.current_fitness <= s.best_fitness),
                mutations_applied=1,  # One per iteration
                perturbations_applied=1,
                elapsed_time=time.time() - start_time,
                iteration_time=time.time() - iter_start,
                total_evaluations=len(self.history) + 1
            )
            
            self.history.append(stats)
            
            if callback:
                callback(stats)
            
            # 7. TERMINATION CHECKS
            if no_improve_count >= self.config.max_no_improve_iterations:
                print(f"[ILS] No improvement for {no_improve_count} iterations. Stopping.")
                break
            
            if time.time() - start_time > self.config.max_time_seconds:
                print(f"[ILS] Time limit exceeded. Stopping.")
                break
            
            if self.config.target_fitness and self.best_configuration.aggregated_fitness <= self.config.target_fitness:
                print(f"[ILS] Target fitness reached. Stopping.")
                break
            
            # Progress output
            if (iteration + 1) % 5 == 0:
                print(f"[ILS] Iter {iteration + 1}: "
                      f"best={stats.best_fitness:.4f}, "
                      f"current={stats.current_fitness:.4f}, "
                      f"time={stats.iteration_time:.2f}s")
        
        print(f"[ILS] Search complete. Best fitness: {self.best_configuration.aggregated_fitness:.4f}")
        return self.best_configuration
    
    def _acceptance_criterion(self, f_current: float, f_candidate: float) -> bool:
        """Determine if candidate should be accepted"""
        
        if self.config.acceptance_criterion == "better":
            return f_candidate < f_current
        elif self.config.acceptance_criterion == "better_or_equal":
            return f_candidate <= f_current
        elif self.config.acceptance_criterion == "always":
            return True
        else:
            return f_candidate <= f_current  # default


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Configuration for ILS-based search
    config = ILSConfig(
        max_iterations=500,
        max_no_improve_iterations=50,
        enable_local_search=True,
        ls_max_moves=10,
        perturbation_strength=0.20,
        acceptance_criterion="better_or_equal"
    )
    
    # Dummy fitness function (for testing)
    def dummy_fitness(cfg: Configuration) -> Dict[str, float]:
        """Dummy fitness: penalize complex ASTs"""
        stats = ast_statistics(cfg.ast)
        size = stats['num_nodes']
        return {'dummy_instance': float(size)}
    
    # Run ILS search
    ils = IteratedLocalSearchOptimizer(config)
    ils.initialize()
    
    def print_progress(stats: ILSStatistics):
        if stats.iteration % 10 == 0:
            print(f"ILS: {stats}")
    
    best = ils.search(dummy_fitness, callback=print_progress)
    
    print(f"\n=== BEST CONFIGURATION FOUND ===")
    print(best.ast.to_pseudocode())
    print(f"Fitness: {best.aggregated_fitness:.4f}")
    print(f"AST Statistics: {ast_statistics(best.ast)}")
