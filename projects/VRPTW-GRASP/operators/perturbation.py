"""
Perturbation Operators - Modificaciones grandes para escapar de óptimos locales

Implementa 4 operadores de perturbación para salir de mínimos locales.
"""

from typing import List, Optional, Set
import random
from copy import deepcopy
from core.problem import VRPTWProblem
from core.solution import VRPTWSolution


class PerturbationOperator:
    """Clase base para operadores de perturbación"""
    
    def __init__(self, problem: VRPTWProblem):
        self.problem = problem
    
    def apply(self, solution: VRPTWSolution, **kwargs) -> VRPTWSolution:
        """Aplica perturbación y retorna nueva solución"""
        raise NotImplementedError


class EjectionChain(PerturbationOperator):
    """
    Operador Ejection Chain: causa 'expulsión' en cadena.
    
    Remueve un cliente de su ruta, causando cascade de inserciones.
    """
    
    def apply(self, solution: VRPTWSolution, chain_length: int = 3, 
              seed: Optional[int] = None) -> VRPTWSolution:
        """
        Aplica ejection chain.
        
        Args:
            solution: Solución actual
            chain_length: Longitud de la cadena de expulsión
            seed: Seed para aleatoriedad
        """
        if seed is not None:
            random.seed(seed)
        
        result = solution.copy()
        customers = result.all_customers()
        
        if not customers:
            return result
        
        # Seleccionar clientes aleatorios para encadenar
        num_ejections = min(chain_length, len(customers))
        ejected = []
        
        for _ in range(num_ejections):
            # Seleccionar cliente aleatorio
            customer = random.choice(customers)
            
            # Remover cliente
            removal = result.remove_customer(customer)
            if removal:
                ejected.append(customer)
                customers.remove(customer)
        
        # Reinsertar en mejores posiciones
        for customer in ejected:
            best_cost = float('inf')
            best_route = -1
            best_pos = -1
            
            # Encontrar mejor posición
            for r_idx, route in enumerate(result.routes):
                for pos in range(1, len(route)):
                    new_route = route[:pos] + [customer] + route[pos:]
                    
                    if not self.problem.is_route_feasible(new_route):
                        continue
                    
                    cost_increase = (self.problem.distance(route[pos-1], customer) +
                                   self.problem.distance(customer, route[pos]) -
                                   self.problem.distance(route[pos-1], route[pos]))
                    
                    if cost_increase < best_cost:
                        best_cost = cost_increase
                        best_route = r_idx
                        best_pos = pos
            
            # Si no hay posición, crear nueva ruta
            if best_route < 0:
                result.add_route([0, customer, 0])
            else:
                result.insert_customer(customer, best_route, best_pos - 1)
        
        result._invalidate_cache()
        return result


class RuinRecreate(PerturbationOperator):
    """
    Operador Ruin & Recreate: destruye parte y reconstruye.
    
    Remueve múltiples clientes y los reinserta greedy.
    """
    
    def apply(self, solution: VRPTWSolution, ruin_percentage: float = 0.2,
              seed: Optional[int] = None) -> VRPTWSolution:
        """
        Aplica ruin & recreate.
        
        Args:
            solution: Solución actual
            ruin_percentage: Porcentaje de clientes a remover
            seed: Seed para aleatoriedad
        """
        if seed is not None:
            random.seed(seed)
        
        result = solution.copy()
        customers = result.all_customers()
        
        # Determinar cuántos remover
        num_to_remove = max(1, int(len(customers) * ruin_percentage))
        
        # RUIN: Remover clientes
        removed = random.sample(customers, num_to_remove)
        
        for customer in removed:
            result.remove_customer(customer)
        
        # RECREATE: Reinsertar greedy
        for customer in removed:
            # Nearest insertion
            best_cost = float('inf')
            best_route = -1
            best_pos = -1
            
            if not result.routes:
                result.add_route([0, customer, 0])
                continue
            
            for r_idx, route in enumerate(result.routes):
                for pos in range(1, len(route)):
                    new_route = route[:pos] + [customer] + route[pos:]
                    
                    if not self.problem.is_route_feasible(new_route):
                        continue
                    
                    cost_increase = (self.problem.distance(route[pos-1], customer) +
                                   self.problem.distance(customer, route[pos]) -
                                   self.problem.distance(route[pos-1], route[pos]))
                    
                    if cost_increase < best_cost:
                        best_cost = cost_increase
                        best_route = r_idx
                        best_pos = pos
            
            if best_route < 0:
                result.add_route([0, customer, 0])
            else:
                result.insert_customer(customer, best_route, best_pos - 1)
        
        result._invalidate_cache()
        return result


class RandomRemoval(PerturbationOperator):
    """
    Operador Random Removal: remueve clientes aleatorios.
    
    Similar a Ruin pero sin reinserción estructurada.
    """
    
    def apply(self, solution: VRPTWSolution, removal_rate: float = 0.1,
              seed: Optional[int] = None) -> VRPTWSolution:
        """
        Aplica remoción aleatoria.
        
        Args:
            solution: Solución actual
            removal_rate: Porcentaje de clientes a remover
            seed: Seed para aleatoriedad
        """
        if seed is not None:
            random.seed(seed)
        
        result = solution.copy()
        customers = result.all_customers()
        
        # Determinar cuántos remover
        num_to_remove = max(1, int(len(customers) * removal_rate))
        
        # Remover aleatorios
        to_remove = random.sample(customers, num_to_remove)
        
        for customer in to_remove:
            result.remove_customer(customer)
        
        # Limpiar rutas vacías
        result.routes = [r for r in result.routes if len(r) > 2]
        
        result._invalidate_cache()
        return result


class RouteElimination(PerturbationOperator):
    """
    Operador Route Elimination: elimina una ruta completa.
    
    Remueve una ruta y redistribuye sus clientes.
    """
    
    def apply(self, solution: VRPTWSolution, seed: Optional[int] = None) -> VRPTWSolution:
        """
        Aplica eliminación de ruta.
        
        Args:
            solution: Solución actual
            seed: Seed para aleatoriedad
        """
        if seed is not None:
            random.seed(seed)
        
        result = solution.copy()
        
        if len(result.routes) <= 1:
            return result
        
        # Seleccionar ruta a eliminar
        route_to_eliminate = random.randint(0, len(result.routes) - 1)
        eliminated_route = result.routes[route_to_eliminate]
        
        # Extraer clientes de la ruta
        removed_customers = eliminated_route[1:-1]
        
        # Remover ruta
        result.routes.pop(route_to_eliminate)
        
        # Reinsertar clientes en otras rutas
        for customer in removed_customers:
            best_cost = float('inf')
            best_route = -1
            best_pos = -1
            
            if not result.routes:
                result.add_route([0, customer, 0])
                continue
            
            for r_idx, route in enumerate(result.routes):
                for pos in range(1, len(route)):
                    new_route = route[:pos] + [customer] + route[pos:]
                    
                    if not self.problem.is_route_feasible(new_route):
                        continue
                    
                    cost_increase = (self.problem.distance(route[pos-1], customer) +
                                   self.problem.distance(customer, route[pos]) -
                                   self.problem.distance(route[pos-1], route[pos]))
                    
                    if cost_increase < best_cost:
                        best_cost = cost_increase
                        best_route = r_idx
                        best_pos = pos
            
            if best_route < 0:
                result.add_route([0, customer, 0])
            else:
                result.insert_customer(customer, best_route, best_pos - 1)
        
        result._invalidate_cache()
        return result


# Factory
PERTURBATION_OPERATORS = {
    'ejection_chain': EjectionChain,
    'ruin_recreate': RuinRecreate,
    'random_removal': RandomRemoval,
    'route_elimination': RouteElimination,
}


def get_perturbation_operator(name: str, problem: VRPTWProblem) -> Optional[PerturbationOperator]:
    """Obtiene operador de perturbación por nombre"""
    operator_class = PERTURBATION_OPERATORS.get(name.lower())
    if operator_class:
        return operator_class(problem)
    return None
