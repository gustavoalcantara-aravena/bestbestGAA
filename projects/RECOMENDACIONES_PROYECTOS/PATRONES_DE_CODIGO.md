# Patrones de Código: KBP-SA como Referencia

## 📌 Patrones Implementados en KBP-SA

Este documento muestra **patrones de código real** usados en KBP-SA que deberías replicar en otros proyectos.

---

## 1️⃣ Patrón: Clases con @dataclass

### ✅ **Lo que hace KBP-SA**

```python
# core/problem.py
from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class KnapsackProblem:
    """
    Definición del Knapsack Problem (0/1)
    
    Parámetros:
    -----------
    n : int
        Número de ítems
    capacity : int
        Capacidad máxima de la mochila
    values : np.ndarray
        Vector de valores [v1, v2, ..., vn]
    weights : np.ndarray
        Vector de pesos [w1, w2, ..., wn]
    optimal_value : Optional[int]
        Valor óptimo conocido (si existe)
    name : str
        Nombre descriptivo de la instancia
    
    Ejemplo:
    --------
    >>> problem = KnapsackProblem(
    ...     n=5,
    ...     capacity=10,
    ...     values=np.array([1,2,3,4,5]),
    ...     weights=np.array([2,3,4,5,6])
    ... )
    """
    
    n: int
    capacity: int
    values: np.ndarray
    weights: np.ndarray
    optimal_value: Optional[int] = None
    name: str = "KBP"
    
    def __post_init__(self):
        """Validación tras inicialización"""
        # Validar que n sea positivo
        if self.n <= 0:
            raise ValueError(f"n debe ser positivo, recibido: {self.n}")
        
        # Convertir a numpy si es necesario
        if not isinstance(self.values, np.ndarray):
            self.values = np.array(self.values, dtype=int)
        if not isinstance(self.weights, np.ndarray):
            self.weights = np.array(self.weights, dtype=int)
        
        # Validar tamaños coinciden
        if len(self.values) != self.n:
            raise ValueError(
                f"len(values)={len(self.values)} != n={self.n}"
            )
        if len(self.weights) != self.n:
            raise ValueError(
                f"len(weights)={len(self.weights)} != n={self.n}"
            )
        
        # Validar valores no negativos
        if not np.all(self.values >= 0):
            raise ValueError("Todos los valores deben ser >= 0")
        
        # Validar pesos positivos
        if not np.all(self.weights > 0):
            raise ValueError("Todos los pesos deben ser > 0")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnapsackProblem':
        """
        Alternativa: Crear desde diccionario
        
        Ejemplo:
        --------
        >>> data = {
        ...     'n': 5,
        ...     'capacity': 10,
        ...     'values': [1,2,3,4,5],
        ...     'weights': [2,3,4,5,6]
        ... }
        >>> problem = KnapsackProblem.from_dict(data)
        """
        return cls(
            n=data['n'],
            capacity=data['capacity'],
            values=np.array(data['values']),
            weights=np.array(data['weights']),
            optimal_value=data.get('optimal_value'),
            name=data.get('name', 'KBP')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializar a diccionario"""
        return {
            'n': self.n,
            'capacity': self.capacity,
            'values': self.values.tolist(),
            'weights': self.weights.tolist(),
            'optimal_value': self.optimal_value,
            'name': self.name
        }
```

### ❌ **Lo que NO deberías hacer**

```python
# Malo: Clase tradicional sin documentación
class KnapsackProblem:
    def __init__(self, n, capacity, values, weights, optimal=None, name="KBP"):
        self.n = n
        self.capacity = capacity
        self.values = values
        self.weights = weights
        self.optimal = optimal
        self.name = name
        # ¡Sin validaciones!
        # ¡Sin documentación!
```

### **Lecciones**:
- ✅ Usa `@dataclass` para datos simples
- ✅ Documenta en docstring con parámetros, retorno, ejemplo
- ✅ Valida en `__post_init__`
- ✅ Proporciona métodos helper (`from_dict`, `to_dict`)
- ✅ Usa type hints explícitos
- ✅ Valores por defecto sensatos

---

## 2️⃣ Patrón: Strategy Pattern en Operadores

### ✅ **Lo que hace KBP-SA**

```python
# operators/constructive.py
from abc import ABC, abstractmethod
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
import numpy as np

class ConstructiveOperator(ABC):
    """Interfaz base para operadores constructivos"""
    
    @abstractmethod
    def construct(self, problem: KnapsackProblem) -> KnapsackSolution:
        """Construir una solución inicial"""
        pass


class GreedyByValue(ConstructiveOperator):
    """
    Heurística greedy ordenando por valor
    
    Pseudocódigo:
    1. Ordenar ítems por valor descendente
    2. Agregar ítems mientras quepan en la mochila
    
    Complejidad: O(n log n)
    """
    
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Ordenar índices por valor descendente
        sorted_indices = np.argsort(-problem.values)
        
        x = np.zeros(problem.n, dtype=int)
        current_weight = 0
        
        # Agregar ítems greedy
        for idx in sorted_indices:
            if current_weight + problem.weights[idx] <= problem.capacity:
                x[idx] = 1
                current_weight += problem.weights[idx]
        
        return KnapsackSolution(x=x, problem=problem)


class GreedyByWeight(ConstructiveOperator):
    """
    Heurística greedy ordenando por peso
    
    Útil para problemas donde capacidad es restrictiva
    """
    
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Ordenar índices por peso ascendente
        sorted_indices = np.argsort(problem.weights)
        
        x = np.zeros(problem.n, dtype=int)
        current_weight = 0
        
        for idx in sorted_indices:
            if current_weight + problem.weights[idx] <= problem.capacity:
                x[idx] = 1
                current_weight += problem.weights[idx]
        
        return KnapsackSolution(x=x, problem=problem)


class GreedyByRatio(ConstructiveOperator):
    """
    Heurística greedy por ratio valor/peso
    
    Mejor heurística para Knapsack: maximiza eficiencia
    """
    
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        # Calcular ratio valor/peso
        ratios = problem.values / problem.weights
        sorted_indices = np.argsort(-ratios)
        
        x = np.zeros(problem.n, dtype=int)
        current_weight = 0
        
        for idx in sorted_indices:
            if current_weight + problem.weights[idx] <= problem.capacity:
                x[idx] = 1
                current_weight += problem.weights[idx]
        
        return KnapsackSolution(x=x, problem=problem)


class RandomConstruct(ConstructiveOperator):
    """
    Solución aleatoria (para comparación)
    """
    
    @staticmethod
    def construct(problem: KnapsackProblem) -> KnapsackSolution:
        x = np.random.randint(0, 2, size=problem.n)
        solution = KnapsackSolution(x=x, problem=problem)
        
        # Reparar infactibilidad
        while solution.weight > problem.capacity:
            # Remover ítem aleatorio
            valid_indices = np.where(solution.x == 1)[0]
            if len(valid_indices) == 0:
                break
            idx_to_remove = np.random.choice(valid_indices)
            solution.x[idx_to_remove] = 0
        
        return solution


# Uso: Inyección de dependencias
def run_with_constructor(problem, constructor_class):
    """
    Función genérica que funciona con cualquier constructor
    """
    constructor = constructor_class()
    solution = constructor.construct(problem)
    return solution

# Ejemplo:
problem = load_problem('f1.json')
solution1 = run_with_constructor(problem, GreedyByValue)      # ✅ Funciona
solution2 = run_with_constructor(problem, GreedyByRatio)      # ✅ Funciona
solution3 = run_with_constructor(problem, RandomConstruct)    # ✅ Funciona
```

### ❌ **Lo que NO deberías hacer**

```python
# Malo: Hardcodeado, no extensible
def construct_solution(problem, strategy="greedy"):
    if strategy == "greedy":
        # Código de GreedyByValue
        ...
    elif strategy == "weight":
        # Código de GreedyByWeight
        ...
    elif strategy == "ratio":
        # Código de GreedyByRatio
        ...
    else:
        raise ValueError("Estrategia desconocida")
    # ¡Nueva estrategia requiere modificar esta función!
```

### **Lecciones**:
- ✅ Define interfaz base con `ABC` y `@abstractmethod`
- ✅ Cada estrategia = clase separada
- ✅ Fácil agregar nuevas sin tocar código existente (Open/Closed)
- ✅ Usa composición, no condicionales
- ✅ Documenta pseudocódigo y complejidad

---

## 3️⃣ Patrón: Inyección de Dependencias en Metaheurística

### ✅ **Lo que hace KBP-SA**

```python
# metaheuristic/sa_core.py
from typing import Callable, Optional
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
from metaheuristic.cooling_schedules import CoolingSchedule, GeometricCooling
from metaheuristic.acceptance import AcceptanceCriterion, MetropolisCriterion

class SimulatedAnnealing:
    """
    Simulated Annealing con inyección de dependencias
    
    Constructor recibe todas las estrategias inyectadas:
    - cooling_schedule: Cómo disminuye la temperatura
    - acceptance: Criterio de aceptación de movimientos
    - initial_constructor: Cómo crear solución inicial
    - perturbation_operator: Cómo perturbar
    """
    
    def __init__(self,
                 problem: KnapsackProblem,
                 cooling_schedule: CoolingSchedule = None,
                 acceptance: AcceptanceCriterion = None,
                 initial_constructor: Callable = None,
                 perturbation_operator: Callable = None,
                 T0: float = 100.0,
                 alpha: float = 0.95,
                 iterations_per_temp: int = 100,
                 T_min: float = 0.01,
                 max_evaluations: int = 10000,
                 seed: int = None,
                 verbose: bool = False):
        """
        Parámetros:
        -----------
        problem : KnapsackProblem
            Instancia del problema
        cooling_schedule : CoolingSchedule, optional
            Esquema de enfriamiento (default: GeometricCooling)
        acceptance : AcceptanceCriterion, optional
            Criterio de aceptación (default: MetropolisCriterion)
        initial_constructor : Callable, optional
            Función para crear solución inicial
        perturbation_operator : Callable, optional
            Función para perturbar solución
        T0 : float
            Temperatura inicial
        alpha : float
            Factor de enfriamiento (0 < alpha < 1)
        iterations_per_temp : int
            Iteraciones por nivel de temperatura
        T_min : float
            Temperatura mínima
        max_evaluations : int
            Presupuesto máximo de evaluaciones
        seed : int, optional
            Semilla para reproducibilidad
        verbose : bool
            Si imprimir logs durante ejecución
        """
        
        self.problem = problem
        self.evaluator = KnapsackEvaluator()
        
        # Inyectar estrategias con valores por defecto
        self.cooling_schedule = cooling_schedule or GeometricCooling(alpha)
        self.acceptance = acceptance or MetropolisCriterion()
        
        # Inyectar operadores
        if initial_constructor is None:
            from operators.constructive import GreedyByRatio
            initial_constructor = GreedyByRatio.construct
        self.initial_constructor = initial_constructor
        
        if perturbation_operator is None:
            from operators.improvement import FlipBestItem
            perturbation_operator = FlipBestItem.move
        self.perturbation_operator = perturbation_operator
        
        # Parámetros
        self.T0 = T0
        self.alpha = alpha
        self.iterations_per_temp = iterations_per_temp
        self.T_min = T_min
        self.max_evaluations = max_evaluations
        self.seed = seed
        self.verbose = verbose
        
        # Ejecutar cuando se inyecta seed
        if seed is not None:
            np.random.seed(seed)
    
    def run(self) -> Dict[str, Any]:
        """
        Ejecutar Simulated Annealing
        
        Retorna:
        --------
        Dict con claves:
            - solution: mejor solución encontrada
            - best_value: mejor fitness
            - execution_time: tiempo en segundos
            - iterations: número de iteraciones
            - evaluations: número de evaluaciones
            - temperature_history: [T0, T1, T2, ...]
            - best_value_history: [v0, v1, v2, ...]
        """
        
        import time
        start_time = time.time()
        
        # 1. Solución inicial
        current_solution = self.initial_constructor(self.problem)
        best_solution = current_solution.copy()
        
        # Evaluación inicial
        current_value = self.evaluator.evaluate(current_solution)['fitness']
        best_value = current_value
        
        # 2. Historial
        temperature_history = [self.T0]
        best_value_history = [best_value]
        accepted_count = 0
        iteration = 0
        evaluations = 0
        
        # 3. Bucle principal SA
        T = self.T0
        while T > self.T_min and evaluations < self.max_evaluations:
            
            for _ in range(self.iterations_per_temp):
                
                # Generar vecino
                neighbor = self.perturbation_operator(current_solution)
                neighbor_value = self.evaluator.evaluate(neighbor)['fitness']
                evaluations += 1
                
                # Diferencia de energía
                delta_e = neighbor_value - current_value
                
                # Criterio de aceptación (Metropolis)
                if self.acceptance.accept(delta_e, T):
                    current_solution = neighbor
                    current_value = neighbor_value
                    accepted_count += 1
                    
                    # Actualizar mejor solución
                    if current_value > best_value:
                        best_solution = current_solution.copy()
                        best_value = current_value
                
                iteration += 1
                
                if evaluations >= self.max_evaluations:
                    break
            
            # Enfriamiento
            T = self.cooling_schedule.next_temperature(T)
            temperature_history.append(T)
            best_value_history.append(best_value)
            
            if self.verbose:
                acceptance_rate = accepted_count / iteration if iteration > 0 else 0
                print(f"T={T:.4f} | Best={best_value} | "
                      f"Acceptance={acceptance_rate:.2%}")
        
        # 4. Retornar resultados
        execution_time = time.time() - start_time
        
        return {
            'solution': best_solution,
            'best_value': best_value,
            'execution_time': execution_time,
            'iterations': iteration,
            'evaluations': evaluations,
            'acceptance_rate': accepted_count / iteration if iteration > 0 else 0,
            'temperature_history': temperature_history,
            'best_value_history': best_value_history,
        }


# USO: Muy flexible gracias a inyección
from operators.constructive import GreedyByValue, GreedyByRatio
from operators.improvement import FlipBestItem, OneExchange
from metaheuristic.cooling_schedules import LinearCooling, ExponentialCooling
from metaheuristic.acceptance import MetropolisCriterion

problem = load_problem('f1.json')

# Configuración 1: Default
sa1 = SimulatedAnnealing(problem)
result1 = sa1.run()

# Configuración 2: Custom cooling
sa2 = SimulatedAnnealing(
    problem,
    cooling_schedule=LinearCooling(),
    T0=50.0
)
result2 = sa2.run()

# Configuración 3: Custom operators
sa3 = SimulatedAnnealing(
    problem,
    initial_constructor=GreedyByValue.construct,
    perturbation_operator=OneExchange.move,
    cooling_schedule=ExponentialCooling(),
    iterations_per_temp=200
)
result3 = sa3.run()

# ✅ Todas las configuraciones funcionan sin modificar código SA
```

### ❌ **Lo que NO deberías hacer**

```python
# Malo: Todo hardcodeado, sin inyección
class SimulatedAnnealing:
    def __init__(self, problem):
        self.problem = problem
        # Estrategias hardcodeadas
        self.cooling = GeometricCooling(0.95)  # No se puede cambiar
        self.acceptance = MetropolisCriterion()  # No se puede cambiar
        self.initial = GreedyByRatio()  # No se puede cambiar
    
    def run(self):
        # Código que usa siempre las mismas estrategias
        # ¡Para probar otra configuración hay que editar esta clase!
```

### **Lecciones**:
- ✅ Acepta dependencias en constructor
- ✅ Proporciona valores por defecto sensatos
- ✅ Permite cambiar cualquier estrategia sin modificar código
- ✅ Tipo hints para claridad
- ✅ Documentación clara de qué inyecta

---

## 4️⃣ Patrón: Validación con Type Hints y Docstrings

### ✅ **Lo que hace KBP-SA**

```python
# core/evaluation.py
from typing import Dict, Any
import numpy as np
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution

class KnapsackEvaluator:
    """
    Evaluador de soluciones del Knapsack Problem
    
    Calcula múltiples métricas de calidad:
    - fitness: valor total de ítems seleccionados
    - gap: diferencia respecto a óptimo conocido
    - feasibility: si respeta restricciones
    - efficiency: valor/peso promedio
    """
    
    @staticmethod
    def evaluate(solution: KnapsackSolution, 
                 problem: KnapsackProblem = None) -> Dict[str, Any]:
        """
        Evaluar una solución
        
        Parámetros:
        -----------
        solution : KnapsackSolution
            Solución a evaluar. Debe tener atributo x (vector binario)
        problem : KnapsackProblem, optional
            Instancia del problema (si no se pasó en construcción)
        
        Retorna:
        --------
        Dict con claves:
            'fitness' : int
                Valor total de ítems seleccionados
            'weight' : int
                Peso total
            'feasible' : bool
                ¿Respeta capacidad?
            'infeasibility' : int
                Exceso de peso (0 si factible)
            'gap' : float
                (optimal - value) / optimal si se conoce óptimo
            'efficiency' : float
                fitness / weight (ratio valor/peso promedio)
        
        Raises:
        -------
        ValueError
            Si x no es binario o tiene longitud incorrecta
        TypeError
            Si solution o problem tienen tipo incorrecto
        
        Ejemplo:
        --------
        >>> problem = load_problem('f1.json')
        >>> solution = GreedyByRatio.construct(problem)
        >>> metrics = KnapsackEvaluator.evaluate(solution, problem)
        >>> print(f"Fitness: {metrics['fitness']}, Factible: {metrics['feasible']}")
        Fitness: 45, Factible: True
        """
        
        # Validación de tipos
        if not isinstance(solution, KnapsackSolution):
            raise TypeError(f"solution debe ser KnapsackSolution, "
                          f"recibido {type(solution)}")
        
        if problem is None:
            problem = solution.problem
        
        if not isinstance(problem, KnapsackProblem):
            raise TypeError(f"problem debe ser KnapsackProblem, "
                          f"recibido {type(problem)}")
        
        # Validación de x
        if len(solution.x) != problem.n:
            raise ValueError(f"len(x)={len(solution.x)} != n={problem.n}")
        
        if not all(xi in [0, 1] for xi in solution.x):
            raise ValueError(f"x debe ser binario [0,1]*, recibido {solution.x}")
        
        # Calcular fitness
        fitness = np.sum(solution.x * problem.values)
        weight = np.sum(solution.x * problem.weights)
        
        # Verificar factibilidad
        feasible = weight <= problem.capacity
        infeasibility = max(0, weight - problem.capacity)
        
        # Calcular gap respecto a óptimo
        gap = None
        if problem.optimal_value is not None:
            gap = (problem.optimal_value - fitness) / problem.optimal_value
        
        # Calcular eficiencia
        efficiency = fitness / weight if weight > 0 else 0
        
        return {
            'fitness': fitness,
            'weight': weight,
            'feasible': feasible,
            'infeasibility': infeasibility,
            'gap': gap,
            'efficiency': efficiency
        }
    
    @staticmethod
    def batch_evaluate(solutions: list[KnapsackSolution],
                       problem: KnapsackProblem) -> list[Dict[str, Any]]:
        """
        Evaluar múltiples soluciones
        
        Parámetros:
        -----------
        solutions : list[KnapsackSolution]
            Lista de soluciones
        problem : KnapsackProblem
            Instancia del problema
        
        Retorna:
        --------
        list[Dict[str, Any]]
            Lista de métricas (una por solución)
        
        Ejemplo:
        --------
        >>> solutions = [algorithm.run() for _ in range(10)]
        >>> metrics_list = KnapsackEvaluator.batch_evaluate(solutions, problem)
        """
        
        if not isinstance(solutions, list):
            raise TypeError(f"solutions debe ser list, recibido {type(solutions)}")
        
        return [KnapsackEvaluator.evaluate(sol, problem) for sol in solutions]
```

### ❌ **Lo que NO deberías hacer**

```python
# Malo: Sin validación, sin tipos, sin documentación
class Evaluator:
    def evaluate(self, sol, prob):
        fitness = sum(sol.x * prob.values)
        weight = sum(sol.x * prob.weights)
        gap = prob.optimal - fitness if prob.optimal else None
        return {
            'fitness': fitness,
            'weight': weight,
            'gap': gap
        }
        # ¡Qué pasa si x no es binario? ¡Qué pasa si lengths no coinciden?
```

### **Lecciones**:
- ✅ Type hints en todos los parámetros y retorno
- ✅ Docstring con Parámetros, Retorna, Raises, Ejemplo
- ✅ Valida tipos explícitamente
- ✅ Valida contenido (binario, longitudes, valores)
- ✅ Proporciona ejemplos ejecutables en docstring

---

## 5️⃣ Patrón: Configuración Centralizada con Config.yaml

### ✅ **Lo que hace KBP-SA**

```yaml
# config/config.yaml
project:
  name: "KBP-SA"
  version: "1.0.0"
  description: "Knapsack Problem + Simulated Annealing"

problem:
  type: "knapsack"
  optimization: "maximize"

metaheuristic:
  name: "Simulated Annealing"
  
  parameters:
    T0: 100.0                    # Temperatura inicial
    alpha: 0.95                  # Factor de enfriamiento
    iterations_per_temp: 100     # Iteraciones por temperatura
    T_min: 0.01                  # Temperatura mínima
    max_evaluations: 10000       # Máximo de evaluaciones
    seed: 42                      # Para reproducibilidad

gaa:
  max_depth: 5
  population_size: 50
  n_generations: 100

datasets:
  low_dimensional:
    path: "datasets/low_dimensional/"
    sizes: [4, 11, 20, 23]
  large_scale:
    path: "datasets/large_scale/"
    sizes: [100, 500, 1000, 10000]

visualization:
  output_dir: "output/"
  formats: ["png", "pdf"]
  dpi: 300
```

```python
# utils/config.py
from pathlib import Path
import yaml
from typing import Dict, Any

class ConfigManager:
    """Gestión centralizada de configuración"""
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Parámetros:
        -----------
        config_path : str
            Ruta al archivo YAML de configuración
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde YAML"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default=None) -> Any:
        """
        Obtener valor de configuración
        
        Soporta notación de punto: 'metaheuristic.parameters.T0'
        
        Ejemplo:
        --------
        >>> config = ConfigManager()
        >>> T0 = config.get('metaheuristic.parameters.T0')  # 100.0
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def get_sa_params(self) -> Dict[str, Any]:
        """Obtener todos los parámetros de SA"""
        return self.config['metaheuristic']['parameters']
    
    def get_gaa_params(self) -> Dict[str, Any]:
        """Obtener todos los parámetros de GAA"""
        return self.config['gaa']
    
    def get_datasets_path(self, category: str = 'low_dimensional') -> Path:
        """Obtener ruta a datasets"""
        return Path(self.config['datasets'][category]['path'])

# USO: Centralizado
config = ConfigManager()

# Obtener parámetros específicos
T0 = config.get('metaheuristic.parameters.T0')
alpha = config.get('metaheuristic.parameters.alpha')
seed = config.get('metaheuristic.parameters.seed')

# Crear SA con parámetros de config
sa = SimulatedAnnealing(
    problem,
    T0=T0,
    alpha=alpha,
    **config.get_sa_params()
)

# Obtener rutas de datasets
datasets_path = config.get_datasets_path('low_dimensional')

# Obtener directorio de salida
output_dir = config.get('visualization.output_dir')
```

### ❌ **Lo que NO deberías hacer**

```python
# Malo: Parámetros hardcodeados en código
class SimulatedAnnealing:
    def __init__(self, problem):
        self.T0 = 100.0  # Hardcodeado
        self.alpha = 0.95  # Hardcodeado
        self.iterations_per_temp = 100  # Hardcodeado
        # ¡Para cambiar parámetro hay que editar código!

# Uso:
sa = SimulatedAnnealing(problem)  # No hay forma de cambiar parámetros
```

### **Lecciones**:
- ✅ Centraliza TODOS los parámetros en config.yaml
- ✅ Proporciona `ConfigManager` para acceso fácil
- ✅ Soporta notación de punto para acceso anidado
- ✅ Métodos helper para categorías comunes
- ✅ Sin parámetros hardcodeados en código

---

## 6️⃣ Patrón: Logging Detallado

### ✅ **Lo que hace KBP-SA**

```python
# utils/logging_util.py
import logging
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, 
                 output_dir: str = 'output',
                 level = logging.INFO) -> logging.Logger:
    """
    Configurar logger con archivo y consola
    
    Parámetros:
    -----------
    name : str
        Nombre del logger (usualmente __name__)
    output_dir : str
        Directorio para archivos de log
    level : int
        Nivel de logging (DEBUG, INFO, WARNING, ERROR)
    
    Retorna:
    --------
    Logger configurado
    
    Ejemplo:
    --------
    >>> logger = setup_logger(__name__)
    >>> logger.info("Iniciando SA")
    >>> logger.debug(f"Temperatura: {T:.4f}")
    """
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Crear directorio de logs
    log_dir = Path(output_dir) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Formato detallado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para consola (solo INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# USO en métodos
import numpy as np

class SimulatedAnnealing:
    def __init__(self, problem, verbose=False):
        self.problem = problem
        self.logger = setup_logger(__name__) if verbose else logging.getLogger(__name__)
    
    def run(self):
        self.logger.info(f"Iniciando SA para problema {self.problem.name}")
        self.logger.debug(f"n={self.problem.n}, capacity={self.problem.capacity}")
        
        T = self.T0
        iteration = 0
        
        while T > self.T_min:
            # ... código SA ...
            
            for i in range(self.iterations_per_temp):
                delta_e = self.evaluator.evaluate(neighbor) - current
                prob_accept = np.exp(-delta_e / T) if delta_e > 0 else 1.0
                
                if self.accept(delta_e, T):
                    self.logger.debug(
                        f"Iter {iteration}: T={T:.4f}, ΔE={delta_e:.2f}, "
                        f"P={prob_accept:.4f}, Aceptada"
                    )
                
                iteration += 1
            
            T *= self.alpha
            self.logger.info(f"Iteración {iteration}, T={T:.4f}")
        
        self.logger.info(f"SA terminado. Mejor valor: {best_value}")
```

### **Lecciones**:
- ✅ Logging a archivo Y consola
- ✅ Timestamps automáticos
- ✅ Múltiples niveles (DEBUG, INFO, WARNING)
- ✅ Incluye valores durante ejecución
- ✅ Facilita debugging y auditoría

---

## 📋 Resumen de Patrones

| Patrón | Dónde Usarlo | Beneficio |
|--------|-------------|----------|
| **@dataclass** | Clases de datos simples | Menos código, serialización automática |
| **Strategy Pattern** | Operadores/algoritmos | Extensible sin modificar código |
| **Inyección de Dependencias** | Clase principal | Máxima flexibilidad |
| **Type Hints + Docstrings** | Todas partes | IDE autocomplete + documentación |
| **Config.yaml** | Parámetros globales | Cambios sin recompilar |
| **Logging detallado** | Durante ejecución | Debugging y auditoría |

Usa estos patrones **como base** para tus propios proyectos.

