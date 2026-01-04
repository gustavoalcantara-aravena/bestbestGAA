# Características del Dataset Solomon VRPTW

## Introducción

Especificación detallada de las **56 instancias Solomon** organizadas por familia, con parámetros clave para implementación GAA.

**Directorio base:**
```
/Solomon-VRPTW-Dataset/
```

---

## Información General Común

| Parámetro | Valor |
|-----------|-------|
| **Número de clientes** | 100 por instancia |
| **Depósitos** | 1 (centrado) |
| **Vehículos** | Homogéneos, no limitados explícitamente |
| **Velocidad** | 1 unidad = 1 unidad de tiempo |
| **Ventanas** | Duras (no se relajan) |
| **Objetivo** | Minimizar (# vehículos ≫ distancia total) |

---

## Familia C1: Clientes Agrupados + Ventanas Cortas

### Características para Código

Ventanas relativamente ajustadas  
Capacidad muy ajustada  
Tiempo de servicio largo  
**Crítico:** Factibilidad temporal importante

---

## Familia C2: Clientes Agrupados + Ventanas Largas

### Características para Código

Ventanas muy holgadas  
Capacidad holgada  
Poca presión temporal  
**Crítico:** Optimización dominada por distancia

---

## Familia R1: Clientes Aleatorios + Ventanas Muy Cortas

### Características para Código

Ventanas **extremadamente restrictivas**  
Tiempo de servicio = ventana  
**Crítico:** Factibilidad temporal crítica  
Alta tasa de soluciones infactibles sin control

---

## Familia R2: Clientes Aleatorios + Ventanas Largas

### Características para Código

Ventanas holgadas  
Capacidad muy holgada  
Poca presión de factibilidad  
**Crítico:** Optimización espacial dominante

---

## Familia RC1: Clientes Mixtos + Ventanas Cortas|

### Características para Código

Presión temporal **moderada-alta**  
Capacidad ajustada  
Estructura mixta (clusters + aleatorios)  
**Crítico:** Balancear tiempo y capacidad

---

## Familia RC2: Clientes Mixtos + Ventanas Largas

### Características para Código

Ventanas holgadas  
Capacidad holgada  
Optimización espacial con estructura mixta  
Menor riesgo de infactibilidad

---

## Resumen Jerárquico: Dimensiones del Dataset

| Dimensión | Familia | Presión Temporal | Presión Capacidad | Estructura |
|-----------|---------|------------------|-------------------|-----------|
| **Agrupado + Corto** | C1 |  Alta |  Alta | Clusters |
| **Agrupado + Largo** | C2 |  Baja |  Baja | Clusters |
| **Aleatorio + Muy Corto** | R1 |  Crítica |  Media | Random |
| **Aleatorio + Largo** | R2 |  Baja |  Baja | Random |
| **Mixto + Corto** | RC1 |  Media |  Media | Mixed |
| **Mixto + Largo** | RC2 |  Baja |  Baja | Mixed |

---

## Recomendaciones de Uso Operativo

### Para Pruebas Rápidas de Factibilidad Temporal
**Familias:** R1, RC1  
Ventanas ajustadas; testean lógica temporal

### Para Pruebas de Optimización Espacial
**Familias:** C2, R2  
Capacidad/horizonte holgados; distancia dominante

### Para Evaluación Balanceada
**Familias:** RC1, RC2  
Presión temporal y espacial simultánea

### Para Benchmarking Completo (Q5)
**Familias:** Todas (C1, C2, R1, R2, RC1, RC2)  
56 instancias = cobertura completa de casos

---

## Estructura de Archivos Esperada

```
Solomon-VRPTW-Dataset/
├── C1/
│   ├── C101, C102, ..., C109
├── C2/
│   ├── C201, C202, ..., C208
├── R1/
│   ├── R101, R102, ..., R112
├── R2/
│   ├── R201, R202, ..., R211
├── RC1/
│   ├── RC101, RC102, ..., RC108
└── RC2/
    ├── RC201, RC202, ..., RC208
```

Cada archivo contiene formato estándar Solomon: coordinates, demand, time windows, service time