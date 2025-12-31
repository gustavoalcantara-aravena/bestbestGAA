"""
Genetic Algorithm for AST Search in GCP-ILS-GAA

Implements genetic programming over the AST space defined in 01-System/Grammar.md
and 01-System/AST-Nodes.md.

This GA:
  - Evolves populations of AlgorithmNode ASTs
  - Uses mutation, crossover, insertion, deletion on ASTs
  - Evaluates fitness via multi-instance evaluation
  - Maintains diversity via tournament and elitism selection

Author: GAA Framework
Version: 1.0.0
"""

import random
import time
from typing import List, Tuple, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from copy import deepcopy
import heapq
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
    mutate_ast, crossover_ast, insert_phase, remove_phase,
    ast_statistics, validate_ast
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Individual:
    """Represents one algorithm (AST) in the population"""
    
    ast: AlgorithmNode
    fitness_scores: Dict[str, float] = field(default_factory=dict)  # per-instance
    aggregated_fitness: float = float('inf')  # Combined fitness value
    
    # Metadata
    generation_created: int = 0
    parent_ids: Tuple[int, int] = (None, None)  # IDs of parents
    created_by: str = "initialization"  # "mutation", "crossover", "initialization"
    
    def __hash__(self):
        return id(self)
    
    def __lt__(self, other):
        """For heap operations (better fitness = lower value)"""
        return self.aggregated_fitness < other.aggregated_fitness
    
    def __repr__(self):
        return f"Ind(fit={self.aggregated_fitness:.4f}, ast_size={self.ast.size()})"


@dataclass
class GAConfig:
    """Genetic Algorithm configuration"""
    
    population_size: int = 20  # λ (mu + lambda strategy)
    generations: int = 30  # Total generations to evolve
    
    # Selection
    tournament_size: int = 3
    elite_fraction: float = 0.1  # Top 10% copied to next generation
    
    # Mutation rates (per AST)
    mutation_rate: float = 0.4  # Prob of applying mutation
    mutation_types: Dict[str, float] = field(default_factory=lambda: {
        'change_constructive': 0.2,
        'change_ls_operator': 0.2,
        'change_perturbation': 0.2,
        'change_parameter': 0.2,
        'insert_phase': 0.1,
        'remove_phase': 0.1,
    })
    
    # Crossover
    crossover_rate: float = 0.5  # Prob of crossover vs mutation
    
    # Population dynamics
    reproduction_rate: float = 0.7  # Fraction of offspring
    lambda_: int = None  # Offspring per generation (default = population_size)
    
    # Termination
    max_time_seconds: float = 3600  # 1 hour
    max_generations: int = 100
    stagnation_generations: int = 10  # Stop if no improvement
    
    # Multi-objective
    fitness_weights: Dict[str, float] = field(default_factory=lambda: {
        'quality': 0.5,      # Minimize num_colors
        'time': 0.2,         # Minimize computation time
        'robustness': 0.2,   # Consistency across instances
        'feasibility': 0.1,  # Always find feasible solution
    })
    
    # Seed
    seed: Optional[int] = None


@dataclass
class GAStatistics:
    """Statistics collected during GA execution"""
    
    generation: int = 0
    best_fitness: float = float('inf')
    mean_fitness: float = float('inf')
    std_fitness: float = 0.0
    
    best_individual: Optional[Individual] = None
    worst_individual: Optional[Individual] = None
    
    diversity: float = 0.0  # Phenotypic diversity metric
    
    # Timing
    elapsed_time: float = 0.0
    generation_time: float = 0.0
    total_evaluations: int = 0
    
    # Evolutionary events
    mutations_applied: int = 0
    crossovers_applied: int = 0
    insertions_applied: int = 0
    deletions_applied: int = 0


# ============================================================================
# INITIALIZATION
# ============================================================================

class AlgorithmInitializer:
    """Factory for creating initial algorithm populations"""
    
    CONSTRUCTIVES = [DSATURNode(), LargestFirstNode(), SmallestLastNode(),
                    RandomSequentialNode(), RLFNode()]
    
    LS_OPERATORS = [KempeChainNode(), SingleVertexMoveNode(),
                   ColorClassMergeNode(), TabuSearchNode(), SwapColorsNode()]
    
    PERTURBATIONS = [RandomRecolorNode(), PartialDestroyNode(),
                    ShakeColorsNode()]
    
    TERMINATIONS = [MaxIterNode(500), MaxIterNode(1000), TimeLimitNode(60)]
    
    ACCEPTANCES = [BetterOrEqualNode(), FirstImprovementNode()]
    
    @staticmethod
    def create_random_algorithm() -> AlgorithmNode:
        """Create random valid algorithm"""
        # Initialization
        init = InitPhaseNode(random.choice(AlgorithmInitializer.CONSTRUCTIVES))
        
        # Search phases (1-3 phases)
        num_phases = random.randint(1, 3)
        search_phases = []
        
        for _ in range(num_phases):
            if random.random() < 0.7:
                # Local search phase
                num_ops = random.randint(1, 2)
                ops = [random.choice(AlgorithmInitializer.LS_OPERATORS).copy() 
                       for _ in range(num_ops)]
                search_phases.append(LocalSearchPhaseNode(ops, max_iterations=100))
            else:
                # Perturbation phase
                search_phases.append(PerturbationPhaseNode(
                    random.choice(AlgorithmInitializer.PERTURBATIONS).copy(),
                    strength=random.uniform(0.1, 0.4)
                ))
        
        # Termination
        termination = random.choice(AlgorithmInitializer.TERMINATIONS).copy()
        
        # Acceptance
        acceptance = random.choice(AlgorithmInitializer.ACCEPTANCES).copy()
        
        return AlgorithmNode(init, search_phases, termination, acceptance)
    
    @staticmethod
    def create_ils_classic() -> AlgorithmNode:
        """Create classic ILS algorithm"""
        init = InitPhaseNode(DSATURNode())
        search = [
            LocalSearchPhaseNode([KempeChainNode(max_iterations=100)]),
            PerturbationPhaseNode(RandomRecolorNode(strength=0.2)),
            LocalSearchPhaseNode([KempeChainNode(max_iterations=100)])
        ]
        term = MaxIterNode(max_iterations=500)
        accept = BetterOrEqualNode()
        return AlgorithmNode(init, search, term, accept)
    
    @staticmethod
    def create_greedy_intensification() -> AlgorithmNode:
        """Create algorithm emphasizing local search"""
        init = InitPhaseNode(DSATURNode())
        search = [
            LocalSearchPhaseNode([KempeChainNode(100), TabuSearchNode(100)])
        ]
        term = MaxIterNode(max_iterations=1000)
        accept = FirstImprovementNode()
        return AlgorithmNode(init, search, term, accept)


# ============================================================================
# GENETIC OPERATORS
# ============================================================================

class MutationOperator:
    """Sophisticated mutation on ASTs"""
    
    @staticmethod
    def mutate(ind: Individual, config: GAConfig) -> Individual:
        """Apply mutation to individual"""
        mutated_ast = ind.ast.copy()
        
        # Decide which mutations to apply
        for mutation_type, prob in config.mutation_types.items():
            if random.random() < prob:
                mutated_ast = MutationOperator._apply_mutation(mutated_ast, mutation_type)
        
        new_ind = Individual(
            ast=mutated_ast,
            generation_created=ind.generation_created + 1,
            created_by="mutation",
            parent_ids=(id(ind), None)
        )
        
        return new_ind
    
    @staticmethod
    def _apply_mutation(ast: AlgorithmNode, mutation_type: str) -> AlgorithmNode:
        """Apply specific mutation operation"""
        
        if mutation_type == 'change_constructive':
            new_constructive = random.choice(AlgorithmInitializer.CONSTRUCTIVES).copy()
            ast.init_phase.constructive = new_constructive
        
        elif mutation_type == 'change_ls_operator':
            for phase in ast.search_phases:
                if isinstance(phase, LocalSearchPhaseNode) and phase.operators:
                    idx = random.randint(0, len(phase.operators) - 1)
                    phase.operators[idx] = random.choice(AlgorithmInitializer.LS_OPERATORS).copy()
        
        elif mutation_type == 'change_perturbation':
            for phase in ast.search_phases:
                if isinstance(phase, PerturbationPhaseNode):
                    phase.operator = random.choice(AlgorithmInitializer.PERTURBATIONS).copy()
        
        elif mutation_type == 'change_parameter':
            # Change parameter values (e.g., max_iterations, strength)
            for node in ast.all_nodes():
                if hasattr(node, 'parameters'):
                    for param_name in node.parameters:
                        if param_name == 'max_iterations':
                            node.parameters[param_name] = random.choice([50, 100, 200, 500])
                        elif param_name == 'strength':
                            node.parameters[param_name] = random.uniform(0.1, 0.5)
        
        elif mutation_type == 'insert_phase':
            if len(ast.search_phases) < 5:
                new_phase = random.choice([
                    LocalSearchPhaseNode([random.choice(AlgorithmInitializer.LS_OPERATORS)]),
                    PerturbationPhaseNode(random.choice(AlgorithmInitializer.PERTURBATIONS))
                ])
                position = random.randint(0, len(ast.search_phases))
                ast = insert_phase(ast, new_phase, position)
        
        elif mutation_type == 'remove_phase':
            if len(ast.search_phases) > 1:
                position = random.randint(0, len(ast.search_phases) - 1)
                ast = remove_phase(ast, position)
        
        return ast


class CrossoverOperator:
    """Crossover operations on ASTs"""
    
    @staticmethod
    def crossover(ind1: Individual, ind2: Individual, config: GAConfig) -> Tuple[Individual, Individual]:
        """Perform crossover between two individuals"""
        
        child1_ast, child2_ast = crossover_ast(ind1.ast, ind2.ast)
        
        child1 = Individual(
            ast=child1_ast,
            generation_created=ind1.generation_created,
            created_by="crossover",
            parent_ids=(id(ind1), id(ind2))
        )
        
        child2 = Individual(
            ast=child2_ast,
            generation_created=ind1.generation_created,
            created_by="crossover",
            parent_ids=(id(ind1), id(ind2))
        )
        
        return child1, child2


# ============================================================================
# SELECTION STRATEGIES
# ============================================================================

class SelectionStrategy:
    """Parent selection strategies"""
    
    @staticmethod
    def tournament_selection(population: List[Individual], 
                           tournament_size: int = 3) -> Individual:
        """Select best of random tournament"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return min(tournament, key=lambda x: x.aggregated_fitness)
    
    @staticmethod
    def elitism_selection(population: List[Individual], 
                         elite_fraction: float = 0.1) -> List[Individual]:
        """Select top fraction of population"""
        k = max(1, int(len(population) * elite_fraction))
        return sorted(population, key=lambda x: x.aggregated_fitness)[:k]


# ============================================================================
# FITNESS EVALUATION
# ============================================================================

class FitnessAggregator:
    """Aggregate fitness scores across instances and objectives"""
    
    @staticmethod
    def aggregate_fitness(ind: Individual, config: GAConfig) -> float:
        """
        Compute aggregated fitness from:
        1. Per-instance quality scores
        2. Time efficiency
        3. Robustness (consistency)
        4. Feasibility
        
        Returns: Single fitness value (lower is better)
        """
        
        if not ind.fitness_scores:
            return float('inf')
        
        # Quality: average colors used across instances
        quality_scores = list(ind.fitness_scores.values())
        mean_quality = sum(quality_scores) / len(quality_scores) if quality_scores else float('inf')
        
        # Robustness: std dev of colors (lower = more consistent)
        if len(quality_scores) > 1:
            mean = sum(quality_scores) / len(quality_scores)
            variance = sum((x - mean) ** 2 for x in quality_scores) / len(quality_scores)
            robustness = variance ** 0.5
        else:
            robustness = 0
        
        # Time: approximated by AST complexity
        ast_stats = ast_statistics(ind.ast)
        time_penalty = ast_stats['num_nodes'] * 0.01  # Small penalty for complexity
        
        # Feasibility: check if all runs found solutions
        feasibility = 1.0 if all(s < float('inf') for s in quality_scores) else 100.0
        
        # Weighted combination
        components = {
            'quality': mean_quality,
            'time': time_penalty,
            'robustness': robustness,
            'feasibility': feasibility
        }
        
        weighted_fitness = sum(
            components[key] * config.fitness_weights.get(key, 0.0)
            for key in components
        )
        
        return weighted_fitness


# ============================================================================
# GENETIC ALGORITHM MAIN
# ============================================================================

class GeneticAlgorithm:
    """
    Genetic Programming search over AST space.
    
    Implements (μ + λ) evolution strategy:
    - μ: parent population size
    - λ: offspring per generation
    - Selection: tournament selection + elitism
    - Variation: mutation + crossover
    """
    
    def __init__(self, config: GAConfig):
        self.config = config
        self.population: List[Individual] = []
        self.best_individual: Optional[Individual] = None
        self.history: List[GAStatistics] = []
        
        if config.seed is not None:
            random.seed(config.seed)
        
        if config.lambda_ is None:
            config.lambda_ = config.population_size
    
    def initialize(self) -> None:
        """Create initial population"""
        
        # Add some reference algorithms
        reference_algorithms = [
            AlgorithmInitializer.create_ils_classic(),
            AlgorithmInitializer.create_greedy_intensification(),
        ]
        
        # Fill rest with random
        for algo in reference_algorithms:
            self.population.append(Individual(
                ast=algo,
                generation_created=0,
                created_by="initialization"
            ))
        
        while len(self.population) < self.config.population_size:
            self.population.append(Individual(
                ast=AlgorithmInitializer.create_random_algorithm(),
                generation_created=0,
                created_by="initialization"
            ))
    
    def evolve(self, fitness_function: Callable[[Individual], Dict[str, float]],
               callback: Optional[Callable[[GAStatistics], None]] = None) -> Individual:
        """
        Main evolution loop.
        
        Args:
            fitness_function: Evaluates Individual and sets fitness_scores
            callback: Called after each generation with statistics
        
        Returns:
            Best individual found
        """
        
        start_time = time.time()
        stagnation_count = 0
        
        print(f"[GA] Starting evolution...")
        print(f"[GA] Population size: {self.config.population_size}")
        print(f"[GA] Max generations: {self.config.max_generations}")
        
        for generation in range(self.config.max_generations):
            gen_start = time.time()
            
            # Evaluate population
            for ind in self.population:
                if ind.aggregated_fitness == float('inf'):
                    # Need to evaluate
                    ind.fitness_scores = fitness_function(ind)
                    ind.aggregated_fitness = FitnessAggregator.aggregate_fitness(ind, self.config)
            
            # Select best
            gen_best = min(self.population, key=lambda x: x.aggregated_fitness)
            
            if self.best_individual is None or gen_best.aggregated_fitness < self.best_individual.aggregated_fitness:
                self.best_individual = deepcopy(gen_best)
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            # Generate offspring
            offspring = []
            
            # Elitism: copy top individuals
            elite = SelectionStrategy.elitism_selection(
                self.population, 
                self.config.elite_fraction
            )
            offspring.extend([deepcopy(ind) for ind in elite])
            
            # Create rest via recombination
            while len(offspring) < self.config.lambda_:
                if random.random() < self.config.crossover_rate:
                    # Crossover
                    parent1 = SelectionStrategy.tournament_selection(
                        self.population,
                        self.config.tournament_size
                    )
                    parent2 = SelectionStrategy.tournament_selection(
                        self.population,
                        self.config.tournament_size
                    )
                    child1, child2 = CrossoverOperator.crossover(parent1, parent2, self.config)
                    offspring.extend([child1, child2])
                else:
                    # Mutation
                    parent = SelectionStrategy.tournament_selection(
                        self.population,
                        self.config.tournament_size
                    )
                    child = MutationOperator.mutate(parent, self.config)
                    offspring.append(child)
            
            # Trim to size
            offspring = offspring[:self.config.lambda_]
            
            # Select next generation (μ + λ strategy)
            combined = self.population + offspring
            combined.sort(key=lambda x: x.aggregated_fitness)
            self.population = combined[:self.config.population_size]
            
            # Statistics
            fitness_values = [ind.aggregated_fitness for ind in self.population]
            stats = GAStatistics(
                generation=generation,
                best_fitness=min(fitness_values),
                mean_fitness=sum(fitness_values) / len(fitness_values),
                std_fitness=self._compute_std(fitness_values),
                best_individual=self.best_individual,
                worst_individual=max(self.population, key=lambda x: x.aggregated_fitness),
                elapsed_time=time.time() - start_time,
                generation_time=time.time() - gen_start,
                total_evaluations=sum(1 for ind in self.population if ind.fitness_scores)
            )
            
            self.history.append(stats)
            
            # Callback
            if callback:
                callback(stats)
            
            # Termination checks
            if stagnation_count >= self.config.stagnation_generations:
                print(f"[GA] Stagnation after {generation} generations. Stopping.")
                break
            
            if time.time() - start_time > self.config.max_time_seconds:
                print(f"[GA] Time limit exceeded. Stopping.")
                break
            
            # Progress
            if (generation + 1) % 5 == 0:
                print(f"[GA] Gen {generation + 1}: best={stats.best_fitness:.4f}, "
                      f"mean={stats.mean_fitness:.4f}, "
                      f"time={stats.generation_time:.2f}s")
        
        print(f"[GA] Evolution complete. Best fitness: {self.best_individual.aggregated_fitness:.4f}")
        return self.best_individual
    
    @staticmethod
    def _compute_std(values: List[float]) -> float:
        """Compute standard deviation"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Configuration
    config = GAConfig(
        population_size=20,
        generations=30,
        tournament_size=3,
        mutation_rate=0.4,
        crossover_rate=0.5
    )
    
    # Simple fitness function (for testing)
    def dummy_fitness(ind: Individual) -> Dict[str, float]:
        """Dummy fitness: penalize complex ASTs"""
        stats = ast_statistics(ind.ast)
        size = stats['num_nodes']
        return {'dummy_instance': float(size)}
    
    # Run GA
    ga = GeneticAlgorithm(config)
    ga.initialize()
    
    def print_progress(stats: GAStatistics):
        if stats.generation % 5 == 0:
            print(f"Gen {stats.generation}: best={stats.best_fitness:.4f}")
    
    best = ga.evolve(dummy_fitness, callback=print_progress)
    
    print(f"\n=== BEST ALGORITHM FOUND ===")
    print(best.ast.to_pseudocode())
    print(f"Fitness: {best.aggregated_fitness:.4f}")
    print(f"AST Statistics: {ast_statistics(best.ast)}")
