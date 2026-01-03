# Análisis Detallado: Bug en _repair_solution()

**Problema:** Después de construcción, GRASP tiene 100 clientes. Pero después de reparación, tiene solo 7.

---

## 1. Flujo de Reparación en GRASP.solve()

```python
# Línea 120: src/metaheuristic/grasp.py
for iteration in range(self.max_iterations):
    # Phase 1: Construcción ✓ Funciona bien (100 clientes)
    solution = self._construct_solution(instance)  
    
    # Phase 1b: REPARACIÓN ❌ ROMPE TODO
    if not solution.feasible:
        solution = self._repair_solution(solution)  # ← AQUÍ FALLA
    
    # Phase 2: Local Search
    solution = self._local_search(solution)
```

---

## 2. Análisis de _repair_solution()

**Ubicación:** `src/metaheuristic/grasp.py` líneas 205-225

```python
def _repair_solution(self, solution: Solution) -> Solution:
    """Repair infeasible solution."""
    repaired = deepcopy(solution)
    
    # Paso A: Reparar violaciones de ventana de tiempo
    if not all(route.is_feasible for route in repaired.routes):
        repair_tw = RepairTimeWindows()
        repaired = repair_tw.apply(repaired)  # ← SOSPECHOSO #1
    
    # Paso B: Reparar violaciones de capacidad
    if not repaired.feasible:
        repair_cap = RepairCapacity()
        repaired = repair_cap.apply(repaired)  # ← SOSPECHOSO #2
    
    return repaired
```

---

## 3. Análisis de RepairTimeWindows

**Ubicación:** `src/operators/perturbation.py` líneas 414-512

### ¿Qué hace?

```python
def apply(self, solution: Solution) -> Solution:
    repaired = deepcopy(solution)
    to_reinsert = []
    
    # Para cada ruta:
    for route in repaired.routes:
        current_time = 0
        violated = []
        
        # Forward pass: calcula tiempo en cada cliente
        for i, cust_id in enumerate(route.sequence):
            cust = repaired.instance.get_customer(cust_id)
            
            if cust_id != 0:  # No es depot
                arrival = current_time
                
                # ⚠️ AQUÍ: Si arrival > due_date, marcar como violado
                if arrival > cust.due_date:
                    violated.append((i, cust_id))
                else:
                    # Actualizar current_time
                    if arrival < cust.ready_time:
                        current_time = cust.ready_time
                    else:
                        current_time = arrival
                    current_time += cust.service_time
                
                # Viaje al siguiente
                if i < len(route.sequence) - 1:
                    next_id = route.sequence[i + 1]
                    current_time += route._distance(cust_id, next_id)
        
        # ⚠️ CRÍTICO: ELIMINAR clientes con violaciones
        for _, cust_id in violated:
            route.remove_customer(cust_id)  # ← ELIMINA CLIENTES
            to_reinsert.append(cust_id)
    
    # Intentar reinsertar
    for cust in to_reinsert:
        self._reinsert_customer(repaired, cust)
```

### 🔴 Problema #1: Bug en la Lógica de Tiempo

**El algoritmo no actualiza `current_time` cuando arrival > due_date:**

```python
if arrival > cust.due_date:
    violated.append((i, cust_id))  # ← Marca como violado
    # ⚠️ PERO NO ACTUALIZA current_time
    # Entonces el siguiente cliente calcula tiempo de llegada INCORRECTO
else:
    current_time = ...  # Solo entra aquí si NO hay violación
```

**Consecuencia:** Después de marcar un cliente como violado, el tiempo no se actualiza para los siguientes clientes. Esto causa que **TODOS LOS CLIENTES POSTERIORES** se marquen como violados (porque el tiempo acumulado es incorrecto).

**Resultado:** Se eliminan 93 de 100 clientes en cascada.

---

## 4. Análisis de _reinsert_customer()

**Ubicación:** `src/operators/perturbation.py` líneas 483-512

```python
def _reinsert_customer(self, solution: Solution, customer_id: int):
    """Reinsert customer respecting time windows."""
    best_route = None
    best_pos = None
    best_cost = float('inf')
    
    for route in solution.routes:
        for pos in range(1, len(route.sequence)):
            # Simular inserción en posición pos
            test_seq = route.sequence[:pos] + [customer_id] + route.sequence[pos:]
            
            # Verificar factibilidad de tiempo
            time = 0
            feasible = True
            
            for i, cid in enumerate(test_seq):
                c = solution.instance.get_customer(cid)
                
                if cid != 0:
                    arrival = time
                    # ⚠️ Si NO es factible, marcar como no factible
                    if arrival > c.due_date:
                        feasible = False
                        break  # ← SALE DEL LOOP
                    
                    time = max(arrival, c.ready_time) + c.service_time
                
                if i < len(test_seq) - 1:
                    next_id = test_seq[i + 1]
                    time += route._distance(cid, next_id)
            
            if feasible:
                # Calcular costo de inserción
                old_dist = route._distance(route.sequence[pos-1], route.sequence[pos])
                new_dist = ...
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
    
    # ⚠️ Si best_route es None, el cliente NO se reinserta (SE PIERDE)
    if best_route is not None:
        best_route.add_customer(customer_id, best_pos)
```

### 🔴 Problema #2: Clientes Perdidos

Si un cliente eliminado **no se puede reinsertar** en ninguna posición (porque violaría ventanas de tiempo), simplemente **se pierde**. No hay mecanismo para garantizar que se reinserte en una ruta nueva.

---

## 5. Resumen de Problemas

| # | Ubicación | Problema | Consecuencia |
|---|-----------|----------|--------------|
| 1 | RepairTimeWindows.apply() L447-462 | `current_time` no se actualiza cuando hay violación | Clientes posteriores se marcan como violados en cascada |
| 2 | RepairTimeWindows._reinsert_customer() | Clientes eliminados no se pueden reinsertar | Se pierden clientes (NO se ponen en ruta nueva) |
| 3 | _repair_solution() | Usa reparadores demasiado agresivos | Elimina más clientes de los necesarios |

---

## 6. Solución Recomendada

### Opción A: Corregir RepairTimeWindows ⭐ RECOMENDADO
1. Actualizar `current_time` incluso cuando hay violación
2. Solo eliminar clientes si tiempo actualizado sigue siendo inviable
3. Garantizar reinserción en ruta nueva si no cabe en existentes

### Opción B: Deshabilitar Reparación
- Comentar `_repair_solution()` en GRASP.solve()
- RandomizedInsertion ya produce soluciones factibles
- VND las mejora sin necesidad de reparación

### Opción C: Usar GreedyRepair en lugar de reparadores específicos
- GreedyRepair reconstruye desde cero si hay demasiadas violaciones
- Más robusto que intentar reparar cliente por cliente

---

## 7. Debug Output Esperado Después de Correción

```
[CONSTRUCCIÓN]  K=1, clientes=100  ✓
[AFTER REPAIR]  K=?, clientes=100  ✓  (puede aumentar K pero mantiene clientes)
[AFTER VND]     K=?, clientes=100  ✓
[FINAL]         K=?, clientes=100  ✓
```

**NO debería haber:**
```
❌ clientes=7 después de reparación
```

