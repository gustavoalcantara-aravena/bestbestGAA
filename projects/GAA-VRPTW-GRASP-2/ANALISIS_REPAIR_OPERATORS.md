# ANÁLISIS Y CORRECCIÓN: Repair Operators - VRPTW

**Fecha**: 2 Enero 2026  
**Problema**: RandomizedInsertion construye 100 clientes, pero después de Repair solo quedan 6-8  
**Causa**: `RepairTimeWindows._reinsert_customer()` PIERDE clientes cuando no puede insertarlos

---

## 📋 Análisis del Problema

### Flujo Observado

```
[CONSTRUCCIÓN]
  RandomizedInsertion → 100 clientes en 1 ruta
  K=1, D=732.81
  ✓ CORRECTO

        ↓ REPAIR

[REPARACIÓN DAÑADA]
  RepairTimeWindows.apply()
    - Detecta violaciones de TW
    - Remueve clientes violados
    - Llama _reinsert_customer() para cada cliente
    - SI NO ENCUENTRA POSICIÓN → CLIENTE SE PIERDE (!)
  
  K=1, clientes=6-8
  ❌ 94 CLIENTES DESAPARECIDOS

        ↓ LOCAL SEARCH

[FINAL]
  K=1, D=54-75 (solo 6-8 clientes)
  ❌ SOLUCIÓN INFACTIBLE
```

### Código Problemático

**Ubicación**: `src/operators/perturbation.py` líneas 511-526

```python
def _reinsert_customer(self, solution: Solution, customer_id: int):
    """Reinsert customer respecting time windows."""
    cust = solution.instance.get_customer(customer_id)
    best_route = None
    best_pos = None
    best_cost = float('inf')
    
    for route in solution.routes:
        for pos in range(1, len(route.sequence)):
            # ... intenta encontrar mejor posición ...
            if feasible:
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
    
    if best_route is not None:
        best_route.add_customer(customer_id, best_pos)
    # ⚠️ AQUÍ: Si best_route is None, NO HACER NADA
    # ⚠️ Cliente customer_id DESAPARECE SILENCIOSAMENTE
```

### Por qué pasa

1. Se construye solución de 100 clientes en 1 ruta
2. La ruta SÍ tiene violaciones de TW (100 clientes en 1 ruta es ineficiente)
3. RepairTimeWindows identifica clientes problemáticos
4. Intenta reinsertar cada cliente removido:
   - Itera sobre rutas existentes (solo 1)
   - Busca posiciones factibles para cada cliente
   - Si NO encuentra, retorna sin hacer nada
5. Resultado: Muchos clientes se pierden

---

## ✅ SOLUCIÓN: 3 Opciones

### OPCIÓN A: Permitir crear nuevas rutas (RECOMENDADO)

Si no cabe en ruta existente → crear nueva ruta con ese cliente

```python
def _reinsert_customer(self, solution: Solution, customer_id: int):
    """Reinsert customer respecting time windows."""
    cust = solution.instance.get_customer(customer_id)
    best_route = None
    best_pos = None
    best_cost = float('inf')
    
    # Buscar mejor posición en rutas existentes
    for route in solution.routes:
        for pos in range(1, len(route.sequence)):
            test_seq = route.sequence[:pos] + [customer_id] + route.sequence[pos:]
            
            # Verificar factibilidad de TW
            time = 0
            feasible = True
            
            for i, cid in enumerate(test_seq):
                c = solution.instance.get_customer(cid)
                
                if cid != 0:
                    arrival = time
                    if arrival > c.due_date:
                        feasible = False
                        break
                    
                    time = max(arrival, c.ready_time) + c.service_time
                
                if i < len(test_seq) - 1:
                    next_id = test_seq[i + 1]
                    time += route._distance(cid, next_id)
            
            if feasible:
                old_dist = route._distance(route.sequence[pos-1], route.sequence[pos])
                new_dist = route._distance(route.sequence[pos-1], customer_id) + route._distance(customer_id, route.sequence[pos])
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
    
    # NUEVA LÓGICA: Si no cabe en ruta existente, crear nueva ruta
    if best_route is not None:
        best_route.add_customer(customer_id, best_pos)
    else:
        # Crear nueva ruta con este cliente
        new_route = Route(
            vehicle_id=len(solution.routes),
            sequence=[0, customer_id, 0],
            instance=solution.instance
        )
        solution.routes.append(new_route)
```

**Ventaja**: Los clientes siempre se reinsertan  
**Desventaja**: Puede crear muchas rutas (K aumenta)

### OPCIÓN B: Reparación más permisiva

Aceptar inserciones que "casi" cumplen TW (con esperas razonables)

```python
def _reinsert_customer(self, solution: Solution, customer_id: int):
    """Reinsert customer respecting time windows (with wait)."""
    cust = solution.instance.get_customer(customer_id)
    best_route = None
    best_pos = None
    best_cost = float('inf')
    best_feasible = False
    
    for route in solution.routes:
        for pos in range(1, len(route.sequence)):
            test_seq = route.sequence[:pos] + [customer_id] + route.sequence[pos:]
            
            # Simular con esperas
            time = 0
            feasible = True
            
            for i, cid in enumerate(test_seq):
                c = solution.instance.get_customer(cid)
                
                if cid != 0:
                    arrival = time
                    
                    # PERMITIR espera si ready_time < due_date
                    if c.ready_time <= c.due_date:
                        time = max(arrival, c.ready_time) + c.service_time
                    else:
                        feasible = False
                        break
                
                if i < len(test_seq) - 1:
                    next_id = test_seq[i + 1]
                    time += route._distance(cid, next_id)
            
            if feasible:
                old_dist = route._distance(route.sequence[pos-1], route.sequence[pos])
                new_dist = route._distance(route.sequence[pos-1], customer_id) + route._distance(customer_id, route.sequence[pos])
                cost = new_dist - old_dist
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_pos = pos
                    best_feasible = True
    
    if best_route is not None:
        best_route.add_customer(customer_id, best_pos)
    elif not best_feasible:
        # Si no encontramos posición factible, crear nueva ruta
        new_route = Route(
            vehicle_id=len(solution.routes),
            sequence=[0, customer_id, 0],
            instance=solution.instance
        )
        solution.routes.append(new_route)
```

**Ventaja**: Equilibrio entre K y factibilidad  
**Desventaja**: Requiere ajustes cuidadosos

### OPCIÓN C: Detectar y loguear clientes perdidos

Mantener fallback pero registrar problema

```python
def _reinsert_customer(self, solution: Solution, customer_id: int):
    """Reinsert customer respecting time windows."""
    # ... código igual hasta el final ...
    
    if best_route is not None:
        best_route.add_customer(customer_id, best_pos)
    else:
        # FALLBACK: crear nueva ruta
        new_route = Route(
            vehicle_id=len(solution.routes),
            sequence=[0, customer_id, 0],
            instance=solution.instance
        )
        solution.routes.append(new_route)
        if self.verbose:
            print(f"[REPAIR] Customer {customer_id} moved to new route")
```

---

## 🔧 IMPLEMENTACIÓN RECOMENDADA

**Usar OPCIÓN A** porque:

1. ✅ Garantiza que todos los clientes se reinsertan
2. ✅ Resultado SIEMPRE es factible (todos los clientes visitados)
3. ✅ K puede aumentar pero es mejor que K=1 con 6 clientes
4. ✅ Es conceptualmente correcta: "mejor K=19 y factible que K=1 e infactible"

---

## 📝 Pseudocódigo de Reparación Correcta

```
PROCEDURE RepairTimeWindows(solution):
  to_reinsert = []
  
  FOR EACH route IN solution.routes:
    current_time = 0
    violated = []
    
    FOR EACH (i, customer) IN route.sequence:
      IF customer != DEPOT:
        arrival = current_time
        
        IF arrival > customer.due_date:
          violated.append(customer)
        ELSE:
          current_time = max(arrival, customer.ready_time)
          current_time += customer.service_time
        
        IF i < route.length - 1:
          next = route.sequence[i+1]
          current_time += distance(customer, next)
    
    FOR EACH customer IN violated:
      remove(route, customer)
      to_reinsert.append(customer)
  
  FOR EACH customer IN to_reinsert:
    inserted = FALSE
    
    FOR EACH route IN solution.routes:
      FOR pos IN 1 to route.length:
        IF can_insert_at(route, customer, pos):
          insert(route, customer, pos)
          inserted = TRUE
          BREAK
    
    IF NOT inserted:
      # IMPORTANTE: Crear nueva ruta si no se puede insertar
      new_route = Route([DEPOT, customer, DEPOT])
      solution.routes.append(new_route)
  
  RETURN solution
```

---

## ✅ Próximos Pasos

1. Implementar OPCIÓN A en `RepairTimeWindows._reinsert_customer()`
2. Implementar fallback similar en `RepairCapacity._reinsert_customer()`
3. Test: Verificar que construcción (100 clientes) se preserve
4. Test: Verificar K final es razonable
5. Ejecutar experiments.py nuevamente

