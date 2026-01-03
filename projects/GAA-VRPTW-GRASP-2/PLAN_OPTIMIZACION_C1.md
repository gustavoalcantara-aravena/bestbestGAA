# Plan de Optimización de Parámetros para Familia C1

## Objetivo General
Encontrar la combinación óptima de parámetros del **Algoritmo 3** que se acerque lo máximo posible a los **KBS (Best Known Solutions)** de la familia **C1** en términos de:
- **K** (número de vehículos)
- **D** (distancia total)

---

## 1. Estructura de la Familia C1

**Familias de Dataset:**
- **C1**: Clustered - Normal Period
  - 9 instancias: C101, C102, C103, C104, C105, C106, C107, C108, C109
  - K_BKS: 10 vehículos (todas las instancias)
  - D_BKS: ~828.93 km (promedio)

---

## 2. Parámetros a Optimizar para Algoritmo 3

Parámetros actuales ITER-7:
```
While: 100
TwoOpt (pre): 45
DoubleBridge: 1.5
TwoOpt (post): 40
Relocate: 35
```

### Rangos de Búsqueda Sugeridos:

| Parámetro | Mínimo | Máximo | Paso | Descripción |
|-----------|--------|--------|------|-------------|
| **While** | 50 | 150 | 10 | Iteraciones principales del ILS |
| **TwoOpt (pre)** | 20 | 80 | 5 | Movimientos 2-opt antes de perturbación |
| **DoubleBridge** | 0.5 | 3.0 | 0.5 | Intensidad de perturbación |
| **TwoOpt (post)** | 20 | 80 | 5 | Movimientos 2-opt después de perturbación |
| **Relocate** | 10 | 50 | 5 | Movimientos de reubicación final |

---

## 3. Metodología de Búsqueda

### Fase 1: Búsqueda Exhaustiva Acotada (100 ejecuciones)
- **Estrategia**: Muestreo aleatorio dentro de los rangos definidos
- **Ejecuciones por combinación**: 1 ejecución QUICK (solo C1)
- **Total**: 100 combinaciones diferentes
- **Métrica de éxito**: 
  - GAP_K = (K_algo - K_BKS) / K_BKS * 100
  - GAP_D = (D_algo - D_BKS) / D_BKS * 100
  - **Puntuación**: GAP_K + GAP_D (minimizar)

### Fase 2: Refinamiento (Opcional)
- Basado en los mejores 10 resultados de Fase 1
- Búsqueda más granular alrededor de esos parámetros

---

## 4. Estructura de Ejecución

### Paso 1: Generar 100 Combinaciones Aleatorias
```python
combinations = generate_random_combinations(
    num_combinations=100,
    ranges={
        'while': (50, 150, 10),
        'twoopt_pre': (20, 80, 5),
        'doublebridge': (0.5, 3.0, 0.5),
        'twoopt_post': (20, 80, 5),
        'relocate': (10, 50, 5)
    }
)
```

### Paso 2: Ejecutar QUICK para cada Combinación
```
for cada combinación:
    - Modificar parámetros en algorithm_generator.py
    - Ejecutar: python scripts/experiments.py --mode QUICK_C1
    - Recolectar resultados (K, D, GAP_K, GAP_D)
    - Registrar en archivo JSON
```

### Paso 3: Analizar Resultados
```
- Ordenar por puntuación (GAP_K + GAP_D)
- Top 10 mejores combinaciones
- Estadísticas de convergencia
- Gráficos de sensibilidad de parámetros
```

---

## 5. Archivos a Crear/Modificar

### Nuevos Archivos:

1. **`parameter_optimizer_c1.py`** (Script principal)
   - Generador de combinaciones
   - Ejecutor de QUICK modificado
   - Análisis de resultados
   - Generador de reportes

2. **`scripts/experiments_quick_c1.py`** (Experimento customizado)
   - QUICK mode pero SOLO para C1
   - Más rápido (~1-2 minutos por ejecución)

3. **`optimization_results_c1.json`** (Salida)
   - Todas las 100 combinaciones probadas
   - Resultados por instancia
   - Ranking de mejores parámetros

4. **`optimization_report_c1.txt`** (Reporte)
   - Resumen ejecutivo
   - Top 10 combinaciones
   - Análisis de sensibilidad
   - Recomendaciones

---

## 6. Métrica de Evaluación

Para cada combinación y cada instancia C1:

```
GAP_K = ((K_algo - K_BKS) / K_BKS) * 100
GAP_D = ((D_algo - D_BKS) / D_BKS) * 100
SCORE = GAP_K + GAP_D  (minimizar)
```

**Agregado para C1 completa:**
```
AVG_GAP_K = promedio de GAP_K en 9 instancias
AVG_GAP_D = promedio de GAP_D en 9 instancias
TOTAL_SCORE = AVG_GAP_K + AVG_GAP_D
```

---

## 7. Timeline Esperado

| Fase | Duración | Descripción |
|------|----------|-------------|
| Preparación | 10 min | Crear scripts de optimización |
| Búsqueda (100 iteraciones) | 150-200 min | ~1.5-2 min por ejecución QUICK |
| Análisis | 10 min | Procesar resultados |
| Reporte | 10 min | Generar visualizaciones |
| **TOTAL** | **3-4 horas** | Ejecución completa |

---

## 8. Extensiones Futuras

Después de optimizar C1:
- [ ] Familia R1 (Random distribution)
- [ ] Familia RC1 (Mixed distribution)
- [ ] Multi-family optimization (encontrar parámetros universales)
- [ ] Fine-tuning final con algoritmo genético o Bayesian Optimization

---

## 9. Archivos de Referencia

- `best_known_solutions.json` - BKS para todas las familias
- `src/gaa/algorithm_generator.py` - Generador actual de algoritmos
- `scripts/experiments.py` - Framework de ejecución

---

## 10. Notas Importantes

1. **C1 es la familia de prueba**: Instancias pequeñas, rápidas de resolver
2. **KBS conocidos**: Todos los valores de C1 están bien documentados
3. **Determinismo**: Usar seeds fijos para reproducibilidad
4. **Paralelización**: Opcional en futuro para acelerar búsqueda
5. **Almacenamiento**: Cada combinación genera ~5 MB de data (gráficos + CSVs)

