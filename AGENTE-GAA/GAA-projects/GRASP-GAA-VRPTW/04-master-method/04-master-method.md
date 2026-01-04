Método Maestro para GAA – VRPTW
PARTE A: Definición del Problema Maestro
El Problema Maestro (Master Problem)

Dado el conjunto de instancias benchmark del Vehicle Routing Problem with Time Windows (VRPTW) propuesto por Solomon, el Problema Maestro de Generación Automática de Algoritmos (GAA) consiste en determinar la mejor combinación de FUNCIONES y TERMINALES que, organizadas en forma de Árbol Sintáctico Abstracto (AST), definen la lógica de un algoritmo heurístico capaz de producir soluciones de alta calidad para dichas instancias.

Formulación Formal

Formalmente, el problema maestro se define como la optimización del espacio de programas P, donde cada programa p ∈ P representa un algoritmo heurístico expresado como un AST, construido a partir de un conjunto predefinido de funciones F y terminales T.

El objetivo es encontrar el programa p* que maximiza el desempeño promedio del algoritmo inducido sobre un conjunto de instancias VRPTW del benchmark Solomon, considerando criterios de calidad de solución y factibilidad, permitiendo evaluaciones penalizadas de soluciones parcialmente infactibles para favorecer la exploración del espacio de búsqueda.

Definición matemática:

p* = arg max_{p ∈ P(F,T)} Fitness(p)

donde:

P(F,T) es el espacio de todos los AST posibles generados a partir de funciones F y terminales T

Fitness(p) evalúa la calidad del algoritmo inducido por el AST p al resolver instancias VRPTW

Interpretación Conceptual

Este enfoque enfatiza que la optimización se realiza sobre la lógica del algoritmo (estructura de decisiones, criterios de inserción y selección), y no directamente sobre las rutas o soluciones específicas generadas.

PARTE B: Metaheurística para Resolver el Problema Maestro
Metaheurística Elegida: GRASP

Se emplea una adaptación de GRASP como metaheurística de alto nivel para explorar el espacio de programas (AST).

En este contexto, cada iteración de GRASP genera un algoritmo candidato mediante:

Una fase de construcción aleatorizada, en la que se genera un AST completo combinando funciones y terminales.

Una fase de mejora local, en la que se aplican transformaciones estructurales sobre el AST, tales como sustitución de terminales, reemplazo de funciones heurísticas o reordenamiento de subárboles.

Justificación de la Elección

GRASP se adopta por las siguientes razones:

Permite balancear exploración y explotación en espacios de búsqueda altamente discretos y no convexos, como el espacio de AST.

Es compatible con la generación incremental de estructuras algorítmicas basadas en componentes heurísticos.

Facilita la incorporación de mecanismos de randomización controlada para diversificar la lógica algorítmica generada.

Presenta antecedentes exitosos en problemas de optimización combinatoria y diseño automatizado de heurísticas.

PARTE C: Función de Fitness Canónica
Definición de Fitness

La función de fitness evalúa la calidad de un AST en función del desempeño del algoritmo heurístico inducido al resolver un conjunto de instancias VRPTW.

Para cada AST p, el fitness se calcula como el promedio del costo total obtenido al ejecutar el algoritmo definido por p sobre un subconjunto representativo de instancias del benchmark Solomon.

Criterios Jerárquicos

El costo de una solución s se define jerárquicamente como:

Minimización del número de vehículos utilizados.

Minimización de la distancia total recorrida.

Formulación Matemática

Formalmente, el fitness de un AST p se define como:

Fitness(p) = − (1 / |I|) · Σ_{i ∈ I} [ α · Vehicles(p,i) + β · Distance(p,i) + γ · Penalty(p,i) ]

donde:

I es el conjunto de instancias VRPTW utilizadas para evaluación.

Vehicles(p,i) es el número de vehículos utilizados por el algoritmo p en la instancia i.

Distance(p,i) es la distancia total recorrida.

Penalty(p,i) representa penalizaciones por violaciones de restricciones.

α ≫ β, y γ se selecciona de modo que las soluciones infactibles sean penalizadas severamente sin eclipsar la jerarquía principal entre número de vehículos y distancia.

El signo negativo se utiliza porque el problema maestro es de maximización.

Las penalizaciones permiten evaluar algoritmos que generan soluciones parcialmente infactibles, favoreciendo la conectividad del espacio de búsqueda.

PARTE D: Reproducibilidad
Reproducibilidad Experimental

Para garantizar la reproducibilidad, se utilizan semillas pseudoaleatorias controladas. Los experimentos se repiten para un conjunto fijo de semillas, reportándose promedios y desviaciones estándar.

Cuando se requiere replicabilidad exacta de un experimento específico, se emplea una semilla base fija.

Semilla base utilizada: 42

Las semillas se aplican a:

Generación aleatoria de AST en GRASP.

Selección aleatoria de componentes heurísticos.

Procedimientos estocásticos internos del algoritmo VRPTW.

PARTE E: Best Known Solutions (BKS)

En el contexto del VRPTW de Solomon, el Best Known Solution (BKS) corresponde a la mejor solución reportada en la literatura para una instancia específica, considerando el criterio jerárquico estándar del problema.

Una solución s se caracteriza por el par (V(s), D(s)), donde V(s) es el número de vehículos utilizados y D(s) es la distancia total recorrida.

Una solución s₁ es mejor que una solución s₂ si:

V(s₁) < V(s₂), o

V(s₁) = V(s₂) y D(s₁) < D(s₂).

Este criterio define una relación de orden lexicográfico.

Para cada instancia Solomon existe un BKS denotado como (V*, D*).

Durante la evaluación:

El término asociado al número de vehículos domina la función de fitness.

La distancia se compara únicamente cuando el número de vehículos coincide.

Las soluciones que utilizan más vehículos que el BKS son penalizadas fuertemente, pero no descartadas, para preservar diversidad en el espacio de búsqueda.

Evaluación Final

Esta formulación garantiza coherencia entre:

la definición del problema VRPTW,

el diseño del Problema Maestro de GAA,

la función de fitness,

y la comparación con el estado del arte mediante BKS.