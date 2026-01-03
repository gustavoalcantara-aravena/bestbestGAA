# Guía de Implementación - Solomon VRPTW Dataset

## Tabla de Contenidos
1. [Configuración del Entorno](#configuración-del-entorno)
2. [Lectura y Procesamiento de Datos](#lectura-y-procesamiento-de-datos)
3. [Estructuras de Datos Recomendadas](#estructuras-de-datos-recomendadas)
4. [Funciones Auxiliares](#funciones-auxiliares)
5. [Implementación de Algoritmos Básicos](#implementación-de-algoritmos-básicos)
6. [Validación y Evaluación](#validación-y-evaluación)
7. [Visualización](#visualización)
8. [Ejemplos Completos](#ejemplos-completos)

---

## Configuración del Entorno

### Dependencias Recomendadas

```bash
# Instalación con pip
pip install numpy pandas matplotlib scipy networkx

# O usando conda
conda install numpy pandas matplotlib scipy networkx
```

### Estructura de Proyecto Sugerida

```
proyecto_vrptw/
│
├── data/
│   ├── C1/
│   ├── C2/
│   ├── R1/
│   ├── R2/
│   ├── RC1/
│   └── RC2/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Lectura de datos
│   ├── models.py            # Clases y estructuras
│   ├── algorithms.py        # Algoritmos de solución
│   ├── validators.py        # Validación de soluciones
│   └── visualizer.py        # Visualización
│
├── tests/
│   ├── test_loader.py
│   ├── test_algorithms.py
│   └── test_validators.py
│
├── results/
│   └── solutions/
│
└── main.py
```

---

## Lectura y Procesamiento de Datos

### Clase para Cargar Instancias

```python
# data_loader.py

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

class SolomonInstanceLoader:
    """Cargador de instancias Solomon VRPTW"""
    
    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Directorio raíz del dataset
        """
        self.data_dir = Path(data_dir)
        
    def load_instance(self, instance_name: str) -> Dict:
        """
        Carga una instancia específica
        
        Args:
            instance_name: Nombre de la instancia (ej: 'C101', 'R201')
            
        Returns:
            Diccionario con datos de la instancia
        """
        # Determinar subdirectorio
        if instance_name.startswith('C1'):
            subdir = 'C1'
        elif instance_name.startswith('C2'):
            subdir = 'C2'
        elif instance_name.startswith('R1'):
            subdir = 'R1'
        elif instance_name.startswith('R2'):
            subdir = 'R2'
        elif instance_name.startswith('RC1'):
            subdir = 'RC1'
        elif instance_name.startswith('RC2'):
            subdir = 'RC2'
        else:
            raise ValueError(f"Nombre de instancia inválido: {instance_name}")
        
        # Construir ruta del archivo
        file_path = self.data_dir / subdir / f"{instance_name}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Leer CSV
        df = pd.read_csv(file_path)
        
        # Extraer depósito (primera fila)
        depot = df.iloc[0].to_dict()
        
        # Extraer clientes (resto de filas)
        customers = df.iloc[1:].to_dict('records')
        
        # Determinar capacidad del vehículo según tipo
        vehicle_capacity = self._get_vehicle_capacity(instance_name)
        
        # Calcular matriz de distancias
        distance_matrix = self._compute_distance_matrix(depot, customers)
        
        return {
            'name': instance_name,
            'type': subdir,
            'depot': depot,
            'customers': customers,
            'num_customers': len(customers),
            'vehicle_capacity': vehicle_capacity,
            'distance_matrix': distance_matrix
        }
    
    def _get_vehicle_capacity(self, instance_name: str) -> int:
        """Determina la capacidad del vehículo según el tipo de instancia"""
        if instance_name.startswith('C1'):
            return 200
        elif instance_name.startswith('C2'):
            return 700
        elif instance_name.startswith('R1'):
            return 200
        elif instance_name.startswith('R2'):
            return 1000
        elif instance_name.startswith('RC1'):
            return 200
        elif instance_name.startswith('RC2'):
            return 1000
        else:
            return 200  # Default
    
    def _compute_distance_matrix(self, depot: Dict, customers: List[Dict]) -> np.ndarray:
        """
        Calcula matriz de distancias euclidianas
        
        Returns:
            Matriz (n+1) x (n+1) donde n es el número de clientes
            Índice 0 = depósito, índices 1-n = clientes
        """
        all_nodes = [depot] + customers
        n = len(all_nodes)
        
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = all_nodes[i]['XCOORD.'] - all_nodes[j]['XCOORD.']
                    dy = all_nodes[i]['YCOORD.'] - all_nodes[j]['YCOORD.']
                    distance_matrix[i][j] = np.sqrt(dx**2 + dy**2)
        
        return distance_matrix
    
    def load_all_instances(self, instance_type: str = None) -> Dict[str, Dict]:
        """
        Carga todas las instancias de un tipo específico o todas
        
        Args:
            instance_type: 'C1', 'C2', 'R1', 'R2', 'RC1', 'RC2' o None para todas
            
        Returns:
            Diccionario con todas las instancias cargadas
        """
        instances = {}
        
        if instance_type:
            subdirs = [instance_type]
        else:
            subdirs = ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']
        
        for subdir in subdirs:
            subdir_path = self.data_dir / subdir
            if subdir_path.exists():
                for csv_file in subdir_path.glob('*.csv'):
                    instance_name = csv_file.stem
                    try:
                        instances[instance_name] = self.load_instance(instance_name)
                        print(f"✓ Cargada: {instance_name}")
                    except Exception as e:
                        print(f"✗ Error al cargar {instance_name}: {e}")
        
        return instances
```

### Ejemplo de Uso del Loader

```python
# Ejemplo de uso
loader = SolomonInstanceLoader('data')

# Cargar una instancia específica
instance = loader.load_instance('C101')

print(f"Instancia: {instance['name']}")
print(f"Tipo: {instance['type']}")
print(f"Número de clientes: {instance['num_customers']}")
print(f"Capacidad del vehículo: {instance['vehicle_capacity']}")
print(f"\nDepósito: {instance['depot']}")
print(f"\nPrimer cliente: {instance['customers'][0]}")
```

---

## Estructuras de Datos Recomendadas

### Clases del Modelo

```python
# models.py

from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class Node:
    """Representa un nodo (depósito o cliente)"""
    id: int
    x: float
    y: float
    demand: int
    ready_time: float
    due_date: float
    service_time: float
    
    def __repr__(self):
        return f"Node({self.id}, pos=({self.x},{self.y}), demand={self.demand})"

@dataclass
class Route:
    """Representa una ruta de un vehículo"""
    nodes: List[Node]
    depot: Node
    
    def __post_init__(self):
        self.distance = 0.0
        self.load = 0
        self.total_time = 0.0
        self.waiting_time = 0.0
        self.is_feasible = True
        self.violations = []
    
    def add_node(self, node: Node, position: Optional[int] = None):
        """Añade un nodo a la ruta"""
        if position is None:
            self.nodes.append(node)
        else:
            self.nodes.insert(position, node)
    
    def remove_node(self, position: int) -> Node:
        """Elimina y retorna un nodo de la ruta"""
        return self.nodes.pop(position)
    
    def calculate_metrics(self, distance_matrix: np.ndarray):
        """Calcula métricas de la ruta"""
        if not self.nodes:
            return
        
        self.distance = 0.0
        self.load = 0
        self.total_time = 0.0
        self.waiting_time = 0.0
        
        # Depósito -> Primer cliente
        current_node = self.depot
        current_time = 0.0
        
        for node in self.nodes:
            # Calcular distancia
            travel_distance = distance_matrix[current_node.id][node.id]
            self.distance += travel_distance
            
            # Calcular tiempo de llegada
            arrival_time = current_time + travel_distance
            
            # Verificar ventana de tiempo
            if arrival_time > node.due_date:
                self.is_feasible = False
                self.violations.append(f"Llegada tardía al nodo {node.id}")
            
            # Calcular tiempo de inicio de servicio
            service_start = max(arrival_time, node.ready_time)
            
            # Acumular tiempo de espera
            if service_start > arrival_time:
                self.waiting_time += (service_start - arrival_time)
            
            # Actualizar tiempo actual
            current_time = service_start + node.service_time
            
            # Acumular carga
            self.load += node.demand
            
            current_node = node
        
        # Último cliente -> Depósito
        travel_distance = distance_matrix[current_node.id][self.depot.id]
        self.distance += travel_distance
        self.total_time = current_time + travel_distance
        
        # Verificar regreso al depósito
        if self.total_time > self.depot.due_date:
            self.is_feasible = False
            self.violations.append("Regreso tardío al depósito")
    
    def __len__(self):
        return len(self.nodes)
    
    def __repr__(self):
        node_ids = [n.id for n in self.nodes]
        return f"Route({self.depot.id} -> {node_ids} -> {self.depot.id}, dist={self.distance:.2f})"

@dataclass
class Solution:
    """Representa una solución completa al VRPTW"""
    routes: List[Route]
    instance_name: str
    
    def __post_init__(self):
        self.num_vehicles = len(self.routes)
        self.total_distance = 0.0
        self.total_time = 0.0
        self.is_feasible = True
        self.violations = []
    
    def calculate_metrics(self, distance_matrix: np.ndarray, vehicle_capacity: int):
        """Calcula métricas de la solución"""
        self.total_distance = 0.0
        self.total_time = 0.0
        self.is_feasible = True
        self.violations = []
        
        for i, route in enumerate(self.routes):
            route.calculate_metrics(distance_matrix)
            
            self.total_distance += route.distance
            self.total_time += route.total_time
            
            # Verificar capacidad
            if route.load > vehicle_capacity:
                self.is_feasible = False
                self.violations.append(
                    f"Ruta {i}: Capacidad excedida ({route.load} > {vehicle_capacity})"
                )
            
            # Verificar factibilidad de la ruta
            if not route.is_feasible:
                self.is_feasible = False
                self.violations.extend([f"Ruta {i}: {v}" for v in route.violations])
    
    def get_objective_value(self, alpha: float = 1000.0, beta: float = 1.0) -> float:
        """
        Calcula valor objetivo jerárquico
        
        Args:
            alpha: Peso para número de vehículos
            beta: Peso para distancia total
            
        Returns:
            Valor objetivo (menor es mejor)
        """
        return alpha * self.num_vehicles + beta * self.total_distance
    
    def __repr__(self):
        return (f"Solution({self.instance_name}, "
                f"vehicles={self.num_vehicles}, "
                f"distance={self.total_distance:.2f}, "
                f"feasible={self.is_feasible})")
```

---

## Funciones Auxiliares

### Utilidades Generales

```python
# utils.py

import numpy as np
from typing import List, Tuple
from models import Node

def euclidean_distance(node1: Node, node2: Node) -> float:
    """Calcula distancia euclidiana entre dos nodos"""
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    return np.sqrt(dx**2 + dy**2)

def create_nodes_from_instance(instance: dict) -> Tuple[Node, List[Node]]:
    """
    Convierte datos de instancia en objetos Node
    
    Returns:
        (depot, customers): Tupla con depósito y lista de clientes
    """
    # Crear depósito
    depot_data = instance['depot']
    depot = Node(
        id=0,  # Siempre ID 0 para el depósito
        x=depot_data['XCOORD.'],
        y=depot_data['YCOORD.'],
        demand=depot_data['DEMAND'],
        ready_time=depot_data['READY TIME'],
        due_date=depot_data['DUE DATE'],
        service_time=depot_data['SERVICE TIME']
    )
    
    # Crear clientes
    customers = []
    for i, customer_data in enumerate(instance['customers'], start=1):
        customer = Node(
            id=i,
            x=customer_data['XCOORD.'],
            y=customer_data['YCOORD.'],
            demand=customer_data['DEMAND'],
            ready_time=customer_data['READY TIME'],
            due_date=customer_data['DUE DATE'],
            service_time=customer_data['SERVICE TIME']
        )
        customers.append(customer)
    
    return depot, customers

def calculate_route_distance(route: List[int], distance_matrix: np.ndarray) -> float:
    """
    Calcula distancia total de una ruta
    
    Args:
        route: Lista de IDs de nodos (incluyendo depósito al inicio y fin)
        distance_matrix: Matriz de distancias
        
    Returns:
        Distancia total
    """
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i+1]]
    return total_distance

def is_route_feasible(route: List[Node], depot: Node, 
                      distance_matrix: np.ndarray,
                      vehicle_capacity: int) -> Tuple[bool, List[str]]:
    """
    Verifica si una ruta es factible
    
    Returns:
        (is_feasible, violations): Tupla con resultado y lista de violaciones
    """
    violations = []
    current_time = 0.0
    current_load = 0
    current_node = depot
    
    for node in route:
        # Verificar capacidad
        current_load += node.demand
        if current_load > vehicle_capacity:
            violations.append(f"Capacidad excedida: {current_load} > {vehicle_capacity}")
        
        # Calcular tiempo de viaje
        travel_time = distance_matrix[current_node.id][node.id]
        arrival_time = current_time + travel_time
        
        # Verificar ventana de tiempo
        if arrival_time > node.due_date:
            violations.append(
                f"Nodo {node.id}: Llegada tardía ({arrival_time:.2f} > {node.due_date})"
            )
        
        # Calcular tiempo de inicio de servicio
        service_start = max(arrival_time, node.ready_time)
        current_time = service_start + node.service_time
        current_node = node
    
    # Verificar regreso al depósito
    travel_time = distance_matrix[current_node.id][depot.id]
    arrival_time = current_time + travel_time
    
    if arrival_time > depot.due_date:
        violations.append(
            f"Regreso tardío al depósito ({arrival_time:.2f} > {depot.due_date})"
        )
    
    is_feasible = len(violations) == 0
    return is_feasible, violations

def calculate_savings(i: int, j: int, depot: Node, 
                      customers: List[Node],
                      distance_matrix: np.ndarray) -> float:
    """
    Calcula el ahorro de Clarke-Wright para combinar dos clientes
    
    Savings = d(depot, i) + d(depot, j) - d(i, j)
    """
    depot_id = depot.id
    return (distance_matrix[depot_id][i] + 
            distance_matrix[depot_id][j] - 
            distance_matrix[i][j])
```

---

## Implementación de Algoritmos Básicos

### Algoritmo Nearest Neighbor

```python
# algorithms.py

import numpy as np
from typing import List, Set
from models import Node, Route, Solution

class NearestNeighborVRPTW:
    """Algoritmo del vecino más cercano para VRPTW"""
    
    def __init__(self, depot: Node, customers: List[Node],
                 distance_matrix: np.ndarray, vehicle_capacity: int):
        self.depot = depot
        self.customers = customers
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
    
    def solve(self) -> Solution:
        """
        Resuelve el VRPTW usando vecino más cercano
        
        Returns:
            Solución construida
        """
        unvisited = set(range(len(self.customers)))
        routes = []
        
        while unvisited:
            route = self._construct_route(unvisited)
            if route:
                routes.append(route)
            else:
                # Si no se puede construir ruta, forzar inclusión
                # (puede resultar en solución infactible)
                remaining_node = self.customers[list(unvisited)[0]]
                route = Route([remaining_node], self.depot)
                routes.append(route)
                unvisited.remove(list(unvisited)[0])
        
        solution = Solution(routes, "NearestNeighbor")
        solution.calculate_metrics(self.distance_matrix, self.vehicle_capacity)
        
        return solution
    
    def _construct_route(self, unvisited: Set[int]) -> Route:
        """Construye una ruta usando vecino más cercano"""
        route_nodes = []
        current_node = self.depot
        current_time = 0.0
        current_load = 0
        
        while unvisited:
            # Encontrar cliente más cercano factible
            best_customer = None
            best_distance = float('inf')
            best_idx = None
            
            for idx in unvisited:
                customer = self.customers[idx]
                
                # Verificar capacidad
                if current_load + customer.demand > self.vehicle_capacity:
                    continue
                
                # Calcular tiempo de llegada
                travel_distance = self.distance_matrix[current_node.id][customer.id]
                arrival_time = current_time + travel_distance
                
                # Verificar ventana de tiempo
                if arrival_time > customer.due_date:
                    continue
                
                # Seleccionar el más cercano
                if travel_distance < best_distance:
                    best_distance = travel_distance
                    best_customer = customer
                    best_idx = idx
            
            # Si no hay cliente factible, terminar ruta
            if best_customer is None:
                break
            
            # Añadir cliente a la ruta
            route_nodes.append(best_customer)
            unvisited.remove(best_idx)
            
            # Actualizar estado
            travel_distance = self.distance_matrix[current_node.id][best_customer.id]
            arrival_time = current_time + travel_distance
            service_start = max(arrival_time, best_customer.ready_time)
            current_time = service_start + best_customer.service_time
            current_load += best_customer.demand
            current_node = best_customer
        
        if route_nodes:
            return Route(route_nodes, self.depot)
        else:
            return None
```

### Algoritmo Clarke-Wright Savings

```python
class ClarkeWrightVRPTW:
    """Algoritmo de ahorros de Clarke-Wright para VRPTW"""
    
    def __init__(self, depot: Node, customers: List[Node],
                 distance_matrix: np.ndarray, vehicle_capacity: int):
        self.depot = depot
        self.customers = customers
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
    
    def solve(self) -> Solution:
        """Resuelve el VRPTW usando Clarke-Wright"""
        # Paso 1: Crear rutas individuales para cada cliente
        routes = []
        for customer in self.customers:
            route = Route([customer], self.depot)
            routes.append(route)
        
        # Paso 2: Calcular ahorros para todos los pares
        savings = []
        n = len(self.customers)
        
        for i in range(n):
            for j in range(i + 1, n):
                saving = self._calculate_saving(i, j)
                savings.append((saving, i, j))
        
        # Ordenar ahorros en orden descendente
        savings.sort(reverse=True, key=lambda x: x[0])
        
        # Paso 3: Fusionar rutas según ahorros
        for saving_value, i, j in savings:
            # Encontrar rutas que contienen i y j
            route_i = None
            route_j = None
            
            for route in routes:
                if any(node.id == self.customers[i].id for node in route.nodes):
                    route_i = route
                if any(node.id == self.customers[j].id for node in route.nodes):
                    route_j = route
            
            # Si están en rutas diferentes, intentar fusionar
            if route_i and route_j and route_i != route_j:
                if self._can_merge(route_i, route_j):
                    # Fusionar rutas
                    merged_route = self._merge_routes(route_i, route_j, i, j)
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append(merged_route)
        
        solution = Solution(routes, "ClarkeWright")
        solution.calculate_metrics(self.distance_matrix, self.vehicle_capacity)
        
        return solution
    
    def _calculate_saving(self, i: int, j: int) -> float:
        """Calcula ahorro de fusionar clientes i y j"""
        depot_id = self.depot.id
        customer_i_id = self.customers[i].id
        customer_j_id = self.customers[j].id
        
        return (self.distance_matrix[depot_id][customer_i_id] +
                self.distance_matrix[depot_id][customer_j_id] -
                self.distance_matrix[customer_i_id][customer_j_id])
    
    def _can_merge(self, route1: Route, route2: Route) -> bool:
        """Verifica si dos rutas pueden fusionarse"""
        # Verificar capacidad
        total_load = route1.load + route2.load
        if total_load > self.vehicle_capacity:
            return False
        
        return True
    
    def _merge_routes(self, route1: Route, route2: Route, i: int, j: int) -> Route:
        """Fusiona dos rutas"""
        # Simplificación: concatenar nodos
        merged_nodes = route1.nodes + route2.nodes
        return Route(merged_nodes, self.depot)
```

---

## Validación y Evaluación

### Validador de Soluciones

```python
# validators.py

from typing import List, Tuple
from models import Solution, Node
import numpy as np

class SolutionValidator:
    """Valida soluciones del VRPTW"""
    
    def __init__(self, depot: Node, customers: List[Node],
                 distance_matrix: np.ndarray, vehicle_capacity: int):
        self.depot = depot
        self.customers = customers
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
    
    def validate(self, solution: Solution) -> Tuple[bool, List[str]]:
        """
        Valida una solución completa
        
        Returns:
            (is_valid, violations): Tupla con resultado y violaciones
        """
        violations = []
        
        # 1. Verificar que todos los clientes sean visitados
        visited_customers = set()
        for route in solution.routes:
            for node in route.nodes:
                if node.id in visited_customers:
                    violations.append(f"Cliente {node.id} visitado múltiples veces")
                visited_customers.add(node.id)
        
        all_customer_ids = set(c.id for c in self.customers)
        missing_customers = all_customer_ids - visited_customers
        if missing_customers:
            violations.append(f"Clientes no visitados: {missing_customers}")
        
        # 2. Validar cada ruta individualmente
        for i, route in enumerate(solution.routes):
            route_violations = self._validate_route(route)
            if route_violations:
                violations.extend([f"Ruta {i}: {v}" for v in route_violations])
        
        is_valid = len(violations) == 0
        return is_valid, violations
    
    def _validate_route(self, route: Route) -> List[str]:
        """Valida una ruta individual"""
        violations = []
        
        if not route.nodes:
            return violations
        
        current_time = 0.0
        current_load = 0
        current_node = self.depot
        
        for node in route.nodes:
            # Verificar capacidad
            current_load += node.demand
            if current_load > self.vehicle_capacity:
                violations.append(
                    f"Capacidad excedida: {current_load} > {self.vehicle_capacity}"
                )
            
            # Calcular tiempo de llegada
            travel_time = self.distance_matrix[current_node.id][node.id]
            arrival_time = current_time + travel_time
            
            # Verificar ventana de tiempo
            if arrival_time > node.due_date:
                violations.append(
                    f"Nodo {node.id}: Llegada tardía "
                    f"({arrival_time:.2f} > {node.due_date})"
                )
            
            # Actualizar tiempo
            service_start = max(arrival_time, node.ready_time)
            current_time = service_start + node.service_time
            current_node = node
        
        # Verificar regreso al depósito
        travel_time = self.distance_matrix[current_node.id][self.depot.id]
        arrival_time = current_time + travel_time
        
        if arrival_time > self.depot.due_date:
            violations.append(
                f"Regreso tardío al depósito "
                f"({arrival_time:.2f} > {self.depot.due_date})"
            )
        
        return violations

def print_solution_report(solution: Solution, validator: SolutionValidator):
    """Imprime reporte detallado de una solución"""
    print("=" * 70)
    print(f"REPORTE DE SOLUCIÓN: {solution.instance_name}")
    print("=" * 70)
    
    print(f"\nMétricas Generales:")
    print(f"  Número de vehículos: {solution.num_vehicles}")
    print(f"  Distancia total: {solution.total_distance:.2f}")
    print(f"  Tiempo total: {solution.total_time:.2f}")
    print(f"  Factible: {'SÍ' if solution.is_feasible else 'NO'}")
    
    if not solution.is_feasible:
        print(f"\n  Violaciones:")
        for violation in solution.violations:
            print(f"    - {violation}")
    
    print(f"\nDetalle de Rutas:")
    for i, route in enumerate(solution.routes, 1):
        node_ids = [n.id for n in route.nodes]
        print(f"\n  Ruta {i}:")
        print(f"    Secuencia: {route.depot.id} -> {node_ids} -> {route.depot.id}")
        print(f"    Clientes: {len(route.nodes)}")
        print(f"    Distancia: {route.distance:.2f}")
        print(f"    Carga: {route.load}")
        print(f"    Tiempo total: {route.total_time:.2f}")
        print(f"    Tiempo de espera: {route.waiting_time:.2f}")
        print(f"    Factible: {'SÍ' if route.is_feasible else 'NO'}")
        
        if not route.is_feasible:
            print(f"    Violaciones:")
            for violation in route.violations:
                print(f"      - {violation}")
    
    # Validación adicional
    is_valid, violations = validator.validate(solution)
    print(f"\nValidación Completa: {'VÁLIDA' if is_valid else 'INVÁLIDA'}")
    if not is_valid:
        print(f"Violaciones detectadas:")
        for violation in violations:
            print(f"  - {violation}")
    
    print("=" * 70)
```

---

## Visualización

### Visualizador de Soluciones

```python
# visualizer.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import numpy as np
from typing import List
from models import Solution, Node

class VRPTWVisualizer:
    """Visualizador para instancias y soluciones VRPTW"""
    
    def __init__(self, figsize=(14, 10)):
        self.figsize = figsize
        self.colors = plt.cm.tab20.colors
    
    def plot_instance(self, depot: Node, customers: List[Node], 
                      title: str = "Instancia VRPTW"):
        """Visualiza una instancia sin solución"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plotear depósito
        ax.scatter(depot.x, depot.y, c='red', s=300, marker='s',
                  edgecolors='black', linewidths=2, zorder=5,
                  label='Depósito')
        
        # Plotear clientes
        customer_x = [c.x for c in customers]
        customer_y = [c.y for c in customers]
        ax.scatter(customer_x, customer_y, c='blue', s=100,
                  edgecolors='black', linewidths=1, zorder=3,
                  label='Clientes')
        
        # Añadir IDs de clientes
        for customer in customers:
            ax.annotate(str(customer.id), (customer.x, customer.y),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.7)
        
        ax.set_xlabel('Coordenada X', fontsize=12)
        ax.set_ylabel('Coordenada Y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        return fig, ax
    
    def plot_solution(self, solution: Solution, depot: Node,
                      customers: List[Node], title: str = None):
        """Visualiza una solución completa"""
        if title is None:
            title = f"Solución {solution.instance_name}"
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plotear depósito
        ax.scatter(depot.x, depot.y, c='red', s=300, marker='s',
                  edgecolors='black', linewidths=2, zorder=5,
                  label='Depósito')
        
        # Plotear clientes
        customer_x = [c.x for c in customers]
        customer_y = [c.y for c in customers]
        ax.scatter(customer_x, customer_y, c='lightgray', s=100,
                  edgecolors='black', linewidths=1, zorder=3)
        
        # Plotear rutas
        for i, route in enumerate(solution.routes):
            color = self.colors[i % len(self.colors)]
            
            # Construir secuencia de puntos
            route_x = [depot.x]
            route_y = [depot.y]
            
            for node in route.nodes:
                route_x.append(node.x)
                route_y.append(node.y)
            
            route_x.append(depot.x)
            route_y.append(depot.y)
            
            # Plotear ruta
            ax.plot(route_x, route_y, c=color, linewidth=2,
                   alpha=0.7, zorder=2,
                   label=f'Ruta {i+1} (dist={route.distance:.1f})')
            
            # Resaltar clientes de esta ruta
            for node in route.nodes:
                ax.scatter(node.x, node.y, c=color, s=150,
                          edgecolors='black', linewidths=1.5, zorder=4)
        
        # Añadir información
        info_text = (f"Vehículos: {solution.num_vehicles}\n"
                    f"Distancia: {solution.total_distance:.2f}\n"
                    f"Factible: {'SÍ' if solution.is_feasible else 'NO'}")
        
        ax.text(0.02, 0.98, info_text,
               transform=ax.transAxes,
               fontsize=10,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.set_xlabel('Coordenada X', fontsize=12)
        ax.set_ylabel('Coordenada Y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        return fig, ax
    
    def plot_time_windows(self, customers: List[Node], routes: List = None):
        """Visualiza ventanas de tiempo de los clientes"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Ordenar clientes por ready_time
        sorted_customers = sorted(customers, key=lambda c: c.ready_time)
        
        y_positions = range(len(sorted_customers))
        
        for i, customer in enumerate(sorted_customers):
            # Dibujar ventana de tiempo
            window_width = customer.due_date - customer.ready_time
            rect = mpatches.Rectangle(
                (customer.ready_time, i - 0.3),
                window_width, 0.6,
                linewidth=1, edgecolor='blue',
                facecolor='lightblue', alpha=0.5
            )
            ax.add_patch(rect)
            
            # Añadir ID del cliente
            ax.text(customer.ready_time - 10, i,
                   f'C{customer.id}',
                   ha='right', va='center', fontsize=8)
        
        ax.set_xlabel('Tiempo', fontsize=12)
        ax.set_ylabel('Clientes', fontsize=12)
        ax.set_title('Ventanas de Tiempo de los Clientes',
                    fontsize=14, fontweight='bold')
        ax.set_yticks([])
        ax.grid(True, axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig, ax
```

---

## Ejemplos Completos

### Ejemplo 1: Cargar y Visualizar Instancia

```python
from data_loader import SolomonInstanceLoader
from models import Node
from utils import create_nodes_from_instance
from visualizer import VRPTWVisualizer

# Cargar instancia
loader = SolomonInstanceLoader('data')
instance = loader.load_instance('C101')

# Convertir a objetos Node
depot, customers = create_nodes_from_instance(instance)

# Visualizar
visualizer = VRPTWVisualizer()
fig, ax = visualizer.plot_instance(depot, customers, title='Instancia C101')
plt.savefig('results/C101_instance.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualizar ventanas de tiempo
fig, ax = visualizer.plot_time_windows(customers)
plt.savefig('results/C101_time_windows.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Ejemplo 2: Resolver con Nearest Neighbor

```python
from algorithms import NearestNeighborVRPTW
from validators import SolutionValidator, print_solution_report

# Cargar instancia
loader = SolomonInstanceLoader('data')
instance = loader.load_instance('C101')
depot, customers = create_nodes_from_instance(instance)

# Resolver
solver = NearestNeighborVRPTW(
    depot, customers,
    instance['distance_matrix'],
    instance['vehicle_capacity']
)

solution = solver.solve()

# Validar
validator = SolutionValidator(
    depot, customers,
    instance['distance_matrix'],
    instance['vehicle_capacity']
)

# Imprimir reporte
print_solution_report(solution, validator)

# Visualizar solución
visualizer = VRPTWVisualizer()
fig, ax = visualizer.plot_solution(solution, depot, customers,
                                   title='Solución C101 - Nearest Neighbor')
plt.savefig('results/C101_solution_nn.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Ejemplo 3: Comparar Algoritmos

```python
from algorithms import NearestNeighborVRPTW, ClarkeWrightVRPTW
import pandas as pd

def compare_algorithms(instance_name: str):
    """Compara diferentes algoritmos en una instancia"""
    # Cargar instancia
    loader = SolomonInstanceLoader('data')
    instance = loader.load_instance(instance_name)
    depot, customers = create_nodes_from_instance(instance)
    
    # Resolver con diferentes algoritmos
    algorithms = {
        'Nearest Neighbor': NearestNeighborVRPTW,
        'Clarke-Wright': ClarkeWrightVRPTW
    }
    
    results = []
    
    for alg_name, AlgorithmClass in algorithms.items():
        solver = AlgorithmClass(
            depot, customers,
            instance['distance_matrix'],
            instance['vehicle_capacity']
        )
        
        solution = solver.solve()
        
        results.append({
            'Algoritmo': alg_name,
            'Vehículos': solution.num_vehicles,
            'Distancia': round(solution.total_distance, 2),
            'Factible': solution.is_feasible
        })
    
    # Crear DataFrame
    df = pd.DataFrame(results)
    print(f"\nComparación de Algoritmos - {instance_name}")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60)
    
    return df

# Ejecutar comparación
compare_algorithms('C101')
compare_algorithms('R101')
compare_algorithms('RC101')
```

### Ejemplo 4: Análisis de Múltiples Instancias

```python
def analyze_all_instances():
    """Analiza todas las instancias del dataset"""
    loader = SolomonInstanceLoader('data')
    
    results = []
    
    for instance_type in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
        instances = loader.load_all_instances(instance_type)
        
        for instance_name, instance in instances.items():
            depot, customers = create_nodes_from_instance(instance)
            
            # Resolver con Nearest Neighbor
            solver = NearestNeighborVRPTW(
                depot, customers,
                instance['distance_matrix'],
                instance['vehicle_capacity']
            )
            
            solution = solver.solve()
            
            results.append({
                'Instancia': instance_name,
                'Tipo': instance_type,
                'Clientes': len(customers),
                'Vehículos': solution.num_vehicles,
                'Distancia': round(solution.total_distance, 2),
                'Factible': solution.is_feasible
            })
    
    # Crear DataFrame y guardar
    df = pd.DataFrame(results)
    df.to_csv('results/all_instances_analysis.csv', index=False)
    
    # Estadísticas por tipo
    print("\nEstadísticas por Tipo de Instancia")
    print("=" * 70)
    summary = df.groupby('Tipo').agg({
        'Vehículos': ['mean', 'min', 'max'],
        'Distancia': ['mean', 'min', 'max'],
        'Factible': 'sum'
    }).round(2)
    print(summary)
    
    return df

# Ejecutar análisis
df_results = analyze_all_instances()
```

---

## Conclusión

Esta guía proporciona una base sólida para trabajar con el dataset Solomon VRPTW, incluyendo:

✓ Estructuras de datos bien diseñadas
✓ Funciones de lectura y procesamiento
✓ Implementaciones de algoritmos básicos
✓ Validación completa de soluciones
✓ Visualización profesional
✓ Ejemplos prácticos y completos

Para algoritmos más avanzados (metaheurísticas, optimización exacta), se recomienda construir sobre esta base e implementar técnicas específicas según las necesidades del proyecto.
