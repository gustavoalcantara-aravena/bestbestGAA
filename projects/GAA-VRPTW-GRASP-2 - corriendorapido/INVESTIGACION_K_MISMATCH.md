# INVESTIGACIÓN: Discrepancia K=1 vs K=19 (R101 Solomon)

**Documento:** Análisis del problema de K mismatch  
**Fecha:** 2 de Enero, 2026  
**Status:** ⚠️ INVESTIGACIÓN REQUERIDA

---

## Problema Observado

### Datos
```
Instancia: R101 (Solomon benchmark)
BKS especificado: K=19 vehículos, D=1650.8 km

Nuestros resultados:
  GRASP: K=1, D=54.01 km
  VND:   K=1, D=54.01 km
  ILS:   K=1, D=55.27 km
```

### Análisis
```
Delta_K = 1 - 19 = -18 vehículos

Interpretación:
  ❌ INCORRECTO: "Nuestros algoritmos son 18x mejores"
  ⚠️  PROBLEMA: K=1 es sospechoso (casi siempre insuficiente)
  ⚠️  PROBABLE CAUSA: Los datos no se cargan/interpretan correctamente
```

---

## 🔍 Investigación Sistemática

### Paso 1: Verificar Carga de Datos

**Archivo:** `src/core/loader.py`  
**Pregunta:** ¿Se cargan correctamente los clientes de R101.csv?

```bash
# Script de verificación:
from src.core.loader import SolomonLoader

loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')

print(f"Clientes cargados: {len(instance.customers) - 1}")  # Excluir depósito
print(f"Capacidad: {instance.Q_capacity}")
print(f"BKS esperado: K=19, D=1650.8")

# Mostrar primeros 5 clientes
for c in instance.customers[1:6]:
    print(f"  C{c.id}: demand={c.demand}, window=[{c.ready_time}, {c.due_date}]")
```

**Qué revisar:**
- ¿Se cargan exactamente 100 clientes? (+ 1 depósito = 101 total)
- ¿Demandas están correctas?
- ¿Ventanas de tiempo válidas?

### Paso 2: Validar Soluciones

**Archivo:** `src/core/evaluation.py`  
**Pregunta:** ¿Las soluciones K=1 son realmente factibles?

```bash
# Script de verificación:
from src.metaheuristic.grasp import GRASP
from src.core.loader import SolomonLoader

loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')

grasp = GRASP(instance)
solution, fitness, _ = grasp.solve()

# Verificar factibilidad
is_feasible, details = evaluate_solution(solution)

print(f"¿Factible? {is_feasible}")
print(f"Violaciones: {details['constraint_violations']}")
print(f"Cobertura: {len([c for r in solution.routes for c in r.sequence if c != 0])}")
print(f"Vehículos: {solution.num_vehicles}")
print(f"Distancia: {solution.total_distance}")
```

**Qué revisar:**
- ¿La solución pasa `evaluate_solution()`?
- ¿Todos los 100 clientes están visitados?
- ¿Se respetan capacidades?
- ¿Se respetan ventanas de tiempo?

### Paso 3: Comparar con Baseline

**Pregunta:** ¿Hay una solución manual conocida que podamos verificar?

```bash
# Si K=1 es correcto, la distancia debe ser suma de todas las distancias
# de un recorrido TS de todos los clientes

# Verificar: ¿es D=54 km razonable para 100 clientes?
# Típicamente:
#   - R101 con K=19: D=1650 km → 87 km por ruta
#   - R101 con K=1:  D=54 km → ??? (parece muy bajo)

# Calcular mínima distancia esperada:
# Si todos los clientes están en un círculo de radio r:
# Perímetro ≈ 2πr
# Para 100 clientes: mínimo ≈ 2π × r

from src.core.loader import SolomonLoader
loader = SolomonLoader()
instance = loader.load_instance('datasets/R1/R101.csv')

# Calcular spread
min_x = min(c.x for c in instance.customers)
max_x = max(c.x for c in instance.customers)
min_y = min(c.y for c in instance.customers)
max_y = max(c.y for c in instance.customers)

spread = max(max_x - min_x, max_y - min_y)
print(f"Spread geografico: {spread} unidades")
print(f"Distancia mínima esperada ≈ {spread * 2} (muy aprox)")
```

---

## 📊 Hipótesis

### H1: Datos se cargan incorrectamente
**Síntomas:**
- K=1 viable pero solo si hay 5-10 clientes
- D=54 es consistente con mucho menos que 100 clientes

**Investigación:**
- ¿Cuántos clientes se cargan realmente?
- ¿Se excluye algún cliente por error?

### H2: Soluciones infactibles pasan validación
**Síntomas:**
- K=1 es físicamente imposible con 100 clientes y Q=200
- Pero validación dice "factible"

**Investigación:**
- ¿Evalúa correctamente `evaluate_solution()`?
- ¿Valida todas las restricciones?

### H3: BKS data es incorrecta
**Síntomas:**
- K=19 está mal para R101
- Nuestros datos BKS son incorrectos

**Investigación:**
- Consultar fuente original Solomon benchmark
- Verificar `datasets/bks.json`

### H4: Algoritmos GRASP/VND/ILS no funcionan como esperado
**Síntomas:**
- Todos producen K≈1
- No hay variación

**Investigación:**
- ¿GRASP está construyendo rutas válidas?
- ¿VND/ILS respetan restricciones?

---

## 🛠️ Recomendaciones de Investigación

### Prioridad 1: Verificar Carga de Datos

⚠️ **NOTA IMPORTANTE**: Primero confirmar que los datasets de Solomon existen en la estructura del proyecto.

**Ubicaciones a verificar:**
- `projects/GAA-VRPTW-GRASP-2/data/R1/R101.csv` (o similar)
- `projects/KBP-SA/data/...`
- Los archivos `.csv` deben contener las instancias Solomon completas

```python
# En test_loader.py
def test_r101_loading():
    loader = SolomonLoader()
    inst = loader.load_instance('path/to/R101.csv')  # Ajustar ruta
    
    # MUST be 100 customers + 1 depot
    assert len(inst.customers) == 101
    
    # MUST have customers from index 1-100
    assert all(c.id == i for i, c in enumerate(inst.customers))
    
    # Check demand sum is reasonable
    total_demand = sum(c.demand for c in inst.customers[1:])
    assert total_demand > 0
    print(f"Total demand: {total_demand}")
    print(f"Vehicles needed (approx): {total_demand / inst.Q_capacity}")
```

**⚠️ PREREQUISITO**: Los datasets de Solomon deben estar disponibles. Si no existen:
1. Descargar de https://www.universidade.pt/~rpribeiro/solomon.html
2. Colocar en `projects/GAA-VRPTW-GRASP-2/data/R1/` etc.
3. Verificar que SolomonLoader apunta a esa ubicación

### Prioridad 2: Crear Una Solución Manual
```python
# Generar una solución manual válida y verificar su K y D
# Ejemplo: ruta simple 0→1→2→...→100→0

def create_trivial_solution(instance):
    route = Route(vehicle_id=1)
    for i in range(1, len(instance.customers)):
        route.add_customer(i)
    
    solution = Solution(instance=instance, routes=[route])
    is_feas, details = evaluate_solution(solution)
    
    print(f"Trivial solution: K={solution.num_vehicles}, D={solution.total_distance}")
    print(f"Factible: {is_feas}")
    print(f"Violaciones: {details['constraint_violations']}")
    
    return solution
```

### Prioridad 3: Comparar con Ejemplo Conocido
```python
# Buscar una publicación con solución conocida de R101
# y replicarla exactamente en nuestro código

# Ejemplo: Si literatura dice "R101: K=19, D=1650.8"
# Construir esas 19 rutas exactas y verificar que nuestro código
# calcula K=19, D=1650.8
```

### Prioridad 4: Debug GRASP Paso por Paso
```python
# Agregar logging detallado en GRASP

def debug_grasp_construction(instance):
    grasp = GRASP(instance)
    
    # Detener después de fase constructiva
    sol = grasp._construct_solution()
    
    print(f"Después de construcción:")
    print(f"  Clientes visitados: {sum(len(r.sequence)-2 for r in sol.routes)}")
    print(f"  Vehículos usados: {sol.num_vehicles}")
    print(f"  Distancia: {sol.total_distance}")
    
    # ¿Están faltando clientes?
    visited = set()
    for r in sol.routes:
        for c in r.sequence:
            if c != 0: visited.add(c)
    
    missing = set(range(1, instance.n_customers + 1)) - visited
    if missing:
        print(f"  ⚠️ FALTANDO: {missing}")
```

---

## 📋 Checklist de Investigación

- [ ] Verificar que se cargan 100 clientes
- [ ] Verificar que suma de demandas es > 0
- [ ] Crear solución trivial y validar
- [ ] Verificar que BKS data coincide con Solomon original
- [ ] Agregar logging a GRASP
- [ ] Comparar con ejemplo conocido
- [ ] Verificar factibilidad de K=1 manualmente
- [ ] Revisar si hay clientes duplicados
- [ ] Revisar si hay clientes faltando
- [ ] Revisar ventanas de tiempo

---

## ⚠️ Nota Importante

**LA FUNCIÓN OBJETIVO NO TIENE CULPA.** El problema es anterior: en datos o algoritmos.

Una vez identificada la causa, la solución será simple:
- Si es carga de datos: arreglar loader.py
- Si es factibilidad: revisar evaluate_solution()
- Si es BKS: actualizar datasets/bks.json
- Si es algoritmos: ajustar GRASP/VND/ILS

---

## 📞 Próximos Pasos

1. Ejecutar `test_r101_loading()` para verificar carga
2. Crear solución trivial y validarla
3. Agregar logging a GRASP para trazar construcción
4. Una vez encontrada la causa, generar test de regresión
5. Documentar la solución

---

## ✅ Conclusión

**El problema K≠K_BKS NO es un error de la función objetivo (que es 100% correcta).**

Es un problema de:
- Datos (¿cargados correctamente?)
- Algoritmos (¿producen soluciones factibles?)
- Factibilidad (¿se valida correctamente?)

Requiere investigación sistemática siguiendo este documento.

