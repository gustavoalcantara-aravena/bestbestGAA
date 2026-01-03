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
        
        ALGORITMO 2: ALGORITMO DE CONTROL (ITER-3 - NO MODIFICAR)
        - GANADOR: D=1172.18, t=0.18s, K=0 (perfecto)
        - NearestNeighbor constructor + ILS perturbation
        - DoubleBridge(strength=3) + While(80) iteraciones
        
        ALGORITMO 1: GRASP PURO (A OPTIMIZAR)
        - Múltiples iteraciones de construcción
        - Mejora intensiva con TwoOpt/OrOpt
        - Actualmente: D=1391.51, t=3.41s
        
        ALGORITMO 3: GRASP ADAPTATIVO (A OPTIMIZAR)
        - Secuencia de operadores complementarios
        - Criterio adaptativo de parada
        - Actualmente: D=1504.34, t=0.69s
        
        Args:
            seed: Seed para reproducibilidad
        
        Returns:
            Lista de 3 algoritmos ASTNode optimizados
        """
        random.seed(seed)
        algorithms = []
        
        # ========================================================================
        # ALGORITMO 1: GRASP Puro (A OPTIMIZAR)
        # ========================================================================
        algo1 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=75,  
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
        # ALGORITMO 2: GRASP + Perturbación (CONTROL - NO CAMBIAR)
        # ========================================================================
        # ITER-3: CONFIGURACIÓN GANADORA COMPROBADA
        algo2 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=80,
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=50),
                    Perturbation(operator='DoubleBridge', strength=3),
                    LocalSearch(operator='TwoOpt', max_iterations=35),
                    LocalSearch(operator='Relocate', max_iterations=20)
                ])
            )
        ])
        algorithms.append(algo2)
        
        # ========================================================================
        # ALGORITMO 3: GRASP ADAPTATIVO (A OPTIMIZAR)
        # ========================================================================
        algo3 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=68,
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=50),
                    LocalSearch(operator='OrOpt', max_iterations=20),
                    Perturbation(operator='DoubleBridge', strength=1),
                    LocalSearch(operator='TwoOpt', max_iterations=35),
                    LocalSearch(operator='Relocate', max_iterations=15)
                ])
            )
        ])
        algorithms.append(algo3)
        
        return algorithms
    
    def _generate_tree(self, node_type: str, depth: int, method: str) -> ASTNode:
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
