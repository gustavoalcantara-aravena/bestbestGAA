"""
Interpreter - GAA-GCP-ILS-4
Intérprete/ejecutor de algoritmos representados como AST
"""

from typing import Dict, Any, Optional, List
import time
import numpy as np

from .ast_nodes import (
    ASTNode, Seq, While, For, If, Call,
    GreedyConstruct, LocalSearch, Perturbation
)
from core.problem import GraphColoringProblem
from core.solution import ColoringSolution
from core.evaluation import ColoringEvaluator
from operators.constructive import (
    GreedyDSATUR, GreedyLF, RandomSequential
)
from operators.improvement import (
    KempeChain, OneVertexMove, TabuCol
)
from operators.perturbation import (
    RandomRecolor, PartialDestroy
)


class ExecutionContext:
    """
    Contexto de ejecución para intérprete de AST
    
    Mantiene:
    - Solución actual
    - Mejor solución encontrada
    - Estadísticas de ejecución
    - Presupuesto de iteraciones
    """
    
    def __init__(self, 
                 problem: GraphColoringProblem,
                 rng: Optional[np.random.Generator] = None):
        """
        Inicializa contexto
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio
        """
        self.problem = problem
        self.evaluator = ColoringEvaluator()
        self.rng = rng if rng else np.random.default_rng()
        
        # Estado de solución
        self.current_solution = None
        self.best_solution = None
        self.best_value = float('inf')  # Minimizar número de colores
        
        # Estadísticas
        self.iterations = 0
        self.evaluations = 0
        self.start_time = None
        self.improvement_iterations = []
        self.iterations_without_improvement = 0
    
    def update_solution(self, new_solution: ColoringSolution):
        """Actualiza solución actual y mejor si aplica"""
        self.current_solution = new_solution
        self.evaluations += 1
        
        # Actualizar mejor solución
        if new_solution.num_colors < self.best_value:
            self.best_value = new_solution.num_colors
            self.best_solution = new_solution.copy()
            self.improvement_iterations.append(self.iterations)
            self.iterations_without_improvement = 0
        else:
            self.iterations_without_improvement += 1
    
    def check_stagnation(self, threshold: int = 50) -> bool:
        """Verifica si hay estancamiento"""
        return self.iterations_without_improvement >= threshold
    
    def get_elapsed_time(self) -> float:
        """Obtiene tiempo transcurrido"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def start_timer(self):
        """Inicia cronómetro"""
        self.start_time = time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de ejecución"""
        return {
            'iterations': self.iterations,
            'evaluations': self.evaluations,
            'elapsed_time': self.get_elapsed_time(),
            'best_colors': self.best_value if self.best_solution else None,
            'best_conflicts': self.best_solution.num_conflicts if self.best_solution else None,
            'improvements': len(self.improvement_iterations),
            'final_feasible': self.best_solution.is_feasible(self.problem) if self.best_solution else False
        }


class ASTInterpreter:
    """
    Intérprete/ejecutor de algoritmos ILS representados como AST
    
    Ejecuta la estructura del AST sobre un problema de Graph Coloring
    """
    
    # Mapeo de operadores
    CONSTRUCTIVE_OPS = {
        "DSATUR": GreedyDSATUR,
        "LF": GreedyLF,
        "RandomSequential": RandomSequential
    }
    
    IMPROVEMENT_OPS = {
        "KempeChain": KempeChain,
        "OneVertexMove": OneVertexMove,
        "TabuCol": TabuCol
    }
    
    PERTURBATION_OPS = {
        "RandomRecolor": RandomRecolor,
        "PartialDestroy": PartialDestroy
    }
    
    def __init__(self, 
                 problem: GraphColoringProblem,
                 rng: Optional[np.random.Generator] = None):
        """
        Inicializa intérprete
        
        Args:
            problem: Instancia del problema
            rng: Generador aleatorio
        """
        self.problem = problem
        self.context = ExecutionContext(problem, rng)
        self.rng = self.context.rng
    
    def execute(self, ast: ASTNode) -> ColoringSolution:
        """
        Ejecuta algoritmo representado como AST
        
        Args:
            ast: Árbol sintáctico del algoritmo
        
        Returns:
            Mejor solución encontrada
        """
        self.context.start_timer()
        self._execute_node(ast)
        return self.context.best_solution
    
    def _execute_node(self, node: ASTNode):
        """Ejecuta un nodo del AST"""
        if isinstance(node, GreedyConstruct):
            self._execute_construct(node)
        
        elif isinstance(node, LocalSearch):
            self._execute_improvement(node)
        
        elif isinstance(node, Perturbation):
            self._execute_perturbation(node)
        
        elif isinstance(node, Seq):
            self._execute_seq(node)
        
        elif isinstance(node, While):
            self._execute_while(node)
        
        elif isinstance(node, For):
            self._execute_for(node)
        
        elif isinstance(node, If):
            self._execute_if(node)
        
        elif isinstance(node, Call):
            self._execute_call(node)
    
    def _execute_construct(self, node: GreedyConstruct):
        """Ejecuta construcción greedy"""
        op_class = self.CONSTRUCTIVE_OPS.get(node.heuristic)
        if not op_class:
            return
        
        op = op_class()
        solution = op.construct(self.problem)
        self.context.update_solution(solution)
    
    def _execute_improvement(self, node: LocalSearch):
        """Ejecuta búsqueda local"""
        op_class = self.IMPROVEMENT_OPS.get(node.method)
        if not op_class or not self.context.current_solution:
            return
        
        op = op_class()
        
        # Aplicar mejora iterativa
        best_sol = self.context.current_solution
        for _ in range(node.max_iterations):
            improved_sol = op.improve(best_sol, self.problem)
            if improved_sol.num_colors < best_sol.num_colors:
                best_sol = improved_sol
            else:
                break
        
        self.context.update_solution(best_sol)
    
    def _execute_perturbation(self, node: Perturbation):
        """Ejecuta perturbación"""
        op_class = self.PERTURBATION_OPS.get(node.method)
        if not op_class or not self.context.current_solution:
            return
        
        op = op_class()
        perturbed = op.perturb(
            self.context.current_solution,
            self.problem,
            ratio=node.intensity
        )
        self.context.update_solution(perturbed)
    
    def _execute_seq(self, node: Seq):
        """Ejecuta secuencia"""
        for stmt in node.body:
            self._execute_node(stmt)
    
    def _execute_while(self, node: While):
        """Ejecuta bucle while"""
        max_iter = node.max_iterations
        
        while self.context.iterations < max_iter:
            self.context.iterations += 1
            self._execute_node(node.body)
            
            # Salir si hay estancamiento
            if self.context.check_stagnation():
                break
    
    def _execute_for(self, node: For):
        """Ejecuta bucle for"""
        for i in range(node.iterations):
            self._execute_node(node.body)
    
    def _execute_if(self, node: If):
        """Ejecuta condicional"""
        condition_result = self._evaluate_condition(node.condition)
        
        if condition_result:
            self._execute_node(node.then_branch)
        elif node.else_branch:
            self._execute_node(node.else_branch)
    
    def _evaluate_condition(self, condition: str) -> bool:
        """Evalúa una condición"""
        if condition == "Improves":
            # Último movimiento mejoró
            if len(self.context.improvement_iterations) > 0:
                last_improvement = self.context.improvement_iterations[-1]
                return last_improvement == (self.context.iterations - 1)
            return False
        
        elif condition == "Feasible":
            # Solución actual es factible
            return (self.context.current_solution and 
                    self.context.current_solution.is_feasible(self.context.problem))
        
        elif condition == "Stagnation":
            # Hay estancamiento
            return self.context.check_stagnation(threshold=10)
        
        else:
            return False
    
    def _execute_call(self, node: Call):
        """Ejecuta llamada a operador"""
        # Mapear nombre a operador y ejecutar
        if node.operator in self.IMPROVEMENT_OPS:
            op_class = self.IMPROVEMENT_OPS[node.operator]
            op = op_class()
            if self.context.current_solution:
                improved = op.improve(self.context.current_solution, self.problem)
                self.context.update_solution(improved)


def execute_algorithm(algorithm: ASTNode,
                     problem: GraphColoringProblem,
                     seed: Optional[int] = None) -> ColoringSolution:
    """
    Función de conveniencia para ejecutar un algoritmo
    
    Args:
        algorithm: AST del algoritmo
        problem: Instancia del problema
        seed: Semilla aleatoria
    
    Returns:
        Mejor solución encontrada
    """
    rng = np.random.default_rng(seed)
    interpreter = ASTInterpreter(problem, rng)
    return interpreter.execute(algorithm)
