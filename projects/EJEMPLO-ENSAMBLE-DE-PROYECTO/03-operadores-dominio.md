---
title: "22 Operadores del Dominio VRPTW"
version: "1.0.0"
created: "2026-01-01"
---

# 3️⃣ OPERADORES DEL DOMINIO VRPTW

**Documento**: Operadores Específicos  
**Contenido**: 22 operadores categorizados por tipo

---

## Overview de los 22 Operadores

El proyecto implementa 22 operadores VRPTW distribuidos en 5 categorías:

| Categoría | Count | Ejemplos |
|-----------|-------|----------|
| **Constructivos** | 6 | Savings, NN, Inserción |
| **Mejora Intra-ruta** | 4 | 2-opt, OrOpt, 3-opt, Relocate |
| **Mejora Inter-ruta** | 4 | CrossExchange, 2-opt*, SwapCustomers |
| **Perturbación** | 4 | EjectionChain, RuinRecreate, RandomRemoval |
| **Reparación** | 3 | RepairCapacity, RepairTimeWindows, GreedyRepair |
| **TOTAL** | **22** | - |

---

## 1. OPERADORES CONSTRUCTIVOS (6)

### SavingsHeuristic
- **Referencia**: Clarke & Wright (1964)
- **Descripción**: Heurística de ahorros; fusiona rutas basándose en ahorros
- **Entrada**: Instancia VRPTW
- **Salida**: Solución inicial factible
- **Complejidad**: O(n²)

### NearestNeighbor
- **Referencia**: Solomon (1987)
- **Descripción**: Vecino más cercano básico sin considerar tiempo
- **Entrada**: Instancia, cliente inicial
- **Salida**: Ruta greedy
- **Complejidad**: O(n²)

### TimeOrientedNN
- **Referencia**: Potvin & Bengio (1996)
- **Descripción**: Vecino más cercano priorizando urgencia temporal
- **Entrada**: Instancia, cliente inicial
- **Salida**: Ruta sensible a ventanas
- **Complejidad**: O(n²)

### InsertionI1
- **Referencia**: Solomon (1987)
- **Descripción**: Inserción secuencial minimizando costo adicional
- **Entrada**: Solución parcial, cliente a insertar
- **Salida**: Solución con cliente insertado
- **Complejidad**: O(n)

### RegretInsertion
- **Referencia**: Ropke & Pisinger (2006)
- **Descripción**: Inserción por arrepentimiento (diferencia entre mejor y segunda mejor posición)
- **Entrada**: Instancia, clientes sin asignar
- **Salida**: Cliente insertado donde el "arrepentimiento" es mayor
- **Complejidad**: O(n²)

### RandomizedInsertion
- **Referencia**: Kontoravdis & Bard (1995)
- **Descripción**: Inserción con componente aleatoria (GRASP-style)
- **Entrada**: Instancia, parámetro alpha
- **Salida**: Cliente seleccionado aleatoriamente de opciones buenas
- **Complejidad**: O(n)
- **Nota**: Operador preferido para fase constructiva de GRASP

---

## 2. OPERADORES DE MEJORA LOCAL - INTRA-RUTA (4)

Estos operadores optimizan UNA SOLA RUTA.

### TwoOpt
- **Referencia**: Lin (1965), Solomon (1987)
- **Descripción**: Remueve dos arcos y reconecta invirtiendo subsecuencia
- **Entrada**: Ruta, solución completa
- **Salida**: Ruta mejorada
- **Complejidad**: O(n²) por ruta
- **Efectividad**: Muy alta para VRPTW
- **Nota**: Operador más fundamental

### OrOpt
- **Referencia**: Or (1976)
- **Descripción**: Reubicación de secuencias de 1, 2 o 3 clientes
- **Entrada**: Ruta
- **Salida**: Ruta mejorada
- **Complejidad**: O(n³)
- **Complemento**: Rápido, funciona bien con 2-opt

### ThreeOpt
- **Referencia**: Lin (1965)
- **Descripción**: Remueve tres arcos y reconecta (más intensivo que 2-opt)
- **Entrada**: Ruta
- **Salida**: Ruta mejorada
- **Complejidad**: O(n⁴)
- **Uso**: Cuando 2-opt ya no mejora (refinamiento final)

### Relocate
- **Referencia**: Savelsbergh (1992)
- **Descripción**: Mover un cliente a otra posición en la MISMA ruta
- **Entrada**: Ruta
- **Salida**: Ruta con cliente movido
- **Complejidad**: O(n²)
- **Variante**: Relocate Inter (opera entre rutas)

---

## 3. OPERADORES DE MEJORA LOCAL - INTER-RUTA (4)

Estos operadores mejoran interaccionando DOS O MÁS RUTAS.

### CrossExchange
- **Referencia**: Taillard, Badeau et al. (1997)
- **Descripción**: Intercambio de segmentos entre dos rutas
- **Entrada**: Dos rutas i, j
- **Salida**: Dos rutas con segmentos intercambiados
- **Complejidad**: O(n²) × O(n²) = O(n⁴)
- **Potencial**: Transferencias complejas entre rutas

### TwoOptStar
- **Referencia**: Potvin & Rousseau (1995)
- **Descripción**: 2-opt aplicado entre dos rutas diferentes
- **Entrada**: Dos rutas
- **Salida**: Dos rutas mejoradas
- **Complejidad**: O(n²) × 2
- **Uso**: Balanceo de carga entre vehículos

### SwapCustomers
- **Referencia**: Brøysy & Gendreau (2005)
- **Descripción**: Intercambio de clientes individuales entre rutas
- **Entrada**: Dos rutas
- **Salida**: Dos rutas con clientes intercambiados
- **Complejidad**: O(n²)
- **Frecuencia**: Operador usado a menudo en VND

### RelocateInter
- **Referencia**: Pisinger & Ropke (2007)
- **Descripción**: Mover cliente de una ruta a otra (generalización de Relocate)
- **Entrada**: Dos rutas
- **Salida**: Dos rutas con cliente movido entre ellas
- **Complejidad**: O(n²)

---

## 4. OPERADORES DE PERTURBACIÓN (4)

Estos operadores **destruyen parcialmente** la solución para escapar de óptimos locales.

### EjectionChain
- **Referencia**: Glover (1996)
- **Descripción**: Cadenas de eyección de clientes; remover un cliente causa remociones en cascada
- **Entrada**: Solución
- **Salida**: Solución perturbada
- **Complejidad**: Variable

### RuinRecreate
- **Referencia**: Schrimpf, Schneider et al. (2000)
- **Descripción**: Destruye parcialmente rutas y reconstruye greedy
- **Entrada**: Solución, porcentaje a destruir
- **Salida**: Solución perturbada
- **Complejidad**: O(n²)
- **Uso**: En metaheurísticas como LNS (Large Neighborhood Search)

### RandomRemoval
- **Referencia**: Shaw (1998)
- **Descripción**: Remoción aleatoria de k clientes y reinserción greedy
- **Entrada**: Solución, k
- **Salida**: Solución con k clientes removidos y reinsertados
- **Complejidad**: O(n²)

### RouteElimination
- **Referencia**: Nagata & Kobayashi (2010)
- **Descripción**: Elimina una ruta completa y redistribuye clientes a otras rutas
- **Entrada**: Solución, ruta a eliminar
- **Salida**: Solución con una ruta menos
- **Complejidad**: O(n²)
- **Nota**: Útil para reducir K (objetivo primario)

---

## 5. OPERADORES DE REPARACIÓN (3)

Estos operadores **corrigen violaciones** de restricciones en soluciones infactibles.

### RepairCapacity
- **Referencia**: Brøysy & Gendreau (2005)
- **Descripción**: Repara violaciones de capacidad removiendo clientes y reinserrtando en otras rutas
- **Entrada**: Solución infactible (capacidad violada)
- **Salida**: Solución factible
- **Complejidad**: O(n²)

### RepairTimeWindows
- **Referencia**: Potvin & Gendreau (1996)
- **Descripción**: Ajusta rutas para cumplir ventanas de tiempo; puede esperar en cliente o mover
- **Entrada**: Solución infactible (ventanas violadas)
- **Salida**: Solución factible
- **Complejidad**: O(n²)
- **Crítica**: Operador muy importante en VRPTW

### GreedyRepair
- **Referencia**: Pisinger & Ropke (2007)
- **Descripción**: Reconstrucción voraz de solución tras destrucción parcial
- **Entrada**: Solución parcial/inválida
- **Salida**: Solución completa y factible
- **Complejidad**: O(n²)

---

## Tabla Comparativa de Operadores

| Operador | Tipo | Complejidad | Efectividad | Uso en VND |
|----------|------|-----------|------------|-----------|
| SavingsHeuristic | Constructivo | O(n²) | Media | Inicial |
| NearestNeighbor | Constructivo | O(n²) | Media | Fallback |
| RegretInsertion | Constructivo | O(n²) | Alta | Inicial |
| RandomizedInsertion | Constructivo | O(n) | Alta | Principal GRASP |
| TwoOpt | Intra-ruta | O(n²) | Muy Alta | Siempre |
| OrOpt | Intra-ruta | O(n³) | Alta | Frecuente |
| ThreeOpt | Intra-ruta | O(n⁴) | Muy Alta | Final |
| Relocate | Intra-ruta | O(n²) | Media | Ocasional |
| CrossExchange | Inter-ruta | O(n⁴) | Alta | Ocasional |
| TwoOptStar | Inter-ruta | O(n²) | Media-Alta | Frecuente |
| SwapCustomers | Inter-ruta | O(n²) | Media | Frecuente |
| RelocateInter | Inter-ruta | O(n²) | Media | Ocasional |
| EjectionChain | Perturbación | Variable | Alta | Perturbación |
| RuinRecreate | Perturbación | O(n²) | Alta | Perturbación |
| RandomRemoval | Perturbación | O(n²) | Media-Alta | Perturbación |
| RouteElimination | Perturbación | O(n²) | Media | Para reducir K |
| RepairCapacity | Reparación | O(n²) | Crítica | Necesario |
| RepairTimeWindows | Reparación | O(n²) | Crítica | Necesario |
| GreedyRepair | Reparación | O(n²) | Alta | Reconstrucción |

---

## Restricción Canónica de Uso en GAA

Para que un algoritmo GRASP generado automáticamente sea válido, DEBE cumplir:

1. ✅ **Constructor Randomizado Obligatorio**: 1 de {RandomizedInsertion, TimeOrientedNN, RegretInsertion}
2. ✅ **Operadores Mejora**: Mínimo 2 de {2-opt, OrOpt, TwoOptStar, SwapCustomers, ...}
3. ✅ **Reparación**: Incluir RepairTimeWindows si es necesario
4. ✅ **Iteración**: 1 estrategia de control (ChooseBestOf, ApplyUntilNoImprove, For)

---

## Referencias Bibliográficas

- Clarke, G., & Wright, J. W. (1964). Scheduling of vehicles. OR, 12(4), 568-581.
- Lin, S. (1965). Computer solutions of the traveling salesman problem. Bell System Technical Journal, 44(10).
- Solomon, M. M. (1987). Algorithms for VRPTW. Operations Research, 35(2), 254-265.
- Glover, F. (1996). Ejection chains, reference structures and alternating path methods. JCIT.
- Shaw, P. (1998). Using constraint programming and local search methods to solve vehicle routing problems. CP-98.

---

**Siguiente documento**: [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md)  
**Volver a**: [INDEX.md](INDEX.md)
