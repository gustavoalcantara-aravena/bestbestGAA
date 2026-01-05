from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# -------- Presupuestos --------

@dataclass
class Budget:
    kind: str
    value: Any


# -------- Condiciones --------

@dataclass
class Condition:
    type: str
    params: Optional[Dict[str, Any]] = None


# -------- Nodos AST --------

@dataclass
class ASTNode:
    type: str


@dataclass
class Call(ASTNode):
    name: str
    args: Optional[Dict[str, Any]] = None


@dataclass
class Seq(ASTNode):
    body: List[ASTNode]


@dataclass
class If(ASTNode):
    cond: Condition
    then_branch: ASTNode
    else_branch: ASTNode


@dataclass
class While(ASTNode):
    budget: Budget
    body: ASTNode


@dataclass
class DestroyRepair(ASTNode):
    destroy: ASTNode
    repair: ASTNode
