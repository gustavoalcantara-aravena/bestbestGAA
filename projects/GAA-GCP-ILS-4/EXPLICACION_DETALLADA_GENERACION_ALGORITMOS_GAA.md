# Explicación Detallada: Cómo se Arman los Algoritmos Generados Automáticamente en GAA

**Fecha**: 01 Enero 2026  
**Tema**: Flujo completo de generación automática de algoritmos con ejemplo detallado

---

## 🎯 CONCEPTO FUNDAMENTAL

GAA (Generative Algorithm Architecture) genera **algoritmos automáticamente** combinando operadores de una **Gramática BNF** en forma de **Árboles de Sintaxis Abstracta (AST)**.

**Analogía**: Es como armar un árbol genealógico donde:
- **Raíz**: El algoritmo completo
- **Nodos internos**: Estructuras de control (Seq, If, While, For)
- **Hojas**: Operadores (DSATUR, KempeChain, RandomRecolor, etc.)

---

## 📋 PASO 1: DEFINIR LA GRAMÁTICA BNF

### Gramática para GCP-ILS

```
TERMINALES CONSTRUCTIVOS (4 opciones):
├─ DSATUR              (Construcción por grado de saturación)
├─ LF                  (Construcción por lista de frecuencias)
├─ RandomSequential    (Construcción aleatoria secuencial)
└─ SL                  (Construcción simple)

TERMINALES DE MEJORA LOCAL (4 opciones):
├─ KempeChain          (Cadenas de Kempe)
├─ OneVertexMove       (Mover un vértice)
├─ TabuCol             (Búsqueda tabú)
└─ SwapColors          (Intercambiar colores)

TERMINALES DE PERTURBACIÓN (3 opciones):
├─ RandomRecolor       (Recolorear aleatoriamente)
├─ PartialDestroy      (Destruir parcialmente)
└─ ColorClassMerge     (Fusionar clases de color)

ESTRUCTURAS DE CONTROL (4 opciones):
├─ Seq                 (Secuencia: A → B)
├─ If                  (Condicional: Si condición entonces A sino B)
├─ While               (Bucle: Mientras condición hacer A)
└─ For                 (Bucle: Para cada iteración hacer A)

CONDICIONES (3 opciones):
├─ Improves            (¿Mejora la solución?)
├─ Feasible            (¿Es factible?)
└─ Stagnation          (¿Hay estancamiento?)
```

### Restricciones de Profundidad

```
min_depth = 2  (mínimo 2 niveles)
max_depth = 4  (máximo 4 niveles)
```

---

## 🔄 PASO 2: GENERACIÓN ALEATORIA CON SEED=42

### Código de Generación

```python
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator

# Paso 1: Crear gramática
grammar = Grammar(min_depth=2, max_depth=4)

# Paso 2: Crear generador con seed fijo
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# Paso 3: Generar 3 algoritmos
algorithms = []
for i in range(3):
    algo = generator.generate_with_validation()
    algorithms.append(algo)
```

### ¿Qué hace `generate_with_validation()`?

1. **Genera un árbol AST aleatorio** respetando la gramática
2. **Valida que cumpla restricciones**:
   - Profundidad entre min_depth y max_depth
   - Estructura válida
   - Operadores válidos
3. **Retorna el AST** si es válido, sino intenta nuevamente

---

## 📊 EJEMPLO COMPLETO: GENERACIÓN DE 3 ALGORITMOS

### ALGORITMO 1: Estructura Simple (Profundidad 2)

```
Seed: 42
Iteración: 1

PASO 1: Elegir raíz
├─ Opciones: Seq, If, While, For
└─ Seleccionado: Seq (secuencia)

PASO 2: Generar hijo izquierdo (Constructivo)
├─ Opciones: DSATUR, LF, RandomSequential, SL
└─ Seleccionado: DSATUR

PASO 3: Generar hijo derecho (Mejora Local)
├─ Opciones: KempeChain, OneVertexMove, TabuCol, SwapColors
└─ Seleccionado: KempeChain

RESULTADO AST:
┌─────────────────────────────────────┐
│           Seq                       │  (Secuencia)
├─────────────────────────────────────┤
│  ├─ DSATUR                          │  (Construcción)
│  └─ KempeChain                      │  (Mejora Local)
└─────────────────────────────────────┘

PSEUDOCÓDIGO GENERADO:
```
algorithm_1():
    solution = DSATUR(graph)           # Construcción inicial
    solution = KempeChain(solution)    # Mejora local
    return solution
```

Profundidad: 2 ✓ (válido)
```

---

### ALGORITMO 2: Estructura con Condicional (Profundidad 3)

```
Seed: 42
Iteración: 2

PASO 1: Elegir raíz
└─ Seleccionado: If (condicional)

PASO 2: Generar condición
├─ Opciones: Improves, Feasible, Stagnation
└─ Seleccionado: Improves

PASO 3: Generar rama THEN (si se cumple)
├─ Seleccionado: Seq (secuencia)
│  ├─ LF (Construcción)
│  └─ OneVertexMove (Mejora)

PASO 4: Generar rama ELSE (si no se cumple)
├─ Seleccionado: RandomRecolor (Perturbación)

RESULTADO AST:
┌────────────────────────────────────────────┐
│              If                            │  (Condicional)
├────────────────────────────────────────────┤
│  ├─ Condición: Improves                    │
│  ├─ THEN:                                  │
│  │   └─ Seq                                │
│  │       ├─ LF                             │
│  │       └─ OneVertexMove                  │
│  └─ ELSE:                                  │
│      └─ RandomRecolor                      │
└────────────────────────────────────────────┘

PSEUDOCÓDIGO GENERADO:
```
algorithm_2():
    solution = initial_solution()
    
    if solution.improves():
        solution = LF(graph)                # Construcción alternativa
        solution = OneVertexMove(solution)  # Mejora local
    else:
        solution = RandomRecolor(solution)  # Perturbación
    
    return solution
```

Profundidad: 3 ✓ (válido)
```

---

### ALGORITMO 3: Estructura con Bucle (Profundidad 3)

```
Seed: 42
Iteración: 3

PASO 1: Elegir raíz
└─ Seleccionado: While (bucle)

PASO 2: Generar condición del bucle
├─ Opciones: Improves, Feasible, Stagnation
└─ Seleccionado: Feasible

PASO 3: Generar cuerpo del bucle
├─ Seleccionado: Seq (secuencia)
│  ├─ TabuCol (Mejora)
│  └─ PartialDestroy (Perturbación)

RESULTADO AST:
┌────────────────────────────────────────────┐
│              While                         │  (Bucle)
├────────────────────────────────────────────┤
│  ├─ Condición: Feasible                    │
│  └─ Cuerpo:                                │
│      └─ Seq                                │
│          ├─ TabuCol                        │
│          └─ PartialDestroy                 │
└────────────────────────────────────────────┘

PSEUDOCÓDIGO GENERADO:
```
algorithm_3():
    solution = initial_solution()
    
    while solution.is_feasible():
        solution = TabuCol(solution)        # Mejora local
        solution = PartialDestroy(solution) # Perturbación
    
    return solution
```

Profundidad: 3 ✓ (válido)
```

---

## 🔍 PASO 3: VALIDACIÓN DE ALGORITMOS

### Validaciones Realizadas

```python
def validate_ast(ast):
    """Valida que el AST respeta la gramática"""
    
    # 1. Validar tipo
    if not isinstance(ast, ASTNode):
        return False  # Error: no es un nodo válido
    
    # 2. Validar profundidad
    depth = ast.depth()
    if depth < 2 or depth > 4:
        return False  # Error: profundidad fuera de rango
    
    # 3. Validar tamaño
    size = ast.size()
    if size > 100:
        return False  # Error: demasiados nodos
    
    # 4. Validar estructura
    # - Seq debe tener 2 hijos
    # - If debe tener condición + rama THEN + rama ELSE
    # - While debe tener condición + cuerpo
    # - For debe tener iteraciones + cuerpo
    
    return True  # Válido
```

---

## 🎬 PASO 4: EJECUCIÓN DEL ALGORITMO GENERADO

### Ejemplo: Ejecutar Algorithm_1 en una instancia

```python
from gaa.interpreter import execute_algorithm
from core.problem import GraphColoringProblem

# Cargar instancia
problem = GraphColoringProblem.load_from_dimacs("datasets/MYC/myciel3.col")

# Ejecutar algoritmo generado
solution = execute_algorithm(algorithm_1_ast, problem, seed=42)

# Resultado
print(f"Colores utilizados: {solution.num_colors}")
print(f"Tiempo: {solution.time:.3f}s")
print(f"Factible: {solution.is_feasible}")
```

### Flujo de Ejecución Interno

```
1. DSATUR(graph)
   ├─ Inicializar solución vacía
   ├─ Ordenar vértices por grado de saturación
   ├─ Asignar colores secuencialmente
   └─ Retorna: solución inicial con ~4 colores

2. KempeChain(solution)
   ├─ Para cada par de colores (i, j)
   │  ├─ Buscar cadena de Kempe
   │  ├─ Si mejora, aplicar intercambio
   │  └─ Actualizar solución
   └─ Retorna: solución mejorada con ~3 colores

RESULTADO FINAL: Solución con 3 colores (óptimo para myciel3)
```

---

## 📊 RESUMEN: LOS 3 ALGORITMOS GENERADOS

| Algoritmo | Estructura | Profundidad | Operadores | Pseudocódigo |
|-----------|-----------|-------------|-----------|--------------|
| **Alg 1** | Seq | 2 | DSATUR → KempeChain | Construcción + Mejora |
| **Alg 2** | If | 3 | LF, OneVertexMove, RandomRecolor | Construcción condicional |
| **Alg 3** | While | 3 | TabuCol, PartialDestroy | Bucle de mejora |

---

## 🔄 VARIABILIDAD: ¿POR QUÉ CAMBIAN LOS ALGORITMOS?

Aunque el **seed es fijo (42)**, los algoritmos **pueden variar** porque:

1. **Generador usa operadores aleatorios** dentro de la gramática
2. **Cada llamada a `generate_with_validation()`** puede producir un árbol diferente
3. **Validación puede rechazar** árboles inválidos, causando reintentos
4. **Orden de exploración** de operadores puede variar

**Resultado**: Con seed=42, obtienes **3 algoritmos diferentes pero reproducibles** cada vez que ejecutas.

---

## 🎯 FLUJO COMPLETO EN CÓDIGO

```python
# 1. CREAR GRAMÁTICA
grammar = Grammar(min_depth=2, max_depth=4)

# 2. CREAR GENERADOR CON SEED FIJO
generator = AlgorithmGenerator(grammar=grammar, seed=42)

# 3. GENERAR 3 ALGORITMOS
algorithms = []
for i in range(3):
    # Generar AST aleatorio
    ast = generator.generate_with_validation()
    
    # Validar estructura
    if grammar.validate_ast(ast):
        algorithms.append({
            'id': i + 1,
            'name': f'GAA_Algorithm_{i+1}',
            'ast': ast,
            'depth': ast.depth(),
            'size': ast.size()
        })

# 4. EJECUTAR EN INSTANCIAS
for algo in algorithms:
    for instance in instances:
        solution = execute_algorithm(algo['ast'], instance, seed=42)
        print(f"{algo['name']} en {instance.name}: {solution.num_colors} colores")

# 5. ANALIZAR RESULTADOS
analyzer = StatisticalAnalyzer()
comparison = analyzer.compare_multiple_algorithms(results)
print(f"Mejor algoritmo: {comparison['best_algorithm']}")
```

---

## 📝 CONCLUSIÓN

**Los algoritmos se arman así**:

1. **Gramática BNF** define operadores disponibles
2. **Generador aleatorio** (seed=42) construye ASTs
3. **Validación** asegura que cumplan restricciones
4. **Interpretador** ejecuta el AST en instancias
5. **Análisis estadístico** compara los 3 algoritmos

**Resultado**: 3 algoritmos únicos, generados automáticamente, reproducibles con seed=42.

