"""
AST Nodes - Nodos del Árbol de Sintaxis Abstracta para VRPTW-GRASP
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class ASTNode(ABC):
    """Clase base para todos los nodos del AST"""
    
    @abstractmethod
    def depth(self) -> int:
        """Retorna la profundidad del subárbol"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Retorna el número total de nodos"""
        pass
    
    @abstractmethod
    def get_all_nodes(self) -> List['ASTNode']:
        """Retorna todos los nodos del subárbol"""
        pass
    
    @abstractmethod
    def to_pseudocode(self) -> str:
        """Retorna pseudocódigo del algoritmo"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa a diccionario"""
        pass


# ============================================================================
# NODOS DE CONTROL DE FLUJO
# ============================================================================

@dataclass
class Seq(ASTNode):
    """Secuencia: ejecuta operaciones en orden"""
    body: List[ASTNode] = field(default_factory=list)
    
    def depth(self) -> int:
        if not self.body:
            return 1
        return 1 + max(node.depth() for node in self.body)
    
    def size(self) -> int:
        return 1 + sum(node.size() for node in self.body)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        for node in self.body:
            nodes.extend(node.get_all_nodes())
        return nodes
    
    def to_pseudocode(self) -> str:
        lines = ["SECUENCIA:"]
        for i, node in enumerate(self.body, 1):
            code = node.to_pseudocode()
            for line in code.split('\n'):
                lines.append(f"  {i}. {line}")
        return '\n'.join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Seq',
            'body': [node.to_dict() for node in self.body]
        }


@dataclass
class If(ASTNode):
    """Condicional: if-then-else"""
    condition: str = "Improves"
    then_branch: ASTNode = None
    else_branch: Optional[ASTNode] = None
    
    def depth(self) -> int:
        d_then = self.then_branch.depth() if self.then_branch else 0
        d_else = self.else_branch.depth() if self.else_branch else 0
        return 1 + max(d_then, d_else)
    
    def size(self) -> int:
        s_then = self.then_branch.size() if self.then_branch else 0
        s_else = self.else_branch.size() if self.else_branch else 0
        return 1 + s_then + s_else
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.then_branch:
            nodes.extend(self.then_branch.get_all_nodes())
        if self.else_branch:
            nodes.extend(self.else_branch.get_all_nodes())
        return nodes
    
    def to_pseudocode(self) -> str:
        then_code = self.then_branch.to_pseudocode() if self.then_branch else "nada"
        else_code = self.else_branch.to_pseudocode() if self.else_branch else "nada"
        return f"SI {self.condition}:\n  {then_code}\nSI NO:\n  {else_code}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'If',
            'condition': self.condition,
            'then_branch': self.then_branch.to_dict() if self.then_branch else None,
            'else_branch': self.else_branch.to_dict() if self.else_branch else None
        }


@dataclass
class While(ASTNode):
    """Bucle while: repite hasta condición"""
    condition: str = "IterBudget"
    max_iterations: int = 100
    body: ASTNode = None
    
    def depth(self) -> int:
        return 1 + (self.body.depth() if self.body else 0)
    
    def size(self) -> int:
        return 1 + (self.body.size() if self.body else 0)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.body:
            nodes.extend(self.body.get_all_nodes())
        return nodes
    
    def to_pseudocode(self) -> str:
        body_code = self.body.to_pseudocode() if self.body else "nada"
        return f"MIENTRAS {self.condition} < {self.max_iterations}:\n  {body_code}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'While',
            'condition': self.condition,
            'max_iterations': self.max_iterations,
            'body': self.body.to_dict() if self.body else None
        }


@dataclass
class For(ASTNode):
    """Bucle for: repite N veces"""
    iterations: int = 5
    body: ASTNode = None
    
    def depth(self) -> int:
        return 1 + (self.body.depth() if self.body else 0)
    
    def size(self) -> int:
        return 1 + (self.body.size() if self.body else 0)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.body:
            nodes.extend(self.body.get_all_nodes())
        return nodes
    
    def to_pseudocode(self) -> str:
        body_code = self.body.to_pseudocode() if self.body else "nada"
        return f"PARA i=1 HASTA {self.iterations}:\n  {body_code}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'For',
            'iterations': self.iterations,
            'body': self.body.to_dict() if self.body else None
        }


# ============================================================================
# NODOS DE OPERADORES
# ============================================================================

@dataclass
class GreedyConstruct(ASTNode):
    """Construcción greedy inicial"""
    heuristic: str = "NearestNeighbor"
    alpha: float = 0.15  # Para GRASP
    
    def depth(self) -> int:
        return 1
    
    def size(self) -> int:
        return 1
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def to_pseudocode(self) -> str:
        return f"Construcción: {self.heuristic}(alpha={self.alpha})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'GreedyConstruct',
            'heuristic': self.heuristic,
            'alpha': self.alpha
        }


@dataclass
class LocalSearch(ASTNode):
    """Búsqueda local"""
    operator: str = "TwoOpt"
    max_iterations: int = 100
    
    def depth(self) -> int:
        return 1
    
    def size(self) -> int:
        return 1
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def to_pseudocode(self) -> str:
        return f"Mejora Local: {self.operator}(max_iter={self.max_iterations})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'LocalSearch',
            'operator': self.operator,
            'max_iterations': self.max_iterations
        }


@dataclass
class Perturbation(ASTNode):
    """Perturbación para escapar de óptimos locales"""
    operator: str = "RandomRouteRemoval"
    strength: int = 2  # Número de rutas a perturbar
    
    def depth(self) -> int:
        return 1
    
    def size(self) -> int:
        return 1
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def to_pseudocode(self) -> str:
        return f"Perturbación: {self.operator}(strength={self.strength})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Perturbation',
            'operator': self.operator,
            'strength': self.strength
        }
