# ⚡ QUICK START: run_experiments.py en 2 Minutos

**Cómo usar el script interactivo - Lo más directo posible**

---

## 🚀 Iniciar (3 pasos)

```bash
cd projects/GCP-ILS-GAA
python run_experiments.py
```

---

## 📊 Lo que ves

```
================================================================================
🎯 GENERATIVE ALGORITHM ARCHITECTURE - EXPERIMENT RUNNER
================================================================================

📊 FAMILIAS DISPONIBLES:

  1. CUL        ( 6 instancias) │ ✅ ÓPTIMO
  2. DSJ        (15 instancias) │ ❓ ABIERTA
  3. LEI        (12 instancias) │ ✅ ÓPTIMO
  4. MYC        ( 5 instancias) │ ✅ ÓPTIMO
  5. REG        (14 instancias) │ ✅ ÓPTIMO
  6. SCH        ( 2 instancias) │ ❓ ABIERTA
  7. SGB        (25 instancias) │ 📊 BKS
  8. LAT        ( 1 instancias) │ ❓ ABIERTA

────────────────────────────────────────────────────────────────────────────────

¿QUÉ DESEAS EJECUTAR?

  1. Una instancia específica
  2. Una familia COMPLETA
  3. TODAS las familias
  0. Salir

Opción: 
```

---

## 🎯 Ejemplos

### Ejemplo 1: Ejecutar una familia COMPLETA

```
Opción: 2

¿Cuál familia deseas usar?

  1. CUL        ( 6 instancias)
  2. DSJ        (15 instancias)
  3. LEI        (12 instancias)
  ...

Opción: 3
```

**Espera un momento...**

```
================================================================================
📋 FAMILY: LEI
================================================================================
Descripción: Leighton Graphs - Guaranteed chromatic number

Instancia            │ Nodes │ Edges   │ Valor │ Tipo
─────────────────────┼───────┼─────────┼───────┼──────────────────────────
le450_5a             │   450 │   5,714 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_5b             │   450 │   5,734 │     5 │ ✅ ÓPTIMO (Garantizado)
...

¿Ejecutar LEI completo? (s/n): s

================================================================================
🔬 EJECUTANDO FAMILIA COMPLETA
================================================================================
Familia:      LEI
Instancias:   12
Output Dir:   output/LEI_30_12_25_14_45
================================================================================

📊 Resumen de instancias:

  ✅ ÓPTIMOS (Garantizados):
     • le450_5a: 5 colores
     • le450_5b: 5 colores
     ...

✅ Configuración guardada en output/LEI_30_12_25_14_45/config.json

⏳ Ejecutando GAA en 12 instancias...
```

**Resultado**:
```
output/LEI_30_12_25_14_45/
├── config.json  ← Guardado automáticamente
└── results.json ← Se crearía cuando ejecute GAA
```

---

### Ejemplo 2: Ejecutar una instancia específica

```
Opción: 1

¿Cuál familia deseas usar?

  1. CUL        ( 6 instancias)
  ...

Opción: 1

¿Cuál instancia de CUL deseas usar?

  1. flat300_20_0
  2. flat300_26_0
  3. flat300_28_0
  4. flat1000_50_0
  5. flat1000_60_0
  6. flat1000_76_0
  0. Volver atrás

Opción: 1

================================================================================
🔬 EJECUTANDO EXPERIMENTO
================================================================================
Familia:      CUL
Instancia:    flat300_20_0
Nodos:        300
Aristas:      21,375
Valor Ref.:   20 (✅ ÓPTIMO)
Output Dir:   output/CUL_30_12_25_14_30
================================================================================

✅ Configuración guardada en output/CUL_30_12_25_14_30/config.json
```

**Resultado**:
```
output/CUL_30_12_25_14_30/
├── config.json  ← Guardado automáticamente
└── results.json ← Se crearía cuando ejecute GAA
```

---

### Ejemplo 3: Ejecutar TODAS las familias

```
Opción: 3

¿Ejecutar TODAS las familias? (s/n): s

================================================================================
🔬 EJECUTANDO TODAS LAS FAMILIAS
================================================================================

📂 CUL: 6 instancias
   └─ Salida: output/CUL_30_12_25_14_30

📂 DSJ: 15 instancias
   └─ Salida: output/DSJ_30_12_25_14_31

📂 LEI: 12 instancias
   └─ Salida: output/LEI_30_12_25_14_32

📂 MYC: 5 instancias
   └─ Salida: output/MYC_30_12_25_14_33

📂 REG: 14 instancias
   └─ Salida: output/REG_30_12_25_14_34

📂 SCH: 2 instancias
   └─ Salida: output/SCH_30_12_25_14_35

📂 SGB: 25 instancias
   └─ Salida: output/SGB_30_12_25_14_36

📂 LAT: 1 instancias
   └─ Salida: output/LAT_30_12_25_14_37

✅ Configuraciones guardadas para 8 familias
```

**Resultado**:
```
output/
├── CUL_30_12_25_14_30/
│   └── config.json
├── DSJ_30_12_25_14_31/
│   └── config.json
├── LEI_30_12_25_14_32/
│   └── config.json
└── ... (todas las familias)
```

---

## 📁 Estructura de Carpetas

**Lo que el script CREA automáticamente**:

```
output/                          ← Carpeta raíz (creada si no existe)
├── CUL_30_12_25_14_30/          ← FAMILY_DD_MM_YY_HH_MM
│   ├── config.json              ← Guardado automático
│   └── results.json             ← Se crea cuando ejecuta GAA
│
├── LEI_30_12_25_14_45/
│   ├── config.json
│   └── results.json
│
└── DSJ_30_12_25_14_50/
    ├── config.json
    └── results.json
```

**Formato del nombre**:
- `CUL` = Nombre de familia
- `30` = Día (30)
- `12` = Mes (Diciembre)
- `25` = Año (2025)
- `14` = Hora (14:00)
- `30` = Minuto (30)

---

## 🎯 Lo que VES en cada instancia/familia

### Símbolos de Tipo

```
✅ ÓPTIMO            → Valor garantizado matemáticamente
✅ ÓPTIMO (Garantizado) → Demostrado por teoría (como Leighton 1979)
📊 BKS               → Best Known Solution (mejor encontrado, no garantizado)
❓ ABIERTA           → Óptimo desconocido (benchmark abierto)
```

### Qué significa cada uno

**Cuando ves ✅ ÓPTIMO**:
- Si GAA lo encuentra: ✅ Perfecto
- Si no lo encuentra: Necesita mejoras

**Cuando ves 📊 BKS**:
- Si GAA lo iguala: ✅ Competitivo
- Si lo supera: 🎉 Descubrimiento nuevo

**Cuando ves ❓ ABIERTA**:
- Cualquier solución buena: 📊 Contribución
- Si supera papers: 🎉 Publicable

---

## 🚀 Uso por Línea de Comandos (si prefieres no interactivo)

```bash
# Ejecutar una familia completa
python run_experiments.py --family CUL

# Ejecutar una instancia específica
python run_experiments.py --family CUL --instance flat300_20_0

# Ejecutar todas las familias
python run_experiments.py --all
```

---

## ✅ Qué hace el script automáticamente

- [x] **Crea** carpeta `output/` si no existe
- [x] **Crea** subcarpeta con formato `FAMILY_DD_MM_YY_HH_MM`
- [x] **Guarda** `config.json` con toda la información
- [x] **Muestra** símbolos claros (✅, 📊, ❓)
- [x] **Diferencia** entre ÓPTIMO y BKS automáticamente
- [x] **Lista** todas las instancias con sus propiedades
- [x] **Permite** elegir por número (muy simple)
- [x] **Genera** resultados en la carpeta timestamped

---

## 🎓 Resumido

**Usuario aprieta:**
```
1. Número de familia (1-8)
2. Enter
3. Número de opción (ejecutar instancia/familia/todas)
4. Enter
5. Confirma (s/n si es necesario)
6. Enter
```

**Script automáticamente:**
```
✅ Crea: output/FAMILY_DD_MM_YY_HH_MM/
✅ Guarda: config.json
✅ Prepara: ejecución de GAA
✅ Muestra: símbolos de ÓPTIMO vs BKS
```

---

**¡LISTO PARA USAR!**

Próximo paso: `python run_experiments.py`
