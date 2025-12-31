# 🚀 GAA EXPERIMENT EXECUTOR - Guía de Uso

## Sistema Integrado de Ejecución de Experimentos

Este es el punto de entrada principal para toda operación con experimentos GAA. Articula de forma limpia:
- Ejecución de experimentos
- Generación de reportes
- Regeneración de reportes faltantes

---

## 📦 Scripts Principales

| Script | Responsabilidad |
|--------|-----------------|
| **execute_experiments.py** | 🎯 SCRIPT MAESTRO - Punto de entrada principal |
| run_experiments.py | Lógica de ejecución y generación de reportes |
| regenerate_reports.py | Regeneración de reportes faltantes |
| gaa_executor.py | Bridge con GAA para optimización |

---

## ▶️ Cómo Usar

### Opción 1: Modo Interactivo (Recomendado)

```bash
python execute_experiments.py
```

Proporciona un menú interactivo con opciones:
1. Ejecutar instancia específica
2. Ejecutar familia completa
3. Ejecutar todas las familias
4. Regenerar reportes faltantes
0. Salir

---

### Opción 2: Línea de Comandos (No-interactivo)

#### Ejecutar familia específica
```bash
python execute_experiments.py --family CUL
```

#### Ejecutar instancia específica
```bash
python execute_experiments.py --family CUL --instance flat300_20_0
```

#### Ejecutar todas las familias
```bash
python execute_experiments.py --all
```

#### Regenerar reportes faltantes
```bash
python execute_experiments.py --regenerate
```

---

## 📊 Estructura de Salida

Cada ejecución genera una carpeta en `output/FAMILY_DD_MM_YY_HH_MM/` con:

```
output/CUL_30_12_25_21_39/
├── config.json                 ← Configuración del experimento
├── results.json                ← Resultados brutos
├── RESULTS.md                  ← Reporte legible (Markdown)
├── analysis_report.json        ← Análisis estadístico (JSON)
└── analysis_report.csv         ← Tabla Excel-compatible
```

### Contenido de Archivos

**config.json**: Metadatos de experimento
```json
{
  "experiment": "family",
  "family": "CUL",
  "instances": 6,
  "timestamp": "2025-12-30T21:39:00.000000",
  "summary": {
    "with_optimal": 5,
    "with_bks": 0,
    "open": 1
  }
}
```

**RESULTS.md**: Tabla resumen + detalles
```markdown
# Resultados - CUL

## Resumen Ejecutivo
| Métrica | Valor |
|---------|-------|
| Instancias Ejecutadas | 6 |
| Completadas | 6 ✅ |
| Tiempo Total | 0.0001s |
```

**analysis_report.json**: Estadísticas por instancia
```json
{
  "timestamp": "...",
  "family": "CUL",
  "summary": {
    "total_instances": 6,
    "completed": 6,
    "avg_fitness": 0.9
  },
  "instances": [...]
}
```

**analysis_report.csv**: Formato tabular
```
Family,Instance,Vertices,Edges,Fitness,Iterations,Time_s,Status
CUL,flat300_20_0,300,1450,0.9000,50,0.000023,completed
```

---

## 🔄 Regeneración de Reportes

Si algunas carpetas output carecen de reportes (por interrupción o error), usa:

```bash
python execute_experiments.py --regenerate
```

O desde Python:
```python
from regenerate_reports import regenerate_missing_reports
regenerate_missing_reports()
```

---

## 🎯 Flujo de Trabajo Recomendado

### 1️⃣ Ejecución Individual (Testing)
```bash
# Probar una instancia pequeña
python execute_experiments.py --family MYC --instance myciel2
```

### 2️⃣ Ejecución Familiar (Validación)
```bash
# Ejecutar una familia completa
python execute_experiments.py --family CUL
```

### 3️⃣ Ejecución Masiva (Producción)
```bash
# Ejecutar todas las familias
python execute_experiments.py --all
```

### 4️⃣ Asegurar Integridad
```bash
# Regenerar cualquier reporte faltante
python execute_experiments.py --regenerate
```

---

## 📈 Familias Disponibles

| Familia | Instancias | Estado |
|---------|-----------|--------|
| CUL | 6 | ÓPTIMO |
| DSJ | 15 | ÓPTIMO |
| LEI | 12 | ÓPTIMO |
| MYC | 6 | ÓPTIMO |
| REG | 5 | ÓPTIMO |
| SCH | 7 | ÓPTIMO |
| GEOM | 5 | ÓPTIMO |
| IMBALANCE | 8 | ÓPTIMO |

**Total: 64 instancias**

---

## 🛠️ Scripts de Soporte (No usar directamente)

Estos scripts se usan internamente por `execute_experiments.py`:

```python
# Lógica de ejecución
from run_experiments import ExperimentRunner
runner = ExperimentRunner()
runner.run_family('CUL')

# Generación de reportes
from regenerate_reports import regenerate_missing_reports
regenerate_missing_reports()

# Análisis avanzados
from analyze_results import analyze_folder_results
from validate_verificador import validate_punto_10
```

---

## ✅ Verificación

Para verificar que todo funciona:

```bash
# Test rápido
python execute_experiments.py --family MYC

# Verificar que se generaron reportes
ls output/MYC_*/*
```

Deberías ver:
- ✅ config.json
- ✅ results.json  
- ✅ RESULTS.md
- ✅ analysis_report.json
- ✅ analysis_report.csv

---

## 🐛 Solución de Problemas

### Error: "No module named 'gaa_executor'"
```bash
# Verificar que estás en el directorio correcto
cd projects/GCP-ILS-GAA
```

### Error: "results.json no encontrado"
```bash
# Regenerar reportes
python execute_experiments.py --regenerate
```

### Carpetas output vacías
```bash
# Limpiar y regenerar
rm -r output/*
python execute_experiments.py --all
```

---

## 📝 Ejemplos Prácticos

### Ejecutar familia pequeña y ver reportes
```bash
python execute_experiments.py --family LEI
cat output/LEI_*/RESULTS.md
```

### Ejecutar todas y luego regenerar
```bash
python execute_experiments.py --all
python execute_experiments.py --regenerate
```

### Verificar una instancia específica
```bash
python execute_experiments.py --family CUL --instance flat300_20_0
cat output/CUL_*/analysis_report.csv
```

---

**Última actualización:** 2025-12-30  
**Versión:** 2.0 - Sistema Integrado
