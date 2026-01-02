---
title: "ÍNDICE MAESTRO - VRPTW-GRASP"
version: "1.0.0"
created: "2026-01-01"
status: "Activo"
---

# 📚 ÍNDICE MAESTRO: VRPTW con GRASP

**Proyecto**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Metaheurística**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Enfoque**: Generación Automática de Algoritmos (GAA)

---

## 🗂️ Estructura de Documentación

Este proyecto se documenta en **9 documentos temáticos** para mejor organización y comprensión:

### 1. **PROBLEMA Y DEFINICIÓN**
📄 [01-problema-vrptw.md](01-problema-vrptw.md)  
**Contenido**: Definición informal del VRPTW, aplicaciones, características por familia Solomon (C, R, RC)  
**Secciones**: 
- Descripción del problema
- Categorización del problema
- Aplicaciones prácticas
- Características por familia

---

### 2. **MODELO MATEMÁTICO CANÓNICO**
📄 [02-modelo-matematico.md](02-modelo-matematico.md)  
**Contenido**: Formulación matemática exacta, variables, restricciones, función objetivo  
**Secciones**:
- Grafo del problema
- Función objetivo (jerárquica)
- Variables de decisión
- Restricciones (capacidad, tiempo, cobertura)
- Parámetros del problema
- Dominio de variables

---

### 3. **OPERADORES DEL DOMINIO**
📄 [03-operadores-dominio.md](03-operadores-dominio.md)  
**Contenido**: 22 operadores VRPTW categorizados  
**Secciones**:
- Operadores Constructivos (6): Savings, NN, Inserción
- Operadores Intra-ruta (4): 2-opt, OrOpt, 3-opt, Relocate
- Operadores Inter-ruta (4): CrossExchange, 2-opt*, SwapCustomers, RelocateInter
- Operadores de Perturbación (4): EjectionChain, RuinRecreate, RandomRemoval, RouteElimination
- Operadores de Reparación (3): RepairCapacity, RepairTimeWindows, GreedyRepair
- Referencias bibliográficas por operador

---

### 4. **METAHEURÍSTICA GRASP**
📄 [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md)  
**Contenido**: GRASP, configuración, búsqueda local, VND  
**Secciones**:
- Descripción general de GRASP
- Fase constructiva (greedy randomized)
- RCL (Restricted Candidate List)
- Parámetros de configuración (α, iteraciones, parada)
- Variable Neighborhood Descent (VND)
- Pseudocódigos GRASP
- Presupuesto computacional

---

### 5. **DATASETS SOLOMON**
📄 [05-datasets-solomon.md](05-datasets-solomon.md)  
**Contenido**: Descripción de 56 instancias Solomon, formato, ubicación  
**Secciones**:
- Especificación del formato Solomon
- Descripción de 6 familias (C1, C2, R1, R2, RC1, RC2)
- Características espaciales y temporales
- Ubicación de archivos
- Validación de datasets
- Compatibilidad 100% con proyecto

---

### 6. **PLAN EXPERIMENTAL Y GAA**
📄 [06-experimentos-plan.md](06-experimentos-plan.md)  
**Contenido**: Plan experimental, dos modos (QUICK/FULL), generación única de algoritmos  
**Secciones**:
- Visión general del plan
- Modo QUICK (1 familia, 5-10 minutos)
- Modo FULL (6 familias, 40-60 minutos)
- Generación de 3 algoritmos con seed=42 (UNA SOLA VEZ)
- Criterio de uso de operadores (restricciones canónicas)
- Variables independientes y dependientes
- Presupuesto computacional

---

### 7. **FUNCIÓN FITNESS CANÓNICA**
📄 [07-fitness-canonico.md](07-fitness-canonico.md)  
**Contenido**: Función fitness jerárquica, gráficos canónicos, evaluación  
**Secciones**:
- Función fitness lexicográfica (K primario, D secundario)
- Comparación de soluciones
- Dominio de factibilidad
- Gráficos canónicos VRPTW (11 tipos)
- Relación GRASP-Fitness

---

### 8. **MÉTRICAS CANÓNICAS**
📄 [08-metricas-canonicas.md](08-metricas-canonicas.md)  
**Contenido**: Métricas jerárquicas por familia, análisis estadístico, cálculo de GAP  
**Secciones**:
- Métricas primarias (K_mean, K_best, %Instancias_K_BKS)
- Métricas secundarias (D_mean, %GAP, %GAP_std)
- Métricas de robustez
- Métricas de convergencia
- Métricas de eficiencia
- Validación de factibilidad
- Cálculo canónico del GAP
- Análisis por familia

---

### 9. **ESTRUCTURA DE OUTPUTS Y COMPATIBILIDAD**
📄 [09-outputs-estructura.md](09-outputs-estructura.md)  
**Contenido**: Esquema CSV exacto, OutputManager, estructura de directorios  
**Secciones**:
- OutputManager unificado (con timestamps)
- 8 archivos CSV canónicos con columnas exactas
- Estructura de directorios (results/, solutions/, plots/, gaa/, logs/)
- Clase OutputManager (pseudocódigo)
- Patrón de uso en código
- Validación de estructura
- Compatibilidad con GAA-GCP-ILS-4

---

### 10. **GENERACIÓN AUTOMÁTICA DE ALGORITMOS (GAA) CON AST**
📄 [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md)  
**Contenido**: Sistema GAA, Abstract Syntax Trees, generación y evolución de algoritmos  
**Secciones**:
- Introducción a GAA (qué es, motivación, flujo general)
- Representación AST (concepto, propiedades, ventajas)
- 7 tipos de nodos: Seq, While, For, If, GreedyConstruct, LocalSearch, Perturbation
- Gramática BNF para generación válida de algoritmos
- Generador aleatorio (4 patrones: simple, iterativo, multi-start, complejo)
- Operadores genéticos (mutación, crossover, selección)
- Intérprete de AST (ejecución en instancias VRPTW)
- Integración completa con VRPTW-GRASP
- Ejemplo funcional de 5 pasos (generación, visualización, ejecución, evaluación, persistencia)
- Módulos necesarios y flujo de ejecución

---

### 11. **BUENAS PRÁCTICAS: GENERACIÓN DE 3 ALGORITMOS** ⭐ IMPLEMENTACIÓN
📄 [11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md)  
**Contenido**: Guía práctica para generar 3 algoritmos automáticamente y ejecutar pruebas (inspirado en KBP-SA)  
**Secciones**:
- Arquitectura general con estructura de directorios
- Los 3 patrones de algoritmos VRPTW (Simple, Iterativo, Multi-start)
- Generación automática paso a paso (código completo)
- Selector inteligente de 3 algoritmos diversos
- Ejecución de batería QUICK (validación: 9 instancias)
- Ejecución de batería FULL (evaluación: 56 instancias)
- Estructura y formato de resultados (JSON + CSV)
- Análisis estadístico de resultados
- Script completo de pipeline (inicio a fin)
- Checklist de implementación
- Ejemplos de ejecución y salidas esperadas

---

## 🔗 Referencias Cruzadas Rápidas

| Concepto | Documento |
|----------|-----------|
| Definición del problema | [01-problema-vrptw.md](01-problema-vrptw.md) |
| Modelo matemático | [02-modelo-matematico.md](02-modelo-matematico.md) |
| Operadores VRPTW | [03-operadores-dominio.md](03-operadores-dominio.md) |
| GRASP configuración | [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) |
| Datasets Solomon | [05-datasets-solomon.md](05-datasets-solomon.md) |
| Plan experimental | [06-experimentos-plan.md](06-experimentos-plan.md) |
| Función fitness | [07-fitness-canonico.md](07-fitness-canonico.md) |
| Métricas | [08-metricas-canonicas.md](08-metricas-canonicas.md) |
| Outputs | [09-outputs-estructura.md](09-outputs-estructura.md) |
| GAA y AST | [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md) |
| **Implementación GAA (3 algoritmos)** | **[11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md)** |

---

## 🎯 Cómo Usar Esta Documentación

### Para Desarrolladores

1. **Entender el proyecto**: Leer [01-problema-vrptw.md](01-problema-vrptw.md) + [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md)
2. **Implementar estructura de datos**: Usar [02-modelo-matematico.md](02-modelo-matematico.md)
3. **Implementar operadores**: Seguir [03-operadores-dominio.md](03-operadores-dominio.md)
4. **Configurar GRASP**: Usar [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md)
5. **Validar datos**: Consultar [05-datasets-solomon.md](05-datasets-solomon.md)
6. **Ejecutar experimentos**: Seguir [06-experimentos-plan.md](06-experimentos-plan.md)
7. **Validar salidas**: Consultar [09-outputs-estructura.md](09-outputs-estructura.md)
8. **Implementar GAA**: Seguir [10-gaa-ast-implementation.md](10-gaa-ast-implementation.md)
9. **Generar 3 algoritmos**: Usar [11-buenas-practicas-gaa.md](11-buenas-practicas-gaa.md) ⭐

### Para Investigadores

1. **Entender fundamento teórico**: [02-modelo-matematico.md](02-modelo-matematico.md) + [07-fitness-canonico.md](07-fitness-canonico.md)
2. **Diseño de experimentos**: [06-experimentos-plan.md](06-experimentos-plan.md)
3. **Interpretación de resultados**: [08-metricas-canonicas.md](08-metricas-canonicas.md)
4. **Comparación con literatura**: [05-datasets-solomon.md](05-datasets-solomon.md)

### Para Revisores

1. **Canonicidad del modelo**: [02-modelo-matematico.md](02-modelo-matematico.md)
2. **Canonicidad del fitness**: [07-fitness-canonico.md](07-fitness-canonico.md)
3. **Canonicidad de métricas**: [08-metricas-canonicas.md](08-metricas-canonicas.md)
4. **Reproducibilidad**: [06-experimentos-plan.md](06-experimentos-plan.md) + [09-outputs-estructura.md](09-outputs-estructura.md)

---

## 📊 Estadísticas de Documentación

| Documento | Tópicos | Complejidad |
|-----------|---------|------------|
| 01-problema-vrptw.md | 5 | Media |
| 02-modelo-matematico.md | 8 | Alta |
| 03-operadores-dominio.md | 5 | Media |
| 04-metaheuristica-grasp.md | 7 | Media-Alta |
| 05-datasets-solomon.md | 6 | Media |
| 06-experimentos-plan.md | 7 | Alta |
| 07-fitness-canonico.md | 6 | Alta |
| 08-metricas-canonicas.md | 8 | Alta |
| 09-outputs-estructura.md | 7 | Media |
| 10-gaa-ast-implementation.md | 9 | Alta |
| **11-buenas-practicas-gaa.md** | **8** | **Media-Alta** |

**Total**: 11 documentos, ~75 tópicos, información completa sin duplicación

---

## 🔄 Flujo de Lectura Recomendado

### Lectura Rápida (30 minutos)
1. Este INDEX (5 min)
2. [01-problema-vrptw.md](01-problema-vrptw.md) (10 min)
3. [04-metaheuristica-grasp.md](04-metaheuristica-grasp.md) (10 min)
4. [06-experimentos-plan.md](06-experimentos-plan.md) (5 min)

### Lectura Comprensiva (2-3 horas)
Leer en orden: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10

### Lectura Técnica Profunda (6-8 horas)
- Énfasis en: 02, 03, 04, 07, 08, 09, 10, 11
- Incluir pseudocódigos, fórmulas, ejemplos de código y buenas prácticas

---

## ✅ Checklist Relacionado

Para gestionar el desarrollo del proyecto, consultar:  
📋 [development_checklist.md](development_checklist.md)

---

## 📝 Notas Importantes

### Canonicidad
- Toda la documentación sigue **estándares canónicos** de Solomon VRPTW
- Función fitness es **jerárquica** (K primario, D secundario)
- GAP se calcula **solo cuando K = K_BKS**
- No se usan pesos o combinaciones lineales

### Reproducibilidad
- Generación de algoritmos con **seed=42** (determinístico)
- Datasets **públicos y estándar** (Solomon)
- Métricas **claramente definidas** y sin ambigüedad

### Modularidad
- Cada documento puede leerse **independientemente**
- Referencias cruzadas explícitas
- Consistencia terminológica mantenida

---

## 🚀 Próximos Pasos

1. ✅ Leer este INDEX (ahora)
2. ⏳ Leer documentos según necesidad temática
3. 📋 Usar [development_checklist.md](development_checklist.md) para implementación
4. 🔄 Mantener sincronización entre documentación y código

---

**Última actualización**: 2026-01-01  
**Versión**: 1.0.0  
**Mantenedor**: Proyecto VRPTW-GRASP
