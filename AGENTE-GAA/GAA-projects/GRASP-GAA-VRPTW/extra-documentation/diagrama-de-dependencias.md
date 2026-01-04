1️⃣ Diagrama de Dependencias entre Módulos

(GRASP + GAA + VRPTW)

Visión General (flujo de control)
main.py
  |
  v
ExperimentRunner
  |
  +--> DatasetLoader
  |
  +--> BKSLoader
  |
  +--> AlgorithmRepository
  |        |
  |        +--> Algorithm (AST wrapper)
  |               |
  |               +--> AST Parser
  |               +--> AST Validator
  |
  +--> GRASPSolver
  |        |
  |        +--> ConstructiveHeuristic
  |        |        |
  |        |        +--> AST (decisiones)
  |        |
  |        +--> LocalSearch
  |                 |
  |                 +--> AST (selección operador)
  |
  +--> SolutionEvaluator
  |
  +--> SolutionPool
  |
  +--> Logger
  |
  +--> ReportGenerator / Visualization

Dependencias por módulo (exactas)
main.py

Responsabilidad:

Punto de entrada

Depende de:

ExperimentRunner

config.yaml

No debe depender de:

lógica VRPTW

AST

GRASP

experiment/ExperimentRunner.py

Responsabilidad:

Orquestación completa del experimento

Depende de:

DatasetLoader

BKSLoader

AlgorithmRepository

GRASPSolver

SolutionEvaluator

SolutionPool

Logger

NO debe:

evaluar soluciones directamente

implementar heurísticas

manipular rutas

data/dataset_loader.py

Responsabilidad:

Parsear instancias Solomon

Produce:

Instance

Node

Depende de:

Modelo de datos (Node, Instance)

NO depende de:

GRASP

AST

evaluación

data/bks_loader.py

Responsabilidad:

Cargar BKS

Produce:

dict: instance_id → (k_bks, d_bks)

NO depende de:

soluciones

algoritmos

gaa/algorithm_repository.py

Responsabilidad:

Gestionar algoritmos (ASTs)

Depende de:

AST parser

AST validator

Produce:

Algorithm objects

gaa/algorithm_generator.py

Responsabilidad:

Generar ASTs automáticamente

Depende de:

ast/generator.py

ast/validator.py

Produce:

AST JSON

Algorithm

ast/

Responsabilidad:

Representar lógica del algoritmo

Submódulos:

nodes.py (nodos AST)

parser.py (JSON → AST)

generator.py (AST aleatorio)

validator.py

printer.py

NO depende de:

VRPTW

Solution

GRASP

grasp/grasp_solver.py

Responsabilidad:

Resolver VRPTW con GRASP

Depende de:

Instance

Algorithm (AST)

Solution

Route

SolutionEvaluator (solo para comparar)

Subcomponentes:

Constructive

LocalSearch

solution/solution_container.py

Responsabilidad:

Representar UNA solución

Contiene:

rutas

métricas

factibilidad

NO ejecuta:

GRASP

AST

solution/solution_pool.py

Responsabilidad:

Mantener mejores soluciones

Depende de:

Solution

evaluation/solution_evaluator.py

Responsabilidad:

Evaluar UNA solución

Calcula:

vehicles

distance

feasibility

penalties

gap

NO:

modifica soluciones

controla experimentos

experiment/logging

Responsabilidad:

Trazabilidad

Depende de:

Solution

Algorithm

Resultados evaluación

Regla de dependencias (importante)
Experiment → Solver → Solution → Evaluator
Experiment → AST
AST → NADA del dominio


👉 Nunca al revés.