# 🔬 PRÓXIMOS PASOS - GUÍA DE EXPERIMENTOS

**Ahora que el framework está completo, aquí hay opciones para continuar**

---

## 🎯 OPCIÓN 1: Ejecutar Pruebas Rápidas (15 minutos)

### Test de Validación Rápida
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\GAA-GCP-ILS-4

# Test rápido (validación de instalación)
python scripts/test_quick.py

# Output esperado:
# ✓ Core importado
# ✓ Operators importados
# ✓ Metaheuristic importado
# ✓ Configuración cargada
```

### Suite de Testing
```bash
# Todos los tests
pytest tests/ -v

# Solo Core (rápido)
pytest tests/test_core.py -v

# Con cobertura
pytest tests/ --cov=core --cov=operators --cov=metaheuristic
```

---

## 🧪 OPCIÓN 2: Experimento Simple (30 minutos)

### Crear Script de Prueba
```python
# test_single_instance.py
import time
from core import GraphColoringProblem, ColoringEvaluator
from metaheuristic import IteratedLocalSearch

# Cargar instancia pequeña
problem = GraphColoringProblem.load_from_dimacs(
    "datasets/myciel3.col"
)

print(f"Problema: {problem.name}")
print(f"Vértices: {problem.n_vertices}, Aristas: {problem.n_edges}")
print(f"Óptimo conocido: {problem.colors_known}\n")

# Ejecutar ILS
start = time.time()
ils = IteratedLocalSearch(
    problem,
    max_iterations=100,
    time_budget=10.0,
    seed=42,
    verbose=True
)

best_solution, history = ils.solve()
elapsed = time.time() - start

# Resultados
metrics = ColoringEvaluator.evaluate(best_solution, problem)
print(f"\n=== RESULTADOS ===")
print(f"Colores: {metrics['num_colors']}")
print(f"Óptimo: {problem.colors_known}")
print(f"Gap: {metrics['gap']} ({metrics['gap_percent']:.2f}%)")
print(f"Tiempo: {elapsed:.2f}s")
print(f"Iteraciones: {len(history.iterations)}")
```

### Ejecutar
```bash
python test_single_instance.py
```

---

## 📊 OPCIÓN 3: Comparación de Constructores (1 hora)

### Script: Comparar Métodos Iniciales
```python
# compare_constructors.py
import time
from core import GraphColoringProblem, ColoringEvaluator
from operators import GreedyDSATUR, GreedyLF, RandomSequential, compare_constructives

# Cargar varias instancias
instances = [
    "datasets/myciel3.col",
    "datasets/myciel4.col",
    "datasets/myciel5.col",
]

print("=" * 60)
print("COMPARACIÓN DE OPERADORES CONSTRUCTIVOS")
print("=" * 60)

for instance_file in instances:
    problem = GraphColoringProblem.load_from_dimacs(instance_file)
    
    print(f"\n{problem.name} ({problem.n_vertices} vértices)")
    print("-" * 40)
    
    # Comparar constructivos
    stats = compare_constructives(problem, num_trials=5)
    
    for method, stat in stats.items():
        print(f"{method:12} | min={stat['min_colors']:2d} "
              f"max={stat['max_colors']:2d} "
              f"mean={stat['mean_colors']:5.1f} "
              f"std={stat['std_colors']:5.2f}")
```

### Ejecutar
```bash
python compare_constructors.py
```

---

## 🔍 OPCIÓN 4: Análisis de Perturbación (1 hora)

### Script: Visualizar Estrategias
```python
# analyze_perturbation.py
from metaheuristic import (
    ConstantPerturbation, LinearPerturbation, ExponentialPerturbation,
    DynamicPerturbation, create_schedule
)
import matplotlib.pyplot as plt

# Crear schedules
schedules = {
    'Constant': create_schedule('constant', strength=0.2),
    'Linear': create_schedule('linear', initial_strength=0.1, final_strength=0.5, plateau_iterations=50),
    'Exponential': create_schedule('exponential', initial_strength=0.1, growth_factor=1.1),
    'Dynamic': create_schedule('dynamic', window_size=20),
}

# Simular iteraciones
iterations = 200
results = {name: [] for name in schedules.keys()}

no_improvement = 0
improvement_history = []

for i in range(iterations):
    # Simular mejora ocasional
    if i % 40 == 0:
        improvement_history.append(0.5)
        no_improvement = 0
    else:
        improvement_history.append(0.0)
        no_improvement += 1
    
    for name, schedule in schedules.items():
        strength = schedule.get_strength(
            i,
            no_improvement_count=no_improvement,
            improvement_history=improvement_history
        )
        results[name].append(strength)

# Graficar
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
for name, strengths in results.items():
    plt.plot(strengths, label=name, linewidth=2)

plt.xlabel('Iteración')
plt.ylabel('Intensidad de Perturbación')
plt.title('Comparación de Estrategias de Perturbación')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('perturbation_strategies.png', dpi=100)
plt.show()
```

### Ejecutar
```bash
python analyze_perturbation.py
```

---

## 🏃 OPCIÓN 5: Experimento Multi-Instancia (2-3 horas)

### Script: Ejecutar en Múltiples Instancias
```python
# experiment_multiple.py
import os
import time
import json
from glob import glob
from core import GraphColoringProblem, ColoringEvaluator
from metaheuristic import IteratedLocalSearch

# Buscar archivos .col
dataset_dir = "datasets"
instances = sorted(glob(os.path.join(dataset_dir, "**/*.col"), recursive=True))[:10]

results = []

print("Ejecutando experimentos en múltiples instancias...")
print(f"Total: {len(instances)} instancias\n")

for instance_path in instances:
    filename = os.path.basename(instance_path)
    
    try:
        # Cargar problema
        problem = GraphColoringProblem.load_from_dimacs(instance_path)
        
        # Ejecutar ILS
        start = time.time()
        ils = IteratedLocalSearch(
            problem,
            max_iterations=200,
            time_budget=30.0,
            seed=42,
            verbose=False
        )
        best_solution, history = ils.solve()
        elapsed = time.time() - start
        
        # Evaluar
        metrics = ColoringEvaluator.evaluate(best_solution, problem)
        
        # Registrar
        result = {
            'instance': filename,
            'vertices': problem.n_vertices,
            'edges': problem.n_edges,
            'optimal': problem.colors_known,
            'colors': metrics['num_colors'],
            'gap': metrics['gap'],
            'gap_percent': metrics['gap_percent'],
            'time_seconds': elapsed,
            'iterations': len(history.iterations),
            'feasible': metrics['feasible']
        }
        results.append(result)
        
        print(f"✓ {filename:20} | "
              f"{metrics['num_colors']:2d} colores "
              f"({metrics['gap_percent']:5.1f}% gap) "
              f"{elapsed:6.2f}s")
        
    except Exception as e:
        print(f"✗ {filename}: {str(e)}")

# Guardar resultados
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Mostrar resumen
print(f"\n=== RESUMEN ===")
print(f"Instancias procesadas: {len(results)}")
print(f"Gap promedio: {sum(r['gap_percent'] for r in results)/len(results):.2f}%")
print(f"Tiempo promedio: {sum(r['time_seconds'] for r in results)/len(results):.2f}s")
print(f"Resultados guardados en: results.json")
```

### Ejecutar
```bash
python experiment_multiple.py
```

---

## 📈 OPCIÓN 6: Análisis Estadístico (2 horas)

### Script: Comparar Múltiples Ejecuciones
```python
# statistical_analysis.py
import numpy as np
from core import GraphColoringProblem
from metaheuristic import IteratedLocalSearch

problem = GraphColoringProblem.load_from_dimacs("datasets/myciel5.col")

# Ejecutar múltiples veces
num_runs = 20
results = []

print(f"Ejecutando {num_runs} réplicas independientes...")

for run in range(num_runs):
    ils = IteratedLocalSearch(
        problem,
        max_iterations=500,
        time_budget=30.0,
        seed=run,  # Diferentes seeds
        verbose=False
    )
    
    best_solution, _ = ils.solve()
    colors = best_solution.num_colors
    results.append(colors)
    
    print(f"Run {run+1:2d}: {colors} colores")

# Estadísticas
results = np.array(results)
print(f"\n=== ESTADÍSTICAS ===")
print(f"Media:     {np.mean(results):.2f}")
print(f"Mediana:   {np.median(results):.0f}")
print(f"Desv. Est: {np.std(results):.2f}")
print(f"Mínimo:    {np.min(results)}")
print(f"Máximo:    {np.max(results)}")
print(f"CV:        {np.std(results)/np.mean(results)*100:.1f}%")
```

### Ejecutar
```bash
python statistical_analysis.py
```

---

## 🎯 OPCIÓN 7: Crear Demo Interactivo (2 horas)

### Script: Demo Paso a Paso
```python
# demo_interactive.py
from core import GraphColoringProblem, ColoringEvaluator
from operators import GreedyDSATUR, KempeChain
from metaheuristic import IteratedLocalSearch

print("=" * 60)
print("DEMO INTERACTIVO - Graph Coloring Problem")
print("=" * 60)

# 1. Cargar problema
print("\n[1] Cargar problema...")
problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
print(f"    ✓ {problem.name}")
print(f"    Vértices: {problem.n_vertices}, Aristas: {problem.n_edges}")
print(f"    Óptimo: {problem.colors_known} colores")

# 2. Construir solución
print("\n[2] Construir solución inicial (DSATUR)...")
initial = GreedyDSATUR.construct(problem)
metrics = ColoringEvaluator.evaluate(initial, problem)
print(f"    ✓ {metrics['num_colors']} colores, {metrics['conflicts']} conflictos")

# 3. Mejorar
print("\n[3] Aplicar búsqueda local (KempeChain)...")
improved = KempeChain.improve(initial, problem, max_iterations=50)
metrics = ColoringEvaluator.evaluate(improved, problem)
print(f"    ✓ {metrics['num_colors']} colores, {metrics['conflicts']} conflictos")

# 4. ILS
print("\n[4] Ejecutar ILS completo...")
ils = IteratedLocalSearch(problem, max_iterations=100, verbose=True)
best, history = ils.solve()

# 5. Mostrar resultado
print("\n[5] Resultado final...")
final_metrics = ColoringEvaluator.evaluate(best, problem)
print(ColoringEvaluator.format_result(best, problem))

print("\n✅ Demo completado")
```

### Ejecutar
```bash
python demo_interactive.py
```

---

## 🚀 PRÓXIMOS PASOS RECOMENDADOS

### Corto Plazo (Hoy)
1. ✅ Ejecutar `test_quick.py` para validación
2. ✅ Correr `compare_constructors.py` para entender operadores
3. ✅ Ver `analyze_perturbation.py` para visualizar estrategias

### Mediano Plazo (Esta Semana)
1. ✅ Experimento multi-instancia con `experiment_multiple.py`
2. ✅ Análisis estadístico con `statistical_analysis.py`
3. ✅ Comparación de configuraciones

### Largo Plazo (Este Mes)
1. ✅ Experimentos en 79 datasets DIMACS
2. ✅ Publicación de resultados con gráficas
3. ✅ Comparación con otros algoritmos (GRASP, SA, GA)

---

## 📊 Comandos Útiles

```bash
# Validación rápida
python scripts/test_quick.py

# Tests unitarios
pytest tests/ -v

# Generar documento de perturbación
python metaheuristic/perturbation_schedules.py

# Ejemplo constructivos
python operators/constructive.py

# Ejemplo mejora
python operators/improvement.py

# Ejemplo perturbación
python operators/perturbation.py

# Ejemplo reparación
python operators/repair.py

# Ejemplo ILS
python metaheuristic/ils_core.py
```

---

## 📝 Notas Importantes

- **Reproducibilidad**: Usar `seed` para resultados consistentes
- **Presupuesto**: Ajustar `time_budget` y `max_iterations` según necesidad
- **Configuración**: Editar `config/config.yaml` para cambios globales
- **Logging**: Ver historial en `history.iterations`, `history.best_fitness`
- **Datasets**: 79 instancias DIMACS disponibles en `datasets/`

---

**¡Framework listo para empezar experimentos!** 🚀

Cualquier pregunta, revisar documentación en:
- `QUICK_START_GUIDE.md`
- `MODULES_REFERENCE.md`
- `OPERATORS_METAHEURISTIC_COMPLETE.md`
