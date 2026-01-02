# Completación de Parte 4: Plan Experimental

**Fecha**: 1 de Enero de 2026  
**Documento**: `problema_metaheuristica.md`  
**Líneas agregadas**: ~450 líneas de contenido nuevo  
**Basado en**: Estudio de `KBP-SA/ESTRUCTURA_EJECUCION_BOTH.md` y `KBP-SA/METODOLOGIA_EXPERIMENTAL.md`

---

## 📋 Resumen de Cambios

### Antes
La Parte 4 contenía solo esquemas vacíos:
- Lista incompleta de variables independientes/dependientes
- Sin estructura de experimentos
- Sin especificación de datasets
- Sin criterios operacionales
- Faltaban referencias bibliográficas

### Después
Documento completo con 989 líneas (antes: ~540 líneas) que incluye:

---

## ✅ Secciones Completadas

### 1. **Visión General del Experimento**
```markdown
- Patrón adoptado de KBP-SA: generación de 3 algoritmos automáticos
- Dos modos operacionales: Test Rápido (5-10 min) vs Full (20-30 min)
- Reutilización de algoritmos generados en TODOS los experimentos
- Single-seed baseline: seed=42 para reproducibilidad
```

### 2. **Dimensiones del Experimento**
```markdown
- Familias Solomon: R (aleatorio), C (clusters), RC (mixto)
- Total instancias: 30 (10 por familia)
- 3 algoritmos GAA × 30 instancias × 1 repetición = 90 experimentos (FULL)
- 3 algoritmos GAA × 10 instancias × 1 repetición = 30 experimentos (RÁPIDO)

Matriz clara:
┌─────────────────────────────────────────┐
│ R:  10 × 3 = 30 experimentos            │
│ C:  10 × 3 = 30 experimentos            │
│ RC: 10 × 3 = 30 experimentos            │
├─────────────────────────────────────────┤
│ TOTAL: 90 experimentos (MODO FULL)      │
└─────────────────────────────────────────┘
```

### 3. **Criterio de Uso de Operadores** (SECCIÓN CRÍTICA)
Especificación detallada de restricciones obligatorias para algoritmos generados:

#### ✅ Obligatorio (Cada algoritmo DEBE tener):
1. **Constructor Randomizado** (1 exacto):
   - `RandomizedInsertion(alpha)` ← Preferido para GRASP
   - `TimeOrientedNN`
   - `RegretInsertion`
   - `NearestNeighbor`

2. **Operadores de Mejora Local** (2+ mínimo):
   - **Intra-ruta**: TwoOpt, OrOpt, ThreeOpt, Relocate
   - **Inter-ruta**: CrossExchange, TwoOptStar, SwapCustomers, RelocateInter
   - **Recomendado**: 1 intra-ruta + 1 inter-ruta (VND balance)

3. **Criterio de Iteración** (1 exacto):
   - `ApplyUntilNoImprove(max_stagnation=k)` ← Estándar
   - `ChooseBestOf(n_iterations)` ← Variante GRASP
   - `For(fixed_iterations)`

4. **Reparación** (Opcional pero recomendada):
   - `RepairTimeWindows` ← Crítica para VRPTW
   - `RepairCapacity` ← Crítica para VRPTW
   - `GreedyRepair`

#### ❌ Prohibido:
- Constructores sin aleatoriedad (GreedyByRatio puro)
- Perturbaciones sin reparación posterior
- Menos de 2 operadores de mejora

### 4. **Ejemplos de Validación de Algoritmos**
```markdown
✅ Algoritmo 1 VÁLIDO:
  - Constructor: RandomizedInsertion(alpha=0.15)
  - Operadores: TwoOpt + CrossExchange
  - Reparación: RepairTimeWindows
  → Cumple: randomizado + 2 ops + reparación

❌ Algoritmo 2 INVÁLIDO:
  - Constructor: GreedyByValue (sin aleatoriedad)
  - Operadores: TwoOpt (solo 1)
  → Falla: no GRASP + insuficientes ops

✅ Algoritmo 3 VÁLIDO:
  - Constructor: RegretInsertion(random_seed)
  - Operadores: OrOpt + SwapCustomers
  - Reparación: RepairCapacity
  → Cumple: constructor randomizado + 2 ops + reparación
```

### 5. **Variables Independientes y Dependientes**
```markdown
Independientes:
- Algoritmo GRASP (3 variantes)
- Familia de instancias (R, C, RC)
- Parámetro α (típicamente 0.10-0.20)
- Operadores de mejora (combinaciones variables)

Dependientes:
- Distancia total recorrida (métrica principal)
- Número de vehículos (métrica secundaria)
- Gap al BKS (Best Known Solution): %(solución - BKS) / BKS
- Tiempo ejecución (segundos)
- Iteraciones GRASP completadas
- Evaluaciones de soluciones
```

### 6. **Análisis Estadístico Completo**
```markdown
1. Descriptivas por algoritmo (media, desviación, min/max, mediana)
2. Kruskal-Wallis (comparación múltiple, 3 algoritmos)
3. Wilcoxon pareado (entre dos mejores algoritmos)
4. Cohen's d (tamaño del efecto)
5. Trade-off calidad-tiempo (correlación, Pareto-óptimos)
6. Nivel significancia: α = 0.05
```

### 7. **Presupuesto Computacional Estimado**
```markdown
Por ejecución GRASP:
- Max iteraciones: 100
- Max sin mejora: 20 iteraciones
- Timeout: 60 segundos por instancia
- Evaluaciones máximas: 5000-10000

Presupuesto total:
- Test Rápido (R family): ~5-10 minutos
- Full (todas familias): ~20-30 minutos
```

### 8. **Estructura de Archivos de Salida**
```markdown
output/
├── vrptw_experiments_RAPID_YYYYMMDD_HHMMSS/
│   └── experiment_rapid_*.json (30 resultados)
├── vrptw_experiments_FULL_YYYYMMDD_HHMMSS/
│   └── experiment_full_*.json (90 resultados)
├── plots_vrptw_RAPID_YYYYMMDD_HHMMSS/
│   ├── gap_comparison_boxplot.png
│   ├── gap_comparison_bars.png
│   ├── quality_vs_time_scatter.png
│   ├── convergence_curves.png
│   ├── vehicles_used_comparison.png
│   ├── routes_detailed_*.png (1 por instancia)
│   ├── README.md (resumen)
│   └── time_tracking.md (tiempos)
├── plots_vrptw_FULL_YYYYMMDD_HHMMSS/
│   ├── (idem anterior +)
│   ├── performance_by_family.png (R vs C vs RC)
│   ├── performance_by_size.png (por tamaño)
│   └── statistics_summary.md
└── algorithms/
    ├── GAA_Algorithm_1.json
    ├── GAA_Algorithm_2.json
    ├── GAA_Algorithm_3.json
    └── algorithms_pseudocode.md
```

### 9. **Gráficas Generadas**
```markdown
Estadísticas:
- Boxplot comparación gap
- Barras gap promedio ± desv est
- Scatter trade-off calidad-tiempo
- Barras número vehículos

Convergencia:
- Curvas de evolución de gap

Detalle:
- Visualizaciones de rutas (posiciones + ventanas tiempo)

Analysis (Full):
- Desempeño por familia (R/C/RC)
- Desempeño por tamaño (pequeño/mediano/grande)
```

### 10. **Criterios de Validación**
```markdown
✅ Factibilidad: 100% soluciones factibles (sin violaciones)
✅ Completitud: Todos experimentos completados
✅ Reproducibilidad: Seed=42 fijo
✅ Estadística: Tests con p-values reportados
✅ Documentación: Todos archivos presentes
```

### 11. **Escenarios de Interpretación**
```markdown
Caso 1: Un algoritmo domina
  → Resultado: Algoritmo robusto para VRPTW

Caso 2: Especialización por familia
  → Familia R: Algoritmo A mejor
  → Familia C: Algoritmo B mejor
  → Familia RC: Algoritmo C mejor
  → Resultado: Especialización, combinar

Caso 3: Trade-off calidad-tiempo
  → Alg1: 4.8% gap (25s)
  → Alg2: 5.5% gap (8s)
  → Resultado: Seleccionar según restricción temporal
```

### 12. **Próximos Pasos**
```markdown
1. Análisis detallado de patrones
2. Refinamiento de parámetros GRASP
3. Escalabilidad (Gehring-Homberger instances)
4. Comparación contra heurísticas referencia
5. Publicación de resultados en paper
```

---

## 🔄 Adaptación desde KBP-SA

### Patrón Copiado (con Adaptaciones):

| Concepto KBP-SA | Adaptado para VRPTW-GRASP |
|---|---|
| 2 grupos instancias (low-dim, large-scale) | 3 familias Solomon (R, C, RC) |
| 31 instancias totales | 30 instancias Solomon |
| 3 algoritmos KBP generados | 3 algoritmos GRASP generados |
| 1 repetición | 1 repetición |
| Test matriz = 93 experimentos | Test matriz = 90 experimentos |
| Evaluaciones SA: 5000 | Iteraciones GRASP: 100 |
| Gráficas: boxplot, bars, scatter | Gráficas: boxplot, bars, scatter, convergence, rutas |
| Tests: Kruskal-Wallis, Wilcoxon | Tests: Kruskal-Wallis, Wilcoxon (idéntico) |
| JSON + PNG + MD | JSON + PNG + MD (idéntico) |

### Diferencias Principales:

1. **Criterios operacionales NUEVOS** (no existían en KBP-SA):
   - Restricciones obligatorias de composición de operadores
   - Validación de algoritmo randomizado (para GRASP)
   - Validación de múltiples operadores VND
   - Validación de reparación de restricciones

2. **Contexto de problema**:
   - KBP-SA: Problema de optimización simple (maximización de valor)
   - VRPTW-GRASP: Problema multiobjetivo con restricciones duras
   - Requiere validación de factibilidad (capacidad, ventanas tiempo)

3. **Métricas de problema**:
   - KBP-SA: Valor de solución, gap al óptimo
   - VRPTW-GRASP: Distancia, vehículos, gap al BKS, violaciones

---

## 📊 Verificación de Contenido

### Secciones Completadas:
- [x] 1. Visión General
- [x] 2. Dimensiones del Experimento
- [x] 3. Datasets Utilizados
- [x] 4. Generación de Algoritmos
- [x] 5. Criterio de Uso de Operadores (CRÍTICA)
- [x] 6. Variables Independientes/Dependientes
- [x] 7. Comparación y Análisis
- [x] 8. Análisis Estadístico
- [x] 9. Presupuesto Computacional
- [x] 10. Reportes y Visualizaciones
- [x] 11. Criterios de Validación
- [x] 12. Interpretación de Resultados
- [x] 13. Próximos Pasos

### Estado del Proyecto Actualizado:
```markdown
- [x] Problema definido
- [x] Modelo matemático
- [x] Operadores identificados
- [x] Metaheurística seleccionada
- [x] Parámetros configurados
- [x] Plan experimental COMPLETO ← NUEVO
- [x] Criterios de validación ← NUEVO
- [ ] Datasets agregados (próximo paso)
- [ ] Gramática implementada
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados
```

---

## 💡 Notas Importantes

### Para el Usuario:
1. **Criterio de Operadores es CRÍTICA**: Define qué hace un algoritmo "válido" para VRPTW
2. **Dos modos operacionales**: Test rápido para validación, Full para análisis completo
3. **Reproducibilidad**: Seed=42 garantiza mismos algoritmos generados cada vez
4. **Escalabilidad**: Estructura permite fácilmente agregar instancias Gehring-Homberger

### Próxima Fase:
1. Agregación de datasets Solomon (archivos .txt en `datasets/`)
2. Implementación de gramática VRPTW-GRASP
3. Adaptación de scripts `runner.py` para VRPTW
4. Ejecución experimental

---

## 📚 Referencias Añadidas
Mantiene todas las referencias bibliográficas originales + contexto de KBP-SA

**Estado**: ✅ Parte 4 completada correctamente
**Documento Final**: `problema_metaheuristica.md` (989 líneas)
