"""
Generator - GAA-GCP-ILS-4
Generador de algoritmos aleatorios respetando gramática
"""

from typing import Optional, List
import numpy as np
from .ast_nodes import (
    ASTNode, Seq, If, While, For, Call,
    GreedyConstruct, LocalSearch, Perturbation,
    random_ast, mutate_ast
)
from .grammar import Grammar


class AlgorithmGenerator:
    """
    Generador de algoritmos ILS representados como AST
    
    Genera estructuras válidas combinando:
    - Construcción greedy inicial
    - Búsqueda local iterativa
    - Perturbación y diversificación
    """
    
    def __init__(self, 
                 grammar: Optional[Grammar] = None,
                 seed: Optional[int] = None):
        """
        Inicializa generador
        
        Args:
            grammar: Gramática a usar
            seed: Semilla aleatoria para reproducibilidad
        """
        self.grammar = grammar if grammar else Grammar()
        self.rng = np.random.default_rng(seed)
        self.seed = seed
    
    def generate(self, max_depth: Optional[int] = None) -> ASTNode:
        """
        Genera algoritmo aleatorio completo
        
        Estructura típica:
        1. Construcción inicial
        2. Bucle de mejora con perturbación
        """
        if max_depth is None:
            max_depth = self.grammar.max_depth
        
        # Elegir estructura tipo
        structure = self.rng.choice([
            'simple',
            'iterative',
            'multistart_simple',
            'complex'
        ])
        
        if structure == 'simple':
            return self._generate_simple()
        elif structure == 'iterative':
            return self._generate_iterative()
        elif structure == 'multistart_simple':
            return self._generate_multistart_simple()
        else:
            return self._generate_complex()
    
    def _generate_simple(self) -> ASTNode:
        """
        Algoritmo simple: Construcción + Mejora
        
        Pseudocódigo:
            1. CONSTRUIR solución inicial
            2. MEJORAR con búsqueda local
        """
        construction = GreedyConstruct(
            heuristic=self.rng.choice([
                "DSATUR", "LF", "RandomSequential", "SL"
            ])
        )
        
        improvement = LocalSearch(
            method=self.rng.choice([
                "KempeChain", "OneVertexMove", "TabuCol"
            ]),
            max_iterations=int(self.rng.choice([100, 200, 500]))
        )
        
        return Seq(body=[construction, improvement])
    
    def _generate_iterative(self) -> ASTNode:
        """
        Algoritmo iterativo: Construcción + Bucle de mejora
        
        Pseudocódigo:
            1. CONSTRUIR solución inicial
            2. MIENTRAS iteraciones < MAX:
                 MEJORAR con búsqueda local
        """
        construction = GreedyConstruct(
            heuristic=self.rng.choice([
                "DSATUR", "LF", "RandomSequential", "SL"
            ])
        )
        
        improvement = LocalSearch(
            method=self.rng.choice([
                "KempeChain", "OneVertexMove", "TabuCol"
            ]),
            max_iterations=int(self.rng.choice([50, 100, 200]))
        )
        
        loop = While(
            max_iterations=int(self.rng.choice([100, 200, 500])),
            body=improvement
        )
        
        return Seq(body=[construction, loop])
    
    def _generate_multistart_simple(self) -> ASTNode:
        """
        Algoritmo multi-start simple
        
        Pseudocódigo:
            PARA i = 0 a N:
              1. CONSTRUIR solución
              2. MEJORAR localmente
        """
        n_tries = int(self.rng.choice([3, 5, 10]))
        
        construction = GreedyConstruct(
            heuristic=self.rng.choice([
                "DSATUR", "LF", "RandomSequential", "SL"
            ])
        )
        
        improvement = LocalSearch(
            method=self.rng.choice([
                "KempeChain", "OneVertexMove", "TabuCol"
            ]),
            max_iterations=int(self.rng.choice([100, 200]))
        )
        
        body = Seq(body=[construction, improvement])
        
        return For(iterations=n_tries, body=body)
    
    def _generate_complex(self) -> ASTNode:
        """
        Algoritmo complejo con todas las fases ILS
        
        Pseudocódigo:
            1. CONSTRUIR solución
            2. MEJORAR localmente
            3. MIENTRAS iteraciones < MAX:
                 SI mejora: 
                   MEJORAR más
                 SINO:
                   PERTURBAR y volver a intentar
        """
        construction = GreedyConstruct(
            heuristic=self.rng.choice([
                "DSATUR", "LF", "RandomSequential", "SL"
            ])
        )
        
        initial_improvement = LocalSearch(
            method=self.rng.choice([
                "KempeChain", "OneVertexMove", "TabuCol"
            ]),
            max_iterations=int(self.rng.choice([100, 200]))
        )
        
        # Cuerpo del bucle principal
        improvement = LocalSearch(
            method=self.rng.choice([
                "KempeChain", "OneVertexMove", "TabuCol"
            ]),
            max_iterations=int(self.rng.choice([50, 100]))
        )
        
        perturbation = Perturbation(
            method=self.rng.choice(["RandomRecolor", "PartialDestroy"]),
            intensity=float(self.rng.uniform(0.15, 0.35))
        )
        
        # Condicional de aceptación
        loop_body = If(
            condition="Improves",
            then_branch=improvement,
            else_branch=Seq(body=[perturbation, improvement])
        )
        
        main_loop = While(
            max_iterations=int(self.rng.choice([200, 500, 1000])),
            body=loop_body
        )
        
        return Seq(body=[construction, initial_improvement, main_loop])
    
    def generate_population(self, size: int) -> List[ASTNode]:
        """
        Genera población de algoritmos aleatorios
        
        Args:
            size: Cantidad de algoritmos
        
        Returns:
            Lista de AST
        """
        return [self.generate() for _ in range(size)]
    
    def generate_with_validation(self, max_attempts: int = 100) -> Optional[ASTNode]:
        """
        Genera algoritmo válido según gramática
        
        Args:
            max_attempts: Intentos máximos
        
        Returns:
            AST válido o None si falla
        """
        for attempt in range(max_attempts):
            ast = self.generate()
            errors = self.grammar.validate_ast(ast)
            
            if not errors:
                return ast
        
        return None
    
    def generate_fixed_structure(self) -> ASTNode:
        """
        Genera algoritmo con estructura fija: 4 nodos y profundidad 3
        
        Estructura:
        Seq (1 nodo)
          ├─ GreedyConstruct (1 nodo)
          └─ If (1 nodo)
              ├─ LocalSearch (1 nodo - then_branch)
              └─ Perturbation (1 nodo - else_branch)
        
        Total: 4 nodos, profundidad 3
        
        Returns:
            AST con 4 nodos y profundidad 3
        """
        # Nodo 1: Construcción
        construction = GreedyConstruct(
            heuristic=self.rng.choice(list(self.grammar.CONSTRUCTIVE_TERMINALS))
        )
        
        # Nodo 3: Mejora local
        improvement = LocalSearch(
            method=self.rng.choice(list(self.grammar.IMPROVEMENT_TERMINALS)),
            max_iterations=int(self.rng.choice([100, 200, 500]))
        )
        
        # Nodo 4: Perturbación
        perturbation = Perturbation(
            method=self.rng.choice(list(self.grammar.PERTURBATION_TERMINALS)),
            intensity=float(self.rng.uniform(0.15, 0.35))
        )
        
        # Nodo 2: Condicional
        conditional = If(
            condition=self.rng.choice(list(self.grammar.CONDITIONS)),
            then_branch=improvement,
            else_branch=perturbation
        )
        
        # Secuencia
        return Seq(body=[construction, conditional])
    
    def get_generation_stats(self, algorithm: ASTNode) -> dict:
        """
        Obtiene estadísticas del algoritmo generado
        
        Args:
            algorithm: AST generado
        
        Returns:
            Diccionario con estadísticas
        """
        stats = self.grammar.get_statistics(algorithm)
        stats['seed'] = self.seed
        stats['generation_method'] = 'random'
        return stats


def generate_initial_population(size: int, 
                               grammar: Optional[Grammar] = None,
                               seed: Optional[int] = None) -> List[ASTNode]:
    """
    Función de conveniencia para generar población inicial
    
    Args:
        size: Tamaño de población
        grammar: Gramática a usar
        seed: Semilla aleatoria
    
    Returns:
        Lista de algoritmos (AST)
    """
    generator = AlgorithmGenerator(grammar=grammar, seed=seed)
    return generator.generate_population(size)
