# PROPUESTA DE UNIFICACIÓN DE OUTPUTS

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025  
**Objetivo**: Unificar todos los outputs del proyecto en una estructura coherente

---

## 📊 ANÁLISIS DEL SISTEMA ACTUAL

### Outputs Identificados en el Código:

#### 1. **Script: `gaa_experiment.py`**
```python
# Líneas 241-242
output_dir = project_root / "output" / "gaa"
```
**Outputs generados**:
- `output/gaa/best_algorithm_{timestamp}.json`
- `output/gaa/evolution_history_{timestamp}.json`
- `output/gaa/summary_{timestamp}.txt`

#### 2. **Script: `gaa_quick_demo.py`**
**Outputs**: Solo consola (sin archivos)

#### 3. **Script: `test_quick.py`**
**Outputs**: Solo consola (sin archivos)

#### 4. **Módulo: `visualization/plotter.py`**
```python
# Líneas 89-117
def create_session_dir(self, mode: str = "all_datasets") -> Path:
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    
    if mode.startswith("specific_datasets/"):
        family = mode.split("/")[1]
        session_dir = self.output_dir / "specific_datasets" / family / timestamp
    else:
        session_dir = self.output_dir / "all_datasets" / timestamp
```

**Outputs generados**:
- `output/plots/all_datasets/{timestamp}/convergence_plot.png`
- `output/plots/all_datasets/{timestamp}/boxplot_robustness.png`
- `output/plots/all_datasets/{timestamp}/time_quality_tradeoff.png`
- `output/plots/all_datasets/{timestamp}/scalability_plot.png`
- `output/plots/all_datasets/{timestamp}/conflict_heatmap.png`
- `output/plots/specific_datasets/{family}/{timestamp}/...`

#### 5. **Configuración: `config.yaml`**
```yaml
output:
  results_dir: "./output/results"
  solutions_dir: "./output/solutions"
  logs_dir: "./output/logs"
  plots_dir: "./output/plots"
```

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### 1. **Inconsistencia de Directorios**
- `gaa_experiment.py` → `output/gaa/`
- `plotter.py` → `output/plots/`
- `config.yaml` → `output/results/`, `output/solutions/`, `output/logs/`, `output/plots/`

### 2. **Falta de Integración**
- Los scripts no usan la estructura definida en `config.yaml`
- `PlotManager` tiene su propia lógica de directorios
- No hay un módulo centralizado de gestión de outputs

### 3. **Formatos de Timestamp Inconsistentes**
- `gaa_experiment.py`: `"%d-%m-%y_%H-%M-%S"` (DD-MM-YY_HH-MM-SS)
- `plotter.py`: `"%d-%m-%y_%H-%M-%S"` (DD-MM-YY_HH-MM-SS)
- ✅ Al menos estos dos son consistentes

### 4. **Estructura No Alineada con .md**
El archivo `problema_metaheuristica.md` (líneas 691-734) especifica:
```
output/
├── results/
│   ├── all_datasets/{timestamp}/
│   └── specific_datasets/{family}/{timestamp}/
├── solutions/
└── logs/
```

Pero el código actual genera:
```
output/
├── gaa/
├── plots/
├── results/
├── solutions/
└── logs/
```

---

## ✅ PROPUESTA DE ESTRUCTURA UNIFICADA

### Estructura de Directorios:

```
output/
├── results/
│   ├── all_datasets/
│   │   └── {timestamp}/
│   │       ├── summary.csv
│   │       ├── detailed_results.json
│   │       ├── statistics.txt
│   │       ├── convergence_plot.png
│   │       ├── boxplot_robustness.png
│   │       ├── time_quality_tradeoff.png
│   │       ├── scalability_plot.png
│   │       └── conflict_heatmap.png
│   │
│   ├── specific_datasets/
│   │   ├── CUL/{timestamp}/
│   │   ├── DSJ/{timestamp}/
│   │   ├── LEI/{timestamp}/
│   │   ├── MYC/{timestamp}/
│   │   ├── REG/{timestamp}/
│   │   ├── SCH/{timestamp}/
│   │   └── SGB/{timestamp}/
│   │
│   └── gaa_experiments/
│       └── {timestamp}/
│           ├── best_algorithm.json
│           ├── evolution_history.json
│           ├── summary.txt
│           └── convergence_plot.png
│
├── solutions/
│   ├── {instance_name}_{timestamp}.sol
│   └── ...
│
└── logs/
    ├── execution_{timestamp}.log
    └── ...
```

### Formato de Timestamp Unificado:
```
DD-MM-YY_HH-MM-SS
Ejemplo: 31-12-25_19-30-45
```

---

## 🎯 TIPOS DE OUTPUTS CONTEMPLADOS

### 1. **Outputs de Datos** (Archivos)

#### A. Resultados Tabulares
- **`summary.csv`**: Tabla resumen de todas las instancias
  ```csv
  Instance,Dataset,Vertices,Edges,BKS,Colors,Feasible,Gap,Gap(%),Time(s),Conflicts
  ```

#### B. Resultados Detallados
- **`detailed_results.json`**: Información completa en formato JSON
  ```json
  {
    "metadata": {...},
    "algorithm_config": {...},
    "results": [...],
    "statistics": {...}
  }
  ```

#### C. Reportes de Texto
- **`statistics.txt`**: Reporte legible para humanos
  ```
  ═══════════════════════════════════════════════
  NEW-GCP-ILS-OK - REPORT
  ═══════════════════════════════════════════════
  ```

#### D. Archivos de Solución
- **`{instance}_{timestamp}.sol`**: Solución específica
  ```
  c Solution for myciel3.col
  c Colors: 4
  c Feasible: True
  1 0
  2 1
  3 2
  ...
  ```

#### E. Logs de Ejecución
- **`execution_{timestamp}.log`**: Log detallado
  ```
  [2025-12-31 19:30:45] INFO: Starting ILS...
  [2025-12-31 19:30:46] INFO: Iteration 1: 5 colors
  ```

---

### 2. **Outputs Visuales** (Gráficas)

#### A. Convergencia
- **`convergence_plot.png`**: Fitness vs iteraciones
- **`convergence_ensemble_plot.png`**: Promedio de múltiples runs

#### B. Robustez Estadística
- **`boxplot_robustness.png`**: Distribución de resultados
- **`boxplot_multi_instances.png`**: Comparación entre instancias

#### C. Escalabilidad
- **`scalability_plot.png`**: Tiempo vs tamaño de instancia
- **`scalability_iterations.png`**: Iteraciones vs tamaño

#### D. Tiempo-Calidad
- **`time_quality_tradeoff.png`**: Trade-off tiempo/calidad
- **`convergence_speed.png`**: Velocidad de convergencia

#### E. Análisis de Conflictos
- **`conflict_heatmap.png`**: Matriz de conflictos
- **`conflict_distribution.png`**: Distribución de conflictos
- **`conflict_statistics.png`**: Estadísticas de conflictos

---

### 3. **Outputs de GAA** (Específicos)

#### A. Algoritmos Generados
- **`best_algorithm.json`**: Mejor algoritmo encontrado (AST)
- **`population_{gen}.json`**: Población en generación N
- **`algorithm_pseudocode.txt`**: Pseudocódigo legible

#### B. Evolución
- **`evolution_history.json`**: Historial completo de evolución
- **`fitness_evolution.png`**: Gráfica de evolución de fitness
- **`diversity_plot.png`**: Diversidad de población

#### C. Análisis de Algoritmos
- **`algorithm_statistics.json`**: Estadísticas de algoritmos generados
- **`operator_usage.png`**: Frecuencia de uso de operadores
- **`structure_analysis.png`**: Análisis de estructuras generadas

---

### 4. **Outputs de Consola** (Tiempo Real)

#### A. Progreso de Ejecución
```
[Iter 50/500] Actual: 4 colores | Mejor: 4 | Tiempo: 2.3s
```

#### B. Métricas Intermedias
```
✅ Mejora encontrada: 5 → 4 colores
⚠️  Estancamiento detectado (30 iteraciones)
```

#### C. Resumen Final
```
════════════════════════════════════════════════
RESULTADO FINAL
════════════════════════════════════════════════
Mejor solución: 4 colores
Gap a BKS: 0.0%
Tiempo total: 3.2s
════════════════════════════════════════════════
```

---

## 🔧 MÓDULO CENTRALIZADO: `OutputManager`

### Propuesta de Implementación:

```python
# utils/output_manager.py

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import csv
import logging

class OutputManager:
    """
    Gestor centralizado de outputs del proyecto.
    
    Responsabilidades:
    - Crear estructura de directorios
    - Generar timestamps consistentes
    - Guardar archivos en ubicaciones correctas
    - Integrar con PlotManager
    - Gestionar logs
    """
    
    def __init__(self, config_path: Optional[str] = None):
        # Cargar configuración
        self.config = self._load_config(config_path)
        
        # Directorios base
        self.base_dir = Path(self.config.get('output', {}).get('results_dir', 'output/results'))
        self.solutions_dir = Path(self.config.get('output', {}).get('solutions_dir', 'output/solutions'))
        self.logs_dir = Path(self.config.get('output', {}).get('logs_dir', 'output/logs'))
        
        # Crear directorios
        self._create_base_dirs()
        
        # Session actual
        self.session_dir = None
        self.timestamp = None
    
    def create_session(self, mode: str = "all_datasets", family: Optional[str] = None) -> Path:
        """
        Crea una sesión de ejecución con timestamp.
        
        Args:
            mode: "all_datasets", "specific_dataset", "gaa_experiment"
            family: Familia de dataset (para modo specific)
        
        Returns:
            Path del directorio de sesión
        """
        self.timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        
        if mode == "all_datasets":
            self.session_dir = self.base_dir / "all_datasets" / self.timestamp
        elif mode == "specific_dataset":
            if not family:
                raise ValueError("Family required for specific_dataset mode")
            self.session_dir = self.base_dir / "specific_datasets" / family / self.timestamp
        elif mode == "gaa_experiment":
            self.session_dir = self.base_dir / "gaa_experiments" / self.timestamp
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        self.session_dir.mkdir(parents=True, exist_ok=True)
        return self.session_dir
    
    def save_summary_csv(self, data: List[Dict[str, Any]]) -> str:
        """Guarda summary.csv"""
        filepath = self.session_dir / "summary.csv"
        
        if not data:
            return str(filepath)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return str(filepath)
    
    def save_detailed_json(self, data: Dict[str, Any]) -> str:
        """Guarda detailed_results.json"""
        filepath = self.session_dir / "detailed_results.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def save_statistics_txt(self, content: str) -> str:
        """Guarda statistics.txt"""
        filepath = self.session_dir / "statistics.txt"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def save_solution(self, instance_name: str, solution: 'ColoringSolution') -> str:
        """Guarda archivo .sol"""
        filename = f"{instance_name}_{self.timestamp}.sol"
        filepath = self.solutions_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"c Solution for {instance_name}\n")
            f.write(f"c Colors: {solution.num_colors}\n")
            f.write(f"c Feasible: {solution.is_feasible()}\n")
            for vertex, color in sorted(solution.assignment.items()):
                f.write(f"{vertex} {color}\n")
        
        return str(filepath)
    
    def get_plot_dir(self) -> Path:
        """Retorna directorio para gráficas de la sesión actual"""
        return self.session_dir
    
    def create_log_file(self) -> str:
        """Crea archivo de log para la sesión"""
        filename = f"execution_{self.timestamp}.log"
        filepath = self.logs_dir / filename
        return str(filepath)
```

---

## 🔄 INTEGRACIÓN CON MÓDULOS EXISTENTES

### 1. Actualizar `PlotManager`

```python
# visualization/plotter.py

class PlotManager:
    def __init__(self, output_manager: OutputManager):
        self.output_manager = output_manager
        self.output_dir = output_manager.get_plot_dir()
```

### 2. Actualizar Scripts

```python
# scripts/gaa_experiment.py

from utils.output_manager import OutputManager

def main():
    # Crear gestor de outputs
    output_mgr = OutputManager()
    session_dir = output_mgr.create_session(mode="gaa_experiment")
    
    # Ejecutar experimento
    solver = GAASolver(...)
    best_algorithm, best_fitness = solver.evolve()
    
    # Guardar resultados usando OutputManager
    output_mgr.save_detailed_json({
        'best_algorithm': best_algorithm.to_dict(),
        'best_fitness': best_fitness,
        'history': solver.history
    })
    
    output_mgr.save_statistics_txt(generate_summary_text(...))
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Crear Módulo Base
- [ ] Crear `utils/output_manager.py`
- [ ] Implementar `OutputManager` con métodos básicos
- [ ] Integrar con `config.yaml`
- [ ] Crear tests unitarios

### Fase 2: Integrar con Visualización
- [ ] Modificar `PlotManager` para usar `OutputManager`
- [ ] Actualizar métodos de guardado de gráficas
- [ ] Verificar compatibilidad con estructura de directorios

### Fase 3: Actualizar Scripts
- [ ] Actualizar `gaa_experiment.py`
- [ ] Actualizar `gaa_quick_demo.py` (agregar guardado)
- [ ] Actualizar `test_quick.py` (agregar guardado)
- [ ] Crear script de experimentación completo

### Fase 4: Documentación
- [ ] Actualizar README con nueva estructura
- [ ] Crear guía de uso de `OutputManager`
- [ ] Documentar formatos de archivos

### Fase 5: Testing
- [ ] Probar generación de outputs en modo `all_datasets`
- [ ] Probar generación de outputs en modo `specific_dataset`
- [ ] Probar generación de outputs en modo `gaa_experiment`
- [ ] Verificar integridad de archivos generados

---

## 🎯 BENEFICIOS DE LA UNIFICACIÓN

### 1. **Consistencia**
✅ Todos los outputs en ubicaciones predecibles  
✅ Formato de timestamp único  
✅ Nomenclatura estandarizada

### 2. **Mantenibilidad**
✅ Un solo punto de cambio para estructura de outputs  
✅ Código más limpio y DRY  
✅ Fácil de extender

### 3. **Trazabilidad**
✅ Cada sesión tiene timestamp único  
✅ Fácil correlacionar outputs de una ejecución  
✅ Logs centralizados

### 4. **Compatibilidad**
✅ Alineado con especificación del .md  
✅ Compatible con config.yaml  
✅ Integrado con PlotManager existente

### 5. **Usabilidad**
✅ Estructura clara para el usuario  
✅ Fácil encontrar resultados  
✅ Archivos bien organizados

---

## 📊 RESUMEN DE OUTPUTS POR TIPO DE EJECUCIÓN

### Ejecución ILS Estándar (all_datasets):
```
output/results/all_datasets/31-12-25_19-30-45/
├── summary.csv                    # Tabla de resultados
├── detailed_results.json          # Datos completos
├── statistics.txt                 # Reporte legible
├── convergence_plot.png           # Gráfica convergencia
├── boxplot_robustness.png         # Boxplot robustez
├── time_quality_tradeoff.png      # Tiempo vs calidad
├── scalability_plot.png           # Escalabilidad
└── conflict_heatmap.png           # Mapa de conflictos
```

### Ejecución Específica (familia DSJ):
```
output/results/specific_datasets/DSJ/31-12-25_19-30-45/
├── summary.csv
├── detailed_results.json
├── statistics.txt
└── [gráficas...]
```

### Experimento GAA:
```
output/results/gaa_experiments/31-12-25_19-30-45/
├── best_algorithm.json            # Mejor algoritmo (AST)
├── evolution_history.json         # Historial evolución
├── summary.txt                    # Resumen textual
├── fitness_evolution.png          # Evolución fitness
└── algorithm_pseudocode.txt       # Pseudocódigo
```

### Soluciones:
```
output/solutions/
├── myciel3_31-12-25_19-30-45.sol
├── DSJC125_31-12-25_19-30-45.sol
└── ...
```

### Logs:
```
output/logs/
├── execution_31-12-25_19-30-45.log
└── ...
```

---

## ✅ CONCLUSIÓN

Esta propuesta unifica **TODOS** los outputs del proyecto en una estructura coherente, mantenible y alineada con las especificaciones del archivo `problema_metaheuristica.md`.

**Outputs contemplados**: 15+ tipos de archivos organizados en 3 categorías principales.

**Próximo paso**: Implementar el módulo `OutputManager` y actualizar los scripts existentes.
