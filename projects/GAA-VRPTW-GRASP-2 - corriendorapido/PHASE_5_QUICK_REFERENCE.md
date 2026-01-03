---
title: "Phase 5 Quick Reference: GAA Usage Guide"
date: 2025-01-09
version: 1.0
---

# 🚀 FASE 5: GUÍA DE USO RÁPIDO - GAA (Generación Automática de Algoritmos)

## 📦 Import Rápido

```python
from src.gaa import (
    # AST Nodes
    ASTNode, Seq, While, For, If, ChooseBestOf, ApplyUntilNoImprove,
    GreedyConstruct, LocalSearch, Perturbation, Repair,
    reconstruct_node,
    
    # Grammar
    VRPTWGrammar, ConstraintValidator,
    
    # Generator
    AlgorithmGenerator,
    
    # Interpreter
    ASTInterpreter,
    
    # Repair
    ASTValidator, ASTRepairMechanism, ASTNormalizer,
)

from src.models import Instance, Solution
```

---

## 1️⃣ Generar Algoritmos Aleatorios

### Opción A: 3 Algoritmos con Seed (Reproducible)

```python
generator = AlgorithmGenerator(seed=42)
algos = generator.generate_three_algorithms()

for i, algo in enumerate(algos):
    print(f"Algoritmo {i+1}:")
    print(f"  Profundidad: {algo.depth()}")
    print(f"  Tamaño: {algo.size()}")
    print(algo.to_pseudocode())
    print()
```

**Resultado**: Siempre genera los mismos 3 algoritmos con seed=42

### Opción B: Generar Algoritmo Individual

```python
generator = AlgorithmGenerator(seed=42)

# Método grow (típicamente más pequeños)
algo_grow = generator.generate_algorithm(depth=2, method='grow')

# Método full (típicamente más grandes)
algo_full = generator.generate_algorithm(depth=3, method='full')
```

**Parámetros**:
- `depth`: Profundidad máxima (2-4 típico)
- `method`: 'grow' o 'full'
  - `grow`: No-terminales pueden ser terminales
  - `full`: No-terminales siempre se expanden

### Opción C: Generar Múltiples Algoritmos

```python
generator = AlgorithmGenerator()
algos = [generator.generate_algorithm(depth=3) for _ in range(10)]
```

---

## 2️⃣ Validar Algoritmos

### Validación Simple

```python
validator = ASTValidator()
is_valid, violations = validator.validate(algo)

if is_valid:
    print("✅ Algoritmo válido")
else:
    print("❌ Violaciones encontradas:")
    for violation in violations:
        print(f"  - {violation}")
```

### Validación Detallada

```python
from src.gaa import AlgorithmValidator

algo_validator = AlgorithmValidator()
is_valid, errors, warnings = algo_validator.validate_all(algo)

print(f"Válido: {is_valid}")
print(f"Errores: {errors}")
print(f"Advertencias: {warnings}")
```

---

## 3️⃣ Reparar Algoritmos Inválidos

### Auto-reparación

```python
repair = ASTRepairMechanism()
repaired_algo, was_repaired, repairs = repair.repair(invalid_algo)

if was_repaired:
    print("Reparaciones aplicadas:")
    for repair_type in repairs:
        print(f"  - {repair_type}")
    print(repaired_algo.to_pseudocode())
```

### Normalización

```python
normalizer = ASTNormalizer()
normalized_algo = normalizer.normalize(algo)
# Colapsa sequences, reordena fases, simplifica control flow
```

---

## 4️⃣ Ejecutar Algoritmos en Instancias

### Ejecución Básica

```python
# Cargar instancia
from src.data.loader import InstanceLoader
loader = InstanceLoader()
instance = loader.load_instance("C101")

# Crear intérprete
interpreter = ASTInterpreter()

# Ejecutar algoritmo
solution = interpreter.execute(algo, instance)

print(f"Costo: {solution.cost}")
print(f"Rutas: {solution.num_routes}")
print(f"Factible: {solution.is_feasible}")
```

### Con Solución Inicial

```python
initial_solution = Solution(instance)
# ... crear solución inicial si es necesario ...

solution = interpreter.execute(algo, instance, initial_solution)
```

### Acceder a Estadísticas

```python
stats = interpreter.get_stats()
print(f"Nodos ejecutados: {stats['nodes_executed']}")
print(f"Llamadas a operadores: {stats['operator_calls']}")
print(f"Soluciones factibles: {stats['feasible_solutions']}")
print(f"Mejoras realizadas: {stats['improvements']}")
```

---

## 5️⃣ Crear Algoritmos Manualmente

### Algoritmo Simple: Constructor + Local Search

```python
algo = Seq(body=[
    GreedyConstruct(heuristic='RandomizedInsertion'),
    LocalSearch(operator='TwoOpt', max_iterations=50)
])
```

### Algoritmo Complejo: GRASP-like

```python
algo = Seq(body=[
    GreedyConstruct(heuristic='RandomizedInsertion'),
    While(
        max_iterations=100,
        body=Seq(body=[
            LocalSearch(operator='TwoOpt', max_iterations=50),
            LocalSearch(operator='OrOpt', max_iterations=30)
        ])
    ),
    Perturbation(operator='RuinRecreate', strength=0.2)
])
```

### Algoritmo Multi-start

```python
algo = For(
    iterations=5,
    body=Seq(body=[
        GreedyConstruct(heuristic='RandomizedInsertion'),
        While(
            max_iterations=50,
            body=LocalSearch(operator='TwoOpt', max_iterations=30)
        )
    ])
)
```

### Algoritmo con Selección Adaptativa

```python
algo = ChooseBestOf(alternatives=[
    LocalSearch(operator='TwoOpt', max_iterations=50),
    LocalSearch(operator='OrOpt', max_iterations=50),
    LocalSearch(operator='Relocate', max_iterations=50),
])
```

---

## 6️⃣ Serialización y Persistencia

### Guardar Algoritmo a JSON

```python
import json

# Convertir a diccionario
data = algo.to_dict()

# Guardar
with open('algorithm.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Cargar Algoritmo desde JSON

```python
import json
from src.gaa import reconstruct_node

# Cargar
with open('algorithm.json', 'r') as f:
    data = json.load(f)

# Reconstruir
algo = reconstruct_node(data)
```

### Clonar Algoritmo

```python
algo_copy = algo.clone()  # Deep copy

# Modificar copia sin afectar original
algo_copy.max_iterations = 1000
```

---

## 7️⃣ Análisis de Algoritmos

### Métricas Estructurales

```python
print(f"Profundidad: {algo.depth()}")      # 0 = terminal, >0 = nesting level
print(f"Tamaño: {algo.size()}")            # Total de nodos
print(f"Tipo: {type(algo).__name__}")      # 'Seq', 'While', etc.
```

### Pseudocódigo

```python
print(algo.to_pseudocode())
```

**Ejemplo de salida**:
```
Seq:
  GreedyConstruct(RandomizedInsertion)
  While(max_iterations=100):
    LocalSearch(TwoOpt, max_iterations=50)
```

---

## 8️⃣ Operadores Disponibles

### Constructores (6)

```python
constructores = [
    'NearestNeighbor',
    'RandomizedInsertion',
    'SavingsHeuristic',
    'TimeOrientedNN',
    'InsertionI1',
    'RegretInsertion'
]

# Usar en AST
GreedyConstruct(heuristic='SavingsHeuristic')
```

### Local Search Intra-ruta (4)

```python
intra = [
    'TwoOpt',
    'OrOpt',
    'Relocate',
    'ThreeOpt'
]

LocalSearch(operator='ThreeOpt', max_iterations=100)
```

### Local Search Inter-ruta (4)

```python
inter = [
    'CrossExchange',
    'TwoOptStar',
    'SwapCustomers',
    'RelocateInter'
]

LocalSearch(operator='CrossExchange', max_iterations=50)
```

### Perturbadores (4)

```python
perturbadores = [
    'EjectionChain',
    'RuinRecreate',
    'RandomRemoval',
    'RouteElimination'
]

Perturbation(operator='EjectionChain', strength=0.3)
```

### Reparadores (3)

```python
reparadores = [
    'RepairCapacity',
    'RepairTimeWindows',
    'GreedyRepair'
]

Repair(operator='GreedyRepair')
```

---

## 9️⃣ Flujo Completo: Generar → Validar → Reparar → Ejecutar

```python
from src.gaa import *
from src.models import Instance
from src.data.loader import InstanceLoader

# 1. Generar algoritmo
print("1️⃣ Generando algoritmo...")
generator = AlgorithmGenerator(seed=42)
algo = generator.generate_algorithm(depth=3, method='grow')
print(f"   Tamaño: {algo.size()}, Profundidad: {algo.depth()}")

# 2. Validar
print("\n2️⃣ Validando...")
validator = ASTValidator()
is_valid, violations = validator.validate(algo)
if not is_valid:
    print(f"   Violaciones encontradas: {len(violations)}")
else:
    print("   ✅ Válido")

# 3. Reparar si es necesario
if not is_valid:
    print("\n3️⃣ Reparando...")
    repair = ASTRepairMechanism()
    algo, fixed, repairs = repair.repair(algo)
    print(f"   Reparaciones: {repairs}")
else:
    print("\n3️⃣ Reparación: No necesario")

# 4. Ejecutar
print("\n4️⃣ Ejecutando en instancia...")
loader = InstanceLoader()
instance = loader.load_instance("C101")

interpreter = ASTInterpreter()
solution = interpreter.execute(algo, instance)

print(f"   Costo final: {solution.cost}")
print(f"   Factible: {solution.is_feasible}")
print(f"   Nodos ejecutados: {interpreter.get_stats()['nodes_executed']}")
```

---

## 🔟 Debugging y Troubleshooting

### Problema: Algoritmo genera excepciones

```python
try:
    solution = interpreter.execute(algo, instance)
except Exception as e:
    print(f"Error durante ejecución: {e}")
    # Aplicar reparación
    repair = ASTRepairMechanism()
    fixed_algo, _, _ = repair.repair(algo)
    solution = interpreter.execute(fixed_algo, instance)
```

### Problema: Algoritmo muy grande/profundo

```python
if algo.size() > 20:
    print("⚠️ Algoritmo muy grande")
    normalizer = ASTNormalizer()
    algo = normalizer.normalize(algo)
    print(f"   Después de normalización: tamaño={algo.size()}")
```

### Problema: Validación falla

```python
validator = ASTValidator()
is_valid, violations = validator.validate(algo)

for i, violation in enumerate(violations, 1):
    print(f"{i}. {violation}")

# Ver qué se puede reparar automáticamente
repair = ASTRepairMechanism()
fixed_algo, was_fixed, repairs = repair.repair(algo)
print(f"Se puede reparar: {was_fixed}")
print(f"Tipos de reparación: {repairs}")
```

---

## 📊 Resumen de Componentes

| Componente | Clase | Función |
|-----------|-------|---------|
| **Generar** | `AlgorithmGenerator` | Crear AST aleatorios |
| **Validar** | `ASTValidator` | Verificar restricciones |
| **Reparar** | `ASTRepairMechanism` | Fijar AST inválidos |
| **Normalizar** | `ASTNormalizer` | Simplificar AST |
| **Ejecutar** | `ASTInterpreter` | Correr AST en instancia |
| **Analizar** | `ASTStatistics` | Extraer métricas |

---

## ✅ Checklist para Usar GAA

- [ ] Importar módulos GAA necesarios
- [ ] Generar o crear algoritmo AST
- [ ] Validar con ASTValidator
- [ ] Reparar si hay violaciones
- [ ] Cargar instancia VRPTW
- [ ] Ejecutar con ASTInterpreter
- [ ] Verificar factibilidad y costo
- [ ] Guardar/serializar si es necesario

---

**Última actualización:** 2025-01-09  
**Versión:** 1.0  
**Estado:** ✅ Listo para usar
