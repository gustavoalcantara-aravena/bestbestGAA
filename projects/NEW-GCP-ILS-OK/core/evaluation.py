"""
Core module: Graph Coloring Problem evaluator

Este modulo define la clase ColoringEvaluator que calcula
metricas de calidad para soluciones del GCP.
"""

from typing import Dict, List, Any, Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class ColoringEvaluator:
    """
    Evaluador de soluciones para el Graph Coloring Problem
    
    Calcula multiples metricas de calidad para soluciones:
    - fitness: numero de colores + penalizacion por conflictos
    - num_colors: numero de colores utilizados
    - num_conflicts: numero de aristas monocromaticas
    - is_feasible: indicador de factibilidad
    - gap: brecha respecto a mejor conocido
    
    Ejemplo:
        >>> problem = GraphColoringProblem(vertices=5, edges=[(0,1), (1,2)])
        >>> solution = ColoringSolution(np.array([0, 1, 0, 1, 0]), problem)
        >>> metrics = ColoringEvaluator.evaluate(solution, problem)
        >>> print(metrics['num_colors'])
        2
        >>> print(metrics['is_feasible'])
        True
    """
    
    CONFLICT_PENALTY = 100  # Penalizacion por cada conflicto
    
    @staticmethod
    def evaluate(
        solution: ColoringSolution,
        problem: GraphColoringProblem,
        penalty_weight: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Evalua una solucion y retorna sus metricas
        
        Args:
            solution: Solucion a evaluar
            problem: Instancia del problema
            penalty_weight: Peso de penalizacion (por defecto CONFLICT_PENALTY)
        
        Returns:
            Dict con claves:
                - num_colors (int): Numero de colores utilizados
                - num_conflicts (int): Numero de conflictos
                - is_feasible (bool): Indica si es factible
                - fitness (float): Valor de fitness
                - gap (Optional[float]): Gap respecto a optimo si es conocido
                - conflict_ratio (float): Porcentaje de aristas en conflicto
        """
        if penalty_weight is None:
            penalty_weight = ColoringEvaluator.CONFLICT_PENALTY
        
        # Obtener metricas basicas
        num_colors = solution.num_colors
        num_conflicts = solution.num_conflicts
        is_feasible = solution.is_feasible()
        
        # Calcular fitness con penalizacion
        fitness = num_colors + num_conflicts * penalty_weight
        
        # Calcular gap respecto a optimo si es conocido
        gap = None
        gap_percent = None
        if problem.colors_known is not None:
            gap = num_colors - problem.colors_known
            gap_percent = (gap / problem.colors_known * 100) if problem.colors_known > 0 else 0
        
        # Calcular razon de conflictos
        conflict_ratio = 0.0
        if problem.num_edges > 0:
            conflict_ratio = num_conflicts / problem.num_edges * 100
        
        return {
            'num_colors': num_colors,
            'num_conflicts': num_conflicts,
            'is_feasible': is_feasible,
            'fitness': fitness,
            'gap': gap,
            'gap_percent': gap_percent,
            'conflict_ratio': conflict_ratio,
            'instance_name': problem.name,
            'instance_source': problem.source,
            'instance_size': problem.vertices,
            'instance_edges': problem.num_edges,
            'instance_density': problem.density
        }
    
    @staticmethod
    def batch_evaluate(
        solutions: List[ColoringSolution],
        problem: GraphColoringProblem,
        penalty_weight: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Evalua multiples soluciones
        
        Args:
            solutions: Lista de soluciones
            problem: Instancia del problema
            penalty_weight: Peso de penalizacion
        
        Returns:
            list: Lista de dicts con metricas (uno por solucion)
        """
        return [
            ColoringEvaluator.evaluate(sol, problem, penalty_weight)
            for sol in solutions
        ]
    
    @staticmethod
    def compare_solutions(
        solution1: ColoringSolution,
        solution2: ColoringSolution,
        problem: GraphColoringProblem
    ) -> Dict[str, Any]:
        """
        Compara dos soluciones
        
        Args:
            solution1: Primera solucion
            solution2: Segunda solucion
            problem: Instancia del problema
        
        Returns:
            Dict con:
                - metrics1: Metricas de solucion1
                - metrics2: Metricas de solucion2
                - better: Cual es mejor (1, 2, o 'tie')
                - color_diff: Diferencia en numero de colores
                - conflict_diff: Diferencia en conflictos
        """
        metrics1 = ColoringEvaluator.evaluate(solution1, problem)
        metrics2 = ColoringEvaluator.evaluate(solution2, problem)
        
        # Comparar por numero de colores principalmente
        if metrics1['num_colors'] < metrics2['num_colors']:
            better = 1
        elif metrics2['num_colors'] < metrics1['num_colors']:
            better = 2
        else:
            # Empate en colores, desempatar por conflictos
            if metrics1['num_conflicts'] < metrics2['num_conflicts']:
                better = 1
            elif metrics2['num_conflicts'] < metrics1['num_conflicts']:
                better = 2
            else:
                better = 'tie'
        
        return {
            'metrics1': metrics1,
            'metrics2': metrics2,
            'better': better,
            'color_diff': metrics1['num_colors'] - metrics2['num_colors'],
            'conflict_diff': metrics1['num_conflicts'] - metrics2['num_conflicts']
        }
    
    @staticmethod
    def print_report(
        metrics: Dict[str, Any],
        detailed: bool = False
    ) -> str:
        """
        Genera un reporte formateado de metricas
        
        Args:
            metrics: Dict de metricas
            detailed: Si incluir detalles adicionales
        
        Returns:
            str: Reporte formateado
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"INSTANCIA: {metrics.get('instance_name', 'N/A')}")
        lines.append(f"FUENTE: {metrics.get('instance_source', 'N/A')}")
        lines.append("-" * 60)
        lines.append(f"Numero de colores: {metrics['num_colors']}")
        lines.append(f"Numero de conflictos: {metrics['num_conflicts']}")
        lines.append(f"Factibilidad: {'SI' if metrics['is_feasible'] else 'NO'}")
        lines.append(f"Fitness: {metrics['fitness']:.2f}")
        
        if metrics['gap'] is not None:
            lines.append(f"Gap respecto a BKS: {metrics['gap']} ({metrics['gap_percent']:.1f}%)")
        
        if detailed:
            lines.append("-" * 60)
            lines.append(f"Tamano de instancia: {metrics['instance_size']} vertices")
            lines.append(f"Numero de aristas: {metrics['instance_edges']}")
            lines.append(f"Densidad: {metrics['instance_density']:.4f}")
            lines.append(f"Razon de conflictos: {metrics['conflict_ratio']:.2f}%")
        
        lines.append("=" * 60)
        return "\n".join(lines)
