Plan de Pruebas Técnicas

GRASP + GAA para VRPTW (Solomon)

Este documento define todos los tests que deben existir para garantizar que el sistema es correcto, reproducible y científicamente válido.

Cada test tiene:

Objetivo

Qué se valida

Entrada mínima

Resultado esperado

NIVEL 0 — Pruebas de Infraestructura
TEST-0.1: Arranque del proyecto

Objetivo:
Verificar que el proyecto corre sin errores básicos.

Valida:

Imports correctos

Estructura de carpetas

Configuración mínima

Entrada:
Ejecutar:

python main.py


Resultado esperado:

El programa arranca

Carga configuración

No hay excepciones

TEST-0.2: Carga de config.yaml

Objetivo:
Verificar que la configuración se carga correctamente.

Valida:

Lectura de YAML

Tipos correctos

Valores por defecto

Entrada:
config.yaml mínimo

Resultado esperado:

Objeto config accesible

Parámetros numéricos válidos

Paths existentes

NIVEL 1 — Datos y Parsing
TEST-1.1: Parser Solomon básico

Objetivo:
Verificar que una instancia Solomon se parsea correctamente.

Valida:

Número de nodos

Depósito = nodo 0

Clientes correctamente leídos

Entrada:
C101.txt

Resultado esperado:

instance.n_nodes == 101

instance.depot.id == 0

len(instance.clients) == 100

TEST-1.2: Ventanas de tiempo válidas

Objetivo:
Validar consistencia temporal de los nodos.

Valida:

ready_time ≤ due_date

tiempos no negativos

Entrada:
C101

Resultado esperado:

Ninguna ventana inválida

No excepción

TEST-1.3: Distancias y tiempos de viaje

Objetivo:
Verificar coherencia distancia–tiempo.

Valida:

Simetría de distancias

travel_time = distance (si velocidad = 1)

Resultado esperado:

d(i,j) == d(j,i)

travel_time consistente

NIVEL 2 — BKS
TEST-2.1: Carga de BKS

Objetivo:
Verificar carga correcta del archivo BKS.

Valida:

Mapeo instance_id → (k, d)

Acceso O(1)

Entrada:
bks.csv

Resultado esperado:

Todas las instancias tienen BKS

Ninguna falta

TEST-2.2: Coherencia BKS

Objetivo:
Verificar que BKS es consistente.

Valida:

k_bks > 0

d_bks > 0

Resultado esperado:

No valores inválidos

NIVEL 3 — Modelo de Datos
TEST-3.1: Clase Route

Objetivo:
Validar una ruta individual.

Valida:

Cálculo de distancia

Cálculo de carga

Cálculo de tiempos

Entrada:
Ruta simple: depot → i → depot

Resultado esperado:

Distancia correcta

Carga = demanda(i)

Tiempo factible

TEST-3.2: Clase Solution

Objetivo:
Validar solución completa.

Valida:

Número de rutas

Atención única

Distancia total

Resultado esperado:

Cada cliente aparece una vez

No duplicados

No faltantes

NIVEL 4 — Evaluación de Soluciones
TEST-4.1: Factibilidad completa

Objetivo:
Detectar violaciones duras.

Valida:

Ventanas de tiempo

Capacidad

Atención única

Entrada:
Solución manualmente inválida

Resultado esperado:

feasible = False

penalización > 0

TEST-4.2: Métrica lexicográfica

Objetivo:
Validar orden (V, D).

Valida:

Prioridad de vehículos

Distancia solo si V igual

Resultado esperado:

Comparación correcta

TEST-4.3: Gap respecto a BKS

Objetivo:
Validar cálculo de gap.

Resultado esperado:

gap = 0 si D = D_bks

gap > 0 si peor

gap < 0 si mejora

NIVEL 5 — AST
TEST-5.1: Parser JSON → AST

Objetivo:
Verificar creación correcta del AST.

Valida:

Tipos de nodos

Jerarquía

Profundidad

Entrada:
AST JSON simple

Resultado esperado:

AST válido

Sin nodos inválidos

TEST-5.2: Evaluación determinista del AST

Objetivo:
Garantizar pureza funcional.

Valida:

Mismo input → mismo output

Resultado esperado:

No efectos colaterales

TEST-5.3: Validator de AST

Objetivo:
Detectar AST inválidos.

Valida:

Profundidad máxima

Nº nodos funcionales

Terminales permitidos

Resultado esperado:

AST inválido rechazado

NIVEL 6 — GRASP Constructivo
TEST-6.1: Construcción básica

Objetivo:
Construir solución inicial.

Valida:

Se crean rutas

Se insertan clientes

Resultado esperado:

Solución no vacía

Clientes cubiertos

TEST-6.2: RCL funcional

Objetivo:
Validar componente aleatorizado.

Valida:

Tamaño RCL

Selección aleatoria controlada

Resultado esperado:

Variabilidad con distinta seed

Reproducibilidad con misma seed

NIVEL 7 — Local Search
TEST-7.1: Operador Relocate

Objetivo:
Verificar relocate intra/inter ruta.

Valida:

Mejora o mantiene factibilidad

Resultado esperado:

No rompe restricciones

TEST-7.2: Operador Swap

Objetivo:
Validar intercambio de clientes.

Resultado esperado:

Clientes siguen únicos

Factibilidad preservada

TEST-7.3: Convergencia LS

Objetivo:
Verificar criterio de parada.

Resultado esperado:

LS termina

No bucle infinito

NIVEL 8 — SolutionPool
TEST-8.1: Inserción controlada

Objetivo:
Verificar política del pool.

Valida:

Solo mejores soluciones

Reemplazo correcto

Resultado esperado:

Pool estable

TEST-8.2: Estadísticas agregadas

Objetivo:
Validar métricas globales.

Valida:

mean gap

std

feasible rate

NIVEL 9 — Logging
TEST-9.1: Log por solución

Objetivo:
Verificar trazabilidad.

Valida:
Campos mínimos:

algorithm_id

run_id

instance_id

vehicles

distance

gap

feasible

time

seed

Resultado esperado:

Un log por ejecución

Formato consistente

NIVEL 10 — ExperimentRunner
TEST-10.1: Loop completo

Objetivo:
Ejecutar todo el experimento.

Valida:

algoritmos × runs × instancias

Resultado esperado:

No crashes

Resultados guardados

TEST-10.2: Reproducibilidad

Objetivo:
Validar ciencia reproducible.

Valida:

Misma seed → mismos resultados

NIVEL 11 — Baselines
TEST-11.1: ALGO-1 ejecutable

Objetivo:
Validar baseline mínimo.

Resultado esperado:

Produce solución válida

TEST-11.2: ALGO-2 mejora ALGO-1

Objetivo:
Validar calidad relativa.

Resultado esperado:

gap(ALGO-2) < gap(ALGO-1)

TEST-11.3: ALGO-3 domina

Objetivo:
Validar baseline superior.

Resultado esperado:

gap(ALGO-3) ≤ gap(ALGO-2)

NIVEL 12 — Go / No-Go Final
TEST-12.1: Caso canónico

Objetivo:
Ejecutar C101 end-to-end.

Resultado esperado:

Resultado reproducible

Gap razonable

Logs completos

Regla Final

Si un test no existe → el sistema NO está validado
Si un resultado no se loguea → el resultado NO existe
Si no es reproducible → NO es científico