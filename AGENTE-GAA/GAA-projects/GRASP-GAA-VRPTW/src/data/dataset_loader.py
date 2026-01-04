# src/data/dataset_loader.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import csv
import math
import re


@dataclass(frozen=True)
class Node:
    id: int
    x: float
    y: float
    demand: float
    ready_time: float
    due_date: float
    service_time: float


@dataclass
class Instance:
    instance_id: str
    capacity: float
    nodes: List[Node]                 # nodes[0] must be depot
    distance_matrix: List[List[float]]
    time_matrix: List[List[float]]    # usually = distance_matrix for Solomon (speed=1)

    @property
    def depot(self) -> Node:
        return self.nodes[0]

    @property
    def clients(self) -> List[Node]:
        return self.nodes[1:]

    @property
    def n_nodes(self) -> int:
        return len(self.nodes)

    @property
    def n_customers(self) -> int:
        return len(self.nodes) - 1


def _euclid(a: Node, b: Node) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def _build_matrices(nodes: List[Node]) -> Tuple[List[List[float]], List[List[float]]]:
    n = len(nodes)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dist[i][j] = _euclid(nodes[i], nodes[j])
    # Solomon estándar: tiempo de viaje = distancia (velocidad = 1)
    time = [row[:] for row in dist]
    return dist, time


def load_instance(path: Union[str, Path], capacity_default: Optional[float] = None) -> Instance:
    """
    Carga una instancia Solomon desde .csv (como C101.csv) o .txt (formato Solomon clásico).

    Requisitos (salida):
      - depot.id = 0
      - clientes ids = 1..n
      - nodes[0] es depot

    CSV esperado (como tu C101.csv):
      Columnas: CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
      (depósito es fila con CUST NO.=1, se normaliza a id=0)

    TXT: parser básico (suficiente para Solomon estándar con bloque de clientes).
    """
    path = Path(path)
    instance_id = path.stem

    if path.suffix.lower() == ".csv":
        return _load_solomon_csv(path, instance_id, capacity_default)
    if path.suffix.lower() == ".txt":
        return _load_solomon_txt(path, instance_id, capacity_default)

    raise ValueError(f"Formato no soportado: {path.suffix} (use .csv o .txt)")


def _load_solomon_csv(path: Path, instance_id: str, capacity_default: Optional[float]) -> Instance:
    rows: List[Dict[str, str]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            rows.append(r)

    if len(rows) < 2:
        raise ValueError(f"CSV inválido (muy pocas filas): {path}")

    # Normalización de nombres de columnas (tolerante)
    def pick(d: Dict[str, str], *keys: str) -> str:
        for k in keys:
            if k in d:
                return d[k]
        # buscar por coincidencia aproximada
        low = {kk.strip().lower(): kk for kk in d.keys()}
        for k in keys:
            kk = k.strip().lower()
            if kk in low:
                return d[low[kk]]
        raise KeyError(f"No encuentro columna {keys} en CSV {path}. Columnas: {list(d.keys())}")

    nodes: List[Node] = []
    for r in rows:
        cust_no = int(float(pick(r, "CUST NO.", "CUST NO", "CUST_NO", "id")))
        x = float(pick(r, "XCOORD.", "XCOORD", "x"))
        y = float(pick(r, "YCOORD.", "YCOORD", "y"))
        demand = float(pick(r, "DEMAND", "demand"))
        ready = float(pick(r, "READY TIME", "READY_TIME", "ready_time"))
        due = float(pick(r, "DUE DATE", "DUE_DATE", "due_date"))
        service = float(pick(r, "SERVICE TIME", "SERVICE_TIME", "service_time"))

        # depot es cust_no=1 en tu CSV -> id=0
        node_id = cust_no - 1
        nodes.append(Node(node_id, x, y, demand, ready, due, service))

    # ordenar por id y verificar que depot exista como 0
    nodes.sort(key=lambda n: n.id)
    if nodes[0].id != 0:
        raise ValueError("Normalización fallida: el depósito no quedó como id=0")

    # capacity: si no viene en csv, usar default
    if capacity_default is None:
        # Solomon: depende de la familia; para C1 suele ser 200, C2 700, R2 1000, etc.
        # pero no lo inferimos aquí sin metadata => requerir config o default externo
        raise ValueError(
            f"capacity_default requerido para CSV {path} (no viene Q en el archivo). "
            "Pásalo desde config.yaml"
        )

    dist, time = _build_matrices(nodes)

    _validate_instance(nodes, capacity_default)
    return Instance(instance_id=instance_id, capacity=capacity_default, nodes=nodes,
                    distance_matrix=dist, time_matrix=time)


def _load_solomon_txt(path: Path, instance_id: str, capacity_default: Optional[float]) -> Instance:
    """
    Parser básico de Solomon TXT:
    - Busca línea con 'CAPACITY' y toma el número siguiente
    - Luego busca bloque de clientes con 7 columnas:
      id x y demand ready due service
    """
    txt = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    capacity = None

    # intentamos encontrar capacidad
    for line in txt:
        if "CAPACITY" in line.upper():
            nums = re.findall(r"[-+]?\d*\.?\d+", line)
            if nums:
                # a veces aparece "CAPACITY 200"
                capacity = float(nums[-1])
                break

    # si no está, usamos default
    if capacity is None:
        if capacity_default is None:
            raise ValueError(f"No pude inferir capacidad en {path} y no se pasó capacity_default")
        capacity = float(capacity_default)

    # buscar líneas con 7 números (id x y demand ready due service)
    data: List[Tuple[int, float, float, float, float, float, float]] = []
    for line in txt:
        nums = re.findall(r"[-+]?\d*\.?\d+", line)
        if len(nums) == 7:
            i, x, y, dem, rt, dd, st = nums
            data.append((int(float(i)), float(x), float(y), float(dem), float(rt), float(dd), float(st)))

    if len(data) < 2:
        raise ValueError(f"No se encontró bloque de nodos válido en {path}")

    # Solomon TXT típico: depot id=0 ya; si viene 1-based, normalizamos
    min_id = min(t[0] for t in data)
    if min_id == 1:
        # 1-based: depot =1 -> 0
        data = [(i - 1, x, y, dem, rt, dd, st) for (i, x, y, dem, rt, dd, st) in data]

    nodes = [Node(i, x, y, dem, rt, dd, st) for (i, x, y, dem, rt, dd, st) in sorted(data, key=lambda t: t[0])]
    if nodes[0].id != 0:
        raise ValueError("El depósito no quedó como id=0 tras parsing TXT")

    dist, time = _build_matrices(nodes)
    _validate_instance(nodes, capacity)
    return Instance(instance_id=instance_id, capacity=capacity, nodes=nodes,
                    distance_matrix=dist, time_matrix=time)


def _validate_instance(nodes: List[Node], capacity: float) -> None:
    if capacity <= 0:
        raise ValueError("Capacidad Q inválida")
    ids = [n.id for n in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs duplicados en nodos")
    if ids[0] != 0:
        raise ValueError("El primer nodo debe ser el depósito id=0")
    for n in nodes:
        if n.ready_time > n.due_date:
            raise ValueError(f"Ventana inválida en nodo {n.id}: ready>{'due'}")
        if n.ready_time < 0 or n.due_date < 0 or n.service_time < 0:
            raise ValueError(f"Tiempos negativos en nodo {n.id}")
        if n.demand < 0:
            raise ValueError(f"Demanda negativa en nodo {n.id}")
