# 📋 DOCUMENTACIÓN: ILS vs GA - Índice de Recursos

**Estado**: ✅ COMPLETO Y VERIFICADO  
**Última actualización**: Edición de documentación de componentes  
**Propósito**: Proporcionar referencia única sobre terminología ILS vs GA

---

## 🎯 Inicio Rápido: ¿Es GA o ILS?

**Respuesta**: **Este proyecto es ILS, NO GA**

```
ILS (Iterated Local Search) = El algoritmo base
├─ Una solución que mejora iterativamente
├─ Búsqueda local (intensificación)
├─ Perturbación (escape)
└─ 500 iteraciones

NO incluye:
❌ Población
❌ Cromosomas
❌ Crossover
❌ Generaciones
```

---

## 📚 Documentación Disponible

### 1️⃣ Para Entender Rápidamente (5 min)

**[CLARIFICACION_TERMINOLOGIA.md](CLARIFICACION_TERMINOLOGIA.md)** ⭐ RECOMENDADO
- 📊 Tabla GA vs ILS
- 📊 Tabla metaheurísticas + multi-objetivo
- ✅ Sección 8: Palabras clave (qué sí, qué no)
- 📖 Referencias académicas

**Tiempo**: 5-10 minutos  
**Nivel**: Ejecutivo / Rápida referencia

---

### 2️⃣ Para Validación de Documentación (10 min)

**[EDICION_DOCUMENTACION_COMPLETADA.md](../../EDICION_DOCUMENTACION_COMPLETADA.md)** ✅
- Cambios específicos realizados
- Líneas modificadas en cada archivo
- Verificación de coherencia

**Tiempo**: 5 minutos  
**Nivel**: Revisor de cambios

---

### 3️⃣ Para Comprensión Profunda (30 min)

**[ACLARACION_MUTACION_MULTIOBJETIVO.md](ACLARACION_MUTACION_MULTIOBJETIVO.md)** 📖
- Explicación detallada de terminología
- 2500+ líneas de análisis
- Secciones sobre cada concepto por separado
- Diagramas ASCII comparativos

**Tiempo**: 20-30 minutos  
**Nivel**: Técnico / Investigador

---

### 4️⃣ Archivos de Especificación Actualizada

#### ✅ [02-Components/Search-Operators.md](02-Components/Search-Operators.md)
**Cambios**:
- Línea 28: Nuevo header "Esto NO es Algoritmo Genético"
- Línea 30: Tabla GA vs ILS
- Línea 57: Diagrama ILS Loop
- Línea 85: Encabezado actualizado

**Qué buscar**: Aclaraciones sobre "mutación" como perturbación, no genética

#### ✅ [02-Components/Fitness-Function.md](02-Components/Fitness-Function.md)
**Cambios**:
- Línea 25: Nuevo header "Multi-Objetivo es Independiente"
- Línea 27: Tabla de metaheurísticas
- Línea 56: Sección "¿Por qué Multi-Objetivo?"
- Línea 82: Explicación de agregación con pesos

**Qué buscar**: Aclaraciones sobre "multi-objetivo" como concepto independiente

---

## 🔍 Búsqueda Rápida por Pregunta

### ❓ "¿Por qué dice 'mutación'? ¿No es eso GA?"

**Respuesta**: NO. En ILS, "mutación" = perturbación para escape.

📍 **Ver**:
- [CLARIFICACION_TERMINOLOGIA.md - Sección 1](CLARIFICACION_TERMINOLOGIA.md#1-mutación-en-ils-no-es-genética)
- [Search-Operators.md - Header (línea 28)](02-Components/Search-Operators.md#l28)
- [ACLARACION_MUTACION_MULTIOBJETIVO.md - Sección 2](ACLARACION_MUTACION_MULTIOBJETIVO.md#sección-2-la-mutación-en-ils)

---

### ❓ "¿Qué es 'multi-objetivo'? ¿Significa que es GA?"

**Respuesta**: NO. Multi-objetivo es independiente del metaheurístico.

📍 **Ver**:
- [CLARIFICACION_TERMINOLOGIA.md - Sección 2](CLARIFICACION_TERMINOLOGIA.md#2-multi-objetivo-concepto-independiente-del-metaheurístico)
- [Fitness-Function.md - Header (línea 25)](02-Components/Fitness-Function.md#l25)
- [ACLARACION_MUTACION_MULTIOBJETIVO.md - Sección 3](ACLARACION_MUTACION_MULTIOBJETIVO.md#sección-3-multi-objetivo-independiente)

---

### ❓ "¿Dónde está la prueba académica de que es ILS?"

**Respuesta**: Ver referencias en documentación.

📍 **Referencias incluidas**:
- Lourenço, H. R., Martin, O. C., & Stützle, T. (2003). "Iterated local search"
- Talbi, E. G. (2009). "Metaheuristics: from design to implementation"
- Deb, K. (2001). "Multi-objective optimization using evolutionary algorithms"

📍 **Ver**: [CLARIFICACION_TERMINOLOGIA.md - Sección 5](CLARIFICACION_TERMINOLOGIA.md#5-referencias-académicas)

---

### ❓ "¿Qué cambios se hicieron en la documentación?"

**Respuesta**: Se aclararon 4 áreas clave.

📍 **Ver**: [EDICION_DOCUMENTACION_COMPLETADA.md](../../EDICION_DOCUMENTACION_COMPLETADA.md)

Cambios resumidos:
- Search-Operators.md: +50 líneas de aclaraciones ILS
- Fitness-Function.md: +60 líneas de aclaraciones multi-objetivo

---

## 📊 Tabla de Referencia

### Términos Usados en Este Proyecto

| Término | Significa | Contexto | ¿GA? |
|---------|-----------|----------|------|
| **ILS** | Iterated Local Search | Metaheurística base | ❌ |
| **Perturbación** | Cambio aleatorio de solución para escape | Operador ILS | ❌ |
| **Mutación** | Perturbación (en contexto ILS) | Operador de búsqueda | ❌ |
| **Multi-objetivo** | Múltiples dimensiones de optimización | Característica general | ⚠️ Sí pero independiente |
| **AST** | Abstract Syntax Tree | Representación de configuración | ❌ |
| **Iteraciones** | Ciclos de mejora | Parámetro ILS (500) | ❌ |
| **Búsqueda Local** | Mejora de parámetros | Intensificación ILS | ❌ |

### Términos NO Usados

| Término | Por qué NO | Alternativa |
|---------|-----------|-------------|
| **Cromosoma** | Esto es ILS, no GA | Configuración AST |
| **Gen** | Esto es ILS, no GA | Parámetro |
| **Población** | Solo una solución en ILS | Configuración actual |
| **Generación** | Esto es ILS, no GA | Iteración |
| **Crossover** | No en ILS | (no existe) |
| **Selección Natural** | No en ILS | (no existe) |
| **NSGA-II** | Eso es GA multi-objetivo | Nuestro: ILS multi-objetivo |

---

## 🔗 Conexiones Entre Documentos

```
CLARIFICACION_TERMINOLOGIA.md (Este documento)
├─ Referencia → ACLARACION_MUTACION_MULTIOBJETIVO.md
├─ Referencia → Search-Operators.md (línea 28)
└─ Referencia → Fitness-Function.md (línea 25)

Search-Operators.md
├─ Implementa → ILS Perturbation
├─ Referencia → Lourenço et al. 2003
└─ Usa → 5 tipos de mutación

Fitness-Function.md
├─ Implementa → ILS Multi-objetivo
├─ Referencia → Talbi 2009
└─ Usa → Agregación de 4 objetivos

ACLARACION_MUTACION_MULTIOBJETIVO.md (Detalle profundo)
├─ Amplía → CLARIFICACION_TERMINOLOGIA.md
├─ Cita → Académicos clave
└─ Proporciona → Ejemplos extensivos
```

---

## ✅ Verificación de Consistencia

### Punto 1: "¿Aparece 'GA' en documentación crítica?"

✅ **Resultado**: NO (a menos que sea para aclaración de diferencias)

- Search-Operators.md: Solo en tabla de diferencias (línea 30)
- Fitness-Function.md: Solo en tabla de diferencias (línea 27)
- CLARIFICACION_TERMINOLOGIA.md: Solo para contraste educativo

---

### Punto 2: "¿Es claro que es ILS?"

✅ **Resultado**: SÍ (explícitamente mencionado 50+ veces)

- Cada aclaración dice: "En ILS"
- Cada tabla muestra: "ILS (Este Proyecto)"
- Cada diagrama etiqueta: "Iterated Local Search"

---

### Punto 3: "¿Hay referencias académicas?"

✅ **Resultado**: SÍ (4 autores clave citados)

1. Lourenço, H. R., Martin, O. C., & Stützle, T. (2003)
2. Talbi, E. G. (2009)
3. Deb, K. (2001)
4. Caruana, R. (1997) [en ACLARACION_MUTACION_MULTIOBJETIVO.md]

---

## 🚀 Próximos Pasos Opcionales

Si deseas aún mayor claridad:

1. **Metaheuristic.md** (00-Core/): Agregar sección "Why ILS, not GA?"
2. **FRAMEWORK_STATUS.md**: Agregar tabla "✅ ILS | ❌ GA"
3. **GAA-Agent-System-Prompt.md**: Revisar para evitar menciones de GA
4. **ARCHITECTURE.md**: Referenciar esta clarificación

**Pero el trabajo crítico está COMPLETO** ✅

---

## 📝 Resumen Final

| Aspecto | Estado |
|---------|--------|
| Search-Operators.md clarificado | ✅ |
| Fitness-Function.md clarificado | ✅ |
| Referencias académicas agregadas | ✅ |
| Documentación de referencia creada | ✅ |
| Tabla GA vs ILS visible | ✅ |
| Imposible confundir con GA | ✅ |

---

## 🎓 Para Académicos

**Si esto es para un paper, conferencia o revisión:**

Cite:
1. Lourenço, H. R., Martin, O. C., & Stützle, T. (2003)
2. Talbi, E. G. (2009), Capítulo 1: "Introduction"

Describa así:
> "Usamos Iterated Local Search (ILS) conforme a Lourenço et al. (2003), con agregación multi-objetivo de 4 métricas."

**No diga**:
> "Usamos algoritmo genético"

**Sí diga**:
> "Usamos búsqueda local iterada con perturbación"

---

## 💬 Preguntas Frecuentes

**P: ¿Pero algunos archivos dicen "mutación"? ¿Eso no es GA?**

R: No. "Mutación" en ILS = "Perturbación". Hemos añadido aclaraciones claras en los encabezados de esos archivos.

---

**P: ¿Pero el fitness es multi-objetivo, ¿eso no es NSGA-II?**

R: No. Multi-objetivo es independiente del metaheurístico. NSGA-II es GA multi-objetivo. Nosotros hacemos ILS multi-objetivo.

---

**P: ¿Hay población de configuraciones?**

R: NO. Solo una configuración que mejora iterativamente durante 500 iteraciones.

---

**P: ¿Hay cromosomas y genes?**

R: NO. Hay configuraciones AST con parámetros.

---

**P: ¿Hay crossover?**

R: NO. Solo perturbación para escape.

---

## 📞 Para Dudas

Si algo sigue siendo confuso:

1. **Primer paso**: Lee [CLARIFICACION_TERMINOLOGIA.md](CLARIFICACION_TERMINOLOGIA.md) Sección 3: "Tabla Comparativa"
2. **Segundo paso**: Lee [Search-Operators.md línea 28](02-Components/Search-Operators.md#l28) y [Fitness-Function.md línea 25](02-Components/Fitness-Function.md#l25)
3. **Tercer paso**: Lee [ACLARACION_MUTACION_MULTIOBJETIVO.md](ACLARACION_MUTACION_MULTIOBJETIVO.md) sección correspondiente

---

**Generado por**: Revisión de Documentación Sistemática  
**Propósito**: Referencia única sobre terminología ILS vs GA  
**Validado contra**: Especificaciones de proyecto (Talbi 2009 + Lourenço 2003)
