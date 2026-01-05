Q5: EXPERIMENTO COMPUTACIONAL

OBJETIVO

Evaluar la efectividad, robustez y capacidad de generalización empírica del enfoque de Generación Automática de Algoritmos (GAA) aplicado al VRPTW, donde la lógica algorítmica se optimiza mediante Iterated Local Search (ILS) sobre ASTs. Asimismo, se busca comparar los algoritmos generados automáticamente bajo un marco experimental controlado, reproducible y estadísticamente validado.

PRESUPUESTO COMPUTACIONAL

CONFIGURACIÓN GENERAL

Parámetro | Valor
Ejecuciones independientes del Problema Maestro | 10 runs
Semillas pseudoaleatorias | {42, 43, 44, …}
Número máximo de iteraciones ILS | 100 iteraciones
Evaluaciones por AST | 10 instancias Solomon
Profundidad máxima del AST | 3 niveles
Número máximo de nodos funcionales | 2 nodos internos

Cada ejecución independiente del Problema Maestro utiliza una semilla distinta, manteniéndose controlada para garantizar reproducibilidad y permitir análisis estadístico.

GENERACIÓN Y SELECCIÓN DE ALGORITMOS AUTOMÁTICOS

Durante cada ejecución del Problema Maestro de GAA, el algoritmo ILS explora el espacio de programas (ASTs), partiendo desde un AST inicial y generando sucesivos ASTs vecinos mediante transformaciones estructurales.

Características del procedimiento:

En cada run, ILS genera una secuencia de ASTs candidatos.

Cada AST es evaluado mediante su fitness promedio sobre el conjunto de instancias de diseño.

A lo largo de la ejecución, se mantiene un registro de los mejores ASTs encontrados.

Para efectos de análisis comparativo y reporte experimental:

De cada run se seleccionan los 3 ASTs con mejor desempeño promedio.

Cada uno de estos algoritmos seleccionados se ejecuta múltiples veces sobre los conjuntos de instancias definidos.

El desempeño se evalúa en términos de gap respecto a BKS y variabilidad entre instancias.

El algoritmo final se selecciona considerando desempeño promedio, estabilidad y consistencia global.

Solo el algoritmo ganador es sometido a análisis estructural y cualitativo detallado.

PROTOCOLO EXPERIMENTAL

CONJUNTOS DE INSTANCIAS

El benchmark Solomon se divide en subconjuntos con propósitos metodológicos diferenciados, propios del diseño automático de algoritmos y no de aprendizaje supervisado.

CONJUNTO DE DISEÑO (DESIGN SET)

Instancias:

R1, C1 (18 instancias)

Propósito:
Evaluar el fitness de los ASTs durante la resolución del Problema Maestro mediante ILS y guiar la exploración del espacio de algoritmos.

CONJUNTO DE SELECCIÓN (SELECTION SET)

Instancias:

RC1 (8 instancias)

Propósito:
Comparar algoritmos candidatos y detectar soluciones excesivamente especializadas, privilegiando algoritmos con desempeño estable en distintas clases de instancias.

CONJUNTO DE EVALUACIÓN (EVALUATION SET)

Instancias:

R2, C2, RC2 (30 instancias)

Propósito:
Evaluar de manera independiente el desempeño final del algoritmo seleccionado en instancias no utilizadas durante el proceso de diseño.

No se realiza ajuste específico de parámetros por clase de instancia; el algoritmo inducido se evalúa de forma idéntica en todos los conjuntos.

RESTRICCIONES ESTRUCTURALES DEL AST

Para controlar la complejidad, evitar bloat y favorecer interpretabilidad, se imponen las siguientes restricciones:

Restricción | Valor | Justificación
Profundidad máxima | 3 niveles | Evitar algoritmos excesivamente complejos
Nodos funcionales | ≤ 2 | Favorecer interpretabilidad
Terminales | Solo en hojas | Mantener estructura clara del AST

Estas restricciones se imponen deliberadamente para privilegiar algoritmos compactos, comprensibles y analizables.

MÉTRICAS CANÓNICAS (SOLOMON)

Métrica primaria:

Número de vehículos utilizados (V).
Una solución con menor número de vehículos es siempre preferida, incluso si la distancia total es mayor.

Métrica secundaria:

Distancia total recorrida (D).
Solo se compara entre soluciones con el mismo número de vehículos.

Criterio de comparación:

Orden lexicográfico (V, D).

MÉTRICAS COMPLEMENTARIAS

Gap respecto a BKS: reportado únicamente cuando V(solución) = V(BKS).

Tiempo de ejecución: eficiencia computacional del algoritmo.

Consistencia: desviación estándar del desempeño en el conjunto de evaluación.

Robustez: estabilidad del desempeño entre diferentes clases de instancias.

Cuando V(solución) ≠ V(BKS), la comparación se realiza exclusivamente en términos del número de vehículos, conforme al criterio lexicográfico.

SELECCIÓN Y ANÁLISIS DEL MEJOR ALGORITMO

El algoritmo final se selecciona considerando:

Desempeño promedio (gap medio respecto a BKS en el conjunto de evaluación).

Estabilidad (baja variabilidad entre instancias).

Consistencia entre conjuntos de diseño, selección y evaluación.

Para el algoritmo seleccionado se realiza un análisis cualitativo de su estructura, incluyendo:

funciones utilizadas en el AST,

terminales dominantes,

profundidad real del árbol,

lógica heurística inducida (énfasis temporal, espacial o híbrido).

El objetivo es interpretar el conocimiento heurístico aprendido automáticamente y relacionarlo con la literatura clásica del VRPTW.

VALIDACIÓN ESTADÍSTICA

Dado que las métricas del VRPTW no siguen necesariamente distribuciones normales y las instancias están emparejadas, se emplean métodos estadísticos no paramétricos.

Test de significancia:

Wilcoxon signed-rank para comparaciones pareadas.

Friedman cuando se comparan múltiples algoritmos.

Intervalo de confianza:

95%.

Nivel de significancia:

p-value < 0.05.

RESUMEN EJECUTIVO

Ejecuciones independientes del GAA: 10 runs con semillas distintas.

Metaheurística del Problema Maestro: Iterated Local Search sobre ASTs.

Generación de algoritmos: secuencias de ASTs por run; selección de los mejores.

Evaluación: basada en orden lexicográfico (V, D).

Benchmark: Solomon (C, R, RC).

Restricciones del AST: profundidad ≤ 3, nodos funcionales ≤ 2.

Validación: estadística no paramétrica con 95% de confianza.