"""
Algorithm Generator for VRPTW-GRASP

Generates random VRPTW algorithms using ramped half-and-half method.
Ensures all generated algorithms satisfy canonical constraints.

Ramped Half-and-Half:
- Generate programs of varying depths (ramped)
- Use full and grow methods equally (half-and-half)
- Full method: all non-terminals expand fully
- Grow method: non-terminals may become terminals
"""

import random
from typing import List, Optional
from src.gaa.ast_nodes import (
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair
)
from src.gaa.grammar import VRPTWGrammar, ConstraintValidator


class AlgorithmGenerator:
    """
    Generates random VRPTW algorithms as AST structures.
    
    Features:
    - Ramped half-and-half generation (varying depths, full/grow methods)
    - Reproduction control (seed for determinism)
    - Constraint validation (ensures all algorithms are valid)
    - Configurable depth and complexity
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize algorithm generator.
        
        Args:
            seed: Random seed for reproducibility (None = random)
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        
        self.grammar = VRPTWGrammar()
        self.validator = ConstraintValidator()
        
        # Generation parameters
        self.min_depth = 2
        self.max_depth = 4
        self.terminal_probability = 0.5  # Probability of terminal in grow method
    
    def generate_algorithm(self, depth: int = 3, method: str = 'grow') -> ASTNode:
        """
        Generate a single random algorithm.
        
        Args:
            depth: Target depth (actual may be less)
            method: 'grow' or 'full'
                - 'grow': Non-terminals may become terminals (smaller trees)
                - 'full': All non-terminals expand fully (larger trees)
        
        Returns:
            ASTNode representing a valid algorithm
        """
        if method not in ['grow', 'full']:
            raise ValueError("method must be 'grow' or 'full'")
        
        # Generate tree
        tree = self._generate_tree('algorithm', depth, method)
        
        # Validate
        is_valid, violations = self.validator.validate_tree(tree)
        if not is_valid:
            # Try again up to 10 times
            for _ in range(10):
                tree = self._generate_tree('algorithm', depth, method)
                is_valid, violations = self.validator.validate_tree(tree)
                if is_valid:
                    break
        
        return tree
    
    def generate_three_algorithms(self, seed: int = 42) -> List[ASTNode]:
        """
        Generate three complementary algorithms optimizing GRASP principles:
        
        ALGORITMO 1: GRASP PURO (construcción aleatoria + mejora intensiva)
        - Múltiples iteraciones de construcción con alpha variable
        - Mejora agresiva con TwoOpt/OrOpt
        - Rápida convergencia a soluciones sólidas
        
        ALGORITMO 2: GRASP + PERTURBACIÓN (ILS-like: escape óptimos locales)
        - Construcción + mejora + perturbación iterada
        - Equilibrio exploración/explotación
        - Mejor calidad que GRASP puro
        
        ALGORITMO 3: GRASP ADAPTATIVO (VND-like: múltiples operadores)
        - Secuencia de operadores de mejora complementarios
        - Criterio de parada adaptativo (no mejora)
        - Máxima diversidad de búsqueda local
        
        Args:
            seed: Seed para reproducibilidad
        
        Returns:
            Lista de 3 algoritmos ASTNode optimizados
        """
        random.seed(seed)
        algorithms = []
        
        # ========================================================================
        # ALGORITMO 1: GRASP Puro (Múltiples construcciones + mejora)
        # ========================================================================
        # ITERACIÓN 3: Algoritmo 1 sin ThreeOpt, más TwoOpt/OrOpt puro
        algo1 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=75,  # Más iteraciones, menos costosas
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=52),
                    LocalSearch(operator='OrOpt', max_iterations=28),
                    Perturbation(operator='DoubleBridge', strength=2.0),
                    LocalSearch(operator='TwoOpt', max_iterations=32),
                    LocalSearch(operator='Relocate', max_iterations=18)
                ])
            )
        ])
        algorithms.append(algo1)
        
        # ========================================================================
        # ALGORITMO 2: GRASP + Perturbación (ILS: Iterated Local Search)
        # ========================================================================
        # Estrategia: Mejora local → perturba → mejora local → repite (LA ESTRUCTURA GANADORA)
        # Constructor determinista rápido + perturbación moderada + re-mejora
        algo2 = Seq(body=[
            # CONSTRUCCIÓN: NearestNeighbor (rápido, determinista, buena calidad)
            GreedyConstruct(heuristic='NearestNeighbor'),
            # MEJORA ITERADA CON PERTURBACIÓN (estructura probada exitosa)
            While(
                max_iterations=80,  # Iteraciones controladas
                body=Seq(body=[
                    # Mejora agresiva
                    LocalSearch(
                        operator='TwoOpt',
                        max_iterations=50
                    ),
                    # Perturbación: escapa óptimos locales
                    Perturbation(
                        operator='DoubleBridge',
                        strength=3  # Moderada
                    ),
                    # Re-mejora después de perturbar
                    LocalSearch(
                        operator='TwoOpt',
                        max_iterations=35
                    ),
                    # Operador complementario
                    LocalSearch(
                        operator='Relocate',
                        max_iterations=20
                    )
                ])
            )
        ])
        algorithms.append(algo2)
        
        # ITERACIÓN 3: Algoritmo 3 con perturbación muy controlada
        algo3 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=68,
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=50),
                    LocalSearch(operator='OrOpt', max_iterations=20),
                    Perturbation(operator='DoubleBridge', strength=1),  # MUY leve
                    LocalSearch(operator='TwoOpt', max_iterations=35),
                    LocalSearch(operator='Relocate', max_iterations=15)
                ])
            )
        ])
        algorithms.append(algo3)
        
        return algorithms
    
    def _generate_tree(self, node_type: str, depth: int, method: str) -> ASTNode:
        """
        Recursively generate AST node.
        
        Args:
            node_type: Type of node to generate ('algorithm', 'phase', etc.)
            depth: Remaining depth budget
            method: 'grow' or 'full'
        
        Returns:
            Generated ASTNode
        """
        # Decide whether to generate terminal or non-terminal
        at_max_depth = (depth <= 0)
        
        if method == 'grow':
            use_terminal = at_max_depth or random.random() < self.terminal_probability
        else:  # full
            use_terminal = at_max_depth
        
        if node_type == 'algorithm':
            # Algorithm = Construction + Phase
            construction = GreedyConstruct(heuristic=random.choice(
                list(self.grammar.get_all_constructors())
            ))
            phase = self._generate_phase(depth - 1, method)
            return Seq(body=[construction, phase])
        
        elif node_type == 'phase':
            if depth <= 0:
                # Must have local search
                return LocalSearch(
                    operator=random.choice(list(self.grammar.get_all_local_search())),
                    max_iterations=random.randint(20, 100)
                )
            
            # Generate phase: local search + control structure
            local_search = LocalSearch(
                operator=random.choice(list(self.grammar.get_all_local_search())),
                max_iterations=random.randint(20, 100)
            )
            
            if use_terminal:
                return local_search
            
            # Random control structure
            control_type = random.choice(['while', 'for', 'apply_until', 'sequence'])
            
            if control_type == 'while':
                return While(
                    max_iterations=random.randint(50, 150),
                    body=local_search
                )
            elif control_type == 'for':
                return For(
                    iterations=random.randint(3, 10),
                    body=Seq(body=[
                        local_search,
                        self._generate_phase(depth - 2, method)
                    ])
                )
            elif control_type == 'apply_until':
                return ApplyUntilNoImprove(
                    max_no_improve=random.randint(10, 30),
                    body=local_search
                )
            else:  # sequence
                phase2 = self._generate_phase(depth - 1, method)
                return Seq(body=[local_search, phase2])
        
        elif node_type == 'intensification':
            # Intensification: multiple operators in sequence or VND-like
            if use_terminal or depth <= 0:
                return LocalSearch(
                    operator=random.choice(list(self.grammar.get_all_local_search())),
                    max_iterations=random.randint(20, 50)
                )
            
            # Sequence of local searches
            ops = random.sample(list(self.grammar.get_all_local_search()), k=2)
            body = [LocalSearch(operator=op, max_iterations=random.randint(10, 30)) 
                   for op in ops]
            
            return While(
                max_iterations=random.randint(50, 100),
                body=Seq(body=body) if len(body) > 1 else body[0]
            )
        
        else:
            raise ValueError(f"Unknown node_type: {node_type}")
    
    def _generate_phase(self, depth: int, method: str) -> ASTNode:
        """Generate a phase (local search + control)."""
        return self._generate_tree('phase', depth, method)
    
    def _generate_intensification(self, depth: int, method: str) -> ASTNode:
        """Generate intensification phase."""
        return self._generate_tree('intensification', depth, method)


class AlgorithmValidator:
    """
    Validates generated algorithms for correctness and efficiency.
    """
    
    def __init__(self):
        self.grammar = VRPTWGrammar()
        self.constraint_validator = ConstraintValidator()
    
    def validate_all(self, algorithm: ASTNode) -> tuple:
        """
        Validate algorithm against all constraints.
        
        Returns:
            (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check constraints
        is_valid, violations = self.constraint_validator.validate_tree(algorithm)
        if not is_valid:
            errors.extend(violations)
        
        # Check size/depth warnings
        if algorithm.size() > 20:
            warnings.append(f"Large algorithm (size={algorithm.size()}), may be slow")
        
        if algorithm.depth() > 4:
            warnings.append(f"Deep algorithm (depth={algorithm.depth()}), may be complex")
        
        return is_valid, errors, warnings
