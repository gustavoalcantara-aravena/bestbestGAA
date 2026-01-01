"""
Grammar - GAA-GCP-ILS-4
Definición de la gramática BNF para ILS con Graph Coloring Problem
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Grammar:
    """
    Gramática BNF para algoritmos ILS en GCP
    
    Define:
    - Terminales disponibles (operadores)
    - Límites de profundidad
    - Restricciones de estructura
    """
    
    # TERMINALES CONSTRUCTIVOS
    CONSTRUCTIVE_TERMINALS = [
        "DSATUR",
        "LF",
        "RandomSequential"
    ]
    
    # TERMINALES DE MEJORA LOCAL
    IMPROVEMENT_TERMINALS = [
        "KempeChain",
        "OneVertexMove",
        "TabuCol"
    ]
    
    # TERMINALES DE PERTURBACIÓN
    PERTURBATION_TERMINALS = [
        "RandomRecolor",
        "PartialDestroy"
    ]
    
    # CONDICIONES
    CONDITIONS = [
        "Improves",
        "Feasible",
        "Stagnation"
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
        
        self.all_operators = self.all_terminals + self.CONDITIONS + self.CONTROL_STRUCTURES
    
    def validate_ast(self, ast) -> List[str]:
        """
        Valida que un AST respeta la gramática
        
        Retorna lista de errores (vacía si es válido)
        """
        from .ast_nodes import (
            ASTNode, Seq, While, For, If, Call,
            GreedyConstruct, LocalSearch, Perturbation
        )
        
        errors = []
        
        # Validar estructura
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
        
        # Validar nodos
        all_nodes = ast.get_all_nodes()
        for node in all_nodes:
            if isinstance(node, GreedyConstruct):
                if node.heuristic not in self.CONSTRUCTIVE_TERMINALS:
                    errors.append(f"Heurística no válida: {node.heuristic}")
            
            elif isinstance(node, LocalSearch):
                if node.method not in self.IMPROVEMENT_TERMINALS:
                    errors.append(f"Método mejora no válido: {node.method}")
            
            elif isinstance(node, Perturbation):
                if node.method not in self.PERTURBATION_TERMINALS:
                    errors.append(f"Método perturbación no válido: {node.method}")
                if not (0.0 <= node.intensity <= 1.0):
                    errors.append(f"Intensidad fuera de rango: {node.intensity}")
            
            elif isinstance(node, Call):
                if node.operator not in self.all_terminals:
                    errors.append(f"Operador no válido: {node.operator}")
            
            elif isinstance(node, If):
                if node.condition not in self.CONDITIONS:
                    errors.append(f"Condición no válida: {node.condition}")
        
        return errors
    
    def get_statistics(self, ast) -> Dict[str, Any]:
        """Obtiene estadísticas de un AST"""
        all_nodes = ast.get_all_nodes()
        
        # Contar tipos de nodos
        from .ast_nodes import (
            GreedyConstruct, LocalSearch, Perturbation, Call,
            Seq, If, While, For
        )
        
        counts = {
            "constructive": sum(1 for n in all_nodes if isinstance(n, GreedyConstruct)),
            "improvement": sum(1 for n in all_nodes if isinstance(n, LocalSearch)),
            "perturbation": sum(1 for n in all_nodes if isinstance(n, Perturbation)),
            "call": sum(1 for n in all_nodes if isinstance(n, Call)),
            "seq": sum(1 for n in all_nodes if isinstance(n, Seq)),
            "if": sum(1 for n in all_nodes if isinstance(n, If)),
            "while": sum(1 for n in all_nodes if isinstance(n, While)),
            "for": sum(1 for n in all_nodes if isinstance(n, For)),
        }
        
        return {
            "total_nodes": len(all_nodes),
            "depth": ast.depth(),
            "node_counts": counts,
            "is_valid": len(self.validate_ast(ast)) == 0
        }


# Gramática por defecto
DEFAULT_GRAMMAR = Grammar(min_depth=2, max_depth=5)
