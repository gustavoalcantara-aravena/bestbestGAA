# 📊 PLAN DE OPTIMIZACIÓN - VISUALIZACIÓN RÁPIDA

## 🎯 OBJETIVO

```
┌─────────────────────────────────────────────────────────────────┐
│ Encontrar los MEJORES PARÁMETROS para ALGORITMO 3 en FAMILIA C1 │
│                                                                  │
│ Métrica: Minimizar (GAP_K + GAP_D) respecto a KBS              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 FAMILIA C1

```
┌─────────────────────────────────────────┐
│ C1: Clustered - Normal Period            │
├─────────────────────────────────────────┤
│ Instancias:     9 (C101 - C109)         │
│ K_BKS:          10 vehículos (todas)    │
│ D_BKS:          ~828.93 km (promedio)  │
│ Tiempo QUICK:   ~1-2 min por combo      │
└─────────────────────────────────────────┘
```

---

## 🔧 PARÁMETROS A OPTIMIZAR

```
┌──────────────────┬─────────┬─────────┬──────────────────────┐
│ Parámetro        │ Mínimo  │ Máximo  │ Descripción          │
├──────────────────┼─────────┼─────────┼──────────────────────┤
│ While            │ 50      │ 150     │ Iteraciones ILS      │
│ TwoOpt (pre)     │ 20      │ 80      │ Pre-perturbación     │
│ DoubleBridge     │ 0.5     │ 3.0     │ Intensidad pert.     │
│ TwoOpt (post)    │ 20      │ 80      │ Post-perturbación    │
│ Relocate         │ 10      │ 50      │ Movimientos finales  │
└──────────────────┴─────────┴─────────┴──────────────────────┘
```

---

## 🚀 FLUJO DE EJECUCIÓN

```
START
  │
  ├─→ [FASE 1] Generar 100 Combinaciones Aleatorias (10 min)
  │   │
  │   └─→ combinations.json
  │
  ├─→ [FASE 2] Ejecutar Búsqueda (165 min ≈ 2.75 horas)
  │   │
  │   └─→ FOR i = 1 TO 100:
  │       │
  │       ├─→ Actualizar parámetros en algorithm_generator.py
  │       ├─→ Ejecutar: python scripts/experiments.py --mode QUICK
  │       ├─→ Recolectar resultados (K, D para C1)
  │       ├─→ Calcular: GAP_K = (K_algo - K_BKS) / K_BKS * 100
  │       ├─→ Calcular: GAP_D = (D_algo - D_BKS) / D_BKS * 100
  │       ├─→ SCORE = GAP_K + GAP_D
  │       └─→ Guardar resultado
  │
  ├─→ [FASE 3] Ranking y Análisis (10 min)
  │   │
  │   ├─→ Ordenar por SCORE (menor es mejor)
  │   ├─→ Identificar Top 10
  │   └─→ Calcular estadísticas
  │
  ├─→ [FASE 4] Generar Reportes (10 min)
  │   │
  │   ├─→ results.json (todos los resultados)
  │   ├─→ report.txt (reporte ejecutivo)
  │   └─→ Mostrar Top 10 en consola
  │
END
  │
  └─→ TOTAL: ~4 HORAS
```

---

## 💻 SCRIPTS DISPONIBLES

```
┌──────────────────────────────────────────┐
│ PRINCIPAL - parameter_tuner_algo3.py     │ ⭐ RECOMENDADO
├──────────────────────────────────────────┤
│ $ python parameter_tuner_algo3.py        │
│   --num-combinations 100                 │
│   --output-dir results_c1                │
│                                          │
│ ✓ Script ágil y directo                 │
│ ✓ Output limpio                         │
│ ✓ Reporte automático                    │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ ALTERNATIVO - parameter_optimizer_c1.py │
├──────────────────────────────────────────┤
│ $ python parameter_optimizer_c1.py       │
│                                          │
│ ✓ Framework más completo                │
│ ✓ Clases detalladas                     │
│ ✓ Análisis estadísticos avanzados       │
└──────────────────────────────────────────┘
```

---

## 📊 EJEMPLO DE SALIDA

```
================================================================================
PARAMETER TUNING - Algorithm 3 - Family C1
Combinaciones a probar: 100
Timestamp: 2026-01-03 10:30:45
================================================================================

[1/4] Generando 100 combinaciones...
      [OK] 100 combinaciones generadas

[2/4] Ejecutando búsqueda de parámetros...

  [  1/100] W:100 2OP:45 DB:1.5 2POST:40 REL:35
       [OK] Score=2.531, GAP_K=1.23%, GAP_D=1.31%, Time=45.3s

  [  2/100] W:120 2OP:65 DB:2.1 2POST:55 REL:28
       [OK] Score=3.845, GAP_K=1.89%, GAP_D=1.96%, Time=48.1s

  ... 98 combinaciones más ...

[3/4] Analizando resultados...

  Top 10 Combinaciones:
    #1: W:75 2OP:35 DB:1.8 2POST:35 REL:25 → Score=1.987
    #2: W:85 2OP:40 DB:1.7 2POST:38 REL:28 → Score=2.012
    #3: W:80 2OP:42 DB:1.6 2POST:36 REL:30 → Score=2.045
    ... 7 más ...

[4/4] Generando reportes...

================================================================================
[OK] OPTIMIZACIÓN COMPLETADA - 165 minutos
[OK] Archivos: optimization_results_c1/
================================================================================
```

---

## 📁 ESTRUCTURA DE SALIDA

```
optimization_results_c1/
│
├── combinations.json          ← Todas las 100 combinaciones
│   {
│     "id": 1,
│     "while_iters": 100,
│     "twoopt_pre": 45,
│     "doublebridge": 1.5,
│     "twoopt_post": 40,
│     "relocate": 35
│   }
│
├── results.json              ← Resultados detallados
│   {
│     "combo_id": 1,
│     "parameters": {...},
│     "instance_results": {
│       "C101": {"k": 10.0, "d": 828.99, "gap_k": 0.0, "gap_d": 0.0007},
│       "C102": {...},
│       ...
│     },
│     "avg_gap_k": 0.876,
│     "avg_gap_d": 1.111,
│     "score": 1.987,
│     "rank": 1
│   }
│
└── report.txt               ← Reporte ejecutivo
    TOP 10 BEST COMBINATIONS
    ================================================================================
    
    #1: Score = 1.987456
      Parámetros: While=75, 2Opt_pre=35, DB=1.8, 2Opt_post=35, Relocate=25
      Avg GAP_K: 0.876%
      Avg GAP_D: 1.111%
      Exec Time: 44.1s
    
    #2: Score = 2.012389
    ...
```

---

## 🎓 CÓMO INTERPRETAR RESULTADOS

```
┌─────────────────────────────────────────────────────────┐
│ SCORE = GAP_K + GAP_D                                   │
│                                                         │
│ Ejemplo #1 (MEJOR):                                     │
│   GAP_K = 0.876%   (0.876% sobre BKS en vehículos)    │
│   GAP_D = 1.111%   (1.111% sobre BKS en distancia)    │
│   SCORE = 1.987    ✓ Excelente                         │
│                                                         │
│ Ejemplo #10 (PEOR):                                     │
│   GAP_K = 2.345%   (2.345% sobre BKS en vehículos)    │
│   GAP_D = 3.210%   (3.210% sobre BKS en distancia)    │
│   SCORE = 5.555    ✗ Regular                           │
│                                                         │
│ Escala de Calidad:                                      │
│   Score < 2.0   → ⭐⭐⭐⭐⭐ Excelente              │
│   Score 2-3     → ⭐⭐⭐⭐  Muy bueno              │
│   Score 3-5     → ⭐⭐⭐   Bueno                    │
│   Score > 5     → ⭐⭐    Regular                   │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ CHECKLIST RÁPIDO

```
ANTES DE EJECUTAR:
  ☐ Estar en directorio correcto: GAA-VRPTW-GRASP-2/
  ☐ Verificar que existe best_known_solutions.json
  ☐ Verificar que existe src/gaa/algorithm_generator.py
  ☐ Verificar que existe scripts/experiments.py

EJECUTAR:
  ☐ python parameter_tuner_algo3.py --num-combinations 100

DURANTE:
  ☐ Monitorear progreso (debería tomar ~3-4 horas)
  ☐ Verificar que cada combinación muestre "[OK]"

DESPUÉS:
  ☐ Leer optimization_results_c1/report.txt
  ☐ Identificar parámetros del #1
  ☐ Aplicar parámetros a algorithm_generator.py
  ☐ Ejecutar FULL experiment para validar
```

---

## 🚀 COMANDOS RÁPIDOS

```bash
# Prueba rápida (10 minutos)
python parameter_tuner_algo3.py --num-combinations 10

# Búsqueda principal (3-4 horas) ⭐ RECOMENDADO
python parameter_tuner_algo3.py --num-combinations 100

# Búsqueda exhaustiva (6-8 horas)
python parameter_tuner_algo3.py --num-combinations 200

# Ver resultados
cat optimization_results_c1/report.txt

# Extraer mejores parámetros
python -c "
import json
with open('optimization_results_c1/results.json') as f:
    best = json.load(f)[0]
    p = best['parameters']
    print(f'MEJORES PARÁMETROS:')
    print(f'  While: {p[\"while\"]}')
    print(f'  TwoOpt (pre): {p[\"twoopt_pre\"]}')
    print(f'  DoubleBridge: {p[\"doublebridge\"]}')
    print(f'  TwoOpt (post): {p[\"twoopt_post\"]}')
    print(f'  Relocate: {p[\"relocate\"]}')
"
```

---

## 📞 DOCUMENTACIÓN

- 📄 **PLAN_OPTIMIZACION_C1.md** - Plan completo (10 páginas)
- 📄 **GUIA_PARAMETER_TUNING.md** - Guía práctica de uso
- 📄 **RESUMEN_PLAN_OPTIMIZACION.md** - Resumen ejecutivo
- 💾 **parameter_tuner_algo3.py** - Script principal
- 💾 **parameter_optimizer_c1.py** - Framework alternativo

---

## ⏱️ TIMELINE

```
┌────────────────────────────────────────────────────────┐
│ FASE 1: Generación de Combinaciones      10 minutos    │
├────────────────────────────────────────────────────────┤
│ FASE 2: Búsqueda (100 combos × 1.6 min) 165 minutos   │
├────────────────────────────────────────────────────────┤
│ FASE 3: Análisis                         10 minutos    │
├────────────────────────────────────────────────────────┤
│ FASE 4: Generación de Reportes          10 minutos    │
├────────────────────────────────────────────────────────┤
│ TOTAL:                                  ~195 minutos   │
│                                          (~3.25 horas)  │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 PRÓXIMOS PASOS

```
1. Ejecutar búsqueda
   $ python parameter_tuner_algo3.py --num-combinations 100
   
   ↓ (esperar ~3 horas)
   
2. Revisar Top 10
   $ cat optimization_results_c1/report.txt
   
   ↓
   
3. Extraer mejores parámetros del #1
   
   ↓
   
4. Aplicar a src/gaa/algorithm_generator.py
   (Reemplazar parámetros del ALGORITMO 3)
   
   ↓
   
5. Validar con FULL experiment
   $ python scripts/experiments.py --mode FULL
   
   ↓
   
6. Comparar ITER-7 vs ITER-8 (optimizado)
```

---

**¡Listo para comenzar!** 🚀

