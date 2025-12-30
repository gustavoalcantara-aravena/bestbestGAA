"""
Local Search Operators - Mejora de soluciones mediante operadores de entorno local

Implementa 8 operadores de búsqueda local: 4 intra-ruta y 4 inter-ruta.
"""

from typing import List, Optional, Tuple
import random
from copy import deepcopy
from core.problem import VRPTWProblem
from core.solution import VRPTWSolution


class LocalSearchOperator:
    """Clase base para operadores de búsqueda local"""
    
    def __init__(self, problem: VRPTWProblem):
        self.problem = problem
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Aplica operador y retorna solución mejorada o None"""
        raise NotImplementedError


# ========== OPERADORES INTRA-RUTA ==========

class TwoOpt(LocalSearchOperator):
    """
    Operador 2-opt: invierte segmento de ruta.
    
    Elimina dos aristas y reconecta invirtiendo el segmento.
    """
    
    def apply(self, solution: VRPTWSolution, best_improvement: bool = True) -> Optional[VRPTWSolution]:
        """
        Aplica 2-opt.
        
        Args:
            solution: Solución actual
            best_improvement: Si True, busca mejor mejora; si False, retorna primera mejora
        """
        improved = False
        best_delta = 0
        best_swap = None
        
        # Iterar sobre todas las rutas
        for r_idx, route in enumerate(solution.routes):
            if len(route) <= 4:  # Mínimo 2 clientes
                continue
            
            # Probar todos los pares de aristas
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    # Calcular delta
                    curr_dist = (self.problem.distance(route[i], route[i+1]) +
                               self.problem.distance(route[j], route[j+1]))
                    
                    new_dist = (self.problem.distance(route[i], route[j]) +
                              self.problem.distance(route[i+1], route[j+1]))
                    
                    delta = new_dist - curr_dist
                    
                    if delta < best_delta:
                        # Probar factibilidad
                        new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
                        if self.problem.is_route_feasible(new_route):
                            best_delta = delta
                            best_swap = (r_idx, i, j)
                            improved = True
                            
                            if not best_improvement:
                                break
                
                if improved and not best_improvement:
                    break
            
            if improved and not best_improvement:
                break
        
        # Aplicar mejor swap
        if best_swap:
            new_solution = solution.copy()
            r_idx, i, j = best_swap
            route = new_solution.routes[r_idx]
            new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
            new_solution.routes[r_idx] = new_route
            new_solution._invalidate_cache()
            return new_solution
        
        return None


class OrOpt(LocalSearchOperator):
    """
    Operador Or-opt: reubica secuencia de 1-3 clientes.
    
    Elimina secuencia de una ruta e inserta en otra posición.
    """
    
    def apply(self, solution: VRPTWSolution, sequence_size: int = 1) -> Optional[VRPTWSolution]:
        """
        Aplica Or-opt.
        
        Args:
            solution: Solución actual
            sequence_size: Longitud de secuencia a mover (1-3)
        """
        best_delta = 0
        best_move = None
        
        for r_idx, route in enumerate(solution.routes):
            if len(route) <= 2 + sequence_size:
                continue
            
            # Probar cada secuencia de tamaño sequence_size
            for i in range(1, len(route) - sequence_size):
                # Secuencia a mover
                seq = route[i:i+sequence_size]
                
                # Probar inserción en cada posición
                for j in range(1, len(route) - sequence_size + 1):
                    if abs(j - i) <= sequence_size:
                        continue  # Ignorar movimientos triviales
                    
                    # Construir nueva ruta
                    if j < i:
                        new_route = (route[:j] + seq + route[j:i] + 
                                   route[i+sequence_size:])
                    else:
                        new_route = (route[:i] + route[i+sequence_size:j] + 
                                   seq + route[j:])
                    
                    # Calcular delta
                    old_dist = self.problem.route_distance(route)
                    new_dist = self.problem.route_distance(new_route)
                    delta = new_dist - old_dist
                    
                    if delta < best_delta:
                        if self.problem.is_route_feasible(new_route):
                            best_delta = delta
                            best_move = (r_idx, route, new_route)
        
        if best_move:
            new_solution = solution.copy()
            r_idx, _, new_route = best_move
            new_solution.routes[r_idx] = new_route
            new_solution._invalidate_cache()
            return new_solution
        
        return None


class ThreeOpt(LocalSearchOperator):
    """
    Operador 3-opt: reestructura ruta removiendo 3 aristas.
    
    Más complejo que 2-opt pero potencialmente mejor.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Aplica 3-opt (implementación simplificada)"""
        
        for r_idx, route in enumerate(solution.routes):
            if len(route) <= 5:  # Mínimo 3 clientes
                continue
            
            # Probar combinaciones de 3 posiciones
            for i in range(1, len(route) - 4):
                for j in range(i + 1, len(route) - 3):
                    for k in range(j + 1, len(route) - 2):
                        # Intentar recombinaciones
                        candidates = self._get_3opt_candidates(route, i, j, k)
                        
                        for new_route in candidates:
                            if not self.problem.is_route_feasible(new_route):
                                continue
                            
                            old_cost = self.problem.route_distance(route)
                            new_cost = self.problem.route_distance(new_route)
                            
                            if new_cost < old_cost:
                                result = solution.copy()
                                result.routes[r_idx] = new_route
                                result._invalidate_cache()
                                return result
        
        return None
    
    @staticmethod
    def _get_3opt_candidates(route: List[int], i: int, j: int, k: int) -> List[List[int]]:
        """Genera candidatos de 3-opt"""
        candidates = []
        
        # Hay múltiples formas de reconectar, aquí algunas de las más comunes
        candidates.append(route[:i+1] + route[j:i:-1] + route[k:j:-1] + route[k+1:])
        candidates.append(route[:i+1] + route[j:k+1] + route[i+1:j] + route[k+1:])
        
        return candidates


class Relocate(LocalSearchOperator):
    """
    Operador Relocate: mueve un cliente a otra posición en la misma ruta.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Aplica relocate intra-ruta"""
        
        best_delta = 0
        best_move = None
        
        for r_idx, route in enumerate(solution.routes):
            if len(route) <= 3:
                continue
            
            # Para cada cliente en la ruta
            for i in range(1, len(route) - 1):
                customer = route[i]
                
                # Probar insertar en cada otra posición
                for j in range(1, len(route) - 1):
                    if abs(i - j) <= 1:
                        continue
                    
                    # Crear nueva ruta
                    new_route = route[:i] + route[i+1:]
                    if j < i:
                        new_route = (new_route[:j] + [customer] + 
                                   new_route[j:])
                    else:
                        new_route = (new_route[:j-1] + [customer] + 
                                   new_route[j-1:])
                    
                    # Calcular delta
                    old_dist = self.problem.route_distance(route)
                    new_dist = self.problem.route_distance(new_route)
                    delta = new_dist - old_dist
                    
                    if delta < best_delta:
                        if self.problem.is_route_feasible(new_route):
                            best_delta = delta
                            best_move = (r_idx, new_route)
        
        if best_move:
            new_solution = solution.copy()
            r_idx, new_route = best_move
            new_solution.routes[r_idx] = new_route
            new_solution._invalidate_cache()
            return new_solution
        
        return None


# ========== OPERADORES INTER-RUTA ==========

class CrossExchange(LocalSearchOperator):
    """
    Operador Cross-Exchange: intercambia clientes entre dos rutas.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Aplica intercambio entre rutas"""
        
        best_delta = 0
        best_swap = None
        
        # Para cada par de rutas
        for r1 in range(len(solution.routes)):
            for r2 in range(r1 + 1, len(solution.routes)):
                route1 = solution.routes[r1]
                route2 = solution.routes[r2]
                
                # Para cada cliente en ruta1
                for i in range(1, len(route1) - 1):
                    # Para cada cliente en ruta2
                    for j in range(1, len(route2) - 1):
                        # Intercambiar
                        cust1 = route1[i]
                        cust2 = route2[j]
                        
                        new_route1 = route1[:i] + [cust2] + route1[i+1:]
                        new_route2 = route2[:j] + [cust1] + route2[j+1:]
                        
                        # Verificar factibilidad
                        if not (self.problem.is_route_feasible(new_route1) and
                              self.problem.is_route_feasible(new_route2)):
                            continue
                        
                        # Calcular delta
                        old_cost = (self.problem.route_distance(route1) +
                                  self.problem.route_distance(route2))
                        new_cost = (self.problem.route_distance(new_route1) +
                                  self.problem.route_distance(new_route2))
                        delta = new_cost - old_cost
                        
                        if delta < best_delta:
                            best_delta = delta
                            best_swap = (r1, i, new_route1, r2, j, new_route2)
        
        if best_swap:
            new_solution = solution.copy()
            r1, i, new_r1, r2, j, new_r2 = best_swap
            new_solution.routes[r1] = new_r1
            new_solution.routes[r2] = new_r2
            new_solution._invalidate_cache()
            return new_solution
        
        return None


class TwoOptStar(LocalSearchOperator):
    """
    Operador 2-opt*: 2-opt entre rutas.
    
    Intercambia segmentos entre dos rutas.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Aplica 2-opt entre rutas"""
        
        best_delta = 0
        best_move = None
        
        for r1 in range(len(solution.routes)):
            for r2 in range(r1 + 1, len(solution.routes)):
                route1 = solution.routes[r1]
                route2 = solution.routes[r2]
                
                # Para cada segmento en ruta1
                for i in range(1, len(route1) - 1):
                    # Para cada segmento en ruta2
                    for j in range(1, len(route2) - 1):
                        # Intercambiar segmentos
                        new_r1 = route1[:i] + route2[j:] + [route1[-1]]
                        new_r2 = route2[:j] + route1[i:-1] + [route2[-1]]
                        
                        if len(new_r1) <= 2 or len(new_r2) <= 2:
                            continue
                        
                        if not (self.problem.is_route_feasible(new_r1) and
                              self.problem.is_route_feasible(new_r2)):
                            continue
                        
                        old_cost = (self.problem.route_distance(route1) +
                                  self.problem.route_distance(route2))
                        new_cost = (self.problem.route_distance(new_r1) +
                                  self.problem.route_distance(new_r2))
                        delta = new_cost - old_cost
                        
                        if delta < best_delta:
                            best_delta = delta
                            best_move = (r1, new_r1, r2, new_r2)
        
        if best_move:
            new_solution = solution.copy()
            r1, new_r1, r2, new_r2 = best_move
            new_solution.routes[r1] = new_r1
            new_solution.routes[r2] = new_r2
            new_solution._invalidate_cache()
            return new_solution
        
        return None


class RelocateIntRoute(LocalSearchOperator):
    """
    Operador Relocate Inter-Route: mueve cliente de una ruta a otra.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Mueve cliente entre rutas"""
        
        best_delta = 0
        best_move = None
        
        # Para cada ruta origen
        for r_src in range(len(solution.routes)):
            src_route = solution.routes[r_src]
            
            if len(src_route) <= 3:
                continue
            
            # Para cada cliente
            for i in range(1, len(src_route) - 1):
                customer = src_route[i]
                
                # Para cada ruta destino
                for r_dst in range(len(solution.routes)):
                    if r_src == r_dst:
                        continue
                    
                    dst_route = solution.routes[r_dst]
                    
                    # Para cada posición en ruta destino
                    for j in range(1, len(dst_route)):
                        # Crear nuevas rutas
                        new_src = src_route[:i] + src_route[i+1:]
                        new_dst = dst_route[:j] + [customer] + dst_route[j:]
                        
                        if len(new_src) <= 2:
                            continue
                        
                        if not (self.problem.is_route_feasible(new_src) and
                              self.problem.is_route_feasible(new_dst)):
                            continue
                        
                        old_cost = (self.problem.route_distance(src_route) +
                                  self.problem.route_distance(dst_route))
                        new_cost = (self.problem.route_distance(new_src) +
                                  self.problem.route_distance(new_dst))
                        delta = new_cost - old_cost
                        
                        if delta < best_delta:
                            best_delta = delta
                            best_move = (r_src, new_src, r_dst, new_dst)
        
        if best_move:
            new_solution = solution.copy()
            r_src, new_src, r_dst, new_dst = best_move
            new_solution.routes[r_src] = new_src
            new_solution.routes[r_dst] = new_dst
            
            # Eliminar rutas vacías
            new_solution.routes = [r for r in new_solution.routes if len(r) > 2]
            new_solution._invalidate_cache()
            return new_solution
        
        return None


class SwapCustomers(LocalSearchOperator):
    """
    Operador Swap: intercambia dos clientes entre rutas.
    """
    
    def apply(self, solution: VRPTWSolution) -> Optional[VRPTWSolution]:
        """Intercambia clientes entre rutas"""
        
        best_delta = 0
        best_swap = None
        
        for r1 in range(len(solution.routes)):
            for r2 in range(r1 + 1, len(solution.routes)):
                route1 = solution.routes[r1]
                route2 = solution.routes[r2]
                
                for i in range(1, len(route1) - 1):
                    for j in range(1, len(route2) - 1):
                        c1 = route1[i]
                        c2 = route2[j]
                        
                        new_r1 = route1[:i] + [c2] + route1[i+1:]
                        new_r2 = route2[:j] + [c1] + route2[j+1:]
                        
                        if not (self.problem.is_route_feasible(new_r1) and
                              self.problem.is_route_feasible(new_r2)):
                            continue
                        
                        old_cost = (self.problem.route_distance(route1) +
                                  self.problem.route_distance(route2))
                        new_cost = (self.problem.route_distance(new_r1) +
                                  self.problem.route_distance(new_r2))
                        delta = new_cost - old_cost
                        
                        if delta < best_delta:
                            best_delta = delta
                            best_swap = (r1, new_r1, r2, new_r2)
        
        if best_swap:
            new_solution = solution.copy()
            r1, new_r1, r2, new_r2 = best_swap
            new_solution.routes[r1] = new_r1
            new_solution.routes[r2] = new_r2
            new_solution._invalidate_cache()
            return new_solution
        
        return None


# Factory
LOCAL_SEARCH_OPERATORS = {
    # Intra-route
    '2opt': TwoOpt,
    'oropt': OrOpt,
    '3opt': ThreeOpt,
    'relocate': Relocate,
    # Inter-route
    'cross_exchange': CrossExchange,
    '2opt_star': TwoOptStar,
    'relocate_inter': RelocateIntRoute,
    'swap': SwapCustomers,
}


def get_local_search_operator(name: str, problem: VRPTWProblem) -> Optional[LocalSearchOperator]:
    """Obtiene operador de búsqueda local por nombre"""
    operator_class = LOCAL_SEARCH_OPERATORS.get(name.lower())
    if operator_class:
        return operator_class(problem)
    return None
