"""
Algorithm Generator - Generador Automático de Algoritmos VRPTW-GRASP
Genera algoritmos válidos como AST (Abstract Syntax Trees)
"""

from typing import Optional, List, Dict, Any
import random
import json
from datetime import datetime
from pathlib import Path

from .grammar import Grammar
from .ast_nodes import (
    ASTNode, Seq, If, While, For,
    GreedyConstruct, LocalSearch, Perturbation
)


class AlgorithmGenerator:
    """
    Generador de algoritmos VRPTW-GRASP representados como AST
    
    Genera estructuras válidas combinando:
    - Construcción greedy inicial (6 opciones)
    - Búsqueda local (8 opciones)
    - Perturbación y diversificación (4 opciones)
    """
    
    def __init__(self, grammar: Optional[Grammar] = None, seed: Optional[int] = None):
        """
        Inicializa el generador
        
        Args:
            grammar: Gramática a usar (default: Grammar())
            seed: Semilla para reproducibilidad
        """
        self.grammar = grammar or Grammar()
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
    
    def generate(self, max_depth: Optional[int] = None) -> ASTNode:
        """
        Genera algoritmo aleatorio válido
        
        Args:
            max_depth: Profundidad máxima (default: grammar.max_depth)
        
        Returns:
            AST raíz del algoritmo generado
        """
        if max_depth is None:
            max_depth = self.grammar.max_depth
        
        # Elegir patrón de estructura
        pattern = random.choice(['simple', 'iterative', 'multistart', 'complex'])
        
        if pattern == 'simple':
            return self._generate_simple()
        elif pattern == 'iterative':
            return self._generate_iterative()
        elif pattern == 'multistart':
            return self._generate_multistart()
        else:
            return self._generate_complex()
    
    def _generate_simple(self) -> ASTNode:
        """
        Patrón SIMPLE: Construcción + Mejora
        
        Estructura:
        Seq(
            GreedyConstruct,
            LocalSearch
        )
        """
        construction = GreedyConstruct(
            heuristic=random.choice(self.grammar.CONSTRUCTIVE_TERMINALS),
            alpha=round(random.uniform(0.1, 0.5), 2)
        )
        
        improvement = LocalSearch(
            operator=random.choice(self.grammar.IMPROVEMENT_TERMINALS),
            max_iterations=random.choice([50, 100, 150, 200])
        )
        
        return Seq(body=[construction, improvement])
    
    def _generate_iterative(self) -> ASTNode:
        """
        Patrón ITERATIVO: Construcción + While(Mejora + Perturbación)
        
        Estructura:
        Seq(
            GreedyConstruct,
            While(
                Seq(LocalSearch, Perturbation)
            )
        )
        """
        construction = GreedyConstruct(
            heuristic=random.choice(self.grammar.CONSTRUCTIVE_TERMINALS),
            alpha=round(random.uniform(0.1, 0.5), 2)
        )
        
        improvement = LocalSearch(
            operator=random.choice(self.grammar.IMPROVEMENT_TERMINALS),
            max_iterations=random.choice([50, 100, 150])
        )
        
        perturbation = Perturbation(
            operator=random.choice(self.grammar.PERTURBATION_TERMINALS),
            strength=random.choice([1, 2, 3])
        )
        
        loop_body = Seq(body=[improvement, perturbation])
        
        loop = While(
            condition="IterBudget",
            max_iterations=random.choice([100, 200, 300, 500]),
            body=loop_body
        )
        
        return Seq(body=[construction, loop])
    
    def _generate_multistart(self) -> ASTNode:
        """
        Patrón MULTI-START: For(Construcción + Mejora)
        
        Estructura:
        For(
            Seq(GreedyConstruct, LocalSearch)
        )
        """
        construction = GreedyConstruct(
            heuristic=random.choice(self.grammar.CONSTRUCTIVE_TERMINALS),
            alpha=round(random.uniform(0.1, 0.5), 2)
        )
        
        improvement = LocalSearch(
            operator=random.choice(self.grammar.IMPROVEMENT_TERMINALS),
            max_iterations=random.choice([100, 150, 200])
        )
        
        body = Seq(body=[construction, improvement])
        
        return For(
            iterations=random.choice([3, 5, 7, 10]),
            body=body
        )
    
    def _generate_complex(self) -> ASTNode:
        """
        Patrón COMPLEJO: Construcción + While(If(Mejora, Perturbación))
        
        Estructura:
        Seq(
            GreedyConstruct,
            While(
                If(Improves, LocalSearch, Perturbation)
            )
        )
        """
        construction = GreedyConstruct(
            heuristic=random.choice(self.grammar.CONSTRUCTIVE_TERMINALS),
            alpha=round(random.uniform(0.1, 0.5), 2)
        )
        
        improvement = LocalSearch(
            operator=random.choice(self.grammar.IMPROVEMENT_TERMINALS),
            max_iterations=random.choice([50, 100, 150])
        )
        
        perturbation = Perturbation(
            operator=random.choice(self.grammar.PERTURBATION_TERMINALS),
            strength=random.choice([1, 2, 3])
        )
        
        conditional = If(
            condition=random.choice(["Improves", "Feasible"]),
            then_branch=improvement,
            else_branch=perturbation
        )
        
        loop = While(
            condition="IterBudget",
            max_iterations=random.choice([200, 300, 500]),
            body=conditional
        )
        
        return Seq(body=[construction, loop])
    
    def generate_with_validation(self, max_attempts: int = 100) -> Optional[ASTNode]:
        """
        Genera algoritmo con validación
        
        Args:
            max_attempts: Intentos máximos de generación
        
        Returns:
            AST válido o None si falla
        """
        for attempt in range(max_attempts):
            ast = self.generate()
            errors = self.grammar.validate_ast(ast)
            
            if not errors:
                return ast
        
        return None
    
    def generate_three_algorithms(self, fixed_depth: int = 3, fixed_size: int = 4) -> List[Dict[str, Any]]:
        """
        Genera 3 algoritmos con CARACTERÍSTICAS IDÉNTICAS (depth=3, size=4)
        
        Esto asegura comparación justa entre GAA y algoritmos estándar (GRASP/VND/ILS)
        
        Estructura: Seq(GreedyConstruct, While(LocalSearch))
        - Depth: 1(Seq) + 1(While) + 1(LocalSearch) = 3
        - Size: 1(Seq) + 1(GreedyConstruct) + 1(While) + 1(LocalSearch) = 4
        
        Args:
            fixed_depth: Profundidad fija del AST (default: 3)
            fixed_size: Tamaño fijo del AST (default: 4)
        
        Returns:
            Lista de 3 dicts con estructura:
            {
                'name': 'GAA_Algorithm_1',
                'ast': <AST>,
                'pattern': 'simple',
                'seed': 42,
                'timestamp': '2026-01-02T...',
                'stats': {'depth': 3, 'size': 4, ...}
            }
        """
        algorithms = []
        timestamp = datetime.now().isoformat()
        
        for i in range(3):
            # Reset seed para reproducibilidad consistente
            # Cada iteración usa seed derivado del seed original
            if self.seed is not None:
                random.seed(self.seed + i)
            
            # Generar AST con características específicas (depth=3, size=4)
            # Patrón: Seq(GreedyConstruct, While(LocalSearch))
            # Depth: 1(Seq) + 1(While) + 1(LocalSearch) = 3
            # Size: 1(Seq) + 1(Greedy) + 1(While) + 1(LocalSearch) = 4
            construction = GreedyConstruct(
                heuristic=random.choice(self.grammar.CONSTRUCTIVE_TERMINALS),
                alpha=round(random.uniform(0.1, 0.5), 2)
            )
            
            improvement = LocalSearch(
                operator=random.choice(self.grammar.IMPROVEMENT_TERMINALS),
                max_iterations=random.choice([50, 100, 150, 200])
            )
            
            # Create While to increase depth
            while_loop = While(
                max_iterations=random.choice([50, 100, 150, 200]),
                body=improvement
            )
            
            # Final sequence
            ast = Seq(body=[construction, while_loop])
            
            # Validate AST
            errors = self.grammar.validate_ast(ast)
            if errors:
                print(f"[WARNING] Algorithm {i+1} failed validation: {errors}")
                continue
            
            # Get statistics
            stats = self.grammar.get_statistics(ast)
            
            # Crear metadata
            algo_dict = {
                'id': i + 1,
                'name': f'GAA_Algorithm_{i+1}',
                'ast': ast.to_dict(),
                'pattern': 'iterative-simple',  # Iterativo pero simple
                'seed': self.seed,
                'timestamp': timestamp,
                'stats': stats,
                'characteristics': {
                    'depth': stats.get('depth', 3),
                    'size': stats.get('size', 4),
                    'note': 'Fixed for fair comparison with GRASP/VND/ILS'
                }
            }
            
            algorithms.append(algo_dict)
        
        return algorithms
    
    def _detect_pattern(self, ast: ASTNode) -> str:
        """Detecta qué patrón tiene el AST"""
        if isinstance(ast, Seq):
            body_types = [type(n).__name__ for n in ast.body]
            
            # Patrón simple: Seq(GreedyConstruct, LocalSearch)
            if len(body_types) == 2 and body_types[1] == 'LocalSearch':
                return 'simple'
            
            # Patrón iterativo: Seq(GreedyConstruct, While)
            if len(body_types) == 2 and body_types[1] == 'While':
                return 'iterative'
        
        # Patrón multistart: For(...)
        if isinstance(ast, For):
            return 'multistart'
        
        return 'complex'
    
    def save_algorithms(self, algorithms: List[Dict[str, Any]], output_dir: str = "algorithms"):
        """
        Guarda algoritmos generados a archivos JSON
        
        Args:
            algorithms: Lista de algoritmos (desde generate_three_algorithms)
            output_dir: Directorio de salida
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Guardar archivo individual por algoritmo
        for algo in algorithms:
            algo_file = output_path / f"{algo['name']}.json"
            
            # Serializar (preservar estructura sin AST original)
            algo_serializable = {
                'id': algo['id'],
                'name': algo['name'],
                'ast': algo['ast'],
                'pattern': algo['pattern'],
                'seed': algo['seed'],
                'timestamp': algo['timestamp'],
                'stats': algo['stats']
            }
            
            with open(algo_file, 'w') as f:
                json.dump(algo_serializable, f, indent=2)
        
        # Guardar índice con metadata global
        index_file = output_path / '_algorithms.json'
        index_data = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_algorithms': len(algorithms),
            'seed_used': self.seed,
            'algorithms': [
                {
                    'id': a['id'],
                    'name': a['name'],
                    'pattern': a['pattern'],
                    'file': f"{a['name']}.json",
                    'stats': a['stats']
                }
                for a in algorithms
            ]
        }
        
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
