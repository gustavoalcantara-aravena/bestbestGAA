"""
AST Nodes - GAA-GCP-ILS-4
Definición de nodos del Árbol Sintáctico Abstracto para ILS

Tipos de nodos:
- Control: Seq, If, While, For
- Función: Call (invoca operador)
- Especializados: GreedyConstruct, LocalSearch, Perturbation
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import copy


class ASTNode(ABC):
    """Clase base para todos los nodos del AST"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el nodo a diccionario"""
        pass
    
    @abstractmethod
    def to_pseudocode(self, indent: int = 0) -> str:
        """Genera pseudocódigo legible"""
        pass
    
    @abstractmethod
    def get_all_nodes(self) -> List['ASTNode']:
        """Retorna lista de todos los nodos del subárbol"""
        pass
    
    @abstractmethod
    def get_random_node(self):
        """Retorna nodo aleatorio del subárbol (para mutación)"""
        pass
    
    def size(self) -> int:
        """Retorna cantidad total de nodos"""
        return len(self.get_all_nodes())
    
    def depth(self) -> int:
        """Retorna profundidad máxima del árbol"""
        if isinstance(self, (Call, GreedyConstruct)):
            return 1
        
        max_child_depth = 0
        if isinstance(self, (Seq, While, For, If)):
            children = []
            if isinstance(self, Seq):
                children = self.body
            elif isinstance(self, While):
                children = [self.body]
            elif isinstance(self, For):
                children = [self.body]
            elif isinstance(self, If):
                children = [self.then_branch]
                if self.else_branch:
                    children.append(self.else_branch)
            
            for child in children:
                max_child_depth = max(max_child_depth, child.depth())
        
        return 1 + max_child_depth
    
    def __repr__(self) -> str:
        return self.to_pseudocode()


@dataclass
class Seq(ASTNode):
    """Secuencia de operaciones"""
    body: List[ASTNode] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Seq",
            "body": [stmt.to_dict() for stmt in self.body]
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        if not self.body:
            return "  " * indent + "VACIO"
        
        ind = "  " * indent
        lines = []
        for i, stmt in enumerate(self.body, 1):
            stmt_code = stmt.to_pseudocode(indent + 1)
            lines.append(stmt_code)
        return "\n".join(lines)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        for stmt in self.body:
            nodes.extend(stmt.get_all_nodes())
        return nodes
    
    def get_random_node(self):
        import random
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)


@dataclass
class While(ASTNode):
    """Bucle While con presupuesto de iteraciones"""
    max_iterations: int
    body: ASTNode = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "While",
            "max_iterations": self.max_iterations,
            "body": self.body.to_dict() if self.body else None
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        body_code = self.body.to_pseudocode(indent + 1) if self.body else ""
        return f"{ind}MIENTRAS iteraciones < {self.max_iterations}:\n{body_code}"
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.body:
            nodes.extend(self.body.get_all_nodes())
        return nodes
    
    def get_random_node(self):
        import random
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)


@dataclass
class For(ASTNode):
    """Bucle For determinista"""
    iterations: int
    body: ASTNode = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "For",
            "iterations": self.iterations,
            "body": self.body.to_dict() if self.body else None
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        body_code = self.body.to_pseudocode(indent + 1) if self.body else ""
        return f"{ind}PARA i = 0 a {self.iterations}:\n{body_code}"
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.body:
            nodes.extend(self.body.get_all_nodes())
        return nodes
    
    def get_random_node(self):
        import random
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)


@dataclass
class If(ASTNode):
    """Condicional con rama then y else opcional"""
    condition: str  # "Improves", "Feasible", "Stagnation"
    then_branch: ASTNode = None
    else_branch: Optional[ASTNode] = None
    params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": "If",
            "condition": self.condition,
            "params": self.params,
            "then": self.then_branch.to_dict() if self.then_branch else None
        }
        if self.else_branch:
            result["else"] = self.else_branch.to_dict()
        return result
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}SI {self.condition}:"]
        if self.then_branch:
            lines.append(self.then_branch.to_pseudocode(indent + 1))
        if self.else_branch:
            lines.append(f"{ind}SINO:")
            lines.append(self.else_branch.to_pseudocode(indent + 1))
        return "\n".join(lines)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        if self.then_branch:
            nodes.extend(self.then_branch.get_all_nodes())
        if self.else_branch:
            nodes.extend(self.else_branch.get_all_nodes())
        return nodes
    
    def get_random_node(self):
        import random
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)


@dataclass
class Call(ASTNode):
    """Llamada a operador con argumentos opcionales"""
    operator: str
    args: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Call",
            "operator": self.operator,
            "args": self.args
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        args_str = ", ".join(f"{k}={v}" for k, v in self.args.items())
        if args_str:
            return f"{ind}{self.operator}({args_str})"
        return f"{ind}{self.operator}()"
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def get_random_node(self):
        return self


@dataclass
class GreedyConstruct(ASTNode):
    """Nodo especializado para construcción greedy"""
    heuristic: str  # "DSATUR", "LF", "RandomSequential", "SL"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "GreedyConstruct",
            "heuristic": self.heuristic
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}CONSTRUIR({self.heuristic})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def get_random_node(self):
        return self


@dataclass
class LocalSearch(ASTNode):
    """Nodo especializado para búsqueda local"""
    method: str  # "KempeChain", "OneVertexMove", "TabuCol"
    max_iterations: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LocalSearch",
            "method": self.method,
            "max_iterations": self.max_iterations
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}MEJORA_LOCAL({self.method}, iter={self.max_iterations})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def get_random_node(self):
        return self


@dataclass
class Perturbation(ASTNode):
    """Nodo especializado para perturbación"""
    method: str  # "RandomRecolor", "PartialDestroy"
    intensity: float = 0.2  # Proporción de vértices
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Perturbation",
            "method": self.method,
            "intensity": self.intensity
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}PERTURBAR({self.method}, intensidad={self.intensity:.2f})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        return [self]
    
    def get_random_node(self):
        return self


def random_ast(max_depth: int = 3, terminals: Optional[List[str]] = None, depth: int = 0) -> ASTNode:
    """Genera AST aleatorio respetando profundidad máxima"""
    import random
    
    # Si alcanzamos profundidad máxima, generar terminal
    if depth >= max_depth:
        return Call(operator=random.choice([
            "KempeChain", "OneVertexMove", "TabuCol"
        ]))
    
    # Elegir tipo de nodo
    node_type = random.choice(["construct", "local_search", "perturbation", "seq", "while", "if"])
    
    if node_type == "construct":
        return GreedyConstruct(heuristic=random.choice([
            "DSATUR", "LF", "RandomSequential", "SL"
        ]))
    
    elif node_type == "local_search":
        return LocalSearch(
            method=random.choice(["KempeChain", "OneVertexMove", "TabuCol"]),
            max_iterations=random.choice([50, 100, 200])
        )
    
    elif node_type == "perturbation":
        return Perturbation(
            method=random.choice(["RandomRecolor", "PartialDestroy"]),
            intensity=round(random.uniform(0.1, 0.4), 2)
        )
    
    elif node_type == "seq":
        n_stmts = random.randint(2, 4)
        body = [random_ast(max_depth, terminals, depth + 1) for _ in range(n_stmts)]
        return Seq(body=body)
    
    elif node_type == "while":
        return While(
            max_iterations=random.choice([50, 100, 200, 500]),
            body=random_ast(max_depth, terminals, depth + 1)
        )
    
    else:  # if
        return If(
            condition=random.choice(["Improves", "Feasible", "Stagnation"]),
            then_branch=random_ast(max_depth, terminals, depth + 1),
            else_branch=random_ast(max_depth, terminals, depth + 1) if random.random() > 0.5 else None
        )


def mutate_ast(ast: ASTNode, mutation_rate: float = 0.3) -> ASTNode:
    """Muta un AST reemplazando un nodo aleatorio"""
    import random
    
    # Copiar AST
    mutated = copy.deepcopy(ast)
    
    # Obtener todos los nodos
    all_nodes = mutated.get_all_nodes()
    
    if not all_nodes:
        return mutated
    
    # Seleccionar nodo a mutar
    idx = random.randint(0, len(all_nodes) - 1)
    node_to_mutate = all_nodes[idx]
    
    # Generar reemplazo
    if isinstance(node_to_mutate, GreedyConstruct):
        node_to_mutate.heuristic = random.choice(["DSATUR", "LF", "RandomSequential", "SL"])
    
    elif isinstance(node_to_mutate, LocalSearch):
        node_to_mutate.method = random.choice(["KempeChain", "OneVertexMove", "TabuCol"])
        node_to_mutate.max_iterations = random.choice([50, 100, 200])
    
    elif isinstance(node_to_mutate, Perturbation):
        node_to_mutate.method = random.choice(["RandomRecolor", "PartialDestroy"])
        node_to_mutate.intensity = round(random.uniform(0.1, 0.4), 2)
    
    elif isinstance(node_to_mutate, While):
        node_to_mutate.max_iterations = random.choice([50, 100, 200, 500])
    
    elif isinstance(node_to_mutate, If):
        node_to_mutate.condition = random.choice(["Improves", "Feasible", "Stagnation"])
    
    elif isinstance(node_to_mutate, Call):
        node_to_mutate.operator = random.choice(["KempeChain", "OneVertexMove", "TabuCol"])
    
    return mutated


def crossover_ast(ast1: ASTNode, ast2: ASTNode) -> tuple:
    """Crossover entre dos AST intercambiando subárboles"""
    import random
    
    # Copiar árboles
    child1 = copy.deepcopy(ast1)
    child2 = copy.deepcopy(ast2)
    
    # Obtener nodos de cada uno
    nodes1 = child1.get_all_nodes()
    nodes2 = child2.get_all_nodes()
    
    if not nodes1 or not nodes2:
        return child1, child2
    
    # Seleccionar índices de cruce
    idx1 = random.randint(0, len(nodes1) - 1)
    idx2 = random.randint(0, len(nodes2) - 1)
    
    # Intercambiar (simplificado: solo para Call y Terminal nodes)
    node1 = nodes1[idx1]
    node2 = nodes2[idx2]
    
    if isinstance(node1, Call) and isinstance(node2, Call):
        node1.operator, node2.operator = node2.operator, node1.operator
    
    return child1, child2
