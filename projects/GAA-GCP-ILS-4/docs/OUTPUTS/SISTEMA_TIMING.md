# ⏱️ SISTEMA DE TIMING - run_full_experiment.py

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025  
**Script**: `scripts/run_full_experiment.py`

---

## 📋 DESCRIPCIÓN

Se ha implementado un sistema completo de timing que registra y documenta cuánto tiempo se demora cada etapa de la ejecución del experimento.

---

## 🎯 CARACTERÍSTICAS

### 1. **Clase TimingTracker**
Registra automáticamente el tiempo de cada etapa:
- Carga de datasets
- Ejecución de ILS
- Guardado de resultados
- Generación de gráficas

### 2. **Información en Pantalla**
Muestra tiempos en tiempo real mientras se ejecuta:
- Tiempo de cada etapa
- Porcentaje del tiempo total
- Gráfica de barras visual

### 3. **Documentación Automática**
Guarda reportes de timing en la carpeta de output:
- `timing_report.txt` - Reporte legible
- `timing_report.json` - Datos estructurados

---

## 📊 ETAPAS REGISTRADAS

El sistema registra automáticamente 4 etapas principales:

| Etapa | Descripción |
|-------|------------|
| **Carga de datasets** | Tiempo para cargar los 79 datasets DIMACS |
| **Ejecución de ILS** | Tiempo total de ejecución del algoritmo ILS |
| **Guardado de resultados** | Tiempo para guardar CSV, JSON, TXT, .sol |
| **Generación de gráficas** | Tiempo para generar gráficas PNG |

---

## 📺 EJEMPLO DE OUTPUT EN PANTALLA

### 1️⃣ Tiempo de Carga
```
📂 CARGANDO DATASETS
--------------------------------------------------------------------------------
✅ 79 datasets cargados

⏱️  Tiempo de carga: 2.45s
```

### 2️⃣ Ejecución de ILS
```
================================================================================
🔬 EXPERIMENTO COMPLETO: ILS EN 79 INSTANCIAS
================================================================================
⏱️  Tiempo máximo por instancia: 300.0s
🔄 Réplicas por instancia: 1
🌱 Semilla: 42
================================================================================

[  1/ 79] (  0.0%) myciel3
   📊 Vértices:   11 | Aristas:     20 | BKS: 4
   Réplica 1/1: 4 colores (0 conflictos) ✓ 0.15s (0.0%)
   📈 Resumen: 4 colores (mejor), 4.0±0.0 (promedio), 1/1 factibles

... (77 instancias más) ...

================================================================================
✅ EJECUCIÓN DE ILS COMPLETADA
================================================================================
⏱️  Tiempo total: 20.75m (1245.3s)
📊 Instancias procesadas: 79
🔄 Réplicas por instancia: 1
📈 Tiempo promedio por instancia: 15.76s
================================================================================
```

### 3️⃣ Guardado de Resultados
```
================================================================================
💾 GUARDANDO RESULTADOS
================================================================================
✅ CSV: summary.csv
✅ JSON: detailed_results.json
✅ TXT: statistics.txt
✅ SOL: myciel3_31-12-25_20-30-45.sol
... (78 soluciones más) ...
✅ TIMING: timing_report.txt
✅ TIMING JSON: timing_report.json

⏱️  Tiempo de guardado: 3.21s
```

### 4️⃣ Generación de Gráficas
```
================================================================================
📊 GENERANDO GRÁFICAS
================================================================================
✅ Gráfica de convergencia generada
✅ Gráfica de escalabilidad generada
================================================================================
✅ PROCESO COMPLETADO
================================================================================
⏱️  Tiempo de generación de gráficas: 1.85s
📁 Resultados guardados en: output/results/all_datasets/31-12-25_20-30-45
================================================================================

⏱️  RESUMEN DE TIEMPOS POR ETAPA
--------------------------------------------------------------------------------
Ejecución de ILS                1245.30s             ████████████████████ 98.2%
Guardado de resultados             3.21s             ░░░░░░░░░░░░░░░░░░░░  0.3%
Generación de gráficas             1.85s             ░░░░░░░░░░░░░░░░░░░░  0.1%
Carga de datasets                   2.45s             ░░░░░░░░░░░░░░░░░░░░  0.2%
--------------------------------------------------------------------------------
TIEMPO TOTAL                    1252.81s
================================================================================
```

---

## 📁 ARCHIVOS GENERADOS

### timing_report.txt
Reporte legible con desglose de tiempos:

```
REPORTE DE TIEMPOS DE EJECUCIÓN
================================================================================

RESUMEN GENERAL:
--------------------------------------------------------------------------------
Tiempo total: 20.88m (1252.81s)

DESGLOSE POR ETAPA:
--------------------------------------------------------------------------------
Etapa                          Tiempo               % Total
--------------------------------------------------------------------------------
Ejecución de ILS               20.75m (1245.3s)      98.2%
Guardado de resultados         3.21s                  0.3%
Generación de gráficas         1.85s                  0.1%
Carga de datasets              2.45s                  0.2%

================================================================================
```

### timing_report.json
Datos estructurados para análisis:

```json
{
  "total_time_seconds": 1252.81,
  "total_time_formatted": "20.88m (1252.81s)",
  "stages": {
    "Carga de datasets": {
      "seconds": 2.45,
      "formatted": "2.45s",
      "percentage": 0.2
    },
    "Ejecución de ILS": {
      "seconds": 1245.3,
      "formatted": "20.75m (1245.3s)",
      "percentage": 98.2
    },
    "Guardado de resultados": {
      "seconds": 3.21,
      "formatted": "3.21s",
      "percentage": 0.3
    },
    "Generación de gráficas": {
      "seconds": 1.85,
      "formatted": "1.85s",
      "percentage": 0.1
    }
  }
}
```

---

## 🎯 CÓMO FUNCIONA

### 1. Inicialización
```python
self.timing = TimingTracker()
```

### 2. Inicio de Etapa
```python
self.timing.start_stage("Carga de datasets")
# ... código de la etapa ...
load_time = self.timing.end_stage()
```

### 3. Obtener Tiempo Formateado
```python
formatted = self.timing.format_time(seconds)
# Resultado: "20.75m (1245.3s)" o "2.45s"
```

### 4. Generar Reportes
```python
# Reporte en texto
report = self.timing.generate_report()

# Datos en JSON
data = self.timing.to_dict()
```

---

## 📊 FORMATOS DE TIEMPO

El sistema formatea automáticamente los tiempos según su duración:

| Duración | Formato |
|----------|---------|
| < 60 segundos | `2.45s` |
| 60s - 3600s | `20.75m (1245.3s)` |
| > 3600s | `1.25h (4500.0s)` |

---

## 📈 INTERPRETACIÓN DE RESULTADOS

### Gráfica de Barras
```
Ejecución de ILS                ████████████████████ 98.2%
Guardado de resultados          ░░░░░░░░░░░░░░░░░░░░  0.3%
```

- **Lleno (█)**: Porcentaje del tiempo total
- **Vacío (░)**: Espacio restante
- **Porcentaje**: Proporción exacta

### Análisis Típico
- **Ejecución de ILS**: 95-99% (la mayoría del tiempo)
- **Guardado**: 0.5-2% (rápido)
- **Gráficas**: 0.1-1% (muy rápido)
- **Carga**: 0.1-0.5% (muy rápido)

---

## 🚀 UBICACIÓN DE ARCHIVOS

Los reportes de timing se guardan en:

```
output/results/all_datasets/{timestamp}/
├── timing_report.txt          # Reporte legible
└── timing_report.json         # Datos JSON

output/results/specific_datasets/{family}/{timestamp}/
├── timing_report.txt
└── timing_report.json
```

---

## 💡 CASOS DE USO

### 1. Monitoreo en Tiempo Real
Observa el progreso y los tiempos mientras se ejecuta:
```bash
python scripts/run_full_experiment.py --mode all
```

### 2. Análisis Post-Ejecución
Revisa los reportes generados:
```bash
cat output/results/all_datasets/31-12-25_20-30-45/timing_report.txt
```

### 3. Comparación Entre Ejecuciones
Compara tiempos entre diferentes ejecuciones:
```bash
# Ejecución 1
python scripts/run_full_experiment.py --mode all

# Ejecución 2 (con diferentes parámetros)
python scripts/run_full_experiment.py --mode all --max-time 60
```

### 4. Optimización
Identifica cuellos de botella:
- Si "Ejecución de ILS" es muy larga → aumentar `--max-time`
- Si "Guardado de resultados" es lento → revisar disco
- Si "Generación de gráficas" es lenta → revisar PlotManager

---

## 📝 EJEMPLO COMPLETO

### Ejecución
```bash
$ python scripts/run_full_experiment.py --mode family --family DSJ

📂 CARGANDO DATASETS
✅ 15 datasets cargados
⏱️  Tiempo de carga: 0.85s

[  1/ 15] (  0.0%) DSJC125.1
   Réplica 1/1: 6 colores (12 conflictos) ✗ 12.30s (+20.0%)
   📈 Resumen: 6 colores (mejor), 6.0±0.0 (promedio), 0/1 factibles

... (14 instancias más) ...

⏱️  Tiempo total: 35.75m (2145.3s)

💾 GUARDANDO RESULTADOS
✅ TIMING: timing_report.txt
✅ TIMING JSON: timing_report.json
⏱️  Tiempo de guardado: 1.23s

📊 GENERANDO GRÁFICAS
✅ Gráfica de convergencia generada
✅ Gráfica de escalabilidad generada
⏱️  Tiempo de generación de gráficas: 0.95s

⏱️  RESUMEN DE TIEMPOS POR ETAPA
Ejecución de ILS                2145.30s             ████████████████████ 99.2%
Guardado de resultados             1.23s             ░░░░░░░░░░░░░░░░░░░░  0.1%
Generación de gráficas             0.95s             ░░░░░░░░░░░░░░░░░░░░  0.0%
Carga de datasets                   0.85s             ░░░░░░░░░░░░░░░░░░░░  0.0%
TIEMPO TOTAL                    2148.33s
```

---

## ✅ CONCLUSIÓN

El sistema de timing proporciona:
- ✅ Monitoreo en tiempo real
- ✅ Documentación automática en TXT y JSON
- ✅ Análisis visual con gráficas de barras
- ✅ Almacenamiento en carpeta de output
- ✅ Formatos legibles y estructurados

**Ahora puedes saber exactamente cuánto tiempo se demora cada etapa de tu experimento.**

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Sistema de timing completamente implementado
