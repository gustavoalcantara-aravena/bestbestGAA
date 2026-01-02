# REFERENCIA RÁPIDA: KBP-SA - 3 Algoritmos Generados Automáticamente

## ⚡ Cheat Sheet

### 1️⃣ Comando para Ejecutar TODO
```bash
cd projects/KBP-SA
python scripts/demo_experimentation_both_OPTIMIZED.py
```
**Resultado:** 93 experimentos (30 low-dim + 63 large-scale) en ~40 segundos

---

### 2️⃣ Generar 3 Algoritmos (Solo)
```python
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar

grammar = Grammar(min_depth=2, max_depth=3)
generator = AlgorithmGenerator(grammar=grammar, seed=123)

algos = []
for i in range(3):
    ast = generator.generate_with_validation()
    if ast:
        algos.append({'name': f'Algo_{i+1}', 'ast': ast})

print(f"✅ {len(algos)} algoritmos generados")
```

---

### 3️⃣ Ejecutar 3 Algoritmos en Instancias
```python
from experimentation.runner import ExperimentRunner, ExperimentConfig
from data.loader import DatasetLoader

# Cargar instancias
loader = DatasetLoader("./datasets")
instances = loader.load_folder("low_dimensional")

# Configurar
config = ExperimentConfig(
    name="test",
    instances=[i.name for i in instances],
    algorithms=algos,          # Los 3 algoritmos
    repetitions=1,
    max_time_seconds=5.0
)

# Ejecutar
runner = ExperimentRunner(config)
runner.problems = {i.name: i for i in instances}
results = runner.run_all(verbose=True)

# Guardar
json_file = runner.save_results()
```

---

### 4️⃣ Analizar Resultados
```python
import json

with open(json_file) as f:
    data = json.load(f)

print("\n🏆 RANKING (por gap promedio):\n")
for alg, stats in sorted(data['summary']['by_algorithm'].items(), 
                         key=lambda x: x[1]['avg_gap']):
    print(f"{alg}: {stats['avg_gap']:.2f}% ± {stats['std_gap']:.2f}%")
```

---

## 📍 Archivos Clave

| Ruta | Función | Líneas |
|------|---------|--------|
| `gaa/generator.py` | **AlgorithmGenerator** - Crea AST aleatorios | 282 |
| `gaa/grammar.py` | Gramática BNF + validación | 324 |
| `experimentation/runner.py` | **ExperimentRunner** - Ejecuta experimentos | 372 |
| `scripts/demo_experimentation_both_OPTIMIZED.py` | Script principal con demo completa | 804 |
| `config/config.yaml` | Parámetros (profundidad, terminales, etc) | 162 |

---

## 🔧 Parámetros Importantes

### Generación (AlgorithmGenerator)
```
grammar.min_depth = 2          # Profundidad mínima
grammar.max_depth = 3          # Profundidad máxima
seed = 123                     # Para reproducibilidad
num_algorithms = 3             # Cantidad a generar
```

### Ejecución (ExperimentConfig)
```
instances = 10 (low-dim)       # Instancias de prueba
algorithms = 3                 # Los 3 algoritmos generados
repetitions = 1                # Repeticiones por combo
max_time_seconds = 5.0         # Timeout por ejecución
total_runs = 10 × 3 × 1 = 30  # Total ejecuciones
```

---

## 📊 Flujo en 5 Pasos

```
1. GENERAR 3 ALGORITMOS
   AlgorithmGenerator(seed=123).generate() × 3 → [Algo_1, Algo_2, Algo_3]

2. CARGAR INSTANCIAS
   DatasetLoader().load_folder("low_dimensional") → 10 instancias

3. EJECUTAR EXPERIMENTOS
   ExperimentRunner(config).run_all() → 30 resultados (10 × 3 × 1)

4. GUARDAR RESULTADOS
   runner.save_results() → JSON con config, results, summary

5. ANALIZAR
   compare_algorithms(Friedman test) → Ranking: Algo_3 > Algo_2 > Algo_1
```

---

## 🎯 Estructura de Salida JSON

```json
{
  "config": {
    "instances": 10,
    "algorithms": 3,
    "repetitions": 1,
    "total_experiments": 30
  },
  "results": [
    {
      "instance_name": "instance_f1",
      "algorithm_name": "Algo_1",
      "best_value": 255,
      "gap_to_optimal": 3.2,
      "total_time": 0.0068
    },
    ... (30 elementos)
  ],
  "summary": {
    "by_algorithm": {
      "Algo_1": {
        "avg_gap": 2.85,
        "std_gap": 1.23,
        "avg_time": 0.0072
      },
      "Algo_2": {
        "avg_gap": 1.92,
        "std_gap": 0.87,
        "avg_time": 0.0245
      },
      "Algo_3": {
        "avg_gap": 1.54,
        "std_gap": 0.65,
        "avg_time": 0.0602
      }
    }
  }
}
```

---

## 🏆 Ranking Esperado

```
1. Algo_3: 1.54% gap     ✓ Mejor (menor gap)
2. Algo_2: 1.92% gap     ◇ Intermedio
3. Algo_1: 2.85% gap     ✗ Peor (mayor gap)
```

---

## 📁 Estructura de Outputs

```
output/
├── plots_low_dimensional_{TS}/
│   ├── demo_boxplot.png           ← Comparación visual
│   ├── demo_bars.png              ← Gap por algoritmo
│   ├── demo_scatter.png           ← Tiempo vs calidad
│   ├── best_algorithm_ast.png     ← Estructura del mejor
│   ├── gap_evolution.png          ← SA analysis
│   └── time_tracking.md           ← Log de tiempos
│
├── low_dimensional_experiments/
│   └── experiment_*.json          ← Datos principales
│
└── execution_logs/
    └── *.json                     ← Logs detallados
```

---

## ✅ Checklist

- [ ] Python 3.8+ instalado
- [ ] `pip install -r requirements.txt`
- [ ] Datasets en `datasets/low_dimensional/` y `datasets/large_scale/`
- [ ] Directorio `output/` existe
- [ ] Ejecutar: `python scripts/demo_experimentation_both_OPTIMIZED.py`
- [ ] Verificar: `output/plots_*/demo_boxplot.png`
- [ ] Revisar JSON: `output/*/experiment_*.json`

---

## 🐛 Troubleshooting Rápido

| Error | Solución |
|-------|----------|
| "No datasets found" | Verificar `datasets/low_dimensional/*.txt` |
| Timeout en ejecución | Aumentar `max_time_seconds` en ExperimentConfig |
| Graphviz no disponible | `choco install graphviz` (Windows) |
| "No module 'gaa'" | Verificar que está en la ruta correcta |
| Matplotlib backend error | Usar `matplotlib.use('Agg')` al inicio |

---

## 📊 Interpretación Rápida de Resultados

### Boxplot
- **Caja baja** = mejor desempeño (gap menor)
- **Caja alta** = peor desempeño (gap mayor)
- **× = Outliers**

### Barras
- **Más corta** = mejor (gap menor)
- **Más larga** = peor (gap mayor)
- Las líneas = desviación estándar

### Test Friedman
- **p-value < 0.05** = Hay diferencia significativa entre algoritmos
- **p-value > 0.05** = No hay diferencia clara

---

## 🚀 Comandos Útiles

```bash
# Ejecutar demo completa
python scripts/demo_experimentation_both_OPTIMIZED.py

# Verificar datasets
ls datasets/low_dimensional/*.txt | wc -l    # Debe ser 10
ls datasets/large_scale/*.txt | wc -l        # Debe ser 21

# Revisar resultados JSON
cat output/low_dimensional_experiments/experiment_*.json | python -m json.tool

# Contar ejecuciones exitosas
python -c "import json; d=json.load(open('output/.../experiment_*.json')); print(d['summary']['successful'])"
```

---

## 📚 Documentos Completos

1. **ANALISIS_KBP-SA_GENERACION_3_ALGORITMOS.md** - Análisis profundo (completo)
2. **GUIA_RAPIDA_KBP-SA.md** - Guía de ejecución y resultados
3. **EJEMPLOS_CODIGO_KBP-SA.md** - 5 ejemplos de código prácticos
4. **DIAGRAMA_VISUAL_FLUJO_KBP-SA.md** - Diagramas arquitectónicos
5. **REFERENCIA_RAPIDA_KBP-SA.md** - Este documento (cheat sheet)

---

## 🎓 Conceptos Clave

| Término | Definición |
|---------|-----------|
| **AST** | Árbol Sintáctico Abstracto - Representación de algoritmo |
| **GAA** | Generación Automática de Algoritmos |
| **Grammar** | Reglas que definen qué AST son válidos |
| **Seed** | Valor inicial que controla aleatoriedad (123 = reproducible) |
| **Gap** | Distancia a la solución óptima (%) - menor es mejor |
| **Friedman Test** | Test estadístico para comparar 3+ algoritmos |
| **Wilcoxon Test** | Test pareado para comparar 2 algoritmos |
| **Cohen's d** | Tamaño del efecto de diferencias |

---

## 🔗 Relaciones entre Módulos

```
demo_experimentation_both_OPTIMIZED.py
    ├─ AlgorithmGenerator (gaa/)
    │   ├─ Grammar (gaa/)
    │   └─ ASTNode (gaa/)
    │
    ├─ ExperimentRunner (experimentation/)
    │   ├─ ASTInterpreter (gaa/)
    │   ├─ DatasetLoader (data/)
    │   └─ ExperimentResult
    │
    ├─ StatisticalAnalyzer (experimentation/)
    │   └─ Tests (Friedman, Wilcoxon, Cohen's d)
    │
    └─ ResultsVisualizer (experimentation/)
        └─ matplotlib/PNG outputs
```

---

## 💡 Tips Pro

1. **Reproducibilidad:** Usar `seed=123` para generar siempre los mismos 3 algoritmos
2. **Velocidad:** Reducir `max_depth` de 3 a 2 para algoritmos más simples
3. **Precisión:** Aumentar `repetitions` de 1 a 3-5 para estadísticas más robustas
4. **Testing:** Empezar con 1-2 instancias antes de todo el conjunto
5. **Análisis:** Usar `verbose=True` en `run_all()` para ver progreso en tiempo real

---

## 🎯 Objetivo Alcanzado

✅ **Generar automáticamente 3 algoritmos** usando AlgorithmGenerator  
✅ **Ejecutarlos en 31 instancias** (10 low-dim + 21 large-scale)  
✅ **Realizar 93 experimentos** controlados (instancia × algoritmo × repetición)  
✅ **Guardar resultados** en JSON estructurado  
✅ **Análisis estadístico** con Friedman + Wilcoxon  
✅ **Generar visualizaciones** (boxplot, scatter, AST, SA analysis)  
✅ **Identificar mejor algoritmo** mediante ranking estadístico  

**Tiempo total:** ~40 segundos  
**Líneas de código utilizadas:** ~2,600+  

---

**Versión:** 1.0  
**Última actualización:** Enero 2026  
**Proyecto:** KBP-SA (Knapsack Problem con Simulated Annealing)
