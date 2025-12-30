"""
GRASP Core - Implementación del algoritmo GRASP (Greedy Randomized Adaptive Search Procedure)

Combina construcción greedy randomizada con búsqueda local variable neighborhood descent.
"""

from typing import List, Dict, Optional, Tuple
import time
import random
from copy import deepcopy

from core.problem import VRPTWProblem
from core.solution import VRPTWSolution
from core.evaluation import VRPTWEvaluator

from operators.constructive import get_constructive_operator
from operators.local_search import (
    TwoOpt, OrOpt, Relocate, 
    CrossExchange, TwoOptStar, RelocateIntRoute
)
from operators.perturbation import RuinRecreate
from operators.repair import HybridRepair


class GRASPParameters:
    """Parámetros configurables para GRASP"""
    
    def __init__(self):
        self.max_iterations = 100
        self.alpha_rcl = 0.15  # RCL parameter (0=greedy, 1=random)
        self.stagnation_limit = 20  # Iteraciones sin mejora antes de perturbar
        self.time_limit = None  # Límite de tiempo en segundos
        self.construction_method = 'randomized'  # Método constructivo
        self.seed = None  # Seed para reproducibilidad
        self.repair_strategy = 'hybrid'  # Estrategia de reparación
        self.log_level = 0  # 0=silent, 1=minimal, 2=detailed
    
    def __repr__(self) -> str:
        return f"""
GRASPParameters:
  max_iterations:     {self.max_iterations}
  alpha_rcl:          {self.alpha_rcl}
  stagnation_limit:   {self.stagnation_limit}
  time_limit:         {self.time_limit}
  construction_method: {self.construction_method}
  seed:               {self.seed}
  repair_strategy:    {self.repair_strategy}
        """


class GRASPStatistics:
    """Estadísticas de ejecución del GRASP"""
    
    def __init__(self):
        self.total_iterations = 0
        self.total_time = 0
        self.best_cost = float('inf')
        self.best_iteration = 0
        self.stagnation_counter = 0
        self.improvement_history = []
        self.iteration_times = []
        self.construction_times = []
        self.local_search_times = []
    
    def record_iteration(self, iteration: int, cost: float, 
                        construction_time: float, ls_time: float) -> None:
        """Registra estadísticas de iteración"""
        self.total_iterations = iteration
        self.iteration_times.append(construction_time + ls_time)
        self.construction_times.append(construction_time)
        self.local_search_times.append(ls_time)
        
        if cost < self.best_cost:
            self.best_cost = cost
            self.best_iteration = iteration
            self.stagnation_counter = 0
        else:
            self.stagnation_counter += 1
        
        self.improvement_history.append(cost)
    
    def summary(self) -> str:
        """Retorna resumen de estadísticas"""
        if self.total_iterations == 0:
            return "No statistics available"
        
        avg_time = self.total_time / self.total_iterations if self.total_iterations > 0 else 0
        
        return f"""
GRASP Execution Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Iterations:       {self.total_iterations}
Best Cost:              {self.best_cost:,.2f}
Best at Iteration:      {self.best_iteration}
Total Time:             {self.total_time:.2f}s
Avg Time per Iter:      {avg_time:.3f}s
Stagnation Counter:     {self.stagnation_counter}

Time Breakdown:
  Construction Phase:   {sum(self.construction_times):.2f}s ({sum(self.construction_times)/self.total_time*100:.1f}%)
  Local Search Phase:   {sum(self.local_search_times):.2f}s ({sum(self.local_search_times)/self.total_time*100:.1f}%)
        """


class GRASP:
    """
    Implementación de GRASP para VRPTW.
    
    Estructura:
    1. Fase de construcción: Greedy randomizado con RCL
    2. Fase de mejora: Variable Neighborhood Descent (VND)
    3. Perturbación: Escape de óptimos locales
    """
    
    def __init__(self, problem: VRPTWProblem, params: Optional[GRASPParameters] = None):
        """
        Inicializa GRASP.
        
        Args:
            problem: Instancia VRPTWProblem
            params: GRASPParameters (defaults si None)
        """
        self.problem = problem
        self.params = params or GRASPParameters()
        self.evaluator = VRPTWEvaluator(problem)
        self.statistics = GRASPStatistics()
        
        # Configurar seed si se proporciona
        if self.params.seed is not None:
            random.seed(self.params.seed)
        
        # Mejor solución encontrada
        self.best_solution = None
        
        # Neighborhoods para VND
        self.neighborhoods = self._setup_neighborhoods()
    
    def _setup_neighborhoods(self) -> List:
        """Configura orden de neighborhoods para VND"""
        return [
            (TwoOpt(self.problem), "2-opt"),
            (OrOpt(self.problem), "Or-opt"),
            (Relocate(self.problem), "Relocate"),
            (CrossExchange(self.problem), "Cross-exchange"),
            (TwoOptStar(self.problem), "2-opt*"),
            (RelocateIntRoute(self.problem), "Relocate-inter"),
        ]
    
    def solve(self) -> VRPTWSolution:
        """
        Ejecuta GRASP.
        
        Returns:
            Mejor solución encontrada
        """
        if self.params.seed is not None:
            random.seed(self.params.seed)
        
        start_time = time.time()
        
        if self.params.log_level >= 1:
            print(f"\nGRASP Execution Started")
            print(f"Problem: {self.problem.name}")
            print(f"Instance: {self.problem.n_customers} customers")
            print(f"Parameters: alpha_rcl={self.params.alpha_rcl}, "
                  f"max_iterations={self.params.max_iterations}")
        
        iteration = 0
        
        while iteration < self.params.max_iterations:
            iteration += 1
            
            # Verificar límite de tiempo
            if self.params.time_limit:
                if time.time() - start_time > self.params.time_limit:
                    break
            
            iter_start = time.time()
            
            # Fase 1: Construcción
            const_start = time.time()
            solution = self._construction_phase()
            const_time = time.time() - const_start
            
            # Fase 2: Búsqueda local
            ls_start = time.time()
            solution = self._local_search_phase(solution)
            ls_time = time.time() - ls_start
            
            # Fase 3: Perturbación si está estancado
            if self.statistics.stagnation_counter >= self.params.stagnation_limit:
                if self.params.log_level >= 2:
                    print(f"  Stagnation detected, applying perturbation...")
                solution = self._perturbation_phase(solution)
            
            # Actualizar mejor solución
            if self.best_solution is None or solution.cost < self.best_solution.cost:
                self.best_solution = solution.copy()
                if self.params.log_level >= 1:
                    print(f"Iteration {iteration:3d}: Cost = {solution.cost:10,.2f} "
                          f"(improved) | Vehicles: {solution.num_routes()}")
            else:
                if self.params.log_level >= 2:
                    print(f"Iteration {iteration:3d}: Cost = {solution.cost:10,.2f} "
                          f"| Vehicles: {solution.num_routes()}")
            
            # Registrar estadísticas
            self.statistics.record_iteration(iteration, solution.cost, const_time, ls_time)
        
        # Tiempo total
        self.statistics.total_time = time.time() - start_time
        
        if self.params.log_level >= 1:
            print(f"\nGRASP Execution Completed")
            print(self.statistics.summary())
        
        return self.best_solution
    
    def _construction_phase(self) -> VRPTWSolution:
        """
        Fase de construcción: greedy randomizado con RCL.
        
        Returns:
            Solución inicial construida
        """
        # Obtener operador constructivo
        operator = get_constructive_operator(self.params.construction_method, self.problem)
        
        if operator is None:
            # Fallback a nearest neighbor
            operator = get_constructive_operator('nearest_neighbor', self.problem)
        
        # Construir solución
        if hasattr(operator, 'build'):
            solution = operator.build(alpha=self.params.alpha_rcl)
        else:
            solution = operator.build()
        
        # Reparar si es necesario
        if not solution.is_feasible:
            repair_op = HybridRepair(self.problem)
            solution = repair_op.repair(solution)
        
        return solution
    
    def _local_search_phase(self, solution: VRPTWSolution) -> VRPTWSolution:
        """
        Fase de búsqueda local: Variable Neighborhood Descent.
        
        Args:
            solution: Solución inicial
            
        Returns:
            Solución mejorada
        """
        current = solution.copy()
        neighborhood_idx = 0
        
        while neighborhood_idx < len(self.neighborhoods):
            operator, name = self.neighborhoods[neighborhood_idx]
            
            # Intentar mejorar con el operador actual
            improved = operator.apply(current)
            
            if improved is not None and improved.cost < current.cost:
                # Mejora encontrada, reiniciar con primer neighborhood
                current = improved
                neighborhood_idx = 0
                
                if self.params.log_level >= 2:
                    print(f"    Improved via {name}: {current.cost:.2f}")
            else:
                # Sin mejora, pasar al siguiente neighborhood
                neighborhood_idx += 1
        
        return current
    
    def _perturbation_phase(self, solution: VRPTWSolution) -> VRPTWSolution:
        """
        Fase de perturbación: escape de óptimos locales.
        
        Args:
            solution: Solución actual
            
        Returns:
            Solución perturbada
        """
        perturbator = RuinRecreate(self.problem)
        
        # Aplicar perturbación con 20% de clientes removidos
        perturbed = perturbator.apply(solution, ruin_percentage=0.2)
        
        # Reparar si es necesario
        if not perturbed.is_feasible:
            repair_op = HybridRepair(self.problem)
            perturbed = repair_op.repair(perturbed)
        
        return perturbed
    
    def get_statistics(self) -> GRASPStatistics:
        """Retorna estadísticas de ejecución"""
        return self.statistics
    
    def get_best_solution(self) -> Optional[VRPTWSolution]:
        """Retorna mejor solución encontrada"""
        return self.best_solution
    
    def print_summary(self) -> str:
        """Retorna resumen de ejecución"""
        if self.best_solution is None:
            return "No solution found"
        
        return f"""
GRASP Execution Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Problem:          {self.problem.name}
Customers:        {self.problem.n_customers}

Best Solution:
{self.best_solution.info()}

Execution Statistics:
{self.statistics.summary()}
        """


# Función de utilidad para ejecutar GRASP
def solve_vrptw(problem: VRPTWProblem, 
                max_iterations: int = 100,
                alpha_rcl: float = 0.15,
                time_limit: Optional[float] = None,
                seed: Optional[int] = None,
                log_level: int = 1) -> VRPTWSolution:
    """
    Resuelve problema VRPTW usando GRASP.
    
    Args:
        problem: Instancia VRPTWProblem
        max_iterations: Máximo número de iteraciones
        alpha_rcl: Parámetro RCL (0=greedy, 1=random)
        time_limit: Límite de tiempo en segundos
        seed: Seed para reproducibilidad
        log_level: Nivel de logging (0=silent, 1=minimal, 2=detailed)
    
    Returns:
        Mejor solución encontrada
    """
    params = GRASPParameters()
    params.max_iterations = max_iterations
    params.alpha_rcl = alpha_rcl
    params.time_limit = time_limit
    params.seed = seed
    params.log_level = log_level
    
    grasp = GRASP(problem, params)
    return grasp.solve()
