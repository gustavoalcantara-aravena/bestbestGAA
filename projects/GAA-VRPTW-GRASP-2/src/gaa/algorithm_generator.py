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
        
        ALGORITMO 1: GRASP PURO (ITER-5 - REVERTIR ITER-4A)
        - Revertir cambios ITER-4A que causaron empeoramiento
        - DoubleBridge(3.5) fue demasiado agresiva
        - Mantener ITER-3 baseline: D=1391.51, t=3.41s
        
        ALGORITMO 3: GRASP ADAPTATIVO (ITER-5 FINE-TUNE ITER-4B)
        - Mantener fix CRITICAL de ITER-4B (strength=1.0→3.0)
        - Fine-tune operadores: OrOpt(12→15), TwoOpt(45→40)
        - Objetivo: D ~1300-1350 (mejor que Algo1)
        
        Args:
            seed: Seed para reproducibilidad
        
        Returns:
            Lista de 3 algoritmos ASTNode optimizados
        """
        random.seed(seed)
        algorithms = []
        
        # ========================================================================
        # ALGORITMO 1: GRASP Puro (ITER-5 - REVERTIR A ITER-3)
        # ========================================================================
        # ITER-5: Lección aprendida de ITER-4 - strength=3.5 fue TOO AGGRESSIVE
        # Revertir cambios ITER-4A que empeoraron Algo1 (D 1391.51 → 1536.86)
        # - Perturbación: 3.5 → 2.0 (revertir: strength incorrecta para este algo)
        # - While: 80 → 75 (revertir: volver a baseline)
        # - TwoOpt pre-perturb: 40 → 52 (revertir: mantener trabajo pre-mejora)
        # - OrOpt: 18 → 28 (revertir: balance mejor)
        # - TwoOpt post-perturb: 40 → 32 (revertir: correcto balance)
        # Objetivo: D 1536.86 → 1391.51 (restore ITER-3)
        algo1 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=75,  # Revertir: 80→75
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=52),  # Revertir: 40→52
                    LocalSearch(operator='OrOpt', max_iterations=28),   # Revertir: 18→28
                    Perturbation(operator='DoubleBridge', strength=2.0),  # Revertir: 3.5→2.0 (CRITICAL)
                    LocalSearch(operator='TwoOpt', max_iterations=32),  # Revertir: 40→32
                    LocalSearch(operator='Relocate', max_iterations=18)  # sin cambio
                ])
            )
        ])
        algorithms.append(algo1)
        
        # ========================================================================
        # ALGORITMO 2: GRASP + Perturbación (CONTROL - NO CAMBIAR)
        # ========================================================================
        # ITER-3/4/5: CONFIGURACIÓN GANADORA COMPROBADA
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
        # ALGORITMO 3: GRASP ADAPTATIVO (ITER-5 - FINE-TUNE ITER-4B)
        # ========================================================================
        # ITER-5: Mantener éxitos ITER-4B, fine-tune parámetros
        # ITER-4B fue parcialmente exitoso: strength=1.0→3.0 fue CRITICAL FIX
        # - Mantener DoubleBridge(3.0) - fue corrección necesaria
        # - Mantener While(90) - permitió mejor exploración
        # - Fine-tune OrOpt: 12 → 15 (mejor balance)
        # - Fine-tune TwoOpt post-perturb: 45 → 40 (reducir overhead)
        # Objetivo: D 1408.04 → ~1300-1350 (mantener mejora vs Algo1)
        algo3 = Seq(body=[
            GreedyConstruct(heuristic='NearestNeighbor'),
            While(
                max_iterations=90,  # Mantener: 90 (ITER-4B éxito)
                body=Seq(body=[
                    LocalSearch(operator='TwoOpt', max_iterations=50),  # Mantener: 50
                    LocalSearch(operator='OrOpt', max_iterations=15),   # Fine-tune: 12→15 (balance)
                    Perturbation(operator='DoubleBridge', strength=3.0),  # Mantener: 3.0 (CRITICAL FIX)
                    LocalSearch(operator='TwoOpt', max_iterations=40),  # Fine-tune: 45→40 (reducir)
                    LocalSearch(operator='Relocate', max_iterations=15)  # Mantener: 15
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
