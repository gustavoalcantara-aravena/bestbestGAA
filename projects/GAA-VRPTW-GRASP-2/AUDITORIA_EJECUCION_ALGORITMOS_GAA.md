# Auditoría: Ejecución de Algoritmos Generados por GAA
**Fecha**: 2 de enero de 2026  
**Problema Identificado**: Los algoritmos generados por GAA no se están ejecutando - se usan GRASP/VND/ILS en su lugar

---

## 1. ANÁLISIS DE LA ARQUITECTURA ACTUAL

### 1.1 Generación de Algoritmos GAA
**Ubicación**: `scripts/experiments.py` (líneas 335-346)

```python
gaa_generator = AlgorithmGenerator(seed=config.seed)
gaa_algorithms = gaa_generator.generate_three_algorithms()
```

**Estructura Generada**:
- **Nombre**: `GAA_Algorithm_1`, `GAA_Algorithm_2`, `GAA_Algorithm_3`
- **Tipo**: Árboles Sintácticos Abstractos (AST) únicos
- **Patrón**: `Seq(GreedyConstruct, While(LocalSearch))`
- **Profundidad**: 3 (fija para comparación justa)
- **Tamaño**: 4 nodos

**Operadores Disponibles**:

**Constructivos** (6 opciones):
- NearestNeighbor, Savings, Sweep, TimeOrientedNN, RegretInsertion, RandomizedInsertion

**Mejora Local** (8 opciones):
- TwoOpt, OrOpt, ThreeOpt, Relocate, Exchange, GENI, LKH, VND

Cada algoritmo selecciona aleatoriamente (pero con seed reproducible):
- 1 operador constructivo
- 1 operador de mejora local
- Parámetros (alpha, iteraciones)

### 1.2 Problema: Ejecución Hardcodeada
**Ubicación**: `scripts/experiments.py` (línea 367)

```python
algorithms_to_test = ['GRASP', 'VND', 'ILS']  # ← IGNORA GAA generados
```

**Impacto**:
- Los 3 algoritmos GAA se generan pero NO se ejecutan
- Se ejecutan algoritmos estándar (GRASP, VND, ILS) en su lugar
- Pierde el propósito de GAA: generar variantes automáticas de GRASP
- Logs registran "GRASP/VND/ILS" en lugar de "GAA_Algorithm_X"

### 1.3 Infraestructura Disponible para Ejecución

**ASTInterpreter** (`src/gaa/interpreter.py`):
- ✅ Existe y está completamente implementado
- ✅ Puede ejecutar cualquier AST en una instancia VRPTW
- ✅ Maneja todos los tipos de nodos (control flow + terminales)
- ✅ Integrado con OperatorRegistry (6 constructivos + 8 mejora)
- ✅ Retorna Solution con K y D finales

**Compatibilidad GRASP-GAA**:
- ✅ Los AST generados son compatibles con GRASP base
- ✅ Estructura: Construcción greedy → mejora iterativa (GRASP esencial)
- ✅ Usa mismos operadores que GRASP puede usar
- ✅ Parámetros (alpha, iteraciones) ajustables

---

## 2. ANÁLISIS DE GENERACIÓN DE ALGORITMOS

### 2.1 Estructura del Algoritmo Generado

```
GAA_Algorithm_1:
├── AST Dict con:
│   ├── name: "GAA_Algorithm_1"
│   ├── ast: ASTNode (Seq structure)
│   ├── pattern: "iterative-simple"
│   ├── stats: {depth: 3, size: 4, nodes: 4}
│   ├── components: {
│   │   ├── constructor: "NearestNeighbor" (random)
│   │   ├── local_search: "TwoOpt" (random)
│   │   ├── alpha: 0.25 (random ∈ [0.1, 0.5])
│   │   └── iterations: 100 (random ∈ [50,100,150,200])
│   └── seed: 42
```

### 2.2 Función que los Genera

**`AlgorithmGenerator.generate_three_algorithms()`**:
- Genera 3 ASTs con características IDÉNTICAS (depth=3, size=4)
- Asegura comparación justa con GRASP/VND/ILS
- Cada AST tiene COMBINACIÓN ÚNICA de operadores
- Retorna: `List[Dict[str, Any]]` (compatible con experiments.py)

---

## 3. ANÁLISIS DE INTERPRETACIÓN

### 3.1 ASTInterpreter Disponible

**Clase**: `ASTInterpreter` (`src/gaa/interpreter.py`)

**Método Clave**:
```python
def execute(self, algorithm: ASTNode, instance: Instance, 
            initial_solution: Optional[Solution] = None) -> Solution:
    """Execute algorithm on instance."""
    # Retorna: Solution con K (vehículos), D (distancia)
```

**Entrada**:
- `algorithm`: ASTNode (del dict generado)
- `instance`: Instance VRPTW
- `initial_solution`: opcional

**Salida**:
- `Solution`: objeto con atributos `num_vehicles`, `total_distance`

### 3.2 OperatorRegistry

Mapea nombres de operadores → implementaciones:
- **Constructores**: `self.constructors['NearestNeighbor']`, etc.
- **LocalSearch**: `self.local_search['TwoOpt']`, etc.
- **Perturbadores**: `self.perturbation[...]`
- **Reparadores**: `self.repair[...]`

---

## 4. ESTADO ACTUAL DE ExperimentExecutor

**Ubicación**: `scripts/experiments.py` (línea ~100)

**Métodos**:
- `get_solomon_instances(families)`: Carga instancias Solomon
- `all_instances[family][instance_id]`: Acceso a instancias
- `add_result(metric_dict)`: Registra resultados

**Compatible con**: Tanto GRASP/VND/ILS como algoritmos GAA

---

## 5. CONCLUSIONES DE AUDITORÍA

| Aspecto | Estado | Comentario |
|---------|--------|-----------|
| **Generación GAA** | ✅ Funcional | 3 algoritmos generados correctamente |
| **Interpretación AST** | ✅ Funcional | ASTInterpreter listo para ejecutar |
| **Ejecución** | ❌ No implementada | Hardcodeada a GRASP/VND/ILS |
| **Logging** | ✅ Adaptable | Ya registra GAA generados |
| **Compatibility** | ✅ Total | Infraestructura lista |

---

## 6. PUNTOS CLAVE PARA IMPLEMENTACIÓN

### ✅ Lo que SÍ existe:
1. **AlgorithmGenerator**: Genera 3 ASTs únicos
2. **ASTInterpreter**: Ejecuta ASTs en instancias
3. **OperatorRegistry**: Mapea operadores a implementaciones
4. **ExperimentExecutor**: Maneja instancias y resultados
5. **ExperimentLogger**: Registra ejecuciones

### ❌ Lo que FALTA:
1. **Conexión entre GAA generados y ASTInterpreter**
2. **Loop de ejecución sobre algoritmos GAA** en lugar de GRASP/VND/ILS
3. **Extracción de K y D** del resultado de ASTInterpreter
4. **Manejo de errores** específico para ejecución AST

