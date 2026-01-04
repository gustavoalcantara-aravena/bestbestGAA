Q5: Experimento Computacional
Objetivo

Evaluar la efectividad, robustez y capacidad de generalización empírica del enfoque de Generación Automática de Algoritmos (GAA) aplicado al VRPTW, así como comparar los algoritmos generados automáticamente bajo un marco experimental controlado y reproducible.

Presupuesto Computacional
Configuración General
Parámetro	Valor
Ejecuciones independientes del Problema Maestro	10 runs
Semillas pseudoaleatorias	{42, 43, 44, …}
Profundidad máxima del AST	3 niveles
Número máximo de nodos funcionales	2 nodos internos

Cada ejecución independiente utiliza una semilla distinta, manteniéndose controlada para garantizar reproducibilidad y permitir análisis estadístico.

Generación y Selección de Algoritmos Automáticos

Durante cada ejecución del Problema Maestro de GAA se explora el espacio de programas (AST), generándose múltiples algoritmos candidatos.

Para efectos de análisis comparativo y reporte experimental, se seleccionan los tres algoritmos con mejor desempeño promedio por ejecución, de acuerdo con la función de fitness definida.

Características del procedimiento:

En cada run del GAA se generan múltiples AST candidatos.

De cada run se seleccionan los 3 algoritmos con mejor fitness.

Cada algoritmo seleccionado se ejecuta múltiples veces sobre los conjuntos de instancias definidos.

El desempeño se evalúa mediante gap promedio respecto a BKS y variabilidad entre instancias.

El algoritmo final se selecciona considerando desempeño promedio, estabilidad y consistencia entre conjuntos de instancias.

Solo el algoritmo ganador es sometido a análisis estructural y cualitativo detallado.

Protocolo Experimental
Conjuntos de Instancias

El benchmark Solomon se divide en subconjuntos con propósitos metodológicos diferenciados, propios del diseño automático de algoritmos y no de aprendizaje supervisado.

Conjunto de Diseño (Design Set)

Instancias: R1, C1 (18 instancias)

Propósito: Evaluar el fitness de los AST durante la resolución del Problema Maestro y guiar la exploración del espacio de algoritmos.

Conjunto de Selección (Selection Set)

Instancias: RC1 (8 instancias)

Propósito: Comparar algoritmos candidatos y detectar soluciones excesivamente especializadas, privilegiando algoritmos con desempeño estable en distintas clases de instancias.

Conjunto de Evaluación (Evaluation Set)

Instancias: R2, C2, RC2 (30 instancias)

Propósito: Evaluar de manera independiente el desempeño final del algoritmo seleccionado en instancias no utilizadas durante el proceso de diseño.

No se realiza ajuste específico de parámetros por clase de instancia; el algoritmo inducido se evalúa de forma idéntica en todos los conjuntos.

Restricciones Estructurales del AST

Para controlar la complejidad, evitar bloat y favorecer interpretabilidad, se imponen las siguientes restricciones:

Restricción	Valor	Justificación
Profundidad máxima	3 niveles	Evitar árboles excesivamente complejos
Nodos funcionales	≤ 2	Priorizar interpretabilidad
Terminales	Solo en hojas	Estructura clara del AST

Estas restricciones se imponen deliberadamente para privilegiar algoritmos compactos y comprensibles sobre soluciones altamente complejas.

Métricas Canónicas (Solomon)

Métrica primaria:
Número de vehículos utilizados (V).
Una solución con menor número de vehículos es siempre preferida, incluso si la distancia total es mayor.

Métrica secundaria:
Distancia total recorrida (D).
Solo se compara entre soluciones con el mismo número de vehículos.

Criterio de comparación:
Orden lexicográfico (V, D).

Métricas Complementarias

Gap respecto a BKS: se reporta únicamente cuando V(solución) = V(BKS).

Tiempo de ejecución: métrica de eficiencia computacional.

Consistencia: desviación estándar del desempeño en el conjunto de evaluación.

Robustez: estabilidad del desempeño entre diferentes clases de instancias.

Cuando V(solución) ≠ V(BKS), la comparación se realiza exclusivamente en términos del número de vehículos, conforme al criterio lexicográfico.

Selección y Análisis del Mejor Algoritmo

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

Validación Estadística

Dado que las métricas del VRPTW no siguen necesariamente distribuciones normales y las instancias están emparejadas, se emplean métodos estadísticos no paramétricos.

Test de significancia: Wilcoxon signed-rank o Friedman, según corresponda.

Intervalos de confianza: 95%.

Nivel de significancia: p-value < 0.05.

Resumen Ejecutivo

Ejecuciones independientes del GAA: 10 runs con semillas distintas.

Generación de algoritmos: múltiples AST por run; selección de los mejores.

Evaluación: basada en orden lexicográfico (V, D).

Benchmark: Solomon (C, R, RC).

Restricciones del AST: profundidad ≤ 3, nodos funcionales ≤ 2.

Validación: estadística no paramétrica con 95% de confianza.