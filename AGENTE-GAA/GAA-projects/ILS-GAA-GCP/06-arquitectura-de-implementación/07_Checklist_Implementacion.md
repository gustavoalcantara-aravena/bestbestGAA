Checklist de Implementación
GRASP + GAA para VRPTW (Solomon)

Este documento es una lista de verificación técnica.
Nada conceptual: todo lo que aquí aparece debe existir en código.

1. Estructura Base del Proyecto

 Carpeta raíz del proyecto creada

 Subcarpetas definidas:

 src/

 data/

 logs/

 results/

 config/

 docs/

 Separación clara entre:

código

datasets

documentación

resultados

2. Carga de Instancias VRPTW

 Parser Solomon implementado

 Lectura correcta de:

 coordenadas

 demanda

 ventanas de tiempo

 tiempo de servicio

 capacidad del vehículo

 Depósito identificado como nodo 0

 Distancias euclidianas precomputadas

 Tiempos de viaje coherentes con distancia

 Validación básica de datos (nodos, demandas, ventanas)

3. Carga de BKS

 Archivo BKS cargado (CSV o JSON)

 Mapeo instance_id → (k_bks, d_bks)

 Acceso O(1) al BKS durante evaluación

 Validación: todas las instancias tienen BKS

4. Modelo de Datos (Clases)

 Clase Node

 Clase Instance

 Clase Route

 Clase Solution

 Clase Algorithm (AST wrapper)

 Clase SolutionPool

 Clase ExperimentRunner

5. Representación del Algoritmo (AST)

 Definición explícita de nodos del AST

 Tipos de nodos:

 Funcionales (if, select, combine, etc.)

 Terminales (distance, slack, demand, etc.)

 Profundidad máxima controlada

 Número máximo de nodos funcionales controlado

 Evaluación determinista del AST (sin efectos colaterales)

6. GRASP – Fase Constructiva

 Construcción greedy parametrizada por AST

 Lista RCL (Restricted Candidate List)

 Control de aleatoriedad vía semilla

 Inserciones solo factibles (o penalizadas)

 Generación de solución inicial válida (o cuasi-válida)

7. GRASP – Búsqueda Local

 Operadores implementados:

 Relocate (intra/inter)

 Swap

 2-opt / Or-opt (si aplica)

 Verificación eficiente de factibilidad temporal

 Control de movimientos inválidos

 Criterio de parada (no improving / max iters)

 AST controla selección de operador

8. Evaluación de Soluciones

 Cálculo correcto de:

 número de vehículos

 distancia total

 Verificación de:

 atención única

 capacidad

 ventanas de tiempo

 Penalización definida para infactibilidad

 Cálculo de gap respecto a BKS

 Orden lexicográfico respetado

9. SolutionPool

 Pool global inicializado

 Registro de soluciones por:

 algoritmo

 run

 instancia

 Almacenamiento solo de:

 mejores soluciones

 soluciones factibles

 Política clara de reemplazo

 Acceso a estadísticas agregadas

10. Logging y Trazabilidad

 Logger central implementado

 Log por solución generado

 Campos mínimos en logs:

 algorithm_id

 run_id

 instance_id

 vehicles

 distance

 gap

 feasible

 cpu_time

 seed

 Logs en formato CSV o JSON

 Sin logging de bajo nivel (movimientos)

11. Control Experimental

 Semilla global definida

 Semilla derivada por run

 Orden fijo de instancias

 ASTs inmutables durante ejecución

 Sin estado compartido entre runs

12. Ejecutor del Experimento

 Loop:

 algoritmos

 runs

 instancias

 Medición de tiempo por ejecución

 Captura de excepciones por instancia

 Continuación segura ante fallos

 Resultados almacenados incrementalmente

13. Agregación y Ranking

 Agregación por algoritmo:

 mean vehicles

 mean gap

 std gap

 feasible rate

 Ranking lexicográfico correcto

 Selección del algoritmo ganador

 Exportación de resultados finales

14. Análisis del Algoritmo Ganador

 AST serializado

 Profundidad real calculada

 Conteo de nodos funcionales

 Identificación de terminales dominantes

 Registro en archivo dedicado

15. Validación Final

 Corre una instancia simple (C101)

 Resultado reproducible

 No violaciones silenciosas

 Gap coherente con literatura

 Logs completos y consistentes

16. Checklist Final (Go / No-Go)
Ítem	Estado
Parsing correcto	⬜
GRASP funcional	⬜
AST evaluable	⬜
SolutionPool estable	⬜
Logging completo	⬜
Resultados reproducibles	⬜

Solo cuando todos estén en ⬜→✅ el experimento es válido.

17. Regla de Oro

Si algo no puede loguearse, no existe.
Si algo no puede reproducirse, no es científico.