DEFINICIÓN DEL PROBLEMA DE OPTIMIZACIÓN

IDENTIDAD DEL PROBLEMA

Nombre oficial: Vehicle Routing Problem with Time Windows
Acrónimo: VRPTW
Tipo de optimización: Minimización
Categoría: Optimización combinatoria (NP-Hard)

DESCRIPCIÓN

El Vehicle Routing Problem with Time Windows (VRPTW) consiste en determinar un conjunto de rutas que parten y regresan a un depósito, de modo que todos los clientes sean atendidos exactamente una vez, respetando restricciones de capacidad y ventanas de tiempo.

Cada cliente posee una demanda conocida y un intervalo de tiempo durante el cual debe iniciarse el servicio. Los vehículos son homogéneos y tienen capacidad limitada. El objetivo es minimizar el costo total de las rutas, usualmente medido como la distancia total recorrida, garantizando la factibilidad respecto a las restricciones de capacidad y ventanas de tiempo, o bien penalizando adecuadamente las violaciones en enfoques heurísticos y metaheurísticos.

VARIABLES DE DECISIÓN (CONCEPTUAL)

Asignación de clientes a rutas.
Secuencia de visita de los clientes dentro de cada ruta.
Uso de arcos entre pares de nodos.
Tiempo de inicio de servicio en cada cliente.
Asignación implícita de clientes a vehículos.

PARÁMETROS DEL PROBLEMA

Conjunto de nodos (clientes y depósito).
Costo o distancia de viaje entre cada par de nodos.
Tiempo de viaje entre cada par de nodos.
Demanda de cada cliente.
Capacidad de los vehículos.
Ventana de tiempo asociada a cada nodo.
Tiempo de servicio en cada cliente.
El número de vehículos no se encuentra acotado explícitamente y se determina implícitamente como parte del proceso de optimización.


RESTRICCIONES (CONCEPTUAL)

Cada cliente debe ser atendido exactamente una vez por un único vehículo.
Todas las rutas comienzan y terminan en el depósito.
La capacidad del vehículo no debe ser excedida a lo largo de cada ruta; las posibles violaciones son tratadas mediante operadores de reparación, penalizaciones o funciones de evaluación dentro del marco metaheurístico.
El servicio a cada cliente debe iniciarse dentro de su ventana de tiempo.
La factibilidad temporal de las rutas debe respetar los tiempos de viaje y los tiempos de servicio.
No se permiten ciclos o subtours que no incluyan al depósito.


MODELO MATEMÁTICO (FORMAL) DEL VRPTW – SIN ÍNDICE DE VEHÍCULO (Solomon)
CONJUNTOS
V = {0, 1, 2, …, n}, conjunto de nodos, donde 0 representa el depósito.
C = V \ {0}, conjunto de clientes.

PARÁMETROS
c_ij : costo o distancia asociada al viaje desde el nodo i al nodo j.
τ_ij : tiempo de viaje desde el nodo i al nodo j.
d_i : demanda del cliente i.
Q   : capacidad homogénea del vehículo.
[a_i, b_i] : ventana de tiempo asociada al nodo i.
s_i : tiempo de servicio requerido en el nodo i.
M   : constante suficientemente grande.


Observa:
No aparece K
Tiempo y costo están separados
Totalmente coherente con Solomon

VARIABLES DE DECISIÓN
x_ij ∈ {0,1} :
    vale 1 si algún vehículo viaja directamente del nodo i al nodo j, y 0 en caso contrario.

t_i ≥ 0 :
    tiempo de inicio del servicio en el nodo i.

Dado que el modelo no incluye un índice explícito de vehículo, las restricciones de capacidad por ruta y el control del número de vehículos no se imponen de forma explícita en el modelo matemático, sino que se gestionan mediante la función objetivo y operadores de construcción, evaluación y reparación dentro del marco metaheurístico y de Generación Automática de Algoritmos.


FUNCIÓN OBJETIVO

En las instancias de Solomon, el objetivo es de tipo lexicográfico: en primer lugar se minimiza el número de vehículos utilizados y, en segundo lugar, la distancia total recorrida.

En el modelo sin índice de vehículo, el número de vehículos utilizados se obtiene implícitamente a partir del número de arcos que salen del depósito. Para su implementación en enfoques metaheurísticos y de Generación Automática de Algoritmos, este objetivo se expresa mediante la siguiente función ponderada:

Minimizar:

α · (sumatoria sobre j en C de x_0j) + (sumatoria sobre i en V y j en V de c_ij · x_ij)

donde α es una constante suficientemente grande para garantizar que la minimización del número de vehículos tenga prioridad sobre la minimización de la distancia total recorrida.

RESTRICCIONES

Atención única de cada cliente:

Para todo i en C:
Sumatoria sobre j en V de x_ij = 1

Conservación de flujo en los clientes:

Para todo i en C:
Sumatoria sobre j en V de x_ij = Sumatoria sobre j en V de x_ji

Inicio y fin de rutas en el depósito:

Las rutas comienzan y terminan en el depósito. El número de rutas utilizadas se determina implícitamente a través de las variables x_0j y forma parte del objetivo de optimización, por lo que no se impone una restricción explícita sobre el número de vehículos.

Restricciones temporales (propagación del tiempo):

Para todo i, j en V:
t_j ≥ t_i + s_i + τ_ij − M · (1 − x_ij)

Ventanas de tiempo:

Para todo i en V:
a_i ≤ t_i ≤ b_i

Dominio de las variables:

Para todo i, j en V:
x_ij ∈ {0, 1}

Para todo i en V:
t_i ≥ 0

Comentario sobre la capacidad:

En este modelo no se incluyen explícitamente restricciones de capacidad debido a la ausencia de un índice de vehículo. La factibilidad respecto a la capacidad se controla mediante operadores de construcción, penalización y reparación dentro del marco metaheurístico y de Generación Automática de Algoritmos.