DEFINICIÓN DEL PROBLEMA DE OPTIMIZACIÓN

IDENTIDAD DEL PROBLEMA

Nombre oficial: Graph Coloring Problem
Acrónimo: GCP
Tipo de optimización: Minimización
Categoría: Optimización Combinatoria (NP-Hard)

DESCRIPCIÓN INFORMAL

El Graph Coloring Problem (GCP) consiste en asignar colores a los vértices de un grafo de tal manera que ningún par de vértices adyacentes, es decir, conectados por una arista, tenga el mismo color. El objetivo es realizar dicha asignación utilizando el menor número posible de colores, garantizando que todas las restricciones de adyacencia sean satisfechas.

Este problema aparece en múltiples contextos prácticos, tales como la asignación de frecuencias, la planificación de horarios, la asignación de registros en compiladores y la resolución de conflictos entre tareas. Desde el punto de vista computacional, el GCP es un problema NP-Hard, por lo que resulta especialmente relevante el uso de metaheurísticas y enfoques aproximados para instancias de gran tamaño.

VARIABLES DE DECISIÓN (CONCEPTUAL)

Asignación de color a un vértice: determina qué color se asigna a cada vértice del grafo.

Uso de un color: indica si un color es utilizado por al menos un vértice.

Número total de colores utilizados: cantidad total de colores distintos empleados en la solución.

PARÁMETROS DEL PROBLEMA

Grafo G = (V, E): donde V es el conjunto de vértices y E es el conjunto de aristas.

Conjunto de colores C: conjunto finito de colores potenciales disponibles.

Relación de adyacencia: definida por las aristas del grafo.

RESTRICCIONES (CONCEPTUAL)

Dos vértices adyacentes no pueden compartir el mismo color.

Cada vértice debe recibir exactamente un color.

Un color se considera utilizado si al menos un vértice es asignado a él.

MODELO MATEMÁTICO (FORMAL)

Conjuntos y parámetros:

V: conjunto de vértices del grafo.

E: conjunto de aristas, donde cada arista conecta dos vértices adyacentes.

C: conjunto de colores potenciales.

Variables de decisión:

x(v,c): variable binaria que vale 1 si el vértice v es asignado al color c, y 0 en caso contrario.

y(c): variable binaria que vale 1 si el color c es utilizado, y 0 en caso contrario.

FUNCIÓN OBJETIVO

Minimizar el número total de colores utilizados:

Minimizar
suma sobre c en C de y(c)

RESTRICCIONES

Asignación única de color por vértice

Cada vértice debe ser asignado exactamente a un color:

Para todo v en V:
suma sobre c en C de x(v,c) = 1

Restricción de adyacencia

Dos vértices adyacentes no pueden compartir el mismo color:

Para toda arista (u,v) en E y para todo c en C:
x(u,c) + x(v,c) ≤ 1

Activación del uso del color

Un color se considera utilizado si al menos un vértice es asignado a él:

Para todo v en V y para todo c en C:
x(v,c) ≤ y(c)

Dominio de las variables

Para todo v en V y todo c en C:
x(v,c) pertenece a {0,1}
y(c) pertenece a {0,1}

Si quieres, en el próximo mensaje puedo:

darte una versión aún más conceptual (sin binarios, ideal para metaheurísticas),

o adaptar este modelo exactamente a la narrativa de GAA que usas en tu doctorado.

ok, vamos sin binarios para metaheuristicas

Excelente, vamos entonces a la formulación canónica SIN variables binarias, pensada explícitamente para metaheurísticas (GRASP, SA, ILS, Tabú, GAA, etc.).
Todo va en texto plano, listo para Notes.

DEFINICIÓN DEL PROBLEMA DE OPTIMIZACIÓN

IDENTIDAD DEL PROBLEMA

Nombre oficial: Graph Coloring Problem
Acrónimo: GCP
Tipo de optimización: Minimización
Categoría: Optimización Combinatoria (NP-Hard)

DESCRIPCIÓN INFORMAL

El Graph Coloring Problem (GCP) consiste en asignar colores a los vértices de un grafo de forma tal que ningún par de vértices adyacentes comparta el mismo color. El objetivo es encontrar una asignación válida que utilice el menor número posible de colores.

Desde la perspectiva de las metaheurísticas, el GCP se aborda como un problema de búsqueda en un espacio discreto de soluciones, donde cada solución representa una coloración completa del grafo. La calidad de una solución se mide principalmente por el número de colores utilizados y, en formulaciones relajadas, por el número de conflictos presentes.

VARIABLES DE DECISIÓN (CONCEPTUAL)

c(v): color asignado al vértice v.

Cmax: número total de colores distintos utilizados en la solución (máximo color asignado).

PARÁMETROS DEL PROBLEMA

Grafo G = (V, E), donde V es el conjunto de vértices y E el conjunto de aristas.

Conjunto de colores potenciales, representados por los enteros positivos.

Relación de adyacencia definida por las aristas del grafo.

RESTRICCIONES (CONCEPTUAL)

Restricción de adyacencia: para todo par de vértices adyacentes, los colores asignados deben ser distintos.

Restricción de dominio: cada vértice debe ser asignado a un único color válido.

Restricción implícita de factibilidad: la solución no debe contener conflictos de coloración.

MODELO MATEMÁTICO (FORMAL – ENFOQUE METAHEURÍSTICO)

Sea G = (V, E) un grafo no dirigido.

Variables de decisión:

Para cada vértice v en V, se define una variable entera:
c(v) ∈ {1, 2, ..., Cmax}

FUNCIÓN OBJETIVO

Minimizar el número de colores utilizados en la coloración:

Minimizar
Cmax = máximo de c(v) para todo v en V

RESTRICCIONES

Restricción de adyacencia

Para toda arista (u, v) en E:
c(u) ≠ c(v)

Dominio de las variables

Para todo v en V:
c(v) pertenece a los enteros positivos

FORMULACIÓN EQUIVALENTE USADA EN METAHEURÍSTICAS (CON CONFLICTOS)

En enfoques metaheurísticos es común permitir soluciones no factibles durante la búsqueda y penalizar los conflictos.

Definiciones adicionales:

Un conflicto ocurre cuando dos vértices adyacentes comparten el mismo color.

Conf(c) representa el número total de conflictos en la solución.

FUNCIÓN OBJETIVO PENALIZADA

Minimizar
F(c) = Cmax + λ * Conf(c)

donde λ es un parámetro de penalización suficientemente grande para priorizar soluciones factibles.

Esta formulación permite:

explorar el espacio de soluciones de forma más flexible,

definir movimientos simples (recoloración de un vértice),

integrar fácilmente estrategias de búsqueda local, perturbaciones y aprendizaje adaptativo.