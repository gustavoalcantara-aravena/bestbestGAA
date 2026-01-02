---
title: "Datasets Solomon - 56 Instancias VRPTW"
version: "1.0.0"
created: "2026-01-01"
---

# 5️⃣ DATASETS SOLOMON

**Documento**: Datasets  
**Contenido**: 56 instancias Solomon, ubicación, especificación

---

## Overview: 56 Instancias Estándar

Solomon (1987) definió 56 instancias estándar de VRPTW, distribuidas en 6 familias:

| Familia | Tipo | Instancias | Total |
|---------|------|-----------|-------|
| **C1** | Clustered, Tight | C101-C109 | 9 |
| **C2** | Clustered, Wide | C201-C208 | 8 |
| **R1** | Random, Tight | R101-R112 | 12 |
| **R2** | Random, Wide | R201-R211 | 11 |
| **RC1** | Mixed, Tight | RC101-RC108 | 8 |
| **RC2** | Mixed, Wide | RC201-RC208 | 8 |
| **TOTAL** | - | - | **56** |

---

## Estructura de Directorios Recomendada

```
proyecto/
  datasets/
    C1/
      C101.csv
      C102.csv
      ...
      C109.csv
    C2/
      C201.csv
      ...
      C208.csv
    R1/
      R101.csv
      ...
      R112.csv
    R2/
      R201.csv
      ...
      R211.csv
    RC1/
      RC101.csv
      ...
      RC108.csv
    RC2/
      RC201.csv
      ...
      RC208.csv
    documentation/
      Solomon_README.md
      best_known_solutions.txt
```

---

## Formato de Archivo Solomon (CSV)

### Estructura Estándar

```
VEHICLE
NUMBER     CAPACITY
  K          Q

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
    0       x0        y0          0         0          T            0
    1       x1        y1         q1        a1         b1           s1
    2       x2        y2         q2        a2         b2           s2
    ...
```

### Ejemplo: Solomon R101

```
VEHICLE
NUMBER     CAPACITY
  25         200

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME

    0      35       35          0          0       230           0   
    1      41       49         10        161       171          10   
    2      35       17          7         50        60          10   
    3      55       45         13        116       126          10   
    ...
   100     ...     ...         ...       ...       ...         ...
```

### Interpretación de Columnas

| Columna | Significado | Rango |
|---------|-------------|-------|
| CUST NO. | Identificador cliente | 0 (depósito) a 100 |
| XCOORD | Coordenada X | [0, 100] |
| YCOORD | Coordenada Y | [0, 100] |
| DEMAND | Demanda | [0, Q] |
| READY TIME | Inicio ventana temporal | [0, 230/600] |
| DUE DATE | Fin ventana temporal | [Ready, 230/600] |
| SERVICE TIME | Tiempo servicio | [10] |

---

## Características por Familia

### Familia C1: Clustered + Tight Windows

- **Clientes**: 100 agrupados en ~4 clusters
- **Ventanas**: Estrictas (rango ~50 minutos)
- **K esperado**: 9-11 vehículos
- **Dificultad**: Baja
- **Instancias**: 9 (C101-C109)

**Característica Clave**: Clustering claro facilita ruteo, pero ventanas estrictas limitan flexibilidad

---

### Familia C2: Clustered + Wide Windows

- **Clientes**: 100 agrupados en ~4 clusters
- **Ventanas**: Amplias (rango 240-600 minutos)
- **K esperado**: 3-5 vehículos
- **Dificultad**: Muy baja
- **Instancias**: 8 (C201-C208)

**Característica Clave**: Clustering + ventanas amplias = problema fácil, se optimiza principalmente distancia

---

### Familia R1: Random + Tight Windows

- **Clientes**: 100 distribuidos aleatoriamente
- **Ventanas**: Estrictas (rango ~50 minutos)
- **K esperado**: 12-15 vehículos
- **Dificultad**: Alta
- **Instancias**: 12 (R101-R112)

**Característica Clave**: Sin estructura espacial + ventanas restrictivas = problema muy desafiante

---

### Familia R2: Random + Wide Windows

- **Clientes**: 100 distribuidos aleatoriamente
- **Ventanas**: Amplias (rango 240-600 minutos)
- **K esperado**: 12-14 vehículos
- **Dificultad**: Media-Alta
- **Instancias**: 11 (R201-R211)

**Característica Clave**: Sin estructura + ventanas amplias = moderadamente desafiante

---

### Familia RC1: Mixed + Tight Windows

- **Clientes**: 100 con clustering parcial (~50% clustered)
- **Ventanas**: Estrictas
- **K esperado**: 13-16 vehículos
- **Dificultad**: Alta
- **Instancias**: 8 (RC101-RC108)

**Característica Clave**: Equilibrio entre clustering y aleatoriedad con ventanas estrictas

---

### Familia RC2: Mixed + Wide Windows

- **Clientes**: 100 con clustering parcial
- **Ventanas**: Amplias
- **K esperado**: 11-13 vehículos
- **Dificultad**: Media
- **Instancias**: 8 (RC201-RC208)

**Característica Clave**: Equilibrio natural, complejidad media

---

## Horizonte Temporal

### Tipo 1 (Tight Windows)

- **Duración del día**: 230 minutos (~3.8 horas)
- **Ventanas típicas**: [9:00, 10:00], [10:30, 11:00], etc.
- **Implicación**: Planeación muy restrictiva, imposible servir muchos clientes por ruta

### Tipo 2 (Wide Windows)

- **Duración del día**: 600 minutos (~10 horas)
- **Ventanas típicas**: [0, 600] (todo el día) o rangos amplios
- **Implicación**: Flexibilidad temporal, se optimiza principalmente distancia

---

## Validación de Instancias

Cada instancia debe tener:
- ✅ Exactamente 101 líneas de clientes (0 + 100)
- ✅ Nodo 0 = depósito (demand=0, service=0)
- ✅ Nodos 1-100 = clientes
- ✅ Todas las demandas ≤ Q
- ✅ Todas las ventanas válidas (ready ≤ due)
- ✅ Distancias euclidianas correctas

---

## Mejores Soluciones Conocidas (BKS)

Las soluciones óptimas o mejores conocidas para Solomon están documentadas en literatura:

### Disponibilidad de BKS

**Familia C**:
- C1: K_BKS bien conocido (~10)
- C2: K_BKS bien conocido (~3-4)

**Familia R**:
- R1: K_BKS bien conocido (~12-13)
- R2: K_BKS bien conocido (~12-14)

**Familia RC**:
- RC1: K_BKS bien conocido (~13-14)
- RC2: K_BKS bien conocido (~11-12)

**Nota**: El proyecto debe cargar BKS desde archivo `best_known_solutions.csv` para cálculo de GAP

---

## Carga de Datos en Código

```python
from pathlib import Path
from data_loader import load_solomon_instance

dataset_root = Path("datasets")
families = ["C1", "C2", "R1", "R2", "RC1", "RC2"]

instances = {}
for family in families:
    family_path = dataset_root / family
    instances[family] = []
    
    for csv_file in sorted(family_path.glob("*.csv")):
        instance = load_solomon_instance(csv_file)
        # instance.n_customers = 100
        # instance.K_vehicles_available = 25
        # instance.Q_capacity = 200
        # instance.customers = [Customer(...) for i in range(101)]
        instances[family].append(instance)

# Total: 56 instancias cargadas
print(f"Total instances: {sum(len(v) for v in instances.values())}")
```

---

## Garantía de Compatibilidad 100%

El proyecto VRPTW-GRASP es **100% compatible** con datasets Solomon:

✅ Formato de entrada: CSV estándar Solomon  
✅ Parámetros: q_i, [a_i, b_i], s_i, (x_i, y_i)  
✅ Número de instancias: 56 exactas  
✅ Clientes por instancia: 100  
✅ Modelo matemático: Idéntico para todas las familias  
✅ Función fitness: Jerárquica (K primario, D secundario)  
✅ Métricas: %GAP canónico  

---

## Fuentes de Descarga

**Oficial (Solomon)**:  
http://web.cba.neu.edu/~msolomon/problems.htm

**Espejo Alternativo (SINTEF)**:  
http://www.sintef.no/projectweb/top/vrptw/

---

## Resumen Estadístico

| Métrica | Valor |
|---------|-------|
| **Total instancias** | 56 |
| **Clientes por instancia** | 100 |
| **Clientes totales** | 5,600 |
| **Vehículos típicos** | 3-16 |
| **Horizonte temporal** | 230 o 600 min |
| **Capacidad estándar** | 200 unidades |

---

**Siguiente documento**: [06-experimentos-plan.md](06-experimentos-plan.md)  
**Volver a**: [INDEX.md](INDEX.md)
