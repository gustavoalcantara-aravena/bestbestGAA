# ✅ SCRIPT DE EXPERIMENTACIÓN COMPLETO: run_full_experiment.py

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025  
**Estado**: ✅ **COMPLETADO**

---

## 📋 DESCRIPCIÓN

Script que ejecuta **ILS en todos los 79 datasets DIMACS** y genera:
- ✅ Resultados tabulares (CSV, JSON)
- ✅ Reportes estadísticos (TXT)
- ✅ Gráficas de análisis (PNG)
- ✅ Archivos de solución (.sol)

**Ubicación**: `scripts/run_full_experiment.py`  
**Líneas de código**: 450+  
**Integración**: OutputManager + PlotManager

---

## 🚀 CÓMO USAR

### Opción 1: Ejecutar en todos los datasets (79 instancias)
```bash
python scripts/run_full_experiment.py --mode all
```

### Opción 2: Ejecutar en familia específica
```bash
python scripts/run_full_experiment.py --mode family --family DSJ
```

Familias disponibles: `CUL`, `DSJ`, `LEI`, `MYC`, `REG`, `SCH`, `SGB`

### Opción 3: Con parámetros personalizados
```bash
python scripts/run_full_experiment.py \
    --mode all \
    --max-time 60 \
    --num-replicas 3 \
    --seed 42 \
    --verbose
```

### Parámetros disponibles

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `--mode` | str | `all` | `all` o `family` |
| `--family` | str | - | Familia específica (requerido si mode=family) |
| `--max-time` | float | 300.0 | Tiempo máximo por instancia (segundos) |
| `--num-replicas` | int | 1 | Número de ejecuciones independientes |
| `--seed` | int | 42 | Semilla aleatoria |
| `--verbose` | flag | False | Mostrar progreso detallado |

---

## 📊 OUTPUTS GENERADOS

### Estructura de directorios

```
output/results/
├── all_datasets/{timestamp}/
│   ├── summary.csv                    # Tabla resumen
│   ├── detailed_results.json          # Resultados detallados
│   ├── statistics.txt                 # Reporte estadístico
│   ├── convergence_plot.png           # Gráfica de convergencia
│   └── scalability_plot.png           # Gráfica de escalabilidad
│
└── specific_datasets/DSJ/{timestamp}/
    ├── summary.csv
    ├── detailed_results.json
    ├── statistics.txt
    └── [gráficas...]

output/solutions/
├── myciel3_31-12-25_19-30-45.sol
├── DSJC125_31-12-25_19-30-45.sol
└── ...
```

### Archivos generados

#### 1. **summary.csv** - Tabla Resumen
```csv
Instance,Family,Vertices,Edges,BKS,Best_Colors,Avg_Colors,Worst_Colors,Feasible,Avg_Time,Gap
myciel3,MYC,11,20,4,4,4.0,4,True,0.50,0.0000
DSJC125.1,DSJ,125,736,5,6,6.2,7,True,12.30,0.2000
```

#### 2. **detailed_results.json** - Resultados Detallados
```json
{
  "metadata": {
    "timestamp": "31-12-25_19-30-45",
    "mode": "all",
    "total_instances": 79,
    "total_time": 945.3,
    "num_replicas": 1
  },
  "results": [
    {
      "instance": "myciel3",
      "family": "MYC",
      "vertices": 11,
      "edges": 20,
      "bks": 4,
      "colors": [4],
      "conflicts": [0],
      "times": [0.5],
      "feasible": [true],
      "gaps": [0.0],
      "avg_colors": 4.0,
      "best_colors": 4,
      "worst_colors": 4
    }
  ],
  "statistics": {
    "total_instances": 79,
    "total_feasible": 79,
    "avg_colors": 22.4,
    "std_colors": 15.2,
    "avg_time": 11.96,
    "avg_gap": 0.018
  }
}
```

#### 3. **statistics.txt** - Reporte Estadístico
```
EXPERIMENTO COMPLETO: GRAPH COLORING PROBLEM CON ILS
================================================================================

Timestamp: 31-12-25_19-30-45
Modo: all
Tiempo total: 945.3s
Réplicas por instancia: 1

RESUMEN GENERAL:
--------------------------------------------------------------------------------
Total instancias: 79
Instancias factibles: 79/79
Colores promedio: 22.40 ± 15.20
Tiempo promedio: 11.96s
Gap promedio: 0.0180

RESULTADOS POR INSTANCIA:
--------------------------------------------------------------------------------
Instancia            Colores    Tiempo     Gap
--------------------------------------------------------------------------------
myciel3              4          0.50s      0.0000
DSJC125.1            6          12.30s     0.2000
...
```

#### 4. **{instance}_{timestamp}.sol** - Archivos de Solución
```
c Solution for myciel3
c Timestamp: 31-12-25_19-30-45
c Colors: 4
c Conflicts: 0
c Feasible: True
c
c Format: vertex color
c
1 0
2 1
3 2
4 0
5 1
...
```

#### 5. **convergence_plot.png** - Gráfica de Convergencia
- Muestra evolución del fitness a lo largo de iteraciones
- Útil para analizar velocidad de convergencia

#### 6. **scalability_plot.png** - Gráfica de Escalabilidad
- Tiempo de ejecución vs tamaño de instancia
- Muestra cómo escala el algoritmo

---

## 🔧 CARACTERÍSTICAS IMPLEMENTADAS

### 1. Carga de Datasets
- ✅ Carga automática de todos los 79 datasets DIMACS
- ✅ Soporte para familias específicas (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
- ✅ Validación de archivos .col
- ✅ Manejo de errores

### 2. Ejecución de ILS
- ✅ Configuración automática de ILS
- ✅ Soporte para múltiples réplicas
- ✅ Control de tiempo máximo por instancia
- ✅ Reproducibilidad con seeds

### 3. Integración OutputManager
- ✅ Creación automática de sesiones
- ✅ Guardado de CSV, JSON, TXT
- ✅ Guardado de soluciones (.sol)
- ✅ Logging automático

### 4. Integración PlotManager
- ✅ Generación de gráficas de convergencia
- ✅ Generación de gráficas de escalabilidad
- ✅ Manejo de errores en gráficas

### 5. Reportes Estadísticos
- ✅ Cálculo de estadísticas generales
- ✅ Análisis por instancia
- ✅ Análisis por familia
- ✅ Resumen ejecutivo

---

## 📈 CLASE FullExperiment

### Métodos principales

```python
class FullExperiment:
    def __init__(self, mode, family, max_time, num_replicas, seed, verbose)
    def load_datasets() -> List[GraphColoringProblem]
    def run_ils(problem) -> Tuple[ColoringSolution, Dict]
    def run_experiment()
    def _save_results(elapsed_time)
    def _calculate_statistics() -> Dict
    def _generate_report(elapsed_time) -> str
    def _generate_plots()
```

### Flujo de ejecución

```
1. Inicializar FullExperiment
   ├─ Crear OutputManager
   ├─ Crear PlotManager
   └─ Configurar logging

2. Cargar datasets DIMACS
   └─ Validar archivos .col

3. Ejecutar ILS en cada instancia
   ├─ Ejecutar réplicas
   ├─ Calcular métricas
   └─ Guardar soluciones

4. Guardar resultados
   ├─ summary.csv
   ├─ detailed_results.json
   ├─ statistics.txt
   └─ {instance}.sol

5. Generar gráficas
   ├─ convergence_plot.png
   └─ scalability_plot.png
```

---

## 💻 EJEMPLO DE USO

### Ejemplo 1: Ejecutar en todos los datasets
```bash
python scripts/run_full_experiment.py --mode all
```

**Salida esperada**:
```
================================================================================
  EXPERIMENTO COMPLETO: Graph Coloring Problem con ILS
================================================================================

📁 Sesión: output/results/all_datasets/31-12-25_19-30-45
🎯 Modo: all
⏱️  Tiempo máximo por instancia: 300s
🔄 Réplicas por instancia: 1
🌱 Semilla: 42

📂 CARGANDO DATASETS
--------------------------------------------------------------------------------
✅ 79 datasets cargados

🔬 EJECUTANDO ILS EN 79 INSTANCIAS
--------------------------------------------------------------------------------

[1/79] myciel3
   Vértices: 11, Aristas: 20
   Réplica 1: 4 colores, 0.50s

[2/79] DSJC125.1
   Vértices: 125, Aristas: 736
   Réplica 1: 6 colores, 12.30s

...

[79/79] SGB512
   Vértices: 512, Aristas: 1024
   Réplica 1: 28 colores, 145.20s

================================================================================
✅ EXPERIMENTO COMPLETADO
   Tiempo total: 945.3s
   Instancias: 79
   Réplicas por instancia: 1
================================================================================

💾 GUARDANDO RESULTADOS
--------------------------------------------------------------------------------
✅ CSV: summary.csv
✅ JSON: detailed_results.json
✅ TXT: statistics.txt
✅ SOL: myciel3_31-12-25_19-30-45.sol
✅ SOL: DSJC125_31-12-25_19-30-45.sol
...

📊 GENERANDO GRÁFICAS
--------------------------------------------------------------------------------
✅ Convergencia
✅ Escalabilidad
```

### Ejemplo 2: Ejecutar en familia DSJ con 3 réplicas
```bash
python scripts/run_full_experiment.py \
    --mode family \
    --family DSJ \
    --num-replicas 3 \
    --max-time 60
```

---

## ⏱️ TIEMPO DE EJECUCIÓN ESTIMADO

| Modo | Instancias | Réplicas | Tiempo Estimado |
|------|-----------|----------|-----------------|
| all | 79 | 1 | 15-20 min |
| all | 79 | 3 | 45-60 min |
| DSJ | 15 | 1 | 3-5 min |
| DSJ | 15 | 3 | 9-15 min |

---

## 🎯 CASOS DE USO

### 1. Validación Rápida
```bash
python scripts/run_full_experiment.py --mode family --family MYC --max-time 10
```
Ejecuta en 6 instancias pequeñas (~1 minuto)

### 2. Experimento Completo
```bash
python scripts/run_full_experiment.py --mode all --num-replicas 1
```
Ejecuta en todos los 79 datasets (~15-20 minutos)

### 3. Análisis Estadístico
```bash
python scripts/run_full_experiment.py --mode all --num-replicas 30
```
Ejecuta 30 réplicas por instancia para análisis estadístico (~8-10 horas)

### 4. Benchmark de Familia
```bash
python scripts/run_full_experiment.py --mode family --family DSJ --num-replicas 5
```
Ejecuta 5 réplicas en familia DSJ (~15-20 minutos)

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Clase FullExperiment creada
- [x] Carga de datasets DIMACS
- [x] Ejecución de ILS en todas las instancias
- [x] Soporte para múltiples réplicas
- [x] Integración con OutputManager
- [x] Integración con PlotManager
- [x] Generación de CSV
- [x] Generación de JSON
- [x] Generación de TXT
- [x] Generación de .sol
- [x] Generación de gráficas
- [x] Cálculo de estadísticas
- [x] Argumentos de línea de comandos
- [x] Logging automático
- [x] Manejo de errores
- [x] Documentación completa

---

## 🔗 INTEGRACIÓN CON OTROS MÓDULOS

### OutputManager
```python
output_manager = OutputManager()
session_dir = output_manager.create_session(mode="all_datasets")
output_manager.save_summary_csv(csv_data)
output_manager.save_detailed_json(json_data)
output_manager.save_statistics_txt(txt_content)
output_manager.save_solution(instance_name, solution)
```

### PlotManager
```python
plot_manager = PlotManager(output_dir=str(output_manager.get_plot_dir()))
plot_manager.plot_convergence(fitness_history)
plot_manager.plot_scalability(vertices, times)
```

### ILS
```python
ils = IteratedLocalSearch(
    problem=problem,
    constructive=GreedyDSATUR.construct,
    improvement=KempeChain.improve,
    perturbation=RandomRecolor.perturb,
    max_iterations=1000,
    time_budget=max_time
)
best_solution, history = ils.solve()
```

---

## 📝 CONCLUSIÓN

✅ **Script de experimentación completo implementado y listo para usar**

El script `run_full_experiment.py`:
- Ejecuta ILS en todos los 79 datasets DIMACS
- Integra OutputManager para guardar resultados automáticamente
- Integra PlotManager para generar gráficas
- Genera reportes completos (CSV, JSON, TXT)
- Soporta múltiples réplicas para análisis estadístico
- Incluye argumentos de línea de comandos para flexibilidad
- Está completamente documentado

**Listo para producción** ✅
