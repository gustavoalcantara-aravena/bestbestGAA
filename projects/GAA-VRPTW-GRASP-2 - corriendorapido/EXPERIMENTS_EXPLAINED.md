# EXPLICACIÓN DETALLADA: experiments.py

**Archivo**: `scripts/experiments.py` (330 líneas)  
**Propósito**: Es LA BASE del framework de experimentación  
**Status**: ✅ Completamente funcional

---

## 🎯 ¿QUÉ HACE ESTE CÓDIGO?

```
experiments.py = INFRAESTRUCTURA PARA EJECUTAR EXPERIMENTOS A ESCALA

Permite:
  ✓ Generar algoritmos automáticamente
  ✓ Configurar experimentos (qué instancias, cuántas repeticiones, etc.)
  ✓ Ejecutar múltiples experimentos
  ✓ Guardar resultados en CSV
  ✓ Almacenar metadatos en JSON
```

---

## 📋 COMPONENTES PRINCIPALES

### **1. ExperimentConfig (Líneas 20-35)**

```python
@dataclass
class ExperimentConfig:
    mode: str                    # 'QUICK' o 'FULL'
    families: List[str]          # Qué familias ejecutar: ['C1'], ['R1', 'C1'], etc.
    algorithms: List[str]        # Qué algoritmos: ['GAA_Algorithm_1', ...]
    repetitions: int = 1         # Cuántas veces cada combo
    seed: int = 42               # Para reproducibilidad
    timeout_sec: int = 600       # 10 minutos máximo por experimento
```

**¿Para qué sirve?**
- Define los parámetros de un experimento
- Es como una "receta": qué ingredientes usar

**Ejemplo**:
```python
config = ExperimentConfig(
    mode='QUICK',
    families=['R1'],
    algorithms=['GAA_1', 'GAA_2', 'GAA_3'],
    repetitions=1,
    seed=42
)
# "Voy a ejecutar 36 experimentos: 12 instancias × 3 algoritmos × 1 repetición"
```

---

### **2. AlgorithmGenerator (Líneas 38-97)**

```python
class AlgorithmGenerator:
    def __init__(self, seed: int = 42, output_dir: str = "algorithms"):
        # Inicializa el generador con seed para reproducibilidad
    
    def generate_algorithms(self, num_algorithms: int = 3) -> List[str]:
        # GENERA algoritmos automáticamente
        # Guarda en JSON: 'algorithms/GAA_Algorithm_1.json', etc.
        # Retorna: ['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3']
```

**¿Para qué sirve?**
- Crea algoritmos GAA automáticamente
- Cada uno tiene parámetros aleatorios pero reproducibles (seed=42)
- Guarda metadata de cada algoritmo en JSON

**Ejemplo**:
```python
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(num_algorithms=3)
# Resultado: ['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3']
# Archivos creados:
#   - algorithms/GAA_Algorithm_1.json
#   - algorithms/GAA_Algorithm_2.json
#   - algorithms/GAA_Algorithm_3.json
```

**¿Qué contiene cada JSON?**
```json
{
  "algorithm_id": "GAA_Algorithm_1",
  "seed": 42,
  "version": "1.0",
  "components": {
    "construction": "ConstructionHeuristic_1",
    "local_search": "LocalSearch_1",
    "parameters": {
      "alpha": 0.32,
      "beta": 0.78,
      "max_iterations": 150
    }
  },
  "description": "Auto-generated GAA algorithm #1 with seed=42"
}
```

---

### **3. ExperimentExecutor (Líneas 100-220)**

```python
class ExperimentExecutor:
    def __init__(self, config: ExperimentConfig):
        # Crea estructura de carpetas
        # output/vrptw_experiments_QUICK_02-01-26_03-14-54/
        #   ├── results/
        #   ├── plots/
        #   └── logs/
    
    def get_solomon_instances(self, families):
        # Retorna qué instancias pertenecen a cada familia
        # C1 → [C101, C102, C103, ..., C109]
        # R1 → [R101, R102, ..., R112]
    
    def add_result(self, algorithm_id, instance_id, family, ...):
        # ACUMULA un resultado en memoria
        # Cada resultado es: algoritmo × instancia × repetición = 1 fila
    
    def save_raw_results(self):
        # Guarda TODAS las filas acumuladas en un CSV
        # raw_results.csv con 36 (o 168) filas
    
    def save_experiment_metadata(self):
        # Guarda información sobre la ejecución en JSON
```

**¿Para qué sirve?**
- Orquesta toda la ejecución
- Crea estructura de carpetas
- Acumula resultados
- Guarda archivos

**Workflow**:
```
ExperimentExecutor
    ↓
[Crea carpeta output/vrptw_experiments_QUICK_...]
    ↓
[Para cada experimento]:
  - Resuelve (simulado o real)
  - add_result()  ← Acumula en memoria
    ↓
[Al terminar]:
  - save_raw_results()  ← Escribe CSV
  - save_experiment_metadata()  ← Escribe JSON
```

---

### **4. QuickExperiment (Líneas 223-275)**

```python
class QuickExperiment:
    @staticmethod
    def get_config() -> ExperimentConfig:
        return ExperimentConfig(
            mode='QUICK',
            families=['R1'],                    # Solo R1
            algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        # 1. Crea config QUICK
        # 2. Crea executor
        # 3. Para cada instancia en R1:
        #    Para cada algoritmo:
        #      Simula experimento → add_result()
        # 4. save_raw_results() y save_experiment_metadata()
        # Retorna executor
```

**¿Para qué sirve?**
- Implementación específica para QUICK
- 1 familia (R1) × 12 instancias × 3 algoritmos = 36 experimentos

**Lo que hace**:
```
QuickExperiment.run()
    ↓
[Prepara config QUICK]
    ↓
[Itera sobre 36 combos]:
  R101 × GAA_1 → Simula → Guarda resultado
  R101 × GAA_2 → Simula → Guarda resultado
  R101 × GAA_3 → Simula → Guarda resultado
  R102 × GAA_1 → Simula → Guarda resultado
  ... (33 más)
    ↓
[Escribe CSV con 36 filas]
[Escribe JSON con metadatos]
```

---

### **5. FullExperiment (Líneas 278-330)**

```python
class FullExperiment:
    @staticmethod
    def get_config() -> ExperimentConfig:
        return ExperimentConfig(
            mode='FULL',
            families=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],  # 6 familias
            algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        # EXACTAMENTE igual a QuickExperiment.run()
        # pero con 6 familias en lugar de 1
```

**¿Para qué sirve?**
- Implementación específica para FULL
- 6 familias × 56 instancias × 3 algoritmos = 168 experimentos

---

## 🔄 FLUJO GENERAL

```
┌─────────────────────────────────────────────┐
│     experiments.py (Base Conceptual)        │
├─────────────────────────────────────────────┤
│                                             │
│  1. ExperimentConfig                        │
│     └─ Define parámetros del experimento    │
│                                             │
│  2. AlgorithmGenerator                      │
│     └─ Crea 3 algoritmos automáticamente    │
│                                             │
│  3. ExperimentExecutor                      │
│     ├─ Crea estructura de carpetas          │
│     ├─ Ejecuta experimentos                 │
│     ├─ Acumula resultados                   │
│     └─ Guarda CSV + JSON                    │
│                                             │
│  4. QuickExperiment / FullExperiment        │
│     └─ Implementaciones concretas           │
│                                             │
└─────────────────────────────────────────────┘
         ↓                           ↓
    script_quick.py            script_full.py
    (wrapper simple)            (wrapper simple)
```

---

## 📊 EJEMPLO PASO A PASO

### Paso 1: Importar y Generar Algoritmos

```python
from scripts.experiments import QuickExperiment, AlgorithmGenerator

gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(3)
# ✓ Se crean 3 algoritmos
# ✓ Se guardan en: algorithms/GAA_Algorithm_1.json, etc.
# Resultado: ['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3']
```

### Paso 2: Ejecutar Experimentos

```python
executor = QuickExperiment.run()
# ✓ Se crea config QUICK
# ✓ Se ejecutan 36 experimentos (R1 × 3 algoritmos)
# ✓ Se guardan resultados en memoria
# ✓ Se escribe CSV: raw_results.csv
# ✓ Se escribe JSON: experiment_metadata.json
# Resultado: executor con 36 filas de datos
```

### Paso 3: Acceder a Resultados

```python
# Los resultados están en memory:
for result in executor.raw_results:
    print(f"{result['algorithm_id']} on {result['instance_id']}: "
          f"Cost={result['D_final']:.1f}, BKS={result['reached_K_BKS']}")

# También están guardados en disco:
# output/vrptw_experiments_QUICK_02-01-26_03-14-54/results/raw_results.csv
```

---

## 🎯 ¿ES LA BASE DE LA EXPERIMENTACIÓN?

**SÍ, 100%**

Este código es:

✅ **Flexible**: Puedes cambiar `families`, `algorithms`, `repetitions`  
✅ **Modular**: Cada clase tiene responsabilidad específica  
✅ **Automatizado**: Genera algoritmos, ejecuta, guarda resultados  
✅ **Escalable**: Funciona igual para QUICK (36) o FULL (168)  
✅ **Reproducible**: Seed fijo (42) garantiza mismos resultados  

---

## 📈 ESTADÍSTICAS

Cuando ejecutas `QuickExperiment.run()`:

```
Input:
  - 3 algoritmos generados
  - 1 familia (R1 con 12 instancias)
  - 1 repetición por combo

Processing:
  - 12 instancias × 3 algoritmos × 1 repetición = 36 experimentos
  - Cada experimento genera 1 fila de datos

Output:
  - raw_results.csv: 36 filas × 15 columnas
  - experiment_metadata.json: información de la ejecución
  - Carpetas: results/, plots/, logs/
```

---

## 🚀 RESUMEN

| Componente | Qué Hace | Salida |
|-----------|----------|--------|
| **ExperimentConfig** | Define parámetros | Config object |
| **AlgorithmGenerator** | Crea algoritmos | 3 JSONs + lista de IDs |
| **ExperimentExecutor** | Ejecuta y guarda | Carpetas y archivos |
| **QuickExperiment** | Wrapper QUICK | 36 experimentos |
| **FullExperiment** | Wrapper FULL | 168 experimentos |

---

## 💡 ANALOGÍA

```
experiments.py es como UNA FÁBRICA:

- ExperimentConfig = Especificación (qué producir)
- AlgorithmGenerator = Diseñador (crea moldes)
- ExperimentExecutor = Máquinas (producen)
- QuickExperiment = Línea Express (36 unidades)
- FullExperiment = Línea Completa (168 unidades)
```

---

**Conclusión**: `experiments.py` es el **corazón del framework**. Todo lo demás depende de él. ✅

Cuando ejecutas `python script_quick.py`, en realidad solo estás:
1. Llamando a `AlgorithmGenerator.generate_algorithms()`
2. Llamando a `QuickExperiment.run()`
3. Imprimiendo resultados

La **lógica real** está en `experiments.py`. 🎯
