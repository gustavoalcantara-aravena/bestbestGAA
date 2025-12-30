"""
Perturbation Operators - Escapar de óptimos locales

Operadores que perturbam soluciones para generar diversidad:
1. RandomRecolor: Reasignar colores aleatorios a vértices
2. PartialDestroy: Eliminar colores de un subconjunto de vértices
"""

import numpy as np
from typing import Set

try:
    from ..core.solution import ColoringSolution
    from ..core.problem import GraphColoringProblem
except ImportError:
    from core.solution import ColoringSolution
    from core.problem import GraphColoringProblem


class RandomRecolor:
    """
    Random Recolor - Reasignar colores aleatorios a vértices.
    
    Selecciona un porcentaje de vértices y les asigna colores aleatorios.
    Mantiene la factibilidad mediante asignación greedy.
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution,
                problem: GraphColoringProblem,
                perturbation_rate: float = 0.2,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Perturbam solución mediante recoloreado aleatorio.
        
        Args:
            solution: Solución inicial
            problem: Instancia
            perturbation_rate: Fracción de vértices a reasignar (0.0-1.0)
            rng: Generador aleatorio
            
        Returns:
            Solución perturbada (factible)
        """
        if rng is None:
            rng = np.random.default_rng()
        
        perturbed = solution.copy()
        n_to_perturb = max(1, int(problem.n * perturbation_rate))
        
        # Seleccionar vértices aleatorios
        vertices_to_perturb = rng.choice(
            problem.n,
            size=n_to_perturb,
            replace=False
        )
        
        # Reasignar con color aleatorio (recoloring greedy)
        for v_idx in vertices_to_perturb:
            v = v_idx + 1
            
            # Obtener colores forbididos
            forbidden = {perturbed.coloring[n - 1]
                        for n in problem.get_neighbors(v)
                        if perturbed.coloring[n - 1] > 0}
            
            # Seleccionar color aleatorio
            max_color = max(perturbed.coloring) if max(perturbed.coloring) > 0 else 1
            
            # Intenta color aleatorio
            color = rng.integers(1, max_color + 2)  # Incluir color nuevo
            
            # Si está forbidido, buscar disponible
            while color in forbidden:
                color = rng.integers(1, max_color + 2)
            
            perturbed.coloring[v_idx] = color
        
        perturbed.clear_cache()
        
        return perturbed


class PartialDestroy:
    """
    Partial Destroy - Eliminar colores de subconjunto de vértices.
    
    Selecciona una región del grafo y quita sus colores,
    luego reconoce con greedy.
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution,
                problem: GraphColoringProblem,
                destroy_rate: float = 0.3,
                rng: np.random.Generator = None) -> ColoringSolution:
        """
        Perturbam mediante destrucción parcial y reconstrucción.
        
        Args:
            solution: Solución inicial
            problem: Instancia
            destroy_rate: Fracción de vértices a destruir (0.0-1.0)
            rng: Generador aleatorio
            
        Returns:
            Solución perturbada (factible)
        """
        if rng is None:
            rng = np.random.default_rng()
        
        perturbed = solution.copy()
        n_to_destroy = max(1, int(problem.n * destroy_rate))
        
        # Seleccionar semilla de vértices a destruir
        seed_vertices = set(rng.choice(problem.n, size=1) + 1)
        
        # Expandir región: agregar vecinos
        to_destroy = seed_vertices.copy()
        for v in seed_vertices:
            to_destroy.update(problem.get_neighbors(v))
        
        # Limitar a destroy_rate
        if len(to_destroy) > n_to_destroy:
            to_destroy = set(rng.choice(
                list(to_destroy),
                size=n_to_destroy,
                replace=False
            ))
        
        # Destruir: resetear a color 0
        for v in to_destroy:
            perturbed.coloring[v - 1] = 0
        
        # Reconstruir con greedy
        for v in to_destroy:
            # Asignar color disponible más pequeño
            forbidden = {perturbed.coloring[n - 1]
                        for n in problem.get_neighbors(v)
                        if perturbed.coloring[n - 1] > 0}
            
            color = 1
            while color in forbidden:
                color += 1
            
            perturbed.coloring[v - 1] = color
        
        perturbed.clear_cache()
        
        return perturbed


# Factory function
def get_perturbation(name: str):
    """
    Retorna clase de operador de perturbación por nombre.
    
    Args:
        name: Nombre del operador (random_recolor, partial_destroy)
        
    Returns:
        Clase del operador
    """
    operators = {
        'random_recolor': RandomRecolor,
        'recolor': RandomRecolor,
        'partial_destroy': PartialDestroy,
        'destroy': PartialDestroy
    }
    
    name_lower = name.lower().strip()
    if name_lower not in operators:
        raise ValueError(
            f"Operador de perturbación desconocido: {name}. "
            f"Opciones: {list(operators.keys())}"
        )
    
    return operators[name_lower]
