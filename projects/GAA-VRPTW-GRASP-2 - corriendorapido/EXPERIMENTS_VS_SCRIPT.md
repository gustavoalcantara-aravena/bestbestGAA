# Aclaración: ¿Qué es experiments.py vs script_full.py?

## 🎯 La Respuesta Rápida

**NO son idénticas**. La relación es:

```
experiments.py (330 líneas)
    ├── Clases base para experimentos
    ├── Lógica de configuración y ejecución
    └── 2 implementaciones: QuickExperiment y FullExperiment
                │
                └─→ script_full.py solo LLAMA a FullExperiment.run()
                    (es un wrapper, no la implementación)
```

---

## 📊 Desglose de `experiments.py`

El archivo tiene **5 componentes principales**:

### **1. ExperimentConfig (Líneas 20-35)**
```python
@dataclass
class ExperimentConfig:
    mode: str                    # 'QUICK' o 'FULL'
    families: List[str]          # Cuales familias
    algorithms: List[str]        # Cuales algoritmos
    repetitions: int = 1         # Cuántas repeticiones
    seed: int = 42
    timeout_sec: int = 600
```

**Propósito**: Define parámetros de ejecución (configuración)

---

### **2. AlgorithmGenerator (Líneas 38-97)**
```python
class AlgorithmGenerator:
    def generate_algorithms(num_algorithms: int = 3) -> List[str]:
        # Genera algoritmos GAA automáticamente
        # Guarda en carpeta 'algorithms/'
        # Retorna lista de IDs
```

**Propósito**: Generar algoritmos una sola vez (seed=42)

---

### **3. ExperimentExecutor (Líneas 100-220)**
```python
class ExperimentExecutor:
    def __init__(config):
        # Crea estructura de output
        # output/vrptw_experiments_QUICK_02-01-26_14-30-45/
        #   ├── results/
        #   ├── plots/
        #   └── logs/
    
    def add_result():
        # Acumula un resultado en memoria
    
    def get_solomon_instances(families):
        # Retorna qué instancias corresponden a cada familia
    
    def save_raw_results():
        # Guarda CSV con todos los resultados
    
    def save_experiment_metadata():
        # Guarda JSON con metadatos
```

**Propósito**: Orquesta la ejecución y guarda resultados

---

### **4. QuickExperiment (Líneas 223-275)**
```python
class QuickExperiment:
    @staticmethod
    def get_config() -> ExperimentConfig:
        return ExperimentConfig(
            mode='QUICK',
            families=['R1'],                    # ← 1 familia
            algorithms=['GAA_Algorithm_1', ...], # ← 3 algoritmos
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        # 1. Crea executor con config QUICK
        # 2. Itera sobre R1 × 3 algoritmos
        # 3. Simula experimentos (mock data)
        # 4. Llama a save_raw_results()
        # 5. Llama a save_experiment_metadata()
        # Retorna executor
```

**Propósito**: Implementación específica para QUICK (36 experimentos)

---

### **5. FullExperiment (Líneas 278-330)**
```python
class FullExperiment:
    @staticmethod
    def get_config() -> ExperimentConfig:
        return ExperimentConfig(
            mode='FULL',
            families=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],  # ← 6 familias
            algorithms=['GAA_Algorithm_1', ...],  # ← 3 algoritmos
            repetitions=1,
            seed=42
        )
    
    @staticmethod
    def run():
        # 1. Crea executor con config FULL
        # 2. Itera sobre 6 familias × 3 algoritmos
        # 3. Simula experimentos (mock data)
        # 4. Llama a save_raw_results()
        # 5. Llama a save_experiment_metadata()
        # Retorna executor
```

**Propósito**: Implementación específica para FULL (168 experimentos)

---

## 🔗 Relación: experiments.py vs script_full.py

```
experiments.py (La "fábrica")
    │
    ├─ Define clases base
    ├─ Define FullExperiment.run()  ← Implementación real
    │
    └──────────────────────┐
                           │
                           ↓
                    script_full.py (El "wrapper")
                           │
                           ├─ Importa: FullExperiment, AlgorithmGenerator
                           ├─ Llama: AlgorithmGenerator().generate_algorithms(3)
                           ├─ Llama: FullExperiment.run()
                           └─ Imprime resultados
```

---

## 📋 DIFERENCIAS CLAVE

| Aspecto | experiments.py | script_full.py |
|---------|-----------------|-----------------|
| **Qué es** | Módulo con clases | Script ejecutable |
| **Líneas** | 330 líneas | ~50 líneas |
| **Define** | Toda la lógica | Solo orquesta |
| **Puede usarse** | Importado por otros scripts | Directo: `python script_full.py` |
| **Funcionalidades** | 100% (todas las clases) | Solo 2: AlgorithmGenerator + FullExperiment |

---

## ✅ LO QUE HACE `script_full.py`

```python
# 1. Importa clases de experiments.py
from scripts.experiments import FullExperiment, AlgorithmGenerator

# 2. Crea generador
gen = AlgorithmGenerator(seed=42)

# 3. Genera 3 algoritmos
algorithms = gen.generate_algorithms(num_algorithms=3)

# 4. Ejecuta FullExperiment (que internamente):
#    - Crea ExperimentConfig con 6 familias
#    - Crea ExperimentExecutor
#    - Itera sobre 56 instancias × 3 algoritmos
#    - Simula experimentos
#    - Guarda CSV y JSON

executor = FullExperiment.run()

# 5. Imprime resultados
```

---

## 🔍 FUNCIONALIDADES DE `experiments.py` QUE USA `script_full.py`

✅ **SÍ utiliza**:
1. `AlgorithmGenerator.generate_algorithms()` - Genera 3 algoritmos
2. `FullExperiment.get_config()` - Define 6 familias
3. `FullExperiment.run()` - Ejecuta 168 experimentos
4. `ExperimentExecutor` (internamente en FullExperiment.run())
   - Crea estructura de carpetas
   - Llama `add_result()` para cada experimento
   - Llama `save_raw_results()`
   - Llama `save_experiment_metadata()`

❌ **NO utiliza** (pero existen en experiments.py):
1. `QuickExperiment` - Eso es diferente
2. `ExperimentConfig` directamente - Se crea internamente en FullExperiment
3. `get_solomon_instances()` directamente - Se llama internamente

---

## 🎯 RESUMEN

**¿script_full.py corre TODAS las funcionalidades de experiments.py?**

**NO, pero:**
- ✅ Corre TODAS las funcionalidades **de FullExperiment**
- ✅ Usa las clases bases de `experiments.py`
- ✅ No corre **QuickExperiment** (eso sería script_quick.py)
- ✅ No corre código en el `if __name__ == "__main__"` de experiments.py

**Es como:**
```
experiments.py = La biblioteca / toolkit
script_full.py = Un programa que UTILIZA esa biblioteca para hacer FULL

La relación es:
- experiments.py contiene TODO el código
- script_full.py solo LLAMA a partes específicas de experiments.py
```

---

## 💡 ANALOGÍA

```
experiments.py  = Caja de herramientas (destornillador, martillo, sierra)
script_full.py  = Un proyecto que usa SOLO sierra + martillo
script_quick.py = Un proyecto que usa SOLO destornillador + martillo
```

No necesitas usar la caja completa cada vez.

---

## 🚀 SI QUISIERAS EJECUTAR TODAS LAS FUNCIONALIDADES DE experiments.py

Tendrías que ejecutar:

```python
# script_run_all.py
from scripts.experiments import QuickExperiment, FullExperiment, AlgorithmGenerator

# Generar algoritmos (una vez)
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(3)

# Ejecutar QUICK
print("Ejecutando QUICK...")
quick_executor = QuickExperiment.run()
print(f"  ✓ {len(quick_executor.raw_results)} experimentos")

# Ejecutar FULL
print("Ejecutando FULL...")
full_executor = FullExperiment.run()
print(f"  ✓ {len(full_executor.raw_results)} experimentos")

# Total: 36 + 168 = 204 experimentos
```

Pero eso tomaría 20-30 minutos.

---

## ✨ CONCLUSIÓN

```
experiments.py      = Infraestructura (todas las clases)
script_quick.py     = Ejecuta QuickExperiment (36 exp)
script_custom.py    = Ejecuta ExperimentExecutor custom (24-36 exp)
script_full.py      = Ejecuta FullExperiment (168 exp)
```

**script_full.py corre las funcionalidades que necesita de experiments.py, pero no todas.**

¿Necesitas algo más específico? 🎯
