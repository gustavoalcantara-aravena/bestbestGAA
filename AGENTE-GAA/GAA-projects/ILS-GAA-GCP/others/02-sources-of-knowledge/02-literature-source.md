Modelado y Resolución del Problema de Coloreado de Grafos: Una Perspectiva Metaheurística para la Generación Automática de Algoritmos
1. Introducción: El Paradigma de la Generación Automática en la Optimización Combinatoria
La optimización combinatoria ha transitado históricamente desde el diseño artesanal de algoritmos específicos para problemas concretos hacia una era de abstracción y automatización sin precedentes. En el centro de esta evolución se encuentra el Problema de Coloreado de Grafos (Graph Coloring Problem, GCP), un desafío matemático que no solo sirve como banco de pruebas (benchmark) fundamental para nuevas teorías computacionales, sino que modela una vasta gama de problemas del mundo real, desde la asignación de frecuencias en telecomunicaciones hasta la programación de horarios y la gestión de registros en compiladores.1 Este informe técnico tiene como objetivo desglosar el GCP desde una perspectiva metaheurística avanzada, sistematizando sus componentes —representaciones, operadores, objetivos y estrategias de control— de tal manera que puedan ser ingeridos y explotados por sistemas de Generación Automática de Algoritmos (Automated Algorithm Generation, AAG), tales como hiper-heurísticas basadas en gramáticas o marcos evolutivos impulsados por Modelos de Lenguaje Grande (LLMs) como LLaMEA y REMS.3
1.1 Naturaleza Computacional y Complejidad del GCP
El GCP, en su formulación más clásica de coloreado de vértices, busca asignar una etiqueta (color) a cada vértice de un grafo $G = (V, E)$ de manera que ningún par de vértices adyacentes comparta la misma etiqueta, minimizando el número total de etiquetas utilizadas, denotado como el número cromático $\chi(G)$.1 A pesar de la simplicidad de su definición, el GCP pertenece a la clase de problemas NP-duros. Más aún, se ha demostrado que no solo determinar el número cromático es computacionalmente intratable para grafos generales, sino que incluso encontrar una aproximación $\epsilon$-cercana dentro de un factor constante es NP-duro.6
La intratabilidad del GCP implica que los algoritmos exactos, como aquellos basados en ramificación y acotación (Branch and Bound) o programación lineal entera, son incapaces de resolver instancias con más de 100 vértices en tiempos razonables.1 Esto ha forzado a la comunidad científica a migrar hacia métodos heurísticos y metaheurísticos que sacrifican la garantía de optimalidad por la eficiencia computacional y la capacidad de encontrar soluciones de alta calidad (subóptimas) en tiempos polinomiales. Sin embargo, el diseño de estas metaheurísticas ha sido tradicionalmente un proceso manual, lento y propenso al sesgo humano, donde expertos diseñan operadores específicos (como el operador de cruce o la estructura de vecindad) basándose en la intuición y el ensayo y error.
1.2 La Transición hacia la Generación Automática de Algoritmos (AAG)
La premisa de la AAG es revertir la dependencia del experto humano. En lugar de diseñar un algoritmo para resolver el GCP, se diseña un sistema que genera algoritmos para resolver el GCP. Este meta-nivel de optimización requiere una ontología clara de los componentes del problema. Un sistema AAG no puede inventar conceptos matemáticos desde el vacío; requiere bloques de construcción (building blocks) robustos: formas de representar una solución, mecanismos para alterar esa solución y métricas para evaluar su calidad.
Recientemente, marcos como REMS (Resource-Centered Modeling and Solving) y LLaMEA han demostrado que es posible unificar la representación de problemas combinatorios diversos bajo paradigmas comunes, permitiendo que algoritmos generados para un problema (e.g., Bin Packing) sean adaptados o sirvan de inspiración para otros (e.g., GCP).3 Por ejemplo, el marco REMS modela el GCP como un problema de asignación de recursos donde los recursos son los colores y las tareas son los vértices, sujetos a restricciones de incompatibilidad.8
Este reporte se estructura para servir como una base de conocimiento para tales sistemas. No se limita a describir cómo funcionan los algoritmos existentes, sino que disecciona por qué funcionan y cómo sus partes constituyentes pueden ser parametrizadas, intercambiadas y evolucionadas automáticamente.
2. Bloque 1: Representación de Soluciones y Espacios de Búsqueda
La representación de la solución es la decisión arquitectónica fundamental en cualquier sistema de AAG. Define el genotipo sobre el cual operan los mecanismos evolutivos y determina la topología del paisaje de aptitud (fitness landscape). Una representación inadecuada puede introducir redundancia, simetrías no deseadas o hacer que soluciones válidas sean inaccesibles. Para el GCP, identificamos tres familias principales de representaciones explotables por AAG.
2.1 Representaciones Directas: Asignación de Enteros y Vectores
La representación más inmediata para un sistema computacional es el vector de enteros. Dado un grafo con $n$ vértices, una solución se codifica como un array $S$ de longitud $n$, donde $S[i]$ representa el color asignado al vértice $i$. Los valores de $S[i]$ pertenecen al rango $[1, k]$, donde $k$ es un límite superior del número cromático.
Análisis Crítico para AAG
Aunque intuitiva y fácil de manipular por operadores de mutación simples (cambiar un entero por otro), esta representación sufre de un problema crítico para la búsqueda automatizada: la redundancia por simetría. En el GCP, las etiquetas de los colores son intercambiables; una solución donde el vértice A es rojo y el B es azul es estructuralmente idéntica a una donde A es azul y B es rojo. Esto implica que el espacio de búsqueda contiene $k!$ copias de cada solución única.
Implicación para AAG: Si un sistema evolutivo (como un Algoritmo Genético o LLaMEA) utiliza esta representación sin control, gastará recursos computacionales explorando soluciones que son fenotípicamente idénticas pero genotípicamente distintas.
Estrategia de Mitigación: Los sistemas AAG deben implementar operadores de "canonización" o normalización antes de la evaluación de aptitud, transformando cualquier permutación de colores en una forma canónica léxica única, reduciendo así el tamaño efectivo del espacio de búsqueda.10
2.2 Representaciones Basadas en Particiones (Conjuntos Independientes)
Una representación más sofisticada, y a menudo preferida en el estado del arte de las metaheurísticas (como en los algoritmos meméticos avanzados), es la de partición de conjuntos. Aquí, la solución no es un array de colores, sino una colección de conjuntos disjuntos de vértices $\{C_1, C_2, \dots, C_k\}$ tal que $\bigcup C_i = V$ y $C_i \cap C_j = \emptyset$.
Ventajas Estructurales
Esta representación es agnóstica a las etiquetas, eliminando automáticamente la redundancia por simetría. Además, se alinea naturalmente con la estructura matemática del problema, ya que cada clase de color $C_i$ debe ser, idealmente, un conjunto independiente (ningún par de vértices en $C_i$ está conectado por una arista).11
Explotación en AAG
Para un sistema de generación automática, esta representación cambia la naturaleza de los operadores requeridos. En lugar de operaciones aritméticas sobre enteros, el sistema debe tener acceso a primitivas de teoría de conjuntos:
unión(Set A, Set B)
intersección(Set A, Set B)
diferencia(Set A, Set B)
transferir_vertice(Vertice v, Set Origen, Set Destino)
Esta abstracción permite la evolución de heurísticas que manipulan bloques completos de la solución, facilitando el descubrimiento de operadores de alto nivel como las Cadenas de Kempe o el cruce GPX (Greedy Partition Crossover).13
2.3 Representaciones Indirectas: Permutaciones y Decodificadores
En esta aproximación, el genotipo que evoluciona el sistema AAG no es una coloración explícita, sino una permutación $\pi$ de los vértices del grafo. La coloración real (fenotipo) se genera aplicando un algoritmo constructivo determinista (decodificador) que procesa los vértices en el orden dictado por $\pi$.
Decodificadores Comunes
Greedy Secuencial: Asigna a cada vértice el primer color disponible ($1, 2, \dots$) que no cause conflictos con los vecinos ya procesados.
DSATUR Dinámico: Utiliza la permutación solo para romper empates, decidiendo el orden principal basado en la saturación dinámica.
Potencial para Hiper-heurísticas
Esta representación transforma el GCP de un problema de asignación a un problema de ordenamiento (similar al TSP). Esto es extremadamente valioso para marcos AAG como LLaMEA o hiper-heurísticas de selección, ya que permite reciclar operadores de cruce y mutación diseñados para problemas de permutación (e.g., PMX, Order Crossover) y aplicarlos directamente al GCP sin modificaciones.11 La investigación muestra que el espacio de las permutaciones es a menudo más suave y navegable que el espacio de las asignaciones directas, facilitando la convergencia de estrategias evolutivas.16
| Tipo de Representación | Estructura de Datos | Primitivas Algorítmicas Requeridas | Ventaja Principal en AAG | Desafío Principal |
|---|---|---|---|---|
| Directa (Enteros) | `Array<Int>` | `assign(v, c)`, `swap(v1, v2)` | Simplicidad, compatibilidad con LLMs básicos. | Explosión combinatoria por simetrías. |
| Partición (Conjuntos) | `List<Set<Vertice>>` | `set_union`, `set_diff`, `move_element` | Elimina simetría, opera sobre estructura del grafo. | Implementación compleja de operadores de cruce. |
| Permutación (Orden) | `Array<Index>` | `reorder`, `shift`, `PMX_crossover` | Reutilización de operadores de otros dominios (TSP). | Fuerte dependencia de la calidad del decodificador. |
| Dominio (Binaria/SAT) | `Matrix<Bool>` | `flip_bit`, `logical_constraints` | Mapeo directo a solvers SAT/CSP genéricos. | Escalabilidad deficiente en grafos densos/grandes. |

**Tabla 1: Comparativa de Representaciones para Marcos de Generación Automática**

3. Bloque 2: Operadores de Búsqueda y Estrategias de Variación
Si la representación es la estructura estática, los operadores son la dinámica que permite navegar el espacio de búsqueda. Un sistema AAG robusto debe poseer una biblioteca granular de operadores que cubran tres espectros: construcción, perturbación local y recombinación global. La literatura sugiere que la eficacia de una metaheurística depende crucialmente del equilibrio entre estos operadores.
3.1 Operadores Constructivos (Heurísticas de Bajo Nivel)
Las heurísticas constructivas son algoritmos voraces que construyen una solución válida desde cero. En el contexto de AAG, estas no son solo métodos de inicialización, sino "primitivas" que pueden ser invocadas por hiper-heurísticas durante la búsqueda para reparar soluciones parciales.15
3.1.1 DSATUR (Degree of Saturation)
El algoritmo DSATUR, propuesto por Brélaz, es omnipresente en la literatura debido a su equilibrio entre velocidad y calidad. Selecciona dinámicamente el vértice con el mayor "grado de saturación" (número de colores diferentes usados por sus vecinos) para colorearlo a continuación.
Mecanismo: Prioriza los vértices más restringidos, postergando las decisiones fáciles.
Uso en AAG: En sistemas de programación genética, DSATUR se descompone en sus componentes de evaluación (getSaturationDegree) para ser combinados con otros criterios.10
3.1.2 RLF (Recursive Largest First)
RLF construye la solución color por color, en lugar de vértice por vértice. Para cada color, busca el Conjunto Independiente Maximal (Maximal Independent Set) más grande posible en el subgrafo residual.
Mecanismo: Extrae grandes bloques de vértices que pueden compartir el mismo color, reduciendo la fragmentación del grafo.
Relevancia: Aunque más lento que DSATUR ($O(n^3)$ vs $O(n^2)$), RLF suele producir mejores resultados en grafos grandes y dispersos. Para AAG, RLF representa una estrategia de "divide y vencerás" que puede ser aprendida o seleccionada para instancias específicas.6
3.2 Operadores de Búsqueda Local y Perturbación
Una vez construida una solución inicial, los operadores de búsqueda local exploran la vecindad inmediata para mejorar la calidad o reducir conflictos.
3.2.1 Operador 1-Exchange (1-opt) y Criticalidad
El movimiento más fundamental es cambiar el color de un único vértice $v$ a otro color $c'$.
Optimización: En lugar de probar todos los movimientos, los sistemas eficientes se centran en vértices "críticos" (aquellos involucrados en conflictos o que definen el número cromático actual).
Tabu Search: Para evitar ciclos, este operador se suele envolver en una estrategia Tabu, prohibiendo revertir el cambio de color de $v$ durante $\tau$ iteraciones.11
3.2.2 Cadenas de Kempe (Kempe Chains): El "Túnel" Topológico
Las Cadenas de Kempe son, sin duda, el operador más poderoso para la navegación avanzada en el GCP. Su capacidad para realizar cambios macroscópicos en la solución manteniendo la factibilidad las hace indispensables para escapar de óptimos locales.
Definición Formal: Dados dos colores $c_i$ y $c_j$ en una coloración parcial o total, una Cadena de Kempe es una componente conexa del subgrafo inducido $G[V_{c_i} \cup V_{c_j}]$, donde $V_{c}$ es el conjunto de vértices con color $c$.
Mecanismo de Intercambio: Al intercambiar los colores $c_i$ y $c_j$ solo dentro de una componente conexa (Cadena de Kempe), se garantiza que no se introducen nuevos conflictos internos (pues los vértices adyacentes dentro de la cadena simplemente invierten sus colores, manteniendo la distinción) y no se generan conflictos con el exterior (pues la cadena está aislada de otros vértices de colores $c_i$ o $c_j$ por definición).11
Implementación en AAG: Los sistemas automatizados deben tratar el intercambio de Kempe como una "mutación inteligente". Mientras que una mutación aleatoria suele destruir la validez de una solución, una mutación basada en Kempe preserva la estructura válida, permitiendo "tunelar" a través de barreras de alta energía en el paisaje de aptitud. Los estudios muestran que las metaheurísticas que integran cadenas de Kempe superan consistentemente a las que solo usan 1-opt.11
3.3 Operadores Evolutivos de Recombinación (Crossover)
El diseño de operadores de cruce para GCP es notoriamente difícil debido a la ambigüedad de las etiquetas de color. Un cruce de punto simple entre dos padres

$$y$$
podría generar un hijo inválido o redundante.
3.3.1 Greedy Partition Crossover (GPX)
Considerado el estado del arte en algoritmos meméticos para GCP.
Funcionamiento: Trabaja sobre la representación de particiones. Alternadamente, selecciona la clase de color (conjunto independiente) más grande de cada padre y la añade al hijo, eliminando los vértices correspondientes del otro padre para evitar duplicados.
Lógica: Hereda los "bloques de construcción" más fuertes (grandes conjuntos independientes) de ambos padres.
AAG: En marcos como LLaMEA, el GPX debe ser pre-programado como una función de alto nivel o descubierto mediante la composición de primitivas de conjuntos (find_max_set, remove_vertices).13
3.3.2 Cruce de Unión de Conjuntos Independientes (UIS)
Intenta identificar subestructuras comunes. Calcula la intersección de las clases de color de los padres y construye el hijo a partir de estos núcleos consensuados, rellenando los vértices restantes con heurísticas constructivas. Este operador promueve una explotación intensa de las características compartidas.10
4. Bloque 3: Funciones Objetivo y Análisis del Paisaje de Aptitud
La función objetivo es la brújula que guía al sistema AAG. Sin embargo, en el GCP, la definición de "mejor" puede variar dependiendo de si se trata de un problema de decisión (k-fijo) o de optimización (k-variable), y de la topología del paisaje de aptitud resultante.
4.1 Formulaciones Matemáticas del Objetivo
4.1.1 Minimización de Conflictos (Enfoque de Penalización)
Para un número fijo de colores $k$, el objetivo es minimizar el número de aristas conflictivas (bad edges).


$$f(S) = |\{(u, v) \in E : c(u) = c(v)\}|$$

Este es el enfoque estándar para Tabu Search (TabuCol) y Simulated Annealing. El algoritmo intenta reducir $f(S)$ a 0. Si lo logra, se reduce $k$ a $k-1$ y se reinicia la búsqueda.6
4.1.2 Función de Energía de Johnson (Suma de Cuadrados)
Una formulación alternativa, diseñada para facilitar la transición entre diferentes valores de $k$, es maximizar la suma de los cuadrados de los tamaños de las clases de color:


$$f(S) = \sum_{i=1}^k |C_i|^2$$

Esta función, utilizada en enfoques de recocido simulado, favorece soluciones desequilibradas donde algunas clases de color son muy grandes y otras muy pequeñas. Esto facilita indirectamente la eliminación de las clases pequeñas (vaciándolas), permitiendo reducir el número total de colores.11
Insight para AAG: Un sistema automatizado podría beneficiarse de alternar dinámicamente entre estas funciones. Al inicio, usar la minimización de conflictos para encontrar una solución factible rápida; luego, cambiar a la función de Johnson para compactar la solución y reducir $k$.
4.2 Análisis del Paisaje de Aptitud: Rugosidad y Neutralidad
El paisaje de aptitud (Fitness Landscape) del GCP presenta características patológicas que dificultan la búsqueda simple y que deben ser consideradas por cualquier sistema AAG.
4.2.1 Neutralidad Masiva
El GCP se caracteriza por una alta neutralidad. Existen vastas regiones del espacio de búsqueda (mesetas o plateaus) donde las soluciones vecinas tienen exactamente el mismo valor de aptitud. Por ejemplo, en una solución parcial, intercambiar dos colores en un subgrafo desconectado puede no cambiar el número de conflictos.22
Consecuencia: Los algoritmos de descenso de gradiente (Hill Climbing) se detienen prematuramente o vagan aleatoriamente (random walk) sobre estas mesetas sin dirección.
Estrategia AAG: Los algoritmos generados deben incluir mecanismos explícitos para la navegación de mesetas. Esto implica aceptar movimientos con $\Delta f = 0$ (movimientos laterales) y buscar "portales" (soluciones en la meseta que tienen vecinos con mejor aptitud). La métrica de "grado de neutralidad" puede ser usada por el sistema AAG para ajustar la agresividad de la exploración.24
4.2.2 Rugosidad (Ruggedness) y Óptimos Locales
A medida que $k$ se acerca al número cromático real $\chi(G)$, el paisaje se vuelve extremadamente rugoso, lleno de óptimos locales profundos de los cuales es difícil escapar con operadores simples como 1-opt.
Diagnóstico Automatizado: Un sistema AAG avanzado puede calcular métricas como la autocorrelación del paisaje o la correlación aptitud-distancia (FDC) durante una fase de muestreo inicial. Si la autocorrelación es baja (paisaje muy rugoso), el sistema debería favorecer la generación de algoritmos con alta perturbación (ILS, Cadenas de Kempe); si es alta (paisaje suave), debería favorecer búsquedas locales intensivas.25
5. Bloque 4: Penalizaciones y Manejo de Restricciones
La gestión de la infactibilidad es un aspecto crítico. Los enfoques modernos para el GCP no descartan las soluciones inválidas, sino que las exploran estratégicamente para atravesar el espacio de búsqueda.
5.1 Penalizaciones Adaptativas y Búsqueda Oscilante
En lugar de imponer una prohibición estricta sobre las soluciones inválidas, algoritmos como AFISA (Adaptive Feasible and Infeasible Search) utilizan una función de evaluación extendida que penaliza los conflictos con un peso dinámico $\alpha$:


$$f_{eval}(S) = f_{obj}(S) + \alpha \cdot \text{Violaciones}$$
Mecanismo de Adaptación para AAG
La clave del éxito de AFISA y estrategias similares es que $\alpha$ no es constante.
Si el algoritmo no encuentra una solución válida durante un tiempo, $\alpha$ aumenta para forzar la búsqueda hacia la factibilidad.
Si el algoritmo está atrapado en óptimos locales válidos, $\alpha$ disminuye, permitiendo que la búsqueda atraviese regiones infactibles ("túneles") para alcanzar nuevas zonas prometedoras del espacio válido.27
Relevancia para la Generación Automática:
Un sistema AAG como LLaMEA puede ser utilizado para aprender la función de control de $\alpha$. En lugar de usar reglas heurísticas fijas (e.g., "multiplicar por 1.1 cada 10 iteraciones"), el LLM puede generar código que ajuste $\alpha$ basándose en un análisis complejo del estado de la búsqueda (diversidad de la población, tasa de mejora reciente), descubriendo estrategias de control no lineales y altamente efectivas.3
5.2 Espacio de Búsqueda Dual
Algunas metaheurísticas generadas mantienen dos poblaciones simultáneas: una de soluciones factibles y otra de infactibles. Los operadores de cruce entre estas dos poblaciones permiten inyectar diversidad (de las infactibles) en la élite (factible), un patrón de diseño que los sistemas AAG pueden replicar mediante la evolución de arquitecturas de población múltiple.28
6. Bloque 5: Estrategias de Control y Marcos de Generación Automática
Este bloque integra los componentes anteriores en arquitecturas algorítmicas coherentes. Analizamos cómo los sistemas de AAG actuales, desde hiper-heurísticas clásicas hasta los modernos enfoques basados en LLMs, orquestan la resolución del GCP.
6.1 Hiper-heurísticas de Selección
Las hiper-heurísticas de selección no "crean" nuevo código, sino que seleccionan dinámicamente qué heurística de bajo nivel (LLH) aplicar en cada momento.
Modelo de Estado: El sistema observa el estado actual (e.g., mejora de la aptitud, iteraciones sin mejora).
Acción: Selecciona una heurística del conjunto {Greedy, Random_Swap, Kempe_Chain, Destroy_k_nodes}.
Aprendizaje: Utilizan mecanismos como cadenas de Markov ocultas, aprendizaje por refuerzo o tablas de elección adaptativas para aprender secuencias exitosas. Por ejemplo, aprender que después de un estancamiento prolongado, una perturbación fuerte (Kempe Chain) es más efectiva que una débil (1-opt).15
6.2 Hiper-heurísticas de Generación (Programación Genética)
A diferencia de la selección, la generación crea nuevas heurísticas combinando componentes atómicos. Esto se realiza típicamente mediante Programación Genética (GP) o Evolución Gramatical.
Gramáticas Libres de Contexto (BNF) para GCP
Para restringir el espacio de búsqueda a algoritmos sintácticamente válidos, se define una gramática BNF. Un ejemplo de estructura gramatical para generar heurísticas constructivas de GCP sería:

BNF


<heuristic> ::= <selector> | if <condition> then <selector> else <selector>
<selector>  ::= select_max_degree | select_max_saturation | select_random
<condition> ::= conflict_density > <threshold> | iterations < <limit>


Sistemas basados en esta gramática han logrado evolucionar heurísticas que superan a DSATUR en dominios específicos como la programación de exámenes (exam timetabling), descubriendo combinaciones de criterios que los humanos no habían considerado (e.g., "usar saturación, pero si hay empate, usar el grado de los vecinos de segundo nivel").18
6.3 Marcos Basados en LLMs: LLaMEA y REMS
La frontera actual en AAG es el uso de Modelos de Lenguaje Grande (LLMs) como motores de variación.
LLaMEA (Large Language Model Evolutionary Algorithm)
LLaMEA sustituye los operadores de mutación y cruce tradicionales de la computación evolutiva por prompts a un LLM.
Ciclo de Vida:
Inicialización: El LLM genera $N$ algoritmos de GCP en código Python (e.g., una clase con un método solve).
Evaluación: Se ejecutan los algoritmos en un conjunto de entrenamiento (instancias pequeñas de DIMACS). Se captura no solo el resultado, sino el error de ejecución (traceback) si falla.
Variación (Prompting): Se selecciona el mejor algoritmo y se alimenta al LLM junto con su rendimiento y cualquier error. El prompt instruye: "Mejora este algoritmo para reducir el tiempo de ejecución en grafos densos. Considera usar estructuras de datos más eficientes para la matriz de adyacencia".
Iteración: El LLM genera una versión refinada, cerrando el bucle.
Ventaja: LLaMEA puede introducir lógica semántica compleja (e.g., "implementa un mecanismo de reinicio basado en la temperatura") que sería casi imposible de ensamblar mediante mutación de bits o árboles de GP.3
REMS (Resource-Centered Modeling)
REMS abstrae el GCP como un problema de asignación de recursos. Esto permite que el sistema AAG transfiera conocimiento entre dominios. Un algoritmo eficaz generado para el problema de Bin Packing (asignar ítems a contenedores) puede ser "traducido" automáticamente por REMS para el GCP (asignar vértices a colores), dado que ambos comparten la estructura subyacente de particionamiento bajo restricciones.8
7. Bloque 6: Evaluación y Benchmarking
La evaluación rigurosa es el mecanismo de retroalimentación que permite a los sistemas AAG aprender. Un conjunto de prueba mal diseñado conducirá a un "sobreajuste" (overfitting) donde el algoritmo generado funciona bien solo en grafos aleatorios pero falla en grafos estructurados del mundo real.
7.1 Instancias de Referencia Estándar (DIMACS)
El conjunto de instancias del Desafío DIMACS es el estándar de facto. Un sistema AAG debe ser evaluado contra familias diversas dentro de este conjunto para garantizar generalidad.35
Grafos Aleatorios (DSJC): Generados con probabilidad de arista constante. Son útiles para probar la gestión pura de conflictos, pero carecen de estructura profunda. Los algoritmos simples como DSATUR funcionan razonablemente bien aquí.
Grafos Geométricos (DSJR, r): Generados por proximidad en un plano 2D. Tienen estructura local fuerte y clustering alto. Requieren operadores que exploten la localidad.
Grafos Planos (Flat): Generados artificialmente para tener un número cromático conocido pero "escondido" mediante la adición de aristas que no violan la coloración. Son engañosos para heurísticas voraces y prueban la capacidad de escape de óptimos locales.
Grafos de Leighton (le450): Contienen cliques de tamaño conocido garantizado. Son extremadamente difíciles porque el número cromático está determinado por un clique denso que el algoritmo debe encontrar.
Grafos "Reales" (Scheduling, Registros): Provienen de aplicaciones industriales. Suelen ser muy dispersos pero con restricciones duras específicas.
7.2 Métricas de Rendimiento para AAG
Además de las métricas estándar (número de colores $k$, tiempo de ejecución), la evaluación de AAG requiere métricas de segundo orden:
Distancia al Óptimo (Gap): Diferencia porcentual respecto al mejor límite conocido ($\chi$ o Best Known Solution).
Robustez: Varianza del rendimiento a través de múltiples ejecuciones estocásticas.
Generalidad (Cross-domain): Capacidad de un algoritmo generado para rendir bien en familias de grafos no vistas durante el entrenamiento (e.g., entrenar en DSJC y probar en Leighton).38
Complejidad del Código: En generación basada en LLMs, se penaliza el código innecesariamente complejo o "spaghetti code". Se busca la parsimonia (Navaja de Ockham) para asegurar que el algoritmo sea interpretable y mantenible.39
8. Conclusiones y Futuro de la Investigación
La revisión y sistematización de la literatura permite responder afirmativamente a la pregunta de investigación: el Graph Coloring Problem puede ser modelado eficazmente como una composición de bloques funcionales reutilizables para la Generación Automática de Algoritmos.
8.1 Síntesis de Hallazgos
La Representación Importa: Los sistemas AAG deben priorizar representaciones basadas en particiones o permutaciones sobre las directas para evitar la explosión combinatoria por simetrías.
Operadores Inteligentes: La inclusión de operadores avanzados como las Cadenas de Kempe y el cruce GPX como primitivas atómicas es fundamental. Un sistema AAG que tenga que "redescubrir" la lógica de las cadenas de Kempe desde cero probablemente fallará; debe dársele como una herramienta de alto nivel.
Control Adaptativo: Las funciones de penalización y los parámetros de búsqueda no deben ser estáticos. La AAG brilla especialmente en el diseño de leyes de control dinámicas que adaptan la búsqueda en tiempo real basándose en la topología del paisaje (rugosidad, neutralidad).
El Rol de los LLMs: Marcos como LLaMEA representan el futuro inmediato, permitiendo una evolución semántica del código que trasciende las limitaciones de la programación genética tradicional. La capacidad de los LLMs para entender el contexto y transferir conceptos de otros dominios de optimización (vía frameworks como REMS) promete acelerar el descubrimiento de nuevas heurísticas de estado del arte.
8.2 Perspectivas Futuras
El siguiente paso en la investigación de AAG para el GCP reside en la interpretabilidad. A medida que los algoritmos generados se vuelven más complejos, entender por qué una heurística generada funciona mejor que una humana se vuelve vital. El desarrollo de herramientas de análisis automático que expliquen la lógica de las estrategias generadas (e.g., "el algoritmo aprendió a priorizar vértices de alto grado solo en las fases tempranas") cerrará el ciclo entre la inteligencia artificial y la teoría de grafos humana.
Nota sobre Citas: Las referencias citadas en el texto `` corresponden al material de investigación proporcionado y analizado para la elaboración de este informe.
Obras citadas
An island-parallel ensemble metaheuristic algorithm for large graph coloring problems, fecha de acceso: enero 4, 2026, https://arxiv.org/html/2504.15082v1
Graph Coloring Problem (GCP) - Artificial Intelligence, fecha de acceso: enero 4, 2026, https://schneppat.com/graph-coloring-problem-gcp.html
Natural Computing Group: LLaMEA, fecha de acceso: enero 4, 2026, https://naco.liacs.nl/projects/2024-llamea/
Code Evolution Graphs: Understanding Large Language Model Driven Design of Algorithms, fecha de acceso: enero 4, 2026, https://arxiv.org/html/2503.16668v1
LLaMEA: A Large Language Model Evolutionary Algorithm for Automatically Generating Metaheuristics - IEEE Xplore, fecha de acceso: enero 4, 2026, https://ieeexplore.ieee.org/iel8/4235/10947080/10752628.pdf
The Graph Coloring Problem: Exact and Heuristic Solutions - Towards Data Science, fecha de acceso: enero 4, 2026, https://towardsdatascience.com/the-graph-coloring-problem-exact-and-heuristic-solutions-169dce4d88ab/
Stochastic Local Search Algorithms for the Graph Colouring Problem - IMADA, fecha de acceso: enero 4, 2026, https://www.imada.sdu.dk/u/march/Publications/Files/AIDA-05-03.pdf
REMS: a unified solution representation, problem modeling and metaheuristic algorithm design for general combinatorial optimization problems - arXiv, fecha de acceso: enero 4, 2026, https://arxiv.org/html/2505.17108v1
Exact and Metaheuristic Algorithms for Variable Reduction | Request PDF - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/375683371_Exact_and_Metaheuristic_Algorithms_for_Variable_Reduction
Genetic Algorithm Applied to the Graph Coloring Problem - CEUR-WS.org, fecha de acceso: enero 4, 2026, https://ceur-ws.org/Vol-841/submission_10.pdf
(PDF) Local Search for the Colouring Graph Problem. A ..., fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/2476724_Local_Search_for_the_Colouring_Graph_Problem_A_Computational_Study
*CRT-Ecole Polytechnique, 3000 chemin de la Cote Sainte-Catherine, Montreal (QC) H3T 2A7, Canada, philippe.galinier@polymtl.ca t - GERAD, fecha de acceso: enero 4, 2026, https://www.gerad.ca/~alainh/ColorationLocal.pdf
Evolutionary Graph Coloring, fecha de acceso: enero 4, 2026, https://publikationen.bibliothek.kit.edu/1000073698/4337798
A deep learning guided memetic framework for graph coloring problems - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/354572157_A_deep_learning_guided_memetic_framework_for_graph_coloring_problems
A Graph Coloring Constructive Hyper-Heuristic for Examination ..., fecha de acceso: enero 4, 2026, https://people.cs.nott.ac.uk/pszrq/files/APIN11.pdf
Stochastic Learning for SAT- Encoded Graph Coloring Problems - IDEAS/RePEc, fecha de acceso: enero 4, 2026, https://ideas.repec.org/a/igg/jamc00/v1y2010i3p1-19.html
A Unified Framework of Graph-based Evolutionary Multitasking Hyper-heuristic - University of Nottingham, fecha de acceso: enero 4, 2026, https://people.cs.nott.ac.uk/pszrq/files/TEVC20.pdf
Automatically Generated Algorithms for the Vertex Coloring Problem ..., fecha de acceso: enero 4, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC3596313/
Graph Coloring and Recombination - Rhyd Lewis, fecha de acceso: enero 4, 2026, https://rhydlewis.eu/papers/gColChapter.pdf
An ACO Algorithm for the Graph Coloring Problem - m-hikari.com, fecha de acceso: enero 4, 2026, https://www.m-hikari.com/ijcms-password2008/5-8-2008/eshghiIJCMS5-8-2008.pdf
An introduction of preference based stepping ahead firefly algorithm for the uncapacitated examination timetabling - PMC - NIH, fecha de acceso: enero 4, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC9455270/
Neutrality in the Graph Coloring Problem, fecha de acceso: enero 4, 2026, https://perso.eleves.ens-rennes.fr/people/aymeric.blot/files/papers/marmion_lion_2013.pdf
Neutrality in the Graph Coloring Problem - arXiv, fecha de acceso: enero 4, 2026, https://arxiv.org/pdf/1301.6092
(PDF) Neutrality in the Graph Coloring Problem - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/235008892_Neutrality_in_the_Graph_Coloring_Problem
Anatomy of the fitness landscape for dense graph-colouring problem - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/273480723_Anatomy_of_the_fitness_landscape_for_dense_graph-colouring_problem
How Predictable are Fitness Landscapes with Machine Learning? A Traveling Salesman Ruggedness Study - The Science and Information (SAI) Organization, fecha de acceso: enero 4, 2026, https://thesai.org/Downloads/Volume15No11/Paper_118-How_Predictable_are_Fitness_Landscapes_with_Machine_Learning.pdf
Adaptive feasible and infeasible tabu search for weighted vertex coloring - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/326596699_Adaptive_feasible_and_infeasible_tabu_search_for_weighted_vertex_coloring
Adaptive feasible and infeasible tabu search for weighted vertex coloring - Université Angers, fecha de acceso: enero 4, 2026, https://leria-info.univ-angers.fr/~jinkao.hao/papers/Sunetal2018INS.pdf
Large Language Model Assisted Automated Algorithm Generation and Evolution via Meta-black-box optimization - arXiv, fecha de acceso: enero 4, 2026, https://arxiv.org/html/2509.13251v2
LLaMEA: A Large Language Model Evolutionary Algorithm for Automatically Generating Metaheuristics - arXiv, fecha de acceso: enero 4, 2026, https://arxiv.org/html/2405.20132v4
A Graph Coloring Constructive Hyper-Heuristic for Examination Timetabling Problems - Graham Kendall, fecha de acceso: enero 4, 2026, https://www.graham-kendall.com/papers/saqk2012.pdf
A Classification of Hyper-Heuristic Approaches: Revisited - Graham Kendall, fecha de acceso: enero 4, 2026, https://www.graham-kendall.com/papers/bhkoow2019.pdf
Grammar-based genetic programming for timetabling - IEEE Xplore, fecha de acceso: enero 4, 2026, http://ieeexplore.ieee.org/document/4983259/
(PDF) Grammar-Based Genetic Programming for Timetabling, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/221006929_Grammar-Based_Genetic_Programming_for_Timetabling
Graph Coloring Benchmarks - Multicoloring - Google Sites, fecha de acceso: enero 4, 2026, https://sites.google.com/site/graphcoloring/multicoloring
COLOR02/03/04: Graph Coloring and its Generalizations, fecha de acceso: enero 4, 2026, https://mat.tepper.cmu.edu/COLOR02/
DIMACS Graphs and Best Algorithms - Cedric-Cnam, fecha de acceso: enero 4, 2026, https://cedric.cnam.fr/~porumbed/graphs/
A Unified Framework of Graph-Based Evolutionary Multitasking Hyper-Heuristic | Request PDF - ResearchGate, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/341096103_A_Unified_Framework_of_Graph-Based_Evolutionary_Multitasking_Hyper-Heuristic
Code Evolution Graphs: Understanding Large Language Model Driven Design of Algorithms, fecha de acceso: enero 4, 2026, https://www.researchgate.net/publication/390114788_Code_Evolution_Graphs_Understanding_Large_Language_Model_Driven_Design_of_Algorithms



