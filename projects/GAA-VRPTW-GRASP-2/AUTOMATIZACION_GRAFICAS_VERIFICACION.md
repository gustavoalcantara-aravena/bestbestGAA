# ✅ Automatización de Gráficas GAP - VERIFICACIÓN COMPLETA

## Estado: IMPLEMENTADO Y OPERATIVO

Última actualización: 3 de enero, 2026 - 03:07:52

---

## 📋 Resumen Ejecutivo

Se ha integrado automáticamente la generación de **5 gráficas comparativas de GAP** al final de cada ejecución de experimentos (QUICK y FULL). Las gráficas se guardan directamente en la carpeta `plots` del experimento actual con timestamp automático.

---

## ✅ Gráficas Generadas Automáticamente

Cada vez que se ejecuta `python scripts/experiments.py --mode QUICK` o `--mode FULL`:

| # | Archivo | Descripción | Estado |
|---|---------|-------------|--------|
| 1 | `01_gap_comparison_all_instances.png` | Comparación GAP todas instancias (barras) | ✅ Generada |
| 2 | `02_gap_evolution_lines.png` | Evolución de GAP por instancia (líneas) | ✅ Generada |
| 3 | `03_gap_boxplot_by_family.png` | Distribución GAP por familia (boxplot) | ✅ Generada |
| 4 | `04_gap_heatmap.png` | Mapa de calor: instancias vs algoritmos | ✅ Generada |
| 5 | `05_gap_by_family_grid.png` | Grid comparativo por familia (6 subfigs) | ✅ Generada |

---

## 📁 Estructura de Carpetas

```
output/
└── vrptw_experiments_[MODE]_[DD-MM-YY_HH-MM-SS]/
    ├── results/
    │   ├── raw_results.csv
    │   └── raw_results_detailed.csv
    ├── plots/
    │   ├── 01_gap_comparison_all_instances.png       ← GAP (AUTOMÁTICO)
    │   ├── 02_gap_evolution_lines.png                ← GAP (AUTOMÁTICO)
    │   ├── 03_gap_boxplot_by_family.png              ← GAP (AUTOMÁTICO)
    │   ├── 04_gap_heatmap.png                        ← GAP (AUTOMÁTICO)
    │   ├── 05_gap_by_family_grid.png                 ← GAP (AUTOMÁTICO)
    │   ├── 01_performance_comparison.png             (canónica)
    │   ├── 02_distance_by_instance.png               (canónica)
    │   └── ... (10 más gráficas canónicas)
    └── logs/
        ├── algorithm_specifications.json
        ├── performance_summary.txt
        └── best_algorithm_report.txt
```

---

## 🔧 Implementación Técnica

### Archivos Modificados

#### 1. `scripts/experiments.py`
- **Cambios**: Integración de llamada a `plot_gap_comparison.py` al final
- **Líneas**: Después de `generate_summary_report()`
- **Comportamiento**:
  - Ejecuta `python plot_gap_comparison.py` en subprocess
  - Captura stdout para mostrar progreso
  - Maneja errores sin detener ejecución

```python
# Generate GAP comparison visualizations automatically
print("\n[INFO] Generando gráficas de comparación GAP...")
try:
    import subprocess
    result = subprocess.run(
        [sys.executable, "plot_gap_comparison.py"],
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode == 0:
        if result.stdout:
            print(result.stdout)
    else:
        print(f"[WARNING] Error generando gráficas GAP: {result.stderr}")
except Exception as e:
    print(f"[WARNING] Error en generación automática de gráficas: {e}")
```

#### 2. `plot_gap_comparison.py`
- **Cambios**: Rutas dinámicas vs hardcoded
- **Búsqueda automática de CSV**: 
  - Busca en `output/*/results/raw_results.csv`
  - Selecciona el más reciente por `st_mtime`
  
```python
# Buscar el archivo CSV más reciente
output_dir = Path('output')
csv_files = sorted(output_dir.glob('*/results/raw_results.csv'), 
                   key=lambda x: x.stat().st_mtime, reverse=True)
results_path = csv_files[0]
plots_dir = results_path.parent.parent / 'plots'
```

- **Guardado directo**: Todas las gráficas usan la variable `plots_dir`
  - Evita necesidad de copiar archivos
  - Garantiza ubicación correcta automáticamente

---

## 📊 Ejemplo: FULL Experiment (3 de enero, 2026)

### Ejecución
```bash
python scripts/experiments.py --mode FULL
```

### Resultado
```
[INFO] Cargando datasets REALES de Solomon...
[OK] 56/56 instancias cargadas
...
[OK] 3 algoritmos GAA generados
Experiments: 100%|███████████████████████████| 168/168 [04:22<00:00,  1.56s/exp]
...
[INFO] Generando gráficas de comparación GAP...
[INFO] Cargando CSV más reciente: output\vrptw_experiments_FULL_03-01-26_03-01-57\results\raw_results.csv
[INFO] Guardando gráficas en: output\vrptw_experiments_FULL_03-01-26_03-01-57\plots

[OK] Guardado: 01_gap_comparison_all_instances.png
[OK] Guardado: 02_gap_evolution_lines.png
[OK] Guardado: 03_gap_boxplot_by_family.png
[OK] Guardado: 04_gap_heatmap.png
[OK] Guardado: 05_gap_by_family_grid.png

[SUMMARY] 168/168 completados
[RESULTS] output\vrptw_experiments_FULL_03-01-26_03-01-57\results
```

### Archivos Generados
```
01_gap_comparison_all_instances.png  286 KB  03-01-2026 3:07:50
02_gap_evolution_lines.png          763 KB  03-01-2026 3:07:51
03_gap_boxplot_by_family.png        153 KB  03-01-2026 3:07:51
04_gap_heatmap.png                  731 KB  03-01-2026 3:07:52
05_gap_by_family_grid.png           338 KB  03-01-2026 3:07:52
```

---

## 📈 Datos Estadísticos Generados

### Resumen GAP Global (FULL 168 instancias)
```
                          Algoritmo 1  Algoritmo 2  Algoritmo 3
Promedio GAP (%)                64.43        25.25        45.82
Mediana GAP (%)                 55.37        20.91        30.69
Desv. Estándar                  57.89        35.35        41.94
Min GAP (%)                    -13.49       -28.99       -11.33
Max GAP (%)                    208.12        95.28       125.38
Instancias mejor que BKS         3.00        16.00         5.00
Instancias < 5% GAP              6.00        18.00         6.00
```

### Por Familia (ejemplos)
```
C1 (9 instancias):
  Algo 1: 79.29%, Algo 2: 33.18%, Algo 3: 107.34% → MEJOR: Algo2

R1 (12 instancias):
  Algo 1: 15.60%, Algo 2: -0.60%, Algo 3: 24.73% → MEJOR: Algo2

R2 (11 instancias):
  Algo 1: 44.74%, Algo 2: 25.90%, Algo 3: 11.95% → MEJOR: Algo3
```

---

## 🔍 Verificación de Funcionamiento

### ✅ QUICK Experiment (36 instancias)
- **Timestamp**: 03-01-2026 02:58:05
- **Duración total**: ~51 segundos
- **Gráficas generadas**: 5/5 ✅

### ✅ FULL Experiment (168 instancias)
- **Timestamp**: 03-01-2026 03:01:57
- **Duración total**: 4 minutos 22 segundos
- **Gráficas generadas**: 5/5 ✅

---

## 🎯 Flujo Automático Integrado

```
1. Usuario ejecuta: python scripts/experiments.py --mode [QUICK|FULL]
   ↓
2. Crea output/vrptw_experiments_[MODE]_[TIMESTAMP]/
   ↓
3. Ejecuta experimentos (36 o 168 instances)
   ↓
4. Guarda raw_results.csv en results/
   ↓
5. Genera visualizaciones canónicas (11 gráficas)
   ↓
6. ⭐ AUTOMÁTICO: Ejecuta plot_gap_comparison.py
   ├─ Busca CSV más reciente
   ├─ Genera 5 gráficas GAP
   └─ Guarda en plots/ del mismo experimento
   ↓
7. Genera resumen de resultados
   ↓
8. Finaliza e informa ubicación completa
```

---

## 🚀 Ventajas de la Automatización

| Aspecto | Antes | Ahora |
|--------|-------|-------|
| **Generación de gráficas** | Manual (correr script aparte) | Automática (integrada) |
| **Pérdida de datos** | Riesgo (olvidar ejecutar script) | 0% (garantizado) |
| **Rutas hardcoded** | Sí (frágil) | No (dinámicas) |
| **Soporte QUICK** | No | Sí ✅ |
| **Soporte FULL** | Sí | Sí ✅ |
| **Organización** | Gráficas dispersas | Todas en plots/ del experimento |
| **Rastreabilidad** | Difícil | Fácil (timestamp integrado) |

---

## 📝 Commits Relacionados

```
400a1d6 - Automatización: Generación de gráficas GAP en cada ejecución
41b53a3 - Documentación: ITER-4A/4B implementación completa
9ac8e19 - ITER-4B: Algoritmo 3 optimizado (strength 1.0→3.0, CRÍTICO)
166012c - ITER-4A: Algoritmo 1 optimizado (strength 2.0→3.5)
```

---

## ⚠️ Notas Importantes

1. **Encoding**: Se cambió de emojis Unicode a ASCII para compatibilidad con Windows cp1252
2. **Timeout**: plot_gap_comparison.py tiene timeout de 60 segundos
3. **Robustez**: Errores en generación de gráficas NO detienen experimento
4. **Idempotencia**: Script busca siempre el CSV más reciente (safe to re-run)

---

## 📞 Próximos Pasos

Para futuras iteraciones (ITER-4A/4B/5), las gráficas se generarán automáticamente:

```bash
cd projects/GAA-VRPTW-GRASP-2
python scripts/experiments.py --mode FULL  # Genera gráficas al final
# output/vrptw_experiments_FULL_DD-MM-YY_HH-MM-SS/plots/ → 5 gráficas GAP ✅
```

---

**Estado Final**: ✅ COMPLETADO Y OPERATIVO
**Fecha**: 3 de enero, 2026
