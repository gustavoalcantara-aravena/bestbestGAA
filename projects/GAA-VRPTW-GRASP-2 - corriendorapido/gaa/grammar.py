"""
Grammar - Definición de la gramática BNF para algoritmos VRPTW-GRASP
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Grammar:
    """
    Gramática BNF para algoritmos VRPTW-GRASP
    
    Define:
    - Terminales disponibles (operadores constructivos, mejora, perturbación)
    - Límites de profundidad y complejidad
    - Restricciones de estructura válida
    """
    
    # TERMINALES CONSTRUCTIVOS (6 opciones)
    CONSTRUCTIVE_TERMINALS = [
        "NearestNeighbor",
        "Savings",
        "Sweep",
        "TimeOrientedNN",
        "RegretInsertion",
        "RandomizedInsertion"
    ]
    
    # TERMINALES DE MEJORA LOCAL (8 opciones)
    IMPROVEMENT_TERMINALS = [
        # Intra-route
        "TwoOpt",
        "OrOpt",
        "ThreeOpt",
        "Relocate",
        # Inter-route
        "CrossExchange",
        "TwoOptStar",
        "SwapCustomers",
        "RelocateInter"
    ]
    
    # TERMINALES DE PERTURBACIÓN (4 opciones)
    PERTURBATION_TERMINALS = [
        "RandomRouteRemoval",
        "WorseFeasibleMove",
        "RandomRelocate",
        "SegmentShift"
    ]
    
    # CONDICIONES
    CONDITIONS = [
        "Improves",
        "Feasible",
        "StagnationCount",
        "TimeLimit"
    ]
    
    # ESTRUCTURAS DE CONTROL
    CONTROL_STRUCTURES = [
        "Seq",
        "If",
        "While",
        "For"
    ]
    
    # Parámetros de la gramática
    min_depth: int = 2
    max_depth: int = 5
    
    def __post_init__(self):
        """Inicializar atributos derivados"""
        self.all_terminals = (
            self.CONSTRUCTIVE_TERMINALS +
            self.IMPROVEMENT_TERMINALS +
            self.PERTURBATION_TERMINALS
        )
        
        self.all_operators = (
            self.all_terminals + 
            self.CONDITIONS + 
            self.CONTROL_STRUCTURES
        )
    
    def validate_ast(self, ast) -> List[str]:
        """
        Valida que un AST respeta la gramática
        
        Args:
            ast: Árbol de sintaxis abstracta a validar
        
        Returns:
            Lista de errores (vacía si es válido)
        """
        from .ast_nodes import ASTNode
        
        errors = []
        
        # Validar que es un AST válido
        if not isinstance(ast, ASTNode):
            errors.append("AST raíz no es un ASTNode")
            return errors
        
        # Validar profundidad
        depth = ast.depth()
        if depth > self.max_depth:
            errors.append(f"Profundidad {depth} excede máximo {self.max_depth}")
        if depth < self.min_depth:
            errors.append(f"Profundidad {depth} menor que mínimo {self.min_depth}")
        
        # Validar tamaño
        size = ast.size()
        if size > 100:
            errors.append(f"AST muy grande ({size} nodos)")
        if size < 3:
            errors.append(f"AST muy pequeño ({size} nodos, mínimo 3)")
        
        return errors
    
    def get_statistics(self, ast) -> Dict[str, Any]:
        """
        Obtiene estadísticas del AST
        
        Args:
            ast: Árbol a analizar
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'depth': ast.depth(),
            'size': ast.size(),
            'num_constructive': self._count_operator_type(ast, 'GreedyConstruct'),
            'num_improvement': self._count_operator_type(ast, 'LocalSearch'),
            'num_perturbation': self._count_operator_type(ast, 'Perturbation'),
            'num_control': self._count_operator_type(ast, ['Seq', 'If', 'While', 'For']),
        }
    
    def _count_operator_type(self, ast, operator_type) -> int:
        """Cuenta nodos de un tipo específico"""
        from .ast_nodes import ASTNode
        
        if isinstance(operator_type, str):
            operator_type = [operator_type]
        
        count = 0
        all_nodes = ast.get_all_nodes()
        
        for node in all_nodes:
            node_class_name = node.__class__.__name__
            if node_class_name in operator_type:
                count += 1
        
        return count
