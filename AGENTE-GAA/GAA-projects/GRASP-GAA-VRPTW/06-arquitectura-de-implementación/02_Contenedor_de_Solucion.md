Contenedor de Solución – VRPTW
Diseño para Implementación (GRASP + GAA)
1. Propósito del Contenedor de Solución

El Contenedor de Solución define la estructura y responsabilidades de los objetos que representan rutas y soluciones completas del VRPTW durante la ejecución de algoritmos heurísticos y metaheurísticos.

Este contenedor:

encapsula el estado de una solución VRPTW

permite evaluación eficiente

gestiona factibilidad y penalizaciones

sirve como unidad básica para GRASP y GAA

separa datos de lógica de búsqueda

2. Principios de Diseño

Encapsulación estricta: cada objeto mantiene su propio estado

Independencia de la metaheurística

Evaluación incremental posible

Compatibilidad con soluciones infactibles

Orden lexicográfico canónico Solomon

Listo para automatización (GAA)

3. Objeto Route (Ruta)
3.1 Definición

Una ruta representa el recorrido de un único vehículo desde el depósito, visitando un subconjunto de clientes y regresando al depósito.

Forma canónica:

[depot, c1, c2, ..., ck, depot]

3.2 Atributos de Route

Obligatorios:

nodes: lista ordenada de nodos

load: demanda acumulada

distance: distancia total

time_feasible: booleano

capacity_feasible: booleano

Opcionales (recomendados):

start_times: lista paralela a nodes

slack_forward, slack_backward (si se usa Savelsbergh)

3.3 Responsabilidades de Route

Una ruta debe:

verificar inserciones (can_insert)

insertar clientes (insert)

remover clientes (remove)

recalcular métricas internas (recompute)

evaluar factibilidad temporal y de capacidad

La ruta no decide movimientos, solo evalúa su impacto.

3.4 Factibilidad de Ruta

Una ruta es factible si:

load ≤ Q

el servicio a cada cliente comienza en [ready, due]

se respetan tiempos de viaje y servicio

Las violaciones deben marcar la ruta como infactible, no abortar la ejecución.

4. Objeto Solution (Solución)
4.1 Definición

Una solución VRPTW es un conjunto de rutas que cubren todos los clientes exactamente una vez.

4.2 Atributos de Solution

Obligatorios:

routes: lista de objetos Route

num_vehicles: número de rutas

total_distance: distancia total

is_feasible: booleano

penalty: penalización escalar

4.3 Responsabilidades de Solution

La solución debe:

agregar y remover rutas

mantener métricas globales actualizadas

verificar cobertura de clientes

evaluar factibilidad global

computar penalizaciones

La solución no conoce BKS ni ranking.

5. Invariantes del Contenedor de Solución

Las siguientes condiciones deben cumplirse tras cada operación:

Todas las rutas comienzan y terminan en el depósito

Cada cliente aparece a lo sumo una vez

No existen rutas vacías

num_vehicles = len(routes)

total_distance = sum(route.distance)

Estas invariantes deben verificarse automáticamente tras modificaciones.

6. Factibilidad Global

Una solución es factible si:

todas las rutas son factibles

no hay clientes duplicados

no hay clientes sin asignar

En GAA se permite factibilidad parcial, controlada por penalizaciones.

7. Penalización

La penalización se usa solo cuando se permiten soluciones infactibles.

Componentes típicos:

exceso de capacidad

violaciones de ventanas de tiempo

violaciones estructurales (opcional)

La penalización:

es escalar

se suma a la evaluación

no reemplaza el criterio lexicográfico

8. Evaluación Canónica (Solomon)

El orden de comparación entre soluciones es:

Menor número de vehículos

Menor distancia total

Formalmente:

(V1, D1) ≺ (V2, D2) si:
V1 < V2, o
V1 = V2 y D1 < D2


Este criterio se aplica:

en GRASP

en SolutionPool

en ranking GAA

9. Qué NO hace el Contenedor de Solución

El contenedor NO:

selecciona heurísticas

aplica búsqueda local

gestiona población

maneja BKS

registra logs

conoce el AST

10. Interacción con Otros Componentes

El Contenedor de Solución es utilizado por:

algoritmos constructivos

operadores de búsqueda local

SolutionPool

sistema de logging

Es el núcleo operativo del sistema.

11. Resumen

El Contenedor de Solución define:

la estructura interna de rutas y soluciones

las invariantes del VRPTW

la base para evaluación eficiente

la interfaz limpia entre datos y búsqueda

Este diseño es:

correcto

minimalista

extensible

alineado con Solomon

listo para implementación asistida por LLM