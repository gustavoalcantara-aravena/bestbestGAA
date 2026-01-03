# CONTEXT.md - Solomon VRPTW Dataset

## Resumen Ejecutivo

Este documento proporciona un contexto completo del **Solomon VRPTW Benchmark Dataset**, un conjunto de datos estándar ampliamente utilizado en investigación de optimización combinatoria y logística desde 1987. El dataset contiene 56 instancias de prueba para el **Vehicle Routing Problem with Time Windows (VRPTW)**, organizadas en 6 familias que representan diferentes escenarios de complejidad.

---

## 1. Descripción General del Dataset

### 1.1 Información Básica

| Atributo | Valor |
|----------|-------|
| **Nombre** | Solomon VRPTW Benchmark Dataset |
| **Autor Original** | Marius M. Solomon (1987) |
| **Total de Instancias** | 56 |
| **Clientes por Instancia** | 100 + 1 depósito = 101 nodos |
| **Fuente de Descarga** | https://www.kaggle.com/datasets/masud7866/solomon-vrptw-benchmark |
| **Formato** | CSV |
| **Publicación Original** | Operations Research, 35(2), 254-265 (1987) |

### 1.2 Problema que Modela

El **VRPTW (Vehicle Routing Problem with Time Windows)** consiste en:

**Objetivo**: Diseñar rutas óptimas para una flota de vehículos que deben:
- Partir desde un depósito central
- Visitar un conjunto de clientes geográficamente dispersos
- Satisfacer la demanda de cada cliente
- Respetar las ventanas de tiempo de cada cliente (restricción crítica)
- Regresar al depósito
- Minimizar el número de vehículos y/o la distancia total recorrida

**Restricciones Principales**:
1. Capacidad del vehículo no puede excederse
2. Ventanas de tiempo [READY TIME, DUE DATE] deben respetarse estrictamente
3. Cada cliente debe ser visitado exactamente una vez
4. Todas las rutas comienzan y terminan en el depósito
5. Tiempo de servicio debe completarse en cada cliente

**Complejidad**: Problema NP-hard (no existe algoritmo polinomial conocido)

---

## 2. Estructura del Dataset

### 2.1 Organización de Directorios

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
├── DOCUMENTACION_DATASET.md     # Documentación completa del dataset
├── CARACTERISTICAS_FAMILIAS.md # Características detalladas por familia
├── ANALISIS_ESTADISTICO.md     # Análisis estadístico exhaustivo
├── GUIA_IMPLEMENTACION.md       # Guía práctica de implementación
├── FUENTE_DESCARGA.txt          # URL de descarga
├── Solomon VRPTW benchmark.pdf  # Documentación original
└── archive.zip                  # Archivo comprimido del dataset
```

### 2.2 Formato de Archivos CSV

Cada archivo CSV contiene **103 líneas**:
- **Línea 1**: Encabezado con nombres de columnas
- **Líneas 2-102**: Datos de 101 nodos (1 depósito + 100 clientes)
- **Línea 103**: Línea vacía

**Estructura de Columnas**:

| Columna | Nombre | Tipo | Descripción | Rango Típico |
|---------|--------|------|-------------|--------------|
| 1 | CUST NO. | Entero | Número identificador del nodo (1=depósito, 2-101=clientes) | 1-101 |
| 2 | XCOORD. | Entero | Coordenada X en el plano euclidiano | 0-100 |
| 3 | YCOORD. | Entero | Coordenada Y en el plano euclidiano | 0-100 |
| 4 | DEMAND | Entero | Demanda del cliente en unidades (0 para depósito) | 0-50 |
| 5 | READY TIME | Entero | Inicio de la ventana de tiempo | 0-3000+ |
| 6 | DUE DATE | Entero | Fin de la ventana de tiempo (límite estricto) | 0-3500+ |
| 7 | SERVICE TIME | Entero | Tiempo requerido para atender al cliente | 0-90 |

**Ejemplo (C101.csv)**:
```csv
CUST NO.,XCOORD.,YCOORD.,DEMAND,READY TIME,DUE DATE,SERVICE TIME
1,40,50,0,0,1236,0
2,45,68,10,912,967,90
3,45,70,30,825,870,90
```

---

## 3. Familias de Instancias

### 3.1 Nomenclatura

**Formato**: `[TIPO][SERIE][NÚMERO].csv`

- **TIPO**: 
  - `C` = Clustered (Agrupados)
  - `R` = Random (Aleatorios)
  - `RC` = Random-Clustered (Mixtos)

- **SERIE**:
  - `1` = Ventanas de tiempo cortas (short time windows)
  - `2` = Ventanas de tiempo largas (long time windows)

- **NÚMERO**: Identificador de la instancia específica (01-12)

### 3.2 Matriz Comparativa de Familias

| Familia | Distribución Espacial | Ventanas | Instancias | Horizonte Temporal | Servicio | Capacidad | Dificultad |
|---------|----------------------|----------|------------|-------------------|----------|-----------|------------|
| **C1** | Agrupada (4 clusters) | Cortas | 9 | 1,236 | 90 | 200 | Media-Alta |
| **C2** | Agrupada (4 clusters) | Largas | 8 | 3,390 | 90 | 700 | Baja |
| **R1** | Aleatoria uniforme | Cortas | 12 | 230 | 10 | 200 | **Muy Alta** |
| **R2** | Aleatoria uniforme | Largas | 11 | 1,000 | 10 | 1,000 | Media |
| **RC1** | Semi-agrupada (2-3 clusters) | Cortas | 8 | 240 | 10 | 200 | Alta |
| **RC2** | Semi-agrupada (2-3 clusters) | Largas | 8 | ~1,500 | 10 | 1,000 | Media-Alta |

### 3.3 Familia C1: Clientes Agrupados, Ventanas Cortas

**Características**:
- **Distribución**: 4 clusters geográficos bien definidos (NE, NW, SE, SW)
- **Ventanas**: 45-69 unidades de amplitud (promedio: 55)
- **Tiempo de servicio**: 90 unidades (164% de la ventana → muy ajustado)
- **Capacidad**: 200 unidades
- **Vehículos requeridos**: 10 típicamente
- **Objetivo primario**: Minimizar número de vehículos

**Ejemplo de BKS**: C101 → 10 vehículos, 828.94 distancia

**Casos de uso**: Entrega urbana con zonas definidas, servicios técnicos con citas programadas

### 3.4 Familia C2: Clientes Agrupados, Ventanas Largas

**Características**:
- **Distribución**: Idéntica a C1 (4 clusters)
- **Ventanas**: 160 unidades constantes (+190% vs C1)
- **Tiempo de servicio**: 90 unidades (56% de la ventana → holgado)
- **Capacidad**: 700 unidades (+250% vs C1)
- **Vehículos requeridos**: 3-4 típicamente (-70% vs C1)
- **Objetivo primario**: Minimizar distancia total

**Ejemplo de BKS**: C201 → 3 vehículos, 591.56 distancia

**Casos de uso**: Distribución mayorista con entregas flexibles, planificación semanal

### 3.5 Familia R1: Clientes Aleatorios, Ventanas Cortas

**Características**:
- **Distribución**: Uniforme aleatoria (sin clusters)
- **Ventanas**: 10 unidades constantes (extremadamente estrechas)
- **Tiempo de servicio**: 10 unidades (100% de la ventana → sin margen)
- **Horizonte**: 230 unidades (muy corto)
- **Capacidad**: 200 unidades
- **Vehículos requeridos**: 9-19 (alta variabilidad)
- **Dificultad**: **MUY ALTA** (la más difícil del dataset)

**Ejemplo de BKS**: R101 → 19 vehículos, 1650.80 distancia

**Casos de uso**: Servicios médicos a domicilio con citas exactas, entregas urgentes

### 3.6 Familia R2: Clientes Aleatorios, Ventanas Largas

**Características**:
- **Distribución**: Idéntica a R1 (uniforme aleatoria)
- **Ventanas**: 57-139 unidades (promedio: 100)
- **Tiempo de servicio**: 10 unidades (10% de la ventana → muy holgado)
- **Horizonte**: 1,000 unidades (+335% vs R1)
- **Capacidad**: 1,000 unidades (+400% vs R1)
- **Vehículos requeridos**: 2-4 típicamente (-80% vs R1)

**Ejemplo de BKS**: R201 → 4 vehículos, 1252.37 distancia

**Casos de uso**: Distribución rural con entregas flexibles, logística de largo plazo

### 3.7 Familia RC1: Clientes Mixtos, Ventanas Cortas

**Características**:
- **Distribución**: Semi-agrupada (60% en clusters, 40% dispersos)
- **Ventanas**: 30 unidades constantes
- **Tiempo de servicio**: 10 unidades (33% de la ventana → moderado)
- **Horizonte**: 240 unidades
- **Capacidad**: 200 unidades
- **Vehículos requeridos**: 10-14 típicamente

**Ejemplo de BKS**: RC101 → 14 vehículos, 1696.95 distancia

**Casos de uso**: Distribución urbana-suburbana mixta, áreas metropolitanas

### 3.8 Familia RC2: Clientes Mixtos, Ventanas Largas

**Características**:
- **Distribución**: Idéntica a RC1 (semi-agrupada)
- **Ventanas**: 30-175 unidades (promedio: 90)
- **Tiempo de servicio**: 10 unidades (11% de la ventana → holgado)
- **Capacidad**: 1,000 unidades
- **Vehículos requeridos**: 3-4 típicamente

**Ejemplo de BKS**: RC201 → 4 vehículos, 1406.94 distancia

**Casos de uso**: Logística mixta con flexibilidad temporal

---

## 4. Estadísticas del Dataset

### 4.1 Estadísticas Globales

| Métrica | Valor |
|---------|-------|
| Total de instancias | 56 |
| Total de nodos | 5,656 (56 × 101) |
| Total de clientes | 5,600 (56 × 100) |
| Tipos de instancias | 6 familias |
| Rango de coordenadas X | [0, 95] |
| Rango de coordenadas Y | [5, 85] |
| Rango de demandas | [1, 50] unidades |
| Rango de horizontes temporales | [230, 3,390] unidades |

### 4.2 Distribución de Instancias

```
C1:  9 instancias (16.1%)
C2:  8 instancias (14.3%)
R1:  12 instancias (21.4%)
R2:  11 instancias (19.6%)
RC1: 8 instancias (14.3%)
RC2: 8 instancias (14.3%)
```

### 4.3 Estadísticas de Demandas por Tipo

| Tipo | Demanda Mín | Demanda Máx | Demanda Promedio | Desv. Estándar | CV |
|------|-------------|-------------|------------------|----------------|-----|
| C1/C2 | 10 | 50 | 20.0 | 10.5 | 0.53 |
| R1/R2 | 1 | 41 | 15.2 | 9.8 | 0.64 |
| RC1/RC2 | 3 | 40 | 17.8 | 10.2 | 0.57 |

### 4.4 Análisis de Ventanas de Tiempo

| Tipo | Amplitud de Ventanas | Tiempo de Servicio | Tasa de Ocupación | Margen |
|------|---------------------|-------------------|-------------------|---------|
| C1 | 45-69 (prom: 55) | 90 | 164% | Negativo (requiere espera) |
| C2 | 160 (constante) | 90 | 56% | 70 unidades |
| R1 | 10 (constante) | 10 | 100% | 0 unidades (sin margen) |
| R2 | 57-139 (prom: 100) | 10 | 10% | 90 unidades |
| RC1 | 30 (constante) | 10 | 33% | 20 unidades |
| RC2 | 30-175 (prom: 90) | 10 | 11% | 80 unidades |

### 4.5 Relación Demanda-Capacidad

| Tipo | Capacidad Vehículo | Demanda Total | Clientes/Vehículo (teórico) | Utilización |
|------|-------------------|---------------|----------------------------|-------------|
| C1 | 200 | ~2,000 | 10 | 100% (muy ajustado) |
| C2 | 700 | ~2,000 | 35 | 29% (holgado) |
| R1 | 200 | ~1,500 | 13 | 75% (moderado) |
| R2 | 1,000 | ~1,500 | 67 | 15% (muy holgado) |
| RC1 | 200 | ~1,800 | 11 | 90% (ajustado) |
| RC2 | 1,000 | ~1,800 | 56 | 18% (holgado) |

---

## 5. Mejores Soluciones Conocidas (BKS)

### 5.1 Resumen de BKS por Familia

#### Familia C1 (todas requieren 10 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| C101-C109 | 10 | ~828 | 1997-2003 | Rochat & Taillard / Bent & Van Hentenryck |

#### Familia C2 (todas requieren 3 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| C201-C208 | 3 | 588-591 | 1999-2003 | Mester & Bräysy / Bent & Van Hentenryck |

#### Familia R1 (9-19 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| R101 | 19 | 1650.80 | 2003 | Bent & Van Hentenryck |
| R104 | 9 | 1007.31 | 2003 | Bent & Van Hentenryck |
| R108 | 9 | 960.88 | 2003 | Bent & Van Hentenryck |

#### Familia R2 (2-4 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| R204 | 2 | 825.52 | 2003 | Bent & Van Hentenryck |
| R207 | 2 | 890.61 | 2003 | Bent & Van Hentenryck |
| R208 | 2 | 726.82 | 2003 | Bent & Van Hentenryck |

#### Familia RC1 (10-14 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| RC101 | 14 | 1696.95 | 2003 | Bent & Van Hentenryck |
| RC104 | 10 | 1135.48 | 2003 | Bent & Van Hentenryck |

#### Familia RC2 (3-4 vehículos)
| Instancia | Vehículos | Distancia | Año | Método |
|-----------|-----------|-----------|------|--------|
| RC201 | 4 | 1406.94 | 1999 | Mester & Bräysy |
| RC204 | 3 | 798.46 | 2003 | Bent & Van Hentenryck |

### 5.2 Evolución Temporal de BKS

```
1987: Solomon publica dataset con soluciones iniciales
1997: Rochat & Taillard mejoran significativamente tipo C
1999: Mester & Bräysy establecen BKS para serie 2
2003: Bent & Van Hentenryck dominan con Large Neighborhood Search (LNS)
2010+: Mejoras marginales (<1%) con metaheurísticas híbridas
```

---

## 6. Complejidad Computacional

### 6.1 Ranking de Dificultad

| Posición | Familia | Dificultad | Factores Clave |
|----------|---------|-----------|----------------|
| 1 | **R1** | Muy Alta | Ventanas extremadamente estrechas + distribución aleatoria |
| 2 | **RC1** | Alta | Ventanas estrechas + distribución mixta |
| 3 | **C1** | Media-Alta | Ventanas estrechas + capacidad ajustada |
| 4 | **RC2** | Media-Alta | Distribución mixta |
| 5 | **R2** | Media | Distribución aleatoria |
| 6 | **C2** | Baja | Ventanas amplias + clusters definidos |

### 6.2 Tiempos de Resolución Típicos

| Familia | Heurística Simple | Metaheurística | Método Exacto |
|---------|------------------|----------------|---------------|
| C1 | 1-5 segundos | 10-60 segundos | Horas |
| C2 | 0.5-2 segundos | 5-30 segundos | Factible |
| R1 | 5-30 segundos | 30-300 segundos | Intratable (>24h) |
| R2 | 2-10 segundos | 10-60 segundos | Difícil |
| RC1 | 3-15 segundos | 15-120 segundos | Muy difícil |
| RC2 | 2-8 segundos | 10-80 segundos | Difícil |

### 6.3 Espacio de Búsqueda

Para n=100 clientes:
- **Número de soluciones posibles**: ≈ 100! ≈ 9.3 × 10^157
- **Número de rutas posibles**: 2^100 ≈ 1.27 × 10^30

---

## 7. Algoritmos y Estrategias de Solución

### 7.1 Algoritmos Comunes

#### Métodos Exactos
- Branch and Bound
- Branch and Cut
- Programación Dinámica
- **Limitación**: Solo para instancias pequeñas (<50 clientes)

#### Heurísticas Constructivas
- Nearest Neighbor (Vecino más cercano)
- Clarke-Wright Savings Algorithm
- Insertion Heuristics
- **Ventaja**: Rápidas
- **Desventaja**: Soluciones subóptimas

#### Metaheurísticas
- Genetic Algorithms (GA)
- Simulated Annealing (SA)
- Tabu Search (TS)
- Ant Colony Optimization (ACO)
- Variable Neighborhood Search (VNS)
- Large Neighborhood Search (LNS)
- Adaptive Large Neighborhood Search (ALNS)
- **Ventaja**: Equilibrio entre calidad y tiempo

#### Métodos Híbridos
- Combinación de varios enfoques
- Estado del arte en competencias

### 7.2 Estrategias Recomendadas por Familia

#### Para C1/C2 (Agrupadas)
1. Identificar clusters (K-means, k=4)
2. Asignar vehículos por cluster
3. Ruteo intra-cluster (TSP)
4. Optimización local (2-opt, 3-opt)

#### Para R1/R2 (Aleatorias)
1. Construcción temporal (ordenar por ready_time)
2. Sweep algorithm (barrido angular)
3. Minimización de esperas
4. Large Neighborhood Search

#### Para RC1/RC2 (Mixtas)
1. Clustering parcial (k=2-3)
2. Identificar clientes satélite
3. Construcción híbrida
4. Adaptive Large Neighborhood Search

### 7.3 Función Objetivo

**Jerárquica** (típica para serie 1):
```
f(solución) = 1000 × num_vehículos + distancia_total
```

**Ponderada** (típica para serie 2):
```
f(solución) = distancia_total + 100 × num_vehículos
```

---

## 8. Aplicaciones del Mundo Real

### 8.1 Sectores de Aplicación

#### Logística y Distribución
- Entrega de paquetes (Amazon, FedEx, UPS)
- Distribución de alimentos perecederos
- Reparto de medicamentos
- Última milla (last-mile delivery)

#### Servicios Públicos
- Recolección de residuos
- Transporte escolar
- Servicios de ambulancia
- Mantenimiento de infraestructura

#### Servicios a Domicilio
- Técnicos de reparación
- Servicios de limpieza
- Atención médica domiciliaria
- Servicios de mensajería

#### Comercio Electrónico
- Entregas en el mismo día
- Ventanas de entrega programadas
- Entregas express

### 8.2 Mapeo Familia-Aplicación

| Familia | Escenario Real |
|---------|----------------|
| C1 | Entrega urbana con zonas definidas, servicios técnicos con citas de 2-3 horas |
| C2 | Distribución mayorista con entregas flexibles de 1-2 días |
| R1 | Servicios médicos urgentes con slots de 15-30 minutos |
| R2 | Distribución rural con entregas flexibles de varios días |
| RC1 | Distribución urbana-suburbana mixta con ventanas moderadas |
| RC2 | Logística mixta con planificación flexible |

---

## 9. Documentación Disponible

### 9.1 Archivos de Documentación

1. **DOCUMENTACION_DATASET.md** (1,064 líneas)
   - Introducción completa al VRPTW
   - Estructura detallada del dataset
   - Formato de archivos CSV
   - Ejemplos detallados con cálculos
   - Guía de uso con código Python

2. **CARACTERISTICAS_FAMILIAS.md** (1,513 líneas)
   - Análisis exhaustivo de cada familia
   - Características geográficas y temporales
   - Estadísticas espaciales
   - Estrategias de solución recomendadas
   - Casos de uso real por familia

3. **ANALISIS_ESTADISTICO.md** (923 líneas)
   - Estadísticas descriptivas completas
   - Análisis de distribución espacial
   - Análisis de demandas y ventanas de tiempo
   - Correlaciones y patrones
   - Benchmarks y BKS completos

4. **GUIA_IMPLEMENTACION.md** (1,209 líneas)
   - Configuración del entorno
   - Clases y estructuras de datos
   - Implementación de algoritmos básicos
   - Validación de soluciones
   - Visualización con matplotlib
   - Ejemplos completos de código

5. **Solomon VRPTW benchmark.pdf**
   - Publicación original de Solomon (1987)
   - Descripción teórica del problema
   - Metodología de generación de instancias

### 9.2 Contenido de los Archivos de Datos

Cada archivo CSV (56 archivos totales) contiene:
- 1 depósito (CUST NO. = 1)
- 100 clientes (CUST NO. = 2-101)
- 7 columnas de datos
- Formato estandarizado y consistente

---

## 10. Guía de Inicio Rápido

### 10.1 Lectura de Datos (Python)

```python
import pandas as pd
import numpy as np

# Leer instancia
df = pd.read_csv('C1/C101.csv')

# Separar depósito y clientes
depot = df.iloc[0]
customers = df.iloc[1:]

# Calcular matriz de distancias
def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

# Acceder a datos
depot_x = depot['XCOORD.']
depot_y = depot['YCOORD.']
customer_demands = customers['DEMAND'].values
ready_times = customers['READY TIME'].values
due_dates = customers['DUE DATE'].values
```

### 10.2 Validación de Solución

Para validar una solución, verificar:
1. ✓ Todos los clientes visitados exactamente una vez
2. ✓ Capacidad del vehículo no excedida en ninguna ruta
3. ✓ Ventanas de tiempo respetadas (arrival_time ≤ due_date)
4. ✓ Todas las rutas comienzan y terminan en el depósito
5. ✓ Regreso al depósito dentro del horizonte temporal

### 10.3 Métricas de Evaluación

```python
# Calcular métricas
num_vehicles = len(routes)
total_distance = sum(route.distance for route in routes)

# Función objetivo (serie 1)
objective_value = 1000 * num_vehicles + total_distance

# Función objetivo (serie 2)
objective_value = total_distance + 100 * num_vehicles
```

### 10.4 Instancias Recomendadas para Pruebas

| Propósito | Instancias Recomendadas |
|-----------|------------------------|
| Prueba inicial | C101, R101, RC101 |
| Validación de algoritmo | C201, R201, RC201 |
| Benchmark completo | Todas las instancias de una familia |
| Comparación con literatura | Reportar BKS y gap |

---

## 11. Referencias y Recursos

### 11.1 Publicación Original

**Solomon, M. M. (1987)**  
"Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints"  
*Operations Research*, 35(2), 254-265.

### 11.2 Repositorios de Referencia

1. **SINTEF - Vehicle Routing Problem Repository**
   - URL: https://www.sintef.no/projectweb/top/vrptw/
   - Contiene BKS actualizados

2. **VRP-REP: Vehicle Routing Problem Repository**
   - URL: http://www.vrp-rep.org/
   - Repositorio estandarizado de instancias VRP

3. **Kaggle Dataset**
   - URL: https://www.kaggle.com/datasets/masud7866/solomon-vrptw-benchmark
   - Versión en CSV del dataset original

### 11.3 Cita Recomendada

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

## 12. Notas Importantes

### 12.1 Consideraciones Clave

1. **Ventanas de Tiempo**: Son restricciones DURAS (no pueden violarse)
2. **Distancias**: Se calculan con distancia euclidiana
3. **Velocidad**: Se asume 1 unidad de distancia = 1 unidad de tiempo
4. **Capacidad**: Varía según el tipo de instancia (200, 700, o 1000)
5. **Depósito**: Siempre tiene ID=1, demanda=0, service_time=0

### 12.2 Errores Comunes

- ❌ Confundir READY TIME (inicio) con DUE DATE (fin)
- ❌ No considerar tiempo de espera cuando se llega antes del READY TIME
- ❌ Olvidar validar el regreso al depósito
- ❌ No verificar capacidad acumulada en la ruta
- ❌ Usar capacidad incorrecta para el tipo de instancia

### 12.3 Mejores Prácticas

- ✓ Siempre validar soluciones antes de reportar resultados
- ✓ Reportar tanto número de vehículos como distancia total
- ✓ Comparar con BKS publicados
- ✓ Probar en múltiples familias para generalización
- ✓ Documentar parámetros del algoritmo usado

---

## 13. Resumen de Archivos del Dataset

| Archivo | Tipo | Tamaño | Descripción |
|---------|------|--------|-------------|
| C1/*.csv | Datos | 9 archivos | Instancias agrupadas, ventanas cortas |
| C2/*.csv | Datos | 8 archivos | Instancias agrupadas, ventanas largas |
| R1/*.csv | Datos | 12 archivos | Instancias aleatorias, ventanas cortas |
| R2/*.csv | Datos | 11 archivos | Instancias aleatorias, ventanas largas |
| RC1/*.csv | Datos | 8 archivos | Instancias mixtas, ventanas cortas |
| RC2/*.csv | Datos | 8 archivos | Instancias mixtas, ventanas largas |
| DOCUMENTACION_DATASET.md | Documentación | 32.9 KB | Documentación completa |
| CARACTERISTICAS_FAMILIAS.md | Documentación | 39.2 KB | Características por familia |
| ANALISIS_ESTADISTICO.md | Documentación | 25.8 KB | Análisis estadístico |
| GUIA_IMPLEMENTACION.md | Documentación | 40.4 KB | Guía de implementación |
| FUENTE_DESCARGA.txt | Referencia | 83 bytes | URL de descarga |
| Solomon VRPTW benchmark.pdf | Documentación | 384 KB | Publicación original |
| archive.zip | Archivo | 64.2 KB | Dataset comprimido |

**Total**: 56 archivos CSV de datos + 7 archivos de documentación

---

## 14. Conclusión

El **Solomon VRPTW Benchmark Dataset** es el estándar de facto para evaluar algoritmos de ruteo de vehículos con ventanas de tiempo. Su diseño cuidadoso proporciona:

- **Diversidad**: 6 familias con características distintas
- **Escalabilidad**: 100 clientes por instancia (tamaño realista)
- **Complejidad**: Desde instancias fáciles (C2) hasta muy difíciles (R1)
- **Validación**: BKS bien documentados para comparación
- **Aplicabilidad**: Modela escenarios reales de logística

Este dataset ha sido utilizado en miles de publicaciones científicas desde 1987 y continúa siendo relevante para la investigación en optimización combinatoria, inteligencia artificial, y logística.

---

**Documento generado**: Diciembre 2024  
**Versión**: 1.0  
**Fuente**: Solomon VRPTW Benchmark Dataset  
**Autor del contexto**: Análisis exhaustivo de documentación y datos disponibles
