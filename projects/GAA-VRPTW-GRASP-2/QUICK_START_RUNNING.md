# Quick Start: Ejecutar el Framework

## 📋 ¿Qué código existe?

El framework tiene **2 modos principales** de ejecución definidos en `scripts/experiments.py`:

### **Modo 1: QUICK (Rápido - Test)**
```
1 familia (R1)
12 instancias (R101-R112)
3 algoritmos
1 repetición cada uno
━━━━━━━━━━━━━━━
Total: 36 experimentos
Tiempo estimado: 2-5 minutos
```

### **Modo 2: FULL (Completo)**
```
6 familias (C1, C2, R1, R2, RC1, RC2)
56 instancias total
3 algoritmos
1 repetición cada uno
━━━━━━━━━━━━━━━
Total: 168 experimentos
Tiempo estimado: 10-20 minutos
```

---

## 🚀 Cómo Ejecutar

### **Opción A: QUICK (Recomendado para Empezar)**

```python
# script_quick.py
from scripts.experiments import QuickExperiment, AlgorithmGenerator

# Paso 1: Generar algoritmos (una sola vez)
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(num_algorithms=3)
print(f"✓ Generados: {algorithms}")

# Paso 2: Ejecutar QUICK
executor = QuickExperiment.run()
print(f"✓ Experimentos completados: {len(executor.raw_results)}")
print(f"✓ Resultados en: {executor.output_dir}")
```

**Ejecutar:**
```bash
python script_quick.py
```

**Salida:**
```
output/
└── vrptw_experiments_QUICK_02-01-26_14-30-45/
    ├── results/
    │   ├── raw_results.csv          ← Todos los resultados
    │   └── experiment_metadata.json  ← Configuración
    ├── plots/                        ← (para después)
    └── logs/                         ← (para después)
```

---

### **Opción B: FULL (Todos los datos)**

```python
# script_full.py
from scripts.experiments import FullExperiment, AlgorithmGenerator

# Paso 1: Generar algoritmos
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(num_algorithms=3)

# Paso 2: Ejecutar FULL
executor = FullExperiment.run()
print(f"✓ Total de experimentos: {len(executor.raw_results)}")
print(f"✓ Ubicación: {executor.output_dir}")
```

**Ejecutar:**
```bash
python script_full.py
```

---

### **Opción C: CUSTOM (Una sola familia diferente)**

Para ejecutar **solo una familia específica**, modifica `ExperimentConfig`:

```python
# script_custom.py
from scripts.experiments import ExperimentExecutor, ExperimentConfig, AlgorithmGenerator

# PASO 1: Generar algoritmos
gen = AlgorithmGenerator(seed=42)
algorithms = gen.generate_algorithms(num_algorithms=3)

# PASO 2: Crear configuración PERSONALIZADA
config = ExperimentConfig(
    mode='CUSTOM',
    families=['C1'],           # ← CAMBIA AQUÍ (C1, C2, R1, R2, RC1, o RC2)
    algorithms=algorithms,
    repetitions=1,
    seed=42
)

# PASO 3: Ejecutar
executor = ExperimentExecutor(config)
solomon_data = executor.get_solomon_instances(config.families)

for family, instances in solomon_data.items():
    for instance_id in instances:
        for algo_id in config.algorithms:
            # Aquí va el código real de solveo (ahora es mock)
            executor.add_result(
                algorithm_id=algo_id,
                instance_id=instance_id,
                family=family,
                run_id=1,
                k_final=10,      # ← Valor real del solver
                k_bks=10,        # ← Mejor conocido
                d_final=850.5,   # ← Distancia real
                d_bks=850.5,
                total_time_sec=5.2,
                iterations=100
            )

executor.save_raw_results()
executor.save_experiment_metadata()
print(f"✓ Resultados: {executor.output_dir}")
```

**Ejecutar:**
```bash
python script_custom.py
```

---

## 📊 Familias disponibles

| Familia | Instancias | Total | Característica |
|---------|-----------|-------|-----------------|
| **C1** | C101-C109 | 9 | Clustered, tiempo limitado |
| **C2** | C201-C208 | 8 | Clustered, tiempo largo |
| **R1** | R101-R112 | 12 | Random, tiempo limitado |
| **R2** | R201-R211 | 11 | Random, tiempo largo |
| **RC1** | RC101-RC108 | 8 | Mezcla C+R, tiempo limitado |
| **RC2** | RC201-RC208 | 8 | Mezcla C+R, tiempo largo |

---

## 🎯 Casos de Uso

### **Caso 1: Prueba rápida (5 min)**
```python
# Ejecuta QUICK (36 experimentos)
QuickExperiment.run()
```

### **Caso 2: Solo familia C1 (test de clustered)**
```python
config = ExperimentConfig(
    mode='CUSTOM',
    families=['C1'],    # ← Solo clustered
    algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
    repetitions=1,
    seed=42
)
executor = ExperimentExecutor(config)
# ... completar experimento
```

### **Caso 3: Solo familia R1 (test de random)**
```python
config = ExperimentConfig(
    mode='CUSTOM',
    families=['R1'],    # ← Solo random
    algorithms=['GAA_Algorithm_1', 'GAA_Algorithm_2', 'GAA_Algorithm_3'],
    repetitions=1,
    seed=42
)
executor = ExperimentExecutor(config)
# ... completar experimento
```

### **Caso 4: Todas las familias (20 min)**
```python
# Ejecuta FULL (168 experimentos)
FullExperiment.run()
```

### **Caso 5: Una instancia sola (ultra-rápido)**
```python
config = ExperimentConfig(
    mode='DEBUG',
    families=['R1'],
    algorithms=['GAA_Algorithm_1'],
    repetitions=1,
    seed=42
)
# Luego solo procesar R101
```

---

## ⚙️ Parámetros Configurables

```python
ExperimentConfig(
    mode='QUICK',              # 'QUICK', 'FULL', o nombre personalizado
    families=['R1'],           # Cuales familias ejecutar
    algorithms=['GAA_1', '...'],  # Cuales algoritmos
    repetitions=1,             # Cuantas veces repetir cada combo
    seed=42,                   # Seed para reproducibilidad
    timeout_sec=600            # Timeout por experimento (10 min)
)
```

---

## 📈 Estructura de Resultados

Después de ejecutar, obtendrás:

```
output/
└── vrptw_experiments_QUICK_02-01-26_14-30-45/
    ├── results/
    │   ├── raw_results.csv
    │   │   └── Columnas: algorithm_id, instance_id, family, 
    │   │            K_final, K_BKS, D_final, D_BKS, gap_percent, total_time_sec
    │   │
    │   └── experiment_metadata.json
    │       └── {experiment_id, mode, families, algorithms, timestamp, seed}
    │
    ├── plots/  (después de visualización)
    │   ├── convergence.png
    │   ├── boxplots_K.png
    │   └── ...
    │
    └── logs/  (logs de ejecución)
```

---

## 🔍 Analizar Resultados

Después de ejecutar, puedes analizar con:

```python
import pandas as pd

# Cargar resultados
df = pd.read_csv('output/.../results/raw_results.csv')

# Resumen por familia
print(df.groupby('family')[['K_final', 'D_final']].mean())

# Resumen por algoritmo
print(df.groupby('algorithm_id')[['reached_K_BKS']].mean())

# Instancias donde se alcanzó BKS
bks_reached = df[df['reached_K_BKS'] == True]
print(f"Alcanzaron BKS: {len(bks_reached)}/{len(df)}")

# Gap promedio
print(f"Gap de distancia promedio: {df['gap_percent'].mean():.2f}%")
```

---

## 💡 Diferencias: QUICK vs CUSTOM (una familia) vs FULL

| Aspecto | QUICK | CUSTOM (C1) | CUSTOM (R1) | FULL |
|---------|-------|-----------|-----------|------|
| **Familias** | 1 (R1) | 1 (C1) | 1 (R1) | 6 |
| **Instancias** | 12 | 9 | 12 | 56 |
| **Experimentos** | 36 | 27 | 36 | 168 |
| **Tiempo** | 2-5 min | 2-3 min | 2-5 min | 15-25 min |
| **Uso** | Testing | Debug clustered | Testing | Investigación |

---

## ✅ Checklist: Primeros Pasos

- [ ] Leer este archivo
- [ ] Crear `script_quick.py` con código QUICK
- [ ] Ejecutar: `python script_quick.py`
- [ ] Verificar `output/` se creó
- [ ] Abrir `raw_results.csv` y ver datos
- [ ] (Opcional) Probar con CUSTOM (una familia)
- [ ] (Opcional) Probar FULL (todas las familias)
- [ ] Analizar resultados con pandas

---

## 🆘 Troubleshooting

### Problema: "No data generated"
**Solución**: Verifica que `AlgorithmGenerator.generate_algorithms()` se ejecutó primero

### Problema: Ruta de output no existe
**Solución**: El código crea `output/` automáticamente con `mkdir(exist_ok=True, parents=True)`

### Problema: Quiero MÁS experimentos
**Solución**: Aumenta `repetitions` en `ExperimentConfig`
```python
config = ExperimentConfig(
    mode='QUICK',
    families=['R1'],
    algorithms=['GAA_1', 'GAA_2', 'GAA_3'],
    repetitions=10,  # ← Ahora 10 repeticiones = 360 experimentos
    seed=42
)
```

### Problema: Quiero MENOS experimentos
**Solución**: Usa una sola familia y algoritmo
```python
config = ExperimentConfig(
    mode='MICRO',
    families=['R1'],
    algorithms=['GAA_1'],  # ← Solo 1 algoritmo
    repetitions=1,
    seed=42
)
# Total: 12 experimentos (muy rápido)
```

---

## 📚 Referencias

- **Modo QUICK**: En archivo `scripts/experiments.py` línea ~280
- **Modo FULL**: En archivo `scripts/experiments.py` línea ~310
- **ExperimentConfig**: En archivo `scripts/experiments.py` línea ~20
- **Familias Solomon**: Línea ~130 (`get_solomon_instances`)

---

**Última actualización**: Enero 2, 2026  
**Estado**: Guía Completa ✅
