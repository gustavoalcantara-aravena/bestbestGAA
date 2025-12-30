"""
VRPTW Parser - Lectura y validación de instancias Solomon

Carga archivos CSV en formato Solomon para VRPTW:
- Clientes con coordenadas, demanda, ventanas de tiempo
- Información del depósito
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple


class Client(NamedTuple):
    """Información de un cliente"""
    id: int
    x: float
    y: float
    demand: int
    ready_time: int
    due_date: int
    service_time: int


class VRPTWInstance(NamedTuple):
    """Instancia VRPTW cargada"""
    name: str
    depot: Client
    clients: List[Client]
    n_customers: int
    distance_matrix: np.ndarray
    metadata: Dict


class SolomonParser:
    """Parser para instancias Solomon VRPTW en formato CSV"""
    
    @staticmethod
    def parse(filepath: str) -> VRPTWInstance:
        """
        Carga una instancia VRPTW desde archivo CSV Solomon.
        
        Formato esperado:
        CUST NO., XCOORD., YCOORD., DEMAND, READY TIME, DUE DATE, SERVICE TIME
        
        Args:
            filepath: Ruta al archivo CSV
            
        Returns:
            VRPTWInstance con datos cargados
            
        Raises:
            ValueError: Si el formato no es válido
            FileNotFoundError: Si el archivo no existe
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        # Leer CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            raise ValueError(f"Error al leer CSV: {e}")
        
        # Validar columnas
        required_cols = ['CUST NO.', 'XCOORD.', 'YCOORD.', 'DEMAND', 
                        'READY TIME', 'DUE DATE', 'SERVICE TIME']
        
        if not all(col in df.columns for col in required_cols):
            raise ValueError(
                f"Columnas faltantes. Esperado: {required_cols}. "
                f"Encontrado: {list(df.columns)}"
            )
        
        # Procesar depósito (primera fila, índice 1)
        depot_row = df.iloc[0]
        depot = Client(
            id=0,  # Depósito siempre es 0
            x=float(depot_row['XCOORD.']),
            y=float(depot_row['YCOORD.']),
            demand=int(depot_row['DEMAND']),
            ready_time=int(depot_row['READY TIME']),
            due_date=int(depot_row['DUE DATE']),
            service_time=int(depot_row['SERVICE TIME'])
        )
        
        # Procesar clientes
        clients = [depot]  # Incluir depósito al inicio
        
        for idx, row in df.iloc[1:].iterrows():
            client = Client(
                id=len(clients),  # ID secuencial
                x=float(row['XCOORD.']),
                y=float(row['YCOORD.']),
                demand=int(row['DEMAND']),
                ready_time=int(row['READY TIME']),
                due_date=int(row['DUE DATE']),
                service_time=int(row['SERVICE TIME'])
            )
            clients.append(client)
        
        n_customers = len(clients) - 1  # Excluye depósito
        
        # Calcular matriz de distancias Euclidiana
        distance_matrix = SolomonParser._compute_distance_matrix(clients)
        
        # Metadatos
        metadata = {
            'filename': filepath.name,
            'n_customers': n_customers,
            'n_total_nodes': len(clients),
            'total_demand': sum(c.demand for c in clients[1:]),
            'time_horizon': depot.due_date,
        }
        
        return VRPTWInstance(
            name=filepath.stem,
            depot=depot,
            clients=clients,
            n_customers=n_customers,
            distance_matrix=distance_matrix,
            metadata=metadata
        )
    
    @staticmethod
    def _compute_distance_matrix(clients: List[Client]) -> np.ndarray:
        """
        Calcula matriz de distancias Euclidiana.
        
        Args:
            clients: Lista de clientes
            
        Returns:
            Matriz de distancias NxN
        """
        n = len(clients)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = clients[i].x - clients[j].x
                    dy = clients[i].y - clients[j].y
                    distances[i][j] = np.sqrt(dx*dx + dy*dy)
        
        return distances
    
    @staticmethod
    def parse_with_metadata(filepath: str) -> Dict:
        """
        Carga instancia y retorna diccionario con información completa.
        
        Args:
            filepath: Ruta al archivo CSV
            
        Returns:
            Diccionario con todos los datos y metadatos
        """
        instance = SolomonParser.parse(filepath)
        
        return {
            'name': instance.name,
            'n_customers': instance.n_customers,
            'n_nodes': len(instance.clients),
            'total_demand': instance.metadata['total_demand'],
            'time_horizon': instance.metadata['time_horizon'],
            'depot': {
                'id': instance.depot.id,
                'x': instance.depot.x,
                'y': instance.depot.y,
            },
            'clients': [
                {
                    'id': c.id,
                    'x': c.x,
                    'y': c.y,
                    'demand': c.demand,
                    'ready_time': c.ready_time,
                    'due_date': c.due_date,
                    'service_time': c.service_time,
                }
                for c in instance.clients
            ],
            'distance_matrix': instance.distance_matrix.tolist(),
            'metadata': instance.metadata
        }


def validate_vrptw_file(filepath: str) -> Tuple[bool, str]:
    """
    Valida un archivo VRPTW CSV.
    
    Args:
        filepath: Ruta al archivo
        
    Returns:
        (is_valid: bool, message: str)
    """
    try:
        instance = SolomonParser.parse(filepath)
        
        # Validaciones básicas
        if instance.n_customers <= 0:
            return False, "No hay clientes válidos"
        
        if instance.metadata['total_demand'] <= 0:
            return False, "Demanda total debe ser positiva"
        
        return True, f"Válido: {instance.n_customers} clientes"
        
    except FileNotFoundError as e:
        return False, f"Archivo no encontrado: {e}"
    except ValueError as e:
        return False, f"Error de formato: {e}"
    except Exception as e:
        return False, f"Error: {e}"
