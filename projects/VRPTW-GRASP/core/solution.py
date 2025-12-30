"""
VRPTW Solution - Representación y operaciones sobre soluciones

Maneja la estructura de solución, evaluación de viabilidad y cálculo de costos.
"""

from typing import List, Dict, Optional, Tuple
from copy import deepcopy
import numpy as np


class VRPTWSolution:
    """
    Representa una solución VRPTW (conjunto de rutas).
    
    Attributes:
        routes: Lista de rutas [route1, route2, ...]
        problem: Instancia del problema VRPTW
        _evaluated: Bandera para evaluación lazy
        _cost: Costo total cacheado
        _distance: Distancia total cacheada
        _time: Tiempo total cacheado
        _feasible: Estado de viabilidad cacheado
    """
    
    def __init__(self, routes: List[List[int]], problem):
        """
        Inicializa solución VRPTW.
        
        Args:
            routes: Lista de rutas (cada ruta es lista de nodos)
            problem: Instancia VRPTWProblem
        """
        self.routes = deepcopy(routes)
        self.problem = problem
        
        # Caché para evaluación lazy
        self._evaluated = False
        self._cost = None
        self._distance = None
        self._time = None
        self._feasible = None
        self._violation_count = None
    
    @classmethod
    def empty(cls, problem) -> 'VRPTWSolution':
        """Crea solución vacía (depósito solo)"""
        return cls([[0, 0]], problem)
    
    def copy(self) -> 'VRPTWSolution':
        """Retorna copia profunda"""
        return VRPTWSolution(self.routes, self.problem)
    
    # =========== Operaciones en Rutas ===========
    
    def num_routes(self) -> int:
        """Número de rutas (vehículos)"""
        return len(self.routes)
    
    def num_customers(self) -> int:
        """Número de clientes visitados"""
        count = 0
        for route in self.routes:
            count += len(route) - 2  # Excluir depósito inicial y final
        return count
    
    def get_route(self, route_idx: int) -> List[int]:
        """Obtiene ruta por índice"""
        if route_idx < len(self.routes):
            return self.routes[route_idx]
        return []
    
    def customers_in_route(self, route_idx: int) -> List[int]:
        """Retorna clientes en una ruta (sin depósito)"""
        route = self.get_route(route_idx)
        return route[1:-1]  # Excluir depósito inicio y fin
    
    def add_route(self, route: List[int]) -> None:
        """Agrega nueva ruta"""
        self.routes.append(deepcopy(route))
        self._invalidate_cache()
    
    def insert_customer(self, customer_id: int, route_idx: int, position: int) -> None:
        """
        Inserta cliente en ruta en posición.
        
        Args:
            customer_id: ID del cliente
            route_idx: Índice de ruta
            position: Posición en la ruta (0=después del depósito)
        """
        if route_idx < len(self.routes):
            route = self.routes[route_idx]
            actual_pos = position + 1  # +1 para saltear depósito inicial
            if 0 <= actual_pos <= len(route) - 1:
                route.insert(actual_pos, customer_id)
                self._invalidate_cache()
    
    def remove_customer(self, customer_id: int) -> Optional[Tuple[int, int]]:
        """
        Elimina cliente de la solución.
        
        Returns:
            (route_idx, position) donde estaba, None si no existe
        """
        for r_idx, route in enumerate(self.routes):
            if customer_id in route:
                pos = route.index(customer_id)
                route.remove(customer_id)
                
                # Eliminar ruta si queda vacía
                if len(route) == 2:  # Solo depósito
                    self.routes.pop(r_idx)
                
                self._invalidate_cache()
                return (r_idx, pos - 1)  # -1 para excluir depósito inicial
        
        return None
    
    def move_customer(self, customer_id: int, 
                      new_route_idx: int, new_position: int) -> bool:
        """Mueve cliente a otra ruta/posición"""
        removal = self.remove_customer(customer_id)
        if removal is None:
            return False
        
        self.insert_customer(customer_id, new_route_idx, new_position)
        self._invalidate_cache()
        return True
    
    # =========== Evaluación ===========
    
    def _invalidate_cache(self) -> None:
        """Invalida caché de evaluación"""
        self._evaluated = False
        self._cost = None
        self._distance = None
        self._time = None
        self._feasible = None
        self._violation_count = None
    
    def evaluate(self, force: bool = False) -> None:
        """
        Evalúa solución completamente (lazy evaluation).
        
        Args:
            force: Si True, recalcula incluso si está cacheado
        """
        if self._evaluated and not force:
            return
        
        # Calcular métricas por ruta
        total_distance = 0.0
        total_time = 0.0
        all_feasible = True
        
        for route in self.routes:
            total_distance += self.problem.route_distance(route)
            total_time += self.problem.route_time(route)
            
            if not self.problem.is_route_feasible(route):
                all_feasible = False
        
        self._distance = total_distance
        self._time = total_time
        self._feasible = all_feasible
        
        # Costo jerárquico: viabilidad → vehículos → distancia
        self._cost = self._compute_cost()
        self._violation_count = self._count_violations() if not all_feasible else 0
        
        self._evaluated = True
    
    def _compute_cost(self) -> float:
        """Calcula costo jerárquico"""
        # Penalización de infactibilidad es muy grande
        penalty = self._count_violations()
        if penalty > 0:
            # Penalización: 10000 por violación + distancia
            return 10000 * penalty + self._distance
        
        # Factible: penalizar por exceso de vehículos
        min_vehicles = self.problem.min_vehicles_needed()
        excess_vehicles = max(0, self.num_routes() - min_vehicles) * 1000
        
        return excess_vehicles + self._distance
    
    def _count_violations(self) -> int:
        """Cuenta total de violaciones de restricciones"""
        violations = 0
        
        for route in self.routes:
            # Violación de capacidad
            if not self.problem.is_capacity_feasible(route):
                violations += 1
            
            # Violación de tiempo
            if not self.problem.is_time_feasible(route):
                violations += 1
        
        return violations
    
    # =========== Propiedades ===========
    
    @property
    def cost(self) -> float:
        """Costo total (jerárquico)"""
        if not self._evaluated:
            self.evaluate()
        return self._cost
    
    @property
    def distance(self) -> float:
        """Distancia total"""
        if not self._evaluated:
            self.evaluate()
        return self._distance
    
    @property
    def is_feasible(self) -> bool:
        """Si la solución es factible"""
        if not self._evaluated:
            self.evaluate()
        return self._feasible
    
    @property
    def violation_count(self) -> int:
        """Número de restricciones violadas"""
        if not self._evaluated:
            self.evaluate()
        return self._violation_count
    
    def total_demand_served(self) -> int:
        """Demanda total servida"""
        total = 0
        for route in self.routes:
            for node_id in route[1:-1]:
                total += self.problem.demand(node_id)
        return total
    
    def gap_to_lower_bound(self) -> float:
        """Brecha respecto al límite inferior (min vehículos)"""
        if not self.is_feasible:
            return float('inf')
        
        min_vehicles = self.problem.min_vehicles_needed()
        excess = max(0, self.num_routes() - min_vehicles)
        
        return excess * 1000 + self.distance
    
    # =========== Comparación ===========
    
    def is_better_than(self, other: 'VRPTWSolution') -> bool:
        """Compara costos (jerarquía: viabilidad → vehículos → distancia)"""
        return self.cost < other.cost
    
    def is_feasible_and_better(self, other: 'VRPTWSolution') -> bool:
        """Es factible y mejor que otro"""
        return self.is_feasible and (not other.is_feasible or self.is_better_than(other))
    
    # =========== Búsqueda ===========
    
    def find_customer(self, customer_id: int) -> Optional[Tuple[int, int]]:
        """
        Encuentra ubicación de un cliente.
        
        Returns:
            (route_idx, position_in_route) o None
        """
        for r_idx, route in enumerate(self.routes):
            if customer_id in route:
                pos = route.index(customer_id)
                return (r_idx, pos - 1)  # -1 para excluir depósito inicial
        return None
    
    def all_customers(self) -> List[int]:
        """Retorna lista de todos los clientes"""
        customers = []
        for route in self.routes:
            customers.extend(route[1:-1])
        return customers
    
    def get_customers_by_route(self) -> Dict[int, List[int]]:
        """Retorna dict {route_idx: [customers]}"""
        result = {}
        for r_idx, route in enumerate(self.routes):
            result[r_idx] = route[1:-1]
        return result
    
    # =========== Información y Debugging ===========
    
    def info(self) -> str:
        """Retorna información detallada de la solución"""
        self.evaluate()
        
        info = f"""
Solution Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vehicles:             {self.num_routes()}
Customers:            {self.num_customers()}
Feasible:             {'Yes' if self.is_feasible else 'No'}
Cost:                 {self.cost:,.2f}
Distance:             {self.distance:,.2f}
Violations:           {self.violation_count}
Total Demand Served:  {self.total_demand_served()} / {self.problem.total_demand}
        """
        
        info += "\nRoutes:\n"
        for i, route in enumerate(self.routes):
            load = self.problem.route_load(route)
            dist = self.problem.route_distance(route)
            feas = "✓" if self.problem.is_route_feasible(route) else "✗"
            info += f"  Route {i:2d}: {route} | Load: {load}/{self.problem.vehicle_capacity} | Dist: {dist:,.2f} {feas}\n"
        
        return info
    
    def __repr__(self) -> str:
        return f"VRPTWSolution({self.num_routes()} routes, {self.num_customers()} customers, cost={self.cost:.2f})"
