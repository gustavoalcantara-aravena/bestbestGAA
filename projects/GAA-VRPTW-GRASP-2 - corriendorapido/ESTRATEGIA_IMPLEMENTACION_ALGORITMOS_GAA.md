# Estrategia de Implementación: Ejecución de Algoritmos GAA
**Fecha**: 2 de enero de 2026

---

## 1. OBJETIVO

Reemplazar la ejecución hardcodeada de `['GRASP', 'VND', 'ILS']` por la ejecución real de los **3 algoritmos generados automáticamente por GAA** mediante `ASTInterpreter`.

---

## 2. ARQUITECTURA PROPUESTA

### Flujo Actual (INCORRECTO)
```
[AlgorithmGenerator] → [AST generados, IGNORADOS]
                           ↓
                     [Hardcoded GRASP/VND/ILS]
                           ↓
                     [Ejecución]
```

### Flujo Propuesto (CORRECTO)
```
[AlgorithmGenerator] → [GAA_Algorithm_1/2/3 ASTs]
                           ↓
                     [ASTInterpreter]
                           ↓
                     [Ejecución en instancias]
                           ↓
                     [Resultados K, D]
```

---

## 3. CAMBIOS REQUERIDOS EN `scripts/experiments.py`

### 3.1 Importaciones Necesarias
```python
# AGREGAR:
from src.gaa.interpreter import ASTInterpreter
from src.gaa.ast_nodes import ASTNode  # Para reconstituir AST desde dict
```

### 3.2 Crear Función Auxiliar: Reconstruir AST desde Dict
```python
def dict_to_ast(ast_dict: Dict[str, Any]) -> ASTNode:
    """
    Convierte dict de AST generado a objeto ASTNode ejecutable.
    
    Args:
        ast_dict: Dict con estructura {'type': '...', 'params': {...}}
    
    Returns:
        ASTNode ejecutable
    """
    # Implementar reconstrucción JSON → AST
```

**Lógica**:
- GAA genera ASTs como dicts (para serialización)
- ASTInterpreter necesita objetos ASTNode
- Necesitamos función para convertir: `dict → ASTNode`

### 3.3 Modificar Bucle Principal de Ejecución

**Cambio 1: Usar algoritmos GAA en lugar de hardcoded**
```python
# ANTES (línea 367):
algorithms_to_test = ['GRASP', 'VND', 'ILS']

# DESPUÉS:
algorithms_to_test = gaa_algorithms  # Lista de dicts con AST
```

**Cambio 2: Reemplazar lógica de ejecución**
```python
# ANTES (líneas 380-410):
if algo_name == 'GRASP':
    grasp = GRASP(...)
    solution, fitness, stats = grasp.solve(instance)
    k_final, d_final = fitness[0], fitness[1]
elif algo_name == 'VND':
    # ... específico VND
else:  # ILS
    # ... específico ILS

# DESPUÉS:
# Todos los algoritmos se ejecutan de la misma manera:
interpreter = ASTInterpreter()
ast_node = dict_to_ast(algo_dict['ast'])
solution = interpreter.execute(ast_node, instance)
k_final = solution.num_vehicles
d_final = solution.total_distance
```

### 3.4 Actualizar Logging

**Cambio 3: Nombres correctos en logs**
```python
# ANTES:
logger.log_algorithm_execution(
    algorithm=algo_name,  # 'GRASP', 'VND', 'ILS'
    ...
)

# DESPUÉS:
logger.log_algorithm_execution(
    algorithm=algo_dict['name'],  # 'GAA_Algorithm_1', etc.
    ...
)
```

---

## 4. DETALLES TÉCNICOS DE IMPLEMENTACIÓN

### 4.1 Estructura de Dict GAA Generado
```python
gaa_algorithms = [
    {
        'id': 1,
        'name': 'GAA_Algorithm_1',
        'ast': ASTNode or Dict,  # ← AQUÍ ESTÁ EL ÁRBOL
        'pattern': 'iterative-simple',
        'seed': 42,
        'timestamp': '2026-01-02T...',
        'stats': {
            'depth': 3,
            'size': 4,
            'nodes': 4
        },
        'characteristics': {...}
    },
    # ... 2 más
]
```

### 4.2 Conversión AST Dict → ASTNode

El generador ya crea AST como objetos, pero también provee método `to_dict()`.
Necesitamos la inversa:

```python
def dict_to_ast(ast_dict) -> ASTNode:
    """Reconstruir ASTNode desde su representación dict"""
    
    if isinstance(ast_dict, ASTNode):
        # Ya es ASTNode, devolver tal cual
        return ast_dict
    
    if isinstance(ast_dict, dict):
        node_type = ast_dict.get('type')
        
        if node_type == 'Seq':
            body = [dict_to_ast(b) for b in ast_dict.get('body', [])]
            return Seq(body=body)
        
        elif node_type == 'While':
            condition = ast_dict.get('condition')
            body = dict_to_ast(ast_dict.get('body'))
            return While(condition=condition, body=body)
        
        elif node_type == 'GreedyConstruct':
            heuristic = ast_dict.get('heuristic')
            alpha = ast_dict.get('alpha')
            return GreedyConstruct(heuristic=heuristic, alpha=alpha)
        
        elif node_type == 'LocalSearch':
            operator = ast_dict.get('operator')
            max_iterations = ast_dict.get('max_iterations')
            return LocalSearch(operator=operator, max_iterations=max_iterations)
        
        # ... más tipos según necesidad
```

### 4.3 Ejecución con ASTInterpreter

```python
# Dentro del bucle de experimentos
for algo_dict in algorithms_to_test:  # ahora son dicts GAA
    try:
        # Reconstruir AST ejecutable
        ast_node = dict_to_ast(algo_dict['ast'])
        
        # Crear intérprete
        interpreter = ASTInterpreter()
        
        # Ejecutar en instancia
        start_time = time.time()
        solution = interpreter.execute(ast_node, instance)
        elapsed = time.time() - start_time
        
        # Extraer resultados
        k_final = solution.num_vehicles
        d_final = solution.total_distance
        
        # Registrar
        logger.log_algorithm_execution(
            algorithm=algo_dict['name'],  # 'GAA_Algorithm_1'
            instance_id=instance_id,
            family=family,
            k_final=k_final,
            d_final=d_final,
            elapsed_time=elapsed,
            status='success'
        )
        
    except Exception as e:
        # Manejo de errores AST
        elapsed = time.time() - start_time
        logger.log_algorithm_execution(
            algorithm=algo_dict['name'],
            instance_id=instance_id,
            family=family,
            elapsed_time=elapsed,
            status='failed',
            error=str(e)
        )
```

---

## 5. CAMBIOS SECUNDARIOS

### 5.1 ExperimentConfig
```python
# ANTES:
config.algorithms = ['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3']

# DESPUÉS: Se usa el mismo campo, pero ahora con dicts GAA reales
algorithms_to_test = gaa_algorithms
```

### 5.2 Cálculo de Total Experimentos
```python
# ANTES:
algorithms_to_test = ['GRASP', 'VND', 'ILS']
num_algorithms = len(algorithms_to_test)  # Siempre 3

# DESPUÉS:
num_algorithms = len(gaa_algorithms)  # Siempre 3, pero son GAA
```

### 5.3 Logging de Algoritmos Generados
```python
# Ya existe (líneas 353-362), MANTENER:
for algo in gaa_algorithms:
    logger.log_algorithm_generated(AlgorithmMetadata(
        name=algo['name'],
        pattern=algo['pattern'],
        depth=algo['stats']['depth'],
        size=algo['stats']['size'],
        components={'structure': 'AST'},
        parameters={'seed': config.seed}
    ))
```

---

## 6. VENTAJAS DE ESTA IMPLEMENTACIÓN

1. **Coherencia**: Los algoritmos generados se ejecutan realmente
2. **Reproducibilidad**: AST con seed fijo = resultados reproducibles
3. **Transparencia**: Logs mostrarán `GAA_Algorithm_X` en lugar de GRASP/VND/ILS
4. **Comparación Justa**: Todos (incluyendo GAA) tienen depth=3, size=4
5. **Extensibilidad**: Fácil de agregar más algoritmos GAA después
6. **Auditabilidad**: AST serializable = se pueden guardar y revisar

---

## 7. CHECKLIST DE IMPLEMENTACIÓN

- [ ] Agregar imports: `ASTInterpreter`, `ASTNode`
- [ ] Implementar `dict_to_ast(ast_dict)` function
- [ ] Cambiar `algorithms_to_test = ['GRASP', ...]` → `= gaa_algorithms`
- [ ] Reemplazar lógica hardcodeada de GRASP/VND/ILS por ASTInterpreter
- [ ] Actualizar nombres en logger
- [ ] Mantener manejo de errores robusto
- [ ] Verificar que `solution.num_vehicles` y `solution.total_distance` son correctos
- [ ] Validar con QUICK (36 experimentos)
- [ ] Probar con FULL (168 experimentos)
- [ ] Verificar logs muestren GAA_Algorithm_X

---

## 8. ESTIMACIÓN DE ESFUERZO

- **Implementación**: 30-45 minutos
- **Testing QUICK**: 10-15 minutos
- **Validación completa**: 20-30 minutos

Total: ~1-1.5 horas

