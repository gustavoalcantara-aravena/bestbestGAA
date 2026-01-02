---
title: "Metaheurística GRASP"
version: "1.0.0"
created: "2026-01-01"
---

# 4️⃣ METAHEURÍSTICA GRASP

**Documento**: GRASP  
**Contenido**: Descripción, configuración, búsqueda local, VND

---

## Definición General de GRASP

**GRASP** (Greedy Randomized Adaptive Search Procedure) es una metaheurística iterativa de dos fases:

1. **Fase Constructiva**: Construcción voraz aleatoria (greedy randomized)
2. **Fase de Mejora Local**: Búsqueda local hasta óptimo local

**Característica Clave**: Balancea voracidad (determinísmo) y aleatoriedad (exploración)

---

## Fase 1: Construcción Voraz Aleatoria

### Concepto General

En lugar de construir greedy puro (determinístico), GRASP usa un RCL (Restricted Candidate List).

```
En cada paso:
1. Evaluar costos de todos los candidatos
2. Construir RCL = {mejores candidatos dentro de rango}
3. Seleccionar ALEATORIAMENTE uno del RCL
4. Repetir hasta solución completa
```

### RCL (Restricted Candidate List)

**Definición**: Subconjunto de candidatos "suficientemente buenos"

**Opción 1: Alpha-based (Estándar)**

$$\text{threshold} = c_{min} + \alpha \cdot (c_{max} - c_{min})$$

$$\text{RCL} = \{i : c_i \leq \text{threshold}\}$$

**Parámetro α**:
- α = 0: RCL contiene solo mejor candidato (greedy puro)
- α = 1: RCL contiene todos los candidatos (aleatorio puro)
- α = 0.15: Recomendado para VRPTW (balance)

**Opción 2: Size-based**

$$\text{RCL} = \{top-k mejores candidatos\}$$

(Alternativa si tamaño RCL es importante)

### Pseudocódigo: Construcción Greedy Randomizada

```python
def greedy_randomized_construction(instance, alpha):
    solution = initialize_empty_routes()
    unrouted = all_customers.copy()
    
    while unrouted:
        # 1. Evaluar costos de inserción
        costs = {}
        for customer in unrouted:
            costs[customer] = evaluate_insertion_cost(
                customer, solution, instance
            )
        
        c_min = min(costs.values())
        c_max = max(costs.values())
        
        # 2. Construir RCL
        threshold = c_min + alpha * (c_max - c_min)
        RCL = [c for c in unrouted if costs[c] <= threshold]
        
        # 3. Seleccionar aleatoriamente del RCL
        selected = random.choice(RCL)
        
        # 4. Insertar en mejor posición
        insert_customer_best_position(selected, solution, instance)
        unrouted.remove(selected)
    
    return solution
```

---

## Fase 2: Búsqueda Local

### Concepto General

Una vez construida una solución, mejorarla iterativamente aplicando operadores de mejora.

**Criterio de parada**: Cuando no hay mejora posible (óptimo local)

### Variable Neighborhood Descent (VND)

El proyecto usa **VND** como estrategia de búsqueda local.

**Idea**: Cambiar de vecindario cuando se alcanza óptimo local en uno

```python
def variable_neighborhood_descent(solution, instance):
    neighborhoods = [TwoOpt, OrOpt, Relocate, SwapCustomers]
    k = 0
    
    while k < len(neighborhoods):
        # Aplicar vecindario k
        solution_new = neighborhoods[k](solution, instance)
        
        if fitness(solution_new) < fitness(solution):
            # Mejora encontrada: reiniciar desde primer vecindario
            solution = solution_new
            k = 0
        else:
            # No hay mejora: pasar al siguiente vecindario
            k += 1
    
    return solution
```

**Ventaja**: Explora diferentes estructuras de vecindad, más robusto que vecindario único

---

## Configuración GRASP para VRPTW

### Parámetros Principales

```yaml
max_iteraciones: 100
alpha: 0.15                    # Parámetro RCL
tamaño_rcl: null               # Usar alpha-based, no size-based
tipo_mejora: "VND"             # Variable Neighborhood Descent
max_sin_mejora: 20             # Criterio parada alternativo
neighborhoods_order: [TwoOpt, OrOpt, Relocate, SwapCustomers]
```

### Justificación de Parámetros

| Parámetro | Valor | Razón |
|-----------|-------|-------|
| max_iteraciones | 100 | Balance entre diversidad y tiempo |
| alpha | 0.15 | 15% voracidad, 85% aleatoriedad |
| max_sin_mejora | 20 | Parada cuando estancamiento claro |
| tipo_mejora | VND | Más efectivo que vecindario único |

---

## Pseudocódigo GRASP Completo

```python
def GRASP(instance, max_iterations, alpha):
    s_best = None
    f_best = infinity
    
    for iter in range(max_iterations):
        # Fase 1: Construcción Voraz Aleatoria
        s = greedy_randomized_construction(instance, alpha)
        
        # Validar factibilidad
        if not is_feasible(s):
            repair(s, instance)
        
        # Fase 2: Búsqueda Local (VND)
        s = variable_neighborhood_descent(s, instance)
        
        # Actualizar mejor solución encontrada
        if fitness(s) < f_best:
            s_best = s
            f_best = fitness(s)
            iterations_since_improvement = 0
        else:
            iterations_since_improvement += 1
        
        # Criterio de parada
        if iterations_since_improvement >= max_sin_mejora:
            break
    
    return s_best, f_best
```

---

## Integración con Operadores VRPTW

### Constructivos Recomendados
- Preferencia: **RandomizedInsertion** (adaptada a GRASP)
- Alternativa: RegretInsertion, TimeOrientedNN

### Mejora Local Recomendada (VND)
- Orden: TwoOpt → OrOpt → SwapCustomers → Relocate
- Parada: Cuando todos agotan mejoras

### Reparación
- Incluir **RepairTimeWindows** si es necesario
- Preservar factibilidad en cada iteración

---

## Presupuesto Computacional

### Por Iteración GRASP

- **Fase constructiva**: O(n²)
- **Búsqueda local (VND)**: O(n⁴) en peor caso
- **Total por iteración**: ~0.5-1 segundo para 100 clientes

### Presupuesto Total

```
max_iteraciones = 100
tiempo_por_iteracion ≈ 0.5-1 segundo
presupuesto_total ≈ 50-100 segundos por instancia

timeout_recomendado = 60 segundos
→ Alcanza ~60-120 iteraciones
```

### Evaluaciones Totales

- Iteraciones GRASP: 100
- Movimientos búsqueda local: ~100-1000 por iteración
- Total de evaluaciones: 10,000-100,000 por instancia

---

## Ventajas de GRASP para VRPTW

| Ventaja | Razón |
|---------|-------|
| Simple de implementar | Dos fases claras |
| Robusto | Diversidad por aleatoriedad |
| Flexible | Parámetro α ajustable |
| Escalable | Funciona con instancias grandes |
| Bien estudiado | Amplia literatura |

---

## Limitaciones Conocidas

| Limitación | Mitigación |
|-----------|-----------|
| Sin memoria entre iteraciones | Aceptable en GRASP básico |
| No garantiza optimización de K | Usar operadores como RouteElimination |
| Dependencia de parámetro α | Testear α ∈ [0.10, 0.25] |

---

## Referencias

- Feo, T. A., & Resende, M. G. (1995). Greedy randomized adaptive search procedures. Journal of Global Optimization, 6(2), 109-133.
- Resende, M. G., & Ribeiro, C. C. (2009). Greedy randomized adaptive search procedures. Handbook of Metaheuristics, 219-249.

---

**Siguiente documento**: [05-datasets-solomon.md](05-datasets-solomon.md)  
**Volver a**: [INDEX.md](INDEX.md)
