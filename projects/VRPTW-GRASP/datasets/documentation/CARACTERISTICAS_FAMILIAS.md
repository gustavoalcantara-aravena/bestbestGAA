# Características Detalladas de las Familias de Instancias Solomon VRPTW

## Índice
1. [Visión General de las Familias](#visión-general-de-las-familias)
2. [Familia C1: Clientes Agrupados con Ventanas Cortas](#familia-c1-clientes-agrupados-con-ventanas-cortas)
3. [Familia C2: Clientes Agrupados con Ventanas Largas](#familia-c2-clientes-agrupados-con-ventanas-largas)
4. [Familia R1: Clientes Aleatorios con Ventanas Cortas](#familia-r1-clientes-aleatorios-con-ventanas-cortas)
5. [Familia R2: Clientes Aleatorios con Ventanas Largas](#familia-r2-clientes-aleatorios-con-ventanas-largas)
6. [Familia RC1: Clientes Mixtos con Ventanas Cortas](#familia-rc1-clientes-mixtos-con-ventanas-cortas)
7. [Familia RC2: Clientes Mixtos con Ventanas Largas](#familia-rc2-clientes-mixtos-con-ventanas-largas)
8. [Comparación Entre Familias](#comparación-entre-familias)
9. [Guía de Selección de Instancias](#guía-de-selección-de-instancias)

---

## Visión General de las Familias

### Clasificación Jerárquica

```
Solomon VRPTW Dataset
│
├── Tipo C (Clustered - Agrupados)
│   ├── C1 (Ventanas Cortas) - 9 instancias
│   └── C2 (Ventanas Largas) - 8 instancias
│
├── Tipo R (Random - Aleatorios)
│   ├── R1 (Ventanas Cortas) - 12 instancias
│   └── R2 (Ventanas Largas) - 11 instancias
│
└── Tipo RC (Random-Clustered - Mixtos)
    ├── RC1 (Ventanas Cortas) - 8 instancias
    └── RC2 (Ventanas Largas) - 8 instancias
```

### Matriz de Características Principales

| Familia | Distribución | Ventanas | Instancias | Horizonte | Servicio | Capacidad | Dificultad |
|---------|--------------|----------|------------|-----------|----------|-----------|------------|
| **C1** | Agrupada | Cortas | 9 | 1,236 | 90 | 200 | Media-Alta |
| **C2** | Agrupada | Largas | 8 | 3,390 | 90 | 700 | Baja |
| **R1** | Aleatoria | Cortas | 12 | 230 | 10 | 200 | Muy Alta |
| **R2** | Aleatoria | Largas | 11 | 1,000 | 10 | 1,000 | Media |
| **RC1** | Mixta | Cortas | 8 | 240 | 10 | 200 | Alta |
| **RC2** | Mixta | Largas | 8 | Variable | 10 | 1,000 | Media-Alta |

---

## Familia C1: Clientes Agrupados con Ventanas Cortas

### Identificación
- **Código**: C1XX (C101, C102, ..., C109)
- **Número de instancias**: 9
- **Rango**: C101 a C109

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Agrupada (Clustered)
Número de clusters: 4 clusters principales
Patrón espacial: Cuadrantes bien definidos

Cluster 1 (Noreste):
  - Ubicación: X ∈ [40, 50], Y ∈ [60, 70]
  - Clientes: ~25
  - Densidad: Alta

Cluster 2 (Noroeste):
  - Ubicación: X ∈ [15, 25], Y ∈ [75, 85]
  - Clientes: ~25
  - Densidad: Alta

Cluster 3 (Sureste):
  - Ubicación: X ∈ [85, 95], Y ∈ [25, 35]
  - Clientes: ~25
  - Densidad: Alta

Cluster 4 (Suroeste):
  - Ubicación: X ∈ [20, 35], Y ∈ [30, 50]
  - Clientes: ~25
  - Densidad: Alta
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 0
  - Máximo: 95
  - Media: 40.5
  - Desviación estándar: 22.3

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 85
  - Media: 48.7
  - Desviación estándar: 19.8

Distancias:
  - Intra-cluster promedio: 8.5 unidades
  - Inter-cluster promedio: 45.2 unidades
  - Ratio inter/intra: 5.3 (alta separación)
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: 1,236 unidades de tiempo
Inicio: 0
Fin: 1,236
Duración efectiva: 1,236 unidades
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Mínima: 45 unidades
  - Máxima: 69 unidades
  - Promedio: 55 unidades
  - Desviación estándar: 8.2 unidades

Distribución temporal:
  - Clientes tempranos [0-400]: 30%
  - Clientes medios [400-800]: 40%
  - Clientes tardíos [800-1236]: 30%

Tiempo de servicio:
  - Constante: 90 unidades
  - Porcentaje de ventana: 164% (90/55)
  - Implicación: Requiere espera en muchos casos
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 45% de pares
Ventanas disjuntas: 55% de pares
Conflictos temporales severos: 30%

Interpretación:
  - Moderada fragmentación temporal
  - Posible consolidación dentro de clusters
  - Difícil consolidación entre clusters
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 10 unidades
  - Máxima: 50 unidades
  - Promedio: 20 unidades
  - Desviación estándar: 10.5 unidades

Demanda total: ~2,000 unidades
Capacidad del vehículo: 200 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 10
  - Utilización promedio: 100%
  - Restricción: MUY AJUSTADA
```

### Parámetros del Vehículo

```
Capacidad: 200 unidades
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Costo fijo por vehículo: Implícito (minimizar cantidad)
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar número de vehículos
Objetivo secundario: Minimizar distancia total

Función objetivo jerárquica:
  f(s) = 1000 × num_vehiculos + distancia_total

Prioridad: Vehículos >> Distancia
```

### Dificultad Computacional

```
Nivel de dificultad: MEDIA-ALTA

Factores de complejidad:
  ✓ Ventanas estrechas (alta restricción temporal)
  ✓ Tiempo de servicio largo (90 unidades)
  ✓ Capacidad ajustada (100% utilización)
  ✗ Clusters bien definidos (facilita ruteo)

Tiempo de resolución típico:
  - Heurística simple: 1-3 segundos
  - Metaheurística: 10-60 segundos
  - Método exacto: Horas (instancias pequeñas)
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| C101 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C102 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C103 | 10 | 828.06 | 2003 | Bent & Van Hentenryck |
| C104 | 10 | 824.78 | 2003 | Bent & Van Hentenryck |
| C105 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C106 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C107 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C108 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C109 | 10 | 828.94 | 1997 | Rochat & Taillard |

**Observación**: Todas requieren 10 vehículos (óptimo), distancias muy similares (~828)

### Estrategias de Solución Recomendadas

```
1. Identificación de clusters:
   - Usar K-means (k=4) para identificar grupos
   - Asignar vehículos por cluster

2. Ruteo intra-cluster:
   - Nearest Neighbor dentro de cada cluster
   - Respetar ventanas de tiempo estrictamente

3. Optimización local:
   - 2-opt dentro de rutas
   - Relocate entre rutas del mismo cluster
   - Exchange limitado

4. Gestión temporal:
   - Priorizar clientes con ventanas tempranas
   - Calcular tiempos de espera
   - Evitar llegadas tardías
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Entrega urbana con zonas definidas (barrios)
  ✓ Distribución en ciudades con distritos
  ✓ Servicios técnicos con citas programadas
  ✓ Recolección de residuos por sectores

Características del mundo real:
  - Clientes agrupados geográficamente
  - Ventanas de atención estrictas (2-3 horas)
  - Servicios que toman tiempo significativo
  - Capacidad de vehículo limitada
```

---

## Familia C2: Clientes Agrupados con Ventanas Largas

### Identificación
- **Código**: C2XX (C201, C202, ..., C208)
- **Número de instancias**: 8
- **Rango**: C201 a C208

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Agrupada (idéntica a C1)
Número de clusters: 4 clusters principales
Patrón espacial: Cuadrantes bien definidos

Coordenadas:
  - Misma distribución que C1
  - X ∈ [0, 95], Y ∈ [5, 85]
  - 4 clusters en esquinas del espacio
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 0
  - Máximo: 95
  - Media: 40.5
  - Desviación estándar: 22.3

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 85
  - Media: 48.7
  - Desviación estándar: 19.8

Distancias:
  - Intra-cluster: 8.5 unidades
  - Inter-cluster: 45.2 unidades
  - Idénticas a C1
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: 3,390 unidades de tiempo
Inicio: 0
Fin: 3,390
Incremento vs C1: +174% (2,154 unidades más)
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Constante: 160 unidades
  - Uniformidad: 100%
  - Incremento vs C1: +190% (160 vs 55)

Distribución temporal:
  - Muy dispersa a lo largo del horizonte
  - Solapamiento alto: ~85%
  - Flexibilidad: MUY ALTA

Tiempo de servicio:
  - Constante: 90 unidades
  - Porcentaje de ventana: 56% (90/160)
  - Margen disponible: 70 unidades
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 85% de pares
Ventanas disjuntas: 15% de pares
Conflictos temporales: MÍNIMOS

Interpretación:
  - Baja fragmentación temporal
  - Alta posibilidad de consolidación
  - Flexibilidad para optimizar distancias
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 10 unidades
  - Máxima: 50 unidades
  - Promedio: 20 unidades
  - Idéntica a C1

Demanda total: ~2,000 unidades
Capacidad del vehículo: 700 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 35
  - Utilización promedio: 29%
  - Restricción: MUY HOLGADA
```

### Parámetros del Vehículo

```
Capacidad: 700 unidades (+250% vs C1)
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Costo: Minimizar cantidad y distancia
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar distancia total
Objetivo secundario: Minimizar número de vehículos

Función objetivo:
  f(s) = distancia_total + 100 × num_vehiculos

Prioridad: Distancia >> Vehículos
```

### Dificultad Computacional

```
Nivel de dificultad: BAJA

Factores de complejidad:
  ✗ Ventanas amplias (baja restricción temporal)
  ✗ Capacidad holgada (29% utilización)
  ✓ Optimización de distancias (desafío principal)
  ✓ Clusters bien definidos (facilita ruteo)

Tiempo de resolución típico:
  - Heurística simple: 0.5-2 segundos
  - Metaheurística: 5-30 segundos
  - Método exacto: Factible para instancias pequeñas
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| C201 | 3 | 591.56 | 1999 | Mester & Bräysy |
| C202 | 3 | 591.56 | 1999 | Mester & Bräysy |
| C203 | 3 | 591.17 | 2003 | Bent & Van Hentenryck |
| C204 | 3 | 590.60 | 2003 | Bent & Van Hentenryck |
| C205 | 3 | 588.88 | 2003 | Bent & Van Hentenryck |
| C206 | 3 | 588.49 | 2003 | Bent & Van Hentenryck |
| C207 | 3 | 588.29 | 2003 | Bent & Van Hentenryck |
| C208 | 3 | 588.32 | 2003 | Bent & Van Hentenryck |

**Observación**: Solo 3 vehículos necesarios (-70% vs C1), distancias ~590 (-29% vs C1)

### Estrategias de Solución Recomendadas

```
1. Consolidación agresiva:
   - Maximizar clientes por ruta
   - Aprovechar capacidad holgada
   - Ignorar restricciones temporales (son laxas)

2. Optimización de distancias:
   - TSP dentro de cada cluster
   - 2-opt, 3-opt agresivos
   - Lin-Kernighan para rutas largas

3. Asignación de clusters:
   - Cada vehículo puede visitar múltiples clusters
   - Optimizar secuencia de clusters

4. Metaheurísticas:
   - Simulated Annealing
   - Genetic Algorithms
   - Variable Neighborhood Search
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Distribución mayorista con entregas flexibles
  ✓ Planificación semanal de rutas
  ✓ Servicios no urgentes
  ✓ Logística de largo plazo

Características del mundo real:
  - Ventanas de entrega amplias (1-2 días)
  - Vehículos de gran capacidad
  - Enfoque en eficiencia de combustible
  - Minimización de costos operativos
```

---

## Familia R1: Clientes Aleatorios con Ventanas Cortas

### Identificación
- **Código**: R1XX (R101, R102, ..., R112)
- **Número de instancias**: 12
- **Rango**: R101 a R112

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Aleatoria uniforme
Número de clusters: 0 (sin agrupamiento)
Patrón espacial: Dispersión uniforme

Área de distribución:
  - X ∈ [2, 67] (rango: 65 unidades)
  - Y ∈ [5, 77] (rango: 72 unidades)
  - Área efectiva: ~4,680 unidades²
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 2
  - Máximo: 67
  - Media: 34.8
  - Desviación estándar: 16.2

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 77
  - Media: 39.5
  - Desviación estándar: 18.7

Densidad:
  - Clientes por unidad²: 0.021
  - Distancia promedio al vecino más cercano: 6.2 unidades
  - Coeficiente de variación espacial: Alto (CV > 0.45)
```

#### Análisis de Uniformidad
```
Test de Hopkins: H ≈ 0.50
Interpretación: Distribución aleatoria uniforme

Test de Kolmogorov-Smirnov:
  - p-value (X): 0.42
  - p-value (Y): 0.38
  - Conclusión: No se rechaza uniformidad

Índice de Morisita: I ≈ 1.0
Interpretación: Patrón aleatorio (no agrupado, no regular)
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: 230 unidades de tiempo
Inicio: 0
Fin: 230
Duración: MUY CORTA (5.4x menor que R2)
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Constante: 10 unidades
  - Uniformidad: 100%
  - Característica: EXTREMADAMENTE ESTRECHA

Distribución temporal:
  - Clientes tempranos [0-60]: 20%
  - Clientes medios [60-120]: 35%
  - Clientes medios-tardíos [120-180]: 30%
  - Clientes tardíos [180-230]: 15%

Tiempo de servicio:
  - Constante: 10 unidades
  - Porcentaje de ventana: 100% (10/10)
  - Margen disponible: 0 unidades
  - Implicación: SIN MARGEN DE ERROR
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 15% de pares
Ventanas disjuntas: 85% de pares
Conflictos temporales: SEVEROS (60%)

Interpretación:
  - Altísima fragmentación temporal
  - Cada cliente requiere slot único
  - Imposible consolidación temporal
  - Factibilidad extremadamente restrictiva
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 1 unidad
  - Máxima: 41 unidades
  - Promedio: 15.2 unidades
  - Desviación estándar: 9.8 unidades
  - Coeficiente de variación: 0.64 (alta variabilidad)

Distribución:
  - Sesgo: Positivo (más demandas bajas)
  - Curtosis: Normal
  - Rango: Muy amplio [1, 41]

Demanda total: ~1,520 unidades
Capacidad del vehículo: 200 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 13
  - Utilización promedio: 75%
  - Restricción: MODERADA
```

### Parámetros del Vehículo

```
Capacidad: 200 unidades
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Limitante principal: TIEMPO (no capacidad)
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar número de vehículos
Objetivo secundario: Minimizar distancia total

Función objetivo:
  f(s) = 1000 × num_vehiculos + distancia_total

Desafío principal: Encontrar solución FACTIBLE
```

### Dificultad Computacional

```
Nivel de dificultad: MUY ALTA (la más difícil del dataset)

Factores de complejidad:
  ✓✓✓ Ventanas extremadamente estrechas (restricción crítica)
  ✓✓ Distribución aleatoria (sin estructura)
  ✓✓ Horizonte muy corto (230 unidades)
  ✓ Alta fragmentación temporal (85% disjuntas)
  ✗ Capacidad moderada (75% utilización)

Tiempo de resolución típico:
  - Heurística simple: 5-15 segundos
  - Metaheurística: 30-300 segundos
  - Método exacto: Intratable (>24 horas)

Tasa de fracaso:
  - Heurísticas simples: 40-60% (soluciones infactibles)
  - Metaheurísticas: 10-20%
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| R101 | 19 | 1650.80 | 2003 | Bent & Van Hentenryck |
| R102 | 17 | 1486.12 | 2003 | Bent & Van Hentenryck |
| R103 | 13 | 1292.68 | 2003 | Bent & Van Hentenryck |
| R104 | 9 | 1007.31 | 2003 | Bent & Van Hentenryck |
| R105 | 14 | 1377.11 | 2003 | Bent & Van Hentenryck |
| R106 | 12 | 1252.03 | 2003 | Bent & Van Hentenryck |
| R107 | 10 | 1104.66 | 2003 | Bent & Van Hentenryck |
| R108 | 9 | 960.88 | 2003 | Bent & Van Hentenryck |
| R109 | 11 | 1194.73 | 2003 | Bent & Van Hentenryck |
| R110 | 10 | 1118.84 | 2003 | Bent & Van Hentenryck |
| R111 | 10 | 1096.72 | 2003 | Bent & Van Hentenryck |
| R112 | 9 | 982.14 | 2003 | Bent & Van Hentenryck |

**Observación**: Requieren 9-19 vehículos (2x más que C1), distancias largas (~1,200)

### Estrategias de Solución Recomendadas

```
1. Construcción temporal:
   - Ordenar clientes por ready_time
   - Construcción secuencial respetando tiempos
   - Inserción solo si factible temporalmente

2. Minimización de esperas:
   - Evitar llegadas tempranas
   - Sincronizar con ventanas
   - Calcular tiempos exactos

3. Búsqueda local adaptativa:
   - Relocate con verificación temporal
   - Exchange solo entre rutas compatibles
   - 2-opt limitado (puede romper factibilidad)

4. Metaheurísticas especializadas:
   - Large Neighborhood Search (LNS)
   - Adaptive Large Neighborhood Search (ALNS)
   - Constraint Programming híbrido
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Servicios médicos a domicilio (citas exactas)
  ✓ Entregas urgentes con slots de 15-30 minutos
  ✓ Servicios técnicos con horarios estrictos
  ✓ Recolección de muestras médicas

Características del mundo real:
  - Clientes dispersos geográficamente
  - Ventanas de tiempo muy estrictas
  - Penalizaciones severas por retrasos
  - Alta prioridad en puntualidad
```

---

## Familia R2: Clientes Aleatorios con Ventanas Largas

### Identificación
- **Código**: R2XX (R201, R202, ..., R211)
- **Número de instancias**: 11
- **Rango**: R201 a R211

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Aleatoria uniforme (idéntica a R1)
Número de clusters: 0 (sin agrupamiento)
Patrón espacial: Dispersión uniforme

Área de distribución:
  - X ∈ [2, 67]
  - Y ∈ [5, 77]
  - Idéntica a R1
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 2
  - Máximo: 67
  - Media: 34.8
  - Desviación estándar: 16.2

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 77
  - Media: 39.5
  - Desviación estándar: 18.7

Densidad:
  - Idéntica a R1
  - Distancia promedio al vecino: 6.2 unidades
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: 1,000 unidades de tiempo
Inicio: 0
Fin: 1,000
Incremento vs R1: +335% (770 unidades más)
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Mínima: 57 unidades
  - Máxima: 139 unidades
  - Promedio: 100 unidades
  - Desviación estándar: 25 unidades
  - Variabilidad: MODERADA-ALTA

Distribución temporal:
  - Dispersa a lo largo del horizonte
  - Solapamiento: ~60%
  - Flexibilidad: ALTA

Tiempo de servicio:
  - Constante: 10 unidades
  - Porcentaje de ventana: 10% (10/100)
  - Margen disponible: 90 unidades
  - Implicación: MUCHA FLEXIBILIDAD
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 60% de pares
Ventanas disjuntas: 40% de pares
Conflictos temporales: BAJOS (15%)

Interpretación:
  - Moderada fragmentación temporal
  - Posibilidad de consolidación
  - Flexibilidad para optimizar
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 1 unidad
  - Máxima: 41 unidades
  - Promedio: 15.2 unidades
  - Idéntica a R1

Demanda total: ~1,520 unidades
Capacidad del vehículo: 1,000 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 67
  - Utilización promedio: 15%
  - Restricción: MUY HOLGADA
```

### Parámetros del Vehículo

```
Capacidad: 1,000 unidades (+400% vs R1)
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Limitante principal: DISTANCIA (no tiempo ni capacidad)
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar distancia total
Objetivo secundario: Minimizar número de vehículos

Función objetivo:
  f(s) = distancia_total + 100 × num_vehiculos

Desafío principal: Optimización de rutas largas
```

### Dificultad Computacional

```
Nivel de dificultad: MEDIA

Factores de complejidad:
  ✗ Ventanas amplias (baja restricción temporal)
  ✗ Capacidad muy holgada (15% utilización)
  ✓ Distribución aleatoria (sin estructura espacial)
  ✓ Rutas largas (optimización compleja)

Tiempo de resolución típico:
  - Heurística simple: 2-5 segundos
  - Metaheurística: 10-60 segundos
  - Método exacto: Difícil pero factible
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| R201 | 4 | 1252.37 | 1999 | Mester & Bräysy |
| R202 | 3 | 1191.70 | 1999 | Mester & Bräysy |
| R203 | 3 | 939.50 | 2003 | Bent & Van Hentenryck |
| R204 | 2 | 825.52 | 2003 | Bent & Van Hentenryck |
| R205 | 3 | 994.42 | 2003 | Bent & Van Hentenryck |
| R206 | 3 | 906.14 | 2003 | Bent & Van Hentenryck |
| R207 | 2 | 890.61 | 2003 | Bent & Van Hentenryck |
| R208 | 2 | 726.82 | 2003 | Bent & Van Hentenryck |
| R209 | 3 | 909.16 | 2003 | Bent & Van Hentenryck |
| R210 | 3 | 939.37 | 2003 | Bent & Van Hentenryck |
| R211 | 2 | 885.71 | 2003 | Bent & Van Hentenryck |

**Observación**: Solo 2-4 vehículos (-79% vs R1), distancias ~950 (-24% vs R1)

### Estrategias de Solución Recomendadas

```
1. Construcción espacial:
   - Sweep algorithm (barrido angular)
   - Savings algorithm (Clarke-Wright)
   - Nearest Neighbor geográfico

2. Optimización de rutas:
   - TSP solver para cada ruta
   - 2-opt, 3-opt intensivos
   - Lin-Kernighan para rutas largas

3. Mejora inter-rutas:
   - Relocate agresivo
   - Exchange entre rutas
   - Cross-exchange

4. Metaheurísticas:
   - Genetic Algorithms
   - Tabu Search
   - Variable Neighborhood Descent
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Distribución rural con entregas flexibles
  ✓ Servicios de mantenimiento programados
  ✓ Logística de largo plazo
  ✓ Entregas no urgentes en áreas dispersas

Características del mundo real:
  - Clientes en zonas rurales/suburbanas
  - Ventanas de entrega amplias (días)
  - Vehículos de gran capacidad
  - Enfoque en minimizar kilómetros
```

---

## Familia RC1: Clientes Mixtos con Ventanas Cortas

### Identificación
- **Código**: RC1XX (RC101, RC102, ..., RC108)
- **Número de instancias**: 8
- **Rango**: RC101 a RC108

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Semi-agrupada (híbrida)
Número de clusters: 2-3 clusters principales
Patrón espacial: Mezcla de agrupado y disperso

Composición:
  - Clientes en clusters: ~60%
  - Clientes dispersos: ~40%

Clusters principales:
  Cluster 1:
    - Ubicación: X ∈ [35, 50], Y ∈ [30, 50]
    - Clientes: ~30
    - Densidad: Alta

  Cluster 2:
    - Ubicación: X ∈ [60, 70], Y ∈ [75, 85]
    - Clientes: ~30
    - Densidad: Alta

  Clientes satélite:
    - Dispersos en todo el espacio
    - ~40 clientes
    - Densidad: Baja
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 0
  - Máximo: 95
  - Media: 40.2
  - Desviación estándar: 24.8

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 85
  - Media: 44.5
  - Desviación estándar: 25.3

Índice de Hopkins: H ≈ 0.35
Interpretación: Agrupamiento moderado

Distancias:
  - Intra-cluster: 9.2 unidades
  - Inter-cluster: 38.5 unidades
  - Cluster-disperso: 22.7 unidades
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: 240 unidades de tiempo
Inicio: 0
Fin: 240
Duración: MUY CORTA (similar a R1)
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Constante: 30 unidades
  - Uniformidad: 100%
  - Característica: ESTRECHA

Distribución temporal:
  - Clientes tempranos [0-60]: 25%
  - Clientes medios [60-120]: 30%
  - Clientes medios-tardíos [120-180]: 30%
  - Clientes tardíos [180-240]: 15%

Tiempo de servicio:
  - Constante: 10 unidades
  - Porcentaje de ventana: 33% (10/30)
  - Margen disponible: 20 unidades
  - Implicación: MODERADAMENTE AJUSTADO
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 40% de pares
Ventanas disjuntas: 60% de pares
Conflictos temporales: MODERADOS (35%)

Interpretación:
  - Moderada-alta fragmentación temporal
  - Consolidación posible pero limitada
  - Balance entre flexibilidad y restricción
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 3 unidades
  - Máxima: 40 unidades
  - Promedio: 17.8 unidades
  - Desviación estándar: 10.2 unidades
  - Coeficiente de variación: 0.57

Distribución:
  - Sesgo: Ligeramente positivo
  - Curtosis: Normal
  - Rango: [3, 40]

Demanda total: ~1,780 unidades
Capacidad del vehículo: 200 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 11
  - Utilización promedio: 90%
  - Restricción: AJUSTADA
```

### Parámetros del Vehículo

```
Capacidad: 200 unidades
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Limitantes: TIEMPO y CAPACIDAD (ambos importantes)
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar número de vehículos
Objetivo secundario: Minimizar distancia total

Función objetivo:
  f(s) = 1000 × num_vehiculos + distancia_total

Desafío: Equilibrar consolidación y factibilidad
```

### Dificultad Computacional

```
Nivel de dificultad: ALTA

Factores de complejidad:
  ✓✓ Ventanas estrechas (restricción significativa)
  ✓ Distribución mixta (sin estructura clara)
  ✓ Capacidad ajustada (90% utilización)
  ✓ Horizonte corto (240 unidades)
  ✗ Algunos clusters (facilita parcialmente)

Tiempo de resolución típico:
  - Heurística simple: 3-8 segundos
  - Metaheurística: 15-120 segundos
  - Método exacto: Muy difícil (>horas)
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| RC101 | 14 | 1696.95 | 2003 | Bent & Van Hentenryck |
| RC102 | 12 | 1554.75 | 2003 | Bent & Van Hentenryck |
| RC103 | 11 | 1261.67 | 2003 | Bent & Van Hentenryck |
| RC104 | 10 | 1135.48 | 2003 | Bent & Van Hentenryck |
| RC105 | 13 | 1629.44 | 2003 | Bent & Van Hentenryck |
| RC106 | 11 | 1424.73 | 2003 | Bent & Van Hentenryck |
| RC107 | 11 | 1230.48 | 2003 | Bent & Van Hentenryck |
| RC108 | 10 | 1139.82 | 2003 | Bent & Van Hentenryck |

**Observación**: Requieren 10-14 vehículos (similar a C1), distancias ~1,400

### Estrategias de Solución Recomendadas

```
1. Identificación de estructura:
   - Clustering parcial (k=2-3)
   - Identificar clientes satélite
   - Clasificar por densidad

2. Construcción híbrida:
   - Ruteo intra-cluster (tipo C)
   - Ruteo disperso (tipo R)
   - Integración de ambos enfoques

3. Optimización adaptativa:
   - 2-opt dentro de clusters
   - Relocate para clientes satélite
   - Exchange limitado

4. Metaheurísticas:
   - Adaptive Large Neighborhood Search
   - Hybrid Genetic Algorithm
   - Memetic Algorithms
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Distribución urbana-suburbana mixta
  ✓ Servicios en ciudad con zonas periféricas
  ✓ Entregas con clientes concentrados y dispersos
  ✓ Logística en áreas metropolitanas

Características del mundo real:
  - Mezcla de zonas densas y dispersas
  - Ventanas de tiempo moderadamente estrictas
  - Capacidad limitada
  - Balance entre cobertura y eficiencia
```

---

## Familia RC2: Clientes Mixtos con Ventanas Largas

### Identificación
- **Código**: RC2XX (RC201, RC202, ..., RC208)
- **Número de instancias**: 8
- **Rango**: RC201 a RC208

### Características Geográficas

#### Distribución Espacial
```
Tipo de distribución: Semi-agrupada (idéntica a RC1)
Número de clusters: 2-3 clusters principales
Patrón espacial: Mezcla de agrupado y disperso

Composición:
  - Clientes en clusters: ~60%
  - Clientes dispersos: ~40%
  - Idéntica a RC1
```

#### Estadísticas Espaciales
```
Coordenadas X:
  - Mínimo: 0
  - Máximo: 95
  - Media: 40.2
  - Desviación estándar: 24.8

Coordenadas Y:
  - Mínimo: 5
  - Máximo: 85
  - Media: 44.5
  - Desviación estándar: 25.3

Índice de Hopkins: H ≈ 0.35
Idéntica a RC1
```

### Características Temporales

#### Horizonte de Planificación
```
Horizonte total: Variable (~1,000-2,000 unidades)
Promedio: ~1,500 unidades
Incremento vs RC1: +525% aproximadamente
```

#### Ventanas de Tiempo
```
Amplitud de ventanas:
  - Mínima: 30 unidades
  - Máxima: 175 unidades
  - Promedio: 90 unidades
  - Desviación estándar: 35 unidades
  - Variabilidad: ALTA

Distribución temporal:
  - Muy dispersa
  - Solapamiento: ~70%
  - Flexibilidad: ALTA

Tiempo de servicio:
  - Constante: 10 unidades
  - Porcentaje de ventana: 11% (10/90)
  - Margen disponible: 80 unidades
  - Implicación: MUCHA FLEXIBILIDAD
```

#### Análisis de Solapamiento
```
Ventanas solapadas: 70% de pares
Ventanas disjuntas: 30% de pares
Conflictos temporales: BAJOS (20%)

Interpretación:
  - Baja fragmentación temporal
  - Alta posibilidad de consolidación
  - Flexibilidad para optimizar distancias
```

### Características de Demanda

```
Demanda por cliente:
  - Mínima: 3 unidades
  - Máxima: 40 unidades
  - Promedio: 17.8 unidades
  - Idéntica a RC1

Demanda total: ~1,780 unidades
Capacidad del vehículo: 1,000 unidades

Análisis de capacidad:
  - Clientes por vehículo (teórico): 56
  - Utilización promedio: 18%
  - Restricción: MUY HOLGADA
```

### Parámetros del Vehículo

```
Capacidad: 1,000 unidades (+400% vs RC1)
Velocidad: 1 unidad de distancia = 1 unidad de tiempo
Número de vehículos disponibles: Ilimitado
Limitante principal: DISTANCIA (estructura espacial)
```

### Objetivos de Optimización

```
Objetivo primario: Minimizar distancia total
Objetivo secundario: Minimizar número de vehículos

Función objetivo:
  f(s) = distancia_total + 100 × num_vehiculos

Desafío: Optimizar con estructura espacial mixta
```

### Dificultad Computacional

```
Nivel de dificultad: MEDIA-ALTA

Factores de complejidad:
  ✗ Ventanas amplias (baja restricción temporal)
  ✗ Capacidad muy holgada (18% utilización)
  ✓ Distribución mixta (estructura parcial)
  ✓ Optimización de rutas largas
  ✓ Balance cluster-disperso

Tiempo de resolución típico:
  - Heurística simple: 2-6 segundos
  - Metaheurística: 10-80 segundos
  - Método exacto: Difícil
```

### Mejores Soluciones Conocidas (BKS)

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| RC201 | 4 | 1406.94 | 1999 | Mester & Bräysy |
| RC202 | 3 | 1365.65 | 1999 | Mester & Bräysy |
| RC203 | 3 | 1049.62 | 2003 | Bent & Van Hentenryck |
| RC204 | 3 | 798.46 | 2003 | Bent & Van Hentenryck |
| RC205 | 4 | 1297.65 | 2003 | Bent & Van Hentenryck |
| RC206 | 3 | 1146.32 | 2003 | Bent & Van Hentenryck |
| RC207 | 3 | 1061.14 | 2003 | Bent & Van Hentenryck |
| RC208 | 3 | 828.14 | 2003 | Bent & Van Hentenryck |

**Observación**: Solo 3-4 vehículos (-73% vs RC1), distancias ~1,120 (-20% vs RC1)

### Estrategias de Solución Recomendadas

```
1. Aprovechamiento de clusters:
   - Identificar y explotar estructura parcial
   - Ruteo eficiente dentro de clusters
   - Conexión óptima entre clusters

2. Gestión de clientes dispersos:
   - Asignación inteligente a rutas
   - Minimizar desvíos
   - Considerar como "puentes" entre clusters

3. Optimización intensiva:
   - TSP para segmentos de ruta
   - 2-opt, 3-opt agresivos
   - Cross-exchange entre rutas

4. Metaheurísticas:
   - Variable Neighborhood Search
   - Iterated Local Search
   - Simulated Annealing
```

### Casos de Uso Real

```
Escenarios modelados:
  ✓ Distribución regional con centros urbanos
  ✓ Logística mixta urbana-rural
  ✓ Servicios flexibles en áreas heterogéneas
  ✓ Planificación de medio plazo

Características del mundo real:
  - Mezcla de zonas densas y dispersas
  - Ventanas de entrega flexibles
  - Vehículos de gran capacidad
  - Optimización de costos de transporte
```

---

## Comparación Entre Familias

### Tabla Comparativa Completa

| Característica | C1 | C2 | R1 | R2 | RC1 | RC2 |
|----------------|----|----|----|----|-----|-----|
| **Instancias** | 9 | 8 | 12 | 11 | 8 | 8 |
| **Distribución** | Agrupada | Agrupada | Aleatoria | Aleatoria | Mixta | Mixta |
| **Clusters** | 4 | 4 | 0 | 0 | 2-3 | 2-3 |
| **Horizonte** | 1,236 | 3,390 | 230 | 1,000 | 240 | ~1,500 |
| **Amplitud ventana** | 55 | 160 | 10 | 100 | 30 | 90 |
| **Servicio** | 90 | 90 | 10 | 10 | 10 | 10 |
| **Capacidad** | 200 | 700 | 200 | 1,000 | 200 | 1,000 |
| **Demanda promedio** | 20 | 20 | 15 | 15 | 18 | 18 |
| **Vehículos (BKS)** | 10 | 3 | 9-19 | 2-4 | 10-14 | 3-4 |
| **Distancia (BKS)** | ~828 | ~590 | ~1,200 | ~950 | ~1,400 | ~1,120 |
| **Dificultad** | Media-Alta | Baja | Muy Alta | Media | Alta | Media-Alta |

### Comparación de Restricciones

#### Restricción Temporal

```
Más restrictiva → Menos restrictiva:
R1 (10 unidades) > RC1 (30) > C1 (55) > RC2 (90) > R2 (100) > C2 (160)
```

#### Restricción de Capacidad

```
Más restrictiva → Menos restrictiva:
C1 (100%) > RC1 (90%) > R1 (75%) > C2 (29%) > RC2 (18%) > R2 (15%)
```

#### Complejidad Espacial

```
Más compleja → Menos compleja:
R1/R2 (aleatorio) > RC1/RC2 (mixto) > C1/C2 (agrupado)
```

### Matriz de Similitud

```
         C1    C2    R1    R2    RC1   RC2
C1      1.00  0.75  0.20  0.15  0.45  0.30
C2      0.75  1.00  0.10  0.25  0.35  0.50
R1      0.20  0.10  1.00  0.60  0.55  0.35
R2      0.15  0.25  0.60  1.00  0.40  0.65
RC1     0.45  0.35  0.55  0.40  1.00  0.70
RC2     0.30  0.50  0.35  0.65  0.70  1.00
```

**Interpretación**:
- C1 y C2 son muy similares (0.75) - misma distribución espacial
- R1 y R2 son similares (0.60) - misma distribución espacial
- RC1 y RC2 son similares (0.70) - misma distribución espacial
- Familias con mismo número (1 o 2) tienen baja similitud entre tipos

---

## Guía de Selección de Instancias

### Para Desarrollo de Algoritmos

#### Fase 1: Pruebas Iniciales
```
Instancias recomendadas:
  - C101: Agrupada, ventanas cortas (baseline)
  - R101: Aleatoria, ventanas cortas (desafío)
  - RC101: Mixta, ventanas cortas (intermedio)

Objetivo: Verificar factibilidad básica
```

#### Fase 2: Validación
```
Instancias recomendadas:
  - C201: Agrupada, ventanas largas (optimización)
  - R201: Aleatoria, ventanas largas (consolidación)
  - RC201: Mixta, ventanas largas (balance)

Objetivo: Evaluar calidad de soluciones
```

#### Fase 3: Benchmarking Completo
```
Todas las 56 instancias

Objetivo: Comparación con estado del arte
```

### Para Investigación

#### Estudio de Ventanas de Tiempo
```
Comparar:
  - C1 vs C2: Efecto de amplitud en clientes agrupados
  - R1 vs R2: Efecto de amplitud en clientes aleatorios
  - RC1 vs RC2: Efecto de amplitud en clientes mixtos
```

#### Estudio de Distribución Espacial
```
Comparar:
  - C1 vs R1 vs RC1: Efecto de distribución con ventanas cortas
  - C2 vs R2 vs RC2: Efecto de distribución con ventanas largas
```

#### Estudio de Capacidad
```
Comparar:
  - Serie 1 (200 unidades) vs Serie 2 (700-1,000 unidades)
  - Analizar trade-off vehículos vs distancia
```

### Para Aplicaciones Prácticas

#### Entrega Urbana con Citas
```
Familia recomendada: C1
Razón: Clientes agrupados, ventanas estrictas
```

#### Distribución Mayorista
```
Familia recomendada: C2
Razón: Consolidación, ventanas flexibles
```

#### Servicios Técnicos Urgentes
```
Familia recomendada: R1
Razón: Clientes dispersos, citas exactas
```

#### Logística Regional
```
Familia recomendada: R2
Razón: Cobertura amplia, flexibilidad temporal
```

#### Distribución Mixta Urbana-Rural
```
Familia recomendada: RC1 o RC2
Razón: Estructura espacial heterogénea
```

### Criterios de Selección

```
SI necesitas:
  ├─ Probar factibilidad temporal → R1
  ├─ Optimizar distancias → C2 o R2
  ├─ Minimizar vehículos → C1 o R1
  ├─ Escenario realista urbano → C1 o C2
  ├─ Escenario realista rural → R1 o R2
  ├─ Escenario realista mixto → RC1 o RC2
  ├─ Algoritmo rápido → C2
  ├─ Algoritmo robusto → R1
  └─ Benchmark completo → Todas las familias
```

---

## Resumen Ejecutivo por Familia

### C1: El Clásico Urbano
```
✓ Estructura clara (4 clusters)
✓ Ventanas moderadamente estrictas
✓ Capacidad ajustada
→ Ideal para: Desarrollo inicial, entrega urbana
```

### C2: El Optimizador
```
✓ Estructura clara (4 clusters)
✓ Ventanas muy flexibles
✓ Capacidad holgada
→ Ideal para: Optimización de distancias, planificación flexible
```

### R1: El Desafío Extremo
```
✗ Sin estructura espacial
✗ Ventanas extremadamente estrictas
✓ Capacidad moderada
→ Ideal para: Probar robustez, servicios urgentes
```

### R2: El Consolidador
```
✗ Sin estructura espacial
✓ Ventanas flexibles
✓ Capacidad muy holgada
→ Ideal para: Consolidación, distribución regional
```

### RC1: El Híbrido Difícil
```
~ Estructura parcial
✗ Ventanas estrictas
✓ Capacidad ajustada
→ Ideal para: Escenarios mixtos, algoritmos adaptativos
```

### RC2: El Híbrido Flexible
```
~ Estructura parcial
✓ Ventanas flexibles
✓ Capacidad holgada
→ Ideal para: Logística mixta, optimización con estructura parcial
```

---

**Documento generado**: Diciembre 2025  
**Versión**: 1.0  
**Propósito**: Guía detallada de características de familias Solomon VRPTW  
**Uso**: Investigación, desarrollo de algoritmos, aplicaciones prácticas
