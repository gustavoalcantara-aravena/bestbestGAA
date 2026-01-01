# Explicación: Generación Automática de Algoritmos (GAA) en GAA-GCP-ILS-4

## 1. ¿QUÉ ES UN ALGORITMO GENERADO AUTOMÁTICAMENTE?

Un algoritmo generado automáticamente es un **árbol sintáctico (AST)** que representa un programa de resolución de problemas de coloración de grafos. Este árbol se construye usando operadores (terminales) disponibles en la gramática.

### Estructura General de un Algoritmo

```
Algoritmo = Secuencia de operaciones
          = Seq(
              GreedyConstruct,    # Construcción inicial
              If(                 # Decisión
                LocalSearch,      # Búsqueda local
                Perturbation      # Perturbación
              )
            )
```

## 2. CARACTERÍSTICAS FIJAS DE LOS 3 ALGORITMOS GENERADOS

En el proyecto actual, los 3 algoritmos generados tienen **EXACTAMENTE las mismas características estructurales**:

### Características Idénticas:
- **Número de nodos**: 4 nodos en el AST
- **Profundidad máxima**: 3 niveles
- **Estructura base**: Seq(GreedyConstruct, If(LocalSearch, Perturbation))
- **Seed**: 42 (para reproducibilidad)
- **Gramática**: Misma para los 3

### Ejemplo de Estructura Fija:

```
Algoritmo_1:
├── Seq (nodo raíz)
│   ├── GreedyConstruct (nodo 1)
│   │   └── DSATUR (operador específico)
│   └── If (nodo 2)
│       ├── LocalSearch (nodo 3)
│       │   └── KempeChain (operador específico)
│       └── Perturbation (nodo 4)
│           └── RandomRecolor (operador específico)

Algoritmo_2:
├── Seq (nodo raíz)
│   ├── GreedyConstruct (nodo 1)
│   │   └── LF (operador específico - DIFERENTE)
│   └── If (nodo 2)
│       ├── LocalSearch (nodo 3)
│       │   └── OneVertexMove (operador específico - DIFERENTE)
│       └── Perturbation (nodo 4)
│           └── PartialDestroy (operador específico - DIFERENTE)

Algoritmo_3:
├── Seq (nodo raíz)
│   ├── GreedyConstruct (nodo 1)
│   │   └── RandomSequential (operador específico - DIFERENTE)
│   └── If (nodo 2)
│       ├── LocalSearch (nodo 3)
│       │   └── TabuCol (operador específico - DIFERENTE)
│       └── Perturbation (nodo 4)
│           └── RandomRecolor (operador específico - IGUAL)
```

## 3. ¿EN QUÉ SE DIFERENCIAN LOS 3 ALGORITMOS?

Los 3 algoritmos se diferencian **ÚNICAMENTE en los operadores específicos** que se seleccionan para cada nodo:

### Operadores Disponibles por Tipo:

**Constructivos (GreedyConstruct):**
- DSATUR
- LF (Largest First)
- RandomSequential

**Mejora Local (LocalSearch):**
- KempeChain
- OneVertexMove
- TabuCol

**Perturbación (Perturbation):**
- RandomRecolor
- PartialDestroy

### Ejemplo Concreto:

```
ALGORITMO 1:
  Paso 1: Construcción inicial con DSATUR
  Paso 2: Si es posible, mejora con KempeChain
  Paso 3: Si no mejora, perturba con RandomRecolor

ALGORITMO 2:
  Paso 1: Construcción inicial con LF
  Paso 2: Si es posible, mejora con OneVertexMove
  Paso 3: Si no mejora, perturba con PartialDestroy

ALGORITMO 3:
  Paso 1: Construcción inicial con RandomSequential
  Paso 2: Si es posible, mejora con TabuCol
  Paso 3: Si no mejora, perturba con RandomRecolor
```

## 4. PROCESO DE GENERACIÓN

### Paso 1: Crear Gramática
```python
grammar = Grammar(
    min_depth=2,
    max_depth=3,
    terminals={
        'GreedyConstruct': [DSATUR, LF, RandomSequential],
        'LocalSearch': [KempeChain, OneVertexMove, TabuCol],
        'Perturbation': [RandomRecolor, PartialDestroy]
    }
)
```

### Paso 2: Generar 3 Algoritmos
```python
generator = AlgorithmGenerator(grammar)
algorithms = [
    generator.generate(),  # Algoritmo 1
    generator.generate(),  # Algoritmo 2
    generator.generate()   # Algoritmo 3
]
```

Cada `generate()` crea un nuevo árbol con:
- Misma estructura (4 nodos, profundidad 3)
- **Diferentes operadores seleccionados aleatoriamente**

### Paso 3: Ejecutar en Instancias
```python
for algo in algorithms:
    for problem in problems:
        solution = execute_algorithm(algo, problem)
        # Registrar número de colores encontrados
```

## 5. ¿POR QUÉ TIENEN DIFERENTES RESULTADOS SI TIENEN LA MISMA ESTRUCTURA?

Aunque tienen la misma estructura, los algoritmos producen **diferentes resultados** porque:

1. **Operadores diferentes**: Cada operador tiene lógica diferente
   - DSATUR: Colorea vértices por grado decreciente
   - LF: Colorea vértices por orden de tamaño de clique
   - RandomSequential: Colorea en orden aleatorio

2. **Diferentes estrategias de mejora**:
   - KempeChain: Intercambia colores en cadenas
   - OneVertexMove: Mueve un vértice a otro color
   - TabuCol: Búsqueda tabú con memoria

3. **Diferentes perturbaciones**:
   - RandomRecolor: Recolores aleatorios
   - PartialDestroy: Destruye parcialmente la solución

## 6. EJEMPLO DE EJECUCIÓN

### Entrada: myciel3 (11 vértices, 20 aristas, BKS=4)

```
Algoritmo 1 (DSATUR + KempeChain + RandomRecolor):
  → Construcción: 5 colores
  → Mejora: 4 colores (KempeChain optimiza)
  → Resultado: 4 colores ✅ ÓPTIMO (gap=0%)

Algoritmo 2 (LF + OneVertexMove + PartialDestroy):
  → Construcción: 5 colores
  → Mejora: 4 colores (OneVertexMove optimiza)
  → Resultado: 4 colores ✅ ÓPTIMO (gap=0%)

Algoritmo 3 (RandomSequential + TabuCol + RandomRecolor):
  → Construcción: 6 colores
  → Mejora: 4 colores (TabuCol optimiza fuertemente)
  → Resultado: 4 colores ✅ ÓPTIMO (gap=0%)
```

## 7. RESUMEN

| Aspecto | Valor |
|---------|-------|
| **Número de algoritmos** | 3 |
| **Estructura** | IDÉNTICA (4 nodos, profundidad 3) |
| **Diferencia** | Operadores seleccionados aleatoriamente |
| **Variabilidad** | Baja (estructura fija) |
| **Propósito** | Comparar desempeño de diferentes operadores |

## 8. VISUALIZACIÓN DE LA GRAMÁTICA

```
Grammar:
├── Seq
│   ├── GreedyConstruct
│   │   ├── DSATUR
│   │   ├── LF
│   │   └── RandomSequential
│   └── If
│       ├── LocalSearch
│       │   ├── KempeChain
│       │   ├── OneVertexMove
│       │   └── TabuCol
│       └── Perturbation
│           ├── RandomRecolor
│           └── PartialDestroy
```

Cada algoritmo selecciona **UNO** de cada operador disponible.

## 9. CÓDIGO RELEVANTE

### En `test_experiment_quick.py`:

```python
# Generar 3 algoritmos con estructura fija
generator = AlgorithmGenerator(grammar)
gaa_algorithms = [
    generator.generate(),  # Algoritmo 1
    generator.generate(),  # Algoritmo 2
    generator.generate()   # Algoritmo 3
]

# Ejecutar en instancias
for algo_idx, algo in enumerate(gaa_algorithms):
    algo_name = f"GAA_Algorithm_{algo_idx + 1}"
    for problem in gaa_problems:
        solution = execute_algorithm(algo, problem, seed=42)
        # Registrar resultado
```

### En `core/grammar.py`:

```python
class Grammar:
    def __init__(self, min_depth=2, max_depth=3, terminals=None):
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.terminals = terminals or {}
    
    def generate_random_node(self, depth):
        """Genera un nodo aleatorio respetando profundidad"""
        # Selecciona operador aleatorio del terminal
        # Mantiene estructura fija (Seq -> If -> operadores)
```

## CONCLUSIÓN

Los 3 algoritmos generados automáticamente tienen:
- ✅ **Misma estructura**: 4 nodos, profundidad 3
- ✅ **Diferentes operadores**: Seleccionados aleatoriamente
- ✅ **Diferentes resultados**: Debido a la lógica diferente de cada operador
- ✅ **Propósito**: Comparar qué combinación de operadores es mejor
