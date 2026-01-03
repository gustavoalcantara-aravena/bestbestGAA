# AUDITORÍA: Restricciones del Modelo en el Flujo de Experimentación (experiments.py)

**Fecha**: 3 de enero de 2026  
**Archivo auditado**: `scripts/experiments.py`  
**Proyecto**: GAA-VRPTW-GRASP-2

---

## 1. FLUJO DE EXPERIMENTACIÓN Y RESTRICCIONES

### Diagrama del flujo:

```
experiments.py:QuickExperiment.run()
    ↓
AlgorithmGenerator.generate_three_algorithms() [Línea ~425]
    ├─ Genera AST abstract syntax trees
    └─ Parámetros: seed=42, depth=3, size=4
    
    ↓
Para cada (familia, instancia, algoritmo):
    ↓
1. Carga Instancia [Línea ~455]
   └─ loader.load_instance() → Instance object
      ├─ ✅ Valida 100 clientes
      ├─ ✅ Valida parámetros (Q, time windows)
      └─ ✅ Valida depot en posición 0
    
    ↓
2. Reconstruye AST [Línea ~465]
   └─ dict_to_ast(ast_dict) → ASTNode
      └─ Convierte representación dict a objeto ejecutable
    
    ↓
3. Ejecuta Algoritmo [Línea ~470]
   └─ ASTInterpreter.execute(ast_node, instance)
      ├─ Crea solución inicial vacía: Solution(instance)
      ├─ Ejecuta nodos del AST secuencialmente
      └─ Retorna solución final
    
    ↓
4. Extrae Resultados [Línea ~475]
   ├─ k_final = solution.num_vehicles
   ├─ d_final = solution.total_distance
   └─ elapsed = tiempo en segundos
    
    ↓
5. Valida Restricciones (IMPLÍCITO) [Línea ~490]
   └─ Si solution.feasible == False:
      └─ Aún aparece en logs (⚠️ NO SE REPORTA)
```

---

## 2. VERIFICACIÓN DE RESTRICCIONES EN CADA PASO

### 2.1 Paso 1: Carga de Instancia

**Código** (experiments.py, línea 455):
```python
instance = executor.all_instances[family][instance_id]
```

**Restricciones validadas**:
- ✅ **R1**: Visita Única → Instancia cargada correctamente
- ✅ **R2**: Salida Única → Instancia cargada correctamente
- ✅ **R3**: Depósito/K → Depot en posición 0
- ✅ **R4**: Capacidad → Q_capacity está definida
- ✅ **R5**: Ventanas tiempo → ready_time, due_date presentes
- ✅ **R7**: Subtours → Se cargará desde benchmark válido

**Status**: ✅ Todas las restricciones están presentes en instancia

---

### 2.2 Paso 2: Reconstrucción de AST

**Código** (experiments.py, línea 467):
```python
ast_dict = algo_dict['ast']
ast_node = dict_to_ast(ast_dict)
```

**Qué ocurre**:
- Se convierte dict → ASTNode object
- El AST contiene estructura de algoritmo:
  - GreedyConstruct → Construye solución
  - LocalSearch → Mejora solución
  - While loops → Iteraciones

**Restricciones impactadas**:
- ⚠️ El AST define CÓMO se respetan las restricciones
- El constructor (GreedyConstruct) debe insertar clientes respetando capacidad
- El local search debe mantener factibilidad

**Status**: ⚠️ Depende de implementación de operadores

---

### 2.3 Paso 3: Ejecución del Algoritmo

**Código** (experiments.py, línea 470):
```python
solution = interpreter.execute(ast_node, instance)
```

**Flujo interno** (src/gaa/interpreter.py):
```
ASTInterpreter.execute(ast_node, instance)
    ↓
1. Crea Solution inicial vacía: Solution(instance)
   └─ solution.routes = []
   └─ solution.num_vehicles = 0
   └─ solution.total_distance = 0
    
    ↓
2. Ejecuta AST recursivamente:
   
   _execute_node(GreedyConstruct)
       ↓
       Constructor.apply(instance) → Solution con rutas
       └─ AQUÍ SE RESPETAN:
           ✅ R1-R2: Se inserten clientes
           ✅ R3: Se crean rutas (vehículos)
           ✅ R4: Se valida capacidad
           ✅ R5: Se respetan ventanas (parcial)
           ✅ R6: Se respeta precedencia temporal
       
   _execute_node(While > LocalSearch)
       ↓
       LocalSearch.apply(solution) → Solución mejorada
       └─ AQUÍ SE MANTIENEN:
           ✅ R1-R2: Mismos clientes visitados
           ✅ R3: Mismo número de vehículos (o menos)
           ✅ R4: No se viola capacidad
           ✅ R5: No se viola ventanas (idealmente)
           ✅ R7: No crea subtours
    
    ↓
3. Retorna solución final
```

**Status**: ✅ Restricciones respetadas EN TEORÍA

---

### 2.4 Paso 4: Extracción de Resultados

**Código** (experiments.py, línea 475):
```python
k_final = solution.num_vehicles      # Propiedades que validan restricciones
d_final = solution.total_distance
```

**Qué se calcula**:
```python
# src/core/models.py
@property
def num_vehicles(self) -> int:
    return sum(1 for route in self.routes if len(route.sequence) > 2)
    # Esta propiedad asume:
    # ✅ R1: Cada cliente en exactamente una ruta
    # ✅ R3: Cada ruta = 1 vehículo

@property
def total_distance(self) -> float:
    total = 0.0
    for route in self.routes:
        total += route.distance
    return total
    # Suma distancias de todos los viajes depot→clientes→depot
```

**Status**: ✅ Resultados consisten con restricciones

---

### 2.5 Paso 5: Logging y Almacenamiento

**Código** (experiments.py, línea 490):
```python
metrics = {
    'algorithm': algo_name,
    'instance_id': instance_id,
    'family': family,
    'k_final': k_final,
    'd_final': d_final,
    'time_sec': elapsed,
    'status': 'success'
}
executor.add_result(metric_dict=metrics)
logger.log_algorithm_execution(...)
```

**⚠️ PROBLEMA IDENTIFICADO**:
- ❌ NO se reporta `solution.feasible`
- ❌ NO se valida si restricciones fueron violadas
- ❌ K=1 reportado, pero ¿es factible? (posible violación de capacidad)

**Recomendación**: Agregar validación

```python
# AGREGAR DESPUÉS DE LÍNEA 475:
if not solution.feasible:
    logger.warning(f"[WARNING] Solución infeasible para {algo_name} en {instance_id}")
    # Analizar qué restricción se violó
```

---

## 3. ANÁLISIS DE RESULTADOS EXPERIMENTALES

Del último experimento QUICK (36 tests):

| Algoritmo | K promedio | Interpretación |
|-----------|-----------|-----------------|
| GAA_Algorithm_1 | 1.00 | ⚠️ Sospechoso - Posible violación de capacidad |
| GAA_Algorithm_2 | 1.00 | ⚠️ Sospechoso - Posible violación de capacidad |
| GAA_Algorithm_3 | 14.33 | ✅ Realista - En rango esperado (8-20 típicamente) |

**Análisis crítico**:

Para instancia R101:
- 100 clientes
- Capacidad: 200 unidades
- Demanda promedio: ~15-20 unidades por cliente
- ✅ Esperado: K = 100/200 × 15-20 ≈ 7-10 vehículos

Con K=1:
- ❌ IMPOSIBLE respetar capacidad (1 vehículo × 200 unidades < 100 clientes × 15-20 unidades)
- ❌ IMPOSIBLE respetar time windows (una ruta tan larga violará deadlines)

**Conclusión**: GAA_Algorithm_1 y GAA_Algorithm_2 están generando soluciones INFEASIBLES

---

## 4. PUNTOS DE FALLO IDENTIFICADOS

### 4.1 Constructores con K=1 (CRÍTICO)

**Ubicación**: `src/operators/constructive.py`

**Problema**: Los constructores insertan TODOS los clientes en UNA sola ruta

```python
# EJEMPLO PROBLEMÁTICO:
# NearestNeighbor inserta cliente por cliente sin crear nuevas rutas
# cuando la capacidad se llena

while unvisited:
    nearest = find_nearest_unvisited(current)
    if total_load + demand[nearest] > Q_capacity:
        # ❌ BUG: No crea nueva ruta, solo marca como visitado
        # ✅ DEBERÍA: Crear nueva ruta y empezar desde depot
        pass
```

---

### 4.2 Validación en Experimentos (CRÍTICO)

**Ubicación**: `scripts/experiments.py` línea 475-490

**Problema**: No se verifica `solution.feasible` antes de reportar

```python
# ACTUAL:
k_final = solution.num_vehicles  # Reporta K sin validar
d_final = solution.total_distance

# DEBERÍA SER:
if not solution.feasible:
    logger.error(f"INFEASIBLE SOLUTION for {algo_name}!")
    # Investigar qué restricción se violó
```

---

## 5. TABLA DE RESTRICCIONES EN EXPERIMENTOS

| Restricción | En Instance | En Construcción | En Local Search | En Reporte |
|------------|------------|-----------------|-----------------|-----------|
| R1: Visita Única | ✅ Cargada | ✅ Respetada | ✅ Mantenida | ⚠️ No validada |
| R2: Salida Única | ✅ Cargada | ✅ Respetada | ✅ Mantenida | ⚠️ No validada |
| R3: Depósito/K | ✅ Cargada | ✅ Respetada | ⚠️ Puede reducir K | ✅ Reportada |
| R4: Capacidad | ✅ Cargada | ❌ **VIOLADA** | ✅ Mantenida | ❌ No validada |
| R5: Ventanas Tiempo | ✅ Cargada | ⚠️ Parcial | ⚠️ Parcial | ❌ No validada |
| R6: Precedencia Temporal | ✅ Cargada | ✅ Respetada | ✅ Mantenida | ⚠️ No validada |
| R7: Sin Subtours | ✅ Cargada | ✅ Prevenida | ✅ Mantenida | ⚠️ No validada |

---

## 6. RECOMENDACIONES PARA REPARACIÓN

### CRÍTICA - Fijar Constructores:

```python
# En src/operators/constructive.py, NearestNeighbor:

while unvisited:
    # Busca cliente más cercano que QUEPA en ruta actual
    nearest = None
    min_dist = float('inf')
    
    for cand in unvisited:
        dist = instance.get_distance(current, cand)
        demand = instance.get_customer(cand).demand
        
        # ✅ AHORA VALIDA CAPACIDAD ANTES DE ELEGIR
        if total_load + demand <= instance.Q_capacity and dist < min_dist:
            min_dist = dist
            nearest = cand
    
    # Si no hay cliente que quepa, CREA NUEVA RUTA
    if nearest is None:
        current_route.append(0)  # Cierra ruta actual
        route = Route(vehicle_id=len(routes), sequence=current_route, instance=instance)
        routes.append(route)
        
        # Inicia nueva ruta
        current_route = [0]
        current = 0
        total_load = 0
        continue
    
    # Inserta cliente en ruta actual
    current_route.append(nearest)
    current = nearest
    unvisited.remove(nearest)
    total_load += demand
```

### IMPORTANTE - Validar en Experimentos:

```python
# En scripts/experiments.py línea 478:

# Extrae resultados
k_final = solution.num_vehicles
d_final = solution.total_distance

# ✅ AÑADE VALIDACIÓN:
if not solution.feasible:
    logger.warning(f"[WARNING] Solution is INFEASIBLE for {algo_name} on {instance_id}")
    print(f"[WARNING] K={k_final}, D={d_final} but INFEASIBLE")
    # Opcional: analizar qué restricción se viola
```

---

## 7. CONCLUSIÓN

### Estado Actual: ⚠️ CRÍTICO

- ✅ Restricciones definidas correctamente en modelo
- ✅ Validaciones implementadas en src/core/models.py
- ❌ **Constructores generan soluciones INFEASIBLES** (K=1 sospechoso)
- ❌ **Experimentos NO validan feasibility** antes de reportar

### Acción Requerida:

1. **INMEDIATO**: Fijar constructores para respetar capacidad
2. **INMEDIATO**: Agregar validación en experiments.py
3. **URGENTE**: Re-ejecutar QUICK para verificar

### Pasos Próximos:

```bash
# 1. Arreglar constructores en src/operators/constructive.py
# 2. Arreglar validación en scripts/experiments.py
# 3. Re-ejecutar: python scripts/experiments.py --mode QUICK
# 4. Verificar: todos los K_final deben ser >= 8 para R101
# 5. Verificar: solution.feasible debe ser True para todos
```

