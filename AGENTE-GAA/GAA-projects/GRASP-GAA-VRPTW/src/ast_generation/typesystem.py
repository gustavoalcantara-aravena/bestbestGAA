# src/ast/typesystem.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


TYPE_NUM = "numeric"
TYPE_BOOL = "bool"
TYPE_CAT = "categorical"


@dataclass
class TypeResult:
    ok: bool
    inferred: Optional[str]
    error: Optional[str] = None


class TypeSystem:
    """
    Sistema de tipos mínimo para AST:
      - numeric, bool, categorical
      - inferencia recursiva desde JSON node

    feature_types: dict feature_name -> type
    """

    def __init__(self, feature_types: Dict[str, str], operator_pool: Optional[List[str]] = None):
        self.feature_types = dict(feature_types)
        self.operator_pool = set(operator_pool or [])

    def feature_type(self, name: str) -> str:
        if name not in self.feature_types:
            raise KeyError(f"Feature no registrada: {name}")
        return self.feature_types[name]

    def infer_type(self, node: Dict[str, Any]) -> TypeResult:
        t = node.get("type")
        if t is None:
            return TypeResult(False, None, "Node sin campo 'type'")

        # terminals
        if t == "Feature":
            name = node.get("name")
            if not name:
                return TypeResult(False, None, "Feature sin name")
            if name not in self.feature_types:
                return TypeResult(False, None, f"Feature desconocida: {name}")
            return TypeResult(True, self.feature_types[name])

        if t == "Const":
            v = node.get("value")
            if isinstance(v, (int, float)):
                return TypeResult(True, TYPE_NUM)
            if isinstance(v, bool):
                return TypeResult(True, TYPE_BOOL)
            if isinstance(v, str):
                return TypeResult(True, TYPE_CAT)
            return TypeResult(False, None, f"Const con tipo no soportado: {type(v)}")

        # numeric ops
        if t in {"Add", "Sub", "Mul", "Div", "Min", "Max"}:
            a = self.infer_type(node["a"])
            b = self.infer_type(node["b"])
            if not (a.ok and b.ok):
                return TypeResult(False, None, a.error or b.error)
            if a.inferred != TYPE_NUM or b.inferred != TYPE_NUM:
                return TypeResult(False, None, f"{t} requiere numeric, got {a.inferred},{b.inferred}")
            return TypeResult(True, TYPE_NUM)

        if t == "Neg":
            a = self.infer_type(node["a"])
            if not a.ok:
                return a
            if a.inferred != TYPE_NUM:
                return TypeResult(False, None, "Neg requiere numeric")
            return TypeResult(True, TYPE_NUM)

        if t == "WeightedSum":
            terms = node.get("terms", [])
            if not isinstance(terms, list) or len(terms) == 0:
                return TypeResult(False, None, "WeightedSum sin terms")
            for it in terms:
                w = self.infer_type(it["w"])
                x = self.infer_type(it["x"])
                if not (w.ok and x.ok):
                    return TypeResult(False, None, w.error or x.error)
                if w.inferred != TYPE_NUM or x.inferred != TYPE_NUM:
                    return TypeResult(False, None, "WeightedSum requiere w,x numeric")
            return TypeResult(True, TYPE_NUM)

        # comparisons
        if t in {"Less", "LessEq", "Greater", "GreaterEq"}:
            a = self.infer_type(node["a"])
            b = self.infer_type(node["b"])
            if not (a.ok and b.ok):
                return TypeResult(False, None, a.error or b.error)
            if a.inferred != TYPE_NUM or b.inferred != TYPE_NUM:
                return TypeResult(False, None, f"{t} requiere numeric")
            return TypeResult(True, TYPE_BOOL)

        # boolean ops
        if t in {"And", "Or"}:
            a = self.infer_type(node["a"])
            b = self.infer_type(node["b"])
            if not (a.ok and b.ok):
                return TypeResult(False, None, a.error or b.error)
            if a.inferred != TYPE_BOOL or b.inferred != TYPE_BOOL:
                return TypeResult(False, None, f"{t} requiere bool")
            return TypeResult(True, TYPE_BOOL)

        if t == "Not":
            a = self.infer_type(node["a"])
            if not a.ok:
                return a
            if a.inferred != TYPE_BOOL:
                return TypeResult(False, None, "Not requiere bool")
            return TypeResult(True, TYPE_BOOL)

        # if
        if t == "If":
            c = self.infer_type(node["cond"])
            a = self.infer_type(node["then"])
            b = self.infer_type(node["else"])
            if not (c.ok and a.ok and b.ok):
                return TypeResult(False, None, c.error or a.error or b.error)
            if c.inferred != TYPE_BOOL:
                return TypeResult(False, None, "If requiere cond bool")
            if a.inferred != b.inferred:
                return TypeResult(False, None, f"If ramas con tipos distintos: {a.inferred} vs {b.inferred}")
            return TypeResult(True, a.inferred)

        # choose operator (categorical)
        if t == "Choose":
            opts = node.get("options", [])
            if not isinstance(opts, list) or len(opts) == 0:
                return TypeResult(False, None, "Choose sin options")
            # options deben ser Const string
            for o in opts:
                ot = self.infer_type(o)
                if not ot.ok:
                    return ot
                if ot.inferred != TYPE_CAT:
                    return TypeResult(False, None, "Choose options deben ser categorical (string)")
                if self.operator_pool and o.get("value") not in self.operator_pool:
                    return TypeResult(False, None, f"Operador no permitido: {o.get('value')}")
            return TypeResult(True, TYPE_CAT)

        return TypeResult(False, None, f"Tipo de nodo no soportado: {t}")
