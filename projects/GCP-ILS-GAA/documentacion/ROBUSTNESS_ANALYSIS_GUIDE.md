# 📊 Análisis de Robustez - Múltiples Ejecuciones

## ¿Qué es?

Permite ejecutar el MISMO experimento varias veces para medir la **robustez y estabilidad** del algoritmo GAA.

---

## ¿Cómo Usar?

### Opción 1: Línea de Comandos

```bash
# Ejecutar una instancia 5 veces
python main.py --family CUL --instance flat300_20_0 --runs 5

# Ejecutar una familia completa 3 veces
python main.py --family CUL --runs 3

# Ejecutar TODAS las familias 2 veces
python main.py --all --runs 2
```

### Opción 2: Modo Interactivo

```bash
python main.py

# Selecciona opción 1, 2 o 3
# Te pide: "¿Cuántas ejecuciones? (default 1)"
# Ingresa: 5
# Se ejecuta 5 veces automáticamente
```

---

## Salida Esperada

Cuando ejecutas con `--runs 5`:

```
================================================================================
📄 Generando documentación en: CUL_30_12_25_21_50/
================================================================================

   ✅ RESULTS.md (6 instancias x 5 ejecuciones = 30 resultados)
   ✅ analysis_report.json
   ✅ analysis_report.csv
   ✅ COMPARISON_GAP_ANALYSIS.json
   ✅ COMPARISON_GAP_ANALYSIS.csv
   ✅ validation_report.json
   ✅ EXECUTIVE_SUMMARY.md
   ✅ ROBUSTNESS_ANALYSIS.json       ← NUEVO
   ✅ ROBUSTNESS_ANALYSIS.csv         ← NUEVO
   ✅ ROBUSTNESS_ANALYSIS.md          ← NUEVO

✅ Documentación generada completamente
```

---

## Archivos de Robustez Generados

### 1. **ROBUSTNESS_ANALYSIS.json**

Contiene estadísticas de todas las ejecuciones:

```json
{
  "num_runs": 5,
  "instances": {
    "flat300_20_0": {
      "fitness": {
        "mean": 0.9200,
        "min": 0.9000,
        "max": 0.9500,
        "stdev": 0.0184,
        "all_values": [0.9000, 0.9200, 0.9150, 0.9500, 0.9200]
      },
      "iterations": {
        "mean": 45.0,
        "min": 40,
        "max": 50,
        "all_values": [40, 45, 42, 50, 48]
      },
      "time": {
        "mean": 0.000021,
        "min": 0.000015,
        "max": 0.000028,
        "all_values": [0.000015, 0.000021, 0.000018, 0.000028, 0.000022]
      }
    }
  }
}
```

### 2. **ROBUSTNESS_ANALYSIS.csv**

Tabla Excel-compatible:

```
Instance,Fitness_Mean,Fitness_Min,Fitness_Max,Fitness_StDev,Iterations_Mean,Iterations_Min,Iterations_Max,Time_Mean,Time_Min,Time_Max
flat300_20_0,0.9200,0.9000,0.9500,0.0184,45.0,40,50,0.000021,0.000015,0.000028
flat300_26_0,0.9150,0.8950,0.9350,0.0142,43.0,40,48,0.000019,0.000014,0.000025
```

### 3. **ROBUSTNESS_ANALYSIS.md**

Reporte legible:

```markdown
# 📊 Análisis de Robustez

**Número de ejecuciones:** 5

## Estadísticas por Instancia

### flat300_20_0

**Fitness:**
- Media: 0.9200
- Min: 0.9000
- Max: 0.9500
- Desv. Est.: 0.0184

**Iteraciones:**
- Media: 45.0
- Min: 40
- Max: 50

**Tiempo (segundos):**
- Media: 0.000021
- Min: 0.000015
- Max: 0.000028
```

---

## Interpretación

### Fitness Robustness (Desv. Estándar)

```
Stdev < 0.01    → Muy robusto ✅
0.01 < Stdev < 0.05  → Robusto
Stdev > 0.05    → Poco robusto ⚠️
```

### Variabilidad de Tiempo

```
Diferencia < 10%    → Eficiente y estable
Diferencia > 50%    → Inestable (revisar)
```

---

## Ejemplos Prácticos

### Analizar Robustez de una Instancia

```bash
python main.py --family MYC --instance myciel2 --runs 10
```

Genera: `output/MYC_DD_MM_YY_HH_MM/`
- 10 ejecuciones de la misma instancia
- ROBUSTNESS_ANALYSIS.json con estadísticas
- CSV para Excel
- Markdown para lectura rápida

### Comparar Robustez Entre Familias

```bash
python main.py --family CUL --runs 5
python main.py --family MYC --runs 5
```

Compara:
- Desv. estándar de fitness
- Consistencia de iteraciones
- Variabilidad de tiempo

### Validación de Producción

```bash
python main.py --all --runs 3
```

- 3 ejecuciones de TODAS las instancias
- Garantiza comportamiento consistente
- Genera reporte de robustez global

---

## Datos Almacenados

Cuando ejecutas con `--runs N`:

1. **Se ejecuta N veces** la misma instancia/familia
2. **Se guardan N resultados** en `results.json`
3. **Se calculan estadísticas** (media, min, max, stdev)
4. **Se generan reportes** de robustez

**Ejemplo:** `--runs 5` para familia CUL (6 instancias)
- Total: 6 × 5 = 30 ejecuciones
- 30 resultados en `results.json`
- Estadísticas para cada una de las 6 instancias

---

## Casos de Uso

### 1. Validación de Algoritmo
```bash
python main.py --family LEI --runs 20
# Valida consistencia en 20 ejecuciones
```

### 2. Comparación de Performance
```bash
python main.py --family CUL --runs 5
python main.py --family DSJ --runs 5
# Compara robustez entre familias
```

### 3. Análisis de Sensibilidad
```bash
python main.py --family MYC --instance myciel3 --runs 50
# Analiza variabilidad en 50 ejecuciones
```

### 4. Reporte de Robustez
```bash
python main.py --all --runs 3
# Genera reporte completo de robustez
# Ideal para presentaciones
```

---

## Interpretación de Resultados

### Excelente (Stdev < 0.005)
```json
"fitness": {
  "mean": 20.0,
  "stdev": 0.002,
  "min": 19.99,
  "max": 20.01
}
// Algoritmo es muy consistente
```

### Bueno (Stdev 0.005 - 0.05)
```json
"fitness": {
  "mean": 20.1,
  "stdev": 0.03,
  "min": 20.0,
  "max": 20.2
}
// Ligeras variaciones normales
```

### Revisar (Stdev > 0.05)
```json
"fitness": {
  "mean": 20.3,
  "stdev": 0.12,
  "min": 20.0,
  "max": 20.8
}
// Mucha variabilidad - revisar parámetros
```

---

## Archivos en output/FAMILY_TIMESTAMP/

Con múltiples runs:

```
output/CUL_30_12_25_21_50/
├── config.json
├── results.json                    (30 resultados = 6 instancias × 5 runs)
├── RESULTS.md
├── analysis_report.json
├── analysis_report.csv
├── COMPARISON_GAP_ANALYSIS.json
├── COMPARISON_GAP_ANALYSIS.csv
├── validation_report.json
├── EXECUTIVE_SUMMARY.md
├── ROBUSTNESS_ANALYSIS.json        ← Estadísticas de robustez
├── ROBUSTNESS_ANALYSIS.csv         ← CSV para Excel
└── ROBUSTNESS_ANALYSIS.md          ← Reporte legible
```

**11 archivos totales (vs 9 sin robustness)**

---

**Recomendación:** Usa `--runs 5` o más para validaciones críticas. Mínimo 3 runs para obtener desviación estándar significativa.
