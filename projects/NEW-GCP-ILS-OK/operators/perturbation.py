"""
Perturbation operators for Graph Coloring (ILS)

Operadores que realizan cambios grandes en la solucion para escapar
de optimos locales en el Iterated Local Search.
"""

from typing import Optional
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution


class RandomRecolor:
    """
    Random Recolor perturbation
    
    Reasigna aleatoriamente los colores de un numero de vertices.
    
    Ventajas:
    - Simple
    - Controlable con parametro strength
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                num_vertices: int, seed: Optional[int] = None) -> ColoringSolution:
        """
        Perturba solucion recoloreando vertices aleatorios
        
        Args:
            solution: Solucion a perturbar
            problem: Instancia del problema
            num_vertices: Numero de vertices a recolorear
            seed: Semilla para reproducibilidad
        
        Returns:
            Solucion perturbada
        """
        if seed is not None:
            np.random.seed(seed)
        
        new_assignment = solution.assignment.copy()
        num_colors = solution.num_colors
        
        # Seleccionar vertices aleatorios
        vertices_to_recolor = np.random.choice(
            problem.vertices,
            size=min(num_vertices, problem.vertices),
            replace=False
        )
        
        # Reasignar colores aleatorios
        for vertex in vertices_to_recolor:
            new_assignment[vertex] = np.random.randint(0, max(num_colors + 1, 2))
        
        return ColoringSolution(new_assignment, problem)


class PartialDestroy:
    """
    Partial Destroy and Repair perturbation
    
    Remueve la coloracion de algunos vertices y los reasigna greedy.
    
    Ventajas:
    - Puede encontrar nuevas regiones del espacio de busqueda
    - Adapta la solucion al destruir parcialmente
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                destruction_rate: float = 0.1, seed: Optional[int] = None) -> ColoringSolution:
        """
        Perturba solucion destruyendo y reparando parte de la coloracion
        
        Args:
            solution: Solucion a perturbar
            problem: Instancia del problema
            destruction_rate: Fraccion de vertices a destruir [0,1]
            seed: Semilla para reproducibilidad
        
        Returns:
            Solucion perturbada
        """
        if seed is not None:
            np.random.seed(seed)
        
        new_assignment = solution.assignment.copy()
        
        # Seleccionar vertices a destruir
        num_to_destroy = max(1, int(problem.vertices * destruction_rate))
        vertices_to_destroy = np.random.choice(
            problem.vertices,
            size=num_to_destroy,
            replace=False
        )
        
        # Marcar como sin color
        for vertex in vertices_to_destroy:
            new_assignment[vertex] = -1
        
        # Reparar greedy: asignar minimo color disponible
        for vertex in vertices_to_destroy:
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(vertex):
                if new_assignment[neighbor] != -1:
                    forbidden_colors.add(new_assignment[neighbor])
            
            color = 0
            while color in forbidden_colors:
                color += 1
            
            new_assignment[vertex] = color
        
        return ColoringSolution(new_assignment, problem)


class ColorClassMerge:
    """
    Color Class Merge perturbation
    
    Combina dos clases de colores y reasigna los vertices de una de ellas.
    
    Ventajas:
    - Intenta reducir numero de colores
    - Puede encontrar oportunidades de compactacion
    """
    
    @staticmethod
    def perturb(solution: ColoringSolution, problem: GraphColoringProblem,
                seed: Optional[int] = None) -> Optional[ColoringSolution]:
        """
        Perturba solucion fusionando clases de colores
        
        Args:
            solution: Solucion a perturbar
            problem: Instancia del problema
            seed: Semilla para reproducibilidad
        
        Returns:
            Solucion perturbada o None si no es posible
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Obtener clases de colores
        color_classes = solution.color_classes
        
        if len(color_classes) < 2:
            return None
        
        # Seleccionar dos clases de colores aleatorias
        colors_to_merge = np.random.choice(
            list(color_classes.keys()),
            size=2,
            replace=False
        )
        
        color1, color2 = colors_to_merge
        vertices_to_move = color_classes[color1]
        
        new_assignment = solution.assignment.copy()
        
        # Intentar mover vertices de color1 a color2
        for vertex in vertices_to_move:
            forbidden_colors = set()
            for neighbor in problem.get_neighbors(vertex):
                if new_assignment[neighbor] != -1:
                    forbidden_colors.add(new_assignment[neighbor])
            
            # Si color2 no es prohibido, usar color2
            if color2 not in forbidden_colors:
                new_assignment[vertex] = color2
            else:
                # Si no, encontrar minimo color disponible
                color = 0
                while color in forbidden_colors:
                    color += 1
                new_assignment[vertex] = color
        
        return ColoringSolution(new_assignment, problem)


class AdaptivePerturbation:
    """
    Adaptive Perturbation
    
    Adapta la intensidad de perturbacion basada en el exito de la busqueda.
    
    Estrategia:
    - Si mejora encontrada: disminuir intensidad
    - Si sin mejora: aumentar intensidad
    """
    
    def __init__(self, initial_strength: float = 0.1):
        """
        Inicializa perturbacion adaptativa
        
        Args:
            initial_strength: Intensidad inicial (0-1)
        """
        self.strength = initial_strength
        self.min_strength = 0.01
        self.max_strength = 0.5
    
    def perturb(self, solution: ColoringSolution, problem: GraphColoringProblem,
                improved: bool, seed: Optional[int] = None) -> ColoringSolution:
        """
        Perturba con intensidad adaptativa
        
        Args:
            solution: Solucion a perturbar
            problem: Instancia del problema
            improved: Si la busqueda local mejoro
            seed: Semilla para reproducibilidad
        
        Returns:
            Solucion perturbada
        """
        # Adaptar intensidad
        if improved:
            # Disminuir intensidad (mantener en region prometedora)
            self.strength *= 0.9
            self.strength = max(self.strength, self.min_strength)
        else:
            # Aumentar intensidad (explorar lejos del optimo local)
            self.strength *= 1.1
            self.strength = min(self.strength, self.max_strength)
        
        # Aplicar perturbacion con intensidad actual
        num_vertices = max(1, int(problem.vertices * self.strength))
        
        return RandomRecolor.perturb(solution, problem, num_vertices, seed)
