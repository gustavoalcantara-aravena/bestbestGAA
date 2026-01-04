# 🔗 GUÍA DE INTEGRACIÓN - FLUJO COMPLETO BKS + VALIDATION + EXPERIMENT RUNNER

## Diagrama de Flujo

```
CONFIG (config.yaml)
    ↓
ExperimentRunner
    ├─→ BKSLoader.load("data/bks.json")
    │   └─→ BKSEntry("C101", k=10, d=828.94)
    │
    ├─→ Para cada instancia:
    │   ├─ GRASP.solve(instance)
    │   │   └─→ Solution {n_vehicles, total_distance}
    │   │
    │   ├─ validate_solution_vs_bks()
    │   │   └─→ BKSComparison {gap, dominates, ...}
    │   │
    │   └─ Logger.log_jsonl()
    │       └─→ {"timestamp", "gap_percent", "feasible", ...}
    │
    └─→ compute_aggregate_statistics()
        └─→ {avg_gap, dominates_count, ...}
```

---

## 1. CARGA DE CONFIGURACIÓN

**Archivo:** `config/config.yaml`

```yaml
project:
  name: "GRASP-GAA-VRPTW"

random:
  global_seed: 42
  deterministic: true

dataset:
  root_dir: "data/Solomon-VRPTW-Dataset/"
  families: [C1, C2, R1, R2, RC1, RC2]

bks:
  file: "data/best_known_solutions.json"  # ← BKSLoader lee desde aquí

evaluation:
  design_set: [R1, C1]
  selection_set: [RC1]
  evaluation_set: [R2, C2, RC2]

logging:
  format: "JSONL"
  output_dir: "logs/"
```

---

## 2. INICIALIZACIÓN DE BKS LOADER

**Código:**

```python
from evaluation.bks_loader import BKSLoader

# Cargar BKS desde JSON
bks_loader = BKSLoader("data/best_known_solutions.json")

# Acceso individual
bks = bks_loader.get("C101")
print(f"C101 BKS: {bks.n_vehicles} vehículos, {bks.total_distance:.2f} distancia")

# Validar que todas las instancias necesarias tienen BKS
required_instances = ["C101", "C102", "R101", "RC101"]
bks_loader.validate_all_present(required_instances)

# Estadísticas
print(bks_loader.stats())
# {
#   "total_instances": 56,
#   "min_vehicles": 9,
#   "max_vehicles": 12,
#   "avg_vehicles": 10.3,
#   ...
# }
```

### Formato de archivo BKS (JSON)

```json
{
  "C101": {
    "k": 10,
    "d": 828.94
  },
  "C102": {
    "k": 10,
    "d": 1092.37
  },
  "R101": {
    "k": 19,
    "d": 1645.79
  },
  ...
}
```

O alternativo (CSV):

```csv
instance_id,k,d
C101,10,828.94
C102,10,1092.37
R101,19,1645.79
```

---

## 3. VALIDACIÓN DE SOLUCIONES

**Código:**

```python
from evaluation.bks_validation import validate_solution_vs_bks

# Simulación de solución generada por GRASP
solution_metrics = {
    "instance_id": "C101",
    "n_vehicles": 10,           # Mismo que BKS
    "total_distance": 820.50,   # Mejor que BKS (828.94)
    "feasible": True
}

# Obtener BKS
bks = bks_loader.get("C101")

# Validar
comparison = validate_solution_vs_bks(solution_metrics, bks)

# Resultados
print(comparison.summary_str())
# Output: ✓ MEJOR | C101 | V:10 (BKS:10) | D:820.50 (BKS:828.94) | Gap: -1.01%

print(comparison.to_dict())
# {
#   "instance_id": "C101",
#   "solution_vehicles": 10,
#   "solution_distance": 820.5,
#   "k_bks": 10,
#   "d_bks": 828.94,
#   "feasible": true,
#   "vehicles_gap": 0,
#   "distance_gap": -8.44,
#   "vehicles_gap_percent": 0.0,
#   "distance_gap_percent": -1.01,
#   "dominates_bks": true,
#   "lexicographic_comparison": 1
# }

if comparison.dominates_bks:
    print("✓ ¡Nueva mejor solución encontrada!")
```

---

## 4. VALIDACIÓN POR LOTES

```python
from evaluation.bks_validation import batch_validate_solutions

# Múltiples soluciones
solutions = [
    {"instance_id": "C101", "n_vehicles": 10, "total_distance": 820.5},
    {"instance_id": "C102", "n_vehicles": 10, "total_distance": 1080.0},
    {"instance_id": "R101", "n_vehicles": 19, "total_distance": 1650.0},
]

# Validar todas
comparisons = batch_validate_solutions(solutions, bks_loader)

# Iterar resultados
for cmp in comparisons:
    print(cmp.summary_str())

# Estadísticas agregadas
from evaluation.bks_validation import compute_aggregate_statistics

stats = compute_aggregate_statistics(comparisons)
print(f"Instancias que mejoran BKS: {stats['dominates_count']}")
print(f"Gap promedio: {stats['avg_distance_gap_percent']:.2f}%")
print(f"Factibilidad: {stats['feasible_percent']:.1f}%")
```

---

## 5. EXPERIMENT RUNNER - FLUJO COMPLETO

**Código:**

```python
from src.experiment_runner import ExperimentRunner

# Inicializar
runner = ExperimentRunner(config_path="config/config.yaml")

# Ejecutar experimento completo
results = runner.run_experiment()

# Resultados
print(results)
# {
#   "experiment_id": "abc12345",
#   "timestamp": "2026-01-04T14:30:00",
#   "total_runs": 56,
#   "successful_runs": 55,
#   "failed_runs": 1,
#   "results_by_instance": {
#     "C101": {...},
#     "C102": {...},
#     ...
#   },
#   "aggregate_stats": {
#     "total_instances": 56,
#     "feasible_count": 55,
#     "feasible_percent": 98.21,
#     "dominates_count": 3,
#     "avg_gap_percent": 2.45,
#     "min_gap_percent": -1.01,
#     "max_gap_percent": 8.50
#   },
#   "duration_seconds": 324.5
# }
```

---

## 6. LOGGING JSONL

**Archivo generado:** `logs/experiment_20260104_143000.jsonl`

```jsonl
{"timestamp": "2026-01-04T14:30:02.123Z", "experiment_id": "abc12345", "instance_id": "C101", "algorithm_id": "GRASP-v1", "run_id": 1, "seed": 42, "solution_vehicles": 10, "solution_distance": 820.5, "k_bks": 10, "d_bks": 828.94, "feasible": true, "vehicles_gap": 0, "distance_gap": -8.44, "vehicles_gap_percent": 0.0, "distance_gap_percent": -1.01, "dominates_bks": true, "lexicographic_comparison": 1, "cpu_time_sec": 1.234, "status": "OK"}
{"timestamp": "2026-01-04T14:30:03.456Z", "experiment_id": "abc12345", "instance_id": "C102", "algorithm_id": "GRASP-v1", "run_id": 1, "seed": 42, "solution_vehicles": 10, "solution_distance": 1080.0, "k_bks": 10, "d_bks": 1092.37, "feasible": true, "vehicles_gap": 0, "distance_gap": -12.37, "vehicles_gap_percent": 0.0, "distance_gap_percent": -1.13, "dominates_bks": true, "lexicographic_comparison": 1, "cpu_time_sec": 1.567, "status": "OK"}
...
```

---

## 7. CLASE BKSComparison - TODOS LOS CAMPOS

```python
@dataclass
class BKSComparison:
    instance_id: str                        # "C101"
    solution_vehicles: int                  # 10
    solution_distance: float                # 820.50
    bks_vehicles: int                       # 10
    bks_distance: float                     # 828.94
    feasible: bool                          # True
    vehicles_gap: int                       # 0 (sol - bks)
    distance_gap: float                     # -8.44 (sol - bks)
    vehicles_gap_percent: float             # 0.0
    distance_gap_percent: float             # -1.01
    dominates_bks: bool                     # True (lexicografico)
    lexicographic_comparison: int           # 1 (1=mejor, 0=igual, -1=peor)
    
    def to_dict() → Dict                    # Serializar para JSONL
    def summary_str() → str                 # Resumen legible
```

---

## 8. FLUJO PASO A PASO (ExperimentRunner)

```python
# 1. CONFIGURACIÓN
config = load_yaml("config/config.yaml")

# 2. BKS LOADER
bks_loader = BKSLoader(config["bks"]["file"])

# 3. PARA CADA INSTANCIA
for instance_id in ["C101", "C102", ...]:
    
    # 3.1 Obtener BKS
    bks = bks_loader.get(instance_id)
    
    # 3.2 Ejecutar GRASP (TODO: integrar solver real)
    solution = grasp_solver.solve(instance_id)
    # solution = {
    #     "n_vehicles": 10,
    #     "total_distance": 820.5
    # }
    
    # 3.3 Crear métricas
    solution_metrics = {
        "instance_id": instance_id,
        "n_vehicles": solution["n_vehicles"],
        "total_distance": solution["total_distance"],
        "feasible": solution.get("feasible", True)
    }
    
    # 3.4 Validar vs BKS
    comparison = validate_solution_vs_bks(solution_metrics, bks)
    
    # 3.5 Preparar log JSONL
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "experiment_id": runner.experiment_id,
        **comparison.to_dict(),
        "cpu_time_sec": solution.get("cpu_time", 0),
        "status": "OK" if comparison.feasible else "INFEASIBLE"
    }
    
    # 3.6 Guardar log
    logger.log_jsonl(log_entry)

# 4. ESTADÍSTICAS AGREGADAS
stats = compute_aggregate_statistics(all_comparisons)
print(f"Gap promedio: {stats['avg_distance_gap_percent']:.2f}%")
```

---

## 9. INTEGRACIÓN CON GRASP SOLVER (TODO)

```python
# En experiment_runner.py, reemplazar:

# ACTUAL (simulación):
solution_metrics = {
    "instance_id": instance_id,
    "n_vehicles": bks_entry.n_vehicles - 1,
    "total_distance": bks_entry.total_distance * 0.95,
    "feasible": True
}

# FUTURO (solver real):
from grasp.grasp_solver import GRASPSolver

solver = GRASPSolver(config=self.config)
solution = solver.solve(instance_id)

solution_metrics = {
    "instance_id": instance_id,
    "n_vehicles": solution.n_vehicles,
    "total_distance": solution.total_distance,
    "feasible": solution.is_feasible()
}
```

---

## 10. EJEMPLO COMPLETO (main.py)

```python
#!/usr/bin/env python3
"""
Ejecutor principal del experimento GRASP-GAA-VRPTW
"""

from src.experiment_runner import ExperimentRunner
import sys

def main():
    try:
        runner = ExperimentRunner(config_path="config/config.yaml")
        results = runner.run_experiment()
        
        # Resumen final
        print("\n" + "="*70)
        print("RESULTADOS FINALES")
        print("="*70)
        stats = results["aggregate_stats"]
        print(f"Total instancias:          {stats['total_instances']}")
        print(f"Factibles:                 {stats['feasible_count']} ({stats['feasible_percent']:.1f}%)")
        print(f"Mejoran BKS:               {stats['dominates_count']}")
        print(f"Gap promedio:              {stats['avg_gap_percent']:.2f}%")
        print(f"Tiempo total:              {results['duration_seconds']:.1f}s")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## 11. CHECKLIST DE IMPLEMENTACIÓN

- [x] `BKSLoader` - Cargar JSON/CSV
- [x] `BKSEntry` - Representación de una entrada BKS
- [x] `BKSComparison` - Resultado de comparación
- [x] `validate_solution_vs_bks()` - Validación individual
- [x] `batch_validate_solutions()` - Validación por lotes
- [x] `compute_aggregate_statistics()` - Estadísticas agregadas
- [x] `ExperimentRunner` - Orquestador principal
- [ ] Integración con `GRASPSolver` (pendiente)
- [ ] Integración con `ASTGenerator` (pendiente)
- [ ] Tests unitarios (pendiente)

---

**Status:** 🟢 **Infraestructura BKS + Validation lista para usar**

**Próximo paso:** Integrar con GRASPSolver y ASTGenerator
