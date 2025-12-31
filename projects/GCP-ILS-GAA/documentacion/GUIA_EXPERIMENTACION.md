# 🚀 SCRIPT DE EXPERIMENTACIÓN: Guía de Ejecución

**Pregunta**: ¿Corramos script de experimentación? ¿Qué mido? ¿Qué output entrega?

**Respuesta**: ✅ Sí, hay script listo. Aquí te muestro qué hacer, qué se mide y qué outputs genera.

---

## 🎯 Script Principal: `gaa_orchestrator.py`

**Ubicación**: `04-Generated/scripts/gaa_orchestrator.py` (476 líneas)

**Propósito**: Ejecuta el ciclo GAA completo de forma automática

---

## ⚙️ Requisitos Previos

### 1. Python 3.8+
```bash
python --version
# Debería mostrar: Python 3.8+
```

### 2. Dependencias
```bash
pip install pyyaml numpy
```

### 3. Estructura de Carpetas
```
projects/GCP-ILS-GAA/
├── 04-Generated/scripts/
│   ├── gaa_orchestrator.py      ← ESTE SCRIPT
│   ├── ils_search.py
│   ├── ast_nodes.py
│   ├── ast_evaluator.py
│   ├── problem_gcp.py
│   └── metaheuristic_ils.py
│
├── datasets/
│   ├── training/      ← Instancias para entrenar
│   ├── validation/    ← Instancias para validación
│   └── test/          ← Instancias finales
│
└── config.yaml        ← Configuración (SE CREA AUTOMÁTICAMENTE)
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Ejecución Básica (Recomendado)

```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_orchestrator.py
```

### Opción 2: Con Parámetros Personalizados

```bash
python 04-Generated/scripts/gaa_orchestrator.py \
  --max-iterations 1000 \
  --perturbation-strength 0.25 \
  --seed 123
```

### Opción 3: Especificar Instancias

```bash
python 04-Generated/scripts/gaa_orchestrator.py \
  --training datasets/training/*.gcp \
  --validation datasets/validation/*.gcp \
  --test datasets/test/*.gcp
```

---

## 📊 ¿QUÉ SE MIDE?

El script mide **6 dimensiones principales** durante la experimentación:

### 1. **CALIDAD DE SOLUCIÓN**
```
Métrica: Número de colores usados
Unidad: Entero (menor = mejor)
Ejemplo: Config A usa 24 colores, Config B usa 25

Se mide para:
├─ Cada instancia individual
├─ Promedio por configuración
└─ Estadísticas (media, std, min, max)
```

### 2. **ROBUSTEZ**
```
Métrica: Tasa de éxito
Unidad: Porcentaje (0-100%)
Ejemplo: Config A tiene éxito en 98.5% de ejecuciones

Se mide:
├─ % de instancias donde el algoritmo converge
├─ % de instancias donde encuentra buena solución
└─ Consistencia entre diferentes semillas
```

### 3. **EFICIENCIA (Tiempo)**
```
Métrica: Tiempo de ejecución
Unidad: Milisegundos (ms) o segundos (s)
Ejemplo: Instancia pequeña: 250ms, grande: 5s

Se mide:
├─ Tiempo por instancia individual
├─ Tiempo promedio
└─ Correlación tamaño vs tiempo
```

### 4. **CONSISTENCIA**
```
Métrica: Desviación estándar
Unidad: Número de colores (desv. std)
Ejemplo: Media 24.3 colores, ±1.2 std

Mide cuánto varía la solución entre ejecuciones:
├─ Baja variabilidad (std=0.5): Confiable
└─ Alta variabilidad (std=3.0): Inconsistente
```

### 5. **FITNESS AGREGADO**
```
Métrica: Función multi-objetivo
Fórmula: fitness = 0.5*f_calidad + 0.2*f_tiempo + 
                   0.2*f_robustez + 0.1*f_factibilidad

Rango: 0.0 a 1.0
Ejemplo: Config A: 0.8542, Config B: 0.7956
```

### 6. **ESTADÍSTICAS DE BÚSQUEDA ILS**
```
Métricas de convergencia:
├─ Iteración donde encuentra mejor: iter 245/500
├─ Mejoras encontradas: 87 mejoras en 500 iters
├─ Tasa de aceptación: 18.2% (91/500)
├─ Tiempo de búsqueda: 2.3 segundos
└─ Configuraciones evaluadas: 500
```

---

## 📤 ¿QUÉ OUTPUT ENTREGA?

El script entrega **múltiples tipos de outputs** en diferentes formatos:

### 1. **SALIDA EN CONSOLA (Terminal)**

```
╔═══════════════════════════════════════════════════════════════╗
║              GAA-ILS CONFIGURATION SEARCH                     ║
║              Graph Coloring Problem (GCP)                     ║
╚═══════════════════════════════════════════════════════════════╝

[GAA] Loading configuration...
[GAA] Loading problem instances...
  ✓ training/instance_1_n100_d0.5.gcp
  ✓ training/instance_2_n100_d0.5.gcp
  ...
[GAA] Loaded 70 training, 15 validation, 15 test instances

[GAA] Initializing ILS-based configuration search...
[GAA] Running ILS configuration search...

ITERATION PROGRESS:
├─ Iter   0: Current fitness: 0.6234 | Best: 0.6234
├─ Iter  10: Current fitness: 0.7105 | Best: 0.7345 ⭐ NEW BEST
├─ Iter  20: Current fitness: 0.7012 | Best: 0.7345
├─ Iter  30: Current fitness: 0.7823 | Best: 0.7823 ⭐ NEW BEST
│ ...
├─ Iter 490: Current fitness: 0.8401 | Best: 0.8542 ⭐ BEST SO FAR
└─ Iter 500: Current fitness: 0.8156 | Best: 0.8542 ⭐ FINAL BEST

[GAA] ILS search completed in 47.3 seconds
[GAA] Found 87 improvements in 500 iterations

[GAA] Evaluating best configurations on test set...
CONFIGURATION #1 (ILS Search Best)
├─ Average colors: 24.3 ± 1.2
├─ Success rate: 98.5%
├─ Avg time: 245ms
└─ Fitness: 0.8542 ⭐ BEST

CONFIGURATION #2
├─ Average colors: 25.1 ± 2.3
├─ Success rate: 97.2%
├─ Avg time: 312ms
└─ Fitness: 0.8201

[GAA] Generating reports...
[GAA] All results saved to: results/
[GAA] Total time: 52.4 seconds
```

### 2. **ARCHIVOS GENERADOS EN CARPETA `results/`**

```
results/
├── summary.txt                    ← Resumen textual
├── results.json                   ← Todos los datos JSON
├── results.csv                    ← Tabla CSV para Excel
├── configuration_top_1.yaml       ← Config mejor (YAML)
├── configuration_top_2.yaml       ← Segunda mejor
├── configuration_top_3.yaml       ← Tercera mejor
├── convergence_plot.json          ← Datos para gráfico
└── comparison_table.txt           ← Tabla comparativa
```

### 3. **ARCHIVO: `results/summary.txt`** (Ejemplo)

```
═══════════════════════════════════════════════════════════════
            EXPERIMENTACIÓN GAA-ILS-GCP SUMMARY
═══════════════════════════════════════════════════════════════

PROJECT CONFIGURATION
─────────────────────
Project Name:         GCP-ILS-GAA
Problem:              Graph Coloring Problem
Metaheuristic:        Iterated Local Search (ILS)
Seed:                 42
Max Iterations:       500
Perturbation Strength: 0.20

INSTANCES LOADED
────────────────
Training:   70 instances
Validation: 15 instances
Test:       15 instances
Total:     100 instances

ILS SEARCH RESULTS
──────────────────
Search Duration:      47.3 seconds
Total Configurations: 500
Improvements Found:   87
Best Fitness Found:   0.8542 (at iteration 342)
Acceptance Rate:      18.2% (91/500 accepted)

TOP-3 CONFIGURATIONS
────────────────────

Configuration #1
  Fitness Score:     0.8542 ⭐ BEST
  Colores (avg):     24.3 ± 1.2
  Success Rate:      98.5%
  Time (avg):        245 ms
  
Configuration #2
  Fitness Score:     0.8201
  Colores (avg):     25.1 ± 2.3
  Success Rate:      97.2%
  Time (avg):        312 ms

Configuration #3
  Fitness Score:     0.7956
  Colores (avg):     25.8 ± 1.5
  Success Rate:      96.8%
  Time (avg):        198 ms

STATISTICS BY INSTANCE TYPE
──────────────────────────

Training Set (70 instances):
  Mean Colors:       24.2
  Std Dev:          1.1
  Min:              22
  Max:              27
  Success Rate:      98.7%
  Avg Time:         242 ms

Validation Set (15 instances):
  Mean Colors:       24.5
  Std Dev:          1.3
  Min:              23
  Max:              28
  Success Rate:      97.8%
  Avg Time:         251 ms

Test Set (15 instances):
  Mean Colors:       24.3
  Std Dev:          1.2
  Min:              22
  Max:              26
  Success Rate:      98.5%
  Avg Time:         245 ms

═══════════════════════════════════════════════════════════════
CONCLUSION: Configuration #1 recomendada para producción
═══════════════════════════════════════════════════════════════
```

### 4. **ARCHIVO: `results/results.json`** (Estructura)

```json
{
  "metadata": {
    "project_name": "GCP-ILS-GAA",
    "timestamp": "2025-12-30T15:32:45Z",
    "version": "1.0.0"
  },
  "search_results": {
    "total_iterations": 500,
    "improvements_found": 87,
    "best_fitness": 0.8542,
    "search_time_seconds": 47.3,
    "iterations_to_best": 342
  },
  "top_configurations": [
    {
      "rank": 1,
      "fitness": 0.8542,
      "configuration": {
        "constructor": "LargestDegreeFirst",
        "local_search": "ColorSwap",
        "perturbation": "Remove3",
        "iterations": 450
      },
      "statistics": {
        "mean_colors": 24.3,
        "std_colors": 1.2,
        "min_colors": 22,
        "max_colors": 27,
        "success_rate": 0.985,
        "mean_time_ms": 245
      }
    },
    // ... más configuraciones ...
  ]
}
```

### 5. **ARCHIVO: `results/results.csv`** (Para Excel/Análisis)

```csv
rank,fitness,constructor,local_search,perturbation,iterations,mean_colors,std_colors,success_rate,mean_time_ms
1,0.8542,LargestDegreeFirst,ColorSwap,Remove3,450,24.3,1.2,0.985,245
2,0.8201,GreedyByWeight,Relocate,Remove2,480,25.1,2.3,0.972,312
3,0.7956,RandomConstruct,Swaps,RemoveSingle,420,25.8,1.5,0.968,198
...
```

### 6. **ARCHIVO: `configuration_top_1.yaml`** (Mejore Config)

```yaml
project_name: GCP-ILS-GAA
metadata:
  rank: 1
  fitness_score: 0.8542
  iteration_found: 342

configuration:
  constructor: LargestDegreeFirst
  constructor_description: "Ordena vértices por grado (mayor primero)"
  
  local_search:
    operator: ColorSwap
    max_moves: 10
    description: "Intenta intercambiar colores de vértices adyacentes"
  
  perturbation:
    operator: Remove3
    strength: 0.2
    description: "Remueve asignación de color a 3 vértices"
  
  parameters:
    iterations: 450
    seed: 42

performance_metrics:
  mean_colors: 24.3
  std_colors: 1.2
  min_colors: 22
  max_colors: 27
  success_rate: 0.985
  mean_time_ms: 245

dataset_breakdown:
  training:
    mean_colors: 24.2
    instances: 70
  validation:
    mean_colors: 24.5
    instances: 15
  test:
    mean_colors: 24.3
    instances: 15
```

---

## 📋 EJEMPLO COMPLETO: Ejecución Paso a Paso

```bash
# 1. Navegar a la carpeta del proyecto
cd projects/GCP-ILS-GAA

# 2. Ejecutar el script
python 04-Generated/scripts/gaa_orchestrator.py

# 3. Script hará:
#    a) Cargar config.yaml
#    b) Cargar 100 instancias de datasets/
#    c) Ejecutar 500 iteraciones ILS
#    d) Evaluar en validación
#    e) Generar reportes
#    f) Salvar resultados en results/

# 4. Revisar resultados
cat results/summary.txt

# 5. Analizar datos (opcional)
python -c "
import json
with open('results/results.json') as f:
    data = json.load(f)
print('Top Configuration:')
print(f\"  Fitness: {data['top_configurations'][0]['fitness']}\")
print(f\"  Colors: {data['top_configurations'][0]['statistics']['mean_colors']}\")
"
```

---

## ⏱️ Tiempo Estimado de Ejecución

| Configuración | Tiempo Estimado |
|---------------|-----------------|
| **Modo rápido** (50 iter, 10 inst) | 2-3 minutos |
| **Modo normal** (500 iter, 100 inst) | 30-60 minutos |
| **Modo exhaustivo** (1000 iter, 100 inst) | 60-120 minutos |

**Tiempo = (iteraciones × instancias × tiempo_por_ejecución) / num_workers**

---

## 🔧 Personalizar la Experimentación

### Opción A: Modificar `config.yaml`

```yaml
max_iterations: 1000          # De 500 a 1000
perturbation_strength: 0.25   # Más perturbación
seed: 123                     # Cambiar semilla

# Pesos del fitness
fitness_weights:
  quality: 0.5                # 50% calidad
  time: 0.2                   # 20% tiempo
  robustness: 0.2             # 20% robustez
  feasibility: 0.1            # 10% factibilidad
```

### Opción B: Parámetros en línea de comando

```bash
python 04-Generated/scripts/gaa_orchestrator.py \
  --max-iterations 1000 \
  --perturbation-strength 0.25 \
  --seed 123 \
  --fitness-quality 0.6 \
  --fitness-time 0.2 \
  --fitness-robustness 0.1 \
  --fitness-feasibility 0.1
```

---

## 📊 Interpretar Resultados

### ¿Qué significa cada métrica?

**Fitness 0.8542**
- Rango: 0.0 a 1.0
- 0.8542 = 85.42% de optimalidad
- Interpretación: ✅ MUY BUENO

**Colors 24.3 ± 1.2**
- Media: 24.3 colores
- Std: ±1.2 (variabilidad)
- Interpretación: ✅ Baja variabilidad = Consistente

**Success Rate 98.5%**
- Éxito en 98.5% de ejecuciones
- Interpretación: ✅ MUY CONFIABLE

**Time 245ms**
- 245 milisegundos por instancia
- Interpretación: ✅ RÁPIDO (< 1 segundo)

---

## ✅ Checklist de Ejecución

- [ ] Python 3.8+ instalado
- [ ] Dependencias (`pip install pyyaml numpy`)
- [ ] Carpeta `datasets/` tiene instancias
- [ ] Carpeta `results/` existe o se creará
- [ ] Script `gaa_orchestrator.py` existe
- [ ] Ejecutar: `python 04-Generated/scripts/gaa_orchestrator.py`
- [ ] Revisar salida en consola
- [ ] Revisar archivos en `results/`

---

## 🚨 Troubleshooting

### Error: "Module not found"
```bash
pip install pyyaml numpy
# O crea un environment virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Error: "No instances found"
```bash
# Verifica que existen instancias:
ls datasets/training/
ls datasets/validation/
ls datasets/test/
# Deben tener archivos .gcp o .txt
```

### Ejecución muy lenta
```bash
# Reducir iteraciones:
python 04-Generated/scripts/gaa_orchestrator.py --max-iterations 100

# O reducir instancias (usa solo training):
# Edita config.yaml y comenta validation/test
```

---

## 📞 Resumen Rápido

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué script correr?** | `gaa_orchestrator.py` |
| **¿Qué se mide?** | 6 dimensiones: calidad, robustez, eficiencia, consistencia, fitness, estadísticas ILS |
| **¿Cuánto tarda?** | 30-60 minutos (500 iteraciones × 100 instancias) |
| **¿Qué output genera?** | Summary.txt, JSON, CSV, YAML, gráficos |
| **¿Dónde se guardan?** | Carpeta `results/` |

---

**¿Ejecutamos ahora?** ✅ Sí, directamente con:
```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_orchestrator.py
```

**Tiempo de espera**: 30-60 minutos aproximadamente.
