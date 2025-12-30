"""
Repair Operators - Corrección de soluciones infactibles

Implementa 2 operadores para reparar violaciones de restricciones.
"""

from typing import List, Optional
from core.problem import VRPTWProblem
from core.solution import VRPTWSolution


class RepairOperator:
    """Clase base para operadores de reparación"""
    
    def __init__(self, problem: VRPTWProblem):
        self.problem = problem
    
    def repair(self, solution: VRPTWSolution) -> VRPTWSolution:
        """Repara solución infactible"""
        raise NotImplementedError


class CapacityRepair(RepairOperator):
    """
    Reparador de capacidad: remueve clientes de rutas sobrecargadas.
    
    Si una ruta excede capacidad, remueve clientes de menor demanda.
    """
    
    def repair(self, solution: VRPTWSolution) -> VRPTWSolution:
        """
        Repara violaciones de capacidad.
        
        Estrategia: remover clientes de menor demanda hasta factible.
        """
        result = solution.copy()
        
        modified = True
        while modified:
            modified = False
            
            for r_idx, route in enumerate(result.routes):
                if not self.problem.is_capacity_feasible(route):
                    # Ruta sobrecargada - remover cliente
                    load = self.problem.route_load(route)
                    excess = load - self.problem.vehicle_capacity
                    
                    # Encontrar cliente de menor demanda
                    best_customer = None
                    best_demand = float('inf')
                    best_pos = -1
                    
                    for pos, customer in enumerate(route[1:-1], 1):
                        demand = self.problem.demand(customer)
                        if demand < best_demand:
                            best_demand = demand
                            best_customer = customer
                            best_pos = pos
                    
                    # Remover cliente
                    if best_customer is not None:
                        result.remove_customer(best_customer)
                        modified = True
                        break  # Reiniciar búsqueda
        
        # Reinsertar clientes removidos greedy
        visited = set()
        for route in result.routes:
            visited.update(route[1:-1])
        
        all_customers = set(range(1, self.problem.n_nodes))
        unvisited = all_customers - visited
        
        for customer in unvisited:
            inserted = False
            
            # Intentar inserción en cada ruta
            for r_idx, route in enumerate(result.routes):
                for pos in range(1, len(route)):
                    new_route = route[:pos] + [customer] + route[pos:]
                    
                    if self.problem.is_route_feasible(new_route):
                        result.insert_customer(customer, r_idx, pos - 1)
                        inserted = True
                        break
                
                if inserted:
                    break
            
            # Si no se insertó, crear nueva ruta
            if not inserted:
                new_route = [0, customer, 0]
                if self.problem.is_route_feasible(new_route):
                    result.add_route(new_route)
        
        result._invalidate_cache()
        return result


class TimeWindowRepair(RepairOperator):
    """
    Reparador de ventana de tiempo: remueve clientes que violan TW.
    
    Si una ruta viola ventanas de tiempo, remueve el cliente más problemático.
    """
    
    def repair(self, solution: VRPTWSolution) -> VRPTWSolution:
        """
        Repara violaciones de ventana de tiempo.
        
        Estrategia: remover cliente que causa mayor violación.
        """
        result = solution.copy()
        
        modified = True
        while modified:
            modified = False
            
            for r_idx, route in enumerate(result.routes):
                if not self.problem.is_time_feasible(route):
                    # Encontrar cliente que causa violación
                    current_time = 0
                    worst_customer = None
                    worst_violation = 0
                    worst_pos = -1
                    
                    for pos, node_id in enumerate(route):
                        if pos > 0:
                            current_time += self.problem.travel_time(route[pos-1], node_id)
                        
                        ready_time, due_date = self.problem.time_window(node_id)
                        
                        # Esperar si es necesario
                        current_time = max(current_time, ready_time)
                        
                        # Calcular violación
                        if current_time > due_date and node_id != 0:
                            violation = current_time - due_date
                            if violation > worst_violation:
                                worst_violation = violation
                                worst_customer = node_id
                                worst_pos = pos
                        
                        if node_id != 0:
                            current_time += self.problem.service_time(node_id)
                    
                    # Remover cliente problemático
                    if worst_customer is not None:
                        result.remove_customer(worst_customer)
                        modified = True
                        break  # Reiniciar búsqueda
        
        # Reinsertar clientes removidos (similar a CapacityRepair)
        visited = set()
        for route in result.routes:
            visited.update(route[1:-1])
        
        all_customers = set(range(1, self.problem.n_nodes))
        unvisited = all_customers - visited
        
        for customer in unvisited:
            inserted = False
            
            # Intentar inserción primero por restricción de tiempo
            best_cost = float('inf')
            best_route = -1
            best_pos = -1
            
            for r_idx, route in enumerate(result.routes):
                for pos in range(1, len(route)):
                    new_route = route[:pos] + [customer] + route[pos:]
                    
                    if self.problem.is_route_feasible(new_route):
                        # Preferir inserciones que respeten tiempo
                        cost = self.problem.distance(route[pos-1], customer) + \
                               self.problem.distance(customer, route[pos]) - \
                               self.problem.distance(route[pos-1], route[pos])
                        
                        if cost < best_cost:
                            best_cost = cost
                            best_route = r_idx
                            best_pos = pos
            
            if best_route >= 0:
                result.insert_customer(customer, best_route, best_pos - 1)
            else:
                # Crear nueva ruta
                new_route = [0, customer, 0]
                if self.problem.is_route_feasible(new_route):
                    result.add_route(new_route)
        
        result._invalidate_cache()
        return result


class HybridRepair(RepairOperator):
    """
    Reparador híbrido: combina capacidad y ventana de tiempo.
    """
    
    def repair(self, solution: VRPTWSolution) -> VRPTWSolution:
        """Repara ambas violaciones simultáneamente"""
        
        # Aplicar reparadores en secuencia
        capacity_repair = CapacityRepair(self.problem)
        time_repair = TimeWindowRepair(self.problem)
        
        result = capacity_repair.repair(solution)
        result = time_repair.repair(result)
        
        return result


# Factory
REPAIR_OPERATORS = {
    'capacity': CapacityRepair,
    'time_window': TimeWindowRepair,
    'hybrid': HybridRepair,
}


def get_repair_operator(name: str, problem: VRPTWProblem) -> Optional[RepairOperator]:
    """Obtiene operador de reparación por nombre"""
    operator_class = REPAIR_OPERATORS.get(name.lower())
    if operator_class:
        return operator_class(problem)
    return None
