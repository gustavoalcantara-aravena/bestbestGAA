---
title: "Estructura de Outputs y Compatibilidad"
version: "1.0.0"
created: "2026-01-01"
---

# 9️⃣ ESTRUCTURA DE OUTPUTS

**Documento**: Outputs y Estructura  
**Contenido**: OutputManager, CSV canónico, directorios, compatibilidad

---

## Principio Central

Todos los outputs van a una **ÚNICA carpeta raíz** `output/`, donde **cada ejecución crea su propia subcarpeta con timestamp único**.

**Formato timestamp**: `DD-MM-YY_HH-MM-SS` (ejemplo: `01-01-26_14-23-45`)

---

## Estructura de Directorios

```
output/
├── 01-01-26_14-23-45/           # Ejecución 1 (QUICK o FULL)
│   ├── results/
│   │   ├── raw_results.csv
│   │   ├── convergence_trace.csv
│   │   ├── summary_by_instance.csv
│   │   ├── summary_by_family.csv
│   │   ├── time_metrics.csv
│   │   └── experiment_metadata.json
│   ├── solutions/
│   │   ├── solutions.csv
│   │   └── time_windows_check.csv
│   ├── plots/
│   │   ├── convergence_K.png
│   │   ├── convergence_D.png
│   │   ├── gap_analysis.png
│   │   ├── [8-10 gráficos más]
│   │   └── route_visualization_*.png (12 o 56)
│   ├── gaa/
│   │   ├── generated_algorithms.json
│   │   ├── grammar_specification.txt
│   │   └── ast_nodes_trace.json
│   └── logs/
│       ├── execution.log
│       ├── errors.log
│       └── session_summary.txt
│
└── 01-01-26_15-30-20/           # Ejecución 2
    ├── results/
    ├── solutions/
    ├── plots/
    ├── gaa/
    └── logs/
```

---

## 8 Archivos CSV Canónicos

### 1. raw_results.csv

**Ubicación**: `results/raw_results.csv`  
**Una fila = Una ejecución independiente**

**Columnas Exactas**:

```
algorithm_id | instance_id | family | run_id | random_seed | 
K_final | D_final | K_BKS | D_BKS | delta_K | gap_distance | 
gap_percent | total_time_sec | iterations_executed | reached_K_BKS
```

**Tipos**:
- algorithm_id: str (ej: "GAA_Algorithm_1")
- instance_id: str (ej: "R101")
- family: str (ej: "R1")
- run_id: int (ej: 0)
- random_seed: int (ej: 42)
- K_final, K_BKS: int
- D_final, D_BKS, gap_distance, gap_percent, total_time_sec: float
- iterations_executed: int
- reached_K_BKS: bool

**Notas**:
- gap_distance y gap_percent = NA si K_final ≠ K_BKS
- reached_K_BKS = (K_final == K_BKS)

---

### 2. convergence_trace.csv

**Ubicación**: `results/convergence_trace.csv`  
**Una fila = Una iteración de una ejecución**

**Columnas**:

```
algorithm_id | instance_id | family | run_id | iteration | 
elapsed_time_sec | K_best_so_far | D_best_so_far | is_K_BKS
```

**Propósito**: Rastrear convergencia iteración por iteración

---

### 3. summary_by_instance.csv

**Ubicación**: `results/summary_by_instance.csv`  
**Una fila = (Algoritmo × Instancia)**

**Columnas**:

```
algorithm_id | instance_id | family | runs_total | 
K_best | K_mean | K_std | K_min | K_max | percent_runs_K_min | 
D_mean_at_K_min | D_std_at_K_min | gap_percent_mean | 
gap_percent_std | time_mean_sec
```

**Nota**: D_* solo si K_min == K_BKS

---

### 4. summary_by_family.csv

**Ubicación**: `results/summary_by_family.csv`  
**Una fila = (Algoritmo × Familia)**  
**Solo en modo FULL**

**Columnas**:

```
algorithm_id | family | instances_count | K_mean | 
percent_instances_K_BKS | gap_percent_mean | gap_percent_std | time_mean_sec
```

---

### 5. time_metrics.csv

**Ubicación**: `results/time_metrics.csv`  
**Una fila = Una ejecución**

**Columnas**:

```
algorithm_id | instance_id | family | run_id | time_to_K_min_sec | 
iteration_to_K_min | time_to_best_D_sec | iteration_to_best_D
```

---

### 6. solutions.csv

**Ubicación**: `solutions/solutions.csv`  
**Una fila = Una ruta de una solución final**

**Columnas**:

```
algorithm_id | instance_id | family | run_id | route_id | 
vehicle_load | route_distance | customer_sequence
```

**Ejemplo customer_sequence**: "0-12-5-8-0"

---

### 7. time_windows_check.csv

**Ubicación**: `solutions/time_windows_check.csv`  
**Una fila = Un cliente en una solución**  
**Solo para soluciones con K = K_BKS**

**Columnas**:

```
algorithm_id | instance_id | family | run_id | customer_id | 
arrival_time | window_start | window_end | slack_time
```

---

### 8. experiment_metadata.json

**Ubicación**: `results/experiment_metadata.json`

**Contenido Ejemplo**:

```json
{
  "experiment_date": "2026-01-01T14:23:45",
  "experiment_mode": "QUICK",
  "algorithm_count": 3,
  "dataset_name": "Solomon VRPTW",
  "families_used": ["R1"],
  "instances_total": 12,
  "stopping_criterion": "max_iterations=100",
  "max_time_per_instance": 60.0,
  "alpha_value": 0.15,
  "hardware_cpu": "Intel Core i7",
  "hardware_ram": "16GB",
  "os": "Windows 10",
  "python_version": "3.9.0",
  "code_version": "1.0.0"
}
```

---

## Clase OutputManager

### Pseudocódigo

```python
class OutputManager:
    """
    Gestor centralizado de outputs VRPTW-GRASP
    Garantiza estructura con timestamps
    """
    
    TIMESTAMP_FORMAT = "%d-%m-%y_%H-%M-%S"
    
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.session_dir = None
    
    def create_session(self):
        """Crear nueva sesión con timestamp"""
        timestamp = datetime.now().strftime(self.TIMESTAMP_FORMAT)
        self.session_dir = self.base_output_dir / timestamp
        
        # Crear subdirectorios
        (self.session_dir / "results").mkdir(parents=True)
        (self.session_dir / "solutions").mkdir(parents=True)
        (self.session_dir / "plots").mkdir(parents=True)
        (self.session_dir / "gaa").mkdir(parents=True)
        (self.session_dir / "logs").mkdir(parents=True)
    
    def save_raw_results(self, data: List[Dict]) -> str:
        """Guardar raw_results.csv"""
        filepath = self.session_dir / "results" / "raw_results.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def save_summary_by_instance(self, data: List[Dict]) -> str:
        """Guardar summary_by_instance.csv"""
        filepath = self.session_dir / "results" / "summary_by_instance.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    # Métodos similares para otros archivos...
    
    def get_session_dir(self) -> Path:
        """Retornar directorio de sesión"""
        return self.session_dir
```

---

## Patrón de Uso en Código

```python
from utils.output_manager import OutputManager

# Crear gestor
output_mgr = OutputManager(base_output_dir="output")

# Iniciar sesión (crea estructura con timestamp)
session_dir = output_mgr.create_session()
print(f"Session: {session_dir}")
# Output: output/01-01-26_14-23-45/

# Ejecutar experimentos y recolectar datos
raw_results = []
for algo in algorithms:
    for instance in instances:
        result = algo.run(instance)
        raw_results.append({
            'algorithm_id': algo.name,
            'instance_id': instance.name,
            'K_final': result.num_vehicles,
            'D_final': result.distance,
            # ... más campos
        })

# Guardar resultados
output_mgr.save_raw_results(raw_results)
output_mgr.save_summary_by_instance(aggregate(raw_results))
output_mgr.save_experiment_metadata(metadata)

print(f"Outputs en: {output_mgr.get_session_dir()}")
```

---

## Validación de Estructura

Después de cada ejecución:

```python
def validate_output_structure(session_dir: Path) -> bool:
    required_dirs = ['results', 'solutions', 'plots', 'gaa', 'logs']
    required_files = {
        'results': [
            'raw_results.csv',
            'summary_by_instance.csv',
            'experiment_metadata.json'
        ],
        'solutions': ['solutions.csv'],
    }
    
    # Validar directorios
    for dir_name in required_dirs:
        if not (session_dir / dir_name).exists():
            raise FileNotFoundError(f"Directorio faltante: {dir_name}")
    
    # Validar archivos
    for dir_name, files in required_files.items():
        for filename in files:
            filepath = session_dir / dir_name / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Archivo faltante: {filepath}")
    
    return True
```

---

## Compatibilidad con GAA-GCP-ILS-4

La estructura es **100% compatible** porque:

| Aspecto | Compatibilidad |
|--------|----------------|
| **Estructura base** | output/{timestamp}/ |
| **Timestamp format** | DD-MM-YY_HH-MM-SS |
| **OutputManager** | Unificado, reutilizable |
| **Directorios temáticos** | results/, solutions/, plots/, gaa/, logs/ |
| **Logging centralizado** | Mismo patrón |
| **Metadata JSON** | Mismo formato |

**Diferencias adaptadas a VRPTW**:
- Archivos CSV específicos para VRPTW (no GCP)
- Gráficos específicos para VRPTW (11 tipos canónicos, no coloración de nodos)
- Campos: K_final, D_final, K_BKS, ventanas de tiempo

---

## Resumen Final

| Aspecto | Detalles |
|--------|----------|
| **Carpeta raíz** | output/ |
| **Timestamp por ejecución** | DD-MM-YY_HH-MM-SS |
| **Subdirectorios** | 5 (results, solutions, plots, gaa, logs) |
| **Archivos CSV** | 8 (columnas exactas) |
| **Gráficos canónicos** | 11 tipos |
| **Reproducibilidad** | seed=42, timestamps, metadata |
| **Escalabilidad** | Múltiples ejecuciones aisladas |

---

**Volver a**: [INDEX.md](INDEX.md)

---

## Documento Finalizado

Este es el último documento de la serie. Los 9 documentos forman una **documentación completa, modular y coherente** del proyecto VRPTW-GRASP, sin perder información pero mejorando significativamente la legibilidad.

**Total de Documentos**:
- INDEX.md (guía de navegación)
- 01-problema-vrptw.md
- 02-modelo-matematico.md
- 03-operadores-dominio.md
- 04-metaheuristica-grasp.md
- 05-datasets-solomon.md
- 06-experimentos-plan.md
- 07-fitness-canonico.md
- 08-metricas-canonicas.md
- 09-outputs-estructura.md

**Total: 10 documentos** (1 índice + 9 temáticos)
