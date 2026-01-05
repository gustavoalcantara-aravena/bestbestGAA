import os
from typing import Dict, Set, Tuple

def load_dimacs_col(filepath: str) -> Tuple[Dict[int, Set[int]], int, int]:
    graph: Dict[int, Set[int]] = {}
    n = m_decl = 0

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue

            parts = line.split()
            if parts[0] == "p":
                if parts[1] != "edge":
                    raise ValueError("Formato DIMACS no soportado")
                n = int(parts[2])
                m_decl = int(parts[3])
                graph = {i: set() for i in range(1, n + 1)}

            elif parts[0] == "e":
                u = int(parts[1])
                v = int(parts[2])
                if u == v:
                    continue
                graph[u].add(v)
                graph[v].add(u)

    m = sum(len(vs) for vs in graph.values()) // 2
    if m_decl and m != m_decl:
        print(
            f"[WARN] {os.path.basename(filepath)}: "
            f"declaradas={m_decl}, contadas={m}"
        )

    return graph, n, m


def scan_dimacs_families(root_dir: str):
    families = {}
    for fam in os.listdir(root_dir):
        p = os.path.join(root_dir, fam)
        if os.path.isdir(p):
            files = [
                os.path.join(p, f)
                for f in os.listdir(p)
                if f.endswith(".col")
            ]
            files.sort()
            if files:
                families[fam] = files
    return families
