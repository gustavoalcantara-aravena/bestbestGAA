# Diagramas de Flujo: GAA, Operadores y AST

**Visualización en ASCII de los flujos de ejecución**

---

## Diagrama 1: Generación de Algoritmos GAA

```
┌─────────────────────────────────────────────────────────────────┐
│                  INICIO EXPERIMENTO (QUICK/FULL)                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│              AlgorithmGenerator(seed=42)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ generate_three_algorithms():                             │  │
│  │                                                          │  │
│  │  FOR i IN [1, 2, 3]:                                    │  │
│  │    ├─ random.seed(42 + i)  ← DETERMINISMO             │  │
│  │    │                                                    │  │
│  │    ├─ generate_with_validation(max_attempts=20)       │  │
│  │    │  └─ LOOP:                                         │  │
│  │    │      ast = generate()  ← Patrón aleatorio        │  │
│  │    │      errors = validate(ast)                      │  │
│  │    │      IF NOT errors: RETURN ast                   │  │
│  │    │                                                   │  │
│  │    ├─ to_dict() → Serialización                       │  │
│  │    ├─ get_statistics() → Metadatos                    │  │
│  │    │                                                   │  │
│  │    └─ Crear dict con:                                 │  │
│  │       id, name, ast, pattern, seed,                  │  │
│  │       timestamp, stats                                │  │
│  │                                                        │  │
│  │  RETORNA: [algo1, algo2, algo3]                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  save_algorithms(algorithms, 'algorithms/')                │
│  └─ Crea JSON files:                                       │
│     ├─ GAA_Algorithm_1.json                               │
│     ├─ GAA_Algorithm_2.json                               │
│     ├─ GAA_Algorithm_3.json                               │
│     └─ _algorithms.json (índice)                          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ↓
                    [Algoritmos generados]
```

---

## Diagrama 2: Selección de Patrones

```
                         generate()
                            │
                   random.choice([...])
                  /          │          \          \
                 /           │           \          \
            25%             25%          25%         25%
           /                │            \           \
    SIMPLE            ITERATIVE       MULTISTART    COMPLEX
      │                  │                │           │
      ↓                  ↓                ↓           ↓
┌─────────────┐  ┌──────────────┐  ┌──────────┐  ┌────────────┐
│ Depth: 2    │  │ Depth: 4     │  │ Depth:3-4│  │ Depth:4-5  │
│ Size: 3     │  │ Size: 6      │  │ Size:4   │  │ Size:7-8   │
│ ⭐          │  │ ⭐⭐         │  │ ⭐⭐    │  │ ⭐⭐⭐    │
│             │  │              │  │          │  │            │
│ Seq(        │  │ Seq(         │  │ For(...) │  │ Seq(      │
│  GreedyC,  │  │  GreedyC,    │  │          │  │  GreedyC, │
│  LocalS    │  │  While(      │  │          │  │  While(   │
│ )          │  │   Seq(       │  │          │  │   If(... )│
│            │  │    LocalS,   │  │          │  │  )        │
│            │  │    Perturb   │  │          │  │ )         │
│            │  │   )          │  │          │  │           │
│            │  │  )           │  │          │  │           │
│            │  │ )            │  │          │  │           │
└─────────────┘  └──────────────┘  └──────────┘  └────────────┘
```

---

## Diagrama 3: Estructura AST Jerárquica

```
                           ASTNode (Base)
                                │
                ┌───────────────┼───────────────┐
                │               │               │
           CONTROL FLOW      OPERATORS       (otros)
                │               │
      ┌─────────┼──────┐    ┌────┼────────┐
      │         │      │    │    │        │
    Seq        If    While  │  LocalS  Perturb
              /  \    │     │    │      │
         then else   body   │    │      │
                     │      │    │      │
                  GreedyC   │    │      │

SIZE & DEPTH CALCULATION:

Seq(
  GreedyConstruct(),              ← depth=1, size=1
  While(
    body=Seq(
      LocalSearch(),              ← depth=1, size=1
      Perturbation()              ← depth=1, size=1
    )
  )
)

Tamaño:
  GreedyConstruct: 1
  LocalSearch: 1
  Perturbation: 1
  Seq(inner): 1 + 1 + 1 = 3
  While: 1 + 3 = 4
  Seq(outer): 1 + 1 + 4 = 6
  ─────────────────────
  TOTAL: 6

Profundidad:
  GreedyConstruct: 1
  Seq(inner): 1 + max(1, 1) = 2
  While: 1 + 2 = 3
  Seq(outer): 1 + max(1, 3) = 4
  ─────────────────────
  TOTAL: 4
```

---

## Diagrama 4: Los 18 Operadores

```
┌──────────────────────────────────────────────────────────────────┐
│                      18 OPERADORES GAA                          │
│                                                                  │
│  CONSTRUCTIVOS (6)        MEJORA (8)         PERTURBACIÓN (4)   │
│  ┌──────────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ 1. NearestNeighbor   │  │ 1. TwoOpt    │  │ 1. RouteRemov  │ │
│  │ 2. Savings           │  │ 2. OrOpt     │  │ 2. WorseFeasib │ │
│  │ 3. Sweep             │  │ 3. ThreeOpt  │  │ 3. RandomReloc │ │
│  │ 4. TimeOrientedNN    │  │ 4. Relocate  │  │ 4. SegmentShif │ │
│  │ 5. RegretInsertion   │  │ 5. Exchange  │  │                │ │
│  │ 6. RandomizedInsert  │  │ 6. GENI      │  │ Usado en:      │ │
│  │                      │  │ 7. LKH       │  │ - ITERATIVE    │ │
│  │ Genera solución      │  │ 8. VND       │  │ - COMPLEX      │ │
│  │ inicial con          │  │              │  │                │ │
│  │ parámetro alpha      │  │ Mejoran      │  │ Diversifican   │ │
│  │                      │  │ solución     │  │ solución       │ │
│  │ Complejidad:         │  │ localmente   │  │                │ │
│  │ O(n²) ~ O(n³)        │  │              │  │ Complejidad:   │ │
│  │                      │  │ Complejidad: │  │ O(n) ~ O(n²)   │ │
│  │                      │  │ O(n²) ~      │  │                │ │
│  │                      │  │ O(n³)        │  │                │ │
│  └──────────────────────┘  └──────────────┘  └────────────────┘ │
│                                                                  │
│  TOTAL: 6 + 8 + 4 = 18 Operadores                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Diagrama 5: Flujo Experimental Completo

```
┌──────────────────────────────────────────────────────────────────┐
│                   EXPERIMENTO RÁPIDO (QUICK)                    │
│                     12 instancias (R1)                          │
└──────────────────────────────────────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ↓                     ↓
         ┌────────────────────┐ ┌─────────────────────┐
         │  GENERAR 3 ALGOS   │ │  CARGAR INSTANCIAS  │
         │  CON GAA           │ │  SOLOMON (R1)       │
         │                    │ │                     │
         │ ✓ simple           │ │ R101.csv            │
         │ ✓ iterative        │ │ R102.csv            │
         │ ✓ simple           │ │ ...                 │
         │ (patterns aleatorios)│ │ R112.csv            │
         │                    │ │ (12 instancias)     │
         └────────────────────┘ └─────────────────────┘
                    │                     │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │  MATRIZ EXPERIMENTAL │
                    │  12 × 3 = 36 CASOS  │
                    └──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ↓                      ↓                      ↓
    ┌────────┐            ┌────────┐            ┌────────┐
    │  GRASP │            │  VND   │            │  ILS   │
    │ × 12   │            │ × 12   │            │ × 12   │
    │ cases  │            │ cases  │            │ cases  │
    └────────┘            └────────┘            └────────┘
        │                      │                      │
        └──────────────┬───────┴──────────┬──────────┘
                       │                  │
                   [36 results]       [36 results]
                       │                  │
                       └──────────┬───────┘
                                  │
                                  ↓
                       ┌────────────────────┐
                       │  raw_results.csv   │
                       │  (36 rows)         │
                       │                    │
                       │ algorithm|instance │
                       │ GRASP|R101        │
                       │ VND|R101          │
                       │ ILS|R101          │
                       │ ...               │
                       └────────────────────┘
                                  │
                    ┌─────────────┼──────────────┐
                    │             │              │
                    ↓             ↓              ↓
            ┌─────────────┐ ┌──────────┐ ┌─────────────┐
            │  GRÁFICOS   │ │ REPORTES │ │ ANÁLISIS    │
            │             │ │          │ │             │
            │ 11 plots    │ │ summary  │ │ Estadísticas│
            │             │ │ report   │ │ Comparativas│
            └─────────────┘ └──────────┘ └─────────────┘
```

---

## Diagrama 6: Ciclo de GRASP (Algoritmo 1)

```
                    GRASP(alpha=0.15, max_iterations=100)
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ↓                       ↓
            ITERACIÓN 1...100
            (repetir 100 veces)

        ┌───────────────────────────────────────┐
        │     ITERACIÓN i (1 a 100)             │
        │                                       │
        │  FASE 1: CONSTRUCCIÓN GREEDY          │
        │  ────────────────────────────          │
        │  ├─ RCL = Restricted Candidate List   │
        │  │  (candidatos buenos: dentro alpha) │
        │  │                                    │
        │  ├─ candidato = random.choice(RCL)   │
        │  │  (NO siempre el mejor)             │
        │  │                                    │
        │  └─ RETORNA: solución inicial         │
        │                                       │
        │  FASE 2: BÚSQUEDA LOCAL                │
        │  ────────────────────────              │
        │  ├─ while mejor mejora encontrada:   │
        │  │   ├─ for arco (i,j):               │
        │  │   │   if 2opt(i,j) mejora:         │
        │  │   │     └─ aplicar mejora          │
        │  │   │                                │
        │  │   └─ RETORNA: óptimo local         │
        │  │                                    │
        │  FASE 3: ACTUALIZAR MEJOR              │
        │  ────────────────────────              │
        │  └─ if solución_actual < mejor_global │
        │       └─ mejor_global = solución      │
        │                                       │
        └───────────────────────────────────────┘
                        │
                        │ (100 veces)
                        │
                        ↓
        ┌─────────────────────────────────────┐
        │  RETORNA: mejor_solution encontrada │
        │                                     │
        │  Output: (k, d, fitness, stats)     │
        │  ─────                              │
        │  k: número de vehículos             │
        │  d: distancia total                 │
        │  fitness: (k, d)                    │
        └─────────────────────────────────────┘
```

---

## Diagrama 7: Ciclo de VND (Algoritmo 2)

```
            VND(Variable Neighborhood Descent)
                          │
        (requiere: solución inicial de GRASP)
                          │
                          ↓
    ┌─────────────────────────────────────────┐
    │  k = 1 (primer vecindario)              │
    │                                         │
    │  ├─ operador_actual = operators[k]     │
    │  │  (ej: TwoOpt)                       │
    │  │                                     │
    │  ├─ search_mejor = buscar mejora       │
    │  │  con operador_actual                │
    │  │                                     │
    │  ├─ if mejora encontrada:              │
    │  │  ├─ solución = search_mejor         │
    │  │  └─ k = 1 (reiniciar)              │
    │  │                                     │
    │  └─ else:                              │
    │      └─ k = k + 1 (siguiente vecindario)
    │                                         │
    └─────────────────────────────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
    ↓                   ↓                   ↓
   k=1               k=2...8            k>8
 TwoOpt            OrOpt/etc.        (terminar)
   │                   │                   │
   └───────────────────┼───────────────────┘
                       │
                       ↓
            ┌──────────────────────┐
            │  ÓPTIMO LOCAL (VND)  │
            │  (mejor que GRASP)   │
            │                      │
            │  Retorna: solución   │
            │           mejorada   │
            └──────────────────────┘
```

---

## Diagrama 8: Ciclo de ILS (Algoritmo 3)

```
        ILS (Iterated Local Search)
        perturbation_strength=3
        max_iterations=100
                    │
                    ↓
    ┌────────────────────────────────┐
    │  solución = GRASP.solve()      │
    │  mejor = solución              │
    └────────────────────────────────┘
                    │
            FOR iteración IN [1..100]:
                    │
        ┌───────────────────────────┐
        │  FASE 1: MEJORA LOCAL    │
        │  ──────────────────────  │
        │  s' = VND.search(s)      │
        │  (búsqueda local completa)
        │                           │
        └───────────────────────────┘
                    │
        ┌───────────────────────────┐
        │  FASE 2: PERTURBACIÓN    │
        │  ──────────────────────  │
        │  if iteración % 5 == 0: │
        │    ├─ perturbador =      │
        │    │  RandomRouteRemoval │
        │    │  strength=3         │
        │    │                     │
        │    └─ s' = perturb(s')   │
        │       (destruir solución │
        │        para escapar)     │
        │                           │
        └───────────────────────────┘
                    │
        ┌───────────────────────────┐
        │  FASE 3: ACEPTACIÓN      │
        │  ──────────────────────  │
        │  if fitness(s') <        │
        │     fitness(mejor):      │
        │    └─ mejor = s'         │
        │                           │
        │  s = s'                   │
        │                           │
        └───────────────────────────┘
                    │
        (100 iteraciones)
                    │
                    ↓
    ┌────────────────────────────────┐
    │  RETORNA: mejor solución      │
    │                               │
    │  (típicamente mejor que       │
    │   GRASP y VND)               │
    └────────────────────────────────┘
```

---

## Diagrama 9: Matriz de Resultados

```
┌──────────────────────────────────────────────────────────────┐
│                    raw_results.csv                          │
│  ────────────────────────────────────────────────────────   │
│  algorithm | instance | family | k_final | d_final | time  │
│  ─────────────────────────────────────────────────────────  │
│  GRASP     | R101     | R1     | 11      | 1234.5  | 2.34  │
│  VND       | R101     | R1     | 10      | 1210.2  | 3.21  │
│  ILS       | R101     | R1     | 10      | 1198.7  | 5.45  │
│  ─────────────────────────────────────────────────────────  │
│  GRASP     | R102     | R1     | 12      | 1345.2  | 2.51  │
│  VND       | R102     | R1     | 11      | 1298.1  | 3.45  │
│  ILS       | R102     | R1     | 10      | 1256.3  | 5.67  │
│  ─────────────────────────────────────────────────────────  │
│  ...       | ...      | ...    | ...     | ...     | ...   │
│  ─────────────────────────────────────────────────────────  │
│  GRASP     | R112     | R1     | 10      | 1089.3  | 2.12  │
│  VND       | R112     | R1     | 10      | 1056.7  | 3.78  │
│  ILS       | R112     | R1     | 9       | 1023.4  | 6.23  │
│                                                              │
│  TOTAL FILAS: 36 (12 instancias × 3 algoritmos)           │
└──────────────────────────────────────────────────────────────┘

ANÁLISIS:
  ├─ ILS típicamente mejor que VND, VND mejor que GRASP
  ├─ VND ~50% más rápido que ILS
  ├─ GRASP más rápido (~2.3s promedio)
  ├─ ILS más lento (~5.6s promedio) pero mejor calidad
  └─ Consistencia verificable: reproducible con seed=42
```

---

## Diagrama 10: Árbol de Decisión de Operadores

```
                    CONSTRUCTOR HEURISTIC?
                           │
           ┌───────────────┼───────────────┐
           │               │               │
        Greedy        Insertion        Sweep
           │               │               │
           ├─NN            ├─Regret       └─ Sweep
           └─Savings       ├─Random        └─ TimeOrient
                           └─...

           ↓ CONSTRUCCIÓN INICIAL

                    LOCAL SEARCH?
                           │
           ┌───────────────┼───────────────┐
           │               │               │
        Basic          Advanced         Meta
           │               │               │
           ├─ 2opt         ├─ GENI        └─ VND
           ├─ OrOpt        ├─ LKH         
           ├─ Relocate     └─ 3opt
           └─ Exchange

           ↓ OPTIMIZACIÓN LOCAL

           ┌─ PATRÓN SIMPLE?
           │  └─ STOP
           │
           └─ PATRÓN ITERATIVO/COMPLEX?
              │
              ↓
              
                    PERTURBATION?
                           │
           ┌───────────────┼───────────────┐
           │               │               │
        Low Power      Medium Power    High Power
           │               │               │
           ├─ Random       ├─ Segment      └─ RouteRemov
           │  Relocate     │  Shift
           └─ ...          └─ Worse
                            Feasible

           ↓ DIVERSIFICACIÓN

           ─────────────────────────
           [Vuelve a búsqueda local]
           ─────────────────────────
```

---

**Estos diagramas muestran la estructura y flujo completo del sistema GAA integrado con los operadores VRPTW.**

