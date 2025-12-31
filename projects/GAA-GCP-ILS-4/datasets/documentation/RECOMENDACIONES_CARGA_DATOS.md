# Recomendaciones para Cargar Datos y Ejecutar Algoritmos

## 📋 Tabla de Contenidos

1. [Validación del Formato DIMACS](#validación-del-formato-dimacs)
2. [Lectura Segura de Archivos](#lectura-segura-de-archivos)
3. [Estructuras de Datos Recomendadas](#estructuras-de-datos-recomendadas)
4. [Inicialización Correcta](#inicialización-correcta)
5. [Validación Post-Carga](#validación-post-carga)
6. [Manejo de Memoria](#manejo-de-memoria)
7. [Errores Comunes y Soluciones](#errores-comunes-y-soluciones)
8. [Testing y Debugging](#testing-y-debugging)
9. [Benchmark y Performance](#benchmark-y-performance)

---

## Validación del Formato DIMACS

### ✅ Estructura DIMACS Correcta

Cada archivo .col debe tener este formato:

```
c FILE: ejemplo.col
c SOURCE: fuente del grafo
c DESCRIPTION: descripción breve
p edge <nodos> <aristas>
e <u> <v>
e <u> <v>
...
```

### ⚠️ Validaciones Obligatorias

#### 1. **Validar Línea de Parámetros (p edge)**

```python
# ❌ INCORRECTO
p edge 100            # Falta el número de aristas
p 100 500             # Falta "edge"
edge 100 500          # Falta "p"

# ✅ CORRECTO
p edge 100 500        # p + edge + #nodos + #aristas
```

**Recomendación:**
```python
def validate_header(line):
    """Valida la línea de parámetros DIMACS"""
    parts = line.strip().split()
    
    if len(parts) != 4:
        raise ValueError(f"Header inválido. Esperado: 'p edge <n> <m>'")
    
    if parts[0] != 'p' or parts[1] != 'edge':
        raise ValueError(f"Header debe comenzar con 'p edge'")
    
    try:
        n_nodes = int(parts[2])
        n_edges = int(parts[3])
        
        if n_nodes <= 0 or n_edges < 0:
            raise ValueError("Nodos y aristas deben ser positivos")
        
        return n_nodes, n_edges
    except ValueError as e:
        raise ValueError(f"Parámetros no son enteros válidos: {e}")
```

#### 2. **Validar Aristas**

```python
# ❌ INCORRECTO
e 0 5                 # Nodos indexados desde 0 (DIMACS usa 1)
e 101 50              # Nodo 101 > 100 (fuera de rango)
e 5 5                 # Auto-loops no permitidos
e 10 20
e 20 10               # Duplicados (misma arista dos veces)

# ✅ CORRECTO
e 1 5                 # Nodos indexados desde 1
e 10 20               # Ambos ≤ 100
e 20 30               # Sin auto-loops
```

**Recomendación:**
```python
def validate_edge(u, v, n_nodes, seen_edges):
    """Valida una arista"""
    # Rango: [1, n_nodes]
    if u < 1 or u > n_nodes or v < 1 or v > n_nodes:
        raise ValueError(f"Nodo fuera de rango [1, {n_nodes}]: e {u} {v}")
    
    # Sin auto-loops
    if u == v:
        raise ValueError(f"Auto-loop no permitido: e {u} {v}")
    
    # Sin duplicados (normalizar a (min, max))
    edge = tuple(sorted([u, v]))
    if edge in seen_edges:
        raise ValueError(f"Arista duplicada: e {u} {v}")
    
    seen_edges.add(edge)
    return True
```

#### 3. **Archivos Problemáticos en el Dataset**

⚠️ **Cuidado especial con:**
- `myciel2.col` - **Formato incompleto/corrupto** (no tiene encabezado DIMACS)
  - Solo contiene datos brutos sin headers
  - **NO USAR en algoritmos**

---

## Lectura Segura de Archivos

### Plantilla Recomendada

```python
def load_dimacs_safe(filepath):
    """Carga un archivo DIMACS con validaciones completas"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    except Exception as e:
        raise IOError(f"Error leyendo archivo: {e}")
    
    if not lines:
        raise ValueError("Archivo vacío")
    
    # Procesar encabezado
    n_nodes = None
    n_edges_expected = None
    
    for line in lines:
        line = line.strip()
        
        # Ignorar comentarios y líneas vacías
        if not line or line.startswith('c'):
            continue
        
        # Procesar parámetros
        if line.startswith('p edge'):
            try:
                n_nodes, n_edges_expected = validate_header(line)
            except ValueError as e:
                raise ValueError(f"Error en header (línea): {e}")
            break
    
    if n_nodes is None:
        raise ValueError("No se encontró línea 'p edge' en el archivo")
    
    # Procesar aristas
    adjacency = {i: set() for i in range(1, n_nodes + 1)}
    seen_edges = set()
    n_edges_read = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line or line.startswith('c') or line.startswith('p'):
            continue
        
        if not line.startswith('e'):
            raise ValueError(f"Línea {line_num}: Esperado 'e' al inicio")
        
        try:
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Línea {line_num}: Formato inválido '{line}'")
            
            u, v = int(parts[1]), int(parts[2])
            validate_edge(u, v, n_nodes, seen_edges)
            
            adjacency[u].add(v)
            adjacency[v].add(u)
            n_edges_read += 1
            
        except ValueError as e:
            raise ValueError(f"Línea {line_num}: {e}")
    
    # Verificar cantidad de aristas
    if n_edges_read != n_edges_expected:
        raise ValueError(
            f"Cantidad de aristas mismatch: "
            f"expected={n_edges_expected}, "
            f"read={n_edges_read}"
        )
    
    return {
        'n_nodes': n_nodes,
        'n_edges': n_edges_read,
        'adjacency': adjacency
    }
```

---

## Estructuras de Datos Recomendadas

### 1. **Lista de Adyacencia (Recomendado para Grafos Sparse)**

```python
class Graph:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.n_edges = 0
        self.adj = {i: set() for i in range(1, n_nodes + 1)}
    
    def add_edge(self, u, v):
        """Agregar arista sin duplicados"""
        if u != v:  # Evitar auto-loops
            if v not in self.adj[u]:
                self.adj[u].add(v)
                self.adj[v].add(u)
                self.n_edges += 1
    
    def get_neighbors(self, node):
        """Obtener vecinos de un nodo"""
        return self.adj.get(node, set())
    
    def get_degree(self, node):
        """Grado del nodo"""
        return len(self.adj[node])
    
    def is_edge(self, u, v):
        """Verificar si existe arista"""
        return v in self.adj.get(u, set())
```

**Ventajas:**
- Eficiente en memoria para grafos sparse
- Acceso O(1) a vecinos
- Fácil implementar BFS/DFS

**Desventajas:**
- Acceso más lento si el grafo es muy denso

### 2. **Matriz de Adyacencia (Para Grafos Densos)**

```python
import numpy as np

class DenseGraph:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.matrix = np.zeros((n_nodes + 1, n_nodes + 1), dtype=np.uint8)
    
    def add_edge(self, u, v):
        """Agregar arista"""
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1
    
    def is_edge(self, u, v):
        """Verificar arista O(1)"""
        return self.matrix[u][v] == 1
    
    def get_neighbors(self, node):
        """Obtener vecinos"""
        return np.where(self.matrix[node] == 1)[0]
```

**Ventajas:**
- Acceso O(1) a cualquier arista
- Mejor para grafos densos

**Desventajas:**
- O(n²) memoria siempre
- Ineficiente para sparse

### 3. **Estructura Híbrida (Recomendado)**

```python
class SmartGraph:
    def __init__(self, n_nodes, n_edges):
        self.n_nodes = n_nodes
        # Decidir estructura según densidad
        density = 2 * n_edges / (n_nodes * (n_nodes - 1))
        
        if density > 0.5:
            # Usar matriz para grafos densos
            self.use_matrix = True
            self.matrix = np.zeros((n_nodes + 1, n_nodes + 1), dtype=np.uint8)
        else:
            # Usar lista adyacencia para sparse
            self.use_matrix = False
            self.adj = {i: set() for i in range(1, n_nodes + 1)}
    
    def add_edge(self, u, v):
        if self.use_matrix:
            self.matrix[u][v] = 1
            self.matrix[v][u] = 1
        else:
            self.adj[u].add(v)
            self.adj[v].add(u)
    
    def is_edge(self, u, v):
        if self.use_matrix:
            return self.matrix[u][v] == 1
        else:
            return v in self.adj[u]
```

---

## Inicialización Correcta

### 1. **Variable de Coloreo**

```python
def initialize_coloring(n_nodes):
    """Inicializar array de coloreo"""
    
    # ✅ CORRECTO: Indexar desde 1 (DIMACS)
    coloring = {}
    for node in range(1, n_nodes + 1):
        coloring[node] = 0  # 0 = sin color
    
    return coloring

def initialize_coloring_array(n_nodes):
    """Usando array (más eficiente)"""
    # Índice 0 no se usa (DIMACS comienza en 1)
    return [0] * (n_nodes + 1)
```

### 2. **Estructuras Auxiliares**

```python
def initialize_color_info(n_nodes):
    """Inicializar información de coloreo"""
    return {
        'coloring': [0] * (n_nodes + 1),      # coloring[i] = color del nodo i
        'color_count': {},                      # color_count[c] = cantidad nodos con color c
        'color_available': [set() for _ in range(n_nodes + 1)],  # colores disponibles por nodo
    }
```

### 3. **Metrices de Monitoreo**

```python
def initialize_metrics():
    """Inicializar métricas"""
    return {
        'colors_used': 0,           # Cantidad de colores usado
        'colors_history': [],       # Histórico de colores en cada iteración
        'time_start': time.time(),  # Tiempo de inicio
        'conflicts': 0,             # Cantidad de conflictos
    }
```

---

## Validación Post-Carga

### ✅ Checklist de Validación

```python
def validate_graph(graph_data):
    """Validar integridad del grafo cargado"""
    
    issues = []
    
    # 1. Verificar coherencia de nodos
    max_node = max(graph_data['adjacency'].keys())
    if max_node != graph_data['n_nodes']:
        issues.append(f"Max nodo {max_node} != n_nodes {graph_data['n_nodes']}")
    
    # 2. Verificar simetría (grafo no dirigido)
    for u in graph_data['adjacency']:
        for v in graph_data['adjacency'][u]:
            if u not in graph_data['adjacency'][v]:
                issues.append(f"Asimetría: ({u}, {v}) existe pero ({v}, {u}) no")
    
    # 3. Contar aristas reales
    edge_count = 0
    for u in graph_data['adjacency']:
        edge_count += len(graph_data['adjacency'][u])
    edge_count //= 2  # Contar dos veces (u->v y v->u)
    
    if edge_count != graph_data['n_edges']:
        issues.append(
            f"Contador de aristas mismatch: "
            f"header={graph_data['n_edges']}, actual={edge_count}"
        )
    
    # 4. Verificar rangos de nodos
    for u in graph_data['adjacency']:
        if u < 1 or u > graph_data['n_nodes']:
            issues.append(f"Nodo {u} fuera de rango [1, {graph_data['n_nodes']}]")
    
    # 5. Verificar sin auto-loops
    for u in graph_data['adjacency']:
        if u in graph_data['adjacency'][u]:
            issues.append(f"Auto-loop encontrado en nodo {u}")
    
    if issues:
        print("⚠️  ADVERTENCIAS DE VALIDACIÓN:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("✅ Grafo válido y coherente")
    return True
```

---

## Manejo de Memoria

### 1. **Estimación de Memoria**

```python
def estimate_memory(n_nodes, n_edges):
    """Estimar requerimientos de memoria"""
    
    # Lista adyacencia
    adj_memory = n_edges * 2 * 8  # Bytes (aprox)
    
    # Coloring array
    coloring_memory = n_nodes * 8
    
    # Total
    total_mb = (adj_memory + coloring_memory) / (1024 ** 2)
    
    print(f"Estimado de memoria:")
    print(f"  Grafo: {adj_memory / 1024 / 1024:.2f} MB")
    print(f"  Coloring: {coloring_memory / 1024 / 1024:.2f} MB")
    print(f"  TOTAL: {total_mb:.2f} MB")
    
    return total_mb
```

### 2. **Optimizaciones**

```python
# ✅ Usar tipos eficientes
import numpy as np

# Para nodos
nodes = np.array([1, 2, 3, ...], dtype=np.uint32)  # Si n < 2^32

# Para colores (limitado)
coloring = np.zeros(n_nodes + 1, dtype=np.uint8)   # 256 colores máx

# Para sets de adyacencia (sparse)
adj = {i: set() for i in range(1, n_nodes + 1)}
```

### 3. **Garbage Collection**

```python
import gc

def load_and_process(filepath):
    """Cargar, procesar y limpiar"""
    
    # Cargar grafo
    graph = load_dimacs_safe(filepath)
    
    # Procesar
    result = process_graph(graph)
    
    # Limpiar
    del graph
    gc.collect()
    
    return result
```

---

## Errores Comunes y Soluciones

### ❌ Error 1: Indexación Incorrecta

```python
# ❌ INCORRECTO
adjacency = [set() for _ in range(n_nodes)]  # Índices 0 a n_nodes-1
coloring[0] = 1  # Usa índice 0

# ✅ CORRECTO
adjacency = {i: set() for i in range(1, n_nodes + 1)}  # Índices 1 a n_nodes
coloring = [0] * (n_nodes + 1)  # coloring[0] no se usa
```

**Explicación:** DIMACS indexa nodos desde 1, no desde 0.

---

### ❌ Error 2: Duplicación de Aristas

```python
# ❌ INCORRECTO
def add_edge(u, v):
    adj[u].add(v)
    adj[v].add(u)
    n_edges += 1     # ¡Contar dos veces!

# ✅ CORRECTO
def add_edge(u, v):
    adj[u].add(v)
    adj[v].add(u)
    n_edges += 1     # Solo contar una vez
```

---

### ❌ Error 3: No Validar Auto-loops

```python
# ❌ INCORRECTO
e 5 5  # Auto-loop: ¡permitido!

# ✅ CORRECTO
if u == v:
    raise ValueError("Auto-loop no permitido")
```

---

### ❌ Error 4: Ignorar Comentarios

```python
# ❌ INCORRECTO
for line in lines:
    parts = line.split()  # No salta comentarios
    u, v = int(parts[1]), int(parts[2])

# ✅ CORRECTO
for line in lines:
    if line.startswith('c') or not line.strip():
        continue  # Saltar comentarios y líneas vacías
    # Procesar
```

---

### ❌ Error 5: Mismatch de Tipos

```python
# ❌ INCORRECTO
coloring = []  # Lista vacía
coloring[1] = 3  # IndexError

# ✅ CORRECTO
coloring = [0] * (n_nodes + 1)  # Pre-asignar
coloring[1] = 3  # OK
```

---

## Testing y Debugging

### Cargar y Validar

```python
# Cargar instancia de prueba pequeña
test_file = "by_family/MYC/myciel3.col"

try:
    graph = load_dimacs_safe(test_file)
    print(f"Nodos: {graph['n_nodes']}")
    print(f"Aristas: {graph['n_edges']}")
    
    # Validar integridad
    if validate_graph(graph):
        print("✅ Carga exitosa")
    else:
        print("❌ Problemas detectados")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

### Debug de Coloreo

```python
def debug_coloring(graph, coloring, node):
    """Debug información de un nodo"""
    print(f"\nDEBUG Nodo {node}:")
    print(f"  Color asignado: {coloring[node]}")
    print(f"  Vecinos: {graph['adjacency'][node]}")
    
    neighbor_colors = set()
    for neighbor in graph['adjacency'][node]:
        color = coloring[neighbor]
        neighbor_colors.add(color)
        print(f"    Nodo {neighbor} -> Color {color}")
    
    print(f"  Colores vecinos: {neighbor_colors}")
    print(f"  Próximo color disponible: {max(neighbor_colors or {0}) + 1}")
```

---

## Benchmark y Performance

### Medir Tiempo

```python
import time

def benchmark_algorithm(filepath, algorithm_func):
    """Medir tiempo de algoritmo"""
    
    # Cargar
    t0 = time.time()
    graph = load_dimacs_safe(filepath)
    t_load = time.time() - t0
    
    # Ejecutar algoritmo
    t0 = time.time()
    coloring = algorithm_func(graph)
    t_algo = time.time() - t0
    
    # Validar resultado
    t0 = time.time()
    colors_used = validate_coloring(graph, coloring)
    t_validate = time.time() - t0
    
    # Resumen
    print(f"\n{'=' * 50}")
    print(f"Benchmark: {os.path.basename(filepath)}")
    print(f"  Nodos: {graph['n_nodes']}")
    print(f"  Aristas: {graph['n_edges']}")
    print(f"  Densidad: {2 * graph['n_edges'] / (graph['n_nodes'] * (graph['n_nodes'] - 1)):.3f}")
    print(f"{'=' * 50}")
    print(f"Tiempo carga:     {t_load:.4f}s")
    print(f"Tiempo algoritmo: {t_algo:.4f}s")
    print(f"Tiempo validación:{t_validate:.4f}s")
    print(f"Colores usados:   {colors_used}")
    print(f"{'=' * 50}\n")
```

### Validar Coloreo

```python
def validate_coloring(graph, coloring):
    """Validar que el coloreo es correcto"""
    
    colors_used = 0
    
    for u in graph['adjacency']:
        if coloring[u] == 0:
            raise ValueError(f"Nodo {u} sin color")
        
        colors_used = max(colors_used, coloring[u])
        
        # Verificar que vecinos tienen colores diferentes
        for v in graph['adjacency'][u]:
            if coloring[u] == coloring[v]:
                raise ValueError(
                    f"Conflicto: nodos {u} y {v} tienen mismo color {coloring[u]}"
                )
    
    return colors_used
```

---

## 🎯 Checklist Final

Antes de ejecutar tu algoritmo:

- [ ] ✅ Archivo DIMACS válido (con encabezado)
- [ ] ✅ Validación de formato (p edge, rango de nodos)
- [ ] ✅ Validación post-carga (simetría, conteo de aristas)
- [ ] ✅ Estructura de datos apropiada (sparse/dense/híbrida)
- [ ] ✅ Inicialización correcta (índices desde 1)
- [ ] ✅ Sin auto-loops ni duplicados
- [ ] ✅ Memoria estimada < RAM disponible
- [ ] ✅ Validación de resultado (sin conflictos)
- [ ] ✅ Benchmark de tiempo y memoria
- [ ] ✅ Test en instancia pequeña (myciel3, myciel4)

---

## 📚 Referencias

| Recurso | Link |
|---------|------|
| DIMACS Format | [specs](http://dimacs.rutgers.edu/Challenges/) |
| Metadata Dataset | [metadata.json](metadata.json) |
| Instancias Pequeñas | [by_family/MYC/](by_family/MYC/) |
| Loader Utility | [loader.py](loader.py) |
| Estructura Completa | [ESTRUCTURA_BY_FAMILY.md](ESTRUCTURA_BY_FAMILY.md) |

