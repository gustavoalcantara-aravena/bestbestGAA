# Ejemplo de Documentación Generada Automáticamente

Cada vez que ejecutes `demo_experimentation_both_OPTIMIZED.py`, se generarán automáticamente 2 archivos en `output/execution_logs/`:

---

## 📄 Archivo 1: execution_log_{timestamp}.md

Este archivo Markdown contiene toda la información legible:

```markdown
# Execution Log: Multi-Group_Experimentation_OPTIMIZED

**Timestamp**: 20251226_140530
**Start Time**: 2025-12-26 14:05:30

---

## Environment Information

- **Python**: 3.10.12
- **Platform**: Linux-4.4.0-x86_64-with-glibc2.35
- **NumPy**: 1.26.4
- **Working Directory**: /home/user/bestbestGAA/projects/KBP-SA

## Git Information

- **Git Hash**: `fda7437a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q`
- **Branch**: `claude/debug-both-py-performance-HySBp`
- **Uncommitted Changes**: False

---

## Configuration Parameters

```json
{
  "seed": 123,
  "grammar_min_depth": 2,
  "grammar_max_depth": 3,
  "max_time_per_experiment_seconds": 5.0,
  "max_evaluations_sa": 2000,
  "repetitions_per_instance": 1,
  "num_algorithms": 3,
  "matplotlib_backend": "Agg",
  "optimization_version": "v2_with_timeout_5s"
}
```

---

## Algorithm: GAA_Algorithm_1

**Pseudocode:**

```
SECUENCIA:
  1. CONSTRUIR_VORAZ usando GreedyByValue
  2. APLICAR_HASTA_NO_MEJORAR (parada: Stagnation=20):
    LLAMAR FlipBestItem
```

---

## Algorithm: GAA_Algorithm_2

**Pseudocode:**

```
SECUENCIA:
  1. CONSTRUIR_VORAZ usando GreedyByWeight
  2. LLAMAR FlipWorstItem
```

---

## Algorithm: GAA_Algorithm_3

**Pseudocode:**

```
SECUENCIA:
  1. CONSTRUIR_VORAZ usando RandomConstruct
  2. MIENTRAS (presupuesto: 1000 iteraciones):
    SECUENCIA:
      1. BUSQUEDA_LOCAL en TwoExchange (aceptación: Improving)
      2. LLAMAR TwoExchange
```

---

### Step: Generating GAA Algorithms

**Time**: 14:05:31

**Details:**

```json
{
  "num_algorithms": 3,
  "seed": 123,
  "min_depth": 2,
  "max_depth": 3
}
```

### Step: Processing Low-Dimensional Group

**Time**: 14:05:32

### Result: Low-Dimensional Results

```json
{
  "best_algorithm": "GAA_Algorithm_2",
  "experiments_completed": "29/30",
  "json_file": "output/low_dimensional_experiments/experiment_low_dimensional_experiment_20251226_140530.json"
}
```

### Step: Processing Large-Scale Group

**Time**: 14:05:50

### Result: Large-Scale Results

```json
{
  "best_algorithm": "GAA_Algorithm_1",
  "experiments_completed": "55/63",
  "json_file": "output/large_scale_experiments/experiment_large_scale_experiment_20251226_140551.json"
}
```

---

## Execution Summary

- **Status**: ✅ Success
- **End Time**: 2025-12-26 14:06:15
- **Total Time**: 45.23s

**Configuration saved to**: `execution_config_20251226_140530.json`

### Algorithms Generated

- **GAA_Algorithm_1**
- **GAA_Algorithm_2**
- **GAA_Algorithm_3**

### Results Summary

```json
{
  "Low-Dimensional Results": {
    "best_algorithm": "GAA_Algorithm_2",
    "experiments_completed": "29/30",
    "json_file": "output/low_dimensional_experiments/experiment_low_dimensional_experiment_20251226_140530.json"
  },
  "Large-Scale Results": {
    "best_algorithm": "GAA_Algorithm_1",
    "experiments_completed": "55/63",
    "json_file": "output/large_scale_experiments/experiment_large_scale_experiment_20251226_140551.json"
  }
}
```

---

**Log completed at**: 2025-12-26 14:06:15
```

---

## 📄 Archivo 2: execution_config_{timestamp}.json

Este archivo JSON contiene toda la configuración programáticamente accesible:

```json
{
  "experiment_name": "Multi-Group_Experimentation_OPTIMIZED",
  "timestamp": "20251226_140530",
  "start_time": "2025-12-26T14:05:30.123456",
  "end_time": "2025-12-26T14:06:15.654321",
  "success": true,
  "total_execution_time_seconds": 45.23,
  "environment": {
    "python_version": "3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]",
    "platform": "Linux-4.4.0-x86_64-with-glibc2.35",
    "platform_system": "Linux",
    "platform_release": "4.4.0",
    "numpy_version": "1.26.4",
    "working_directory": "/home/user/bestbestGAA/projects/KBP-SA"
  },
  "git_info": {
    "git_hash": "fda7437a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q",
    "git_branch": "claude/debug-both-py-performance-HySBp",
    "has_uncommitted_changes": false,
    "git_status": "clean"
  },
  "parameters": {
    "seed": 123,
    "grammar_min_depth": 2,
    "grammar_max_depth": 3,
    "max_time_per_experiment_seconds": 5.0,
    "max_evaluations_sa": 2000,
    "repetitions_per_instance": 1,
    "num_algorithms": 3,
    "matplotlib_backend": "Agg",
    "optimization_version": "v2_with_timeout_5s"
  },
  "algorithms": [
    {
      "name": "GAA_Algorithm_1",
      "pseudocode": "SECUENCIA:\n  1. CONSTRUIR_VORAZ usando GreedyByValue\n  2. APLICAR_HASTA_NO_MEJORAR (parada: Stagnation=20):\n    LLAMAR FlipBestItem",
      "timestamp": "2025-12-26T14:05:31.234567"
    },
    {
      "name": "GAA_Algorithm_2",
      "pseudocode": "SECUENCIA:\n  1. CONSTRUIR_VORAZ usando GreedyByWeight\n  2. LLAMAR FlipWorstItem",
      "timestamp": "2025-12-26T14:05:31.345678"
    },
    {
      "name": "GAA_Algorithm_3",
      "pseudocode": "SECUENCIA:\n  1. CONSTRUIR_VORAZ usando RandomConstruct\n  2. MIENTRAS (presupuesto: 1000 iteraciones):\n    SECUENCIA:\n      1. BUSQUEDA_LOCAL en TwoExchange (aceptación: Improving)\n      2. LLAMAR TwoExchange",
      "timestamp": "2025-12-26T14:05:31.456789"
    }
  ],
  "execution_steps": [
    {
      "step_name": "Generating GAA Algorithms",
      "timestamp": "2025-12-26T14:05:31.123456",
      "details": {
        "num_algorithms": 3,
        "seed": 123,
        "min_depth": 2,
        "max_depth": 3
      }
    },
    {
      "step_name": "Processing Low-Dimensional Group",
      "timestamp": "2025-12-26T14:05:32.234567"
    },
    {
      "step_name": "Processing Large-Scale Group",
      "timestamp": "2025-12-26T14:05:50.345678"
    }
  ],
  "results_summary": {
    "Low-Dimensional Results": {
      "best_algorithm": "GAA_Algorithm_2",
      "experiments_completed": "29/30",
      "json_file": "output/low_dimensional_experiments/experiment_low_dimensional_experiment_20251226_140530.json"
    },
    "Large-Scale Results": {
      "best_algorithm": "GAA_Algorithm_1",
      "experiments_completed": "55/63",
      "json_file": "output/large_scale_experiments/experiment_large_scale_experiment_20251226_140551.json"
    }
  }
}
```

---

## 🎯 Beneficios

### 1. Reproducibilidad Científica

Con estos archivos, puedes:
- **Reproducir exactamente** cualquier ejecución (mismo git hash + mismos parámetros)
- **Comparar** diferentes ejecuciones para detectar cambios
- **Auditar** qué algoritmos se generaron y usaron

### 2. Debugging

Si algo falla:
- Sabes **exactamente** qué parámetros se usaron
- Ves el **git hash** del código que se ejecutó
- Sabes si había **cambios no commiteados**
- Puedes ver **paso a paso** dónde falló

### 3. Documentación Automática

No necesitas recordar:
- Qué seed usaste
- Qué algoritmos se generaron
- Qué parámetros cambiaste
- **Todo está documentado automáticamente**

---

## 📂 Ubicación de los Archivos

```
output/
└── execution_logs/
    ├── execution_config_20251226_140530.json
    ├── execution_log_20251226_140530.md
    ├── execution_config_20251226_152145.json
    ├── execution_log_20251226_152145.md
    └── ... (un par de archivos por cada ejecución)
```

---

## 🔍 Ejemplo de Uso

### Comparar dos ejecuciones:

```bash
# Ver diferencias en configuración
diff output/execution_logs/execution_config_20251226_140530.json \
     output/execution_logs/execution_config_20251226_152145.json

# Ver qué algoritmos se generaron en cada una
grep -A5 "Algorithm:" output/execution_logs/execution_log_20251226_140530.md
grep -A5 "Algorithm:" output/execution_logs/execution_log_20251226_152145.md
```

### Encontrar ejecuciones con seed específico:

```bash
grep -l '"seed": 123' output/execution_logs/execution_config_*.json
```

### Ver todas las ejecuciones exitosas:

```bash
grep -l '"success": true' output/execution_logs/execution_config_*.json
```

---

## ✅ Verificación

Para verificar que el logging funciona, ejecuta:

```bash
python3 scripts/demo_experimentation_both_OPTIMIZED.py
```

Al finalizar, verás:

```
📋 Execution Documentation:
   • Config: output/execution_logs/execution_config_20251226_140530.json
   • Log: output/execution_logs/execution_log_20251226_140530.md
```

Luego puedes inspeccionar estos archivos para ver toda la información capturada.
