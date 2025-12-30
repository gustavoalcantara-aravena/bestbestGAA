"""
DIMACS Parser - Carga de instancias Graph Coloring Problem

Formato DIMACS estándar:
    p edge n m
    e v1 v2
    e v1 v3
    ...

Donde:
    n = número de vértices (1-indexed)
    m = número de aristas
    e v1 v2 = arista entre vértices v1 y v2
"""

from typing import Tuple, List, Set
from pathlib import Path


class DIMACParser:
    """Parser para archivos de grafo en formato DIMACS"""
    
    @staticmethod
    def parse(filepath: str) -> Tuple[int, List[Tuple[int, int]]]:
        """
        Parsea un archivo DIMACS y extrae información del grafo.
        
        Args:
            filepath: Ruta al archivo .col
            
        Returns:
            Tupla (n, edges) donde:
            - n: número de vértices
            - edges: lista de aristas (v1, v2) con v1 < v2
            
        Raises:
            ValueError: Si el formato es inválido
            FileNotFoundError: Si el archivo no existe
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            raise ValueError(f"Error al leer archivo: {e}")
        
        n = None
        m = None
        edges = []
        edge_set = set()  # Para detectar duplicados
        
        for line_num, line in enumerate(lines, 1):
            # Ignorar líneas vacías y comentarios
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            
            # Línea de problema
            if line.startswith('p'):
                parts = line.split()
                
                if len(parts) < 4:
                    raise ValueError(
                        f"Línea {line_num}: Formato 'p edge' inválido. "
                        f"Esperado: 'p edge n m', recibido: '{line}'"
                    )
                
                if parts[1] != 'edge':
                    raise ValueError(
                        f"Línea {line_num}: Solo se soporta 'p edge', "
                        f"recibido: 'p {parts[1]}'"
                    )
                
                try:
                    n = int(parts[2])
                    m = int(parts[3])
                except ValueError:
                    raise ValueError(
                        f"Línea {line_num}: n y m deben ser enteros. "
                        f"Recibido: n={parts[2]}, m={parts[3]}"
                    )
                
                if n <= 0:
                    raise ValueError(
                        f"Línea {line_num}: n debe ser positivo, recibido: {n}"
                    )
                
                if m < 0:
                    raise ValueError(
                        f"Línea {line_num}: m debe ser no-negativo, recibido: {m}"
                    )
                
                continue
            
            # Línea de arista
            if line.startswith('e'):
                parts = line.split()
                
                if len(parts) < 3:
                    raise ValueError(
                        f"Línea {line_num}: Formato 'e' inválido. "
                        f"Esperado: 'e v1 v2', recibido: '{line}'"
                    )
                
                try:
                    v1 = int(parts[1])
                    v2 = int(parts[2])
                except ValueError:
                    raise ValueError(
                        f"Línea {line_num}: Vértices deben ser enteros. "
                        f"Recibido: v1={parts[1]}, v2={parts[2]}"
                    )
                
                # Validación: vértices en rango [1, n]
                if n is None:
                    raise ValueError(
                        f"Línea {line_num}: Arista antes de declaración 'p edge'"
                    )
                
                if v1 < 1 or v1 > n:
                    raise ValueError(
                        f"Línea {line_num}: Vértice v1={v1} fuera de rango [1, {n}]"
                    )
                
                if v2 < 1 or v2 > n:
                    raise ValueError(
                        f"Línea {line_num}: Vértice v2={v2} fuera de rango [1, {n}]"
                    )
                
                # Validación: sin auto-loops
                if v1 == v2:
                    raise ValueError(
                        f"Línea {line_num}: Auto-loop detectado ({v1}, {v2})"
                    )
                
                # Normalizar arista (v1 < v2)
                if v1 > v2:
                    v1, v2 = v2, v1
                
                # Validación: sin duplicados
                if (v1, v2) in edge_set:
                    raise ValueError(
                        f"Línea {line_num}: Arista duplicada ({v1}, {v2})"
                    )
                
                edge_set.add((v1, v2))
                edges.append((v1, v2))
        
        # Validación final
        if n is None:
            raise ValueError("Archivo no contiene línea 'p edge'")
        
        if len(edges) != m:
            raise ValueError(
                f"Número de aristas inconsistente: "
                f"esperado {m}, encontrado {len(edges)}"
            )
        
        return n, edges
    
    @staticmethod
    def parse_with_metadata(filepath: str) -> dict:
        """
        Parsea archivo DIMACS y retorna información estructurada.
        
        Args:
            filepath: Ruta al archivo .col
            
        Returns:
            Diccionario con:
            - 'n': número de vértices
            - 'edges': lista de aristas
            - 'm': número de aristas
            - 'filename': nombre del archivo
            - 'density': densidad del grafo (m / (n*(n-1)/2))
            - 'max_degree': grado máximo
            - 'min_degree': grado mínimo
            - 'avg_degree': grado promedio
        """
        path = Path(filepath)
        n, edges = DIMACParser.parse(filepath)
        
        # Calcular estadísticas
        m = len(edges)
        
        # Grados
        degrees = [0] * (n + 1)  # 1-indexed
        for v1, v2 in edges:
            degrees[v1] += 1
            degrees[v2] += 1
        
        degrees_valid = degrees[1:]  # Quitar índice 0
        max_degree = max(degrees_valid) if degrees_valid else 0
        min_degree = min(degrees_valid) if degrees_valid else 0
        avg_degree = sum(degrees_valid) / len(degrees_valid) if degrees_valid else 0
        
        # Densidad
        max_edges = n * (n - 1) / 2
        density = m / max_edges if max_edges > 0 else 0
        
        return {
            'n': n,
            'm': m,
            'edges': edges,
            'filename': path.name,
            'filepath': str(path.absolute()),
            'density': density,
            'max_degree': max_degree,
            'min_degree': min_degree,
            'avg_degree': avg_degree
        }


def validate_dimacs_file(filepath: str) -> Tuple[bool, str]:
    """
    Valida un archivo DIMACS sin cargar completamente.
    
    Args:
        filepath: Ruta al archivo
        
    Returns:
        Tupla (es_válido, mensaje)
    """
    try:
        DIMACParser.parse(filepath)
        return True, "Archivo válido"
    except Exception as e:
        return False, str(e)
