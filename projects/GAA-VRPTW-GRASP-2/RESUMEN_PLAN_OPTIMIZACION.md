# Plan de Optimización de Parámetros - RESUMEN EJECUTIVO

**Fecha**: 3 de Enero, 2026  
**Objetivo**: Encontrar la combinación óptima de parámetros para el **Algoritmo 3** en familia **C1**  
**Método**: Búsqueda exhaustiva de 100 combinaciones aleatorias  
**Duración estimada**: 3-4 horas  

---

## 🎯 OBJETIVO PRINCIPAL

Identificar qué combinación de parámetros para el **Algoritmo 3** se acerca lo máximo posible a los **Best Known Solutions (BKS)** de la familia **C1** tanto en:
- **K** (número de vehículos)
- **D** (distancia total)

---

## 📊 FAMILIA C1

```
C1: Clustered - Normal Period
├── 9 instancias: C101, C102, ..., C109
├── K_BKS: 10 vehículos (fijo para todas)
├── D_BKS: ~828.93 km (promedio)
└── Tiempo ejecución QUICK: ~1-2 minutos por combinación
```

---

## 🔧 PARÁMETROS A OPTIMIZAR (Algoritmo 3)

| Parámetro | Rango Actual (ITER-7) | Rango Búsqueda | Paso |
|-----------|----------------------|-----------------|------|
| **While** | 100 | 50 - 150 | 10 |
| **TwoOpt (pre)** | 45 | 20 - 80 | 5 |
| **DoubleBridge** | 1.5 | 0.5 - 3.0 | 0.5 |
| **TwoOpt (post)** | 40 | 20 - 80 | 5 |
| **Relocate** | 35 | 10 - 50 | 5 |

---

## 📈 METODOLOGÍA

### Fase 1: Generación (10 minutos)
```
✓ Generar 100 combinaciones aleatorias de parámetros
✓ Guardar en: optimization_results_c1/combinations.json
```

### Fase 2: Búsqueda (165 minutos ≈ 2.75 horas)
```
Para cada una de las 100 combinaciones:
  1. Actualizar parámetros en src/gaa/algorithm_generator.py
  2. Ejecutar: python scripts/experiments.py --mode QUICK (solo C1)
  3. Recolectar resultados (K, D) para 9 instancias
  4. Calcular: GAP_K = (K_algo - K_BKS) / K_BKS * 100
  5. Calcular: GAP_D = (D_algo - D_BKS) / D_BKS * 100
  6. SCORE = GAP_K + GAP_D  (minimizar)
  7. Guardar resultados
```

**Tiempo por combinación**: ~1.6 minutos (160 segundos)

### Fase 3: Análisis (10 minutos)
```
✓ Ordenar por SCORE (menor es mejor)
✓ Identificar Top 10 mejores combinaciones
✓ Generar estadísticas (promedio, mediana, desv. est.)
```

### Fase 4: Reporte (10 minutos)
```
✓ Generar: optimization_results_c1/report.txt
✓ Generar: optimization_results_c1/results.json
✓ Mostrar Top 10 en consola
```

---

## 📁 ARCHIVOS ENTREGABLES

Se han creado **3 archivos principales**:

### 1. **`parameter_tuner_algo3.py`** ⭐ RECOMENDADO
```bash
python parameter_tuner_algo3.py --num-combinations 100
```

**Características**:
- Script más ágil y directo
- Output limpio y fácil de interpretar
- Gestión eficiente de memoria
- Reporte automático al finalizar

**Genera**:
- `optimization_results_c1/combinations.json` (100 combinaciones)
- `optimization_results_c1/results.json` (resultados detallados)
- `optimization_results_c1/report.txt` (reporte ejecutivo)

### 2. **`parameter_optimizer_c1.py`** (Alternativa)
```bash
python parameter_optimizer_c1.py
```

**Características**:
- Framework más completo
- Clases detalladas y documentadas
- Análisis estadísticos adicionales
- Extensible para futuras mejoras

### 3. **`PLAN_OPTIMIZACION_C1.md`** (Documentación)
Plan detallado con:
- Objetivos y alcance
- Rangos de parámetros
- Métricas de evaluación
- Timeline esperado

---

## 🚀 CÓMO EJECUTAR

### Opción 1: Prueba Rápida (10 minutos)
```bash
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python parameter_tuner_algo3.py --num-combinations 10
```

### Opción 2: Búsqueda Principal (3-4 horas)
```bash
python parameter_tuner_algo3.py --num-combinations 100
```

### Opción 3: Búsqueda Exhaustiva (6-8 horas)
```bash
python parameter_tuner_algo3.py --num-combinations 200
```

---

## 📊 EJEMPLO DE SALIDA ESPERADA

```
================================================================================
PARAMETER TUNING - Algorithm 3 - Family C1
Combinaciones a probar: 100
Instancias: C1 (9 instancias)
Timestamp: 2026-01-03 10:30:45
================================================================================

[1/4] Generando 100 combinaciones...
      [OK] 100 combinaciones generadas

[2/4] Ejecutando búsqueda de parámetros...

  [  1/100] W:100 2OP:45 DB:1.5 2POST:40 REL:35
       [OK] Score=2.531, GAP_K=1.23%, GAP_D=1.31%, Time=45.3s

  [  2/100] W:120 2OP:65 DB:2.1 2POST:55 REL:28
       [OK] Score=3.845, GAP_K=1.89%, GAP_D=1.96%, Time=48.1s

  ...

  [100/100] W:75 2OP:35 DB:1.8 2POST:35 REL:25
       [OK] Score=1.987, GAP_K=0.92%, GAP_D=1.07%, Time=44.1s

[3/4] Analizando resultados...

  Top 10 Combinaciones:
    #1: W:75 2OP:35 DB:1.8 2POST:35 REL:25 → Score=1.987
    #2: W:85 2OP:40 DB:1.7 2POST:38 REL:28 → Score=2.012
    #3: W:80 2OP:42 DB:1.6 2POST:36 REL:30 → Score=2.045
    ...

[4/4] Generando reportes...

  Resultados JSON:  optimization_results_c1/results.json
  Reporte Texto:    optimization_results_c1/report.txt

================================================================================
[OK] OPTIMIZACIÓN COMPLETADA
[OK] Tiempo total: 165.3 minutos (2.75 horas)
[OK] Resultados: 100/100
[OK] Archivos: optimization_results_c1
================================================================================
```

---

## 📋 REPORTE ESPERADO

```
TOP 10 BEST COMBINATIONS
================================================================================

#1: Score = 1.987456
  Parámetros: While=75, 2Opt_pre=35, DB=1.8, 2Opt_post=35, Relocate=25
  Avg GAP_K: 0.920%
  Avg GAP_D: 1.067%
  Exec Time: 44.1s

#2: Score = 2.012389
  Parámetros: While=85, 2Opt_pre=40, DB=1.7, 2Opt_post=38, Relocate=28
  Avg GAP_K: 0.945%
  Avg GAP_D: 1.067%
  Exec Time: 45.3s

...

STATISTICS
================================================================================
Best Score:   1.234567
Worst Score:  5.678901
Avg Score:    3.456789
Median Score: 3.234567
Std Dev:      0.987654
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Plan detallado creado: `PLAN_OPTIMIZACION_C1.md`
- [x] Script principal: `parameter_tuner_algo3.py`
- [x] Script alternativo: `parameter_optimizer_c1.py`
- [x] Guía de uso: `GUIA_PARAMETER_TUNING.md`
- [x] Generador de combinaciones (aleatorio)
- [x] Integración con best_known_solutions.json
- [x] Sistema de evaluación de resultados
- [x] Generador de reportes (JSON + TXT)
- [x] Documentación completa

---

## 🎓 PRÓXIMOS PASOS

### Inmediato (Después de optimizar C1):
1. **Ejecutar búsqueda**: `python parameter_tuner_algo3.py --num-combinations 100`
2. **Revisar resultados**: `cat optimization_results_c1/report.txt`
3. **Identificar mejores parámetros**: Tomar los valores del #1

### Corto Plazo (1-2 días):
1. **Aplicar parámetros óptimos** a `src/gaa/algorithm_generator.py`
2. **Ejecutar FULL experiment** para validar:
   ```bash
   python scripts/experiments.py --mode FULL
   ```
3. **Comparar resultados** ITER-7 vs ITER-8 (con parámetros optimizados)

### Mediano Plazo (1-2 semanas):
1. **Repetir optimización** para familia R1
2. **Repetir optimización** para familia RC1
3. **Buscar parámetros universales** que funcionen bien en todas las familias

### Largo Plazo (Investigación):
1. **Implementar optimización automática** con algoritmos genéticos o Bayesian Optimization
2. **Extender a otras familias** (R2, RC2, etc.)
3. **Publicar resultados** y parámetros óptimos

---

## 🔍 INTERPRETACIÓN DE MÉTRICAS

```
SCORE = GAP_K + GAP_D

Ejemplo:
  GAP_K = 0.920%   (0.920% por encima del BKS en vehículos)
  GAP_D = 1.067%   (1.067% por encima del BKS en distancia)
  SCORE = 1.987    (suma total)

Interpretación:
  - Score < 2.0   → Excelente
  - Score 2.0-3.0 → Muy bueno
  - Score 3.0-5.0 → Bueno
  - Score > 5.0   → Regular
```

---

## 📝 NOTAS TÉCNICAS

1. **C1 es familia de prueba**: Instancias pequeñas, ejecución rápida
2. **Parámetros actuales ITER-7**: While=100, 2Opt_pre=45, DB=1.5, 2Opt_post=40, Relocate=35
3. **Reproducibilidad**: Seed fijo (42) para generar las mismas 100 combinaciones
4. **Paralelización**: Opcional en futuro si se necesita acelerar

---

## 📞 CONTACTO Y SOPORTE

- **Script principal**: `parameter_tuner_algo3.py`
- **Documentación**: `GUIA_PARAMETER_TUNING.md`
- **Resultados**: `optimization_results_c1/`

---

**¡Listo para comenzar la optimización!** 🚀

