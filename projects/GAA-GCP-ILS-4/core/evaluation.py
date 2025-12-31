"""
core/evaluation.py
Evaluador de soluciones para el problema de coloración de grafos.

Proporciona:
    - Cálculo de múltiples métricas de calidad
    - Evaluación individual y en lote
    - Gap respecto a óptimo conocido
"""

from typing import Dict, Any, List, Optional
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class ColoringEvaluator:
    """
    Evaluador de soluciones para Graph Coloring Problem.
    
    Calcula múltiples métricas de calidad:
        - num_colors: número de colores utilizados
        - conflicts: número de conflictos (aristas monocromáticas)
        - feasible: ¿es una solución válida?
        - fitness: valor de función objetivo con penalizaciones
        - gap: diferencia respecto a mejor conocido
    """
    
    # Parámetro de penalización
    CONFLICT_PENALTY = 1000
    
    @staticmethod
    def evaluate(
        solution: ColoringSolution,
        problem: GraphColoringProblem
    ) -> Dict[str, Any]:
        """
        Evaluar una solución y retornar métricas de calidad.
        
        Parametros:
        -----------
        solution : ColoringSolution
            Solución a evaluar
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        Dict con claves:
            'num_colors' : int
                Número de colores utilizados (k)
            'conflicts' : int
                Número de conflictos (aristas monocromáticas)
            'feasible' : bool
                ¿Respeta todas las restricciones?
            'fitness' : float
                Valor de función objetivo con penalización
            'gap' : Optional[float]
                (solution.num_colors - optimal) / optimal si se conoce óptimo
            'gap_percent' : Optional[float]
                Gap en porcentaje
        
        Ejemplo:
        --------
        >>> problem = GraphColoringProblem(vertices=3, 
        ...                                 edges=[(1,2), (2,3), (1,3)],
        ...                                 colors_known=3)
        >>> solution = ColoringSolution({1: 0, 2: 1, 3: 2})
        >>> metrics = ColoringEvaluator.evaluate(solution, problem)
        >>> print(f"Colores: {metrics['num_colors']}, Gap: {metrics['gap']}")
        Colores: 3, Gap: 0
        """
        
        # Calcular número de colores
        num_colors = solution.num_colors
        
        # Calcular conflictos
        conflicts = solution.num_conflicts(problem)
        
        # Evaluar factibilidad
        feasible = conflicts == 0
        
        # Calcular fitness con penalización
        fitness = float(num_colors + conflicts * ColoringEvaluator.CONFLICT_PENALTY)
        
        # Calcular gap respecto a óptimo
        gap = None
        gap_percent = None
        if problem.colors_known is not None:
            gap = (num_colors - problem.colors_known) / problem.colors_known
            gap_percent = 100 * gap
        
        return {
            'num_colors': num_colors,
            'conflicts': conflicts,
            'feasible': feasible,
            'fitness': fitness,
            'gap': gap,
            'gap_percent': gap_percent,
        }
    
    @staticmethod
    def batch_evaluate(
        solutions: List[ColoringSolution],
        problem: GraphColoringProblem
    ) -> List[Dict[str, Any]]:
        """
        Evaluar múltiples soluciones.
        
        Parametros:
        -----------
        solutions : List[ColoringSolution]
            Lista de soluciones a evaluar
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        List[Dict]: Lista de métricas para cada solución
        
        Ejemplo:
        --------
        >>> solutions = [sol1, sol2, sol3]
        >>> results = ColoringEvaluator.batch_evaluate(solutions, problem)
        >>> print(f"Mejor solución: {min(results, key=lambda r: r['num_colors'])}")
        """
        return [
            ColoringEvaluator.evaluate(solution, problem)
            for solution in solutions
        ]
    
    @staticmethod
    def get_best(
        solutions: List[ColoringSolution],
        problem: GraphColoringProblem
    ) -> tuple[ColoringSolution, Dict[str, Any]]:
        """
        Obtener la mejor solución de una lista.
        
        Criterio: menos conflictos primero, luego menos colores.
        
        Parametros:
        -----------
        solutions : List[ColoringSolution]
            Lista de soluciones
        problem : GraphColoringProblem
            Instancia del problema
        
        Retorna:
        --------
        Tuple: (mejor_solucion, metricas)
        """
        if not solutions:
            raise ValueError("Lista de soluciones vacía")
        
        results = ColoringEvaluator.batch_evaluate(solutions, problem)
        
        # Ordenar por: factibilidad, número de colores
        best_idx = min(
            range(len(results)),
            key=lambda i: (
                results[i]['conflicts'],  # Primero: menos conflictos
                results[i]['num_colors']   # Segundo: menos colores
            )
        )
        
        return solutions[best_idx], results[best_idx]
    
    @staticmethod
    def get_statistics(
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcular estadísticas sobre una lista de resultados.
        
        Parametros:
        -----------
        results : List[Dict[str, Any]]
            Lista de resultados de evaluación
        
        Retorna:
        --------
        Dict con estadísticas (min, max, mean, std) de cada métrica
        """
        if not results:
            return {}
        
        import numpy as np
        
        statistics = {}
        
        # Extraer valores para cada métrica
        metrics = ['num_colors', 'conflicts', 'fitness', 'gap', 'gap_percent']
        
        for metric in metrics:
            values = [r[metric] for r in results if r[metric] is not None]
            
            if values:
                statistics[metric] = {
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'median': float(np.median(values)),
                }
        
        return statistics
    
    @staticmethod
    def format_result(
        solution: ColoringSolution,
        problem: GraphColoringProblem,
        metrics: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Formato bonito para mostrar resultados de evaluación.
        
        Parametros:
        -----------
        solution : ColoringSolution
            Solución a mostrar
        problem : GraphColoringProblem
            Instancia del problema
        metrics : Optional[Dict]
            Métricas precalculadas (si no se proporcionan, se calculan)
        
        Retorna:
        --------
        str: Formato bonito de los resultados
        """
        if metrics is None:
            metrics = ColoringEvaluator.evaluate(solution, problem)
        
        result_str = f"\n{'='*70}\n"
        result_str += f"Instancia: {problem.name}\n"
        result_str += f"{'='*70}\n"
        result_str += f"Número de colores:     {metrics['num_colors']}\n"
        result_str += f"Conflictos:            {metrics['conflicts']}\n"
        result_str += f"Factible:              {'✓ Sí' if metrics['feasible'] else '✗ No'}\n"
        result_str += f"Fitness:               {metrics['fitness']:.2f}\n"
        
        if problem.colors_known is not None:
            result_str += f"Óptimo conocido:       {problem.colors_known}\n"
            if metrics['gap'] is not None:
                result_str += f"Gap:                   {metrics['gap']:.4f} ({metrics['gap_percent']:.2f}%)\n"
        
        result_str += f"{'='*70}\n"
        
        return result_str


# ============================================================================
# UTILIDADES DE COMPARACIÓN
# ============================================================================

def compare_solutions(
    solutions: List[ColoringSolution],
    problem: GraphColoringProblem
) -> str:
    """
    Comparar múltiples soluciones en formato tabular.
    
    Parametros:
    -----------
    solutions : List[ColoringSolution]
        Soluciones a comparar
    problem : GraphColoringProblem
        Instancia del problema
    
    Retorna:
    --------
    str: Tabla comparativa
    """
    results = ColoringEvaluator.batch_evaluate(solutions, problem)
    
    # Encabezado
    table = f"\n{'='*100}\n"
    table += f"Comparación de Soluciones - {problem.name}\n"
    table += f"{'='*100}\n"
    table += f"{'Sol':<5} {'Colores':<10} {'Conflictos':<12} {'Factible':<10} {'Gap':<10} {'Fitness':<15}\n"
    table += f"{'-'*100}\n"
    
    # Filas
    for i, (solution, result) in enumerate(zip(solutions, results)):
        gap_str = f"{result['gap_percent']:.2f}%" if result['gap_percent'] is not None else "N/A"
        factible_str = "✓" if result['feasible'] else "✗"
        
        table += (
            f"{i+1:<5} "
            f"{result['num_colors']:<10} "
            f"{result['conflicts']:<12} "
            f"{factible_str:<10} "
            f"{gap_str:<10} "
            f"{result['fitness']:<15.2f}\n"
        )
    
    table += f"{'='*100}\n"
    
    return table
