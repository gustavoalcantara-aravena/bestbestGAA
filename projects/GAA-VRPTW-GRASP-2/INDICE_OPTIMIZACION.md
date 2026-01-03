# 📑 ÍNDICE COMPLETO - PLAN DE OPTIMIZACIÓN DE PARÁMETROS

## 🎯 OBJETIVO

Encontrar la combinación óptima de parámetros para el **Algoritmo 3** en la familia **C1**, probando **100 combinaciones diferentes** para minimizar `GAP_K + GAP_D` respecto a los Best Known Solutions (BKS).

---

## 📚 DOCUMENTOS (ORDEN DE LECTURA)

### 1️⃣ **GUIA_PASO_A_PASO.md** ⭐ EMPIEZA AQUÍ (30 minutos)
**Mejor para**: Usuarios que quieren ejecutar inmediatamente
```
Contenido:
  ✓ Preparación del entorno (5 min)
  ✓ Lectura rápida (5 min)
  ✓ Prueba rápida opcional (10 min)
  ✓ Búsqueda principal (3-4 horas)
  ✓ Revisión de resultados (10 min)
  ✓ Aplicación de parámetros (15 min)
  ✓ Validación FULL test (30 min)
  ✓ Git commit (5 min)
  ✓ Troubleshooting

Duración total: 4.5 horas (3.5 horas del script)
```

### 2️⃣ **VISUALIZACION_PLAN.md** (5 minutos)
**Mejor para**: Entender el flujo visualmente
```
Contenido:
  ✓ Diagrama visual del flujo
  ✓ Tabla de parámetros
  ✓ Ejemplo de salida esperada
  ✓ Estructura de carpetas de salida
  ✓ Interpretación de métricas
  ✓ Checklist rápido
  ✓ Comandos rápidos

Ideal para: Entendimiento rápido del proceso
```

### 3️⃣ **README_OPTIMIZACION.md** (10 minutos)
**Mejor para**: Resumen general y referencia rápida
```
Contenido:
  ✓ Inicio rápido
  ✓ Índice de documentación
  ✓ Scripts disponibles
  ✓ Parámetros a optimizar
  ✓ Cronograma
  ✓ Ejemplo de resultado
  ✓ FAQ (preguntas frecuentes)
  ✓ Interpretación de métricas

Ideal para: Quick reference durante ejecución
```

### 4️⃣ **RESUMEN_PLAN_OPTIMIZACION.md** (15 minutos)
**Mejor para**: Entender la metodología completa
```
Contenido:
  ✓ Objetivo principal
  ✓ Familia C1 (9 instancias)
  ✓ Parámetros a optimizar
  ✓ Metodología (4 fases)
  ✓ Archivos entregables
  ✓ Cómo ejecutar
  ✓ Ejemplo de salida esperada
  ✓ Reporte esperado
  ✓ Checklist de implementación
  ✓ Próximos pasos
  ✓ Notas técnicas

Ideal para: Comprender todo el proceso
```

### 5️⃣ **GUIA_PARAMETER_TUNING.md** (20 minutos)
**Mejor para**: Detalles técnicos y troubleshooting
```
Contenido:
  ✓ Descripción de scripts (dos opciones)
  ✓ Uso básico y avanzado
  ✓ Estructura de salida detallada
  ✓ Archivo results.json explicado
  ✓ Parámetros explorados (rangos)
  ✓ Personalización de rangos
  ✓ Flujo de actualización de parámetros
  ✓ Análisis post-optimización
  ✓ Troubleshooting completo
  ✓ Próximos pasos recomendados

Ideal para: Resolver problemas y detalles técnicos
```

### 6️⃣ **PLAN_OPTIMIZACION_C1.md** (30 minutos)
**Mejor para**: Plan completo y profundo
```
Contenido:
  ✓ Objetivo general
  ✓ Estructura familia C1
  ✓ Parámetros a optimizar (3 tablas)
  ✓ Metodología de búsqueda
  ✓ Estructura de ejecución
  ✓ Archivos a crear/modificar
  ✓ Métrica de evaluación
  ✓ Timeline esperado
  ✓ Extensiones futuras

Ideal para: Referencia completa y documentación
```

---

## 💾 SCRIPTS (2 OPCIONES)

### `parameter_tuner_algo3.py` ⭐ RECOMENDADO
```bash
python parameter_tuner_algo3.py --num-combinations 100
```

**Características**:
- ✅ Script ágil y directo
- ✅ Output limpio y fácil
- ✅ Reporte automático
- ✅ RECOMENDADO para iniciarse

**Genera**:
- `optimization_results_c1/combinations.json` (100 combos)
- `optimization_results_c1/results.json` (resultados)
- `optimization_results_c1/report.txt` (reporte ejecutivo)

### `parameter_optimizer_c1.py` (Alternativa)
```bash
python parameter_optimizer_c1.py
```

**Características**:
- ✅ Framework más completo
- ✅ Clases detalladas
- ✅ Análisis estadísticos
- ✅ Para usuarios avanzados

---

## 📊 FAMILIA C1

```
┌──────────────────────────────────┐
│ C1: Clustered - Normal Period     │
├──────────────────────────────────┤
│ Instancias: 9 (C101 - C109)      │
│ K_BKS: 10 vehículos (todas)      │
│ D_BKS: ~828.93 km (promedio)    │
│ Duración QUICK: 1-2 min/combo   │
│ Total: 100 combos × 1.6 min      │
│      = 160 minutos ≈ 2.75 h     │
└──────────────────────────────────┘
```

---

## 🔧 PARÁMETROS A OPTIMIZAR

| Parámetro | Mínimo | Máximo | Paso | Actual |
|-----------|--------|--------|------|--------|
| **While** | 50 | 150 | 10 | 100 |
| **TwoOpt (pre)** | 20 | 80 | 5 | 45 |
| **DoubleBridge** | 0.5 | 3.0 | 0.5 | 1.5 |
| **TwoOpt (post)** | 20 | 80 | 5 | 40 |
| **Relocate** | 10 | 50 | 5 | 35 |

---

## 📈 CRONOGRAMA

| Fase | Duración | Actividad |
|------|----------|-----------|
| 1️⃣ Generación | 10 min | Crear 100 combinaciones |
| 2️⃣ Búsqueda | 165 min | Ejecutar QUICK × 100 |
| 3️⃣ Análisis | 10 min | Ranking y stats |
| 4️⃣ Reportes | 10 min | Generar archivos |
| **TOTAL** | **~3.25 h** | **Búsqueda completa** |

---

## 🚀 CÓMO USAR ESTE ÍNDICE

### Si estoy en apurado (5 minutos)
1. Lee: **VISUALIZACION_PLAN.md**
2. Lee: **README_OPTIMIZACION.md**
3. Ejecuta: `python parameter_tuner_algo3.py --num-combinations 100`

### Si tengo 1 hora para entender antes de ejecutar
1. Lee: **GUIA_PASO_A_PASO.md** (30 min)
2. Lee: **VISUALIZACION_PLAN.md** (5 min)
3. Lee: **RESUMEN_PLAN_OPTIMIZACION.md** (15 min)
4. Lee: **README_OPTIMIZACION.md** (10 min)
5. Prepárate: **GUIA_PASO_A_PASO.md Paso 1**

### Si quiero entendimiento completo (1.5 horas)
1. **VISUALIZACION_PLAN.md** (5 min)
2. **GUIA_PASO_A_PASO.md** (30 min)
3. **README_OPTIMIZACION.md** (10 min)
4. **RESUMEN_PLAN_OPTIMIZACION.md** (15 min)
5. **GUIA_PARAMETER_TUNING.md** (20 min)
6. **PLAN_OPTIMIZACION_C1.md** (30 min)

### Si algo sale mal (Troubleshooting)
1. Revisa: **GUIA_PARAMETER_TUNING.md** (sección Troubleshooting)
2. Revisa: **GUIA_PASO_A_PASO.md** (sección Problemas Comunes)
3. Si sigue sin funcionar, revisa error en terminal

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
GAA-VRPTW-GRASP-2/
│
├── 📄 SCRIPTS
│   ├── parameter_tuner_algo3.py          (⭐ PRINCIPAL)
│   └── parameter_optimizer_c1.py         (Alternativa)
│
├── 📖 DOCUMENTACIÓN
│   ├── GUIA_PASO_A_PASO.md              (⭐ EMPIEZA AQUÍ)
│   ├── VISUALIZACION_PLAN.md            (Visual rápido)
│   ├── README_OPTIMIZACION.md           (Guía rápida)
│   ├── RESUMEN_PLAN_OPTIMIZACION.md     (Resumen ejecutivo)
│   ├── GUIA_PARAMETER_TUNING.md         (Detalles técnicos)
│   ├── PLAN_OPTIMIZACION_C1.md          (Plan completo)
│   └── INDICE_OPTIMIZACION.md           (Este archivo)
│
├── 📁 DATOS
│   ├── best_known_solutions.json        (BKS de referencia)
│   └── optimization_results_c1/         (Salida del script)
│       ├── combinations.json            (100 combinaciones)
│       ├── results.json                 (Resultados detallados)
│       └── report.txt                   (Reporte ejecutivo)
│
├── 💻 CÓDIGO ACTUAL
│   ├── src/gaa/algorithm_generator.py   (Dónde aplicas parámetros)
│   └── scripts/experiments.py           (Ejecutor QUICK)
│
└── 🔧 CONFIGURACIÓN
    └── .gitignore                       (No subir ciertos archivos)
```

---

## 🎓 FLUJO RECOMENDADO

```
INICIO
  │
  ├─→ ¿Tengo 5 min?
  │   ├─ Sí → VISUALIZACION_PLAN.md
  │   └─ No → Espera mejor momento
  │
  ├─→ ¿Tengo 30 min?
  │   ├─ Sí → GUIA_PASO_A_PASO.md
  │   └─ No → README_OPTIMIZACION.md (10 min)
  │
  ├─→ ¿Tengo 1 hora?
  │   ├─ Sí → Lee los 6 documentos (orden arriba)
  │   └─ No → VISUALIZACION_PLAN.md + README
  │
  ├─→ EJECUTAR
  │   └─ python parameter_tuner_algo3.py --num-combinations 100
  │
  ├─→ ESPERAR (~3-4 horas)
  │
  ├─→ REVISAR RESULTADOS
  │   └─ cat optimization_results_c1/report.txt
  │
  └─→ APLICAR PARÁMETROS ÓPTIMOS
```

---

## 💡 PUNTOS CLAVE

1. **C1 es familia de prueba**: Instancias pequeñas, rápidas
2. **100 combinaciones**: Búsqueda exhaustiva pero razonable
3. **~3 horas**: Tiempo total de ejecución
4. **GAP_K + GAP_D**: Métrica a minimizar
5. **Reproducible**: Seed fijo (42) para comparabilidad

---

## ✅ CHECKLIST PRE-EJECUCIÓN

- [ ] Leí GUIA_PASO_A_PASO.md completamente
- [ ] Estoy en directorio: `GAA-VRPTW-GRASP-2`
- [ ] Existen: `best_known_solutions.json`, `parameter_tuner_algo3.py`
- [ ] Existen: `src/gaa/algorithm_generator.py`, `scripts/experiments.py`
- [ ] Tengo ~3-4 horas disponibles
- [ ] No hay programas pesados ejecutándose

---

## 📞 REFERENCIAS RÁPIDAS

**Preguntas frecuentes**: Ver **README_OPTIMIZACION.md** (sección FAQ)

**Problemas técnicos**: Ver **GUIA_PARAMETER_TUNING.md** (sección Troubleshooting)

**Cómo ejecutar paso a paso**: Ver **GUIA_PASO_A_PASO.md**

**Plan general**: Ver **PLAN_OPTIMIZACION_C1.md**

---

## 🎯 RESUMEN DE UNA LÍNEA

> Ejecuta `python parameter_tuner_algo3.py --num-combinations 100`, espera 3 horas, y obtén los parámetros óptimos del Algoritmo 3 para la familia C1.

---

**Documento generado**: 3 de Enero, 2026  
**Última actualización**: 3 de Enero, 2026  
**Estado**: ✅ Listo para usar

