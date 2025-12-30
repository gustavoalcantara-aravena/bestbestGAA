"""
VRPTW Evaluation - Módulo de evaluación multi-criterio

Proporciona criterios de evaluación, métricas de calidad y análisis de soluciones.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from core.solution import VRPTWSolution
from core.problem import VRPTWProblem


class VRPTWEvaluator:
    """
    Evaluador de soluciones VRPTW multi-criterio.
    
    Criterios de evaluación:
    1. Viabilidad (factibilidad de restricciones)
    2. Número de vehículos
    3. Distancia total
    
    Jerarquía: Viabilidad >> Vehículos >> Distancia
    """
    
    def __init__(self, problem: VRPTWProblem, 
                 best_known: Optional[float] = None):
        """
        Inicializa evaluador.
        
        Args:
            problem: Instancia VRPTWProblem
            best_known: Mejor solución conocida (para comparación)
        """
        self.problem = problem
        self.best_known = best_known
        
        # Historiales de evaluación
        self.evaluation_history: List[Dict] = []
        self.best_solution: Optional[VRPTWSolution] = None
        self.best_cost = float('inf')
    
    def evaluate(self, solution: VRPTWSolution) -> Dict:
        """
        Evalúa una solución completa.
        
        Args:
            solution: VRPTWSolution a evaluar
            
        Returns:
            Dict con métricas de evaluación
        """
        solution.evaluate()
        
        metrics = {
            'cost': solution.cost,
            'distance': solution.distance,
            'vehicles': solution.num_routes(),
            'customers': solution.num_customers(),
            'feasible': solution.is_feasible,
            'violations': solution.violation_count,
            'total_demand': solution.total_demand_served(),
            'load_balance': self._compute_load_balance(solution),
            'time_utilization': self._compute_time_utilization(solution),
        }
        
        # Agregar gap si existe best_known
        if self.best_known is not None:
            metrics['gap'] = self._compute_gap(solution)
        
        # Rastrear mejor solución
        if solution.cost < self.best_cost:
            self.best_cost = solution.cost
            self.best_solution = solution.copy()
        
        # Guardar en historial
        self.evaluation_history.append(metrics)
        
        return metrics
    
    def compare(self, sol1: VRPTWSolution, sol2: VRPTWSolution) -> Dict:
        """
        Compara dos soluciones.
        
        Returns:
            Dict con análisis comparativo
        """
        sol1.evaluate()
        sol2.evaluate()
        
        result = {
            'better': 'sol1' if sol1.cost < sol2.cost else 'sol2',
            'cost_diff': abs(sol1.cost - sol2.cost),
            'distance_diff': abs(sol1.distance - sol2.distance),
            'vehicle_diff': abs(sol1.num_routes() - sol2.num_routes()),
            'sol1_feasible': sol1.is_feasible,
            'sol2_feasible': sol2.is_feasible,
        }
        
        # Análisis de viabilidad
        if sol1.is_feasible and not sol2.is_feasible:
            result['better'] = 'sol1'
            result['reason'] = 'sol1 es factible, sol2 no'
        elif sol2.is_feasible and not sol1.is_feasible:
            result['better'] = 'sol2'
            result['reason'] = 'sol2 es factible, sol1 no'
        else:
            # Ambas con mismo estado de viabilidad
            if sol1.num_routes() < sol2.num_routes():
                result['reason'] = 'sol1 usa menos vehículos'
            elif sol2.num_routes() < sol1.num_routes():
                result['reason'] = 'sol2 usa menos vehículos'
            else:
                result['reason'] = 'sol1 menor distancia' if sol1.distance < sol2.distance else 'sol2 menor distancia'
        
        return result
    
    # =========== Métricas Internas ===========
    
    def _compute_gap(self, solution: VRPTWSolution) -> float:
        """
        Calcula GAP respecto a mejor solución conocida.
        
        GAP = (solución - best_known) / best_known * 100
        """
        if self.best_known is None or self.best_known == 0:
            return 0.0
        
        return (solution.cost - self.best_known) / self.best_known * 100
    
    def _compute_load_balance(self, solution: VRPTWSolution) -> float:
        """
        Calcula equilibrio de carga entre vehículos.
        
        Usa coeficiente de variación (std/mean).
        """
        if solution.num_routes() == 0:
            return 0.0
        
        loads = []
        for route in solution.routes:
            load = self.problem.route_load(route)
            loads.append(load)
        
        loads = np.array(loads)
        
        if loads.mean() == 0:
            return 0.0
        
        cv = loads.std() / loads.mean() if loads.mean() > 0 else 0
        return float(cv)
    
    def _compute_time_utilization(self, solution: VRPTWSolution) -> float:
        """
        Calcula utilización promedio de ventanas de tiempo.
        
        Returns:
            Porcentaje de utilización (0-100)
        """
        if solution.num_routes() == 0:
            return 0.0
        
        total_utilization = 0.0
        num_routes = 0
        
        for route in solution.routes:
            if len(route) > 2:  # Al menos un cliente
                route_time = self.problem.route_time(route)
                utilization = (route_time / self.problem.time_horizon) * 100
                total_utilization += min(100, utilization)  # Máximo 100%
                num_routes += 1
        
        return total_utilization / num_routes if num_routes > 0 else 0.0
    
    # =========== Análisis de Calidad ===========
    
    def get_quality_score(self, solution: VRPTWSolution) -> float:
        """
        Calcula score de calidad (0-100).
        
        - 100: Factible, mínimos vehículos, distancia óptima
        - >0: Factible
        - 0: Infactible
        """
        metrics = self.evaluate(solution)
        
        if not metrics['feasible']:
            return 0.0
        
        # Score basado en eficiencia
        min_vehicles = self.problem.min_vehicles_needed()
        excess_vehicles = max(0, metrics['vehicles'] - min_vehicles)
        
        # Componentes del score
        vehicle_efficiency = 1.0 - min(0.5, excess_vehicles * 0.1)
        load_balance = max(0.5, 1.0 - metrics['load_balance'])
        time_utilization = metrics['time_utilization'] / 100.0
        
        # Promedio ponderado
        score = (vehicle_efficiency * 0.4 + 
                 load_balance * 0.3 + 
                 time_utilization * 0.3) * 100
        
        return min(100, max(0, score))
    
    def get_feasibility_report(self, solution: VRPTWSolution) -> Dict:
        """
        Genera reporte detallado de viabilidad.
        
        Returns:
            Dict con análisis de restricciones
        """
        solution.evaluate()
        
        report = {
            'overall_feasible': solution.is_feasible,
            'capacity_violations': 0,
            'time_violations': 0,
            'coverage_violations': 0,
            'violation_details': [],
        }
        
        # Verificar cada restricción
        visited = set()
        
        for r_idx, route in enumerate(solution.routes):
            # Capacidad
            if not self.problem.is_capacity_feasible(route):
                report['capacity_violations'] += 1
                load = self.problem.route_load(route)
                report['violation_details'].append({
                    'route': r_idx,
                    'type': 'capacity',
                    'load': load,
                    'capacity': self.problem.vehicle_capacity,
                    'excess': load - self.problem.vehicle_capacity,
                })
            
            # Tiempo
            if not self.problem.is_time_feasible(route):
                report['time_violations'] += 1
                report['violation_details'].append({
                    'route': r_idx,
                    'type': 'time_window',
                })
            
            # Rastrear cobertura
            visited.update(route[1:-1])
        
        # Cobertura
        expected = set(range(1, self.problem.n_nodes))
        missing = expected - visited
        if missing:
            report['coverage_violations'] = len(missing)
            report['violation_details'].append({
                'type': 'coverage',
                'missing_customers': list(missing),
            })
        
        return report
    
    # =========== Estadísticas ===========
    
    def get_statistics(self) -> Dict:
        """
        Calcula estadísticas del historial de evaluación.
        
        Returns:
            Dict con estadísticas
        """
        if not self.evaluation_history:
            return {}
        
        costs = [e['cost'] for e in self.evaluation_history]
        distances = [e['distance'] for e in self.evaluation_history]
        vehicles = [e['vehicles'] for e in self.evaluation_history]
        
        stats = {
            'evaluations': len(self.evaluation_history),
            'best_cost': min(costs),
            'worst_cost': max(costs),
            'avg_cost': np.mean(costs),
            'std_cost': np.std(costs),
            'best_distance': min(distances),
            'worst_distance': max(distances),
            'avg_distance': np.mean(distances),
            'min_vehicles': min(vehicles),
            'max_vehicles': max(vehicles),
            'avg_vehicles': np.mean(vehicles),
            'feasible_ratio': sum(1 for e in self.evaluation_history if e['feasible']) / len(self.evaluation_history),
        }
        
        return stats
    
    # =========== Información ===========
    
    def print_summary(self) -> str:
        """Retorna resumen de evaluación"""
        if not self.best_solution:
            return "No solutions evaluated yet"
        
        stats = self.get_statistics()
        
        summary = f"""
VRPTW Evaluation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Evaluations:          {stats.get('evaluations', 0)}
Feasible Ratio:       {stats.get('feasible_ratio', 0):.2%}

Best Solution:
  Cost:               {self.best_cost:,.2f}
  Distance:           {self.best_solution.distance:,.2f}
  Vehicles:           {self.best_solution.num_routes()}
  Quality Score:      {self.get_quality_score(self.best_solution):.1f}%

Cost Statistics:
  Best:               {stats.get('best_cost', 0):,.2f}
  Worst:              {stats.get('worst_cost', 0):,.2f}
  Average:            {stats.get('avg_cost', 0):,.2f}
  Std Dev:            {stats.get('std_cost', 0):,.2f}

Vehicle Statistics:
  Minimum:            {stats.get('min_vehicles', 0)}
  Maximum:            {stats.get('max_vehicles', 0)}
  Average:            {stats.get('avg_vehicles', 0):.1f}
        """
        
        return summary
