Q6: Tres Algoritmos Específicos de Referencia
Introducción

Este documento define tres algoritmos heurísticos concretos que se utilizan como algoritmos de referencia (baselines) durante la experimentación del marco GAA–VRPTW.

Estos algoritmos representan estrategias clásicas y bien conocidas en la literatura del VRPTW, y cumplen dos propósitos principales:

Servir como puntos de comparación cuantitativa frente a los algoritmos generados automáticamente por el GAA.

Proveer estructuras semilla y patrones de diseño que el sistema GAA puede eventualmente redescubrir, combinar o mejorar.

Importante:

Estos algoritmos NO son optimizados ni modificados por el proceso de GAA.

Se implementan como heurísticas fijas, con estructura y parámetros constantes.

Se expresan como ASTs definidos manualmente, utilizando el mismo DSL que el GAA, para garantizar comparabilidad estructural directa.

Algoritmo 1: Baseline Constructivo Puro

Nombre largo:
Sequential Insertion Heuristic (Solomon-inspired baseline)

Acrónimo:
ALGO-1-SEQINS

Descripción

Algoritmo puramente constructivo inspirado en el heurístico I1 de Solomon. Construye una solución mediante inserción secuencial de clientes, priorizando cercanía espacial y respetando restricciones de ventanas de tiempo y capacidad.

No incluye fase de búsqueda local.

Características principales:

Algoritmo simple y rápido

Determinista con semilla fijada

Calidad de solución limitada

Utilizado como baseline inferior

Estructura AST (fija)

Seq
→ GreedyConstruct
(No incluye Local Search)

Terminales utilizados

Distance(i, j)

ReadyTime(i)

DueDate(i)

Demand(i)

Funciones utilizadas

Seq

GreedyConstruct

Parámetros de ejecución

Número de iteraciones: 1

Tiempo máximo por instancia: 30 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

Desempeño esperado (orientativo)

Los valores indicados son estimaciones cualitativas basadas en la literatura y en el comportamiento típico de heurísticas similares.

C1: 8–12%

C2: 2–4%

R1: 15–25%

R2: 1–3%

RC1: 10–15%

RC2: 3–5%

Rol en el experimento

Baseline inferior

Validación del parser, evaluador y pipeline experimental

Punto de referencia mínimo aceptable

Algoritmo 2: Regret Insertion con Enfoque Temporal

Nombre largo:
Regret Insertion with Temporal Urgency Focus

Acrónimo:
ALGO-2-REGRET

Descripción

Algoritmo constructivo que prioriza la factibilidad temporal mediante el uso del criterio de regret. Los clientes con mayor urgencia temporal y mayor pérdida potencial si no son insertados temprano reciben prioridad.

Incluye una fase de búsqueda local basada en Or-Opt.

Características principales:

Especializado en ventanas de tiempo ajustadas

Mejor factibilidad que ALGO-1

Calidad intermedia

Determinista con semilla fijada

Estructura AST (fija)

Seq
→ GreedyConstruct (Urgency + Regret + Distance)
→ LocalSearch (OrOpt)

Terminales utilizados

Urgency(i)

Regret(i)

Distance(i, j)

ForwardSlack(i)

Demand(i)

Funciones utilizadas

Seq

GreedyConstruct

LocalSearch

OrOpt

Parámetros de ejecución

Construcción: 1 iteración

Local Search: hasta 50 iteraciones

Tiempo máximo por instancia: 60 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

Desempeño esperado (orientativo)

C1: 4–7%

C2: 3–6%

R1: 5–10%

R2: 2–5%

RC1: 6–10%

RC2: 3–6%

Rol en el experimento

Baseline medio

Referencia para instancias con presión temporal

Validación de combinación constructivo + búsqueda local

Algoritmo 3: Algoritmo Híbrido Adaptativo Temporal–Espacial

Nombre largo:
Adaptive Construction with Temporal–Spatial Balancing

Acrónimo:
ALGO-3-HYBRID

Descripción

Algoritmo adaptativo que ajusta su estrategia de construcción y mejora según las características de la instancia:

Si las ventanas de tiempo son estrictas, prioriza urgencia y regret.

Si el horizonte temporal es amplio, prioriza criterios espaciales.

En instancias mixtas, balancea ambos enfoques.

Incluye búsqueda local adaptativa con selección dinámica de operadores.

Características principales:

Algoritmo híbrido y versátil

Adecuado para todas las familias Solomon

Representa un baseline superior

Inspiración directa para el GAA

Estructura AST (fija)

Seq
→ AnalyzeInstance
→ If (TightTimeWindows)
  → GreedyConstruct (Urgency + Regret)
 Else
  → GreedyConstruct (Distance + Savings)
→ LocalSearch (operador adaptativo)

Terminales utilizados

Distance(i, j)

Urgency(i)

Regret(i)

Slack(i)

Demand(i)

CapacityUtilization()

Funciones utilizadas

Seq

AnalyzeInstance

If

GreedyConstruct

LocalSearch

OrOpt

TwoOpt

SelectBest

Parámetros de ejecución

Construcción: 1 iteración

Local Search: hasta 100 iteraciones

Tiempo máximo por instancia: 90 segundos

Aleatoriedad: semilla fijada (determinismo reproducible)

Desempeño esperado (orientativo)

C1: 3–6%

C2: 2–4%

R1: 4–8%

R2: 1–3%

RC1: 3–7%

RC2: 2–4%

Rol en el experimento

Baseline superior

Referencia aspiracional

Validación de mecanismos adaptativos

Benchmark directo para evaluar el GAA

Interpretación para el GAA

Estos algoritmos permiten evaluar si el proceso de Generación Automática de Algoritmos es capaz de:

Redescubrir patrones heurísticos conocidos

Combinar criterios temporales y espaciales de forma efectiva

Superar heurísticas manuales bien diseñadas

El algoritmo generado automáticamente por el GAA se espera que alcance o supere el desempeño de ALGO-3-HYBRID, especialmente en instancias mixtas (RC1, RC2).

Fecha: 4 de enero de 2026
Estado: Documento listo para implementación y experimentación