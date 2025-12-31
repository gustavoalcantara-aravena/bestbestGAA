# 🎯 Resumen: Script Interactivo de Experimentación

**Lo que se acaba de crear: Sistema completo para elegir y ejecutar experimentos con diferenciación de ÓPTIMO vs BKS**

---

## ✅ Lo Que Se Implementó

### 1. **run_experiments.py** - Script Interactivo Principal

📍 Ubicación: `projects/GCP-ILS-GAA/run_experiments.py`

**Características**:
```
✅ Menú interactivo con 3 opciones principales
✅ Seleccionar instancia individual
✅ Seleccionar familia completa
✅ Seleccionar todas las familias
✅ Detalles de cada instancia (nodes, edges, valor ref)
✅ Indicadores claros de ÓPTIMO vs BKS vs ABIERTA
✅ Carpetas output con timestamp automático
✅ Archivo config.json para cada ejecución
✅ Modo línea de comandos para automatización
✅ Interfaz amigable con colores y símbolos
```

**Uso Básico**:
```bash
cd projects/GCP-ILS-GAA
python run_experiments.py
```

---

### 2. **OPTIMO_vs_BKS.md** - Guía Conceptual

📍 Ubicación: `projects/GCP-ILS-GAA/OPTIMO_vs_BKS.md`

**Contenido** (800+ líneas):
- ✅ Diferencia fundamental entre ÓPTIMO y BKS
- 📊 Cómo interpretar cada tipo
- 🎯 Matriz de familias (cuál tiene qué)
- 💡 Ejemplos reales con interpretación
- 📈 Estrategia de pruebas recomendada
- 🎓 Checklist de comprensión

**Clave**: Explica POR QUÉ cada familia es importante

---

### 3. **GUIA_RUN_EXPERIMENTS.md** - Manual de Uso

📍 Ubicación: `projects/GCP-ILS-GAA/GUIA_RUN_EXPERIMENTS.md`

**Contenido** (700+ líneas):
- 🚀 Modo interactivo step-by-step
- 🚀 Modo línea de comandos
- 📁 Estructura de carpetas output
- 💾 Formato de timestamp explicado
- 🎯 Casos de uso prácticos
- 🚨 Problemas comunes y soluciones
- ✅ Checklist de uso

**Clave**: Explica CÓMO usar el script

---

## 🎯 Flujo de Uso Esperado

```
┌─────────────────────────────────────────┐
│ 1. Usuario ejecuta run_experiments.py   │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │  Menú Interactivo:   │
        │  1. Una instancia    │
        │  2. Una familia      │
        │  3. Todas            │
        └────────┬─────────────┘
                 │
        ┌────────┴────────┬─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   ┌─────────┐    ┌─────────────┐    ┌──────────────┐
   │ CUL: 6  │    │ LEI: 12     │    │ DSJ: 15 (❓) │
   │ ✅ OPT  │    │ ✅ OPT GUAR │    │ ABIERTA      │
   └────┬────┘    └──────┬──────┘    └───────┬──────┘
        │                │                   │
        ▼                ▼                   ▼
    Elige instancia  Ejecuta 12       Ejecuta 15
                     instancias        instancias
        │                │                   │
        └────────────────┼───────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │ Crear carpeta:                       │
        │ output/FAMILY_DD_MM_YY_HH_MM/       │
        │                                      │
        │ Ejemplo:                             │
        │ output/CUL_30_12_25_14_30/           │
        └────────────────┬─────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │ Guardar config.json con:             │
        │ • Familia                            │
        │ • Instancias seleccionadas           │
        │ • Valores de referencia              │
        │ • Timestamp                          │
        └────────────────┬─────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │ [Si se ejecuta GAA]                  │
        │ Guardar results.json                 │
        └──────────────────────────────────────┘
```

---

## 🗂️ Estructura de Carpetas

```
projects/GCP-ILS-GAA/
├── run_experiments.py              ← NUEVO: Script principal
│
├── OPTIMO_vs_BKS.md                ← NUEVO: Guía conceptual
├── GUIA_RUN_EXPERIMENTS.md         ← NUEVO: Manual de uso
│
├── datasets/
│   ├── BKS.json                    ← Datos de referencia
│   ├── CUL/                        ← 6 instancias ✅
│   ├── LEI/                        ← 12 instancias ✅
│   ├── REG/                        ← 14 instancias ✅
│   ├── DSJ/                        ← 15 instancias ❓
│   ├── MYC/                        ← 5 instancias ✅
│   ├── SGB/                        ← 25 instancias 📊
│   ├── SCH/                        ← 2 instancias ❓
│   └── LAT/                        ← 1 instancia ❓
│
└── output/                         ← Resultados (generado)
    ├── CUL_30_12_25_14_30/
    │   ├── config.json
    │   └── results.json (si ejecuta)
    ├── LEI_30_12_25_14_45/
    │   ├── config.json
    │   └── results.json
    └── DSJ_30_12_25_14_50/
        ├── config.json
        └── results.json
```

---

## 🎯 Características Principales

### Característica 1: Menú Interactivo Visual

```
================================================================================
🎯 GENERATIVE ALGORITHM ARCHITECTURE - EXPERIMENT RUNNER
================================================================================

📊 Familias de instancias disponibles:

  1. CUL        ( 6 instancias) | ✅ ÓPTIMO | 
  2. DSJ        (15 instancias) | ❓ ABIERTA
  3. LEI        (12 instancias) | ✅ ÓPTIMO | 
  4. MYC        ( 5 instancias) | ✅ ÓPTIMO | 
  5. REG        (14 instancias) | ✅ ÓPTIMO | 
  6. SCH        ( 2 instancias) | ❓ ABIERTA
  7. SGB        (25 instancias) | 📊 BKS
  8. LAT        ( 1 instancias) | ❓ ABIERTA
```

**Beneficio**: Ves de un vistazo qué familias tienen ÓPTIMO vs BKS vs ABIERTAS

---

### Característica 2: Detalles por Instancia

```
================================================================================
📋 FAMILY: LEI
================================================================================
Descripción: Leighton Graphs - Guaranteed chromatic number

Instancia            │ Nodes │ Edges   │ Valor │ Tipo
─────────────────────┼───────┼─────────┼───────┼──────────────────────────
le450_5a             │   450 │   5,714 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_5b             │   450 │   5,734 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_15a            │   450 │   8,168 │    15 │ ✅ ÓPTIMO (Garantizado)
le450_25d            │   450 │  17,425 │    25 │ ✅ ÓPTIMO (Garantizado)
```

**Beneficio**: Antes de ejecutar, ves exactamente qué vas a probar

---

### Característica 3: Timestamps Automáticos

```
Carpeta: output/CUL_30_12_25_14_30/
         └─ FAMILY_DD_MM_YY_HH_MM

Beneficios:
  ✅ Cada ejecución tiene su carpeta única
  ✅ Fácil de leer (30 de Diciembre, 2025, 14:30)
  ✅ Compatible con Windows/Linux
  ✅ Permite múltiples ejecuciones del mismo día
  ✅ Ordenable alfabéticamente
```

---

### Característica 4: Diferenciación Automática

El script diferencia automáticamente:

```
De: datasets/BKS.json

Lee propiedades de cada instancia:
├─ optimal = true + guaranteed = true
│  └─ Muestra: ✅ ÓPTIMO (Garantizado)
│
├─ optimal = true + guaranteed = false
│  └─ Muestra: ✅ ÓPTIMO
│
├─ optimal = false (y tiene valor)
│  └─ Muestra: 📊 BKS
│
└─ open = true (no tiene valor)
   └─ Muestra: ❓ ABIERTA
```

---

## 📊 Distrib ución de Instancias

```
Total: 81 instancias

✅ CON ÓPTIMO GARANTIZADO:  37 instancias (45.7%)
   └─ LEI (12) + CUL (6) + REG (14) + MYC (5)
   └─ Ideales para VALIDAR que GAA funciona

📊 CON BKS (no garantizado):  18 instancias (22.2%)
   └─ SGB (18)
   └─ Ideales para COMPARAR vs literatura

❓ INSTANCIAS ABIERTAS:  26 instancias (32.1%)
   └─ DSJ (15) + SCH (2) + LAT (1) + SGB (7)
   └─ Ideales para EXPLORAR y descubrir
```

---

## 🚀 Cómo Usar - Rápido

### Opción A: Menú Interactivo (Recomendado)
```bash
python run_experiments.py
# Aparece menú, eliges qué ejecutar
```

### Opción B: Línea de Comandos (Automatización)
```bash
# Una familia
python run_experiments.py --family CUL

# Una instancia
python run_experiments.py --family CUL --instance flat300_20_0

# Todas
python run_experiments.py --all
```

---

## 📋 Resumen de Archivos Creados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| **run_experiments.py** | 450 | Script interactivo principal |
| **OPTIMO_vs_BKS.md** | 800+ | Guía conceptual de diferencias |
| **GUIA_RUN_EXPERIMENTS.md** | 700+ | Manual de uso completo |
| **RESUMEN_SCRIPT_INTERACTIVO.md** | Este | Resumen ejecutivo |

**Total**: 3 archivos nuevos + documentación actualizada

---

## 🎓 Aprendizaje del Usuario

Después de usar este sistema, el usuario entenderá:

1. ✅ Qué es ÓPTIMO (garantizado, el mejor posible)
2. 📊 Qué es BKS (mejor conocido, podría no ser óptimo)
3. ❓ Qué es ABIERTA (óptimo desconocido, oportunidad)
4. 🎯 Cuál familia usar para qué objetivo
5. 📁 Cómo se organizan resultados con timestamps
6. 🚀 Cómo automatizar ejecuciones
7. 💡 Por qué cada familia importa para validación

---

## 🎯 Casos de Uso

### Caso 1: Validar Setup de GAA
```bash
# Ejecutar familia con ÓPTIMO garantizado
python run_experiments.py --family LEI

# Si GAA encuentra ÓPTIMO en >80%:
# ✅ Setup funciona correctamente
```

### Caso 2: Prueba Rápida
```bash
# Una instancia específica
python run_experiments.py --family CUL --instance flat300_20_0

# Resultado rápido (1-5 minutos)
# Confirma que sistema funciona
```

### Caso 3: Comparación vs Literatura
```bash
# Ejecutar familia con BKS
python run_experiments.py --family SGB

# Analizar:
# python compare_with_bks.py --results-dir output/SGB_*/
```

### Caso 4: Descubrir Algo Nuevo
```bash
# Ejecutar familia abierta (puede tomar tiempo)
python run_experiments.py --family DSJ

# Si encuentra soluciones mejores que papers:
# 🎉 Potencial publicación
```

### Caso 5: Estudio Exhaustivo
```bash
# Ejecutar todas
python run_experiments.py --all

# Después de varias horas:
# 81 instancias testeadas
# Análisis completo vs estado del arte
```

---

## 💾 Lo Que Se Guarda

### Cada ejecución genera:

```
output/FAMILY_DD_MM_YY_HH_MM/
├── config.json    ← Configuración
│   {
│     "experiment": "family",
│     "family": "CUL",
│     "instances": 6,
│     "timestamp": "2025-12-30T14:30:45",
│     "instances_detail": {...},
│     "summary": {
│       "with_optimal": 6,
│       "with_bks": 0,
│       "open": 0
│     }
│   }
│
└── results.json   ← Resultados (si ejecuta)
    {
      "flat300_20_0": 20,
      "flat300_26_0": 26,
      ...
    }
```

**Beneficio**: 
- ✅ Fácil rastrear qué se ejecutó
- ✅ Múltiples ejecuciones sin conflictos
- ✅ Historial completo de experimentos

---

## 🔄 Flujo Completo Recomendado

```
DÍA 1: VALIDAR
├─ python run_experiments.py --family LEI
├─ python run_experiments.py --family CUL
└─ python run_experiments.py --family REG
   └─ Resultado esperado: >80% óptimos ✅

DÍA 2: COMPARAR
├─ python run_experiments.py --family SGB
└─ python compare_with_bks.py --results-dir output/SGB_*/
   └─ Resultado esperado: Iguala o mejora BKS

DÍA 3: EXPLORAR
├─ python run_experiments.py --family DSJ (puede tardar)
└─ Resultado esperado: Soluciones competitivas 📊
   └─ Si supera papers: Publicable 🎉

DÍA 4-5: ANÁLISIS GLOBAL
└─ python run_experiments.py --all
   └─ Ejecuta todas las 81 instancias
```

---

## ✅ Checklist: Listo para Usar

- [x] Script `run_experiments.py` creado
- [x] Interfaz interactiva implementada
- [x] Modo línea de comandos implementado
- [x] Timestamps automáticos por ejecución
- [x] Diferenciación ÓPTIMO vs BKS vs ABIERTA
- [x] Documentación conceptual (OPTIMO_vs_BKS.md)
- [x] Manual de uso (GUIA_RUN_EXPERIMENTS.md)
- [x] Ejemplos de ejecución
- [x] Casos de uso prácticos
- [x] Integración con BKS.json
- [x] Carpetas output organizadas
- [x] Config.json por ejecución

---

## 🎓 Conclusión

Se ha creado un **sistema completo e integrado** que permite:

1. ✅ **Elegir** qué experimentación correr (instancia, familia, todas)
2. ✅ **Entender** la diferencia entre ÓPTIMO y BKS
3. ✅ **Organizar** resultados con timestamps únicos
4. ✅ **Documentar** cada ejecución automáticamente
5. ✅ **Escalar** desde pruebas rápidas hasta lotes exhaustivos
6. ✅ **Analizar** resultados contra literatura (con compare_with_bks.py)

**Status**: ✅ **LISTO PARA USAR EN PRODUCCIÓN**

**Próximo paso**: Ejecuta `python run_experiments.py` y comienza con validación en LEI familia.
