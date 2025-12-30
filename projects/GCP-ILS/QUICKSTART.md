# QUICKSTART - GCP-ILS Ejecución Rápida

## 🚀 Inicio Rápido

### Opción 1: Ejecución Simple (Recomendado para comenzar)

```bash
cd projects/GCP-ILS

# Ejecutar ILS sobre una instancia pequeña
python scripts/run.py CUL10

# Ejemplo de salida:
# ============================================================
# Result: k = 3
# Time: 0.45s
# Iterations: 200
# Gap to optimal: 1 (33.33%)
# ============================================================
# ✓ Solution is feasible
```

### Opción 2: Demo Completa (Múltiples instancias)

```bash
cd projects/GCP-ILS

# Ejecutar demo en 4 instancias diferentes
python scripts/demo_complete.py

# Mostrará:
# - Instancias probadas con sus parámetros
# - Colores encontrados (k)
# - Tiempos de ejecución
# - Tabla resumen comparativa
```

### Opción 3: Ejecución Personalizada

```bash
# Usar operador constructivo Largest First
python scripts/run.py DSJ10 --constructive lf

# Usar búsqueda tabu
python scripts/run.py LEI10 --local-search tabu

# Parametrización completa
python scripts/run.py MYC02 \
  --constructive rlf \
  --local-search ovm \
  --perturbation partial_destroy \
  --max-iterations 1000 \
  --perturbation-strength 0.3 \
  --restart-threshold 75 \
  --seed 42 \
  --verbose
```

### Opción 4: Ejecución Desde Python

```python
import sys
sys.path.insert(0, 'projects/GCP-ILS')

from data.loader import DataLoader
from metaheuristic.ils_core import IteratedLocalSearch

# Cargar instancia
loader = DataLoader('projects/GCP-ILS/datasets')
problem = loader.load('CUL10')

# Crear y ejecutar ILS
ils = IteratedLocalSearch(
    problem=problem,
    constructive='dsatur',
    max_iterations=500,
    seed=42,
    verbose=True
)

best_solution, stats = ils.run()

print(f"\nResultado: k = {stats['best_k']}")
print(f"Tiempo: {stats['total_time']:.2f}s")
print(f"Iteraciones: {stats['iterations_completed']}")
```

---

## 📊 Instancias Disponibles

### Pequeñas (Rápidas, <1s)
- **CUL** (6): CUL10, CUL100, CUL200, CUL300, CUL400, CUL500
- **DSJ** (12): DSJ10, DSJ50, DSJ100, DSJ150, DSJ200, DSJ250, ...
- **LEI** (12): LEI10, LEI50, LEI100, ...
- **MYC** (4): MYC02, MYC03, MYC04, MYC05
- **REG** (13): REG10, REG20, REG30, ...
- **SCH** (2): SCHOOL1, SCHOOL1_NEQ
- **SGB** (24): SGB25, SGB50, SGB75, ...

### Medianas (2-5s)
- CUL600, CUL700, CUL800
- DSJ300, DSJ350, DSJ400, DSJ450, DSJ500, DSJ550
- LEI150, LEI200, LEI250

### Grandes (>10s)
- CUL900, CUL1000
- DSJ600, DSJ700, DSJ750, DSJ800
- LEI300, LEI400, LEI500

---

## 🔧 Opciones de Línea de Comandos

```
Uso: python scripts/run.py <instance> [options]

Parámetros obligatorios:
  instance              Nombre de la instancia (e.g., CUL10, DSJ50)

Parámetros opcionales:
  -c, --constructive    Operador constructivo (default: dsatur)
                       Opciones: dsatur, lf, sl, rs, rlf
  
  -ls, --local-search  Operador local search (default: kempe)
                       Opciones: kempe, tabu, ovm, swap
  
  -p, --perturbation   Operador de perturbación (default: random_recolor)
                       Opciones: random_recolor, partial_destroy
  
  -i, --max-iterations Máximo de iteraciones (default: 500)
  
  -ps, --perturbation-strength  Intensidad de perturbación 0.0-1.0 (default: 0.2)
  
  -rt, --restart-threshold  Iteraciones sin mejora antes de reiniciar (default: 50)
  
  -s, --seed           Semilla aleatoria (default: random)
  
  -v, --verbose        Modo verboso con salida detallada
  
  --dataset-root       Ruta al directorio de datasets
```

---

## 📈 Ejemplos de Configuraciones

### Configuración 1: Rápida y Confiable (DSATUR + Kempe)
```bash
python scripts/run.py CUL10
# Tiempo esperado: 0.3-0.5s
# Calidad: Buena (cercana a óptimo)
```

### Configuración 2: Búsqueda Tabu (Más Potente)
```bash
python scripts/run.py DSJ10 --local-search tabu --max-iterations 1000
# Tiempo esperado: 1-2s
# Calidad: Muy buena
```

### Configuración 3: Explorativa (Diversidad)
```bash
python scripts/run.py LEI10 --constructive rlf --perturbation partial_destroy
# Tiempo esperado: 0.5-1s
# Calidad: Variable (mejor para exploración)
```

### Configuración 4: Exhaustiva (Mejor resultado)
```bash
python scripts/run.py REG10 \
  --constructive lf \
  --local-search tabu \
  --max-iterations 2000 \
  --perturbation-strength 0.3 \
  --restart-threshold 100 \
  --verbose
# Tiempo esperado: 3-5s
# Calidad: Excelente
```

---

## 🧪 Ejecutar Tests

```bash
cd projects/GCP-ILS

# Ejecutar suite de pruebas
python tests/test_core.py

# Salida esperada:
# ==================================================
# Running Core Module Tests
# ==================================================
# 
# Test: DIMACParser
# ✓ Parser: n=4, m=3, density=0.500
# 
# Test: GraphColoringProblem Construction
# ✓ Problem: n=4, m=4
#   Degrees: max=2, min=2
#   Density: 0.667
#
# ... más tests ...
#
# ==================================================
# ✓ All tests passed!
# ==================================================
```

---

## 📊 Interpretación de Resultados

```
Result: k = 3
├─ k = 3: Número de colores encontrados
├─ Optimal k = 2: Óptimo conocido (si disponible)
└─ Gap = 1 (50%): Diferencia respecto al óptimo

Time: 0.45s
├─ Tiempo total de ejecución

Iterations: 200
├─ Número de iteraciones completadas

Status: ✓ FEASIBLE
├─ Solución sin conflictos (aristas monocromáticas)
```

---

## 🎯 Operadores Disponibles

### Constructivos
| Nombre | Descripción | Calidad | Velocidad |
|--------|-------------|---------|-----------|
| **DSATUR** | Orden por saturation degree | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **LF** | Largest first (por grado) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **SL** | Smallest last | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **RS** | Random sequential | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **RLF** | Recursive large first | ⭐⭐⭐ | ⭐⭐⭐ |

### Local Search
| Nombre | Estrategia | Potencia | Velocidad |
|--------|-----------|---------|-----------|
| **Kempe** | Intercambio de colores | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Tabu** | Búsqueda tabu | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **OVM** | Reasignar vértices | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Swap** | Intercambiar colores | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### Perturbación
| Nombre | Estrategia |
|--------|-----------|
| **RandomRecolor** | Colorear aleatorios |
| **PartialDestroy** | Destruir y reconstruir región |

---

## 🐛 Troubleshooting

### Error: "Instance not found"
```
Solución: Verificar el nombre de la instancia
python scripts/run.py --help
# Ver lista de instancias disponibles
```

### Error: "No module named 'core'"
```
Solución: Ejecutar desde el directorio correcto
cd projects/GCP-ILS
python scripts/run.py CUL10
```

### Error: "Invalid instance file"
```
Solución: Verificar que el archivo .col existe en datasets/
Los archivos deben estar en:
  projects/GCP-ILS/datasets/{family}/{instance}.col
```

### Resultado lento
```
Soluciones:
1. Reducir --max-iterations
2. Usar constructivo rápido: --constructive rs
3. Usar local search rápido: --local-search swap
4. Usar instancia más pequeña
```

---

## 📝 Notas Importantes

1. **Reproducibilidad**: Use `--seed` para obtener resultados reproducibles
2. **Instancias pequeñas**: CUL10, DSJ10 recomendadas para pruebas rápidas
3. **Métrica de éxito**: Solución "✓ FEASIBLE" sin conflictos
4. **Gap**: Mostrado si se conoce el óptimo (en metadatos)
5. **Tiempos**: Varían según máquina y configuración del SO

---

## 🔗 Documentación Relacionada

- **IMPLEMENTATION_COMPLETE.md**: Detalles técnicos completos
- **problema_metaheuristica.md**: Especificaciones del problema
- **README.md**: Descripción general del proyecto

---

**¡Listo para experimentar!** 🎯
