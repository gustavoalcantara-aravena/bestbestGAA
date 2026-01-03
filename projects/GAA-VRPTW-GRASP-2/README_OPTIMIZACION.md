# 🎯 OPTIMIZACIÓN DE PARÁMETROS - ALGORITMO 3 - FAMILIA C1

## ⚡ INICIO RÁPIDO

```bash
# Ejecutar búsqueda de 100 combinaciones (~3-4 horas)
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python parameter_tuner_algo3.py --num-combinations 100

# Ver resultados cuando termine
cat optimization_results_c1/report.txt
```

---

## 📋 DOCUMENTACIÓN DISPONIBLE

**Lee en este orden:**

1. **[VISUALIZACION_PLAN.md](VISUALIZACION_PLAN.md)** ← **EMPIEZA AQUÍ** (5 minutos)
   - Diagrama visual del flujo
   - Tabla de parámetros
   - Ejemplos de salida esperada
   - Checklist rápido

2. **[RESUMEN_PLAN_OPTIMIZACION.md](RESUMEN_PLAN_OPTIMIZACION.md)** (10 minutos)
   - Resumen ejecutivo
   - Objetivos y metodología
   - Timeline estimado
   - Próximos pasos

3. **[GUIA_PARAMETER_TUNING.md](GUIA_PARAMETER_TUNING.md)** (15 minutos)
   - Guía de uso práctica
   - Comandos y ejemplos
   - Interpretación de resultados
   - Troubleshooting

4. **[PLAN_OPTIMIZACION_C1.md](PLAN_OPTIMIZACION_C1.md)** (30 minutos)
   - Plan completo y detallado
   - Métricas de evaluación
   - Análisis técnico profundo
   - Extensiones futuras

---

## 🔧 SCRIPTS

### Principal: `parameter_tuner_algo3.py` ⭐ RECOMENDADO

```bash
# Uso básico
python parameter_tuner_algo3.py --num-combinations 100

# Customizado
python parameter_tuner_algo3.py \
  --num-combinations 200 \
  --output-dir my_results
```

**Genera**:
- `optimization_results_c1/combinations.json` - 100 combinaciones
- `optimization_results_c1/results.json` - Resultados detallados
- `optimization_results_c1/report.txt` - Reporte ejecutivo

### Alternativo: `parameter_optimizer_c1.py`

```bash
python parameter_optimizer_c1.py
```

Framework más completo con análisis avanzados.

---

## 📊 QUÉ OPTIMIZAMOS

**Algoritmo 3** en **Familia C1** (9 instancias):

| Parámetro | Rango | Actual |
|-----------|-------|--------|
| While | 50-150 | 100 |
| TwoOpt (pre) | 20-80 | 45 |
| DoubleBridge | 0.5-3.0 | 1.5 |
| TwoOpt (post) | 20-80 | 40 |
| Relocate | 10-50 | 35 |

**Métrica**: Minimizar `SCORE = GAP_K + GAP_D` respecto a KBS

---

## 📈 CRONOGRAMA

| Fase | Duración | Qué Hace |
|------|----------|----------|
| 1️⃣ Generación | 10 min | Genera 100 combinaciones |
| 2️⃣ Búsqueda | 165 min | Ejecuta QUICK 100 veces |
| 3️⃣ Análisis | 10 min | Ranking y estadísticas |
| 4️⃣ Reportes | 10 min | Genera JSON y TXT |
| **TOTAL** | **~3.25 h** | **Búsqueda completa** |

---

## 💡 EJEMPLO DE RESULTADO

```
TOP 10 BEST COMBINATIONS
================================================================================

#1: Score = 1.987456
  Parámetros: While=75, 2Opt_pre=35, DB=1.8, 2Opt_post=35, Relocate=25
  Avg GAP_K: 0.920%
  Avg GAP_D: 1.067%
  
#2: Score = 2.012389
  Parámetros: While=85, 2Opt_pre=40, DB=1.7, 2Opt_post=38, Relocate=28
  Avg GAP_K: 0.945%
  Avg GAP_D: 1.067%

... 8 más ...
```

---

## 🚀 PRÓXIMOS PASOS

1. **Ejecutar búsqueda**
   ```bash
   python parameter_tuner_algo3.py --num-combinations 100
   ```

2. **Revisar Top 10**
   ```bash
   cat optimization_results_c1/report.txt
   ```

3. **Aplicar mejores parámetros** a `src/gaa/algorithm_generator.py`

4. **Validar** con `python scripts/experiments.py --mode FULL`

5. **Comparar** ITER-7 vs ITER-8 (optimizado)

---

## ❓ FAQ

**P: ¿Cuánto tarda?**  
R: ~3 horas para 100 combinaciones (1.6 min c/u)

**P: ¿Puedo usar menos combinaciones?**  
R: Sí, `--num-combinations 50` tarda ~1.5 horas

**P: ¿Dónde veo los resultados?**  
R: En `optimization_results_c1/report.txt` cuando termine

**P: ¿Cómo aplico los parámetros óptimos?**  
R: Actualizar `src/gaa/algorithm_generator.py` con valores del #1

**P: ¿Puedo parallelizar?**  
R: Sí, con modificaciones futures (no está implementado aún)

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
GAA-VRPTW-GRASP-2/
│
├── 📄 parameter_tuner_algo3.py          ← Script PRINCIPAL
├── 📄 parameter_optimizer_c1.py         ← Script alternativo
│
├── 📖 VISUALIZACION_PLAN.md             ← Lee PRIMERO
├── 📖 RESUMEN_PLAN_OPTIMIZACION.md      ← Resumen ejecutivo
├── 📖 GUIA_PARAMETER_TUNING.md          ← Guía de uso
├── 📖 PLAN_OPTIMIZACION_C1.md           ← Plan detallado
│
├── 📁 optimization_results_c1/          ← Salida
│   ├── combinations.json
│   ├── results.json
│   └── report.txt
│
├── best_known_solutions.json            ← Datos de referencia
├── src/gaa/algorithm_generator.py       ← Donde aplicas parámetros
└── scripts/experiments.py               ← Ejecutor de QUICK
```

---

## 🎓 INTERPRETACIÓN DE MÉTRICAS

```
GAP_K = (K_algo - K_BKS) / K_BKS * 100
  ├─ GAP_K = 0% → Encontró número óptimo de vehículos
  ├─ GAP_K = 1% → 1% más vehículos que óptimo
  └─ GAP_K = 5% → 5% más vehículos (malo)

GAP_D = (D_algo - D_BKS) / D_BKS * 100
  ├─ GAP_D = 0% → Encontró distancia óptima
  ├─ GAP_D = 1% → 1% más distancia que óptima
  └─ GAP_D = 5% → 5% más distancia (malo)

SCORE = GAP_K + GAP_D
  ├─ Score < 2.0  → ⭐⭐⭐⭐⭐ Excelente
  ├─ Score < 3.0  → ⭐⭐⭐⭐  Muy bueno
  ├─ Score < 5.0  → ⭐⭐⭐   Bueno
  └─ Score > 5.0  → ⭐⭐    Regular
```

---

## ✅ VALIDACIÓN

Para verificar que todo funciona:

```bash
# 1. Verificar archivos requeridos
ls best_known_solutions.json
ls src/gaa/algorithm_generator.py
ls scripts/experiments.py

# 2. Prueba rápida (10 min)
python parameter_tuner_algo3.py --num-combinations 5

# 3. Si todo OK, ejecutar búsqueda principal
python parameter_tuner_algo3.py --num-combinations 100
```

---

## 📞 SOPORTE

Si tienes problemas:

1. **Verifica** que estés en el directorio correcto
2. **Lee** GUIA_PARAMETER_TUNING.md (sección Troubleshooting)
3. **Ejecuta** prueba rápida con `--num-combinations 5`
4. **Revisa** que todos los archivos requeridos existan

---

## 🔗 REFERENCIAS

- **BKS (Best Known Solutions)**: `best_known_solutions.json`
- **Algoritmo 3**: `src/gaa/algorithm_generator.py` (líneas 80-140)
- **Ejecutor QUICK**: `scripts/experiments.py` (QuickExperiment.run())

---

## 📝 NOTAS

- **C1 es familia de prueba**: Instancias pequeñas, rápidas de resolver
- **KBS bien documentados**: Todos los valores están verificados
- **Reproducibilidad**: Seed fijo (42) para comparabilidad
- **Paralelización**: Futura optimización posible

---

## 🎯 CHECKLIST FINAL

Antes de ejecutar:
- [ ] Estoy en directorio `GAA-VRPTW-GRASP-2`
- [ ] Existe `best_known_solutions.json`
- [ ] Existe `src/gaa/algorithm_generator.py`
- [ ] Existe `scripts/experiments.py`
- [ ] Leí VISUALIZACION_PLAN.md (5 min)

Listo para:
```bash
python parameter_tuner_algo3.py --num-combinations 100
```

---

**¡Buena suerte con la optimización!** 🚀

*Generado: 3 de Enero, 2026*

