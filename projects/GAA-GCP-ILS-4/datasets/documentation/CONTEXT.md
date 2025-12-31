# Graph Coloring Instances - Documentación Completa

## Formato de Instancias

Las instancias de coloreo de grafos están en formato DIMACS estándar:

- **`.col`**: Formato ASCII (texto plano)
- **`.col.b`**: Formato comprimido/binario (requiere traducción a ASCII)

Existe un traductor disponible para convertir entre formatos ASCII y binario.

## Estructura de Información

Cada instancia incluye la siguiente información:

```
(nodes, edges), coloring_value, source_code
```

Donde:
- **nodes**: Número de vértices en el grafo
- **edges**: Número de aristas en el grafo
- **coloring_value**: Número cromático conocido o mejor valor encontrado (ver nota abajo)
- **source_code**: Código de la fuente del grafo (DSJ, CUL, REG, LEI, SCH, LAT, SGB, MYC)

### Nota sobre los valores de coloreo

**Los valores mostrados son los mejores valores conocidos / valores óptimos encontrados hasta la fecha**, no necesariamente valores garantizados como óptimos en todos los casos. Los `?` indican que no se conoce el valor óptimo exacto o no ha sido determinado.

---

## Instancias por Tipo

### DSJ - Random Graphs (David Johnson)

Grafos aleatorios utilizados en la investigación de Johnson et al. sobre "Optimization by Simulated Annealing" (1991).

**Características:**
- DSJC: Grafos aleatorios estándar $(n,p)$ con probabilidad de arista $p$
- DSJR: Grafos geométricos
- DSJR...c: Complementos de grafos geométricos

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| DSJC125.1 | 125 | 1,472 | ? |
| DSJC125.5 | 125 | 7,782 | ? |
| DSJC125.9 | 125 | 13,922 | ? |
| DSJC250.1 | 250 | 6,436 | ? |
| DSJC250.5 | 250 | 31,366 | ? |
| DSJC250.9 | 250 | 55,794 | ? |
| DSJC500.1 | 500 | 24,916 | ? |
| DSJC500.5 | 500 | 125,249 | ? |
| DSJC500.9 | 500 | 224,874 | ? |
| DSJC1000.1 | 1,000 | 99,258 | ? |
| DSJC1000.5 | 1,000 | 499,652 | ? |
| DSJC1000.9 | 1,000 | 898,898 | ? |
| DSJR500.1 | 500 | 7,110 | ? |
| DSJR500.1c | 500 | 242,550 | ? |
| DSJR500.5 | 500 | 117,724 | ? |

---

### CUL - Quasi-Random Coloring Problems (Joe Culberson)

Problemas de coloreo cuasi-aleatorios con una estructura específica.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| flat300_20_0 | 300 | 21,375 | 20 |
| flat300_26_0 | 300 | 21,633 | 26 |
| flat300_28_0 | 300 | 21,695 | 28 |
| flat1000_50_0 | 1,000 | 245,000 | 50 |
| flat1000_60_0 | 1,000 | 245,830 | 60 |
| flat1000_76_0 | 1,000 | 246,708 | 76 |

---

### REG - Register Allocation (Gary Lewandowski)

Problemas basados en asignación de registros para variables en códigos reales.

**Aplicación práctica:** Optimización de compiladores y asignación de registros en arquitecturas de procesadores.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| fpsol2.i.1 | 496 | 11,654 | 65 |
| fpsol2.i.2 | 451 | 8,691 | 30 |
| fpsol2.i.3 | 425 | 8,688 | 30 |
| inithx.i.1 | 864 | 18,707 | 54 |
| inithx.i.2 | 645 | 13,979 | 31 |
| inithx.i.3 | 621 | 13,969 | 31 |
| mulsol.i.1 | 197 | 3,925 | 49 |
| mulsol.i.2 | 188 | 3,885 | 31 |
| mulsol.i.3 | 184 | 3,916 | 31 |
| mulsol.i.4 | 185 | 3,946 | 31 |
| mulsol.i.5 | 186 | 3,973 | 31 |
| zeroin.i.1 | 211 | 4,100 | 49 |
| zeroin.i.2 | 211 | 3,541 | 30 |
| zeroin.i.3 | 206 | 3,540 | 30 |

---

### LEI - Leighton Graphs (Craig Morgenstern)

Grafos de Leighton con tamaño de coloreo garantizado.

**Referencia académica:** F.T. Leighton, Journal of Research of the National Bureau of Standards, 84: 489-505 (1979).

**Características:** Estos grafos tienen garantías teóricas sobre el número cromático.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| le450_5a | 450 | 5,714 | 5 |
| le450_5b | 450 | 5,734 | 5 |
| le450_5c | 450 | 9,803 | 5 |
| le450_5d | 450 | 9,757 | 5 |
| le450_15a | 450 | 8,168 | 15 |
| le450_15b | 450 | 8,169 | 15 |
| le450_15c | 450 | 16,680 | 15 |
| le450_15d | 450 | 16,750 | 15 |
| le450_25a | 450 | 8,260 | 25 |
| le450_25b | 450 | 8,263 | 25 |
| le450_25c | 450 | 17,343 | 25 |
| le450_25d | 450 | 17,425 | 25 |

---

### SCH - Class Scheduling Graphs (Gary Lewandowski)

Grafos de programación de horarios escolares con y sin aulas de estudio.

**Aplicación práctica:** Generación automática de horarios educativos.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| school1 | 385 | 19,095 | ? |
| school1_nsh | 352 | 14,612 | ? |

---

### LAT - Latin Square Problem (Gary Lewandowski)

Problema de cuadrado latino.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| latin_square_10 | 900 | 307,350 | ? |

---

### SGB - Stanford GraphBase (Michael Trick / Donald Knuth)

Grafos de la colección Stanford GraphBase de Donald Knuth. Se dividen en varias categorías:

#### Book Graphs (Grafos de Literatura)

Cada nodo representa un personaje, y las aristas conectan personajes que se encuentran en el libro.

| Instancia | Nodos | Aristas | Mejor Coloreo | Obra Literaria |
|-----------|-------|---------|---------------|----------------|
| anna | 138 | 493 | 11 | Anna Karenina (Tolstoy) |
| david | 87 | 406 | 11 | David Copperfield (Dickens) |
| homer | 561 | 1,629 | 13 | La Ilíada (Homer) |
| huck | 74 | 301 | 11 | Las Aventuras de Huckleberry Finn (Twain) |
| jean | 80 | 254 | 10 | Los Miserables (Hugo) |

#### Game Graphs (Grafos de Juegos)

Representa los partidos de fútbol americano universitario (temporada 1990).

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| games120 | 120 | 638 | 9 |

#### Miles Graphs (Grafos de Distancias)

Los nodos representan ciudades estadounidenses, y las aristas conectan ciudades cercanas (distancia por carretera en millas de 1947).

**Característica:** A diferencia de los grafos geométricos aleatorios, estos tienen una base geográfica real.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| miles250 | 128 | 387 | 8 |
| miles500 | 128 | 1,170 | 20 |
| miles750 | 128 | 2,113 | 31 |
| miles1000 | 128 | 3,216 | 42 |
| miles1500 | 128 | 5,198 | 73 |

#### Queen Graphs (Grafos de la Reina)

Dado un tablero de ajedrez de $n \times n$, cada nodo corresponde a una casilla. Dos nodos están conectados si sus casillas correspondientes comparten fila, columna o diagonal.

**Interpretación Natural:** El problema de coloreo equivale a: ¿Es posible colocar $n$ conjuntos de $n$ reinas en el tablero sin que dos reinas del mismo conjunto se ataquen entre sí? La respuesta es sí si y solo si el grafo tiene número cromático $n$.

**Teorema de Martin Gardner:** El número cromático es $n$ si y solo si $n$ no es divisible por 2 ni por 3.

**Cotas:** 
- Clique máximo ≤ $n$
- Número cromático ≥ $n$

| Instancia | Nodos | Aristas | Mejor Coloreo | Tablero |
|-----------|-------|---------|---------------|---------| 
| queen5_5 | 25 | 160 | 5 | 5×5 |
| queen6_6 | 36 | 290 | 7 | 6×6 |
| queen7_7 | 49 | 476 | 7 | 7×7 |
| queen8_8 | 64 | 728 | 9 | 8×8 |
| queen8_12 | 96 | 1,368 | 12 | 8×12 |
| queen9_9 | 81 | 2,112 | 10 | 9×9 |
| queen10_10 | 100 | 2,940 | ? | 10×10 |
| queen11_11 | 121 | 3,960 | 11 | 11×11 |
| queen12_12 | 144 | 5,192 | ? | 12×12 |
| queen13_13 | 169 | 6,656 | 13 | 13×13 |
| queen14_14 | 196 | 8,372 | ? | 14×14 |
| queen15_15 | 225 | 10,360 | ? | 15×15 |
| queen16_16 | 256 | 12,640 | ? | 16×16 |

---

### MYC - Mycielski Graphs (Michael Trick)

Grafos basados en la transformación de Mycielski.

**Características especiales:**
- **Libres de triángulos** (clique number = 2)
- **Número cromático creciente:** A pesar de no tener triángulos, el número cromático aumenta con el tamaño del problema
- **Difíciles de resolver:** Desafío importante para algoritmos de coloreo

**Significado teórico:** Demuestran que la ausencia de cliques grandes no implica que el número cromático sea pequeño.

| Instancia | Nodos | Aristas | Mejor Coloreo |
|-----------|-------|---------|---------------|
| myciel3 | 11 | 20 | 4 |
| myciel4 | 23 | 71 | 5 |
| myciel5 | 47 | 236 | 6 |
| myciel6 | 95 | 755 | 7 |
| myciel7 | 191 | 2,360 | 8 |

---

## Resumen Estadístico

- **Total de instancias:** 81
- **Rango de tamaño:** Desde 11 nodos (myciel3) hasta 1,000 nodos (DSJC1000.x)
- **Rango de densidad:** Desde grafos dispersos (miles250) hasta grafos densos (latin_square_10)
- **Categorías:** 8 tipos diferentes de grafos con orígenes teóricos y prácticos variados

---

## Referencias

- **Fuente Principal:** https://mat.tepper.cmu.edu/COLOR/instances.html
- **Repositorio GitHub:** https://github.com/BartMassey/instances
- **Especificación DIMACS:** Ver archivo `ccformat.pdf`
