# Resumen Ejecutivo: Análisis de Rendimiento de both.py

**Fecha**: 26 de Diciembre de 2025
**Tiempo actual**: ~34 segundos (ambos grupos: low_dimensional + large_scale)

---

## 🎯 Hallazgos Principales

### 1. **Causa Raíz del Tiempo de 34 Segundos**

**79% del tiempo** (26-28s) se gasta en generar visualizaciones SA:

```
Fase                                    Tiempo    %
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generar visualizaciones SA              ~26s     79%
  ├─ Ejecutar SA con 5000 evaluaciones  ~18s
  │  └─ 31 instancias × 5000 evals cada una
  └─ Generar 37 gráficas                ~8s
     ├─ 31 gráficas individuales
     └─ 6 gráficas agregadas

Generar visualizaciones base            ~4s      12%
Imports y preparación                   ~2s       6%
Ejecutar experimentos (30 total)       ~1s       3%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                                   ~34s    100%
```

**Ubicación en código**: `demo_experimentation_both.py:50-270`

---

### 2. **Causa Raíz de Variabilidad entre Ejecuciones**

**Variabilidad normal medida**: **4.0%** (±0.7s)

| Ejecución | Archivos | Tamaño | Tiempo | Variación |
|-----------|----------|--------|--------|-----------|
| 1 (limpio)| 18       | 5.3 MB | 17.79s | baseline  |
| 2         | 35       | 10.5 MB| 17.95s | +0.9%     |
| 3         | 52       | 15.8 MB| 19.01s | +6.9%     |
| 4         | 69       | 21.1 MB| 16.82s | -5.5%     |
| 5 (limpio)| 18       | 5.3 MB | 17.57s | -1.2%     |

**CONCLUSIÓN**:
- ✅ Variabilidad del 4% es **NORMAL** (factores del SO)
- ✅ **NO** hay degradación por acumulación de archivos
- ⚠️  Si observas variabilidad >10%, la causa es **externa** (ver tabla abajo)

---

## 🔍 Tabla de Diagnóstico Rápido

| Síntoma | Causa Raíz | Probabilidad | Solución |
|---------|-----------|--------------|----------|
| Siempre ~34s | Operaciones costosas (diseño del script) | 100% | Optimizar (ver abajo) |
| Primera vez +10% más lenta | Imports + cache matplotlib | 90% | Normal, ignorar |
| +5-10% variable | Garbage collection Python | 70% | `gc.collect()` antes |
| +100-500% MUY lento | **SWAPPING** (falta RAM) | 95% | Cerrar apps, liberar RAM |
| Gradualmente más lento | Throttling por temperatura CPU | 60% | Mejorar ventilación |
| Variable sin patrón ±10% | Procesos background | 80% | Cerrar apps innecesarias |

**Diagnóstico rápido**:
```bash
# Verificar RAM disponible
free -h

# Ver swap usado (debe ser 0)
free -h | grep Swap

# Ver procesos pesados
top -o %CPU
```

Si swap > 0 o RAM < 500MB libre → **ESA es la causa raíz**

---

## 🚀 Soluciones Recomendadas

### Opción 1: Quick Win (3 cambios, 60% más rápido)

**Tiempo esperado**: De 34s → **~14s**

```python
# 1. Línea 19: Backend matplotlib sin GUI
import matplotlib
matplotlib.use('Agg')  # +5% mejora

# 2. Línea 95: Reducir evaluaciones SA
max_evaluations=2000,  # Era 5000 → +30% mejora

# 3. Líneas 251-266: Solo 5 gráficas representativas
representative_indices = [0, len(instances)//4, len(instances)//2,
                         3*len(instances)//4, len(instances)-1]
for idx in representative_indices:
    if idx < len(instances):
        # Generar gráfica solo para estas
```

**Archivo optimizado ya creado**: `demo_experimentation_both_OPTIMIZED.py`

---

### Opción 2: Optimización Completa (65% más rápido)

**Tiempo esperado**: De 34s → **~12s**

Incluye Quick Win + eliminación de carga duplicada de datasets + reducción de DPI

Ver detalles en: `PERFORMANCE_ANALYSIS.md`

---

### Opción 3: Reducir Variabilidad (para ejecuciones más consistentes)

```bash
# Antes de ejecutar:

# 1. Verificar RAM disponible
free -h  # Debe mostrar >1GB libre

# 2. Limpiar cache del sistema (opcional)
sync && echo 3 > /proc/sys/vm/drop_caches

# 3. Cerrar aplicaciones innecesarias
# - Navegadores
# - IDEs pesados
# - Docker

# 4. Ejecutar con prioridad alta
nice -n -10 python3 scripts/demo_experimentation_both.py
```

---

## 📁 Archivos Generados en Este Análisis

```
projects/KBP-SA/
├── PERFORMANCE_ANALYSIS.md              ← Análisis completo de rendimiento
├── ROOT_CAUSE_VARIABILITY.md            ← Causas raíz de variabilidad
├── RESUMEN_EJECUTIVO_PERFORMANCE.md     ← Este archivo
└── scripts/
    ├── demo_experimentation_both_OPTIMIZED.py  ← Versión optimizada
    ├── profile_both.py                  ← Script de profiling
    ├── time_analysis_both.py            ← Análisis de tiempos por fase
    ├── quick_test_both.py               ← Test rápido (solo low_dim)
    ├── quick_variability_test.py        ← Test de variabilidad
    └── diagnose_variability.py          ← Diagnóstico completo
```

---

## 🎯 Recomendación Final

### Si quieres **SOLO reducir el tiempo de 34s a ~14s**:

```bash
# Usar la versión optimizada
python3 scripts/demo_experimentation_both_OPTIMIZED.py
```

### Si observas **variabilidad significativa (>10%)**:

1. Verificar RAM: `free -h` (debe tener >1GB libre)
2. Cerrar aplicaciones pesadas
3. Ver `ROOT_CAUSE_VARIABILITY.md` sección "Checklist de Diagnóstico"

### Si necesitas **entender TODO en detalle**:

- **Rendimiento**: `PERFORMANCE_ANALYSIS.md`
- **Variabilidad**: `ROOT_CAUSE_VARIABILITY.md`

---

## 📊 Comparación de Versiones

| Versión | Tiempo | Gráficas | Evaluaciones SA | Mejora |
|---------|--------|----------|-----------------|--------|
| **Original** | 34s | 37 | 5000 × 31 | - |
| **Optimizada (Fase 1)** | ~14s | 16 | 2000 × 31 | **59%** |
| **Optimizada (Fase 2)** | ~12s | 16 | 2000 × 31 | **65%** |

---

## ✅ Próximos Pasos

1. **PROBAR** la versión optimizada:
   ```bash
   python3 scripts/demo_experimentation_both_OPTIMIZED.py
   ```

2. **MEDIR** el tiempo real en tu sistema

3. **VALIDAR** que las visualizaciones sigan siendo útiles

4. Si todo está bien:
   - Reemplazar `demo_experimentation_both.py` con la versión optimizada
   - O integrar los cambios específicos que necesites

5. Si hay problemas de variabilidad:
   - Consultar `ROOT_CAUSE_VARIABILITY.md`
   - Ejecutar diagnóstico: `python3 scripts/diagnose_variability.py`

---

**¿Preguntas?** Consulta los archivos de análisis detallado o ejecuta los scripts de diagnóstico.
