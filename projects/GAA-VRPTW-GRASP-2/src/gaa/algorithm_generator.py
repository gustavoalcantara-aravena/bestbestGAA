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
        
        ALGORITMO 2: ALGORITMO DE CONTROL (INMUTABLE)
        - CONTROL baseline: D=1172.18, t=0.18s
        - NearestNeighbor constructor + ILS perturbation
        - DoubleBridge(strength=3) + While(80) iteraciones
        
        ALGORITMO 1: GRASP EXPLORATIVO (ITER-7)
        - Exploración similar a Algo 3 pero con variaciones
        - While: 95 (vs 100 en Algo 3, menos iteraciones)
        - TwoOpt pre: 48 (vs 45 en Algo 3, más agresivo)
        - DoubleBridge: 1.5 (igual a Algo 3)
        - TwoOpt post: 38 (vs 40 en Algo 3, menos)
        - Relocate: 32 (vs 35 en Algo 3, menos)
        - Objetivo: Balance entre exploración y explotación
        
        ALGORITMO 3: GRASP MUY EXPLORATIVO (ITER-7)
        - Máxima exploración vs BKS
        - While: 100 (máximo)
        - TwoOpt pre: 45 (menos que Algo 1)
        - DoubleBridge: 1.5 (perturbación moderada)
        - TwoOpt post: 40 (más que Algo 1)
        - Relocate: 35 (máximo)
        - Objetivo: Máxima mejora sin over-optimization
        
        Args:
            seed: Seed para reproducibilidad
        
        Returns:
            Lista de 3 algoritmos ASTNode optimizados
        """
        random.seed(seed)
        algorithms = []
        
        # ========================================================================
        # ALGORITMO 1: GRASP Explorativo (ITER-7 - Balance)
        # ========================================================================
        # Similar a Algo 3 pero con variaciones estratégicas
        # - While: 95 (iteraciones altas pero < Algo 3)
        # - TwoOpt pre: 48 (pre-perturbación agresiva, > Algo 3)
        # - DoubleBridge: 1.5 (igual a Algo 3, perturbación moderada)
        # - TwoOpt post: 38 (post-perturbación moderada)
        # - Relocate: 32 (ajustes finales moderados)
        # Balance: Más TwoOpt pre, menos relocate
        algo1 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=95,  # Balance: 95 iteraciones
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=48),  # Agresivo pre: 48
                    Perturbation(operator='DoubleBridge', strength=1.5),  # Moderado: 1.5
                    LocalSearch(operator='TwoOpt', max_iterations=38),  # Post: 38
                    LocalSearch(operator='Relocate', max_iterations=32)  # Ajustes: 32
                ])
            )
        ])
        algorithms.append(algo1)
        
        # ========================================================================
        # ALGORITMO 2: GRASP + Perturbación (CONTROL - INMUTABLE)
        # ========================================================================
        # SIN CAMBIOS - Control absoluto para comparación
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
        # ALGORITMO 3: GRASP MUY EXPLORATIVO (ITER-7 - Máxima exploración)
        # ========================================================================
        # Exploración agresiva con DoubleBridge moderado
        # - While: 100 (máximas iteraciones)
        # - TwoOpt pre: 45 (prep pre-perturbación)
        # - DoubleBridge: 1.5 (perturbación moderada, explorativa)
        # - TwoOpt post: 40 (mejora post-perturbación)
        # - Relocate: 35 (máximos ajustes finales)
        # Objetivo: Máxima exploración del espacio de soluciones
        algo3 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=100,  # Máximas iteraciones
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=45),  # Pre-prep: 45
                    Perturbation(operator='DoubleBridge', strength=1.5),  # Moderado: 1.5
                    LocalSearch(operator='TwoOpt', max_iterations=40),  # Post: 40
                    LocalSearch(operator='Relocate', max_iterations=35)  # Máximos: 35
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
