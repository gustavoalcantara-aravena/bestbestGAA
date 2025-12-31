# 🎮 Guía de Uso: run_experiments.py

**Cómo usar el script interactivo para ejecutar experimentos de GAA con selección flexible**

---

## 🎯 ¿Qué es run_experiments.py?

Script interactivo que permite:
- ✅ Elegir qué experimentación correr (instancia, familia, todas)
- ✅ Diferenciar entre ÓPTIMO y BKS automáticamente
- ✅ Guardar resultados en carpetas con timestamp
- ✅ Ver información de cada instancia antes de ejecutar

**Ubicación**: `projects/GCP-ILS-GAA/run_experiments.py`

---

## 📁 Estructura de Carpetas de Salida

```
output/
├── CUL_30_12_25_14_30/          ← Formato: FAMILY_DD_MM_YY_HH_MM
│   ├── config.json              ← Configuración de la ejecución
│   ├── results.json             ← Resultados (si se ejecutó)
│   └── log.txt                  ← Registro de ejecución
│
├── LEI_30_12_25_14_45/
│   ├── config.json
│   ├── results.json
│   └── log.txt
│
└── DSJ_30_12_25_15_00/
    ├── config.json
    ├── results.json
    └── log.txt
```

**Explicación del nombre**:
- `CUL` = Nombre de la familia
- `30_12_25` = Día 30, Mes 12, Año 25
- `14_30` = Hora 14, Minuto 30

**Beneficio**: Fácil rastrear cuándo se ejecutó cada experimento

---

## 🚀 Modo 1: Interactivo (Recomendado para primeros usos)

### Paso 1: Iniciar el script
```bash
cd projects/GCP-ILS-GAA
python run_experiments.py
```

### Paso 2: Ver menú principal

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

────────────────────────────────────────────────────────────────────────────────

¿Qué deseas hacer?

  1. Ejecutar una instancia específica
  2. Ejecutar familia completa
  3. Ejecutar todas las familias
  0. Salir

Opción: 
```

**Símbolos mostrados**:
- ✅ ÓPTIMO = Valor garantizado matemáticamente
- 📊 BKS = Best Known Solution (no garantizado)
- ❓ ABIERTA = Óptimo desconocido

### Paso 3: Elegir opción

#### Opción 1: Una Instancia Específica

```
Opción: 1

¿Cuál familia deseas usar?

  1. CUL        ( 6 instancias)
  2. DSJ        (15 instancias)
  3. LEI        (12 instancias)
  4. MYC        ( 5 instancias)
  5. REG        (14 instancias)
  6. SCH        ( 2 instancias)
  7. SGB        (25 instancias)
  8. LAT        ( 1 instancias)
  0. Volver atrás

Opción: 1
```

**Luego ve detalles de familia**:
```
================================================================================
📋 FAMILY: CUL
================================================================================
Descripción: Culberson - Quasi-Random Coloring Problems

Instancia            │ Nodes │ Edges   │ Valor │ Tipo
─────────────────────┼───────┼─────────┼───────┼──────────────────────
flat300_20_0         │   300 │  21,375 │    20 │ ✅ ÓPTIMO
flat300_26_0         │   300 │  21,633 │    26 │ ✅ ÓPTIMO
flat300_28_0         │   300 │  21,695 │    28 │ ✅ ÓPTIMO
flat1000_50_0        │ 1,000 │ 245,000 │    50 │ ✅ ÓPTIMO
flat1000_60_0        │ 1,000 │ 245,830 │    60 │ ✅ ÓPTIMO
flat1000_76_0        │ 1,000 │ 246,708 │    76 │ ✅ ÓPTIMO

📊 Resumen:
  • Total instancias: 6
  • Con ÓPTIMO: 6
  • Con BKS: 0
  • Abiertas: 0
```

**Luego seleccionar instancia**:
```
¿Cuál instancia de CUL deseas usar?

  1. flat300_20_0
  2. flat300_26_0
  3. flat300_28_0
  4. flat1000_50_0
  5. flat1000_60_0
  6. flat1000_76_0
  0. Volver atrás

Opción: 1
```

**Luego ve confirmación de ejecución**:
```
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

⏳ Ejecutando GAA...
(Los resultados se guardarían en output/CUL_30_12_25_14_30/results.json)
```

---

#### Opción 2: Familia Completa

```
Opción: 2

¿Cuál familia deseas usar?

  1. CUL        ( 6 instancias)
  2. DSJ        (15 instancias)
  ...

Opción: 3
```

**Ve detalles de LEI**:
```
================================================================================
📋 FAMILY: LEI
================================================================================
Descripción: Leighton Graphs - Guaranteed chromatic number

Instancia            │ Nodes │ Edges   │ Valor │ Tipo
─────────────────────┼───────┼─────────┼───────┼──────────────────────────
le450_5a             │   450 │   5,714 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_5b             │   450 │   5,734 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_5c             │   450 │   9,803 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_5d             │   450 │   9,757 │     5 │ ✅ ÓPTIMO (Garantizado)
le450_15a            │   450 │   8,168 │    15 │ ✅ ÓPTIMO (Garantizado)
le450_15b            │   450 │   8,169 │    15 │ ✅ ÓPTIMO (Garantizado)
le450_15c            │   450 │  16,680 │    15 │ ✅ ÓPTIMO (Garantizado)
le450_15d            │   450 │  16,750 │    15 │ ✅ ÓPTIMO (Garantizado)
le450_25a            │   450 │   8,260 │    25 │ ✅ ÓPTIMO (Garantizado)
le450_25b            │   450 │   8,263 │    25 │ ✅ ÓPTIMO (Garantizado)
le450_25c            │   450 │  17,343 │    25 │ ✅ ÓPTIMO (Garantizado)
le450_25d            │   450 │  17,425 │    25 │ ✅ ÓPTIMO (Garantizado)

📊 Resumen:
  • Total instancias: 12
  • Con ÓPTIMO: 12
  • Con BKS: 0
  • Abiertas: 0
```

**Confirmación**:
```
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
     • le450_5c: 5 colores
     • le450_5d: 5 colores
     • le450_15a: 15 colores
     • le450_15b: 15 colores
     • le450_15c: 15 colores
     • le450_15d: 15 colores
     • le450_25a: 25 colores
     • le450_25b: 25 colores
     • le450_25c: 25 colores
     • le450_25d: 25 colores

✅ Configuración guardada en output/LEI_30_12_25_14_45/config.json

⏳ Ejecutando GAA en 12 instancias...
(Los resultados se guardarían en output/LEI_30_12_25_14_45/results.json)
```

---

#### Opción 3: Todas las Familias

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

⏳ Ejecutando GAA en todas las familias...
```

---

## 🚀 Modo 2: Línea de Comandos (Para automatización)

Si prefieres ejecutar directamente sin menú:

### Ejecutar una familia completa
```bash
python run_experiments.py --family CUL
```

**Output**:
```
================================================================================
📋 FAMILY: CUL
================================================================================
[Detalles de la familia...]

================================================================================
🔬 EJECUTANDO FAMILIA COMPLETA
================================================================================
[Ejecución...]
```

### Ejecutar una instancia específica
```bash
python run_experiments.py --family CUL --instance flat300_20_0
```

### Ejecutar todas las familias
```bash
python run_experiments.py --all
```

---

## 📊 Archivo config.json Generado

Cada ejecución genera un `config.json` con los detalles:

**Para una instancia**:
```json
{
  "experiment": "single_instance",
  "family": "CUL",
  "instance": "flat300_20_0",
  "timestamp": "2025-12-30T14:30:45.123456",
  "reference": {
    "value": 20,
    "type": "✅ ÓPTIMO",
    "nodes": 300,
    "edges": 21375
  }
}
```

**Para una familia**:
```json
{
  "experiment": "family",
  "family": "LEI",
  "instances": 12,
  "timestamp": "2025-12-30T14:45:12.654321",
  "instances_detail": {
    "le450_5a": {
      "value": 5,
      "type": "✅ ÓPTIMO (Garantizado)",
      "nodes": 450,
      "edges": 5714
    },
    ...
  },
  "summary": {
    "with_optimal": 12,
    "with_bks": 0,
    "open": 0
  }
}
```

---

## 🎯 Casos de Uso

### Caso 1: Validar que GAA funciona

```bash
# Ejecutar familia con ÓPTIMO conocido
python run_experiments.py --family LEI

# Resultado esperado:
# ✅ Si GAA encuentra ÓPTIMO en >80% → Funciona correctamente
# ⚠️ Si no → Revisar parámetros
```

### Caso 2: Comparar contra BKS

```bash
# Ejecutar familia con BKS
python run_experiments.py --family SGB

# Resultado esperado:
# ✅ Si iguala BKS → Competitivo
# 🎉 Si mejora BKS → Descubrimiento
```

### Caso 3: Explorar instancias abiertas

```bash
# Ejecutar familia abierta
python run_experiments.py --family DSJ

# Resultado esperado:
# 📊 Cualquier solución buena → Contribución
# 🎉 Superar papers → Publicable
```

### Caso 4: Prueba rápida de una instancia

```bash
# Una instancia específica para quick test
python run_experiments.py --family CUL --instance flat300_20_0
```

### Caso 5: Lote completo de ejecuciones

```bash
# Ejecutar todas las familias overnight
python run_experiments.py --all
# Cada familia genera su carpeta timestamped
```

---

## 📝 Cómo Interpretar la Salida

### Símbolos de Tipo de Valor

| Símbolo | Significado | Interpretación |
|---------|-----------|---|
| ✅ ÓPTIMO | Garantizado matemáticamente | Si GAA lo iguala: perfecto ✅ |
| ✅ ÓPTIMO (Garantizado) | Demostrado por teoría (Leighton) | Muy valioso para validación |
| 📊 BKS | Mejor conocido (no garantizado) | Si lo iguala: competitivo ✅ |
| ❓ ABIERTA | Óptimo desconocido | Cualquier solución buena es contribución |

### Resumen de Familia

```
📊 Resumen:
  • Total instancias: 6
  • Con ÓPTIMO: 6        ← Todas tienen ÓPTIMO garantizado
  • Con BKS: 0
  • Abiertas: 0

Interpretación:
  → Esta familia es ideal para VALIDAR que GAA funciona
  → Si GAA encuentra ÓPTIMO en >80%: ✅ Excelente
```

---

## ⏱️ Formato de Timestamp

El timestamp en la carpeta es: `DD_MM_YY_HH_MM`

```
Ejemplo: CUL_30_12_25_14_30
├─ 30    = Día 30
├─ 12    = Mes 12 (Diciembre)
├─ 25    = Año 25 (2025)
├─ 14    = Hora 14 (2 PM)
└─ 30    = Minuto 30

Beneficios:
  ✅ Fácil de leer (casi como ISO 8601)
  ✅ Ordenable alfabéticamente
  ✅ Compatible con Windows/Linux
  ✅ Permite múltiples ejecuciones del mismo día
```

---

## 🔍 Entender Datos de Referencia

### Cómo el script obtiene ÓPTIMO vs BKS

```
Lee de: datasets/BKS.json

Para cada instancia:
  "value": 20          ← El número
  "optimal": true      ← ¿Es óptimo?
  "guaranteed": true   ← ¿Garantizado por teoría?
  "open": false        ← ¿Abierto/desconocido?

Script determina:
  Si optimal=true y guaranteed=true:
    → ✅ ÓPTIMO (Garantizado)
  
  Si optimal=true y guaranteed=false:
    → ✅ ÓPTIMO
  
  Si optimal=false:
    → 📊 BKS
  
  Si open=true y value=null:
    → ❓ ABIERTA
```

---

## 💾 Archivos Generados

Después de cada ejecución:

```
output/FAMILY_DD_MM_YY_HH_MM/
├── config.json         ← Configuración (siempre creado)
├── results.json        ← Resultados de GAA (cuando se ejecute)
└── log.txt            ← Registro de ejecución (cuando se ejecute)
```

---

## 🎓 Flujo Recomendado de Ejecuciones

### Día 1: Validar
```bash
# Ejecutar familias con ÓPTIMO para validar setup
python run_experiments.py --family LEI
python run_experiments.py --family CUL
python run_experiments.py --family REG

# Resultado esperado: >80% óptimos encontrados
# Si se cumple: ✅ GAA funciona correctamente
```

### Día 2: Comparar
```bash
# Ejecutar familias con BKS
python run_experiments.py --family SGB

# Resultado esperado: Iguala o mejora BKS
# Si mejora: 🎉 Descubrimiento
```

### Día 3: Explorar
```bash
# Ejecutar familias abiertas (largo puede tomar tiempo)
python run_experiments.py --family DSJ
python run_experiments.py --family SCH

# Resultado esperado: Soluciones competitivas
# Si supera papers recientes: 🏆 Publicable
```

---

## 🚨 Problemas Comunes

**P: No se ve el menú interactivo**
```bash
# Asegúrate de estar en el directorio correcto
cd projects/GCP-ILS-GAA
python run_experiments.py
```

**P: Dice "Opción inválida"**
```
# Ingresa un número del 0 al 3
Opción: 2  ✅ (válido)
# NO: dos (❌) o 2.5 (❌)
```

**P: No encuentro los resultados**
```bash
# Busca en la carpeta output/ con el timestamp
ls -la output/

# Ejemplo:
# CUL_30_12_25_14_30/    ← Aquí están los resultados
# LEI_30_12_25_14_45/
# DSJ_30_12_25_14_50/
```

**P: ¿Puedo ejecutar múltiples familias en paralelo?**
```bash
# Sí, cada una genera su carpeta unique con timestamp
# Ejecuta en diferentes terminales:
Terminal 1: python run_experiments.py --family CUL
Terminal 2: python run_experiments.py --family LEI
Terminal 3: python run_experiments.py --family DSJ

# Cada una genera:
# output/CUL_30_12_25_14_30/
# output/LEI_30_12_25_14_31/
# output/DSJ_30_12_25_14_32/
```

---

## ✅ Checklist de Uso

- [ ] Ubicarme en: `projects/GCP-ILS-GAA/`
- [ ] Ejecutar: `python run_experiments.py`
- [ ] Ver menú con familias y tipos (✅, 📊, ❓)
- [ ] Entender diferencia ÓPTIMO vs BKS
- [ ] Elegir qué ejecutar (instancia, familia, todas)
- [ ] Ver detalles de instancias antes de ejecutar
- [ ] Confirmar ejecución
- [ ] Encontrar resultados en `output/FAMILY_timestamp/`
- [ ] Revisar `config.json` para confirmar configuración
- [ ] Usar `compare_with_bks.py` en resultados (próximo paso)

---

## 🎓 Conclusión

`run_experiments.py` te permite:

1. ✅ **Elegir** qué experimentación correr fácilmente
2. ✅ **Ver** diferencia entre ÓPTIMO y BKS
3. ✅ **Organizar** resultados con timestamps
4. ✅ **Documentar** cada ejecución en config.json
5. ✅ **Escalar** desde una instancia hasta todas las familias

**Próximo paso**: Después de ejecutar, usa `compare_with_bks.py` para analizar resultados contra literatura.

```bash
# Ejemplo flujo completo:
python run_experiments.py --family CUL      # Ejecuta
python compare_with_bks.py --results-dir output/CUL_*/  # Analiza
```
