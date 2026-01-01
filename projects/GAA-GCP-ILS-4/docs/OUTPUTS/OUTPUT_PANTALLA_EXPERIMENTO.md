# 📺 OUTPUT EN PANTALLA - run_full_experiment.py

**Proyecto**: GAA-GCP-ILS-4  
**Fecha**: 31 de Diciembre, 2025  
**Script**: `scripts/run_full_experiment.py`

---

## 📋 QUÉ SE IMPRIME EN PANTALLA

El script imprime información detallada en cada paso de la ejecución, permitiéndote seguir el progreso en tiempo real.

---

## 🎬 EJEMPLO COMPLETO DE OUTPUT

### 1️⃣ INICIO DEL EXPERIMENTO

```
================================================================================
🔬 EXPERIMENTO COMPLETO: ILS EN 79 INSTANCIAS
================================================================================
⏱️  Tiempo máximo por instancia: 300.0s
🔄 Réplicas por instancia: 1
🌱 Semilla: 42
================================================================================

📂 CARGANDO DATASETS
--------------------------------------------------------------------------------
✅ 79 datasets cargados

```

**Información mostrada**:
- Total de instancias a procesar
- Configuración (tiempo máximo, réplicas, semilla)
- Cantidad de datasets cargados

---

### 2️⃣ EJECUCIÓN DE INSTANCIAS

```
[  1/ 79] (  0.0%) myciel3
   📊 Vértices:   11 | Aristas:     20 | BKS: 4
   Réplica 1/1: 4 colores (0 conflictos) ✓ 0.15s (0.0%)
   📈 Resumen: 4 colores (mejor), 4.0±0.0 (promedio), 1/1 factibles

[  2/ 79] (  1.3%) myciel4
   📊 Vértices:   23 | Aristas:     71 | BKS: 5
   Réplica 1/1: 5 colores (0 conflictos) ✓ 0.22s (0.0%)
   📈 Resumen: 5 colores (mejor), 5.0±0.0 (promedio), 1/1 factibles

[  3/ 79] (  2.5%) myciel5
   📊 Vértices:   47 | Aristas:    236 | BKS: 6
   Réplica 1/1: 6 colores (0 conflictos) ✓ 0.45s (0.0%)
   📈 Resumen: 6 colores (mejor), 6.0±0.0 (promedio), 1/1 factibles

[  4/ 79] (  3.8%) DSJC125.1
   📊 Vértices:  125 | Aristas:    736 | BKS: 5
   Réplica 1/1: 6 colores (12 conflictos) ✗ 12.30s (+20.0%)
   📈 Resumen: 6 colores (mejor), 6.0±0.0 (promedio), 0/1 factibles

[  5/ 79] (  5.1%) DSJC125.5
   📊 Vértices:  125 | Aristas:   3891 | BKS: 17
   Réplica 1/1: 18 colores (5 conflictos) ✗ 45.20s (+5.9%)
   📈 Resumen: 18 colores (mejor), 18.0±0.0 (promedio), 0/1 factibles

...
```

**Información mostrada por instancia**:
- `[X/79]` - Número de instancia actual
- `(Y%)` - Porcentaje de progreso
- Nombre de la instancia
- 📊 Vértices, aristas y BKS (Best Known Solution)
- Para cada réplica:
  - Número de colores encontrados
  - Conflictos (0 = solución factible)
  - ✓/✗ - Factibilidad
  - Tiempo de ejecución
  - Gap respecto a BKS (si se conoce)
- 📈 Resumen: mejor solución, promedio±desviación, factibles

---

### 3️⃣ FINALIZACIÓN DEL EXPERIMENTO

```
================================================================================
✅ EXPERIMENTO COMPLETADO
================================================================================
⏱️  Tiempo total: 1245.3s (20.8 minutos)
📊 Instancias procesadas: 79
🔄 Réplicas por instancia: 1
📈 Tiempo promedio por instancia: 15.8s
================================================================================

```

**Información mostrada**:
- Tiempo total de ejecución (en segundos y minutos)
- Total de instancias procesadas
- Réplicas ejecutadas
- Tiempo promedio por instancia

---

### 4️⃣ GUARDANDO RESULTADOS

```
================================================================================
💾 GUARDANDO RESULTADOS
================================================================================
✅ CSV: summary.csv
✅ JSON: detailed_results.json
✅ TXT: statistics.txt
✅ Soluciones: 79 archivos .sol guardados

```

**Información mostrada**:
- Archivos CSV guardados
- Archivos JSON guardados
- Archivos TXT guardados
- Cantidad de soluciones guardadas

---

### 5️⃣ GENERANDO GRÁFICAS

```
================================================================================
📊 GENERANDO GRÁFICAS
================================================================================
✅ Gráfica de convergencia generada
✅ Gráfica de escalabilidad generada
================================================================================
✅ PROCESO COMPLETADO
================================================================================
📁 Resultados guardados en: output/results/all_datasets/31-12-25_20-30-45
================================================================================

```

**Información mostrada**:
- Estado de cada gráfica generada
- Ubicación final de todos los resultados

---

## 📊 INFORMACIÓN POR SECCIÓN

### Encabezado de Instancia
```
[  1/ 79] (  0.0%) myciel3
   📊 Vértices:   11 | Aristas:     20 | BKS: 4
```
- Número de instancia actual / Total
- Porcentaje de progreso
- Nombre de la instancia
- Número de vértices
- Número de aristas
- Best Known Solution (si se conoce)

### Línea de Réplica
```
   Réplica 1/1: 4 colores (0 conflictos) ✓ 0.15s (0.0%)
```
- Número de réplica actual / Total
- Número de colores encontrados
- Conflictos (0 = factible)
- ✓ = Solución factible, ✗ = Infactible
- Tiempo de ejecución
- Gap respecto a BKS

### Resumen de Instancia
```
   📈 Resumen: 4 colores (mejor), 4.0±0.0 (promedio), 1/1 factibles
```
- Mejor solución encontrada
- Promedio ± desviación estándar
- Soluciones factibles / Total de réplicas

---

## 🎯 SÍMBOLOS UTILIZADOS

| Símbolo | Significado |
|---------|------------|
| ✓ | Solución factible (sin conflictos) |
| ✗ | Solución infactible (con conflictos) |
| 📊 | Información de problema |
| 📈 | Resumen de resultados |
| 💾 | Guardando datos |
| 📊 | Generando gráficas |
| ✅ | Completado exitosamente |
| ❌ | Error |
| ⚠️ | Advertencia |
| 🔬 | Experimento |
| ⏱️ | Tiempo |
| 🔄 | Réplicas |
| 🌱 | Semilla |
| 📁 | Directorio |

---

## 📈 INTERPRETACIÓN DE RESULTADOS

### Gap (Brecha respecto a BKS)

```
(+20.0%)  → Solución 20% peor que BKS
(0.0%)    → Solución igual a BKS (óptima)
(-5.0%)   → Imposible (no puede ser mejor que BKS)
```

### Factibilidad

```
✓ = Sin conflictos (solución válida)
✗ = Con conflictos (solución inválida)
```

### Progreso

```
[  1/ 79] (  0.0%) → Primera instancia, 0% completado
[ 40/ 79] ( 50.6%) → Mitad del proceso
[ 79/ 79] (100.0%) → Última instancia
```

---

## 🚀 CÓMO EJECUTAR Y VER OUTPUT

### Ejecución básica (todos los datasets)
```bash
python scripts/run_full_experiment.py --mode all
```

### Ejecución en familia específica
```bash
python scripts/run_full_experiment.py --mode family --family DSJ
```

### Con múltiples réplicas
```bash
python scripts/run_full_experiment.py --mode all --num-replicas 3
```

### Con tiempo límite personalizado
```bash
python scripts/run_full_experiment.py --mode all --max-time 60
```

---

## 💡 TIPS PARA INTERPRETAR OUTPUT

1. **Progreso**: Observa el porcentaje `(X%)` para saber cuánto falta
2. **Velocidad**: El tiempo promedio por instancia te dice cuánto tardará el total
3. **Factibilidad**: Busca ✓ para saber si las soluciones son válidas
4. **Gap**: Compara con BKS para evaluar calidad
5. **Variabilidad**: La desviación estándar (±) muestra consistencia

---

## 📊 EJEMPLO DE EJECUCIÓN RÁPIDA (Familia DSJ)

```bash
$ python scripts/run_full_experiment.py --mode family --family DSJ

================================================================================
🔬 EXPERIMENTO COMPLETO: ILS EN 15 INSTANCIAS
================================================================================
⏱️  Tiempo máximo por instancia: 300.0s
🔄 Réplicas por instancia: 1
🌱 Semilla: 42
================================================================================

📂 CARGANDO DATASETS
--------------------------------------------------------------------------------
✅ 15 datasets cargados

[  1/ 15] (  0.0%) DSJC125.1
   📊 Vértices:  125 | Aristas:    736 | BKS: 5
   Réplica 1/1: 6 colores (12 conflictos) ✗ 12.30s (+20.0%)
   📈 Resumen: 6 colores (mejor), 6.0±0.0 (promedio), 0/1 factibles

... (13 instancias más) ...

[15/ 15] (100.0%) DSJC500.9
   📊 Vértices:  500 | Aristas: 112437 | BKS: 128
   Réplica 1/1: 135 colores (234 conflictos) ✗ 287.45s (+5.5%)
   📈 Resumen: 135 colores (mejor), 135.0±0.0 (promedio), 0/1 factibles

================================================================================
✅ EXPERIMENTO COMPLETADO
================================================================================
⏱️  Tiempo total: 2145.3s (35.8 minutos)
📊 Instancias procesadas: 15
🔄 Réplicas por instancia: 1
📈 Tiempo promedio por instancia: 143.0s
================================================================================

💾 GUARDANDO RESULTADOS
================================================================================
✅ CSV: summary.csv
✅ JSON: detailed_results.json
✅ TXT: statistics.txt
✅ Soluciones: 15 archivos .sol guardados

📊 GENERANDO GRÁFICAS
================================================================================
✅ Gráfica de convergencia generada
✅ Gráfica de escalabilidad generada
================================================================================
✅ PROCESO COMPLETADO
================================================================================
📁 Resultados guardados en: output/results/specific_datasets/DSJ/31-12-25_20-45-30
================================================================================
```

---

## ✅ CONCLUSIÓN

El script ahora imprime información detallada en cada paso:
- ✅ Carga de datasets
- ✅ Progreso de ejecución (con porcentaje)
- ✅ Resultados por instancia
- ✅ Resumen de estadísticas
- ✅ Guardado de archivos
- ✅ Generación de gráficas
- ✅ Ubicación final de resultados

**Puedes seguir el progreso en tiempo real y saber exactamente qué está sucediendo en cada momento.**

---

**Última actualización**: 31 Diciembre 2025  
**Estado**: ✅ Output mejorado y documentado
