# Documentación Completa del Dataset Solomon VRPTW

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [¿Qué es el Problema VRPTW?](#qué-es-el-problema-vrptw)
3. [Estructura del Dataset](#estructura-del-dataset)
4. [Caracterización Detallada](#caracterización-detallada)
5. [Formato de los Archivos](#formato-de-los-archivos)
6. [Ejemplos Detallados](#ejemplos-detallados)
7. [Tipos de Instancias](#tipos-de-instancias)
8. [Análisis Estadístico](#análisis-estadístico)
9. [Uso y Aplicaciones](#uso-y-aplicaciones)
10. [Referencias](#referencias)

---

## Introducción

El **Solomon VRPTW Benchmark** es un conjunto de datos estándar ampliamente utilizado en la investigación de optimización combinatoria y logística. Fue desarrollado por Marius M. Solomon en 1987 y se ha convertido en el benchmark de referencia para evaluar algoritmos que resuelven el **Vehicle Routing Problem with Time Windows (VRPTW)**.

### Características Principales
- **56 instancias de prueba** organizadas en 6 categorías
- **100 clientes** por instancia (más el depósito)
- **Ventanas de tiempo estrictas** que deben respetarse
- **Diferentes patrones geográficos** de distribución de clientes
- **Formato CSV estandarizado** para fácil procesamiento

### Fuente Original
```
https://www.kaggle.com/datasets/masud7866/solomon-vrptw-benchmark
```

---

## ¿Qué es el Problema VRPTW?

### Definición del Problema

El **Vehicle Routing Problem with Time Windows (VRPTW)** es un problema de optimización combinatoria que consiste en:

**Objetivo**: Diseñar rutas óptimas para una flota de vehículos que deben:
1. Partir desde un depósito central
2. Visitar un conjunto de clientes geográficamente dispersos
3. Satisfacer la demanda de cada cliente
4. Respetar las ventanas de tiempo de cada cliente
5. Regresar al depósito
6. Minimizar el número de vehículos y/o la distancia total recorrida

### Restricciones Principales

1. **Capacidad del Vehículo**: Cada vehículo tiene una capacidad máxima que no puede excederse
2. **Ventanas de Tiempo**: Cada cliente tiene un intervalo de tiempo [READY TIME, DUE DATE] durante el cual debe ser atendido
3. **Tiempo de Servicio**: Cada cliente requiere un tiempo específico para ser atendido
4. **Visita Única**: Cada cliente debe ser visitado exactamente una vez por un solo vehículo
5. **Inicio y Fin en el Depósito**: Todas las rutas comienzan y terminan en el depósito

### Complejidad Computacional

El VRPTW es un problema **NP-hard**, lo que significa que:
- No existe un algoritmo conocido que pueda resolver todas las instancias en tiempo polinomial
- El tiempo de resolución crece exponencialmente con el número de clientes
- Se requieren heurísticas y metaheurísticas para instancias grandes

---

## Estructura del Dataset

### Organización de Directorios

```
SOLOMON_VRPTW_DATASET/
│
├── C1/                          # 9 instancias - Clientes agrupados, ventanas cortas
│   ├── C101.csv
│   ├── C102.csv
│   ├── ...
│   └── C109.csv
│
├── C2/                          # 8 instancias - Clientes agrupados, ventanas largas
│   ├── C201.csv
│   ├── C202.csv
│   ├── ...
│   └── C208.csv
│
├── R1/                          # 12 instancias - Clientes aleatorios, ventanas cortas
│   ├── R101.csv
│   ├── R102.csv
│   ├── ...
│   └── R112.csv
│
├── R2/                          # 11 instancias - Clientes aleatorios, ventanas largas
│   ├── R201.csv
│   ├── R202.csv
│   ├── ...
│   └── R211.csv
│
├── RC1/                         # 8 instancias - Clientes mixtos, ventanas cortas
│   ├── RC101.csv
│   ├── RC102.csv
│   ├── ...
│   └── RC108.csv
│
├── RC2/                         # 8 instancias - Clientes mixtos, ventanas largas
│   ├── RC201.csv
│   ├── RC202.csv
│   ├── ...
│   └── RC208.csv
│
├── FUENTE_DESCARGA.txt          # URL de descarga del dataset
├── Solomon VRPTW benchmark.pdf  # Documentación original
└── archive.zip                  # Archivo comprimido del dataset
```

### Nomenclatura de Archivos

El nombre de cada archivo sigue un patrón específico:

**Formato**: `[TIPO][SERIE][NÚMERO].csv`

- **TIPO**: 
  - `C` = Clustered (Agrupados)
  - `R` = Random (Aleatorios)
  - `RC` = Random-Clustered (Mixtos)

- **SERIE**:
  - `1` = Ventanas de tiempo cortas (short time windows)
  - `2` = Ventanas de tiempo largas (long time windows)

- **NÚMERO**: Identificador de la instancia específica (01-12)

**Ejemplos**:
- `C101.csv`: Clientes agrupados, ventanas cortas, instancia 1
- `R205.csv`: Clientes aleatorios, ventanas largas, instancia 5
- `RC108.csv`: Clientes mixtos, ventanas cortas, instancia 8

---

## Caracterización Detallada

### Tipos de Instancias

#### **Tipo C (Clustered - Agrupados)**

**Características**:
- Los clientes están organizados en grupos geográficos claramente definidos
- Facilita la formación de rutas compactas
- Los clientes dentro de un mismo cluster están próximos entre sí
- Generalmente requiere menos vehículos que los tipos R

**Diferencias entre C1 y C2**:
- **C1**: Ventanas de tiempo estrechas (horizonte temporal ~1,236 unidades)
- **C2**: Ventanas de tiempo amplias (horizonte temporal ~3,390 unidades)

**Número de instancias**:
- C1: 9 instancias (C101-C109)
- C2: 8 instancias (C201-C208)

#### **Tipo R (Random - Aleatorios)**

**Características**:
- Los clientes están distribuidos uniformemente en el espacio
- No hay patrones geográficos evidentes
- Mayor dificultad para formar rutas eficientes
- Requiere más vehículos y rutas más largas

**Diferencias entre R1 y R2**:
- **R1**: Ventanas de tiempo estrechas (horizonte temporal ~230 unidades)
- **R2**: Ventanas de tiempo amplias (horizonte temporal ~1,000 unidades)

**Número de instancias**:
- R1: 12 instancias (R101-R112)
- R2: 11 instancias (R201-R211)

#### **Tipo RC (Random-Clustered - Mixtos)**

**Características**:
- Combinación de clientes agrupados y dispersos
- Algunos clientes forman clusters, otros están aislados
- Dificultad intermedia entre tipos C y R
- Refleja escenarios del mundo real más realistas

**Diferencias entre RC1 y RC2**:
- **RC1**: Ventanas de tiempo estrechas (horizonte temporal ~240 unidades)
- **RC2**: Ventanas de tiempo amplias (horizonte temporal variable)

**Número de instancias**:
- RC1: 8 instancias (RC101-RC108)
- RC2: 8 instancias (RC201-RC208)

### Parámetros Comunes

Todos los archivos comparten las siguientes características:

1. **Número de clientes**: 100 clientes + 1 depósito = 101 nodos totales
2. **Capacidad del vehículo**: Varía según la instancia (típicamente 200 unidades)
3. **Espacio de coordenadas**: Plano euclidiano 2D (típicamente 0-100 en X e Y)
4. **Cálculo de distancias**: Distancia euclidiana entre puntos
5. **Velocidad del vehículo**: Generalmente se asume constante (1 unidad de distancia = 1 unidad de tiempo)

---

## Formato de los Archivos

### Estructura del CSV

Cada archivo CSV contiene **103 líneas**:
- **Línea 1**: Encabezado con nombres de columnas
- **Líneas 2-102**: Datos de 101 nodos (1 depósito + 100 clientes)
- **Línea 103**: Línea vacía

### Columnas del Dataset

| Columna | Nombre | Tipo | Descripción | Rango Típico |
|---------|--------|------|-------------|--------------|
| 1 | CUST NO. | Entero | Número identificador del cliente | 1-101 |
| 2 | XCOORD. | Entero | Coordenada X en el plano | 0-100 |
| 3 | YCOORD. | Entero | Coordenada Y en el plano | 0-100 |
| 4 | DEMAND | Entero | Demanda del cliente (unidades) | 0-50 |
| 5 | READY TIME | Entero | Inicio de la ventana de tiempo | 0-3000+ |
| 6 | DUE DATE | Entero | Fin de la ventana de tiempo | 0-3500+ |
| 7 | SERVICE TIME | Entero | Tiempo requerido para atender al cliente | 0-90 |

### Descripción Detallada de Cada Campo

#### 1. CUST NO. (Customer Number)

**Descripción**: Identificador único del nodo.

**Características**:
- El valor `1` siempre representa el **depósito** (punto de inicio y fin)
- Los valores `2-101` representan los **clientes** a visitar
- Es un identificador secuencial y único

**Ejemplo**:
```
CUST NO.
1          ← Depósito
2          ← Cliente 1
3          ← Cliente 2
...
101        ← Cliente 100
```

#### 2. XCOORD. (X Coordinate)

**Descripción**: Posición horizontal del nodo en el plano cartesiano.

**Características**:
- Valores enteros
- Rango típico: 0-100 (aunque puede variar)
- Unidades arbitrarias (pueden representar kilómetros, millas, etc.)
- Se usa para calcular distancias euclidianas

**Fórmula de distancia**:
```
distancia = √[(X₂ - X₁)² + (Y₂ - Y₁)²]
```

#### 3. YCOORD. (Y Coordinate)

**Descripción**: Posición vertical del nodo en el plano cartesiano.

**Características**:
- Valores enteros
- Rango típico: 0-100
- Complementa XCOORD para definir la posición exacta
- Mismo sistema de unidades que XCOORD

#### 4. DEMAND (Demanda)

**Descripción**: Cantidad de producto/servicio que requiere el cliente.

**Características**:
- El depósito (CUST NO. = 1) siempre tiene demanda = 0
- Los clientes tienen demandas > 0
- Rango típico: 1-50 unidades
- La suma de demandas en una ruta no puede exceder la capacidad del vehículo

**Restricción**:
```
∑(demandas en ruta) ≤ Capacidad del Vehículo
```

**Ejemplo**:
```
CUST NO.  DEMAND
1         0       ← Depósito (sin demanda)
2         10      ← Cliente requiere 10 unidades
3         30      ← Cliente requiere 30 unidades
4         10      ← Cliente requiere 10 unidades
```

#### 5. READY TIME (Tiempo de Inicio)

**Descripción**: Momento más temprano en el que el cliente puede ser atendido.

**Características**:
- El depósito tiene READY TIME = 0 (inicio de operaciones)
- Representa el inicio de la ventana de tiempo
- Si un vehículo llega antes, debe esperar
- Unidades de tiempo arbitrarias (minutos, horas, etc.)

**Regla**:
```
Si tiempo_llegada < READY_TIME:
    tiempo_inicio_servicio = READY_TIME  (esperar)
Sino:
    tiempo_inicio_servicio = tiempo_llegada
```

#### 6. DUE DATE (Fecha Límite)

**Descripción**: Momento más tardío en el que el cliente puede ser atendido.

**Características**:
- Representa el fin de la ventana de tiempo
- El servicio DEBE comenzar antes o en este momento
- Si un vehículo llega después, la solución es **inválida**
- Para el depósito, representa el fin del horizonte de planificación

**Restricción crítica**:
```
tiempo_llegada ≤ DUE_DATE  (OBLIGATORIO)
```

**Ventana de tiempo**:
```
[READY_TIME, DUE_DATE] = Intervalo válido para iniciar el servicio
```

#### 7. SERVICE TIME (Tiempo de Servicio)

**Descripción**: Duración del servicio al cliente.

**Características**:
- El depósito tiene SERVICE TIME = 0
- Los clientes típicamente tienen 10 o 90 unidades de tiempo
- Se suma al tiempo de llegada para calcular el tiempo de salida
- Afecta la factibilidad de visitar clientes subsecuentes

**Cálculo del tiempo de salida**:
```
tiempo_salida = max(tiempo_llegada, READY_TIME) + SERVICE_TIME
```

---

## Ejemplos Detallados

### Ejemplo 1: Instancia C101 (Clientes Agrupados, Ventanas Cortas)

#### Encabezado y Primeras Líneas

```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
1,40,50,0,0,1236,0
2,45,68,10,912,967,90
3,45,70,30,825,870,90
4,42,66,10,65,146,90
5,42,68,10,727,782,90
```

#### Análisis Detallado

**Depósito (Línea 2)**:
```
CUST NO. = 1
Posición: (40, 50)
Demanda: 0 (no requiere servicio)
Ventana: [0, 1236] (toda la jornada laboral)
Servicio: 0 (sin tiempo de servicio)
```

**Cliente 2 (Línea 3)**:
```
CUST NO. = 2
Posición: (45, 68)
Demanda: 10 unidades
Ventana: [912, 967] (55 unidades de amplitud)
Servicio: 90 unidades de tiempo
```

**Interpretación**:
- El cliente 2 está ubicado en (45, 68), cerca del depósito
- Requiere 10 unidades de producto
- Solo puede ser atendido entre los tiempos 912 y 967
- El servicio toma 90 unidades de tiempo
- Si un vehículo llega a tiempo 912, terminará el servicio a tiempo 1002 (912 + 90)

**Distancia del depósito al cliente 2**:
```
d = √[(45-40)² + (68-50)²]
d = √[25 + 324]
d = √349
d ≈ 18.68 unidades
```

**Cliente 3 (Línea 4)**:
```
CUST NO. = 3
Posición: (45, 70)
Demanda: 30 unidades
Ventana: [825, 870] (45 unidades de amplitud)
Servicio: 90 unidades de tiempo
```

**Observación importante**:
- Los clientes 2 y 3 están muy cerca geográficamente (45,68) y (45,70)
- Pero tienen ventanas de tiempo diferentes: [912,967] vs [825,870]
- Esto crea un desafío: ¿se pueden visitar en la misma ruta?

**Análisis de factibilidad**:
```
Distancia entre cliente 3 y cliente 2:
d = √[(45-45)² + (70-68)²] = √4 = 2 unidades

Si visitamos cliente 3 primero:
- Llegada: tiempo 825 (en el mejor caso)
- Inicio servicio: 825
- Fin servicio: 825 + 90 = 915
- Viaje a cliente 2: 915 + 2 = 917
- ¿917 ≤ 967? SÍ → Factible visitar cliente 2 después
```

### Ejemplo 2: Instancia C201 (Clientes Agrupados, Ventanas Largas)

```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
1,40,50,0,0,3390,0
2,52,75,10,311,471,90
3,45,70,30,213,373,90
4,62,69,10,1167,1327,90
5,60,66,10,1261,1421,90
```

#### Comparación con C101

| Aspecto | C101 | C201 | Diferencia |
|---------|------|------|------------|
| Horizonte temporal | 1,236 | 3,390 | +174% más tiempo |
| Ventana cliente 2 | [912, 967] | [311, 471] | 160 unidades de amplitud |
| Ventana cliente 3 | [825, 870] | [213, 373] | 160 unidades de amplitud |
| Flexibilidad | Baja | Alta | Más opciones de ruteo |

**Implicaciones**:
- C201 permite más flexibilidad en el diseño de rutas
- Las ventanas de tiempo más amplias facilitan la consolidación de clientes
- Generalmente se requieren menos vehículos en C2 que en C1

### Ejemplo 3: Instancia R101 (Clientes Aleatorios, Ventanas Cortas)

```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
1,35,35,0,0,230,0
2,41,49,10,161,171,10
3,35,17,7,50,60,10
4,55,45,13,116,126,10
5,55,20,19,149,159,10
```

#### Características Distintivas

**Horizonte temporal muy corto**: Solo 230 unidades
**Ventanas extremadamente estrechas**: 10 unidades de amplitud
**Tiempo de servicio reducido**: 10 unidades (vs 90 en tipo C)

**Cliente 2**:
```
Ventana: [161, 171] → Solo 10 unidades de amplitud
Servicio: 10 unidades
Margen de error: CERO (ventana = tiempo de servicio)
```

**Desafío**:
- Si un vehículo llega a tiempo 161, termina a tiempo 171
- No hay margen para retrasos
- Requiere planificación muy precisa

### Ejemplo 4: Instancia R201 (Clientes Aleatorios, Ventanas Largas)

```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
1,35,35,0,0,1000,0
2,41,49,10,707,848,10
3,35,17,7,143,282,10
4,55,45,13,527,584,10
5,55,20,19,678,801,10
```

#### Comparación R101 vs R201

| Aspecto | R101 | R201 | Factor |
|---------|------|------|--------|
| Horizonte | 230 | 1,000 | 4.35x |
| Ventana cliente 2 | [161,171] (10) | [707,848] (141) | 14.1x |
| Ventana cliente 3 | [50,60] (10) | [143,282] (139) | 13.9x |
| Dificultad | Muy alta | Moderada | - |

### Ejemplo 5: Cálculo Completo de una Ruta

**Ruta propuesta**: Depósito → Cliente 3 → Cliente 2 → Depósito (usando datos de C101)

**Datos**:
```
Depósito:  (40, 50), ventana [0, 1236]
Cliente 3: (45, 70), demanda 30, ventana [825, 870], servicio 90
Cliente 2: (45, 68), demanda 10, ventana [912, 967], servicio 90
```

**Paso 1: Salida del depósito**
```
Tiempo de salida: 0
Capacidad usada: 0
```

**Paso 2: Viaje al Cliente 3**
```
Distancia: √[(45-40)² + (70-50)²] = √[25 + 400] = √425 ≈ 20.62
Tiempo de llegada: 0 + 20.62 ≈ 21
Ventana del cliente: [825, 870]
¿21 < 825? SÍ → Debe esperar hasta tiempo 825
Inicio de servicio: 825
Fin de servicio: 825 + 90 = 915
Capacidad usada: 30
```

**Paso 3: Viaje al Cliente 2**
```
Distancia: √[(45-45)² + (68-70)²] = √4 = 2
Tiempo de llegada: 915 + 2 = 917
Ventana del cliente: [912, 967]
¿917 ≤ 967? SÍ → Factible
¿917 ≥ 912? SÍ → No hay espera
Inicio de servicio: 917
Fin de servicio: 917 + 90 = 1007
Capacidad usada: 30 + 10 = 40
```

**Paso 4: Regreso al depósito**
```
Distancia: √[(40-45)² + (50-68)²] = √[25 + 324] = √349 ≈ 18.68
Tiempo de llegada: 1007 + 18.68 ≈ 1026
Ventana del depósito: [0, 1236]
¿1026 ≤ 1236? SÍ → Factible
```

**Resumen de la ruta**:
```
Distancia total: 20.62 + 2 + 18.68 = 41.30 unidades
Tiempo total: 1026 unidades
Demanda total: 40 unidades
Tiempo de espera: 825 - 21 = 804 unidades
Tiempo de servicio: 90 + 90 = 180 unidades
Tiempo de viaje: 41.30 unidades
```

**Validación**:
```
✓ Todas las ventanas de tiempo respetadas
✓ Capacidad del vehículo no excedida (40 ≤ 200)
✓ Todos los clientes visitados exactamente una vez
✓ Ruta comienza y termina en el depósito
```

---

## Tipos de Instancias

### Resumen Comparativo

| Tipo | Distribución | Ventanas | Instancias | Horizonte | Servicio | Dificultad |
|------|--------------|----------|------------|-----------|----------|------------|
| C1 | Agrupada | Cortas | 9 | ~1,236 | 90 | Media |
| C2 | Agrupada | Largas | 8 | ~3,390 | 90 | Baja |
| R1 | Aleatoria | Cortas | 12 | ~230 | 10 | Muy Alta |
| R2 | Aleatoria | Largas | 11 | ~1,000 | 10 | Alta |
| RC1 | Mixta | Cortas | 8 | ~240 | 10 | Alta |
| RC2 | Mixta | Largas | 8 | Variable | 10 | Media-Alta |

### Características por Categoría

#### Serie 1 (Ventanas Cortas)

**Características**:
- Horizontes temporales reducidos
- Ventanas de tiempo estrechas
- Mayor número de vehículos necesarios
- Rutas más cortas
- Mayor dificultad computacional

**Objetivos típicos**:
1. Minimizar número de vehículos (prioridad)
2. Minimizar distancia total (secundario)

#### Serie 2 (Ventanas Largas)

**Características**:
- Horizontes temporales amplios
- Ventanas de tiempo flexibles
- Menor número de vehículos necesarios
- Rutas más largas y consolidadas
- Menor dificultad computacional

**Objetivos típicos**:
1. Minimizar distancia total (prioridad)
2. Minimizar número de vehículos (secundario)

---

## Análisis Estadístico

### Estadísticas Generales del Dataset

**Total de instancias**: 56
**Total de nodos**: 56 × 101 = 5,656 nodos
**Total de clientes**: 56 × 100 = 5,600 clientes

### Distribución por Tipo

```
C1:  9 instancias (16.1%)
C2:  8 instancias (14.3%)
R1:  12 instancias (21.4%)
R2:  11 instancias (19.6%)
RC1: 8 instancias (14.3%)
RC2: 8 instancias (14.3%)
```

### Rangos de Valores Típicos

#### Coordenadas Espaciales

| Tipo | X mín | X máx | Y mín | Y máx | Área |
|------|-------|-------|-------|-------|------|
| C | 0 | 95 | 5 | 85 | Amplia |
| R | 2 | 67 | 5 | 77 | Media |
| RC | 0 | 95 | 5 | 85 | Amplia |

#### Demandas

| Tipo | Demanda mín | Demanda máx | Demanda promedio |
|------|-------------|-------------|------------------|
| C | 10 | 50 | ~20 |
| R | 1 | 41 | ~15 |
| RC | 3 | 40 | ~18 |

#### Ventanas de Tiempo

| Tipo | Amplitud mín | Amplitud máx | Amplitud promedio |
|------|--------------|--------------|-------------------|
| C1 | 45 | 69 | ~55 |
| C2 | 160 | 160 | 160 |
| R1 | 10 | 10 | 10 |
| R2 | 57 | 139 | ~100 |
| RC1 | 30 | 30 | 30 |
| RC2 | 30 | 175 | ~90 |

### Capacidad Típica de Vehículos

Aunque no está explícita en los archivos CSV, la capacidad estándar es:

| Tipo | Capacidad |
|------|-----------|
| C1 | 200 |
| C2 | 700 |
| R1 | 200 |
| R2 | 1,000 |
| RC1 | 200 |
| RC2 | 1,000 |

---

## Uso y Aplicaciones

### Aplicaciones del Mundo Real

El VRPTW modela problemas reales en:

1. **Logística y Distribución**
   - Entrega de paquetes (Amazon, FedEx, UPS)
   - Distribución de alimentos perecederos
   - Reparto de medicamentos

2. **Servicios Públicos**
   - Recolección de residuos
   - Transporte escolar
   - Servicios de ambulancia

3. **Servicios a Domicilio**
   - Técnicos de reparación
   - Servicios de limpieza
   - Atención médica domiciliaria

4. **Comercio Electrónico**
   - Última milla (last-mile delivery)
   - Entregas en el mismo día
   - Ventanas de entrega programadas

### Cómo Usar el Dataset

#### 1. Lectura de Datos

**Python (pandas)**:
```python
import pandas as pd

# Leer archivo CSV
df = pd.read_csv('C1/C101.csv')

# Separar depósito y clientes
depot = df.iloc[0]
customers = df.iloc[1:]

# Acceder a datos específicos
depot_x = depot['XCOORD.']
depot_y = depot['YCOORD.']
customer_demands = customers['DEMAND'].values
```

**Python (lectura manual)**:
```python
def read_solomon_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Saltar encabezado
    data_lines = lines[1:]
    
    depot = None
    customers = []
    
    for line in data_lines:
        if line.strip():  # Ignorar líneas vacías
            parts = line.strip().split(',')
            node = {
                'id': int(parts[0]),
                'x': int(parts[1]),
                'y': int(parts[2]),
                'demand': int(parts[3]),
                'ready_time': int(parts[4]),
                'due_date': int(parts[5]),
                'service_time': int(parts[6])
            }
            
            if node['id'] == 1:
                depot = node
            else:
                customers.append(node)
    
    return depot, customers
```

#### 2. Cálculo de Distancias

```python
import numpy as np

def euclidean_distance(node1, node2):
    """Calcula distancia euclidiana entre dos nodos"""
    dx = node1['x'] - node2['x']
    dy = node1['y'] - node2['y']
    return np.sqrt(dx**2 + dy**2)

def create_distance_matrix(depot, customers):
    """Crea matriz de distancias entre todos los nodos"""
    all_nodes = [depot] + customers
    n = len(all_nodes)
    
    dist_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = euclidean_distance(
                    all_nodes[i], 
                    all_nodes[j]
                )
    
    return dist_matrix
```

#### 3. Validación de Soluciones

```python
def validate_route(route, depot, customers, distance_matrix, capacity):
    """
    Valida si una ruta es factible
    
    Args:
        route: Lista de IDs de clientes en orden de visita
        depot: Diccionario con datos del depósito
        customers: Lista de diccionarios con datos de clientes
        distance_matrix: Matriz de distancias
        capacity: Capacidad del vehículo
    
    Returns:
        (is_valid, violations): Tupla con validez y lista de violaciones
    """
    violations = []
    current_time = 0
    current_load = 0
    current_node = depot
    
    for customer_id in route:
        customer = customers[customer_id - 2]  # Ajustar índice
        
        # Calcular tiempo de viaje
        travel_time = distance_matrix[current_node['id']][customer['id']]
        arrival_time = current_time + travel_time
        
        # Verificar ventana de tiempo
        if arrival_time > customer['due_date']:
            violations.append(f"Cliente {customer_id}: llegada tardía")
        
        # Calcular tiempo de inicio de servicio (esperar si es necesario)
        service_start = max(arrival_time, customer['ready_time'])
        
        # Actualizar tiempo actual
        current_time = service_start + customer['service_time']
        
        # Verificar capacidad
        current_load += customer['demand']
        if current_load > capacity:
            violations.append(f"Capacidad excedida: {current_load} > {capacity}")
        
        current_node = customer
    
    # Verificar regreso al depósito
    travel_time = distance_matrix[current_node['id']][depot['id']]
    arrival_time = current_time + travel_time
    
    if arrival_time > depot['due_date']:
        violations.append("Regreso tardío al depósito")
    
    is_valid = len(violations) == 0
    return is_valid, violations
```

#### 4. Visualización

```python
import matplotlib.pyplot as plt

def plot_instance(depot, customers, routes=None):
    """
    Visualiza una instancia del VRPTW
    
    Args:
        depot: Diccionario con datos del depósito
        customers: Lista de diccionarios con datos de clientes
        routes: Lista de rutas (opcional)
    """
    plt.figure(figsize=(12, 10))
    
    # Plotear depósito
    plt.scatter(depot['x'], depot['y'], c='red', s=200, 
                marker='s', label='Depósito', zorder=3)
    
    # Plotear clientes
    customer_x = [c['x'] for c in customers]
    customer_y = [c['y'] for c in customers]
    plt.scatter(customer_x, customer_y, c='blue', s=50, 
                label='Clientes', zorder=2)
    
    # Plotear rutas si se proporcionan
    if routes:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(routes)))
        
        for route, color in zip(routes, colors):
            route_x = [depot['x']]
            route_y = [depot['y']]
            
            for customer_id in route:
                customer = customers[customer_id - 2]
                route_x.append(customer['x'])
                route_y.append(customer['y'])
            
            route_x.append(depot['x'])
            route_y.append(depot['y'])
            
            plt.plot(route_x, route_y, c=color, linewidth=2, 
                    alpha=0.7, zorder=1)
    
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Instancia VRPTW')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()
```

### Métricas de Evaluación

Las soluciones al VRPTW se evalúan típicamente con:

1. **Número de vehículos** (m)
   - Objetivo primario en instancias con ventanas cortas
   - Minimizar: m

2. **Distancia total** (D)
   - Objetivo primario en instancias con ventanas largas
   - Minimizar: ∑(distancias de todas las rutas)

3. **Función objetivo jerárquica**:
   ```
   f(solución) = α × m + β × D
   
   Donde:
   - α >> β (priorizar número de vehículos)
   - O evaluar lexicográficamente: primero m, luego D
   ```

4. **Tiempo computacional**
   - Tiempo requerido para encontrar la solución
   - Importante para aplicaciones en tiempo real

### Algoritmos Comunes

Los algoritmos más utilizados para resolver el VRPTW incluyen:

#### Métodos Exactos
- **Branch and Bound**
- **Branch and Cut**
- **Programación Dinámica**
- Limitados a instancias pequeñas (<50 clientes)

#### Heurísticas Constructivas
- **Nearest Neighbor**
- **Savings Algorithm (Clarke-Wright)**
- **Insertion Heuristics**
- Rápidas pero soluciones subóptimas

#### Metaheurísticas
- **Genetic Algorithms (GA)**
- **Simulated Annealing (SA)**
- **Tabu Search (TS)**
- **Ant Colony Optimization (ACO)**
- **Variable Neighborhood Search (VNS)**
- **Large Neighborhood Search (LNS)**
- Equilibrio entre calidad y tiempo

#### Métodos Híbridos
- Combinación de varios enfoques
- Estado del arte en competencias

---

## Referencias

### Publicación Original

**Solomon, M. M. (1987)**
"Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints"
*Operations Research*, 35(2), 254-265.

### Recursos Adicionales

1. **SINTEF - Vehicle Routing Problem Repository**
   - URL: https://www.sintef.no/projectweb/top/vrptw/
   - Contiene mejores soluciones conocidas (Best Known Solutions - BKS)

2. **VRP-REP: Vehicle Routing Problem Repository**
   - URL: http://www.vrp-rep.org/
   - Repositorio estandarizado de instancias VRP

3. **Kaggle Dataset**
   - URL: https://www.kaggle.com/datasets/masud7866/solomon-vrptw-benchmark
   - Versión en CSV del dataset original

### Mejores Soluciones Conocidas (BKS)

Las mejores soluciones conocidas para las instancias Solomon están documentadas y actualizadas regularmente. Algunos ejemplos:

| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| C101 | 10 | 828.94 | 1997 | Rochat & Taillard |
| C201 | 3 | 591.56 | 1999 | Mester & Bräysy |
| R101 | 19 | 1650.80 | 2003 | Bent & Van Hentenryck |
| R201 | 4 | 1252.37 | 1999 | Mester & Bräysy |
| RC101 | 14 | 1696.95 | 2003 | Bent & Van Hentenryck |
| RC201 | 4 | 1406.94 | 1999 | Mester & Bräysy |

### Citas Recomendadas

Si utilizas este dataset en investigación, cita:

```bibtex
@article{solomon1987algorithms,
  title={Algorithms for the vehicle routing and scheduling problems with time window constraints},
  author={Solomon, Marius M},
  journal={Operations research},
  volume={35},
  number={2},
  pages={254--265},
  year={1987},
  publisher={INFORMS}
}
```

---

## Apéndices

### Apéndice A: Glosario de Términos

- **VRPTW**: Vehicle Routing Problem with Time Windows
- **Depósito**: Punto de inicio y fin de todas las rutas
- **Cliente**: Nodo que requiere servicio
- **Ventana de tiempo**: Intervalo [ready_time, due_date] para atender un cliente
- **Capacidad**: Máxima carga que puede transportar un vehículo
- **Ruta**: Secuencia de clientes visitados por un vehículo
- **Solución**: Conjunto de rutas que atienden a todos los clientes
- **Factibilidad**: Una solución es factible si respeta todas las restricciones
- **Optimalidad**: Una solución es óptima si minimiza la función objetivo

### Apéndice B: Preguntas Frecuentes

**P: ¿Cuál es la diferencia entre READY TIME y DUE DATE?**
R: READY TIME es el momento más temprano para iniciar el servicio (si llegas antes, esperas). DUE DATE es el momento más tardío (si llegas después, la solución es inválida).

**P: ¿Qué pasa si un vehículo llega antes del READY TIME?**
R: El vehículo debe esperar hasta el READY TIME para iniciar el servicio. El tiempo de espera no se penaliza, pero aumenta el tiempo total de la ruta.

**P: ¿La capacidad del vehículo está en los archivos CSV?**
R: No, la capacidad es un parámetro externo que debe consultarse en la documentación original o asumirse según estándares (típicamente 200 para serie 1, 1000 para serie 2 en tipos R y RC).

**P: ¿Cómo se calcula la distancia entre dos nodos?**
R: Se usa la distancia euclidiana: d = √[(x₂-x₁)² + (y₂-y₁)²]

**P: ¿Qué instancias son más difíciles de resolver?**
R: Las instancias R1 son las más difíciles debido a la distribución aleatoria de clientes y ventanas de tiempo muy estrechas.

**P: ¿Puedo modificar los datos del dataset?**
R: Sí, pero si lo haces para investigación, debes documentar claramente las modificaciones. Para comparaciones con otros trabajos, usa los datos originales.

### Apéndice C: Checklist de Validación

Al implementar un algoritmo para VRPTW, verifica:

- [ ] Todos los clientes son visitados exactamente una vez
- [ ] Todas las rutas comienzan y terminan en el depósito
- [ ] La capacidad del vehículo no se excede en ninguna ruta
- [ ] Todas las ventanas de tiempo se respetan
- [ ] Los tiempos de servicio se incluyen en los cálculos
- [ ] Las distancias se calculan correctamente (euclidiana)
- [ ] El tiempo de llegada al depósito no excede su DUE DATE
- [ ] Los tiempos de espera se contabilizan correctamente

---

## Conclusión

El dataset Solomon VRPTW es un recurso fundamental para la investigación en optimización combinatoria y logística. Su estructura bien definida, variedad de instancias y amplia adopción en la comunidad científica lo convierten en el benchmark estándar para evaluar algoritmos de ruteo de vehículos con ventanas de tiempo.

Esta documentación proporciona una base completa para comprender, utilizar y trabajar con el dataset, desde los conceptos básicos hasta implementaciones avanzadas.

---

**Documento generado**: Diciembre 2025
**Versión**: 1.0
**Autor**: Documentación técnica del dataset Solomon VRPTW
**Licencia**: Uso académico y de investigación
