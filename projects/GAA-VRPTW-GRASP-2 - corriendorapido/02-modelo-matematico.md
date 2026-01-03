---
title: "Modelo Matemático Canónico VRPTW"
version: "1.0.0"
created: "2026-01-01"
---

# 2️⃣ MODELO MATEMÁTICO CANÓNICO VRPTW

**Documento**: Modelo Matemático  
**Contenido**: Formulación exacta, variables, restricciones, función objetivo

---

## Grafo del Problema

El VRPTW se define sobre un grafo completo dirigido:

$$G = (V, A)$$

donde:

- $V = \{0, 1, 2, \ldots, n\}$ es el conjunto de nodos
- $A = \{(i, j) : i, j \in V, i \neq j\}$ es el conjunto de arcos

- Nodo 0 = **depósito**
- Nodos 1,...,n = **clientes**

---

## Parámetros Espaciales y Temporales

Para cada nodo $i \in V$:
- Coordenadas $(x_i, y_i)$

Para cada arco $(i, j) \in A$:
- $c_{ij}$ = distancia euclidiana entre $i$ y $j$
- $t_{ij}$ = tiempo de viaje entre $i$ y $j$

**En Solomon VRPTW se cumple**:
$$c_{ij} = t_{ij}$$

(La distancia y el tiempo de viaje son equivalentes)

---

## Parámetros de los Clientes

Para cada cliente $i \in \{1, \ldots, n\}$:

- $q_i$ = demanda del cliente $i$ 
- $[a_i, b_i]$ = ventana de tiempo del cliente $i$
- $s_i$ = tiempo de servicio en el cliente $i$

**Para el depósito** $(i = 0)$:

- $q_0 = 0$
- $s_0 = 0$  
- $[a_0, b_0]$ = ventana operativa del depósito

---

## Parámetros de los Vehículos

- $Q$ = capacidad máxima de cada vehículo
- $K$ = número total de vehículos utilizados

**En Solomon**:
- Los vehículos son **homogéneos** (mismo tipo)
- El número disponible se asume **suficientemente grande**
- **El objetivo es minimizar K** (número real utilizado)

---

## Variables de Decisión

### Variable de Enrutamiento

$$x_{ij} = \begin{cases}
1 & \text{si un vehículo viaja directamente del nodo } i \text{ al nodo } j \\
0 & \text{en caso contrario}
\end{cases}$$

para todo $(i, j) \in A$.

### Variable Temporal

$$t_i = \text{instante de inicio del servicio en el nodo } i$$

para todo $i \in V$.

---

## Función Objetivo (Jerárquica Canónica)

El VRPTW se formula como un problema de optimización **jerárquica estricta**:

### Objetivo Primario

$$\text{Minimizar } K$$

### Objetivo Secundario

$$\text{Minimizar } \sum_{i \in V} \sum_{j \in V} c_{ij} \cdot x_{ij}$$

### Formulación Lexicográfica

$$\text{Minimizar} \quad \left( K, \sum_{i \in V} \sum_{j \in V} c_{ij} \cdot x_{ij} \right)$$

**Significado**: La distancia solo se optimiza entre soluciones que usan el mismo número de vehículos K.

---

## Restricciones del Modelo

### Restricción 1: Visita Única de Clientes

Cada cliente debe ser visitado exactamente una vez:

$$\sum_{i \in V, i \neq j} x_{ij} = 1 \quad \forall j \in \{1, \ldots, n\}$$

### Restricción 2: Salida Única de Clientes

Desde cada cliente se debe partir exactamente una vez:

$$\sum_{j \in V, j \neq i} x_{ij} = 1 \quad \forall i \in \{1, \ldots, n\}$$

### Restricción 3: Depósito y Número de Vehículos

El depósito define el número de rutas activas:

$$\sum_{j \in V, j \neq 0} x_{0j} = K$$

$$\sum_{i \in V, i \neq 0} x_{i0} = K$$

(Cada vehículo parte del depósito y regresa a él)

### Restricción 4: Capacidad del Vehículo

La carga total de cada ruta no puede exceder $Q$.

**Formulación mediante flujo**:

$$\sum_{i=1}^{n} q_i \sum_{j \in V} x_{ij} \leq Q$$

(adaptada según formulación específica)

### Restricción 5: Ventanas de Tiempo

El servicio debe comenzar dentro de la ventana permitida:

$$a_i \leq t_i \leq b_i \quad \forall i \in V$$

### Restricción 6: Precedencia Temporal

Si un vehículo viaja de $i$ a $j$, entonces:

$$t_j \geq t_i + s_i + t_{ij} - M(1 - x_{ij}) \quad \forall (i, j) \in A$$

donde $M$ es una constante suficientemente grande (típicamente $M = b_0 + c_{0j}$ para cualquier j).

### Restricción 7: Eliminación de Subtours

Se evitan ciclos que no incluyan el depósito, mediante:
- Restricciones MTZ (Miller-Tucker-Zemlin)
- Restricciones de flujo
- O formulaciones equivalentes

---

## Dominio de las Variables

$$x_{ij} \in \{0, 1\} \quad \forall (i, j) \in A$$

$$t_i \geq 0 \quad \forall i \in V$$

---

## Equivalencia Canónica

Este modelo matemático es **idéntico para las 6 familias Solomon** (C1, C2, R1, R2, RC1, RC2).

**Las diferencias emergen únicamente de los datos de entrada**, no de la estructura del modelo.

---

## Propiedades del Modelo

| Propiedad | Valor |
|-----------|-------|
| Número de variables x | n(n-1) |
| Número de variables t | n+1 |
| Número de restricciones | O(n²) |
| Complejidad | NP-Hard |
| Tamaño Solomon | 100 clientes, ~10,000 variables |

---

## Forma Equivalente para Implementación

Aunque el objetivo es jerárquico, puede implementarse como:

$$\text{Minimizar} \quad M \cdot K + D$$

donde:

- $M$ = constante suficientemente grande (ej: $M = 10,000$)
- $D = \sum_{i,j} c_{ij} \cdot x_{ij}$

**Nota Crítica**: Esta es una **implementación técnica**. En papel y análisis, el objetivo debe describirse como **jerárquico**, no ponderado.

---

## Resumen: Componentes Canónicas

| Componente | Descripción |
|-----------|-------------|
| **Grafo** | G = (V, A) con n+1 nodos |
| **Parámetros espaciales** | Coordenadas (x_i, y_i), distancias c_ij |
| **Parámetros temporales** | Ventanas [a_i, b_i], servicios s_i |
| **Parámetros capacidad** | Demandas q_i, capacidad Q |
| **Variables enrutamiento** | x_ij ∈ {0,1} |
| **Variables tiempo** | t_i ≥ 0 |
| **Objetivo** | Lexicográfico: (K, D) |
| **Restricciones** | 7 categorías (visita, flujo, capacidad, tiempo, subtours) |

---

## Validación del Modelo

El modelo está validado si:

- ✅ Todas las restricciones se respetan en soluciones factibles
- ✅ Función objetivo es determin
ística
- ✅ Objetivo primario (K) se optimiza antes que secundario (D)
- ✅ Compatible con 100% de instancias Solomon

---

**Siguiente documento**: [03-operadores-dominio.md](03-operadores-dominio.md)  
**Volver a**: [INDEX.md](INDEX.md)
