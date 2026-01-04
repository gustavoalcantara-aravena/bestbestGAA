RESTRICCIONES CANÓNICAS DEL VRPTW (SOLOMON)

Introducción

El VRPTW canónico propuesto por Solomon se define mediante un conjunto de restricciones estructurales y temporales que determinan la factibilidad de una solución. En enfoques metaheurísticos y de Generación Automática de Algoritmos, algunas de estas restricciones se gestionan de forma implícita o mediante penalizaciones, con el fin de favorecer la exploración del espacio de búsqueda.

Las restricciones se describen a continuación a nivel conceptual, sin introducir índices explícitos de vehículo.

Restricción de atención única

Cada cliente debe ser atendido exactamente una vez.

No se permiten clientes no visitados.
No se permiten visitas duplicadas.

Esta restricción garantiza la cobertura completa de la demanda y constituye una restricción estructural básica del VRPTW.

Restricción de inicio y fin en el depósito

Cada ruta debe comenzar y terminar en el depósito.

Todas las rutas parten desde el depósito y regresan a él.
No se permiten caminos abiertos ni ciclos que no incluyan al depósito.

Esta restricción define la estructura cerrada de las rutas.

Restricción de continuidad de ruta (conservación de flujo)

Si una ruta visita un cliente, debe existir continuidad antes y después de dicho cliente.

Para cada cliente, el número de arcos entrantes debe ser igual al número de arcos salientes.

Esta restricción asegura la coherencia estructural de las rutas y evita soluciones fragmentadas o inconsistentes.

Restricción de capacidad del vehículo

La suma de las demandas de los clientes atendidos en una misma ruta no debe exceder la capacidad del vehículo.

En el VRPTW Solomon, los vehículos son homogéneos y la capacidad es común a todas las rutas.

En el contexto de metaheurísticas y GAA, esta restricción puede gestionarse de forma estricta o mediante penalizaciones y operadores de reparación, en función del diseño algorítmico.

Restricción de ventanas de tiempo (ventanas duras)

El servicio a cada cliente debe comenzar dentro de su ventana de tiempo especificada.

Cada cliente i posee un intervalo [e_i, l_i], y el inicio del servicio debe cumplir:

e_i ≤ inicio_i ≤ l_i

En las instancias Solomon, las ventanas de tiempo son duras y definen la factibilidad temporal de las soluciones.

Restricción de precedencia temporal (consistencia del cronograma)

El orden de visita de los clientes debe ser compatible con los tiempos de viaje y de servicio.

Si un cliente i es visitado antes que un cliente j, entonces el inicio del servicio en j debe respetar el tiempo acumulado desde i, considerando desplazamiento y servicio.

Esta restricción evita inconsistencias temporales y es la más costosa de verificar sin optimizaciones específicas. En implementaciones eficientes se emplean técnicas como forward y backward slack para su evaluación en tiempo constante.

Control implícito del número de vehículos

En el VRPTW Solomon no se impone un límite explícito al número de vehículos disponibles.

El número de rutas utilizadas se determina implícitamente por el algoritmo y se minimiza como objetivo primario, conforme al criterio lexicográfico canónico del problema.

Esta característica distingue al VRPTW Solomon de variantes con flota fija.

Implicaciones para GAA

Los algoritmos generados automáticamente deben:

Respetar las restricciones estructurales del problema.

Evaluar la factibilidad temporal de forma eficiente.

Minimizar prioritariamente el número de vehículos y, secundariamente, la distancia total recorrida.

Gestionar posibles infactibilidades mediante penalizaciones y operadores de reparación cuando se requiera favorecer la exploración del espacio de búsqueda.