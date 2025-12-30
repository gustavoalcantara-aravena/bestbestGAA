"""
VRPTW Problem - Definición de la instancia del problema

Representa una instancia VRPTW con operaciones de cálculo de costos,
validación de restricciones y utilidades.
"""

from typing import List, Dict, Optional, Set
import numpy as np
from data.parser import SolomonParser, Client, VRPTWInstance


class VRPTWProblem:
    """
    Problema de ruteo de vehículos con ventanas de tiempo.
    
    Attributes:
        name: Nombre de la instancia
        n_customers: Número de clientes
        n_nodes: Número total de nodos (depósito + clientes)
        clients: Lista de clientes
        depot: Nodo depósito
        distance_matrix: Matriz de distancias
        vehicle_capacity: Capacidad de cada vehículo
        time_horizon: Horizonte de tiempo
    """
    
    def __init__(self,
                 instance: VRPTWInstance,
                 vehicle_capacity: int = 200):
        """
        Inicializa problema VRPTW.
        
        Args:
            instance: VRPTWInstance cargada
            vehicle_capacity: Capacidad de cada vehículo
        """
        self.name = instance.name
        self.n_customers = instance.n_customers
        self.n_nodes = len(instance.clients)
        self.clients = instance.clients
        self.depot = instance.clients[0]
        self.distance_matrix = instance.distance_matrix
        self.vehicle_capacity = vehicle_capacity
        self.time_horizon = instance.metadata['time_horizon']
        
        # Precalcular demandas
        self.total_demand = sum(c.demand for c in self.clients[1:])
        self.customer_demands = {c.id: c.demand for c in self.clients}
    
    @classmethod
    def from_file(cls, filepath: str, vehicle_capacity: int = 200) -> 'VRPTWProblem':
        """
        Carga problema desde archivo CSV Solomon.
        
        Args:
            filepath: Ruta al archivo
            vehicle_capacity: Capacidad de vehículos
            
        Returns:
            VRPTWProblem instance
        """
        instance = SolomonParser.parse(filepath)
        return cls(instance, vehicle_capacity)
    
    def distance(self, i: int, j: int) -> float:
        """
        Obtiene distancia entre nodos i y j.
        
        Args:
            i, j: IDs de nodos
            
        Returns:
            Distancia euclidiana
        """
        return self.distance_matrix[i][j]
    
    def travel_time(self, i: int, j: int) -> float:
        """
        Tiempo de viaje entre nodos (asume velocidad unitaria).
        
        Args:
            i, j: IDs de nodos
            
        Returns:
            Tiempo de viaje
        """
        return self.distance(i, j)
    
    def service_time(self, customer_id: int) -> int:
        """Obtiene tiempo de servicio para un cliente"""
        client = next((c for c in self.clients if c.id == customer_id), None)
        return client.service_time if client else 0
    
    def demand(self, customer_id: int) -> int:
        """Obtiene demanda de un cliente"""
        return self.customer_demands.get(customer_id, 0)
    
    def time_window(self, customer_id: int) -> tuple:
        """
        Obtiene ventana de tiempo para un cliente.
        
        Returns:
            (ready_time, due_date)
        """
        client = next((c for c in self.clients if c.id == customer_id), None)
        if client:
            return (client.ready_time, client.due_date)
        return (0, self.time_horizon)
    
    def min_vehicles_needed(self) -> int:
        """
        Calcula límite inferior de vehículos necesarios.
        
        Returns:
            Mínimo vehículos por capacidad
        """
        if self.vehicle_capacity == 0:
            return 1
        return max(1, (self.total_demand + self.vehicle_capacity - 1) // self.vehicle_capacity)
    
    def route_distance(self, route: List[int]) -> float:
        """
        Calcula distancia total de una ruta.
        
        Args:
            route: Secuencia de nodos [0, c1, c2, ..., 0]
            
        Returns:
            Distancia total
        """
        if len(route) < 2:
            return 0.0
        
        total = 0.0
        for i in range(len(route) - 1):
            total += self.distance(route[i], route[i+1])
        
        return total
    
    def route_load(self, route: List[int]) -> int:
        """
        Calcula carga total de una ruta.
        
        Args:
            route: Secuencia de nodos
            
        Returns:
            Demanda acumulada
        """
        total_load = 0
        for node_id in route[1:-1]:  # Excluir depósito inicial y final
            total_load += self.demand(node_id)
        return total_load
    
    def route_time(self, route: List[int]) -> float:
        """
        Calcula tiempo total de una ruta incluyendo servicios.
        
        Args:
            route: Secuencia de nodos
            
        Returns:
            Tiempo total
        """
        if len(route) < 2:
            return 0.0
        
        time = 0.0
        
        for i in range(len(route) - 1):
            curr = route[i]
            next_node = route[i + 1]
            
            # Tiempo de viaje
            time += self.travel_time(curr, next_node)
            
            # Tiempo de servicio (excepto en el depósito final)
            if next_node != 0:
                time += self.service_time(next_node)
        
        return time
    
    def is_capacity_feasible(self, route: List[int]) -> bool:
        """Verifica si la ruta respeta capacidad"""
        return self.route_load(route) <= self.vehicle_capacity
    
    def is_time_feasible(self, route: List[int]) -> bool:
        """
        Verifica si la ruta respeta ventanas de tiempo.
        
        Args:
            route: Secuencia de nodos
            
        Returns:
            True si factible
        """
        current_time = 0
        
        for i, node_id in enumerate(route):
            if i > 0:
                # Tiempo de viaje desde nodo anterior
                prev = route[i-1]
                current_time += self.travel_time(prev, node_id)
            
            # Verificar ventana de tiempo
            ready_time, due_date = self.time_window(node_id)
            
            # Esperar si es necesario
            current_time = max(current_time, ready_time)
            
            # Verificar si se excede due_date
            if current_time > due_date:
                return False
            
            # Agregar tiempo de servicio
            if node_id != 0:  # No hay servicio en depósito
                current_time += self.service_time(node_id)
        
        return True
    
    def is_route_feasible(self, route: List[int]) -> bool:
        """Verifica si una ruta es factible (capacidad + tiempo)"""
        return (self.is_capacity_feasible(route) and 
                self.is_time_feasible(route))
    
    def verify_solution(self, routes: List[List[int]]) -> Dict:
        """
        Verifica una solución completa.
        
        Args:
            routes: Lista de rutas
            
        Returns:
            Dict con información de viabilidad
        """
        visited = set()
        
        for route in routes:
            # Validar estructura
            if route[0] != 0 or route[-1] != 0:
                return {'feasible': False, 'error': 'Rutas deben comenzar y terminar en depósito'}
            
            # Validar restricciones
            if not self.is_route_feasible(route):
                return {'feasible': False, 'error': f'Ruta {route} infactible'}
            
            # Rastrear clientes visitados
            for node in route[1:-1]:
                if node in visited:
                    return {'feasible': False, 'error': f'Cliente {node} visitado múltiples veces'}
                visited.add(node)
        
        # Verificar cobertura
        expected_customers = set(range(1, self.n_nodes))
        if visited != expected_customers:
            missing = expected_customers - visited
            return {'feasible': False, 'error': f'Clientes no visitados: {missing}'}
        
        return {'feasible': True, 'error': None}
    
    def summary(self) -> str:
        """Retorna resumen del problema"""
        return f"""
VRPTW Problem Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:                 {self.name}
Customers:            {self.n_customers}
Total Nodes:          {self.n_nodes}
Total Demand:         {self.total_demand} units
Vehicle Capacity:     {self.vehicle_capacity} units
Min Vehicles (LB):    {self.min_vehicles_needed()}
Time Horizon:         {self.time_horizon}
        """
