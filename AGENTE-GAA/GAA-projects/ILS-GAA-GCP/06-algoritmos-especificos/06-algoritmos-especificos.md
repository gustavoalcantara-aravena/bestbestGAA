# OJO NO ME CONVENCE MUCHOOO



Q6: TRES ALGORITMOS ESPECÍFICOS DE REFERENCIA (GCP)

INTRODUCCIÓN

Este documento define tres algoritmos heurísticos concretos que se utilizan como algoritmos de referencia (baselines) durante la experimentación del marco GAA–GCP, donde la lógica algorítmica es optimizada mediante Iterated Local Search (ILS) sobre ASTs.

Estos algoritmos representan estrategias clásicas y bien establecidas en la literatura del Graph Coloring Problem, y cumplen dos propósitos principales:

Servir como puntos de comparación cuantitativa frente a los algoritmos generados automáticamente por el GAA.

Proveer estructuras semilla y patrones de diseño que el sistema GAA puede eventualmente redescubrir, combinar o mejorar.

IMPORTANTE

Estos algoritmos NO son optimizados ni modificados por el proceso de GAA.

Se implementan como heurísticas fijas, con estructura y parámetros constantes.

Se expresan como ASTs definidos manualmente, utilizando el mismo DSL del GAA, garantizando comparabilidad estructural directa.

ALGORITMO 1: BASELINE CONSTRUCTIVO PURO

Nombre largo:
Greedy Sequential Graph Coloring

Acrónimo:
ALGO-1-GREEDY

DESCRIPCIÓN

Algoritmo puramente constructivo que asigna colores a los vértices de forma secuencial utilizando un criterio voraz simple. Cada vértice recibe el menor color disponible que no genere conflictos con sus vecinos previamente coloreados.

No incluye ninguna fase de búsqueda local ni refinamiento posterior.

CARACTERÍSTICAS PRINCIPALES

Algoritmo simple y rápido

Determinista con semilla fijada

Calidad de solución limitada

Utilizado como baseline inferior

ESTRUCTURA AST (FIJA)

Seq
→ OrderVertices
→ GreedyColoring

(No incluye búsqueda local)

TERMINALES UTILIZADOS

Degree(v)

AdjacentColors(v)

FUNCIONES UTILIZADAS

Seq

OrderVertices

GreedyColoring

PARÁMETROS DE EJECUCIÓN

Número de iteraciones: 1

Tiempo máximo por instancia: 10 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

DESEMPEÑO ESPERADO (ORIENTATIVO)

C1: +3 a +6 colores sobre BKS
C2: +2 a +4 colores
R1: +4 a +7 colores
R2: +1 a +3 colores
RC1: +3 a +6 colores
RC2: +2 a +4 colores

ROL EN EL EXPERIMENTO

Baseline inferior

Validación del pipeline experimental

Punto de referencia mínimo aceptable

ALGORITMO 2: CONSTRUCTIVO + BÚSQUEDA LOCAL SIMPLE

Nombre largo:
DSATUR with Local Search Refinement

Acrónimo:
ALGO-2-DSATUR-LS

DESCRIPCIÓN

Algoritmo basado en el heurístico DSATUR, que prioriza vértices con mayor grado de saturación durante la fase constructiva. Posteriormente, aplica una búsqueda local simple basada en recoloración de vértices conflictivos.

CARACTERÍSTICAS PRINCIPALES

Buen manejo de restricciones locales

Calidad intermedia

Determinista con semilla fijada

Combina construcción informada y refinamiento local

ESTRUCTURA AST (FIJA)

Seq
→ DSATURConstruct
→ LocalSearch (Recoloring)

TERMINALES UTILIZADOS

SaturationDegree(v)

Degree(v)

Conflicts(v)

FUNCIONES UTILIZADAS

Seq

DSATURConstruct

LocalSearch

RecolorVertex

PARÁMETROS DE EJECUCIÓN

Construcción: 1 iteración

Búsqueda local: hasta 50 iteraciones

Tiempo máximo por instancia: 30 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

DESEMPEÑO ESPERADO (ORIENTATIVO)

C1: +2 a +4 colores
C2: +1 a +3 colores
R1: +2 a +4 colores
R2: +1 a +2 colores
RC1: +2 a +4 colores
RC2: +1 a +3 colores

ROL EN EL EXPERIMENTO

Baseline medio

Referencia para grafos con alta densidad local

Validación de la combinación constructivo + búsqueda local

ALGORITMO 3: ALGORITMO HÍBRIDO CON PERTURBACIÓN (ILS CLÁSICO)

Nombre largo:
Hybrid Coloring with Iterated Local Search and Kempe Chains

Acrónimo:
ALGO-3-ILS-KEMPE

DESCRIPCIÓN

Algoritmo híbrido que combina una fase constructiva basada en DSATUR con una búsqueda local intensiva y un mecanismo de perturbación mediante Cadenas de Kempe, siguiendo el esquema clásico de Iterated Local Search.

CARACTERÍSTICAS PRINCIPALES

Algoritmo robusto y versátil

Adecuado para grafos de distinta estructura y densidad

Representa un baseline superior

Inspiración directa para el proceso GAA

ESTRUCTURA AST (FIJA)

Seq
→ DSATURConstruct
→ IteratedLocalSearch
  → LocalSearch (Recoloring)
  → Perturbation (KempeChain)

TERMINALES UTILIZADOS

SaturationDegree(v)

Degree(v)

Conflicts(v)

ColorClassSize(c)

FUNCIONES UTILIZADAS

Seq

DSATURConstruct

IteratedLocalSearch

LocalSearch

RecolorVertex

KempeChain

PARÁMETROS DE EJECUCIÓN

Construcción: 1 iteración

Búsqueda local: hasta 100 iteraciones

Perturbación: 1 cadena de Kempe por estancamiento

Tiempo máximo por instancia: 60 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

DESEMPEÑO ESPERADO (ORIENTATIVO)

C1: +1 a +3 colores
C2: +1 a +2 colores
R1: +1 a +3 colores
R2: 0 a +1 color
RC1: +1 a +2 colores
RC2: +1 a +2 colores

ROL EN EL EXPERIMENTO

Baseline superior

Referencia aspiracional

Benchmark directo para evaluar el GAA

INTERPRETACIÓN PARA EL GAA

Estos algoritmos de referencia permiten evaluar si el proceso de Generación Automática de Algoritmos es capaz de:

Redescubrir patrones heurísticos clásicos (DSATUR, recoloración, Kempe).

Combinar construcción, búsqueda local y perturbación de forma efectiva.

Superar heurísticas manuales bien diseñadas en términos de número de colores y robustez.

Se espera que el algoritmo generado automáticamente por el GAA alcance o supere el desempeño de ALGO-3-ILS-KEMPE, especialmente en instancias mixtas y estructuralmente complejas.