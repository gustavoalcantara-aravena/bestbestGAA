VRPTW SOLOMON CON GRASP

Panorama del problema

El Vehicle Routing Problem with Time Windows (VRPTW) consiste en diseñar un conjunto de rutas que parten y regresan a un depósito, atendiendo a todos los clientes exactamente una vez, respetando restricciones de capacidad y ventanas de tiempo.

Las instancias de Solomon consideran una flota homogénea, un único depósito, ventanas de tiempo duras y un objetivo lexicográfico: primero minimizar el número de vehículos utilizados y, luego, minimizar la distancia total recorrida.

Las instancias se agrupan en seis clases: C1, C2 (clientes clusterizados), R1, R2 (clientes aleatorios) y RC1, RC2 (distribución mixta). Las clases “1” presentan ventanas de tiempo más ajustadas que las clases “2”.

El VRPTW es un problema NP-hard y se resuelve eficazmente mediante metaheurísticas como GRASP.

Heurística constructiva base (Solomon Sequential Insertion – I1)

GRASP se basa en una fase constructiva aleatorizada. Para VRPTW Solomon, la heurística de inserción secuencial de Solomon es el punto de partida estándar.

Selección del cliente inicial:

cliente más lejano al depósito, o

cliente con la fecha límite (due date) más temprana.

Inserción de clientes:

se evalúan todas las posiciones factibles de inserción de un cliente no atendido en una ruta,

se calcula un costo de inserción que combina incremento de distancia y deterioro temporal,

se selecciona el mejor lugar de inserción para cada cliente candidato.

Criterio de selección:

se priorizan clientes lejanos al depósito con bajo costo de inserción,

este criterio ordena los clientes candidatos.

GRASP:

se construye una lista restringida de candidatos (RCL) con los mejores clientes según el criterio de selección,

el cliente a insertar se elige aleatoriamente desde la RCL,

el proceso se repite hasta que no quedan clientes por insertar,

si un cliente no puede insertarse en ninguna ruta existente, se abre una nueva ruta.

Construcción paralela (opcional)

Como alternativa a la construcción secuencial, pueden inicializarse varias rutas simultáneamente. En cada iteración, un cliente se inserta en la mejor posición factible de cualquiera de las rutas abiertas.

Este enfoque reduce el efecto de la “última ruta” y es compatible con GRASP multi-start.

Fase de mejora local (Local Search)

Tras la construcción inicial, se aplica búsqueda local hasta alcanzar un óptimo local.

Operadores intra-ruta:

Or-Opt (k = 1, 2 o 3): mueve cadenas cortas dentro de una ruta; muy efectivo con ventanas de tiempo ajustadas.

Relocate intra-ruta: mueve un cliente a otra posición dentro de la misma ruta.

Exchange intra-ruta: intercambia dos clientes de una ruta.

2-Opt: invierte un segmento de la ruta; usar con precaución en instancias con ventanas ajustadas.

Operadores inter-ruta:

Relocate inter-ruta: mueve un cliente de una ruta a otra; operador clave para reducir el número de vehículos.

Swap (1-1): intercambia clientes entre dos rutas.

2-Opt*: intercambia los finales de dos rutas distintas.

Cross-Exchange (opcional): intercambia segmentos entre rutas; es potente pero computacionalmente más costoso.

La búsqueda local continúa mientras exista un movimiento que mejore la función objetivo.

Verificación eficiente de factibilidad temporal

Para que GRASP sea eficiente, la factibilidad temporal de inserciones y movimientos debe verificarse en tiempo constante.

Se utilizan variables acumuladas por ruta que resumen la información temporal:

tiempos de llegada más tempranos,

holguras temporales,

tiempos de espera acumulados.

Con esta información, es posible verificar si una inserción o un movimiento mantiene la factibilidad temporal sin recalcular toda la ruta, evitando evaluaciones de orden O(n).

Manejo de restricciones

Ventanas de tiempo:

se tratan como restricciones duras; movimientos que las violan no se aceptan.

Capacidad:

puede tratarse como restricción estricta o

manejarse mediante penalización durante la búsqueda local.

La función objetivo prioriza:

minimizar el número de rutas (vehículos),

minimizar la distancia total recorrida.

Interpretación por clases de instancias

R1 y RC1:

ventanas de tiempo ajustadas,

conviene priorizar operadores que preserven el orden, como Or-Opt y Relocate.

R2:

restricciones temporales más laxas,

predominan operadores espaciales como 2-Opt y Swap.

C1 y C2:

fuerte estructura geométrica,

conviene completar un cluster antes de pasar a otro.

RC:

requieren estrategias balanceadas entre criterios espaciales y temporales.

Este análisis se utiliza para interpretar resultados, no para modificar el algoritmo base.