"""
Evaluator - Función de evaluación para soluciones de Graph Coloring Problem

Calcula:
- Fitness: números de colores (objetivo primario)
- Penalización por conflictos
- Brecha respecto al óptimo conocido
- Restricciones de factibilidad
"""

from typing import Dict, Optional, Union

try:
    from .solution import ColoringSolution
    from .problem import GraphColoringProblem
except ImportError:
    from core.solution import ColoringSolution
    from core.problem import GraphColoringProblem


class ColoringEvaluator:
    """
    Evaluador de soluciones del Graph Coloring Problem.
    
    La evaluación considera:
    1. Número de colores (objetivo primario)
    2. Número de conflictos (para soluciones infactibles)
    3. Brecha al óptimo conocido (si disponible)
    """
    
    def __init__(self, problem: GraphColoringProblem):
        """
        Inicializa evaluador.
        
        Args:
            problem: Instancia del problema
        """
        self.problem = problem
    
    def evaluate(self, solution: ColoringSolution) -> Dict[str, Union[int, float]]:
        """
        Evalúa una solución de forma completa.
        
        Args:
            solution: Solución a evaluar
            
        Returns:
            Dict con métricas:
            - 'k': Número de colores
            - 'conflicts': Número de aristas monocromáticas
            - 'is_feasible': True si no hay conflictos
            - 'gap_to_optimal': Brecha al óptimo (si conocido)
            - 'gap_percentage': Porcentaje de brecha
            - 'penalty': Penalización total (k + peso*conflictos)
        """
        k = solution.num_colors
        conflicts = solution.count_conflicts(self.problem)
        is_feasible = conflicts == 0
        
        # Calcular brecha al óptimo
        gap_to_optimal = None
        gap_percentage = None
        if self.problem.optimal_value is not None:
            gap_to_optimal = k - self.problem.optimal_value
            gap_percentage = (gap_to_optimal / self.problem.optimal_value) * 100
        
        # Penalización: k + peso * conflictos
        # Usa un peso alto para conflictos para forzar factibilidad
        penalty = k + 1000 * conflicts
        
        return {
            'k': k,
            'conflicts': conflicts,
            'is_feasible': is_feasible,
            'gap_to_optimal': gap_to_optimal,
            'gap_percentage': gap_percentage,
            'penalty': penalty
        }
    
    def fitness(self, solution: ColoringSolution) -> float:
        """
        Calcula el fitness (valor a minimizar).
        
        Para soluciones factibles: k (número de colores)
        Para soluciones infactibles: k + penalización por conflictos
        
        Args:
            solution: Solución a evaluar
            
        Returns:
            Fitness value (menor es mejor)
        """
        evaluation = self.evaluate(solution)
        return float(evaluation['penalty'])
    
    def is_better(self, sol1: ColoringSolution, sol2: ColoringSolution) -> bool:
        """
        Compara dos soluciones.
        
        Criterios (en orden):
        1. Factibilidad: factible > infactible
        2. Si ambas factibles: menor k
        3. Si ambas infactibles: menor conflictos, luego menor k
        
        Args:
            sol1, sol2: Soluciones a comparar
            
        Returns:
            True si sol1 es mejor que sol2
        """
        eval1 = self.evaluate(sol1)
        eval2 = self.evaluate(sol2)
        
        # Criterio 1: Factibilidad
        if eval1['is_feasible'] and not eval2['is_feasible']:
            return True
        if not eval1['is_feasible'] and eval2['is_feasible']:
            return False
        
        # Criterio 2: Si ambas factibles, comparar k
        if eval1['is_feasible'] and eval2['is_feasible']:
            return eval1['k'] < eval2['k']
        
        # Criterio 3: Si ambas infactibles, menor conflictos, luego menor k
        if eval1['conflicts'] != eval2['conflicts']:
            return eval1['conflicts'] < eval2['conflicts']
        
        return eval1['k'] < eval2['k']
    
    def count_conflicts(self, solution: ColoringSolution) -> int:
        """
        Cuenta conflictos en una solución.
        
        Args:
            solution: Solución
            
        Returns:
            Número de aristas monocromáticas
        """
        return solution.count_conflicts(self.problem)
    
    def get_upper_bound(self) -> int:
        """
        Retorna cota superior para número de colores.
        
        Usa Δ + 1 (greedy coloring bound), donde Δ es el grado máximo.
        
        Returns:
            Cota superior
        """
        return self.problem.max_degree + 1
    
    def get_lower_bound(self) -> int:
        """
        Retorna cota inferior para número de colores.
        
        Returns:
            Cota inferior (del problema si existe, sino 1)
        """
        return self.problem.lower_bound
    
    def gap_to_lower_bound(self, k: int) -> int:
        """
        Calcula brecha respecto a cota inferior.
        
        Args:
            k: Número de colores actual
            
        Returns:
            k - lower_bound
        """
        return k - self.get_lower_bound()
    
    def gap_to_upper_bound(self, k: int) -> int:
        """
        Calcula brecha respecto a cota superior.
        
        Args:
            k: Número de colores actual
            
        Returns:
            upper_bound - k
        """
        return self.get_upper_bound() - k
    
    def optimality_gap(self, k: int) -> Optional[float]:
        """
        Calcula brecha de optimalidad (si se conoce óptimo).
        
        Args:
            k: Número de colores
            
        Returns:
            (k - k_opt) / k_opt * 100, o None si no se conoce óptimo
        """
        if self.problem.optimal_value is None:
            return None
        
        return ((k - self.problem.optimal_value) 
                / self.problem.optimal_value * 100)
    
    def evaluate_batch(self, solutions: list) -> list:
        """
        Evalúa un lote de soluciones.
        
        Args:
            solutions: Lista de ColoringSolution
            
        Returns:
            Lista de dicts de evaluación
        """
        return [self.evaluate(sol) for sol in solutions]
    
    def best_of_batch(self, solutions: list) -> int:
        """
        Retorna el índice de la mejor solución en un lote.
        
        Args:
            solutions: Lista de ColoringSolution
            
        Returns:
            Índice de la mejor solución
        """
        if not solutions:
            raise ValueError("Lista vacía")
        
        best_idx = 0
        for i in range(1, len(solutions)):
            if self.is_better(solutions[i], solutions[best_idx]):
                best_idx = i
        
        return best_idx
    
    def summary(self, solution: ColoringSolution) -> str:
        """
        Retorna resumen de evaluación en formato string.
        
        Args:
            solution: Solución a evaluar
            
        Returns:
            String con métricas formateadas
        """
        eval_dict = self.evaluate(solution)
        
        summary = f"""
Evaluation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Número de colores:      {eval_dict['k']}
Conflictos:             {eval_dict['conflicts']}
Factible:               {'✓ YES' if eval_dict['is_feasible'] else '✗ NO'}
        """
        
        if eval_dict['gap_to_optimal'] is not None:
            summary += f"""Gap al óptimo:          {eval_dict['gap_to_optimal']} ({eval_dict['gap_percentage']:.2f}%)
        """
        
        summary += f"""Bounds:
  - Lower bound:        {self.get_lower_bound()}
  - Upper bound:        {self.get_upper_bound()}
  - Gap (lower):        {self.gap_to_lower_bound(eval_dict['k'])}
  - Gap (upper):        {self.gap_to_upper_bound(eval_dict['k'])}
        """
        
        return summary
