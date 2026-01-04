Modelo de Datos – VRPTW (Arquitectura de Implementación)
1. Propósito del Modelo de Datos

Este documento define el modelo de datos base utilizado para implementar algoritmos heurísticos y metaheurísticos para el Vehicle Routing Problem with Time Windows (VRPTW), en el contexto de GRASP y Generación Automática de Algoritmos (GAA).

El modelo de datos:

representa instancias VRPTW (clientes, depósito, distancias)

define rutas individuales (vehículos)

define soluciones completas (conjunto de rutas)

permite evaluación eficiente, factibilidad y penalización

es independiente de la lógica de búsqueda y del método maestro

2. Principios de Diseño

El modelo de datos cumple los siguientes principios:

Separación de responsabilidades: datos ≠ búsqueda ≠ evaluación

Compatibilidad Solomon: ventanas duras, capacidad homogénea

Evaluación incremental posible

Factibilidad parcial permitida (para GAA)

Estructuras simples y auditables

Sin dependencia de metaheurística específica

3. Entidades Fundamentales
3.1 Cliente (Customer)

Representa un cliente del VRPTW.

Atributos obligatorios:

id: identificador único

x, y: coordenadas espaciales

demand: demanda del cliente

ready_time: inicio de la ventana de tiempo (e_i)

due_time: fin de la ventana de tiempo (l_i)

service_time: tiempo de servicio

Notas:

Las ventanas de tiempo son duras (Solomon).

El tiempo de viaje se asume proporcional a la distancia.

3.2 Instancia VRPTW (VRPTWInstance)

Representa una instancia completa del problema.

Componentes:

conjunto de clientes

identificador del depósito

capacidad homogénea del vehículo

matriz de distancias (precomputada)

Atributos:

customers: diccionario {id → Customer}

depot_id: entero (usualmente 0)

vehicle_capacity: capacidad Q

distance_matrix[i][j]: distancia entre nodos

Notas:

La matriz de distancias debe precomputarse para eficiencia.

No contiene lógica de solución.

4. Ruta (Route)

Una ruta representa un vehículo y su secuencia de visitas.

4.1 Estructura de la Ruta

Una ruta contiene:

nodes: lista ordenada de nodos
Formato canónico: [depot, c1, c2, ..., ck, depot]

load: demanda acumulada

distance: distancia total

time_feasible: indicador de factibilidad temporal

capacity_feasible: indicador de factibilidad de capacidad

Opcional (pero recomendado):

start_times: tiempos de inicio de servicio por nodo

4.2 Responsabilidades de Route

Una ruta debe ser capaz de:

verificar si una inserción es factible

insertar o remover clientes

recalcular su estado interno

evaluar factibilidad temporal y de capacidad

La ruta no decide qué movimiento aplicar; solo evalúa.

4.3 Factibilidad en la Ruta

Una ruta es factible si:

la carga total ≤ capacidad del vehículo

el servicio a cada cliente comienza dentro de su ventana

se respeta la precedencia temporal entre visitas

Las violaciones pueden:

marcar la ruta como infactible

contribuir a una penalización (para GAA)

5. Solución (Solution)

Una solución VRPTW es un conjunto de rutas.

5.1 Estructura de la Solución

Atributos principales:

routes: lista de objetos Route

num_vehicles: número de rutas

total_distance: suma de distancias

is_feasible: factibilidad global

penalty: penalización acumulada

5.2 Responsabilidades de Solution

La solución debe:

agregar y remover rutas

mantener métricas globales actualizadas

evaluar factibilidad global

calcular penalizaciones si existen violaciones

La solución no conoce BKS ni ranking; eso pertenece a capas superiores.

6. Factibilidad Global

Una solución es factible si:

todas las rutas son factibles

todos los clientes aparecen exactamente una vez

no existen rutas vacías o degeneradas

En enfoques GAA, se permite:

factibilidad parcial

penalización suave de violaciones

comparación de soluciones infactibles

7. Penalización (para GAA)

Cuando se permiten soluciones infactibles, la penalización se define como:

exceso de capacidad por ruta

violaciones de ventanas de tiempo

penalización escalar agregada a la evaluación

La penalización:

no reemplaza las métricas canónicas

solo se usa para guiar la búsqueda

8. Lo que el Modelo de Datos NO hace

El modelo de datos NO debe:

implementar GRASP

implementar búsqueda local

implementar operadores de vecindario

manejar BKS

manejar logging

manejar AST o GAA

Estas responsabilidades pertenecen a capas superiores.

9. Relación con Otras Carpetas

Este modelo de datos es utilizado por:

06/02_Contenedor_de_Solucion.md

06/03_SolutionPool_GRASP_GAA.md

06/04_Logging_y_Trazabilidad.md

06/05_Estructura_Codigo_Pseudocodigo.md

10. Resumen

El modelo de datos define una base sólida, minimalista y extensible para:

VRPTW Solomon

GRASP clásico

Generación Automática de Algoritmos

evaluación reproducible

implementación asistida por LLM

Es la columna vertebral del sistema de optimización.