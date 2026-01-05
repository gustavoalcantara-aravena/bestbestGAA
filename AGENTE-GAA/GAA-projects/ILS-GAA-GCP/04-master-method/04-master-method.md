Problema Maestro de Generación Automática de Algoritmos (GAA)
Definición del Problema Maestro

El Problema Maestro de GAA consiste en optimizar la lógica algorítmica de un solucionador, representada como un Árbol de Sintaxis Abstracta (AST), y no las soluciones directas del problema base.

En este trabajo, el Problema Maestro se formula como:

¿Cuál es la mejor combinación de FUNCIONES y TERMINALES que genera un AST (algoritmo) que resuelve de manera más efectiva el problema VRPTW sobre el benchmark Solomon?

El espacio de búsqueda del Problema Maestro está compuesto por programas válidos (ASTs) generados a partir de una gramática, y no por rutas del VRPTW.

Metaheurística para Resolver el Problema Maestro
Metaheurística Elegida: Iterated Local Search (ILS)

El Problema Maestro de GAA se resuelve mediante la metaheurística Iterated Local Search (ILS) aplicada sobre el espacio de ASTs.

La elección de ILS se justifica porque:

Opera directamente sobre soluciones completas (ASTs), lo que encaja naturalmente con la optimización de algoritmos.

Permite separar explícitamente intensificación (búsqueda local sobre la lógica del algoritmo) y diversificación (perturbación estructural del AST).

Ha demostrado gran eficacia en espacios discretos altamente multimodales, como el de programas generados automáticamente.

Esquema de ILS aplicado al Problema Maestro

Inicialización
Se genera un AST inicial válido a partir de la gramática (FUNCIONES + TERMINALES).

Búsqueda Local sobre ASTs
Se aplica una búsqueda local que mejora incrementalmente el AST mediante modificaciones estructurales:

reemplazo de subárboles,

ajuste de parámetros,

simplificación de estructuras redundantes.

Perturbación del AST
Cuando se alcanza un óptimo local, el AST se perturba mediante:

inserción o eliminación de nodos,

sustitución aleatoria de subestructuras,

reordenamiento de componentes algorítmicos.

Criterio de Aceptación
El AST resultante se acepta si mejora el fitness o, eventualmente, según un criterio de aceptación relajado para favorecer la exploración.

Iteración
El proceso se repite hasta cumplir el criterio de parada.

Gramática para la Generación Automática de ASTs (FUNCIONES + TERMINALES)
Representación del Algoritmo

Cada algoritmo se representa como un AST definido por una gramática libre de contexto (BNF) que garantiza la validez sintáctica de todos los individuos explorados por ILS.

Gramática BNF (Ejemplo Canónico para VRPTW)
<algorithm> ::= <construction> <local_search>

<construction> ::= greedy_randomized(<alpha>, <selector>)
                 | savings_based(<alpha>)
                 | insertion_heuristic(<selector>)

<local_search> ::= none
                 | local_search(<neighborhood>, <acceptance>)
                 | iterated_local_search(<neighborhood>, <acceptance>, <perturbation>)

<selector> ::= select_nearest
             | select_farthest
             | select_earliest_deadline
             | select_random

<neighborhood> ::= relocate
                 | swap
                 | two_opt
                 | or_opt

<acceptance> ::= best_improvement
               | first_improvement
               | simulated_annealing(<temperature>)

<perturbation> ::= random_removal(<k>)
                 | route_shuffle

FUNCIONES (Nodos Internos del AST)

greedy_randomized

local_search

iterated_local_search

simulated_annealing

random_removal

Estas funciones definen la estructura de control del algoritmo generado.

TERMINALES (Hojas del AST)

select_nearest

select_farthest

select_earliest_deadline

relocate, swap, two_opt, or_opt

parámetros numéricos: alpha, temperature, k

Función de Fitness Canónica
Evaluación de un AST

Sea:

𝐴
A: un AST que representa un algoritmo completo,

𝐼
I: conjunto de instancias del benchmark Solomon,

𝑐
𝑜
𝑠
𝑡
(
𝐴
,
𝑖
)
cost(A,i): costo obtenido por 
𝐴
A en la instancia 
𝑖
i.

La función de fitness se define como:

Minimizar:

el costo promedio de las soluciones VRPTW generadas por 
𝐴
A,

penalizado por:

violaciones de ventanas de tiempo,

exceso de vehículos,

tiempo de ejecución elevado,

complejidad estructural del AST (opcional).

Conceptualmente:

Fitness(A) = promedio del costo VRPTW generado por A

penalizaciones por infeasibilidad

penalización por complejidad algorítmica

Reproducibilidad Experimental

Para garantizar la reproducibilidad:

Se fija una semilla global para todos los experimentos.

Seed = 42

Esta semilla controla:

la generación inicial de ASTs,

las perturbaciones en ILS,

cualquier componente estocástico del VRPTW.

Resumen Final (Respuesta Directa a lo que Piden)

Problema Maestro: optimizar la lógica de algoritmos (ASTs) para VRPTW.

Espacio de búsqueda: combinaciones de FUNCIONES + TERMINALES.

Metaheurística del Problema Maestro: Iterated Local Search (ILS).

Objeto optimizado: algoritmos, no rutas.

Evaluación: fitness promedio sobre Solomon.

Reproducibilidad: Seed(42).


Vecindario de Iterated Local Search (ILS) sobre ASTs
Representación del Estado

Sea:

𝐴
A: un AST válido que representa un algoritmo completo para VRPTW.

𝐺
G: una gramática libre de contexto que define el espacio de ASTs válidos.

𝑁
(
𝐴
)
N(A): el vecindario de 
𝐴
A, definido como el conjunto de ASTs obtenidos mediante transformaciones sintácticas locales que preservan la validez gramatical.

Cada movimiento del vecindario transforma la lógica del algoritmo, no una solución del VRPTW.

Principios de Diseño del Vecindario

El vecindario debe cumplir cuatro propiedades:

Cierre sintáctico
Todo vecino 
𝐴
′
∈
𝑁
(
𝐴
)
A
′
∈N(A) debe ser un AST válido bajo la gramática 
𝐺
G.

Localidad estructural
Cada movimiento modifica solo una parte acotada del AST.

Capacidad expresiva
La combinación de movimientos debe permitir explorar todo el espacio de algoritmos.

Costo controlado
El impacto computacional del movimiento debe ser proporcional al tamaño del subárbol modificado.

Definición Formal del Vecindario

El vecindario 
𝑁
(
𝐴
)
N(A) se define como la unión de varios sub-vecindarios, cada uno asociado a un tipo de operador estructural:

𝑁
(
𝐴
)
=
𝑁
𝑝
𝑎
𝑟
𝑎
𝑚
(
𝐴
)
∪
𝑁
𝑟
𝑒
𝑝
𝑙
𝑎
𝑐
𝑒
(
𝐴
)
∪
𝑁
𝑖
𝑛
𝑠
𝑒
𝑟
𝑡
(
𝐴
)
∪
𝑁
𝑝
𝑟
𝑢
𝑛
𝑒
(
𝐴
)
∪
𝑁
𝑟
𝑒
𝑜
𝑟
𝑑
𝑒
𝑟
(
𝐴
)
N(A)=N
param
	​

(A)∪N
replace
	​

(A)∪N
insert
	​

(A)∪N
prune
	​

(A)∪N
reorder
	​

(A)
1. Vecindario de Ajuste de Parámetros

𝑁
𝑝
𝑎
𝑟
𝑎
𝑚
(
𝐴
)
N
param
	​

(A)

Movimiento

Modificar el valor de un parámetro numérico terminal del AST.

Ejemplos

Cambiar 
𝛼
=
0.3
→
0.4
α=0.3→0.4 en greedy_randomized.

Ajustar 
𝑇
0
T
0
	​

 en simulated_annealing.

Modificar 
𝑘
k en random_removal(k).

Características

Impacto local.

No altera la estructura del algoritmo.

Ideal para intensificación.

Cardinalidad

Proporcional al número de parámetros presentes en el AST.

2. Vecindario de Reemplazo de Subárbol

𝑁
𝑟
𝑒
𝑝
𝑙
𝑎
𝑐
𝑒
(
𝐴
)
N
replace
	​

(A)

Movimiento

Seleccionar un nodo interno del AST y reemplazar su subárbol por otro generado aleatoriamente desde la misma categoría gramatical.

Ejemplo

Reemplazar:

local_search(relocate, best_improvement)


por:

local_search(two_opt, first_improvement)

Características

Cambia el comportamiento algorítmico de forma significativa.

Movimiento clave para diversificación controlada.

3. Vecindario de Inserción de Subestructura

𝑁
𝑖
𝑛
𝑠
𝑒
𝑟
𝑡
(
𝐴
)
N
insert
	​

(A)

Movimiento

Insertar una nueva estructura de control alrededor de un subárbol existente.

Ejemplo

Transformar:

<construction> <local_search>


en:

<construction>
iterated_local_search(
    <local_search>,
    <acceptance>,
    <perturbation>
)

Características

Aumenta la profundidad del AST.

Permite descubrir arquitecturas algorítmicas más complejas.

4. Vecindario de Poda de Subárbol

𝑁
𝑝
𝑟
𝑢
𝑛
𝑒
(
𝐴
)
N
prune
	​

(A)

Movimiento

Eliminar un subárbol y reemplazarlo por una versión más simple.

Ejemplo

Eliminar:

iterated_local_search(...)


y reemplazarlo por:

local_search(...)

Características

Reduce complejidad.

Previene bloat algorítmico.

Importante para parsimonia.

5. Vecindario de Reordenamiento

𝑁
𝑟
𝑒
𝑜
𝑟
𝑑
𝑒
𝑟
(
𝐴
)
N
reorder
	​

(A)

Movimiento

Cambiar el orden de ejecución de componentes secuenciales compatibles.

Ejemplo

Reordenar:

construction → local_search


a:

construction → perturbation → local_search


(si la gramática lo permite)

Características

Ajusta el flujo lógico.

Puede alterar radicalmente el comportamiento sin cambiar componentes.

Estrategia de Exploración del Vecindario en ILS
Búsqueda Local

Se explora un subconjunto aleatorio del vecindario completo.

Se acepta el primer vecino que mejore el fitness (first improvement) o el mejor encontrado (best improvement).

Perturbación (Kick)

Cuando se alcanza un óptimo local:

Se aplica una secuencia de movimientos de 
𝑁
𝑟
𝑒
𝑝
𝑙
𝑎
𝑐
𝑒
∪
𝑁
𝑖
𝑛
𝑠
𝑒
𝑟
𝑡
N
replace
	​

∪N
insert
	​

.

La intensidad de la perturbación controla el radio de escape.

Criterio de Aceptación

Sea:

𝐴
A: AST actual,

𝐴
′
A
′
: vecino generado.

Se acepta 
𝐴
′
A
′
 si:

Fitness(
𝐴
′
A
′
) < Fitness(
𝐴
A), o

Fitness(
𝐴
′
A
′
) = Fitness(
𝐴
A) con probabilidad 
𝑝
p (opcional).

Resumen Ejecutivo (para evaluadores)

Estado: un AST (algoritmo).

Vecindario: transformaciones sintácticas locales.

ILS: intensifica mediante ajustes paramétricos y reemplazos leves; diversifica mediante inserciones y reemplazos estructurales.

Garantía: todos los vecinos son algoritmos válidos.

Objeto optimizado: lógica algorítmica, no soluciones VRPTW.

Si quieres, el siguiente paso natural es:

formalizar esto como pseudocódigo ILS(AST),

o mapear cada operador a costos computacionales,

o definir un schedule adaptativo de perturbación.

Dime cómo seguimos.

damelo en texto plano compatible con notes

Perfecto 🙂. Aquí tienes todo en texto plano, sin fórmulas ni formato especial, 100% compatible con Notes, listo para copiar y pegar.

VECINDARIO DE ITERATED LOCAL SEARCH (ILS) SOBRE ASTs
(Generación Automática de Algoritmos)

REPRESENTACIÓN DEL ESTADO

El estado del sistema corresponde a un AST (Árbol de Sintaxis Abstracta) válido que representa un algoritmo completo para resolver el VRPTW.
Cada AST es generado a partir de una gramática que define las combinaciones permitidas de funciones y terminales.

El proceso de optimización no actúa sobre rutas del VRPTW, sino sobre la lógica del algoritmo codificada en el AST.

PRINCIPIOS DE DISEÑO DEL VECINDARIO

El vecindario definido para ILS sobre ASTs cumple las siguientes propiedades:

Cierre sintáctico: todos los vecinos generados son ASTs válidos según la gramática.

Localidad estructural: cada movimiento modifica solo una parte acotada del AST.

Capacidad expresiva: la combinación de movimientos permite explorar el espacio completo de algoritmos.

Costo controlado: las modificaciones tienen impacto computacional acotado.

DEFINICIÓN GENERAL DEL VECINDARIO

El vecindario de un AST se define como la unión de varios sub-vecindarios, cada uno asociado a un tipo de transformación estructural:

Vecindario de ajuste de parámetros

Vecindario de reemplazo de subárboles

Vecindario de inserción de subestructuras

Vecindario de poda de subárboles

Vecindario de reordenamiento de componentes

VECINDARIO 1: AJUSTE DE PARÁMETROS

Descripción:
Se modifica el valor de un parámetro numérico terminal del AST sin alterar la estructura del algoritmo.

Ejemplos:

Cambiar el valor de alpha en una heurística greedy-randomizada.

Ajustar la temperatura inicial en un componente de recocido simulado.

Modificar el número de elementos eliminados en una perturbación.

Características:

Movimiento de bajo impacto.

Ideal para intensificación.

No altera la lógica estructural del algoritmo.

VECINDARIO 2: REEMPLAZO DE SUBÁRBOL

Descripción:
Se selecciona un nodo interno del AST y se reemplaza el subárbol correspondiente por otro subárbol generado desde la misma categoría gramatical.

Ejemplo:

Reemplazar una búsqueda local basada en relocate por otra basada en two-opt.

Cambiar el criterio de aceptación de best-improvement a first-improvement.

Características:

Modificación estructural moderada.

Cambia el comportamiento algorítmico.

Útil para diversificación controlada.

VECINDARIO 3: INSERCIÓN DE SUBESTRUCTURA

Descripción:
Se inserta una nueva estructura de control alrededor de un subárbol existente, aumentando la profundidad del AST.

Ejemplo:

Envolver una búsqueda local simple dentro de una estructura de Iterated Local Search.

Añadir una fase de perturbación antes de la búsqueda local.

Características:

Aumenta la complejidad del algoritmo.

Permite descubrir arquitecturas más expresivas.

Movimiento de diversificación fuerte.

VECINDARIO 4: PODA DE SUBÁRBOL

Descripción:
Se elimina una subestructura del AST y se reemplaza por una versión más simple, preservando la validez sintáctica.

Ejemplo:

Eliminar una capa de perturbación.

Sustituir un Iterated Local Search por una búsqueda local directa.

Características:

Reduce complejidad innecesaria.

Previene el crecimiento excesivo del AST.

Favorece la parsimonia algorítmica.

VECINDARIO 5: REORDENAMIENTO DE COMPONENTES

Descripción:
Se modifica el orden de ejecución de componentes secuenciales compatibles dentro del AST.

Ejemplo:

Ejecutar una perturbación antes de la búsqueda local en lugar de después.

Cambiar el orden entre dos fases independientes.

Características:

No introduce nuevos componentes.

Puede alterar significativamente el comportamiento del algoritmo.

Útil para ajustar el flujo de control.

ESTRATEGIA DE EXPLORACIÓN DEL VECINDARIO EN ILS

Búsqueda local:

Se explora un subconjunto del vecindario del AST actual.

Se acepta el primer vecino que mejora el fitness o el mejor encontrado.

Perturbación:

Cuando se alcanza un óptimo local, se aplican uno o más movimientos de inserción o reemplazo estructural.

La intensidad de la perturbación controla el grado de diversificación.

CRITERIO DE ACEPTACIÓN

Un AST vecino se acepta si:

Mejora el valor de la función de fitness.

En algunos casos, se acepta un AST de igual calidad para favorecer la exploración.

RESUMEN EJECUTIVO

El estado del ILS es un AST que representa un algoritmo completo.

El vecindario se define mediante transformaciones sintácticas locales.

ILS alterna intensificación (ajustes finos) y diversificación (cambios estructurales).

Todos los vecinos son algoritmos válidos.

El objetivo es optimizar la lógica algorítmica, no las soluciones del VRPTW.