# 🎯 RESUMEN: Experimentación por Familias de Instancias

**Tu solicitud**: "Necesito que se corra para familias de instancias de los dataset (CUL, DSJ, LEI, etc)"

**Solución**: Dos nuevos scripts automatizados

---

## 📊 Dos Scripts Nuevos Creados

### 1. `gaa_family_experiments.py` - Ejecuta Experimentos

**Ubicación**: `04-Generated/scripts/gaa_family_experiments.py`

**Función**: Ejecuta GAA completo para cada familia de instancias

```bash
# Todas las familias
python 04-Generated/scripts/gaa_family_experiments.py

# Una familia
python 04-Generated/scripts/gaa_family_experiments.py --family DSJ

# Varias familias
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ LEI

# Con parámetros personalizados
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ --iterations 1000
```

### 2. `analyze_family_results.py` - Analiza Resultados

**Ubicación**: `04-Generated/scripts/analyze_family_results.py`

**Función**: Genera comparativas entre familias después de experimentos

```bash
python 04-Generated/scripts/analyze_family_results.py
```

---

## 🏗️ Las 7 Familias de Instancias

```
Familia  │ Descripción                      │ # Instancias
─────────┼──────────────────────────────────┼──────────────
CUL      │ Culberson - Flat graph           │ 6
DSJ      │ DIMACS-Sparse-Johnson - Sparse   │ 15
LEI      │ Leighton - Structured            │ 4
MYC      │ Mycielski - Mycielski construct  │ 6
REG      │ Regular - Regular degree          │ 5
SCH      │ Schure - Carefully structured    │ 6
SGB      │ Stanford GraphBase - Various     │ 8
         │                          TOTAL   │ 50+
```

---

## 🚀 Flujo Recomendado

### Paso 1: Ejecutar Experimentos

```bash
cd projects/GCP-ILS-GAA

# Opción A: Prueba rápida (10 minutos)
python 04-Generated/scripts/gaa_family_experiments.py --family CUL --iterations 100

# Opción B: Análisis medio (2-3 horas)
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ LEI --iterations 500

# Opción C: Estudio completo (5-8 horas)
python 04-Generated/scripts/gaa_family_experiments.py --iterations 500
```

### Paso 2: Analizar Resultados

```bash
python 04-Generated/scripts/analyze_family_results.py
```

**Output**:
- Tabla comparativa entre familias
- Rankings por: fitness, calidad, velocidad, consistencia, robustez
- Insights: cuál familia es más fácil/difícil
- CSV para análisis avanzado

---

## 📁 Estructura de Salida

```
results/
├── CUL/
│   ├── summary.txt
│   ├── results.json
│   ├── results.csv
│   ├── configuration_top_1.yaml       ← Mejor config para CUL
│   ├── configuration_top_2.yaml
│   ├── configuration_top_3.yaml
│   └── family_results.json
│
├── DSJ/
│   ├── summary.txt
│   ├── results.json
│   ├── results.csv
│   ├── configuration_top_1.yaml       ← Mejor config para DSJ
│   └── ... (idéntico a CUL)
│
├── LEI/, MYC/, REG/, SCH/, SGB/
│   └── (estructura idéntica)
│
├── multi_family_summary.json          ← RESUMEN DE TODAS
├── family_comparison_report.txt       ← REPORTE COMPARATIVO
└── family_comparison.csv              ← Tabla para Excel/análisis
```

---

## 📊 Qué obtienes de cada familia

Para **CUL**, por ejemplo:

```
✓ 6 instancias cargadas
✓ 500 iteraciones de búsqueda ILS
✓ Evaluación en 6 instancias
✓ Top-3 mejores configuraciones encontradas
✓ Reportes: TXT, JSON, CSV, YAML
✓ Ejemplo de output:

FAMILIA CUL RESULTS
─────────────────────────────────────
Best Fitness:     0.8542
Best Config:      LargestDegreeFirst + ColorSwap + Remove3
Mean Colors:      24.3 ± 1.2
Success Rate:     98.5%
Avg Time:         245 ms
```

---

## 📋 Ejemplo de Output: `analyze_family_results.py`

```
════════════════════════════════════════════════════════════════════
FAMILY COMPARISON TABLE
════════════════════════════════════════════════════════════════════

Family     │ Fitness        │ Colors (mean±std)    │ Success Rate    │ Time (ms)
────────────┼────────────────┼──────────────────────┼─────────────────┼──────────
1. MYC      │ 0.8712         │ 23.1±0.9             │ 99.2%           │ 198
2. CUL      │ 0.8542         │ 24.3±1.2             │ 98.5%           │ 245
3. REG      │ 0.8456         │ 24.7±1.4             │ 97.8%           │ 267
4. SGB      │ 0.8334         │ 25.2±1.6             │ 96.9%           │ 289
5. DSJ      │ 0.8234         │ 25.8±2.1             │ 95.6%           │ 312
6. SCH      │ 0.8123         │ 25.9±2.2             │ 94.8%           │ 298
7. LEI      │ 0.7956         │ 26.5±1.8             │ 93.7%           │ 276

════════════════════════════════════════════════════════════════════
INSIGHTS AND FINDINGS
════════════════════════════════════════════════════════════════════

🏆 BEST OVERALL: MYC
✓ EASIEST FOR GAA: MYC
✗ HARDEST FOR GAA: LEI
📊 BEST SOLUTION QUALITY: MYC
🔄 MOST CONSISTENT: MYC
⚡ FASTEST: MYC
✅ MOST ROBUST: MYC
```

---

## ⏱️ Tiempos Estimados

| Escenario | Comando | Tiempo |
|-----------|---------|--------|
| **Prueba 1 familia (100 iter)** | `--family CUL --iterations 100` | 10 min |
| **Análisis 3 familias** | `--families CUL DSJ LEI` | 2-3 hrs |
| **Estudio 7 familias** | (sin argumentos) | 5-8 hrs |
| **Análisis exhaustivo** | `--iterations 1000` | 10-15 hrs |

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Comparar DSJ vs CUL

```bash
# Ejecutar solo estas dos
python 04-Generated/scripts/gaa_family_experiments.py --families DSJ CUL

# Analizar
python 04-Generated/scripts/analyze_family_results.py

# Resultado: Ver cuál es más fácil
# (DSJ probablemente más difícil que CUL)
```

### Ejemplo 2: Encontrar Familia más Difícil

```bash
# Correr todas
python 04-Generated/scripts/gaa_family_experiments.py

# Analizar
python 04-Generated/scripts/analyze_family_results.py

# Output dice: "HARDEST FOR GAA: LEI"
```

### Ejemplo 3: Usar Configuración Óptima por Familia

```bash
# Después de experimentos, puedes:
# - Usar CUL/configuration_top_1.yaml para instancias CUL
# - Usar DSJ/configuration_top_1.yaml para instancias DSJ
# - Usar MYC/configuration_top_1.yaml para instancias MYC
# etc.
```

---

## 📝 Checklist de Uso

- [ ] Decidir qué familias correr
- [ ] Decidir cuántas iteraciones (100/500/1000)
- [ ] Ejecutar: `python gaa_family_experiments.py [opciones]`
- [ ] Esperar a que termine (10 min - 8 hrs)
- [ ] Ejecutar: `python analyze_family_results.py`
- [ ] Revisar resultados en `results/` y reportes
- [ ] (Opcional) Crear gráficos con datos CSV

---

## 🔄 Workflow Completo (Ejemplo)

```bash
# 1. Ir a carpeta
cd projects/GCP-ILS-GAA

# 2. Ejecutar todas las familias (asume 8 horas disponibles)
python 04-Generated/scripts/gaa_family_experiments.py

# [Esperar 8 horas]

# 3. Ver resultados en consola + archivos
ls results/CUL/
ls results/DSJ/
cat results/multi_family_summary.json

# 4. Análisis comparativo
python 04-Generated/scripts/analyze_family_results.py

# 5. (Opcional) Crear gráfico con pandas
python << 'EOF'
import pandas as pd
df = pd.read_csv('results/family_comparison.csv')
df.plot(x='Family', y='Fitness', kind='bar')
EOF
```

---

## 📚 Documentación Completa

Para detalles:
- **[GUIA_EXPERIMENTOS_FAMILIAS.md](GUIA_EXPERIMENTOS_FAMILIAS.md)** - Guía completa de uso
- **[GUIA_EXPERIMENTACION.md](GUIA_EXPERIMENTACION.md)** - Detalles de GAA básico

---

## 🚀 ¿Empezamos?

### Opción A: Prueba Rápida (10 min)
```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_family_experiments.py --family CUL --iterations 100
```

### Opción B: Análisis Medio (2-3 hrs)
```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ LEI --iterations 500
python 04-Generated/scripts/analyze_family_results.py
```

### Opción C: Estudio Completo (5-8 hrs)
```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_family_experiments.py
# [esperar 8 horas]
python 04-Generated/scripts/analyze_family_results.py
```

---

**Resultado**: Sabrás exactamente qué configuración de ILS es óptima para cada familia de instancias.
