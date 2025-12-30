"""
Constructive Operators - Heurísticas de construcción de soluciones

Implementa 6 heurísticas constructivas para inicializar soluciones VRPTW.
"""

from typing import List, Set, Tuple, Optional
import random
import math
from core.problem import VRPTWProblem
from core.solution import VRPTWSolution


class ConstructiveOperator:
    """Clase base para operadores constructivos"""
    
    def __init__(self, problem: VRPTWProblem):
        self.problem = problem
    
    def build(self, **kwargs) -> VRPTWSolution:
        """Construye solución. Debe ser implementado por subclases"""
        raise NotImplementedError


class NearestNeighbor(ConstructiveOperator):
    """
    Heurística de Nearest Neighbor.
    
    Construcción greedy: comenzar desde depósito, ir al cliente más cercano
    no visitado, repetir hasta que todos estén visitados o capacidad excedida.
    """
    
    def build(self, start_depot: bool = True, **kwargs) -> VRPTWSolution:
        """
        Construye solución con NN.
        
        Args:
            start_depot: Si True, siempre inicia en depósito
            
        Returns:
            VRPTWSolution
        """
        routes = []
        unvisited = set(range(1, self.problem.n_nodes))
        
        while unvisited:
            route = [0]  # Comienza en depósito
            current = 0
            route_load = 0
            
            # Agregar clientes a la ruta actual
            while unvisited:
                # Encontrar cliente más cercano factible
                best_customer = None
                best_distance = float('inf')
                
                for customer in unvisited:
                    distance = self.problem.distance(current, customer)
                    
                    # Verificar factibilidad
                    load = route_load + self.problem.demand(customer)
                    if load > self.problem.vehicle_capacity:
                        continue
                    
                    # Verificar ventana de tiempo
                    test_route = route + [customer, 0]
                    if not self.problem.is_time_feasible(test_route):
                        continue
                    
                    # Seleccionar el más cercano
                    if distance < best_distance:
                        best_distance = distance
                        best_customer = customer
                
                # Si no hay cliente factible, cerrar ruta
                if best_customer is None:
                    break
                
                # Agregar cliente a ruta
                route.append(best_customer)
                route_load += self.problem.demand(best_customer)
                unvisited.remove(best_customer)
                current = best_customer
            
            # Cerrar ruta
            route.append(0)
            
            # Agregar si visitó clientes
            if len(route) > 2:
                routes.append(route)
        
        return VRPTWSolution(routes, self.problem)


class SavingsHeuristic(ConstructiveOperator):
    """
    Heurística de Ahorros (Savings) de Clarke-Wright.
    
    Calcula ahorros de combinar rutas individuales.
    """
    
    def build(self, **kwargs) -> VRPTWSolution:
        """Construye solución con ahorros"""
        
        # Fase 1: crear rutas individuales
        routes = []
        for customer in range(1, self.problem.n_nodes):
            route = [0, customer, 0]
            if self.problem.is_route_feasible(route):
                routes.append(route)
        
        # Fase 2: calcular matriz de ahorros
        savings = {}
        for i in range(1, self.problem.n_nodes):
            for j in range(i+1, self.problem.n_nodes):
                # s(i,j) = d(0,i) + d(0,j) - d(i,j)
                save = (self.problem.distance(0, i) + 
                       self.problem.distance(0, j) - 
                       self.problem.distance(i, j))
                savings[(i, j)] = save
        
        # Fase 3: combinar rutas por ahorros
        sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)
        
        for (i, j), save_value in sorted_savings:
            # Encontrar rutas que contienen i y j
            route_i = None
            route_j = None
            pos_i = -1
            pos_j = -1
            
            for r_idx, route in enumerate(routes):
                if i in route:
                    route_i = r_idx
                    pos_i = route.index(i)
                if j in route:
                    route_j = r_idx
                    pos_j = route.index(j)
            
            # Si están en rutas diferentes, intentar combinarlas
            if route_i is not None and route_j is not None and route_i != route_j:
                # Verificar si son clientes finales en su ruta
                r1 = routes[route_i]
                r2 = routes[route_j]
                
                if (pos_i == len(r1) - 2 and pos_j == 1) or \
                   (pos_j == len(r2) - 2 and pos_i == 1):
                    
                    # Intentar combinar
                    if pos_i == len(r1) - 2 and pos_j == 1:
                        new_route = r1[:-1] + r2[1:]
                    else:
                        new_route = r2[:-1] + r1[1:]
                    
                    # Verificar factibilidad
                    if self.problem.is_route_feasible(new_route):
                        routes[route_i] = new_route
                        routes.pop(route_j)
        
        return VRPTWSolution(routes, self.problem)


class NearestInsertion(ConstructiveOperator):
    """
    Heurística de Nearest Insertion.
    
    Comenzar con ruta parcial y insertar cliente más cercano a la ruta.
    """
    
    def build(self, **kwargs) -> VRPTWSolution:
        """Construye solución con nearest insertion"""
        
        routes = []
        unvisited = set(range(1, self.problem.n_nodes))
        
        while unvisited:
            # Iniciar ruta con cliente más lejano del depósito
            start_customer = max(unvisited, 
                               key=lambda c: self.problem.distance(0, c))
            
            route = [0, start_customer, 0]
            unvisited.remove(start_customer)
            
            # Insertar clientes mientras haya espacio
            while unvisited:
                # Encontrar cliente más cercano a cualquier nodo de la ruta
                best_customer = None
                best_increase = float('inf')
                best_position = -1
                
                for customer in unvisited:
                    # Probar inserción en cada posición
                    for pos in range(1, len(route)):
                        # Costo de inserción
                        prev_node = route[pos-1]
                        next_node = route[pos]
                        
                        increase = (self.problem.distance(prev_node, customer) +
                                  self.problem.distance(customer, next_node) -
                                  self.problem.distance(prev_node, next_node))
                        
                        # Verificar factibilidad
                        test_route = route[:pos] + [customer] + route[pos:]
                        if not self.problem.is_route_feasible(test_route):
                            continue
                        
                        # Seleccionar mejor aumento
                        if increase < best_increase:
                            best_increase = increase
                            best_customer = customer
                            best_position = pos
                
                # Si no hay inserción posible, cerrar ruta
                if best_customer is None:
                    break
                
                # Insertar cliente
                route.insert(best_position, best_customer)
                unvisited.remove(best_customer)
            
            # Agregar ruta si visitó clientes
            if len(route) > 2:
                routes.append(route)
        
        return VRPTWSolution(routes, self.problem)


class RandomizedInsertion(ConstructiveOperator):
    """
    Heurística de Inserción Randomizada.
    
    Similar a NearestInsertion pero con probabilidad de seleccionar
    clientes sub-óptimos (para diversidad).
    """
    
    def build(self, alpha: float = 0.15, seed: Optional[int] = None, 
              **kwargs) -> VRPTWSolution:
        """
        Construye solución con inserción randomizada.
        
        Args:
            alpha: Parámetro RCL (0=greedy, 1=random)
            seed: Seed para aleatoriedad
        """
        if seed is not None:
            random.seed(seed)
        
        routes = []
        unvisited = set(range(1, self.problem.n_nodes))
        
        while unvisited:
            # Iniciar con cliente aleatorio
            start_customer = random.choice(list(unvisited))
            route = [0, start_customer, 0]
            unvisited.remove(start_customer)
            
            # Insertar con RCL
            while unvisited:
                candidates = []
                
                for customer in unvisited:
                    for pos in range(1, len(route)):
                        prev_node = route[pos-1]
                        next_node = route[pos]
                        
                        increase = (self.problem.distance(prev_node, customer) +
                                  self.problem.distance(customer, next_node) -
                                  self.problem.distance(prev_node, next_node))
                        
                        test_route = route[:pos] + [customer] + route[pos:]
                        if self.problem.is_route_feasible(test_route):
                            candidates.append((increase, customer, pos))
                
                if not candidates:
                    break
                
                # Construir RCL basada en alpha
                candidates.sort(key=lambda x: x[0])
                rcl_size = max(1, int(len(candidates) * alpha))
                rcl = candidates[:rcl_size]
                
                # Seleccionar aleatorio de RCL
                increase, customer, pos = random.choice(rcl)
                route.insert(pos, customer)
                unvisited.remove(customer)
            
            if len(route) > 2:
                routes.append(route)
        
        return VRPTWSolution(routes, self.problem)


class TimeOrientedNN(ConstructiveOperator):
    """
    Nearest Neighbor orientado por ventanas de tiempo.
    
    Considera restricciones de tiempo al seleccionar clientes.
    """
    
    def build(self, **kwargs) -> VRPTWSolution:
        """Construye solución con NN orientado por tiempo"""
        
        routes = []
        unvisited = set(range(1, self.problem.n_nodes))
        
        while unvisited:
            route = [0]
            current = 0
            route_load = 0
            current_time = 0
            
            while unvisited:
                best_customer = None
                best_score = -float('inf')
                
                for customer in unvisited:
                    ready_time, due_date = self.problem.time_window(customer)
                    distance = self.problem.distance(current, customer)
                    travel_time = self.problem.travel_time(current, customer)
                    
                    # Tiempo de llegada
                    arrival_time = current_time + travel_time
                    
                    # Verificar capacidad
                    load = route_load + self.problem.demand(customer)
                    if load > self.problem.vehicle_capacity:
                        continue
                    
                    # Verificar ventana de tiempo
                    if arrival_time > due_date:
                        continue
                    
                    # Verificar ruta completa
                    test_route = route + [customer, 0]
                    if not self.problem.is_time_feasible(test_route):
                        continue
                    
                    # Calcular score (distancia - urgencia)
                    slack = due_date - max(arrival_time, ready_time)
                    score = -distance + slack * 0.1  # Preferir cercanos y urgentes
                    
                    if score > best_score:
                        best_score = score
                        best_customer = customer
                
                if best_customer is None:
                    break
                
                route.append(best_customer)
                route_load += self.problem.demand(best_customer)
                current = best_customer
                ready_time, _ = self.problem.time_window(best_customer)
                current_time = max(current_time + self.problem.travel_time(
                    route[-2], best_customer), ready_time)
                current_time += self.problem.service_time(best_customer)
                
                unvisited.remove(best_customer)
            
            route.append(0)
            if len(route) > 2:
                routes.append(route)
        
        return VRPTWSolution(routes, self.problem)


class RegretInsertion(ConstructiveOperator):
    """
    Heurística de Regret Insertion.
    
    Inserta cliente que tiene mayor "arrepentimiento" si no se inserta ahora.
    """
    
    def build(self, **kwargs) -> VRPTWSolution:
        """Construye solución con regret insertion"""
        
        routes = []
        unvisited = set(range(1, self.problem.n_nodes))
        
        # Iniciar con ruta vacía
        initial_route = [0, 0]
        routes.append(initial_route)
        
        while unvisited:
            # Calcular regret para cada cliente
            regrets = {}
            
            for customer in unvisited:
                # Encontrar las 2 mejores posiciones de inserción
                best_costs = []
                
                for route in routes:
                    for pos in range(1, len(route)):
                        prev = route[pos-1]
                        next_node = route[pos]
                        
                        increase = (self.problem.distance(prev, customer) +
                                  self.problem.distance(customer, next_node) -
                                  self.problem.distance(prev, next_node))
                        
                        test_route = route[:pos] + [customer] + route[pos:]
                        if self.problem.is_route_feasible(test_route):
                            best_costs.append(increase)
                
                # Calcular regret
                if len(best_costs) >= 2:
                    best_costs.sort()
                    regret = best_costs[1] - best_costs[0]  # Diferencia entre 2 mejores
                else:
                    regret = 0
                
                regrets[customer] = regret
            
            if not regrets:
                break
            
            # Seleccionar cliente con mayor regret
            customer = max(regrets, key=regrets.get)
            
            # Encontrar mejor posición global
            best_cost = float('inf')
            best_route_idx = -1
            best_pos = -1
            
            for r_idx, route in enumerate(routes):
                for pos in range(1, len(route)):
                    prev = route[pos-1]
                    next_node = route[pos]
                    
                    increase = (self.problem.distance(prev, customer) +
                              self.problem.distance(customer, next_node) -
                              self.problem.distance(prev, next_node))
                    
                    test_route = route[:pos] + [customer] + route[pos:]
                    if self.problem.is_route_feasible(test_route) and increase < best_cost:
                        best_cost = increase
                        best_route_idx = r_idx
                        best_pos = pos
            
            # Insertar cliente
            if best_route_idx >= 0:
                routes[best_route_idx].insert(best_pos, customer)
                unvisited.remove(customer)
            else:
                # Si no puede insertar, crear nueva ruta
                routes.append([0, customer, 0])
                unvisited.remove(customer)
        
        # Limpiar rutas vacías
        routes = [r for r in routes if len(r) > 2]
        
        return VRPTWSolution(routes, self.problem)


# Factory para crear operadores constructivos
CONSTRUCTIVE_OPERATORS = {
    'nearest_neighbor': NearestNeighbor,
    'savings': SavingsHeuristic,
    'insertion': NearestInsertion,
    'randomized': RandomizedInsertion,
    'time_oriented': TimeOrientedNN,
    'regret': RegretInsertion,
}


def get_constructive_operator(name: str, problem: VRPTWProblem) -> Optional[ConstructiveOperator]:
    """Obtiene operador constructivo por nombre"""
    operator_class = CONSTRUCTIVE_OPERATORS.get(name.lower())
    if operator_class:
        return operator_class(problem)
    return None
