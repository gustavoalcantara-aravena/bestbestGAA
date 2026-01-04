# Configuración Óptima para Algoritmos VRPTW

## Resumen Ejecutivo

Este documento define la estructura óptima de datos y configuración que cualquier algoritmo necesita para trabajar correctamente con el Solomon VRPTW Dataset. Se basa en el análisis exhaustivo de las 56 instancias y las mejores prácticas de la literatura.

---

## 1. Datos Esenciales que el Algoritmo DEBE Recibir

### 1.1 Datos de la Instancia (Obligatorios)

```python
instance_config = {
    # Identificación
    "name": "C101",                    # Nombre de la instancia
    "family": "C1",                    # Familia (C1, C2, R1, R2, RC1, RC2)
    
    # Parámetros del vehículo
    "vehicle_capacity": 200,           # Capacidad máxima del vehículo
    "num_vehicles": None,              # None = ilimitado, o especificar máximo
    
    # Horizonte temporal
    "time_horizon": 1236,              # Fin del día laboral (due_date del depósito)
    
    # Datos de nodos (depósito + clientes)
    "depot": {
        "id": 0,                       # Siempre 0 para el depósito
        "x": 40,
        "y": 50,
        "demand": 0,                   # Siempre 0
        "ready_time": 0,               # Siempre 0
        "due_date": 1236,              # Horizonte temporal
        "service_time": 0              # Siempre 0
    },
    
    "customers": [
        {
            "id": 1,                   # IDs secuenciales 1-100
            "x": 45,
            "y": 68,
            "demand": 10,
            "ready_time": 912,
            "due_date": 967,
            "service_time": 90
        },
        # ... 99 clientes más
    ],
    
    # Matriz de distancias (opcional pero recomendado para eficiencia)
    "distance_matrix": [[0.0, 18.68, ...], [...], ...]  # (101 x 101)
}
```

### 1.2 Datos de Referencia (Altamente Recomendados)

```python
reference_data = {
    # Best Known Solution (para comparación)
    "bks": {
        "vehicles": 10,
        "distance": 828.94,
        "year": 1997,
        "method": "Rochat & Taillard"
    },
    
    # Límites inferiores teóricos
    "lower_bounds": {
        "vehicles_capacity": 10,       # ceil(total_demand / capacity)
        "vehicles_time": 8             # Estimación temporal
    },
    
    # Características de la instancia
    "characteristics": {
        "spatial_distribution": "4_clusters",
        "difficulty": "medium_high",
        "tight_capacity": true,
        "tight_time_windows": true,
        "primary_objective": "minimize_vehicles"
    }
}
```

### 1.3 Parámetros del Algoritmo (Configurables)

```python
algorithm_config = {
    # Función objetivo
    "objective": {
        "type": "hierarchical",        # o "weighted"
        "weights": {
            "vehicles": 1000,          # Serie 1: 1000, Serie 2: 100
            "distance": 1
        }
    },
    
    # Restricciones
    "constraints": {
        "capacity": "hard",            # No puede violarse
        "time_windows": "hard",        # No puede violarse
        "depot_return": "hard"         # No puede violarse
    },
    
    # Parámetros de cálculo
    "distance_method": "euclidean",
    "speed": 1.0,                      # 1 unidad distancia = 1 unidad tiempo
    "precision": 1e-6,                 # Para comparaciones flotantes
    
    # Criterios de parada
    "max_iterations": 10000,
    "max_time_seconds": 300,
    "target_gap": 0.01,                # 1% del BKS
    
    # Estrategia según familia
    "strategy": "auto"                 # o especificar manualmente
}
```

---

## 2. Estructura de Datos Recomendada

### 2.1 Clase Instance (Propuesta)

```python
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class Node:
    """Nodo (depósito o cliente)"""
    id: int
    x: float
    y: float
    demand: int
    ready_time: float
    due_date: float
    service_time: float
    
    def is_depot(self) -> bool:
        return self.id == 0

@dataclass
class InstanceMetadata:
    """Metadatos de la instancia"""
    name: str
    family: str                        # C1, C2, R1, R2, RC1, RC2
    type: str                          # Clustered, Random, Random-Clustered
    time_windows: str                  # Short, Long
    
    # BKS
    bks_vehicles: int
    bks_distance: float
    bks_year: int
    bks_method: str
    
    # Límites inferiores
    lb_vehicles_capacity: int
    lb_vehicles_time: int
    
    # Características
    difficulty: str
    spatial_distribution: str
    tight_capacity: bool
    tight_time_windows: bool
    primary_objective: str

@dataclass
class Instance:
    """Instancia completa del VRPTW"""
    # Identificación
    name: str
    metadata: InstanceMetadata
    
    # Datos del problema
    depot: Node
    customers: List[Node]
    vehicle_capacity: int
    time_horizon: float
    
    # Datos precalculados
    distance_matrix: np.ndarray
    num_customers: int
    total_demand: int
    
    # Configuración del algoritmo
    objective_weights: dict
    recommended_algorithms: List[str]
    
    def __post_init__(self):
        self.num_customers = len(self.customers)
        self.total_demand = sum(c.demand for c in self.customers)
```

### 2.2 Loader con Metadatos Integrados

```python
import json
import pandas as pd
from pathlib import Path

class EnhancedSolomonLoader:
    """Cargador mejorado con metadatos"""
    
    def __init__(self, data_dir: str, metadata_file: str):
        self.data_dir = Path(data_dir)
        self.metadata_file = Path(metadata_file)
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> dict:
        """Carga metadatos desde JSON"""
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
    
    def load_instance(self, instance_name: str) -> Instance:
        """
        Carga instancia con todos los metadatos necesarios
        
        Returns:
            Instance completa con configuración óptima
        """
        # Cargar datos CSV
        csv_data = self._load_csv(instance_name)
        
        # Obtener metadatos
        meta = self.metadata['instance_metadata'].get(instance_name)
        if not meta:
            # Inferir metadatos desde el nombre
            meta = self._infer_metadata(instance_name)
        
        # Crear nodos
        depot = self._create_depot(csv_data.iloc[0])
        customers = [self._create_customer(row, i+1) 
                    for i, row in enumerate(csv_data.iloc[1:].itertuples())]
        
        # Calcular matriz de distancias
        distance_matrix = self._compute_distance_matrix(depot, customers)
        
        # Crear metadata object
        metadata_obj = InstanceMetadata(
            name=instance_name,
            family=meta['family'],
            type=meta['type'],
            time_windows=meta['time_windows'],
            bks_vehicles=meta['bks']['vehicles'],
            bks_distance=meta['bks']['distance'],
            bks_year=meta['bks']['year'],
            bks_method=meta['bks']['method'],
            lb_vehicles_capacity=meta['lower_bounds']['vehicles_capacity'],
            lb_vehicles_time=meta['lower_bounds']['vehicles_time'],
            difficulty=meta['difficulty'],
            spatial_distribution=meta['spatial_distribution'],
            tight_capacity=meta['characteristics']['tight_capacity'],
            tight_time_windows=meta['characteristics']['tight_time_windows'],
            primary_objective=meta['characteristics']['primary_objective']
        )
        
        # Obtener configuración de familia
        family_config = self.metadata['family_configurations'][meta['family']]
        
        # Crear instancia completa
        instance = Instance(
            name=instance_name,
            metadata=metadata_obj,
            depot=depot,
            customers=customers,
            vehicle_capacity=meta['vehicle_capacity'],
            time_horizon=meta['time_horizon'],
            distance_matrix=distance_matrix,
            num_customers=len(customers),
            total_demand=sum(c.demand for c in customers),
            objective_weights=family_config['objective_weights'],
            recommended_algorithms=meta['recommended_algorithms']
        )
        
        return instance
    
    def get_algorithm_config(self, instance: Instance) -> dict:
        """
        Genera configuración óptima del algoritmo para la instancia
        
        Returns:
            Diccionario con parámetros recomendados
        """
        family = instance.metadata.family
        
        config = {
            "objective_weights": instance.objective_weights,
            "primary_objective": instance.metadata.primary_objective,
            "difficulty": instance.metadata.difficulty,
            "recommended_algorithms": instance.recommended_algorithms,
            
            # Parámetros adaptativos según dificultad
            "max_iterations": self._get_max_iterations(family),
            "max_time_seconds": self._get_max_time(family),
            "target_gap": 0.01 if family in ['C1', 'C2'] else 0.05,
            
            # Estrategias específicas
            "use_clustering": instance.metadata.spatial_distribution != "uniform_random",
            "time_priority": instance.metadata.tight_time_windows,
            "capacity_priority": instance.metadata.tight_capacity,
            
            # Límites de referencia
            "expected_vehicles_min": instance.metadata.lb_vehicles_capacity,
            "expected_vehicles_max": instance.metadata.bks_vehicles * 1.5,
            "bks_distance": instance.metadata.bks_distance
        }
        
        return config
    
    def _get_max_iterations(self, family: str) -> int:
        """Iteraciones recomendadas según familia"""
        iterations = {
            'C1': 5000, 'C2': 3000,
            'R1': 10000, 'R2': 5000,
            'RC1': 8000, 'RC2': 5000
        }
        return iterations.get(family, 5000)
    
    def _get_max_time(self, family: str) -> int:
        """Tiempo máximo recomendado según familia"""
        times = {
            'C1': 60, 'C2': 30,
            'R1': 300, 'R2': 120,
            'RC1': 180, 'RC2': 120
        }
        return times.get(family, 120)
```

---

## 3. Validación y Verificación

### 3.1 Validador Completo

```python
class SolutionValidator:
    """Validador exhaustivo de soluciones"""
    
    def __init__(self, instance: Instance):
        self.instance = instance
    
    def validate(self, solution) -> dict:
        """
        Valida solución completa
        
        Returns:
            {
                'is_valid': bool,
                'violations': list,
                'metrics': dict,
                'quality_assessment': dict
            }
        """
        violations = []
        
        # 1. Validar cobertura
        violations.extend(self._validate_coverage(solution))
        
        # 2. Validar capacidad
        violations.extend(self._validate_capacity(solution))
        
        # 3. Validar ventanas de tiempo
        violations.extend(self._validate_time_windows(solution))
        
        # 4. Validar depósito
        violations.extend(self._validate_depot(solution))
        
        # Calcular métricas
        metrics = self._calculate_metrics(solution)
        
        # Evaluar calidad
        quality = self._assess_quality(solution, metrics)
        
        return {
            'is_valid': len(violations) == 0,
            'violations': violations,
            'metrics': metrics,
            'quality_assessment': quality
        }
    
    def _assess_quality(self, solution, metrics: dict) -> dict:
        """Evalúa calidad de la solución vs BKS"""
        bks_vehicles = self.instance.metadata.bks_vehicles
        bks_distance = self.instance.metadata.bks_distance
        
        gap_vehicles = ((metrics['num_vehicles'] - bks_vehicles) / bks_vehicles) * 100
        gap_distance = ((metrics['total_distance'] - bks_distance) / bks_distance) * 100
        
        # Clasificación de calidad
        if gap_vehicles == 0 and gap_distance < 1:
            quality_level = "optimal_or_near_optimal"
        elif gap_vehicles == 0 and gap_distance < 5:
            quality_level = "excellent"
        elif gap_vehicles <= 1 and gap_distance < 10:
            quality_level = "good"
        elif gap_vehicles <= 2 and gap_distance < 20:
            quality_level = "acceptable"
        else:
            quality_level = "poor"
        
        return {
            'quality_level': quality_level,
            'gap_vehicles_percent': gap_vehicles,
            'gap_distance_percent': gap_distance,
            'vehicles_vs_bks': f"{metrics['num_vehicles']} vs {bks_vehicles}",
            'distance_vs_bks': f"{metrics['total_distance']:.2f} vs {bks_distance}",
            'meets_lower_bound': metrics['num_vehicles'] >= self.instance.metadata.lb_vehicles_capacity
        }
```

---

## 4. Ejemplo de Uso Completo

### 4.1 Flujo Recomendado

```python
# 1. Cargar instancia con metadatos
loader = EnhancedSolomonLoader(
    data_dir='data',
    metadata_file='METADATA_INSTANCIAS.json'
)

instance = loader.load_instance('C101')

# 2. Obtener configuración óptima del algoritmo
algo_config = loader.get_algorithm_config(instance)

print(f"Instancia: {instance.name}")
print(f"Familia: {instance.metadata.family}")
print(f"Dificultad: {instance.metadata.difficulty}")
print(f"BKS: {instance.metadata.bks_vehicles} vehículos, {instance.metadata.bks_distance} distancia")
print(f"Objetivo primario: {instance.metadata.primary_objective}")
print(f"Algoritmos recomendados: {instance.recommended_algorithms}")
print(f"\nConfiguración del algoritmo:")
print(f"  - Pesos objetivo: {algo_config['objective_weights']}")
print(f"  - Iteraciones máximas: {algo_config['max_iterations']}")
print(f"  - Tiempo máximo: {algo_config['max_time_seconds']}s")
print(f"  - Usar clustering: {algo_config['use_clustering']}")

# 3. Ejecutar algoritmo con configuración óptima
algorithm = YourVRPTWAlgorithm(
    instance=instance,
    config=algo_config
)

solution = algorithm.solve()

# 4. Validar solución
validator = SolutionValidator(instance)
validation_result = validator.validate(solution)

print(f"\n¿Solución válida? {validation_result['is_valid']}")
if not validation_result['is_valid']:
    print("Violaciones:")
    for v in validation_result['violations']:
        print(f"  - {v}")

print(f"\nMétricas:")
print(f"  Vehículos: {validation_result['metrics']['num_vehicles']}")
print(f"  Distancia: {validation_result['metrics']['total_distance']:.2f}")

print(f"\nCalidad:")
quality = validation_result['quality_assessment']
print(f"  Nivel: {quality['quality_level']}")
print(f"  Gap vehículos: {quality['gap_vehicles_percent']:.2f}%")
print(f"  Gap distancia: {quality['gap_distance_percent']:.2f}%")
```

---

## 5. Datos Adicionales Opcionales (Pero Útiles)

### 5.1 Para Optimización Avanzada

```python
advanced_data = {
    # Análisis espacial
    "spatial_analysis": {
        "clusters": [
            {"id": 0, "center": (45, 68), "customers": [2, 3, 4, ...]},
            {"id": 1, "center": (20, 80), "customers": [10, 11, 12, ...]},
            # ...
        ],
        "outliers": [25, 67, 89],  # Clientes aislados
    },
    
    # Análisis temporal
    "temporal_analysis": {
        "early_customers": [4, 6, 8],      # ready_time < 300
        "middle_customers": [2, 5, 7],     # 300 <= ready_time < 900
        "late_customers": [3, 9, 10],      # ready_time >= 900
        "tight_windows": [2, 3, 4],        # window_width < 60
        "flexible_windows": [50, 60, 70]   # window_width > 100
    },
    
    # Análisis de demanda
    "demand_analysis": {
        "high_demand": [3, 15, 42],        # demand > 30
        "medium_demand": [2, 5, 7],        # 15 <= demand <= 30
        "low_demand": [10, 20, 30],        # demand < 15
    },
    
    # Vecindarios precalculados
    "neighborhoods": {
        1: [2, 3, 4, 5],     # 5 vecinos más cercanos del cliente 1
        2: [1, 3, 6, 7],
        # ...
    },
    
    # Pares incompatibles (por tiempo)
    "incompatible_pairs": [
        (2, 50),  # No pueden estar en la misma ruta
        (3, 45),
        # ...
    ]
}
```

### 5.2 Para Debugging y Análisis

```python
debug_data = {
    # Información de ejecución
    "execution_info": {
        "start_time": "2024-12-30 13:00:00",
        "end_time": "2024-12-30 13:05:23",
        "duration_seconds": 323.45,
        "iterations_completed": 5000,
        "convergence_iteration": 3245
    },
    
    # Historial de mejoras
    "improvement_history": [
        {"iteration": 0, "vehicles": 15, "distance": 950.5},
        {"iteration": 100, "vehicles": 12, "distance": 875.3},
        {"iteration": 500, "vehicles": 10, "distance": 835.2},
        # ...
    ],
    
    # Operadores aplicados
    "operators_stats": {
        "relocate": {"applied": 1500, "improved": 450},
        "exchange": {"applied": 2000, "improved": 320},
        "2opt": {"applied": 3000, "improved": 890}
    }
}
```

---

## 6. Formato de Salida Recomendado

### 6.1 Solución Estándar

```python
solution_output = {
    # Identificación
    "instance_name": "C101",
    "algorithm": "Adaptive Large Neighborhood Search",
    "timestamp": "2024-12-30 13:05:23",
    
    # Métricas principales
    "metrics": {
        "num_vehicles": 10,
        "total_distance": 835.42,
        "total_time": 1200.5,
        "total_waiting_time": 450.2,
        "objective_value": 10835.42
    },
    
    # Comparación con BKS
    "comparison": {
        "bks_vehicles": 10,
        "bks_distance": 828.94,
        "gap_vehicles": 0.0,
        "gap_distance": 0.78,
        "quality": "excellent"
    },
    
    # Rutas
    "routes": [
        {
            "vehicle_id": 1,
            "sequence": [0, 4, 6, 8, 10, 0],  # IDs de nodos
            "customers": [4, 6, 8, 10],
            "distance": 85.3,
            "load": 45,
            "time": 120.5,
            "waiting_time": 15.2,
            "is_feasible": true
        },
        # ... más rutas
    ],
    
    # Validación
    "validation": {
        "is_valid": true,
        "violations": [],
        "all_customers_visited": true,
        "capacity_respected": true,
        "time_windows_respected": true
    },
    
    # Información de ejecución
    "execution": {
        "duration_seconds": 45.3,
        "iterations": 5000,
        "convergence_iteration": 3245
    }
}
```

---

## 7. Recomendaciones Finales

### 7.1 Lo MÁS IMPORTANTE

1. **SIEMPRE proporcionar**:
   - Capacidad del vehículo (varía por familia)
   - Horizonte temporal (due_date del depósito)
   - BKS para comparación
   - Pesos de la función objetivo (varía por serie)

2. **NUNCA asumir**:
   - Capacidad fija de 200 (varía: 200, 700, 1000)
   - Tiempo de servicio constante (varía: 10 o 90)
   - Misma función objetivo para todas las familias

3. **VALIDAR siempre**:
   - Ventanas de tiempo (restricción DURA)
   - Capacidad del vehículo
   - Regreso al depósito dentro del horizonte
   - Todos los clientes visitados exactamente una vez

### 7.2 Estrategia Adaptativa

```python
def select_strategy(instance: Instance) -> str:
    """Selecciona estrategia según características"""
    
    if instance.metadata.family in ['C1', 'C2']:
        return "cluster_first_route_second"
    
    elif instance.metadata.family in ['R1', 'R2']:
        if instance.metadata.tight_time_windows:
            return "temporal_construction"
        else:
            return "spatial_construction"
    
    else:  # RC1, RC2
        return "hybrid_approach"
```

### 7.3 Checklist Pre-Ejecución

- [ ] Instancia cargada con todos los datos
- [ ] Capacidad del vehículo correcta para la familia
- [ ] Matriz de distancias calculada
- [ ] Función objetivo configurada (pesos correctos)
- [ ] BKS cargado para comparación
- [ ] Límites inferiores conocidos
- [ ] Estrategia seleccionada según familia
- [ ] Parámetros de parada definidos
- [ ] Validador configurado

---

**Conclusión**: Un algoritmo bien configurado con estos metadatos tendrá las mejores condiciones para:
1. Ejecutarse correctamente (sin errores de configuración)
2. Converger eficientemente (estrategia adaptada)
3. Producir soluciones de calidad (comparables con BKS)
4. Ser validado objetivamente (métricas estándar)
