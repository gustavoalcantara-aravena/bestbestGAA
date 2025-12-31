# 🏗️ EXPERIMENTACIÓN POR FAMILIAS: Guía Completa

**Necesidad**: Ejecutar experimentos GAA para cada familia de instancias (CUL, DSJ, LEI, MYC, REG, SCH, SGB)

**Solución**: Script `gaa_family_experiments.py` que automatiza todo

---

## 🎯 Familias Disponibles

```
CUL  → Culberson instances (flat graph coloring)
DSJ  → DIMACS-Sparse-Johnson instances (sparse random graphs)
LEI  → Leighton instances (structured graphs)
MYC  → Mycielski instances (Mycielski construction)
REG  → Regular instances (regular degree graphs)
SCH  → Schure instances (carefully structured)
SGB  → Stanford GraphBase instances (various patterns)
```

**Total**: 7 familias con decenas de instancias cada una

---

## 🚀 Cómo Ejecutar

### Opción 1: Todas las Familias

```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_family_experiments.py
```

**Esto ejecuta**:
- ✅ Experimento GAA completo para CUL
- ✅ Experimento GAA completo para DSJ
- ✅ Experimento GAA completo para LEI
- ✅ ... (todas las 7 familias)
- ✅ Genera resumen comparativo

**Tiempo**: ~5-8 horas (500 iteraciones × 7 familias)

---

### Opción 2: Una Familia Específica

```bash
# Solo DSJ
python 04-Generated/scripts/gaa_family_experiments.py --family DSJ

# Solo CUL
python 04-Generated/scripts/gaa_family_experiments.py --family CUL

# Solo LEI
python 04-Generated/scripts/gaa_family_experiments.py --family LEI
```

**Tiempo**: ~40-60 minutos por familia

---

### Opción 3: Múltiples Familias Seleccionadas

```bash
# CUL + DSJ + LEI solamente
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ LEI

# REG + SCH
python 04-Generated/scripts/gaa_family_experiments.py --families REG SCH
```

---

### Opción 4: Con Iteraciones Personalizadas

```bash
# Modo rápido: 100 iteraciones
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ --iterations 100

# Modo exhaustivo: 1000 iteraciones
python 04-Generated/scripts/gaa_family_experiments.py --families CUL DSJ LEI --iterations 1000

# Solo verbosidad mínima
python 04-Generated/scripts/gaa_family_experiments.py --quiet
```

---

## 📊 Flujo de Ejecución

```
Para cada familia (CUL, DSJ, LEI, MYC, REG, SCH, SGB):

1. CARGAR INSTANCIAS
   ├─ Lee todas las instancias .col de la familia
   ├─ Ej: DSJ tiene 15 instancias
   └─ Ej: CUL tiene 6 instancias

2. CREAR DIRECTORIO DE RESULTADOS
   ├─ results/CUL/
   ├─ results/DSJ/
   ├─ results/LEI/
   └─ ... etc ...

3. EJECUTAR EXPERIMENTO GAA
   ├─ 500 iteraciones ILS
   ├─ Evalúa todas las instancias de la familia
   ├─ Busca mejores configuraciones
   └─ Tiempo: 40-60 minutos por familia

4. GENERAR REPORTES
   ├─ summary.txt
   ├─ results.json
   ├─ results.csv
   ├─ configuration_top_1.yaml
   └─ convergence_plot.json

5. GUARDAR RESULTADOS FAMILIA
   └─ family_results.json

REPETIR PARA SIGUIENTE FAMILIA
```

---

## 📤 Outputs Esperados

### Por Familia

```
results/
├── CUL/
│   ├── summary.txt
│   ├── results.json
│   ├── results.csv
│   ├── configuration_top_1.yaml
│   ├── configuration_top_2.yaml
│   ├── configuration_top_3.yaml
│   ├── convergence_plot.json
│   └── family_results.json
│
├── DSJ/
│   ├── summary.txt
│   ├── results.json
│   ├── results.csv
│   ├── configuration_top_1.yaml
│   ├── configuration_top_2.yaml
│   ├── configuration_top_3.yaml
│   ├── convergence_plot.json
│   └── family_results.json
│
├── LEI/
│   └─ (estructura idéntica)
│
├── MYC/
│   └─ (estructura idéntica)
│
├── REG/
│   └─ (estructura idéntica)
│
├── SCH/
│   └─ (estructura idéntica)
│
├── SGB/
│   └─ (estructura idéntica)
│
├── multi_family_summary.json        ← RESUMEN DE TODAS LAS FAMILIAS
└── family_comparison_report.txt     ← COMPARATIVA EN TEXTO
```

---

## 📋 Contenido: `multi_family_summary.json`

```json
{
  "timestamp": "2025-12-30T14:32:15Z",
  "families": {
    "CUL": {
      "status": "completed",
      "duration_seconds": 2145.3
    },
    "DSJ": {
      "status": "completed",
      "duration_seconds": 3215.7
    },
    "LEI": {
      "status": "completed",
      "duration_seconds": 2876.4
    },
    ...
  },
  "summary": {
    "total_families": 7,
    "successful": 7,
    "failed": 0,
    "total_duration_seconds": 18543.2,
    "successful_families": ["CUL", "DSJ", "LEI", "MYC", "REG", "SCH", "SGB"],
    "failed_families": []
  }
}
```

---

## 📋 Contenido: `family_comparison_report.txt`

```
════════════════════════════════════════════════════════════════════════════

MULTI-FAMILY EXPERIMENTATION COMPARISON REPORT

════════════════════════════════════════════════════════════════════════════

Timestamp: 2025-12-30T14:32:15Z
Total families tested: 7
Iterations per family: 500

FAMILY RESULTS
────────────────────────────────────────────────────────────────────────────
Family          Status         Time (s)     Description
────────────────────────────────────────────────────────────────────────────
CUL             ✓ Completed    2145.3       Culberson instances - Flat graph c
DSJ             ✓ Completed    3215.7       DIMACS-Sparse-Johnson instances - 
LEI             ✓ Completed    2876.4       Leighton instances - Structured gr
MYC             ✓ Completed    1956.2       Mycielski instances - Mycielski co
REG             ✓ Completed    2345.8       Regular instances - Regular degree
SCH             ✓ Completed    2187.3       Schure instances - Carefully struc
SGB             ✓ Completed    2876.5       Stanford GraphBase instances - Var
────────────────────────────────────────────────────────────────────────────
TOTAL           7              18543.2
════════════════════════════════════════════════════════════════════════════
```

---

## 📊 Análisis Comparativo Entre Familias

Después de ejecutar, puedes comparar:

### 1. **Por Familia** (Mejor configuración):
```
CUL  → Fitness: 0.8542 | Colores: 24.3 ± 1.2
DSJ  → Fitness: 0.8234 | Colores: 25.8 ± 2.1
LEI  → Fitness: 0.7956 | Colores: 26.5 ± 1.8
MYC  → Fitness: 0.8712 | Colores: 23.1 ± 0.9
REG  → Fitness: 0.8456 | Colores: 24.7 ± 1.4
SCH  → Fitness: 0.8123 | Colores: 25.9 ± 2.2
SGB  → Fitness: 0.8334 | Colores: 25.2 ± 1.6
```

### 2. **Preguntas que puedes responder**:
- ¿Cuál familia es más fácil (mejor fitness)?
- ¿Cuál familia es más difícil?
- ¿Hay patrones entre familias?
- ¿Qué configuración generaliza mejor?

### 3. **Crear tabla comparativa**:
```python
import json
import pandas as pd

# Cargar resultados
results = {}
for family in ['CUL', 'DSJ', 'LEI', 'MYC', 'REG', 'SCH', 'SGB']:
    with open(f'results/{family}/results.json') as f:
        results[family] = json.load(f)

# Crear tabla
data = []
for family, result in results.items():
    top_config = result['top_configurations'][0]
    data.append({
        'Family': family,
        'Fitness': top_config['fitness'],
        'Colors': top_config['statistics']['mean_colors'],
        'Success': top_config['statistics']['success_rate'],
    })

df = pd.DataFrame(data).sort_values('Fitness', ascending=False)
print(df.to_string())
```

---

## ⏱️ Estimaciones de Tiempo

| Configuración | Tiempo Estimado |
|---------------|-----------------|
| 1 familia (500 iter) | 40-60 minutos |
| 3 familias (500 iter) | 2-3 horas |
| 7 familias (500 iter) | 5-8 horas |
| 7 familias (1000 iter) | 10-15 horas |

---

## 🎯 Casos de Uso

### Caso 1: Prueba Rápida

```bash
# Ejecutar solo CUL con 100 iteraciones (10 minutos)
python 04-Generated/scripts/gaa_family_experiments.py \
  --family CUL \
  --iterations 100
```

### Caso 2: Dos Familias Medianas

```bash
# DSJ + LEI con 500 iteraciones (2 horas)
python 04-Generated/scripts/gaa_family_experiments.py \
  --families DSJ LEI \
  --iterations 500
```

### Caso 3: Experiencia Completa

```bash
# Todas las familias, 500 iteraciones (5-8 horas)
python 04-Generated/scripts/gaa_family_experiments.py
```

### Caso 4: Análisis Exhaustivo

```bash
# Todas las familias, 1000 iteraciones (10-15 horas, noche)
python 04-Generated/scripts/gaa_family_experiments.py \
  --iterations 1000
```

---

## 📖 Interpretando Resultados

### Comparar Familias:

```python
# Ver cuál familia es más fácil para GAA
import json

results_by_family = {}
for family in ['CUL', 'DSJ', 'LEI']:
    with open(f'results/{family}/results.json') as f:
        data = json.load(f)
        best_fit = data['top_configurations'][0]['fitness']
        results_by_family[family] = best_fit

# Ordenar por mejor fitness
for family, fitness in sorted(results_by_family.items(), 
                               key=lambda x: x[1], 
                               reverse=True):
    print(f"{family}: {fitness:.4f}")

# Resultado:
# MYC: 0.8712  ← Más fácil
# CUL: 0.8542
# DSJ: 0.8234  ← Más difícil
```

### Preguntas para Investigar:

1. **¿Qué familia es más sensible al metaheurístico?**
   - Comparar variación entre familias

2. **¿Hay operadores que funcionan mejor en ciertas familias?**
   - Comparar configuraciones top-1 entre familias

3. **¿La dificultad correlaciona con tamaño?**
   - Correlacionar: tamaño instancia vs fitness

---

## 🔧 Personalización Avanzada

### Modificar pesos de fitness por familia:

```bash
# Editar directamente en el script:
# familia_config.fitness_weights = {
#     'quality': 0.6,    # 60% calidad
#     'time': 0.2,       # 20% tiempo
#     'robustness': 0.15,
#     'feasibility': 0.05
# }
```

### Usar different números de iteraciones:

```bash
# Rápido: 100 iter para prueba
# Normal: 500 iter para análisis
# Exhaustivo: 2000 iter para publicación
```

---

## ✅ Checklist

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install pyyaml numpy`)
- [ ] Script `gaa_family_experiments.py` existe
- [ ] Carpeta `datasets/` tiene las 7 familias
- [ ] Carpeta `results/` existe (se crea si no)
- [ ] Disco tiene espacio (cada familia ~100-200 MB)
- [ ] Decidir tiempo disponible (5 min → 8 horas)

---

## 📞 Resumen Rápido

| Acción | Comando |
|--------|---------|
| **Todas las familias** | `python gaa_family_experiments.py` |
| **Una familia** | `python gaa_family_experiments.py --family DSJ` |
| **Varias familias** | `python gaa_family_experiments.py --families CUL DSJ LEI` |
| **Modo rápido** | `python gaa_family_experiments.py --families CUL --iterations 100` |
| **Sin logs** | `python gaa_family_experiments.py --quiet` |

---

## 🎯 Próximo Paso

Ejecuta:
```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/gaa_family_experiments.py --family CUL
```

Este comando:
1. ✅ Carga 6 instancias de CUL
2. ✅ Ejecuta 500 iteraciones ILS
3. ✅ Genera reportes en `results/CUL/`
4. ✅ Tiempo: ~45 minutos
5. ✅ Tienes configuración óptima para CUL

---

**¿Empezamos?** ✅ Ejecuta cualquiera de los comandos arriba
