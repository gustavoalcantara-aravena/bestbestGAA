---
title: "Plan Experimental y GAA"
version: "1.0.0"
created: "2026-01-01"
---

# 6️⃣ PLAN EXPERIMENTAL Y GAA

**Documento**: Experimentos  
**Contenido**: Dos modos (QUICK/FULL), generación de algoritmos, dimensiones experimentales

---

## Visión General

El plan experimental sigue un **enfoque de dos modos**:

1. **QUICK Mode**: Validación rápida (1 familia Solomon, ~5-10 minutos)
2. **FULL Mode**: Evaluación exhaustiva (6 familias Solomon, ~40-60 minutos)

**Generación de Algoritmos**: 3 algoritmos automáticos **UNA SOLA VEZ** (seed=42), reutilizados en ambos modos.

---

## Modo QUICK (Validación Rápida)

### Propósito
- Validar funcionamiento del sistema GAA
- Verificar estructura de datos y outputs
- Estimación de tiempos antes de experimento full

### Cobertura

```
Familias: 1 (típicamente R1)
Instancias: 12 (R101-R112)
Algoritmos: 3 (GAA_Algorithm_1, 2, 3)
Repeticiones: 1 por (instancia, algoritmo)
Experimentos: 12 × 3 × 1 = 36
Tiempo estimado: 5-10 minutos
```

### Script

```bash
# Ubicación: scripts/demo_experimentation_quick.py
python scripts/demo_experimentation_quick.py

# Salida:
# output/vrptw_experiments_QUICK_DDMMYY_HHMMSS/
#   ├── results/
#   │   ├── raw_results.csv
#   │   ├── summary_by_instance.csv
#   │   └── experiment_metadata.json
#   ├── plots/
#   │   ├── gap_comparison.png
#   │   ├── convergence.png
#   │   └── routes_detailed_R101.png (12 en total)
#   └── logs/
```

---

## Modo FULL (Evaluación Exhaustiva)

### Propósito
- Análisis completo de robustez
- Comparación inter-familias
- Identificación de especialización

### Cobertura

```
Familias: 6 (C1, C2, R1, R2, RC1, RC2)
Instancias: 56 totales
  - C1: 9
  - C2: 8
  - R1: 12
  - R2: 11
  - RC1: 8
  - RC2: 8

Algoritmos: 3 (mismos que QUICK, seed=42)
Repeticiones: 1 por (instancia, algoritmo)
Experimentos: 56 × 3 × 1 = 168
Tiempo estimado: 40-60 minutos
```

### Script

```bash
# Ubicación: scripts/demo_experimentation_full.py
python scripts/demo_experimentation_full.py

# Salida:
# output/vrptw_experiments_FULL_DDMMYY_HHMMSS/
#   ├── results/
#   │   ├── raw_results.csv (168 filas)
#   │   ├── summary_by_instance.csv
#   │   ├── summary_by_family.csv
#   │   └── experiment_metadata.json
#   ├── plots/
#   │   ├── [8 gráficos estadísticos]
#   │   ├── [3 gráficos por familia]
#   │   └── [56 gráficos de rutas]
#   └── logs/
```

---

## Generación de Algoritmos (UNA SOLA VEZ)

### Proceso

Antes de ejecutar cualquier experimento, generar 3 algoritmos automáticos:

```python
# Pseudocódigo
from gaa import AlgorithmGenerator

generator = AlgorithmGenerator(
    grammar=vrptw_grasp_grammar,
    min_depth=2,
    max_depth=3,
    seed=42  # ← Reproducibilidad
)

algorithms = []
for i in range(3):
    ast = generator.generate_with_validation()
    algorithms.append({
        'id': f'GAA_Algorithm_{i+1}',
        'ast': ast,
        'pseudocode': ast.to_pseudocode(),
        'validation': ast.validate_restrictions()
    })

# Guardar en algorithms/
save_algorithms(algorithms)
```

### Duración
Negligible (~< 1 segundo)

### Reutilización
Los mismo 3 algoritmos se usan en QUICK y FULL

---

## Restricciones Canónicas de Operadores

Para que algoritmo generado sea válido:

### 1️⃣ Constructor Randomizado (Obligatorio)
Exactamente 1 de:
- `RandomizedInsertion(alpha)` ✅ Preferido
- `TimeOrientedNN`
- `RegretInsertion`
- `NearestNeighbor` (básico)

### 2️⃣ Operadores de Mejora (Mínimo 2)
Combinación de:
- **Intra-ruta**: TwoOpt, OrOpt, ThreeOpt, Relocate
- **Inter-ruta**: CrossExchange, TwoOptStar, SwapCustomers, RelocateInter

Recomendado: 1 intra-ruta + 1 inter-ruta

### 3️⃣ Criterio de Iteración (Obligatorio)
Exactamente 1 de:
- `ApplyUntilNoImprove(max_stagnation=k)`
- `ChooseBestOf(n_iterations)` ✅ Preferido para GRASP
- `For(fixed_iterations)`

### 4️⃣ Reparación (Recomendada)
Si hay restricciones violadas:
- `RepairTimeWindows` ✅ Crítica
- `RepairCapacity` ✅ Crítica
- `GreedyRepair`

---

## Ejemplo de Algoritmo Válido

```json
{
  "name": "GAA_Algorithm_1",
  "structure": {
    "type": "ChooseBestOf",
    "n": 100,
    "body": {
      "type": "Seq",
      "statements": [
        {
          "type": "Call",
          "operator": "RandomizedInsertion",
          "params": {"alpha": 0.15}
        },
        {
          "type": "ApplyUntilNoImprove",
          "operator": "TwoOpt",
          "max_stagnation": 5
        },
        {
          "type": "ApplyUntilNoImprove",
          "operator": "SwapCustomers",
          "max_stagnation": 3
        },
        {
          "type": "Call",
          "operator": "RepairTimeWindows"
        }
      ]
    }
  },
  "validation": {
    "has_randomized_constructor": true,
    "num_improvement_operators": 2,
    "has_repair": true,
    "is_valid": true
  }
}
```

---

## Variables Independientes

| Variable | Descripción | Valores |
|----------|-------------|---------|
| **Algoritmo** | GAA-generado | 3 variantes |
| **Familia** | Solomon | C1, C2, R1, R2, RC1, RC2 |
| **Instancia** | Específica dentro familia | 56 totales |
| **Repetición** | Ejecución independiente | 1 (determinística con seed) |

---

## Variables Dependientes

### Métricas de Calidad

- **K_final**: Número vehículos alcanzado
- **D_final**: Distancia total
- **K_BKS**: Número vehículos óptimo conocido
- **D_BKS**: Distancia óptima conocida
- **Gap en distancia**: (D_final - D_BKS) / D_BKS × 100 % (solo si K=K_BKS)

### Métricas de Rendimiento

- **time_total_sec**: Tiempo ejecución total
- **iterations_executed**: Iteraciones GRASP completadas
- **time_to_K_BKS**: Tiempo hasta alcanzar K óptimo

### Métricas de Validez

- **violations_capacity**: Número de violaciones (debe ser 0)
- **violations_time**: Número de violaciones (debe ser 0)
- **feasible**: Booleano

---

## Matriz de Ejecución

```
QUICK:  R1 (12) × 3 algoritmos × 1 rep = 36 experimentos
        Tiempo: 5-10 minutos
        
FULL:   (C1:9 + C2:8 + R1:12 + R2:11 + RC1:8 + RC2:8) × 3 × 1 = 168
        Tiempo: 40-60 minutos
```

---

## Presupuesto Computacional

### Por Algoritmo × Instancia

- **Construcción GRASP**: O(n²)
- **VND búsqueda local**: O(n⁴)
- **Iteraciones**: 100 máximo
- **Tiempo**: ~0.5-1 segundo

### Total por Instancia

```
Tiempo = 3 algoritmos × 1 segundo = 3 segundos
(En paralelo: 1 segundo secuencial)
```

### QUICK: 12 instancias

```
12 × 3 algoritmos × 1 segundo = 36 segundos
Tempo total: ~5-10 minutos (con I/O, logging)
```

### FULL: 56 instancias

```
56 × 3 algoritmos × 1 segundo = 168 segundos
Tiempo total: ~40-60 minutos (con I/O, logging, análisis)
```

---

## Flujo de Ejecución Recomendado

```
1. python scripts/generate_algorithms.py
   └─ Genera 3 algoritmos (seed=42)
   └─ Guarda en algorithms/

2. python scripts/demo_experimentation_quick.py
   └─ Valida funcionamiento (5-10 min)
   └─ Si OK: continuar

3. python scripts/demo_experimentation_full.py
   └─ Experimento exhaustivo (40-60 min)
   └─ Genera todos outputs y análisis
```

---

## Validación de Estructura

Después de cada ejecución, validar:

```python
def validate_experiment_structure(output_dir):
    required_files = [
        'results/raw_results.csv',
        'results/summary_by_instance.csv',
        'results/summary_by_family.csv' if 'FULL' else None,
        'plots/convergence.png',
        'plots/gap_analysis.png',
        'logs/execution.log'
    ]
    
    for file in required_files:
        assert (output_dir / file).exists()
    
    return True
```

---

**Siguiente documento**: [07-fitness-canonico.md](07-fitness-canonico.md)  
**Volver a**: [INDEX.md](INDEX.md)
