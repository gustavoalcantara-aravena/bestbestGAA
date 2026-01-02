# 🚀 Cómo Correr el Proyecto VRPTW-GRASP

**Tipo de Proyecto**: Algoritmo de Ruteo con Ventanas de Tiempo  
**Script Principal**: `run.py`  
**Estado**: Listo para usar

---

## 📋 ¿Qué es este Proyecto?

```
VRPTW-GRASP = Vehicle Routing Problem with Time Windows
                usando GRASP (Greedy Randomized Adaptive Search)

Resuelve problemas de:
  ✓ Entregar paquetes en múltiples ubicaciones
  ✓ Cada cliente tiene ventana de tiempo (horario)
  ✓ Capacidad máxima de vehículos
  ✓ Minimizar distancia/costo total
```

---

## 🎯 FORMAS DE EJECUTAR

### **OPCIÓN 1: Familia Completa (Recomendado para Empezar)**

Resuelve todas las instancias de UNA familia:

```bash
python run.py --family C1
```

**¿Qué hace?**
- Carga 9 instancias de la familia C1 (C101, C102, ..., C109)
- Resuelve cada una
- Muestra resumen al final

**Salida esperada:**
```
Solving Family: C1
Found 9 instances

Instance C101    : Cost:    828.94 | Vehicles:  10 | Feasible: Yes
Instance C102    : Cost:    828.94 | Vehicles:  10 | Feasible: Yes
Instance C103    : Cost:    828.94 | Vehicles:  10 | Feasible: Yes
...

Family Summary:
  Total Instances:     9
  Feasible:            9/9
  Average Cost:        828.94
  Average Vehicles:    10.0
```

**Tiempo**: 2-5 minutos

---

### **OPCIÓN 2: Instancia Individual**

Resuelve UNA instancia específica con detalles:

```bash
python run.py --family C1 --instance C101
```

**¿Qué hace?**
- Carga solo C101
- Resuelve con detalles
- Muestra métricas completas

**Salida esperada:**
```
Solving: datasets/training/C101.txt

VRPTW Problem Summary:
  Customers:        100
  Vehicles:         25
  Capacity:         200
  Planning Horizon: 230 minutes

GRASP Parameters:
  max_iterations: 100
  alpha_rcl:      0.15
  seed:           None
  time_limit:     None

Solution Information:
  Routes:           10
  Total Distance:   828.94
  Total Cost:       828.94
  Feasible:         True

Detailed Metrics:
  total_cost:         828.94
  total_distance:     828.94
  total_time:         ...
  num_routes:         10
```

**Tiempo**: 10-20 segundos

---

## ⚙️ PARÁMETROS CONFIGURABLES

### **Familias Disponibles**

| Familia | Instancias | Tipo | Clientes |
|---------|-----------|------|----------|
| **C1** | 9 (C101-C109) | Clustered | 100 cada una |
| **C2** | 8 (C201-C208) | Clustered + ventanas largas | 100 cada una |
| **R1** | 12 (R101-R112) | Random | 100 cada una |
| **R2** | 11 (R201-R211) | Random + ventanas largas | 100 cada una |
| **RC1** | 8 (RC101-RC108) | Mezcla | 100 cada una |
| **RC2** | 8 (RC201-RC208) | Mezcla + ventanas largas | 100 cada una |

### **Otros Parámetros**

```bash
# Máximo de iteraciones (default: 100)
python run.py --family R1 --iterations 200

# Parámetro alpha (0=greedy, 1=random, default: 0.15)
python run.py --family C1 --alpha 0.3

# Seed para reproducibilidad (default: None)
python run.py --family C1 --seed 42

# Límite de tiempo en segundos (default: None)
python run.py --family C1 --time-limit 300
```

---

## 🎬 EJEMPLOS COMPLETOS

### Ejemplo 1: Probar Rápido (30 seg)

```bash
python run.py --family C1 --instance C101
```

Una instancia, ver si funciona.

---

### Ejemplo 2: Familia Clustered Completa (3 min)

```bash
python run.py --family C1
```

9 instancias de clustered, tiempo limitado.

---

### Ejemplo 3: Familia Random con Más Iteraciones (5 min)

```bash
python run.py --family R1 --iterations 200
```

12 instancias de random, más iteraciones = mejor calidad.

---

### Ejemplo 4: Con Reproducibilidad (2 min)

```bash
python run.py --family RC1 --seed 42 --iterations 100
```

Mezcla RC, seed fijo para reproducir resultados.

---

### Ejemplo 5: Con Límite de Tiempo (3 min)

```bash
python run.py --family C2 --time-limit 30
```

C2 (clustered), máximo 30 segundos por instancia.

---

### Ejemplo 6: Instancia Individual con Todos los Parámetros

```bash
python run.py --family R101 --instance R101 --iterations 500 --alpha 0.2 --seed 42 --time-limit 60
```

R101 específicamente, 500 iteraciones, seed=42, max 60 segundos.

---

## 📊 COMPARAR RESULTADOS

### Parámetro `--alpha`

- **α = 0.0** → Puro Greedy (determinístico, rápido, puede quedar atrapado)
- **α = 0.15** → Poco Random (default, buen balance)
- **α = 0.5** → Equilibrado (más exploración)
- **α = 1.0** → Puro Random (exploración máxima, lento)

```bash
# Comparar diferentes alphas
python run.py --family C1 --alpha 0.0 --instance C101
python run.py --family C1 --alpha 0.15 --instance C101
python run.py --family C1 --alpha 0.5 --instance C101
```

---

### Parámetro `--iterations`

- **100** → Rápido, calidad moderada
- **200** → Balance
- **500** → Calidad alta, más lento

```bash
# Más iteraciones = mejor solución (generalmente)
python run.py --family R1 --instance R101 --iterations 100
python run.py --family R1 --instance R101 --iterations 500
```

---

## 📁 ARCHIVOS DEL PROYECTO

```
VRPTW-GRASP/
├── run.py                       ← SCRIPT PRINCIPAL (aquí ejecutas)
├── README.md                    ← Documentación
├── config.yaml                  ← Configuración (opcional)
│
├── core/                        ← Núcleo del solver
│   ├── problem.py               ├─ Definición del problema
│   ├── solution.py              ├─ Estructura de solución
│   └── evaluation.py            └─ Cálculo de métricas
│
├── data/                        ← Carga de datos
│   └── loader.py                └─ Lector de archivos Solomon
│
├── metaheuristic/               ← Algoritmo GRASP
│   ├── grasp_core.py            ├─ Implementación GRASP
│   └── operators.py             └─ Operadores de búsqueda
│
├── operators/                   ← Operadores especiales
│   ├── insert.py                ├─ Inserción de clientes
│   ├── swap.py                  ├─ Intercambio
│   └── twoc.py                  └─ 2-opt con ventanas
│
└── datasets/                    ← Instancias Solomon
    ├── training/                ├─ Para entrenamiento
    ├── validation/              ├─ Para validación
    └── test/                    └─ Para pruebas finales
```

---

## ⚠️ PROBLEMAS COMUNES

### Problema: "ModuleNotFoundError: No module named 'data'"

**Solución**: Ejecuta desde la carpeta del proyecto
```bash
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP
python run.py --family C1
```

### Problema: "No instances found for family X"

**Solución**: Verifica que los datasets están en `datasets/training/`
```bash
ls datasets/training/
# Deberías ver: C101.txt, C102.txt, etc.
```

### Problema: "Instance not found: C1/C101"

**Solución**: El archivo debe ser `C101.txt` (no `C101.csv` ni otros)

---

## 📈 ENTENDER LA SALIDA

### Para Familia Completa

```
Instance C101    : Cost:    828.94 | Vehicles:  10 | Feasible: Yes
       │          │ Cost total │ Número de   │ ¿Es válida?
       │          │ (distancia)│ rutas usadas│
       Instancia
```

**Significa:**
- ✓ Instancia C101
- ✓ Distancia total: 828.94 km
- ✓ Usó 10 vehículos
- ✓ Respeta todas las restricciones

---

### Para Instancia Individual

```
Solution Information:
  Routes:           10        ← Vehículos usados
  Total Distance:   828.94    ← Distancia total
  Total Cost:       828.94    ← Costo (= distancia aquí)
  Feasible:         True      ← ¿Solución válida?
```

---

## 🎯 PRÓXIMOS PASOS

### Paso 1: Ejecutar Primera Instancia
```bash
python run.py --family C1 --instance C101
```

### Paso 2: Ejecutar Familia Completa
```bash
python run.py --family C1
```

### Paso 3: Comparar Parámetros
```bash
python run.py --family C1 --alpha 0.15 --iterations 100
python run.py --family C1 --alpha 0.5 --iterations 200
```

### Paso 4: Explorar Otras Familias
```bash
python run.py --family R1
python run.py --family RC1
```

---

## 🚀 COMANDO RÁPIDO PARA EMPEZAR

```bash
# Copiar y pegar esto en terminal:
cd c:\Users\gustavo_windows\Desktop\bestbestGAA\projects\VRPTW-GRASP
python run.py --family C1 --instance C101
```

**¿Qué verás?**
- Descripción del problema
- Proceso de resolución
- Solución encontrada con métricas

**Tiempo**: ~10 segundos

---

**Status**: ✅ Listo para ejecutar  
**Última actualización**: Enero 2, 2026
