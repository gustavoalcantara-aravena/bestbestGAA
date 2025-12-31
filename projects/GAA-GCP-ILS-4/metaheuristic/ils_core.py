"""
Iterated Local Search (ILS) para Graph Coloring Problem

Implementación de un algoritmo metaheurístico que combina:
1. Construcción: Generar solución inicial
2. Mejora Local: Búsqueda local hasta óptimo local
3. Perturbación: Escape de óptimos locales
4. Aceptación: Criterio para aceptar nuevas soluciones
5. Iteración: Repetir hasta criterio de parada

Referencias:
- Lourenço, H. R., Martin, O. C., & Stützle, T. (2003).
  Iterated local search: Framework and applications.
- Galinier, P., & Hao, J. K. (2006).
  Hybrid evolutionary algorithms for graph coloring.
"""

import time
import numpy as np
from typing import Callable, Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from collections import deque

from core import GraphColoringProblem, ColoringSolution, ColoringEvaluator
from operators import (
    GreedyDSATUR, RandomSequential,
    KempeChain, TabuCol,
    RandomRecolor, PartialDestroy,
    RepairConflicts
)


@dataclass
class ILSHistory:
    """Registro histórico de la ejecución de ILS"""
    iterations: List[int] = field(default_factory=list)
    best_fitness: List[float] = field(default_factory=list)
    current_fitness: List[float] = field(default_factory=list)
    num_colors: List[int] = field(default_factory=list)
    num_conflicts: List[int] = field(default_factory=list)
    times: List[float] = field(default_factory=list)
    acceptance_decisions: List[bool] = field(default_factory=list)
    improvement_steps: List[bool] = field(default_factory=list)
    
    def add_iteration(self, iteration: int, best_fitness: float,
                     current_fitness: float, num_colors: int,
                     num_conflicts: int, elapsed_time: float,
                     accepted: bool, improved: bool) -> None:
        """Registrar información de una iteración"""
        self.iterations.append(iteration)
        self.best_fitness.append(best_fitness)
        self.current_fitness.append(current_fitness)
        self.num_colors.append(num_colors)
        self.num_conflicts.append(num_conflicts)
        self.times.append(elapsed_time)
        self.acceptance_decisions.append(accepted)
        self.improvement_steps.append(improved)


class IteratedLocalSearch:
    """
    Algoritmo Iterated Local Search (ILS)
    
    Pipeline:
    1. Construcción: Generar solución inicial s0
    2. Mejora: Aplicar búsqueda local a s0 → s*
    3. Mejor global: best = s*
    4. Perturbación: Perturbar s* → s'
    5. Mejora: Búsqueda local en s' → s*'
    6. Aceptación: Aceptar s*' según criterio
    7. Iteración: Repetir 4-6 hasta criterio parada
    8. Retornar: best
    
    Parámetros configurables:
    - Operador constructivo
    - Operador de mejora (búsqueda local)
    - Operador de perturbación
    - Criterio de aceptación
    - Criterios de parada
    """
    
    def __init__(self,
                 problem: GraphColoringProblem,
                 constructive: Callable = None,
                 improvement: Callable = None,
                 perturbation: Callable = None,
                 acceptance_strategy: str = "best",
                 max_iterations: int = 500,
                 time_budget: float = 300.0,
                 no_improvement_limit: int = 50,
                 seed: int = None,
                 verbose: bool = False):
        """
        Inicializar algoritmo ILS.
        
        Parámetros:
            problem: Instancia GCP
            constructive: Operador constructivo (default: GreedyDSATUR)
            improvement: Operador mejora (default: KempeChain)
            perturbation: Operador perturbación (default: RandomRecolor)
            acceptance_strategy: "best" (solo mejora), "always", "probabilistic"
            max_iterations: Máximo de iteraciones
            time_budget: Presupuesto de tiempo en segundos
            no_improvement_limit: Parar después de N iteraciones sin mejora
            seed: Seed para reproducibilidad
            verbose: Mostrar progreso
        """
        self.problem = problem
        self.constructive = constructive or GreedyDSATUR.construct
        self.improvement = improvement or KempeChain.improve
        self.perturbation = perturbation or RandomRecolor.perturb
        self.acceptance_strategy = acceptance_strategy
        self.max_iterations = max_iterations
        self.time_budget = time_budget
        self.no_improvement_limit = no_improvement_limit
        self.seed = seed
        self.verbose = verbose
        
        if seed is not None:
            np.random.seed(seed)
        
        self.best_solution: Optional[ColoringSolution] = None
        self.best_fitness: float = float('inf')
        self.iteration_count: int = 0
        self.history = ILSHistory()
    
    def solve(self) -> Tuple[ColoringSolution, ILSHistory]:
        """
        Ejecutar algoritmo ILS.
        
        Retorna:
            (best_solution, history): Mejor solución encontrada e historial
        """
        start_time = time.time()
        
        # Paso 1: Construcción
        current_solution = self.constructive(self.problem, seed=self.seed)
        current_solution = RepairConflicts.repair(current_solution, self.problem)
        
        # Paso 2: Mejora inicial
        current_solution = self.improvement(current_solution, self.problem)
        
        # Paso 3: Mejor global
        self.best_solution = current_solution.copy()
        self.best_fitness = ColoringEvaluator.evaluate(
            current_solution, self.problem
        )['num_colors']
        
        if self.verbose:
            print(f"Solución inicial: {self.best_fitness} colores")
        
        # Contadores
        no_improvement_count = 0
        iteration = 0
        
        # Bucle principal
        while iteration < self.max_iterations:
            iteration += 1
            self.iteration_count = iteration
            
            # Verificar tiempo
            elapsed = time.time() - start_time
            if elapsed > self.time_budget:
                if self.verbose:
                    print(f"[Parada] Presupuesto de tiempo agotado")
                break
            
            # Paso 4: Perturbación
            perturbed = self.perturbation(current_solution, self.problem)
            
            # Paso 5: Mejora
            improved_solution = self.improvement(perturbed, self.problem)
            
            # Paso 6: Aceptación
            improved_solution = RepairConflicts.repair(
                improved_solution, self.problem
            )
            
            new_fitness = ColoringEvaluator.evaluate(
                improved_solution, self.problem
            )['num_colors']
            
            current_fitness = ColoringEvaluator.evaluate(
                current_solution, self.problem
            )['num_colors']
            
            accepted = self._accept(current_fitness, new_fitness)
            
            if accepted:
                current_solution = improved_solution
                
                # Actualizar mejor global
                if new_fitness < self.best_fitness:
                    self.best_solution = improved_solution.copy()
                    self.best_fitness = new_fitness
                    no_improvement_count = 0
                    
                    if self.verbose:
                        print(f"Iter {iteration}: Mejora a {self.best_fitness} "
                              f"colores ({elapsed:.1f}s)")
                else:
                    no_improvement_count += 1
            else:
                no_improvement_count += 1
            
            # Registrar en historial
            self.history.add_iteration(
                iteration,
                self.best_fitness,
                new_fitness,
                self.best_solution.num_colors if self.best_solution else new_fitness,
                self.best_solution.num_conflicts(self.problem) if self.best_solution else 0,
                elapsed,
                accepted,
                new_fitness < current_fitness
            )
            
            # Verificar criterio de parada (sin mejora)
            if no_improvement_count >= self.no_improvement_limit:
                if self.verbose:
                    print(f"[Parada] {self.no_improvement_limit} iteraciones sin mejora")
                break
        
        if self.verbose:
            total_time = time.time() - start_time
            print(f"\nResultado final: {self.best_fitness} colores "
                  f"({total_time:.1f}s, {iteration} iteraciones)")
        
        return self.best_solution, self.history
    
    def _accept(self, current_fitness: float, new_fitness: float) -> bool:
        """
        Criterio de aceptación de nueva solución.
        
        Estrategias:
        - "best": Solo acepta si mejora
        - "always": Siempre acepta
        - "probabilistic": Acepta con probabilidad inversamente proporcional a gap
        """
        if self.acceptance_strategy == "best":
            return new_fitness <= current_fitness
        
        elif self.acceptance_strategy == "always":
            return True
        
        elif self.acceptance_strategy == "probabilistic":
            if new_fitness <= current_fitness:
                return True
            else:
                # Aceptar con probabilidad basada en gap
                gap = new_fitness - current_fitness
                prob = np.exp(-gap / 10)  # Parámetro de temperatura
                return np.random.random() < prob
        
        else:
            return new_fitness <= current_fitness


class AdaptiveILS(IteratedLocalSearch):
    """
    Versión adaptativa de ILS que ajusta parámetros durante la búsqueda.
    
    Ajustes:
    - Intensidad de perturbación aumenta si se estanca
    - Operador de mejora cambia según necesidad
    - Tasa de aceptación se adapta
    """
    
    def solve(self) -> Tuple[ColoringSolution, ILSHistory]:
        """
        Ejecutar ILS adaptativo con ajuste de parámetros.
        """
        start_time = time.time()
        
        # Construcción
        current_solution = self.constructive(self.problem, seed=self.seed)
        current_solution = RepairConflicts.repair(current_solution, self.problem)
        
        # Mejora inicial
        current_solution = self.improvement(current_solution, self.problem)
        
        # Mejor global
        self.best_solution = current_solution.copy()
        self.best_fitness = ColoringEvaluator.evaluate(
            current_solution, self.problem
        )['num_colors']
        
        # Variables adaptativas
        perturbation_strength = 0.2
        improvement_history = deque(maxlen=10)
        
        no_improvement_count = 0
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # Verificar tiempo
            elapsed = time.time() - start_time
            if elapsed > self.time_budget:
                break
            
            # Adaptar intensidad de perturbación
            if len(improvement_history) >= 5:
                recent_improvements = list(improvement_history)
                stagnation = 1.0 - (sum(recent_improvements) / 
                                   (len(recent_improvements) * (self.best_fitness + 1)))
                perturbation_strength = 0.1 + stagnation * 0.4
            
            # Perturbación adaptativa
            if np.random.random() < 0.7:
                perturbed = RandomRecolor.perturb(
                    current_solution, self.problem, ratio=perturbation_strength
                )
            else:
                perturbed = PartialDestroy.perturb(
                    current_solution, self.problem, region_size=perturbation_strength
                )
            
            # Mejora
            improved_solution = self.improvement(perturbed, self.problem)
            improved_solution = RepairConflicts.repair(
                improved_solution, self.problem
            )
            
            new_fitness = ColoringEvaluator.evaluate(
                improved_solution, self.problem
            )['num_colors']
            
            current_fitness = ColoringEvaluator.evaluate(
                current_solution, self.problem
            )['num_colors']
            
            # Aceptación
            accepted = self._accept(current_fitness, new_fitness)
            
            improvement = current_fitness - new_fitness
            improvement_history.append(improvement)
            
            if accepted:
                current_solution = improved_solution
                
                if new_fitness < self.best_fitness:
                    self.best_solution = improved_solution.copy()
                    self.best_fitness = new_fitness
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
            else:
                no_improvement_count += 1
            
            # Registrar
            self.history.add_iteration(
                iteration,
                self.best_fitness,
                new_fitness,
                self.best_solution.num_colors,
                self.best_solution.num_conflicts(self.problem),
                elapsed,
                accepted,
                improvement > 0
            )
            
            if no_improvement_count >= self.no_improvement_limit:
                break
        
        return self.best_solution, self.history


if __name__ == "__main__":
    # Ejemplo de uso
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    
    print("=== Iterated Local Search ===\n")
    
    # ILS estándar
    ils = IteratedLocalSearch(
        problem,
        max_iterations=200,
        time_budget=30.0,
        seed=42,
        verbose=True
    )
    
    best_solution, history = ils.solve()
    
    metrics = ColoringEvaluator.evaluate(best_solution, problem)
    print(f"\nMétricas finales:")
    print(f"  Colores: {metrics['num_colors']}")
    print(f"  Conflictos: {metrics['conflicts']}")
    print(f"  Factible: {metrics['feasible']}")
    print(f"  Gap: {metrics['gap']} ({metrics['gap_percent']:.2f}%)")
