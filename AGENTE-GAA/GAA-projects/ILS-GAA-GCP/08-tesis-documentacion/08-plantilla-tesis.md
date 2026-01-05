# Q7: Plantilla de Documentación de Tesis/Paper

## Introducción

Este documento proporciona la **plantilla estructural** para la tesis final o paper académico que reporte los resultados del proyecto **GAA para VRPTW**.

**Objetivo:** Proporcionar un esquema coherente que asegure que toda la documentación anterior (Q1-Q6) se integre armónicamente en el documento final.

---

## Estructura Recomendada para Tesis de Máster / Paper ESWA

### **PORTADA Y PRELIMINARES**

```
[ Portada oficial universidad ]
[ Título: "Automatic Algorithm Design for Vehicle Routing Problem with 
          Time Windows using Genetic Programming: A GRASP-based Approach" ]

Autor(es): [Nombre(s)]
Asesor(es): [Nombres]
Fecha: [4 de Enero de 2026]
Institución: [Universidad/Centro]

RESUMEN EJECUTIVO (200-300 palabras)
- Problema tratado
- Metodología propuesta (GAA + GRASP + GP)
- Resultados principales (gap conseguido, mejora respecto a baselines)
- Impacto y aplicaciones

ABSTRACT (English, idéntico al resumen)

ÍNDICE GENERAL
ÍNDICE DE FIGURAS
ÍNDICE DE TABLAS
```

---

## **CAPÍTULO 1: INTRODUCCIÓN**

### **1.1 Motivación y Contexto**

**Fuente:** Q1 (Definición del Problema)

```markdown
- Importancia del VRPTW en logística
- Dificultad computacional (NP-Hard)
- Limitaciones de métodos exactos en instancias grandes
- Relevancia de heurísticas y metaheurísticas
- Brecha: Necesidad de diseño sistemático de heurísticas
```

### **1.2 Pregunta de Investigación**

```markdown
¿Es posible usar Programación Genética para descobrir automáticamente 
la lógica heurística óptima para VRPTW que supere a algoritmos 
diseñados manualmente y que generalice a nuevas instancias?
```

### **1.3 Objetivos**

**Objetivo General:**
```
Desarrollar un marco de Generación Automática de Algoritmos (GAA) 
basado en GRASP y Programación Genética para descubrir automáticamente 
algoritmos heurísticos de alta calidad para el VRPTW.
```

**Objetivos Específicos:**
```
1. Especificar formalmente el Problema Maestro de GAA para VRPTW
2. Definir los conjuntos de funciones y terminales válidos para GP
3. Implementar GRASP como metaheurística de alto nivel
4. Generar y evaluar múltiples algoritmos candidatos
5. Validar que algoritmos generados superan baselines manuales
6. Analizar características de mejores algoritmos descubiertos
```

### **1.4 Contribuciones Principales**

```markdown
- Framework GAA formal para VRPTW
- Demostración de efectividad de GP en AAD para VRPTW
- Conjuntos de terminales y funciones derivados de literatura
- Algoritmos descubiertos que superan a Solomon I1 + 2-Opt
- Análisis de patrones en heurísticas automáticamente generadas
```

### **1.5 Organización del Documento**

```
Cap. 1: Introducción
Cap. 2: Estado del Arte (Literature Review)
Cap. 3: Formulación del Problema
Cap. 4: Metodología Propuesta (GAA)
Cap. 5: Diseño Experimental
Cap. 6: Resultados y Análisis
Cap. 7: Conclusiones y Trabajo Futuro
Apéndices: Detalles técnicos, pseudocódigos, tablas
```

---

## **CAPÍTULO 2: ESTADO DEL ARTE**

### **2.1 Vehicle Routing Problem with Time Windows (VRPTW)**

**Fuente:** Q1 (Definición Problema) + Q3 (Dataset)

**Secciones:**

```markdown
2.1.1 Definición y Formulación Matemática
  - Conjuntos, parámetros, variables
  - Función objetivo jerárquica
  - Restricciones canónicas (7 restricciones)
  
2.1.2 Complejidad Computacional
  - NP-hardness proof sketch
  - Tricotomía (TSP + BPP + Scheduling)
  
2.1.3 Instancias de Benchmark
  - Solomon (56 instancias)
  - Características de familias (C1, C2, R1, R2, RC1, RC2)
  - Homberger (escalabilidad a N=1000)
  
2.1.4 Límites de Métodos Exactos
  - Branch-and-price
  - Column generation
  - Impracticabilidad en N>100
```

### **2.2 Heurísticas Constructivas**

**Fuente:** Q2 (Literatura)

```markdown
2.2.1 Solomon Sequential Insertion (I1)
  - Algoritmo fundacional
  - Criterios de inserción: c11, c12, c2
  
2.2.2 Extensiones Modernas
  - Parallel insertion
  - Regret insertion
  - Time-oriented insertion
  
2.2.3 Operadores de Mejora Local (Neighborhood Operators)
  - Intra-ruta: 2-Opt, Or-Opt
  - Inter-ruta: Relocate, Swap, 2-Opt*
  - Especialidades por familia de instancia
```

### **2.3 Metaheurísticas para VRP**

```markdown
2.3.1 Tabu Search (TS)
  - Memoria corta
  - Granular Tabu Search (GTS)
  
2.3.2 Genetic Algorithms (GA) y Memetic Algorithms
  - Representación de permutación
  - Crossover operators (OX, BCRC)
  
2.3.3 Adaptive Large Neighborhood Search (ALNS)
  - Destroy operators (Random, Worst, Shaw Removal)
  - Repair operators (Regret Insertion)
  - Mecanismos adaptativos
  
2.3.4 GRASP (Greedy Randomized Adaptive Search Procedure)
  - Fases: Construcción aleatoria + Local search
  - Historial de exitosas aplicaciones en VRP
```

### **2.4 Automated Algorithm Design (AAD) y Hyper-heuristics**

**Fuente:** Q2 (Literatura)

```markdown
2.4.1 Selection Hyper-heuristics
  - Choice functions
  - Machine Learning approaches
  
2.4.2 Generation Hyper-heuristics (Genetic Programming)
  - Evolucionar código/lógica, no soluciones
  - AST representation
  - Terminal sets y function sets
  
2.4.3 Antecedentes en VRP
  - Grammatical Evolution para VNS
  - GP para hyper-heuristics en scheduling
  - Éxito limitado pero promisorio
```

### **2.5 Síntesis y Brecha de Investigación**

```markdown
- Métodos exactos impracticables para N grande
- Heurísticas manuales requieren ingeniería exhaustiva
- ALNS representa estado del arte (pero aún requiere diseño)
- AAD con GP promete automatizar descubrimiento
- Falta evidencia empírica fuerte de GP en VRPTW específicamente
```

---

## **CAPÍTULO 3: FORMULACIÓN DEL PROBLEMA**

### **3.1 Definición Formal del VRPTW**

**Fuente:** Q1 (completo)

```markdown
3.1.1 Notación Matemática
3.1.2 Restricciones Canónicas (7)
3.1.3 Objetivo Jerárquico: (Vehículos, Distancia)
3.1.4 Formulación de Programación Entera Mixta (MIP)
3.1.5 Relajaciones y Penalizaciones Suaves
```

### **3.2 Problema Maestro de GAA**

**Fuente:** Q4 (Método Maestro)

```markdown
3.2.1 Formulación del Espacio de Programas P(F,T)
  p* = arg max_{p ∈ P(F,T)} Fitness(p)
  
3.2.2 Interpretación: Optimización de Lógica, no Soluciones
  - Meta-nivel: algoritmo → AST
  - Base-nivel: ejecución del AST en instancia → solución
  
3.2.3 Diferencia con Optimización Directa de Soluciones
  - No es un GA tradicional que evoluciona soluciones
  - Es un GP que evoluciona el programa/heurística
```

### **3.3 Función de Fitness**

**Fuente:** Q4 + Q5

```markdown
Fitness(p) = -1/|I| * Σ_{i ∈ I} [α*V(s_i) + β*D(s_i) + γ*P(s_i)]

Donde:
  p: programa AST candidato
  i: instancia en benchmark
  s_i: solución generada por p en instancia i
  V(s_i): # vehículos (métrica primaria)
  D(s_i): distancia total (métrica secundaria)
  P(s_i): penalización por infactibilidad
  
  α ≫ β ≫ γ: pesos jerárquicos
```

---

## **CAPÍTULO 4: METODOLOGÍA PROPUESTA**

### **4.1 Componentes del Framework GAA**

```markdown
4.1.1 Fase 1: Definición de Primitivos
  - Terminal set: 9 terminales (distancia, demanda, urgencia, etc.)
  - Function set: 11 funciones (Seq, If, While, GreedyConstruct, etc.)
  - Restricciones: Profundidad ≤ 3, Funciones ≤ 2
  
4.1.2 Fase 2: Generador Aleatorio de ASTs
  - Respeto a restricciones
  - Control de bloat (parsimony pressure)
  - Inicialización válida
  
4.1.3 Fase 3: Evaluador de Fitness
  - Ejecución segura de AST en instancia
  - Cálculo de métrica primaria/secundaria
  - Acceso O(1) a BKS
  
4.1.4 Fase 4: GRASP para Problema Maestro
  - Construcción aleatoria: generar AST
  - Local search: mutaciones estructurales (cambiar terminal, función)
  - Iteraciones con presupuesto computacional
```

### **4.2 GRASP (Metaheurística de Alto Nivel)**

**Fuente:** Q4

```markdown
4.2.1 Fases de GRASP
  
  CONSTRUCCIÓN:
    - Generar AST aleatorio respetando restricciones
    - Evaluación rápida (fitness en Design Set)
    - Resultado: solución candidata
  
  BÚSQUEDA LOCAL:
    - Mutaciones: reemplazar terminal, operador, rama
    - Evaluación de vecinos
    - Mejora iterativa hasta convergencia o límite
  
  ACTUALIZACIÓN GLOBAL:
    - Mantener mejor AST encontrado
    - Reinicio con nueva semilla para exploración

4.2.2 Parámetros de GRASP
  - Iteraciones: 10 ejecuciones independientes (Q5)
  - Semillas: {42, 43, ..., 51}
  - Presupuesto: hasta 100 segundos por iteración
```

### **4.3 Implementación Técnica**

```markdown
4.3.1 Representación de AST
  - Árbol con nodos (función/terminal)
  - Serialización JSON para persistencia
  - Deserialización para ejecución
  
4.3.2 Verificación de Restricciones
  - Profundidad máxima (DFS)
  - Conteo de funciones (BFS)
  - Validez de composición
  
4.3.3 Ejecución Segura
  - Timeouts para evitar loops infinitos
  - Manejo de excepciones (infactibilidad)
  - Logging de traza para debugging
```

---

## **CAPÍTULO 5: DISEÑO EXPERIMENTAL**

### **5.1 Protocolo Experimental**

**Fuente:** Q5 (Experimento Computacional)

```markdown
5.1.1 Divición del Dataset
  - Design Set: R1, C1 (18 instancias)
    Propósito: guiar evolución del GAA
  - Selection Set: RC1 (8 instancias)
    Propósito: detectar overfitting
  - Evaluation Set: R2, C2, RC2 (30 instancias)
    Propósito: validar generalización

5.1.2 Procedimiento Experimental
  - 10 ejecuciones independientes del Problema Maestro
  - Cada ejecución: GAA genera múltiples ASTs
  - Seleccionar 3 mejores ASTs por ejecución
  - Evaluar en Selection Set y Evaluation Set
  - Elegir 1 mejor AST globalmente

5.1.3 Métricas de Evaluación
  - Métrica primaria: # Vehículos
  - Métrica secundaria: Distancia (si V es igual)
  - Orden lexicográfico: (V, D)
  - Gap respecto a BKS (cuando V coincide)
  - Consistencia: desviación estándar
  - Generalizabilidad: gap(Design) vs gap(Evaluation)

5.1.4 Validación Estadística
  - Test t pareado
  - Intervalo de confianza 95%
  - Significancia: p-value < 0.05
```

### **5.2 Algoritmos de Referencia (Baselines)**

**Fuente:** Q6 (Tres Algoritmos)

```markdown
5.2.1 ALGO-1: Sequential Insertion (Solomon I1)
  - Baseline inferior
  - Construcción pura sin local search
  
5.2.2 ALGO-2: Regret Insertion + Or-Opt
  - Baseline medio
  - Énfasis en factibilidad temporal
  
5.2.3 ALGO-3: Hybrid Adaptativo
  - Baseline superior
  - Adaptación dinámica temporal/espacial
```

### **5.3 Cálculo de Presupuesto Computacional**

```markdown
Presupuesto por ejecución del Problema Maestro:
  - 10 iteraciones GRASP
  - Cada iteración: 1 construcción + local search
  - Evaluación en Design Set (18 instancias × ~30s cada una)
  - Total por ejecución: ~2-3 horas
  
Presupuesto total:
  - 10 ejecuciones × 3 horas = 30 horas máquina
  - En cluster paralelo: ~3-4 horas wall-clock
```

---

## **CAPÍTULO 6: RESULTADOS Y ANÁLISIS**

### **6.1 Resultados Cuantitativos**

#### **6.1.1 Tabla Principal de Resultados**

```
| Algoritmo | Design Gap | Selection Gap | Evaluation Gap | Consistencia |
|-----------|------------|---------------|----------------|--------------|
| ALGO-1    | 8.5% ±2.1% | 7.2% ±1.8%    | 8.9% ±2.3%     | 24% |
| ALGO-2    | 5.2% ±1.5% | 4.8% ±1.2%    | 5.6% ±1.8%     | 32% |
| ALGO-3    | 3.1% ±1.0% | 3.2% ±0.9%    | 3.5% ±1.1%     | 35% |
| GAA-Best  | 2.1% ±0.8% | 2.3% ±0.7%    | 2.6% ±0.9%     | 38% |
```

#### **6.1.2 Desglose por Familia**

```
| Familia | ALGO-1 | ALGO-2 | ALGO-3 | GAA-Best |
|---------|--------|--------|--------|----------|
| C1      | 9.2%   | 5.1%   | 2.8%   | 1.9%     |
| C2      | 3.5%   | 4.0%   | 2.1%   | 1.2%     |
| R1      | 18.2%  | 6.5%   | 5.3%   | 3.1%     |
| R2      | 2.1%   | 3.2%   | 2.0%   | 1.5%     |
| RC1     | 10.5%  | 5.8%   | 3.5%   | 2.4%     |
| RC2     | 4.2%   | 5.1%   | 3.2%   | 2.2%     |
| PROMEDIO| 8.0%   | 4.9%   | 3.1%   | 2.0%     |
```

### **6.2 Análisis Estadístico**

```markdown
6.2.1 Test de Significancia
  - t-test pareado: GAA-Best vs ALGO-3
  - t-statistic: 3.45
  - p-value: 0.0012 (significancia α = 0.05)
  - Conclusión: Mejora estadísticamente significativa
  
6.2.2 Intervalo de Confianza 95%
  - Gap(ALGO-3) = 3.1% ± 1.0% [2.1%, 4.1%]
  - Gap(GAA-Best) = 2.0% ± 0.8% [1.2%, 2.8%]
  - Conclusión: Intervalos no se solapan (diferencia clara)
  
6.2.3 Análisis de Generalización
  - Diferencia Design → Evaluation:
    ALGO-1: +0.4% (bajo overfitting)
    ALGO-3: +0.4% (bajo overfitting)
    GAA-Best: +0.5% (muy bajo overfitting)
```

### **6.3 Mejora Relativa Respecto a Baselines**

```markdown
Mejora de GAA-Best sobre ALGO-1 (baseline inferior):
  75% de reducción de gap

Mejora de GAA-Best sobre ALGO-3 (baseline superior):
  35% de reducción de gap

Conclusión: GAA es superior a todos los baselines,
incluyendo al algoritmo manual más avanzado (ALGO-3)
```

### **6.4 Análisis Cualitativo del Mejor Algoritmo GAA**

#### **6.4.1 Estructura del AST Descubierto**

```
Nombre: GAA-RUN-5-BEST
Fitness: 2.0%
Estructura:
  Seq(
    GreedyConstruct(
      Criterion = Urgency + 0.4*Regret - 0.2*Distance,
      Tiebreaker = ForwardSlack
    ),
    LocalSearch(
      SelectBest(OrOpt, TwoOpt),
      MaxIter = 80
    )
  )

Profundidad: 2
Nodos funcionales: 3
```

#### **6.4.2 Terminales Más Utilizados**

```
Ranking (por frecuencia de aparición):
1. Urgency: 95% de ejecuciones
2. Regret: 87%
3. ForwardSlack: 76%
4. Distance: 72%
5. Demand: 58%
6. Slack: 42%
```

#### **6.4.3 Funciones Más Utilizadas**

```
1. Seq: 100%
2. GreedyConstruct: 89%
3. SelectBest: 78%
4. OrOpt: 71%
5. TwoOpt: 69%
```

#### **6.4.4 Interpretación**

```markdown
El algoritmo descubierto combina:
- Construcción con énfasis temporal (Urgency + Regret)
- Local search adaptativa (elige mejor operador entre OrOpt y TwoOpt)
- Control robusto de holgura temporal (ForwardSlack)

Insight: GAA "redescubre" la sabiduría de ALNS (importancia de 
Regret, adaptación de operadores) pero de forma automática y 
optimizada para Solomon.

Especialidades:
- Excelente en R1, RC1 (ventanas ajustadas): 3.1%, 2.4%
- Muy bueno en todas las otras familias: 1.2-2.2%
- Balanceado pero con sesgo temporal
```

### **6.5 Convergencia del GRASP**

```markdown
Gráfico sugerido: Fitness (eje Y) vs Iteración GRASP (eje X)

Observación típica:
- Iteraciones 1-3: mejora rápida (steep descent)
- Iteraciones 4-7: mejora lenta (plateau)
- Iteraciones 8-10: estancamiento (no hay mejora)

Conclusión: 10 iteraciones GRASP es suficiente
(agregar más iteraciones ofrece ganancia marginal)
```

---

## **CAPÍTULO 7: CONCLUSIONES Y TRABAJO FUTURO**

### **7.1 Resumen de Hallazgos**

```markdown
1. GAA es viable: Capa demostrar que GP puede generar algoritmos
   para VRPTW que superan baselines manuales

2. Ganancia cuantitativa: 35% reducción de gap respecto a algoritmo
   manual más avanzado (ALGO-3)

3. Generalización: Bajo overfitting (~0.5% diferencia Design → Eval)
   Algoritmo genera bien en instancias no vistas

4. Interpretabilidad: Algoritmo descubierto es comprensible y
   alineable con conocimiento experto (ALNS literature)

5. Escalabilidad: Presupuesto computacional manejable (30 horas máquina
   para descubrir algoritmo, pero reutilizable infinitamente)
```

### **7.2 Contribuciones a la Literatura**

```markdown
- Framework formal de GAA para VRPTW (novedad)
- Demostración empírica de efectividad de GP en AAD para VRP
- Caracterización de terminales y funciones óptimas
- Análisis de patrones en heurísticas automáticamente generadas
```

### **7.3 Limitaciones**

```markdown
1. Limitación de alcance: Solo Solomon (N=100)
   - No probado en Homberger (N>100)
   - Generalización a escala desconocida

2. Limitación de primitivos: Terminal set y function set
   - Definición manual (por dominio experto)
   - No se exploró otros conjuntos alternativos

3. Limitación de presupuesto: 10 iteraciones GRASP
   - Posible mejora con más iteraciones
   - Trade-off: costo computacional vs ganancia marginal

4. Falta de análisis de robustez: Variabilidad en 10 runs
   - Mejor run vs peor run (rango de gap)
   - Desviación estándar entre runs
```

### **7.4 Trabajo Futuro**

#### **Corto Plazo (Extensiones Directas)**

```markdown
1. Escalabilidad a Homberger
   - Probar algoritmo descubierto en N=200, 400, 600, 1000
   - Reentrenamiento GAA en instancias más grandes

2. Variantes del VRPTW
   - Multiple depósitos (MDVRPTW)
   - Ventanas de tiempo suaves (soft time windows)
   - Capacidades heterogéneas
   
3. Optimización de presupuesto
   - Reducir de 30 horas a 10 horas (paralelización)
   - Acelerar evaluaciones (sample smaller benchmark durante GAA)
```

#### **Mediano Plazo (Mejora del Framework)**

```markdown
4. Exploración de primitivos alternativos
   - Terminal set ampliado (nuevas características)
   - Function set alternativo (más operadores)
   - Búsqueda automática de mejor representación
   
5. Aprendizaje multi-tarea
   - Entrenar GAA para múltiples problemas (CVRP, PDPTW, etc.)
   - Transferencia de aprendizaje

6. Interpretabilidad mejorada
   - Extracción de reglas (AST → pseudocódigo → English)
   - Visualización interactiva de ASTs
```

#### **Largo Plazo (Cambio de Paradigma)**

```markdown
7. Co-evolucionariedad
   - Evolucionar terminal set junto con function set
   - Meta-learning: GAA que genera su propio GAA

8. Aprendizaje online
   - Algoritmo que se adapta durante ejecución
   - Per-instance parameter tuning

9. Integración con heurísticas actuales
   - Reemplazar componentes de ALNS con módulos descubiertos
   - Hybrid algoritmos: manual + automático
```

### **7.5 Conclusión Final**

```markdown
Este trabajo demuestra que la **Generación Automática de Algoritmos
mediante Programación Genética** es un enfoque **viable, efectivo e
interpretable** para descubrir heurísticas de alta calidad para el
VRPTW.

Contrariamente a creencias tradicionales (que requiere ingeniero
experto), el framework GAA propuesto puede generar algoritmos
competitivos de forma **automatizada, reproducible y escalable**.

Se anticipa que este enfoque abrirá nuevas oportunidades en la
comunidad de optimización combinatoria, donde la automatización
del diseño algorítmico será clave para resolver problemas más
complejos (urbano, dinámico, estocástico, con requerimientos
heterogéneos, etc.).
```

---

## **APÉNDICES**

### **APÉNDICE A: Especificación Completa de Primitivos**

**Fuente:** Q2 (Literatura)

```markdown
Terminal Set Completo (9 terminales)
Function Set Completo (11 funciones)
Restricciones de Composición
Ejemplos de ASTs válidos e inválidos
```

### **APÉNDICE B: Protocolo Experimental Detallado**

**Fuente:** Q5

```markdown
Conjuntos de instancias exactas
Parámetros del GRASP
Límites de tiempo
Configuración de random seeds
Criterios de parada
```

### **APÉNDICE C: Tablas Completas de Resultados**

```markdown
Resultados por instancia (56 × 3 algoritmos)
Estadísticas por familia
Gráficos de convergencia
Matriz de correlación gap vs características de instancia
```

### **APÉNDICE D: Pseudocódigos**

```markdown
GRASP (algoritmo completo)
Generador aleatorio de AST
Evaluador de fitness
Ejecución segura de AST
Operadores de local search
```

### **APÉNDICE E: Código Fuente**

```markdown
Enlace a repositorio GitHub
Estructura de carpetas
Cómo reproducir resultados
Dependencias y versiones de software
```

### **APÉNDICE F: Datos Brutos**

```markdown
Archivo CSV con resultados por instancia
JSON con ASTs descubiertos
Logs de ejecución del GRASP
Archivos de configuración
```

---

## **BIBLIOGRAFÍA RECOMENDADA**

```markdown
[1] Solomon, M. M. (1987). Algorithms for the vehicle routing and 
    scheduling problems with time window constraints. Operations 
    research, 35(2), 254-265.

[2] Toth, P., & Vigo, D. (Eds.). (2014). Vehicle routing: problems, 
    methods, and applications (2nd ed.). SIAM.

[3] Ropke, S., & Pisinger, D. (2006). Large neighborhood search. 
    Handbook of metaheuristics, 99-127.

[4] Koza, J. R. (1992). Genetic programming: on the programming of 
    computers by means of natural selection. MIT press.

[5] Resende, M. G., & Ribeiro, C. C. (2016). Optimization by GRASP: 
    Greedy randomized adaptive search procedures. Springer Publishing 
    Company.

... [agregar 20+ referencias adicionales]
```

---

## **INFORMACIÓN DE CONTACTO Y REPRODUCIBILIDAD**

```markdown
Autor: [Nombre]
Email: [Email]
Institución: [Institución]
Fecha de publicación: [Fecha]

Código fuente disponible en: [GitHub URL]
Datasets disponibles en: [Zenodo URL]
Resultados completos en: [Open Science Framework URL]

DOI: [Número DOI]
CitationFormat: [BibTeX]
```

---

## Notas para Completar el Documento

1. **Secciones 6.1-6.5 (Resultados):** Se deben llenar con datos reales después de ejecutar el experimento.

2. **Figuras:** Incluir al menos:
   - Gráfico de gap por familia (ALGO-1, ALGO-2, ALGO-3, GAA-Best)
   - Gráfico de convergencia del GRASP
   - Visualización del AST mejor descubierto
   - Mapa de terminales (heatmap de frecuencia)

3. **Tablas adicionales:** Según necesidad, durante redacción:
   - Tabla de parámetros del GRASP
   - Tabla de características de instancias vs gap
   - Matriz de comparación detallada

4. **Contribuciones:** Reemplazo de cualquier sección teórica con análisis del autor.

5. **Tono:** Mantener formal académico, adecuado para revista ESWA, JORS, o Computers & Operations Research.

---

**Plantilla completada:** 4 de Enero, 2026  
**Listo para: Redacción de tesis/paper final**
