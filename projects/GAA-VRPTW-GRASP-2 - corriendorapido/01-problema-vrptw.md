---
title: "Problema VRPTW - Definición e Introducción"
version: "1.0.0"
created: "2026-01-01"
---

# 1️⃣ DEFINICIÓN DEL PROBLEMA VRPTW

**Documento**: Problema y Definición  
**Contenido**: Descripción informal del VRPTW, aplicaciones, características por familia

---

## Problema Seleccionado

**Nombre**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Tipo**: Minimización  
**Categoría**: Combinatorial Optimization - NP-Hard

---

## Descripción Informal

El problema de ruteo de vehículos con ventanas de tiempo (VRPTW) consiste en diseñar rutas óptimas para una flota de vehículos que deben atender un conjunto de clientes desde un depósito central. 

Cada cliente tiene:
- Una demanda de producto
- Una ventana de tiempo [a_i, b_i] durante la cual debe ser visitado
- Un tiempo de servicio s_i

Los vehículos tienen capacidad limitada y deben respetar las ventanas de tiempo de los clientes.

---

## Aplicaciones Prácticas

El VRPTW aparece en numerosos contextos del mundo real:

- **Logística de distribución urbana**: Entregas de paquetes en ciudades
- **Ruteo de vehículos de transporte escolar**: Recogida y entrega de estudiantes en horarios específicos
- **Servicios de mensajería y paquetería**: Entregas con ventanas horarias
- **Distribución de alimentos y bebidas**: Entregas a restaurantes y tiendas
- **Servicios de mantenimiento programado**: Visitas técnicas en horarios acordados

---

## Complejidad Computacional

El VRPTW es **NP-Hard**, lo que implica:

- No existe algoritmo polinomial conocido (salvo P=NP)
- Soluciones exactas solo viable para instancias pequeñas (< 50 clientes)
- Para instancias medianas/grandes (> 100 clientes), se requieren metaheurísticas
- El benchmark Solomon (100 clientes) está diseñado para evaluar heurísticas

---

## Solución Representación

Una solución del VRPTW es un conjunto de rutas, cada ruta es una secuencia de clientes:

```
routes = [
    [0, c1, c3, c5, 0],    # Ruta 1: depósito → c1 → c3 → c5 → depósito
    [0, c2, c4, 0],         # Ruta 2: depósito → c2 → c4 → depósito
    [0, c6, c7, c8, 0]      # Ruta 3: depósito → c6 → c7 → c8 → depósito
]
```

**Ejemplo concreto**:
```
Instancia: 8 clientes, 3 vehículos, Q=100

Solución:
Route 1: 0 → 1(q=30) → 3(q=25) → 5(q=20) → 0  [Carga: 75]
Route 2: 0 → 2(q=40) → 4(q=35) → 0             [Carga: 75]
Route 3: 0 → 6(q=15) → 7(q=20) → 8(q=10) → 0  [Carga: 45]

Costo total: 245.6 unidades
Violaciones: 0 (factible)
```

---

## Restricciones del Problema

### Restricciones Duras (No pueden violarse)

1. **Capacidad**: La demanda acumulada en cada ruta no debe exceder Q
2. **Ventanas de tiempo**: Cada cliente debe ser visitado dentro de su ventana [a_i, b_i]
3. **Cobertura**: Todos los clientes deben ser visitados exactamente una vez
4. **Depósito**: Todas las rutas inician y terminan en el depósito (nodo 0)

### Restricciones Blandas (Pueden penalizarse)

- Minimizar número de vehículos utilizados
- Balancear carga entre vehículos

---

## Parámetros del Problema

| Parámetro | Símbolo | Descripción |
|-----------|---------|-------------|
| Clientes | n | Número de clientes (excluye depósito) |
| Vehículos | K | Número de vehículos utilizados |
| Capacidad | Q | Capacidad máxima de cada vehículo |
| Demanda cliente i | q_i | Cantidad a entregar en cliente i |
| Ventana cliente i | [a_i, b_i] | Intervalo horario permitido |
| Servicio cliente i | s_i | Tiempo de descarga en cliente i |
| Distancia i-j | c_ij | Distancia/tiempo entre nodos i y j |
| Coordenada cliente i | (x_i, y_i) | Ubicación geográfica |

---

## Metricas de Evaluación

**Métrica principal**: Distancia total recorrida (o costo total)  

**Métricas secundarias**:
- Número de vehículos utilizados
- Violaciones de ventanas de tiempo
- Violaciones de capacidad

**Criterio de comparación**: Menor es mejor

---

## Manejo de Infactibilidad

Una solución se considera **infactible** si:
- Excede capacidad en alguna ruta
- Viaja a algún cliente fuera de su ventana de tiempo
- No cubre todos los clientes
- Vehículos no regresan al depósito

**En Solomon VRPTW**, el criterio jerárquico es:
1. Primero: Minimizar número de vehículos (K)
2. Segundo: Minimizar distancia (D), solo cuando K es igual

---

## Familias de Instancias Solomon

Solomon (1987) definió 6 familias de instancias estándar para benchmark:

### Familia C (Clustered)

**Características**:
- Clientes geográficamente agrupados en clusters
- Ventanas de tiempo amplias (tipo 2) o estrictas (tipo 1)

**Subfamilias**:
- **C1**: Clusters + ventanas estrictas (9 instancias: C101-C109)
- **C2**: Clusters + ventanas amplias (8 instancias: C201-C208)

**Dificultad**: Baja-Media  
**K esperado**: 9-11 vehículos

### Familia R (Random)

**Características**:
- Clientes distribuidos aleatoriamente (sin clustering)
- Ventanas de tiempo amplias (tipo 2) o estrictas (tipo 1)

**Subfamilias**:
- **R1**: Aleatorio + ventanas estrictas (12 instancias: R101-R112)
- **R2**: Aleatorio + ventanas amplias (11 instancias: R201-R211)

**Dificultad**: Alta  
**K esperado**: 12-15 vehículos

### Familia RC (Mixed)

**Características**:
- Mezcla de clustering y distribución aleatoria
- Ventanas de tiempo amplias (tipo 2) o estrictas (tipo 1)

**Subfamilias**:
- **RC1**: Mixto + ventanas estrictas (8 instancias: RC101-RC108)
- **RC2**: Mixto + ventanas amplias (8 instancias: RC201-RC208)

**Dificultad**: Media-Alta  
**K esperado**: 13-16 vehículos

---

## Características por Tipo de Ventana de Tiempo

| Tipo | Amplitud | Característica | Ejemplo |
|------|----------|---|---------|
| **Tipo 1** (Tight) | Restrictiva | Más difícil, menos flexibilidad | [9:00, 10:00] |
| **Tipo 2** (Wide) | Amplia | Más fácil, más flexibilidad | [0:00, 24:00] |

**Impacto**: Instancias Tipo 1 requieren rutas más planificadas, Tipo 2 permiten optimización más libre.

---

## Comparativa Cualitativa de Familias

| Familia | Estructura | Dificultad | Tamaño K | Aplicación Típica |
|---------|-----------|-----------|----------|------------------|
| **C** | Clustering claro | Baja | ~10 | Distribución urbana (barrios) |
| **R** | Aleatoria | Alta | ~13 | Área metropolitana dispersa |
| **RC** | Mixta | Media-Alta | ~14 | Región urbano-rural |

---

## Por qué VRPTW para GRASP

VRPTW es ideal para evaluar GRASP porque:

1. **Combinatorial**: Variedad de estructuras de solución
2. **Restricciones diversas**: Capacidad, tiempo, cobertura
3. **Benchmarks estándar**: 56 instancias Solomon con BKS conocidas
4. **Relevancia práctica**: Aplicaciones reales del mundo
5. **Desafío algorítmico**: NP-Hard, requiere metaheurísticas

---

## Referencias

- Solomon, M. M. (1987). *Algorithms for the vehicle routing and scheduling problems with time window constraints*. Operations Research, 35(2), 254-265.
- Brøysy, O., & Gendreau, M. (2005). *Vehicle routing problem with time windows*. Transportation Science, 39(1-2).

---

**Siguiente documento**: [02-modelo-matematico.md](02-modelo-matematico.md)  
**Volver a**: [INDEX.md](INDEX.md)
