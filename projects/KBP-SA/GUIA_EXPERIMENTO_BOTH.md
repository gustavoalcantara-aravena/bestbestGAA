# Guía de Ejecución: Experimento Both (Low-Dimensional + Large-Scale)

**Fecha de creación**: 1 de diciembre de 2025  
**Script**: `demo_experimentation_both.py`  
**Propósito**: Ejecutar experimentos completos en ambos grupos de instancias (corta y larga escala) con análisis estadístico y visualizaciones

---

## Descripción General

Este experimento ejecuta de forma secuencial pruebas sobre dos grupos de instancias del Problema de la Mochila:
1. **Low-Dimensional**: 10 instancias pequeñas (f1-f10)
2. **Large-Scale**: 21 instancias grandes (knapPI_*)

Para cada grupo se generan:
- Experimentos con múltiples algoritmos GAA
- Análisis estadístico completo
- Visualizaciones comparativas
- Gráficas de Simulated Annealing

---

## Comando de Ejecución

### Desde PowerShell:

```powershell
cd c:\Users\alfabeta\Desktop\GAA-Framework-Best\projects\KBP-SA
$env:Path += ";C:\Program Files\Graphviz\bin"
python scripts\demo_experimentation_both.py
```

### Explicación de comandos:
1. **`cd ...`**: Navega al directorio del proyecto
2. **`$env:Path += ...`**: Agrega Graphviz al PATH (necesario para visualización de AST)
3. **`python scripts\...`**: Ejecuta el script principal

---

## Configuración del Experimento

### Parámetros Clave:

| Parámetro | Valor | Ubicación en código |
|-----------|-------|---------------------|
| **Algoritmos GAA** | 3 | Línea 650: `for i in range(3)` |
| **Repeticiones** | 1 | Línea 323: `repetitions=1` |
| **Timeout por ejecución** | 60 segundos | Línea 324: `max_time_seconds=60.0` |
| **Evaluaciones SA** | 5000 | Línea 95: `max_evaluations=5000` |
| **Temperatura inicial** | 100.0 | Línea 91: `T0=100.0` |
| **Factor de enfriamiento** | 0.95 | Línea 92: `alpha=0.95` |

### Total de Experimentos:

#### Low-Dimensional:
- **Instancias**: 10
- **Algoritmos**: 3
- **Repeticiones**: 1
- **Total**: 10 × 3 × 1 = **30 experimentos**

#### Large-Scale:
- **Instancias**: 21
- **Algoritmos**: 3
- **Repeticiones**: 1
- **Total**: 21 × 3 × 1 = **63 experimentos**

#### **TOTAL GLOBAL**: **93 experimentos**

---

## Tiempos de Ejecución

### Última ejecución (01/12/2025 11:50:06 - 11:50:46):

| Fase | Tiempo Real |
|------|-------------|
| **Generación de algoritmos GAA** | **0.001s** (1ms) |
| **Grupo Low-Dimensional** | **9.49s** |
| └─ Configuración | 0.003s (3ms) |
| └─ Experimentos (30 ejecuciones) | 1.26s |
| └─ Guardado de resultados | 0.002s (2ms) |
| └─ Análisis estadístico | 0.004s (4ms) |
| └─ Comparación estadística | 0.003s (3ms) |
| └─ Visualizaciones (17 archivos) | 8.21s |
| **Grupo Large-Scale** | **30.10s** |
| └─ Configuración | 0.035s (35ms) |
| └─ Experimentos (63 ejecuciones) | 15.79s |
| └─ Guardado de resultados | 0.003s (3ms) |
| └─ Análisis estadístico | 0.005s (5ms) |
| └─ Comparación estadística | 0.004s (4ms) |
| └─ Visualizaciones (28 archivos) | 14.26s |
| **TIEMPO TOTAL** | **39.60s (~40 segundos)** |

*Nota: Tiempos medidos en hardware específico. Pueden variar según CPU, RAM y complejidad de algoritmos generados.*

---

## Resultados Generados

### Estructura de Directorios:

```
output/
├── low_dimensional_experiments/
│   └── experiment_low_dimensional_experiment_YYYYMMDD_HHMMSS.json
│
├── large_scale_experiments/
│   └── experiment_large_scale_experiment_YYYYMMDD_HHMMSS.json
│
├── plots_low_dimensional_YYYYMMDD_HHMMSS/
│   ├── README.md                                    # Resumen del experimento
│   ├── time_tracking.md                             # Tiempos de ejecución
│   ├── best_algorithm_ast                           # Estructura del mejor algoritmo
│   ├── demo_boxplot.png                             # Comparación boxplot
│   ├── demo_bars.png                                # Gap promedio por algoritmo
│   ├── demo_scatter.png                             # Tiempo vs calidad
│   ├── gap_evolution.png                            # Evolución del gap (agregado)
│   ├── acceptance_rate.png                          # Tasa de aceptación (agregado)
│   ├── delta_e_distribution.png                     # Distribución ΔE (agregado)
│   ├── exploration_exploitation_f1_l-d_kp_10_269.png
│   ├── exploration_exploitation_f2_l-d_kp_20_878.png
│   └── ... (10 gráficas individuales, una por instancia)
│
├── plots_large_scale_YYYYMMDD_HHMMSS/
│   ├── README.md
│   ├── time_tracking.md
│   ├── best_algorithm_ast
│   ├── demo_boxplot.png
│   ├── demo_bars.png
│   ├── demo_scatter.png
│   ├── gap_evolution.png
│   ├── acceptance_rate.png
│   ├── delta_e_distribution.png
│   ├── exploration_exploitation_knapPI_1_100_1000_1_large_scale.png
│   ├── exploration_exploitation_knapPI_1_200_1000_1_large_scale.png
│   └── ... (21 gráficas individuales, una por instancia)
│
└── time_tracker_global/
    └── time_tracking_global_YYYYMMDD_HHMMSS.md      # Tracking global de tiempos
```

### Conteo de Archivos por Grupo:

#### Low-Dimensional:
- **17 archivos PNG**: 3 estadísticas + 1 AST + 3 SA agregadas + 10 por instancia
- **2 archivos MD**: README.md + time_tracking.md
- **1 archivo AST**: best_algorithm_ast

#### Large-Scale:
- **28 archivos PNG**: 3 estadísticas + 1 AST + 3 SA agregadas + 21 por instancia
- **2 archivos MD**: README.md + time_tracking.md
- **1 archivo AST**: best_algorithm_ast

---

## Descripción de Visualizaciones

### Gráficas Estadísticas (Ambos Grupos):

1. **demo_boxplot.png**
   - Comparación de gap al óptimo entre los 3 algoritmos
   - Muestra mediana, cuartiles y outliers

2. **demo_bars.png**
   - Gap promedio por algoritmo con barras de error (desviación estándar)

3. **demo_scatter.png**
   - Trade-off entre tiempo de ejecución y calidad de solución

4. **best_algorithm_ast**
   - Visualización gráfica de la estructura del mejor algoritmo
   - Muestra operadores y flujo de control

### Gráficas SA Agregadas (Ambos Grupos):

5. **gap_evolution.png**
   - Evolución del gap durante la búsqueda (promedio de todas las instancias)
   - Banda sombreada: desviación estándar
   - Eje derecho: temperatura (escala log)

6. **acceptance_rate.png**
   - Tasa de aceptación de movimientos (promedio)
   - Ventana móvil de 100 iteraciones
   - Muestra transición de exploración a explotación

7. **delta_e_distribution.png**
   - Distribución de cambios de energía (ΔE)
   - Separado por movimientos aceptados/rechazados
   - Datos combinados de todas las instancias

### Gráficas SA Individuales:

8-N. **exploration_exploitation_<instancia>.png**
   - Balance entre exploración y explotación por instancia
   - Área apilada con proporciones:
     * Verde: Explotación (mejoras)
     * Naranja: Exploración (empeoramientos aceptados)
     * Rojo: Rechazados
   - Panel estadístico con métricas clave
   - Línea de temperatura superpuesta

---

## Análisis Estadístico Realizado

### Por Algoritmo:
- Estadísticas descriptivas (media, desviación estándar, min, max)
- Intervalo de confianza al 95%
- Tiempo promedio de ejecución

### Comparación entre Algoritmos:
- **Test de Friedman**: Comparación múltiple (3 algoritmos)
- **Rankings promedio**: Ordenamiento de algoritmos (menor = mejor)
- **Test de Wilcoxon**: Comparación pareada entre los dos mejores
- **Cohen's d**: Tamaño del efecto de la diferencia

### Métricas Calculadas:
- **Gap al óptimo**: `((óptimo - valor) / óptimo) × 100`
- **Tasa de éxito**: Porcentaje de ejecuciones exitosas
- **Tiempo total**: Tiempo de ejecución por experimento

---

## Interpretación de Resultados

### Identificar el Mejor Algoritmo:

El script automáticamente identifica el mejor algoritmo basándose en:
1. **Ranking promedio** del test de Friedman (menor es mejor)
2. **Gap promedio** al valor óptimo (menor es mejor)

### Ejemplo de Salida en Consola:

```
🏆 Mejor algoritmo: GAA_Algorithm_2
   Gap promedio: 0.15%
```

### Significancia Estadística:

- **p-value < 0.05**: Diferencias significativas entre algoritmos
- **Cohen's d**:
  - < 0.2: Efecto pequeño
  - 0.2-0.5: Efecto mediano
  - > 0.5: Efecto grande

---

## Verificación de Resultados

### Checklist Post-Ejecución:

#### Low-Dimensional:
- [ ] JSON generado en `output/low_dimensional_experiments/`
- [ ] Carpeta `plots_low_dimensional_*` creada
- [ ] 17 archivos PNG generados
- [ ] Consola muestra: "✅ Experimentos completados: 30/30"

#### Large-Scale:
- [ ] JSON generado en `output/large_scale_experiments/`
- [ ] Carpeta `plots_large_scale_*` creada
- [ ] 28 archivos PNG generados
- [ ] Consola muestra: "✅ Experimentos completados: 63/63"

### Comando de Verificación (PowerShell):

```powershell
# Contar archivos PNG en la última ejecución
$lowDir = Get-ChildItem "output\plots_low_dimensional_*" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$largeDir = Get-ChildItem "output\plots_large_scale_*" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1

Write-Host "`nLow-Dimensional:"
Write-Host "  Carpeta: $($lowDir.Name)"
Write-Host "  PNGs: $((Get-ChildItem $lowDir.FullName -Filter *.png).Count)"

Write-Host "`nLarge-Scale:"
Write-Host "  Carpeta: $($largeDir.Name)"
Write-Host "  PNGs: $((Get-ChildItem $largeDir.FullName -Filter *.png).Count)"
```

**Salida esperada:**
```
Low-Dimensional:
  Carpeta: plots_low_dimensional_20251201_115006
  PNGs: 17

Large-Scale:
  Carpeta: plots_large_scale_20251201_115006
  PNGs: 28
```

---

## Modificación de Parámetros

### Para aumentar repeticiones (análisis más robusto):

**Archivo**: `scripts/demo_experimentation_both.py`  
**Línea 323**:

```python
# Antes:
repetitions=1,

# Después (ejemplo con 3 repeticiones):
repetitions=3,
```

**Impacto** (estimado basado en tiempos reales):
- Low-Dimensional: 30 → 90 experimentos (~28 segundos, 3× más rápido)
- Large-Scale: 63 → 189 experimentos (~90 segundos, 3× más rápido)
- **Total con 3 repeticiones**: ~2 minutos

### Para cambiar número de algoritmos:

**Línea 650**:

```python
# Antes:
for i in range(3):

# Después (ejemplo con 5 algoritmos):
for i in range(5):
```

**Impacto**:
- Low-Dimensional: 30 → 50 experimentos
- Large-Scale: 63 → 105 experimentos

### Para ajustar timeout:

**Línea 324**:

```python
# Antes:
max_time_seconds=60.0,

# Después (ejemplo con 5 minutos):
max_time_seconds=300.0,
```

---

## Solución de Problemas

### Error: "Graphviz no encontrado"

**Síntoma:**
```
❌ Error generando gráfico AST: failed to execute WindowsPath('dot')
```

**Solución:**
```powershell
# Verificar instalación
dot -V

# Agregar al PATH temporalmente
$env:Path += ";C:\Program Files\Graphviz\bin"

# O instalar
winget install --id Graphviz.Graphviz -e
```

### Script interrumpido antes de completar

**Síntoma:** Solo se generó un grupo (low o large)

**Solución:**
- Revisar logs en consola para identificar el error
- Verificar que todas las instancias existen en `datasets/`
- Aumentar `max_time_seconds` si hay timeouts

### Memoria insuficiente (Large-Scale)

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Solución:**
- Reducir `repetitions` a 1
- Reducir `max_evaluations` en línea 95 (ej: de 5000 a 2000)
- Procesar grupos por separado usando scripts individuales

---

## Comparación con Scripts Individuales

| Característica | `demo_experimentation_both.py` | `demo_experimentation.py` | `demo_experimentation_low.py` |
|----------------|-------------------------------|---------------------------|-------------------------------|
| Grupos procesados | Low + Large | Configurable | Solo Low |
| Algoritmos generados | 3 (compartidos) | 3 | 3 |
| Tiempo total | ~20-25 min | Variable | ~1.5 min |
| Tracking global | ✅ Sí | ❌ No | ❌ No |
| Uso recomendado | Análisis completo | Pruebas específicas | Desarrollo rápido |

---

## Replicación del Experimento

### Para replicar exactamente la misma ejecución:

1. **Usar la misma semilla aleatoria** (ya configurada en línea 647):
   ```python
   generator = AlgorithmGenerator(grammar=grammar, seed=42)
   ```

2. **Mantener los mismos parámetros**:
   - Repetitions: 1
   - Max evaluations: 5000
   - Temperatura: T0=100.0, alpha=0.95

3. **Ejecutar el comando**:
   ```powershell
   cd c:\Users\alfabeta\Desktop\GAA-Framework-Best\projects\KBP-SA
   $env:Path += ";C:\Program Files\Graphviz\bin"
   python scripts\demo_experimentation_both.py
   ```

### Para experimentos con diferentes semillas:

**Modificar línea 647**:
```python
# Cambiar seed para generar diferentes algoritmos
generator = AlgorithmGenerator(grammar=grammar, seed=123)  # Nueva semilla
```

---

## Resumen de la Última Ejecución

**Fecha**: 01/12/2025 11:50:06 - 11:50:46  
**Script ejecutado**: `python scripts\demo_experimentation_both.py`  
**Directorio de trabajo**: `C:\Users\alfabeta\Desktop\GAA-Framework-Best\projects\KBP-SA`  
**Duración total**: **39.60 segundos** (~40 segundos)  
**Experimentos ejecutados**: 93 (30 low + 63 large)  
**Tasa de éxito**: 100% (93/93)  
**Visualizaciones generadas**: 45 archivos PNG (17 low + 28 large)  

### Comando ejecutado:
```powershell
PS C:\Users\alfabeta\Desktop\GAA-Framework-Best\projects\KBP-SA> python scripts\demo_experimentation_both.py
```

### Desglose de tiempos:
- **Generación GAA**: 0.001s
- **Low-Dimensional**: 9.49s (30 experimentos + 17 visualizaciones)
- **Large-Scale**: 30.10s (63 experimentos + 28 visualizaciones)  

### Carpetas de salida:
- `output/plots_low_dimensional_20251201_115006/`
- `output/plots_large_scale_20251201_115006/`
- `output/time_tracker_global/time_tracking_global_20251201_115006.md`

---

## Referencias

- **Script principal**: `scripts/demo_experimentation_both.py`
- **Guía general**: `GUIA_EJECUCION.md`
- **Módulo de experimentación**: `experimentation/`
- **Generador GAA**: `gaa/generator.py`
- **Simulated Annealing**: `metaheuristic/sa_core.py`

---

**Última actualización**: 1 de diciembre de 2025
