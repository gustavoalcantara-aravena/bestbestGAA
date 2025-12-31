# Clarificación de Terminología: ILS vs GA

**Última actualización**: Documentación editada para máxima claridad  
**Archivos afectados**:
- `02-Components/Search-Operators.md` - Aclaración sobre mutación
- `02-Components/Fitness-Function.md` - Aclaración sobre multi-objetivo

---

## Resumen Ejecutivo

Este proyecto implementa **Iterated Local Search (ILS)**, NO un Algoritmo Genético (GA).

Algunos términos como "mutación" y "multi-objetivo" aparecen en la documentación, pero tienen significados específicos en contexto ILS:

| Término | En GA | En ILS (Este Proyecto) |
|---------|-------|--------------------------|
| **Mutación** | Reproducción: cambio aleatorio en cromosoma de población | Perturbación: cambio aleatorio en solución actual para escape |
| **Multi-objetivo** | Parte integral de GA multi-objetivo (NSGA-II, etc.) | Agregación de múltiples dimensiones de optimización (independent del metaheurístico) |

---

## 1. Mutación en ILS (No es Genética)

### Conceptos Clave

```
ALGORITMO GENÉTICO           ITERATED LOCAL SEARCH (Este Proyecto)
├─ Población (N individuos)   ├─ Una solución
├─ Cromosomas                 ├─ Configuración AST
├─ Mutación                   ├─ Perturbación
│  └─ Reproducción genética   │  └─ Cambio aleatorio simple
├─ Crossover                  ├─ (NO EXISTE)
├─ Selección Natural          ├─ (NO EXISTE)
├─ Generaciones               └─ Iteraciones (500)
└─ Fitness → Reproducción

DIFERENCIA CRÍTICA:
GA: Múltiples soluciones → Reproducción selectiva → Nueva población
ILS: Una solución → Perturbación aleatoria → Aceptación simple
```

### Los 5 Tipos de Mutación en ILS

En nuestro proyecto, hay 5 formas diferentes de perturbar (cambiar aleatoriamente) la solución actual:

1. **Mutación Constructiva**: Cambia qué operador inicial se usa
2. **Mutación de LS Operator**: Cambia el operador de búsqueda local
3. **Mutación de Perturbación**: Cambia el operador de perturbación
4. **Mutación de Parámetros**: Ajusta valores numéricos
5. **Mutación de Estructura**: Agrega o elimina fases

**En ILS**: Estas mutaciones son simplemente **opciones de cómo perturbar** la solución para escapar del óptimo local en el que estamos atrapados.

**NO implican**:
- ❌ Población
- ❌ Reproducción
- ❌ Crossover
- ❌ Selección natural
- ❌ Generaciones

### Referencia Académica

- **Lourenço, H. R., Martin, O. C., & Stützle, T. (2003)**. "Iterated local search". Handbook of metaheuristics.
  - Sección 3.1: "Perturbation mechanism" 
  - Claramente define mutación como perturbación de escape, no reproducción

---

## 2. Multi-Objetivo: Concepto Independiente del Metaheurístico

### Visualización

```
DIMENSIÓN 1: ¿Qué metaheurística usamos?
├─ GA (Algoritmo Genético)
├─ ILS (Iterated Local Search)  ← ESTE PROYECTO
├─ PSO (Particle Swarm)
├─ Tabú
└─ Simulated Annealing

DIMENSIÓN 2: ¿Optimizamos un objetivo o varios?
├─ Mono-objetivo (una función)
└─ Multi-objetivo (múltiples funciones)  ← ESTE PROYECTO

COMBINACIONES POSIBLES:
┌─────────────────┬──────────┬──────────────┐
│ Metaheurística  │ Mono-obj │ Multi-objeto │
├─────────────────┼──────────┼──────────────┤
│ GA              │ GA básico│ NSGA-II      │
│ ILS             │ ILS simple│ ILS+4 métricas│
│ PSO             │ PSO clásico│ MOPSO       │
│ Tabú            │ TS clásico│ TS multi-obj │
│ SA              │ SA clásico│ SA multi-obj │
└─────────────────┴──────────┴──────────────┘
```

### Nuestro Caso: ILS Multi-Objetivo

```
Problema: Encontrar configuración ILS óptima para GCP

Múltiples objetivos a balancear:
├─ f1: Minimizar colores usados (calidad)
├─ f2: Maximizar tasa de éxito (robustez)
├─ f3: Minimizar tiempo ejecución (eficiencia)
└─ f4: Minimizar variabilidad (consistencia)

Solución: Agregación con pesos
    Fitness = w₁·f1 + w₂·f2 + w₃·f3 + w₄·f4
    
    ← ESTO NO ES GA
    ← Es agregación en ILS de múltiples dimensiones
```

### Por qué No es GA

- **GA Multi-Objetivo** (NSGA-II): Usa población → Selección Pareto → Nuevas generaciones
- **ILS Multi-Objetivo** (Este Proyecto): Usa UNA solución → Agregación con pesos → Iteraciones

**Los 4 objetivos son completamente ortogonales a la decisión de usar ILS en vez de GA.**

---

## 3. Tabla Comparativa Completa

| Aspecto | GA | ILS (Nuestro Proyecto) |
|--------|----|----|
| **Entidad Principal** | Población de cromosomas | Una configuración AST |
| **Variación** | Mutación (reproducción) + Crossover | Perturbación (escape) |
| **Reproducción** | Sí (selección natural) | NO |
| **Ciclo Iterativo** | Generaciones | Iteraciones (500) |
| **Búsqueda Local** | NO (implícita en fitness) | Sí (operadores explícitos) |
| **Escape de Óptimo Local** | Diversidad de población | Perturbación controlada |
| **Multi-Objetivo** | Posible (NSGA-II) | Sí (agregación con pesos) |
| **Estado Final** | Mejor cromosoma | Mejor configuración encontrada |

---

## 4. Archivos Documentación Actualizada

### Search-Operators.md
✅ **Actualizado**: Ahora incluye sección al inicio explicando que:
- "Mutación" en ILS = perturbación para escape
- NO es reproducción genética
- Tabla clara comparando GA vs ILS
- Visualización del ciclo ILS

**Cambios**:
- Línea 1-50: Nuevo header con aclaración
- Línea 52-110: Nueva sección "¿Por qué Multi-Objetivo?" (corregido de Fitness-Function.md)
- Sección "Tipos de Mutación": Ahora claramente etiquetada como perturbación

### Fitness-Function.md  
✅ **Actualizado**: Ahora incluye sección al inicio explicando que:
- "Multi-objetivo" no implica GA
- Tabla mostrando múltiples metaheurísticas pueden ser multi-objetivo
- Especificación de nuestra agregación de pesos

**Cambios**:
- Línea 1-50: Nuevo header con aclaración
- Línea 52-100: Nueva tabla "¿Por qué Multi-Objetivo?" explicando agregación con pesos

---

## 5. Referencias Académicas

Para confirmar estas afirmaciones:

### ILS y Perturbación
- **Lourenço, H. R., Martin, O. C., & Stützle, T. (2003)**
  - "Iterated local search". *Handbook of metaheuristics*, pp. 320-353
  - Define claramente perturbación como mecanismo de escape, no mutación genética

### Multi-Objetivo Independiente
- **Deb, K. (2001)**
  - "*Multi-objective optimization using evolutionary algorithms*". John Wiley & Sons
  - Muestra NSGA-II como GA multi-objetivo, pero multi-objetivo es independiente del metaheurístico

- **Talbi, E. G. (2009)**
  - "*Metaheuristics: from design to implementation*". Wiley
  - Capítulo 7: Combinaciones de metaheurísticas con objetivos múltiples

---

## 6. Palabras Clave Actualizadas

Para búsquedas futuras, este proyecto usa:

- ✅ **ILS** (Iterated Local Search) - Metaheurística base
- ✅ **Perturbación** - Operador de escape (a veces llamado "mutación" en ILS)
- ✅ **Multi-objetivo** - 4 dimensiones de optimización agregadas
- ✅ **GAA** - Framework de ajuste automático de algoritmos
- ✅ **AST** - Representación de configuraciones como árboles sintácticos

- ❌ **GA** - NO usado en este proyecto
- ❌ **Crossover** - NO usado en este proyecto
- ❌ **Generaciones** - NO usado (usamos iteraciones)
- ❌ **Cromosomas** - NO usado
- ❌ **Selección Natural** - NO usado

---

## 7. Verificación de Documentos

Para asegurar consistencia, todos estos archivos ahora contienen aclaraciones:

| Archivo | Aclaración |
|---------|-----------|
| [Search-Operators.md](02-Components/Search-Operators.md) | "Mutación = Perturbación en ILS, no genética" |
| [Fitness-Function.md](02-Components/Fitness-Function.md) | "Multi-objetivo ≠ GA, es independiente" |
| [00-Core/Metaheuristic.md](../../00-Core/Metaheuristic.md) | Debe confirmar ILS como base |
| [FRAMEWORK_STATUS.md](../../FRAMEWORK_STATUS.md) | Debe confirmar ILS no GA |
| [GAA-Agent-System-Prompt.md](../../GAA-Agent-System-Prompt.md) | Debe evitar mencionar GA |

---

## 8. Conclusión

**Este proyecto es 100% Iterated Local Search (ILS), no GA.**

Los términos "mutación" y "multi-objetivo" pueden ser confusos fuera de contexto, pero:

- **Mutación en ILS** = Perturbación aleatoria para escape de óptimo local
- **Multi-objetivo en ILS** = Agregación de múltiples dimensiones de optimización

Ni uno ni otro implican características de GA como población, crossover o selección natural.

La documentación ha sido actualizada para máxima claridad.

---

**Documento de referencia rápida**: Vea [ACLARACION_MUTACION_MULTIOBJETIVO.md](../../../projects/GCP-ILS-GAA/ACLARACION_MUTACION_MULTIOBJETIVO.md) para explicación más detallada.
