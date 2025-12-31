"""
Iterated Local Search for Graph Coloring

Implementacion completa del metaheuristica ILS con inyeccion de dependencias.
"""

from typing import Optional, Dict, List, Tuple
import numpy as np
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
from operators.constructive import GreedyDSATUR, RandomSequential
from operators.improvement import OneVertexMove, KempeChainMove
from operators.perturbation import RandomRecolor, AdaptivePerturbation
from operators.repair import GreedyRepair


class IteratedLocalSearch:
    """
    Iterated Local Search (ILS) para Graph Coloring
    
    Estructura general:
    1. Generar solucion inicial (constructive)
    2. Aplicar busqueda local (improvement)
    3. Si es mejor que best: aceptar
    4. Perturbar solucion (perturbation)
    5. Volver a paso 2
    
    Parametros clave:
    - construction: Operador constructivo para solucion inicial
    - local_search: Operador de busqueda local
    - perturbation: Operador de perturbacion
    - acceptance_criterion: Criterio de aceptacion
    - max_iterations: Iteraciones totales
    - max_no_improve: Iteraciones sin mejora antes de parar
    """
    
    def __init__(self,
                 problem: GraphColoringProblem,
                 seed: Optional[int] = None,
                 max_iterations: int = 1000,
                 max_no_improve: int = 100,
                 ls_max_iterations: int = 100,
                 perturbation_strength: float = 0.1,
                 use_adaptive_perturbation: bool = True,
                 verbose: bool = False):
        """
        Inicializa ILS
        
        Args:
            problem: Instancia del problema
            seed: Semilla para reproducibilidad
            max_iterations: Iteraciones totales maximas
            max_no_improve: Iteraciones sin mejora antes de parar
            ls_max_iterations: Iteraciones maximas de busqueda local
            perturbation_strength: Fuerza inicial de perturbacion (0-1)
            use_adaptive_perturbation: Si usar perturbacion adaptativa
            verbose: Mostrar progreso
        """
        self.problem = problem
        self.seed = seed
        self.max_iterations = max_iterations
        self.max_no_improve = max_no_improve
        self.ls_max_iterations = ls_max_iterations
        self.verbose = verbose
        
        # Operadores
        self.constructor = GreedyDSATUR()
        self.local_search = OneVertexMove()
        self.perturbator = AdaptivePerturbation(perturbation_strength) \
            if use_adaptive_perturbation else None
        self.perturbation_strength = perturbation_strength
        
        # Evaluador
        self.evaluator = ColoringEvaluator()
        
        # Estado
        self.best_solution = None
        self.best_fitness = float('inf')
        self.current_solution = None
        self.current_fitness = float('inf')
        self.iteration = 0
        self.iterations_without_improvement = 0
        
        # Historial
        self.history = {
            'iteration': [],
            'best_fitness': [],
            'current_fitness': [],
            'num_colors': [],
            'num_conflicts': [],
        }
    
    def run(self) -> ColoringSolution:
        """
        Ejecuta el algoritmo ILS
        
        Returns:
            Mejor solucion encontrada
        """
        # Inicializar con solucion constructiva
        if self.verbose:
            print("ILS: Generando solucion inicial...")
        
        self.current_solution = GreedyDSATUR.construct(self.problem, self.seed)
        self.current_fitness = self.current_solution.fitness()
        
        self.best_solution = self.current_solution.copy()
        self.best_fitness = self.current_fitness
        
        if self.verbose:
            print(f"ILS: Solucion inicial: {self.current_fitness} ({self.current_solution.num_colors} colores)")
        
        # ILS principal
        self.iteration = 0
        self.iterations_without_improvement = 0
        
        while self.iteration < self.max_iterations and \
              self.iterations_without_improvement < self.max_no_improve:
            
            # 1. Aplicar busqueda local
            self.current_solution = self._local_search(self.current_solution)
            self.current_fitness = self.current_solution.fitness()
            
            # 2. Verificar si mejora respecto a best
            if self.current_fitness < self.best_fitness:
                self.best_solution = self.current_solution.copy()
                self.best_fitness = self.current_fitness
                self.iterations_without_improvement = 0
                
                if self.verbose:
                    print(f"ILS {self.iteration}: Nueva mejor solucion: "
                          f"{self.best_fitness} ({self.best_solution.num_colors} colores)")
            else:
                self.iterations_without_improvement += 1
            
            # 3. Perturbar solucion actual
            if self.iteration < self.max_iterations - 1:
                self.current_solution = self._perturb(self.current_solution,
                                                      improved=(self.current_fitness < self.best_fitness))
                self.current_fitness = self.current_solution.fitness()
            
            # 4. Registrar en historial
            self._record_iteration()
            
            self.iteration += 1
        
        if self.verbose:
            print(f"ILS: Terminado en {self.iteration} iteraciones")
            print(f"ILS: Mejor solucion: {self.best_fitness} ({self.best_solution.num_colors} colores)")
        
        return self.best_solution
    
    def _local_search(self, solution: ColoringSolution) -> ColoringSolution:
        """
        Aplica busqueda local a solucion
        
        Args:
            solution: Solucion a mejorar
        
        Returns:
            Solucion mejorada
        """
        return self.local_search.improve(solution, self.problem, self.ls_max_iterations)
    
    def _perturb(self, solution: ColoringSolution, improved: bool = False) -> ColoringSolution:
        """
        Perturba solucion para escapar de optimo local
        
        Args:
            solution: Solucion a perturbar
            improved: Si la busqueda local mejoro
        
        Returns:
            Solucion perturbada
        """
        if self.perturbator is not None:
            # Perturbacion adaptativa
            return self.perturbator.perturb(solution, self.problem, improved, self.seed)
        else:
            # Perturbacion fija
            num_vertices = max(1, int(self.problem.vertices * self.perturbation_strength))
            return RandomRecolor.perturb(solution, self.problem, num_vertices, self.seed)
    
    def _record_iteration(self):
        """Registra estado de iteracion actual en historial"""
        self.history['iteration'].append(self.iteration)
        self.history['best_fitness'].append(self.best_fitness)
        self.history['current_fitness'].append(self.current_fitness)
        self.history['num_colors'].append(self.best_solution.num_colors)
        self.history['num_conflicts'].append(self.best_solution.num_conflicts)
    
    def get_statistics(self) -> Dict:
        """
        Retorna estadisticas de la busqueda
        
        Returns:
            Diccionario con estadisticas
        """
        return {
            'total_iterations': self.iteration,
            'best_fitness': self.best_fitness,
            'num_colors': self.best_solution.num_colors,
            'num_conflicts': self.best_solution.num_conflicts,
            'is_feasible': self.best_solution.is_feasible(),
            'iterations_without_improvement': self.iterations_without_improvement,
            'history': self.history,
        }
    
    def get_solution(self) -> ColoringSolution:
        """Retorna mejor solucion encontrada"""
        return self.best_solution


class HybridILS(IteratedLocalSearch):
    """
    Hybrid ILS con multiples operadores de mejora
    
    Alterna entre diferentes estrategias de busqueda local
    para mejorar diversidad de exploracion.
    """
    
    def __init__(self, *args, **kwargs):
        """Inicializa Hybrid ILS (mismos parametros que ILS)"""
        super().__init__(*args, **kwargs)
        self.ls_strategies = [
            OneVertexMove(),
        ]
        self.current_ls_index = 0
    
    def _local_search(self, solution: ColoringSolution) -> ColoringSolution:
        """Aplica busqueda local alternando estrategias"""
        ls = self.ls_strategies[self.current_ls_index]
        self.current_ls_index = (self.current_ls_index + 1) % len(self.ls_strategies)
        
        if hasattr(ls, 'improve'):
            return ls.improve(solution, self.problem, self.ls_max_iterations)
        else:
            # Fallback para operadores sin metodo improve
            return super()._local_search(solution)
