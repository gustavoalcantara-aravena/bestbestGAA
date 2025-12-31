# 🎨 Visualización - Integración con Estructura de Output

## ✅ Verificación Completada

Se ha verificado y actualizado el módulo de visualización para **respetar completamente** la estructura de output del proyecto definida en `config.yaml` y `problema_metaheuristica.md`.

---

## 📁 Estructura de Output Garantizada

### Modo: Todos los Datasets (ALL)

```
output/results/all_datasets/{DD-MM-YY_HH-MM-SS}/
├── convergence_plot.png              ← Fitness vs iteraciones
├── convergence_ensemble_plot.png     ← Promediada de N ejecuciones
├── boxplot_robustness.png            ← Distribución estadística
├── scalability_plot.png              ← |V| vs Tiempo
├── conflict_heatmap.png              ← Matriz n×n de conflictos
├── time_quality_tradeoff.png         ← Computación vs Calidad
└── summary.json                      ← Resumen de datos
```

### Modo: Dataset Específico (SPECIFIC)

```
output/results/specific_datasets/{FAMILY}/{DD-MM-YY_HH-MM-SS}/
├── convergence_plot.png
├── boxplot_robustness.png
├── scalability_plot.png
├── conflict_heatmap.png
├── time_quality_tradeoff.png
└── summary.json
```

**Familias DIMACS soportadas**: CUL, DSJ, LEI, MYC, REG, SCH, SGB

---

## 🔧 Configuración en config.yaml

El `PlotManager` lee automáticamente:

```yaml
output:
  results_dir: "./output/results"
  solutions_dir: "./output/solutions"
  logs_dir: "./output/logs"
  plots_dir: "./output/plots"
  
  save_csv: true
  save_json: true
  save_txt: true
```

**Nota**: Las visualizaciones se guardan en `results_dir` con la estructura timestamped.

---

## 💻 Uso Integrado

### Opción 1: Cargar config automáticamente

```python
from visualization import PlotManager

# PlotManager busca config.yaml automáticamente
manager = PlotManager()
manager.create_session_dir(mode="all_datasets")

results = manager.plot_all(experiment_data)
```

### Opción 2: Especificar path explícitamente

```python
manager = PlotManager(
    output_dir="output/results",
    config_path="config/config.yaml"
)
manager.create_session_dir(mode="all_datasets")
```

### Opción 3: Dataset específico

```python
# Para familia DSJ
manager.create_session_dir(mode="specific_datasets/DSJ")
results = manager.plot_all(experiment_data)
# Guarda en: output/results/specific_datasets/DSJ/{timestamp}/
```

---

## 📋 Ciclo de Integración Completo

### En tu script de experimentación:

```python
from visualization import PlotManager
from pathlib import Path

def main():
    # 1. Crear gestor
    manager = PlotManager()
    
    # 2. Crear directorio de sesión
    session_dir = manager.create_session_dir(mode="all_datasets")
    print(f"Resultados se guardarán en: {session_dir}")
    
    # 3. Ejecutar experimentos
    experiment_data = {
        'instance_name': 'DSJC250.1',
        'convergence': ils_history.best_fitness,
        'times': ils_history.times,
        'convergence_histories': all_histories,
        'robustness': final_results,
        'bks': 64,
        'vertices': [50, 100, 150, 200],
        'times_scalability': [0.1, 0.3, 0.8, 1.5],
        'conflict_matrix': solution.conflict_matrix,
        'time_fitness_pairs': list(zip(times, fitness))
    }
    
    # 4. Generar visualizaciones
    viz_results = manager.plot_all(experiment_data, create_session=False)
    
    # 5. Guardar resumen
    manager.save_summary(experiment_data)
    
    # 6. Verificar
    print("\n✓ Visualizaciones generadas:")
    for plot_type, path in viz_results.items():
        print(f"  - {plot_type}: {path}")

if __name__ == "__main__":
    main()
```

---

## 🔍 Garantías de Integración

### ✅ Respeto de Estructura

- ✅ Crea directorios según `output/results/{modo}/{timestamp}/`
- ✅ Respeta configuración en `config.yaml`
- ✅ No sobrescribe ejecuciones previas (timestamp único)
- ✅ Crea directorios automáticamente

### ✅ Compatibilidad

- ✅ Compatible con scripts existentes del proyecto
- ✅ Mantiene coherencia con `problema_metaheuristica.md`
- ✅ Integrable con `config.yaml`
- ✅ Logging automático de operaciones

### ✅ Robustez

- ✅ Manejo de excepciones
- ✅ Validación de datos
- ✅ Mensajes informativos
- ✅ Creación automática de directorios

---

## 📊 Verificación de Rutas

### Script de prueba rápida:

```python
from visualization import PlotManager
from pathlib import Path

# Crear gestor
manager = PlotManager()

# Crear sesión
session = manager.create_session_dir(mode="all_datasets")
print(f"Sesión creada: {session}")

# Verificar estructura
print(f"\n✓ Ruta absoluta: {session.absolute()}")
print(f"✓ Existe: {session.exists()}")
print(f"✓ Escribible: {os.access(session, os.W_OK)}")

# Probar generación
import numpy as np
data = {
    'instance_name': 'Test',
    'convergence': [50, 48, 46, 45],
    'times': [0.1, 0.2, 0.4, 0.7],
    'conflict_matrix': np.zeros((10, 10))
}

results = manager.plot_all(data, create_session=False)
print(f"\n✓ Gráficas generadas: {len(results)}")
for name, path in results.items():
    print(f"  - {Path(path).relative_to(manager.output_dir)}")
```

---

## 🚀 Próxima Integración

### Para integrar en tu experimento:

1. **Importar PlotManager**:
   ```python
   from visualization import PlotManager
   ```

2. **Crear instancia al inicio**:
   ```python
   manager = PlotManager()
   manager.create_session_dir(mode="all_datasets")
   ```

3. **Después de ejecutar ILS**:
   ```python
   results = manager.plot_all(experiment_data, create_session=False)
   manager.save_summary(experiment_data)
   ```

4. **Verificar output**:
   ```bash
   # Ver gráficas generadas
   ls -la output/results/all_datasets/*/
   ```

---

## 📝 Documentación Relacionada

- **README.md** - Guía completa del módulo
- **INTEGRATION_GUIDE.py** - 4 ejemplos de integración
- **example_usage.py** - Ejemplos ejecutables
- **problema_metaheuristica.md** - Especificación de output

---

## ✨ Estado Final

**🟢 VERIFICADO Y LISTO**

El módulo de visualización:
- ✅ Respeta la estructura de output del proyecto
- ✅ Integra automáticamente con config.yaml
- ✅ Crea directorios correctamente
- ✅ Mantiene historiales de ejecuciones
- ✅ Listo para integración inmediata

---

*Última verificación: 31 de Diciembre de 2025*
