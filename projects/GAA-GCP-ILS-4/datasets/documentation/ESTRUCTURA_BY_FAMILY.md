# Estructura de by_family/

## Descripción General

La carpeta `by_family/` organiza los 79 archivos DIMACS (.col) por familia de instancias. Cada subfamilia tiene su propia carpeta con los archivos pertinentes.

```
by_family/
├── CUL/          (6 archivos)
├── DSJ/          (15 archivos)
├── LEI/          (12 archivos)
├── MYC/          (5 archivos)
├── REG/          (13 archivos)
├── SCH/          (2 archivos)
└── SGB/          (24 archivos)
    ├── Book_graphs/     (5 archivos)
    ├── Game_graph/      (1 archivo)
    ├── Miles_graphs/    (5 archivos)
    └── Queen_graphs/    (13 archivos)
```

---

## Familias (Nivel 1)

### 1. **CUL** - Quasi-random Coloring (6 archivos)

Grafos de coloreo cuasi-aleatorios generados por Culberson.

**Ubicación:** `by_family/CUL/`

**Archivos:**
```
flat300_20_0.col     (300 nodos)
flat300_26_0.col     (300 nodos)
flat300_28_0.col     (300 nodos)
flat1000_50_0.col    (1000 nodos)
flat1000_60_0.col    (1000 nodos)
flat1000_76_0.col    (1000 nodos)
```

**Características:**
- Rango de densidad variable
- Tamaños: 300 y 1000 nodos
- Parámetro en nombre indica densidad

---

### 2. **DSJ** - Random Graphs (Johnson) (15 archivos)

Grafos aleatorios generados según el modelo Johnson.

**Ubicación:** `by_family/DSJ/`

**Archivos:**
```
DSJC125.1.col        (125 nodos, p=0.1)
DSJC125.5.col        (125 nodos, p=0.5)
DSJC125.9.col        (125 nodos, p=0.9)
DSJC250.1.col        (250 nodos, p=0.1)
DSJC250.5.col        (250 nodos, p=0.5)
DSJC250.9.col        (250 nodos, p=0.9)
DSJC500.1.col        (500 nodos, p=0.1)
DSJC500.5.col        (500 nodos, p=0.5)
DSJC500.9.col        (500 nodos, p=0.9)
DSJC1000.1.col       (1000 nodos, p=0.1)
DSJC1000.5.col       (1000 nodos, p=0.5)
DSJC1000.9.col       (1000 nodos, p=0.9)
DSJR500.1.col        (500 nodos, regular, p=0.1)
DSJR500.1c.col       (500 nodos, regular, coloreable)
DSJR500.5.col        (500 nodos, regular, p=0.5)
```

**Características:**
- Nomenclatura: `DSJC<nodos>.<probabilidad>.col`
- Variaciones regulares: `DSJR` (regular)
- Probabilidades: 0.1 (sparse), 0.5 (dense), 0.9 (very dense)

---

### 3. **LEI** - Leighton Graphs (12 archivos)

Grafos de Leighton, derivados de coloreo de planos.

**Ubicación:** `by_family/LEI/`

**Archivos:**
```
le450_5a.col         (450 nodos, variante a)
le450_5b.col         (450 nodos, variante b)
le450_5c.col         (450 nodos, variante c)
le450_5d.col         (450 nodos, variante d)
le450_15a.col        (450 nodos, variante a)
le450_15b.col        (450 nodos, variante b)
le450_15c.col        (450 nodos, variante c)
le450_15d.col        (450 nodos, variante d)
le450_25a.col        (450 nodos, variante a)
le450_25b.col        (450 nodos, variante b)
le450_25c.col        (450 nodos, variante c)
le450_25d.col        (450 nodos, variante d)
```

**Características:**
- 450 nodos cada uno
- Nomenclatura: `le450_<parámetro><variante>.col`
- Variantes: a, b, c, d
- Basados en coloreos de mapas planos

---

### 4. **MYC** - Mycielski Graphs (5 archivos)

Grafos de Mycielski: triángulo-libres con número cromático creciente.

**Ubicación:** `by_family/MYC/`

**Archivos:**
```
myciel3.col          (11 nodos)
myciel4.col          (23 nodos)
myciel5.col          (47 nodos)
myciel6.col          (95 nodos)
myciel7.col          (191 nodos)
```

**Características:**
- Libres de triángulos (clique number = 2)
- Número cromático creciente: 4, 5, 6, 7, 8
- Propiedad teórica importante: ausencia de cliques grandes ≠ bajo número cromático

---

### 5. **REG** - Register Allocation (13 archivos)

Grafos derivados de problemas de asignación de registros en compiladores.

**Ubicación:** `by_family/REG/`

**Archivos:**
```
fpsol2.i.1.col
fpsol2.i.2.col
fpsol2.i.3.col
inithx.i.1.col
inithx.i.2.col
inithx.i.3.col
mulsol.i.1.col
mulsol.i.2.col
mulsol.i.3.col
mulsol.i.4.col
mulsol.i.5.col
zeroin.i.1.col
zeroin.i.2.col
zeroin.i.3.col
```

**Características:**
- Subfamilias: fpsol2, inithx, mulsol, zeroin
- Origen: benchmarks reales de compiladores
- Variantes numeradas (.1, .2, .3, etc.)

---

### 6. **SCH** - School Scheduling (2 archivos)

Grafos de programación/horarios escolares.

**Ubicación:** `by_family/SCH/`

**Archivos:**
```
school1.col          (problema de horario escolar)
school1_nsh.col      (variante sin horario fijo)
```

**Características:**
- Pequeño conjunto de instancias prácticas
- Origen: problemas de calendarización real
- Aplicación directa: asignación de aulas

---

### 7. **SGB** - Stanford GraphBase (24 archivos)

Colección de grafos de la Stanford GraphBase, subdivididos en 4 subcategorías.

**Ubicación:** `by_family/SGB/`

#### **SGB/Book_graphs/** (5 archivos)

Grafos basados en personajes de obras literarias.

```
anna.col             (86 nodos)
david.col            (87 nodos)
homer.col            (87 nodos)
huck.col             (74 nodos)
jean.col             (77 nodos)
```

**Características:**
- Conexiones entre personajes en obras literarias
- Tamaño pequeño (74-87 nodos)
- Origen: análisis de redes en literatura

#### **SGB/Game_graph/** (1 archivo)

Grafo de juego.

```
games120.col         (120 nodos)
```

**Características:**
- Grafo de posiciones en un juego
- Conexiones basadas en movimientos posibles

#### **SGB/Miles_graphs/** (5 archivos)

Grafos de distancias entre ciudades.

```
miles250.col         (128 nodos)
miles500.col         (128 nodos)
miles750.col         (128 nodos)
miles1000.col        (128 nodos)
miles1500.col        (128 nodos)
```

**Características:**
- Basados en mapa de ciudades USA
- Número indica umbral de distancia (millas)
- Todos con 128 ciudades
- Origen: problema del viajante

#### **SGB/Queen_graphs/** (13 archivos)

Grafos del problema de las N-Reinas (Queen graphs).

```
queen5_5.col         (5x5 tablero = 25 nodos)
queen6_6.col         (6x6 tablero = 36 nodos)
queen7_7.col         (7x7 tablero = 49 nodos)
queen8_8.col         (8x8 tablero = 64 nodos)
queen8_12.col        (8x12 tablero = 96 nodos)
queen9_9.col         (9x9 tablero = 81 nodos)
queen10_10.col       (10x10 tablero = 100 nodos)
queen11_11.col       (11x11 tablero = 121 nodos)
queen12_12.col       (12x12 tablero = 144 nodos)
queen13_13.col       (13x13 tablero = 169 nodos)
queen14_14.col       (14x14 tablero = 196 nodos)
queen15_15.col       (15x15 tablero = 225 nodos)
queen16_16.col       (16x16 tablero = 256 nodos)
```

**Características:**
- Nomenclatura: `queen<filas>_<columnas>.col`
- Nodos = filas × columnas
- Aristas: dos celdas conectadas si una reina puede atacar a la otra
- Aplicación clásica: problema de las N-Reinas

---

## Distribución Total

| Familia | Subcategorías | Archivos | Tamaño (nodos) |
|---------|---------------|----------|----------------|
| CUL     | -             | 6        | 300-1000       |
| DSJ     | -             | 15       | 125-1000       |
| LEI     | -             | 12       | 450            |
| MYC     | -             | 5        | 11-191         |
| REG     | -             | 13       | Variable       |
| SCH     | -             | 2        | Variable       |
| SGB     | 4 (Book, Game, Miles, Queen) | 24 | 25-256 |
| **TOTAL** | **11 tipos** | **79**   | **11-1000**    |

---

## Cómo Usar Esta Estructura

### Acceso Programático (loader.py)

```python
from loader import InstanceLoader

loader = InstanceLoader()

# Obtener todas las instancias de una familia
dsj_instances = loader.get_by_source('DSJ')

# Obtener instancias por dificultad
hard_instances = loader.get_by_difficulty('hard')

# Filtrar por múltiples criterios
large_queens = loader.filter(source='SGB', difficulty='hard', min_nodes=100)
```

### Acceso Manual

1. **Por familia:** Ve directamente a `by_family/<FAMILIA>/`
2. **Busca instancias:** `metadata.json` lista todas con propiedades
3. **Descubre archivos:** Los nombres de archivos indican sus parámetros

---

## Notas Importantes

- **Raw vs Organized:** 
  - `raw/` contiene todos los 79 archivos sin organizar
  - `by_family/` proporciona vista organizada por familia
  
- **SGB Especial:**
  - Única familia con subcarpetas adicionales
  - Organizadas por tipo de grafo (Book, Game, Miles, Queen)
  
- **Naming Conventions:**
  - DSJ: `DSJC<nodos>.<prob>` o `DSJR<nodos>.<prob>`
  - LEI: `le450_<param><var>`
  - MYC: `myciel<num>`
  - SGB depends on subcategory
  
- **Metadata Reference:**
  - Consulta `metadata.json` para optimal values y bounds
  - Usa `loader.py` para acceso programático

